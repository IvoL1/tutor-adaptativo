# Changelog — Tutor Adaptativo

> Só o que muda o comportamento do sistema. Serve para eu saber em que versão
> um material antigo foi gerado, e para não reintroduzir coisa já removida.

## 4.0 — 2026-10-04

**O cofre Obsidian passa a ser lido e escrito pelo MCP do Obsidian, não por Python** (mudança de comportamento)
- Novo `references/obsidian.md`: ferramentas do `obsidian-mcp-server`, regras de segurança (ler antes de
  escrever, nunca sobrescrever, nunca tocar em `pratica/`, nunca apagar), como achar a raiz do cofre e uma
  receita para cada coisa que o `cofre.py` fazia: retomar, criar matéria, atualizar registros, nota da
  sessão, visuais e imagens, transcrever, cartões, abrir, buscar e conferir o cofre. Tabela de equivalência
  para outros dois servidores MCP do Obsidian. Plano B: arquivos diretos, depois o Cartão de retomada.
- **Removidos:** `scripts/cofre.py` e `hooks/hooks.json` (os dois hooks, abertura e diário, rodavam o
  `cofre.py`; um hook não chama MCP). `"retomar"` agora lê os registros pelo MCP. O diário automático
  da conversa acabou: a nota da sessão guarda o que vale reler.
- `quiz.py` não depende mais do `cofre.py`; o estado das perguntas e provas fica na pasta temporária
  (ou em `TUTOR_STATE`), nunca dentro do cofre (a pasta `.tutor/` deixou de existir).
- `fila.py` aceita `-` no lugar do arquivo: lê o texto pelo stdin e, em `registrar`, **não grava**: imprime
  `TROCAR`/`POR`/`FIM` para o Claude aplicar com `obsidian_search_replace`. O modo com caminho continua.
- Novos templates em `references/templates.md`: Painel inicial, `_sessoes-[matéria].base` e `_leia-me.md`
  de `pratica/` (o MCP não cria pasta vazia, então `pratica/projeto/` e `pratica/treinos/` nascem com ele).
  `sessoes/`, `anexos/` e `fontes/` nascem com o primeiro arquivo.
- Comandos `"abrir"`, `"anexa"`, `"transcreve"` e `"cartões"` reescritos sobre o MCP: `"abrir"` entrega o
  link `obsidian://`; `"anexa"` grava Mermaid no corpo ou SVG em `anexos/` (PNG só com acesso ao disco);
  `"transcreve"` lê texto colado ou `.vtt` (e usa o `yt-dlp` se existir).

**Visuais: o que faltava para a skill gerar imagens, gráficos e diagramas**
- Novo `references/visuais-modelos.md`: tabela "qual visual para qual ideia"; modelos Mermaid conferidos no
  analisador do Mermaid 11.17.2 (fluxo, sequência, estado, ER, classes, mapa mental, linha do tempo, git,
  quadrante, pizza, gantt, gráfico de linha e barra); SVG pronto (reta numérica, plano cartesiano, fração,
  teclado de piano); gráficos de função e de dados com valores calculados por código; química com `\ce{}`;
  Canvas opcional do Obsidian; imagem de fonte confiável com crédito; regra para ilustração gerada por IA
  (só mnemônica, nunca fato); visual interativo; e a compatibilidade com o Mermaid do Obsidian, que pode ser
  mais antigo que o do `render.py`.
- `references/visuais.md` agora cobre visuais numéricos, imagem de fonte confiável e interativos, e diz
  como gravar cada tipo no cofre. O `tutor-diagramador` conhece os novos tipos, os modelos de SVG e
  devolve só o código (quem chama grava).
- Eval `cria-materia-por-script` virou `cria-materia-sem-python`.

**Não feito, de propósito**
- `quiz.py`, `fila.py` e `render.py` continuam em Python: são cálculo e renderização, não Obsidian.
- Configurar o servidor MCP dentro do plugin: a chave da API do Obsidian é do Ivo; a configuração está no README.

## 3.3 — 2026-10-01

**Correções (achadas numa segunda varredura, reproduzidas em teste)**
- Quiz e prova se perdiam se a pasta de trabalho mudasse entre `montar` e `corrigir` (o estado ia
  para pastas diferentes). Agora a busca também olha a pasta temporária.
