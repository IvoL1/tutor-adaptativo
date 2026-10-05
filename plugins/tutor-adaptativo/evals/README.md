# Testes automáticos (evals) do tutor-adaptativo

Cada pasta é um caso: `prompt.md` (o que a pessoa digita) mais `graders/*.md` (as verificações).
Rodam com `claude plugin eval`, em sessões isoladas, **com e sem o plugin**, para medir o que ele acrescenta.

```bash
# todos os casos (9 casos x 3 rodadas x 2 braços = 54 execuções; usa a sua cota/créditos)
claude plugin eval . --trust-plugin

# barato: 1 rodada, sem o braço sem-plugin
claude plugin eval . --trust-plugin --runs 1 --ablation none

# só os essenciais
claude plugin eval . --trust-plugin --tag essencial

# casos que usam scripts ou gravam no cofre (precisam liberar Bash e escrita; com o MCP do Obsidian ligado, ele é usado no lugar dos arquivos diretos)
claude plugin eval . --trust-plugin --tag ferramentas --allow-tools Bash,Write,Edit
```

Execute a partir de `plugins/tutor-adaptativo/`. Os resultados ficam em `evals/results/` (não versionar).
Um caso passa com nota 1,0 por padrão (`--threshold`). Um grader `tool_used: Skill` mostra se a skill disparou,
mas não entra na nota do braço com-plugin quando há comparação.
