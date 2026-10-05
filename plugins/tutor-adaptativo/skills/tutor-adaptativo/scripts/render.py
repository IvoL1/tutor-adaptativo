#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renderiza Mermaid e SVG em PNG e valida a sintaxe, usando o navegador já instalado (Edge/Chrome).

  render.py detectar
  render.py mermaid ENTRADA.mmd SAIDA.png [--mermaid-js URL_OU_CAMINHO]
  render.py svg     ENTRADA.svg SAIDA.png

Responde com uma linha JSON: {"ok": true, "png": ..., "largura": ..., "altura": ...} ou {"ok": false, "erro": ...}.
Mermaid 11.17.2 é carregado de cdn.jsdelivr.net, com versão fixa e SRI (precisa de rede); use --mermaid-js com um arquivo local para funcionar offline.
Se o Mermaid acusar erro, "erro" traz a mensagem exata de sintaxe e nenhum PNG é criado.
Funciona com Edge e Chrome: o resultado volta por um servidor local efêmero (127.0.0.1), não por pipes.
O tamanho da imagem é corrigido pelo que o navegador realmente entrega (no Linux a janela "headless=new" vem ~88 px mais baixa que a pedida).
Como root (contêiner), o navegador sobe com --no-sandbox.
"""
import html, http.server, json, os, pathlib, re, shutil, struct, subprocess, sys, tempfile, threading, time, urllib.parse, zlib
import xml.etree.ElementTree as ET

CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.min.js"  # versão exata + SRI: o navegador recusa um arquivo adulterado
CDN_SRI = "sha384-EOXBFmc3gx5mb+vn0vPvvGqACToJD24hhacX5Yx+8NUUQrHIle/Qi5Bg9o3zKwW2"
GIF = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def navegador():
    forcado = os.environ.get("TUTOR_NAVEGADOR")  # caminho de um navegador, para forçar Edge ou Chrome
    if forcado and pathlib.Path(forcado).is_file():
        return forcado
    cand = []
    if sys.platform.startswith("win"):
        for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA")):
            if base:
                cand += [pathlib.Path(base) / r"Google\Chrome\Application\chrome.exe",
                         pathlib.Path(base) / r"Microsoft\Edge\Application\msedge.exe"]
    elif sys.platform == "darwin":
        cand += [pathlib.Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                 pathlib.Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")]
    for nome in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome"):
        w = shutil.which(nome)
        if w:
            cand.append(pathlib.Path(w))
    return next((str(p) for p in cand if p.is_file()), None)


def detectar():
    return {"navegador": navegador(), "mmdc": shutil.which("mmdc"), "rsvg-convert": shutil.which("rsvg-convert"),
            "magick": shutil.which("magick"), "python": sys.version.split()[0]}


def _matar(p):
    if sys.platform.startswith("win"):
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        p.kill()


def _lancar(nav, url, perfil, extra):
    """Abre o navegador sem pipes (pipes herdados pelos filhos travam no Windows)."""
    cmd = [nav, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
           "--force-device-scale-factor=1", f"--user-data-dir={perfil}"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:  # root (contêiner): o sandbox do Chrome não sobe; o conteúdo é local ou tem SRI
        cmd.append("--no-sandbox")
    cmd += extra + [url]
    return subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _esperar_png(png, timeout=45):
    """O Edge entrega o trabalho a outro processo e sai logo: por isso esperamos pelo arquivo, não pelo processo."""
    fim, ultimo = time.time() + timeout, -1
    png = pathlib.Path(png)
    while time.time() < fim:
        if png.is_file():
            tam = png.stat().st_size
            if tam > 1000 and tam == ultimo:
                return True
            ultimo = tam
        time.sleep(0.4)
    return png.is_file() and png.stat().st_size > 1000


def _encerrar(p, marcador):
    """Garante que nenhum navegador desta execução fique vivo (o marcador está no caminho do perfil temporário)."""
    try:
        p.wait(timeout=4)
    except subprocess.TimeoutExpired:
        _matar(p)
    if sys.platform.startswith("win"):
        ps = f"Get-CimInstance Win32_Process -Filter \"CommandLine like '%{marcador}%'\" | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }}"
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
    else:
        subprocess.run(["pkill", "-f", marcador], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _sessao(nav, url, extra, espera=None, timeout=45):
    """Abre o navegador num perfil temporário, espera (evento da página e/ou PNG) e limpa tudo."""
    marcador = "tutor-render-" + os.urandom(4).hex()
    perfil = pathlib.Path(tempfile.gettempdir()) / marcador
    p = _lancar(nav, url, perfil, extra)
    try:
        if espera is not None:
            espera.wait(timeout)
        png = next((a.split("=", 1)[1] for a in extra if a.startswith("--screenshot=")), None)
        return _esperar_png(png, timeout) if png else True
    finally:
        _encerrar(p, marcador)
        shutil.rmtree(perfil, ignore_errors=True)


def _png_ok(p):
    return pathlib.Path(p).is_file() and pathlib.Path(p).stat().st_size > 1000


def _servidor(pagina, js_bytes=None):
    est = {"ev": threading.Event(), "res": {}}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _enviar(self, corpo, tipo):
            self.send_response(200)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            if u.path == "/":
                self._enviar(pagina.encode("utf-8"), "text/html; charset=utf-8")
            elif u.path == "/m.js" and js_bytes is not None:  # Mermaid local: uma página http não pode carregar file://
                self._enviar(js_bytes, "application/javascript; charset=utf-8")
            elif u.path == "/espera":  # segura o evento load até a página avisar que terminou de desenhar
                est["ev"].wait(25)
                self._enviar(GIF, "image/gif")
            elif u.path == "/r":
                est["res"] = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
                est["ev"].set()
                self._enviar(GIF, "image/gif")
            else:
                self.send_error(404)

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, est


def _recortar_png(caminho, w, h):
    """Recorta o PNG para w x h (canto superior esquerdo), só com a biblioteca padrão. Devolve (largura, altura) finais.
    Aceita PNG de 8 bits, RGB ou RGBA, sem entrelaçamento (o que o Chrome e o Edge geram); em qualquer outro caso deixa o arquivo como está."""
    caminho = pathlib.Path(caminho)
    try:
        dados = caminho.read_bytes()
        if dados[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        pos, idat, ihdr = 8, [], None
        while pos < len(dados):
            n, tipo = struct.unpack(">I4s", dados[pos:pos + 8])
            corpo = dados[pos + 8:pos + 8 + n]
            if tipo == b"IHDR":
                ihdr = struct.unpack(">IIBBBBB", corpo)
            elif tipo == b"IDAT":
                idat.append(corpo)
            pos += 12 + n
        W, H, prof, cor, _, _, entrel = ihdr
        if prof != 8 or cor not in (2, 6) or entrel:
            return None
        if W <= w and H <= h:
            return W, H
        w, h = min(w, W), min(h, H)
        bpp = 3 if cor == 2 else 4
        stride = W * bpp
        bruto = zlib.decompress(b"".join(idat))
        linhas, ant = [], bytearray(stride)
        for y in range(H):
            f, lin = bruto[y * (stride + 1)], bytearray(bruto[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
            for i in range(stride):
                a = lin[i - bpp] if i >= bpp else 0
                b, c = ant[i], (ant[i - bpp] if i >= bpp else 0)
                if f == 1:
                    lin[i] = (lin[i] + a) & 255
                elif f == 2:
                    lin[i] = (lin[i] + b) & 255
                elif f == 3:
                    lin[i] = (lin[i] + ((a + b) >> 1)) & 255
                elif f == 4:
                    pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                    lin[i] = (lin[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
            linhas.append(lin)
            ant = lin
            if y + 1 == h:
                break
        novo = b"".join(b"\x00" + bytes(l[:w * bpp]) for l in linhas)
        def chunk(tp, c):
            return struct.pack(">I", len(c)) + tp + c + struct.pack(">I", zlib.crc32(tp + c) & 0xffffffff)
        saida = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, cor, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(novo, 9)) + chunk(b"IEND", b""))
        caminho.write_bytes(saida)
        return w, h
    except (OSError, ValueError, struct.error, zlib.error, IndexError, TypeError):
        return None


def _folga(nav):
    """Quanto a janela real vem menor que a pedida: (dx, dy). Zero onde o navegador respeita --window-size."""
    pagina = ('<!doctype html><meta charset="utf-8"><body><script>'
              'new Image().src="/r?w="+innerWidth+"&h="+innerHeight;</script>')
    srv, est = _servidor(pagina)
    try:
        _sessao(nav, f"http://127.0.0.1:{srv.server_address[1]}/", ["--window-size=800,600"], espera=est["ev"], timeout=20)
        r = est["res"]
        return max(0, 800 - int(r.get("w", 800))), max(0, 600 - int(r.get("h", 600)))
    except (ValueError, OSError):
        return 0, 0
    finally:
        srv.shutdown()


def _pagina_mermaid(codigo, js):
    return ('<!doctype html><meta charset="utf-8"><body style="margin:16px;background:#fff">'
            f'<textarea id="c" hidden>{html.escape(codigo)}</textarea><div id="d"></div>'
            f'<script src="{js or CDN}"' + ('' if js else f' integrity="{CDN_SRI}" crossorigin="anonymous"') + '></script><script>'
            'var i=new Image();i.style.display="none";i.src="/espera";document.body.appendChild(i);'
            'mermaid.initialize({startOnLoad:false,securityLevel:"strict"});'
            '(async()=>{var q="";try{var c=document.getElementById("c").value;await mermaid.parse(c);'
            'var r=await mermaid.render("g1",c);var d=document.getElementById("d");d.innerHTML=r.svg;'
            'var b=d.querySelector("svg").getBoundingClientRect();q="ok=1&w="+Math.ceil(b.width)+"&h="+Math.ceil(b.height);}'
            'catch(e){q="erro="+encodeURIComponent(String((e&&e.message)||e));}'
            'new Image().src="/r?"+q;})();</script>')


def mermaid(entrada, saida, js):
    codigo = pathlib.Path(entrada).read_text(encoding="utf-8")
    nav = navegador()
    if not nav:
        mmdc = shutil.which("mmdc")
        if mmdc:
            r = subprocess.run([mmdc, "-i", str(entrada), "-o", str(saida)], capture_output=True, text=True, timeout=120)
            return {"ok": r.returncode == 0 and _png_ok(saida), "png": str(saida), "renderizador": "mmdc", "erro": r.stderr[-400:] if r.returncode else ""}
        return {"ok": False, "erro": "sem navegador (Edge/Chrome) nem mmdc; só dá para verificar por leitura"}
    js_bytes = None
    if js and not re.match(r"https?://", js):
        arq_js = pathlib.Path(js).expanduser()
        if not arq_js.is_file():
            return {"ok": False, "erro": f"--mermaid-js: o arquivo '{js}' não existe"}
        js_bytes, js = arq_js.read_bytes(), "/m.js"
    dx, dy = _folga(nav)
    srv, est = _servidor(_pagina_mermaid(codigo, js), js_bytes)
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    try:
        medida = pathlib.Path(tempfile.gettempdir()) / ("tutor-medida-" + os.urandom(4).hex() + ".png")
        _sessao(nav, url, [f"--screenshot={medida}", f"--window-size={1800 + dx},{1400 + dy}"], espera=est["ev"])
        try:
            medida.unlink()
        except OSError:
            pass
        res = dict(est["res"])
        if "erro" in res:
            return {"ok": False, "erro": "sintaxe inválida: " + res["erro"].strip()[:600]}
        if res.get("ok") != "1":
            return {"ok": False, "erro": "o Mermaid não carregou (sem rede? use --mermaid-js com um arquivo local)"}
        w, h = min(int(res["w"]) + 40, 4000), min(int(res["h"]) + 40, 4000)
        est["ev"].clear()
        est["res"].clear()
        destino = pathlib.Path(saida).resolve()
        if destino.exists():
            destino.unlink()
        _sessao(nav, url, [f"--screenshot={destino}", f"--window-size={w + dx},{h + dy}"], espera=est["ev"])
    finally:
        srv.shutdown()
    ok = _png_ok(saida)
    if ok and (dx or dy):
        w, h = _recortar_png(saida, w, h) or (w, h)
    return {"ok": ok, "png": str(pathlib.Path(saida).resolve()), "largura": w, "altura": h, "renderizador": pathlib.Path(nav).name,
            **({} if ok else {"erro": "o navegador não gerou o PNG"})}


def svg(entrada, saida):
    texto = pathlib.Path(entrada).read_text(encoding="utf-8")
    try:
        raiz = ET.fromstring(texto)
    except ET.ParseError as e:
        return {"ok": False, "erro": f"SVG inválido (XML): {e}"}
    if not raiz.tag.endswith("svg"):
        return {"ok": False, "erro": "a raiz do arquivo não é <svg>"}
    m = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', texto)
    w, h = (int(float(m.group(1))), int(float(m.group(2)))) if m else (900, 600)
    nums = [re.match(r"[\d.]+", raiz.get(k) or "") for k in ("width", "height")]
    if all(nums):
        w, h = int(float(nums[0].group())), int(float(nums[1].group()))
    w, h = min(w, 4000), min(h, 4000)
    nav = navegador()
    if nav:
        destino = pathlib.Path(saida).resolve()
        if destino.exists():
            destino.unlink()
        arq = pathlib.Path(tempfile.gettempdir()) / ("tutor-svg-" + os.urandom(4).hex() + ".html")
        corpo = re.sub(r"^<\?xml[^>]*\?>", "", texto).strip()
        arq.write_text('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fff">' + corpo, encoding="utf-8")
        try:
            dx, dy = _folga(nav)
            _sessao(nav, arq.as_uri(), [f"--screenshot={destino}", f"--window-size={w + dx},{h + dy}"])
        finally:
            try:
                arq.unlink()
            except OSError:
                pass
        if _png_ok(saida) and (dx or dy):
            w, h = _recortar_png(saida, w, h) or (w, h)
        return {"ok": _png_ok(saida), "png": str(destino), "largura": w, "altura": h, "renderizador": pathlib.Path(nav).name}
    for exe, cmd in (("rsvg-convert", ["rsvg-convert", "-o", str(saida), str(entrada)]), ("magick", ["magick", str(entrada), str(saida)])):
        if shutil.which(exe):
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {"ok": r.returncode == 0 and _png_ok(saida), "png": str(saida), "renderizador": exe, "erro": r.stderr[-300:] if r.returncode else ""}
    return {"ok": False, "erro": "sem navegador, rsvg-convert nem magick; o XML está válido, mas só dá para verificar por leitura"}


def main(argv):
    _utf8()
    if not argv or argv[0] not in ("detectar", "mermaid", "svg"):
        print(__doc__)
        return 2
    if argv[0] == "detectar":
        print(json.dumps(detectar(), ensure_ascii=False))
        return 0
    if len(argv) < 3:
        print(__doc__)
        return 2
    js = argv[argv.index("--mermaid-js") + 1] if "--mermaid-js" in argv else None
    r = mermaid(argv[1], argv[2], js) if argv[0] == "mermaid" else svg(argv[1], argv[2])
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