- Entrada pelo PowerShell: BOM e UTF-16 quebravam o `P:`. Novo `--arquivo` em `quiz.py montar`,
  `cofre.py nota` e `cofre.py cartoes`, e a leitura trata BOM, UTF-16 e CRLF.
- `nova-materia` recusa nomes reservados do Windows (`con`, `nul`, `com1`...), limpa `|`, `[`, `]` e
  afins do nome mostrado e limita o nome da pasta a 60 caracteres.
- `nota` apagava linhas escritas à mão em "Sessões recentes" do painel; agora só as 8 notas mais
  recentes ficam listadas e o resto nunca é tocado. O corpo da nota é gravado só com LF.

**Novo**
- `cofre.py transcrever`: legenda de vídeo (link, via `yt-dlp`) ou `.vtt`/`.srt` local para `fontes/`,
  com marcas de tempo e aviso de que é pista e não fonte (Regra 8).
- `_sessoes-[matéria].base`: tabela nativa (Bases do Obsidian) das sessões, ligada ao painel.
- `cofre.py cartoes` e comando `"cartões"`: cartões `pergunta::resposta` para o plugin Spaced
  Repetition, opcional; a fila do `fila.py` segue como única fonte da Revisão do dia.
- Comando `"transcreve"`. Pasta `fontes/` por matéria. Eval novo (criar a matéria por script).

**Não feito, de propósito**
- Baixar o plugin Spaced Repetition: plugin da comunidade é código com acesso ao cofre; a instalação
  fica pela loja do Obsidian, nas mãos do Ivo. O mesmo vale para ligar a CLI do Obsidian.
- Transcrever áudio (Whisper/ffmpeg): sem legenda, o `transcrever` avisa em vez de adivinhar.

## 3.2 — 2026-10-01

**Correções (achadas numa varredura de erros, testadas)**
- `quiz.py`: o separador ` | ` do equívoco cortava alternativas com pipe no texto (`ls | grep`).
  Agora o equívoco vai numa linha própria que começa com `~`. **Mudança de formato.**
- `quiz.py`: a prova acumulava entre a tentativa e a reprova. Agora a prova parada por mais de
  12 h recomeça sozinha, `placar` avisa quando a prova ficou aberta e a reprova usa outro nome.
- `quiz.py`: com `--sem-nao-sei`, o número seguinte era lido como "não sei"; `--max` inválido
  quebrava com traceback; IDs com caminho eram aceitos.
- O estado dos scripts saiu da pasta temporária: vive em `.tutor/estado/` dentro do cofre.
- `acerto_fragil` deixou de ser órfão: `fila.py --resultado acerto-fragil` repete o intervalo.
- O histórico de dificuldades passou a morar no `CLAUDE.md` do cofre (o arquivo da skill é
  sobrescrito a cada atualização); o destino "Melhorado", que não existia, foi removido.
- Hooks: procuram `python` e depois `python3` (macOS e Linux) e cobrem `fork`; o diário só lê o que o
  transcript ganhou e só conta uma chamada real da skill (não uma conversa que a cita).
- `render.py`: Mermaid com versão exata (11.17.2) e verificação de integridade (SRI).
- Wikilinks entre matérias com caminho completo (`[[matéria/registros-da-skill/conquistas|...]]`),
  porque `conquistas` e `progresso` se repetem em toda matéria.

**Decisões de design (aplicadas a pedido)**
- Prova rápida passou de 3–5 para **5 questões**: com corte de 80%, 3 ou 4 questões exigiam 100%.
- Acerto com 🔴 (frágil) não avança o intervalo da fila.
- Distratores de quiz são equívocos conceituais, nunca prática depreciada (preserva a Regra 25).
- Fio novo para quem é iniciante: exemplo resolvido → com lacunas → problema (heurística da literatura
  de carga cognitiva; a confirmar na fonte).
- Estilo de resposta opcional `Tutor` (`output-styles/`), sem forçar.
- `LICENSE` MIT e campos de manifesto (`license`, `keywords`, `displayName`).

**Obsidian**
- `cofre.py nova-materia`, `nota`, `anexar` (arquivo ou área de transferência), `abrir` e `status`.
- Pasta `anexos/` por matéria e embed `![[...]]`; os templates são lidos de `references/`, sem cópia.

**Não feito**
- Trocar a escada fixa por FSRS: o ganho com poucas revisões é modesto e o `py-fsrs` exige Python 3.10+.
- Editar o `app.json` do Obsidian: o valor exato da configuração de anexos não foi confirmado em fonte oficial.

