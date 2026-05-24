# Jarvis Chatbot API

Uma API REST para um chatbot inteligente com RAG (Retrieval-Augmented Generation) construída com FastAPI.

## Características

- 🤖 **RAG (Retrieval-Augmented Generation)**: Respostas baseadas em documentos relevantes
- 📚 **Processamento de Documentos**: Suporte para .txt e .pdf
- 🔍 **Recuperação Híbrida**: Combinação de BM25 + Embeddings densos
- 🧠 **Embeddings**: Gerados automaticamente com `sentence-transformers`
- 🚀 **Warmup Automático**: Carrega documentos ao iniciar a aplicação
- 📊 **Estatísticas**: Endpoint para monitorar o estado do RAG

## Estrutura do Projeto

```
jarvis-agent/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              # Schemas Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   └── chatbot.py              # Controllers/Endpoints
│   └── services/
│       ├── __init__.py
│       ├── chatbot_service.py      # Orquestração do chatbot
│       └── rag_manager.py          # Gerenciador RAG
├── documents/                       # Pasta de documentos (criada automaticamente)
├── main.py                          # Arquivo principal com warmup
├── requirements.txt                 # Dependências do projeto
├── .env.example                     # Exemplo de variáveis de ambiente
└── README.md                        # Este arquivo
```

## Instalação

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Editar .env e adicionar sua OPENAI_API_KEY
```

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar a aplicação

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Health Check

- `GET /` - Verifica se a API está rodando
- `GET /health` - Health check da API
- `GET /stats` - Estatísticas do RAG (chunks carregados, documentos, etc)

### Chatbot com RAG

- `POST /api/ask` - Envia uma pergunta ao chatbot
  - Request: `{"question": "sua pergunta", "context": "contexto opcional"}`
  - Response: `{"answer": "resposta", "confidence": 0.85}`

- `POST /api/files/upload` - Faz upload de um arquivo
  - Suporta: .txt, .pdf
  - Os arquivos são salvos em `documents/` e adicionados automaticamente ao RAG
  - Response: `{"filename": "nome.pdf", "size": 1024, "message": "..."}`

- `GET /api/files` - Lista todos os documentos
  - Response: `{"total": 2, "files": [{"filename": "doc1.pdf", "size": 1024, "created_at": "2024-01-01T10:00:00"}]}`

## Como Funciona o RAG

### 1. **Upload de Documento**

Quando você faz upload de um arquivo via `POST /api/files/upload`:

- O arquivo é salvo em `documents/`
- É dividido em chunks (pedaços) automáticamente
- Embeddings são gerados para cada chunk
- Um índice BM25 é criado para busca lexical

### 2. **Processamento de Pergunta**

Quando você faz uma pergunta via `POST /api/ask`:

- A pergunta é comparada com os chunks usando BM25 (busca lexical)
- A pergunta é comparada com os chunks usando embeddings densos (busca semântica)
- Os resultados são combinados usando uma abordagem híbrida
- Os chunks mais relevantes são selecionados
- Um prompt é montado com o contexto dos chunks
- O LLM (Gemma) gera uma resposta baseada apenas no contexto fornecido

### 3. **Warmup**

Ao iniciar a aplicação:

- Todos os documentos da pasta `documents/` são carregados automaticamente
- Chunks e embeddings são regenerados
- O sistema fica pronto para responder perguntas

## Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│   FastAPI Routers (Controllers)      │ ← Recebe requisições HTTP
├─────────────────────────────────────┤
│   ChatbotService (Orquestração)      │ ← Coordena RAG e I/O
├─────────────────────────────────────┤
│   RAGManager (Lógica de Negócio)     │ ← Embeddings, BM25, LLM
├─────────────────────────────────────┤
│   Dependências Externas              │ ← OpenAI, Sentence-Transformers
└─────────────────────────────────────┘
```

- **Routers**: Camada de apresentação
- **ChatbotService**: Orquestração e persistência
- **RAGManager**: Lógica de RAG
- **Models/Schemas**: Definição de estruturas de dados

## Configuração de Chunking

Por padrão, os documentos são divididos em chunks de 500 caracteres com 50 caracteres de sobreposição. Para customizar, edite em `rag_manager.py`:

```python
self.chunk_size = 500      # Tamanho de cada chunk
self.chunk_overlap = 50    # Sobreposição entre chunks
```

## Métodos de Recuperação

O RAG suporta 3 métodos de recuperação (configurável na chamada do LLM):

1. **BM25**: Busca lexical (palavras-chave)
2. **Dense**: Busca semântica (embeddings)
3. **Híbrido**: Combinação dos dois (padrão)
