# Referência — Cofre Obsidian por arquivos (cofre de estudos)

> Leia antes de **qualquer** leitura ou escrita no cofre: retomar uma matéria, criar matéria, gravar registros e nota da sessão, guardar visual, transcrever vídeo, gerar cartões, abrir uma nota.

> **Princípio:** o cofre do Obsidian é uma **pasta de arquivos Markdown**. O Claude a lê e escreve com as ferramentas de arquivo (`Read`, `Write`, `Edit`, `Glob`, `Grep` e o Bash para `mkdir`/`cp`), normalmente com o plugin **Claudian** (o cofre é o diretório de trabalho) ou com o Claude Code aberto na pasta do cofre. Não há servidor MCP. Python ficou só para o que é cálculo (`quiz.py`, `fila.py`) e para validar desenho (`render.py`); **nenhum script toca o cofre**.

> **Nesta referência:**
> **1. Ferramentas**
> **2. Como editar: a regra de ouro**
> **3. Regras de segurança do cofre**
> **4. Achar a raiz do cofre**
> **5. Receitas**
>     · Retomar (ler a posição e a Revisão do dia)
>     · Criar a matéria
>     · Atualizar os registros
>     · Gravar a nota da sessão
>     · Visuais e imagens (`"anexa"`)
>     · Transcrever um vídeo (`"transcreve"`)
>     · Terminal + Obsidian (modo cofre)
>     · Exercícios, desafios e provas como nota (`"exportar"`), corrigir um exercício e boletim (`"boletim"`)
>     · Cartões (`"cartões"`)
>     · Abrir no Obsidian (`"abrir"`)
>     · Buscar no cofre
>     · Conferir o cofre
> **6. Sem acesso a arquivos**

## Ferramentas

| Ferramenta | Para que serve aqui |
|---|---|
| `Glob` | listar pastas e arquivos (`{RAIZ}/*`, `{RAIZ}/*/registros-da-skill/*.md`); serve também para ver se um arquivo **já existe** |
| `Read` | ler uma nota inteira. Vários `Read` na **mesma resposta** leem vários arquivos de uma vez |
| `Grep` | buscar texto no cofre (frontmatter, tags, termos) |
| `Write` | **cria** o arquivo (e as pastas do caminho) ou **sobrescreve tudo** se ele já existir |
| `Edit` | trocar um **trecho exato** de um arquivo, deixando o resto intacto |
| `Bash` | só para `mkdir -p`, `cp` de imagem e `date +%F`. **Não** use `rm`, `mv` nem redirecionamento (`>`, `>>`) para gravar nota: para isso há `Write` e `Edit` |

**Caminhos:** use o caminho **relativo ao diretório de trabalho** quando ele for o cofre (Claudian), ou o caminho completo do disco quando o cofre estiver em outro lugar. Use `/` e escreva sempre dentro de `{RAIZ}` (seção 4).

**Data de hoje:** vem do contexto da conversa; se não vier, `date +%F` no Bash (não calcule de cabeça).

## Como editar: a regra de ouro

Escolha o **menor** instrumento que faz o serviço, nesta ordem:

| Quero… | Use |
|---|---|
| **criar** um arquivo novo | confirme que não existe (`Glob` no caminho) e então `Write` |
| **trocar um trecho** (uma linha, uma célula, o corpo de uma seção, um campo do frontmatter) | `Read` do arquivo e `Edit` com `old_string` **único** e exato. Para mudar o corpo de uma seção, use como `old_string` o corpo atual inteiro da seção |
| **acrescentar ao fim** de um arquivo ou seção | `Edit` ancorado na última linha atual (repita-a em `old_string` e devolva-a em `new_string` seguida da linha nova) |
| **mudar o mesmo texto em vários lugares** | `Edit` com `replace_all` (só se for exatamente o mesmo texto) |
| **reescrever o arquivo quase todo** | `Read` → montar o arquivo inteiro → `Write`, **só** em arquivo que é do Claude (registros, painel, notas de sessão, `README.md` e `CLAUDE.md` do cofre), logo depois da leitura, **mantendo o resto igual, caractere por caractere** |

