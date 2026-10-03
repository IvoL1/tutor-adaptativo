# Referência — Ferramentas e subagentes (com plano B)

> Leia ao fazer uma pergunta com opções, aplicar um quiz, delegar pesquisa ou diagrama a um subagente, gravar arquivos, ou quando uma ferramenta não existir no ambiente.

> **Princípio (Regra 33):** use a ferramenta quando ela existir e faça o equivalente na conversa quando não existir. **Nunca** trave por falta de ferramenta, e nunca diga "não consigo" se a conversa resolve.

> **Nesta referência:**
> **1. Perguntas com opções**
> **2. Quiz interativo**
> **3. Subagentes**
>     · Sem subagentes
> **4. Scripts da skill (o código decide)**
>     · Quiz (`quiz.py`)
>     · Fila de revisão (`fila.py`)
>     · Cofre (`cofre.py`)
>     · Obsidian: o que a skill faz sozinha
>     · Diagramas (`render.py`)
> **5. Hooks automáticos (só quando instalado como plugin)**
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

**Como chamar:** descreva a tarefa por **completo** — o subagente roda isolado e **não conhece a conversa**. Inclua o que precisa saber, o que quer de volta e o que já foi descartado — e, para o `tutor-diagramador`, **o caminho completo da pasta `scripts/`** (do `SKILL.md`), onde ele acha o `render.py`. Se a skill foi instalada como plugin, o nome aparece com o prefixo do plugin (`tutor-adaptativo:tutor-pesquisador`); a descrição do subagente basta para o Claude escolher certo.

**Nunca confie cegamente no retorno:** o pesquisador devolve veredito e fonte; leia a fonte quando a afirmação for central para a aula. Se o subagente voltar sem achar fonte oficial, o fato é **não verificável** e **não entra na aula**.

### Sem subagentes

Quando os subagentes não existirem no ambiente (app do claude.ai, instalação só da skill), **faça você mesmo o mesmo trabalho**:
- **Pesquisa:** use a busca e a leitura de páginas da web, se existirem, seguindo a mesma hierarquia de fontes (`references/pedagogia.md` → "Fontes e versão — regra permanente"). Sem acesso à web, **diga que não conseguiu verificar** e marque o fato como não verificado na aula — nunca ensine de memória como se fosse certo.
- **Diagramas:** escreva você mesmo um bloco mermaid simples (`references/visuais.md` → "Como fazer").

## Scripts da skill (o código decide)

**O que são:** scripts em Python que fazem o que **não deve depender de eu obedecer a uma instrução**: sorteio, verificação, contas, datas e renderização. O Claude os chama pelo Bash. Ficam na pasta `scripts/`, ao lado do `SKILL.md` (o `SKILL.md` mostra o caminho completo; use-o no lugar de `<pasta>` abaixo).

**Requisito:** Python 3.8+ no PATH (`python` ou `python3`; use o que existir). Só o `transcrever` precisa de mais uma coisa: o `yt-dlp`. Sem Python, ou se um script falhar: **faça à mão pelo plano B de cada seção e diga que foi à mão** — a skill nunca trava por isso. Para conferir que tudo está certo: `python <pasta>/selftest.py` (deve dizer que todas as verificações passaram).

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
4. Ao fim da prova: `python "<pasta>/quiz.py" placar p1 --topico T1 --parte 1a --fechar`. Devolve o **percentual, a decisão (aprovado, reforço seletivo ou completo) e o bloco pronto para o `progresso.md`**; a conta e os limites de 80% e 50% são do código. **Sempre feche com `--fechar`** (senão a prova continua aberta e uma nova tentativa se soma à anterior); a **reprova usa outro nome** (`p1-reprova`). Se a prova tiver menos de 5 questões, o script avisa que o resultado é provisório. Uma prova parada por mais de 12 h recomeça do zero sozinha. Onde fica o estado: dentro do cofre, em `.tutor/estado/` (pasta oculta); fora de um cofre, na pasta temporária.

### Fila de revisão (`fila.py`)

```bash
python "<pasta>/fila.py" vencidos "<matéria>/registros-da-skill/conhecimento.md"
python "<pasta>/fila.py" registrar "<...>/conhecimento.md" --conceito "git commit" --resultado novo --parte "T1 / 1a"
```

`vencidos` lista até 3 conceitos da Revisão do dia (o resto continua vencido). `registrar` aceita `--resultado novo|acerto|acerto-fragil|erro|erro-confiante` e atualiza intervalo, data e status (1d → 3d → 7d → 16d → 35d → 60d → 120d → arquivado; erro volta para 1d; **acerto frágil** — acertei, mas com 🔴 — repete o mesmo intervalo, sem avançar). Plano B: a tabela de `references/pedagogia.md` → "Fila de revisão espaçada (dentro do `conhecimento.md`)".

