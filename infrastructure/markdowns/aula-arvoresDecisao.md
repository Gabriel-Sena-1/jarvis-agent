<!-- image -->

## Indu Induç ção de ão de Á Árvores de rvores de Decisão Decisão

<!-- image -->

- /boxshadowdwn Várias aplicações em Inteligência Artificial  em tarefas de importância prática são baseadas na construção de um modelo de conhecimento que é utilizado por um especialista humano
- /boxshadowdwn O objetivo desta aula é fornecer conceitos básicos sobre indução de árvores de decisão

## Motiva Motivaç ção ão

- /boxshadowdwn Dados pares (x,f(x)), inferir f(·)

<!-- image -->

Dada uma amostra finita, é freqüentemente impossível determinar a verdadeira função f(·)

Abordagem: Encontre uma hipótese ( modelo ) nos exemplos de treinamento e assuma que a hipótese se repita para exemplos futuros também

## Motiva Motivaç ção ão

<!-- image -->

| Exemplo   |   X 1 |   X 2 |   X 3 |   X 4 |   Y |
|-----------|-------|-------|-------|-------|-----|
| z 1       |     0 |     1 |     1 |     0 |   0 |
| z 2       |     0 |     0 |     0 |     0 |   0 |
| z 3       |     0 |     0 |     1 |     1 |   1 |
| z 4       |     1 |     0 |     0 |     1 |   1 |
| z 5       |     0 |     1 |     1 |     0 |   0 |
| z 6       |     1 |     1 |     0 |     0 |   0 |
| z 7       |     0 |     1 |     0 |     1 |   0 |

<!-- formula-not-decoded -->

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

¯

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

- ¯ Venenoso

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

- ¯ Venenoso

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

- ¯ Venenoso

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

- ¯ Venenoso

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

Hipótese 1: if 2&lt;W and W&lt;4 and H&lt;2 then comestível else venenoso

¯

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

+ Comestível

- ¯ Venenoso

Hipótese 1: if 2&lt;W and W&lt;4 and H&lt;2 then comestível else venenoso

Hipótese 2: if H&gt;W then venenoso else if H&gt;6-W then venenoso else comestível

## Exemplo: Cogumelos Comest Exemplo: Cogumelos Comestí íveis x veis x Venenosos Venenosos

<!-- image -->

- ¯ Venenoso

## Sistemas de Aprendizado Sistemas de Aprendizado de M de Má áquina quina - Á Árvore de Decisão rvore de Decisão

<!-- image -->

## TDIDT TDIDT

- /boxshadowdwn Os algoritmos de classificação cujo conhecimento adquirido é representado como Árvore de Decisão (AD) pertencem a família TDIDT ( Top Down Induction of Decision Trees )
- /boxshadowdwn Árvore de Decisão: estrutura recursiva definida como:
- /square4 um nó folha que indica uma classe, ou
- /square4 um nó de decisão que contém um teste sobre o valor de um atributo. Cada resultado do teste leva a uma sub-árvore. Cada sub-árvore tem a mesma estrutura da árvore

## AD AD para para Jogar Jogar Tênis Tênis

## /boxshadowdwn Atributos:

- /square4 Aparência: Sol, Nublado, Chuva

- /square4 Umidade: Alta, Normal

- /square4 Ventando: Forte, Fraco

- /square4 Temperatura: Quente, Média, Fria

- /square4 Classe (Conceito Alvo) - jogar tênis: Sim, Não

## AD AD para para Jogar Jogar Tênis Tênis

<!-- image -->

## AD para Jogar Tênis AD para Jogar Tênis

<!-- image -->

## AD AD para para Jogar Jogar Tênis Tênis

<!-- image -->

## AD AD para para Jogar Jogar Tênis Tênis

<!-- image -->

## AD AD para para Jogar Jogar Tênis Tênis

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## ADs ADs Representam Disjun Representam Disjunç ções de ões de Conjun Conjunç ções ões

<!-- image -->

(Aparência=Sol ∧ Umidade=Normal) ∨ (Aparência=Nublado) ∨ (Aparência=Chuva ∧ Ventando=Fraco)

## Sim

(Aparência=Sol ∧ Umidade=Alta) ∨ (Aparência=Chuva ∧ Ventando=Forte)

## Não

## Exemplo Exemplo: : Á Árvore rvore de de Decisão Decisão

<!-- image -->

## Representa Representaç ção da AD como um ão da AD como um Conjunto de Regras Conjunto de Regras

- /boxshadowdwn Uma árvore pode ser representada como um conjunto de regras
- /boxshadowdwn Cada regra começa na raiz da árvore e caminha para baixo, em direção às folhas
- /square4 Cada nó de decisão acrescenta um teste às premissas (condições) da regra
- /square4 O nó folha representa a conclusão da regra

## Representa Representaç ção da AD como um ão da AD como um Conjunto de Regras Conjunto de Regras

<!-- image -->

## Representa Representaç ção da AD como um ão da AD como um Conjunto de Regras Disjuntas Conjunto de Regras Disjuntas

- /boxshadowdwn As regras representadas  por uma árvore de decisão são disjuntas
- /boxshadowdwn Assim, elas podem ser escritas como regras separadas , começando pela raiz, e, consequentemente, o else não é necessário

## Representa Representaç ção da AD como um ão da AD como um Conjunto de Regras Disjuntas Conjunto de Regras Disjuntas

<!-- image -->

```
if Paciente se sente bem = sim then classe = saudável end if if Paciente se sente bem = não and Paciente tem dor = não and Temperatura do paciente ≤ 37 then classe = saudável end if if Paciente se sente bem = não and Paciente tem dor = não and Temperatura do paciente > 37 then classe = doente end if if Paciente se sente bem = não and Paciente tem dor = sim then classe = doente
```

```
end if
```

## Qual Qual é é mais mais facil facil de entender? de entender?

```
then if Paciente se sente bem = sim then classe = saudável else if Paciente tem dor = não if Temperatura do paciente ≤ 37 then classe = saudável else {Temperatura do Paciente > 37} classe = doente end if else {Paciente tem dor = sim} classe = doente end if end if
```

```
if Paciente se sente bem = sim then classe = saudável end if if Paciente se sente bem = não and Paciente tem dor = não and Temperatura do paciente ≤ 37 then classe = saudável end if if Paciente se sente bem = não and Paciente tem dor = não and Temperatura do paciente > 37 classe = doente end if if Paciente se sente bem = não and Paciente tem dor = sim then classe = doente end if
```

