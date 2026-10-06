# Referência — Sessão ao vivo, estrutura de pastas e retomada

> Leia ao iniciar ou finalizar uma sessão, ao criar a estrutura de pastas de uma matéria, ao retomar sem arquivos, ou quando precisar do nome canônico de qualquer arquivo, pasta ou seção.

> **Nota sobre `CLAUDE.md`:** é um **ponteiro curto**, não uma cópia do sistema. A fonte única da verdade é sempre esta skill — copiar o conteúdo dela para o cofre criaria duas versões que divergem a cada atualização. O `CLAUDE.md` (template em `references/templates.md`) só diz ao Claude Code: "este cofre usa a skill `tutor-adaptativo`; siga-a; ignore memórias automáticas de sessões antigas". Se `estudos/CLAUDE.md` não existir, gere-o a partir do template. Se existir um `CLAUDE.md` antigo e longo (cópia do sistema), substitua pelo ponteiro.

> **Nesta referência:**
> **1. Se há mais de uma matéria ativa**
> **2. Ao iniciar cada sessão**
>     · Retomar e continuar (padrão)
>     · Dimensionar a sessão ao orçamento de tempo
>     · Matéria nova — Entrevista (Fase 0)
>     · Pedido solto de explicação
> **3. Ao finalizar cada sessão**
> **4. Estrutura de pastas**
>     · Nomes canônicos (pastas, arquivos e seções)
> **5. Sem acesso a arquivos — Cartão de retomada**
> **6. Referência rápida — quem mexe no quê**
>     · Ordem do ciclo, do início ao fim

## Se há mais de uma matéria ativa

Antes de tudo, verifique quantas pastas de matéria existem em `estudos/`.
- **Uma matéria:** segue direto os modos abaixo.
- **Mais de uma:** confirme qual é a de hoje pelo contexto da mensagem, ou pergunte se não estiver claro. O comando `"trocar assunto"` muda a matéria ativa a qualquer momento, sem perder o lugar nas outras — cada uma mantém seu próprio `progresso.md` e `conhecimento.md`.
- **Revisão espaçada entre matérias:** se no mesmo dia houver conceitos vencidos em mais de uma matéria, **não empilhe tudo** — limite a no máximo **3 perguntas de revisão por matéria**, dentro da sessão da matéria ativa. O que sobrar continua vencido e entra na próxima sessão.

## Ao iniciar cada sessão

Primeiro identifique **o modo**:

### Retomar e continuar (padrão)

Quando eu disser `"retomar"`, abrir uma matéria que já existe, ou simplesmente voltar a estudar:

1. **Leia a posição.** Com `Read`, leia `registros-da-skill/progresso.md`, `conquistas.md` e `conhecimento.md` da matéria ativa (receita "Retomar" em `references/obsidian.md`); o `trilha.md` só se precisar do contexto. Sem acesso à pasta, use o **Cartão de retomada** que eu colar. **Se não houver registros nem cartão**, pergunte se eu tenho um cartão guardado; se não tiver, trate como matéria nova (Entrevista). **A posição atual vem só desses registros**, nunca de memória automática de conversas anteriores; se a memória disser uma coisa e os registros outra, os registros vencem.
2. **Se eu estou voltando depois de dias**, aplique a **Reentrada** (`references/pedagogia.md` → "Reentrada depois de uma pausa"): recapitule em 1–2 frases, sem cobrar, e já siga.
3. **Revisão do dia** (`references/pedagogia.md` → "Fila de revisão espaçada (dentro do `conhecimento.md`)"): 1 a 3 quizzes dos conceitos vencidos. Se não houver nenhum, diga isso e siga.
4. **Confirme o plano de hoje em uma pergunta de escolha** (`references/ferramentas.md` → "Perguntas com opções"): continuar do ponto em que parei (padrão, recomendado), revisar, fazer um quiz, ou outra coisa. Se eu parecer sem energia, ofereça o modo leve (`references/pedagogia.md` → "Sessão mínima viável (para manter a continuidade)").
5. **Siga o ciclo de ensino** (`references/ensino.md` → "Fase 3 — Ensino: o ciclo por nó") a partir do `▶ próximo passo`, dimensionado ao orçamento de tempo do `trilha.md` (Regra 24).

