# Referência — Ferramentas e subagentes (com plano B)

> Leia ao fazer uma pergunta com opções, aplicar um quiz, delegar pesquisa ou diagrama a um subagente, rodar um script, ou quando uma ferramenta não existir no ambiente. Para ler ou gravar no cofre, vá direto a `references/obsidian.md`.

> **Princípio (Regra 33):** use a ferramenta quando ela existir e faça o equivalente na conversa quando não existir. **Nunca** trave por falta de ferramenta, e nunca diga "não consigo" se a conversa resolve.

> **Nesta referência:**
> **1. Perguntas com opções**
> **2. Quiz interativo**
> **3. Subagentes**
>     · Sem subagentes
> **4. Obsidian pelo MCP**
> **5. Scripts da skill (o código decide)**
>     · Quiz (`quiz.py`)
>     · Fila de revisão (`fila.py`)
>     · Diagramas (`render.py`)
> **6. Arquivos: com e sem acesso**
> **7. Formatação**

## Perguntas com opções

**O que é:** em vez de soltar a pergunta como texto corrido, a pergunta aparece numa janelinha com opções para eu clicar. Reduz digitação e deixa claro o que está sendo decidido. No Claude Code, é a ferramenta `AskUserQuestion`.

**Como usar:**
- **Autorização:** a descrição da ferramenta pode sugerir usá-la só quando você está travado. Nesta skill o uso em quiz e em escolhas é **intencional e autorizado** — é o que eu quero, mesmo sendo rotineiro.
- Até **4 perguntas** por chamada, com **2 a 4 opções** cada. Uma opção "Outro" com texto livre é acrescentada sozinha.
- Ponha a opção recomendada **primeiro**, marcada "(Recomendado)".
- Use para **perguntas de escolha** (sem resposta certa): o que quero aprender, que direção seguir, o que fazer hoje, qual projeto. Nunca para adivinhar o que eu penso quando dá para perguntar em texto livre.
- Para perguntas abertas ("Conte o que já sabe"), use texto livre.

**Plano B (sem a ferramenta):** escreva a pergunta no chat, com as opções numeradas, e peça que eu responda com o número ou com as minhas palavras. Uma pergunta por vez.

Diferença entre escolha e quiz: `references/avaliacao.md` → "Perguntas com resposta certa e sem resposta certa".

## Quiz interativo

**O que é:** uma pergunta **com resposta certa**, corrigida na hora (✓/✗, a resposta certa e um porquê curto). Não existe uma ferramenta nativa de quiz no Claude: o tutor monta o quiz com a pergunta com opções, e o `quiz.py` (código) cuida do sorteio, da verificação e da correção.

**Com Python (recomendado):** siga "Scripts da skill" → "Quiz (`quiz.py`)". O script **sorteia a posição da certa** (nunca a mesma posição duas vezes seguidas), **verifica as alternativas** (tamanho, "porque", negrito assimétrico, "todas as anteriores") e **corrige** por código. Você só mostra as opções na ordem devolvida, sem indicar a certa.

**Plano B (sem Python):**
1. Escreva as alternativas pelo procedimento de `references/avaliacao.md` → "Como escrever alternativas (valem para todo quiz)".
2. Use a pergunta com opções, **sem marcar qual é a certa**. A ferramenta limita a 4 opções por pergunta; por isso use **até 3 alternativas reais + "Não sei"**. Precisa de mais? Faça em texto, com até 4 + "Não sei".
3. **Posição da certa por regra fixa, não "de cabeça":** ponha a certa na posição `1 + (n mod N)`, onde `n` é o número da pergunta na sessão (1ª, 2ª, 3ª…) e `N` é o número de alternativas reais (sem contar "Não sei"). Com `N = 3`: 2ª, 3ª, 1ª, 2ª… — a certa gira por todas as posições e nunca repete na seguinte. As erradas ocupam as posições que sobram, em qualquer ordem.
4. Em prova e sondagem, use a segunda pergunta da mesma chamada para a **confiança** (🟢 alta · 🟡 média · 🔴 baixa), de modo que eu responda as duas de uma vez, antes de ver o resultado.
5. Quando eu responder, corrija: celebre o que foi certo, diga ✓ ou ✗, a alternativa certa e um porquê curto; se errei, qual equívoco a minha escolha revela.

