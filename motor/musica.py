# ============================================================================
# Música con energía para los Reels (15-oct-2026: el usuario encontró «sosa» la de ambiente)
# ============================================================================
# Tres estilos, todos sintetizados (sin samples ni música de terceros: nada de derechos):
#   phonk   ~130 bpm, medio tiempo: el cencerro del 808 con su riff, un 808 saturado que
#           desliza, charles con redobles y la palmada en el 3. Es lo que suena en el gimnasio.
#   house   ~124 bpm: bombo a negras, palmadas en 2 y 4, acordes cortos que bombean con el
#           bombo y el bajo a contratiempo. Alegre, de producto.
#   pop     ~140 bpm, medio tiempo: un arpegio brillante en Do mayor, 808 limpio y redobles.
# La «caída» (el segundo en que acaba el gancho del reel) cae siempre en el primer tiempo de
# un compás: antes, la música va filtrada y con una subida; en la caída entra todo de golpe.
#   L, R = musica.estilo("phonk", dur, caida)
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve

SR = 48000
_rng = np.random.default_rng(31)

def _f(x, tipo, f, orden=2):
    w = [f[0] / (SR / 2), f[1] / (SR / 2)] if isinstance(f, (list, tuple)) else f / (SR / 2)
    b, a = butter(orden, w, btype=tipo)
    return lfilter(b, a, x)

def nota(nombre):
    pos = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    return 440.0 * 2 ** ((pos[nombre[:-1]] + (int(nombre[-1]) - 4) * 12) / 12)

def _t(n): return np.arange(n) / SR
def _env(n, ataque, caida):
    t = _t(n)
    return np.minimum(1, t / max(ataque, 1e-4)) * np.exp(-t * caida)

# ---- instrumentos -------------------------------------------------------------------
def bombo(duro=1.0):
    n = int(0.45 * SR); t = _t(n)
    f = 44 + 160 * np.exp(-t * 38)
    cuerpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    clic = _f(_rng.standard_normal(n), "highpass", 2500) * np.exp(-t * 500) * 0.35
    return np.tanh((cuerpo + clic) * (1.6 + duro))

def ochocientos(f, dur, desliza_a=None, sucio=2.2):
    """El 808: un seno grave que cae, con una distorsión que lo hace oír en el móvil."""
    n = int(dur * SR); t = _t(n)
    ff = np.full(n, f)
    if desliza_a:
        k = int(0.12 * SR)
        ff[:k] = np.linspace(f, desliza_a, k) if desliza_a else f
        ff[:k] = desliza_a + (f - desliza_a) * (np.arange(k) / k) ** 0.5
    ff = ff * (1 + 0.6 * np.exp(-t * 60))            # el golpe del principio
    x = np.sin(2 * np.pi * np.cumsum(ff) / SR)
    x = np.tanh(x * sucio) / np.tanh(sucio)
    x += 0.35 * np.tanh(np.sin(4 * np.pi * np.cumsum(ff) / SR) * sucio)  # el armónico que se oye en el móvil
    return x * np.minimum(1, t / 0.004) * np.exp(-t * 2.2) * np.clip((dur - t) / 0.03, 0, 1)

def cencerro(f=None, dur=0.32):
    """El cencerro del 808: dos cuadradas (540 y 800 Hz en el original) por un pasabanda."""
    f = f or 540.0
    n = int(dur * SR); t = _t(n)
    sq = lambda fr: np.sign(np.sin(2 * np.pi * fr * t + _rng.random()))
    x = sq(f) * 0.6 + sq(f * 1.4815) * 0.4
    x = _f(x, "bandpass", (f * 0.9, min(f * 6, 20000)), 2)
    env = np.exp(-t * 55) * 0.6 + np.exp(-t * 9) * 0.4
    return x * env * np.minimum(1, t / 0.0015) * 0.8