## Algoritmo TDIDT Algoritmo TDIDT

- /boxshadowdwn Seja T um conjunto de exemplos de treinamento com classes {C 1 , C 2 , ..., C k }. Há três possibilidades:
- 1) T contém um ou mais exemplos, todos pertencendo a uma mesma classe C j : a árvore de decisão para T é uma folha identificando a classe C j
- 2) T não contém exemplos: a árvore de decisão é novamente uma folha, mas a classe associada com a folha deve ser determinada por alguma informação além de T. Por exemplo, a folha pode ser escolhida de acordo com algum conhecimento do domínio, tal como a classe majoritária. C4.5 utiliza a classe mais freqüente do nó pai deste nó (folha)
- 3) T contém exemplos que pertencem a uma mistura de classes: nesta situação a idéia é refinar T em subconjuntos que são (ou aparentam ser) coleções de exemplos de uma única classe. Um teste é escolhido, baseado em um único atributo, com resultados mutuamente exclusivos. Sejam os possíveis resultados do teste denotados por {O 1 ,O 2 , ...,O r }. T é então particionado em subconjuntos T 1 , T 2 , ..., T r , nos quais cada T i contém todos os exemplos em T que possuem como resultado daquele teste o valor O i . A árvore de decisão para T consiste em um nó (interno) identificado pelo teste escolhido e uma aresta para cada um dos resultados possíveis. Para cada partição, pode-se exigir que cada T i contenha um número mínimo de exemplos, evitando partições com poucos exemplos. O default de C4.5 é de 2 exemplos
- /boxshadowdwn Os passos 1, 2 e 3 são aplicados recursivamente para cada subconjunto de exemplos de treinamento de forma que, em cada nó, as arestas levam para as sub-árvores construídas a partir do subconjunto de exemplos T i
- /boxshadowdwn Após a construção da árvore de decisão, a poda pode ser realizada para melhorar sua capacidade de generalização

## Pseudo Pseudo c có ódigo digo

```
function LearnDT(Training_Examples, Attributes, Default):Decision_Tree if IsEmptySet(Training_Examples) then return leaf(Default) if AllSameClass(Training_Examples) then return leaf(ClassOf(Training_Examples[0])) if IsEmptySet(Attributes) then return leaf(MajorityValue(Training_Examples)) bestAttr = ChooseAttribute(Training_Examples,Attributes); node = new node(bestAtt) for each value v_i of bestAttr do Training_Examples_i = {elements of Training_Examples with bestAttr == v_i} subtree = LearnDT(Training_Examples_i,Attributes,MajorityValue(Training_Examples)) add branch: node---v_i--->subtree end for return node end
```

## Classificando Novos Exemplos Classificando Novos Exemplos

- /boxshadowdwn Uma AD pode ser usada para classificar novos exemplos (nunca vistos)
- /boxshadowdwn A partir da raiz basta descer através dos nós de decisão até encontrar um nó folha: a classe correspondente a esse nó folha é a classe do novo exemplo
- /boxshadowdwn Um exemplo (sem valores desconhecidos) é classificado apenas por uma regra (subárvore)

## Exemplo (adaptado de Exemplo (adaptado de Quinlan Quinlan, 93) , 93)

- /boxshadowdwn Neste exemplo, vamos considerar um conjunto de 15 exemplos que contém medições diárias sobre condições meteorológicas
- /boxshadowdwn Atributos
- /square4 aparência: 'sol', 'nublado' ou 'chuva'
- /square4 temperatura: temperatura em graus Celsius
- /square4 umidade: umidade relativa do ar
- /square4 ventando: 'sim' ou 'não'
- /boxshadowdwn Cada exemplo foi rotulado com 'bom' se nas condições meteorológicas daquele dia é aconselhável fazer uma viagem à fazenda e 'ruim', caso contrário

## O Conjunto de Dados O Conjunto de Dados ' 'Viagem Viagem' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

## Escolhendo Escolhendo ' 'Aparência Aparência' ' para para Particionar Particionar

<!-- image -->

## Escolhendo Escolhendo ' 'Umidade Umidade' ' para para Particionar Particionar ' 'Aparência=sol Aparência=sol' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

<!-- image -->

## Escolhendo Escolhendo ' 'Umidade Umidade' ' para para Particionar Particionar ' 'Aparência=nublado Aparência=nublado' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

<!-- image -->

## Escolhendo Escolhendo ' 'Ventando Ventando' ' para para Particionar Particionar ' 'Aparência=chuva Aparência=chuva' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

<!-- image -->

## Á Árvore de Decisão Induzida (sem rvore de Decisão Induzida (sem poda) poda)

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

<!-- image -->

## Á Árvore de Decisão Induzida (sem rvore de Decisão Induzida (sem poda) poda)

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

<!-- image -->

## Á Árvore de Decisão Induzida rvore de Decisão Induzida (podada) (podada)

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Viajar   |
|-----------|-------------|---------------|-----------|------------|----------|
| E 1       | sol         |            25 |        72 | sim        | bom      |
| E 2       | sol         |            28 |        91 | sim        | ruim     |
| E 3       | sol         |            22 |        70 | não        | bom      |
| E 4       | sol         |            23 |        95 | não        | ruim     |
| E 5       | sol         |            30 |        85 | não        | ruim     |
| E 6       | nublado     |            23 |        90 | sim        | bom      |
| E 7       | nublado     |            29 |        78 | não        | bom      |
| E 8       | nublado     |            19 |        65 | sim        | ruim     |
| E 9       | nublado     |            26 |        75 | não        | bom      |
| E 10      | nublado     |            20 |        87 | sim        | bom      |
| E 11      | chuva       |            22 |        95 | não        | bom      |
| E 12      | chuva       |            19 |        70 | sim        | ruim     |
| E 13      | chuva       |            23 |        80 | sim        | ruim     |
| E 14      | chuva       |            25 |        81 | não        | bom      |
| E 15      | chuva       |            21 |        80 | não        | bom      |

<!-- image -->

## ( (P Pó ós s- -)Poda )Poda

- /boxshadowdwn Uma árvore maior é induzida de forma a superajustar os exemplos e então ela é podada até obter uma árvore menor (mais simples)
- /boxshadowdwn A poda evita overfitting

<!-- image -->

## Rela Relaç ção entre Tamanho da ão entre Tamanho da Á Árvore rvore de Decisão e a Taxa de Erro de Decisão e a Taxa de Erro

