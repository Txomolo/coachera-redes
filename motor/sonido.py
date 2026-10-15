# ============================================================================
# El sonido de los Reels: una base rítmica y los efectos, sintetizados (sin samples)
# ============================================================================
#   python3 motor/sonido.py reel.json salida.wav
#
# reel.json es el window.REEL de la página:
#   duracion           segundos
#   musica             { bpm: 112, caida: 5.2 }  la "caída" es donde entra la base completa
#                      (antes va filtrada, con una subida que acaba en un golpe); false = sin música
#   sonidos            [{ t, tipo, vol }]  tipo: toque, pop, barrido, ok, tecla, golpe, marca
#
# Todo es síntesis: un bombo con caída de tono, platos de ruido, un bajo de diente de sierra
# con bombeo (sidechain) y acordes de La menor - Fa - Do - Sol. Sin samples ni música de
# terceros, así no hay derechos que pagar ni avisos de copyright en Instagram.
import json, sys
import numpy as np
from scipy.signal import butter, lfilter

SR = 48000
rng = np.random.default_rng(7)

def env_exp(n, k):
    t = np.arange(n) / SR
    return np.exp(-t * k)

def filtro(x, tipo, f, orden=2):
    if isinstance(f, (list, tuple)):
        b, a = butter(orden, [f[0] / (SR / 2), f[1] / (SR / 2)], btype=tipo)
    else:
        b, a = butter(orden, f / (SR / 2), btype=tipo)
    return lfilter(b, a, x)

def sierra(freq, n, detune_cents=0.0):
    f = freq * 2 ** (detune_cents / 1200)
    t = np.arange(n) / SR
    fase = (t * f + rng.random()) % 1.0
    return 2 * fase - 1

def nota(nombre):
    notas = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    letra, octava = nombre[:-1], int(nombre[-1])
    return 440.0 * 2 ** ((notas[letra] + (octava - 4) * 12) / 12)

# ---- Instrumentos -----------------------------------------------------------------
def bombo():
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t * 32)
    fase = 2 * np.pi * np.cumsum(f) / SR
    cuerpo = np.sin(fase) * np.exp(-t * 7.5)
    clic = filtro(rng.standard_normal(n), "highpass", 3000) * np.exp(-t * 400) * 0.25
    return np.tanh((cuerpo + clic) * 1.4)

def plato(abierto=False):
    n = int((0.22 if abierto else 0.06) * SR)
    x = filtro(rng.standard_normal(n), "highpass", 7000)
    return x * env_exp(n, 14 if abierto else 70) * 0.5

def palmada():
    n = int(0.25 * SR); x = np.zeros(n)
    for i, d in enumerate([0, 0.011, 0.022]):
        k = int(d * SR); m = n - k
        x[k:] += filtro(rng.standard_normal(m), "bandpass", (900, 3200)) * env_exp(m, 30 if i < 2 else 13)
    return x * 0.55

