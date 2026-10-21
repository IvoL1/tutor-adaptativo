# Referência — Pacote de estudo autônomo (estudar sozinho, sem o Claude e sem internet)

> Leia quando eu pedir `"pacote"`, disser "quero estudar X sozinho / sem depender de você / por N horas por dia", pedir material para imprimir, ou quando eu quiser que você planeje a matéria inteira de uma vez. Aqui o Claude **monta** tudo uma vez; depois **eu estudo sozinho**, em Markdown e PDF, sem conversa e sem rede.

> **Nesta referência:**
> **1. A ideia**
> **2. As etapas (0 a 7)**
> **3. Quanto cabe em um dia (tempos)**
> **4. Como escrever o material para quem estuda sozinho**
> **5. Modelos dos arquivos**
> **6. Se algo mudar depois**

## 1. A ideia

- **O Claude usa a internet e os meus anexos só na hora de montar.** Pesquisa a fonte oficial e atual, lê o que eu anexei, e escreve tudo dentro dos arquivos: explicação, exemplo, exercício, dica, gabarito, revisão, prova. Depois disso, **nada no pacote manda eu consultar a internet ou o Claude**.
- **O tempo é o eixo.** Eu digo quantas horas por dia tenho (ex.: 4). O pacote é montado em **dias que fecham essas horas** (ler, entender, tirar dúvida, fazer junto, exercícios, desafio, projeto, prova), na **ordem correta de pré-requisitos e dificuldade**, e diz **até onde a matéria chega** em N dias. Nenhum dia exige algo que só um tópico ainda não estudado ensina.
- **Quem calcula é o código.** `pacote.py planejar` ordena pelos pré-requisitos, distribui os blocos nos dias, reserva a revisão espaçada e mostra até onde cabe; `pacote.py conferir` mede o material escrito contra o tempo prometido. Não estime a mão nem diga "deve dar 4 horas".
- **Isto não substitui a aula ao vivo.** A aula ao vivo (Regras 2 e 4: sondagem, ciclo, quiz na hora) continua existindo; o pacote é o **outro modo**, para quando eu quero estudar sozinho. Os dois podem coexistir na mesma matéria.

## 2. As etapas

### Etapa 0 — Entender o pedido (perguntas curtas, com opções)

Eu me expresso mal quando preciso descrever com palavras livres. **Pergunte com opções** (`references/ferramentas.md` → "Perguntas com opções"), uma coisa por vez, e **repita o que entendeu em 2–3 linhas antes de começar** o trabalho grande. Só pergunte o que não dá para deduzir:

1. **Horas por dia** (obrigatório): 1, 2, 3, 4, 6 ou outro. Se eu disser dias da semana ou prazo, anote (ex.: "só de segunda a sexta").
2. **O que quero ao final** (a meta): em opções concretas para a matéria (ex.: "conseguir ler código", "fazer um projeto meu", "passar numa prova"). Define o projeto do pacote.
3. **Meu ponto de partida**: "do zero", "já conheço o básico" ou "listar o que já sei". Se não souber, o pacote começa com o **Dia 0 — teste de nível**, que eu corrijo sozinho (Etapa 4) e que diz quais tópicos posso pular.
4. **Anexos**: se tenho PDFs, apostilas, links ou anotações para usar (caminho de arquivo ou pasta, ou `fontes/` da matéria). Se não tenho, o pacote usa só fontes oficiais.
5. **Versão ou edição**, se a matéria tiver (Regra 28): confirme a atual estável na pesquisa e congele.

### Etapa 1 — Fontes (obrigatória, com internet)

1. **Leia os meus anexos primeiro** (`Read`; PDF por páginas). Eles dizem o escopo e a ênfase que eu quero.
2. **Pesquise a fonte oficial e atual** com o `tutor-pesquisador`: documentação oficial da versão estável atual, especificação, livro-texto de referência, pré-requisitos reais, ordem usual de ensino, erros comuns. Regras 8, 25, 26 e 28 valem inteiras: nada desatualizado, matéria composta filtra o que é atual, versão congelada, artigos só como pista.
3. **Anexo contra fonte oficial:** o anexo manda no **escopo**; a fonte oficial manda no **fato**. Se discordarem, não escolha em silêncio: ensine o que a fonte oficial atual diz e **registre a divergência** na seção "Fontes" do `plano.md`.
4. **Sem internet ou sem o pesquisador agora:** diga isso no início e **não prometa atualidade**. Monte só com os anexos e com o que você sabe com segurança, marque `verificado: não` no `plano.md` e no `LEIA-ME.md`, e ofereça rodar a verificação depois (seção 6).
5. Guarde para o `plano.md`: título, link e data de cada fonte usada. O pacote já leva o essencial; **o link é só para eu saber de onde veio**, nunca uma tarefa.

