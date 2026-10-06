#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Autoteste dos scripts do tutor-adaptativo (quiz e fila). Não usa rede nem navegador.

    python selftest.py        # sai com 0 se tudo passa, 1 se algo falha
"""
import atexit, contextlib, datetime, importlib, io, json, os, pathlib, shutil, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix="tutor-selftest-"))
atexit.register(shutil.rmtree, TMP, ignore_errors=True)  # não deixa pasta temporária para trás
os.environ["TUTOR_STATE"] = str(TMP / "estado")
sys.path.insert(0, str(AQUI))
quiz, fila = (importlib.import_module(n) for n in ("quiz", "fila"))
falhas, total = [], 0


def ok(cond, nome):
    global total
    total += 1
    if not cond:
        falhas.append(nome)


def rodar(mod_main, args, entrada=""):
    saida = io.StringIO()
    velho = sys.stdin
    sys.stdin = io.TextIOWrapper(io.BytesIO(entrada.encode("utf-8")), encoding="utf-8")
    try:
        with contextlib.redirect_stdout(saida):
            codigo = mod_main(args)
    finally:
        sys.stdin = velho
    return codigo, saida.getvalue()


BOM = "P: O que git commit faz?\nT: git commit\n+ Registra no histórico local as mudanças preparadas\n- Envia ao repositório remoto as mudanças locais\n~ confunde com push\n- Traz do repositório remoto as mudanças de outros\n~ confunde com pull\nE: Commit grava no histórico local.\n"
RUIM = "P: Por que usar constantes?\n+ Dar nome a um valor, porque assim o código fica **legível** e fácil de mudar depois em um só lugar\n- Deixar o código mais lento\n- Gastar menos memória sempre\nE: Nome explica a intenção.\n"


def testa_quiz():
    e, a = quiz.lint(quiz.parse(BOM), 3)
    ok(not e and not a, "quiz bom não gera erro nem aviso")
    e, a = quiz.lint(quiz.parse(RUIM), 3)
    txt = " ".join(a)
    ok(not e and "mais longa" in txt and "justificativa" in txt and "negrito" in txt, "lint pega certa longa, 'porque' e negrito assimétrico")
    ok(quiz.lint(quiz.parse(BOM.replace("E: Commit grava no histórico local.\n", "")), 3)[0], "sem E: é erro")
    ok(quiz.lint(quiz.parse(BOM + "- Outra\n"), 3)[0], "4 alternativas reais com --max 3 é erro")
    ok(quiz.lint(quiz.parse(BOM.replace("Traz do repositório remoto as mudanças de outros", "Envia ao repositório remoto as mudanças locais")), 3)[0], "alternativas repetidas é erro")
    ok(quiz.lint(quiz.parse(BOM.replace("- Envia", "- todas as anteriores\n- Envia")), 4)[1], "'todas as anteriores' gera aviso")
    cod, saida = rodar(quiz.main, ["montar", "--prova", "p1", "--seed", "7"], BOM)
    qid = next(l.split(": ")[1] for l in saida.splitlines() if l.startswith("ID: "))
    ok(cod == 0 and "Não sei" in saida and "CERTA" not in saida, "montar não revela a certa e acrescenta 'Não sei'")
    est = json.loads((pathlib.Path(os.environ["TUTOR_STATE"]) / f"{qid}.json").read_text(encoding="utf-8"))
    pos = [i + 1 for i, o in enumerate(est["opcoes"]) if o["certa"]][0]
    cod, saida = rodar(quiz.main, ["corrigir", qid, str(pos), "--confianca", "verde"])
    ok("RESULTADO: acerto" in saida, "corrigir: acerto")
    rodar(quiz.main, ["montar", "--prova", "p1", "--seed", "7"], BOM)
    q2 = sorted(pathlib.Path(os.environ["TUTOR_STATE"]).glob("q-*.json"))[0].stem
    est = json.loads((pathlib.Path(os.environ["TUTOR_STATE"]) / f"{q2}.json").read_text(encoding="utf-8"))
    errada = [i + 1 for i, o in enumerate(est["opcoes"]) if not o["certa"]][0]
    cod, saida = rodar(quiz.main, ["corrigir", q2, str(errada), "--confianca", "verde"])
    ok("RESULTADO: erro" in saida and "erro_confiante" in saida and "EQUIVOCO_REVELADO" in saida, "corrigir: erro confiante revela o equívoco")
    rodar(quiz.main, ["montar", "--prova", "p1"], BOM)
    q3 = sorted(pathlib.Path(os.environ["TUTOR_STATE"]).glob("q-*.json"))[0].stem
    cod, saida = rodar(quiz.main, ["corrigir", q3, "nao-sei"])
    ok("RESULTADO: lacuna" in saida, "corrigir: não sei é lacuna")
    cod, saida = rodar(quiz.main, ["corrigir", "q-inexistente", "1"])
    ok(cod == 2, "corrigir com ID inexistente dá erro")
    multi = "P: Quais são linguagens?\nMULTIPLA\n+ Python\n+ Go\n- HTML\nE: HTML é marcação.\n"
    cod, saida = rodar(quiz.main, ["montar", "--sem-nao-sei"], multi)
    q4 = next(l.split(": ")[1] for l in saida.splitlines() if l.startswith("ID: "))
    est = json.loads((pathlib.Path(os.environ["TUTOR_STATE"]) / f"{q4}.json").read_text(encoding="utf-8"))
    certas = ",".join(str(i + 1) for i, o in enumerate(est["opcoes"]) if o["certa"])
    parcial = certas.split(",")[0]
    ok("RESULTADO: erro" in rodar(quiz.main, ["corrigir", q4, parcial])[1], "múltipla: marcar só parte é erro (conjunto exato)")
    rodar(quiz.main, ["montar", "--sem-nao-sei"], multi)
    q5 = [p.stem for p in pathlib.Path(os.environ["TUTOR_STATE"]).glob("q-*.json")][-1]
    est = json.loads((pathlib.Path(os.environ["TUTOR_STATE"]) / f"{q5}.json").read_text(encoding="utf-8"))
    ok("RESULTADO: acerto" in rodar(quiz.main, ["corrigir", q5, ",".join(str(i + 1) for i, o in enumerate(est["opcoes"]) if o["certa"])])[1], "múltipla: conjunto exato é acerto")
    # fronteiras: 80% aprova, 79% e 50% pedem reforço seletivo, abaixo de 50% pede reforço completo
    for qtd, total_q, esperado in ((10, 10, "Aprovado"), (8, 10, "Aprovado"), (4, 5, "Aprovado"), (7, 10, "Reforço"), (5, 10, "Reforço"),
                                   (3, 5, "Reforço"), (4, 10, "Reforço completo"), (1, 5, "Reforço completo")):
        est = {"itens": [{"conceito": f"c{i}", "resultado": "acerto" if i < qtd else "erro", "classe": ""} for i in range(total_q)], "ultima": 0}
        quiz._salvar("prova-x", est)
        status = next(l for l in rodar(quiz.main, ["placar", "x"])[1].splitlines() if l.startswith("- Status:"))
        exato = {"Aprovado": "✅ Aprovado", "Reforço": "⚠️ Reforço", "Reforço completo": "🔁 Reforço completo"}[esperado]
        ok(status.endswith(exato), f"placar {qtd}/{total_q} -> {esperado}")
    # amostra pequena: 3 ou 4 questões avisam; 5 não
    for n, avisa in ((3, True), (4, True), (5, False)):
        quiz._salvar("prova-y", {"itens": [{"conceito": f"c{i}", "resultado": "acerto", "classe": ""} for i in range(n)], "ultima": 0})
        ok(("AMOSTRA:" in rodar(quiz.main, ["placar", "y", "--fechar"])[1]) == avisa, f"aviso de amostra pequena com {n} questões")
    # " | " no texto de uma alternativa não corta a alternativa; o equívoco vem na linha ~
    pipe = "P: Qual comando filtra a saída?\n+ ls | grep erro\n- ls > erro\n~ confunde pipe com redirecionamento\n- grep ls erro\nE: O pipe liga a saída de um comando à entrada do outro.\n"
    d = quiz.parse(pipe)
    ok(d["opcoes"][0]["texto"] == "ls | grep erro" and d["opcoes"][1]["equivoco"].startswith("confunde pipe"), "pipe no texto é preservado e ~ liga o equívoco à errada")
    ok(quiz.lint(quiz.parse("P: x\n~ solto\n+ a\n- b\nE: e\n"), 3)[1], "~ sem errada antes gera aviso")
    ok(not quiz.lint(quiz.parse("P: x\n+ 5\n- 23\n- erro\nE: e\n"), 3)[1], "alternativas curtas (5 x 23) não geram aviso de tamanho")
    # a prova não acumula entre tentativas separadas por mais de 12 horas
    quiz._salvar("prova-z", {"itens": [{"conceito": "velho", "resultado": "erro", "classe": ""}], "ultima": 0})
    antigo = pathlib.Path(os.environ["TUTOR_STATE"]) / "prova-z.json"
    os.utime(antigo, (1, 1))
    ok(quiz._prova_estado("z")["itens"] == [], "prova parada há mais de 12 h recomeça do zero")
    # --sem-nao-sei: o número seguinte é inválido, não 'não sei'; --max inválido não quebra
    rodar(quiz.main, ["montar", "--sem-nao-sei"], BOM)
    q6 = sorted(pathlib.Path(os.environ["TUTOR_STATE"]).glob("q-*.json"), key=lambda p: p.stat().st_mtime)[-1].stem
    ok(rodar(quiz.main, ["corrigir", q6, "4"])[0] == 2, "--sem-nao-sei: '4' com 3 opções é resposta inválida")
    ok(rodar(quiz.main, ["montar", "--max", "abc"], BOM)[0] == 2, "--max não numérico dá erro limpo")
    ok(rodar(quiz.main, ["corrigir", "../x", "1"])[0] == 2, "ID com caminho é recusado")


TABELA = "## Fila de revisão espaçada\n> nota\n\n| Conceito | Tópico/Parte | Aprendido em | Intervalo atual | Próxima revisão | Status |\n|---|---|---|---|---|---|\n| — | — | — | — | — | ativo |\n"


def testa_fila():
    f = TMP / "conhecimento.md"
    f.write_text("# c\n\n" + TABELA + "\n## Outra\n", encoding="utf-8")
    d = datetime.date
    reg = lambda c, r, h: rodar(fila.main, ["registrar", str(f), "--conceito", c, "--resultado", r, "--hoje", h])[0]
    ok(reg("A", "novo", "2026-10-01") == 0, "novo")
    lista, total_ = fila.vencidos(f, d(2026, 10, 2))
    ok(total_ == 1 and lista[0][0] == "A", "vence 1 dia depois")
    ok(fila.vencidos(f, d(2026, 10, 1))[1] == 0, "não vence no mesmo dia")
    seq = [("2026-10-02", "3d"), ("2026-10-05", "7d"), ("2026-10-12", "16d"), ("2026-10-28", "35d"), ("2026-12-02", "60d"), ("2027-01-31", "120d")]
    for dia, esperado in seq:
        reg("A", "acerto", dia)
        ok(fila.carregar(f)[3][0][3] == esperado, f"intervalo {esperado}")
    reg("A", "acerto", "2027-05-31")
    ok(fila.carregar(f)[3][0][5] == "arquivado", "arquiva depois de 120d")
    reg("A", "erro", "2027-06-01")
    ok(fila.carregar(f)[3][0][3:6] == ["1d", "2027-06-02", "ativo"], "erro volta a 1d e reativa")
    ok(reg("fantasma", "acerto", "2026-10-01") == 2, "acerto em conceito desconhecido é erro")
    reg("B", "erro-confiante", "2026-10-01")
    ok(any(r[0] == "B" for r in fila.carregar(f)[3]), "erro confiante cria o conceito")
    reg("F", "novo", "2026-11-01")
    reg("F", "acerto", "2026-11-02")
    reg("F", "acerto-fragil", "2026-11-05")
    linha = next(r for r in fila.carregar(f)[3] if r[0] == "F")
    ok(linha[3] == "3d" and linha[4] == "2026-11-08", "acerto frágil repete o intervalo sem avançar")
    ok(reg("fantasma2", "acerto-fragil", "2026-11-05") == 2, "acerto frágil em conceito desconhecido é erro")
    ok("## Outra" in f.read_text(encoding="utf-8"), "o resto do arquivo é preservado")
    ok(all(r[0] != "—" for r in fila.carregar(f)[3]), "linha de exemplo é removida")


def testa_fila_stdin():
    """Modo '-': o texto vem do stdin (nota lida pelo Claude) e 'registrar' devolve a seção atualizada em vez de gravar."""
    ent = "# c\n\n" + TABELA + "\n## Outra\n"
    cod, saida = rodar(fila.main, ["registrar", "-", "--conceito", "git commit", "--resultado", "novo", "--parte", "T1 / 1a", "--hoje", "2026-10-01"], ent)
    ok(cod == 0 and saida.startswith("SECAO: Fila de revisão espaçada\nCONTEUDO:\n> nota\n") and "| git commit | T1 / 1a" in saida and "2026-10-02" in saida and "—" not in saida.split("FIM")[0], "stdin: conceito novo gera a seção sem a linha de exemplo")
    ok("## Outra" not in saida and saida.split("FIM")[0].count("\n| ") >= 1, "stdin: a seção devolvida não vaza o resto do arquivo")
    com_linha = ent.replace("| — | — | — | — | — | ativo |", "| git commit | T1 / 1a | 2026-10-01 | 1d | 2026-10-02 | ativo |")
    cod, saida = rodar(fila.main, ["registrar", "-", "--conceito", "git push", "--resultado", "novo", "--hoje", "2026-10-01"], com_linha)
    corpo = saida.split("FIM")[0]
    ok(cod == 0 and "git commit" in corpo and "git push" in corpo and corpo.index("git commit") < corpo.index("git push"), "stdin: conceito novo entra depois dos existentes")
    cod, saida = rodar(fila.main, ["registrar", "-", "--conceito", "Git Commit", "--resultado", "acerto", "--hoje", "2026-10-02"], com_linha)
    ok(cod == 0 and "| 3d" in saida and "2026-10-05" in saida, "stdin: acerto avança o intervalo")
    cod, saida = rodar(fila.main, ["vencidos", "-", "--hoje", "2026-10-02"], com_linha)
    ok(cod == 0 and "VENCIDOS: 1" in saida and "git commit" in saida, "stdin: vencidos lê o texto colado")
    ok(rodar(fila.main, ["registrar", "-", "--conceito", "x", "--resultado", "acerto", "--hoje", "2026-10-02"], com_linha)[0] == 2, "stdin: acerto em conceito desconhecido é erro")
    ok(rodar(fila.main, ["vencidos", "-"], "sem tabela nenhuma\n")[0] == 2, "stdin: texto sem a seção da fila dá erro limpo")
    # --sem-gravar com caminho de arquivo: lê, imprime a seção atualizada e NÃO grava
    g = TMP / "so-leitura.md"
    g.write_text(com_linha, encoding="utf-8")
    antes = g.read_bytes()
    cod, saida = rodar(fila.main, ["registrar", str(g), "--conceito", "git commit", "--resultado", "acerto", "--hoje", "2026-10-02", "--sem-gravar"])
    ok(cod == 0 and saida.startswith("SECAO: Fila de revisão espaçada\nCONTEUDO:\n") and "| 3d" in saida and g.read_bytes() == antes, "--sem-gravar: imprime a seção e não toca o arquivo")
    ult = rodar(fila.main, ["registrar", "-", "--conceito", "z", "--resultado", "novo", "--hoje", "2026-10-01"], "## Fila de revisão espaçada\n" + TABELA.split("\n", 1)[1])
    ok(ult[0] == 0 and "| z " in ult[1], "stdin: seção que é o fim do arquivo (sem '## ' depois) também funciona")


def testa_png():
    """render.py: recorte de PNG só com a biblioteca padrão (o navegador entrega uma janela maior que a imagem)."""
    import struct, zlib
    render = importlib.import_module("render")
    def png(w, h, cor):
        bpp = 3 if cor == 2 else 4
        linhas = b"".join(b"\x00" + bytes((x * 7 + y * 13) % 256 for x in range(w * bpp)) for y in range(h))
        ch = lambda tp, c: struct.pack(">I", len(c)) + tp + c + struct.pack(">I", zlib.crc32(tp + c) & 0xffffffff)
        return b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, cor, 0, 0, 0)) + ch(b"IDAT", zlib.compress(linhas)) + ch(b"IEND", b"")
    for cor in (2, 6):
        f = TMP / f"c{cor}.png"
        f.write_bytes(png(20, 30, cor))
        ok(render._recortar_png(f, 12, 18) == (12, 18), f"recorte: devolve o tamanho final (cor {cor})")
        d = f.read_bytes()
        ok(struct.unpack(">II", d[16:24]) == (12, 18), f"recorte: o IHDR do arquivo novo diz 12x18 (cor {cor})")
        bpp = 3 if cor == 2 else 4
        bruto = zlib.decompress(b"".join(d[d.index(b"IDAT") + 4:d.index(b"IDAT") + 4 + struct.unpack(">I", d[d.index(b"IDAT") - 4:d.index(b"IDAT")])[0]] for _ in [0]))
        esperado = b"".join(b"\x00" + bytes((x * 7 + y * 13) % 256 for x in range(12 * bpp)) for y in range(18))
        ok(bruto == esperado, f"recorte: os pixels que ficam são os do canto superior esquerdo (cor {cor})")
    ok(render._recortar_png(TMP / "nao-existe.png", 5, 5) is None, "recorte: arquivo inexistente não quebra")
    pequeno = TMP / "pequeno.png"
    pequeno.write_bytes(png(4, 4, 2))
    ok(pequeno.stat().st_size < 1000 and render._png_ok(pequeno), "_png_ok: PNG válido menor que 1 KB é aceito")
    falso = TMP / "falso.png"
    falso.write_bytes(b"x" * 5000)
    ok(not render._png_ok(falso) and not render._png_ok(TMP / "nao-existe.png"), "_png_ok: lixo e arquivo ausente são recusados")


def testa_entrada():
    # entrada: BOM, UTF-16 (PowerShell), CRLF e --arquivo
    def com_stdin(b):
        velho = sys.stdin
        sys.stdin = io.TextIOWrapper(io.BytesIO(b), encoding="utf-8")
        try:
            return quiz.ler_entrada([])
        finally:
            sys.stdin = velho
    ok(com_stdin(b"\xef\xbb\xbfP: x\r\n+ a\r\n") == "P: x\n+ a\n", "entrada: BOM do UTF-8 e CRLF são tratados")
    ok(com_stdin("P: pergunta ção\n".encode("utf-16")) == "P: pergunta ção\n", "entrada: UTF-16 do PowerShell é lido")
    arq = TMP / "quiz-entrada.txt"
    arq.write_bytes(BOM.encode("utf-8"))
    cod, saida = rodar(quiz.main, ["montar", "--arquivo", str(arq)])
    ok(cod == 0 and "ID: q-" in saida, "quiz.py montar --arquivo funciona")
    # o quiz montado é achado mesmo se a pasta de estado mudar entre montar e corrigir
    antigo = quiz.STATE
    quiz.STATE = pathlib.Path(tempfile.gettempdir()) / "tutor-adaptativo"
    cod, saida = rodar(quiz.main, ["montar"], BOM)
    qid = next(l.split(": ")[1] for l in saida.splitlines() if l.startswith("ID: "))
    quiz.STATE = TMP / "outra-pasta" / "estado"
    ok("RESULTADO:" in rodar(quiz.main, ["corrigir", qid, "1"])[1], "o quiz é achado mesmo se a pasta de estado mudou no meio")
    quiz.STATE = antigo


PROGRESSO = """# progresso.md

