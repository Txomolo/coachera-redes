# ============================================================================
# Una locución larga (varios Reels seguidos) → un WAV por Reel y el segundo de cada frase
# ============================================================================
#   python3 motor/alinear.py voz.wav reels/cortos-principios.json salida/voz-cortos/
#
# Para las voces que no se generan aquí (las de Google AI Studio, desde el 18-oct-2026): se
# pide de una vez la locución de todos los Reels de una serie, se descarga y este script la
# parte. Corta por los silencios, transcribe cada trozo con Whisper (sherpa-onnx, en local) y
# casa lo transcrito con el guion para saber dónde empieza cada frase.
#   → <salida>/<nombre>.wav               la voz de ese Reel, empezando a los ANTES segundos
#   → <salida>/<nombre>.tiempos.json      [{texto, marca, t, fin}] en segundos de ese WAV
# El guion: {"reels": [{"nombre": …, "voz": [{"texto": …, "marca": …}, …]}, …]}
# Whisper: WHISPER=<carpeta de sherpa-onnx-whisper-base> (tts-models no; asr-models en GitHub).
import difflib, json, os, re, sys, unicodedata, wave
import numpy as np
from scipy.signal import resample_poly

SR = 48000
ANTES, DESPUES = 0.12, 0.35
WHISPER = os.environ.get("WHISPER", "")

def leer(ruta):
    with wave.open(ruta) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype={2: "<i2", 4: "<i4"}[sw]).astype(float) / (2 ** (8 * sw - 1))
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    return resample_poly(x, SR, sr) if sr != SR else x

def trozos(x, min_sil=0.12):
    """Los tramos con voz, cortando en los silencios de al menos min_sil segundos."""
    w = int(SR * 0.01)
    env = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, "same"))[::w]
    umbral = max(env.max() * 0.025, np.percentile(env, 10) * 3)
    voz = env > umbral
    tramos, i, n = [], 0, len(voz)
    while i < n:
        if voz[i]:
            j = i
            while j < n and (voz[j] or (j + int(min_sil * 100) < n and voz[j:j + int(min_sil * 100)].any())):
                j += 1
            tramos.append([i / 100, j / 100]); i = j
        else:
            i += 1
    return [t for t in tramos if t[1] - t[0] >= 0.12]

def reconocedor():
    import sherpa_onnx
    d = WHISPER
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=os.path.join(d, "base-encoder.int8.onnx"), decoder=os.path.join(d, "base-decoder.int8.onnx"),
        tokens=os.path.join(d, "base-tokens.txt"), language="es", task="transcribe", num_threads=4)

def transcribir(rec, x):
    s = rec.create_stream()
    y = resample_poly(np.pad(x, int(0.15 * SR)), 16000, SR).astype(np.float32)
    s.accept_waveform(16000, y)
    rec.decode_stream(s)
    return s.result.text.strip()