# ---- Efectos ----------------------------------------------------------------------
def fx(tipo):
    if tipo == "toque":
        n = int(0.05 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1650 * t) * env_exp(n, 90) * 0.6 + filtro(rng.standard_normal(n), "highpass", 4000) * env_exp(n, 300) * 0.2)
    if tipo == "pop":
        n = int(0.09 * SR); t = np.arange(n) / SR
        f = 520 + 700 * (t / t[-1])
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 45) * 0.55
    if tipo == "barrido":
        n = int(0.42 * SR); t = np.arange(n) / SR
        x = rng.standard_normal(n); out = np.zeros(n); paso = n // 12
        for i in range(12):   # el filtro sube a trozos: de 300 a 4000 Hz
            a, b = i * paso, min(n, (i + 1) * paso + 200)
            fc = 300 * (4000 / 300) ** (i / 11)
            out[a:b] += filtro(x[a:b], "bandpass", (fc * 0.7, min(fc * 1.4, 20000)))
        joroba = np.sin(np.pi * t / t[-1]) ** 2
        return out * joroba * 0.5
    if tipo == "ok":
        n = int(0.6 * SR); t = np.arange(n) / SR; x = np.zeros(n)
        for f, d in [(nota("E6"), 0), (nota("B6"), 0.07)]:
            k = int(d * SR); tt = t[: n - k]
            x[k:] += (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 7) * np.minimum(1, tt / 0.004)
        return x * 0.32
    if tipo == "marca":
        n = int(0.7 * SR); t = np.arange(n) / SR; x = np.zeros(n)
        for i, f in enumerate([nota("C6"), nota("E6"), nota("G6"), nota("C7")]):
            k = int(i * 0.055 * SR); tt = t[: n - k]
            x[k:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 8) * np.minimum(1, tt / 0.003)
        return x * 0.26
    if tipo == "tecla":
        n = int(0.025 * SR)
        return filtro(rng.standard_normal(n), "bandpass", (1800, 6000)) * env_exp(n, 220) * 0.35
    if tipo == "golpe":
        n = int(0.9 * SR); t = np.arange(n) / SR
        sub = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 18)) / SR) * np.exp(-t * 4.5)
        ruido = filtro(rng.standard_normal(n), "lowpass", 1800) * np.exp(-t * 9) * 0.5
        return np.tanh((sub + ruido) * 1.2) * 0.9
    # ---- Coachera TV (15-oct-2026) ----
    if tipo == "silbato":      # el del árbitro: un tono agudo con el «trino» de la bolita
        n = int(0.55 * SR); t = np.arange(n) / SR
        trino = 1 + 0.5 * np.sign(np.sin(2 * np.pi * 26 * t)) * 0.5
        f = 2950 + 90 * np.sin(2 * np.pi * 26 * t)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * trino + filtro(rng.standard_normal(n), "bandpass", (2500, 3600)) * 0.25
        env = np.minimum(1, t / 0.01) * np.clip((0.55 - t) / 0.06, 0, 1)
        return x * env * 0.32
    if tipo == "publico":      # el estadio que se viene arriba
        n = int(2.2 * SR); t = np.arange(n) / SR
        x = filtro(rng.standard_normal(n), "bandpass", (350, 3200)) + filtro(rng.standard_normal(n), "bandpass", (900, 1800)) * 0.6
        env = np.minimum(1, t / 0.35) * np.exp(-np.maximum(0, t - 0.6) * 1.6)
        return x * env * 0.28
    if tipo == "estatica":     # la tele sin señal
        n = int(0.7 * SR); t = np.arange(n) / SR
        x = filtro(rng.standard_normal(n), "highpass", 900) * (0.7 + 0.3 * (rng.random(n) > 0.995))
        return x * np.minimum(1, t / 0.01) * np.clip((0.7 - t) / 0.05, 0, 1) * 0.3
    if tipo == "var":          # el aviso del VAR: dos pitidos
        n = int(0.5 * SR); t = np.arange(n) / SR; x = np.zeros(n)
        for f, d in [(988, 0.0), (740, 0.18)]:
            k = int(d * SR); m = int(0.15 * SR); tt = t[:m]
            x[k:k + m] += np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 * np.minimum(1, tt / 0.003) * np.clip((0.15 - tt) / 0.01, 0, 1)
        return filtro(x, "lowpass", 5000) * 0.22
    if tipo == "noticia":      # la sintonía de última hora: tres golpes de orquesta
        n = int(1.0 * SR); t = np.arange(n) / SR; x = np.zeros(n)
        for i, acorde in enumerate([["A3", "E4", "A4"], ["A3", "E4", "A4"], ["F3", "C4", "F4"]]):
            k = int(i * 0.14 * SR); m = n - k; tt = t[:m]
            for nt in acorde:
                ff = nota(nt)
                x[k:] += (sierra(ff, m, -6) + sierra(ff, m, 6)) * np.exp(-tt * (9 if i < 2 else 3.5)) * 0.12
        return filtro(x, "lowpass", 4200)
    raise ValueError("tipo de sonido desconocido: " + tipo)

