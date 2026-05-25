## Análise e Projeto de Software Orientado a Objetos Diagrama de Classes de Design

Leonardo S. Victorio

Faculdade de Computação - UFMS

2026/1

<!-- image -->

## Sumário

- 1 Design da Camada de Domínio
- 2 Responsabilidades dos Objetos
- 3 Visibilidade entre Objetos
- 4 Modelagem Dinâmica
- 5 Pós-condições Condicionais e sobre Coleções
- 6 Consultas de Sistema
- 7 Delegação e Acoplamento Baixo
- 8 Diagrama de Classes de Design
- 9 Conclusão

<!-- image -->

<!-- image -->

## De onde Viemos - O que Vem a Seguir

Após a análise (casos de uso, modelo conceitual, contratos), inicia-se o projeto de software . O projeto se divide em:

## Projeto Lógico

- Diagramas de classes evoluídos a partir do modelo conceitual.
- Diagramas de interação (comunicação ou sequência).
- Resultado: o DCD .

## Foco desta aula

Projeto lógico , também chamado de design da camada de domínio . Cobre a modelagem dinâmica e a construção do Diagrama de Classes de Design (DCD) .

## Projeto Tecnológico

- Camada de interface (UI).
- Camada de persistência.
- Segurança, comunicação, etc.

## O que o Projetista Precisa Ter em Mãos

O projeto lógico pode ser realizado de forma sistemática , desde que existam dois artefatos da análise:

<!-- image -->

## Modelo Conceitual de Referência (Figura 9.13)

- O sistema Livir (livraria) será usado nos exemplos da aula. Este é o ponto de partida do DCD.

<!-- image -->

Classes: Livir (controlador), Pessoa , Venda , Item , Livro . A associação «temp» vendaCorrente guarda a venda em andamento.

MS

## Três Formas de Modelagem Dinâmica

| Forma             | Vantagem                                                                             | Desvantagem                                                      |
|-------------------|--------------------------------------------------------------------------------------|------------------------------------------------------------------|
| Algoritmos        | Fáceis de escrever                                                                   | Ocultam as conexões en- tre objetos; induzem alto acoplamento    |
| Diag. Comunicação | Linhas de visibilidade explícitas; mostram bem a distribuição de respon- sabilidades | Difíceis de organizar em colaborações complexas                  |
| Diag. Sequência   | Mais fáceis de ler                                                                   | Não explicitam visibili- dade; permitem comuni- cações inválidas |

## Por que usar diagramas, e não só algoritmos?

Sem método sistemático, as responsabilidades tendem a se concentrar em uma ou duas classes - gerando código tão desestruturado quanto programas espaguete . Os diagramas tornam visíveis as ligações e ajudam a distribuir bem as responsabilidades.

<!-- image -->

## O Erro Comum: 'Simulação do Mundo Real'

## Princípio

Um sistema OO representa as informações sobre o mundo real, não as coisas em si.

- Métodos não correspondem a ações do mundo real.
- Eles realizam internamente os contratos de operações de sistema.
- Por isso, métodos só aparecem na atividade de projeto , nunca na análise.

## Consequência do erro

Sem técnica, classes como Venda , Livro e Pagamento acabam sem métodos relevantes, enquanto a controladora ( Livir ) ou classes como Comprador fazem tudo. Isso é estrutura concentradora , não OO de verdade. Seria preferível um bom projeto estruturado a um OO assim.

<!-- image -->

## Classificação das Responsabilidades - Tabela 9.1

Para distribuir bem os métodos entre as classes, o livro classifica as responsabilidades em dois grupos , cada um com três subgrupos :

|                                   | Conhecer (consultas)        | Fazer (comandos)                   |
|-----------------------------------|-----------------------------|------------------------------------|
| Sobre si mesmo (atributos)        | getAtributo()               | setAtributo(v)                     |
| Sobre vizinhan- ças (associações) | getPapel()                  | addPapel(o) removePapel(o)         |
| Outros (derivado / coordenado)    | getDerivado() consultaXYZ() | métodos delegados (no- mes variam) |

