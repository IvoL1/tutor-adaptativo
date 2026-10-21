# Referência — Pacote de estudo autônomo (estudar sozinho, sem o Claude e sem internet)

> **Este é o modo padrão.** Leia sempre que eu quiser estudar, aprender, revisar ou entender uma matéria ("quero aprender X", "me ensina X", "monta um curso de X"), pedir `"pacote"`, material para imprimir ou plano de estudos. Só use a aula ao vivo se eu pedir. Aqui o Claude **monta** tudo uma vez; depois **eu estudo sozinho**, em Markdown e PDF, sem conversa, sem terminal e sem rede.

> **Nesta referência:**
> **1. A ideia**
> **2. As etapas (0 a 7)**
> **3. Quanto cabe em um dia (tempos)**
> **4. Como escrever o material para quem estuda sozinho**
> **5. Modelos dos arquivos**
> **6. Se algo mudar depois**

## 1. A ideia

- **O objetivo é o material ser suficiente em si mesmo.** Depois de entregue, não preciso de mais nada além da pasta: nem do Claude, nem do terminal, nem de comando, nem de Python, nem de internet, nem de outro livro. Se uma explicação, um exemplo, uma dica, um gabarito ou um passo de instalação não estiver escrito dentro do pacote, o pacote está incompleto.
- **O Claude usa a internet e os meus anexos só na hora de montar** (e a internet só se houver; ver Etapa 1). Pesquisa a fonte oficial e atual, lê o que eu anexei, e escreve tudo dentro dos arquivos: explicação, exemplo, exercício, dica, gabarito, revisão, prova. **Nada no pacote manda eu consultar a internet, o Claude ou outro material.**
- **O tempo é o eixo.** Eu digo quantas horas por dia tenho (ex.: 4). O pacote é montado em **dias que fecham essas horas** (ler, entender, tirar dúvida, fazer junto, exercícios, desafio, projeto, prova), na **ordem correta de pré-requisitos e dificuldade**, e diz **até onde a matéria chega** em N dias. Nenhum dia exige algo que só um tópico ainda não estudado ensina.
- **A matéria inteira, de uma vez.** O pacote cobre o currículo todo, do primeiro ao último dia, na mesma montagem. Não entregue "os primeiros dias" esperando eu pedir o resto, e não pare no meio para perguntar se continua.
- **Quem calcula é o código.** `pacote.py planejar` ordena pelos pré-requisitos, distribui os blocos nos dias, reserva a revisão espaçada e mostra até onde cabe; `pacote.py conferir` mede o material escrito contra o tempo prometido **e acusa o que me mandaria sair do pacote**. Não estime a mão nem diga "deve dar 4 horas".
- **Sem conversa depois.** Nada de "quer que eu continue?", "me diga o que achou", quiz que espera resposta no terminal ou menu de próximos passos. A avaliação é feita **por mim, no papel**, com o gabarito do pacote. A aula ao vivo continua existindo como modo opcional (só se eu pedir); o pacote é o padrão.

## 2. As etapas

### Etapa 0 — Entender o pedido (no máximo uma pergunta)

Eu me expresso mal quando preciso descrever com palavras livres, e **cada pergunta é uma volta a mais no terminal**. Por isso: **deduza tudo o que der e pergunte só o que não dá.**

1. **Horas por dia** — a única pergunta que vale parar para fazer, **uma só, com opções** (`references/ferramentas.md` → "Perguntas com opções"): 1, 2, 3, 4, 6 ou "não sei: assuma 2 h". Se eu já disse as horas (ou dias da semana/prazo) no pedido, **não pergunte nada**: vá direto ao trabalho. Se eu não responder ou escolher "não sei", assuma 2 h e escreva isso no `00-LEIA-ME.md`.
2. **O que quero ao final (a meta):** deduza do pedido ("quero ler código", "passar na prova X"); sem pista, assuma a meta mais comum da matéria (usar o assunto de forma prática) e **escreva a meta assumida** no `01-plano.md`. Não pergunte.
3. **Meu ponto de partida:** assuma "do zero" quando eu não disser. O pacote começa então com o **Dia 0 — teste de nível**, que eu corrijo sozinho e que diz quais tópicos posso pular (regra de pulo por tópico; ver seção 6 para pular).
4. **Anexos:** use o que eu citei no pedido e o que houver em `fontes/` da matéria (`Glob`). Não pergunte "tem anexo?".
5. **Versão ou edição**, se a matéria tiver (Regra 28): confirme a atual estável na pesquisa e congele. Não pergunte.

