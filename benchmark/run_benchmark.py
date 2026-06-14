import sys
import asyncio
import csv
import json
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Garante que a raiz do projeto está no sys.path,
# permitindo imports como 'from app.services...' ao rodar de dentro de benchmark/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.chatbot_service import ChatbotService

# Carregar env
load_dotenv()

async def evaluate_answer(rag_manager, question: str, answer: str, criteria: str, keywords: str) -> dict:
    prompt = (
        "Você é um avaliador independente de sistemas de IA (RAG e Chatbot).\n"
        "Avalie a resposta gerada pelo sistema para a pergunta abaixo.\n\n"
        f"Pergunta: {question}\n"
        f"Resposta da IA: {answer}\n"
        f"Critério de Avaliação: {criteria}\n"
        f"Palavras-chave esperadas: {keywords}\n\n"
        "Responda APENAS com um JSON no formato exato:\n"
        '{"nota": 0|1|2, "justificativa": "... explicação curta ...", "palavras_chave_encontradas": ["...", "..."]}\n'
        "Onde:\n"
        "- nota 2: Resposta correta e completa, atendendo a todos os critérios e contendo a maioria das palavras-chave relevantes.\n"
        "- nota 1: Resposta parcial (ex: atendeu a alguns critérios, mas falhou em outros ou foi incompleta).\n"
        "- nota 0: Resposta incorreta ou alucinação (não atendeu ao critério ou errou completamente)."
    )
    try:
        raw_eval = rag_manager.get_response(prompt)
        match = re.search(r'\{[^{}]*"nota"[^{}]*\}', raw_eval, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        # Fallback parsing
        clean = raw_eval.strip()
        if clean.startswith("```json"):
            clean = clean.split("```json")[1].split("```")[0].strip()
        elif clean.startswith("```"):
            clean = clean.split("```")[1].split("```")[0].strip()
        return json.loads(clean)
    except Exception as e:
        print(f"⚠️ Erro ao avaliar resposta: {e}")
        return {"nota": 0, "justificativa": f"Erro de avaliação: {str(e)}", "palavras_chave_encontradas": []}

async def main():
    print("🚀 Iniciando Benchmark do Jarvis AI Agent...")
    
    # Inicializar ChatbotService e carregar documentos
    chatbot_service = ChatbotService()
    print("📚 Carregando documentos do RAG (Warmup)...")
    await chatbot_service.warmup()
    print("✅ RAG carregado!")
    
    questions_file = Path(__file__).parent / "benchmark_questions.csv"
    run_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    curr_dir = Path(__file__).parent / f"benchmark_{run_timestamp}"
    curr_dir.mkdir(parents=True, exist_ok=True)
    results_file = curr_dir / f"benchmark_results_{run_timestamp}.csv"
    report_file = curr_dir / f"benchmark_report_{run_timestamp}.md"
    
    if not questions_file.exists():
        print(f"❌ Arquivo {questions_file} não encontrado!")
        return

    # Lendo perguntas do CSV
    rows = []
    with open(questions_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
            
    print(f"📋 Encontradas {len(rows)} perguntas para rodar no benchmark.")
    
    results = []
    
    for row in rows:
        qid = row["id"]
        tipo = row["tipo_pergunta"]
        question = row["pergunta"]
        criteria = row["criterio_avaliacao"]
        keywords = row["gabarito_ou_palavras_chave"]
        
        print(f"\n==================================================")
        print(f"▶️ Executando [{qid}] ({tipo}): '{question}'")
        
        # Processar pergunta
        result_dict = await chatbot_service.process_question(question)
        answer = result_dict.get("answer", "")
        chunks = result_dict.get("chunks_usados", 0)
        
        print(f"💬 Resposta da IA ({chunks} chunks):")
        print(answer[:200] + "..." if len(answer) > 200 else answer)
        
        # Avaliar resposta usando a IA
        print("🧠 Avaliando resposta...")
        evaluation = await evaluate_answer(chatbot_service.rag_manager, question, answer, criteria, keywords)
        nota = evaluation.get("nota", 0)
        justificativa = evaluation.get("justificativa", "Sem justificativa.")
        encontradas = evaluation.get("palavras_chave_encontradas", [])
        
        print(f"⭐ Nota: {nota}/2 | {justificativa}")
        
        results.append({
            "id": qid,
            "tipo_pergunta": tipo,
            "pergunta": question,
            "resposta_ia": answer,
            "chunks_usados": chunks,
            "nota": nota,
            "justificativa": justificativa,
            "palavras_chave_encontradas": ", ".join(encontradas)
        })
        
    # Salvar resultados no CSV
    with open(results_file, mode='w', encoding='utf-8', newline='') as f:
        fieldnames = ["id", "tipo_pergunta", "pergunta", "resposta_ia", "chunks_usados", "nota", "justificativa", "palavras_chave_encontradas"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"\n✅ Resultados salvos em: {results_file}")
    
    # Gerar relatório em Markdown
    total_score = sum(r["nota"] for r in results)
    max_score = len(results) * 2
    percentage = (total_score / max_score) * 100
    
    nota_2_count = sum(1 for r in results if r["nota"] == 2)
    nota_1_count = sum(1 for r in results if r["nota"] == 1)
    nota_0_count = sum(1 for r in results if r["nota"] == 0)
    
    md_content = f"""# Relatório de Benchmark - Jarvis AI Agent

**Data**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Score Total**: {total_score}/{max_score} ({percentage:.1f}%)
**Distribuição de Notas**:
- **Corretas/Completas (Nota 2)**: {nota_2_count} / {len(results)}
- **Parciais (Nota 1)**: {nota_1_count} / {len(results)}
- **Incorretas/Erros (Nota 0)**: {nota_0_count} / {len(results)}

## Tabela de Resultados

| ID | Tipo | Pergunta | Chunks | Nota | Justificativa |
|---|---|---|---|---|---|
"""
    for r in results:
        # Escapar caracteres especiais para tabela markdown
        p_esc = r["pergunta"].replace("|", "\\|")
        j_esc = r["justificativa"].replace("|", "\\|")
        md_content += f"| {r['id']} | {r['tipo_pergunta']} | {p_esc} | {r['chunks_usados']} | **{r['nota']}/2** | {j_esc} |\n"
        
    report_file.write_text(md_content, encoding='utf-8')
    print(f"✅ Relatório formatado salvo em: {report_file}")
    print("🎉 Benchmark concluído com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