## Posição atual
- Tópico / Parte: T1 / 1b

## Pendências abertas
| Conceito | Onde travou | Marcado em | Status |
|---|---|---|---|
| — | — | — | aberto / resolvido em [data] |
| mmc | 1a | 2026-10-06 | aberto |
| fração | 1a | 2026-10-05 | resolvido em 2026-10-06 |

## Histórico de provas
## Prova — Tópico [X], Parte [Y] — [data]
- Resultado: [%] | Status: ✅/⚠️/🔁
## Prova — Tópico T1, Parte 1a — 2026-10-06
- Resultado: 80% (4/5)
- Status: ✅ Aprovado
## Prova — Tópico T1, Parte 1b — 2026-10-07
- Resultado: 50% (2/4)
- Status: ⚠️ Reforço seletivo

## Checkpoints
x
"""


def monta_materia():
    raiz = TMP / "Estudos"
    mat = raiz / "mat"
    (mat / "registros-da-skill").mkdir(parents=True, exist_ok=True)
    (mat / "exercicios").mkdir(exist_ok=True)
    (mat / "sessoes").mkdir(exist_ok=True)
    (mat / "anexos").mkdir(exist_ok=True)
    (mat / "registros-da-skill" / "progresso.md").write_text(PROGRESSO, encoding="utf-8")
    (mat / "exercicios" / "2026-10-06-t1-1a-somar.md").write_text("---\ntipo: exercicio\nparte: 1a\nstatus: feito\n---\n# Somar frações\n", encoding="utf-8")
    (mat / "exercicios" / "2026-10-07-t1-1b-mmc.md").write_text("---\ntipo: desafio\nparte: 1b\nstatus: pendente\n---\n# Desafio: mmc\n", encoding="utf-8")
    (mat / "sessoes" / "2026-10-06-fracoes.md").write_text("# s\n", encoding="utf-8")
    return raiz, mat


def testa_boletim():
    boletim = importlib.import_module("boletim")
    raiz, mat = monta_materia()
    cod, saida = rodar(boletim.principal, [str(mat), "--hoje", "2026-10-07"])
    ok(cod == 0 and saida.startswith("SECAO: boletim") and saida.rstrip().endswith("FIM"), "boletim.py devolve SECAO/CONTEUDO/FIM")
    ok("<!-- boletim:inicio -->" in saida and "<!-- boletim:fim -->" in saida, "boletim.py traz os marcadores")
    ok("**Média das 2 prova(s): 65.0%**" in saida, "média das provas calculada por código (80 e 50 = 65.0)")
    ok("[X]" not in saida and "[%]" not in saida, "o bloco-modelo do progresso não vira prova")
    ok("**Feitos: 1 de 2**" in saida and "✅ feito" in saida and "⏳ pendente" in saida, "exercícios feitos e pendentes")
    ok("Pendências abertas: 1" in saida, "pendência 'resolvido' e linha-modelo não contam")
    ok("(exercicios/2026-10-07-t1-1b-mmc.md)" in saida and "(sessoes/2026-10-06-fracoes.md)" in saida, "links relativos ao boletim")
    ok(rodar(boletim.principal, [str(TMP / "nada")])[0] == 2, "pasta que não é matéria dá erro limpo")
    antes = (mat / "registros-da-skill" / "progresso.md").read_text(encoding="utf-8")
    ok(antes == PROGRESSO, "boletim.py não grava nos estudos")
    # regressão: no Windows a saída redirecionada é cp1252 e o emoji quebrava o script
    import subprocess
    env = {k: v for k, v in os.environ.items() if k != "PYTHONIOENCODING"}
    for script, args in (("boletim.py", [str(mat)]), ("ver.py", [str(raiz)])):
        r = subprocess.run([sys.executable, str(AQUI / script)] + args, capture_output=True, env=env)
        ok(r.returncode == 0 and "Traceback" not in r.stderr.decode("utf-8", "replace"), f"{script} roda com a saída redirecionada sem PYTHONIOENCODING")


def testa_ver():
    ver = importlib.import_module("ver")
    raiz, mat = monta_materia()
    (mat / "_painel-mat.md").write_text(
        "---\ntipo: indice\nmateria: mat\ntags: [materia]\n---\n# 📚 Matéria <b>x</b>\n\n> ▶ **Próximo passo** — somar *frações*\n\n"
        "```mermaid\ngraph TD\n  A-->B\n```\n\n- [ ] T1\n  - [x] 1a\n\n| Prova | Resultado |\n|---|---|\n| p1 | 80% |\n\n"
        "$$\nx^2\n$$\n\nFórmula $\\frac{1}{4}$ e `$código$`.\n\n<details>\n<summary>Dica 1</summary>\n\nPense no mmc.\n\n</details>\n\n"
        "![fig](anexos/f.svg) [boletim](_boletim-mat.md) [ex](exercicios/2026-10-07-t1-1b-mmc.md#topo) [site](https://exemplo.com)\n\n1. um\n2. dois\n",
        encoding="utf-8")
    (mat / "_boletim-mat.md").write_text("# Boletim\n", encoding="utf-8")
    os.environ["TUTOR_VER"] = str(TMP / "ver")
    cod, saida = rodar(ver.main, [str(raiz), "mat/_painel-mat.md"])
    info = json.loads(saida)
    ok(cod == 0 and info["ok"] and info["paginas"] >= 4 and info["aberto"] is False, "ver.py gera as páginas sem abrir o navegador")
    h = pathlib.Path(info["html"]).read_text(encoding="utf-8")
    ok("tipo: indice" not in h and "<h1>📚 Matéria &lt;b&gt;x&lt;/b&gt;</h1>" in h, "frontmatter fora do corpo e HTML do texto escapado")
    ok('<pre class="mermaid">' in h and "<table>" in h and "<details>" in h and "<summary>Dica 1</summary>" in h, "mermaid, tabela e details")
    ok("<blockquote><p>▶ <strong>Próximo passo</strong>" in h and "<em>frações</em>" in h, "citação, negrito e itálico")
    ok("☐ T1" in h and "☑ 1a" in h and "<ol>" in h, "tarefas aninhadas e lista numerada")
    ok("$\\frac{1}{4}$" in h and "<code>$código$</code>" in h and '<div class="math">$$' in h, "fórmulas ficam para o KaTeX; código em linha preservado")
    ok('href="_boletim-mat.html"' in h and 'href="exercicios/2026-10-07-t1-1b-mmc.html#topo"' in h and 'href="https://exemplo.com"' in h, "links .md viram .html; externos ficam")
    ok('src="file:///' in h and "anexos/f.svg" in h, "imagem relativa vira file:// absoluto")
    ok("integrity=" in h and "katex" in h and "mermaid" in h, "scripts externos com versão fixa e integridade")
    idx = (pathlib.Path(info["html"]).parents[1] / "index.html").read_text(encoding="utf-8")
    ok('href="mat/_painel-mat.html"' in idx and 'href="mat/_boletim-mat.html"' in idx, "index lista a matéria com painel e boletim")
    ok(rodar(ver.main, [str(raiz), str(TMP / "fora.md")])[0] == 2, "arquivo fora da pasta de estudos é recusado")
    ok(rodar(ver.main, [str(TMP / "nao-existe")])[0] == 2, "pasta inexistente dá erro limpo")
    ok(not list(raiz.rglob("*.html")), "ver.py não grava nada nos estudos")


if __name__ == "__main__":
    for t in (testa_quiz, testa_fila, testa_fila_stdin, testa_png, testa_entrada, testa_boletim, testa_ver):
        try:
            t()
        except Exception as e:  # um erro inesperado também conta como falha
            falhas.append(f"{t.__name__} quebrou: {type(e).__name__}: {e}")
    print(f"{total - len([f for f in falhas if 'quebrou' not in f])}/{total} verificações passaram")
    for f in falhas:
        print("  FALHOU:", f)
    sys.exit(1 if falhas else 0)