Antes de começar o trabalho grande, **diga em 2–3 linhas o que entendeu e o que assumiu**, e **comece em seguida, sem esperar resposta**. Eu corrijo depois se quiser.

### Etapa 1 — Fontes (com internet, se houver)

1. **Leia os meus anexos primeiro** (`Read`; PDF por páginas). Eles dizem o escopo e a ênfase que eu quero.
2. **Se houver internet, pesquise a fonte oficial e atual** com o `tutor-pesquisador`: documentação oficial da versão estável atual, especificação, livro-texto de referência, pré-requisitos reais, ordem usual de ensino, erros comuns. Regras 8, 25, 26 e 28 valem inteiras: nada desatualizado, matéria composta filtra o que é atual, versão congelada, artigos só como pista.
3. **Anexo contra fonte oficial:** o anexo manda no **escopo**; a fonte oficial manda no **fato**. Se discordarem, não escolha em silêncio: ensine o que a fonte oficial atual diz e **registre a divergência** na seção "Fontes" do `01-plano.md`.
4. **Sem internet, sem o pesquisador ou com a busca negada:** **não pare e não peça nada.** Monte só com os anexos e com o que você sabe com segurança, marque `verificado: não` no `01-plano.md` e no `00-LEIA-ME.md` (com a data) e diga isso na entrega. A internet melhora o pacote, mas o pacote não depende dela.
5. Guarde para o `01-plano.md`: título, link e data de cada fonte usada. O pacote já leva o essencial; **o link é só registro de onde veio, só no `01-plano.md`, nunca uma tarefa** e nunca nos dias, gabaritos ou `LEIA-ME.md`.

### Etapa 2 — O currículo (o mapa, em dados)

Decomponha a matéria em **partes → tópicos → blocos**, e escreva `_interno/curriculo.json` (formato no cabeçalho de `scripts/pacote.py`):

- **Tópico:** uma ideia coesa que cabe em 1–3 blocos de cada tipo. `id` curto (`t01`), `titulo`, `parte`, `dificuldade` (1 a 5) e `pre` (lista de ids).
- **Pré-requisitos de verdade.** Para cada tópico: *que outro tópico (ou conhecimento) precisa vir antes, e por quê?* Teste as raízes como no Plano (`references/ensino.md` → "Fase 2 — Plano"): o que parece fundamental pode ser teorema disfarçado. O que a matéria exige de **fora** dela (ex.: JavaScript para TypeScript) vira **tópicos de base** no início, ou, se for grande demais, vai em "Antes de começar" no `00-LEIA-ME.md` com o que eu preciso saber, **e um mini teste**.
- **Dificuldade sobe em degraus.** Dois tópicos seguidos não saltam mais de 2 níveis (o script avisa). Reprodução → modificação → extensão → criação dentro de cada tópico (Regra 15). Depois de um tópico 4–5, um tópico mais leve ou de revisão.
- **Blocos** (tipos: `ler`, `junto`, `exercicios`, `desafio`, `projeto`, `prova`) e minutos, pela tabela da seção 3. Cada bloco entre 5 e 90 min; quebre os maiores.
- **Prova** ao fim de cada parte e de cada tópico grande (Regra 17); **checkpoint** a cada 3 tópicos como bloco `projeto` ou `exercicios` mistos (Regra 20); **projeto de prática** que cresce ao longo da trilha, nunca de uma vez só no fim (Regra 7: passe pela Análise de Cobertura de `references/projetos.md`).
- **Exercícios soltos nunca se misturam com o projeto** (Regra 30): os soltos ficam no dia, e eu faço a resposta em `pratica/treinos/` (minha pasta); o projeto cresce em `pratica/projeto/`. O pacote só descreve o que fazer em cada uma.
- **Toda matéria fecha com a mesma moldura**, para o pacote ter começo, meio e fim: (a) um tópico final **"Prova final e projeto pronto"**, com uma prova integradora de toda a matéria (bloco `prova`) e o último passo do projeto; (b) o dia de fechamento (só revisão) que o `pacote.py` acrescenta sozinho. O `LEIA-ME.md` diz o que significa "terminei" (média das provas e projeto funcionando) e o que estudar a seguir.

