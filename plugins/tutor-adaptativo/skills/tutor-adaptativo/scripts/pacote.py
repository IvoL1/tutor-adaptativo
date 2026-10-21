#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planejador do pacote de estudo autônomo do tutor-adaptativo. Só biblioteca padrão, sem rede. NÃO grava nada.

  pacote.py planejar CURRICULO.json [--horas N] [--ja-sei t01,t02] [--json]
  pacote.py conferir PASTA_DO_PACOTE

planejar: lê o currículo (tópicos com pré-requisitos, dificuldade e blocos com minutos), valida, põe os tópicos na ordem
correta (nenhum tópico antes dos seus pré-requisitos), distribui os blocos em dias que fecham as horas por dia (pelo
menos o orçamento: nunca sobra dia curto, a não ser o último), reserva tempo de revisão espaçada (1, 3, 7 e 16 dias
depois de cada tópico acabar) e diz até onde a matéria chega em cada dia. Imprime o cronograma em Markdown (ou JSON).

conferir: lê a pasta do pacote já escrita (plano.md e dias/dia-NN.md) e confere o que dá para medir por código: a soma
dos minutos de cada dia contra as horas por dia, o texto de leitura contra o tempo declarado, o gabarito de cada dia
com exercício, imagens que faltam e fórmulas/diagramas que não aparecem sem internet.

Formato do currículo (JSON):
  {"materia": "TypeScript", "horas_por_dia": 4, "topicos": [
     {"id": "t01", "titulo": "Tipos básicos", "parte": "Fundamentos", "dificuldade": 1, "pre": [],
      "blocos": [{"tipo": "ler", "min": 30}, {"tipo": "junto", "min": 30}, {"tipo": "exercicios", "min": 45}]}]}
  tipos de bloco: ler, junto, exercicios, desafio, projeto, prova (a ordem dada é a ordem de estudo)