def subida(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); out = np.zeros(n); trozos = 24; paso = n // trozos
    for i in range(trozos):
        a, b = i * paso, min(n, (i + 1) * paso + 300)
        fc = 400 * (9000 / 400) ** (i / (trozos - 1))
        out[a:b] += filtro(x[a:b], "bandpass", (fc * 0.6, min(fc * 1.5, 22000)))
    tono = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (t / dur) ** 2) / SR) * 0.15
    return (out * 0.35 + tono) * (t / dur) ** 2

# ---- La base ----------------------------------------------------------------------
ACORDES = [("A2", ["A3", "C4", "E4"]), ("F2", ["F3", "A3", "C4"]), ("C2", ["C3", "E3", "G3"]), ("G2", ["G3", "B3", "D4"])]

def base(dur, bpm, caida):
    n = int(dur * SR) + SR
    L = np.zeros(n); Rr = np.zeros(n)
    pulso = 60 / bpm
    def poner(señal, t, vol=1.0, pan=0.0):
        k = int(t * SR)
        if k >= n: return
        m = min(len(señal), n - k)
        L[k:k + m] += señal[:m] * vol * (1 - max(0, pan))
        Rr[k:k + m] += señal[:m] * vol * (1 + min(0, pan))
    # sidechain: cuánto "bombea" cada instante tras cada bombo
    bomb = np.ones(n)
    t_b = 0.0
    while t_b < dur:
        if t_b >= caida - 0.01:
            poner(bombo(), t_b, 0.9)
            k = int(t_b * SR); m = min(int(pulso * SR), n - k)
            bomb[k:k + m] = 1 - 0.65 * np.exp(-np.arange(m) / SR * 9)
        elif t_b >= caida - 4 * pulso:      # un compás antes de la caída, solo un bombo suave
            poner(bombo(), t_b, 0.35)
        poner(plato(), t_b + pulso / 2, 0.28 if t_b >= caida else 0.14, 0.3)
        if t_b >= caida and int(round(t_b / pulso)) % 2 == 1:
            poner(palmada(), t_b, 0.45, -0.1)
        t_b += pulso
    # bajo y acordes, un acorde por compás
    compas = 4 * pulso
    pad = np.zeros(n); pad_r = np.zeros(n); bajo = np.zeros(n)
    t_c, i = 0.0, 0
    while t_c < dur:
        raiz, tonos = ACORDES[i % 4]
        m = int(compas * SR); k = int(t_c * SR); m = min(m, n - k)
        tt = np.arange(m) / SR
        envp = np.minimum(1, tt / 0.35) * np.minimum(1, (compas - tt) / 0.25)
        for tn in tonos:
            f = nota(tn)
            pad[k:k + m] += (sierra(f, m, -8) + sierra(f, m, 4)) * envp * 0.08
            pad_r[k:k + m] += (sierra(f, m, 8) + sierra(f, m, -4)) * envp * 0.08
        # bajo en corcheas
        fb = nota(raiz)
        for j in range(8):
            kk = k + int(j * pulso / 2 * SR); mm = min(int(pulso / 2 * SR * 0.9), n - kk)
            if mm <= 0: break
            t2 = np.arange(mm) / SR
            bajo[kk:kk + mm] += (sierra(fb, mm) * 0.6 + np.sin(2 * np.pi * fb * t2)) * np.minimum(1, t2 / 0.004) * np.exp(-t2 * 5) * 0.32
        t_c += compas; i += 1
    # antes de la caída, todo filtrado (como oído desde fuera de la sala)
    corte = int(caida * SR)
    def filtrar_antes(x, f_antes, f_despues):
        a = filtro(x[:corte], "lowpass", f_antes) if corte > 0 else x[:0]
        b = filtro(x[corte:], "lowpass", f_despues)
        return np.concatenate([a, b])
    pad = filtrar_antes(pad, 700, 2600) * bomb
    pad_r = filtrar_antes(pad_r, 700, 2600) * bomb
    bajo = filtrar_antes(bajo, 250, 900) * bomb
    L += pad + bajo; Rr += pad_r + bajo
    if caida > 1.6:
        s = subida(1.5); poner(s, caida - 1.5, 0.8)
        poner(fx("golpe"), caida, 0.7)
    return L[: int(dur * SR)], Rr[: int(dur * SR)]