## 3.1 — 2026-09-30

**Robustez: o código decide o que não deve depender de obediência.**
O `learn` faz sorteio, correção, registro e renderização por código (extensões em
TypeScript para o agente pi). Aqui o equivalente são scripts Python, hooks do
Claude Code e testes automáticos — e alguns itens vão além do `learn`.

**Adicionado**
- `scripts/quiz.py`: sorteia a posição da certa sem repetir em sequência
  (sugestão 1); **verifica as alternativas** (tamanho, "porque", negrito
  assimétrico, "todas as anteriores", ressalva só na certa); corrige, inclusive
  seleção múltipla por conjunto exato; revela o equívoco da errada escolhida;
  calcula o percentual e a decisão da prova (80% e 50%) e gera o bloco do
  `progresso.md`. Plano B sem Python: posição `1 + (n mod N)`.
- **"O que você estava pensando?"** depois de um erro, uma vez e em uma linha,
  com os cuidados antifrustração (sugestão 2).
- `scripts/fila.py`: intervalos e datas da repetição espaçada por código.
- `scripts/cofre.py`: acha o cofre, resume posição, pendências e revisão do dia,
  valida a estrutura e (opt-in) registra o diário.
- `scripts/render.py`: valida Mermaid/SVG e gera PNG com o Chrome ou o Edge já
  instalados, devolvendo a **mensagem exata de erro de sintaxe**. Funciona nos
  dois navegadores (o Edge entrega o trabalho a outro processo; esperamos pelo
  arquivo, não pelo processo).
- `scripts/selftest.py`: 45 verificações, incluindo as fronteiras de 80% e 50%.
  Validado por mutação: estragar a lógica de propósito em cinco pontos faz o
  autoteste falhar em todos.
- **Hooks** no plugin: abertura da sessão (posição e revisão do dia, sem saída
  fora de um cofre) e diário da conversa, desligado por padrão.
- **Testes automáticos** (`evals/`, 8 casos) para o `claude plugin eval`
  (sugestão 3).
- O subagente `tutor-diagramador` passou a usar o `render.py`.

**Não feito, de propósito**
- Uma interface própria de quiz (o `learn` tem uma no pi). No Claude Code o quiz
  continua usando a pergunta com opções nativa; o que foi para código é tudo o
  que não é interface.
- Rodar a suíte de evals: exige login ativo e usa a cota do Ivo.

## 3.0 — 2026-09-30

