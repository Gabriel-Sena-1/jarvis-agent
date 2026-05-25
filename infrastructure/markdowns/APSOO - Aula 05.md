Análise e Projeto de Software Orientado a Objetos Engenharia de Requisitos: Levantamento, Requisitos Funcionais e Não Funcionais

Leonardo S. Victorio

Faculdade de Computação - UFMS

2026/1

<!-- image -->

## Sumário

- 1 Introdução à Engenharia de Requisitos
- 2 Tipos de Requisitos
- 3 Requisitos Funcionais
- 4 Requisitos Não Funcionais
- 5 Levantamento de Requisitos
- 6 Especificação de Requisitos
- 7 Validação e Gerenciamento de Requisitos

<!-- image -->

## O que são Requisitos?

- Requisitos de um sistema são descrições do que o sistema deve fazer: os serviços que oferece e as restrições ao seu funcionamento.
- Refletem as necessidades dos clientes para um sistema que serve a determinado propósito.
- O processo de descobrir, analisar, documentar e verificar esses serviços e restrições é chamado de Engenharia de Requisitos (RE) .

<!-- image -->

## Por que os Requisitos são Importantes?

- Erros nos requisitos são os mais caros de corrigir: quanto mais tarde são descobertos, maior o retrabalho.
- Um sistema tecnicamente perfeito, mas que não atende aos requisitos corretos, é um projeto com falha .
- Estudos mostram que a maioria dos fracassos em projetos de software tem origem em requisitos mal definidos ou incompletos.
- A engenharia de requisitos estabelece a base sólida sobre a qual todo o desenvolvimento é construído.

<!-- image -->

## O Problema da Profundidade dos Requisitos

## O Dilema do Nível de Abstração

Os requisitos variam desde declarações abstratas de alto nível dos serviços do sistema até especificações detalhadas das funções do sistema.

- O nível correto de detalhe depende do uso que se fará dos requisitos.
- Requisitos muito vagos levam a ambiguidades e mal-entendidos.
- Requisitos muito detalhados prematuramente limitam a criatividade da solução de projeto.

<!-- image -->

## Requisitos de Usuário vs. Requisitos de Sistema

## Dois Níveis de Abstração

- Requisitos de Usuário: Declarações em linguagem natural de quais serviços o sistema deve oferecer e as restrições sob as quais deve operar. Escritos para os clientes .
- Requisitos de Sistema: Documentos estruturados que definem de forma detalhada as funções, os serviços e as restrições operacionais do sistema. Escritos para os desenvolvedores .

<!-- image -->

## Quem Lê os Requisitos?

## Requisitos de Usuário

- Gerentes de clientes
- Usuários finais
- Engenheiros de clientes
- Gerentes de contratados
- Arquitetos do sistema

## Requisitos de Sistema

- Engenheiros de sistema
- Engenheiros de software
- Engenheiros de testes
- Engenheiros de interface

<!-- image -->

## O Processo de Engenharia de Requisitos

A engenharia de requisitos compreende um conjunto de atividades estruturadas:

- 1 Estudo de Viabilidade: O sistema é útil e realizável para a empresa?
- 2 Elicitação e Análise: Quais serviços os stakeholders necessitam?
- 3 Especificação: Definição dos requisitos de forma detalhada.
- 4 Validação: Verificar se os requisitos definem o sistema que o cliente quer.
- 5 Gerenciamento: Controle de mudanças ao longo do ciclo de vida.

<!-- image -->

## Classificação dos Requisitos

## Divisão Principal

Os requisitos de sistema são classificados em três grandes categorias:

- 1 Requisitos Funcionais (RF): O que o sistema deve fazer .
- 2 Requisitos Não Funcionais (RNF): Restrições sobre o sistema ou o processo de desenvolvimento.
- 3 Requisitos de Domínio: Derivados diretamente do domínio de aplicação do sistema.

<!-- image -->

## Requisitos Funcionais - Visão Geral

