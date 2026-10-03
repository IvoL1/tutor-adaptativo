# Referência — Visuais: diagramas e mapas

> Leia antes de desenhar qualquer diagrama, mapa ou figura numa aula — e antes de decidir que **não** vale desenhar.

> **Nesta referência:**
> **1. Quando visualizar (e quando não)**
> **2. Como escolher: Mermaid ou SVG**
> **3. Como passar o pedido: uma ideia, poucos elementos**
> **4. Como fazer**
> **5. Verificar antes de mostrar**
> **6. Onde mostrar**

## Quando visualizar (e quando não)

Uma imagem só merece lugar quando mostra algo que palavras não mostram: forma, estrutura, direção, relação, geometria. Este sistema constrói um **mapa de dependências** na minha cabeça — verdades de chão nas raízes, fatos derivados pendurados nelas —, e um visual é poderoso justamente quando torna essa estrutura (ou uma geometria) visível.

**Desenhe quando a ideia é:**
- uma **estrutura ou relação**: dependências, um sistema com partes e setas, um fluxo, uma sequência de trocas, uma máquina de estados, uma árvore, uma comparação, uma contenção (o que está dentro e o que está fora);
- **espacial ou geométrica**: geometria de coordenadas, reta numérica, vetores, o formato de uma função, um arranjo físico.

**Não desenhe quando** uma frase ou uma equação já resolve. Um desenho que só repete o texto ao lado não ensina nada e ainda pode errar. **Na dúvida, fique sem: um desenho errado faz mais estrago que desenho nenhum** (Regra 31).

O **mapa de dependências do plano** é o visual mais importante do sistema (`references/ensino.md` → "Fase 2 — Plano"); os demais são ocasionais.

## Como escolher: Mermaid ou SVG

- **Mermaid** (padrão) — relacional e estrutural: grafos de dependência (`graph TD` ou `LR`), fluxogramas, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `mindmap`, `timeline`, `classDiagram`. É o que serve ao mapa de dependências.
- **SVG** — espacial e geométrico, que o layout automático do Mermaid não resolve: posições exatas, figuras geométricas, retas numéricas, vetores, gráficos de função, formas sob medida.

Regra de bolso: *nós e setas* → Mermaid; *posições e formas* → SVG.

## Como passar o pedido: uma ideia, poucos elementos

O erro mais comum é **entulhar**: cada rótulo extra torna a imagem mais difícil de ler **e** mais difícil de organizar corretamente. Antes de pedir ou desenhar, reduza ao mínimo de elementos que carregam a ideia e, para cada um, pergunte: *"se eu tirar isto, a ideia continua clara?"* Se sim, tire.

Dê ao desenhista a **ideia E os elementos concretos** — não um tema vago nem uma lista longa de exigências:

- **Ruim:** "faça um diagrama sobre funções".
- **Bom:** "graph LR: dois nós, 'parâmetros' e 'corpo', com setas até um nó 'função'; uma seta de 'função' até 'valor devolvido'. Sem título. Mostre que a função *recebe* e *devolve*, e não só executa."

Se o pedido lista mais de ~5 a 7 elementos, corte antes.

## Como fazer

1. **Se o subagente `tutor-diagramador` existir**, delegue a ele (`references/ferramentas.md` → "Subagentes") com o pedido acima, completo, e com o caminho da pasta `scripts/`. Ele devolve o código verificado e diz **como** verificou.
2. **Sem o subagente**, escreva você mesmo um bloco mermaid, com sintaxe simples (poucos nós, rótulos curtos, sem recursos exóticos). Com Python e um navegador (Chrome ou Edge), valide e renderize com `render.py` (`references/ferramentas.md` → "Scripts da skill (o código decide)"): ele acusa erro de sintaxe com a mensagem exata e gera o PNG para você olhar. Em qualquer caso, **releia cada seta** contra o que a aula afirma.
3. **Não invente conteúdo:** desenhe só o que o pedido especifica. Se o pedido é vago, desenhe a coisa menor e verdadeira em vez de preencher com palpites.

## Verificar antes de mostrar

Um diagrama que renderiza não é um diagrama **correto**: renderizar só prova que a sintaxe é válida. Verifique:
- Toda seta aponta para o lado certo? Toda relação é verdadeira?
- Os rótulos são corretos e sem ambiguidade?
- Algo está sobreposto, cortado, apertado ou ilegível? (A correção quase sempre é **menos elementos**, não mais.)
- Eu leria a ideia intencionada só olhando a imagem?

Se você consegue renderizar (o subagente tenta), **olhe** a imagem. Se não consegue, diga isso — **nunca** apresente como verificado visualmente algo que você só releu.

## Onde mostrar

- **No chat:** o bloco mermaid, com uma frase de introdução. Em algumas interfaces ele aparece como código — sem problema, o desenho está na nota da sessão.
- **Na nota da sessão e no painel** (`references/templates.md`): o mesmo bloco, que o Obsidian e o GitHub renderizam nativamente.
- **Imagem guardada na matéria (opcional):** se há PNG (do `render.py` ou do subagente), passe-o por `cofre.py anexar "matéria" arquivo.png --nome "descrição"`; ele fica em `anexos/` e a nota o embute com o `EMBED` devolvido (`![[arquivo.png]]`; para limitar a largura, `![[arquivo.png|500]]`). O mesmo vale para um print que eu copiar: `cofre.py anexar "matéria" --area-de-transferencia`.
- Apresente o visual numa frase e deixe-o carregar a ideia; **não narre cada elemento de volta em texto**.