### Dimensionar a sessão ao orçamento de tempo

> O `trilha.md` guarda quanto tempo eu tenho por sessão (Q7 da entrevista). Calibre a sessão **antes** de começar — uma sessão de 2h para quem tem 30 min é o tipo de coisa que trava e desanima (`references/pedagogia.md` → "Protocolo Antifrustração e Continuidade").

- Estimativas para começar: ~10–15 min por exercício de reprodução ou modificação, ~20–25 min por extensão ou criação, ~10 min por prova rápida e ~5–10 min por nó (motivar até checar). Ajuste com o tempo que eu realmente levo, anotado no `progresso.md`.
- Diga no início quanto a sessão deve durar (*"Hoje: uns 25 min"*), para eu decidir se cabe.
- Se a parte não couber, **divida em duas sessões** em vez de encolher a progressão — nunca pule reprodução → modificação → extensão → criação para caber no relógio (Regra 24).

### Matéria nova — Entrevista (Fase 0)

Se **não houver** `trilha.md` para essa matéria: inicie a entrevista (`references/entrevista.md`), seguida da Sondagem e do Plano (`references/ensino.md`). **Este é o momento que mais exige ida e volta comigo** — é ali que a trilha inteira é desenhada, então vale a pena ser conversado.

### Pedido solto de explicação

Se eu só pedir para você explicar ou ensinar algo pontual, sem uma matéria em andamento: use o ritual pequeno (`references/ensino.md` → "Tamanho do ritual") e, no fim, ofereça transformar aquilo numa matéria com trilha, se fizer sentido.

---

## Ao finalizar cada sessão

1. **Resumo** do que aprendi, em linguagem simples e sem jargão, e uma frase sobre **a ideia que encaixou hoje**.
2. **Atualize os três registros:**
   - `progresso.md` — posição, **Pendências abertas**, provas, linha do tempo da sessão.
   - `conhecimento.md` — termos novos no glossário e os intervalos de revisão (Revisão do dia e nós aprovados).
   - `conquistas.md` — Dashboard (incluindo a **data desta sessão**) e, se concluí uma parte, uma linha no changelog do que o projeto passou a fazer (`references/projetos.md` → "Changelog de conquistas (`conquistas.md`)").
3. **Grave a nota da sessão** em `sessoes/` (template em `references/templates.md`) — o diário em que eu releio o que entendi. Com `Write`, grave a nota com o frontmatter certo, acrescentando (nunca sobrescrevendo) se já houver uma do dia, e liste-a em "Sessões recentes" do painel (receita "Gravar a nota da sessão" em `references/obsidian.md`). Diagramas entram no corpo da nota como bloco mermaid ou como `![[arquivo.svg]]` em `anexos/` (`references/obsidian.md` → "Visuais e imagens"). Sem acesso a arquivos, entregue o **Cartão de retomada** (neste arquivo → "Sem acesso a arquivos — Cartão de retomada").
4. **Atualize o mapa** no `_painel-[assunto].md`: nós firmes marcados e o `▶ próximo passo`.
5. **Confira o cofre** depois de criar ou alterar registros (`references/obsidian.md` → "Conferir o cofre") e corrija o que divergir.
6. **Matéria de código:** verifique mudanças sem commit em `pratica/projeto/` e lembre de commitar antes de fechar (`references/programacao.md` → "Versionamento (git)").
7. **Se a entrevista, a sondagem ou o plano não terminaram** nesta sessão, registre o que já foi levantado como **rascunho** (no `trilha.md` com a marca `rascunho`, ou no Cartão de retomada), para não refazer tudo. O rascunho só vira trilha depois do meu "ok" no plano.
8. Diga **exatamente qual é o próximo passo** e proponha o que fazer na próxima sessão.

---

## Estrutura de pastas

> Desenhada para a ordem ser óbvia só de olhar: o que **eu** escrevo fica em `pratica/`; o que o Claude escreve fica nos registros e nas notas. Compatível com Obsidian (wikilinks, callouts, frontmatter) sem quebrar Markdown padrão — ver "Convenções Obsidian" em `references/templates.md`.