**Virada: de "programação, offline" para "qualquer matéria, ao vivo".**
Fusão com as ideias do sistema `learn` de Amos Blomqvist
(<https://github.com/amosblomqvist/learn>), reescritas com palavras e exemplos
próprios — o repositório original não tem licença, então nada foi copiado.

**Mudou de nome e de escopo**
- `academia-adaptativa-programacao-ivo` → `tutor-adaptativo`. A matéria
  deixou de ser só programação: idiomas, matemática, música, concursos, cursos.
- O que só vale para código foi isolado em `references/programacao.md`
  (clean code, git, scaffold, documentação da versão, fechamento Ship it).

**Removido de propósito**
- Todo o modo offline: módulos em pastas, aulas e provas para fazer sozinho,
  avaliação em lote, `"lote offline"`, `[PULEI]`, pastas `1-estudar-agora/` e
  `3-concluidos/`, `_capa-`, `aula-`, `exercicio-`, `prova-t[N]-[parte]`.
- Comandos `"avaliar"`, `"lote offline"`, `"nivelamento"` e `"docs"`
  (viraram `"retomar"`, `"sondar"`, `"fonte"` e o fluxo ao vivo).
- Entrevista: a pergunta "vou estudar offline?" saiu; 16 → 15 perguntas.
- `references/modo-assincrono.md`, substituído por `avaliacao.md`.

**Adotado do `learn`, adaptado**
- **Sondagem ao vivo** no lugar do teste de nivelamento: achar piso e teto em
  cada fio do assunto; tudo certo = pergunta fácil demais; um erro não basta
  para concluir; concepção errada confiante é desfeita, não complementada.
  Adaptação minha: a sondagem nunca vale nota e para de escalar quando há
  sinal de cansaço (por causa do Protocolo Antifrustração).
- **Plano com mapa de dependências** em mermaid, raízes testadas e o "ok" do
  Ivo antes de qualquer aula.
- **Ciclo por nó:** motivar → estabelecer → conectar → checar, com o "problema
  antes da solução". Conciliado com "prática > teoria": o chão é mostrado em
  ação. Tensão com a Regra 25 (nada desatualizado) resolvida: o "sem isso" é
  a tarefa à mão, nunca um método antigo.
- **Dois princípios de ensino:** começar pelo que é sempre verdade, e "como eu
  poderia ter descoberto isso?".
- **Escrita de alternativas por construção**, com exemplo próprio e base em
  Haladyna, Downing e Rodriguez (2002).
- **"Não sei"** como resposta legítima e distinta de erro (lacuna, reensino
  sem peso).
- **Precisão inegociável** e subagentes `tutor-pesquisador` e
  `tutor-diagramador`, com plano B quando não existirem.
- **Perguntas com opções** e **quiz corrigido na hora**, com plano B em texto.
- **Nota da sessão** (o papel do `md-log`) e mermaid/LaTeX nas convenções.
- Distinção entre **pergunta com resposta certa** (quiz) e **sem resposta
  certa** (escolha).

**Adicionado do meu lado (não vem do `learn`)**
- **Cartão de retomada** para ambientes sem acesso a arquivos (chat do
  claude.ai), já que não há memória entre conversas.
- **Tamanho do ritual** (Regra 34): pedido pequeno recebe a versão mínima,
  sem entrevista nem plano.
- Erro confiante volta à fila de revisão a 1 dia depois do reforço
  (Metcalfe e Miele, 2014).
- Empacotamento como **plugin do Claude Code** (skill + 2 subagentes) e
  `marketplace.json`, para instalar direto do GitHub.

**Correções feitas na auditoria final da 3.0**
- A regra "prova é obrigatória" tinha caído na reescrita; voltou na Regra 17.
- O orçamento de tempo por sessão (estimativas por exercício e por prova) tinha
  caído; voltou em `sessao.md`.
- Faltavam três casos: `"retomar"` sem registros nem cartão; sessão interrompida
  antes do "ok" no plano (agora vira rascunho); vocabulário de nó, parte,
  tópico e trilha.
- Os marcadores `[travei]` e 🟢🟡🔴 ainda diziam "eu escrevo à mão" (resto do
  modo offline).
- Caminho de upload no app corrigido para **Customize → Skills**.
- Next.js: a página da documentação agora é da versão 16.3.8.
- Atribuição do procedimento de alternativas e redação do Haladyna ajustadas ao
  que foi verificado.
- **Nome final:** `tutor-adaptativo` (skill, plugin, marketplace e repositório);
  subagentes `tutor-pesquisador` e `tutor-diagramador`. "Academia" soava como
  academia de ginástica, e o sufixo "-ivo" prendia a skill a uma pessoa.
- **Ortografia**, conferida com o corretor pt-BR do Windows: `antifrustração`,
  `reensinar`, `miniprojeto`, `miniaula`, `hifens`, `ex.:`, "ponto perdido" no
  lugar de "não-acerto" e "seleção múltipla" no lugar de "multisseleção".
- Validado com `claude plugin validate --strict` (plugin e marketplace).

**Decidido**
- Só `pratica/projeto/` entra em git; `pratica/treinos/` não.
- Pergunta de aquecimento só na volta de uma pausa; a Revisão do dia, em
  toda sessão.
- Confiança 🟢🟡🔴 obrigatória em prova e sondagem; opcional na checagem de nó.
- Com a ferramenta de perguntas, quiz tem até 3 alternativas + "Não sei"
  (a ferramenta limita a 4 opções).

## 2.1 — 2026-09-23

Auditoria completa. Corrigidos: `vite create` (não existe), MDN classificada
como especificação, módulo de reforço como arquivo solto, referências
quebradas, `## Minha resposta` vs `## ✍️ Minha resposta`, Regra 4 sobre mini
projeto, comando `"prova"`, acentuação da `description`. Adicionados:
"Nomes canônicos", pasta e template de prova de tópico, Pendências abertas,
data da última sessão, índice de seções, coluna `Status` na fila de revisão.
Última versão offline.

## 2.0

Reescrita para "Academia Adaptativa". Substituiu a skill antiga de estudos.
"Pacote" passou a se chamar "módulo"; `ASSUNTO.md` virou `trilha.md`;
`anotacoes.md` e `revisao.md` viraram `conhecimento.md`; cada módulo passou a
ser uma pasta.