<!-- image -->

## Escolha do Atributo Escolha do Atributo

- /boxshadowdwn A maioria dos algoritmos de construção de árvores de decisão são sem retrocesso (sem backtracking ) ou seja, gulosos ( greedy )
- /boxshadowdwn Uma vez que um teste foi selecionado para particionar o conjunto atual de exemplos, a escolha é fixada e escolhas alternativas não são exploradas

## Escolha do Atributo Escolha do Atributo

- /boxshadowdwn A chave para o sucesso de um algoritmo de aprendizado por árvores de decisão depende do critério utilizado para escolher o atributo que particiona o conjunto de exemplos em cada iteração
- /boxshadowdwn Algumas possibilidades para escolher esse atributo são:
- /square4 aleatória: seleciona qualquer atributo aleatoriamente
- /square4 menos valores: seleciona o atributo com a menor quantidade de valores possíveis
- /square4 mais valores: seleciona o atributo com a maior quantidade de valores possíveis
- /square4 ganho máximo: seleciona o atributo que possui o maior ganho de informação esperado, isto é, seleciona o atributo que resultará no menor tamanho esperado das subárvores, assumindo que a raiz é o nó atual;
- /square4 razão de ganho
- /square4 índice Gini

## Exemplo Exemplo

<!-- image -->

Tira uma bola aleatoriamente -

- Qual a melhor sequencia de perguntas?
- Qual o número médio de perguntas?

8 bolas: 4     , 2   ,  1    , 1

## Exemplo Exemplo

- /boxshadowdwn Melhor conjunto de perguntas (Codigo de Huffman)

```
Vermelha ? azul ? Verde ? Purpura? sim não sim não sim não 1 pergunta 2 perguntas 3 perguntas 3 perguntas
```

O código de Huffman foi desenvolvido por David A. Huffman quando era aluno de PhD no MIT em 1952, e publicado no artigo: A Method for the Construction of Minimum-Redundancy Codes .

Professor David A. Huffman (August 9, 1925 - October 7, 1999)

<!-- image -->

## Exemplo Exemplo

## /boxshadowdwn Número médio de perguntas :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## Teoria Teoria da da Informa Informaç ção ão

<!-- image -->

- /boxshadowdwn Claude E.  Shannon (1916-2001)
- /boxshadowdwn 1948: A Mathematical Theory of Communication
- A entropia mede a falta de informação (medida de desordem) de um sistema

<!-- image -->

A entropia da agua em estado liquido é maior que a entropia da agua em estado sólido (0˚ C )

<!-- image -->

## A entropia de A A entropia entropia de de

gases  &gt; gases  &gt;  liquidos liquidos &gt; &gt;  solidos solidos

## Entropia Entropia

- /boxshadowdwn Pode também ser considerada como uma medida da quantidade de informação que uma pessoa necessita para organizar seus conhecimentos e descobrir uma regra
- /boxshadowdwn Quanto mais alternativas um diagnóstico possui, mais informações são necessárias para aprender ele (maior entropia)
- /boxshadowdwn Se um diagnóstico não tem alternativas, não é necessária nenhuma informação (entropia = 0)

## Entropia Entropia

- /boxshadowdwn Seja S um subconjunto de T
- /boxshadowdwn A informação esperada (ou entropia) do subconjunto S é (em bits) dado por

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## Entropia Entropia

- /boxshadowdwn Quando aplicado a todo o conjunto de treinamento T, info(T) mede a quantidade média de informação necessária para identificar a classe de um exemplo em T
- /boxshadowdwn Lembrar que log b (a) = ln(a) / ln(b) ou seja, log 2 (x) = ln(x) / ln(2)
- /boxshadowdwn Observação: assumir 0*log 2 (0) = 0

## Entropia Entropia

- /boxshadowdwn Considere o conjunto de exemplos T com a seguinte proporção de  exemplos +  e -

- /boxshadowdwn (50%,50%) info(T) = 1

- /boxshadowdwn (20%,80%) info(T) = 0.722

- /boxshadowdwn (100%,0%) info(T) = 0

Pode ser observado que quando T vai ficando mais 'puro', a entropia vai ficando menor. Para duas classes, o valor da entropia fica no intervalo [1,0]

## Exerc Exercí ício cio

- /boxshadowdwn Calcule info(T) para
- /square4 Um conjunto T de 64 exemplos, sendo 29 exemplos da classe positiva e 35 da classe negativa, ou seja, [29+,35-]
- /square4 Um conjunto T de 64 exemplos, sendo 20 exemplos da classe positiva, 32 da classe negativa e 12 da classe asterisco, ou seja, [20+,32-,12*]
- /square4 Idem para T=[20+,32-,6*,6$]

## Solu Soluç ção ão

```
/boxshadowdwn T = [29+,35-] /square4 info(T) =  info([29+,35-]) = -29/64 log 2 29/64 -35/64 log 2 35/64 = 0.99 /boxshadowdwn T = [20+,32-,12*] /square4 info(T) = info([20+,32-,12*]) = -20/64 log 2 20/64 -32/64 log 2 32/64 -12/64log2 12/64 = 1.48 /boxshadowdwn T = [20+,32-,6*,6$] /square4 info(T) = info([20+,32-,6*,6$]) = -20/64 log 2 20/64 -32/64 log 2 32/64 -6/64 log 2 6/64 -6/64 log 2 6/64 = 1.66
```

## Entropia Entropia

- /boxshadowdwn Considere agora que T foi particionado de acordo com r valores do atributo X , ou seja X = O 1 , X = O 2 , ..., X = O r , gerando os subconjuntos T 1 , T 2 , ..., T r , respectivamente
- /square4 Ti é o formado pelos exemplos de T nos quais o atributo X = O i , ou seja, T i = { ∀ z ∈ T: X = O i }
- /boxshadowdwn A informação esperada para este particionamento é a soma ponderada sobre todos os subconjuntos T i :

<!-- formula-not-decoded -->

- /boxshadowdwn lembrando que |T| é a cardinalidade do conjunto T

## Exerc Exercí ício cio

<!-- image -->

Calcule info(X 1 ,T) e info(X 2 ,T), T = [29+,35-]

## Solu Soluç ção ão

<!-- image -->

info([21+,5-]) = 0.71

info([8+,30-]) = 0.74

info(X 1 ,[29+,35-]) =

-26/64*info([21+,5-])

-38/64*info([8+,30-])

= 0.73

<!-- image -->