# ---- Reverberación: lo que hace que un sintetizador no suene a juguete ----------------
from scipy.signal import fftconvolve
def _ir(segs, brillo, semilla):
    g = np.random.default_rng(semilla)
    n = int(segs * SR); t = np.arange(n) / SR
    ir = g.standard_normal(n) * np.exp(-t * 6.9 / segs)          # -60 dB al final
    ir = filtro(ir, "lowpass", brillo)
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))   # un pelo de predelay
    return ir / np.sqrt(np.sum(ir ** 2))
def reverb(L, R, segs=2.4, mezcla=0.3, brillo=5200):
    il, ir = _ir(segs, brillo, 11), _ir(segs, brillo, 23)
    wl = fftconvolve(L, il)[: len(L)]; wr = fftconvolve(R, ir)[: len(R)]
    return L * (1 - mezcla) + wl * mezcla, R * (1 - mezcla) + wr * mezcla

def tono_suave(f, n, detune=0.0):
    """Un tono redondo: seno con dos armónicos flojos (nada de diente de sierra)."""
    t = np.arange(n) / SR; ff = f * 2 ** (detune / 1200); fase = rng.random() * 6.28
    return np.sin(2*np.pi*ff*t + fase) + 0.22*np.sin(4*np.pi*ff*t + fase) + 0.07*np.sin(6*np.pi*ff*t + fase)

def bombo_suave():
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 42 + 70 * np.exp(-t * 26)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t * 6) * np.minimum(1, t / 0.002)

def maraca():
    n = int(0.07 * SR)
    return filtro(rng.standard_normal(n), "bandpass", (5000, 11000)) * env_exp(n, 55) * 0.35

# Acordes con séptimas y novenas: suenan más "producto", menos videojuego
ACORDES_SUAVES = [("A1", ["A3", "C4", "E4", "G4", "B4"]), ("F1", ["F3", "A3", "C4", "E4"]),
                  ("C2", ["C4", "E4", "G4", "B4"]), ("G1", ["G3", "B3", "D4", "E4"])]

def ambiente(dur, bpm, caida, pulso_ritmo=False):
    n = int(dur * SR) + SR
    L = np.zeros(n); R = np.zeros(n)
    pulso = 60 / bpm; compas = 4 * pulso
    t_c, i = 0.0, 0
    while t_c < dur:
        raiz, tonos = ACORDES_SUAVES[i % 4]
        k = int(t_c * SR); m = min(int((compas + 1.2) * SR), n - k)   # cada acorde se solapa con el siguiente
        tt = np.arange(m) / SR
        env = np.minimum(1, tt / 0.9) * np.clip((compas + 1.2 - tt) / 1.2, 0, 1)
        for j, tn in enumerate(tonos):
            f = nota(tn); p = (j / max(1, len(tonos) - 1) - 0.5) * 0.8
            L[k:k+m] += tono_suave(f, m, -6) * env * 0.06 * (1 - p)
            R[k:k+m] += tono_suave(f, m, 6) * env * 0.06 * (1 + p)
        sub = np.sin(2*np.pi*nota(raiz)*2*tt) * env * 0.16                 # el bajo, una octava arriba de la raíz
        L[k:k+m] += sub; R[k:k+m] += sub
        t_c += compas; i += 1
    # antes de la caída, más apagado; después se abre
    corte = int(caida * SR)
    def abrir(x):
        a = filtro(x[:corte], "lowpass", 900) if corte > 0 else x[:0]
        return np.concatenate([a, filtro(x[corte:], "lowpass", 3400)])
    L, R = abrir(L), abrir(R)
    if pulso_ritmo:
        bomb = np.ones(n); t_b = caida
        while t_b < dur:
            k = int(t_b * SR); b = bombo_suave(); m = min(len(b), n - k)
            L[k:k+m] += b[:m] * 0.5; R[k:k+m] += b[:m] * 0.5
            mm = min(int(pulso * SR), n - k)
            bomb[k:k+mm] = 1 - 0.35 * np.exp(-np.arange(mm) / SR * 8)
            for s16 in range(4):
                ks = int((t_b + s16 * pulso / 4) * SR)
                if ks < n:
                    x = maraca() * (0.9 if s16 == 2 else 0.45); ms = min(len(x), n - ks)
                    L[ks:ks+ms] += x[:ms] * 0.8; R[ks:ks+ms] += x[:ms]
            t_b += pulso
        L *= bomb; R *= bomb
    L, R = reverb(L, R, 2.8, 0.38)
    return L[: int(dur * SR)], R[: int(dur * SR)]

