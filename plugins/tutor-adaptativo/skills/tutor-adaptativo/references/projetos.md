# Referência — Validação de projetos

> Leia ao propor ou validar o projeto de prática, os miniprojetos ou o fechamento da trilha.

> **Nesta referência:**
> **1. Protocolo de Validação de Projetos**
>     · As camadas de projeto (leia com atenção)
>     · Validação do Projeto de Prática
>     · Validação de Miniprojetos (o que cada parte acrescenta)
>     · Registro no trilha.md
>     · Changelog de conquistas (`conquistas.md`)

## Protocolo de Validação de Projetos

> Define como avaliar qualquer ideia de projeto. **Nenhum projeto começa sem a sua validação:** o projeto de prática passa pela Análise de Cobertura; cada miniprojeto passa pela Validação de Miniprojetos (mais leve, ver abaixo).

### As camadas de projeto (leia com atenção)

"Projeto" aqui é qualquer **trabalho aplicado** da matéria: um aplicativo, um texto, uma peça musical, um plano de negócios, um conjunto de exercícios resolvidos de ponta a ponta. O que importa é que seja algo que eu construo de verdade.

1. **Projeto de prática (a espinha):** UM projeto que **cresce ao longo de toda a trilha**. É o veículo central do aprendizado.
   - **Começa por um "esqueleto que anda":** a menor versão ponta a ponta que *funciona* — feia e mínima, mas viva (um programa que roda, um texto com começo, meio e fim, uma música tocada do início ao fim). Só depois engorda. Trabalhar semanas sem nada funcionar é o que mais me desanima; ter algo vivo cedo me segura (`references/pedagogia.md` → "Protocolo Antifrustração e Continuidade").
2. **Miniprojeto = como a parte faz o projeto avançar:** um miniprojeto **não é um projeto separado** — é o que aquela parte acrescenta ao projeto de prática. Nem sempre é algo novo e visível: às vezes é **endurecer** o que já existe (testes, tratamento de erros, refatoração, revisão, melhorar a organização). Isso é honesto e ensina uma lição real — nem todo trabalho é produzir coisa nova. Cada parte tem o seu, validado antes de começar.
3. **Fechamento (no fim da trilha):** em vez de um projeto novo do zero (que, pro meu perfil, vira a "coisa grande e complexa" que me trava), o fechamento é uma de duas opções, à minha escolha:
   - **🚀 Ship it:** finalizar o projeto de prática de verdade e deixá-lo **mostrável** — o que isso significa depende da matéria: em código, testes, README, uma passada final de clean code e deploy, virando peça de portfólio (`references/programacao.md` → "Fechamento Ship it para código"); em escrita, uma versão final revisada e publicada; em música, uma gravação. Termino com algo que posso mostrar.
   - **🧠 Sprint de síntese:** reconstruir **uma** fatia do projeto do zero, de memória. Teste de domínio puro (recuperação ativa), mas pequeno e contido.

> **A Análise de Cobertura roda no _projeto de prática_** (na sua forma completa imaginada), porque é o que eu construo de ponta a ponta.

### Validação do Projeto de Prática

Executar quando: o Claude o propõe; eu trago ideia própria; eu uso `"valida projeto"`; eu quero trocar o projeto durante a trilha.

> **Princípio central: nenhuma ideia é só aprovada ou rejeitada de cara.** Toda sugestão de projeto — minha ou do Claude — é primeiro **destrinchada e melhorada**, antes de rodar a análise formal. O objetivo nunca é o mínimo aprovável, é a versão mais rica possível que ainda seja **divertida, motivadora e enxuta o bastante para eu não desanimar** — útil e agradável, os dois ao mesmo tempo, sempre.

**Passo 1 — Entender a ideia + checar o escopo.** Se vaga ("algo com jogos"), no **máximo 2 perguntas** para entender o suficiente. Não peça mais que o necessário.
- **Checagem de escopo:** se o projeto parece ambicioso demais para o ritmo e o tempo definidos na entrevista, **encolha antes de aprovar**. Entre duas ideias com cobertura parecida, escolha sempre a **menor** e a que **eu mais quero construir** — interesse genuíno e escopo enxuto são o que evita a frustração que me faz parar.

**Passo 2 — Destrinchar e propor melhorias (sempre, mesmo se a ideia já parece boa).**
1. Identifique **o que torna a ideia divertida e motivadora pra mim** — o gancho, o tema, o que me faz querer construir aquilo. Isso nunca é descartado nos ajustes seguintes.
2. Identifique **o que ela pratica de verdade** e **o que ela deixa de fora ou só toca de raspão** — antes ainda de rodar a tabela formal de cobertura.
3. Proponha **1 a 3 ajustes concretos** que aumentam o valor de estudo **sem matar a graça** — geralmente é uma camada a mais, não um projeto diferente. Ex.: *"o jogo da velha sozinho é pouco pra praticar banco de dados — e se ele salvasse o histórico de partidas, com um placar de vitórias? Continua sendo o mesmo jogo divertido, só que agora também pratica consultas de verdade."*
4. Mostre o antes e o depois num formato curto:
```
💡 Ideia original: [o que eu trouxe]
🔧 Sugestões de ajuste:
   1. [ajuste] — [por que aumenta o valor de estudo sem perder a diversão]
   2. [ajuste] — [...]
✨ Ideia refinada: [versão ajustada, mantendo o gancho original]
```
5. Eu decido: aceito o ajuste, quero outro ângulo ou prefiro seguir com a ideia original do jeito que veio — a palavra final é sempre minha; o Claude só garante que eu vi a versão mais rica antes de escolher.

