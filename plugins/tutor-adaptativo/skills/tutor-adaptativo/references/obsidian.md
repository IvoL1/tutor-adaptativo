# Referência — Obsidian pelo MCP (cofre de estudos)

> Leia antes de **qualquer** leitura ou escrita no cofre: retomar uma matéria, criar matéria, gravar registros e nota da sessão, guardar visual, transcrever vídeo, gerar cartões, abrir uma nota.

> **Princípio:** o cofre é lido e escrito pelas ferramentas do **MCP do Obsidian**, não por script. Python ficou só para o que é cálculo (`quiz.py`, `fila.py`) e para validar desenho (`render.py`). Plano B quando não houver o MCP: neste arquivo → "Sem o MCP".

> **Nesta referência:**
> **1. Ferramentas (servidor `obsidian-mcp-server`)**
> **2. Regras de segurança do cofre**
> **3. Achar a raiz do cofre**
> **4. Receitas**
>     · Retomar (ler a posição e a Revisão do dia)
>     · Criar a matéria
>     · Atualizar os registros
>     · Gravar a nota da sessão
>     · Visuais e imagens (`"anexa"`)
>     · Transcrever um vídeo (`"transcreve"`)
>     · Cartões (`"cartões"`)
>     · Abrir no Obsidian (`"abrir"`)
>     · Buscar no cofre
>     · Conferir o cofre (substitui o antigo `validar`)
> **5. Sem o MCP**
> **6. Outros servidores MCP do Obsidian**

## Ferramentas (servidor `obsidian-mcp-server`)

O Claude Code mostra cada ferramenta com o prefixo do nome que o servidor tem na sua configuração (por exemplo `mcp__obsidian__obsidian_read_note`). Aqui uso só o nome curto. **Confira o schema real de cada ferramenta antes da primeira chamada**: os nomes dos parâmetros podem mudar de versão para versão, e o que vale é o que a ferramenta declara. Os caminhos são sempre **relativos à raiz do cofre Obsidian**, com `/` e sem `/` no começo.

| Ferramenta | Para que serve aqui |
|---|---|
| `obsidian_read_note` | ler uma nota inteira (registros, painel, nota da sessão); pode devolver o frontmatter separado |
| `obsidian_update_note` | **criar** uma nota nova, **acrescentar** ao fim ou ao começo, ou **sobrescrever** (só em nota que você mesmo acabou de criar; ver "Regras de segurança") |
| `obsidian_search_replace` | trocar um trecho exato dentro de uma nota existente: é a ferramenta de **edição cirúrgica** (uma linha da tabela da fila, uma linha do painel, o `▶ próximo passo`) |
| `obsidian_manage_frontmatter` | ler, criar e alterar uma propriedade do frontmatter (`topico`, `data`, `status`) sem reescrever o corpo |
| `obsidian_manage_tags` | listar, acrescentar e remover tags de uma nota |
| `obsidian_list_notes` | listar uma pasta (com filtro de extensão, regex de nome e profundidade): achar a raiz, ver as matérias, conferir se um arquivo já existe |
| `obsidian_global_search` | buscar texto ou regex no cofre inteiro (ou numa pasta, pelo filtro de caminho) |
| `obsidian_delete_note` | **não use** nesta skill (ver regras) |

**Data de hoje:** vem do contexto da conversa; se não vier, `date +%F` no Bash (não calcule de cabeça).

## Regras de segurança do cofre

1. **Ler antes de escrever.** Antes de alterar qualquer registro, leia a versão atual (`obsidian_read_note`). Nada de reescrever de memória.
2. **Nunca sobrescrever o que já existe.** Para criar, primeiro confirme que o arquivo **não existe** (`obsidian_list_notes` na pasta com `nameRegexFilter`, ou uma leitura que falhe). Só depois grave. Um arquivo que existe é alterado **por troca cirúrgica** (`obsidian_search_replace`) ou por **acréscimo** (`obsidian_update_note` em modo de acrescentar), nunca por sobrescrita.
3. **`pratica/` é meu.** Nunca escreva, edite nem apague nada em `pratica/` além do `_leia-me.md` criado junto com a matéria. O que eu produzo ali eu mesmo gravo.
4. **Nunca apague.** Esta skill não usa `obsidian_delete_note`. Se algo precisa sumir, diga o que e por quê, e eu apago.
5. **Só dentro da raiz do cofre de estudos** (próxima seção). Nada fora dela.
6. **Confirme depois de gravar.** Após criar ou editar, releia o trecho (ou liste a pasta) e confira que ficou como esperado. Se a ferramenta devolveu erro, **diga o erro** e não finja que gravou: o plano B (seção 5) existe para isso.
7. **Troca exata.** No `obsidian_search_replace`, o texto a procurar tem de ser copiado **literalmente** da nota que você acabou de ler (espaços, hífens e acentos incluídos). Se a troca não achar o trecho, releia a nota e tente de novo; nunca troque "mais ou menos".
8. **Texto em UTF-8, só com LF.** Acentos normais; sem caracteres de controle.