def charles(abierto=False):
    n = int((0.25 if abierto else 0.045) * SR); t = _t(n)
    x = _f(_rng.standard_normal(n), "highpass", 8000)
    x += _f(_rng.standard_normal(n), "bandpass", (6000, 9000)) * 0.4
    return x * np.exp(-t * (11 if abierto else 85)) * 0.45

def palmada():
    n = int(0.32 * SR); x = np.zeros(n)
    for i, d in enumerate([0, 0.009, 0.018, 0.027]):
        k = int(d * SR); m = n - k
        x[k:] += _f(_rng.standard_normal(m), "bandpass", (950, 3400)) * np.exp(-_t(m) * (60 if i < 3 else 14))
    return np.tanh(x * 1.4) * 0.6

def caja():
    n = int(0.3 * SR); t = _t(n)
    tono = np.sin(2 * np.pi * np.cumsum(185 + 60 * np.exp(-t * 40)) / SR) * np.exp(-t * 22) * 0.6
    ruido = _f(_rng.standard_normal(n), "bandpass", (1500, 9000)) * np.exp(-t * 16) * 0.7
    return np.tanh((tono + ruido) * 1.5) * 0.6

def sierra(f, n, det=0.0):
    ff = f * 2 ** (det / 1200)
    return 2 * ((_t(n) * ff + _rng.random()) % 1.0) - 1

def pulsado(fs, dur, brillo=4200, caida=10.0, ancho=7.0):
    """Un acorde corto que se abre y se cierra (los «stabs» del house, el arpegio del pop)."""
    n = int(dur * SR); t = _t(n)
    L = np.zeros(n); R = np.zeros(n)
    for f in fs:
        L += sierra(f, n, -ancho) + sierra(f, n, ancho * .4)
        R += sierra(f, n, ancho) + sierra(f, n, -ancho * .4)
    # filtro que cae: en tres tramos (lfilter no varía en el tiempo)
    env = np.exp(-t * caida)
    out = []
    for x in (L, R):
        brillante = _f(x, "lowpass", brillo); oscuro = _f(x, "lowpass", 700)
        out.append((brillante * env + oscuro * (1 - env)) * np.minimum(1, t / 0.003) * np.exp(-t * caida * 0.35) * 0.18 / max(1, len(fs) ** 0.5))
    return out[0], out[1]

def pad(fs, dur):
    n = int(dur * SR); t = _t(n)
    L = np.zeros(n); R = np.zeros(n)
    for f in fs:
        L += sierra(f, n, -9) + sierra(f, n, 5); R += sierra(f, n, 9) + sierra(f, n, -5)
    env = np.minimum(1, t / 0.6) * np.clip((dur - t) / 0.5, 0, 1)
    return _f(L, "lowpass", 1500) * env * 0.05, _f(R, "lowpass", 1500) * env * 0.05

def subida(dur):
    n = int(dur * SR); t = _t(n); x = _rng.standard_normal(n); out = np.zeros(n)
    trozos = 28; paso = n // trozos
    for i in range(trozos):
        a, b = i * paso, min(n, (i + 1) * paso + 300)
        fc = 300 * (10000 / 300) ** (i / (trozos - 1))
        out[a:b] += _f(x[a:b], "bandpass", (fc * .6, min(fc * 1.6, 22000)))
    return out * (t / dur) ** 2.2 * 0.5

def impacto():
    n = int(1.6 * SR); t = _t(n)
    sub = np.sin(2 * np.pi * np.cumsum(36 + 90 * np.exp(-t * 14)) / SR) * np.exp(-t * 2.8)
    ruido = _f(_rng.standard_normal(n), "lowpass", 3000) * np.exp(-t * 5) * 0.4
    return np.tanh((sub + ruido) * 1.8) * 0.8

def _ir(segs, brillo, semilla):
    g = np.random.default_rng(semilla); n = int(segs * SR); t = _t(n)
    ir = _f(g.standard_normal(n) * np.exp(-t * 6.9 / segs), "lowpass", brillo)
    ir[: int(.01 * SR)] *= np.linspace(0, 1, int(.01 * SR))
    return ir / np.sqrt(np.sum(ir ** 2))