Conhecer corresponde a consultas (devolvem valor sem alterar estado). Fazer corresponde a operações (alteram o estado de algum objeto).

<!-- image -->

## Responsabilidades de Conhecer - Detalhes

<!-- image -->

## Responsabilidades de Fazer - Detalhes

<!-- image -->

## Operações Básicas são Implícitas no DCD

Cada classe já tem por padrão todos os métodos básicos:

## Operações implícitas em qualquer classe

- create , destroy
- Para cada atributo: getAtrib() e setAtrib(v)
- Para cada associação: getPapel() , addPapel(o) , removePapel(o)

## Conta da padaria

Uma classe com 6 associações e 15 atributos teria, só de básicas: 1 create + 1 destroy + 15 set + 15 get + 6 add + 6 remove + 6 get = 50 métodos .

No DCD só aparecem explicitamente os métodos delegados (e atributos derivados). Os básicos ficam subentendidos pela existência dos atributos e associações.

<!-- image -->

## Por que Visibilidade Importa?

Para que dois objetos possam trocar mensagens , deve existir visibilidade entre eles. Sem visibilidade, não há comunicação.

## Quatro formas básicas de visibilidade

- 1 Por associação - existe ligação definida no modelo conceitual.
- 2 Por parâmetro - o objeto chega como argumento de um método.
- 3 Localmente declarada - o objeto chega como retorno de uma consulta.
- 4 Global - o objeto é declarado globalmente (Singleton).

## Assimetria

Nenhuma forma é simétrica : se x enxerga y , isso não implica que y enxerga x .

<!-- image -->

## Visibilidade por Associação - Para Um (Figura 9.1)

<!-- image -->

<!-- image -->

<!-- image -->

## Visibilidade por Associação - Para Muitos (Figura 9.2)

<!-- image -->

## Associações Ordenadas e Qualificadas (Figuras 9.3 e 9.4)

<!-- image -->

## Ordenadas {ordered}

Acesso por posição : capitulos[n] (n-ésimo) capitulos.last (último)

<!-- image -->

## Qualificadas

Com a chave do qualificador , acesso direto ao elemento: cartoes[123456] dá visibilidade imediata para aquele cartão.

<!-- image -->

## Classe de Associação (Figura 9.6)

<!-- image -->

## Dupla visibilidade

Pelo papel empregos , uma :Pessoa enxerga dois conjuntos:

- o conjunto de Empresa ;
- o conjunto de Emprego .

## Volta sempre para um

Uma instância de Emprego enxerga exatamente uma Pessoa e exatamente uma Empresa .

<!-- image -->

## Visibilidade por Parâmetro (Figura 9.10)

<!-- image -->

## Como funciona

Ao executar um método, um objeto recebe outro como parâmetro e passa a poder enviar mensagens a ele mesmo sem associação entre suas classes.

## Validade temporária

A visibilidade por parâmetro existe só durante a execução do método. Depois desaparece, igual a uma variável local.

<!-- image -->

(b)

## Visibilidade Localmente Declarada (Figura 9.11)

<!-- image -->

## Como funciona

Quando um objeto recebe outro como retorno de uma consulta, passa a ter visibilidade local sobre ele.

No exemplo, :Venda chama getLivro() em :Item e obtém liv:Livro .

## Também é temporária

Vale apenas dentro do método.

<!-- image -->

## Princípio 'Não Fale com Estranhos'

## Regra (Lei de Demeter)

Evite ao máximo usar visibilidade por parâmetro ou local para enviar mensagens a objetos.

- Mensagens devem trafegar pelas linhas de visibilidade por associação .
- Objetos recebidos como parâmetro/retorno deveriam apenas ser repassados , não chamados.
- Exceção aceitável da local: quando o método que retorna o objeto cria esse objeto.

## Por que?