info([18+,32-]) = 0.94

info([7+,1-]) = 0.54

info([4+,2-]) = 0.92

info(X

2

,[29+,35-]) = -50/64*info([18+,32-]) -

8/64*info([7+,1-]) -6/64*info([4+,2-])

= 0.89

## Ganho de Informa Ganho de Informaç ção ão

- /boxshadowdwn A quantidade
- /square4 gain( X , T ) = info( T ) - info( X , T )
- /square4 mede o ganho de informação pela partição de T de acordo com o atributo X
- /boxshadowdwn O critério de ganho (ganho máximo) seleciona o atributo X ∈ T (ou seja, X ∈ {X 1 , X2 , ..., X m }) que maximiza o ganho de informação

<!-- formula-not-decoded -->

## Exerc Exercí ício cio

[29+,35-]

X1=?

True False

[21+, 5-]

[8+, 30-]

T = [29+,35-]

info([29+,35-]) = 0.99

info(X 1 ,[29+,35-]) = 0.73

info(X 2 ,[29+,35-]) = 0.89

<!-- image -->

Qual o ganho de X 1 ? E de X 2 ?

Com qual atributo obtém-se o ganho máximo?

## Solu Soluç ção ão

<!-- image -->

<!-- formula-not-decoded -->

info([29+,35-]) = 0.99

info(X 1 ,[29+,35-]) = 0.73

info(X 2 ,[29+,35-]) = 0.89

<!-- image -->

<!-- formula-not-decoded -->

= 0.99 - 0.73 = 0.26

gain(X 2 ,T) = info(T) - info(X 2 ,T)

<!-- formula-not-decoded -->

Ganho máximo é obtido com X 1

## Exemplo Exemplo

| Exemplo                                                      | Aparência                                                                         | Temperatura                                                                                                 | Umidade                                                                             | Ventando                                                                                                          | Jogar                                                   |
|--------------------------------------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| E 1 E 2 E 3 E 4 E 5 E 6 E 7 E 8 E 9 E 10 E 11 E 12 E 13 E 14 | sol sol nublado chuva chuva chuva nublado sol sol chuva sol nublado nublado chuva | quente quente quente agradável fria fria fria agradável fria agradável agradável agradável quente agradável | alta alta alta alta normal normal normal alta normal normal normal alta normal alta | falso verdadeiro falso falso falso verdadeiro verdadeiro falso falso falso verdadeiro verdadeiro falso verdadeiro | não não sim sim sim não sim não sim sim sim sim sim não |

## Exemplo Exemplo

| Exemplo   | Aparência   | Temperatura   | Umidade   | Ventando         | Jogar   |
|-----------|-------------|---------------|-----------|------------------|---------|
| E 1 E 2   | sol sol     | quente quente | alta alta | falso verdadeiro | não não |

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total |   Ventando |            |   sim |   não |   Total | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|------------|-------|-------|---------|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |         |          7 | falso      |     6 |     2 |       8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |       |       1 |          7 | verdadeiro |     3 |     3 |       6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |            |       |       |         |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |       |       5 |         14 | Total      |     9 |     5 |      14 | Total   | 14 |

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total | Ventando   | sim   |    |   não Total |    | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|-------|----|-------------|----|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |       7 | falso      |       |  6 |           2 |  8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |     1 |       7 | verdadeiro |       |  3 |           3 |  6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |       |    |             |    |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |     5 |      14 |            | Total |  9 |           5 | 14 | Total   | 14 |

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total | Ventando   | sim   |    |   não Total |    | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|-------|----|-------------|----|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |       7 | falso      |       |  6 |           2 |  8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |     1 |       7 | verdadeiro |       |  3 |           3 |  6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |       |    |             |    |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |     5 |      14 |            | Total |  9 |           5 | 14 | Total   | 14 |

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total | Ventando   | sim   |    |   não Total |    | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|-------|----|-------------|----|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |       7 | falso      |       |  6 |           2 |  8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |     1 |       7 | verdadeiro |       |  3 |           3 |  6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |       |    |             |    |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |     5 |      14 |            | Total |  9 |           5 | 14 | Total   | 14 |

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total | Ventando   | sim   |    |   não Total |    | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|-------|----|-------------|----|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |       7 | falso      |       |  6 |           2 |  8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |     1 |       7 | verdadeiro |       |  3 |           3 |  6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |       |    |             |    |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |     5 |      14 |            | Total |  9 |           5 | 14 | Total   | 14 |

<!-- formula-not-decoded -->

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total | Ventando   | sim   |    |   não Total |    | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|-------|----|-------------|----|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |       7 | falso      |       |  6 |           2 |  8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |     1 |       7 | verdadeiro |       |  3 |           3 |  6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |       |    |             |    |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |     5 |      14 |            | Total |  9 |           5 | 14 | Total   | 14 |

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

| Aparência   |   sim |   não |   Total | Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |   Total | Ventando   | sim   |    |   não Total |    | Jogar   |    |
|-------------|-------|-------|---------|---------------|-------|-------|---------|-----------|-------|-------|---------|------------|-------|----|-------------|----|---------|----|
| sol         |     2 |     3 |       5 | quente        |     2 |     2 |       4 | alta      |     3 |     4 |       7 | falso      |       |  6 |           2 |  8 | sim     |  9 |
| nublado     |     4 |     0 |       4 | agradável     |     4 |     2 |       6 | normal    |     6 |     1 |       7 | verdadeiro |       |  3 |           3 |  6 | não     |  5 |
| chuva       |     3 |     2 |       5 | fria          |     3 |     1 |       4 |           |       |       |         |            |       |    |             |    |         |    |
| Total       |     9 |     5 |      14 | Total         |     9 |     5 |      14 | Total     |     9 |     5 |      14 |            | Total |  9 |           5 | 14 | Total   | 14 |

<!-- formula-not-decoded -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar todo o Conjunto de Exemplos todo o Conjunto de Exemplos

<!-- formula-not-decoded -->

## O Subconjunto O Subconjunto ' 'Aparência=nublado Aparência=nublado' ' possui possui Apenas Exemplos de uma Mesma Classe... Apenas Exemplos de uma Mesma Classe...

<!-- image -->

[4s,0n]

| Exemplo           | Aparência                       | Temperatura                  | Umidade                 | Ventando                          | Jogar           |
|-------------------|---------------------------------|------------------------------|-------------------------|-----------------------------------|-----------------|
| E 3 E 7 E 12 E 13 | nublado nublado nublado nublado | quente fria agradável quente | alta normal alta normal | falso verdadeiro verdadeiro falso | sim sim sim sim |

