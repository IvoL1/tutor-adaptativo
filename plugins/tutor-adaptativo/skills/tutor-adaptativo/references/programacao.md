# Referência — Programação: o que só vale quando a matéria envolve código

> Leia quando a matéria for uma linguagem, framework, biblioteca ou ferramenta de programação, ou quando o projeto de prática for código. Em qualquer outra matéria, ignore este arquivo.

> **Nesta referência:**
> **1. Princípios universais de clean code**
> **2. Versionamento (git)**
> **3. Scaffold automático — limpar primeiro**
> **4. Documentação da versão instalada**
> **5. Estrutura e nomenclatura do projeto**
> **6. Fechamento Ship it para código**

## Princípios universais de clean code

> **As convenções específicas de cada tecnologia NÃO ficam aqui** — são levantadas na entrevista (a partir da fonte oficial) e registradas no `trilha.md`. Aqui ficam só os princípios **universais**, válidos em qualquer linguagem. Todo exemplo de aula, desde o primeiro, já é escrito assim — clean code se aprende por repetição visual, não só por correção depois do erro.

- **Nomes que explicam a intenção** — `fetchUsers` em vez de `getData`; `isLoading` em vez de `flag`.
- **Funções pequenas e com um propósito** — se faz mais de uma coisa, pode ser dividida.
- **Sem números ou strings mágicos** — use constantes nomeadas.
- **Não repita a si mesmo (DRY)** — lógica repetida vira função.
- **Tipos e contratos explícitos nos pontos de entrada** — quando a linguagem permite.
- **Trate os erros** — não ignore falhas em silêncio.
- **Idioma:** nomes de variáveis, funções e classes seguem a convenção da tecnologia (quase sempre inglês — registrado no `trilha.md`); comentários explicativos no código ficam em português, para não virar mais uma camada de tradução enquanto aprendo.

> As convenções concretas (PascalCase x snake_case, estrutura de pastas, um módulo por arquivo etc.) variam por tecnologia e ficam no `trilha.md`.

## Versionamento (git)

Para qualquer projeto técnico:
- `git init` no momento de criar o projeto; primeiro commit antes do código próprio: `chore: init project`.
- Commits frequentes em **Conventional Commits**: `tipo: descrição breve`.
- Tipos principais: `feat`, `fix`, `chore`, `refactor`, `style`, `test`, `docs`, `perf`, `build`, `ci`, `revert`. A especificação ([conventionalcommits.org, v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)) obriga só `feat` e `fix`; os outros são convenção recomendada.
- Ao concluir um exercício com o código funcionando: **commit**. No fim de cada sessão, lembre de commitar antes de fechar.
- **O que é versionado:** só `pratica/projeto/` (o projeto de prática, que cresce a trilha inteira). `pratica/treinos/` são exercícios soltos e **não** entram em git — não há commit a cobrar neles.

## Scaffold automático — limpar primeiro

> Quando a tecnologia gera uma estrutura pré-montada automaticamente (ex.: `npx create-next-app@latest`, `npm create vite@latest`, `rails new`, `django-admin startproject`), **antes de qualquer exercício**, diga:

1. **O que remover** do que foi gerado (arquivos de demonstração, código de exemplo não usado, CSS e conteúdo de exemplo) — e por que cada um pode sair.
2. **O que manter e por quê** — o que realmente faz parte da convenção da tecnologia (não é lixo, é estrutura).
3. **A árvore de pastas depois da limpeza**, para eu comparar visualmente com o que veio pronto.

Isso evita eu carregar arquivo de demonstração sem saber se é essencial ou decorativo — fico só com o que importa para aquela tecnologia.

## Documentação da versão instalada

Quando a tecnologia distribui a documentação junto do pacote instalado, ou tem documentação versionada, **prefira essa fonte** — ela bate exatamente com o que está no meu projeto (`references/pedagogia.md` → "Fontes e versão — regra permanente").

Exemplo verificado na documentação oficial do Next.js (página da versão 16.3.8, atualizada em 07/09/2026 e conferida em 30/09/2026, [nextjs.org/docs/app/guides/ai-agents](https://nextjs.org/docs/app/guides/ai-agents)): desde a 16.2 o pacote `next` traz a documentação completa em `node_modules/next/dist/docs/`, e qualquer página de [nextjs.org/docs](https://nextjs.org/docs) aceita `.md` no fim da URL para devolver Markdown. Isso pode mudar: **confirme na fonte** antes de citar.

## Estrutura e nomenclatura do projeto

Ao criar qualquer arquivo ou pasta do projeto, siga `references/pedagogia.md` → "Estrutura e texto de apoio": onde criar, como nomear, árvore atualizada e uma boa prática. O que é específico da tecnologia (nomenclatura, estrutura recomendada, ferramentas) vem da seção "Convenções desta matéria" do `trilha.md`.

## Fechamento Ship it para código

Quando o fechamento da trilha é 🚀 Ship it (`references/projetos.md` → "Protocolo de Validação de Projetos") e o projeto é código:
- Testes cobrindo o que importa.
- **README claro:** o que é, stack, como rodar, prints.
- **Uma passada final de clean code em todo o projeto**, do início ao fim, usando a lista de "Princípios universais de clean code" como checklist.
- **Deploy** funcionando.
- **Histórico de commits limpo.**

Termino com algo **publicável**: um repositório no GitHub com README claro, deploy funcionando e commits organizados — é o que um recrutador abre primeiro, e vira peça de portfólio.
