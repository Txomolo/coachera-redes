# ============================================================================
# La voz en off de los Reels, generada (sin grabar a nadie)
# ============================================================================
#   python3 motor/voz.py reel.json salida.wav
#
# reel.json es el window.REEL de la página, con:
#   voz: { modelo: "es_ES-sharvard-medium", hablante: 1, velocidad: 1.0,
#          lineas: [{ t: 0.15, texto: "¿Cuántas apps...?", hasta: 2.8 }] }
#   duracion
# Cada línea empieza en su segundo t; si no cabe antes de "hasta" (o de la siguiente línea),
# se dice un poco más rápido (hasta un 15 %) para que entre.
#
# Las voces son modelos libres (Piper, VITS) que corren aquí con sherpa-onnx, sin enviar el
# texto a ningún servicio. Se descargan una vez de las versiones de sherpa-onnx en GitHub:
#   https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-<modelo>.tar.bz2
# a la carpeta de VOCES (por defecto motor/voces, que no se versiona: pesan ~90 MB cada una).
# OJO: en Instagram, un Reel con esta voz se publica con isAiGenerated = true.
import json, os, sys
import numpy as np
from scipy.signal import resample_poly, butter, lfilter

SR = 48000
AQUI = os.path.dirname(os.path.abspath(__file__))
VOCES = os.environ.get("VOCES", os.path.join(AQUI, "voces"))

def motor_tts(modelo):
    import sherpa_onnx
    if modelo == "kokoro":
        # Kokoro v1.0 (multilingüe): en español, 28 = ef_dora (mujer), 29 = em_alex y 53 = em_santa (hombres)
        d = os.path.join(VOCES, "kokoro-multi-lang-v1_0")
        if not os.path.isdir(d):
            sys.exit(f"Falta Kokoro en {d}: tts-models/kokoro-multi-lang-v1_0.tar.bz2 (ver la cabecera)")
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=os.path.join(d, "model.onnx"), voices=os.path.join(d, "voices.bin"),
                    tokens=os.path.join(d, "tokens.txt"), data_dir=os.path.join(d, "espeak-ng-data"), lang="es"),
                num_threads=4),
            max_num_sentences=1)
        return sherpa_onnx.OfflineTts(cfg)
    d = os.path.join(VOCES, f"vits-piper-{modelo}")
    if not os.path.isdir(d):
        sys.exit(f"Falta la voz {modelo}: descárgala en {d} (ver la cabecera de motor/voz.py)")
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=os.path.join(d, f"{modelo}.onnx"), tokens=os.path.join(d, "tokens.txt"), data_dir=os.path.join(d, "espeak-ng-data")),
            num_threads=4),
        max_num_sentences=1)
    return sherpa_onnx.OfflineTts(cfg)

def decir(tts, texto, hablante, velocidad):
    a = tts.generate(texto, sid=hablante, speed=velocidad)
    x = np.asarray(a.samples, dtype=float)
    return resample_poly(x, SR, a.sample_rate)

def recortar_silencio(x, umbral=0.01):
    v = np.where(np.abs(x) > umbral)[0]
    return x[max(0, v[0] - 200): v[-1] + 2400] if len(v) else x

def pulir(x):
    """Lo que se le hace a una locución: quitar graves de sobra, un poco de presencia y compresión."""
    b, a = butter(2, 90 / (SR / 2), "highpass"); x = lfilter(b, a, x)
    b, a = butter(1, [2500 / (SR / 2), 6000 / (SR / 2)], "bandpass"); x = x + 0.35 * lfilter(b, a, x)
    # compresor sencillo: baja lo que pasa de -18 dB con 3:1
    env = np.sqrt(lfilter([1 - 0.995], [1, -0.995], x ** 2)) + 1e-9
    umbral = 10 ** (-18 / 20)
    ganancia = np.where(env > umbral, (umbral / env) ** (1 - 1 / 3), 1.0)
    x = x * ganancia
    return x / (np.abs(x).max() + 1e-9) * 0.7

def montar(reel):
    v = reel["voz"]; dur = float(reel["duracion"])
    tts = motor_tts(v.get("modelo", "es_ES-sharvard-medium"))
    hablante = int(v.get("hablante", 0)); vel = float(v.get("velocidad", 1.0))
    pista = np.zeros(int(dur * SR))
    lineas = v["lineas"]
    for i, l in enumerate(lineas):
        hasta = l.get("hasta") or (lineas[i + 1]["t"] - 0.1 if i + 1 < len(lineas) else dur - 0.3)
        hueco = hasta - l["t"]
        x = recortar_silencio(decir(tts, l["texto"], hablante, vel))
        if len(x) / SR > hueco:                          # no cabe: más rápido, hasta un 15 %
            f = min(1.15, (len(x) / SR) / hueco)
            x = recortar_silencio(decir(tts, l["texto"], hablante, vel * f))
            if len(x) / SR > hueco + 0.05:
                print(f"  ! «{l['texto'][:40]}…» dura {len(x)/SR:.2f} s y su hueco es de {hueco:.2f} s", file=sys.stderr)
        k = int(l["t"] * SR); m = min(len(x), len(pista) - k)
        pista[k:k + m] += x[:m]
        print(f"  {l['t']:5.2f}–{l['t'] + len(x) / SR:5.2f} s  {l['texto']}")
    return pulir(pista)

if __name__ == "__main__":
    reel = json.load(open(sys.argv[1]))
    x = montar(reel)
    import wave
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    print("voz:", sys.argv[2])