## Achar a raiz do cofre

A **raiz de estudos** (`RAIZ`) é a pasta do cofre Obsidian que contém o `CLAUDE.md` ponteiro, o `README.md` e as pastas das matérias. Pode ser uma subpasta (`estudos/`) ou o próprio cofre (`RAIZ` vazia).

1. `obsidian_list_notes` em `/` (profundidade 1 ou 2).
2. Candidata = pasta com `CLAUDE.md` que cite `tutor-adaptativo`, ou com subpastas que tenham `registros-da-skill/`. Se achar uma, use-a. Se achar mais de uma, pergunte qual (pergunta com opções).
3. **Nada encontrado:** é cofre novo. Proponha `estudos/` (ou a raiz do cofre, se for um cofre só de estudos), peça meu "ok" e crie na primeira matéria.
4. Guarde `RAIZ` para a sessão inteira e **mostre-a uma vez** ("Cofre: `estudos/`") para eu corrigir se estiver errada. Registre-a no `trilha.md` (campo "Raiz dos estudos no cofre").

Daqui em diante, `{RAIZ}/{matéria}/...` quer dizer o caminho completo a partir da raiz do cofre.

## Receitas

### Retomar (ler a posição e a Revisão do dia)

1. `obsidian_list_notes` em `{RAIZ}` para ver as matérias (pastas com `registros-da-skill/`). Mais de uma: siga `references/sessao.md` → "Se há mais de uma matéria ativa".
2. Da matéria ativa, leia **`registros-da-skill/progresso.md`** (seções "Posição atual" e "Pendências abertas"), **`conquistas.md`** (a linha "Última sessão: AAAA-MM-DD", para decidir a Reentrada) e **`conhecimento.md`** (a fila). Leia o `trilha.md` só se precisar do contexto (orçamento de tempo, fonte e versão congelada).
3. **Revisão do dia:** com Python, cole a seção `## Fila de revisão espaçada` do `conhecimento.md` no stdin: `python "<pasta>/fila.py" vencidos - --max 3` (datas por código). Sem Python, aplique a tabela de `references/pedagogia.md` → "Fila de revisão espaçada".
4. Siga `references/sessao.md` → "Retomar e continuar".

Se **nenhum** registro existir, é matéria nova (Entrevista), nunca "retomada de memória".

### Criar a matéria

Roda **uma vez**, depois do meu "ok" no plano. Repetir não altera nada, porque cada arquivo só é criado se ainda não existir (regra 2).

**Nome da pasta (`sg`):** o nome da matéria sem acento, em minúsculas, com hifens, até 60 caracteres (`Matemática Básica` → `matematica-basica`). Sem `| [ ] # ^ \ / : * ? " < >` no nome mostrado. Recuse nomes que o Windows reserva (`con`, `prn`, `aux`, `nul`, `com1`…`com9`, `lpt1`…`lpt9`) e peça outro.

**Os arquivos**, na ordem (cada um com `obsidian_update_note` criando a nota; o conteúdo vem dos templates de `references/templates.md`, com `[Nome da Matéria]` e `[Matéria]` trocados pelo nome mostrado e `[matéria]` pelo `sg`):