## ...o que Leva a um N ...o que Leva a um Nó ó Folha Folha

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=sol Aparência=sol' '

| Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não | Total Ventando   | sim        |   não |   Total |    | Jogar   |    |
|---------------|-------|-------|---------|-----------|-------|-------|------------------|------------|-------|---------|----|---------|----|
| quente        |     0 |     2 |       2 | alta      |     0 |     3 | 3 falso          | 1          |     2 |         |  3 | sim     |  2 |
| agradável     |     1 |     1 |       2 | normal    |     2 |     0 | 2                | verdadeiro |     1 |       1 |  2 | não     |  3 |
| fria          |     1 |     0 |       1 |           |       |       |                  |            |       |         |    |         |    |
| Total         |     2 |     3 |       5 | Total     |     2 |     3 | 5                | Total      |     2 |       3 |  5 | Total   |  5 |

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=sol Aparência=sol' '

<!-- image -->

| Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não | Total Ventando   | sim        |   não |   Total |    | Jogar   |    |
|---------------|-------|-------|---------|-----------|-------|-------|------------------|------------|-------|---------|----|---------|----|
| quente        |     0 |     2 |       2 | alta      |     0 |     3 | 3 falso          | 1          |     2 |         |  3 | sim     |  2 |
| agradável     |     1 |     1 |       2 | normal    |     2 |     0 | 2                | verdadeiro |     1 |       1 |  2 | não     |  3 |
| fria          |     1 |     0 |       1 |           |       |       |                  |            |       |         |    |         |    |
| Total         |     2 |     3 |       5 | Total     |     2 |     3 | 5                | Total      |     2 |       3 |  5 | Total   |  5 |

```
0 bits ) info(Umidade , 0.4 bits ) info(Temperatur a, 0.97095  bits ) info( = = = T T T
```