- Descrevem os serviços que o sistema deve fornecer.
- Descrevem como o sistema deve reagir a entradas específicas.
- Descrevem como o sistema deve se comportar em situações particulares.
- Em alguns casos, também declaram explicitamente o que o sistema não deve fazer .

<!-- image -->

## Requisitos Não Funcionais - Visão Geral

- Definem propriedades e restrições do sistema: confiabilidade, tempo de resposta, uso de memória, etc.
- Muitas vezes se aplicam ao sistema como um todo , não a funções individuais.
- Podem ser mais críticos que os requisitos funcionais - um sistema que não os satisfaz pode ser inutilizável .
- Podem surgir de restrições de usuários (orçamento), políticas organizacionais, padrões de segurança ou interoperabilidade.

<!-- image -->

## Requisitos de Domínio

- São derivados do domínio da aplicação do sistema.
- Refletem características e restrições específicas daquele domínio.
- Exemplos: regulamentações bancárias, normas médicas (HIPAA), leis de privacidade (LGPD).
- Podem ser funcionais ou não funcionais .

## Exemplo

Em um sistema de trem, os requisitos de domínio incluem regras de segurança que determinam a distância mínima entre trens, independente das funcionalidades desejadas pelos usuários.

<!-- image -->

## A Inter-relação entre os Tipos de Requisitos

## Atenção Importante

Na prática, a linha entre requisitos funcionais, não funcionais e de domínio pode ser tênue e subjetiva . Uma mesma necessidade pode ser expressa tanto como funcional quanto como não funcional dependendo da perspectiva.

- Exemplo: 'O sistema deve criptografar todos os dados de pagamento.' - Este é um requisito funcional (criptografar) com motivação de domínio (segurança = RNF).

<!-- image -->

## Definição de Requisitos Funcionais

## Definição

Requisitos funcionais são declarações de serviços que o sistema deve fornecer, de como o sistema deve reagir a entradas particulares e de como o sistema deve se comportar em situações específicas.

- Descrevem a funcionalidade ou os serviços do sistema.
- Dependem do tipo de software, dos usuários esperados e do tipo de sistema.
- Podem ser descritos de forma abstrata (para usuários) ou detalhada (para desenvolvedores).

<!-- image -->

## Exemplo: Sistema de Biblioteca (MHC-PMS)

## Requisitos Funcionais de um Sistema de Informações Médicas

- RF-01: Um usuário deve ser capaz de pesquisar todos os registros de pacientes do sistema de saúde.
- RF-02: O sistema deve gerar a cada dia, para cada clínica, uma lista de pacientes esperados naquele dia.
- RF-03: Cada membro da equipe usando o sistema deve ser identificado por seu número de empregado de 8 dígitos.
- RF-04: O sistema deve permitir que os médicos registrem consultas, diagnósticos e medicamentos.

<!-- image -->

## Completude e Consistência dos RFs

## Dois Requisitos Essenciais

- Completude: Os requisitos devem incluir descrições de todos os serviços requeridos.
- Consistência: Os requisitos não devem apresentar definições contraditórias.
- Na prática, é quase impossível produzir um documento de requisitos que seja completo e consistente desde o início.
- Inconsistências aparecem gradualmente à medida que mais detalhes são descobertos.

<!-- image -->

## O Problema da Imprecisão

- Problemas surgem quando os requisitos não são precisos o suficiente.
- Interpretações ambíguas entre desenvolvedores e clientes são a principal causa de retrabalho.

## Exemplo de Imprecisão

- RF mal escrito: 'O sistema deve fornecer uma interface adequada para os operadores.'
- Problema: O que é 'adequada'? Para o cliente pode ser simples; para o desenvolvedor pode ser sofisticada.
- RF bem escrito: 'O sistema deve fornecer uma interface gráfica baseada em menus com tempo máximo de resposta de 2 segundos.'

<!-- image -->

## Especificando Requisitos Funcionais

## Boas Práticas