def _reverb(L, R, segs, mezcla, brillo=6000):
    return (L * (1 - mezcla) + fftconvolve(L, _ir(segs, brillo, 3))[:len(L)] * mezcla,
            R * (1 - mezcla) + fftconvolve(R, _ir(segs, brillo, 5))[:len(R)] * mezcla)

# ---- la mesa -------------------------------------------------------------------------
class Pista:
    def __init__(self, dur):
        self.n = int(dur * SR) + 2 * SR
        self.pistas = {}
    def bus(self, nombre):
        if nombre not in self.pistas:
            self.pistas[nombre] = [np.zeros(self.n), np.zeros(self.n)]
        return self.pistas[nombre]
    def pon(self, nombre, señal, t, vol=1.0, pan=0.0):
        if t < 0: return
        L, R = self.bus(nombre); k = int(t * SR)
        if k >= self.n: return
        if isinstance(señal, tuple): sl, sr = señal
        else: sl = sr = señal
        m = min(len(sl), self.n - k)
        L[k:k + m] += sl[:m] * vol * (1 - max(0, pan)); R[k:k + m] += sr[:m] * vol * (1 + min(0, pan))

def _rejilla(caida, beat, dur):
    """Los tiempos de la música: un compás empieza justo en la caída."""
    k0 = -int(np.ceil(caida / beat)) - 1
    return [caida + k * beat for k in range(k0, int((dur - caida) / beat) + 2)]

def _abrir(x, caida, antes, despues):
    k = int(max(0, caida) * SR)
    a = _f(x[:k], "lowpass", antes) if k > 0 else x[:0]
    return np.concatenate([a, _f(x[k:], "lowpass", despues) if despues else x[k:]])

def _bombeo(n, golpes, beat, cuanto=0.6, rec=9):
    s = np.ones(n)
    for tb in golpes:
        k = int(tb * SR)
        if 0 <= k < n:
            m = min(int(beat * SR), n - k)
            s[k:k + m] = np.minimum(s[k:k + m], 1 - cuanto * np.exp(-_t(m) * rec))
    return s

def phonk(dur, caida, bpm=130):
    beat = 60 / bpm; paso = beat / 4; compas = 4 * beat
    p = Pista(dur)
    # riff del cencerro (La menor), 16 pasos por compás, dos compases que se alternan
    A = ["A5", None, "A5", None, "C6", None, "A5", "G5", None, "A5", None, "E5", None, "G5", "A5", None]
    B = ["A5", None, "A5", None, "C6", None, "D6", "C6", None, "A5", None, "G5", None, "E5", "G5", None]
    bajo_a = [("A1", 0, 0.9), ("A1", 6, 0.6), ("C2", 10, 0.7, "A1")]
    bajo_b = [("A1", 0, 0.9), ("G1", 7, 0.5), ("E1", 10, 0.9, "G1")]
    kick_a = [0, 6, 10]; kick_b = [0, 3, 10, 14]
    golpes = []
    for i, t0 in enumerate([x for x in _rejilla(caida, compas, dur)]):
        if t0 > dur: break
        par = i % 2
        riff = A if par == 0 else B
        dentro = t0 >= caida - 1e-6
        for s, nt in enumerate(riff):
            if nt: p.pon("cencerro", cencerro(nota(nt) * 0.98), t0 + s * paso, 0.85 if dentro else 0.6, 0.1)
        if dentro:
            for s in (kick_a if par == 0 else kick_b):
                p.pon("bombo", bombo(1.4), t0 + s * paso, 0.9); golpes.append(t0 + s * paso)
            for b in (bajo_a if par == 0 else bajo_b):
                nt, s, d = b[0], b[1], b[2]; desde = nota(b[3]) if len(b) > 3 else None
                p.pon("808", ochocientos(nota(nt), d * compas / 2, desde), t0 + s * paso, 0.75)
            p.pon("palmada", palmada(), t0 + 8 * paso, 0.8, -0.05)
            for s in range(0, 16, 2):
                p.pon("charles", charles(), t0 + s * paso, 0.5 if s % 4 else 0.35, 0.25)
            if par == 1:   # el redoble de charles al final del segundo compás
                for r in range(6):
                    p.pon("charles", charles(), t0 + 12 * paso + r * (paso * 4 / 6), 0.4, 0.25)
        p.pon("pad", pad([nota("A2"), nota("C3"), nota("E3")], compas + .4), t0, 0.9)
    n = p.n
    for nombre in ("cencerro", "pad"):
        L, R = p.bus(nombre)
        p.pistas[nombre] = [_abrir(L, caida, 900, None), _abrir(R, caida, 900, None)]
    bomb = _bombeo(n, golpes, beat, 0.55)
    for nombre in ("pad", "cencerro"):
        p.pistas[nombre][0] *= bomb; p.pistas[nombre][1] *= bomb
    return _final(p, dur, caida, compas, {"cencerro": (0.9, 0.2), "palmada": (1.0, 0.25), "pad": (0.8, 0.4)},
                  {"bombo": 0.4, "808": 0.45, "cencerro": 1.6, "palmada": 2.2, "charles": 2.5, "pad": 1.2})

