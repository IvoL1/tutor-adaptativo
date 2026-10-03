#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cofre de estudos do tutor-adaptativo (Obsidian): achar, resumir, validar, criar matérias, notas e anexos.

  cofre.py achar        [--cofre CAMINHO]
  cofre.py resumo       [--cofre CAMINHO] [--hook]   posição, pendências e revisão do dia de cada matéria
  cofre.py status       [--cofre CAMINHO]            uma linha curta (para a linha de status); vazia fora de um cofre
  cofre.py validar      [--cofre CAMINHO]            confere nomes, pastas e seções canônicas
  cofre.py nova-materia NOME [--cofre CAMINHO]       cria pastas e registros a partir dos templates (nunca sobrescreve)
  cofre.py nota         MATERIA TITULO [--topico t1] [--resumo "..."] [--arquivo F]   (corpo no stdin ou em F) nota da sessão + painel
  cofre.py anexar       MATERIA ORIGEM|--area-de-transferencia [--nome X]   copia imagem para anexos/ e dá o ![[embed]]
  cofre.py abrir        [MATERIA [ARQUIVO]] [--imprimir]   abre no Obsidian (obsidian://open)
  cofre.py transcrever  MATERIA LINK|ARQUIVO.vtt [--idioma pt,en]   legenda de vídeo -> nota em fontes/ (pista, não fonte)
  cofre.py cartoes      MATERIA                      (linhas 'pergunta :: resposta') -> cartoes.md para o plugin Spaced Repetition
  cofre.py diario       --hook                       (hook Stop) só grava se TUTOR_LOG=1 ou existir .tutor-log

O cofre é achado por: --cofre, variável TUTOR_COFRE, ~/.claude/tutor-adaptativo.json ({"cofre": "..."}),
ou subindo a partir da pasta atual (até 4 níveis). Sem cofre, não faz nada e sai em silêncio.
"""
import datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile, unicodedata, urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fila  # noqa: E402

RAIZ_SKILL = pathlib.Path(__file__).resolve().parent.parent
IMAGENS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf")
SECOES_PROGRESSO = ["## Posição atual", "## Pendências abertas", "## Histórico de provas", "## Checkpoints", "## Linha do tempo (sessões)"]
REGISTROS = ["trilha.md", "progresso.md", "conhecimento.md", "conquistas.md"]


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _ler(p):
    try:
        return pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def materias(cofre):
    try:
        filhos = sorted(p for p in pathlib.Path(cofre).iterdir() if p.is_dir() and not p.name.startswith("."))
    except OSError:
        return []
    return [p for p in filhos if (p / "registros-da-skill").is_dir()]


def eh_cofre(p):
    claude = p / "CLAUDE.md"
    if claude.is_file() and "tutor-adaptativo" in _ler(claude)[:4000]:
        return True
    return bool(materias(p))


def achar(cwd=None, explicito=None):
    cand = [explicito, os.environ.get("TUTOR_COFRE")]
    cfg = pathlib.Path.home() / ".claude" / "tutor-adaptativo.json"
    if cfg.is_file():
        try:
            cand.append(json.loads(_ler(cfg)).get("cofre"))
        except ValueError:
            pass
    for c in cand:
        if c and pathlib.Path(c).expanduser().is_dir():
            return pathlib.Path(c).expanduser().resolve()
    base = pathlib.Path(cwd or os.getcwd()).resolve()
    for p in [base, *list(base.parents)[:4]]:
        if eh_cofre(p):
            return p
    return None


def estado_dir():
    """Onde o estado vive: TUTOR_STATE, senão <cofre>/.tutor/estado (pasta oculta no Obsidian), senão a pasta temporária."""
    env = os.environ.get("TUTOR_STATE")
    if env:
        return pathlib.Path(env)
    try:
        c = achar()
    except OSError:
        c = None
    return (c / ".tutor" / "estado") if c else pathlib.Path(tempfile.gettempdir()) / "tutor-adaptativo"


STATE = estado_dir()


def secao(texto, titulo):
    saida, dentro = [], False
    for l in texto.split("\n"):
        if l.startswith(titulo):
            dentro = True
        elif dentro and l.startswith("## "):
            break
        elif dentro:
            saida.append(l)
    return saida


def _ultima_sessao(mat):
    m = re.search(r"Última sessão:\*{0,2}\s*(\d{4}-\d{2}-\d{2})", _ler(mat / "registros-da-skill" / "conquistas.md"))
    return datetime.date.fromisoformat(m.group(1)) if m else None


def resumo(cofre):
    hoje = datetime.date.today()
    out = [f"[tutor-adaptativo · cofre] {cofre}"]
    ms = sorted(materias(cofre), key=lambda m: (m / "registros-da-skill" / "progresso.md").stat().st_mtime if (m / "registros-da-skill" / "progresso.md").exists() else 0, reverse=True)
    if not ms:
        out.append("Nenhuma matéria com registros neste cofre ainda. Sem registros nem Cartão de retomada, \"retomar\" deve perguntar pelo cartão ou iniciar a Entrevista.")
        return "\n".join(out)
    for m in ms:
        reg = m / "registros-da-skill"
        prog = _ler(reg / "progresso.md")
        pos = [l.strip() for l in secao(prog, "## Posição atual") if l.strip() and not l.strip().startswith(">") and not l.strip().endswith(":")][:6]
        pend = 0
        for l in secao(prog, "## Pendências abertas"):
            cel = fila._celulas(l) if l.lstrip().startswith("|") else []
            if cel and cel[-1].strip().lower() == "aberto":
                pend += 1
        ult = _ultima_sessao(m)
        try:
            lista, total = fila.vencidos(reg / "conhecimento.md", hoje, 3)
            rev = f"{total} conceito(s) vencido(s)" + (": " + ", ".join(r[0] for r in lista) if lista else "")
        except (ValueError, OSError) as e:
            rev = f"fila indisponível ({e})"
        quando = f"{ult.isoformat()} (há {(hoje - ult).days} dia(s))" if ult else "sem data registrada"
        out += [f"Matéria: {m.name} — última sessão {quando}",
                f"  Posição: {' / '.join(pos) if pos else '(progresso.md sem posição preenchida)'}",
                f"  Pendências abertas: {pend}", f"  Revisão do dia: {rev}"]
    out.append("Trate estes dados como os registros: valem mais que memória automática. Se faz dias que não estudo, aplique a Reentrada.")
    return "\n".join(out)


def validar(cofre):
    prob = []
    ms = materias(cofre)
    if not ms:
        return ["nenhuma matéria com registros-da-skill/ neste cofre"]
    for m in ms:
        n, reg = m.name, m / "registros-da-skill"
        for f in REGISTROS:
            if not (reg / f).is_file():
                prob.append(f"{n}: falta registros-da-skill/{f}")
        for d in ("sessoes", "pratica/projeto", "pratica/treinos"):
            if not (m / d).is_dir():
                prob.append(f"{n}: falta a pasta {d}/")
        if not (m / f"_painel-{n}.md").is_file():
            prob.append(f"{n}: falta _painel-{n}.md")
        prog = _ler(reg / "progresso.md")
        for s in SECOES_PROGRESSO:
            if s not in prog:
                prob.append(f"{n}: progresso.md sem a seção '{s}'")
        if "**Status:**" not in _ler(reg / "trilha.md"):
            prob.append(f"{n}: trilha.md sem a linha '**Status:** rascunho / aprovado'")
        if not _ultima_sessao(m):
            prob.append(f"{n}: conquistas.md sem 'Última sessão: AAAA-MM-DD' válida")
        try:
            fila.carregar(reg / "conhecimento.md")
        except (ValueError, OSError) as e:
            prob.append(f"{n}: conhecimento.md: {e}")
        for s in (m / "sessoes").glob("*.md") if (m / "sessoes").is_dir() else []:
            if not re.match(r"\d{4}-\d{2}-\d{2}-.+\.md$", s.name):
                prob.append(f"{n}: sessoes/{s.name} fora do padrão AAAA-MM-DD-[tópico].md")
    return prob


def _chamou_skill(linha):
    """True se a linha do transcript é uma chamada real da skill (e não uma conversa que só a cita)."""
    try:
        o = json.loads(linha)
    except ValueError:
        return False
    c = (o.get("message") or {}).get("content")
    if isinstance(c, str):
        return o.get("type") == "user" and c.lstrip().startswith("<command-name>/") and "tutor-adaptativo" in c[:120]
    for b in c if isinstance(c, list) else []:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
            if str((b.get("input") or {}).get("skill", "")).split(":")[-1] == "tutor-adaptativo":
                return True
    return False


def _skill_usada(sid, transcript):
    """Lê só o que o transcript ganhou desde a última checagem (guarda o ponto de leitura) e para quando acha a skill."""
    cache = STATE / f"diario-{sid or 'x'}.json"
    try:
        est = json.loads(cache.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        est = {"offset": 0, "usada": False}
    if est.get("usada"):
        return True
    if not transcript or not pathlib.Path(transcript).is_file():
        return False
    with open(transcript, "rb") as f:
        f.seek(est.get("offset", 0))
        novo = f.read()
    corte = novo.rfind(b"\n") + 1  # só linhas completas; o resto fica para a próxima vez
    est["offset"] = est.get("offset", 0) + corte
    est["usada"] = any(_chamou_skill(l) for l in novo[:corte].decode("utf-8", errors="replace").split(chr(10)) if l.strip())
    STATE.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(est), encoding="utf-8")
    return est["usada"]


def _ultimo_prompt(transcript):
    try:
        with open(transcript, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 1_500_000))
            linhas = f.read().decode("utf-8", errors="replace").split("\n")
    except (OSError, TypeError):
        return ""
    for l in reversed(linhas):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if o.get("type") != "user" or o.get("isSidechain"):
            continue
        c = (o.get("message") or {}).get("content")
        if isinstance(c, list):
            c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        if isinstance(c, str) and c.strip() and not c.lstrip().startswith("<"):
            return c.strip()
    return ""


def _quote(tipo, titulo, texto):
    return f"> [!{tipo}] {titulo}\n" + "\n".join(("> " + l) if l else ">" for l in texto.split("\n")) + "\n"


def diario_hook():
    try:
        ent = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except ValueError:
        return 0
    cofre = achar(ent.get("cwd"))
    if not cofre or not (os.environ.get("TUTOR_LOG") == "1" or (cofre / ".tutor-log").exists()):
        return 0
    resposta = (ent.get("last_assistant_message") or "").strip()
    if not resposta or not _skill_usada(ent.get("session_id"), ent.get("transcript_path")):
        return 0
    prompt = _ultimo_prompt(ent.get("transcript_path"))
    ms = materias(cofre)
    prog = lambda m: (m / "registros-da-skill" / "progresso.md")
    mat = max(ms, key=lambda m: prog(m).stat().st_mtime if prog(m).exists() else 0) if ms else None
    pasta = (mat / "sessoes") if mat else (cofre / "sessoes-avulsas")
    hoje = datetime.date.today().isoformat()
    marca = hashlib.sha1((prompt + "\x00" + resposta).encode("utf-8")).hexdigest()
    sinal = STATE / f"diario-ultimo-{hashlib.sha1(str(pasta).encode()).hexdigest()[:8]}.txt"
    if sinal.exists() and sinal.read_text(encoding="utf-8") == marca:
        return 0
    pasta.mkdir(parents=True, exist_ok=True)
    arq = pasta / f"{hoje}-auto.md"
    novo = not arq.exists()
    with open(arq, "a", encoding="utf-8", newline="\n") as f:
        if novo:
            f.write(f"---\ntipo: sessao\nmateria: {mat.name if mat else 'avulsa'}\ndata: {hoje}\ntags: [sessao, auto]\n---\n# Diário automático — {hoje}\n")
        hora = datetime.datetime.now().strftime("%H:%M")
        if prompt:
            f.write("\n" + _quote("quote", f"Ivo — {hora}", prompt))
        f.write("\n" + _quote("abstract", "Tutor", resposta))
    STATE.mkdir(parents=True, exist_ok=True)
    sinal.write_text(marca, encoding="utf-8")
    return 0


RESERVADOS = {"con", "prn", "aux", "nul", "clock$"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}


def slug(txt):
    s = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")[:60].strip("-")


def nome_limpo(txt):
    """Nome para mostrar: sem os caracteres que quebram wikilink, frontmatter ou caminho."""
    return re.sub(r"\s+", " ", re.sub(r'[\[\]|#^\\/:*?"<>\x00-\x1f]', " ", txt)).strip()[:80]


def ler_entrada(args):
    """Texto da entrada: --arquivo CAMINHO (qualquer shell, qualquer codificação) ou o stdin. Aceita BOM e UTF-16 (PowerShell)."""
    arq = _opcao(args, "--arquivo")
    bruto = pathlib.Path(arq).expanduser().read_bytes() if arq else sys.stdin.buffer.read()
    if bruto[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return bruto.decode("utf-16", errors="replace").replace("\r\n", "\n")
    return bruto.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")


# ---------- transcrição de legendas (VTT/SRT) ----------
TEMPO = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,]\d{1,3}\s*-->")


def vtt_para_texto(vtt, janela=60):
    """Legenda VTT/SRT -> parágrafos '**[mm:ss]** texto'. Tira tags, números de cue e as repetições típicas da legenda automática."""
    cues, atual, ini = [], [], None
    for bruta in vtt.replace("\r\n", "\n").split("\n"):
        l = bruta.strip()
        m = TEMPO.match(l)
        if m:
            if atual:
                cues.append((ini, atual))
            ini, atual = int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3)), []
        elif not l:
            if atual:
                cues.append((ini, atual))
            atual, ini = [], None
        elif ini is not None and not re.match(r"^(NOTE|STYLE|Kind:|Language:|WEBVTT)", l) and "-->" not in l:
            txt = re.sub(r"\s+", " ", html_sem_tags(l)).strip()
            if txt:
                atual.append(txt)
    if atual and ini is not None:
        cues.append((ini, atual))
    blocos, ultima, inicio = [], "", None
    for seg, linhas in cues:
        for linha in linhas:
            if linha == ultima or (ultima and ultima.endswith(linha)):
                continue
            if inicio is None or seg - inicio >= janela:
                blocos.append([seg, []])
                inicio = seg
            blocos[-1][1].append(linha)
            ultima = linha
    return "\n\n".join(f"**[{s // 60:02d}:{s % 60:02d}]** " + " ".join(ls) for s, ls in blocos)


def html_sem_tags(txt):
    return re.sub(r"<[^>]+>", "", txt).replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<").replace("&nbsp;", " ")


def url_limpa(u):
    """Guarda na nota só o link do vídeo: sem a lista (list=LL é a sua lista pessoal), o índice e o tempo."""
    pu = urllib.parse.urlparse(u)
    if "youtube.com" in pu.netloc:
        v = urllib.parse.parse_qs(pu.query).get("v", [""])[0]
        if v:
            return "https://www.youtube.com/watch?v=" + v
    return urllib.parse.urlunparse(pu._replace(query="", fragment="")) if "youtu.be" in pu.netloc else u


def _ytdlp():
    exe = shutil.which("yt-dlp")
    if exe:
        return [exe]
    try:
        import yt_dlp  # noqa: F401
        return [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        return None


def transcrever(cofre, materia, fonte, idioma="pt,en", titulo=None):
    """Grava `fontes/AAAA-MM-DD-título.md` a partir de um link de vídeo (yt-dlp) ou de um arquivo .vtt/.srt local."""
    m = resolver_materia(cofre, materia)
    if not m:
        return None, f"matéria '{materia}' não encontrada"
    hoje, origem, canal, url = datetime.date.today().isoformat(), "arquivo local", "", ""
    if re.match(r"^https?://", fonte):
        cmd = _ytdlp()
        if not cmd:
            return None, "yt-dlp não está instalado (python -m pip install --user yt-dlp)"
        url = url_limpa(fonte)
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="tutor-legenda-"))
        try:
            extra = ["--js-runtimes", "node"] if shutil.which("node") else []
            langs = [x.strip() for x in idioma.split(",") if x.strip()]
            base = cmd + extra + ["--no-playlist", "--skip-download", "--sub-format", "vtt", "--no-simulate", "--print", "TITULO=%(title)s",
                                  "--print", "CANAL=%(channel)s", "-o", str(tmp / "%(id)s.%(ext)s")]
            # 1ª passada: legenda feita por gente (manual) nos idiomas pedidos; 2ª: legenda automática original (nunca a traduzida, se houver original)
            r = subprocess.run(base + ["--write-subs", "--sub-langs", ",".join(langs), "--", fonte], stdin=subprocess.DEVNULL, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=180)
            achados = sorted(tmp.glob("*.vtt"))
            origem_tipo = "legenda manual do YouTube"
            if not achados:
                r2 = subprocess.run(base + ["--write-auto-subs", "--sub-langs", ",".join(f"{l}-orig" for l in langs) + ",.*-orig," + ",".join(langs), "--", fonte],
                                    stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
                achados, r = sorted(tmp.glob("*.vtt")), (r2 if r2.stdout else r)
                origem_tipo = "legenda automática do YouTube (original)"
            if not achados:
                return None, "o vídeo não tem legenda nos idiomas pedidos (" + idioma + ") nem legenda original; o yt-dlp disse: " + (r.stderr.strip().splitlines() or ["sem detalhe"])[-1][:200]

            def prioridade(arq):
                cod = arq.name.rsplit(".", 2)[-2]
                for i, l in enumerate(langs):
                    if cod == l or cod == l + "-orig":
                        return (0, i, cod)
                return (1, 0, cod) if cod.endswith("-orig") else (2, 0, cod)
            escolhido = min(achados, key=prioridade)
            cod = escolhido.name.rsplit(".", 2)[-2]
            corpo = vtt_para_texto(escolhido.read_text(encoding="utf-8", errors="replace"))
            origem = f"{origem_tipo}, idioma {cod.replace('-orig', '')}" + ("" if origem_tipo.startswith("legenda manual") or cod.endswith("-orig") else " (tradução automática)")
            for l in r.stdout.splitlines():
                if l.startswith("TITULO=") and not titulo:
                    titulo = l[7:].strip()
                elif l.startswith("CANAL="):
                    canal = l[6:].strip()
        except (subprocess.TimeoutExpired, OSError) as e:
            return None, f"falha ao chamar o yt-dlp: {e}"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        src = pathlib.Path(fonte).expanduser()
        if not src.is_file() or src.suffix.lower() not in (".vtt", ".srt"):
            return None, "informe um link http(s) ou um arquivo .vtt/.srt existente"
        corpo, titulo = vtt_para_texto(src.read_text(encoding="utf-8-sig", errors="replace")), titulo or src.stem
    if not corpo.strip():
        return None, "a legenda veio vazia"
    titulo = nome_limpo(titulo or "video")
    pasta = m / "fontes"
    pasta.mkdir(parents=True, exist_ok=True)
    arq, k = pasta / f"{hoje}-{slug(titulo) or 'video'}.md", 1
    while arq.exists():
        k += 1
        arq = pasta / f"{hoje}-{slug(titulo) or 'video'}-{k}.md"
    cab = (f"---\ntipo: fonte\nmateria: {slug(m.name)}\ndata: {hoje}\ntitulo: \"{titulo}\"\n" + (f"canal: \"{nome_limpo(canal)}\"\n" if canal else "")
           + (f"url: {url}\n" if url else "") + f"origem: {origem}\ntags: [{slug(m.name)}, fonte]\n---\n")
    aviso = "> [!warning] Transcrição automática\n> Serve de **pista** para estudar, não de fonte para ensinar (Regra 8): confirme os fatos na fonte oficial antes de usá-los numa aula.\n\n"
    arq.write_text(cab + f"# {titulo}\n\n" + aviso + corpo + "\n", encoding="utf-8", newline="\n")
    return arq, f"{len(corpo.split())} palavras · {origem}"


# ---------- cartões para o plugin Spaced Repetition do Obsidian ----------
def cartoes(cofre, materia, texto):
    """Acrescenta cartões 'pergunta :: resposta' em `cartoes.md` (formato do plugin Spaced Repetition). Não repete cartões."""
    m = resolver_materia(cofre, materia)
    if not m:
        return None, f"matéria '{materia}' não encontrada", 0
    novos = []
    for l in texto.split("\n"):
        l = l.strip()
        if not l:
            continue
        q, sep, a = l.partition(" :: ")
        if not sep or not q.strip() or not a.strip() or "\n" in l or " :: " in a:
            return None, f"linha inválida (use 'pergunta :: resposta', uma por linha): {l[:60]}", 0
        novos.append(f"{q.strip()}::{a.strip()}")
    arq = m / "cartoes.md"
    if not arq.exists():
        arq.write_text(f"---\ntipo: cartoes\nmateria: {slug(m.name)}\ntags: [{slug(m.name)}]\n---\n# Cartões — {nome_limpo(m.name)}\n\n#flashcards/{slug(m.name)}\n\n", encoding="utf-8", newline="\n")
    atual = _ler(arq)
    add = [c for c in novos if c not in atual]
    if add:
        with open(arq, "a", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(add) + "\n\n")
    return arq, None, len(add)


def base_sessoes(sg):
    """Painel de sessões como Base do Obsidian (recurso nativo): lista as notas de sessoes/ pelo frontmatter."""
    return ("filters:\n  and:\n    - file.inFolder(\"" + sg + "/sessoes\")\n\nformulas: {}\n\nproperties:\n  file.name:\n    displayName: \"Sessão\"\n"
            "  note.data:\n    displayName: \"Data\"\n  note.topico:\n    displayName: \"Tópico\"\n\nviews:\n  - type: table\n    name: \"Sessões\"\n"
            "    order:\n      - file.name\n      - note.data\n      - note.topico\n    summaries: {}\n")


def _template(arquivo, inicio):
    """Primeiro bloco de código depois do título que começa com `inicio` (os templates moram nas referências)."""
    linhas = _ler(RAIZ_SKILL / "references" / arquivo).split("\n")
    i = next((k for k, l in enumerate(linhas) if l.startswith(inicio)), None)
    if i is None:
        raise ValueError(f"template '{inicio}' não achado em references/{arquivo}")
    j = next((k for k in range(i + 1, len(linhas)) if re.match(r"^`{3,}markdown\s*$", linhas[k])), None)
    if j is None:
        raise ValueError(f"template '{inicio}' sem bloco markdown")
    cerca = re.match(r"^(`{3,})", linhas[j]).group(1)
    fim = next((k for k in range(j + 1, len(linhas)) if linhas[k].strip() == cerca), None)
    if fim is None:
        raise ValueError(f"template '{inicio}' com bloco aberto")
    return "\n".join(linhas[j + 1:fim]) + "\n"


def _escrever_novo(caminho, texto, criados):
    caminho = pathlib.Path(caminho)
    if caminho.exists():
        return
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8", newline="\n")
    criados.append(caminho)


def resolver_materia(cofre, nome):
    alvo = slug(nome)
    for m in sorted(p for p in pathlib.Path(cofre).iterdir() if p.is_dir() and not p.name.startswith(".")):
        if slug(m.name) == alvo and (m / "registros-da-skill").is_dir():
            return m
    return None


def _limpar_painel(texto):
    """Troca os exemplos do template do painel (trilha com 5/5, mapa de mentira) por um começo honesto."""
    nl, cerca = chr(10), "`" * 3
    saida, i, ls = [], 0, texto.split(chr(10))
    while i < len(ls):
        l = ls[i]
        if l.startswith("> [nó ou tópico]"):
            saida.append("> Fazer a entrevista e a sondagem; o plano aprovado vira a trilha aqui")
        elif l.startswith(cerca + "mermaid"):
            saida += [l, "graph TD", "  A[entrevista] --> B[sondagem] --> C[plano aprovado]", cerca]
            i += 1
            while i < len(ls) and not ls[i].startswith(cerca):
                i += 1
        elif l.startswith("- [[2026-09-30-"):
            saida.append("- (nenhuma sessão ainda)")
        elif l.startswith("## Trilha"):
            saida += [l, "- [ ] (a trilha aparece aqui depois do plano aprovado)", ""]
            i += 1
            while i < len(ls) and not ls[i].startswith("## "):
                i += 1
            continue
        else:
            saida.append(l)
        i += 1
    return nl.join(saida)


def nova_materia(cofre, nome):
    hoje = datetime.date.today().isoformat()
    nome = nome_limpo(nome)
    sg = slug(nome)
    if not sg:
        return None, ["nome de matéria inválido"]
    if sg in RESERVADOS:
        return None, [f"'{sg}' é nome reservado do Windows (não dá para apagar a pasta depois); escolha outro nome"]
    pasta = pathlib.Path(cofre) / sg
    criados = []
    try:
        _escrever_novo(pathlib.Path(cofre) / "CLAUDE.md", _template("templates.md", "### Template: `CLAUDE.md`"), criados)
        sub = lambda s: s.replace("[Nome da Matéria]", nome).replace("[Matéria]", nome).replace("[matéria]", sg)
        reg = pasta / "registros-da-skill"
        trilha = re.sub(r"\*\*Status:\*\*[^\n]*", "**Status:** rascunho", sub(_template("templates.md", "### Template: `trilha.md`")), count=1)
        progresso = sub(_template("templates.md", "### Template: `progresso.md`")).replace(
            "- Tópico / Parte / Nó / Próximo passo:", "- Tópico / Parte / Nó: —\n- Próximo passo: fazer a entrevista", 1)
        conquistas = sub(_template("projetos.md", "### Changelog de conquistas")).replace("[AAAA-MM-DD]", hoje, 1)
        painel = sub(_template("templates.md", "### Template: `_painel-[matéria].md`"))
        painel = _limpar_painel(painel).replace("## Sessões recentes\n", f"## Sessões recentes\n> Tabela com todas: [[_sessoes-{sg}.base|todas as sessões]]\n", 1)
        _escrever_novo(pasta / f"_painel-{sg}.md", painel, criados)
        _escrever_novo(pasta / f"_sessoes-{sg}.base", base_sessoes(sg), criados)
        _escrever_novo(reg / "trilha.md", trilha, criados)
        _escrever_novo(reg / "progresso.md", progresso, criados)
        _escrever_novo(reg / "conhecimento.md", sub(_template("templates.md", "### Template: `conhecimento.md`")), criados)
        _escrever_novo(reg / "conquistas.md", conquistas, criados)
        for d in ("sessoes", "pratica/projeto", "pratica/treinos", "anexos", "fontes"):
            (pasta / d).mkdir(parents=True, exist_ok=True)
        _indice(cofre, nome, sg)
    except (ValueError, OSError) as e:
        return pasta, [str(e)]
    return pasta, [f"criado: {c.relative_to(cofre).as_posix()}" for c in criados]


def _indice(cofre, nome, sg):
    """Põe a matéria no README.md do cofre (cria o README se não existir). Nunca duplica."""
    rd = pathlib.Path(cofre) / "README.md"
    if not rd.exists():
        base = _template("templates.md", "### Template: `README.md`")
        base = "\n".join(l for l in base.split("\n") if "[[_painel-[matéria]" not in l)
        rd.write_text(base, encoding="utf-8", newline="\n")
    txt = _ler(rd)
    if f"_painel-{sg}" in txt:
        return
    linha = f"- [[_painel-{sg}|{nome}]] — ▶ fazer a entrevista"
    linhas = [l for l in txt.split("\n") if not l.startswith("- (nenhuma ainda")]  # tira o marcador do índice zerado
    i = next((k for k, l in enumerate(linhas) if l.startswith("## Matérias ativas")), None)
    if i is None:
        linhas += ["", "## Matérias ativas", linha]
    else:
        linhas.insert(i + 1, linha)
    rd.write_text("\n".join(linhas), encoding="utf-8", newline="\n")


def nota_sessao(cofre, materia, titulo, corpo, topico="", resumo=""):
    m = resolver_materia(cofre, materia)
    if not m:
        return None, f"matéria '{materia}' não encontrada (rode nova-materia antes)"
    hoje = datetime.date.today().isoformat()
    arq = m / "sessoes" / f"{hoje}-{slug(titulo) or 'sessao'}.md"
    arq.parent.mkdir(parents=True, exist_ok=True)
    corpo = corpo.replace("\r\n", "\n").strip("\n") + "\n"
    if arq.exists():
        with open(arq, "a", encoding="utf-8", newline="\n") as f:
            f.write(f"\n---\n## Acrescentado às {datetime.datetime.now().strftime('%H:%M')}\n{corpo}")
    else:
        cab = f"---\ntipo: sessao\nmateria: {slug(m.name)}\ndata: {hoje}\n" + (f"topico: {topico}\n" if topico else "") + f"tags: [{slug(m.name)}, sessao]\n---\n"
        arq.write_text(cab + (corpo if corpo.lstrip().startswith("#") else f"# Sessão {hoje} — {titulo}\n\n{corpo}"), encoding="utf-8", newline="\n")
    painel = m / f"_painel-{slug(m.name)}.md"
    if painel.is_file():
        ln = f"- [[{arq.stem}]]" + (f" — {resumo}" if resumo else "")
        ls = _ler(painel).split("\n")
        i = next((k for k, l in enumerate(ls) if l.startswith("## Sessões recentes")), None)
        if i is not None and not any(f"[[{arq.stem}]]" in l for l in ls):
            j = i + 1
            while j < len(ls) and not ls[j].startswith("#"):
                j += 1
            bloco = [l for l in ls[i + 1:j] if "[[2026-09-30-tópico]]" not in l and "[[AAAA" not in l and "nenhuma sessão ainda" not in l]
            topo = 0
            while topo < len(bloco) and (bloco[topo].startswith(">") or not bloco[topo].strip()):
                topo += 1
            bloco.insert(topo, ln)
            auto = [k for k, l in enumerate(bloco) if re.match(r"^- \[\[\d{4}-\d{2}-\d{2}-", l)]
            for k in reversed(auto[8:]):  # só as 8 mais recentes ficam no painel; linhas escritas à mão nunca saem
                del bloco[k]
            while bloco and not bloco[-1].strip():
                bloco.pop()
            ls[i + 1:j] = bloco + [""]
            painel.write_text("\n".join(ls), encoding="utf-8", newline="\n")
    return arq, None


def _area_de_transferencia(destino):
    """Salva a imagem da área de transferência em `destino` (.png). Testado no Windows; macOS e Linux dependem de pngpaste / wl-paste / xclip."""
    destino = pathlib.Path(destino)
    if sys.platform.startswith("win"):
        ps = ("Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; "
              "$i=[System.Windows.Forms.Clipboard]::GetImage(); if($i){$i.Save($env:TUTOR_DEST,[System.Drawing.Imaging.ImageFormat]::Png);'ok'}else{'vazio'}")
        r = subprocess.run(["powershell", "-NoProfile", "-STA", "-Command", ps], capture_output=True, text=True, timeout=30,
                           env=dict(os.environ, TUTOR_DEST=str(destino)))
        return "ok" in r.stdout and destino.is_file()
    cmds = []
    if sys.platform == "darwin" and shutil.which("pngpaste"):
        cmds = [["pngpaste", str(destino)]]
    elif shutil.which("wl-paste"):
        cmds = [["wl-paste", "--type", "image/png"]]
    elif shutil.which("xclip"):
        cmds = [["xclip", "-selection", "clipboard", "-t", "image/png", "-o"]]
    for c in cmds:
        r = subprocess.run(c, capture_output=True, timeout=30)
        if c[0] != "pngpaste" and r.returncode == 0 and r.stdout:
            destino.write_bytes(r.stdout)
        if destino.is_file() and destino.stat().st_size > 0:
            return True
    return False


def anexar(cofre, materia, origem, nome=None):
    m = resolver_materia(cofre, materia)
    if not m:
        return None, f"matéria '{materia}' não encontrada"
    pasta = m / "anexos"
    pasta.mkdir(parents=True, exist_ok=True)
    hoje = datetime.date.today().isoformat()
    if origem is None:
        ext, base = ".png", slug(nome or "colagem")
    else:
        src = pathlib.Path(origem).expanduser()
        if not src.is_file():
            return None, f"arquivo '{origem}' não existe"
        ext, base = src.suffix.lower(), slug(nome or src.stem)
        if ext not in IMAGENS:
            return None, f"extensão '{ext}' não aceita (use {', '.join(IMAGENS)})"
    k, destino = 1, pasta / f"{hoje}-{base}{ext}"
    while destino.exists():
        k += 1
        destino = pasta / f"{hoje}-{base}-{k}{ext}"
    if origem is None:
        if not _area_de_transferencia(destino):
            return None, "não há imagem na área de transferência (ou este sistema não tem pngpaste, wl-paste ou xclip)"
    else:
        shutil.copyfile(src, destino)
    return destino, None


def uri_obsidian(cofre, alvo=None):
    q = "obsidian://open?vault=" + urllib.parse.quote(pathlib.Path(cofre).name, safe="")
    if alvo:
        q += "&file=" + urllib.parse.quote(re.sub(r"\.md$", "", pathlib.Path(alvo).as_posix()), safe="")
    return q


def abrir_uri(uri):
    if sys.platform.startswith("win"):
        os.startfile(uri)  # noqa
    else:
        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", uri], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def status_linha(cofre):
    hoje = datetime.date.today()
    partes = []
    for m in materias(cofre):
        try:
            _, total = fila.vencidos(m / "registros-da-skill" / "conhecimento.md", hoje, 3)
        except (ValueError, OSError):
            continue
        if total:
            partes.append(f"{m.name}: {total}")
    return ("estudo: " + " · ".join(partes) + " p/ revisar") if partes else ""


def _opcao(args, nome):
    return args[args.index(nome) + 1] if nome in args and args.index(nome) + 1 < len(args) else None


def main(argv):
    _utf8()
    if not argv or argv[0] not in ("achar", "resumo", "status", "validar", "diario", "nova-materia", "nota", "anexar", "abrir", "transcrever", "cartoes"):
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "diario":
        return diario_hook() if "--hook" in args else 2
    cofre = achar(explicito=_opcao(args, "--cofre"))
    if cmd == "nova-materia":
        if not args or args[0].startswith("--"):
            print("uso: cofre.py nova-materia NOME [--cofre CAMINHO]")
            return 2
        raiz = cofre or (pathlib.Path(_opcao(args, "--cofre")).expanduser() if _opcao(args, "--cofre") else None)
        if not raiz or not raiz.is_dir():
            print("ERRO: cofre não encontrado. Passe --cofre CAMINHO (a pasta do cofre Obsidian).")
            return 1
        pasta, msgs = nova_materia(raiz, args[0])
        for m_ in msgs:
            print(m_)
        if pasta is None or not (pasta / "registros-da-skill").is_dir():
            return 1
        prob = [x for x in validar(raiz) if x.startswith(pasta.name + ":")]
        print("VALIDACAO: " + ("ok" if not prob else "; ".join(prob)))
        return 1 if prob else 0
    if cmd in ("nota", "anexar", "abrir", "status", "transcrever", "cartoes") and not cofre:
        return 0 if cmd == "status" else 1
    if cmd == "status":
        print(status_linha(cofre))
        return 0
    if cmd == "nota":
        pos_ = [a for a in args if not a.startswith("--")]
        vals = {args[i + 1] for i, a in enumerate(args[:-1]) if a.startswith("--")}
        pos_ = [a for a in pos_ if a not in vals]
        if len(pos_) < 2:
            print('uso: cofre.py nota MATERIA TITULO [--topico t1] [--resumo "..."]  (corpo no stdin)')
            return 2
        arq, erro = nota_sessao(cofre, pos_[0], pos_[1], ler_entrada(args), _opcao(args, "--topico") or "", _opcao(args, "--resumo") or "")
        print(f"ERRO: {erro}" if erro else f"NOTA: {arq.relative_to(cofre).as_posix()}\nLINK: [[{arq.stem}]]")
        return 1 if erro else 0
    if cmd in ("transcrever", "cartoes"):
        pos_ = [a for a in args if not a.startswith("--")]
        vals = {args[i + 1] for i, a in enumerate(args[:-1]) if a.startswith("--")}
        pos_ = [a for a in pos_ if a not in vals]
        if cmd == "transcrever":
            if len(pos_) < 2:
                print('uso: cofre.py transcrever MATERIA LINK_OU_ARQUIVO.vtt [--idioma pt,en] [--titulo "..."]')
                return 2
            arq, info = transcrever(cofre, pos_[0], pos_[1], _opcao(args, "--idioma") or "pt,en", _opcao(args, "--titulo"))
            print(f"FONTE: {arq.relative_to(cofre).as_posix()}\nLINK: [[{arq.stem}]]\nINFO: {info}" if arq else f"ERRO: {info}")
            return 0 if arq else 1
        if not pos_:
            print("uso: cofre.py cartoes MATERIA   (linhas 'pergunta :: resposta' no stdin ou em --arquivo)")
            return 2
        arq, erro, n = cartoes(cofre, pos_[0], ler_entrada(args))
        print(f"ERRO: {erro}" if erro else f"CARTOES: {arq.relative_to(cofre).as_posix()} (+{n} novo(s))")
        return 1 if erro else 0
    if cmd == "anexar":
        pos_ = [a for a in args if not a.startswith("--")]
        vals = {args[i + 1] for i, a in enumerate(args[:-1]) if a.startswith("--")}
        pos_ = [a for a in pos_ if a not in vals]
        clip = "--area-de-transferencia" in args
        if not pos_ or (not clip and len(pos_) < 2):
            print("uso: cofre.py anexar MATERIA ORIGEM [--nome X]   ou   cofre.py anexar MATERIA --area-de-transferencia [--nome X]")
            return 2
        dest, erro = anexar(cofre, pos_[0], None if clip else pos_[1], _opcao(args, "--nome"))
        print(f"ERRO: {erro}" if erro else f"ARQUIVO: {dest.relative_to(cofre).as_posix()}\nEMBED: ![[{dest.name}]]")
        return 1 if erro else 0
    if cmd == "abrir":
        pos_ = [a for a in args if not a.startswith("--") and a != _opcao(args, "--cofre")]
        alvo = None
        if pos_:
            m = resolver_materia(cofre, pos_[0])
            if not m:
                print(f"ERRO: matéria '{pos_[0]}' não encontrada")
                return 1
            alvo = (m / pos_[1]).relative_to(cofre) if len(pos_) > 1 else (m / f"_painel-{slug(m.name)}.md").relative_to(cofre)
        uri = uri_obsidian(cofre, alvo)
        print(f"URI: {uri}\n(o nome do cofre no Obsidian precisa ser '{cofre.name}'; confira em Gerenciar cofres)")
        if "--imprimir" not in args:
            abrir_uri(uri)
        return 0
    if cmd == "achar":
        print(cofre if cofre else "nenhum cofre encontrado")
        return 0 if cofre else 1
    if not cofre:
        return 0 if "--hook" in args else 1
    if cmd == "resumo":
        texto = resumo(cofre)
        if "--hook" in args:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": texto}}, ensure_ascii=False))
        else:
            print(texto)
        return 0
    prob = validar(cofre)
    print("VALIDACAO: " + ("ok, nenhum problema" if not prob else f"{len(prob)} problema(s)"))
    for p in prob:
        print(f"  - {p}")
    return 1 if prob else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