**Plano B em texto:** as mesmas alternativas em texto numerado; eu respondo com o número e a confiança.

## Subagentes

**O que são:** assistentes especializados que rodam isolados, com a própria conversa e as próprias ferramentas, e devolvem só o resultado. Mantêm a sessão limpa e a pesquisa profunda fora do caminho da aula. Duas definições acompanham esta skill (pasta `agents/` do repositório):

| Subagente | Para que serve | Quando chamar |
|---|---|---|
| `tutor-pesquisador` | Pesquisar na web e devolver um relatório curto com fontes, links e datas | Na menor dúvida sobre um fato (`references/ensino.md` → "Precisão inegociável"); ao mapear um campo novo; ao levantar fonte e versão na entrevista |
| `tutor-diagramador` | Criar **um** diagrama correto e mínimo e verificá-lo olhando o resultado | Quando uma ideia é melhor como desenho (`references/visuais.md`) |

**Como chamar:** descreva a tarefa por **completo** — o subagente roda isolado e **não conhece a conversa**. Inclua o que precisa saber, o que quer de volta e o que já foi descartado — e, para o `tutor-diagramador`, **o caminho completo da pasta `scripts/`** (do `SKILL.md`), onde ele acha o `render.py`. O subagente devolve o **código** do visual; quem grava no cofre é você, pelo MCP do Obsidian (`references/obsidian.md`). Se a skill foi instalada como plugin, o nome aparece com o prefixo do plugin (`tutor-adaptativo:tutor-pesquisador`); a descrição do subagente basta para o Claude escolher certo.

**Nunca confie cegamente no retorno:** o pesquisador devolve veredito e fonte; leia a fonte quando a afirmação for central para a aula. Se o subagente voltar sem achar fonte oficial, o fato é **não verificável** e **não entra na aula**.

### Sem subagentes

Quando os subagentes não existirem no ambiente (app do claude.ai, instalação só da skill), **faça você mesmo o mesmo trabalho**:
- **Pesquisa:** use a busca e a leitura de páginas da web, se existirem, seguindo a mesma hierarquia de fontes (`references/pedagogia.md` → "Fontes e versão — regra permanente"). Sem acesso à web, **diga que não conseguiu verificar** e marque o fato como não verificado na aula — nunca ensine de memória como se fosse certo.
- **Diagramas:** escreva você mesmo um bloco mermaid simples (`references/visuais.md` → "Como fazer").

## Obsidian pelo MCP

**O que é:** o cofre de estudos é lido e escrito pelas ferramentas do **MCP do Obsidian** (`obsidian_read_note`, `obsidian_update_note`, `obsidian_search_replace`, `obsidian_list_notes`, `obsidian_global_search`, `obsidian_manage_frontmatter`, `obsidian_manage_tags`). Não há mais script de cofre: o que o antigo `cofre.py` fazia agora é receita, em `references/obsidian.md`:

| Antes (`cofre.py`) | Agora |
|---|---|
| `resumo` (hook de abertura) | receita "Retomar": ler `progresso.md`, `conquistas.md` e `conhecimento.md` ao dizer `"retomar"` |
| `nova-materia` | receita "Criar a matéria" (templates em `references/templates.md`) |
| `nota` | receita "Gravar a nota da sessão" |
| `anexar` | receita "Visuais e imagens": Mermaid no corpo, SVG como texto em `anexos/`; PNG só com acesso ao disco |
| `transcrever` | receita "Transcrever um vídeo" (lê `.vtt` ou texto colado, limpa e grava em `fontes/`) |
| `cartoes` | receita "Cartões" |
| `abrir` | link `obsidian://open?…` para clicar |
| `validar` | lista "Conferir o cofre" |
| `diario` (hook `Stop`) | removido: a nota da sessão já guarda o que vale reler |