Detalhes que mordem:
- `Edit` falha se o `old_string` não for único ou não bater exatamente (espaços, acentos, emojis). Releia o trecho e inclua mais contexto; **nunca** caia para `Write` só porque o `Edit` falhou: leia de novo e ajuste o trecho.
- Tabelas Markdown: troque a **linha inteira** da tabela, não só uma célula, para o `old_string` ser único.
- O `Write` exige que o arquivo existente tenha sido lido antes na sessão; se der esse erro, leia e tente de novo.
- **Conferência proporcional.** `Edit` e `Write` devolvem erro quando falham; se voltaram sem erro, a troca exata aconteceu e não precisa reler cada uma. Releia (a seção ou o arquivo) **depois de um `Write` sobre arquivo que já existia**, e **sempre uma vez ao fim** de uma criação ou de um `"salva"` (um `Glob` mais um `Read` ou `Grep` nos pontos que mudaram; não pule). Nunca diga "conferi" sem ter feito isso, e diga o que não foi relido.

## Regras de segurança do cofre

1. **Ler antes de escrever.** Antes de alterar qualquer arquivo existente, leia a versão atual. Nada de reescrever de memória.
2. **`Write` em arquivo existente é sobrescrita total** e só vale nos casos da tabela acima, em arquivo do Claude, logo após ler. Em arquivo que eu escrevi (tudo em `pratica/`, qualquer nota minha fora das pastas da skill), **nunca**.
3. **`pratica/` é meu.** Nunca escreva, edite nem apague nada em `pratica/` além do `_leia-me.md` criado junto com a matéria.
4. **Nunca apague nem mova.** Esta skill não usa `rm`, `mv` nem `del`. Se algo precisa sumir, diga o que e por quê, e eu apago.
5. **Só dentro da raiz do cofre de estudos** (próxima seção). Nada fora dela, e nunca na pasta `.obsidian/` (configurações do Obsidian).
6. **Confirme depois de gravar** (regra de ouro). Se a ferramenta devolveu erro, **diga o erro** e não finja que gravou; o plano B (seção 6) existe para isso.
7. **`Write` cria o arquivo se ele não existe:** um erro de digitação no caminho cria uma nota nova no lugar errado. Confira o caminho antes e, se criou sem querer, diga a mim (não apague).
8. **Texto em UTF-8, só com LF**, acentos normais, sem caracteres de controle.

## Achar a raiz do cofre

A **raiz de estudos** (`RAIZ`) é a pasta do cofre Obsidian que contém o `CLAUDE.md` ponteiro, o `README.md` e as pastas das matérias. Pode ser uma subpasta (`estudos/`) ou o próprio cofre (`RAIZ` vazia).

1. **Onde estou?** Se o diretório de trabalho tem uma pasta `.obsidian/`, ou (sem Obsidian) já tem o `CLAUDE.md` da skill, pastas com `registros-da-skill/` ou se chama `Estudos`, ele **é** a pasta de estudos: o Obsidian é só um leitor opcional e a skill funciona igual sem ele (caso normal do Claudian e do atalho `estudar`) (que abre o Claude Code já dentro do cofre). Se não tem, veja se alguma pasta acima ou abaixo a tem. Se nenhuma, descubra o cofre aberto no Obsidian lendo (`Read`) o `obsidian.json` (Windows: `%APPDATA%\obsidian\obsidian.json`, no Git Bash `~/AppData/Roaming/obsidian/obsidian.json`; macOS: `~/Library/Application Support/obsidian/obsidian.json`; Linux: `~/.config/obsidian/obsidian.json`): cada item de `vaults` tem `path` e o aberto traz `"open": true`. **Mostre o caminho e peça meu "ok"** antes de gravar. Como esse caminho fica fora do diretório de trabalho, o Claude Code pode pedir permissão de escrita; o jeito de evitar é abrir com o atalho `estudar` (ou `claude` dentro da pasta do cofre). Sem `obsidian.json` legível, pergunte o caminho (pergunta com opções).
2. `Glob` por `*` na raiz do cofre (e `**/CLAUDE.md`, `**/registros-da-skill`) para achar a candidata: pasta com `CLAUDE.md` que cite `tutor-adaptativo` (leia para conferir) ou com subpastas que tenham `registros-da-skill/`. Uma candidata: use-a. Mais de uma: pergunte qual (pergunta com opções).
3. **Nada encontrado:** é cofre novo. Proponha `Estudos/` (ou a raiz do cofre, se for um cofre só de estudos), peça meu "ok" e crie na primeira matéria.
4. Guarde `RAIZ` para a sessão inteira e **mostre-a uma vez** ("Cofre: `estudos/`") para eu corrigir se estiver errada. Registre-a no `trilha.md` (campo "Raiz dos estudos no cofre").
5. **Nome do cofre** (só para o link `obsidian://`): é o nome da pasta que contém `.obsidian/` (o Obsidian usa o nome da pasta). Se tiver dúvida, pergunte uma vez.