### Etapa 3 — O cronograma (o código calcula; sem parada para aprovação)

1. Rode `python "<pasta>/pacote.py" planejar caminho/curriculo.json --horas N` (no Windows, `py`; `--json` dá os dados). Se eu já sei tópicos: `--ja-sei t01,t02`.
2. Leia o que ele devolve: **erros** (corrija o JSON), **avisos** (salto de dificuldade, tópico difícil sem pré-requisito: resolva ou justifique), **ordem ajustada** (o script mexeu para respeitar pré-requisitos: confirme que faz sentido) e a tabela **"Até onde cabe"**.
3. **Não pare para pedir "ok".** Grave o cronograma no `01-plano.md` e siga para escrever. O currículo é a matéria inteira, não um corte pelo prazo: se eu disse um prazo, a tabela "Até onde cabe" mostra onde ele alcança e o pacote continua além, para eu seguir no meu ritmo.
4. **Gere todos os dias, na mesma montagem.** Se o volume for grande, divida em lotes **sem me consultar**: use subagentes em paralelo (cada um recebe o `curriculo.json`, o `01-plano.md`, a seção 4 deste arquivo e a lista de dias que deve escrever, e devolve os arquivos gravados), ou escreva em sequência. Confira cada lote (Etapa 5) e siga até o último dia. `"gerar mais dias"` existe só para retomar uma montagem que foi interrompida (limite de contexto, queda), nunca como parte normal do fluxo.

### Etapa 4 — Escrever o pacote

Pasta: `{RAIZ}/{matéria}/pacote/` (`{matéria}` em slug: sem acento, minúsculas, hifens; crie a matéria só com essa pasta se ela ainda não existir; **não** crie os registros da skill). **Estrutura fixa**, pensada para a ordem de leitura ser óbvia só de olhar a pasta (os números fazem os arquivos aparecerem na ordem em que se lê):

```
pacote/
├── 00-LEIA-ME.md              ← comece aqui (1 tela e meia)
├── 01-plano.md                ← o mapa, o cronograma, "até onde cabe" e as fontes
├── 02-acompanhamento.md       ← ✍️ o único arquivo MEU: o que fiz, confiança, notas, dúvidas
├── 03-glossario.md            ← todo termo novo, em ordem alfabética, com o dia em que aparece
├── dias/
│   ├── dia-01-tipos-basicos.md        ← o dia completo (soma as minhas horas)
│   └── dia-02-funcoes.md
├── gabaritos/                 ← separados, para eu não ver sem querer
│   ├── dia-01-tipos-basicos.md        ← MESMO nome do dia
│   └── dia-02-funcoes.md
├── resumos/
│   └── parte-1-fundamentos.md         ← uma página por parte, para revisar antes da prova
├── anexos/                    ← imagens e diagramas locais (SVG/PNG)
└── _interno/
    └── curriculo.json         ← dados do cronograma (não precisa abrir)
```

- **Nomes:** `dia-NN-assunto.md`, onde `NN` tem zeros à esquerda na largura do total de dias (`01` até `30`, `001` se passar de 99) e `assunto` é o slug do tópico principal do dia. O gabarito tem **exatamente o mesmo nome** do dia. Os resumos são `parte-N-nome.md`. Nada de nome genérico (`nota1.md`, `final.md`).
- **`dias/dia-NN-assunto.md`:** um arquivo por dia, **com todo o texto necessário para estudar o dia**, em seções `## N. Tipo — título (M min)` que somam o tempo do dia, e links "← anterior · próximo →" no fim.
- **`gabaritos/dia-NN-assunto.md`:** soluções, correção das provas e erros comuns.
- **`resumos/parte-N-nome.md`:** os conceitos da parte em uma página (definição em uma linha, um exemplo mínimo e o erro mais comum de cada um); é o que eu releio antes da prova da parte.
- **Sem PDF.** O pacote é só Markdown (eu converto para PDF quando quiser). Não gere `pdf/`; `apostila.py` só roda se eu pedir.
- **`01-plano.md`** leva `horas_por_dia` no frontmatter e uma tabela "Dias" com o link de cada dia.
- **Minha área de prática:** crie também `{RAIZ}/{matéria}/pratica/projeto/` e `pratica/treinos/` **com o `_leia-me.md` de cada uma** (única escrita permitida do pacote em `pratica/`; modelos em `references/templates.md`), para eu saber onde fazer as respostas e o projeto sem criar pasta nenhuma. O `00-LEIA-ME.md` diz isso.

