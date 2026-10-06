#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quiz do tutor-adaptativo: sorteio, verificação e correção feitos por código.

  quiz.py montar   [--max N] [--prova NOME] [--seed S] [--sem-nao-sei] [--arquivo F]   (entrada no stdin ou em F)
  quiz.py corrigir ID RESPOSTA [--confianca verde|amarela|vermelha]      (RESPOSTA: 1, 1,3 ou nao-sei)
  quiz.py placar   PROVA [--topico X] [--parte Y] [--fechar]

Entrada de `montar` (uma linha por item):
  P: pergunta                        obrigatória
  C: contexto                        opcional
  T: conceito testado                opcional (aparece no placar)
  + texto da alternativa certa       uma (várias se houver a linha MULTIPLA)
  - texto da errada                  uma por errada
  ~ equívoco da errada acima         opcional, na linha seguinte à errada; só aparece na correção
  E: explicação                      obrigatória
  MULTIPLA                           linha sozinha: seleção múltipla
"""
import datetime, json, os, pathlib, random, re, secrets, sys, tempfile, time

# Estado das perguntas e provas em andamento: TUTOR_STATE, senão a pasta temporária (nunca dentro do cofre Obsidian).
STATE = pathlib.Path(os.environ.get("TUTOR_STATE") or pathlib.Path(tempfile.gettempdir()) / "tutor-adaptativo")
MIN_PROVA = 5  # abaixo disso o percentual de 80% equivale a exigir 100% (3 de 3, 4 de 4)
PROVA_PARADA_H = 12  # prova sem atividade por mais que isso recomeça do zero
ID_OK = re.compile(r"^q-[0-9a-f]{8}$")
PROVA_OK = re.compile(r"^[\w.-]{1,40}$")
NAO_SEI = "Não sei"
JUSTIF = re.compile(r"\b(porque|pois|já que|uma vez que|visto que)\b", re.I)
ANTERIORES = re.compile(r"\b(todas|nenhuma)\s+(as|das)\s+anteriores\b", re.I)
HEDGE = re.compile(r"\b(geralmente|normalmente|em geral|costuma|tende a|na maioria)\b", re.I)


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def parse(texto):
    d = {"pergunta": "", "contexto": "", "conceito": "", "explicacao": "", "multipla": False, "opcoes": [], "ignoradas": []}
    for bruta in texto.splitlines():
        l = bruta.strip()
        if not l:
            continue
        pre = l[:2].upper()
        if l.upper() == "MULTIPLA":
            d["multipla"] = True
        elif pre == "P:":
            d["pergunta"] = l[2:].strip()
        elif pre == "C:":
            d["contexto"] = l[2:].strip()
        elif pre == "T:":
            d["conceito"] = l[2:].strip()
        elif pre == "E:":
            d["explicacao"] = l[2:].strip()
        elif l[0] == "~":
            if d["opcoes"] and not d["opcoes"][-1]["certa"]:
                d["opcoes"][-1]["equivoco"] = l[1:].strip()
            else:
                d["ignoradas"].append(l)
        elif l[0] in "+-":
            d["opcoes"].append({"texto": l[1:].strip(), "certa": l[0] == "+", "equivoco": ""})
        else:
            d["ignoradas"].append(l)
    return d


def lint(d, maximo):
    """Devolve (erros, avisos). Erros impedem montar; avisos pedem que o Claude refaça."""
    erros, avisos = [], []
    ops = d["opcoes"]
    certas = [o for o in ops if o["certa"]]
    erradas = [o for o in ops if not o["certa"]]
    if not d["pergunta"]:
        erros.append("falta a linha P: (a pergunta)")
    if not d["explicacao"]:
        erros.append("falta a linha E: (a explicação é obrigatória)")
    if len(ops) < 2:
        erros.append("use pelo menos 2 alternativas reais")
    if len(ops) > maximo:
        erros.append(f"{len(ops)} alternativas; o máximo é {maximo} (a ferramenta de perguntas limita a 4 opções contando 'Não sei'; para mais, use --max 4 e apresente em texto)")
    if d["multipla"]:
        if len(certas) < 2 or not erradas:
            erros.append("seleção múltipla pede 2 ou mais certas e pelo menos 1 errada")
    elif len(certas) != 1:
        erros.append(f"seleção única pede exatamente 1 alternativa certa (há {len(certas)})")
    norm = [re.sub(r"\W+", " ", o["texto"].lower()).strip() for o in ops]
    if len(set(norm)) != len(norm):
        erros.append("há alternativas repetidas")
    if d["ignoradas"]:
        avisos.append("linhas ignoradas (sem P:, C:, T:, E:, +, - ou ~ depois de uma errada): " + "; ".join(d["ignoradas"][:3]))
    if erros:
        return erros, avisos
    tam = lambda o: len(re.sub(r"[*_`]", "", o["texto"]))
    tc = sum(tam(o) for o in certas) / len(certas)
    te = [tam(o) for o in erradas]
    media = sum(te) / len(te)
    todas = [tam(o) for o in ops]
    if max(todas) > 15:  # respostas curtas (números, termos, "5" x "23") não se entregam pelo tamanho
        if tc > 1.3 * media or (tc == max(todas) and tc > 1.15 * max(te)):
            avisos.append(f"a certa é bem mais longa ({tc:.0f} caracteres contra média {media:.0f}): dá para acertar só pela forma")
        if tc < 0.6 * media:
            avisos.append(f"a certa é bem mais curta ({tc:.0f} contra média {media:.0f}): dá para acertar só pela forma")
        if max(todas) > 2 * min(todas):
            avisos.append("tamanhos muito desiguais entre as alternativas")
    com_justif = [i + 1 for i, o in enumerate(ops) if JUSTIF.search(o["texto"])]
    if com_justif:
        avisos.append(f"justificativa dentro da alternativa {com_justif} (porque/pois/já que): tire; a explicação vai em E:")
    if any(ANTERIORES.search(o["texto"]) for o in ops):
        avisos.append("não use 'todas/nenhuma das anteriores'")
    negritos = sum(1 for o in ops if "**" in o["texto"])
    if 0 < negritos < len(ops):
        avisos.append("negrito só em algumas alternativas: destaque assimétrico entrega a resposta")
    hc = [bool(HEDGE.search(o["texto"])) for o in ops]
    if any(hc[i] for i, o in enumerate(ops) if o["certa"]) and not any(hc[i] for i, o in enumerate(ops) if not o["certa"]):
        avisos.append("só a certa tem ressalva ('geralmente', 'costuma'...): ela se destaca pela forma")
    return erros, avisos


def ler_entrada(args):
    """Texto da entrada: --arquivo CAMINHO (qualquer shell, qualquer codificação) ou o stdin. Aceita BOM, UTF-16 e CRLF."""
    arq = _opcao(args, "--arquivo")
    bruto = pathlib.Path(arq).expanduser().read_bytes() if arq else sys.stdin.buffer.read()
    if bruto[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return bruto.decode("utf-16", errors="replace").replace("\r\n", "\n")
    return bruto.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")


def _arq(nome):
    return STATE / f"{nome}.json"


def _salvar(nome, obj):
    STATE.mkdir(parents=True, exist_ok=True)
    _arq(nome).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _candidatos():
    """Onde procurar o estado: o atual e a pasta temporária, para o quiz não se perder se a pasta de trabalho mudar no meio."""
    tmp = pathlib.Path(tempfile.gettempdir()) / "tutor-adaptativo"
    return [STATE] + ([tmp] if tmp != STATE else [])


def _achar(nome):
    return next((d / f"{nome}.json" for d in _candidatos() if (d / f"{nome}.json").exists()), None)


def _carregar(nome):
    p = _achar(nome)
    return json.loads(p.read_text(encoding="utf-8")) if p else None


def _apagar(nome):
    for d in _candidatos():
        try:
            (d / f"{nome}.json").unlink()
        except OSError:
            pass


def _limpar_antigos(dias=2):
    if not STATE.exists():
        return
    corte = time.time() - dias * 86400
    for p in list(STATE.glob("q-*.json")) + [x for x in STATE.glob("prova-*.json") if time.time() - x.stat().st_mtime > 30 * 86400]:
        try:
            if p.stat().st_mtime < corte or p.name.startswith("prova-"):
                p.unlink()
        except OSError:
            pass


def _opcao(args, nome, padrao=None):
    return args[args.index(nome) + 1] if nome in args and args.index(nome) + 1 < len(args) else padrao


def _prova_estado(nome):
    """Estado da prova; recomeça do zero se ficou parada por mais de PROVA_PARADA_H horas."""
    p = _achar(f"prova-{nome}")
    if p and time.time() - p.stat().st_mtime > PROVA_PARADA_H * 3600:
        _apagar(f"prova-{nome}")
    return _carregar(f"prova-{nome}") or {"itens": [], "ultima": 0}


def montar(args):
    try:
        maximo = int(_opcao(args, "--max", 3))
    except ValueError:
        print("ERRO: --max pede um número inteiro (ex.: --max 3)")
        return 2
    prova = _opcao(args, "--prova")
    if prova and not PROVA_OK.match(prova):
        print("ERRO: nome de prova inválido (use letras, números, ponto, hífen ou sublinhado; até 40 caracteres)")
        return 2
    d = parse(ler_entrada(args))
    erros, avisos = lint(d, maximo)
    if erros:
        print("ERRO: não montei o quiz. Corrija e rode de novo:")
        for e in erros:
            print(f"  - {e}")
        return 2
    _limpar_antigos()
    seed = _opcao(args, "--seed")
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    estado_prova = _prova_estado(prova) if prova else {"itens": [], "ultima": 0}
    ordem = list(range(len(d["opcoes"])))
    for _ in range(30):  # a certa não cai duas vezes seguidas na mesma posição
        rng.shuffle(ordem)
        pos = [i + 1 for i, k in enumerate(ordem) if d["opcoes"][k]["certa"]]
        if d["multipla"] or len(ordem) < 2 or pos[0] != estado_prova["ultima"]:
            break
    opcoes = [d["opcoes"][k] for k in ordem]
    qid = "q-" + secrets.token_hex(4)
    _salvar(qid, {"pergunta": d["pergunta"], "conceito": d["conceito"], "explicacao": d["explicacao"],
                  "multipla": d["multipla"], "opcoes": opcoes, "prova": prova,
                  "sem_nao_sei": "--sem-nao-sei" in args})
    if prova:
        estado_prova["ultima"] = pos[0] if not d["multipla"] else 0
        _salvar(f"prova-{prova}", estado_prova)
    print(f"ID: {qid}")
    print(f"PERGUNTA: {d['pergunta']}")
    if d["contexto"]:
        print(f"CONTEXTO: {d['contexto']}")
    print("OPCOES (mostre exatamente nesta ordem e NÃO indique qual é a certa):")
    for i, o in enumerate(opcoes, 1):
        print(f"  {i}. {o['texto']}")
    if "--sem-nao-sei" not in args:
        print(f"  {len(opcoes) + 1}. {NAO_SEI}")
    print("AVISOS: " + ("nenhum" if not avisos else ""))
    for a in avisos:
        print(f"  - {a}")
    if avisos:
        print("  (refaça a pergunta corrigindo os avisos e rode `montar` de novo)")
    return 0


def _nums(txt):
    return sorted({int(x) for x in re.findall(r"\d+", txt)})


def corrigir(args):
    if len(args) < 2:
        print("uso: quiz.py corrigir ID RESPOSTA [--confianca verde|amarela|vermelha]")
        return 2
    qid, resp = args[0], args[1].strip().lower()
    if not ID_OK.match(qid):
        print(f"ERRO: ID de quiz inválido '{qid}' (formato q-xxxxxxxx).")
        return 2
    q = _carregar(qid)
    if not q:
        print(f"ERRO: quiz {qid} não encontrado (já corrigido ou expirado). Monte de novo.")
        return 2
    conf = (_opcao(args, "--confianca") or "").lower()
    n = len(q["opcoes"])
    certas = [i + 1 for i, o in enumerate(q["opcoes"]) if o["certa"]]
    if resp in ("nao-sei", "não-sei", "naosei", "0") or (resp == str(n + 1) and not q.get("sem_nao_sei")):
        escolhidas, resultado = [], "lacuna"
    else:
        escolhidas = _nums(resp)
        if not escolhidas or any(k < 1 or k > n for k in escolhidas):
            print(f"ERRO: resposta inválida '{resp}'. Use números de 1 a {n} ou nao-sei.")
            return 2
        resultado = "acerto" if escolhidas == certas else "erro"
    classe = ""
    if resultado == "erro" and conf in ("verde", "alta"):
        classe = "erro_confiante"
    elif resultado == "acerto" and conf in ("vermelha", "baixa"):
        classe = "acerto_fragil"
    lista = lambda ks: "; ".join(f"{k}. {q['opcoes'][k - 1]['texto']}" for k in ks) or "(nenhuma)"
    print(f"RESULTADO: {resultado}")
    if classe == "erro_confiante":
        print("CLASSE: erro_confiante (foco de reforço; entra na fila a 1d depois do reforço)")
    elif classe == "acerto_fragil":
        print("CLASSE: acerto_fragil (acertou sem confiança: reforce de leve e registre com fila.py --resultado acerto-fragil, que não avança o intervalo)")
    elif resultado == "lacuna":
        print("CLASSE: lacuna (re-ensino sem peso; não é erro)")
    print(f"CERTA: {lista(certas)}")
    print(f"ESCOLHIDA: {lista(escolhidas)}")
    for k in escolhidas:
        if not q["opcoes"][k - 1]["certa"] and q["opcoes"][k - 1]["equivoco"]:
            print(f"EQUIVOCO_REVELADO: {q['opcoes'][k - 1]['equivoco']}")
    print(f"EXPLICACAO: {q['explicacao']}")
    if q.get("prova"):
        est = _prova_estado(q["prova"])
        est["itens"].append({"conceito": q["conceito"] or q["pergunta"][:40], "resultado": resultado, "classe": classe})
        _salvar(f"prova-{q['prova']}", est)
    _apagar(qid)
    return 0


def decisao(acertos, total):
    if total == 0:
        return "sem questões", "—"
    if acertos * 100 >= 80 * total:
        return "✅ Aprovado", "avança para a próxima parte; os conceitos acertados entram na fila (fila.py registrar --resultado novo)"
    if acertos * 100 >= 50 * total:
        return "⚠️ Reforço", "reforço seletivo: re-ensina só os conceitos errados e faz a reprova"
    return "🔁 Reforço completo", "reforço completo: re-ensina toda a parte e faz a reprova"


def placar(args):
    if not args:
        print("uso: quiz.py placar PROVA [--topico X] [--parte Y] [--fechar]")
        return 2
    if not PROVA_OK.match(args[0]):
        print("ERRO: nome de prova inválido.")
        return 2
    est = _prova_estado(args[0])
    if not est or not est["itens"]:
        print(f"ERRO: prova '{args[0]}' sem questões corrigidas.")
        return 2
    it = est["itens"]
    total, acertos = len(it), sum(1 for x in it if x["resultado"] == "acerto")
    pct = round(100 * acertos / total)
    status, proximo = decisao(acertos, total)
    lst = lambda f: ", ".join(dict.fromkeys(x["conceito"] for x in it if f(x))) or "—"
    print(f"## Prova — Tópico {_opcao(args, '--topico', '[X]')}, Parte {_opcao(args, '--parte', '[Y]')} — {datetime.date.today().isoformat()}")
    print(f"- Resultado: {pct}% ({acertos}/{total})")
    print(f"- Status: {status}")
    print(f"- Conceitos com erro: {lst(lambda x: x['resultado'] == 'erro')}")
    print(f"- Erros confiantes (🟢 + ❌): {lst(lambda x: x['classe'] == 'erro_confiante')}")
    print(f"- Lacunas (\"não sei\"): {lst(lambda x: x['resultado'] == 'lacuna')}")
    print("- Nota de esforço (1-5): [pergunte ao Ivo]")
    print("- Reprova (se houver): —")
    print(f"PROXIMO: {proximo}")
    if total < MIN_PROVA:
        print(f"AMOSTRA: só {total} questão(ões); com menos de {MIN_PROVA}, 80% exige acertar todas. Trate o resultado como provisório e, se a decisão for reforço, confirme com mais 1 ou 2 questões antes de travar o avanço.")
    if "--fechar" not in args:
        print(f"ABERTA: a prova '{args[0]}' continua aberta; ao concluir, rode de novo com --fechar (uma reprova usa outro nome, ex.: {args[0]}-reprova).")
    print(f"CONCEITOS_ACERTADOS: {lst(lambda x: x['resultado'] == 'acerto')}")
    if "--fechar" in args:
        _apagar(f"prova-{args[0]}")
    return 0


def main(argv):
    _utf8()
    if not argv or argv[0] not in ("montar", "corrigir", "placar"):
        print(__doc__)
        return 2
    return {"montar": montar, "corrigir": corrigir, "placar": placar}[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
