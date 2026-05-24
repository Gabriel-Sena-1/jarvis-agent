# Jarvis Agent

API REST de chatbot inteligente construída com FastAPI. Responde perguntas sobre documentos carregados e gerencia a agenda do usuário.

## Estrutura de Pastas

```
jarvis-agent/
├── main.py                          # Entrada da aplicação
├── requirements.txt
├── app/
│   ├── models/
│   │   └── schemas.py               # Schemas Pydantic
│   ├── routers/
│   │   └── chatbot.py               # Endpoints HTTP
│   └── services/
│       ├── chatbot_service.py       # Orquestração principal
│       ├── rag_manager.py           # Busca e geração de resposta (RAG)
│       ├── agenda_service.py        # CRUD de compromissos
│       └── tools.py                 # Definições de function calling
└── infrastructure/
    ├── documents/                   # Arquivos .txt/.pdf carregados pelo usuário
    ├── database/                    # Banco SQLite da agenda
    ├── cache/                       # Cache de embeddings gerados
    └── markdowns/                   # Documentos convertidos para markdown
```

## Como Funciona a Geração de Resposta

Toda pergunta recebida via `POST /api/ask` passa pelo seguinte fluxo:

### 1. Classificação da intenção

O próprio LLM classifica a pergunta em uma de duas categorias:

- **`agenda`** — perguntas sobre compromissos, eventos, horários, o que tem hoje/amanhã/esta semana
- **`documentos`** — perguntas sobre conteúdo de arquivos carregados, conceitos, resumos, matérias

```
Pergunta → LLM classificador → "agenda" | "documentos"
```

### 2. Montagem do contexto

**Se `agenda`:** busca os compromissos relevantes no SQLite (filtrando por hoje, amanhã ou semana) e monta um bloco de texto com nome, data, horário e status de cada item.

**Se `documentos`:** realiza busca híbrida (BM25 + embeddings) nos chunks dos documentos carregados e seleciona os `k` trechos mais relevantes.

### 3. Criação do prompt

O contexto montado é injetado no prompt enviado ao LLM:

```
[contexto: compromissos da agenda OU trechos dos documentos]

Pergunta do usuário: ...
```

### 4. Resposta

O LLM gera a resposta baseando-se exclusivamente no contexto fornecido e a retorna ao usuário junto com o número de chunks utilizados.

## Instalação e Execução

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env  # adicionar as chaves de API

python main.py
```

API disponível em `http://localhost:8000` — documentação em `/docs`.

## Endpoints

| Método | Rota                | Descrição                                 |
| ------ | ------------------- | ----------------------------------------- |
| `POST` | `/api/ask`          | Envia uma pergunta ao chatbot             |
| `POST` | `/api/files/upload` | Faz upload de um documento (.txt ou .pdf) |
| `GET`  | `/api/files`        | Lista os documentos carregados            |
| `GET`  | `/stats`            | Estatísticas do RAG (chunks, documentos)  |