Daqui em diante, `{RAIZ}/{matéria}/...` quer dizer o caminho completo a partir do cofre.

## Receitas

### Retomar (ler a posição e a Revisão do dia)

1. **Uma rodada só de busca:** `Glob` em paralelo de `{RAIZ}/*/registros-da-skill/progresso.md` e `**/registros-da-skill/progresso.md`. Vieram vazios: **pare e responda** (não vasculhe outras pastas): diga que não achou registros e pergunte pelo Cartão de retomada ou ofereça começar com a entrevista. Mais de uma matéria: siga `references/sessao.md` → "Se há mais de uma matéria ativa".
2. **Numa resposta só**, faça três `Read` em paralelo: `{RAIZ}/{sg}/registros-da-skill/progresso.md`, `…/conquistas.md` e `…/conhecimento.md`. Use "Posição atual" e "Pendências abertas" do progresso, a linha `- **Última sessão:** AAAA-MM-DD` do conquistas (decide a Reentrada) e a fila do conhecimento. Leia o `trilha.md` só se precisar do contexto (orçamento de tempo, fonte e versão congelada).
3. **Revisão do dia:** com Python (`py` no Windows, `python3` nos outros; veja `references/ferramentas.md` → "Scripts da skill"), `python "<pasta>/fila.py" vencidos "{RAIZ}/{sg}/registros-da-skill/conhecimento.md" --max 3` (lê o arquivo; datas por código). Sem Python, aplique a tabela de `references/pedagogia.md` → "Fila de revisão espaçada".
4. Siga `references/sessao.md` → "Retomar e continuar".

Se **nenhum** registro existir, é matéria nova (Entrevista), nunca "retomada de memória".

### Criar a matéria

Roda **uma vez**, depois do meu "ok" no plano. Repetir não altera nada, porque cada arquivo só é criado se ainda não existir (`Glob` na pasta antes e **pule** o que já existe).

**Nome da pasta (`sg`):** o nome da matéria sem acento, em minúsculas, com hifens, até 60 caracteres (`Matemática Básica` → `matematica-basica`). Sem `| [ ] # ^ \ / : * ? " < >` no nome mostrado. Recuse nomes que o Windows reserva (`con`, `prn`, `aux`, `nul`, `com1`…`com9`, `lpt1`…`lpt9`) e peça outro.

**Os arquivos**, na ordem (cada um com `Write`, que cria as pastas do caminho; o conteúdo vem dos templates de `references/templates.md`, com `[Nome da Matéria]` e `[Matéria]` trocados pelo nome mostrado e `[matéria]` pelo `sg`):

| # | Caminho | Conteúdo |
|---|---|---|
| 1 | `{RAIZ}/CLAUDE.md` | template "`CLAUDE.md`" (só se não existir; é um por cofre, sem frontmatter) |
| 2 | `{RAIZ}/{sg}/registros-da-skill/trilha.md` | template `trilha.md`, com `**Status:** rascunho` e "Raiz dos estudos no cofre" preenchida |
| 3 | `…/registros-da-skill/progresso.md` | template `progresso.md`, com "Próximo passo: fazer a entrevista" |
| 4 | `…/registros-da-skill/conhecimento.md` | template `conhecimento.md` |
| 5 | `…/registros-da-skill/conquistas.md` | template de `references/projetos.md` → "Changelog de conquistas", com a data de hoje em "Última sessão" |
| 6 | `{RAIZ}/{sg}/_painel-{sg}.md` | template "Painel inicial" de `references/templates.md` |
| 7 | `{RAIZ}/{sg}/_sessoes-{sg}.base` | template "`_sessoes-[matéria].base`" (tabela nativa de sessões; se a gravação falhar, pule este e o link no painel, sem drama) |
| 7b | `{RAIZ}/{sg}/_provas-{sg}.base`, `{RAIZ}/{sg}/_exercicios-{sg}.base` e `{RAIZ}/{sg}/_boletim-{sg}.md` | templates do boletim em `references/templates.md` (as tabelas ficam vazias até a primeira prova ou exercício; mesma regra do item 7 se a gravação do `.base` falhar: pule as bases e as seções do boletim que as mostram) |
| 8 | `{RAIZ}/{sg}/pratica/projeto/_leia-me.md` e `{RAIZ}/{sg}/pratica/treinos/_leia-me.md` | template "`_leia-me.md` de `pratica/`" (já diz de quem é a pasta; o `Write` cria as pastas) |
| 9 | `{RAIZ}/README.md` | se não existir, o template "`README.md`" sem a linha-modelo. Se existir, leia e **acrescente** a linha `- [[_painel-{sg}\|Nome]] — ▶ fazer a entrevista` ao fim da seção `Matérias ativas` (`Edit` ancorado na última linha da seção); se a seção tiver a linha-modelo `- (nenhuma ainda…)`, troque essa linha pela nova. Nunca duplique: procure `_painel-{sg}` antes (`Grep`) |