def mezclar(reel):
    dur = float(reel["duracion"])
    n = int(dur * SR)
    L = np.zeros(n); Rr = np.zeros(n)
    m = reel.get("musica", {"bpm": 112, "caida": 0})
    estilo = (m or {}).get("estilo", "pulso") if m else "efectos"
    if estilo != "efectos":
        if estilo == "base":      # la primera versión (descartada el 13-oct: sonaba a sintetizador barato)
            bl, br = base(dur, m.get("bpm", 112), m.get("caida", 0))
        elif estilo in ("phonk", "house", "pop"):   # con energía (motor/musica.py, desde el 15-oct)
            import os as _os; sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
            import musica
            bl, br = musica.estilo(estilo, dur, m.get("caida", 0), m.get("bpm"))
            pico = max(np.abs(bl).max(), np.abs(br).max()) + 1e-9
            bl, br = bl / pico * 0.5, br / pico * 0.5
        else:
            bl, br = ambiente(dur, m.get("bpm", 112) if estilo == "pulso" else 84, m.get("caida", 0), estilo == "pulso")
        vol = m.get("vol", 0.55)
        L += bl * vol; Rr += br * vol
    fl = np.zeros(n); fr = np.zeros(n)
    for s in reel.get("sonidos", []):
        x = fx(s["tipo"]) * s.get("vol", 1.0)
        k = int(s["t"] * SR); mm = min(len(x), n - k)
        if mm > 0:
            fl[k:k + mm] += x[:mm]; fr[k:k + mm] += x[:mm]
    fl, fr = reverb(fl, fr, 1.4, 0.18, 7000)       # los efectos, con un poco de sala
    L += fl; Rr += fr
    # la voz en off, si la hay: un WAV ya montado (motor/voz.py) que va por encima y baja la música
    if reel.get("voz"):
        import wave as _w
        with _w.open(reel["voz"]) as w:
            v = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(float) / 32768
            if w.getnchannels() == 2: v = v.reshape(-1, 2).mean(1)
            if w.getframerate() != SR:
                from scipy.signal import resample_poly
                v = resample_poly(v, SR, w.getframerate())
        v = np.pad(v, (0, max(0, n - len(v))))[:n]
        # la música se aparta mientras habla (ducking): envolvente de la voz, suavizada
        env = filtro(np.abs(v), "lowpass", 4) ; env = np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
        musica_l, musica_r = L - fl, Rr - fr
        L = musica_l * (1 - 0.55 * env) + fl + v * reel.get("vol_voz", 1.6)
        Rr = musica_r * (1 - 0.55 * env) + fr + v * reel.get("vol_voz", 1.6)
    # entrada y salida suaves
    fi, fo = int(0.04 * SR), int(min(1.2, dur / 6) * SR)
    rampa_in = np.linspace(0, 1, fi); rampa_out = np.linspace(1, 0, fo)
    for c in (L, Rr):
        c[:fi] *= rampa_in; c[-fo:] *= rampa_out
    est = np.stack([L, Rr], 1)
    # nivel: RMS a unos -16 dBFS y un limitador suave
    rms = np.sqrt(np.mean(est ** 2)) + 1e-9
    est *= 10 ** (-16 / 20) / rms
    est = np.tanh(est * 1.1) / np.tanh(1.1)
    est *= 0.89 / max(1e-9, np.abs(est).max())
    return est

if __name__ == "__main__":
    reel = json.load(open(sys.argv[1]))
    est = mezclar(reel)
    import wave
    with wave.open(sys.argv[2], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    print("sonido:", sys.argv[2], f"{len(est) / SR:.1f} s")