ACORDES_HOUSE = [["A4", "C5", "E5", "G5"], ["F4", "A4", "C5", "E5"], ["C5", "E5", "G5", "B5"], ["G4", "B4", "D5", "F#5"]]
RAICES_HOUSE = ["A1", "F1", "C2", "G1"]

def house(dur, caida, bpm=124):
    beat = 60 / bpm; paso = beat / 4; compas = 4 * beat
    p = Pista(dur); golpes = []
    for i, t0 in enumerate(_rejilla(caida, compas, dur)):
        if t0 > dur: break
        dentro = t0 >= caida - 1e-6
        acorde = [nota(x) for x in ACORDES_HOUSE[i % 4]]; raiz = nota(RAICES_HOUSE[i % 4])
        for s in (0, 3, 6, 10, 13):
            p.pon("stab", pulsado(acorde, 0.3, 6500, 7), t0 + s * paso, 1.0 if dentro else 0.7)
        for s in range(16):
            if s % 2 == 1: p.pon("charles", charles(), t0 + s * paso, 0.22, 0.3)
        if dentro:
            for b in range(4):
                p.pon("bombo", bombo(0.6), t0 + b * beat, 0.95); golpes.append(t0 + b * beat)
                p.pon("charles", charles(True), t0 + b * beat + 2 * paso, 0.45, -0.25)
            for b in (1, 3): p.pon("palmada", palmada(), t0 + b * beat, 0.7)
            for s in (2, 6, 10, 14):
                n = int(paso * 1.8 * SR); t = _t(n)
                x = (sierra(raiz * 2, n) * 0.5 + np.sin(2 * np.pi * raiz * 2 * t)) * _env(n, .003, 9)
                p.pon("bajo", _f(x, "lowpass", 900) * 0.55, t0 + s * paso)
    n = p.n
    for nombre in ("stab", "charles"):
        L, R = p.bus(nombre)
        p.pistas[nombre] = [_abrir(L, caida, 1100, None), _abrir(R, caida, 1100, None)]
    bomb = _bombeo(n, golpes, beat, 0.7, 8)
    for nombre in ("stab", "bajo"):
        p.pistas[nombre][0] *= bomb; p.pistas[nombre][1] *= bomb
    return _final(p, dur, caida, compas, {"stab": (1.1, 0.35), "palmada": (1.0, 0.3)},
                  {"bombo": 0.42, "bajo": 0.8, "stab": 2.6, "palmada": 2.0, "charles": 2.2})

ACORDES_POP = [["C4", "E4", "G4", "C5"], ["A3", "C4", "E4", "A4"], ["F3", "A3", "C4", "F4"], ["G3", "B3", "D4", "G4"]]
RAICES_POP = ["C2", "A1", "F1", "G1"]