Escreva o conteúdo conforme a seção 4. Mantenha cada dia **dentro dos minutos que o cronograma deu**: os blocos e os minutos de cada dia vêm do `pacote.py planejar` (use `--json`), **não da sua cabeça**. Escreva por dia, conferindo (Etapa 5) a cada lote.
- **Matéria que exige instalar ou ter algo** (programa, ferramenta, material, instrumento): o `00-LEIA-ME.md` → "Antes de começar" lista **exatamente** o que preciso ter e como conferir que está funcionando, tudo escrito dentro do pacote. Instalar costuma precisar de internet uma vez; diga isso com franqueza ali, em vez de me mandar procurar. Prefira exemplos que rodem com o mínimo possível instalado.

- **Dia 0 (opcional, se eu não sei meu nível):** teste de nível de 20–40 min, em ordem de dificuldade, com gabarito e **uma regra de pulo por tópico** ("acertou 4 de 5 em t01 → pule t01"). O próprio teste traz a tabela "se acertou X, pule Y" e o `00-LEIA-ME.md` explica como pular sozinho (seção 6).
- **Diagramas:** gere o SVG/PNG **agora, com internet**, validando com `render.py` (`references/visuais.md`), e salve em `anexos/`, referenciando com `![descrição](../anexos/arquivo.svg)`. **Nunca** bloco ` ```mermaid ` nem fórmula `$…$` no pacote: sem internet eles não aparecem. Fórmula vai em texto/Unicode (`x² + y² = r²`) ou numa imagem.

### Etapa 5 — Conferir e revisar a qualidade (o código mede; depois um leitor de verdade)

**1. O código mede.** `python "<pasta>/pacote.py" conferir "{RAIZ}/{matéria}/pacote"` checa, por dia: a soma dos minutos contra as horas por dia; frontmatter igual à soma; leitura longa demais para o tempo declarado; **a estrutura didática** (cada leitura com “Por que isso importa”, “Exemplo”, “Checagem” com resposta dobrada e “Dúvidas que costumam aparecer”; cada exercício com “Critério de pronto” e 3 dicas; “Se travar”; prova com 5 ou mais questões, todas com “Não sei”; revisão com resposta dobrada; “Hoje você vai conseguir” no começo do dia); **o gabarito** (existe com o mesmo nome do dia, resolve cada exercício, diz “Se você errou assim”, tem a “Pontuação” da prova); dia faltando na sequência; link quebrado; imagem inexistente; fórmula LaTeX ou mermaid; texto provisório (“TODO”), “é fácil”/“óbvio”; e a **autossuficiência** (link, “pesquise”, “pergunte ao Claude”, scripts da skill). **Corrija até não sobrar `FALHA`** e diga o resultado como veio.

**2. Verifique os fatos e os exemplos (o que o código não vê).** Antes de dar um dia por pronto:
- **Todo exemplo de código roda e dá o resultado que o texto diz.** Rode com `Bash` quando houver o interpretador (uma conta, uma saída, um erro de propósito: o texto mostra exatamente o que aparece). Sem como rodar, diga no `01-plano.md` que aquele trecho não foi executado.
- **Toda conta, tradução, data, nome, versão e número confere** com a fonte (Regra 8). Resposta de gabarito errada é o pior defeito de um pacote sem professor: refaça cada resposta do gabarito do zero, sem olhar a que você escreveu, e compare.
- **Nenhum termo aparece antes de ser explicado:** todo termo novo está no `03-glossario.md` e é definido no dia da primeira aparição, nunca depois.
- **Nenhum exercício pede algo que o pacote ainda não ensinou** (pré-requisito de verdade, não só de tópico).

**3. Leitura cega (o professor que não está lá).** Para o **primeiro dia, um dia do meio e o último** (e todo dia, se houver subagentes sobrando), chame um subagente `general-purpose` com **somente** o arquivo do dia, o gabarito dele e o glossário (sem a sua conversa e sem o currículo) e peça: *“Você é um estudante iniciante, sozinho, sem internet e sem ninguém para perguntar. Estude este dia. Liste: (1) todo termo ou passo que ficou sem explicação; (2) todo ponto em que você teria que adivinhar; (3) exercício cuja resposta o texto não permitiria achar; (4) resposta do gabarito que está errada ou que não bate com o enunciado; (5) o trecho mais difícil de entender e por quê.”* Corrija cada achado **dentro do arquivo** e confira de novo. Sem subagentes, faça você mesmo a leitura, devagar, no papel do iniciante.

### Etapa 6 — PDF (não é feito por padrão)

O pacote é Markdown e eu converto para PDF sozinho. **Não gere `pdf/`.** Só se eu pedir PDF ou apostila para imprimir: `python "<pasta>/apostila.py" --pacote "{RAIZ}/{matéria}/pacote"` (usa o Chrome ou o Edge; sem eles, gera `.html` para imprimir).

### Etapa 7 — Entregar (e terminar)

1. Abra o `00-LEIA-ME.md` no navegador, se der: `python "<pasta>/ver.py" "{RAIZ}" "{matéria}/pacote/00-LEIA-ME.md" --abrir` (se falhar, ignore).
2. Responda em **poucas linhas**, sem perguntas: onde está a pasta; quantos dias e quantas horas ao todo; **por onde começar** ("abra `00-LEIA-ME.md` e depois `dias/dia-01-….md`"); o que foi assumido (horas, meta, ponto de partida) e se a fonte foi verificada; o resultado do `conferir`, como veio.
3. **Termine aí.** Não ofereça menu, não pergunte se quero mais nada, não repita o conteúdo no terminal. Se eu quiser mudar algo, eu peço.

## 3. Quanto cabe em um dia (tempos)

Estime os blocos com estes valores e **corrija pelo meu ritmo** quando eu disser que o tempo estava curto ou longo (anote no `01-plano.md`). O `conferir` pega o texto de leitura longo demais.

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
3. **"Se travar".** Todo bloco de exercício diz o que fazer, nesta ordem: releia o trecho X; use a dica 1; tente de novo; use a dica 2; **pule, faça o próximo e volte**; anote a dúvida em `02-acompanhamento.md`. Dificuldade é normal (Regra 12); nunca "é fácil".
4. **Fazer junto:** cada passo diz **o que fazer** e **o que deve aparecer/acontecer**. Se eu errar, eu comparo e vejo na hora, sem ninguém.
5. **Exercícios:** enunciado sem ambiguidade, **texto de apoio pronto** quando pedir texto (Regra 27), **Critério de pronto** (o que devo conseguir/observar ao acertar, sem dar a solução) e **escada de 3 dicas dobradas** (`<details><summary>Dica 1</summary>…</details>`), a última ainda sem a solução (Regra 9). Resposta e solução **só** no `gabaritos/dia-NN.md`.
6. **Gabarito:** a solução, **por que** funciona, **o erro mais comum** e **uma melhoria** (Regra 29). Para cada exercício, "se você errou assim, o problema é isto". Antes de olhar, eu marco 🟢🟡🔴 no `02-acompanhamento.md` (calibração, Regra 19).
7. **Provas e quizzes:** alternativas pelo procedimento de `references/avaliacao.md`; **a posição da certa varia sem padrão**; cada errada tem o **equívoco que revela** no gabarito; use `quiz.py montar` para receber os avisos de alternativa que se entrega pela forma e refaça o que ele acusar. "Não sei" é resposta válida e distinta de erro. Correção no gabarito: a certa, o porquê e **qual seção reler** para cada erro. **Regra: 80% ou mais, passo; abaixo, refaço o bloco indicado e repito a prova** (Regras 16–17).
8. **Fonte e versão:** o `01-plano.md` diz a versão congelada; o texto ensina só o que é atual (Regras 25–28). Nada de "antigamente se fazia assim".
9. **Prática antes da teoria** quando der (Regra 14): mostre rodando/fazendo, depois nomeie.
10. **Tom:** português do Brasil, frases completas, sem pressa e sem condescendência; celebre antes de corrigir mesmo no papel ("se você chegou aqui, já tem X"). Nunca "é fácil" nem "óbvio".
11. **Matéria sem tela** (idioma, música, matemática, concurso): o mesmo molde. Áudio, partitura ou imagem que o texto não substitui: diga no pacote exatamente **o que preciso ter em mãos** e não dependa de baixar nada na hora; se for imprescindível, ponha o arquivo em `anexos/` (somente de fonte confiável e com crédito, `references/visuais-modelos.md`).

### Padrão de qualidade (o que torna um dia bom, além do que o código mede)

- **Concreto antes de abstrato:** um caso real, depois a regra. Uma ideia nova por vez; cada ideia nova é seguida de checagem ou exercício antes da próxima.
- **Mostre o erro também:** para cada ideia, ao menos um erro típico com a mensagem ou o sintoma exato e o jeito de sair dele. Quem estuda sozinho vai errar e precisa reconhecer o problema.
- **Resultado esperado em todo lugar:** todo exemplo e todo passo dizem o que deve aparecer; todo exercício tem critério de pronto verificável por mim.
- **Escada de dificuldade dentro do dia:** exercício 1 de reprodução, os do meio de modificação, o último de extensão ou criação. Os tempos do exercício batem com a tabela da seção 3.
- **Revisão que ensina:** a revisão espaçada retoma o que **eu mais provavelmente esqueci** (o ponto sutil), não a definição que acabou de ser lida.
- **Gabarito que ensina:** além da resposta, o raciocínio, o erro comum e como confirmar sozinho que acertei (rodar, conferir, comparar).
- **Cada parte fecha com um resumo** em `resumos/parte-N-nome.md` (um conceito por linha: definição, exemplo mínimo, erro comum) e com a prova da parte, cuja pontuação eu anoto no `02-acompanhamento.md`.
- **Tom e acessibilidade:** frases curtas, voz ativa, termo técnico só depois de definido; texto alternativo em toda imagem; nada que dependa de cor para ser entendido.

## 5. Modelos dos arquivos

### `_interno/curriculo.json` (você escreve, o `pacote.py` lê)

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

### `01-plano.md`

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
- Como estudar: abra `dias/dia-01-….md`, faça as seções na ordem, depois confira no gabarito de mesmo nome em `gabaritos/`.

## Mapa (ordem de estudo)
| Tópico | Parte | Dificuldade | Depende de | Dia |
|---|---|---|---|---|

## Dias
| Dia | Min | O que fecha | Arquivo |
|---|---|---|---|
| 1 | 250 | Tipos básicos | [dia-01-tipos-basicos](dias/dia-01-tipos-basicos.md) |

## Cronograma
(cole aqui a saída de `pacote.py planejar`, incluindo "Até onde cabe")

## Fontes
- Título — link — data da fonte — para que serviu
- Divergências entre os meus anexos e a fonte oficial: …
```

