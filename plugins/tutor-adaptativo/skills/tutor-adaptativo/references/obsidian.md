# Referência — Obsidian pelo MCP (cofre de estudos)

> Leia antes de **qualquer** leitura ou escrita no cofre: retomar uma matéria, criar matéria, gravar registros e nota da sessão, guardar visual, transcrever vídeo, gerar cartões, abrir uma nota.

> **Princípio:** o cofre é lido e escrito pelas ferramentas do **MCP do Obsidian**, não por script. Python ficou só para o que é cálculo (`quiz.py`, `fila.py`) e para validar desenho (`render.py`). Plano B quando não houver o MCP: neste arquivo → "Sem o MCP".

> **Nesta referência:**
> **1. Ferramentas (servidor `mcp-obsidian`)**
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
>     · Cartões (`"cartões"`)
>     · Abrir no Obsidian (`"abrir"`)
>     · Buscar no cofre
>     · Conferir o cofre
> **6. Sem o MCP**
> **7. Outros servidores MCP do Obsidian**

## Ferramentas (servidor `mcp-obsidian`)

São 15 ferramentas (a lista foi conferida no código do servidor `mcp-obsidian` 0.2.3, que fala com o plugin **Local REST API** do Obsidian). O Claude Code mostra cada uma com o prefixo do nome que o servidor tem na configuração (por exemplo `mcp__obsidian__obsidian_get_file_contents`); aqui uso só o nome curto. **Caminhos são sempre relativos à raiz do cofre Obsidian**, com `/` e sem `/` no começo. Se a sua versão do servidor declarar parâmetros diferentes destes, vale o que a ferramenta declara.

| Ferramenta | Parâmetros | Para que serve aqui |
|---|---|---|
| `obsidian_list_files_in_vault` | — | listar a **raiz** do cofre (achar a pasta de estudos) |
| `obsidian_list_files_in_dir` | `dirpath` | listar uma pasta. **Pasta vazia ou inexistente não aparece** (dá erro): serve também para ver se um arquivo já existe |
| `obsidian_get_file_contents` | `filepath` | ler uma nota inteira |
| `obsidian_batch_get_file_contents` | `filepaths` (lista) | ler várias notas numa chamada só (devolve concatenadas, com cabeçalho por arquivo) |
| `obsidian_get_frontmatter` | `filepath` | só o frontmatter, como JSON |
| `obsidian_append_content` | `filepath`, `content` | **acrescentar ao fim**; se o arquivo não existe, **cria** |
| `obsidian_patch_content` | `filepath`, `operation` (`append`/`prepend`/`replace`), `target_type` (`heading`/`block`/`frontmatter`), `target`, `content` | mexer **numa seção** (cabeçalho), num bloco ou num campo do frontmatter, deixando o resto intacto |
| `obsidian_put_content` | `filepath`, `content` | **cria** o arquivo (e as pastas do caminho) ou **sobrescreve tudo** se ele já existir |
| `obsidian_simple_search` | `query`, `context_length` | busca de texto no cofre inteiro |
| `obsidian_complex_search` | `query` (JsonLogic) | busca por padrão de caminho ou regex (ex.: `{"glob": ["estudos/ingles/*.md", {"var": "path"}]}`) |
| `obsidian_search_by_tag` | `tag` (sem `#`), `dirpath` | notas com uma tag |
| `obsidian_get_recent_changes` | `limit`, `days` | arquivos mexidos recentemente |
| `obsidian_get_periodic_note`, `obsidian_get_recent_periodic_notes` | — | notas diárias/semanais: **não usadas** nesta skill |
| `obsidian_delete_file` | `filepath` | **não use** (ver regras) |

**Não existe** busca-e-troca de texto, nem criar pasta vazia, nem gravar arquivo binário. As receitas abaixo contornam isso.

**Data de hoje:** vem do contexto da conversa; se não vier, `date +%F` no Bash (não calcule de cabeça). O servidor espera respostas em até 6 s: arquivo muito grande pode estourar; nesse caso, repita a chamada e, se persistir, diga o erro.

## Como editar: a regra de ouro

Escolha o **menor** instrumento que faz o serviço, nesta ordem:

