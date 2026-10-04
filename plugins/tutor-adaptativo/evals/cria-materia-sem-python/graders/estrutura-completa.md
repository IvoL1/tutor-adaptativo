---
type: llm
---

PASS se, para a matéria Inglês, a resposta cria (pelas ferramentas do Obsidian MCP ou, na falta delas, gravando arquivos) os quatro registros em `registros-da-skill/` (`trilha.md`, `progresso.md`, `conhecimento.md`, `conquistas.md`) e o painel `_painel-ingles.md`, e depois mostra a árvore criada explicando onde a pessoa mexe (`pratica/`) e onde não mexe (`registros-da-skill/`).
FAIL se tenta rodar um script `cofre.py`, se escreve algo dentro de `pratica/` além de um `_leia-me.md`, se sobrescreve ou apaga arquivos que já existiam, ou se diz que criou a estrutura sem ter gravado nada.