**Passo 3 — Mapear a cobertura** (já na versão refinada do Passo 2). Para cada parte da trilha: *"para construir este projeto, eu precisaria usar este conceito?"*

```
📊 Análise de cobertura — [Nome do Projeto]

✅ Cobertos (vou praticar ativamente)
   Tópico X — Parte Y: [como o projeto usa esse conceito na prática]

⚠️ Cobertura parcial (toca mas não aprofunda)
   Tópico X — Parte Y: [o que cobre + o que fica de fora]
   Sugestão: [pequeno ajuste que aumentaria a cobertura]

❌ Não cobertos (o projeto ignora)
   Tópico X — Parte Y: [por que não aparece] | Centralidade: [central / periférico]

Cobertura: [N cobertos] + [N parciais] de [total]
Conceitos centrais descobertos: [lista, se houver]
Avaliação: [Forte / Adequada / Fraca]
```

**Passo 4 — Critério de aprovação:**

| Avaliação | Critério | O que fazer |
|---|---|---|
| **Forte** | ≥ 75% cobertos ou parciais **e** nenhum conceito central descoberto | ✅ Aprovado |
| **Adequada** | 50–74% cobertos ou parciais, sem central descoberto | ⚠️ Aprovado com ajustes concretos |
| **Fraca** | < 50%, **ou** qualquer conceito central descoberto | ❌ Não aprovado — explica e propõe alternativas |

> A **centralidade pesa mais que a porcentagem**: deixar um conceito central de fora reprova mesmo com % alto.

**Passo 5 — Se não aprovado ou parcial:**
1. Explique **com clareza e sem julgamento** o que ficaria sem praticar.
2. Proponha **duas saídas:** (A) um ajuste na ideia original que fecha as lacunas; (B) um projeto alternativo que cobre melhor, mantendo o meu tema de interesse.
3. Mostre a Análise de Cobertura das alternativas.
4. Eu decido — nunca se impõe.

> O objetivo não é reprovar ideias, é garantir que o projeto sirva ao aprendizado. Se eu insistir numa ideia com cobertura fraca depois de ver a análise, registre as lacunas no `trilha.md` e siga em frente.

### Validação de Miniprojetos (o que cada parte acrescenta)

Executar ao propor o miniprojeto de cada parte, antes de começar.

O miniprojeto da parte deve: usar **todos os conceitos centrais** daquela parte; caber numa sessão; ser maior que um exercício solto; fazer o projeto de prática avançar (algo novo **ou** endurecimento: testes, tratamento de erro, refatoração, revisão, organização).

> A mesma lente do Passo 2 vale aqui, em miniatura: se o jeito mais óbvio de encaixar o conceito ficar seco ou mecânico demais, **antes de propor assim**, pense se existe um ângulo que deixa a mesma cobertura mais envolvente dentro do tema do projeto — não precisa de passo formal extra, é só não aceitar a primeira ideia burocrática se uma versão mais divertida cobre a mesma coisa.

```
🔍 Miniprojeto — Parte [X]

Ideia: [nome e descrição em 1–2 frases — o que esta parte acrescenta ao projeto de prática]
Tipo: [algo novo / endurecimento]

Conceitos desta parte que cobre:
✅ [conceito] — [como aparece]
⚠️ [conceito] — cobre parcialmente / [ajuste]
❌ [conceito] — não aparece / [como incluir]

Aprovado? [Sim / Com ajuste: ...]
```

Se um conceito central da parte ficou de fora, ajuste o enunciado antes de começar.

### Registro no trilha.md

```markdown
## Validação de projetos

### Projeto de prática — [Nome]
- Ideia original: [o que eu trouxe, ou o que o Claude propôs]
- Ajustes sugeridos no destrinche: [lista dos 1-3 ajustes propostos no Passo 2]
- Versão final escolhida: [ideia refinada aceita, ou original mantida — e por quê]
- Cobertura: [N]/[total] ([%]) — Forte / Adequada / Fraca
- Conceitos centrais descobertos: [lista, se houver]
- Lacunas conhecidas / ajustes feitos: [...]

### Miniprojetos
- Parte 1a — [nome]: ✅ aprovado / ⚠️ ajustado | tipo: novo / endurecimento

### Fechamento
- Escolha: 🚀 Ship it / 🧠 Sprint de síntese — [descrição]
```

### Changelog de conquistas (`conquistas.md`)

> Como minha maior dificuldade é continuidade, o projeto crescendo é meu maior combustível — então o tornamos visível.

Ao fim de cada parte, registre **uma linha** no `conquistas.md` da matéria: o que o projeto passou a fazer (e, se eu quiser, o caminho de um print, áudio ou gif). Nos dias de desânimo, reler isso é ver o quanto já andei.

```markdown
# conquistas.md — [Matéria]

## 📊 Dashboard
- **Última sessão:** [AAAA-MM-DD] — é daqui que sai a Reentrada (`references/pedagogia.md` → "Reentrada depois de uma pausa")
- Sequência atual de sessões: [N] dias ou sessões seguidas
- Exercícios concluídos: [N]
- Provas feitas: [N] | Média geral: [%]
- Conceitos arquivados na revisão espaçada: [N]
- Reforços já superados: [N]

## Changelog
- [data] — Parte 1a: o projeto agora [faz X]
- [data] — Parte 1b: o projeto agora [faz Y]
```

> Atualize o Dashboard ao fim de cada sessão (junto com o passo 2 de `references/sessao.md` → "Ao finalizar cada sessão") — é rápido e é o que eu vejo primeiro ao abrir o comando `"conquistas"` nos dias difíceis.
