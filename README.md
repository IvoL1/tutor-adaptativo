# Tutor Adaptativo

Skill para o Claude Code que **gera material de estudo completo e fechado para qualquer matéria**: você recebe uma pasta (Markdown) e estuda sozinho, **sem o Claude, sem terminal e sem internet**, sem consultar nada fora dela. Há dois modos; o primeiro é o padrão:

| Modo | Como é | Precisa de internet? |
|---|---|---|
| **Pacote autônomo (padrão)** | Você diz a matéria e **quantas horas por dia tem**. O Claude monta **a matéria inteira, de uma vez**, em dias que fecham essas horas, e entrega a pasta. Ele não pede aprovação, não pergunta se deve continuar e não pede nada depois. | Só na montagem, e é opcional (sem internet o pacote sai marcado como "não verificado"). Depois, **não** |
| **Ao vivo (opcional)** | Só se você pedir ("ao vivo"): o Claude ensina em conversa, descobre seu nível, ensina uma ideia por vez e corrige na hora. | Só para pesquisar fontes |

## Instalar

No Claude Code:

```text
/plugin marketplace add IvoL1/tutor-adaptativo
/plugin install tutor-adaptativo@tutor-adaptativo
```

## Como acionar

Abra o terminal numa pasta de estudos (ex.: `Documents\Estudos`), rode `claude` e escreva:

| Você escreve | O que acontece |
|---|---|
| `pacote de TypeScript, 4 horas por dia` | Monta o pacote de estudo autônomo |
| `quero estudar inglês do zero` | Pergunta só as horas por dia e monta o pacote inteiro |
| `quero estudar inglês do zero, ao vivo` | Começa a aula ao vivo (entrevista, sondagem, plano) |
| `retomar` | Continua de onde parou |
| `analisar erros` | Lê o seu Registro de erros e gera reforço + prova de reprova, fechados e com gabarito |
| `mais exercícios de X` · `outra prova de Y` · `um mini projeto de Z` | Gera material novo em `reforco/`, com gabarito à parte |
| `gerar mais dias` | Só se uma montagem foi interrompida: continua até o fim |
| `prova` · `quiz` | Grava o caderno e o gabarito em arquivos separados (você corrige). Corrigir na hora só no `ao vivo` |
| `dica` · `travei` · `boletim` | Dica, ajuda ao travar, notas (modo ao vivo) |

Todos os comandos estão em `plugins/tutor-adaptativo/skills/tutor-adaptativo/SKILL.md`.

## O que o pacote entrega

O Claude calcula o cronograma (e **até onde a matéria chega com o seu tempo**), escreve tudo e entrega `Estudos/<matéria>/pacote/`, sem pedir aprovação no meio:

```text
pacote/
├── 00-LEIA-ME.md       comece aqui (diz o que ter instalado)
├── 01-plano.md         ordem de estudo, cronograma e fontes
├── 02-acompanhamento.md  seu: o que fez, notas, dúvidas
├── 03-glossario.md     todo termo novo, com o dia em que aparece
├── 04-duvidas.md       banco de dúvidas: o que costuma aparecer, com resposta
├── dias/dia-01-tipos-basicos.md …   o dia completo (soma as suas horas)
├── provas/…            cada prova em arquivo próprio, SEM respostas
├── gabaritos/…         respostas de dias e provas, com o mesmo nome, separadas
├── reforco/…           nasce vazia: reforços e extras gerados sob pedido
├── resumos/…           uma página por parte, para revisar
├── anexos/             imagens e diagramas
└── _interno/           dados do cronograma (não precisa abrir)
```

### Provas: você corrige, o Claude só analisa se você pedir

1. Faça a prova do arquivo `provas/…` (folha de respostas incluída), sem olhar nada.
2. Corrija com `gabaritos/…` do mesmo nome (traz o passo a passo, a pontuação e o que reler em cada erro).
3. Anote os erros no **Registro de erros** do `02-acompanhamento.md`.
4. Se quiser mais, abra o Claude e escreva `analisar erros` (ou `mais exercícios de X`, `outra prova de Y`, `um mini projeto de Z`). Ele lê o registro, acha o padrão dos seus erros e gera, em `reforco/` e `provas/`, aula curta por outro ângulo, exercícios, desafio, mini projeto e prova de reprova, **tudo com gabarito à parte**, sem fazer perguntas.

Exemplo real do cronograma (4 h por dia):

```text
## Dia 1 — 255 min
| # | Min | Bloco                  | Tópico                 |
| 1 | 30  | Ler e entender (1/3)   | t01 Tipos básicos      |
| 2 | 30  | Fazer junto (2/3)      | t01 Tipos básicos      |
| 3 | 45  | Exercícios (3/3)       | t01 Tipos básicos      |
| 4 | 35  | Ler e entender (1/4)   | t02 Funções e interfaces |
...
## Até onde cabe
| 1 dia(s) | 2 de 4 tópicos (até "Funções e interfaces") |
```

A ordem respeita os pré-requisitos, a dificuldade sobe em degraus, a revisão espaçada já vem agendada, e cada dia traz dúvidas prováveis, 3 dicas por exercício e gabarito explicado.

## O que ter instalado (para rodar 100%)

| Item | Para quê | Sem ele |
|---|---|---|
| **Claude Code** | Rodar a skill | Obrigatório |
| **Python 3.8+** (no Windows, comando `py`) | Cálculo do cronograma, conferência de tempo, quiz | A skill faz à mão e avisa |
| **Chrome ou Edge** | Só para diagramas e para o PDF opcional (`apostila.py`) | O pacote é Markdown; converta para PDF como preferir |
| Qualquer navegador | Ler as notas bonitas (`ver.py`) | Abra os `.md` num editor de texto |
| Internet | Montar o pacote com fonte oficial e atual | Sem ela, o pacote é marcado como "não verificado" |

**Para estudar um pacote já pronto, basta um editor de texto ou leitor de Markdown (e, se quiser, converter para PDF).**

## Detalhes

- Passo a passo do pacote: `plugins/tutor-adaptativo/skills/tutor-adaptativo/references/pacote.md`
- Histórico de versões: `plugins/tutor-adaptativo/skills/tutor-adaptativo/CHANGELOG.md`
- Verificar os scripts: `py plugins/tutor-adaptativo/skills/tutor-adaptativo/scripts/selftest.py`

A seção "1. Quem sou eu" do `SKILL.md` descreve o perfil de quem estuda; se for usar, troque pelo seu.

Licença MIT. O fluxo de sondagem e plano se inspira no sistema [`learn`](https://github.com/amosblomqvist/learn), reescrito com palavras próprias.