"""
import json, pathlib, re, sys, unicodedata

TIPOS = ("ler", "junto", "exercicios", "desafio", "projeto", "prova")
NOMES = {"ler": "Ler e entender", "junto": "Fazer junto", "exercicios": "Exercícios", "desafio": "Desafio",
         "projeto": "Projeto", "prova": "Prova"}
INTERVALOS = (1, 3, 7, 16)   # mesma ideia do fila.py: revisar 1, 3, 7 e 16 dias depois de acabar o tópico
MIN_REV = 6                  # minutos de revisão por tópico vencido
TETO_REV = 0.15              # a revisão nunca passa de 15% do dia
FOLGA_ACIMA = 1.10           # um dia pode passar até 10% do orçamento para não cortar um bloco ao meio
BLOCO_MAX = 90
PALAVRAS_POR_MIN = 150       # leitura de estudo (com pausa para entender), não leitura corrida
RE_SECAO = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s+\((\d+)\s*min\)\s*$")


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


# ---------- planejar ----------
def validar(cur, ja_sei):
    erros, avisos = [], []
    tops = cur.get("topicos")
    if not isinstance(tops, list) or not tops:
        return ["o currículo não tem a lista 'topicos'"], avisos
    ids = {}
    for i, t in enumerate(tops):
        tid = t.get("id")
        if not tid or not isinstance(tid, str):
            erros.append(f"tópico #{i + 1} sem 'id'")
            continue
        if tid in ids:
            erros.append(f"id repetido: {tid}")
        ids[tid] = t
        if not t.get("titulo"):
            erros.append(f"{tid}: sem 'titulo'")
        if not isinstance(t.get("dificuldade"), int) or not 1 <= t["dificuldade"] <= 5:
            erros.append(f"{tid}: 'dificuldade' deve ser um inteiro de 1 a 5")
        bl = t.get("blocos")
        if not isinstance(bl, list) or not bl:
            erros.append(f"{tid}: sem 'blocos'")
            continue
        for b in bl:
            if b.get("tipo") not in TIPOS:
                erros.append(f"{tid}: tipo de bloco inválido: {b.get('tipo')!r} (use {', '.join(TIPOS)})")
            if not isinstance(b.get("min"), int) or not 5 <= b["min"] <= BLOCO_MAX:
                erros.append(f"{tid}: cada bloco precisa de 'min' inteiro entre 5 e {BLOCO_MAX} (divida os maiores)")
    for tid, t in ids.items():
        for p in t.get("pre", []):
            if p not in ids:
                erros.append(f"{tid}: pré-requisito inexistente: {p}")
            elif p == tid:
                erros.append(f"{tid}: depende de si mesmo")
    for j in ja_sei:
        if j not in ids:
            erros.append(f"--ja-sei: tópico inexistente: {j}")
    if not erros:
        for tid, t in ids.items():
            pres = [ids[p]["dificuldade"] for p in t.get("pre", [])]
            if pres and t["dificuldade"] > max(pres) + 2:
                avisos.append(f"{tid}: salto de dificuldade ({max(pres)} → {t['dificuldade']}) sobre os pré-requisitos; falta um degrau no meio?")
            if not pres and t["dificuldade"] > 2 and tid not in ja_sei:
                avisos.append(f"{tid}: dificuldade {t['dificuldade']} sem nenhum pré-requisito; confira se não falta um tópico antes")
    return erros, avisos


def ordenar(tops, ja_sei):
    """Ordem de estudo: respeita os pré-requisitos e, entre os prontos, mantém a ordem em que o currículo foi escrito."""
    restantes = [t for t in tops if t["id"] not in ja_sei]
    feitos, ordem = set(ja_sei), []
    while restantes:
        pronto = next((t for t in restantes if all(p in feitos for p in t.get("pre", []))), None)
        if pronto is None:
            return ordem, [t["id"] for t in restantes]
        ordem.append(pronto)
        feitos.add(pronto["id"])
        restantes.remove(pronto)
    return ordem, []


def agendar(ordem, orcamento):
    prox = {t["id"]: 0 for t in ordem}
    no_plano = set(prox)
    acabou = {}  # id do tópico -> dia em que acabou
    dias, d = [], 0

    def candidatos():
        c = []
        for t in ordem:
            i = prox[t["id"]]
            if i < len(t["blocos"]) and all((p in acabou) or (p not in no_plano) for p in t.get("pre", [])):
                c.append((t, i))
        return c

    while any(prox[t["id"]] < len(t["blocos"]) for t in ordem):
        d += 1
        vencidos = sorted((d - dd, tid) for tid, dd in acabou.items() if (d - dd) in INTERVALOS)
        cabem = min(len(vencidos), int(orcamento * TETO_REV) // MIN_REV)
        rev = [tid for _, tid in vencidos[:cabem]]
        total, itens = MIN_REV * len(rev), []
        while total < orcamento * 0.97:
            cand = candidatos()
            if not cand:
                break
            escolha = next(((t, i) for t, i in cand if total + t["blocos"][i]["min"] <= orcamento * FOLGA_ACIMA), None)
            if escolha is None:  # nada cabe sem passar da folga: prefere passar um pouco a deixar o dia curto
                escolha = min(cand, key=lambda ti: ti[0]["blocos"][ti[1]]["min"])
            t, i = escolha
            b = t["blocos"][i]
            itens.append({"topico": t["id"], "titulo": t["titulo"], "tipo": b["tipo"], "min": b["min"], "bloco": i + 1, "de": len(t["blocos"])})
            total += b["min"]
            prox[t["id"]] += 1
            if prox[t["id"]] == len(t["blocos"]):
                acabou[t["id"]] = d
        dias.append({"dia": d, "minutos": total, "revisao": rev, "minutos_revisao": MIN_REV * len(rev), "itens": itens,
                     "pausas": total // 50, "concluidos": sorted(tid for tid, dd in acabou.items() if dd == d)})
    # dia de fechamento: só revisão dos tópicos que acabaram nos últimos 16 dias e ainda não foram revistos até o fim
    recentes = [tid for tid, dd in acabou.items() if d - dd < max(INTERVALOS)]
    if recentes:
        recentes.sort(key=lambda tid: -acabou[tid])
        n = min(len(recentes), orcamento // MIN_REV)
        d += 1
        dias.append({"dia": d, "minutos": MIN_REV * n, "revisao": recentes[:n], "minutos_revisao": MIN_REV * n, "itens": [], "pausas": 0,
                     "concluidos": [], "fechamento": True})
    return dias


def cobertura(dias, ordem):
    por_id = {t["id"]: t for t in ordem}
    ate, vistos = [], []
    for dia in dias:
        vistos += dia["concluidos"]
        ate.append({"dia": dia["dia"], "topicos_concluidos": len(vistos),
                    "ultimo": por_id[vistos[-1]]["titulo"] if vistos else None})
    return ate


def md_cronograma(cur, ordem, dias, orcamento, avisos, movidos):
    por_id = {t["id"]: t for t in ordem}
    mat, h = cur.get("materia", "Matéria"), orcamento / 60
    util = sum(d["minutos"] - d["minutos_revisao"] for d in dias)
    L = [f"# Cronograma — {mat} ({h:g} h por dia)", "",
         f"- **{len(ordem)} tópicos** em **{len(dias)} dias** · {util} min de conteúdo novo ({util / 60:.1f} h) mais a revisão espaçada.",
         f"- Cada dia soma **pelo menos {orcamento} min**; um dia pode passar até 10% para não cortar um bloco ao meio.", ""]
    if movidos:
        L += ["**Atenção:** a ordem foi ajustada para respeitar os pré-requisitos: " + ", ".join(movidos) + ".", ""]
    for a in avisos:
        L.append(f"> ⚠ {a}")
    if avisos:
        L.append("")
    for dia in dias:
        extra = f" (revisão {dia['minutos_revisao']} min)" if dia["minutos_revisao"] else ""
        L += [f"## Dia {dia['dia']} — {dia['minutos']} min{extra}" + (" · fechamento" if dia.get("fechamento") else ""), "",
              "| # | Min | Bloco | Tópico |", "|---|---|---|---|"]
        n = 0
        if dia["revisao"]:
            n += 1
            L.append(f"| {n} | {dia['minutos_revisao']} | Revisão espaçada | " + ", ".join(f"{t} {por_id[t]['titulo']}" for t in dia["revisao"]) + " |")
        for it in dia["itens"]:
            n += 1
            cont = f" ({it['bloco']}/{it['de']})" if it["de"] > 1 else ""
            L.append(f"| {n} | {it['min']} | {NOMES[it['tipo']]}{cont} | {it['topico']} {it['titulo']} |")
        if dia["concluidos"]:
            L += ["", "Fecha: " + ", ".join(f"{t} {por_id[t]['titulo']}" for t in dia["concluidos"]) + "."]
        L.append("")
    L += ["## Até onde cabe", "", "| Se eu só tiver… | Termino… |", "|---|---|"]
    for c in cobertura(dias, ordem):
        L.append(f"| {c['dia']} dia(s) | {c['topicos_concluidos']} de {len(ordem)} tópicos" + (f" (até “{c['ultimo']}”)" if c["ultimo"] else "") + " |")
    return "\n".join(L) + "\n"


def planejar(args):
    flags = {}
    pos = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--horas", "--ja-sei"):
            flags[a] = args[i + 1] if i + 1 < len(args) else ""
            i += 2
        elif a.startswith("--"):
            flags[a] = True
            i += 1
        else:
            pos.append(a)
            i += 1
    if not pos:
        print(__doc__)
        return 2
    try:
        cur = json.loads(pathlib.Path(pos[0]).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        print(f"ERRO: não consegui ler o currículo: {e}")
        return 2
    ja_sei = {x.strip() for x in str(flags.get("--ja-sei", "")).split(",") if x.strip()}
    erros, avisos = validar(cur, ja_sei)
    horas = flags.get("--horas") or cur.get("horas_por_dia")
    try:
        orcamento = round(float(str(horas).replace(",", ".")) * 60)
        if orcamento < 30:
            raise ValueError
    except (TypeError, ValueError):
        erros.append("faltam as horas por dia (--horas N ou 'horas_por_dia' no currículo; mínimo 0,5)")
    if erros:
        print("ERROS:")
        for e in erros:
            print("- " + e)
        return 1
    ordem, presos = ordenar(cur["topicos"], ja_sei)
    if presos:
        print("ERRO: pré-requisitos em ciclo entre: " + ", ".join(presos))
        return 1
    original = [t["id"] for t in cur["topicos"] if t["id"] not in ja_sei]
    movidos = [t["id"] for t, o in zip(ordem, original) if t["id"] != o]
    for a, b in zip(ordem, ordem[1:]):
        if b["dificuldade"] > a["dificuldade"] + 2:
            avisos.append(f"{b['id']}: sobe {a['dificuldade']} → {b['dificuldade']} em relação ao tópico anterior ({a['id']}); suavize a transição")
    dias = agendar(ordem, orcamento)
    if flags.get("--json"):
        print(json.dumps({"materia": cur.get("materia"), "orcamento_min": orcamento, "ordem": [t["id"] for t in ordem], "ja_sei": sorted(ja_sei),
                          "avisos": avisos, "dias": dias, "cobertura": cobertura(dias, ordem)}, ensure_ascii=False, indent=1))
    else:
        print(md_cronograma(cur, ordem, dias, orcamento, avisos, movidos))
    return 0


# ---------- conferir ----------
def frontmatter(txt):
    if txt.startswith("---\n"):
        fim = txt.find("\n---", 4)
        if fim != -1:
            meta = {}
            for l in txt[4:fim].splitlines():
                if ":" in l:
                    k, v = l.split(":", 1)
                    meta[k.strip()] = v.strip()
            return meta, txt[fim + 4:]
    return {}, txt


def tipo_da_secao(titulo):
    t = sem_acento(titulo)
    for chave, tipo in (("revis", "revisao"), ("ler", "ler"), ("fazer junto", "junto"), ("junto", "junto"), ("exerc", "exercicios"),
                        ("desafio", "desafio"), ("projeto", "projeto"), ("prova", "prova")):
        if t.startswith(chave):
            return tipo
    return "outro"


def conferir_dia(arq, orcamento, pasta):
    txt = arq.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
    meta, corpo = frontmatter(txt)
    probs, secs, atual = [], [], None
    for l in corpo.split("\n"):
        m = RE_SECAO.match(l)
        if m:
            atual = {"n": int(m.group(1)), "titulo": m.group(2), "min": int(m.group(3)), "palavras": 0, "tipo": tipo_da_secao(m.group(2))}
            secs.append(atual)
        elif l.startswith("## "):
            atual = None
        elif atual is not None:
            atual["palavras"] += len(re.findall(r"\w+", l))
    total = sum(s["min"] for s in secs)
    fechamento = meta.get("fechamento", "").lower() in ("sim", "true", "1")
    if not secs:
        probs.append("nenhuma seção no formato `## N. Tipo — título (M min)`")
    if "minutos" in meta and meta["minutos"].isdigit() and int(meta["minutos"]) != total:
        probs.append(f"frontmatter diz {meta['minutos']} min, mas as seções somam {total} min")
    if secs and not fechamento and total < orcamento * 0.97:
        probs.append(f"o dia soma {total} min, abaixo do orçamento de {orcamento} min")
    if secs and total > orcamento * (FOLGA_ACIMA + 0.05):
        probs.append(f"o dia soma {total} min, mais de 15% acima do orçamento de {orcamento} min")
    for s in secs:
        if s["tipo"] == "ler" and s["palavras"] / PALAVRAS_POR_MIN > s["min"] * 1.25:
            probs.append(f"seção {s['n']} (“{s['titulo']}”): {s['palavras']} palavras levam ~{round(s['palavras'] / PALAVRAS_POR_MIN)} min, mas declara {s['min']} min; corte texto ou aumente o tempo")
        if s["tipo"] == "ler" and s["palavras"] < 40:
            probs.append(f"seção {s['n']} (“{s['titulo']}”): quase sem texto ({s['palavras']} palavras) para um bloco de leitura")
    pratica = any(s["tipo"] in ("exercicios", "desafio", "projeto", "prova") for s in secs)
    num = re.search(r"dia-(\d+)", arq.name)
    if pratica and num and not (pasta / "gabaritos" / f"dia-{num.group(1)}.md").is_file():
        probs.append(f"tem exercício, mas falta gabaritos/dia-{num.group(1)}.md")
    if pratica and not re.search(r"crit[ée]rio de pronto", corpo, re.I):
        probs.append("os exercícios não dizem o 'Critério de pronto' (o que conseguir/observar ao acertar)")
    if re.search(r"(?<![\\$\w])\$[^$\n]+\$", corpo) or "```mermaid" in corpo:
        probs.append("tem fórmula LaTeX ($…$) ou bloco mermaid: não aparece sem internet; escreva a fórmula em texto/Unicode e use imagem em anexos/")
    for alvo in re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", corpo):
        if not re.match(r"^[a-z]+:", alvo) and not (arq.parent / alvo).resolve().is_file():
            probs.append(f"imagem não encontrada: {alvo}")
    return {"arquivo": arq.name, "minutos": total, "palavras": sum(s["palavras"] for s in secs), "problemas": probs}


def conferir(args):
    if not args:
        print(__doc__)
        return 2
    pasta = pathlib.Path(args[0]).expanduser().resolve()
    plano = pasta / "plano.md"
    if not plano.is_file():
        print(f"ERRO: {plano} não existe (a pasta do pacote precisa de plano.md com 'horas_por_dia' no frontmatter)")
        return 2
    meta, _ = frontmatter(plano.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n"))
    try:
        orcamento = round(float(meta["horas_por_dia"].replace(",", ".")) * 60)
    except (KeyError, ValueError):
        print("ERRO: plano.md sem 'horas_por_dia: N' no frontmatter")
        return 2
    arqs = sorted((pasta / "dias").glob("dia-*.md")) if (pasta / "dias").is_dir() else []
    if not arqs:
        print("ERRO: nenhum dias/dia-NN.md encontrado")
        return 2
    res = [conferir_dia(a, orcamento, pasta) for a in arqs]
    ruins = 0
    for r in res:
        marca = "OK  " if not r["problemas"] else "FALHA"
        ruins += bool(r["problemas"])
        print(f"{marca} {r['arquivo']}: {r['minutos']} min, {r['palavras']} palavras")
        for p in r["problemas"]:
            print(f"     - {p}")
    print(f"RESUMO: {len(res)} dia(s) conferido(s), {ruins} com problema; orçamento {orcamento} min/dia")
    return 1 if ruins else 0


def main(argv):
    _utf8()
    if not argv or argv[0] not in ("planejar", "conferir"):
        print(__doc__)
        return 2
    return planejar(argv[1:]) if argv[0] == "planejar" else conferir(argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