| # | Caminho | Conteúdo |
|---|---|---|
| 1 | `{RAIZ}/CLAUDE.md` | template "`CLAUDE.md`" (só se não existir; é um por cofre, sem frontmatter) |
| 2 | `{RAIZ}/{sg}/registros-da-skill/trilha.md` | template `trilha.md`, com `**Status:** rascunho` e "Raiz dos estudos no cofre" preenchida |
| 3 | `…/registros-da-skill/progresso.md` | template `progresso.md`, com "Próximo passo: fazer a entrevista" |
| 4 | `…/registros-da-skill/conhecimento.md` | template `conhecimento.md` |
| 5 | `…/registros-da-skill/conquistas.md` | template de `references/projetos.md` → "Changelog de conquistas", com a data de hoje em "Última sessão" |
| 6 | `{RAIZ}/{sg}/_painel-{sg}.md` | template "Painel inicial" de `references/templates.md` |
| 7 | `{RAIZ}/{sg}/_sessoes-{sg}.base` | template "`_sessoes-[matéria].base`" (tabela nativa de sessões; se a ferramenta recusar a extensão `.base`, pule este e o link no painel, sem drama) |
| 8 | `{RAIZ}/{sg}/pratica/projeto/_leia-me.md` e `{RAIZ}/{sg}/pratica/treinos/_leia-me.md` | template "`_leia-me.md` de `pratica/`" (é o que faz a pasta existir: o MCP não cria pasta vazia) |
| 9 | `{RAIZ}/README.md` | se não existir, o template "`README.md`" sem a linha-modelo; se existir, **acrescente** a linha `- [[_painel-{sg}\|Nome]] — ▶ fazer a entrevista` sob `## Matérias ativas` (troca cirúrgica) e tire a linha `- (nenhuma ainda…)` se houver. Nunca duplique: busque `_painel-{sg}` antes |

`sessoes/`, `anexos/` e `fontes/` **nascem sozinhas** quando a primeira nota, imagem ou transcrição for gravada nelas (o MCP cria as pastas do caminho). Não crie arquivos-fantasma para elas.

Ao terminar: **confira** (receita "Conferir o cofre"), mostre a árvore criada (Regra 30) e diga onde eu mexo (`pratica/`) e onde não (`registros-da-skill/`).

### Atualizar os registros

`progresso.md`, `conhecimento.md`, `conquistas.md`, `trilha.md` e o painel **só mudam por troca cirúrgica ou acréscimo**:

- **Troca:** leia a nota, copie o trecho antigo exato (uma linha, uma linha de tabela, um parágrafo curto) e ponha o novo (`obsidian_search_replace`). Exemplos: o `▶ próximo passo` do painel; a "Última sessão" do `conquistas.md`; o status de uma pendência.
- **Acréscimo:** uma linha nova na "Linha do tempo (sessões)", um bloco novo em "Histórico de provas" (o `quiz.py placar` já devolve o bloco pronto), um termo novo no glossário (`obsidian_update_note` em modo de acrescentar **só** quando o trecho vai mesmo no fim do arquivo; no meio de uma seção, use a troca: procure a última linha da seção e devolva-a seguida da nova).
- **Fila de revisão:** com Python, cole a seção da fila e rode `python "<pasta>/fila.py" registrar - --conceito "..." --resultado novo|acerto|acerto-fragil|erro|erro-confiante --parte "T1 / 1a"`. O script **não grava**: ele imprime `TROCAR:` / `POR:` / `FIM`. Aplique exatamente isso com `obsidian_search_replace` (o trecho de `TROCAR` já é a linha como está na nota). Sem Python, calcule à mão pela tabela de `references/pedagogia.md`.
- **Propriedades:** para `topico`, `data`, `status` e afins no frontmatter, use `obsidian_manage_frontmatter` em vez de reescrever o cabeçalho.
- **`trilha.md`:** quando o plano for aprovado, troque `**Status:** rascunho` por `**Status:** aprovado em AAAA-MM-DD` e complete as seções com trocas, não recriando o arquivo.

### Gravar a nota da sessão

Caminho: `{RAIZ}/{sg}/sessoes/AAAA-MM-DD-{título-em-slug}.md` (título sem acento, minúsculo, hifens; se eu não deu título, use o tópico).

1. **Já existe uma nota do dia com esse nome?** (`obsidian_list_notes` em `sessoes/` com `nameRegexFilter`).
   - **Não:** crie com o template "nota da sessão" de `references/templates.md` (frontmatter `tipo`, `materia`, `data`, `topico`, `tags`).
   - **Sim:** **acrescente** ao fim: uma linha `---`, `## Acrescentado às HH:MM` e o novo trecho. Nunca sobrescreva.
