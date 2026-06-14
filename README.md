# Jarvis Agent

API REST de chatbot inteligente construída com FastAPI.

O Jarvis responde perguntas sobre documentos carregados, gerencia a agenda do usuário e auxilia no estudo utilizando busca híbrida (RAG), Active Recall, planejamento de estudos e recomendação de revisão.

---

## Estrutura de Pastas

```text
jarvis-agent/
├── main.py                          # Entrada da aplicação
├── requirements.txt
├── README.md

├── app/
│   ├── models/
│   │   └── schemas.py               # Schemas Pydantic
│
│   ├── routers/
│   │   └── chatbot.py               # Endpoints HTTP
│
│   └── services/
│       ├── chatbot_service.py       # Orquestração principal
│       ├── tool_caller.py           # Classificação e roteamento
│       ├── rag_manager.py           # Busca híbrida e recuperação
│       ├── agenda_tools.py          # Agenda + estudo + recall
│       ├── agenda_service.py        # CRUD da agenda
│       ├── recall_service.py        # Histórico de estudo
│       ├── logs_service.py          # Persistência de logs
│       └── tools.py                 # Definições auxiliares

└── infrastructure/
    ├── documents/                   # Arquivos carregados
    ├── database/                    # Banco SQLite
    ├── cache/                       # Cache de embeddings
    └── markdowns/                   # Conversão para markdown
```

---

# Como Funciona a Geração de Resposta

Toda pergunta recebida via `POST /api/ask` passa pelo fluxo abaixo.

---

## 1. Classificação da Intenção

O LLM classifica automaticamente a pergunta.

Tipos disponíveis:

* `consultar_agenda`
* `listar_tarefas`
* `adicionar_tarefa`
* `concluir_tarefa`
* `buscar_material_rag`
* `priorizar_hoje`
* `montar_plano_estudos`
* `gerar_perguntas_recall`
* `avaliar_resposta_recall`
* `recomendar_revisao`

Fluxo:

```text
Pergunta
↓

Classificador
↓

Ferramenta
```

---

## 2. Recuperação de Contexto

### Se Agenda

Busca compromissos relevantes.

Informações consideradas:

* data
* horário
* status
* proximidade

---

### Se Documentos (RAG)

Executa busca híbrida.

Estratégia:

```text
BM25
+

Embeddings
```

Parâmetros atuais:

```text
metodo = hibrido
k = 8
alpha = 0.45
```

Objetivos:

* melhorar recuperação de siglas
* reduzir perda de contexto
* aumentar cobertura

---

## 3. Validação do Contexto

Após recuperar documentos, o sistema valida se existe informação suficiente.

Importante:

**A decisão NÃO usa o texto produzido pela IA.**

Não existe tratamento como:

```text
if resposta contém:
"não encontrei"
```

A validação utiliza apenas dados objetivos da recuperação.

Sinais considerados:

```text
Quantidade de chunks
Cobertura do contexto
Diversidade dos documentos
```

Exemplo:

```text
chunks >= 5
→ confiança alta

chunks entre 2–4
→ confiança média

chunks <= 1
→ confiança baixa
```

---

## 4. Controle de Confiança

Fluxo:

```text
Pergunta
↓

Busca RAG
↓

Validação

↓

ALTA
→ responder

↓

MÉDIA
→ responder com limites

↓

BAIXA
→ informar falta de contexto
```

Exemplo:

Entrada:

```text
Explique plano inclinado
```

Saída:

```text
Não encontrei informação suficiente
nos materiais carregados para responder
com confiança.
```

Objetivo:

* evitar alucinação
* evitar respostas inventadas
* manter precisão do sistema

---

## 5. Plano de Estudos

Planejamento atualizado.

Reconhece:

* hoje
* amanhã
* esta semana
* próxima prova
* revisão final

Regras:

* respeitar prazo
* não criar dias extras
* considerar agenda
* funcionar sem documentos

Exemplo:

Entrada:

```text
Monte um plano para prova amanhã
```

Saída:

```text
Plano condensado para 1 dia
```

---

## 6. Active Recall

Fluxo:

```text
Tema
↓

Busca
↓

Validação
↓

Perguntas
↓

Correção
↓

Recomendação
```

Regras:

* perguntas apenas do tema solicitado
* não misturar documentos
* evitar contexto incorreto
* funcionar sem material quando permitido

---

## 7. Recomendação de Revisão

Pontuação:

```text
incorreta = +3
parcial = +1
correta = +0
```

Resultado:

```text
Prioridade 1
↓

Prioridade 2
↓

Prioridade 3
```

Objetivo:

* revisar dificuldades reais
* evitar peso igual para erros diferentes

---

## 8. Logs

Todas as execuções são registradas.

Formato:

```json
{
  "pergunta":"...",
  "resposta":"...",
  "tool":"..."
}
```

Armazenamento:

```text
UTF-8
JSON serializado
```

---

# Melhorias Implementadas

## RAG

* busca híbrida otimizada
* recuperação melhor para siglas
* validação por recuperação
* controle de confiança

## Agenda

* priorização real para hoje
* integração com materiais

## Plano

* respeito ao prazo
* funciona sem documentos

## Recall

* isolamento por tema
* redução de mistura de contexto

## Revisão

* score baseado em desempenho

## Logs

* persistência estruturada

---

# Benchmark

Métricas acompanhadas:

* qualidade RAG
* cobertura de contexto
* aderência temporal
* priorização
* Active Recall
* precisão de revisão
* geração de plano

---

# Instalação e Execução

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

python main.py
```

API:

```text
http://localhost:8000
```

Documentação:

```text
http://localhost:8000/docs
```

---

# Endpoints

| Método | Rota                        | Descrição                |
| ------ | --------------------------- | ------------------------ |
| POST   | `/api/ask`                  | Envia pergunta ao Jarvis |
| POST   | `/api/files/upload`         | Upload de documentos     |
| GET    | `/api/files`                | Lista arquivos           |
| GET    | `/stats`                    | Estatísticas do RAG      |
| GET    | `/api/agenda`               | Lista compromissos       |
| POST   | `/api/agenda`               | Cria compromisso         |
| PATCH  | `/api/agenda/{id}/concluir` | Conclui compromisso      |
| DELETE | `/api/agenda/{id}`          | Remove compromisso       |