def pop(dur, caida, bpm=140):
    beat = 60 / bpm; paso = beat / 4; compas = 4 * beat
    p = Pista(dur); golpes = []
    for i, t0 in enumerate(_rejilla(caida, compas, dur)):
        if t0 > dur: break
        dentro = t0 >= caida - 1e-6
        acorde = [nota(x) for x in ACORDES_POP[i % 4]]
        orden = [0, 1, 2, 3, 2, 1, 2, 3, 0, 2, 3, 2, 1, 2, 3, 2]
        for s, j in enumerate(orden):
            f = acorde[j] * 2
            p.pon("arpegio", pulsado([f], paso * 1.6, 6500, 16, 4), t0 + s * paso, 1.1 if dentro else 0.8, 0.15 if s % 2 else -0.15)
        p.pon("pad", pad(acorde, compas + .3), t0, 0.8)
        if dentro:
            for s in ([0, 7, 10] if i % 2 == 0 else [0, 3, 10, 11]):
                p.pon("bombo", bombo(1.0), t0 + s * paso, 0.85); golpes.append(t0 + s * paso)
            p.pon("808", ochocientos(nota(RAICES_POP[i % 4]), compas * 0.9, sucio=1.2), t0, 0.6)
            p.pon("caja", caja(), t0 + 8 * paso, 0.75)
            p.pon("palmada", palmada(), t0 + 8 * paso, 0.45)
            for s in range(0, 16, 2): p.pon("charles", charles(), t0 + s * paso, 0.4, 0.25)
            if i % 2 == 1:
                for r in range(8): p.pon("charles", charles(), t0 + 14 * paso + r * paso / 4, 0.3, 0.25)
    n = p.n
    for nombre in ("arpegio", "pad"):
        L, R = p.bus(nombre)
        p.pistas[nombre] = [_abrir(L, caida, 1200, None), _abrir(R, caida, 1200, None)]
    bomb = _bombeo(n, golpes, beat, 0.5)
    for nombre in ("arpegio", "pad"):
        p.pistas[nombre][0] *= bomb; p.pistas[nombre][1] *= bomb
    return _final(p, dur, caida, compas, {"arpegio": (1.0, 0.3), "caja": (1.0, 0.25), "pad": (0.9, 0.4)},
                  {"bombo": 0.42, "808": 0.7, "arpegio": 2.4, "pad": 1.2, "caja": 1.8, "palmada": 1.5, "charles": 2.5})

def _final(p, dur, caida, compas, reverb_de, gan=None):
    """Mezcla los buses. «gan» es el volumen de cada uno: medido para que en el altavoz de un móvil
    (que no da graves por debajo de ~150 Hz) se oiga la melodía y no solo el bombo."""
    gan = gan or {}
    n = p.n; L = np.zeros(n); R = np.zeros(n)
    for nombre, (l, r) in p.pistas.items():
        g0 = gan.get(nombre, 1.0); l, r = l * g0, r * g0
        if nombre in reverb_de:
            g, mez = reverb_de[nombre]
            l, r = _reverb(l, r, 1.8, mez)
            l, r = l * g, r * g
        L += l; R += r
    if caida > 1.0:   # la subida que acaba en la caída, y el golpe
        dur_s = min(caida, compas)
        s = subida(dur_s); k = int((caida - dur_s) * SR); m = min(len(s), n - k)
        L[k:k + m] += s[:m] * 0.7; R[k:k + m] += s[:m] * 0.7
        im = impacto(); k = int(caida * SR); m = min(len(im), n - k)
        L[k:k + m] += im[:m] * 0.6; R[k:k + m] += im[:m] * 0.6
    L = _f(L, "highpass", 28); R = _f(R, "highpass", 28)
    return L[: int(dur * SR)], R[: int(dur * SR)]

ESTILOS = {"phonk": phonk, "house": house, "pop": pop}
def estilo(nombre, dur, caida, bpm=None):
    fn = ESTILOS[nombre]
    return fn(dur, caida, bpm) if bpm else fn(dur, caida)
