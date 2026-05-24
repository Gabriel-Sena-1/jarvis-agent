"""
Definições de tools (function calling) para o agente Jarvis.
Cada tool mapeia para um método da AgendaService.
"""

import json
from typing import Any

# ── Schemas no formato OpenAI ──────────────────────────────────────────────────

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "agenda_criar_compromisso",
            "description": (
                "Cria um novo compromisso na agenda do usuário. "
                "Use quando o usuário pedir para agendar, marcar ou criar um compromisso/evento."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "description": "Nome ou título do compromisso (ex: 'Reunião de projeto')"
                    },
                    "data": {
                        "type": "string",
                        "description": "Data do compromisso no formato YYYY-MM-DD (ex: '2026-05-30')"
                    },
                    "horario": {
                        "type": "string",
                        "description": "Horário do compromisso no formato HH:MM (ex: '14:30')"
                    },
                    "descricao": {
                        "type": "string",
                        "description": "Descrição opcional com detalhes do compromisso"
                    }
                },
                "required": ["nome", "data", "horario"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "agenda_listar_compromissos",
            "description": (
                "Lista os compromissos da agenda. "
                "Use quando o usuário quiser ver, consultar ou verificar compromissos agendados."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": (
                            "Filtra por uma data específica no formato YYYY-MM-DD. "
                            "Se não informado, retorna todos os compromissos."
                        )
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "agenda_atualizar_compromisso",
            "description": (
                "Atualiza um compromisso existente na agenda. "
                "Use quando o usuário quiser editar, alterar ou modificar um compromisso."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID do compromisso a ser atualizado"
                    },
                    "nome": {
                        "type": "string",
                        "description": "Novo nome do compromisso"
                    },
                    "data": {
                        "type": "string",
                        "description": "Nova data no formato YYYY-MM-DD"
                    },
                    "horario": {
                        "type": "string",
                        "description": "Novo horário no formato HH:MM"
                    },
                    "descricao": {
                        "type": "string",
                        "description": "Nova descrição"
                    }
                },
                "required": ["id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "agenda_deletar_compromisso",
            "description": (
                "Remove um compromisso da agenda. "
                "Use quando o usuário quiser cancelar, excluir ou deletar um compromisso."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID do compromisso a ser removido"
                    }
                },
                "required": ["id"]
            }
        }
    },
]


# ── Executor ───────────────────────────────────────────────────────────────────

def execute_tool(name: str, args: dict[str, Any], agenda_service) -> str:
    """
    Executa um tool pelo nome, chamando o método correspondente da AgendaService.
    Retorna sempre uma string JSON com o resultado para enviar de volta ao LLM.
    """
    try:
        if name == "agenda_criar_compromisso":
            result = agenda_service.criar(
                nome=args["nome"],
                data=args["data"],
                horario=args["horario"],
                descricao=args.get("descricao", ""),
            )
            return json.dumps(result, ensure_ascii=False, default=str)

        elif name == "agenda_listar_compromissos":
            result = agenda_service.listar(data=args.get("data"))
            return json.dumps(result, ensure_ascii=False, default=str)

        elif name == "agenda_atualizar_compromisso":
            result = agenda_service.atualizar(
                id=args["id"],
                nome=args.get("nome"),
                data=args.get("data"),
                horario=args.get("horario"),
                descricao=args.get("descricao"),
            )
            if result is None:
                return json.dumps({"erro": f"Compromisso com id={args['id']} não encontrado."})
            return json.dumps(result, ensure_ascii=False, default=str)

        elif name == "agenda_deletar_compromisso":
            ok = agenda_service.deletar(id=args["id"])
            return json.dumps({"sucesso": ok, "id": args["id"]})

        else:
            return json.dumps({"erro": f"Tool desconhecido: {name}"})

    except Exception as exc:
        return json.dumps({"erro": str(exc)})