| Quero… | Use |
|---|---|
| **criar** um arquivo novo | confirme que não existe (`list_files_in_dir` da pasta, ou `get_file_contents` que dá erro) e então `put_content` |
| **acrescentar** ao fim de um arquivo | `append_content` |
| **trocar o corpo de uma seção plana** (texto, lista ou tabela, **sem subtítulos dentro**): "Posição atual", "Pendências abertas", "Fila de revisão espaçada", "Sessões recentes" | `patch_content` com `operation=replace`, `target_type=heading`, `target=` o nome do cabeçalho (sem `#`), e em `content` o corpo **novo inteiro**, terminando em linha em branco |
| **acrescentar** ao fim de uma seção plana | `patch_content` com `operation=append` (mesmo alvo) |
| **mudar um campo existente** do frontmatter (`topico`, `data`), valor simples | `patch_content` com `target_type=frontmatter`, `target=` o nome do campo, `operation=replace` |
| **qualquer outra mudança** (seção com subtítulos, como "Histórico de provas" e "Checkpoints"; várias partes de uma vez; tags; uma linha no meio de um texto) | **ler → montar o arquivo inteiro → `put_content`**, só em arquivo que é do Claude (registros, painel, notas de sessão, `README.md` e `CLAUDE.md` do cofre), logo depois da leitura, **mantendo o resto igual, caractere por caractere** |

Detalhes que mordem:
- O `target` de cabeçalho é o **caminho com `::`** quando há cabeçalhos pai (`📚 Inglês::Sessões recentes`); o servidor aceita só o nome (`Sessões recentes`) e o qualifica sozinho **se for único** no arquivo. Cabeçalhos dentro de blocos de código são ignorados. Acentos e emojis funcionam.
- `replace` num cabeçalho troca **o que está debaixo dele até o próximo cabeçalho**; a linha do próprio cabeçalho fica. Por isso o `content` precisa trazer **tudo** que deve continuar ali (inclusive a linha de citação `>` do início da seção).
- `patch_content` **não cria** campo de frontmatter nem cabeçalho que não existe: dá erro. Nesse caso, use `put_content` com o arquivo lido e ajustado.
- Em seção **com subtítulos**, não verifiquei como o servidor delimita a seção; por isso vai pelo caminho "ler → `put_content`".
- **Depois de toda edição, releia** (a seção ou o arquivo) e confira que só mudou o pretendido.

## Regras de segurança do cofre

1. **Ler antes de escrever.** Antes de alterar qualquer arquivo existente, leia a versão atual. Nada de reescrever de memória.
2. **`put_content` em arquivo existente é sobrescrita total** e só vale nos casos da tabela acima, em arquivo do Claude, logo após ler. Em arquivo que eu escrevi (tudo em `pratica/`, qualquer nota minha fora das pastas da skill), **nunca**.
3. **`pratica/` é meu.** Nunca escreva, edite nem apague nada em `pratica/` além do `_leia-me.md` criado junto com a matéria.
4. **Nunca apague.** Esta skill não usa `obsidian_delete_file`. Se algo precisa sumir, diga o que e por quê, e eu apago.
5. **Só dentro da raiz do cofre de estudos** (próxima seção). Nada fora dela.
6. **Confirme depois de gravar** (regra de ouro). Se a ferramenta devolveu erro, **diga o erro** e não finja que gravou; o plano B (seção 6) existe para isso.
7. **`append_content` cria o arquivo se ele não existe:** um erro de digitação no caminho cria uma nota nova no lugar errado. Confira o caminho antes e, se criou sem querer, diga a mim (não apague).
8. **Texto em UTF-8, só com LF**, acentos normais, sem caracteres de controle.

## Achar a raiz do cofre

A **raiz de estudos** (`RAIZ`) é a pasta do cofre Obsidian que contém o `CLAUDE.md` ponteiro, o `README.md` e as pastas das matérias. Pode ser uma subpasta (`estudos/`) ou o próprio cofre (`RAIZ` vazia).

