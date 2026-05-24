---
name: agenda-instructions
description: "Instruções para que o agente use o serviço de agenda"
applyTo: "**"
---

# Instruções de Uso da Agenda

Quando o usuário pedir para criar, agendar, listar ou gerenciar compromissos, use a `AgendaService` diretamente:

```python
from app.services.agenda_service import AgendaService

agenda = AgendaService()

# Criar compromisso
compromisso = agenda.criar(
    nome="Nome do evento",
    data="2026-05-25",  # Formato: YYYY-MM-DD
    horario="14:30",     # Formato: HH:MM
    descricao="Descrição opcional"
)

# Listar compromissos
todos = agenda.listar()  # Todos ordenados
dia = agenda.listar(data="2026-05-25")  # De um dia específico

# Atualizar compromisso
agenda.atualizar(id=1, horario="15:00", nome="Novo nome")

# Deletar compromisso
agenda.deletar(id=1)
```

**Importante:** Você pode chamar diretamente sem passar por HTTP. O banco SQLite está em `infrastructure/database/scheduler.sqlite`.