### Cofre (`cofre.py`)

- `cofre.py resumo`: posição, pendências abertas e revisão do dia de cada matéria (é o que o hook de abertura injeta sozinho).
- `cofre.py validar`: confere nomes de pastas, arquivos e seções contra `references/sessao.md` → "Nomes canônicos (pastas, arquivos e seções)"; rode depois de criar ou alterar registros.
- `cofre.py status`: uma linha curta (`estudo: matéria: N p/ revisar`), vazia fora de um cofre ou sem nada vencido; serve para a linha de status do Claude Code (ver README).
- `cofre.py achar`: mostra onde o cofre foi encontrado (opção `--cofre`, variável `TUTOR_COFRE`, arquivo `~/.claude/tutor-adaptativo.json` com `{"cofre": "..."}`, ou subindo a partir da pasta atual).

### Obsidian: o que a skill faz sozinha

Estes comandos do `cofre.py` fazem, por código, o que o Obsidian precisa para o cofre ficar organizado **sem eu mexer em nada**. Todos escrevem arquivos Markdown direto na pasta do cofre, então **funcionam com o Obsidian aberto ou fechado**.

- **Criar a matéria:** `cofre.py nova-materia "Nome da matéria"` cria a pasta (nome sem acento, com hifens), os quatro registros, o painel, `sessoes/`, `pratica/projeto/`, `pratica/treinos/` e `anexos/` a partir dos templates, põe a matéria no `README.md` do cofre e valida. Roda 1 vez, depois do meu "ok" no plano; repetir não altera nada.
- **Gravar a nota da sessão:** `cofre.py nota "matéria" "título" --topico t1 --resumo "a ideia que encaixou"`, com o corpo no stdin ou em `--arquivo caminho.md` (preferível no PowerShell). Cria `sessoes/AAAA-MM-DD-título.md` com frontmatter (`tipo`, `materia`, `data`, `topico`, `tags`), acrescenta se já houver nota do dia e lista a nota em "Sessões recentes" do painel (as 8 mais recentes; o que eu escrevi à mão ali nunca é apagado).
- **Imagens e visuais:**
  - `cofre.py anexar "matéria" caminho/da/imagem.png --nome "descrição"` copia o arquivo para `anexos/` (nunca sobrescreve) e devolve `EMBED: ![[arquivo.png]]` para colar na nota. Aceita png, jpg, gif, webp, svg e pdf.
  - `cofre.py anexar "matéria" --area-de-transferencia` pega a **imagem que eu copiei** (print com Win+Shift+S, por exemplo) e a salva em `anexos/`. Testado no Windows; no macOS precisa do `pngpaste` e no Linux de `wl-paste` ou `xclip`.
  - **Diagramas:** gere o PNG com `render.py` (abaixo) e passe-o por `anexar`. Para diagramas simples, o bloco ```` ```mermaid ```` na própria nota já renderiza no Obsidian; o PNG é para quando eu quiser a imagem fixa ou o Mermaid do Obsidian divergir.
- **Transcrever uma aula em vídeo:** `cofre.py transcrever "matéria" "https://youtube.com/watch?v=..."` baixa só a **legenda** (nunca o vídeo) com o `yt-dlp` e grava `fontes/AAAA-MM-DD-título.md` com frontmatter (`tipo: fonte`, `url`, `origem`), marcas de tempo `**[mm:ss]**` a cada minuto e um aviso: **transcrição é pista, não fonte para ensinar** (Regra 8; `references/pedagogia.md` → "Fontes e versão"). Prefere a legenda original do vídeo; aceita também um `.vtt` ou `.srt` local. Requer `python -m pip install --user yt-dlp` (e o Node, se existir, para o YouTube). O link vai só ao YouTube. Se o vídeo não tiver legenda, o comando diz isso; transcrever o áudio exigiria o Whisper e o ffmpeg, que não fazem parte do sistema.
- **Base de sessões:** cada matéria nasce com `_sessoes-[matéria].base`, uma tabela nativa do Obsidian (recurso Bases) que lista as notas de `sessoes/` pelo frontmatter, e o painel já aponta para ela. É o recurso nativo Bases do Obsidian (precisa estar ligado em Plugins do núcleo); se a tabela não abrir, as notas continuam valendo.
- **Cartões para o Obsidian (opcional):** `cofre.py cartoes "matéria"` (linhas `pergunta :: resposta` no stdin ou em `--arquivo`) acrescenta cartões a `cartoes.md` no formato do plugin Spaced Repetition (`pergunta::resposta`, etiqueta `#flashcards/[matéria]`), sem repetir. **Só use se eu tiver instalado o plugin e pedir `"cartões"`.** A fila do `fila.py` continua sendo a única fonte de verdade da Revisão do dia: o que eu revisar pelo plugin não é registrado na fila.
- **Abrir no Obsidian:** `cofre.py abrir "matéria" [sessoes/arquivo.md]` abre a nota (ou o painel) por `obsidian://open`. O nome do cofre no Obsidian precisa ser o da pasta (confira em Gerenciar cofres); `--imprimir` só mostra o link.
- **Transcrição automática** da conversa: o hook de diário (abaixo), desligado por padrão.