### Etapa 2 — O currículo (o mapa, em dados)

Decomponha a matéria em **partes → tópicos → blocos**, e escreva `curriculo.json` (formato no cabeçalho de `scripts/pacote.py`):

- **Tópico:** uma ideia coesa que cabe em 1–3 blocos de cada tipo. `id` curto (`t01`), `titulo`, `parte`, `dificuldade` (1 a 5) e `pre` (lista de ids).
- **Pré-requisitos de verdade.** Para cada tópico: *que outro tópico (ou conhecimento) precisa vir antes, e por quê?* Teste as raízes como no Plano (`references/ensino.md` → "Fase 2 — Plano"): o que parece fundamental pode ser teorema disfarçado. O que a matéria exige de **fora** dela (ex.: JavaScript para TypeScript) vira **tópicos de base** no início, ou, se for grande demais, vai em "Antes de começar" no `LEIA-ME.md` com o que eu preciso saber, **e um mini teste**.
- **Dificuldade sobe em degraus.** Dois tópicos seguidos não saltam mais de 2 níveis (o script avisa). Reprodução → modificação → extensão → criação dentro de cada tópico (Regra 15). Depois de um tópico 4–5, um tópico mais leve ou de revisão.
- **Blocos** (tipos: `ler`, `junto`, `exercicios`, `desafio`, `projeto`, `prova`) e minutos, pela tabela da seção 3. Cada bloco entre 5 e 90 min; quebre os maiores.
- **Prova** ao fim de cada parte e de cada tópico grande (Regra 17); **checkpoint** a cada 3 tópicos como bloco `projeto` ou `exercicios` mistos (Regra 20); **projeto de prática** que cresce ao longo da trilha, nunca de uma vez só no fim (Regra 7: passe pela Análise de Cobertura de `references/projetos.md`).
- **Exercícios soltos nunca se misturam com o projeto** (Regra 30): os soltos ficam no dia; o projeto cresce em `pratica/projeto/` (a minha pasta; o pacote só descreve o que fazer).

### Etapa 3 — O cronograma (o código calcula, eu aprovo)

1. Rode `python "<pasta>/pacote.py" planejar caminho/curriculo.json --horas N` (no Windows, `py`; `--json` dá os dados). Se eu já sei tópicos: `--ja-sei t01,t02`.
2. Leia o que ele devolve: **erros** (corrija o JSON), **avisos** (salto de dificuldade, tópico difícil sem pré-requisito: resolva ou justifique), **ordem ajustada** (o script mexeu para respeitar pré-requisitos: confirme que faz sentido) e a tabela **"Até onde cabe"**.
3. **Mostre ao Ivo**: quantos dias, o que fecha em cada dia em uma linha e **até onde chega com o tempo que ele tem** (a tabela "Até onde cabe"). **Pare e espere o "ok"** (Regra 5). Se for grande demais para o prazo dele, ofereça cortar tópicos do fim, não encurtar os blocos.
4. **Gerar tudo de uma vez costuma ser grande demais.** Ofereça gerar **os primeiros 7 dias** e o resto depois (`"gerar mais dias"`). O cronograma e o `plano.md` cobrem **a matéria inteira** desde o começo; só o texto dos dias é gerado em lotes.

### Etapa 4 — Escrever o pacote

Pasta: `{RAIZ}/{matéria}/pacote/` (crie a matéria só com essa pasta se ela ainda não existir; **não** crie os registros da skill nem toque em `pratica/`). Conteúdo e modelos na seção 5. Em resumo:

- `LEIA-ME.md`, `plano.md` (com `horas_por_dia` no frontmatter), `curriculo.json`, `acompanhamento.md`.
- `dias/dia-NN.md` — um arquivo por dia, **com todo o texto necessário para estudar o dia**, em seções `## N. Tipo — título (M min)` que somam o tempo do dia.
- `gabaritos/dia-NN.md` — soluções, correção das provas e erros comuns, **separados** para eu não ver sem querer.
- `anexos/` — imagens e diagramas **como arquivos locais** (SVG/PNG).
- `pdf/` — gerado na Etapa 6.

Escreva o conteúdo conforme a seção 4. Mantenha cada dia **dentro dos minutos que o cronograma deu**: os blocos e os minutos de cada dia vêm do `pacote.py planejar` (use `--json`), **não da sua cabeça**. Escreva em lotes por dia, conferindo (Etapa 5) a cada lote.