`sessoes/`, `anexos/` e `fontes/` **nascem sozinhas** quando a primeira nota, imagem ou transcrição for gravada nelas. Não crie arquivos-fantasma para elas.

Ao terminar: **confira** (receita "Conferir o cofre"), mostre a árvore criada (Regra 30) e diga onde eu mexo (`pratica/`) e onde não (`registros-da-skill/`).

### Atualizar os registros

`progresso.md`, `conhecimento.md`, `conquistas.md`, `trilha.md` e o painel mudam pela **regra de ouro**:

- **Posição atual, Pendências abertas** (progresso): `Read`, depois `Edit` com o corpo atual da seção como `old_string` e o corpo novo inteiro como `new_string` (mantenha a linha de citação `>` do início da seção).
- **Linha do tempo (sessões)** (última seção do progresso): `Edit` ancorado na última linha, acrescentando a linha nova depois dela.
- **Histórico de provas e Checkpoints:** têm subtítulos (`## Prova — …`). Acrescente o bloco (o `quiz.py placar` já devolve o bloco pronto) com `Edit` ancorado no fim do grupo certo.
- **Última sessão e o dashboard do `conquistas.md`:** `Edit` na linha `- **Última sessão:** …` (com os asteriscos) e nas linhas do dashboard que mudaram. Linha nova no changelog de conquistas: `Edit` ancorado na última linha do changelog.
- **Fila de revisão:** com Python, rode `python "<pasta>/fila.py" registrar "{RAIZ}/{sg}/registros-da-skill/conhecimento.md" --conceito "..." --resultado novo|acerto|acerto-fragil|erro|erro-confiante --parte "T1 / 1a" --sem-gravar` (**sempre** `--sem-gravar` dentro do cofre). O script **só lê**: imprime `SECAO:`, `CONTEUDO:` (a seção inteira já atualizada) e `FIM`. Aplique com **um** `Edit`: `old_string` = a seção atual da fila (tabela inteira, como acabou de ler) e `new_string` = o `CONTEUDO`. Sem Python, calcule à mão pela tabela de `references/pedagogia.md`.
- **Frontmatter:** `topico`, `data`, `status` e afins: `Edit` na linha do campo. Adicionar campo ou tag nova: `Edit` na linha de `tags:` ou no `---` de abertura, ou regrave o arquivo se for mais simples.
- **`trilha.md`:** quando o plano for aprovado, troque `**Status:** rascunho` por `**Status:** aprovado em AAAA-MM-DD` e complete as seções, com `Edit` por seção (ou `Write` do arquivo inteiro, que é do Claude, logo após ler).

### Gravar a nota da sessão

Caminho: `{RAIZ}/{sg}/sessoes/AAAA-MM-DD-{título-em-slug}.md` (título sem acento, minúsculo, hifens; se eu não dei título, use o tópico).

1. **Já existe uma nota do dia com esse nome?** (`Glob` em `sessoes/`; a pasta pode nem existir ainda.)
   - **Não:** `Write` com o template "nota da sessão" de `references/templates.md` (frontmatter `tipo`, `materia`, `data`, `topico`, `tags`).
   - **Sim:** `Read` e `Edit` ancorado na última linha, acrescentando `---`, `## Acrescentado às HH:MM` e o novo trecho. Nunca sobrescreva.
