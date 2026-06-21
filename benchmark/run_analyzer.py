import os
import sys
import csv
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Permite imports da raiz se necessário no fluxo do projeto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Carrega as variáveis de ambiente (.env na raiz do projeto)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def list_benchmark_runs(benchmark_dir: Path) -> list:
    """Lista todas as pastas de benchmark que contêm arquivos de resultados CSV."""
    runs = []
    if not benchmark_dir.exists():
        return runs
    
    for item in benchmark_dir.iterdir():
        if item.is_dir() and item.name.startswith("benchmark_"):
            results_csvs = list(item.glob("benchmark_results_*.csv"))
            if results_csvs:
                runs.append({
                    "folder": item,
                    "csv_path": results_csvs[0]
                })
    # Ordena para mostrar os mais recentes primeiro
    runs.sort(key=lambda r: r["folder"].name, reverse=True)
    return runs

def load_questions_metadata(benchmark_dir: Path) -> dict:
    """Lê o arquivo benchmark_questions.csv na pasta benchmark para cruzar informações de critérios e palavras-chave."""
    metadata = {}
    questions_file = benchmark_dir / "benchmark_questions.csv"
    if not questions_file.exists():
        print(f"⚠️  Aviso: Arquivo de perguntas gabarito '{questions_file.name}' não encontrado.")
        return metadata

    try:
        with open(questions_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qid = row.get("id")
                if qid:
                    metadata[str(qid)] = {
                        "criterio_avaliacao": row.get("criterio_avaliacao", "Não especificado"),
                        "gabarito_ou_palavras_chave": row.get("gabarito_ou_palavras_chave", "Não especificado")
                    }
    except Exception as e:
        print(f"⚠️  Erro ao carregar metadados das perguntas: {e}")
    return metadata

def parse_llm_json(raw_text: str) -> dict:
    """Tenta parsear a resposta do modelo como JSON, com fallbacks robustos."""
    # Tenta extrair JSON delimitado por ```json ... ```
    match_json = re.search(r'```json\s*(.*?)\s*```', raw_text, re.DOTALL)
    if match_json:
        try:
            return json.loads(match_json.group(1).strip())
        except Exception:
            pass

    # Tenta extrair qualquer coisa entre { e }
    match_curly = re.search(r'(\{.*\})', raw_text, re.DOTALL)
    if match_curly:
        try:
            return json.loads(match_curly.group(1).strip())
        except Exception:
            pass

    # Tenta decodificar o texto bruto diretamente
    try:
        return json.loads(raw_text.strip())
    except Exception:
        pass

    # Fallback se falhar completamente, para não interromper a execução do script
    print("⚠️  Não foi possível decodificar a resposta da IA em formato JSON. Usando fallback estruturado.")
    return {
        "analise_geral": "Erro de processamento da resposta da IA. Veja o texto original.",
        "falhas": [
            {
                "tipo": "Erro de Formatação",
                "causa": "O modelo de linguagem não respondeu no formato JSON solicitado.",
                "possivel_solucao": "Verificar a conexão com a API ou ajustar a temperatura/prompt."
            },
            {
                "tipo": "Indeterminado",
                "causa": f"Retorno bruto do modelo: {raw_text[:100]}...",
                "possivel_solucao": "Reexecutar a análise para este caso de teste."
            },
            {
                "tipo": "Verificação Manual",
                "causa": "Ocorreu uma falha no parser de JSON interno do script.",
                "possivel_solucao": "Analisar a resposta da IA manualmente no arquivo CSV original."
            }
        ]
    }

def analyze_error_with_llm(client: OpenAI, case: dict) -> dict:
    """Solicita à IA a análise detalhada do erro com base nas informações fornecidas."""
    prompt = (
        "Você é um analista de qualidade de sistemas de IA especialista em RAG (Retrieval-Augmented Generation) e Agentes de IA.\n"
        "Seu objetivo é analisar um erro (resposta parcial ou incorreta) ocorrido durante um teste de benchmark e identificar pelo menos 3 falhas específicas no comportamento do agente.\n\n"
        "Dados do Caso:\n"
        f"- ID da Pergunta: {case['id']}\n"
        f"- Pergunta do Usuário: {case['pergunta']}\n"
        f"- Tipo de Pergunta: {case['tipo_pergunta']}\n"
        f"- Critério de Avaliação Esperado: {case['criterio_avaliacao']}\n"
        f"- Gabarito/Palavras-chave Esperadas: {case['gabarito_ou_palavras_chave']}\n"
        f"- Resposta Gerada pela IA: {case['resposta_ia']}\n"
        f"- Chunks Recuperados (RAG): {case['chunks_usados']}\n"
        f"- Nota Atribuída: {case['nota']}/2\n"
        f"- Justificativa do Avaliador: {case['justificativa']}\n"
        f"- Palavras-chave Encontradas: {case['palavras_chave_encontradas']}\n\n"
        "Sua tarefa é analisar criticamente a resposta da IA e identificar pelo menos 3 falhas distintas no fluxo de execução do agente.\n"
        "Caso o erro seja simples (ex: resposta apenas incompleta), divida a análise em 3 aspectos diferentes do ciclo de vida da requisição (ex: falha na recuperação RAG, falha na geração/estilo da resposta, e falha na cobertura dos critérios de avaliação).\n\n"
        "Para cada uma das falhas (mínimo de 3), identifique:\n"
        "1. Tipo da Falha (use obrigatoriamente termos como: recuperação, geração, alucinação, formatação, contexto_insuficiente, ambiguidade, instrução_ignorada, etc.)\n"
        "2. Causa da Falha (uma explicação técnica e clara de por que a falha ocorreu)\n"
        "3. Possível Solução (uma recomendação acionável e técnica para corrigir a falha)\n\n"
        "Responda APENAS com um objeto JSON no formato abaixo, sem nenhum outro caractere ou explicação fora dele:\n"
        "{\n"
        '  "analise_geral": "descrição resumida do erro principal",\n'
        '  "falhas": [\n'
        "    {\n"
        '      "tipo": "tipo_da_falha_1",\n'
        '      "causa": "causa_da_falha_1",\n'
        '      "possivel_solucao": "possível_solução_para_a_falha_1"\n'
        "    },\n"
        "    {\n"
        '      "tipo": "tipo_da_falha_2",\n'
        '      "causa": "causa_da_falha_2",\n'
        '      "possivel_solucao": "possível_solução_para_a_falha_2"\n'
        "    },\n"
        "    {\n"
        '      "tipo": "tipo_da_falha_3",\n'
        '      "causa": "causa_da_falha_3",\n'
        '      "possivel_solucao": "possível_solução_para_a_falha_3"\n'
        "    }\n"
        '  ]\n'
        "}\n"
    )

    try:
        response = client.chat.completions.create(
            model='Qwen/Qwen2.5-14B-Instruct-AWQ',
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        raw_text = response.choices[0].message.content
        parsed = parse_llm_json(raw_text)
        
        # Garante que temos pelo menos 3 falhas, caso o modelo retorne menos
        while len(parsed.get("falhas", [])) < 3:
            if "falhas" not in parsed:
                parsed["falhas"] = []
            index = len(parsed["falhas"]) + 1
            parsed["falhas"].append({
                "tipo": "Alinhamento & Validação",
                "causa": f"Falha secundária de cobertura ({index}): A resposta não atendeu integralmente aos critérios especificados.",
                "possivel_solucao": "Implementar etapa de auto-correção / crítico interno antes de finalizar a resposta do agente."
            })
            
        return parsed
    except Exception as e:
        print(f"❌ Erro ao consultar API da OpenAI para o caso {case['id']}: {e}")
        return {
            "analise_geral": f"Falha na comunicação com a API: {str(e)}",
            "falhas": [
                {
                    "tipo": "API Error",
                    "causa": "Ocorreu um erro ao chamar o modelo de linguagem.",
                    "possivel_solucao": "Verifique a chave da API e a conectividade com o host."
                },
                {
                    "tipo": "Indeterminado",
                    "causa": "Não foi possível obter resposta para esta análise.",
                    "possivel_solucao": "Reexecutar o script."
                },
                {
                    "tipo": "Verificação Manual",
                    "causa": "Conexão interrompida.",
                    "possivel_solucao": "Inspecionar os logs do sistema."
                }
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="Analisador de Erros de Benchmark do Jarvis")
    parser.add_argument("--folder", "-f", type=str, help="Nome ou caminho da pasta de benchmark (ex: benchmark_20260614_133220)")
    parser.add_argument("--threshold", "-t", type=int, default=1, choices=[0, 1], 
                        help="Critério de erro: 1 = Notas 0 e 1 (padrão); 0 = Apenas nota 0")
    args = parser.parse_args()

    benchmark_dir = Path(__file__).resolve().parent
    
    # 1. Obter e listar os benchmarks disponíveis
    runs = list_benchmark_runs(benchmark_dir)
    
    if not runs:
        print("❌ Nenhuma pasta de execução de benchmark encontrada (padrão 'benchmark_*').")
        print("Certifique-se de executar o benchmark primeiro usando 'python run_benchmark.py'.")
        sys.exit(1)
        
    selected_run = None
    
    if args.folder:
        # Tenta achar a pasta especificada
        for r in runs:
            if r["folder"].name == args.folder or str(r["folder"].resolve()) == str(Path(args.folder).resolve()):
                selected_run = r
                break
        if not selected_run:
            print(f"❌ Pasta de benchmark '{args.folder}' não foi encontrada ou não possui resultados válidos.")
            sys.exit(1)
    else:
        # Prompt interativo para escolha da pasta
        print("\n=======================================================")
        print("🔍 ANALISADOR DE ERROS DE BENCHMARK - SELEÇÃO DE PASTA")
        print("=======================================================\n")
        print("Selecione a execução do benchmark que deseja analisar:")
        for idx, r in enumerate(runs, 1):
            print(f"[{idx}] {r['folder'].name}")
            
        try:
            choice = input(f"\nEscolha uma opção (1-{len(runs)}): ").strip()
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(runs):
                raise ValueError()
            selected_run = runs[choice_idx]
        except (ValueError, IndexError, KeyboardInterrupt):
            print("\n❌ Seleção inválida ou cancelada pelo usuário. Encerrando.")
            sys.exit(1)
            
    # Configurar pasta de destino para relatórios
    reports_dir = benchmark_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    target_folder = selected_run["folder"]
    csv_path = selected_run["csv_path"]
    
    print(f"\n📂 Pasta selecionada: {target_folder.name}")
    print(f"📄 Resultados em: {csv_path.name}")
    
    # Carregar metadados dos gabaritos/critérios
    questions_meta = load_questions_metadata(benchmark_dir)
    
    # Iniciar cliente OpenAI
    print("🧠 Inicializando cliente OpenAI...")
    try:
        client = OpenAI()
    except Exception as e:
        print(f"❌ Erro ao instanciar o cliente OpenAI: {e}")
        sys.exit(1)
        
    # Ler e filtrar resultados com erros baseados no critério objetivo
    cases = []
    total_cases = 0
    errors_count = 0
    
    print("📊 Lendo resultados do CSV...")
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_cases += 1
            try:
                nota = int(row.get("nota", 2))
            except ValueError:
                nota = 2
                
            # Critério objetivo de erro: nota < 2 (se threshold for 1) ou nota == 0 (se threshold for 0)
            is_error = False
            if args.threshold == 1 and nota < 2:
                is_error = True
            elif args.threshold == 0 and nota == 0:
                is_error = True
                
            if is_error:
                errors_count += 1
                qid = row.get("id")
                meta = questions_meta.get(str(qid), {
                    "criterio_avaliacao": "Não disponível no benchmark_questions.csv",
                    "gabarito_ou_palavras_chave": "Não disponível no benchmark_questions.csv"
                })
                
                cases.append({
                    "id": qid,
                    "tipo_pergunta": row.get("tipo_pergunta", "Desconhecido"),
                    "pergunta": row.get("pergunta", ""),
                    "resposta_ia": row.get("resposta_ia", ""),
                    "chunks_usados": row.get("chunks_usados", "0"),
                    "nota": nota,
                    "justificativa": row.get("justificativa", ""),
                    "palavras_chave_encontradas": row.get("palavras_chave_encontradas", ""),
                    "criterio_avaliacao": meta["criterio_avaliacao"],
                    "gabarito_ou_palavras_chave": meta["gabarito_ou_palavras_chave"]
                })
                
    print(f"🔍 Total de casos no benchmark: {total_cases}")
    print(f"❌ Casos com erros identificados (Nota <= {args.threshold}): {errors_count}")
    
    if errors_count == 0:
        print("\n🎉 Nenhum erro encontrado neste benchmark com base nos critérios estabelecidos! Todas as respostas atingiram a nota esperada.")
        # Gerar relatório mesmo sem erros
        report_filename = f"error_analyze_{target_folder.name}.md"
        report_path = reports_dir / report_filename
        
        md_content = f"""# Relatório de Análise de Erros (Error Analyze)

**Data da Análise**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Benchmark Analisado**: `{target_folder.name}`
**Total de Casos Analisados**: {total_cases}
**Total de Erros Encontrados (Nota <= {args.threshold})**: 0

> [!NOTE]
> Parabéns! Nenhuma falha foi encontrada de acordo com o critério estabelecido (Nota <= {args.threshold}). Todas as respostas obtiveram a nota máxima ou satisfatória.
"""
        report_path.write_text(md_content, encoding='utf-8')
        print(f"📝 Relatório gerado em: [reports/{report_filename}](file://{report_path})")
        return

    # Iniciar análise detalhada
    print("\n⚡ Iniciando a análise dos erros com a IA...")
    analyzed_cases = []
    failure_type_distribution = {}
    
    for idx, case in enumerate(cases, 1):
        print(f"🔄 Analisando erro {idx}/{errors_count} - ID {case['id']} | Pergunta: '{case['pergunta'][:40]}...'")
        analysis = analyze_error_with_llm(client, case)
        
        case["analise"] = analysis
        analyzed_cases.append(case)
        
        # Coletar estatísticas das falhas
        for falha in analysis.get("falhas", []):
            tipo = falha.get("tipo", "Outro").capitalize()
            failure_type_distribution[tipo] = failure_type_distribution.get(tipo, 0) + 1
            
    # Gerar Relatório Markdown
    print("\n✍️  Gerando relatório consolidado...")
    report_filename = f"error_analyze_{target_folder.name}.md"
    report_path = reports_dir / report_filename
    
    md_content = f"""# Relatório de Análise de Erros (Error Analyze)

**Data da Análise**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Benchmark Analisado**: `{target_folder.name}`
**Total de Casos Analisados**: {total_cases}
**Total de Erros Encontrados (Nota <= {args.threshold})**: {errors_count}

---

## 📊 Distribuição dos Tipos de Falhas
Abaixo estão os principais gargalos identificados pela IA ao longo das análises:

"""
    # Adicionar estatísticas de falhas
    for f_type, count in sorted(failure_type_distribution.items(), key=lambda x: x[1], reverse=True):
        md_content += f"- **{f_type}**: {count} ocorrências\n"
        
    md_content += """
---

## 📋 Resumo dos Casos com Erros

| ID | Tipo | Pergunta | Chunks | Nota | Justificativa do Erro |
|---|---|---|---|---|---|
"""
    for case in analyzed_cases:
        p_esc = case["pergunta"].replace("|", "\\|")
        analise_resumida = case["analise"].get("analise_geral", "Sem análise disponível.").replace("|", "\\|")
        md_content += f"| {case['id']} | {case['tipo_pergunta']} | {p_esc} | {case['chunks_usados']} | **{case['nota']}/2** | {analise_resumida} |\n"

    md_content += "\n---\n\n## 🔍 Análise Detalhada por Caso\n"
    
    for idx, case in enumerate(analyzed_cases, 1):
        md_content += f"""### ❌ Caso {case['id']} - {case['tipo_pergunta']}
**Pergunta**: {case['pergunta']}

**Critério de Avaliação Esperado**:
> {case['criterio_avaliacao']}

**Gabarito / Palavras-chave**:
`{case['gabarito_ou_palavras_chave']}`

**Resposta Gerada pela IA**:
```text
{case['resposta_ia']}
```

**Nota**: **{case['nota']}/2**
**Justificativa Original**: {case['justificativa']}
**Palavras-chave Encontradas**: `{case['palavras_chave_encontradas']}`

#### 🛠️ Falhas e Planos de Ação Identificados (Mínimo de 3)

"""
        for f_idx, falha in enumerate(case["analise"].get("falhas", []), 1):
            md_content += f"""##### {f_idx}. Falha de **{falha.get('tipo', 'Outro')}**
- **Causa**: {falha.get('causa', 'Não descrita')}
- **Possível Solução**: {falha.get('possivel_solucao', 'Não descrita')}

"""
        md_content += "---\n\n"
        
    report_path.write_text(md_content, encoding='utf-8')
    
    print("\n=======================================================")
    print("🎉 ANÁLISE DE BENCHMARK CONCLUÍDA COM SUCESSO!")
    print("=======================================================")
    print(f"📊 Total de falhas identificadas: {sum(failure_type_distribution.values())}")
    print(f"📝 Relatório gerado com sucesso em:")
    print(f"👉 [error_analyze_{target_folder.name}.md](file://{report_path})")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