2. **Liste a nota no painel**, em `## Sessões recentes` do `_painel-{sg}.md`: leia o painel; ponha `- [[AAAA-MM-DD-título]] — a ideia que encaixou` logo abaixo da linha `> Tabela com todas…` (troca cirúrgica sobre essa linha, devolvendo-a seguida da nova). Se a linha `- (nenhuma sessão ainda)` existir, remova-a na mesma troca.
3. **Só as 8 notas mais recentes ficam listadas:** se passar de 8 linhas no formato `- [[AAAA-MM-DD-…]]`, tire a mais antiga. **Linhas que eu escrevi à mão no painel nunca saem.**
4. Se a nota tem visual (ver a próxima receita), ele já entra no corpo antes de gravar.
5. Atualize o `▶ próximo passo` e o mapa do painel (troca cirúrgica) e confira o resultado.

### Visuais e imagens (`"anexa"`)

O MCP grava **texto**, não arquivos binários. Por isso a ordem de preferência é:

1. **Bloco ```` ```mermaid ```` direto no corpo da nota.** É texto, renderiza nativo no Obsidian e é o caminho padrão para diagramas.
2. **Arquivo `.svg` em `anexos/`**, gravado com `obsidian_update_note` em `{RAIZ}/{sg}/anexos/AAAA-MM-DD-nome.svg` (SVG é texto). Entra na nota com `![[AAAA-MM-DD-nome.svg]]` (largura opcional: `![[…svg|500]]`). Nome sem acento, minúsculo, com hifens; nunca reaproveite um nome que já existe (acrescente `-2`).
3. **PNG ou outra imagem de verdade** (gerada pelo `render.py`, ou um print): o MCP não grava. Se a pasta do cofre está acessível no disco (o caminho aparece no `trilha.md` ou eu informo), copie com o Bash (`cp`) para `{pasta do cofre}/{RAIZ}/{sg}/anexos/` e embuta com `![[arquivo.png]]`. Se não está acessível, **diga** e escolha: (a) embutir o diagrama como Mermaid/SVG; (b) eu colo a imagem direto na nota pelo Obsidian (Ctrl+V), que a guarda sozinho na pasta de anexos que o Obsidian configurou.
4. **Print que eu copiei da tela:** o Claude não enxerga a minha área de transferência. Diga para colar direto na nota no Obsidian; se eu quiser que o Claude olhe a imagem, peço que eu a anexe na conversa.

Verificação e escolha do tipo de visual: `references/visuais.md` e `references/visuais-modelos.md`.

### Transcrever um vídeo (`"transcreve"`)

A transcrição é **pista, não fonte para ensinar** (Regra 8; `references/pedagogia.md` → "Fontes e versão").

1. **Conseguir o texto.** Prefira o que eu colar na conversa ou um `.vtt`/`.srt` que eu indicar (leia com `Read`). Se eu der só o link e o `yt-dlp` existir no ambiente, baixe **só a legenda**, sem o vídeo: `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "pt.*,en.*" --sub-format vtt -o "%(title)s" "<link>"` (rode numa pasta temporária). Sem legenda, ou sem `yt-dlp`, diga isso: transcrever áudio não faz parte do sistema.
2. **Limpar.** Tire marcas de tempo repetidas, tags e linhas duplicadas das legendas automáticas; agrupe por minuto com `**[mm:ss]**` no começo de cada bloco. Textos acima de ~3000 palavras: grave uma versão **condensada** por minuto, não o texto cru, e diga que está condensada.
3. **Gravar** em `{RAIZ}/{sg}/fontes/AAAA-MM-DD-título.md` com o frontmatter `tipo: fonte`, `materia`, `data`, `url` (link **limpo**: sem `list`, `index`, `t`, `si` e rastreio) e `origem` (youtube, arquivo…), um aviso `> [!warning]` dizendo que é pista e não fonte, e o texto.
4. Se algo da transcrição for entrar na aula, **confirme na fonte oficial** antes.

### Cartões (`"cartões"`)

Só se eu uso o plugin **Spaced Repetition** e pedi. A fila do `conhecimento.md` continua sendo a **única** fonte da Revisão do dia.

1. Leia `{RAIZ}/{sg}/cartoes.md` (se existir) para não repetir cartões.
2. Não existe: crie com frontmatter (`tipo: cartoes`, `materia`, `tags`), o título `# Cartões — Nome` e a linha `#flashcards/{sg}`.
3. Acrescente os novos, **uma linha cada**, no formato `pergunta::resposta` (sem espaços em volta de `::`), pulando os que já existem.

