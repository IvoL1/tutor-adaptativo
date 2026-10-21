# Changelog — Tutor Adaptativo

> Só o que muda o comportamento do sistema. Serve para eu saber em que versão
> um material antigo foi gerado, e para não reintroduzir coisa já removida.

## 7.0.0 — 2026-10-21

**Estudar sozinho: pacote de estudo autônomo.** Novo modo, ao lado da aula ao vivo (que continua igual): eu digo a matéria e quantas horas por dia tenho, e a skill monta **uma vez** (com a fonte oficial e atual da internet e os anexos que eu der) um pacote fechado em Markdown e PDF que eu estudo **sem o Claude e sem internet**.
- **`references/pacote.md` (novo):** o passo a passo (entender o pedido com perguntas de opções, fontes, currículo, cronograma, escrita, conferência, PDF, entrega), a tabela de tempos por tipo de bloco, como escrever para quem estuda sozinho (dúvidas antecipadas, "se travar", fazer junto com resultado esperado, escada de 3 dicas, gabarito à parte, prova com correção e "qual seção reler"), os modelos dos arquivos e o que fazer se eu atrasar, pular tópico ou mudar as horas.
- **`scripts/pacote.py` (novo):** `planejar` valida o currículo (ids, pré-requisitos existentes e sem ciclo, dificuldade 1–5, blocos de 5 a 90 min), põe os tópicos na ordem dos pré-requisitos, distribui os blocos em dias que somam **pelo menos** as horas por dia (passa até 10% para não cortar um bloco ao meio), reserva a revisão espaçada (1, 3, 7 e 16 dias depois de cada tópico, até 15% do dia), avisa salto de dificuldade e mostra **até onde a matéria chega** em cada quantidade de dias; `--ja-sei` tira o que já domino. `conferir` mede o material escrito contra o tempo prometido (soma dos minutos, leitura longa demais, falta de gabarito e de "Critério de pronto", imagem inexistente, fórmula LaTeX ou diagrama que não aparecem sem internet).
- **`scripts/apostila.py` (novo):** gera `pdf/plano.pdf`, `pdf/dia-NN.pdf` e `pdf/gabarito-dia-NN.pdf`, sem internet, com o Chrome ou o Edge já instalados; sem eles, `.html` prontos para imprimir (Ctrl+P → Salvar como PDF). Dicas dobráveis saem abertas no papel; gabarito sai separado.
- **`ver.py`:** só carrega fórmulas e diagramas da internet quando a nota realmente os usa; uma nota comum, e todo pacote, abre sem rede.
- **`SKILL.md`:** Regra 36 (o tempo manda, o código calcula, nada depende de internet depois de pronto); comandos `"pacote"`, `"gerar mais dias"` e `"atualizar pacote"`; o perfil ganhou "me expresso mal por escrito": a skill pergunta com opções, uma coisa por vez, e repete o que entendeu antes de um trabalho grande. A Regra 2 (ao vivo) ganhou a exceção do pacote, que eu peço de propósito.
- `sessao.md`/`templates.md`/`ferramentas.md`: pasta `pacote/` nos nomes canônicos, `acompanhamento.md` como único arquivo meu dentro dela, uso dos scripts.
- `selftest.py`: 117 verificações (23 novas para `pacote.py`, `apostila.py` e o `ver.py` sem internet).
- **Limpeza:** o histórico deste arquivo foi reescrito sem citar nenhum programa de terceiros. A skill nunca depende de nenhum programa ou plugin para guardar notas: só pastas de arquivos Markdown comuns.

## 6.0.0 — 2026-10-06

**A skill ficou autossuficiente.** A pasta de estudos (`Estudos/`, uma subpasta por matéria) é Markdown comum, lida e escrita pelo Claude Code com as ferramentas de arquivo (`Read`, `Write`, `Edit`, `Glob`, `Grep`).
- **Removido de propósito:** tabelas dinâmicas e destaques em sintaxe de programas de terceiros, links entre notas em colchetes duplos, links de abrir programa, detecção de programa pelo nome de pastas ocultas, `cartoes.md` (o comando `"cartões"`).
- **Convenções dos arquivos:** links Markdown relativos ao arquivo, destaques em citação com emoji (`> ▶ **Próximo passo** …`), dicas dobráveis com `<details>`, imagens `![descrição](caminho)`.
- **`scripts/ver.py` (novo): o leitor.** Converte as notas `.md` em páginas HTML numa pasta temporária (nada é gravado nos estudos) e abre no navegador padrão: tabelas, listas e tarefas, citações, `<details>`, imagens, links entre notas, fórmulas e diagramas.
- **`scripts/boletim.py` (novo):** o código calcula a média das provas, os exercícios feitos de quantos e as pendências a partir do `progresso.md`, de `exercicios/` e de `sessoes/`.
- Mantidos: `"exportar"`, exercícios e desafios em nota com dicas dobráveis, correção com `status: feito`, prova em nota, `"boletim"` e o modo pasta (Regra 35).

## 5.x — 2026-10-06

- **5.1:** exercícios, desafios e provas como notas na pasta da matéria (`exercicios/`, `provas/`), com o comando `"exportar"`; boletim com a média das provas; modo "terminal curto, notas completas" (Regra 35).
- **5.0.x:** toda leitura e escrita nos estudos passou a usar as ferramentas de arquivo, com a regra de ouro de edição (`Edit` com trecho exato e único; `Write` do arquivo inteiro só em arquivo do Claude, logo após ler), regras de segurança (nunca apagar, nunca escrever em `pratica/`) e `fila.py … --sem-gravar` (lê o arquivo e só imprime). `"retomar"` faz uma rodada só de `Glob` e, sem registros, pergunta pelo Cartão de retomada. No Windows o comando do Python é `py`. `quiz.py`: o aviso de tamanho só vale quando a maior alternativa passa de 15 caracteres. `render.py`: validação do PNG pela assinatura. Evals: 8 de 8 casos que rodam sem sandbox passam.

## 4.x — 2026-10-04 a 05

- Catálogo de visuais (`references/visuais-modelos.md`): Mermaid, SVG pronto, gráficos de função e de dados, imagem de fonte confiável, visual interativo.
- `render.py`: Mermaid local (`--mermaid-js`), recorte exato do PNG, janela do Linux, mensagem exata do erro de sintaxe.
- `fila.py registrar -` devolve a seção da fila inteira (`SECAO`/`CONTEUDO`/`FIM`).
- Evals rodados de verdade; 7 de 9 casos passavam.

## 3.x — 2026-09-30 a 10-01

- **3.0 — virada de "programação, offline" para "qualquer matéria, ao vivo":** entrevista, sondagem (a fronteira só está achada quando está cercada), plano com mapa de dependências e meu "ok", ciclo por ideia (motivar, estabelecer, conectar, checar), prova que fecha cada parte, reforço, repetição espaçada, calibração de confiança, protocolo antifrustração.
- **3.1:** o código decide o que não deve depender de obediência (`quiz.py`, `fila.py`): sorteio da posição da certa, alerta de alternativa que se entrega pela forma, correção e percentual, datas da revisão.
- **3.2–3.3:** correções de varredura, subagentes `tutor-pesquisador` e `tutor-diagramador`, ritual pequeno para dúvida pontual (Regra 34), quiz com ferramenta de perguntas.

## 2.x

- 2.0–2.1: primeira versão, centrada em programação e em trilhas fixas.