### `00-LEIA-ME.md`

Para quem abre a pasta pela primeira vez: **"Este pacote é completo: você não precisa de internet, do Claude nem de terminal para estudá-lo"** logo no começo; o que é; como começar; **como estudar um dia** (ordem das seções, pausas, o que fazer ao travar); como usar o gabarito (só depois de tentar); como preencher o `02-acompanhamento.md`; o que fazer se atrasar ou faltar tempo (seção 6); a data de criação, a versão congelada e se a fonte foi verificada; o que foi assumido (horas por dia, meta, ponto de partida); **"Antes de começar"** (o que preciso saber/ter, com como conferir); **"Mapa da pasta"** (uma linha para cada arquivo e pasta do pacote, na ordem de leitura); onde fazer as respostas e o projeto (`pratica/`); o que significa **"terminei"** (média das provas ≥ 80% e projeto funcionando) e o que estudar a seguir. Curto: cabe em uma tela e meia. Sem link para a internet nem tarefa de internet.

### `dias/dia-NN-assunto.md`

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
(2–3 perguntas por tópico vencido; resposta dobrada em `<details>`)

## 2. Ler — Funções tipadas (35 min)
### Por que isso importa
(o problema que a ideia resolve, em uma situação que eu reconheça)
### A ideia, passo a passo
(uma ideia por vez, apoiada no que já vi; termo novo definido na hora e posto no glossário)
### Exemplo
(mostrado funcionando, com o resultado exato; depois nomeado)
### Checagem
(uma pergunta curta; resposta em `<details><summary>Resposta</summary>…</details>`)
### Dúvidas que costumam aparecer
(2–4 perguntas reais de quem aprende isso, com resposta curta)