- **Dia 0 (opcional, se eu não sei meu nível):** teste de nível de 20–40 min, em ordem de dificuldade, com gabarito e **uma regra de pulo por tópico** ("acertou 4 de 5 em t01 → pule t01"). Depois do teste eu digo ao Claude (ou eu mesmo reordeno, seção 6) quais tópicos pular.
- **Diagramas:** gere o SVG/PNG **agora, com internet**, validando com `render.py` (`references/visuais.md`), e salve em `anexos/`, referenciando com `![descrição](../anexos/arquivo.svg)`. **Nunca** bloco ` ```mermaid ` nem fórmula `$…$` no pacote: sem internet eles não aparecem. Fórmula vai em texto/Unicode (`x² + y² = r²`) ou numa imagem.

### Etapa 5 — Conferir (o código mede)

`python "<pasta>/pacote.py" conferir "{RAIZ}/{matéria}/pacote"`. Ele checa, por dia: a soma dos minutos contra as horas por dia; frontmatter igual à soma; leitura longa demais para o tempo declarado; exercício sem "Critério de pronto"; falta de gabarito; imagem inexistente; fórmula LaTeX ou mermaid. **Corrija até não sobrar `FALHA`** e diga o resultado como veio. O que o script não mede (se a explicação está boa) é com você: releia um dia inteiro como se fosse eu, sozinho, sem ninguém para perguntar.

### Etapa 6 — PDF para imprimir

`python "<pasta>/apostila.py" --pacote "{RAIZ}/{matéria}/pacote"` gera `pdf/plano.pdf`, `pdf/dia-NN.pdf` e `pdf/gabarito-dia-NN.pdf` (gabarito **separado**, para imprimir à parte). Funciona sem internet e usa o Chrome ou o Edge já instalados; sem eles gera `.html` prontos para imprimir (Ctrl+P → Salvar como PDF, em qualquer navegador). Para ler na tela: `python "<pasta>/ver.py" "{RAIZ}" "{matéria}/pacote/plano.md" --abrir`.

### Etapa 7 — Entregar

Diga em poucas linhas: onde está a pasta, quantos dias foram gerados e de quantos, **como começar** ("abra `LEIA-ME.md` e depois `dias/dia-01.md`") e o resultado do `conferir`. Não repita o conteúdo no terminal.

## 3. Quanto cabe em um dia (tempos)

Estime os blocos com estes valores e **corrija pelo meu ritmo** quando eu disser que o tempo estava curto ou longo (anote no `plano.md`). O `conferir` pega o texto de leitura longo demais.

| Bloco | Tempo | O que é | Tamanho do texto |
|---|---|---|---|
| `ler` | 20–40 min | explicação de uma ideia, com porquê, exemplo e checagem | cerca de 1 000 a 2 500 palavras por bloco de 30 min (o `conferir` aceita até 150 palavras/min + 25%) |
| `junto` | 20–40 min | passo a passo para eu fazer junto com o texto, com o resultado esperado de cada passo | passos curtos e numerados |
| `exercicios` | 30–60 min | 4–8 exercícios, reprodução → modificação → extensão; ~10–15 min cada, ~20–25 os de criação | enunciado + critério + dicas |
| `desafio` | 20–40 min | uma variação mais difícil, para tópicos de dificuldade 3+ | um enunciado |
| `projeto` | 60–90 min | um passo do projeto de prática (nunca o projeto inteiro) | roteiro do passo |
| `prova` | 15–30 min | 8–15 questões de múltipla escolha ou aplicadas, sem consulta | caderno + gabarito à parte |

- **Revisão espaçada:** o código reserva ~6 min por tópico que acabou há 1, 3, 7 e 16 dias (no máximo 15% do dia) e diz quais. Escreva 2–3 perguntas por tópico no bloco "Revisão" do dia, com a resposta dobrada.
- **Pausas:** 10 min a cada 50 min de estudo; **não entram** nos minutos do dia (o dia mostra quantas).
- **Dia curto:** os blocos que são o essencial do dia levam ★ no roteiro. Se hoje só tenho metade do tempo, faço só os ★ (Regra 13).
- Um dia pode passar até 10% do tempo para não cortar um bloco ao meio; o último dia de conteúdo e o dia de fechamento podem ser mais curtos.

## 4. Como escrever o material para quem estuda sozinho

Sem ninguém para perguntar, **o texto precisa responder as perguntas que o Claude responderia ao vivo**. Os princípios do ensino valem (`references/ensino.md`, `references/pedagogia.md`); aqui está como eles aparecem no papel.

1. **Cada ideia nova:** o **porquê** (por que alguém precisaria disso), o **chão** (apoiado em algo que já vi no pacote), a **conexão** com o que veio antes e uma **checagem** (pergunta curta com a resposta dobrada em `<details>` logo abaixo). Uma ideia por vez, nunca duas novas sem um exercício no meio (Regra 14).
2. **Dúvidas antecipadas.** Todo bloco `ler` termina com **"Dúvidas que costumam aparecer"**: 2–4 perguntas reais de quem está aprendendo aquilo, com resposta curta. É o substituto de "perguntar ao Claude".
3. **"Se travar".** Todo bloco de exercício diz o que fazer, nesta ordem: releia o trecho X; use a dica 1; tente de novo; use a dica 2; **pule, faça o próximo e volte**; anote a dúvida em `acompanhamento.md`. Dificuldade é normal (Regra 12); nunca "é fácil".
4. **Fazer junto:** cada passo diz **o que fazer** e **o que deve aparecer/acontecer**. Se eu errar, eu comparo e vejo na hora, sem ninguém.
5. **Exercícios:** enunciado sem ambiguidade, **texto de apoio pronto** quando pedir texto (Regra 27), **Critério de pronto** (o que devo conseguir/observar ao acertar, sem dar a solução) e **escada de 3 dicas dobradas** (`<details><summary>Dica 1</summary>…</details>`), a última ainda sem a solução (Regra 9). Resposta e solução **só** no `gabaritos/dia-NN.md`.
6. **Gabarito:** a solução, **por que** funciona, **o erro mais comum** e **uma melhoria** (Regra 29). Para cada exercício, "se você errou assim, o problema é isto". Antes de olhar, eu marco 🟢🟡🔴 no `acompanhamento.md` (calibração, Regra 19).
7. **Provas e quizzes:** alternativas pelo procedimento de `references/avaliacao.md`; **a posição da certa varia sem padrão**; cada errada tem o **equívoco que revela** no gabarito; use `quiz.py montar` para receber os avisos de alternativa que se entrega pela forma e refaça o que ele acusar. "Não sei" é resposta válida e distinta de erro. Correção no gabarito: a certa, o porquê e **qual seção reler** para cada erro. **Regra: 80% ou mais, passo; abaixo, refaço o bloco indicado e repito a prova** (Regras 16–17).
8. **Fonte e versão:** o `plano.md` diz a versão congelada; o texto ensina só o que é atual (Regras 25–28). Nada de "antigamente se fazia assim".
9. **Prática antes da teoria** quando der (Regra 14): mostre rodando/fazendo, depois nomeie.
10. **Tom:** português do Brasil, frases completas, sem pressa e sem condescendência; celebre antes de corrigir mesmo no papel ("se você chegou aqui, já tem X"). Nunca "é fácil" nem "óbvio".
11. **Matéria sem tela** (idioma, música, matemática, concurso): o mesmo molde. Áudio, partitura ou imagem que o texto não substitui: diga no pacote exatamente **o que preciso ter em mãos** e não dependa de baixar nada na hora; se for imprescindível, ponha o arquivo em `anexos/` (somente de fonte confiável e com crédito, `references/visuais-modelos.md`).

## 5. Modelos dos arquivos

### `curriculo.json` (você escreve, o `pacote.py` lê)

```json
{
  "materia": "TypeScript",
  "horas_por_dia": 4,
  "topicos": [
    {"id": "t01", "titulo": "Tipos básicos", "parte": "Fundamentos", "dificuldade": 1, "pre": [],
     "blocos": [{"tipo": "ler", "min": 30}, {"tipo": "junto", "min": 30}, {"tipo": "exercicios", "min": 45}]}
  ]
}
```

### `plano.md`

```markdown
---
materia: TypeScript
horas_por_dia: 4
versao: TypeScript 5.x (edição estável atual na data de criação)
criado_em: AAAA-MM-DD
verificado: sim
---
# Plano — TypeScript (4 h por dia)

