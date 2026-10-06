#!/usr/bin/env python3
"""Leitor da pasta de estudos do tutor-adaptativo: converte os .md em páginas HTML e abre no navegador.

  ver.py RAIZ [ARQUIVO.md] [--abrir]

RAIZ é a pasta de estudos (a que tem as matérias). O script LÊ a pasta e escreve só numa pasta temporária
(TUTOR_VER, senão a temporária do sistema): nada é gravado dentro dos estudos. Gera uma página por .md, com os
links entre notas funcionando, e um index.html. Imprime uma linha JSON com o caminho da página pedida
(ARQUIVO.md; sem ele, o index). Com --abrir, abre essa página no navegador padrão.

Sem rede, as notas ainda abrem: só as fórmulas ($...$) e os diagramas (```mermaid) aparecem como texto.
Só biblioteca padrão. O Markdown aceito é o que as notas da skill usam: títulos, parágrafos, listas (com tarefas),
tabelas, citações, código, <details>, imagens, links, negrito, itálico, código em linha e fórmulas.
"""
import hashlib, html, json, os, pathlib, re, sys, tempfile, urllib.parse, webbrowser

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/"
KATEX_SRI = {
    "katex.min.css": "sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+",
    "katex.min.js": "sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg",
    "contrib/auto-render.min.js": "sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk",
}
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js"
MERMAID_SRI = "sha384-EOXBFmc3gx5mb+vn0vPvvGqACToJD24hhacX5Yx+8NUUQrHIle/Qi5Bg9o3zKwW2"
PULAR = {".git", "__pycache__", "node_modules", ".claude"}
TAGS_OK = ("br", "kbd", "sup", "sub", "mark")

CSS = """
:root{--bg:#fff;--fg:#1f2328;--mut:#59636e;--line:#d1d9e0;--soft:#f6f8fa;--acc:#0969da}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--mut:#9198a1;--line:#3d444d;--soft:#151b23;--acc:#4493f8}}
body{background:var(--bg);color:var(--fg);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0}
main{max-width:820px;margin:0 auto;padding:16px 16px 64px}
nav{border-bottom:1px solid var(--line);padding:10px 16px;font-size:14px}nav a{color:var(--acc);text-decoration:none}
h1,h2,h3{line-height:1.25;margin:1.6em 0 .5em}h1{font-size:1.8em}h2{font-size:1.4em;border-bottom:1px solid var(--line);padding-bottom:.25em}
a{color:var(--acc)}code{background:var(--soft);padding:.15em .35em;border-radius:4px;font-size:.9em}
pre{background:var(--soft);border:1px solid var(--line);border-radius:6px;padding:12px;overflow:auto}pre code{background:none;padding:0}
pre.mermaid{background:none;border:none;text-align:center}
table{border-collapse:collapse;display:block;overflow-x:auto;max-width:100%}th,td{border:1px solid var(--line);padding:6px 12px}th{background:var(--soft)}
blockquote{margin:1em 0;padding:.4em 1em;border-left:4px solid var(--acc);background:var(--soft);color:var(--fg)}blockquote>:first-child{margin-top:0}blockquote>:last-child{margin-bottom:0}
details{border:1px solid var(--line);border-radius:6px;padding:.4em .9em;margin:.7em 0}summary{cursor:pointer;font-weight:600}
img{max-width:100%}hr{border:none;border-top:1px solid var(--line)}ul.tarefas{list-style:none;padding-left:1.2em}
.meta{color:var(--mut);font-size:13px}
"""


def esc(s):
    return html.escape(s, quote=False)