## 3. Fazer junto — … (35 min)
(passos numerados; cada um diz **o que fazer** e **o que deve aparecer**)

## 4. Exercícios — … (50 min)
**Se travar:** 1) releia a seção 2; 2) abra a dica 1 e tente de novo; 3) abra a dica 2; 4) pule, faça o próximo e volte; 5) anote a dúvida no `02-acompanhamento.md`. Travar é normal.

### Exercício 1 — nome (reprodução, ~10 min)
Enunciado sem ambiguidade (texto de apoio já pronto, se pedir texto).
**Critério de pronto:** o que devo observar/conseguir ao acertar (sem dar a solução).
<details><summary>Dica 1</summary>…</details>
<details><summary>Dica 2</summary>…</details>
<details><summary>Dica 3</summary>… (ainda sem a solução)</details>

### Exercício 2 — nome (modificação, ~15 min)
…

## 5. Prova — … (20 min)
> Sem consulta. “Não sei” é resposta válida e vale zero, mas me diz o que reler.
### Questão 1
Enunciado.
A) … B) … C) … D) … E) Não sei

## Fechamento do dia
- [ ] Marquei no `02-acompanhamento.md` o que fiz e a confiança (🟢🟡🔴).
- Amanhã: …

[← Dia anterior](dia-02-tipos.md) · [Próximo dia →](dia-04-classes.md) · Gabarito (só depois de tentar): [dia 3](../gabaritos/dia-03-funcoes.md)
```

Os títulos das seções seguem **exatamente** `## N. Tipo — título (M min)` com o Tipo começando por *Revisão, Ler, Fazer junto, Exercícios, Desafio, Projeto* ou *Prova*: é o que o `conferir` lê. Dia de **fechamento** (só revisão): coloque `fechamento: sim` no frontmatter.