## Em uma tela
- Dias: N · tópicos: N · meta: …
- Como estudar: abra `dias/dia-01.md`, faça as seções na ordem, depois confira em `gabaritos/dia-01.md`.

## Mapa (ordem de estudo)
| Tópico | Parte | Dificuldade | Depende de | Dia |
|---|---|---|---|---|

## Cronograma
(cole aqui a saída de `pacote.py planejar`, incluindo "Até onde cabe")

## Fontes
- Título — link — data da fonte — para que serviu
- Divergências entre os meus anexos e a fonte oficial: …
```

### `LEIA-ME.md`

Para quem abre a pasta pela primeira vez: o que é, como começar, **como estudar um dia** (ordem das seções, pausas, o que fazer ao travar), como usar o gabarito (só depois de tentar), como preencher o `acompanhamento.md`, o que fazer se atrasar ou faltar tempo (seção 6) e **"Antes de começar"** (o que preciso saber/ter). Curto: cabe em uma tela e meia. Sem link nem tarefa de internet.

### `dias/dia-NN.md`

```markdown
---
dia: 3
minutos: 245
---
# Dia 3 — Funções e interfaces

> Hoje: 245 min · pausa de 10 min a cada 50. Dia curto? Faça só as seções com ★.
> Ontem você fechou: … · Hoje você vai conseguir: …