- Use a forma verbal 'deverá' (shall) para indicar obrigatoriedade.
- Use 'deveria' (should) para indicar desejável, mas não obrigatório.
- Numere cada requisito individualmente para rastreabilidade.
- Escreva um requisito por vez - evite combinar múltiplas ações.
- Cada requisito funcional deve ser verificável : deve ser possível escrever um teste para ele.

<!-- image -->

## Definição de Requisitos Não Funcionais

## Definição

Requisitos não funcionais são restrições sobre os serviços ou as funções oferecidos pelo sistema. Incluem restrições de tempo, restrições sobre o processo de desenvolvimento e restrições impostas por padrões.

- Frequentemente se aplicam ao sistema como um todo , em vez de a funções individuais.
- Podem ser mais críticos que os requisitos funcionais.
- Um sistema que não satisfaz seus RNFs pode ser inutilizável , mesmo que funcione corretamente.

<!-- image -->

## Origens dos Requisitos Não Funcionais

## Requisitos de Produto

Especificam o comportamento do produto:

- Desempenho
- Confiabilidade
- Robustez
- Portabilidade
- Usabilidade

## Req. Organizacionais

Derivados de políticas da empresa:

- Padrões de processo
- Requisitos de implementação
- Requisitos de entrega

## Requisitos Externos

Derivados de fatores externos :

- Interoperabilidade
- Requisitos legais
- Ética
- Legislação (LGPD)

<!-- image -->

## Requisitos de Produto - Detalhamento

- Requisitos de velocidade: Número de transações processadas por segundo; tempo de resposta do usuário.
- Requisitos de tamanho: Memória utilizada; tamanho do disco requerido.
- Requisitos de facilidade de uso: Tempo de treinamento necessário; conformidade com padrões de acessibilidade.
- Requisitos de confiabilidade: Tempo médio entre falhas (MTBF); probabilidade de disponibilidade do sistema.
- Requisitos de robustez: Tempo para reinício após falha; percentual de eventos que causam falha.
- Requisitos de portabilidade: Percentual de declarações dependentes da plataforma alvo.

<!-- image -->

## Requisitos Organizacionais e Externos - Detalhamento

## Organizacionais

- Ambientais: O sistema deve operar em ambientes com restrições específicas de hardware.
- Operacionais: O sistema deve ser entregue como scripts Python e documentação HTML.
- De desenvolvimento: O processo deve ser documentado de acordo com a norma ISO/IEC 29119.

## Externos

- Regulatórios: O sistema deve obedecer às regulamentações de privacidade de dados (LGPD).
- De segurança: O sistema deve seguir as normas de segurança de dados médicos.
- De privacidade: Dados de pacientes devem ser armazenados e transmitidos de forma criptografada.

## Exemplo de Requisito Não Funcional

## RNF do Sistema de Saúde MHC-PMS

- RNF-01 (Desempenho): O sistema deve estar disponível para todas as clínicas durante o horário normal de trabalho (seg-sex, 8h às 17h30). Paradas para manutenção devem ocorrer fora desse horário.
- RNF-02 (Privacidade): O sistema deve implementar disposições de privacidade do paciente conforme definido na HStan-03-2006-priv.
- RNF-03 (Segurança): O sistema deve ser implementado em linguagem de programação segura (ex: Java ou Ada).

<!-- image -->

## O Problema da Verificabilidade dos RNFs

## RNFs Difíceis de Verificar

Requisitos como 'o sistema deve ser fácil de usar' ou 'o sistema deve ser rápido' são inverificáveis .

## Métricas para Tornar RNFs Verificáveis

| Propriedade                                                                | Métrica                                                                                                                                                                                          |
|----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Velocidade Tamanho Facilidade de uso Confiabilidade Robustez Portabilidade | Transações/seg; tempo de resposta Kbytes; número de chips de RAM Tempo de treinamento; erros/hora Prob. de indisponibilidade; MTBF Tempo de reinício; eventos de falha % declarações dependentes |

<!-- image -->

## Conflitos entre Requisitos

- Requisitos não funcionais frequentemente conflitam entre si.

