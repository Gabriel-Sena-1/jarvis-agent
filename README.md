# Jarvis Agent

API REST de chatbot inteligente construída com FastAPI. Responde perguntas sobre documentos carregados, gerencia agenda do usuário e auxilia no estudo com geração de planos, Active Recall e recomendações personalizadas.

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
│       ├── rag_manager.py           # Busca híbrida + geração
│       ├── agenda_tools.py          # Agenda + estudo + recall
│       ├── agenda_service.py        # CRUD de compromissos
│       ├── recall_service.py        # Histórico de treino
│       ├── logs_service.py          # Persistência de logs
│       └── tools.py                 # Definições auxiliares

└── infrastructure/
    ├── documents/                   # Arquivos carregados
    ├── database/                    # Banco SQLite
    ├── cache/                       # Cache de embeddings
    └── markdowns/                   # Conversão de documentos
```

---

# Como Funciona a Geração de Resposta

Toda pergunta recebida via `POST /api/ask` passa pelo seguinte fluxo.

## 1. Classificação da intenção

O próprio LLM identifica automaticamente a intenção da pergunta.

Categorias disponíveis:

- `consultar_agenda`
    
- `listar_tarefas`
    
- `adicionar_tarefa`
    
- `concluir_tarefa`
    
- `buscar_material_rag`
    
- `priorizar_hoje`
    
- `montar_plano_estudos`
    
- `gerar_perguntas_recall`
    
- `avaliar_resposta_recall`
    
- `recomendar_revisao`
    

Fluxo:

```text
Pergunta
↓

LLM Classificador

↓

Tool adequada
```

---

## 2. Recuperação do Contexto

### Se for Agenda

Busca compromissos relevantes.

Informações utilizadas:

- nome
    
- data
    
- horário
    
- status
    
- proximidade temporal
    

Exemplo:

```text
Compromissos:

[id:12]
Prova APSOO
2026-06-15
Pendente
```

---

### Se for Documentos (RAG)

Executa busca híbrida.

Estratégia:

```text
BM25
+

Embeddings
```

Configuração:

```text
metodo = hibrido
k = 8
alpha = 0.45
```

Objetivos:

- melhorar recuperação de siglas
    
- reduzir perda de contexto
    
- aumentar cobertura
    

---

## 3. Validação do Contexto

Antes de responder, o sistema verifica se o contexto recuperado é confiável.

Critérios:

```text
chunks <= 1

OU

resposta contém:

não encontrado
não encontrei
não há informações
contexto fornecido
```

---

## 4. Sistema de Fallback

Se o contexto falhar:

ANTES:

```text
Não encontrado no contexto
```

AGORA:

```text
Responder usando conhecimento geral
```

Exemplo:

Entrada:

```text
Como funciona KNN?
```

Saída:

```text
Explicação completa do algoritmo
```

---

## 5. Plano de Estudos

Planejamento atualizado.

Detecta automaticamente:

- hoje
    
- amanhã
    
- esta semana
    
- próxima prova
    
- revisão final
    

Regras:

- respeitar prazo informado
    
- não criar dias extras
    
- considerar agenda
    
- funcionar sem documentos
    

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

Busca de documentos
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

- perguntas apenas do tema solicitado
    
- não misturar documentos
    
- evitar perguntas irrelevantes
    
- funcionar sem contexto quando necessário
    

---

## 7. Recomendação de Revisão

Sistema atualizado.

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

---

## 8. Logs

Todas as execuções são registradas.

Formato:

```json
{
  "pergunta": "...",
  "resposta": "...",
  "tool": "..."
}
```

Codificação:

```text
UTF-8
JSON serializado
```

---

# Melhorias Implementadas

## RAG

- fallback automático
    
- busca híbrida otimizada
    
- recuperação melhor para siglas
    

## Agenda

- priorização real para hoje
    
- integração com materiais
    

## Plano de Estudos

- respeito ao prazo
    
- geração mesmo sem documentos
    

## Active Recall

- isolamento por tema
    
- redução de mistura de contexto
    

## Revisão

- score baseado em desempenho
    

## Logs

- estrutura padronizada
    

---

# Benchmark

Métricas acompanhadas:

- qualidade RAG
    
- cobertura de contexto
    
- aderência temporal
    
- priorização
    
- Active Recall
    
- revisão personalizada
    
- geração de plano
    

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

|Método|Rota|Descrição|
|---|---|---|
|POST|`/api/ask`|Envia pergunta ao Jarvis|
|POST|`/api/files/upload`|Upload de documentos|
|GET|`/api/files`|Lista arquivos|
|GET|`/stats`|Estatísticas do RAG|
|GET|`/api/agenda`|Lista compromissos|
|POST|`/api/agenda`|Cria compromisso|
|PATCH|`/api/agenda/{id}/concluir`|Concluir compromisso|
|DELETE|`/api/agenda/{id}`|Remover compromisso|                                 |