### `gabaritos/dia-NN-assunto.md`

```markdown
# Gabarito — Dia 3
> Só abra depois de tentar. Marque 🟢🟡🔴 no `02-acompanhamento.md` **antes** de olhar.

## Exercício 1
**Resposta:** …
**Por quê:** …
**Se você errou assim:** … → releia a seção 2 (“…”).
**Uma melhoria:** …

(um bloco `## Exercício N` para cada exercício do dia, com o mesmo número)

## Prova
| Questão | Certa | Por que cada errada está errada (o equívoco que revela) | Reler |
|---|---|---|---|
**Pontuação:** acertos/total = %. 80% ou mais: passei. Abaixo: reler as seções da coluna “Reler” e repetir a prova.
```

### `02-acompanhamento.md`

Tabela que **eu** preencho (por dia: feito, confiança, tempo real, dúvida em aberto), a tabela de provas (nota e data) com a média que eu calculo, e a lista "Dúvidas em aberto" (só para eu anotar; o pacote não manda levar a ninguém). É o único arquivo do pacote em que eu escrevo.

## 6. Se algo mudar depois

- **Atrasei ou faltei um dia:** não pule nada. Faço o dia seguinte; o calendário só desloca. Os dias de revisão continuam valendo.
- **Já sei um tópico / quero pular:** sozinho (o jeito que o pacote ensina no `00-LEIA-ME.md`): pulo as seções do tópico e faço a prova dele; passando em 80%, sigo. Se eu pedir ao Claude, ele roda `pacote.py planejar --ja-sei …` e regera só os dias afetados (os arquivos antigos não são apagados; o Claude cria os novos e o `01-plano.md` aponta). O pacote não depende disso.
- **Mudou a minha disponibilidade de horas:** o Claude roda `planejar --horas N` e regera o cronograma; o conteúdo dos tópicos continua, só muda em que dia cai cada bloco.
- **Verificar/atualizar o pacote:** quando eu pedir `"atualizar pacote"` (com internet), o `tutor-pesquisador` confere a versão e os fatos centrais contra a fonte oficial atual; a mudança é listada e o `01-plano.md` ganha a data da verificação. Sem isso, o pacote vale pela data de criação e **o `00-LEIA-ME.md` diz essa data**.
- **Montagem interrompida:** `"gerar mais dias"`: continue do último `dias/dia-NN-assunto.md` existente **até o último dia do currículo**, com o mesmo `curriculo.json`, conferindo cada lote. Termina com a mesma entrega curta da Etapa 7.
- **O pacote só cria as pastas de `pratica/` e os `_leia-me.md` delas, uma vez** (o resto é meu) e **nunca sobrescreve** um arquivo meu. `02-acompanhamento.md` só é criado, nunca regravado depois que eu comecei a preenchê-lo.
