#!/usr/bin/env python3
"""Boletim do tutor-adaptativo: média das provas e situação dos exercícios, calculadas por código.

  boletim.py PASTA_DA_MATERIA [--hoje AAAA-MM-DD]

LÊ (nunca grava) o progresso.md (histórico de provas, posição, pendências), as notas de exercicios/ (frontmatter
`status`, `tipo`, `parte`) e a lista de sessoes/. Imprime SECAO / CONTEUDO / FIM; CONTEUDO é o bloco do boletim
entre <!-- boletim:inicio --> e <!-- boletim:fim -->. Quem grava é o Claude, com Edit, trocando o que está entre
os marcadores do _boletim-[matéria].md. Só biblioteca padrão.
"""
import datetime, pathlib, re, sys, urllib.parse

INI, FIM = "<!-- boletim:inicio -->", "<!-- boletim:fim -->"


def ler(p):
    try:
        return p.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
    except OSError:
        return ""


def secao(t, nome):
    m = re.search(rf"^## {re.escape(nome)}\s*\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    return m.group(1) if m else ""


def frontmatter(t):
    if not t.startswith("---\n"):
        return {}
    fim = t.find("\n---", 4)
    campos = {}
    for l in t[4:fim].split("\n") if fim != -1 else []:
        k, sep, v = l.partition(":")
        if sep:
            campos[k.strip()] = v.strip().strip("\"'")
    return campos


def provas(progresso):
    out = []
    # os blocos "## Prova — ..." são títulos do mesmo nível da seção "Histórico de provas": procure no arquivo todo
    for m in re.finditer(r"^## Prova — ([^\n]+?) — (\d{4}-\d{2}-\d{2})\s*\n(.*?)(?=^## |\Z)", progresso, re.M | re.S):
        r = re.search(r"Resultado:\s*(\d+(?:[.,]\d+)?)\s*%", m.group(3))
        if not r:
            continue
        st = re.search(r"Status:\s*(.+)", m.group(3))
        out.append((m.group(1).strip(), m.group(2), float(r.group(1).replace(",", ".")), (st.group(1).strip() if st else "")))
    return out


def pendencias(progresso):
    """Linhas da tabela de pendências que não são cabeçalho, separador, modelo ("—") nem "resolvido"."""
    n = 0
    for l in secao(progresso, "Pendências abertas").split("\n"):
        if not l.startswith("|"):
            continue
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        if cel[0] in ("", "—", "Conceito") or set(cel[0]) <= set("-: "):
            continue
        if cel[-1].lower().startswith("resolvido"):
            continue
        n += 1
    return n


def _utf8():
    """No Windows a saída redirecionada é cp1252 e quebra com emoji: force UTF-8."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def principal(argv):
    _utf8()
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    mat = pathlib.Path(args[0]).expanduser()
    if not (mat / "registros-da-skill").is_dir():
        print(f"ERRO: {mat} não parece uma pasta de matéria (falta registros-da-skill/).")
        return 2
    hoje = datetime.date.today().isoformat()
    if "--hoje" in argv:
        hoje = argv[argv.index("--hoje") + 1]
    prog = ler(mat / "registros-da-skill" / "progresso.md")
    pos = next((l[2:].strip() for l in secao(prog, "Posição atual").split("\n") if l.startswith("- ")), "—")
    pos = re.sub(r"^Tópico\s*/[^:]*:\s*", "", pos)  # tira o rótulo do modelo ("Tópico / Parte / Nó / Próximo passo:")
    ps = provas(prog)
    exs = []
    for f in sorted((mat / "exercicios").glob("*.md")) if (mat / "exercicios").is_dir() else []:
        fm = frontmatter(ler(f))
        if fm.get("tipo") in ("exercicio", "desafio"):
            titulo = next((l[2:].strip() for l in ler(f).split("\n") if l.startswith("# ")), f.stem)
            exs.append((titulo, f.name, fm.get("tipo", ""), fm.get("parte", ""), fm.get("status", "pendente")))
    sess = sorted((mat / "sessoes").glob("*.md")) if (mat / "sessoes").is_dir() else []
    L = [INI, "", f"> 📋 **Situação** — atualizado em {hoje} · Posição: {pos} · Pendências abertas: {pendencias(prog) or 'nenhuma'}", "", "## Provas", ""]
    if ps:
        media = sum(p[2] for p in ps) / len(ps)
        L += ["| Prova | Data | Resultado | Status |", "|---|---|---|---|"]
        L += [f"| {t} | {d} | {r:g}% | {s} |" for t, d, r, s in ps]
        L += ["", f"**Média das {len(ps)} prova(s): {media:.1f}%** · última: {ps[-1][2]:g}%"]
    else:
        L += ["Nenhuma prova feita ainda."]
    L += ["", "## Exercícios e desafios", ""]
    if exs:
        feitos = sum(1 for e in exs if e[4] == "feito")
        L += ["| Exercício | Tipo | Parte | Status |", "|---|---|---|---|"]
        L += [f"| [{t}](exercicios/{urllib.parse.quote(a)}) | {tp} | {pa} | {'✅ feito' if st == 'feito' else '⏳ pendente'} |" for t, a, tp, pa, st in exs]
        L += ["", f"**Feitos: {feitos} de {len(exs)}**"]
    else:
        L += ["Nenhum exercício em nota ainda."]
    L += ["", "## Sessões", ""]
    if sess:
        L += [f"{len(sess)} sessão(ões) gravada(s). Mais recentes:", ""]
        L += [f"- [{f.stem}](sessoes/{urllib.parse.quote(f.name)})" for f in sess[-8:][::-1]]
    else:
        L += ["Nenhuma sessão gravada ainda."]
    L += ["", FIM]
    print("SECAO: boletim")
    print("CONTEUDO:")
    print("\n".join(L))
    print("FIM")
    return 0


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
