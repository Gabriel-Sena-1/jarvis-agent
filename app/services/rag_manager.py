import json
import os
from pathlib import Path
from typing import Optional
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss


class RAGManager:
    _instance: "RAGManager | None" = None

    @classmethod
    def get_instance(cls) -> "RAGManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.client = OpenAI(base_url='https://llm.liaufms.org/v1/gemma-3-12b-it', api_key=os.getenv("OPENAI_API_KEY"))
        
        print("Carregando modelo de embeddings multilingual...")
        self.embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        
        self.chunks = []
        self.embeddings = None
        self.faiss_index = None
        self.bm25_model = None
        self.tokenized_chunks = []
        
        self.chunk_size = 500
        self.chunk_overlap = 100
        
        self.markdowns_folder = Path(__file__).parent.parent.parent / "infrastructure" / "markdowns"
        self.markdowns_folder.mkdir(exist_ok=True)

        self.cache_folder = Path(__file__).parent.parent.parent / "infrastructure" / "cache"
        self.cache_folder.mkdir(exist_ok=True)

        # Rastreia quais chaves de cache já estão carregados: {cache_key: True}
        self._chunks_carregados: dict[str, bool] = {}
    
    def chunking_janela(self, texto: str) -> list[str]:
        chunks = []
        passo = self.chunk_size - self.chunk_overlap
        inicio = 0
        while inicio < len(texto):
            fim = inicio + self.chunk_size
            chunks.append(texto[inicio:fim])
            inicio += passo
        return chunks
    
    def _cache_key(self, nome_documento: str, timestamp: int) -> str:
        return f"{nome_documento}_{timestamp}"

    def _cache_path(self, cache_key: str) -> Path:
        return self.cache_folder / f"{cache_key}.json"

    def carregar_documento_texto(
        self,
        texto: str,
        nome_documento: str = "documento",
        timestamp: Optional[int] = None,
    ) -> int:
        ts = timestamp if timestamp is not None else int(os.path.getmtime(__file__))
        cache_key = self._cache_key(nome_documento, ts)

        if cache_key in self._chunks_carregados:
            print(f"Chunks de '{nome_documento}' já carregados nesta sessão (cache_key={cache_key}).")
            return 0

        cache_path = self._cache_path(cache_key)
        if cache_path.exists():
            print(f"Carregando chunks do cache: {cache_path}")
            novos_chunks = json.loads(cache_path.read_text(encoding="utf-8"))
        else:
            novos_chunks = [
                {"texto": chunk, "documento": nome_documento}
                for chunk in self.chunking_janela(texto)
            ]
            cache_path.write_text(json.dumps(novos_chunks, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Chunks salvos no cache: {cache_path}")

        self.chunks.extend(novos_chunks)
        self._chunks_carregados[cache_key] = True
        self._atualizar_indices()
        return len(novos_chunks)
    
    def carregar_documento_pdf(self, arquivo_path: str) -> int:
        try:
            nome_arquivo = Path(arquivo_path).stem
            caminho_md = self.markdowns_folder / f"{nome_arquivo}.md"

            if caminho_md.exists():
                print(f"Reutilizando Markdown existente: {caminho_md}")
                texto_markdown = caminho_md.read_text(encoding="utf-8")
            else:
                from docling.document_converter import DocumentConverter
                print(f"Convertendo PDF para Markdown: {arquivo_path}")
                converter = DocumentConverter()
                resultado = converter.convert(arquivo_path)
                texto_markdown = resultado.document.export_to_markdown()
                caminho_md.write_text(texto_markdown, encoding="utf-8")
                print(f"Markdown salvo em: {caminho_md}")

            # Usa o mtime do arquivo original como timestamp
            timestamp = int(Path(arquivo_path).stat().st_mtime)
            return self.carregar_documento_texto(texto_markdown, nome_arquivo, timestamp=timestamp)
        except Exception as e:
            raise Exception(f"Erro ao carregar PDF: {str(e)}")
    
    def carregar_documento_arquivo(self, arquivo_path: str) -> int:
        ext = Path(arquivo_path).suffix.lower()
        
        if ext == '.pdf':
            return self.carregar_documento_pdf(arquivo_path)
        elif ext == '.txt':
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                texto = f.read()
            timestamp = int(Path(arquivo_path).stat().st_mtime)
            return self.carregar_documento_texto(texto, Path(arquivo_path).stem, timestamp=timestamp)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {ext}")
    
    def _atualizar_indices(self):
        if len(self.chunks) == 0:
            self.embeddings = None
            self.faiss_index = None
            self.bm25_model = None
            self.tokenized_chunks = []
            return
        
        print(f"Gerando embeddings para {len(self.chunks)} chunks...")
        textos = [chunk["texto"] for chunk in self.chunks]
        
        self.embeddings = self.embedding_model.encode(
            textos,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")
        
        dim = self.embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dim)
        self.faiss_index.add(self.embeddings)
        
        print(f"Índice FAISS criado: {dim} dimensões, {self.faiss_index.ntotal} vetores")
        
        self.tokenized_chunks = [texto.lower().split() for texto in textos]
        self.bm25_model = BM25Okapi(self.tokenized_chunks)
    
    def recuperar_bm25(self, query: str, k: int = 3) -> list[dict]:
        if not self.bm25_model or not self.chunks:
            return []
        
        query_tokens = query.lower().split()
        scores = self.bm25_model.get_scores(query_tokens)
        top_k_idx = np.argsort(scores)[::-1][:k]
        
        resultado = []
        for idx in top_k_idx:
            if scores[idx] > 0:
                resultado.append(self.chunks[idx])
        
        return resultado
    
    def recuperar_dense(self, query: str, k: int = 3) -> list[dict]:
        if self.faiss_index is None or len(self.chunks) == 0:
            return []
        
        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True,
        ).astype("float32").reshape(1, -1)
        
        distances, indices = self.faiss_index.search(query_embedding, k)
        
        resultado = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx != -1 and distance > 0.1:
                resultado.append(self.chunks[idx])
        
        return resultado
    
    def recuperar_hibrido(self, query: str, k: int = 3, alpha: float = 0.6) -> list[dict]:
        if not self.chunks:
            return []
        
        bm25_results = self.recuperar_bm25(query, k * 2)
        dense_results = self.recuperar_dense(query, k * 2)
        
        if not bm25_results and not dense_results:
            return []
        
        combined = {}
        
        if bm25_results:
            for i, result in enumerate(bm25_results):
                texto = result["texto"]
                score = (1 - alpha) * (1 - i / max(len(bm25_results), 1))
                combined[texto] = combined.get(texto, 0) + score
        
        if dense_results:
            for i, result in enumerate(dense_results):
                texto = result["texto"]
                score = alpha * (1 - i / max(len(dense_results), 1))
                combined[texto] = combined.get(texto, 0) + score
        
        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:k]
        
        resultado = []
        for texto, _ in sorted_results:
            chunk = next((c for c in self.chunks if c["texto"] == texto), None)
            if chunk:
                resultado.append(chunk)
        
        return resultado
    
    def construir_prompt(self, pergunta: str, docs: list[dict]) -> str:
        partes = []

        if docs:
            trechos = "\n\n".join(
                [f"Trecho {i+1}:\n{d['texto']}" for i, d in enumerate(docs)]
            )
            partes.append(f"Contexto de documentos:\n{trechos}")

        contexto_completo = "\n\n".join(partes) if partes else ""

        instrucao = (
            "Responda em português usando as informações do contexto abaixo. "
            "Se não houver informação suficiente, diga: não encontrado no contexto.\n\n"
        )

        return instrucao + (f"Contexto:\n{contexto_completo}\n\n" if contexto_completo else "") + f"Pergunta: {pergunta}"
    
    def get_response(self, content):
        resp = self.client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=[{"role": "user", "content": content}],
        )
        return resp.choices[0].message.content

    async def responder_rag(
        self,
        pergunta: str,
        metodo: str = "hibrido",
        k: int = 3,
        alpha: float = 0.6,
    ) -> tuple[str, list[dict]]:
        print(f"Respondendo pergunta: {pergunta} (método: {metodo}, k={k}, alpha={alpha})")
        if metodo == "bm25":
            docs = self.recuperar_bm25(pergunta, k=k)
        elif metodo == "dense":
            docs = self.recuperar_dense(pergunta, k=k)
        else:
            docs = self.recuperar_hibrido(pergunta, k=k, alpha=alpha)

        print(f"Documentos recuperados: {len(docs)}")

        if not docs:
            return "Não há documentos no contexto para responder.", []

        conteudo = self.construir_prompt(pergunta, docs)

        resp = self.get_response(conteudo)

        return resp, docs
    
    def get_stats(self) -> dict:
        return {
            "total_chunks": len(self.chunks),
            "total_embeddings": self.embeddings.shape[0] if self.embeddings is not None else 0,
            "documentos": list(set([chunk["documento"] for chunk in self.chunks]))
        }