Cada mensagem fora das associações cria acoplamento extra - não previsto no modelo conceitual - e degrada o projeto.

<!-- image -->

## Visibilidade Global (Figura 9.12)

<!-- image -->

## Padrão Singleton

Visibilidade global é válida apenas para instância única de uma classe - o padrão Singleton .

Costuma ser usada para classes de serviço : ConversorDeMoedas , ContadorDeTempo .

Entidades do domínio ( Venda , Livro ) nunca devem ser Singletons.

<!-- image -->

## Pós-condições e Diagramas de Interação

Os contratos dizem o que deve acontecer (pós-condições). Os diagramas mostram como os objetos trocam mensagens para fazê-lo.

## Quatro princípios

- 1 A visibilidade entre objetos é regida pela multiplicidade (e por pré-condições).
- 2 Cada pós-condição vira o envio de uma mensagem básica ao responsável imediato.
- 3 O fluxo sempre inicia no controlador recebendo mensagem da interface.
- 4 Sem visibilidade para o alvo, o controlador deve delegar ao objeto que enxerga.

| Tipo                                                      | Posição           | Quantidade                                       |
|-----------------------------------------------------------|-------------------|--------------------------------------------------|
| Operação de sistema Mensagens básicas Mensagens delegadas | Raiz Folhas Ramos | 1 por diagrama 1 por pós-condição quando preciso |

<!-- image -->

## Criação de Instância - Padrão Criador

<!-- image -->

## Exemplo Livir : criar um Item

Quem cria? Venda - pois há agregação Venda-Item . Livro , Pessoa e Livir não criariam:

- Livir sequer tem associação com Item .
- Livro associa-se a Item , mas Venda ganha pela agregação.

<!-- image -->

## Criação de Instância - Diagramas (Figura 9.14)

Contrato: Livir::adicionaItem(...) cria um novo Item .

<!-- image -->

Livir não tem visibilidade para Item , então delega (mensagem 1) à vendaCorrente:Venda , que então executa o create (mensagem 1.1) - a folha da árvore.

FACOM-UFMS

## Criação de Associação (Figura 9.15)

Toda instância recém-criada precisa ser imediatamente ligada a outra para se tornar acessível.

<!-- image -->

## Pós-condição

vendaCorrente.addItens(item)

## Duas formas simétricas

venda.addItens(item) e item.addVenda(venda) produzem o mesmo efeito. Prefira o receptor mais próximo do controlador .

<!-- image -->

## Caso Completo - Cria, Associa e Atualiza (Figura 9.17)

## Contrato: Livir::adicionaItem(idLivro, quantidade)

<!-- image -->

1: liv := getLivros(idLivro) (qualif.) 2: adicionaItem(liv, qtd) (delega) 2.1: it := create() 2.2: addItens(it) 2.3: addLivro(liv) 2.4: setQuantidade(qtd)

FACOM-UFMS

## Destruição de Instância (Figura 9.18)

<!-- image -->

## destroy()

Após destroy , nenhuma mensagem pode mais ser enviada ao objeto.

Vale o mesmo padrão Criador : composição, agregação ou associação 1-para-*.

## Sem órfãos

Com contratos bem formados, nenhum objeto fica com referência pendente para o destruído.

<!-- image -->

## Remoção de Associação (Figura 9.19) - Troca de Dono

<!-- image -->

## Pós-condições

removeDono(antigo) AND addDono(novo)

Controladora obtém os três objetos via consultas qualificadas e envia remove + add .

<!-- image -->

## Pós-condições Condicionais - Mensagens com Guarda

Algumas pós-condições só valem se uma condição inicial for satisfeita. Nos diagramas, isso vira uma mensagem com guarda .

## Exemplo do livro: desconto de 10% se total &gt; 1000

```
Context Livir::aplicaDesconto() pre: vendaCorrente.size() = 1 post: vendaCorrente.valorTotal > 1000 IMPLIES vendaCorrente.setValorTotal(.../1.1)
```

## No diagrama

