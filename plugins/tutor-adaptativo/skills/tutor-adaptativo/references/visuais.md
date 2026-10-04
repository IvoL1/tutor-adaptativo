# Referência — Visuais: diagramas, gráficos e imagens

> Leia antes de desenhar qualquer diagrama, mapa, gráfico ou figura numa aula — e antes de decidir que **não** vale desenhar. O catálogo de tipos, os modelos prontos e os gráficos estão em `references/visuais-modelos.md`; como gravar no cofre, em `references/obsidian.md` → "Visuais e imagens".

> **Nesta referência:**
> **1. Quando visualizar (e quando não)**
> **2. Como escolher: Mermaid ou SVG**
> **3. Como passar o pedido: uma ideia, poucos elementos**
> **4. Como fazer**
> **5. Verificar antes de mostrar**
> **6. Onde mostrar**
>
> *(catálogo, modelos de SVG, gráficos, Canvas, imagens e interativos: `references/visuais-modelos.md`)*

## Quando visualizar (e quando não)

Uma imagem só merece lugar quando mostra algo que palavras não mostram: forma, estrutura, direção, relação, geometria. Este sistema constrói um **mapa de dependências** na minha cabeça — verdades de chão nas raízes, fatos derivados pendurados nelas —, e um visual é poderoso justamente quando torna essa estrutura (ou uma geometria) visível.

**Desenhe quando a ideia é:**
- uma **estrutura ou relação**: dependências, um sistema com partes e setas, um fluxo, uma sequência de trocas, uma máquina de estados, uma árvore, uma comparação, uma contenção (o que está dentro e o que está fora);
- **espacial ou geométrica**: geometria de coordenadas, reta numérica, vetores, o formato de uma função, um arranjo físico (teclado, braço de instrumento);
- **numérica**: uma função $y=f(x)$, uma série (minhas provas ao longo do tempo), uma proporção — gráfico com os valores **calculados por código**;
- **visual por natureza**: uma foto, um mapa, uma peça anatômica, uma obra — imagem de fonte confiável com crédito, não diagrama;
- **dinâmica**: só se entende mexendo (um parâmetro que muda o gráfico, um algoritmo passo a passo) — visual interativo, se o ambiente permitir.

**Não desenhe quando** uma frase ou uma equação já resolve. Um desenho que só repete o texto ao lado não ensina nada e ainda pode errar. **Na dúvida, fique sem: um desenho errado faz mais estrago que desenho nenhum** (Regra 31).

O **mapa de dependências do plano** é o visual mais importante do sistema (`references/ensino.md` → "Fase 2 — Plano"); os demais são ocasionais.

## Como escolher: Mermaid ou SVG

- **Mermaid** (padrão) — relacional e estrutural: grafos de dependência (`graph TD` ou `LR`), fluxogramas, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `mindmap`, `timeline`, `classDiagram`. É o que serve ao mapa de dependências.
- **Mermaid para números simples:** `xychart-beta` (linha e barra), `pie`, `quadrantChart`, `gantt` — nativos na nota (`references/visuais-modelos.md`).
- **SVG** — espacial e geométrico, que o layout automático do Mermaid não resolve: posições exatas, figuras geométricas, retas numéricas, vetores, gráficos de função, formas sob medida. Há modelos prontos (reta numérica, plano cartesiano, fração, teclado).
- **Tabela Markdown** — quando a ideia é comparar, não desenhar.

Regra de bolso: *nós e setas* → Mermaid; *posições e formas* → SVG; *comparação* → tabela.

## Como passar o pedido: uma ideia, poucos elementos

O erro mais comum é **entulhar**: cada rótulo extra torna a imagem mais difícil de ler **e** mais difícil de organizar corretamente. Antes de pedir ou desenhar, reduza ao mínimo de elementos que carregam a ideia e, para cada um, pergunte: *"se eu tirar isto, a ideia continua clara?"* Se sim, tire.

Dê ao desenhista a **ideia E os elementos concretos** — não um tema vago nem uma lista longa de exigências:

- **Ruim:** "faça um diagrama sobre funções".
- **Bom:** "graph LR: dois nós, 'parâmetros' e 'corpo', com setas até um nó 'função'; uma seta de 'função' até 'valor devolvido'. Sem título. Mostre que a função *recebe* e *devolve*, e não só executa."

Se o pedido lista mais de ~5 a 7 elementos, corte antes.

## Como fazer

1. **Se o subagente `tutor-diagramador` existir**, delegue a ele (`references/ferramentas.md` → "Subagentes") com o pedido acima, completo, e com o caminho da pasta `scripts/`. Ele devolve o código verificado e diz **como** verificou.
2. **Sem o subagente**, escreva você mesmo o bloco, partindo de um modelo de `references/visuais-modelos.md` (poucos nós, rótulos curtos, sem recursos exóticos). Com Python e um navegador (Chrome ou Edge), valide e renderize com `render.py` (`references/ferramentas.md` → "Scripts da skill (o código decide)"): ele acusa erro de sintaxe com a mensagem exata e gera o PNG para você olhar. Em qualquer caso, **releia cada seta** contra o que a aula afirma.
3. **Valores de gráfico vêm de conta feita por código** (`awk` no Bash), nunca de cabeça; coordenadas de SVG, com a conta anotada num comentário.
4. **Não invente conteúdo:** desenhe só o que o pedido especifica. Se o pedido é vago, desenhe a coisa menor e verdadeira em vez de preencher com palpites.

## Verificar antes de mostrar

Um diagrama que renderiza não é um diagrama **correto**: renderizar só prova que a sintaxe é válida. Verifique:
- Toda seta aponta para o lado certo? Toda relação é verdadeira?
- Os rótulos são corretos e sem ambiguidade?
- Algo está sobreposto, cortado, apertado ou ilegível? (A correção quase sempre é **menos elementos**, não mais.)
- Eu leria a ideia intencionada só olhando a imagem?

Se você consegue renderizar (o subagente tenta), **olhe** a imagem. Se não consegue, diga isso — **nunca** apresente como verificado visualmente algo que você só releu.

## Onde mostrar

- **No chat:** o bloco mermaid, com uma frase de introdução. Em algumas interfaces ele aparece como código — sem problema, o desenho está na nota da sessão. SVG: mostre o PNG renderizado, se houver, ou o código.
- **Na nota da sessão e no painel** (`references/templates.md`): o mesmo bloco mermaid, que o Obsidian e o GitHub renderizam nativamente. É o caminho padrão e o único que dispensa arquivo.
- **Arquivo em `anexos/`** (SVG sempre que o visual precisar existir fora de um bloco; PNG só com acesso ao disco): como gravar, nomear e embutir com `![[arquivo.svg]]` está em `references/obsidian.md` → "Visuais e imagens". O MCP do Obsidian grava texto, não binário.
- **Um print que eu copiei:** o Claude não enxerga a minha área de transferência; eu colo direto na nota no Obsidian. Se o Claude precisa **olhar** a imagem, eu a anexo na conversa.
- **Depois de gravar, não dá para ver como o Obsidian renderiza.** Em tipo `-beta` ou pouco comum, diga ao Ivo para conferir a nota e deixe a alternativa pronta (`references/visuais-modelos.md` → "Compatibilidade com o Obsidian").
- Apresente o visual numa frase e deixe-o carregar a ideia; **não narre cada elemento de volta em texto**.