## Exemplos de Conflitos

- Desempenho vs. Segurança: Criptografia aumenta a segurança, mas diminui o desempenho.
- Usabilidade vs. Segurança: Senhas complexas aumentam a segurança, mas dificultam o uso.
- Portabilidade vs. Desempenho: Código genérico é portável, mas menos eficiente que código otimizado para a plataforma.
- É necessário negociar com os stakeholders para definir prioridades.

<!-- image -->

## O que é Elicitação de Requisitos?

## Definição

Elicitação de requisitos (ou levantamento de requisitos) é o processo pelo qual engenheiros de software trabalham com clientes e usuários finais para descobrir os requisitos do sistema a ser desenvolvido.

- Também chamada de descoberta de requisitos .
- Envolve a interação com os stakeholders do sistema.
- É um processo iterativo - os requisitos evoluem com o tempo.
- Stakeholders raramente sabem exatamente o que querem e expressam de forma que pode ser mal interpretada.

<!-- image -->

## Os Stakeholders

## Quem são os Stakeholders?

Stakeholders são as pessoas direta ou indiretamente afetadas pelo sistema - clientes, usuários finais, gerentes, reguladores e a própria equipe de desenvolvimento.

- Usuários finais: Quem usará o sistema no dia a dia - sabem como o trabalho é feito.
- Gerentes: Definem restrições de negócio e prioridades.
- Engenheiros de sistema: Preocupados com a integração com outros sistemas.
- Stakeholders externos: Reguladores, parceiros, entidades legais.

<!-- image -->

## Dificuldades do Levantamento de Requisitos

## Problemas Comuns

- Stakeholders não sabem o que querem e às vezes mudam de ideia durante a elicitação.
- Stakeholders descrevem os requisitos em sua própria linguagem (jargão de domínio) que o analista não conhece.
- Diferentes stakeholders têm requisitos conflitantes - e ambos estão certos do seu ponto de vista.
- Fatores políticos e organizacionais podem influenciar os requisitos do sistema.
- O ambiente muda durante a elicitação - novos stakeholders ou legislações podem surgir.

<!-- image -->

## Técnicas de Levantamento: Entrevistas

## Entrevistas Fechadas

- Conjunto pré-definido de perguntas.
- Útil para confirmar informações já coletadas.
- Resultado mais consistente e fácil de analisar.

## Entrevistas Abertas

- Questões sem respostas pré-definidas.
- Útil para descobrir novos requisitos.
- Permite ao stakeholder explorar livremente o domínio.
- Na prática, o mais eficiente é combinar os dois tipos ao longo do projeto.
- O analista deve compreender o domínio do negócio antes de entrevistar.

<!-- image -->

## Técnicas de Levantamento: Etnografia

## O que é Etnografia?

Técnica de observação em que o analista se insere no ambiente de trabalho para observar e entender como os processos realmente funcionam na prática.

- Eficaz para descobrir requisitos implícitos - aqueles que os usuários fazem automaticamente e não mencionam.
- Revela a diferença entre o processo formal (como deveria ser) e o processo real (como acontece).
- Captura o contexto social do trabalho (colaboração, interrupções, adaptações).
- Limitação: não identifica requisitos novos ou organizacionais não representados na prática atual.

<!-- image -->

## Técnicas de Levantamento: Casos de Uso e Cenários

- Cenários são descrições narrativas de como o sistema será utilizado em situações específicas.
- Casos de Uso são representações estruturadas dessas interações entre usuários (atores) e o sistema.

## Estrutura de um Cenário

- Descrição do estado inicial do sistema.
- Fluxo normal de eventos.
- O que pode dar errado e como tratar (fluxo alternativo).
- Informação sobre atividades concorrentes.
- Descrição do estado final após a interação.

<!-- image -->

## O Processo de Elicitação e Análise