```
Comunicação: a guarda vai entre colchetes antes da mensagem: 2: [vt>1000]: setValorTotal(vt/1.1) Sequência: a mensagem fica dentro de um bloco opt com a condição.
```

<!-- image -->

## Mensagem Condicional nos Diagramas (Figura 9.20)

<!-- image -->

(b)

Se vt ≤ 1000 , a mensagem simplesmente não é executada . Para um if-then-else , basta uma segunda mensagem com a guarda negada. Para um case , uma mensagem por caso.

## Pós-condições sobre Coleções - Iteração

Quando o contrato atualiza todos os elementos de uma coleção, usa-se o prefixo * antes da mensagem.

## Exemplo do livro: aumentar 10% em todos os livros

```
Context Livir::aumentaPrecos() post: livros->forAll(livro | livro.setPreco(livro.preco@pre * 1.1))
```

## Todos os elementos

```
1: *preco := getPreco() 2: *setPreco(preco*1.1)
```

## No diagrama de sequência

O * vira um bloco loop ; o *[cond] vira loop com opt interno.

## Apenas alguns (filtro)

2: *[preco&lt;100] setPreco(...) Só envia a mensagem aos elementos que satisfazem a condição.

## Iteração nos Diagramas (Figura 9.21)

<!-- image -->

Livir envia duas mensagens a cada elemento de livros : getPreco() e setPreco(preco*1.1) . O retângulo empilhado representa a coleção .

AS

## Iteração com Filtro (Figura 9.22)

<!-- image -->

Livir::aumentaLivrosBaratos() - só aumenta os livros com preco &lt; 100 . No diagrama de sequência, dentro do loop aparece um opt [preco&lt;100] que filtra.

MS

## Consultas de Sistema - Três Tipos de Mensagem

Em diagramas de consulta, as mensagens se organizam em três níveis:

## 1. Consulta de sistema (raiz)

Vem da interface, é a única mensagem 'de entrada' no diagrama. Retorna alfanumérico ou uma estrutura DTO ( Data Transfer Object ).

## 2. Consultas básicas (folhas)

São os get de atributos e papéis de associação. Não precisam ser detalhadas.

## 3. Consultas intermediárias (ramos)

Correspondem a atributos derivados ou a consultas com cálculo - e ficam nas classes mais próximas dos dados.

<!-- image -->

## Exemplo CRUD - Consulta de Livro (Figura 9.23)

Contrato: consultaLivro(umIsbn) retorna um DTO com os dados do livro.

<!-- image -->

Livir usa getLivros(umIsbn) (qualificada) para obter o livro , depois envia getTitulo , getAutor , getPreco e getStatus (todas básicas). A Tuple{...} é

.

S

## Quando não Vale a Pena o Diagrama

## Limitação dos diagramas

Diagrama de comunicação e sequência não representam bem funções matemáticas, filtros ou combinações complexas de valores.

## Recomendação do livro

Para consultas com lógica complexa, use algoritmo ou programação direta a partir do contrato, mantendo em mente:

- Se a consulta retorna alfanumérico simples, considere transformá-la em atributo derivado .
- Procure agrupar consultas básicas em estruturas reusáveis (DTO já filtrado, tupla, etc.).

<!-- image -->

## Padrões de Consulta com Filtro

Suponha o modelo da Figura 9.24: Livir tem catálogo de Livro , e queremos filtrar por autor, ano ou gênero.

| Padrão   | Como funciona                                                   | Quando usar                                                  |
|----------|-----------------------------------------------------------------|--------------------------------------------------------------|
| A        | Retorna tudo ; quem cha- mou filtra.                            | Muitos filtros, poucas chamadas; mas gera có- digo repetido. |
| B        | Um método por fil- tro : getPorAutor(a) , getPorGenero(g) . . . | Poucos filtros, muitas chamadas.                             |
| C        | Objeto filtro como parâmetro: getCatalogo(f:Filtro)             | Muitos filtros possíveis; chamadas simples.                  |