**Opcional, na interface do Obsidian (não mexo nos seus arquivos de configuração):** em Configurações → Arquivos e links → "Local padrão para novos anexos", escolha a opção que preferir para imagens que **eu** colar direto numa nota. O Obsidian também tem uma CLI oficial (a partir da versão 1.12, ativada em Configurações → Geral) e um esquema `obsidian://` com `new` e `search`; a skill não depende deles, porque escrever os arquivos direto já resolve.

### Diagramas (`render.py`)

`python "<pasta>/render.py" mermaid entrada.mmd saida.png` (ou `svg`) usa o Chrome ou o Edge que já estão instalados. Ele **valida a sintaxe e devolve a mensagem exata do erro** (linha e ponto), e só gera o PNG quando está válido; aí você **olha** a imagem. Precisa de rede para carregar o Mermaid 11.17.2 (versão fixa, com verificação de integridade; ou `--mermaid-js` com um arquivo local). Para guardar a imagem na matéria: `cofre.py anexar "matéria" saida.png` e cole o `EMBED` na nota. Sem navegador: só verificação por leitura, e diga isso. `render.py detectar` mostra o que está disponível.

## Hooks automáticos (só quando instalado como plugin)

Dois hooks acompanham o plugin; eles **rodam código na sua máquina**, por isso ficam descritos aqui e no README:

- **Abertura da sessão (`SessionStart`):** se a pasta atual (ou uma das 4 acima) for um cofre, injeta o resumo de `cofre.py resumo` — posição, pendências e revisão do dia. Fora de um cofre, **não faz nada** (sai em menos de 1 segundo, sem saída). Com esse bloco na abertura, `"retomar"` já começa sabendo onde você parou.
- **Fim de cada resposta (`Stop`), desligado por padrão:** espelha a conversa em `[matéria]/sessoes/AAAA-MM-DD-auto.md`, em callouts do Obsidian, como o `md-log` do `learn`. Só grava se você **ligar** (`TUTOR_LOG=1` no ambiente, ou um arquivo vazio `.tutor-log` na raiz do cofre), só em cofre, e só em conversas em que esta skill foi usada. Para desligar, apague o `.tutor-log`.

Os dois procuram `python` e, se não houver, `python3`; sem nenhum dos dois, ficam em silêncio e a skill segue pelo plano B. Rodam pelo shell (Git Bash no Windows).

## Arquivos: com e sem acesso

- **Com acesso** (Claude Code, aba Code do app de desktop): crie e atualize a estrutura e os registros de `references/sessao.md` → "Estrutura de pastas", e grave a nota da sessão ao fim de cada sessão. É o que faz o papel de espelhar a conversa num arquivo para eu ler no Obsidian — por padrão **só o que vale reler**, não a transcrição. Quem quiser a transcrição automática liga o hook de diário (ver "Hooks automáticos (só quando instalado como plugin)").
- **Sem acesso** (chat do claude.ai): não há onde gravar. Entregue o **Cartão de retomada** (`references/sessao.md` → "Sem acesso a arquivos — Cartão de retomada").

Nos dois casos, **nunca apague nem sobrescreva** arquivos meus em `pratica/`. Antes de atualizar um registro, leia a versão atual.

## Formatação

- **Markdown** para tudo. Código em blocos com a linguagem.
- **LaTeX** sempre que houver matemática: `$f(x) = x^2$` em linha e `$$` em bloco próprio. Não escreva `f(x) = x^2` em texto simples quando LaTeX resolve.
- **Mermaid** em bloco ```` ```mermaid ````. Renderiza no Obsidian e no GitHub. Em algumas interfaces de chat o bloco aparece como código; nesse caso, o diagrama também vai para a nota da sessão, onde renderiza (`references/visuais.md`).