# ---------- inline ----------
def inline(txt, base, raiz, saida):
    guardado = []

    def guarda(h):
        guardado.append(h)
        return f"\x00{len(guardado) - 1}\x00"

    txt = re.sub(r"`([^`]+)`", lambda m: guarda(f"<code>{esc(m.group(1))}</code>"), txt)  # código antes da fórmula: $ dentro de `` fica como código
    txt = re.sub(r"\\\$", lambda m: guarda("$"), txt)
    txt = re.sub(r"(?<!\\)\$\$.+?\$\$|(?<![\\$])\$(?=\S)[^$\n]+?(?<=\S)\$(?!\d)", lambda m: guarda(esc(m.group(0))), txt)
    txt = esc(txt)
    for t in TAGS_OK:  # só estas tags HTML simples passam
        txt = re.sub(rf"&lt;(/?{t})&gt;", r"<\1>", txt)

    def destino(url, imagem):
        u = html.unescape(url).strip()
        if re.match(r"^[a-z][a-z0-9+.-]*:", u, re.I) or u.startswith("#"):
            return u
        parte, _, ancora = u.partition("#")
        alvo = (base.parent / urllib.parse.unquote(parte)).resolve()
        if imagem:
            return alvo.as_uri()
        if parte.lower().endswith(".md"):
            try:
                rel = alvo.relative_to(raiz.resolve())
                return urllib.parse.quote(os.path.relpath(saida / rel.with_suffix(".html"), saida / base.relative_to(raiz).parent).replace("\\", "/")) + ("#" + ancora if ancora else "")
            except ValueError:
                return alvo.as_uri()
        return alvo.as_uri()

    txt = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;[^)]*&quot;)?\)", lambda m: f'<img alt="{m.group(1)}" src="{destino(m.group(2), True)}">', txt)
    txt = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{destino(m.group(2), False)}">{m.group(1)}</a>', txt)
    txt = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", txt)
    txt = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", txt)
    txt = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", txt)
    return re.sub(r"\x00(\d+)\x00", lambda m: guardado[int(m.group(1))], txt)


# ---------- blocos ----------
RE_LISTA = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_TITULO = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def celulas(linha):
    l = linha.strip()
    if l.startswith("|"):
        l = l[1:]
    if l.endswith("|") and not l.endswith("\\|"):
        l = l[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l)]


def inicio_de_bloco(l, prox=None):
    return bool(RE_TITULO.match(l) or l.startswith(("```", ">", "<details", "</details", "<summary", "$$")) or RE_LISTA.match(l)
                or re.match(r"^\s*([-*_])\s*\1\s*\1[\s\-*_]*$", l) or (l.lstrip().startswith("|") and prox is not None and RE_SEP.match(prox)))


def lista(linhas, i, base, raiz, saida):
    """Converte linhas de lista a partir de i; devolve (html, próximo i). Aninha por indentação."""
    ind0 = len(RE_LISTA.match(linhas[i]).group(1).replace("\t", "    "))
    ordenada = bool(re.match(r"\d", RE_LISTA.match(linhas[i]).group(2)))
    itens, tarefas = [], False
    while i < len(linhas):
        m = RE_LISTA.match(linhas[i])
        if not m:
            if linhas[i].strip() and itens and linhas[i].startswith((" ", "\t")):  # continuação do item
                itens[-1][0] += " " + linhas[i].strip()
                i += 1
                continue
            break
        ind = len(m.group(1).replace("\t", "    "))
        if ind < ind0:
            break
        if ind > ind0 and itens:
            sub, i = lista(linhas, i, base, raiz, saida)
            itens[-1][1] += sub
            continue
        texto = m.group(3)
        t = re.match(r"^\[([ xX])\]\s+(.*)$", texto)
        if t:
            tarefas = True
            texto = ("☑ " if t.group(1) != " " else "☐ ") + t.group(2)
        itens.append([texto, ""])
        i += 1
    tag = "ol" if ordenada else "ul"
    corpo = "".join(f"<li>{inline(t, base, raiz, saida)}{s}</li>" for t, s in itens)
    return f'<{tag}{" class=tarefas" if tarefas else ""}>{corpo}</{tag}>', i