UNIDADES = {"cero": "0", "uno": "1", "una": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9"}
def palabras(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"(\d)[.,](\d)", r"\1\2", t)
    return [UNIDADES.get(p, p) for p in re.findall(r"[a-zñ]+|\d+", t)]

def letras(t):
    """Solo letras y cifras, sin tildes: se casa letra a letra, así «guarda lo» = «guárdalo»."""
    return "".join(palabras(t))

def alinear(x, guion, rec, verbose=True):
    ts = trozos(x)
    # lo transcrito, letra a letra, con el tramo del que sale y su posición en el tramo
    oido = []
    for k, (a, b) in enumerate(ts):
        txt = transcribir(rec, x[int(a * SR):int(b * SR)])
        ls = letras(txt)
        if verbose: print(f"  {a:6.2f}–{b:6.2f}  {txt}")
        oido += [(c, k, i, len(ls)) for i, c in enumerate(ls)]
    # el guion, letra a letra; cada frase es un tramo [ini, fin) de esa cadena
    escrito, rangos = [], []
    for reel in guion["reels"]:
        rr = []
        for l in reel["voz"]:
            ls = letras(l["texto"]); rr.append((len(escrito), len(escrito) + len(ls))); escrito += list(ls)
        rangos.append(rr)
    sm = difflib.SequenceMatcher(None, "".join(o[0] for o in oido), "".join(escrito), autojunk=False)
    casa = {}
    for blk in sm.get_matching_blocks():
        if blk.size < 3: continue        # una o dos letras sueltas casan por azar («Cuárt» con «sesenTa»)
        for d in range(blk.size): casa[blk.b + d] = blk.a + d
    def segundo(j, inicio):
        p, k, i, n = oido[casa[j]]
        a, b = ts[k]
        return a + (b - a) * (i if inicio else i + 1) / max(1, n), k
    # los tramos donde Whisper oyó algo que casa con el guion: lo que falta por casar al principio
    # o al final de una frase no se puede ir a uno de esos (sería la frase de al lado; pasó el
    # 21-oct: «61.000 personas» no casa con «Sesenta y un mil personas» y el principio de la
    # frase se iba hasta el «Guárdalo» del reel anterior)
    usados = {oido[a][1] for a in casa.values()}
    planas = []           # todas las frases en orden, con t/fin si se pudieron casar
    for r, reel in enumerate(guion["reels"]):
        for f, l in enumerate(reel["voz"]):
            i0, i1 = rangos[r][f]
            dentro = [j for j in range(i0, i1) if j in casa]
            fr = {"r": r, "texto": l["texto"], "marca": l.get("marca"), "t": None, "fin": None, "k0": None, "k1": None}
            if len(dentro) >= max(2, (i1 - i0) // 5):
                t0, k0 = segundo(dentro[0], True); t1, k1 = segundo(dentro[-1], False)
                # lo que falta por casar al principio o al final se reparte a velocidad media
                vel = max(1e-3, (t1 - t0) / max(1, dentro[-1] - dentro[0] + 1))
                t0 -= (dentro[0] - i0) * vel; t1 += (i1 - 1 - dentro[-1]) * vel
                # hacia atrás, al tramo de antes solo si está libre y la frase anterior se casó (si
                # no, ese tramo es suyo: se lo dará el relleno de abajo); hacia delante, nunca
                ant = planas[-1] if planas else None
                libre = k0 > 0 and k0 - 1 not in usados and (ant is None or (ant["k1"] is not None and ant["k1"] < k0 - 1))
                if t0 < ts[k0][0]: t0, k0 = (max(t0, ts[k0 - 1][0]), k0 - 1) if libre else (ts[k0][0], k0)
                t1 = min(t1, ts[k1][1])
                # si cae cerca del borde de un tramo, a ese borde: ahí está la pausa
                if abs(t0 - ts[k0][0]) < 0.45: t0 = ts[k0][0]
                if abs(t1 - ts[k1][1]) < 0.45: t1 = ts[k1][1]
                fr.update(t=t0, fin=t1, k0=k0, k1=k1)
            planas.append(fr)
    # las que no se casaron (Whisper la entendió mal): los tramos que quedan entre sus vecinas
    for n, fr in enumerate(planas):
        if fr["t"] is not None: continue
        ant = next((p for p in reversed(planas[:n]) if p["k1"] is not None), None)
        sig = next((p for p in planas[n + 1:] if p["k0"] is not None), None)
        k0 = ant["k1"] + 1 if ant else 0
        k1 = sig["k0"] - 1 if sig else len(ts) - 1
        if k1 < k0: k1 = k0
        fr.update(t=ts[k0][0], fin=ts[k1][1], k0=k0, k1=k1)
        if verbose: print(f"  ! sin casar, por los tramos de alrededor: «{fr['texto']}» {fr['t']:.2f}–{fr['fin']:.2f}")
    salida = [[] for _ in guion["reels"]]
    for fr in planas:
        salida[fr["r"]].append({"texto": fr["texto"], "marca": fr["marca"], "t": fr["t"], "fin": fr["fin"]})
    return salida, ts

def main():
    voz, ruta_guion, carpeta = sys.argv[1:4]
    guion = json.load(open(ruta_guion, encoding="utf-8"))
    x = leer(voz)
    rec = reconocedor()
    todo, ts = alinear(x, guion, rec)
    os.makedirs(carpeta, exist_ok=True)
    for reel, frases in zip(guion["reels"], todo):
        a = frases[0]["t"] - ANTES; b = frases[-1]["fin"] + DESPUES
        trozo = x[max(0, int(a * SR)):int(b * SR)]
        trozo = trozo / (np.abs(trozo).max() + 1e-9) * 0.7
        with wave.open(os.path.join(carpeta, reel["nombre"] + ".wav"), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((trozo * 32767).astype("<i2").tobytes())
        tiempos = [{**f, "t": round(f["t"] - a, 2), "fin": round(f["fin"] - a, 2)} for f in frases]
        json.dump(tiempos, open(os.path.join(carpeta, reel["nombre"] + ".tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{reel['nombre']}: {b - a:.1f} s")
        for f in tiempos: print(f"   {f['t']:5.2f}–{f['fin']:5.2f}  {f['marca'] or '':8} {f['texto'][:60]}")

if __name__ == "__main__":
    main()