## Roteiro do dia
| # | Min | Bloco |
|---|---|---|
| 1 | 12 | Revisão espaçada |
| 2 | 35 | Ler e entender ★ |
| 3 | 35 | Fazer junto ★ |
| 4 | 50 | Exercícios ★ |

## 1. Revisão — o que já vi (12 min)
(2–3 perguntas por tópico vencido; resposta dobrada)

## 2. Ler — Funções tipadas (35 min)
(texto; checagens com resposta dobrada; termina com "Dúvidas que costumam aparecer")

## 3. Fazer junto — … (35 min)
## 4. Exercícios — … (50 min)
**Critério de pronto:** …
(exercícios 1…N, cada um com a escada de 3 dicas dobradas)

## Fechamento do dia
- [ ] Marquei no `acompanhamento.md` o que fiz e a confiança (🟢🟡🔴).
- Amanhã: …
```

Os títulos das seções seguem **exatamente** `## N. Tipo — título (M min)` com o Tipo começando por *Revisão, Ler, Fazer junto, Exercícios, Desafio, Projeto* ou *Prova*: é o que o `conferir` lê. Dia de **fechamento** (só revisão): coloque `fechamento: sim` no frontmatter.

### `gabaritos/dia-NN.md`

```markdown
# Gabarito — Dia 3
> Só abra depois de tentar. Marque 🟢🟡🔴 no `acompanhamento.md` **antes** de olhar.

## Exercício 1
**Resposta:** …
**Por quê:** …
**Se você errou assim:** … → releia a seção 2 (“…”).
**Uma melhoria:** …

## Prova
| Questão | Certa | Por que as outras estão erradas |
|---|---|---|
**Pontuação:** acertos/total = %. 80% ou mais: passei. Abaixo: reler as seções indicadas e repetir a prova.
```

### `acompanhamento.md`

Tabela que **eu** preencho (por dia: feito, confiança, tempo real, dúvida em aberto), a tabela de provas (nota e data) com a média que eu calculo, e a lista "Dúvidas em aberto" (para levar ao Claude **se eu quiser**; o pacote não depende disso). É o único arquivo do pacote em que eu escrevo.

## 6. Se algo mudar depois

- **Atrasei ou faltei um dia:** não pule nada. Faço o dia seguinte; o calendário só desloca. Os dias de revisão continuam valendo.
- **Já sei um tópico / quero pular:** se tenho o Claude por perto, ele roda `pacote.py planejar --ja-sei …` e regera só os dias afetados (os arquivos antigos não são apagados; o Claude cria os novos e o `plano.md` aponta). Sozinho: pulo as seções do tópico e faço a prova dele; passando em 80%, sigo.
- **Mudou a minha disponibilidade de horas:** o Claude roda `planejar --horas N` e regera o cronograma; o conteúdo dos tópicos continua, só muda em que dia cai cada bloco.
- **Verificar/atualizar o pacote:** quando eu pedir `"atualizar pacote"` (com internet), o `tutor-pesquisador` confere a versão e os fatos centrais contra a fonte oficial atual; a mudança é listada e o `plano.md` ganha a data da verificação. Sem isso, o pacote vale pela data de criação e **o `LEIA-ME.md` diz essa data**.
- **Gerar mais dias:** `"gerar mais dias"`: continue do último `dias/dia-NN.md` existente, com o mesmo `curriculo.json`, conferindo cada lote.
- **O pacote nunca grava em `pratica/`** (é minha) e **nunca sobrescreve** um arquivo meu. `acompanhamento.md` só é criado, nunca regravado depois que eu comecei a preenchê-lo.