def blocos(texto, base, raiz, saida):
    L = texto.split("\n")
    out, i, n = [], 0, len(L)
    while i < n:
        l = L[i]
        if not l.strip():
            i += 1
        elif l.startswith("```"):
            lang = l[3:].strip().split()[0] if l[3:].strip() else ""
            i += 1
            cod = []
            while i < n and not L[i].startswith("```"):
                cod.append(L[i])
                i += 1
            i += 1
            c = esc("\n".join(cod))
            out.append(f'<pre class="mermaid">{c}</pre>' if lang == "mermaid" else f"<pre><code>{c}</code></pre>")
        elif l.strip() == "$$" or (l.strip().startswith("$$") and l.strip().endswith("$$") and len(l.strip()) > 4):
            if l.strip() != "$$":
                out.append(f'<div class="math">{esc(l.strip())}</div>')
                i += 1
            else:
                mat = ["$$"]
                i += 1
                while i < n and L[i].strip() != "$$":
                    mat.append(L[i])
                    i += 1
                i += 1
                out.append(f'<div class="math">{esc(chr(10).join(mat + ["$$"]))}</div>')
        elif l.startswith(("<details", "</details", "<summary", "<!--")) or l.strip() in ("</summary>",):
            out.append(l)
            i += 1
        elif RE_TITULO.match(l):
            m = RE_TITULO.match(l)
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2), base, raiz, saida)}</h{len(m.group(1))}>")
            i += 1
        elif re.match(r"^\s*([-*_])\s*\1\s*\1[\s\-*_]*$", l) and not RE_LISTA.match(l):
            out.append("<hr>")
            i += 1
        elif l.lstrip().startswith("|") and i + 1 < n and RE_SEP.match(L[i + 1]):
            cab = celulas(l)
            i += 2
            linhas = []
            while i < n and L[i].lstrip().startswith("|"):
                linhas.append(celulas(L[i]))
                i += 1
            th = "".join(f"<th>{inline(c, base, raiz, saida)}</th>" for c in cab)
            tr = "".join("<tr>" + "".join(f"<td>{inline(c, base, raiz, saida)}</td>" for c in r) + "</tr>" for r in linhas)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>")
        elif l.startswith(">"):
            cit = []
            while i < n and L[i].startswith(">"):
                cit.append(re.sub(r"^>\s?", "", L[i]))
                i += 1
            out.append(f"<blockquote>{blocos(chr(10).join(cit), base, raiz, saida)}</blockquote>")
        elif RE_LISTA.match(l):
            h, i = lista(L, i, base, raiz, saida)
            out.append(h)
        else:
            par = [l.strip()]
            i += 1
            while i < n and L[i].strip() and not inicio_de_bloco(L[i], L[i + 1] if i + 1 < n else None):
                par.append(L[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(par), base, raiz, saida)}</p>")
    return "\n".join(out)


def tira_frontmatter(t):
    if t.startswith("---\n"):
        fim = t.find("\n---", 4)
        if fim != -1:
            meta = t[4:fim]
            return t[fim + 4:].lstrip("\n"), meta
    return t, ""


def pagina(arq, raiz, saida):
    t = arq.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
    corpo, _meta = tira_frontmatter(t)
    destino = saida / arq.relative_to(raiz).with_suffix(".html")
    h = blocos(corpo, arq, raiz, saida)
    m = ""  # o frontmatter é metadado para os scripts: não aparece na leitura
    titulo = re.search(r"^#\s+(.+)$", corpo, re.M)
    idx = urllib.parse.quote(os.path.relpath(saida / "index.html", destino.parent).replace("\\", "/"))
    doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f"<title>{esc(titulo.group(1) if titulo else arq.stem)}</title><style>{CSS}</style>"
           f'<link rel="stylesheet" href="{KATEX}katex.min.css" integrity="{KATEX_SRI["katex.min.css"]}" crossorigin="anonymous"></head><body>'
           f'<nav><a href="{idx}">📚 Estudos</a> · {esc(str(arq.relative_to(raiz)).replace(chr(92), "/"))}</nav><main>{m}{h}</main>'
           f'<script defer src="{KATEX}katex.min.js" integrity="{KATEX_SRI["katex.min.js"]}" crossorigin="anonymous"></script>'
           f'<script defer src="{KATEX}contrib/auto-render.min.js" integrity="{KATEX_SRI["contrib/auto-render.min.js"]}" crossorigin="anonymous" '
           f'onload="renderMathInElement(document.body,{{delimiters:[{{left:\'$$\',right:\'$$\',display:true}},{{left:\'$\',right:\'$\',display:false}}]}})"></script>'
           f'<script src="{MERMAID}" integrity="{MERMAID_SRI}" crossorigin="anonymous"></script>'
           f'<script>window.mermaid&&mermaid.initialize({{startOnLoad:true,securityLevel:"strict"}})</script></body></html>')
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")
    return destino