**Plano B:** sem o MCP, arquivos diretos (`Read`/`Write`/`Edit`) com as mesmas regras; sem acesso a arquivos, o Cartão de retomada (`references/obsidian.md` → "Sem o MCP"). **Nunca apague nem sobrescreva** arquivo meu; **nunca escreva em `pratica/`** (regras de segurança em `references/obsidian.md`).

## Scripts da skill (o código decide)

**O que são:** scripts em Python que fazem o que **não deve depender de eu obedecer a uma instrução**: sorteio, verificação, contas, datas e renderização. O Claude os chama pelo Bash. Ficam na pasta `scripts/`, ao lado do `SKILL.md` (o `SKILL.md` mostra o caminho completo; use-o no lugar de `<pasta>` abaixo). **Nenhum deles toca o cofre:** ler e gravar notas é com o MCP do Obsidian.

**Requisito:** Python 3.8+ no PATH (`python` ou `python3`; use o que existir). Só o `render.py` ainda precisa de um navegador (Chrome ou Edge) e de rede. Sem Python, ou se um script falhar: **faça à mão pelo plano B de cada seção e diga que foi à mão** — a skill nunca trava por isso. Para conferir que tudo está certo: `python <pasta>/selftest.py` (deve dizer que todas as verificações passaram).

### Quiz (`quiz.py`)

**Jeito mais seguro (qualquer shell, qualquer codificação):** grave a pergunta num arquivo temporário com a ferramenta de escrita de arquivos e rode `python "<pasta>/quiz.py" montar --prova p1 --arquivo caminho.txt`. Isso evita os problemas de pipe e de acentos do PowerShell. O formato é o mesmo do exemplo abaixo, que usa o stdin (bash):

```bash
python "<pasta>/quiz.py" montar --prova p1 <<'EOF'
P: O que `git commit` faz?
T: git commit
+ Registra no histórico do repositório local as mudanças já preparadas
- Envia ao repositório remoto as mudanças feitas no repositório local
~ confunde com push
- Traz do repositório remoto as mudanças feitas por outras pessoas
~ confunde com pull
E: O commit grava um ponto no histórico local; enviar é o push e trazer é o pull.
EOF
```

Linhas: `P:` pergunta, `C:` contexto, `T:` conceito testado, `+` certa, `-` errada, e a linha seguinte começada por `~` é o **equívoco** que aquela errada revela (só aparece na correção; assim um `|` ou `->` dentro do texto da alternativa, comum em código, não atrapalha), `E:` explicação, `MULTIPLA` para seleção múltipla.

1. `montar` devolve `ID`, as **opções já sorteadas** (com "Não sei" no fim) e `AVISOS`. **Se houver aviso, refaça a pergunta e rode de novo.** Nunca mostre a certa: o script nem a imprime.
2. Mostre as opções **exatamente na ordem devolvida** (pergunta com opções; em prova e sondagem, junto com a confiança).
3. Com a resposta: `python "<pasta>/quiz.py" corrigir ID NÚMERO --confianca verde|amarela|vermelha` (ou `nao-sei`; em seleção múltipla, `1,3`). Ele devolve `RESULTADO` (acerto, erro ou lacuna), a `CLASSE` (erro confiante, acerto frágil), a `CERTA`, o `EQUIVOCO_REVELADO` e a `EXPLICACAO`. **Use esse resultado como está**; não corrija de cabeça.
4. Ao fim da prova: `python "<pasta>/quiz.py" placar p1 --topico T1 --parte 1a --fechar`. Devolve o **percentual, a decisão (aprovado, reforço seletivo ou completo) e o bloco pronto para o `progresso.md`** (que você acrescenta pelo MCP); a conta e os limites de 80% e 50% são do código. **Sempre feche com `--fechar`** (senão a prova continua aberta e uma nova tentativa se soma à anterior); a **reprova usa outro nome** (`p1-reprova`). Se a prova tiver menos de 5 questões, o script avisa que o resultado é provisório. Uma prova parada por mais de 12 h recomeça do zero sozinha. O estado das perguntas e provas em andamento fica na pasta temporária do sistema (ou em `TUTOR_STATE`), **nunca dentro do cofre**.

### Fila de revisão (`fila.py`)