```
estudos/                                ← raiz dos estudos no cofre Obsidian (subpasta dele, ou o próprio cofre)
├── README.md                           ← 🤖 índice geral: matérias ativas com [[links]] e status
├── CLAUDE.md                           ← 🚫 ponteiro curto: "este cofre usa a skill X, siga-a"
│
├── [nome-da-matéria]/
│   ├── _painel-[matéria].md            ← 🤖 painel: mapa de dependências, status e "▶ próximo passo"
│   │
│   ├── sessoes/                        ← 🤖 uma nota por sessão (o diário: o que entendi, onde travei)
│   │   └── 2026-09-30-[tópico].md
│   │
│   ├── anexos/                         ← 🤖 imagens e diagramas que entram nas notas (![[arquivo.svg]], ![[arquivo.png]])
│   ├── fontes/                         ← 🤖 transcrições de aulas em vídeo (pista, não fonte para ensinar)
│   ├── _sessoes-[matéria].base         ← 🤖 tabela das sessões (Base do Obsidian)
│   ├── cartoes.md                      ← 🤖 opcional: cartões do plugin Spaced Repetition
│   │
│   ├── pratica/                        ← ✍️ 100% MEU
│   │   ├── projeto/                    ←    o projeto de prática (em código: versionado com git)
│   │   └── treinos/                    ←    exercícios soltos, uma subpasta por parte (t1-1a/ ...)
│   │
│   └── registros-da-skill/             ← 🚫 SÓ LEITURA — só o Claude escreve aqui
│       ├── trilha.md                   ←    a trilha, convenções, validações
│       ├── progresso.md                ←    onde estou + próximo passo + pendências + histórico de provas
│       ├── conhecimento.md             ←    conceitos + glossário + fila de revisão
│       └── conquistas.md               ←    dashboard + changelog (abro nos dias difíceis)
│
└── [outra-matéria]/
    └── ...
```

> **Criar tudo de uma vez:** a receita "Criar a matéria" de `references/obsidian.md` grava, por arquivos, os quatro registros, o painel, a Base de sessões e o `_leia-me.md` de `pratica/projeto/` e `pratica/treinos/`, a partir dos templates de `references/templates.md`, e põe a matéria no `README.md` do cofre. `sessoes/`, `anexos/` e `fontes/` nascem quando o primeiro arquivo é gravado neles. Nunca sobrescreve o que já existe.

> **Por que `_painel-` em vez de `README.md` repetido:** no Obsidian, vários arquivos com o mesmo nome tornam `[[README]]` ambíguo (autocompletar inútil, grafo com nós idênticos, busca poluída). Nomes únicos resolvem isso, e o prefixo `_` faz o painel aparecer **sempre no topo** da pasta. O `README.md` sobrevive só na raiz do cofre, onde é único e a convenção tem valor.

### Nomes canônicos (pastas, arquivos e seções)

> **Toda vez que algum nome precisar ser escrito, ele vem daqui.** É a única lista; nada é inventado na hora. Se um nome divergir em outro arquivo da skill, esta seção vence.

#### Pastas

| Pasta | Conteúdo |
|---|---|
| `sessoes/` | uma nota por sessão: `AAAA-MM-DD-[tópico].md` (criada com a primeira nota) |
| `anexos/` | imagens e diagramas: `AAAA-MM-DD-[nome].svg` ou `.png` (só o Claude grava; criada com o primeiro anexo) |
| `fontes/` | transcrições de vídeo: `AAAA-MM-DD-[título].md` (só o Claude grava; criada com a primeira) |
| `pratica/projeto/` | o projeto de prática (uma só pasta, cresce a trilha inteira) |
| `pratica/treinos/t[N]-[parte]/` | exercícios soltos, uma subpasta por parte (ex.: `t1-1a/`) |
| `registros-da-skill/` | os quatro registros — só o Claude escreve |

**Numeração de partes:** as letras reiniciam a cada tópico e vêm prefixadas pelo número do tópico — T1 → `1a`, `1b`, `1c`; T2 → `2a`, `2b`. A ordem é **numérica** no tópico e depois pela letra: `t2` vem antes de `t10`.

#### Arquivos fixos da matéria

