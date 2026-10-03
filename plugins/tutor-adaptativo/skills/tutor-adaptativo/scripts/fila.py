#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fila de revisão espaçada do tutor-adaptativo: datas e intervalos calculados por código.

  fila.py vencidos  ARQUIVO [--max 3] [--hoje AAAA-MM-DD]
  fila.py registrar ARQUIVO --conceito C --resultado novo|acerto|acerto-fragil|erro|erro-confiante
                    [--parte "T1 / 1a"] [--hoje AAAA-MM-DD]
  fila.py mostrar   ARQUIVO

ARQUIVO é o conhecimento.md da matéria. A tabela fica sob "## Fila de revisão espaçada"
e tem as colunas: Conceito | Tópico/Parte | Aprendido em | Intervalo atual | Próxima revisão | Status.
Intervalos: 1d 3d 7d 16d 35d 60d 120d e depois arquivado. Erro volta para 1d.
acerto-fragil (acertou com confiança baixa) repete o mesmo intervalo, sem avançar.
"""
import datetime, pathlib, re, sys

INTERVALOS = [1, 3, 7, 16, 35, 60, 120]
CAB = ["Conceito", "Tópico/Parte", "Aprendido em", "Intervalo atual", "Próxima revisão", "Status"]
TITULO = "## Fila de revisão espaçada"


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def _placeholder(cel):
    return all(c in ("—", "-", "") for c in cel[:5])


def carregar(caminho):
    """Devolve (linhas, inicio, fim, rows): a tabela ocupa linhas[inicio:fim]."""
    linhas = pathlib.Path(caminho).read_text(encoding="utf-8").split("\n")
    t = next((i for i, l in enumerate(linhas) if l.startswith(TITULO)), None)
    if t is None:
        raise ValueError(f"não achei o título '{TITULO}' em {caminho}")
    i = t + 1
    while i < len(linhas) and not (linhas[i].lstrip().startswith("|") and "Conceito" in linhas[i]):
        if linhas[i].startswith("## "):
            raise ValueError("a seção não tem a tabela (faltam as colunas)")
        i += 1
    if i >= len(linhas):
        raise ValueError("a seção não tem a tabela (faltam as colunas)")
    ini = i
    if _celulas(linhas[ini]) != CAB:
        raise ValueError(f"colunas inesperadas: {_celulas(linhas[ini])}; esperado {CAB}")
    fim = ini + 2
    rows = []
    while fim < len(linhas) and linhas[fim].lstrip().startswith("|"):
        cel = _celulas(linhas[fim])
        if len(cel) == 6 and not _placeholder(cel):
            rows.append(cel)
        fim += 1
    return linhas, ini, fim, rows


def salvar(caminho, linhas, ini, fim, rows):
    larg = [max(len(CAB[k]), *(len(r[k]) for r in rows)) if rows else len(CAB[k]) for k in range(6)]
    fmt = lambda c: "| " + " | ".join(c[k].ljust(larg[k]) for k in range(6)) + " |"
    tabela = [fmt(CAB), "|" + "|".join("-" * (w + 2) for w in larg) + "|"] + [fmt(r) for r in rows]
    pathlib.Path(caminho).write_text("\n".join(linhas[:ini] + tabela + linhas[fim:]), encoding="utf-8", newline="\n")


def _data(txt):
    return datetime.date.fromisoformat(txt)


def _dias(txt):
    m = re.match(r"(\d+)d$", txt.strip())
    return int(m.group(1)) if m else None


def proximo_estado(intervalo, resultado, hoje):
    """Devolve (intervalo, proxima_revisao, status) depois de `resultado`."""
    if resultado in ("novo", "erro", "erro-confiante"):
        return "1d", (hoje + datetime.timedelta(days=1)).isoformat(), "ativo"
    atual = _dias(intervalo) or 1
    if resultado == "acerto-fragil":
        return f"{atual}d", (hoje + datetime.timedelta(days=atual)).isoformat(), "ativo"
    seguintes = [d for d in INTERVALOS if d > atual]
    if not seguintes:
        return intervalo, "—", "arquivado"
    return f"{seguintes[0]}d", (hoje + datetime.timedelta(days=seguintes[0])).isoformat(), "ativo"


def vencidos(caminho, hoje, maximo=3):
    _, _, _, rows = carregar(caminho)
    devidos = [r for r in rows if r[5].lower() == "ativo" and r[4] not in ("—", "") and _data(r[4]) <= hoje]
    devidos.sort(key=lambda r: _data(r[4]))
    return devidos[:maximo], len(devidos)


def _opcao(args, nome, padrao=None):
    return args[args.index(nome) + 1] if nome in args and args.index(nome) + 1 < len(args) else padrao


def main(argv):
    _utf8()
    if len(argv) < 2 or argv[0] not in ("vencidos", "registrar", "mostrar"):
        print(__doc__)
        return 2
    cmd, caminho, args = argv[0], argv[1], argv[2:]
    hoje = _data(_opcao(args, "--hoje")) if _opcao(args, "--hoje") else datetime.date.today()
    try:
        if cmd == "mostrar":
            _, _, _, rows = carregar(caminho)
            for r in rows:
                print(" | ".join(r))
            print(f"({len(rows)} conceito(s) na fila)")
            return 0
        if cmd == "vencidos":
            lista, total = vencidos(caminho, hoje, int(_opcao(args, "--max", 3)))
            print(f"VENCIDOS: {total}" + (f" (mostrando {len(lista)}; o resto continua vencido e entra na próxima sessão)" if total > len(lista) else ""))
            for r in lista:
                atraso = (hoje - _data(r[4])).days
                print(f"- {r[0]} | {r[1]} | venceu em {r[4]} ({'hoje' if atraso == 0 else f'há {atraso} dia(s)'}) | intervalo {r[3]}")
            return 0
        conceito, resultado = _opcao(args, "--conceito"), _opcao(args, "--resultado")
        if not conceito or resultado not in ("novo", "acerto", "acerto-fragil", "erro", "erro-confiante"):
            print("ERRO: informe --conceito e --resultado novo|acerto|acerto-fragil|erro|erro-confiante")
            return 2
        linhas, ini, fim, rows = carregar(caminho)
        linha = next((r for r in rows if r[0].lower() == conceito.lower()), None)
        if linha is None:
            if resultado in ("acerto", "acerto-fragil"):
                print(f"ERRO: '{conceito}' não está na fila; registre antes como novo.")
                return 2
            linha = [conceito, _opcao(args, "--parte", "—"), hoje.isoformat(), "1d", "—", "ativo"]
            rows.append(linha)
        if resultado == "novo":
            linha[2] = hoje.isoformat()
            if _opcao(args, "--parte"):
                linha[1] = _opcao(args, "--parte")
        linha[3], linha[4], linha[5] = proximo_estado(linha[3], resultado, hoje)
        salvar(caminho, linhas, ini, fim, rows)
        print(f"OK: {linha[0]} -> intervalo {linha[3]}, próxima revisão {linha[4]}, status {linha[5]}")
        return 0
    except (ValueError, OSError) as e:
        print(f"ERRO: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