- O processo completo de levantamento envolve quatro atividades principais:
- 1 Descoberta de Requisitos: Interação com os stakeholders para identificar e coletar suas necessidades.
- 2 Classificação e Organização: Agrupar os requisitos relacionados em clusters coerentes (funcionais, de desempenho, de segurança, etc.).
- 3 Priorização e Negociação: Resolver conflitos entre stakeholders, priorizando requisitos mais críticos.
- 4 Especificação: Documentar os requisitos de forma clara, precisa e rastreável.

<!-- image -->

## O que é Especificação de Requisitos?

## Definição

Especificação de requisitos é o processo de escrever os requisitos de usuário e de sistema em um documento formal e estruturado, geralmente chamado de Documento de Requisitos de Software (SRS) .

- O documento deve ser completo e consistente .
- Os requisitos de usuário em linguagem natural e os requisitos de sistema em formato estruturado.
- Deve ser verificável : cada requisito precisa poder ser testado.

<!-- image -->

## Formas de Especificação

| Notação                       | Descrição                                                              |
|-------------------------------|------------------------------------------------------------------------|
| Linguagem natural             | Frases em linguagem cotidiana numeradas. Forma mais comum e acessível. |
| Linguagem natural estruturada | Formulários e templates padroni- zados para cada tipo de requisito.    |
| Linguagem de descrição (PDL)  | Linguagem parecida com código, mais precisa que texto livre.           |
| Notação gráfica               | Diagramas UML: casos de uso, diagramas de sequência.                   |
| Especificação matemática      | Baseada em lógica formal. Alta precisão, baixa legibilidade.           |

<!-- image -->

## Especificação em Linguagem Natural

- É a forma mais universalmente utilizada - todos os stakeholders conseguem ler.
- Vantagens: Expressiva, flexível, fácil de entender.
- Desvantagens: Ambiguidade, falta de precisão, difícil de validar automaticamente.

## Diretrizes para Escrever Requisitos em Linguagem Natural

- Invente um formato padrão e use-o consistentemente.
- Use 'deverá' para requisito obrigatório e 'deveria' para desejável.
- Use negrito para destacar partes essenciais do requisito.
- Evite jargões de TI - escreva para o cliente.
- Inclua a justificativa de por que o requisito existe.

<!-- image -->

## Especificação Estruturada de Requisitos

## Campos Típicos de um Formulário de Requisito

- Identificador único do requisito (ex: RF-07).
- Descrição: Enunciado do serviço ou restrição.
- Razão/Justificativa: Por que esse requisito é necessário.
- Origem: Stakeholder ou documento fonte.
- Dependências: Outros requisitos relacionados.
- Critério de aceitação: Como testar se o requisito foi satisfeito.
- Prioridade: Alta, Média, Baixa.

<!-- image -->

## O Documento de Requisitos de Software (SRS)

- O documento oficial que comunica os requisitos do sistema para os clientes, desenvolvedores e testadores.
- Deve especificar o que o sistema faz, não como será implementado.

## Estrutura Típica do SRS (IEEE 830)

- 1 Prefácio e histórico de revisões
- 2 Introdução e propósito
- 3 Glossário
- 4 Definição dos requisitos de usuário
- 5 Arquitetura do sistema (visão geral)
- 6 Especificação dos requisitos de sistema
- 7 Modelos do sistema (UML)
- 8 Evolução do sistema
- 9 Apêndices e índice

## Casos de Uso como Especificação

- Casos de Uso são uma forma visual e narrativa de especificar requisitos funcionais .
- Cada Caso de Uso descreve uma interação entre um ator (usuário ou sistema externo) e o sistema.

## Estrutura de um Caso de Uso

- Nome: Registrar Consulta
- Ator principal: Médico
- Pré-condição: Médico autenticado; paciente localizado no sistema.
- Fluxo principal: (1) Médico seleciona paciente; (2) informa dados da consulta; (3) sistema registra e confirma.
- Fluxo alternativo: Paciente não encontrado → sistema solicita cadastro.
- Pós-condição: Consulta registrada; lista de medicamentos atualizada.

<!-- image -->

## Validação de Requisitos