## Escolha do padrão

Depende da quantidade de filtros e da quantidade de chamadas . Não há padrão sempre correto.

<!-- image -->

## Padrão C - Objeto Filtro (Figura 9.25)

+autorNome:String

+periodo:Intervalo

+genero:String

<!-- image -->

## Duas Abordagens Opostas: Concentração vs. Delegação

Quando o controlador não enxerga o objeto que executaria a operação, há dois caminhos possíveis:

<!-- image -->

<!-- image -->

## Modelo do Exemplo (Figura 9.26)

<!-- image -->

## Cenário

Consulta: valor total da venda corrente .

Cálculo: somar quantidade × valor de cada Item da venda.

Livir não tem associação com Item . Só com Venda (via vendaCorrente ).

<!-- image -->

## Pseudocódigo concentrador

```
CLASSE Livir MÉTODO getTotalVendaCorrente() : Moeda itens := vendaCorrente.getItens() total := 0 PARA CADA item EM itens FAÇA total := total + (item.getValor() * item.getQuantidade()) FIM PARA RETORNA total
```

## Avaliação

- Está correto. Resolve o problema.
- Mas não gera nada reusável : o cálculo fica trancado dentro de getTotalVendaCorrente .
- Livir passa a depender da estrutura interna de Item ( valor , quantidade ).

## Versão com Delegação - Cada Classe Faz o Seu

Cada cálculo vira um atributo derivado na classe que tem os dados:

## Definições OCL

```
Context Item::subtotal:Moeda derive: quantidade*valor Context Venda::valorTotal:Moeda derive: itens->sum(subtotal)
```

## Pseudocódigo distribuído

```
CLASSE Livir MÉTODO getTotalVendaCorrente():Moeda RETORNA vendaCorrente.getValorTotal() CLASSE Venda // soma os subtotais dos itens CLASSE Item // calcula quantidade*valor
```

## Resultado

getSubtotal() e getValorTotal() viram métodos reusáveis em qualquer contexto. Livir não conhece mais Item .

## Delegação em Comandos (Figura 9.27)

Operação: mudaData(umaData) - atualiza a data da venda corrente.

<!-- image -->

## (b) Concentrador

Livir obtém venda via getVendaCorrente() e chama setData diretamente. Acopla-se ao atributo interno.

<!-- image -->

## O que é o DCD?

<!-- image -->

## Cinco Modificações Feitas no DCD durante o Projeto

- 1 Adição de métodos. Métodos delegados descobertos nos diagramas de interação são adicionados às classes correspondentes.
- 2 Direção das associações. Antes não-direcionais; passam a ter setas conforme o sentido das mensagens trocadas nos diagramas.
- 3 Detalhamento de tipos. Tipos abstratos podem virar concretos ( lista → array ou LinkedList ). Tipos de atributos podem ser fixados.
- 4 Reestruturação. Novas classes de projeto podem ser introduzidas (estratégias, serviços, filtros). O DCD pode divergir do conceitual.
- 5 Visibilidade de atributos. No conceitual todos são públicos. No DCD podem aparecer privados ou protegidos para encapsular estado interno.

<!-- image -->

## O que NÃO se Coloca no DCD - Métodos Básicos

Toda classe já tem por padrão os métodos básicos - eles podem ser deduzidos da estrutura:

## Métodos implícitos em qualquer classe

- create , destroy
- Para cada atributo : getAtrib() , setAtrib(v)
- Para cada associação : getPapel() , addPapel(o) , removePapel(o)

## Conta da padaria

Uma classe com 6 associações e 15 atributos teria 50 métodos básicos . Listar todos polui o diagrama.

## O que entra explicitamente no DCD

Apenas os métodos delegados (e atributos derivados não triviais), já que não podem ser deduzidos da estrutura.

## Método Delegado Gera Método no DCD (Figura 9.28)

<!-- image -->

<!-- image -->

<!-- image -->