2. **Liste a nota no painel**, em `## Sessões recentes` do `_painel-{sg}.md`: leia o painel e troque com `Edit` o corpo da seção: a linha `> Tabela com todas…` primeiro, depois `- [[AAAA-MM-DD-título]] — a ideia que encaixou` e as demais; sem a linha `- (nenhuma sessão ainda)`. **Só as 8 notas mais recentes ficam listadas** (linhas no formato `- [[AAAA-MM-DD-…]]`); **linhas que eu escrevi à mão na seção nunca saem.**
3. Se a nota tem visual (próxima receita), ele já entra no corpo antes de gravar.
4. Atualize o `▶ próximo passo` (bloco `> [!info]` no topo) e o mapa do painel com `Edit` nos trechos que mudaram. Se existe o `_boletim-{sg}.md`, atualize só a linha do bloco `> [!info] Situação` (data, posição, quantas pendências abertas), lendo os números do `progresso.md`.
5. Confira uma vez ao fim (releia o painel e a nota).

### Visuais e imagens (`"anexa"`)

Ordem de preferência:

1. **Bloco ```` ```mermaid ```` direto no corpo da nota.** É texto, renderiza nativo no Obsidian e é o caminho padrão para diagramas.
2. **Arquivo `.svg` em `anexos/`**, gravado com `Write` em `{RAIZ}/{sg}/anexos/AAAA-MM-DD-nome.svg` (SVG é texto). Entra na nota com `![[AAAA-MM-DD-nome.svg]]` (largura opcional: `![[…svg|500]]`). Nome sem acento, minúsculo, com hifens; nunca reaproveite um nome que já existe (acrescente `-2`).
3. **PNG ou outra imagem** (gerada pelo `render.py`): como o cofre é uma pasta no disco, copie pelo Bash: `mkdir -p "{RAIZ}/{sg}/anexos" && cp imagem.png "{RAIZ}/{sg}/anexos/AAAA-MM-DD-nome.png"` e embuta com `![[AAAA-MM-DD-nome.png]]`; confira com `Glob`.
4. **Print que eu copiei da tela:** o Claude não enxerga a minha área de transferência. Peça para colar direto na nota no Obsidian (Ctrl+V); se o Claude precisa **olhar** a imagem, eu a anexo na conversa.

Verificação e escolha do tipo de visual: `references/visuais.md` e `references/visuais-modelos.md`.

### Transcrever um vídeo (`"transcreve"`)

A transcrição é **pista, não fonte para ensinar** (Regra 8; `references/pedagogia.md` → "Fontes e versão").

1. **Conseguir o texto.** Prefira o que eu colar na conversa ou um `.vtt`/`.srt` que eu indicar (leia com `Read`). Se eu der só o link e o `yt-dlp` existir no ambiente, baixe **só a legenda**, sem o vídeo: `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "pt.*,en.*" --sub-format vtt -o "%(title)s" "<link>"` (rode numa pasta temporária, **fora** do cofre). Sem legenda, ou sem `yt-dlp`, diga isso: transcrever áudio não faz parte do sistema.
2. **Limpar.** Tire marcas de tempo repetidas, tags e linhas duplicadas das legendas automáticas; agrupe por minuto com `**[mm:ss]**` no começo de cada bloco. Textos acima de ~3000 palavras: grave uma versão **condensada** por minuto, não o texto cru, e diga que está condensada.
3. **Gravar** (`Write`) em `{RAIZ}/{sg}/fontes/AAAA-MM-DD-título.md` com o frontmatter `tipo: fonte`, `materia`, `data`, `url` (link **limpo**: sem `list`, `index`, `t`, `si` e rastreio) e `origem` (youtube, arquivo…), um aviso `> [!warning]` dizendo que é pista e não fonte, e o texto.
4. Se algo da transcrição for entrar na aula, **confirme na fonte oficial** antes.

### Cartões (`"cartões"`)

Só se eu uso o plugin **Spaced Repetition** e pedi. A fila do `conhecimento.md` continua sendo a **única** fonte da Revisão do dia.

1. Leia `{RAIZ}/{sg}/cartoes.md` (se existir) para não repetir cartões.
2. Não existe: `Write` com frontmatter (`tipo: cartoes`, `materia`, `tags`), o título `# Cartões — Nome` e a linha `#flashcards/{sg}`.
3. Existe: `Edit` ancorado na última linha, acrescentando os novos, **uma linha cada**, no formato `pergunta::resposta` (sem espaços em volta de `::`), pulando os que já existem.

