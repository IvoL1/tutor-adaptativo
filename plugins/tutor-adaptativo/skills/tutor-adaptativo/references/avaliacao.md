# Referência — Avaliação: quiz, prova e reforço

> Leia ao fazer qualquer pergunta com resposta certa (checagem de nó, sondagem, quiz, prova), ao escrever alternativas, ao corrigir e ao decidir entre avançar e reforçar.

> **Nesta referência:**
> **1. Perguntas com resposta certa e sem resposta certa**
> **2. Como escrever alternativas (valem para todo quiz)**
> **3. Formato do quiz ao vivo**
> **4. Confiança e lacunas**
>     · Depois de um erro: o que você estava pensando?
> **5. Prova (parte e tópico)**
>     · Quando aplicar
>     · Correção e critério
>     · Registro no progresso.md
> **6. Reforço e reprova**
> **7. Se eu discordar de uma correção**

## Perguntas com resposta certa e sem resposta certa

São dois tipos, e não se misturam:

- **Quiz (tem resposta certa):** mede o que eu sei. É corrigido na hora: ✓ ou ✗, a resposta certa e um porquê curto. Serve para checar um nó, sondar meu nível, revisar e provar. Mesmo uma pergunta socrática ("tente descobrir") vira quiz se existir uma resposta certa.
- **Pergunta de escolha (não tem resposta certa):** colhe uma preferência ou decisão — o que quero aprender, que direção seguir, o que fazer hoje. Nunca é corrigida nem entra em percentual.

Regra de bolso: se dá para errar, é quiz; se não dá, é escolha. Como fazer cada uma com a ferramenta de perguntas: `references/ferramentas.md` → "Perguntas com opções".

## Como escrever alternativas (valem para todo quiz)

O erro mais comum é o teste que se resolve "de fora": escreve-se uma resposta boa e algumas de enchimento, ninguém revisa o enchimento, e quem responde acha a certa sem saber a matéria. Por isso não adianta auditar depois — **construa** as alternativas para o equilíbrio sair de graça.

1. **Nenhuma alternativa leva justificativa — só a afirmação seca.** O vazamento mais comum é a certa trazer o próprio "porque" ("…, porque preserva X") e as erradas não: ela fica mais longa e mais específica, e entrega a resposta. Toda explicação vai no feedback, que só aparece depois que eu respondo.
2. **Escreva a certa primeiro e derive cada errada dela.** Escolha um equívoco específico (ou um conceito vizinho que costuma ser confundido) e escreva o que *quem acredita nele* diria — no mesmo esqueleto, tamanho e registro da certa. Cada alternativa passa a ser "a mesma frase sob uma crença diferente", e o paralelismo nasce da construção em vez de ser conferido depois.
3. **Cada errada é um erro real** (uma ideia mal formada sobre o conceito atual — nunca uma prática antiga ou depreciada, Regra 25) que eu poderia cometer — então a escolha diagnostica — e ao mesmo tempo é inequivocamente errada na leitura pretendida: tentadora, não capciosa.
4. **Sem destaque assimétrico.** Não ponha negrito no termo-chave só numa alternativa. Ou nenhuma tem destaque, ou todas têm o mesmo.
5. **Varie a posição da certa** ao longo da sessão; não deixe que ela caia sempre na mesma letra.
6. **Sem "todas as anteriores" nem "nenhuma das anteriores".**

**Exemplo** (git, sobre `git commit`). Pergunta: *"O que `git commit` faz?"*
- Certa: "Registra no histórico do repositório local as mudanças já preparadas"
- Errada (equívoco: confundir com `push`): "Envia ao repositório remoto as mudanças feitas no repositório local"
- Errada (equívoco: confundir com `pull`): "Traz do repositório remoto as mudanças feitas por outras pessoas"

Todas no mesmo molde (verbo + complemento), sem "porque", com o mesmo tamanho. Quem não sabe a matéria não consegue apontar a certa pela forma.

**Teste a frio:** releia o conjunto pronto como se não conhecesse a matéria. Se ainda dá para adivinhar a certa, você pulou o passo 1 ou o 2 — refaça, não remende.

