#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apostila em PDF (e HTML) do pacote de estudo, 100% offline. Só biblioteca padrão; usa o Chrome ou o Edge já instalados.

  apostila.py SAIDA.pdf ARQ1.md [ARQ2.md ...]     junta as notas, na ordem dada, num PDF (SAIDA.html com --html)
  apostila.py --pacote PASTA_DO_PACOTE            gera pdf/plano.pdf, pdf/dia-NN.pdf e pdf/gabarito-dia-NN.pdf (ou .html, sem Chrome/Edge)

Não precisa de internet: o PDF não carrega nada de fora (fórmulas e diagramas devem estar em texto ou em imagens locais,
como o `pacote.py conferir` cobra). As dicas dobráveis (<details>) saem abertas no papel. Escreve só o PDF/HTML pedido
(no modo --pacote, só dentro de PASTA/pdf/); nunca altera os .md. Sem Chrome nem Edge, gera páginas HTML prontas para imprimir
(Ctrl+P → Salvar como PDF em qualquer navegador) e avisa.
"""
import html, json, os, pathlib, re, shutil, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import render  # noqa: E402  (navegador, _lancar, _encerrar, _esperar_png)
import ver     # noqa: E402  (conversor de Markdown)

CSS = """
@page{size:A4;margin:18mm 16mm}
body{font:11pt/1.55 system-ui,"Segoe UI",Arial,sans-serif;color:#111;background:#fff;margin:0}
h1{font-size:19pt;margin:0 0 .4em;page-break-before:always}section:first-of-type h1{page-break-before:avoid}
h2{font-size:14pt;border-bottom:1px solid #bbb;padding-bottom:.2em;margin:1.4em 0 .5em;page-break-after:avoid}h3{font-size:12pt;page-break-after:avoid}
code{background:#f2f2f2;padding:.1em .3em;border-radius:3px;font-size:.92em}
pre{background:#f6f6f6;border:1px solid #ccc;border-radius:4px;padding:8px;white-space:pre-wrap;word-break:break-word;page-break-inside:avoid}pre code{background:none;padding:0}
table{border-collapse:collapse;max-width:100%;page-break-inside:avoid}th,td{border:1px solid #999;padding:4px 9px;text-align:left}th{background:#eee}
blockquote{margin:.8em 0;padding:.3em .9em;border-left:4px solid #555;background:#f4f4f4;page-break-inside:avoid}
details{border:1px dashed #888;border-radius:4px;padding:.3em .8em;margin:.6em 0}summary{font-weight:700}
img{max-width:100%}ul.tarefas{list-style:none;padding-left:1.2em}a{color:#111;text-decoration:none}
"""


def html_de(arquivos, titulo):
    base_tmp = pathlib.Path(tempfile.mkdtemp(prefix="tutor-apostila-"))
    partes = []
    try:
        for arq in arquivos:
            arq = pathlib.Path(arq).resolve()
            txt = arq.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
            corpo, _ = ver.tira_frontmatter(txt)
            h = ver.blocos(corpo, arq, arq.parent, base_tmp)
            h = re.sub(r'<a href="(?!https?:|mailto:|#)[^"]*">(.*?)</a>', r"\1", h)  # link entre notas não existe no papel
            h = h.replace("<details>", "<details open>")
            partes.append(f"<section>{h}</section>")
    finally:
        shutil.rmtree(base_tmp, ignore_errors=True)
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{html.escape(titulo)}</title>'
            f"<style>{CSS}</style></head><body>{''.join(partes)}</body></html>")


def para_pdf(html_txt, saida, nav):
    saida = pathlib.Path(saida).resolve()
    saida.parent.mkdir(parents=True, exist_ok=True)
    if saida.exists():
        saida.unlink()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="tutor-apostila-"))
    pag = tmp / "apostila.html"
    pag.write_text(html_txt, encoding="utf-8")
    marcador = "tutor-render-" + os.urandom(4).hex()
    perfil = pathlib.Path(tempfile.gettempdir()) / marcador
    p = render._lancar(nav, pag.as_uri(), perfil, ["--no-pdf-header-footer", f"--print-to-pdf={saida}"])
    try:
        ok = render._esperar_png(saida, 60)
    finally:
        render._encerrar(p, marcador)
        shutil.rmtree(perfil, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)
    return ok and saida.read_bytes()[:5] == b"%PDF-"


def pacote(pasta, nav):
    pasta = pathlib.Path(pasta).expanduser().resolve()
    trabalhos = []
    if (pasta / "plano.md").is_file():
        trabalhos.append(("plano.pdf", [pasta / "plano.md"]))
    for a in sorted((pasta / "dias").glob("dia-*.md")):
        trabalhos.append((a.stem + ".pdf", [a]))
    for a in sorted((pasta / "gabaritos").glob("dia-*.md")):
        trabalhos.append(("gabarito-" + a.stem + ".pdf", [a]))
    if not trabalhos:
        return {"ok": False, "erro": "nada para converter: faltam plano.md, dias/ e gabaritos/"}
    feitos, falhas = [], []
    for nome, arqs in trabalhos:
        alvo = pasta / "pdf" / nome
        h = html_de(arqs, nome)
        if nav:
            if para_pdf(h, alvo, nav):
                feitos.append(str(alvo))
            else:
                falhas.append(nome)
        else:  # sem Chrome/Edge: página pronta para imprimir (Ctrl+P → Salvar como PDF) em qualquer navegador
            alvo = alvo.with_suffix(".html")
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(h, encoding="utf-8")
            feitos.append(str(alvo))
    r = {"ok": not falhas, "arquivos": len(feitos), "pasta": str(pasta / "pdf"), "formato": "pdf" if nav else "html", "falhas": falhas}
    if not nav:
        r["aviso"] = "nenhum Chrome ou Edge encontrado: geradas páginas .html prontas para imprimir; abra uma e use Ctrl+P → Salvar como PDF"
    return r


def main(argv):
    render._utf8()
    args = [a for a in argv if not a.startswith("--")]
    nav = render.navegador()
    if "--pacote" in argv:
        if not args:
            print(__doc__)
            return 2
        r = pacote(args[0], nav)
        print(json.dumps(r, ensure_ascii=False))
        return 0 if r["ok"] else 1
    if len(args) < 2:
        print(__doc__)
        return 2
    saida, arqs = pathlib.Path(args[0]), args[1:]
    faltam = [a for a in arqs if not pathlib.Path(a).is_file()]
    if faltam:
        print(json.dumps({"ok": False, "erro": "arquivo não encontrado: " + ", ".join(faltam)}, ensure_ascii=False))
        return 2
    h = html_de(arqs, saida.stem)
    if "--html" in argv or not nav:
        alvo = saida.with_suffix(".html")
        alvo.write_text(h, encoding="utf-8")
        print(json.dumps({"ok": True, "html": str(alvo), "pdf": False, "aviso": None if nav else "sem navegador: só o HTML foi gerado"}, ensure_ascii=False))
        return 0
    ok = para_pdf(h, saida, nav)
    print(json.dumps({"ok": ok, "pdf": str(saida.resolve()) if ok else None}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