### Terminal + Obsidian (modo cofre)

Meu jeito de estudar é conversar com o Claude Code no terminal e **ler e guardar no Obsidian**: ler texto longo no terminal cansa e some quando a janela rola. Por isso, com o cofre ao alcance (seção 4):

1. **Vai direto para uma nota, sem eu pedir:** o enunciado de cada **exercício e desafio** (template "exercício ou desafio"), cada **visual** que valha guardar (receita "Visuais e imagens") e o **caderno** de uma prova em nota (abaixo). Grave a nota e, em seguida, **abra-a no Obsidian** (receita "Abrir no Obsidian"). No terminal, diga em **uma ou duas linhas** o que gravou, o caminho e o que eu devo fazer ("abri o exercício no Obsidian; faça e me diga quando terminar"). **Não repita o enunciado, o critério nem as dicas no terminal**: eles estão na nota. Confirme a gravação com um `Glob` antes de dizer que gravou.
2. **Continua na conversa, ao vivo:** sondagem, checagens de uma pergunta, cada questão de quiz, dica, correção, celebração, o próximo passo. São curtos e dependem da minha última resposta (Regra 2).
3. **A resposta é minha e vai em `pratica/treinos/t[N]-[parte]/`.** Eu escrevo lá (código, texto ou um desenho do Excalidraw). Para o Claude revisar um **desenho**, exporte o Excalidraw como PNG ou SVG para essa pasta e diga o nome: o Claude lê a imagem com `Read`. O Claude **não gera** `.excalidraw`: seus diagramas são Mermaid ou SVG verificados pelo `render.py`.
4. **Prova em nota (só se eu pedir "prova em nota"):** é a única exceção ao "uma pergunta por vez", escolhida por mim. Monte **todas** as questões com `quiz.py montar` (uma chamada por questão, cada uma com a mesma `--prova`), grave `provas/AAAA-MM-DD-{tópico}-{parte}-caderno.md` com as perguntas e as opções **na ordem devolvida**, sem a certa e sem a explicação, e abra no Obsidian. Eu respondo no terminal de uma vez (`1B 🟢, 2A 🔴, 3 não sei`). Corrija cada uma com `quiz.py corrigir`, feche com `placar --fechar` e grave o relatório (template "relatório de prova"). Nunca mostre a certa antes de eu responder.
5. **Sem cofre ao alcance** (sem acesso à pasta ou sem permissão de escrita): tudo volta para a conversa, curto, e diga isso (seção 6).

### Exercícios, desafios e provas como nota (`"exportar"`)

No modo cofre isto já acontece sozinho para o exercício e o desafio. `"exportar"` serve para gravar **depois** algo que ficou só na conversa, e para o relatório da última prova ("põe esse exercício numa nota"). A aula, o quiz e a prova continuam **ao vivo na conversa** (Regra 2); a nota é para eu abrir no Obsidian, reler e refazer.

1. **Exercício ou desafio atual:** caminho `{RAIZ}/{sg}/exercicios/AAAA-MM-DD-{tópico}-{parte}-{nome-em-slug}.md` (slug: minúsculo, sem acento, só letras, números e hifens). Se já existe (`Glob`), não sobrescreva: acrescente `-2`. Grave com `Write` a partir do template "exercício ou desafio" de `references/templates.md`: enunciado, critério de pronto e a escada de dicas **dobrada**, **sem a solução**. Dê o `[[link]]` e diga que a minha resposta vai em `pratica/treinos/t{N}-{parte}/` (essa pasta é minha; não crie nada nela).
2. **Última prova fechada:** caminho `{RAIZ}/{sg}/provas/AAAA-MM-DD-{tópico}-{parte}-{nome-da-prova}.md`, template "relatório de prova". Preencha **só** com os resultados que o `quiz.py` devolveu nesta conversa e com o bloco do `placar`. Se faltar algum (a conversa foi cortada), deixe a linha de fora e diga qual faltou; nunca reconstrua de memória. A pasta `provas/` e o `progresso.md` não se substituem: o resultado oficial continua no `progresso.md`.
3. Sem Python não há `placar`: use os números que você corrigiu à mão e diga que foi à mão.
4. Confira uma vez (`Glob` e `Read` da nota) e liste a nota no `_painel-{sg}.md`, na seção `## Sessões recentes`, só se ela fizer parte da sessão do dia (a nota da sessão pode apenas linkar o exercício).