Fundamento: [Haladyna, Downing e Rodriguez (2002)](https://eric.ed.gov/?id=EJ660246) validaram uma taxonomia de 31 diretrizes de redação de itens de múltipla escolha (revisando 27 livros e 27 estudos). Entre elas estão "manter as alternativas homogêneas em conteúdo e estrutura gramatical" e "manter o tamanho das alternativas aproximadamente igual". Os passos 1 a 4 adaptam o procedimento de construção de alternativas do sistema `learn` (créditos no `CHANGELOG.md`); os passos 5 e 6 são regras deste sistema.

## Formato do quiz ao vivo

1. **Uma pergunta por vez.** Uma linha de contexto (se precisar), a pergunta, as alternativas e "Não sei".
2. **Pergunte a confiança junto** em prova e em sondagem: 🟢 alta · 🟡 média · 🔴 baixa — **antes** de revelar o resultado. Na checagem de um nó, é opcional.
3. **Corrija na hora:** ✓ ou ✗, a alternativa certa e **um** porquê curto. Se eu errei, diga qual equívoco a minha escolha revela — sem sermão e sem "era fácil" (Regra 12).
4. **Celebre antes de corrigir** (Regra 11): comece pelo que foi certo, mesmo que parcial.
5. **Número de alternativas:** com a ferramenta de perguntas, até 3 alternativas reais + "Não sei" (ela limita a 4 opções por pergunta); em texto, até 4 + "Não sei". Não marque qual é a certa. Ver `references/ferramentas.md` → "Quiz interativo".
6. **Seleção múltipla** só quando a resposta certa for de fato um conjunto. Corrija por **conjunto exato**: só é acerto se eu marcar todas as certas e nenhuma errada; "Não sei" continua sendo lacuna.
7. **Sorteio, verificação e correção por código:** com Python, monte e corrija pelo `quiz.py` (`references/ferramentas.md` → "Scripts da skill (o código decide)"): ele embaralha a posição da certa, acusa alternativa que se entrega pela forma e corrige sem conta de cabeça. Sem Python, use a regra fixa de posição do plano B de `references/ferramentas.md` → "Quiz interativo".

## Confiança e lacunas

- **Confiança (🟢🟡🔴):** serve para caçar o caso perigoso — **respondi com 🟢 e errei** (ilusão de competência). Esse quadrante é o foco de reforço. O erro confiante corrigido com feedback claro tende a fixar bem, mas a literatura mostra que ele **pode voltar com o tempo** ([Metcalfe e Miele, 2014](http://www.columbia.edu/cu/psychology/metcalfe/PDFs/MetcalfeMiele2014.pdf)); por isso, depois do reforço, o conceito entra na fila de revisão com **1 dia** de intervalo (`references/pedagogia.md` → "Fila de revisão espaçada (dentro do `conhecimento.md`)").
- **Acerto frágil (acertei com 🔴):** vale o ponto, mas a ideia ainda não está firme. Reforce de leve (um exemplo novo) e registre na fila como `acerto-fragil`: o intervalo **não avança** (`fila.py`).
- **"Não sei":** é uma resposta legítima e **distinta de erro**. Um "não sei" honesto vale mais que um chute, porque mostra onde está a lacuna sem fingir que sei.
  - No percentual da prova, conta como **ponto perdido** (senão infla a nota).
  - No registro, é rotulado **lacuna**, não erro — e nunca vira "erro confiante".
  - A consequência é **reensino sem peso** daquele conceito (Protocolo Antifrustração), nunca bronca.
- **Nota de esforço (1 a 5), no fim de cada prova:** *"Como me senti nesta parte? 1 = exausto/travei muito · 3 = normal · 5 = tranquilo."* Mede o esforço subjetivo, não o acerto. Nota baixa com boa pontuação é sinal para aliviar o ritmo (`references/pedagogia.md` → "Protocolo Antifrustração e Continuidade") antes que a frustração apareça.

### Depois de um erro: o que você estava pensando?

Quando eu errar ou marcar "não sei", **depois de corrigir**, pergunte **uma vez e em uma linha**: *"O que você estava pensando?"* — texto livre, e eu posso pular. A resposta mostra o equívoco **de verdade**, que é mais fino que a alternativa que eu escolhi, e aponta onde reensinar.

- Use o que eu disser para **dirigir o reensino**; se o equívoco se repetir, registre-o em "Erros comuns que já cometi" do `conhecimento.md`.
- **Não pergunte** em acerto, nem no meio de uma prova (se quiser, pergunte no fim de todas), nem se eu estiver cansado ou desanimado (Protocolo Antifrustração): nesse caso só corrija e siga.
- Nunca use a resposta para me cobrar; é diagnóstico, não interrogatório.

## Prova (parte e tópico)

> A prova é feita ao vivo, em sequência de quizzes, e vale o mesmo para qualquer matéria. O feedback vem pergunta a pergunta; a **nota** fecha no fim.

### Quando aplicar

| Gatilho | Tipo |
|---|---|
| Ao fim de cada **parte** | Prova rápida — **5 questões** |
| Ao fim de cada **tópico completo** | Prova do tópico — 6 a 10 questões + 1 exercício prático |
| Após reforço | Reprova — questões diferentes, mesmos conceitos |

- **Toda parte e todo tópico terminam em prova** — nada conclui sem ela (Regra 17).
- **Por que no mínimo 5 questões:** com 80% de corte, 3 questões exigem 3 acertos e 4 exigem 4 — ou seja, 100%, o que contradiz o antifrustração. Com 5, um erro ainda aprova (4/5 = 80%). Se a parte tiver poucos conceitos, o excedente vira questões de recuperação de partes anteriores (conta no percentual). Se por algum motivo a prova tiver menos de 5, o `quiz.py placar` avisa que o resultado é provisório; confirme com mais 1 ou 2 questões antes de travar o avanço.
- Cada questão testa **um conceito** — nunca agrupa dois.
- **Sem gabarito adiantado:** o que foi dito na aula não é repetido na pergunta.
- Adapte o formato ao que combinamos na entrevista (Q14): múltipla escolha, questão aberta, código ou texto para corrigir, explicar com minhas palavras. Questão aberta também é corrigida na hora, contra critérios que você escreveu **antes** de eu responder.
- Prova abre com **1 pergunta de recuperação** de um dos últimos 3 conceitos, sem olhar para trás, e a **Revisão do dia** já terá acontecido no início da sessão.
- A prova **nunca** começa sem eu dizer que estou pronto (Regra 23), e posso adiar.

### Correção e critério

1. **Celebre primeiro** o que ficou bom.
2. Questão por questão: ✓/✗/lacuna + por quê.
3. Calcule **[acertos]/[total] = [%]** (lacuna conta como ponto perdido). Com Python, é o `quiz.py placar` que faz a conta e aplica os limites, e já devolve o bloco do `progresso.md`; não refaça de cabeça.
4. Destaque a **calibração**: acertos confiantes e, principalmente, erros confiantes.
5. Aplique o critério:

| Resultado | O que acontece |
|---|---|
| **80% ou mais** | ✅ Aprovado — avança para a próxima parte; os conceitos aprovados entram na fila de revisão do `conhecimento.md` |
| **50–79%** | ⚠️ Reforço seletivo — reensina só os conceitos errados e faz a reprova |
| **Menos de 50%** | 🔁 Reforço completo — reensina toda a parte e faz a reprova |

> Resultado abaixo de 80% **trava o avanço** até a reprova. Mas trate isso sem peso: reforço é parte normal do processo, não punição (`references/pedagogia.md` → "Protocolo Antifrustração e Continuidade").

### Registro no progresso.md

> O `quiz.py placar` gera este bloco pronto (com Python); sem ele, preencha à mão.

```
## Prova — Tópico [X], Parte [Y] — [data]
- Resultado: [%] ([acertos]/[total])
- Status: ✅ Aprovado / ⚠️ Reforço / 🔁 Reforço completo
- Conceitos com erro: [lista]
- Erros confiantes (🟢 + ❌): [lista — foco de reforço; entram na fila a 1 dia depois do reforço]
- Lacunas ("não sei"): [lista — reensino sem peso]
- Nota de esforço (1-5): [n]
- Reprova (se houver): [%] — [data]
```

## Reforço e reprova

O reforço é uma miniaula, ao vivo, só sobre o que não firmou:

- **Reensine pelo ciclo completo** (`references/ensino.md` → "Fase 3 — Ensino: o ciclo por nó"), mas com **outro ângulo**: nova analogia, novo exemplo mínimo e novos exercícios, com a escada de dicas à mão. Nunca repita as mesmas palavras da primeira vez.
- Confirme o conteúdo na fonte oficial (Regra 8).
- Termina com a **reprova**: questões diferentes, mesmos conceitos, mesmo critério.
- Se a reprova também ficar abaixo de 80%, **encolha o passo** (`references/pedagogia.md` → "Protocolo Antifrustração e Continuidade") em vez de repetir a mesma rota.

## Se eu discordar de uma correção

Uma nota de esforço baixa, ou um comentário como "acho que essa tá errada", merece reabrir a questão — não uma defesa automática do gabarito:

1. Releia a pergunta e a minha resposta com calma, sem assumir que a correção estava certa.
2. Explique o critério de novo, com o exemplo mínimo da fonte oficial se ajudar.
3. Se eu tiver razão: corrija o resultado (%) e agradeça por apontar — isso não abala o sistema, o fortalece.
4. Se o critério estava certo: explique o porquê por um ângulo diferente do que já tentou, sem repetir as palavras da correção original.