## Direção das Associações no DCD (Figuras 9.29 e 9.30)

A direção de cada associação no DCD vem do sentido das mensagens nos diagramas de interação.

<!-- image -->

## DCD vs. Modelo Conceitual

| Aspecto       | Modelo Conceitual                               | DCD                                    |
|---------------|-------------------------------------------------|----------------------------------------|
| Propósito     | Representar o domínio                           | Guiar a implementa- ção                |
| Atributos     | Todos públicos                                  | Podem ser priva- dos/protegidos        |
| Métodos       | Só op./consultas de sistema (na controla- dora) | Métodos delegados ex- plicitados       |
| Associações   | Não direcionais                                 | Direcionadas pelo fluxo                |
| Novas classes | Não                                             | Sim (estratégias, fil- tros, serviços) |
| Tipos         | Abstratos                                       | Podem ser concretos ( array , etc.)    |

## O DCD é vivo

Vai sendo refinado a cada contrato analisado. Mudanças eventuais no modelo conceitual devem ser propagadas ao DCD.

## Pontos-Chave desta Aula

- O design da camada de domínio consiste em modelagem dinâmica e construção do DCD .
- Responsabilidades dos objetos: conhecer e atualizar , cada uma com três subgrupos.
- Quatro formas de visibilidade. Apenas a por associação é permanente.
- O Padrão Criador define quem cria instâncias - prioriza composição e agregação.
- Delegação produz código com menor acoplamento e maior coesão do que concentração.
- O DCD evolui do modelo conceitual: métodos adicionados, associações direcionadas, tipos detalhados.
- 'Não Fale com Estranhos' restringe a comunicação entre objetos sem associação semântica.
- Pós-condições condicionais usam mensagens guardadas ; iterações usam o prefixo * .

<!-- image -->

## Resumo do Processo de Design Lógico

- 1 Partir do modelo conceitual (primeira versão do DCD).
- 2 Para cada contrato de operação de sistema :
- a. Identificar as pós-condições e as visibilidades disponíveis.
- b. Construir o diagrama de comunicação iniciando no controlador.
- c. Delegar responsabilidades respeitando as linhas de visibilidade.
- 3 A cada mensagem recebida por um objeto, adicionar o método à sua classe no DCD.
- 4 Direcionar as associações conforme o fluxo de mensagens.
- 5 Identificar consultas intermediárias e transformá-las em atributos derivados quando possível.
- 6 Repetir até todos os contratos estarem modelados.
- 7 Revisar o DCD garantindo baixo acoplamento e alta coesão .

<!-- image -->

## Conexão com o Restante do Projeto

Com o DCD estabilizado, o projeto tecnológico pode avançar:

<!-- image -->

## O DCD é vivo

À medida que novos contratos são analisados e a implementação avança, o DCD é refinado. Mudanças no modelo conceitual devem ser propagadas.

## Referências Bibliográficas

- WAZLAWICK, Raul Sidnei. Análise e Projeto de Sistemas de Informação Orientados a Objetos . 3. ed. Rio de Janeiro: Elsevier, 2015. Cap. 9 - Projeto da Camada de Domínio.
- LARMAN, Craig. Utilizando UML e Padrões . 3. ed. Porto Alegre: Bookman, 2007. Cap. 9 - Domain Layer Design.
- GAMMA, Erich et al. Padrões de Projeto: soluções reutilizáveis de software OO . Porto Alegre: Bookman, 2000.
- LES/PUC-Rio. UML: Diagrama de Classes . Laboratório de Engenharia de Software, PUC-Rio.

<!-- image -->

## Obrigado!

Dúvidas e Discussões

Leonardo S. Victorio leonardo.victorio@ufms.br

Faculdade de Computação - UFMS

'Fazer design de software orientado a objetos deve ser entendido como um método preciso, guiado por padrões aprendidos, e não simplesmente como o ato de criar classes e associar métodos ad hoc a elas.'

- Wazlawick (2015)

<!-- image -->