| Arquivo | Onde |
|---|---|
| `_painel-[matéria].md` · `_sessoes-[matéria].base` · `cartoes.md` (opcional) | raiz da pasta da matéria |
| `trilha.md` · `progresso.md` · `conhecimento.md` · `conquistas.md` | `registros-da-skill/` |
| `AAAA-MM-DD-[tópico].md` | `sessoes/` |
| `_leia-me.md` (o único arquivo que o Claude grava em `pratica/`, na criação da matéria) | `pratica/projeto/` e `pratica/treinos/` |
| `README.md` · `CLAUDE.md` | raiz de `estudos/` (um por cofre — sem frontmatter) |

#### Seções do `progresso.md` (nomes exatos)

`## Posição atual` · `## Pendências abertas` · `## Histórico de provas` · `## Checkpoints` · `## Linha do tempo (sessões)`

**Marcadores usados nos registros:** `[travei]`, confiança `🟢` / `🟡` / `🔴` e `não sei`. O Claude os anota a partir do que eu digo na conversa — não preciso escrever nada à mão.

---

## Sem acesso a arquivos — Cartão de retomada

Em ambientes sem acesso ao meu disco (o chat do claude.ai, por exemplo) **não há onde gravar registros**, e cada conversa começa do zero. O substituto é o **Cartão de retomada**: um bloco compacto, entregue **no fim de toda sessão**, que eu guardo e colo no começo da próxima com `"retomar"`.

- Entregue o cartão sempre que encerrar uma sessão sem arquivos, e quando eu disser `"salva"`.
- Ele contém só o que é indispensável para retomar: matéria e fonte congelada, posição, próximo passo, pendências, fila de revisão, glossário novo e o que eu preciso que o Claude lembre de mim (tempo por sessão, interesses, histórico emocional). Template em `references/templates.md` → "Template: Cartão de retomada".
- Ao receber um cartão, **trate-o como os registros**: ele é a posição atual, e vale mais que qualquer memória automática.
- Mantenha curto (cabe numa tela). Se a fila de revisão crescer, liste só o que vence nos próximos 7 dias.

## Referência rápida — quem mexe no quê

> Para eu nunca ficar em dúvida sobre o que devo tocar.

| 🚫 Eu NUNCA mexo (o Claude cuida) | ✍️ Eu mexo e escrevo aqui |
|---|---|
| `CLAUDE.md` — ponteiro para a skill | `pratica/projeto/` — o projeto que cresce a cada parte |
| **Toda a pasta `registros-da-skill/`** (posso ler à vontade, nunca editar) | `pratica/treinos/t[N]-[parte]/` — exercícios soltos |
| · `trilha.md` — trilha, convenções, validações | |
| · `progresso.md` — posição e **próximo passo** (é aqui que olho quando não sei o que fazer) | |
| · `conhecimento.md` — conceitos, glossário, fila de revisão | |
| · `conquistas.md` — dashboard e changelog | |
| `_painel-[matéria].md`, as notas de `sessoes/` e os arquivos de `anexos/` | |

### Ordem do ciclo, do início ao fim

| # | O que acontece | Quem faz |
|---|---|---|
| 1 | Eu digo que quero estudar algo novo (ou uso `"entrevista"`) | Eu |
| 2 | Respondo a entrevista (Fase 0) | Eu + Claude |
| 3 | Sondagem: o Claude acha onde termina o que eu sei | Eu + Claude |
| 4 | O Claude apresenta o plano e o mapa; eu aprovo ou ajusto | Eu + Claude |
| 5 | O Claude cria a estrutura e os registros (ou entrega o cartão) | Claude |
| 6 | Sessão: Revisão do dia → ensino em ciclos (motivar, estabelecer, conectar, checar) → exercícios em `pratica/` | Eu + Claude |
| 7 | Quiz e prova com correção na hora; reforço se ficar abaixo de 80% | Eu + Claude |
| 8 | Fim da sessão: registros, nota da sessão, próximo passo | Claude |
| 9 | Repete 6 a 8 até fechar a trilha (🚀 Ship it ou 🧠 Sprint de síntese) | Eu + Claude |

> Os passos 6→7→8 se repetem sem voltar ao 2. Só refaço a entrevista ou a sondagem se eu pedir (`"entrevista"`, `"sondar"`) ou se aparecer um fio novo.
