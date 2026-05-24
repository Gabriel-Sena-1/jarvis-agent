---
name: agenda-crud
description: |
  Gerencia compromissos na agenda com SQLite. Use quando: criar compromisso, 
  agendar reunião, listar agenda, atualizar horário, remover evento, consultar 
  eventos do dia, marcar disponibilidade, reagendar.
---

# Gestão de Agenda

Manipula compromissos diretamente no banco de dados SQLite.

## Operações Disponíveis

### Criar Compromisso

```python
from app.services.agenda_service import AgendaService

agenda = AgendaService()
agenda.criar(
    nome="Reunião com cliente",
    data="2026-05-25",
    horario="14:30",
    descricao="Discussão sobre projeto"
)
```

### Listar Compromissos

```python
agenda.listar()  # Todos

agenda.listar(data="2026-05-25")  # De um dia específico
```

### Atualizar Compromisso

```python
agenda.atualizar(
    id=1,
    horario="15:00",
    descricao="Novo horário"
)
```

### Deletar Compromisso

```python
agenda.deletar(id=1)
```

## Uso no Agente

O agente pode chamar `AgendaService` diretamente para:

- ✅ Criar eventos sem passar por HTTP
- ✅ Buscar disponibilidade
- ✅ Sugerir horários
- ✅ Confirmar agendamentos