**Corrigir um exercício (quando eu digo que fiz):** leia a minha resposta em `pratica/treinos/t{N}-{parte}/` (código, texto ou imagem exportada do Excalidraw, com `Read`), corrija ao vivo na conversa (celebrar, uma melhoria) e então, com `Edit` na nota de `exercicios/`: troque `status: pendente` por `status: feito` e acrescente a seção "Correção" do template. Não mexa em nada de `pratica/`.

### Boletim (`"boletim"`)

O boletim é a nota `_boletim-{sg}.md`, que mostra em tabelas as provas (com a média), os exercícios e as sessões, todas lidas do frontmatter das notas. `"boletim"`: se a nota não existe (matéria criada antes da 5.1), crie-a e as duas bases com os templates; atualize a linha "Situação" como na nota da sessão; abra no Obsidian; e diga em duas linhas o que a tabela mostra. A média das provas é o resumo da tabela do Obsidian: **não calcule nem escreva de cabeça**. Para o resultado oficial de cada prova, vale o `progresso.md`.

### Abrir no Obsidian (`"abrir"`)

O endereço é `obsidian://open?vault={nome-do-cofre}&file={caminho-sem-.md}`, com o caminho codificado (`/` vira `%2F`, espaço vira `%20`). O `nome-do-cofre` é o da seção 4, passo 5. Exemplo: `obsidian://open?vault=Estudos&file=ingles%2F_painel-ingles`.

**Abrir sozinho no Obsidian** (testado no Windows 11: abre o app, se estiver fechado, e a nota): no Windows, `cmd.exe //c start "" "obsidian://open?vault=Estudos&file=…"` pelo Bash (ou `Start-Process "obsidian://…"` pela ferramenta PowerShell, se houver); macOS: `open "obsidian://…"`; Linux: `xdg-open "obsidian://…"`. Mantenha o endereço entre aspas por causa do `&`. A nota já tem de existir. Se a chamada for barrada ou falhar, entregue o **link** para eu clicar e diga que não abriu. No Claudian, eu também posso clicar no `[[link]]` da nota.

### Buscar no cofre

`Grep` ("onde eu já vi X?", com contexto), restrito a uma pasta quando der (`{RAIZ}/{sg}`); `Glob` para achar por nome; `Grep` por `tags:` ou `#tag` para tags. Use também antes de acrescentar um termo ao glossário ou um conceito à fila, para não duplicar.

### Conferir o cofre

Depois de criar a matéria ou de mudar a estrutura, `Glob` em `{RAIZ}/{sg}/**` e confira, contra os nomes de `references/sessao.md` → "Nomes canônicos":

- existem `registros-da-skill/trilha.md`, `progresso.md`, `conhecimento.md`, `conquistas.md` e `_painel-{sg}.md`;
- `progresso.md` tem as cinco seções com os nomes exatos (`## Posição atual`, `## Pendências abertas`, `## Histórico de provas`, `## Checkpoints`, `## Linha do tempo (sessões)`);
- `trilha.md` tem a linha `**Status:** rascunho` (ou `aprovado em …`);
- `conquistas.md` tem `- **Última sessão:** AAAA-MM-DD`;
- a tabela de `conhecimento.md` tem as seis colunas (`fila.py mostrar CAMINHO` confirma);
- as notas de `sessoes/` se chamam `AAAA-MM-DD-[tópico].md`.

Liste o que faltar ou divergir e corrija com as receitas acima.

## Sem acesso a arquivos

Nunca trave por falta de acesso (Regra 33). Se o Claude **não alcança** a pasta do cofre (chat do claude.ai, ou nuvem sem a pasta) ou uma gravação falhou (cofre em outra máquina, permissão negada, caminho errado):

1. **Diga o erro exato** e o que falta (abrir o Claudian ou o Claude Code na pasta do cofre; liberar escrita nela).
2. **Não finja que gravou.** Enquanto isso, segure o conteúdo no **Cartão de retomada** (`references/sessao.md` → "Sem acesso a arquivos — Cartão de retomada") e entregue o texto da nota da sessão para eu colar.