1. `obsidian_list_files_in_vault` (pastas terminam em `/`).
2. Candidata = pasta com `CLAUDE.md` que cite `tutor-adaptativo` (leia para conferir), ou com subpastas que tenham `registros-da-skill/` (`list_files_in_dir`). Uma candidata: use-a. Mais de uma: pergunte qual (pergunta com opções).
3. **Nada encontrado:** é cofre novo. Proponha `estudos/` (ou a raiz do cofre, se for um cofre só de estudos), peça meu "ok" e crie na primeira matéria.
4. Guarde `RAIZ` para a sessão inteira e **mostre-a uma vez** ("Cofre: `estudos/`") para eu corrigir se estiver errada. Registre-a no `trilha.md` (campo "Raiz dos estudos no cofre").
5. **Pasta do cofre no disco (só para PNG):** se o Claude roda **na mesma máquina** do Obsidian, o Obsidian guarda a lista de cofres em `obsidian.json` (Linux: `~/.config/obsidian/obsidian.json`; macOS: `~/Library/Application Support/obsidian/obsidian.json`; Windows: `%APPDATA%\obsidian\obsidian.json`). Leia pelo Bash (`cat`) e pegue o `path` do cofre (o que tem `"open": true`, ou o que bate com o conteúdo listado). Confirme com uma listagem do disco. Guarde como `DISCO`. Se o arquivo não existe ou o Claude roda em outra máquina (nuvem), não há `DISCO`.

Daqui em diante, `{RAIZ}/{matéria}/...` quer dizer o caminho completo a partir da raiz do cofre.

## Receitas

### Retomar (ler a posição e a Revisão do dia)

1. `obsidian_list_files_in_dir` em `{RAIZ}` para ver as matérias (pastas com `registros-da-skill/`). Mais de uma: siga `references/sessao.md` → "Se há mais de uma matéria ativa".
2. **Uma chamada só:** `obsidian_batch_get_file_contents` com `{RAIZ}/{sg}/registros-da-skill/progresso.md`, `…/conquistas.md` e `…/conhecimento.md`. Use "Posição atual" e "Pendências abertas" do progresso, a linha "Última sessão: AAAA-MM-DD" do conquistas (decide a Reentrada) e a fila do conhecimento. Leia o `trilha.md` só se precisar do contexto (orçamento de tempo, fonte e versão congelada).
3. **Revisão do dia:** com Python, cole a seção `## Fila de revisão espaçada` no stdin: `python "<pasta>/fila.py" vencidos - --max 3` (datas por código). Sem Python, aplique a tabela de `references/pedagogia.md` → "Fila de revisão espaçada".
4. Siga `references/sessao.md` → "Retomar e continuar".

Se **nenhum** registro existir, é matéria nova (Entrevista), nunca "retomada de memória".

### Criar a matéria

Roda **uma vez**, depois do meu "ok" no plano. Repetir não altera nada, porque cada arquivo só é criado se ainda não existir (liste a pasta antes e **pule** o que já existe).

**Nome da pasta (`sg`):** o nome da matéria sem acento, em minúsculas, com hifens, até 60 caracteres (`Matemática Básica` → `matematica-basica`). Sem `| [ ] # ^ \ / : * ? " < >` no nome mostrado. Recuse nomes que o Windows reserva (`con`, `prn`, `aux`, `nul`, `com1`…`com9`, `lpt1`…`lpt9`) e peça outro.

**Os arquivos**, na ordem (cada um com `put_content`, que cria as pastas do caminho; o conteúdo vem dos templates de `references/templates.md`, com `[Nome da Matéria]` e `[Matéria]` trocados pelo nome mostrado e `[matéria]` pelo `sg`):

| # | Caminho | Conteúdo |
|---|---|---|
| 1 | `{RAIZ}/CLAUDE.md` | template "`CLAUDE.md`" (só se não existir; é um por cofre, sem frontmatter) |
| 2 | `{RAIZ}/{sg}/registros-da-skill/trilha.md` | template `trilha.md`, com `**Status:** rascunho` e "Raiz dos estudos no cofre" preenchida |
| 3 | `…/registros-da-skill/progresso.md` | template `progresso.md`, com "Próximo passo: fazer a entrevista" |
| 4 | `…/registros-da-skill/conhecimento.md` | template `conhecimento.md` |
| 5 | `…/registros-da-skill/conquistas.md` | template de `references/projetos.md` → "Changelog de conquistas", com a data de hoje em "Última sessão" |
| 6 | `{RAIZ}/{sg}/_painel-{sg}.md` | template "Painel inicial" de `references/templates.md` |
| 7 | `{RAIZ}/{sg}/_sessoes-{sg}.base` | template "`_sessoes-[matéria].base`" (tabela nativa de sessões; se a gravação falhar, pule este e o link no painel, sem drama) |
| 8 | `{RAIZ}/{sg}/pratica/projeto/_leia-me.md` e `{RAIZ}/{sg}/pratica/treinos/_leia-me.md` | template "`_leia-me.md` de `pratica/`" (é o que faz a pasta existir: não há como criar pasta vazia) |
| 9 | `{RAIZ}/README.md` | se não existir, o template "`README.md`" sem a linha-modelo. Se existir, leia e **acrescente** a linha `- [[_painel-{sg}\|Nome]] — ▶ fazer a entrevista` ao fim da seção `Matérias ativas` (`patch_content`, `append`, `heading`); se a seção tiver linha-modelo `- (nenhuma ainda…)`, refaça o arquivo inteiro (regra de ouro, última linha). Nunca duplique: procure `_painel-{sg}` antes |