### Abrir no Obsidian (`"abrir"`)

Nenhuma ferramenta do MCP abre uma nota na tela. Entregue o **link** para eu clicar: `obsidian://open?vault={nome-do-cofre}&file={caminho-sem-.md}`, com o caminho codificado (`/` vira `%2F`, espaço vira `%20`). O `nome-do-cofre` é o nome do cofre no Obsidian (pergunte uma vez se não souber). Exemplo: `obsidian://open?vault=Estudos&file=estudos%2Fingles%2F_painel-ingles`.

### Buscar no cofre

`obsidian_global_search` (texto ou regex; o filtro de caminho limita a `{RAIZ}/{sg}`): "onde eu já vi X?", achar a nota de uma sessão, achar conceitos parecidos antes de acrescentar ao glossário ou à fila. Use também para evitar duplicar um termo.

### Conferir o cofre (substitui o antigo `validar`)

Depois de criar a matéria ou de mudar a estrutura, liste `{RAIZ}/{sg}` (`obsidian_list_notes`, profundidade 3) e confira, contra os nomes de `references/sessao.md` → "Nomes canônicos":

- existem `registros-da-skill/trilha.md`, `progresso.md`, `conhecimento.md`, `conquistas.md` e `_painel-{sg}.md`;
- `progresso.md` tem as cinco seções com os nomes exatos (`## Posição atual`, `## Pendências abertas`, `## Histórico de provas`, `## Checkpoints`, `## Linha do tempo (sessões)`);
- `trilha.md` tem a linha `**Status:** rascunho` (ou `aprovado em …`);
- `conquistas.md` tem `Última sessão: AAAA-MM-DD`;
- a tabela de `conhecimento.md` tem as seis colunas (`fila.py mostrar -` com a seção colada confirma);
- as notas de `sessoes/` se chamam `AAAA-MM-DD-[tópico].md`.

Liste o que faltar ou divergir e corrija com as receitas acima.

## Sem o MCP

Nunca trave por falta da ferramenta (Regra 33). Em ordem:

1. **Arquivos diretos.** Se o cofre está numa pasta que você alcança (Claude Code com a pasta aberta), use `Read`, `Write` e `Edit` nos mesmos caminhos e com as mesmas regras de segurança. Diga que está usando arquivos e não o MCP.
2. **Sem acesso a arquivos.** Não há onde gravar: entregue o **Cartão de retomada** (`references/sessao.md` → "Sem acesso a arquivos — Cartão de retomada") e o texto da nota da sessão para eu colar.
3. **O MCP existe mas uma chamada falhou** (Obsidian fechado, chave de API errada, plugin Local REST API desligado): diga o erro exato, peça para eu abrir o Obsidian ou conferir a configuração (README → "Obsidian MCP") e, enquanto isso, segure o conteúdo no Cartão de retomada para não perder a sessão.

## Outros servidores MCP do Obsidian

Esta skill foi escrita para o `obsidian-mcp-server`. Se a sua configuração usar outro, as receitas valem do mesmo jeito; troque só o nome da ferramenta (confira a lista real de ferramentas do seu servidor):

| Ação | `obsidian-mcp-server` | `mcp-obsidian` | `obsidian-mcp` |
|---|---|---|---|
| Ler uma nota | `obsidian_read_note` | `obsidian_get_file_contents` | `read-note` |
| Criar nota | `obsidian_update_note` | `obsidian_append_content` (cria se não existir) | `create-note` |
| Acrescentar | `obsidian_update_note` (acrescentar) | `obsidian_append_content` | `edit-note` |
| Troca cirúrgica | `obsidian_search_replace` | `obsidian_patch_content` | `edit-note` |
| Listar pasta | `obsidian_list_notes` | `obsidian_list_files_in_dir` | `list-available-vaults` / busca |
| Buscar | `obsidian_global_search` | `obsidian_simple_search` | `search-vault` |
| Frontmatter / tags | `obsidian_manage_frontmatter` / `obsidian_manage_tags` | (pela troca) | `add-tags` / `remove-tags` |
| Apagar | `obsidian_delete_note` (não usar) | `obsidian_delete_file` (não usar) | `delete-note` (não usar) |