def indice(raiz, saida, paginas):
    materias = {}
    for p in paginas:
        rel = p.relative_to(saida)
        if len(rel.parts) > 1:
            materias.setdefault(rel.parts[0], []).append(rel)
    blocos_h = []
    for m in sorted(materias):
        def achar(prefixo):
            return next((r for r in materias[m] if r.name.startswith(prefixo)), None)
        links = [(nome, achar(pre)) for nome, pre in (("Painel", "_painel-"), ("Boletim", "_boletim-"))]
        itens = " · ".join(f'<a href="{urllib.parse.quote(str(r).replace(chr(92), "/"))}">{nome}</a>' for nome, r in links if r)
        blocos_h.append(f"<li><strong>{esc(m)}</strong> — {itens or 'sem painel'}</li>")
    corpo = "<h1>📚 Estudos</h1>" + ("<ul>" + "".join(blocos_h) + "</ul>" if blocos_h else "<p>Nenhuma matéria ainda.</p>")
    (saida / "index.html").write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Estudos</title><style>{CSS}</style></head><body><main>{corpo}</main></body></html>', encoding="utf-8")


def main(argv):
    for s in (sys.stdout, sys.stderr):  # no Windows a saída redirecionada é cp1252 e quebra com acento e emoji
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    raiz = pathlib.Path(args[0]).expanduser().resolve()
    if not raiz.is_dir():
        print(json.dumps({"ok": False, "erro": f"pasta de estudos não encontrada: {raiz}"}, ensure_ascii=False))
        return 2
    base_tmp = pathlib.Path(os.environ.get("TUTOR_VER") or pathlib.Path(tempfile.gettempdir()) / "tutor-ver")
    saida = base_tmp / hashlib.sha1(str(raiz).encode("utf-8")).hexdigest()[:10]
    paginas = []
    for dp, dns, fns in os.walk(raiz):
        dns[:] = [d for d in dns if d not in PULAR and not d.startswith(".")]
        for f in fns:
            if f.lower().endswith(".md"):
                paginas.append(pagina(pathlib.Path(dp) / f, raiz, saida))
    indice(raiz, saida, paginas)
    alvo = saida / "index.html"
    if len(args) > 1:
        pedido = pathlib.Path(args[1])
        pedido = (pedido if pedido.is_absolute() else raiz / pedido).resolve()
        try:
            alvo = saida / pedido.relative_to(raiz).with_suffix(".html")
        except ValueError:
            print(json.dumps({"ok": False, "erro": "o arquivo está fora da pasta de estudos"}, ensure_ascii=False))
            return 2
        if not alvo.exists():
            print(json.dumps({"ok": False, "erro": f"arquivo .md não encontrado: {pedido}"}, ensure_ascii=False))
            return 2
    aberto = False
    if "--abrir" in argv:
        try:
            aberto = bool(webbrowser.open(alvo.as_uri()))
        except Exception:
            aberto = False
    print(json.dumps({"ok": True, "html": str(alvo), "paginas": len(paginas), "aberto": aberto}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