`sessoes/`, `anexos/` e `fontes/` **nascem sozinhas** quando a primeira nota, imagem ou transcrição for gravada nelas. Não crie arquivos-fantasma para elas.

Ao terminar: **confira** (receita "Conferir o cofre"), mostre a árvore criada (Regra 30) e diga onde eu mexo (`pratica/`) e onde não (`registros-da-skill/`).

### Atualizar os registros

`progresso.md`, `conhecimento.md`, `conquistas.md`, `trilha.md` e o painel mudam pela **regra de ouro**:

- **Posição atual, Pendências abertas** (progresso): `patch_content replace` no cabeçalho, com o corpo novo inteiro.
- **Linha do tempo (sessões)** (última seção do progresso): `append_content` (ou `patch_content append` no cabeçalho) com a linha nova.
- **Histórico de provas e Checkpoints:** têm subtítulos (`## Prova — …`). Leia o `progresso.md`, acrescente o bloco (o `quiz.py placar` já devolve o bloco pronto) no fim do grupo certo e regrave o arquivo com `put_content`.
- **Última sessão e o dashboard do `conquistas.md`:** as linhas mudam em vários pontos; leia, ajuste e regrave com `put_content`. Linha nova no changelog de conquistas: `patch_content append` no cabeçalho do changelog, se for uma seção plana.
- **Fila de revisão:** com Python, cole a seção da fila e rode `python "<pasta>/fila.py" registrar - --conceito "..." --resultado novo|acerto|acerto-fragil|erro|erro-confiante --parte "T1 / 1a"`. O script **não grava**: imprime `SECAO:`, `CONTEUDO:` (a seção inteira já atualizada) e `FIM`. Aplique com **uma** chamada `patch_content` (`operation=replace`, `target_type=heading`, `target=` o valor de `SECAO`, `content=` o `CONTEUDO` mais uma linha em branco). Sem Python, calcule à mão pela tabela de `references/pedagogia.md`.
- **Frontmatter:** `topico`, `data`, `status` e afins: `patch_content` com `target_type=frontmatter`. Adicionar campo ou tag nova: regrave o arquivo.
- **`trilha.md`:** quando o plano for aprovado, troque `**Status:** rascunho` por `**Status:** aprovado em AAAA-MM-DD` e complete as seções: leia, ajuste e regrave com `put_content` (o arquivo é do Claude).

### Gravar a nota da sessão

Caminho: `{RAIZ}/{sg}/sessoes/AAAA-MM-DD-{título-em-slug}.md` (título sem acento, minúsculo, hifens; se eu não dei título, use o tópico).

1. **Já existe uma nota do dia com esse nome?** (`list_files_in_dir` em `sessoes/`; a pasta pode nem existir ainda.)
   - **Não:** `put_content` com o template "nota da sessão" de `references/templates.md` (frontmatter `tipo`, `materia`, `data`, `topico`, `tags`).
   - **Sim:** `append_content` com uma linha `---`, `## Acrescentado às HH:MM` e o novo trecho. Nunca sobrescreva.
2. **Liste a nota no painel**, em `## Sessões recentes` do `_painel-{sg}.md`: leia o painel e monte o corpo novo da seção: a linha `> Tabela com todas…` primeiro, depois `- [[AAAA-MM-DD-título]] — a ideia que encaixou` e as demais; sem a linha `- (nenhuma sessão ainda)`. **Só as 8 notas mais recentes ficam listadas** (linhas no formato `- [[AAAA-MM-DD-…]]`); **linhas que eu escrevi à mão na seção nunca saem.** Grave com `patch_content replace` no cabeçalho `Sessões recentes`.
3. Se a nota tem visual (próxima receita), ele já entra no corpo antes de gravar.
4. Atualize o `▶ próximo passo` (bloco `> [!info]` no topo) e o mapa do painel: o painel tem várias partes, então leia, ajuste e regrave com `put_content` (é arquivo do Claude).
5. Confira o resultado (releia o painel e a nota).

