# Tutor Adaptativo

Skill para o Claude Code que ensina **qualquer matéria**, de dois jeitos:

| Modo | Como é | Precisa de internet? |
|---|---|---|
| **Ao vivo** | O Claude ensina em conversa: descobre seu nível, monta o plano, ensina uma ideia por vez e corrige na hora. | Só para pesquisar fontes |
| **Pacote autônomo** | Você diz a matéria e **quantas horas por dia tem**. O Claude monta todo o material em dias que fecham essas horas e você estuda **sozinho**, em Markdown ou PDF. | Só na montagem. Depois, **não** |

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
| `quero estudar inglês do zero` | Começa a aula ao vivo (entrevista, sondagem, plano) |
| `retomar` | Continua de onde parou |
| `gerar mais dias` | Escreve os próximos dias do pacote |
| `dica` · `travei` · `quiz` · `prova` · `boletim` | Dica, ajuda ao travar, quiz, prova, notas |

Todos os comandos estão em `plugins/tutor-adaptativo/skills/tutor-adaptativo/SKILL.md`.

## O que o pacote entrega

O Claude mostra o cronograma e **até onde a matéria chega com o seu tempo**. Com o seu "ok", escreve `Estudos/<matéria>/pacote/`:

```text
pacote/
├── LEIA-ME.md          como começar
├── plano.md            ordem de estudo, cronograma e fontes
├── dias/dia-01.md …    o dia completo (soma as suas horas)
├── gabaritos/…         respostas, separadas
├── pdf/                para imprimir
└── acompanhamento.md   seu: o que fez, notas, dúvidas
```

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
| **Chrome ou Edge** | PDF automático e diagramas | Gera `.html`; abra e use Ctrl+P → Salvar como PDF |
| Qualquer navegador | Ler as notas bonitas (`ver.py`) | Abra os `.md` num editor de texto |
| Internet | Montar o pacote com fonte oficial e atual | Sem ela, o pacote é marcado como "não verificado" |

**Para estudar um pacote já pronto, basta um leitor de PDF ou editor de texto.**

## Detalhes

- Passo a passo do pacote: `plugins/tutor-adaptativo/skills/tutor-adaptativo/references/pacote.md`
- Histórico de versões: `plugins/tutor-adaptativo/skills/tutor-adaptativo/CHANGELOG.md`
- Verificar os scripts: `py plugins/tutor-adaptativo/skills/tutor-adaptativo/scripts/selftest.py`

A seção "1. Quem sou eu" do `SKILL.md` descreve o perfil de quem estuda; se for usar, troque pelo seu.

Licença MIT. O fluxo de sondagem e plano se inspira no sistema [`learn`](https://github.com/amosblomqvist/learn), reescrito com palavras próprias.
