#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Autoteste dos scripts do tutor-adaptativo (quiz, fila, cofre). Não usa rede nem navegador.

    python selftest.py        # sai com 0 se tudo passa, 1 se algo falha
"""
import atexit, contextlib, datetime, importlib, io, json, os, pathlib, shutil, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
TMP = pathlib.Path(tempfile.mkdtemp(prefix="tutor-selftest-"))
atexit.register(shutil.rmtree, TMP, ignore_errors=True)  # não deixa pasta temporária para trás
os.environ["TUTOR_STATE"] = str(TMP / "estado")
sys.path.insert(0, str(AQUI))
quiz, fila, cofre = (importlib.import_module(n) for n in ("quiz", "fila", "cofre"))
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


def testa_cofre():
    cv = TMP / "estudos"
    m = cv / "ingles"
    for d in ("registros-da-skill", "sessoes", "pratica/projeto", "pratica/treinos"):
        (m / d).mkdir(parents=True)
    (cv / "CLAUDE.md").write_text("usa a skill tutor-adaptativo", encoding="utf-8")
    (m / "_painel-ingles.md").write_text("# p", encoding="utf-8")
    reg = m / "registros-da-skill"
    (reg / "trilha.md").write_text("# t\n\n**Status:** rascunho\n", encoding="utf-8")
    (reg / "progresso.md").write_text("\n\n".join(cofre.SECOES_PROGRESSO[:1] + ["- Tópico 1 / Parte 1a"]) + "\n\n## Pendências abertas\n| Conceito | Onde | Quando | Status |\n|---|---|---|---|\n| modais | ex 2 | 2026-10-01 | aberto |\n\n## Histórico de provas\n\n## Checkpoints\n\n## Linha do tempo (sessões)\n", encoding="utf-8")
    (reg / "conquistas.md").write_text("- **Última sessão:** 2026-09-29\n", encoding="utf-8")
    (reg / "conhecimento.md").write_text("# c\n\n" + TABELA, encoding="utf-8")
    rodar(fila.main, ["registrar", str(reg / "conhecimento.md"), "--conceito", "to be", "--resultado", "novo", "--hoje", "2026-09-01"])
    ok(cofre.achar(explicito=str(cv)) == cv.resolve(), "achar por caminho explícito")
    sub = m / "pratica"
    ok(cofre.achar(cwd=str(sub)) == cv.resolve(), "achar subindo a partir de uma subpasta")
    txt = cofre.resumo(cv)
    ok("ingles" in txt and "Tópico 1" in txt and "Pendências abertas: 1" in txt and "to be" in txt, "resumo traz posição, pendência e revisão")
    ok(cofre.validar(cv) == [], "cofre bem formado valida")
    (reg / "progresso.md").write_text("vazio", encoding="utf-8")
    ok(any("Posição atual" in p for p in cofre.validar(cv)), "validar pega seção faltando")
    # hook de diário: só grava com opt-in e com a skill usada
    tr = TMP / "transcricao.jsonl"
    tr.write_text(json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "tutor-adaptativo"}}]}}) + "\n"
                  + json.dumps({"type": "user", "message": {"role": "user", "content": "o que é um loop?"}}) + "\n", encoding="utf-8")
    ent = json.dumps({"cwd": str(cv), "session_id": "s1", "transcript_path": str(tr), "last_assistant_message": "Um loop repete passos."})
    os.environ.pop("TUTOR_LOG", None)
    rodar(cofre.main, ["diario", "--hook"], ent)
    ok(not list((m / "sessoes").glob("*-auto.md")), "sem opt-in não grava nada")
    os.environ["TUTOR_LOG"] = "1"
    rodar(cofre.main, ["diario", "--hook"], ent)
    arq = list((m / "sessoes").glob("*-auto.md"))
    ok(len(arq) == 1 and "[!quote]" in arq[0].read_text(encoding="utf-8") and "Um loop repete" in arq[0].read_text(encoding="utf-8"), "com opt-in grava a pergunta e a resposta")
    rodar(cofre.main, ["diario", "--hook"], ent)
    ok(arq[0].read_text(encoding="utf-8").count("Um loop repete") == 1, "não duplica a mesma rodada")
    os.environ.pop("TUTOR_LOG", None)
    codigo, saida = rodar(cofre.main, ["resumo", "--hook", "--cofre", str(cv)])
    ok(json.loads(saida)["hookSpecificOutput"]["hookEventName"] == "SessionStart", "resumo --hook gera JSON de SessionStart")
    testa_obsidian()


def testa_obsidian():
    c2 = TMP / "novo-cofre"
    c2.mkdir()
    pasta, msgs = cofre.nova_materia(c2, "Matemática Básica")
    ok(pasta == c2 / "matematica-basica" and cofre.validar(c2) == [], "nova-materia cria uma matéria que passa na validação")
    ok((c2 / "matematica-basica" / "anexos").is_dir() and (c2 / "CLAUDE.md").is_file(), "nova-materia cria anexos/ e o CLAUDE.md do cofre")
    leit = (c2 / "README.md").read_text(encoding="utf-8")
    ok("[[_painel-matematica-basica|Matemática Básica]]" in leit and "[matéria]" not in leit, "README do cofre ganha a matéria, sem linha-modelo")
    painel = (c2 / "matematica-basica" / "_painel-matematica-basica.md").read_text(encoding="utf-8")
    ok("5/5" not in painel and "[x]" not in painel and "[Matéria]" not in painel, "painel novo não traz exemplos que parecem progresso")
    antes = {p: p.read_bytes() for p in c2.rglob("*") if p.is_file()}
    cofre.nova_materia(c2, "Matemática Básica")
    ok(antes == {p: p.read_bytes() for p in c2.rglob("*") if p.is_file()}, "nova-materia repetida não altera nada (idempotente)")
    c4 = TMP / "cofre4"
    c4.mkdir()
    (c4 / "README.md").write_text("## Matérias ativas\n- (nenhuma ainda: diga o assunto)\n\n## Matérias concluídas\n- (nenhuma)\n", encoding="utf-8", newline="\n")
    cofre.nova_materia(c4, "Inglês")
    leit2 = (c4 / "README.md").read_text(encoding="utf-8")
    ok("[[_painel-ingles|Inglês]]" in leit2 and "nenhuma ainda" not in leit2 and "- (nenhuma)" in leit2, "o marcador '(nenhuma ainda)' some quando entra a primeira matéria")
    arq, erro = cofre.nota_sessao(c2, "matematica basica", "Frações!", "## O que vimos\n- frações", "t1", "frações são divisões")
    ok(erro is None and arq.name.endswith("-fracoes.md") and "topico: t1" in arq.read_text(encoding="utf-8"), "nota da sessão: nome, frontmatter e tópico")
    painel = (c2 / "matematica-basica" / "_painel-matematica-basica.md").read_text(encoding="utf-8")
    ok(f"[[{arq.stem}]] — frações são divisões" in painel and "nenhuma sessão ainda" not in painel, "nota da sessão entra em Sessões recentes do painel")
    cofre.nota_sessao(c2, "matematica-basica", "Frações!", "mais um trecho")
    ok(arq.read_text(encoding="utf-8").count("mais um trecho") == 1 and "Acrescentado" in arq.read_text(encoding="utf-8"), "segunda nota do dia acrescenta em vez de sobrescrever")
    ok(cofre.nota_sessao(c2, "inexistente", "x", "y")[1] is not None, "nota em matéria inexistente dá erro")
    img = TMP / "foto.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 20)
    d1, _ = cofre.anexar(c2, "matematica-basica", str(img), "Meu Desenho")
    d2, _ = cofre.anexar(c2, "matematica-basica", str(img), "Meu Desenho")
    ok(d1.parent.name == "anexos" and d1 != d2 and d1.exists() and d2.exists(), "anexar copia para anexos/ sem sobrescrever")
    ok(cofre.anexar(c2, "matematica-basica", str(TMP / "x.exe"))[1] is not None, "anexar recusa arquivo inexistente ou extensão não aceita")
    ok(cofre.uri_obsidian(c2, pathlib.Path("matematica-basica/_painel-matematica-basica.md")) == "obsidian://open?vault=novo-cofre&file=matematica-basica%2F_painel-matematica-basica", "URI do Obsidian: cofre e arquivo codificados")
    # diário: conversa que só cita a skill não conta; uma chamada real conta, mesmo chegando depois (leitura incremental)
    tr = TMP / "cita.jsonl"
    tr.write_text(json.dumps({"type": "user", "message": {"role": "user", "content": "o skill tutor-adaptativo está certo?"}}) + chr(10), encoding="utf-8")
    ok(cofre._skill_usada("s-cita", str(tr)) is False, "diário: citar a skill na conversa não conta como uso")
    with open(tr, "a", encoding="utf-8") as f:
        f.write(json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "tutor-adaptativo:tutor-adaptativo"}}]}}) + chr(10))
    ok(cofre._skill_usada("s-cita", str(tr)) is True, "diário: chamada real da skill (mesmo com prefixo do plugin) conta")
    velho, velho_cwd = os.environ.pop("TUTOR_STATE"), os.getcwd()
    try:
        os.chdir(c2)
        ok(cofre.estado_dir() == c2.resolve() / ".tutor" / "estado", "o estado vive em .tutor/estado dentro do cofre")
    finally:
        os.chdir(velho_cwd)
        os.environ["TUTOR_STATE"] = velho


VTT = ("WEBVTT\nKind: captions\nLanguage: en\n\n00:00:01.000 --> 00:00:03.000 align:start position:0%\nhello <00:00:01.500><c>world</c>\n\n"
       "00:00:03.000 --> 00:00:05.000\nhello world\nthis is a test\n\n00:01:10.000 --> 00:01:12.000\nthis is a test\nsecond block &amp; more\n")


def testa_novidades():
    # entrada: BOM, UTF-16 (PowerShell), CRLF e --arquivo
    saida = io.StringIO()
    def com_stdin(b):
        velho = sys.stdin
        sys.stdin = io.TextIOWrapper(io.BytesIO(b), encoding="utf-8")
        try:
            return cofre.ler_entrada([])
        finally:
            sys.stdin = velho
    ok(com_stdin(b"\xef\xbb\xbfP: x\r\n+ a\r\n") == "P: x\n+ a\n", "entrada: BOM do UTF-8 e CRLF são tratados")
    ok(com_stdin("P: pergunta ção\n".encode("utf-16")) == "P: pergunta ção\n", "entrada: UTF-16 do PowerShell é lido")
    arq = TMP / "quiz-entrada.txt"
    arq.write_bytes(BOM.encode("utf-8"))
    cod, saida = rodar(quiz.main, ["montar", "--arquivo", str(arq)])
    ok(cod == 0 and "ID: q-" in saida, "quiz.py montar --arquivo funciona")
    # o quiz montado fora do cofre ainda é achado depois que o estado muda de pasta
    antigo = quiz.STATE
    quiz.STATE = pathlib.Path(tempfile.gettempdir()) / "tutor-adaptativo"
    cod, saida = rodar(quiz.main, ["montar"], BOM)
    qid = next(l.split(": ")[1] for l in saida.splitlines() if l.startswith("ID: "))
    quiz.STATE = TMP / "outro-cofre" / ".tutor" / "estado"
    ok("RESULTADO:" in rodar(quiz.main, ["corrigir", qid, "1"])[1], "o quiz é achado mesmo se a pasta de estado mudou no meio")
    quiz.STATE = antigo
    # nomes de matéria
    c3 = TMP / "cofre3"
    c3.mkdir()
    ok(cofre.nova_materia(c3, "CON")[0] is None and not (c3 / "con").exists(), "nome reservado do Windows é recusado")
    pasta, _ = cofre.nova_materia(c3, "Lógica [1] | básica " + "x" * 300)
    ok(pasta is not None and len(pasta.name) <= 60 and "|" not in (c3 / "README.md").read_text(encoding="utf-8").split("Matérias ativas")[1].split("##")[0].split("]]")[0].split("|", 1)[1], "nome gigante e com | ou [ vira slug curto e wikilink sem quebra")
    pasta, _ = cofre.nova_materia(c3, "Matemática")
    ok((pasta / "_sessoes-matematica.base").is_file() and 'file.inFolder("matematica/sessoes")' in (pasta / "_sessoes-matematica.base").read_text(encoding="utf-8"), "nova-materia cria a Base de sessões do Obsidian")
    ok((pasta / "fontes").is_dir() and "_sessoes-matematica.base" in (pasta / "_painel-matematica.md").read_text(encoding="utf-8"), "nova-materia cria fontes/ e liga a Base no painel")
    # nota preserva o que o Ivo escreveu à mão no painel
    painel = pasta / "_painel-matematica.md"
    painel.write_text(painel.read_text(encoding="utf-8").replace("- (nenhuma sessão ainda)", "- (nenhuma sessão ainda)\nMinha anotação: rever frações\n"), encoding="utf-8", newline="\n")
    cofre.nota_sessao(c3, "matematica", "Primeira", "a\r\nb", "t1", "r1")
    texto = painel.read_text(encoding="utf-8")
    ok("Minha anotação: rever frações" in texto and "Tabela com todas" in texto and "nenhuma sessão ainda" not in texto, "nota não apaga linhas escritas à mão em Sessões recentes")
    ok(b"\r" not in next((pasta / "sessoes").glob("*.md")).read_bytes(), "nota grava só com LF")
    # transcrição de legenda
    txt = cofre.vtt_para_texto(VTT)
    ok(txt.count("hello world") == 1 and txt.count("this is a test") == 1 and "**[00:01]** hello world this is a test" in txt and "**[01:10]** second block & more" in txt, "vtt: tira tags e repetições e agrupa por minuto")
    vtt = TMP / "aula.vtt"
    vtt.write_text(VTT, encoding="utf-8")
    nota, info = cofre.transcrever(c3, "matematica", str(vtt), titulo="Aula 1: Frações")
    conteudo = nota.read_text(encoding="utf-8")
    ok(nota.parent.name == "fontes" and "tipo: fonte" in conteudo and "pista" in conteudo and "hello world" in conteudo, "transcrever grava a nota em fontes/ com aviso de pista")
    ok(cofre.transcrever(c3, "matematica", str(TMP / "x.txt"))[0] is None and cofre.transcrever(c3, "matematica", "ftp://x")[0] is None, "transcrever recusa fonte que não é link nem .vtt/.srt")
    ok(cofre.url_limpa("https://www.youtube.com/watch?v=abc123&list=LL&index=1&t=924s") == "https://www.youtube.com/watch?v=abc123" and cofre.url_limpa("https://youtu.be/abc123?si=zzz&t=5") == "https://youtu.be/abc123", "o link guardado na nota perde lista, índice, tempo e rastreio")
    # cartões para o plugin Spaced Repetition
    cartoes, erro, n = cofre.cartoes(c3, "matematica", "O que é 1/2? :: metade\nO que é um pipe? :: liga saída a entrada\n")
    ct = cartoes.read_text(encoding="utf-8")
    ok(n == 2 and "O que é 1/2?::metade" in ct and "#flashcards/matematica" in ct, "cartões: formato Pergunta::Resposta com a etiqueta do baralho")
    ok(cofre.cartoes(c3, "matematica", "O que é 1/2? :: metade\n")[2] == 0, "cartões: não repete cartão")
    ok(cofre.cartoes(c3, "matematica", "sem separador\n")[1] is not None, "cartões: linha sem ' :: ' é recusada")


if __name__ == "__main__":
    for t in (testa_quiz, testa_fila, testa_cofre, testa_novidades):
        try:
            t()
        except Exception as e:  # um erro inesperado também conta como falha
            falhas.append(f"{t.__name__} quebrou: {type(e).__name__}: {e}")
    print(f"{total - len([f for f in falhas if 'quebrou' not in f])}/{total} verificações passaram")
    for f in falhas:
        print("  FALHOU:", f)
    sys.exit(1 if falhas else 0)