### Visuais e imagens (`"anexa"`)

O MCP grava **texto**, não arquivos binários. Por isso a ordem de preferência é:

1. **Bloco ```` ```mermaid ```` direto no corpo da nota.** É texto, renderiza nativo no Obsidian e é o caminho padrão para diagramas.
2. **Arquivo `.svg` em `anexos/`**, gravado com `put_content` em `{RAIZ}/{sg}/anexos/AAAA-MM-DD-nome.svg` (SVG é texto). Entra na nota com `![[AAAA-MM-DD-nome.svg]]` (largura opcional: `![[…svg|500]]`). Nome sem acento, minúsculo, com hifens; nunca reaproveite um nome que já existe (acrescente `-2`). Releia com `get_file_contents` para ver se o servidor gravou o texto como esperado.
3. **PNG ou outra imagem de verdade** (gerada pelo `render.py`, ou um print): o MCP não grava. Se há `DISCO` (receita "Achar a raiz do cofre", passo 5), copie pelo Bash: `mkdir -p "$DISCO/{RAIZ}/{sg}/anexos" && cp imagem.png "$DISCO/{RAIZ}/{sg}/anexos/AAAA-MM-DD-nome.png"` e embuta com `![[AAAA-MM-DD-nome.png]]`; confira com `list_files_in_dir`. Sem `DISCO`, **diga** e escolha: (a) embutir o diagrama como Mermaid/SVG; (b) eu colo a imagem direto na nota pelo Obsidian (Ctrl+V).
4. **Print que eu copiei da tela:** o Claude não enxerga a minha área de transferência. Peça para colar direto na nota no Obsidian; se o Claude precisa **olhar** a imagem, eu a anexo na conversa.

Verificação e escolha do tipo de visual: `references/visuais.md` e `references/visuais-modelos.md`.

### Transcrever um vídeo (`"transcreve"`)

A transcrição é **pista, não fonte para ensinar** (Regra 8; `references/pedagogia.md` → "Fontes e versão").

1. **Conseguir o texto.** Prefira o que eu colar na conversa ou um `.vtt`/`.srt` que eu indicar (leia com `Read`). Se eu der só o link e o `yt-dlp` existir no ambiente, baixe **só a legenda**, sem o vídeo: `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "pt.*,en.*" --sub-format vtt -o "%(title)s" "<link>"` (rode numa pasta temporária). Sem legenda, ou sem `yt-dlp`, diga isso: transcrever áudio não faz parte do sistema.
2. **Limpar.** Tire marcas de tempo repetidas, tags e linhas duplicadas das legendas automáticas; agrupe por minuto com `**[mm:ss]**` no começo de cada bloco. Textos acima de ~3000 palavras: grave uma versão **condensada** por minuto, não o texto cru, e diga que está condensada.
3. **Gravar** (`put_content`) em `{RAIZ}/{sg}/fontes/AAAA-MM-DD-título.md` com o frontmatter `tipo: fonte`, `materia`, `data`, `url` (link **limpo**: sem `list`, `index`, `t`, `si` e rastreio) e `origem` (youtube, arquivo…), um aviso `> [!warning]` dizendo que é pista e não fonte, e o texto.
4. Se algo da transcrição for entrar na aula, **confirme na fonte oficial** antes.

### Cartões (`"cartões"`)

Só se eu uso o plugin **Spaced Repetition** e pedi. A fila do `conhecimento.md` continua sendo a **única** fonte da Revisão do dia.

1. Leia `{RAIZ}/{sg}/cartoes.md` (se existir) para não repetir cartões.
2. Não existe: `put_content` com frontmatter (`tipo: cartoes`, `materia`, `tags`), o título `# Cartões — Nome` e a linha `#flashcards/{sg}`.
3. `append_content` com os novos, **uma linha cada**, no formato `pergunta::resposta` (sem espaços em volta de `::`), pulando os que já existem.

### Abrir no Obsidian (`"abrir"`)