O arquivo vive no cofre e é lido pelo MCP; o script recebe o texto pelo **stdin** (`-` no lugar do arquivo). Cole a seção `## Fila de revisão espaçada` do `conhecimento.md` (ou o arquivo todo):

```bash
python "<pasta>/fila.py" vencidos - --max 3 <<'EOF'
## Fila de revisão espaçada
| Conceito | Tópico/Parte | Aprendido em | Intervalo atual | Próxima revisão | Status |
|---|---|---|---|---|---|
| git commit | T1 / 1a | 2026-10-01 | 3d | 2026-10-04 | ativo |
EOF
```

- `vencidos` lista até 3 conceitos da Revisão do dia (o resto continua vencido).
- `registrar - --conceito "git commit" --resultado acerto` (mesma seção no stdin) aceita `--resultado novo|acerto|acerto-fragil|erro|erro-confiante` e `--parte "T1 / 1a"` no `novo`. Intervalos: 1d → 3d → 7d → 16d → 35d → 60d → 120d → arquivado; erro volta para 1d; **acerto frágil** (acertei, mas com 🔴) repete o mesmo intervalo, sem avançar. **No modo `-` ele não grava nada:** imprime `TROCAR:` (a linha como está na nota), `POR:` (a linha nova) e `FIM`. Aplique com `obsidian_search_replace`. Conceito novo: o `TROCAR` é a linha de exemplo (`| — | … |`) ou a última linha da tabela, e o `POR` já traz a nova linha logo depois dela.
- `mostrar -` imprime a fila. Com um caminho no lugar do `-`, o script lê e grava o arquivo direto no disco (útil só fora do cofre).
- Plano B: a tabela de `references/pedagogia.md` → "Fila de revisão espaçada (dentro do `conhecimento.md`)".

### Diagramas (`render.py`)

`python "<pasta>/render.py" mermaid entrada.mmd saida.png` (ou `svg`) usa o Chrome ou o Edge que já estão instalados. Ele **valida a sintaxe e devolve a mensagem exata do erro** (linha e ponto), e só gera o PNG quando está válido; aí você **olha** a imagem. Precisa de rede para carregar o Mermaid 11.17.2 (versão fixa, com verificação de integridade; ou `--mermaid-js` com um arquivo local). O que vai para a nota é o **código validado** (bloco mermaid ou SVG); o PNG só vai ao cofre se houver acesso ao disco (`references/obsidian.md` → "Visuais e imagens"). Sem navegador: só verificação por leitura, e diga isso. `render.py detectar` mostra o que está disponível. **Atenção:** o Mermaid que o Obsidian embute pode ser mais antigo que o 11.17.2; tipos novos (`xychart-beta`, `block-beta`, `architecture-beta`…) podem não aparecer no Obsidian mesmo validando aqui (`references/visuais-modelos.md`).

## Arquivos: com e sem acesso

- **Com acesso** (o MCP do Obsidian conectado, ou o disco aberto no Claude Code): crie e atualize a estrutura e os registros de `references/sessao.md` → "Estrutura de pastas" e grave a nota da sessão ao fim de cada sessão, seguindo `references/obsidian.md`. É o que espelha a conversa num arquivo para eu ler no Obsidian — **só o que vale reler**, não a transcrição.
- **Sem acesso** (chat do claude.ai): não há onde gravar. Entregue o **Cartão de retomada** (`references/sessao.md` → "Sem acesso a arquivos — Cartão de retomada").

Nos dois casos, **nunca apague nem sobrescreva** arquivos meus em `pratica/`. Antes de atualizar um registro, leia a versão atual.

## Formatação

- **Markdown** para tudo. Código em blocos com a linguagem.
- **LaTeX** sempre que houver matemática: `$f(x) = x^2$` em linha e `$$` em bloco próprio. Não escreva `f(x) = x^2` em texto simples quando LaTeX resolve.
- **Mermaid** em bloco ```` ```mermaid ````. Renderiza no Obsidian e no GitHub. Em algumas interfaces de chat o bloco aparece como código; nesse caso, o diagrama também vai para a nota da sessão, onde renderiza (`references/visuais.md`).