0.95098  bits ) info(Ventando , = T

0.01997 bits 0.95098 0.97095 ) info(Ventando, ) info( ) gain(Ventando, 0.97095 bits 0 0.97095 ) info(Umidade, ) info( ) gain(Umidade, 0.57095 bits 0.4 0.97095 ) info(Temperatura, ) info( ) gain(Temperatura, = -= -= = -= -= = -= -= T T T T T T T T T

<!-- formula-not-decoded -->

## Escolha do Atributo Escolha do Atributo ' 'Umidade Umidade' ' para para Particionar Particionar ' 'Aparência=sol Aparência=sol' '

<!-- image -->

Exemplo  Aparência  Temperatura  Umidade  Ventando  Jogar

E1

E2

E8

sol

sol

sol quente quente agradável alta alta alta falso verdadeiro falso não não não

| Exemplo   | Aparência   | Temperatura   | Umidade   | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 9       | sol         | fria          | normal    | falso      | sim     |
| E 11      | sol         | agradável     | normal    | verdadeiro | sim     |

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=chuva Aparência=chuva' '

| Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |    | Total      | Ventando   |   sim não |    |   Total | Jogar   |    |
|---------------|-------|-------|---------|-----------|-------|-------|----|------------|------------|-----------|----|---------|---------|----|
| quente        |     0 |     0 |       0 | alta      |     1 |     1 |    | 2          | falso      |         3 |  0 |       3 | sim     |  3 |
| agradável     |     2 |     1 |       3 | normal    |     2 |     1 |  3 | verdadeiro |            |         0 |  2 |       2 | não     |  2 |
| fria          |     1 |     1 |       2 |           |       |       |    |            |            |           |    |         |         |    |
| Total         |     3 |     2 |       5 | Total     |     3 |     2 |  5 |            | Total      |         3 |  2 |       5 | Total   |  5 |

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=chuva Aparência=chuva' '

<!-- image -->

0 bits ) info(Ventando , 0.95098  bits ) info(Umidade , 0.95098  bits ) info(Temperatur a, 0.97095  bits ) info( = = = = T T T T

| Temperatura   |   sim |   não |   Total | Umidade   |   sim |   não |    | Total      | Ventando   |   sim não |    |   Total | Jogar   |    |
|---------------|-------|-------|---------|-----------|-------|-------|----|------------|------------|-----------|----|---------|---------|----|
| quente        |     0 |     0 |       0 | alta      |     1 |     1 |    | 2          | falso      |         3 |  0 |       3 | sim     |  3 |
| agradável     |     2 |     1 |       3 | normal    |     2 |     1 |  3 | verdadeiro |            |         0 |  2 |       2 | não     |  2 |
| fria          |     1 |     1 |       2 |           |       |       |    |            |            |           |    |         |         |    |
| Total         |     3 |     2 |       5 | Total     |     3 |     2 |  5 |            | Total      |         3 |  2 |       5 | Total   |  5 |

0.01997 bits 0.95098 0.97095 ) info(Temperatura, ) info( ) gain(Temperatura, = -= -= T T T

0.97095 bits 0 0.97095 ) info(Ventando, ) info( ) gain(Ventando, 0.01997 bits 0.95098 0.97095 ) info(Umidade, ) info( ) gain(Umidade, = -= -= = -= -= T T T T T T

<!-- formula-not-decoded -->

## Escolha do Atributo Escolha do Atributo ' 'Ventando Ventando' ' para para Particionar Particionar ' 'Aparência=chuva Aparência=chuva' '

<!-- image -->

| Exemplo   | Aparência         | Temperatura    | Umidade            | Ventando    | Jogar       |
|-----------|-------------------|----------------|--------------------|-------------|-------------|
| E 4 E 5 E | chuva chuva chuva | agradável fria | alta normal normal | falso falso | sim sim sim |
| 10        |                   | agradável      |                    | falso       |             |

| Exemplo   | Aparência   | Temperatura   | Umidade     | Ventando   | Jogar   |
|-----------|-------------|---------------|-------------|------------|---------|
| E 6       | chuva       | fria          | normal alta | verdadeiro | não     |
| E 14      | chuva       | agradável     |             | verdadeiro | não     |

## Á Árvore de Decisão Induzida rvore de Decisão Induzida

<!-- image -->

## Exerc Exercí ício cio

- /boxshadowdwn Calcule o ganho para o atributo 'Dia', ou seja, gain(Dia,T), sabendo que info(T)=0.94
- /square4 gain(Dia,T) = info(T) - info(Dia,T)

| Dia   | Aparência   | Temperatura   | Umidade   | Ventando   | Jogar   |
|-------|-------------|---------------|-----------|------------|---------|
| d1    | sol         | quente        | alta      | falso      | não     |
| d2    | sol         | quente        | alta      | verdadeiro | não     |
| d3    | nublado     | quente        | alta      | falso      | sim     |
| d4    | chuva       | agradável     | alta      | falso      | sim     |
| d5    | chuva       | fria          | normal    | falso      | sim     |
| d6    | chuva       | fria          | normal    | verdadeiro | não     |
| d7    | nublado     | fria          | normal    | verdadeiro | sim     |
| d8    | sol         | agradável     | alta      | falso      | não     |
| d9    | sol         | fria          | normal    | falso      | sim     |
| d10   | chuva       | agradável     | normal    | falso      | sim     |
| d11   | sol         | agradável     | normal    | verdadeiro | sim     |
| d12   | nublado     | agradável     | alta      | verdadeiro | sim     |
| d13   | nublado     | quente        | normal    | falso      | sim     |
| d14   | chuva       | agradável     | alta      | verdadeiro | não     |

## Razão de Ganho Razão de Ganho

- /boxshadowdwn Vimos que o ganho máximo é interessante para particionar os exemplos, fornecendo bons resultados
- /boxshadowdwn Entretanto, ele tem uma tendência ( bias ) em favor de testes com muitos valores
- /boxshadowdwn Por exemplo, considere um conjunto de exemplos de diagnóstico médico no qual um dos atributos contém o código de identificação do paciente (ID)
- /boxshadowdwn Uma vez que cada código ID é único, particionando o conjunto de treinamento nos valores deste atributo levará a um grande número de subconjuntos, cada um contendo somente um caso
- /boxshadowdwn Como todos os subconjuntos (de 1 elemento) necessariamente contêm exemplos de uma mesma classe, info(ID,T)=0, assim o ganho de informação deste atributo será máximo

## Razão de Ganho Razão de Ganho

info(ID,T) = 0

<!-- image -->

## Razão de Ganho Razão de Ganho

- /boxshadowdwn Para solucionar esta situação, em analogia à definição de info(T), vamos definir a informação potencial gerada pela partição de T em r subconjuntos

<!-- formula-not-decoded -->

- /boxshadowdwn A razão de ganho é definida como:

<!-- formula-not-decoded -->

- /boxshadowdwn A razão de ganho expressa a proporção de informação gerada pela partição que é útil, ou seja, que aparenta ser útil para a classificação

## Razão de Ganho Razão de Ganho

- /boxshadowdwn Usando o exemplo anterior para o atributo Aparência que produz três subconjuntos com 5, 4 e 5 exemplos, respectivamente

<!-- formula-not-decoded -->

- /boxshadowdwn Para este teste, cujo ganho é gain(Aparência,T)=0.24675 (mesmo valor anterior), a razão de ganho é
- /square4 gain-ratio(Aparência,T) = 0.24675 / 1.57741 = 0.156428

## Atributos Num Atributos Numé éricos ricos

- /boxshadowdwn Se um atributo X assume valores reais (numéricos), é gerado um teste binário cujos resultados são X &lt;= Z e X &gt; Z
- /boxshadowdwn O limite Z pode ser encontrado da seguinte forma
- /square4 Os exemplos de T são inicialmente ordenados considerando os valores do atributo X sendo considerado
- /square4 Há apenas um conjunto finito de valores, que podemos denotar (em ordem) por {v 1 , v 2 , ..., v L }
- /square4 Qualquer limite caindo entre v i e v i+1 tem o mesmo efeito que particionar os exemplos cujos valores do atributo X encontra-se em {v 1 , v 2 , ..., v i } e em {v i+1 , v i+2 , ..., v L }
- /square4 Assim, existem apenas L-1 divisões possíveis para o atributo X, cada uma devendo ser examinada
- /square4 Isso pode ser obtido (uma vez ordenados os valores) em uma única passagem, atualizando as distribuições de classes para a esquerda e para a direita do limite Z durante o processo
- /square4 Alguns indutores podem escolher o valor de limite como sendo o ponto médio de cada intervalo Z=(v i +v i+1 )/2
- /square4 C4.5, entretanto, escolhe o maior valor de Z entre todo o conjunto de treinamento que não excede o ponto médio acima, assegurando que todos os valores que aparecem na árvore de fato ocorrem nos dados

## Exemplo (atributos num Exemplo (atributos numé éricos) ricos)

| Exemplo                                                      | Aparência                                                                         | Temperatura                               | Umidade                                   | Ventando                                                                                                          | Jogar                                                   |
|--------------------------------------------------------------|-----------------------------------------------------------------------------------|-------------------------------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| E 1 E 2 E 3 E 4 E 5 E 6 E 7 E 8 E 9 E 10 E 11 E 12 E 13 E 14 | sol sol nublado chuva chuva chuva nublado sol sol chuva sol nublado nublado chuva | 85 80 83 70 68 65 64 72 69 75 75 72 81 71 | 85 90 86 96 80 70 65 95 70 80 70 90 75 91 | falso verdadeiro falso falso falso verdadeiro verdadeiro falso falso falso verdadeiro verdadeiro falso verdadeiro | não não sim sim sim não sim não sim sim sim sim sim não |

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar todo o Conjunto de Exemplos todo o Conjunto de Exemplos

| Aparência   |   sim |   não | Total    | Ventando     | sim   |   não | Total Jogar   |   Total Jogar |
|-------------|-------|-------|----------|--------------|-------|-------|---------------|---------------|
| sol         |     2 |     3 | 5        | falso        | 6 2   |     8 | sim           |             9 |
| nublado     |     4 |     0 | 4        | verdadeiro 3 | 3     |     6 | não           |             5 |
| chuva       |     3 |     2 | 5        |              |       |       |               |               |
| Total       |     9 |     5 | 14 Total | 9            | 5     |    14 | Total         |            14 |

| Temperatura   | 64   | 65   | 68   | 69   | 70   | 71   | 72      | 75      | 80   | 81   | 83   | 85   |
|---------------|------|------|------|------|------|------|---------|---------|------|------|------|------|
| Jogar         | sim  | não  | sim  | sim  | sim  | não  | não sim | sim sim | não  | sim  | sim  | não  |

| Umidade   | 65   | 70          | 75   | 80      | 85   | 86   | 90      | 91   | 95   | 96   |
|-----------|------|-------------|------|---------|------|------|---------|------|------|------|
| Jogar     | sim  | não sim sim | sim  | sim sim | não  | sim  | não sim | não  | não  | sim  |

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar todo o Conjunto de Exemplos todo o Conjunto de Exemplos

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar todo o Conjunto de Exemplos todo o Conjunto de Exemplos

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar todo o Conjunto de Exemplos todo o Conjunto de Exemplos

```
0.89216 bits ) info(Ventando, 0.92997 bits ) , info(Umidade 0.93980 bits ) , info(Temperatura 0.69354 bits ) info(Aparência, 0.94029 bits ) info( 82.5 Z 84 Z = = = = = = = T T T T T
```

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

O Subconjunto O Subconjunto ' 'Aparência=nublado Aparência=nublado' ' possui Apenas possui Apenas Exemplos de uma Mesma Classe, Levando a um Exemplos de uma Mesma Classe, Levando a um N Nó ó Folha Folha

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=sol Aparência=sol' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 1       | sol         |            85 |        85 | falso      | não     |
| E 2       | sol         |            80 |        90 | verdadeiro | não     |
| E 8       | sol         |            72 |        95 | falso      | não     |
| E 9       | sol         |            69 |        70 | falso      | sim     |
| E 11      | sol         |            75 |        70 | verdadeiro | sim     |

| Ventando   |   sim |   não |   Total | Jogar   |    |
|------------|-------|-------|---------|---------|----|
| falso      |     1 |     2 |       3 | sim     |  2 |
| verdadeiro |     1 |     1 |       2 | não     |  3 |
| Total      |     2 |     3 |       5 | Total   |  5 |

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 4       | chuva       |            70 |        96 | falso      | sim     |
| E 5       | chuva       |            68 |        80 | falso      | sim     |
| E 6       | chuva       |            65 |        70 | verdadeiro | não     |
| E 10      | chuva       |            75 |        80 | falso      | sim     |
| E 14      | chuva       |            71 |        91 | verdadeiro | não     |

| Temperatura   | Temperatura   | 69      | 69      | 72      | 75      | 80   | 85   |
|---------------|---------------|---------|---------|---------|---------|------|------|
| Jogar         | Jogar         | sim     | sim     | não sim | não sim | não  | não  |
| Umidade       | 70            | 70      | 85 90   | 85 90   | 95      |      |      |
| Jogar         | sim sim       | sim sim | não não | não não | não     |      |      |

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=sol Aparência=sol' '

Temperatura

64

65

68

69

70

71

72

75

80

81

83

85

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=sol Aparência=sol' '

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=sol Aparência=sol' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 1       | sol         |            85 |        85 | falso      | não     |
| E 2       | sol         |            80 |        90 | verdadeiro | não     |
| E 8       | sol         |            72 |        95 | falso      | não     |
| E 9       | sol         |            69 |        70 | falso      | sim     |
| E 11      | sol         |            75 |        70 | verdadeiro | sim     |

<!-- image -->

| Ventando   |   sim |   não |   Total | Jogar   |    |
|------------|-------|-------|---------|---------|----|
| falso      |     1 |     2 |       3 | sim     |  2 |
| verdadeiro |     1 |     1 |       2 | não     |  3 |
| Total      |     2 |     3 |       5 | Total   |  5 |

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 4       | chuva       |            70 |        96 | falso      | sim     |
| E 5       | chuva       |            68 |        80 | falso      | sim     |
| E 6       | chuva       |            65 |        70 | verdadeiro | não     |
| E 10      | chuva       |            75 |        80 | falso      | sim     |
| E 14      | chuva       |            71 |        91 | verdadeiro | não     |

| Temperatura   | Temperatura   | 69      | 69      | 72      | 75      | 80   | 85   |
|---------------|---------------|---------|---------|---------|---------|------|------|
| Jogar         | Jogar         | sim     | sim     | não sim | não sim | não  | não  |
| Umidade       | 70            | 70      | 85 90   | 85 90   | 95      |      |      |
| Jogar         | sim sim       | sim sim | não não | não não | não     |      |      |

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

0.95098  bits ) info(Ventando , = T

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## Escolha do Atributo Escolha do Atributo ' 'Umidade Umidade' ' para para Particionar Particionar ' 'Aparência=sol Aparência=sol' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 4       | chuva       |            70 |        96 | falso      | sim     |
| E 5       | chuva       |            68 |        80 | falso      | sim     |
| E 6       | chuva       |            65 |        70 | verdadeiro | não     |
| E 10      | chuva       |            75 |        80 | falso      | sim     |
| E 14      | chuva       |            71 |        91 | verdadeiro | não     |

<!-- image -->

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 9       | sol         |            69 |        70 | falso      | sim     |
| E 11      | sol         |            75 |        70 | verdadeiro | sim     |

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 1       | sol         |            85 |        85 | falso      | não     |
| E 2       | sol         |            80 |        90 | verdadeiro | não     |
| E 8       | sol         |            72 |        95 | falso      | não     |

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=chuva Aparência=chuva' '

| Temperatura Jogar   | 65      | 65   | 68 sim   | 68 sim   | 70 sim   | 71 não   | 75 sim   |
|---------------------|---------|------|----------|----------|----------|----------|----------|
| Umidade             | Umidade | 70   | 70       | 80       | 91       | 91       | 96       |
| Jogar               |         | não  | não      | sim sim  | não      | não      | sim      |

| Ventando   |   sim |   não |   Total | Jogar   |    |
|------------|-------|-------|---------|---------|----|
| falso      |     3 |     0 |       3 | sim     |  3 |
| verdadeiro |     0 |     2 |       2 | não     |  2 |
| Total      |     3 |     2 |       5 | Total   |  5 |

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=chuva Aparência=chuva' '

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=chuva Aparência=chuva' '

<!-- image -->

## Escolha do Atributo para Particionar Escolha do Atributo para Particionar ' 'Aparência=chuva Aparência=chuva' '

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 4       | chuva       |            70 |        96 | falso      | sim     |
| E 5       | chuva       |            68 |        80 | falso      | sim     |
| E 6       | chuva       |            65 |        70 | verdadeiro | não     |
| E 10      | chuva       |            75 |        80 | falso      | sim     |
| E 14      | chuva       |            71 |        91 | verdadeiro | não     |

| Temperatura   | 65      | 65   | 68   | 68      | 70      | 71   | 75   |
|---------------|---------|------|------|---------|---------|------|------|
| Jogar         | não     | não  | sim  | sim     | sim     | não  | sim  |
| Umidade       | Umidade | 70   | 70   | 80      | 80      | 91   | 96   |
| Jogar         | Jogar   | não  | não  | sim sim | sim sim | não  | sim  |

| Ventando   |   sim |   não |   Total | Jogar   |    |
|------------|-------|-------|---------|---------|----|
| falso      |     3 |     0 |       3 | sim     |  3 |
| verdadeiro |     0 |     2 |       2 | não     |  2 |
| Total      |     3 |     2 |       5 | Total   |  5 |

<!-- image -->

## Escolha do Atributo Escolha do Atributo ' 'Ventando Ventando' ' para para Particionar Particionar ' 'Aparência=chuva Aparência=chuva' '

<!-- image -->

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 4       | chuva       |            70 |        96 | falso      | sim     |
| E 5       | chuva       |            68 |        80 | falso      | sim     |
| E 10      | chuva       |            75 |        80 | falso      | sim     |

| Exemplo   | Aparência   |   Temperatura |   Umidade | Ventando   | Jogar   |
|-----------|-------------|---------------|-----------|------------|---------|
| E 6       | chuva       |            65 |        70 | verdadeiro | não     |
| E 14      | chuva       |            71 |        91 | verdadeiro | não     |

## Á Árvore de Decisão Induzida rvore de Decisão Induzida

<!-- image -->

## Poda Poda

- /boxshadowdwn Há duas formas de produzir árvores mais simples
- /square4 pré-poda : decide-se não mais particionar o conjunto de treinamento, utilizando algum critério
- /square4 pós-poda : induz-se a árvore completa e então remove-se alguns dos ramos
- /boxshadowdwn A poda invariavelmente causará a classificação incorreta de exemplos de treinamento
- /boxshadowdwn Conseqüentemente, as folhas não necessariamente conterão exemplos de uma única classe

## Pr Pré é- -Poda Poda

- /boxshadowdwn Evita gastar tempo construindo estruturas (sub-árvores) que não serão usada na árvore final simplificada
- /boxshadowdwn O método usual consiste em analisar a melhor forma de particionar um subconjunto, mensurando-a sob o ponto de vista de significância estatística, ganho de informação, redução de erro ou outra métrica qualquer
- /boxshadowdwn Se a medida encontrada encontrar-se abaixo de um valor limite ( threshold ) o particionamento é interrompido e a árvore para aquele subconjunto é apenas a folha mais apropriada
- /boxshadowdwn Entretanto, a definição do valor limite não é simples de ser definido
- /square4 Um valor muito grande pode terminar o particionamento antes que os benefícios de divisões subseqüentes tornem-se evidentes
- /square4 Um valor muito pequeno resulta em pouca simplificação

## P Pó ós s- -Poda Poda

- /boxshadowdwn O processo de indução ( dividir-e-conquistar ) da árvore continua de forma livre e então a árvore super-ajustada ( overfitted tree ) produzida é então podada
- /boxshadowdwn O custo computacional adicional investido na construção de partes da árvore que serão posteriormente descartadas pode ser substancial
- /boxshadowdwn Entretanto, esse custo é compensador devido a uma maior exploração das possíveis partições
- /boxshadowdwn Crescer e podar árvores é mais lento, mas mais confiável

## P Pó ós s- -Poda Poda

- /boxshadowdwn Existem várias forma de avaliar a taxa de erro de árvores podadas, dentre elas
- /square4 avaliar o desempenho em um subconjunto separado do conjunto de treinamento (o que implica que uma parte dos exemplos devem ser reservada para a poda e, portanto, a árvore tem que ser construída a partir de um conjunto de exemplos menor)
- /square4 avaliar o desempenho no conjunto de treinamento, mas ajustando o valor estimado do erro, já que ele tem a tendência de ser menor no conjunto de treinamento

## Interpreta Interpretaç ção Geom ão Geomé étrica trica

- /boxshadowdwn Consideramos exemplos como um vetor de m atributos
- /boxshadowdwn Cada vetor corresponde a um ponto em um espaço m-dimensional
- /boxshadowdwn A AD corresponde a uma divisão do espaço em regiões, cada região rotulada como uma classe

## Interpreta Interpretaç ção Geom ão Geomé étrica: Atributo trica: Atributo- Valor Valor

- /boxshadowdwn
- Um teste para um atributo é da forma Xi op Valor
- onde X i é um atributo, op ∈ {=, ≠ ,&lt;, ≤ ,&gt;, ≥ } e valor é uma constante válida para o atributo
- /boxshadowdwn O espaço de descrição é particionado em regiões retangulares, nomeadas hiperplanos, que são ortogonais aos eixos
- /boxshadowdwn As regiões produzidas por uma AD são todas hiperplanos
- /boxshadowdwn Enquanto a árvore está sendo formada, mais regiões são adicionadas ao espaço

## Interpreta Interpretaç ção Geom ão Geomé étrica p/ DT trica p/ DT

<!-- image -->

## Interpreta Interpretaç ção Geom ão Geomé étrica p/ DT trica p/ DT

<!-- image -->

## Interpreta Interpretaç ção Geom ão Geomé étrica p/ DT trica p/ DT

<!-- image -->

## Interpreta Interpretaç ção Geom ão Geomé étrica p/ DT trica p/ DT

<!-- image -->

## Combina Combinaç ção Linear de Atributos ão Linear de Atributos

- /boxshadowdwn Produzem árvores de decisão oblíquas
- /boxshadowdwn A representação para os testes são da forma

<!-- formula-not-decoded -->

onde a i é uma constante, X i é um atributo real, op ∈ {&lt;, ≤ ,&gt;, ≥ } e Valor uma constante

- /boxshadowdwn O espaço de descrição é particionado hiperplanos que não são necessariamente ortogonais ao eixos

## Á Árvore de Decisão Obl rvore de Decisão Oblí íqua qua

<!-- image -->

<!-- image -->

<!-- image -->

X1

## Resumo Resumo

- /boxshadowdwn Árvores de decisão, em geral, possuem um tempo de aprendizado relativamente rápido
- /boxshadowdwn Árvores de decisão permitem a classificação de conjuntos com milhões de exemplos e centenas de atributos a uma velocidade razoável
- /boxshadowdwn É possível converter para regras de classificação, podendo ser interpretadas por seres humanos
- /boxshadowdwn Precisão comparável a outros métodos