Nenhuma ferramenta do MCP abre uma nota na tela. Entregue o **link** para eu clicar: `obsidian://open?vault={nome-do-cofre}&file={caminho-sem-.md}`, com o caminho codificado (`/` vira `%2F`, espaço vira `%20`). O `nome-do-cofre` é o nome do cofre no Obsidian (pergunte uma vez se não souber). Exemplo: `obsidian://open?vault=Estudos&file=estudos%2Fingles%2F_painel-ingles`.

### Buscar no cofre

`obsidian_simple_search` ("onde eu já vi X?", com `context_length` para ver o trecho) e `obsidian_complex_search` para limitar a uma pasta (`{"glob": ["{RAIZ}/{sg}/*", {"var": "path"}]}`) ou casar por padrão. `obsidian_search_by_tag` com `dirpath` para tags. Use também antes de acrescentar um termo ao glossário ou um conceito à fila, para não duplicar.

### Conferir o cofre

Depois de criar a matéria ou de mudar a estrutura, liste `{RAIZ}/{sg}` e as subpastas (`list_files_in_dir`) e confira, contra os nomes de `references/sessao.md` → "Nomes canônicos":

- existem `registros-da-skill/trilha.md`, `progresso.md`, `conhecimento.md`, `conquistas.md` e `_painel-{sg}.md`;
- `progresso.md` tem as cinco seções com os nomes exatos (`## Posição atual`, `## Pendências abertas`, `## Histórico de provas`, `## Checkpoints`, `## Linha do tempo (sessões)`);
- `trilha.md` tem a linha `**Status:** rascunho` (ou `aprovado em …`);
- `conquistas.md` tem `Última sessão: AAAA-MM-DD`;
- a tabela de `conhecimento.md` tem as seis colunas (`python fila.py mostrar -` com a seção colada confirma);
- as notas de `sessoes/` se chamam `AAAA-MM-DD-[tópico].md`.

Liste o que faltar ou divergir e corrija com as receitas acima.

## Sem o MCP

Nunca trave por falta da ferramenta (Regra 33). Em ordem:

1. **Arquivos diretos.** Se o cofre está numa pasta que você alcança (Claude Code com a pasta aberta), use `Read`, `Write` e `Edit` nos mesmos caminhos e com as mesmas regras de segurança. Diga que está usando arquivos e não o MCP.
2. **Sem acesso a arquivos.** Não há onde gravar: entregue o **Cartão de retomada** (`references/sessao.md` → "Sem acesso a arquivos — Cartão de retomada") e o texto da nota da sessão para eu colar.
3. **O MCP existe mas uma chamada falhou** (Obsidian fechado, chave de API errada, plugin Local REST API desligado, certificado): diga o erro exato, peça para eu abrir o Obsidian ou conferir a configuração (README → "Obsidian MCP") e, enquanto isso, segure o conteúdo no Cartão de retomada para não perder a sessão.

## Outros servidores MCP do Obsidian

Esta skill foi escrita para o `mcp-obsidian`. Com outro servidor as receitas valem do mesmo jeito; troque só o nome da ferramenta (confira a lista real do seu servidor, e veja se ele tem busca-e-troca de texto, que simplificaria as edições):

| Ação | `mcp-obsidian` | `obsidian-mcp-server` | `obsidian-mcp` |
|---|---|---|---|
| Ler uma nota | `obsidian_get_file_contents` | `obsidian_read_note` | `read-note` |
| Criar / sobrescrever | `obsidian_put_content` | `obsidian_update_note` (sobrescrever) | `create-note` |
| Acrescentar | `obsidian_append_content` | `obsidian_update_note` (acrescentar) | `edit-note` |
| Editar um trecho | `obsidian_patch_content` (por cabeçalho) | `obsidian_search_replace` (texto exato) | `edit-note` |
| Listar pasta | `obsidian_list_files_in_dir` | `obsidian_list_notes` | busca |
| Buscar | `obsidian_simple_search` | `obsidian_global_search` | `search-vault` |
| Frontmatter / tags | `obsidian_get_frontmatter` / `obsidian_search_by_tag` | `obsidian_manage_frontmatter` / `obsidian_manage_tags` | `add-tags` / `remove-tags` |
| Apagar | `obsidian_delete_file` (não usar) | `obsidian_delete_note` (não usar) | `delete-note` (não usar) |

As colunas dos dois outros servidores vêm da documentação deles, de memória, e **não foram conferidas** como a do `mcp-obsidian`.