## Objetivo

Validação de requisitos visa demonstrar que os requisitos definidos correspondem de fato ao sistema que o cliente quer, antes que custos significativos sejam investidos no desenvolvimento.

- Erros nos requisitos custam muito mais quando descobertos após a implementação.
- Um erro de requisito pode levar à necessidade de redesenhar e reimplementar partes inteiras do sistema.
- Verificações importantes: validade, consistência, completude, realismo, verificabilidade.

<!-- image -->

## Verificações na Validação

Validade O sistema fornece as funções que melhor suportam as necessidades do cliente?

Consistência Há algum conflito entre os requisitos documentados?

Completude Estão incluídos todos os serviços e restrições exigidos pelo cliente?

Realismo Os requisitos podem ser implementados com o orçamento e tecnologia disponíveis?

Verificabilidade Pode-se escrever um conjunto de testes para demonstrar que o requisito foi satisfeito?

<!-- image -->

## Técnicas de Validação de Requisitos

## 1. Revisões de Requisitos

Equipe de revisores analisa o documento de requisitos sistematicamente, buscando erros, ambiguidades e omissões. Pode ser formal (auditoria) ou informal (leitura em grupo).

## 2. Prototipação

Desenvolver um protótipo executável do sistema para que os stakeholders possam experimentar e validar os requisitos na prática.

## 3. Geração de Casos de Teste

Desenvolver testes para cada requisito antes da implementação - se um requisito é difícil de testar, é um sinal de que está mal especificado.

<!-- image -->

## Gerenciamento de Requisitos

## Por que os Requisitos Mudam?

- O ambiente de negócio muda após o início do projeto.
- Os stakeholders mudam de opinião ou percebem que o sistema não atende às suas necessidades reais.
- Novas leis, regulações ou competidores surgem.
- A própria compreensão do problema evolui durante o desenvolvimento.

## Conclusão

Mudanças em requisitos são inevitáveis . O gerenciamento de requisitos é o processo de compreender e controlar essas mudanças.

<!-- image -->

## Rastreabilidade de Requisitos

- Rastreabilidade é a capacidade de relacionar, ao longo do ciclo de vida do software, os requisitos às suas origens, às suas implementações e aos seus testes.

## Rastreabilidade para frente

Requisito → Módulo de código → Caso de teste. 'Onde este requisito está implementado?'

## Rastreabilidade para trás

Módulo de código → Requisito → Stakeholder. 'Por que este código existe?'

<!-- image -->

## Controle de Mudanças em Requisitos

- 1 Solicitação de mudança: Registrar formalmente o que mudou e por quê (origem: stakeholder, bug, nova lei).
- 2 Análise de impacto: Identificar quais partes do sistema são afetadas por essa mudança e qual o custo de implementá-la.
- 3 Decisão: O comitê de controle de mudanças aprova ou rejeita a alteração.
- 4 Implementação: Atualizar o documento de requisitos, o design e os testes afetados.

<!-- image -->

## Resumo: O Ciclo Completo da Engenharia de Requisitos

- Elicitação: Descobrir o que os stakeholders precisam por meio de entrevistas, etnografia e cenários.
- Classificação: Separar em funcionais (o que o sistema faz) e não funcionais (como o sistema se comporta).
- Especificação: Documentar de forma clara, completa e consistente no SRS.
- Validação: Revisões, prototipação e geração de testes.
- Gerenciamento: Controlar mudanças e manter rastreabilidade.

<!-- image -->

## Encerramento e Próximos Passos

- A Engenharia de Requisitos é a fundação de todo o desenvolvimento de software - erros aqui se propagam e se ampliam nas fases seguintes.
- Requisitos Funcionais definem o que o sistema faz; Requisitos Não Funcionais definem como o sistema deve se comportar.
- A comunicação e a negociação com os stakeholders são habilidades tão importantes quanto as técnicas formais.
- Nos próximos passos, vamos modelar esses requisitos usando Casos de Uso e Diagramas UML .

<!-- image -->