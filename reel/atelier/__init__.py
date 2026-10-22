"""Atelier Brooze — un compositeur à la After Effects, en code, pour l'agent (version dans VERSION, journal dans VERSIONS.md).

Une scène est un script Python qui construit une `Composition` (calques, images clés, effets) et la nomme `comp` :

    from atelier import *
    comp = Composition(1080, 1920, ips=30, duree=3, fond='#EDEBE7')
    mot = comp.ajouter(Texte('Montre-le.', taille=220, graisse=800,
                             animateurs=[Animateur(par='car', debut=.2, decalage=.03, duree=.4, courbe=sortie(4),
                                                   de=dict(opacite=0, y=60, flou=12))]))
    mot.echelle = K((.4, 1.3, chute(3)), (.6, 1.0))          # images clés : (temps, valeur, courbe du segment)
    comp.sons = [(.6, 'low_hit', .9)]

Rendu : `python3 reel/atelier scene.py --sortie essai.mp4` (voir `python3 reel/atelier --aide`).

Tout est déterministe : la même scène et le même temps donnent la même image (hasard à graine fixe), donc le rendu
peut être découpé, parallélisé et repris. Les images sont en RGBA float32 prémultiplié, en pixels de la composition.
"""
import os, re, math, json, functools
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(ICI, 'VERSION')).read().strip() if os.path.exists(os.path.join(ICI, 'VERSION')) else '0'
POLICES = [os.path.expanduser('~/.cache/brooze/polices')]

__all__ = ['Composition', 'Calque', 'Solide', 'Image_', 'Video', 'Texte', 'Forme', 'Precomp', 'Reglage', 'Nul', 'Camera',
           'Animateur', 'K', 'Voix', 'lin', 'doux', 'entree', 'sortie', 'chute', 'expo', 'bezier', 'ressort', 'tenir',
           'wiggle', 'boucle', 'rect', 'ellipse', 'points', 'svg', 'couleur',
           'FlouGaussien', 'FlouDirectionnel', 'OmbrePortee', 'Lueur', 'Grain', 'Aberration', 'Vignette', 'Niveaux',
           'Teinte', 'Remplir', 'Decaler', 'VERSION']


# =============================================================== couleurs
def couleur(c, a=1.):
    """'#rrggbb', '#rrggbbaa', (r, g, b) 0–255 ou 0–1 → (r, g, b, a) 0–1."""
    if isinstance(c, str):
        c = c.lstrip('#'); v = [int(c[i:i + 2], 16) / 255 for i in range(0, len(c), 2)]
        return tuple(v[:3]) + ((v[3],) if len(v) > 3 else (a,))
    c = tuple(float(x) for x in c)
    if max(c[:3]) > 1: c = tuple(x / 255 for x in c[:3]) + c[3:]
    return c[:3] + ((c[3],) if len(c) > 3 else (a,))


# =============================================================== courbes de vitesse (u ∈ [0, 1] → [0, 1])
lin = lambda u: u
def doux(u): return u * u * (3 - 2 * u)                                    # entrée et sortie douces (smoothstep)
def entree(p=3): return lambda u: u ** p                                     # accélère (départ lent)
def sortie(p=3): return lambda u: 1 - (1 - u) ** p                           # freine (arrivée douce)
def chute(p=2): return lambda u: u ** p                                      # chute accélérée jusqu'au contact
def expo(force=8): return lambda u: (1 - 2 ** (-force * u)) / (1 - 2 ** -force)
def tenir(u): return 0.                                                      # palier : la valeur reste jusqu'à la clé suivante
def bezier(x1, y1, x2, y2):
    """Courbe de vitesse façon After Effects (graphique de vitesse) : bezier cubique (0,0) (x1,y1) (x2,y2) (1,1)."""
    def f(u):
        lo, hi = 0., 1.
        for _ in range(40):
            m = (lo + hi) / 2; x = 3 * (1 - m) ** 2 * m * x1 + 3 * (1 - m) * m * m * x2 + m ** 3
            lo, hi = (m, hi) if x < u else (lo, m)
        m = (lo + hi) / 2
        return 3 * (1 - m) ** 2 * m * y1 + 3 * (1 - m) * m * m * y2 + m ** 3
    return f
def ressort(frequence=2.5, amortissement=.55):
    """Arrivée physique à ressort (dépassement amorti) ; amortissement ≥ 1 = aucun dépassement."""
    w = 2 * math.pi * frequence; z = amortissement
    def f(u):
        if u >= 1: return 1.
        if z >= 1: return 1 - (1 + w * u) * math.exp(-w * u)
        wd = w * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w * u) * (math.cos(wd * u) + z * w / wd * math.sin(wd * u))
    return f


# =============================================================== valeurs animées
def _melange(a, b, u):
    if isinstance(a, (tuple, list)): return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


class K:
    """Images clés : K((t0, v0, courbe), (t1, v1, courbe), …) ; la courbe d'une clé régit le segment qui en PART
    (par défaut `doux`). Avant la première clé : sa valeur ; après la dernière : la sienne."""
    def __init__(self, *cles):
        self.cles = sorted([(c[0], c[1], c[2] if len(c) > 2 else doux) for c in cles], key=lambda c: c[0])
    def __call__(self, t):
        c = self.cles
        if t <= c[0][0]: return c[0][1]
        for (t0, v0, f), (t1, v1, _) in zip(c, c[1:]):
            if t < t1: return _melange(v0, v1, f((t - t0) / (t1 - t0)) if t1 > t0 else 1)
        return c[-1][1]


def val(x, t):
    """Valeur d'un paramètre à l'instant t : constante, K, ou fonction t → valeur (expression)."""
    return x(t) if callable(x) else x


def _bruit(x, graine):
    """Bruit lisse 1D déterministe (valeur interpolée), −1 … 1."""
    i = math.floor(x); f = x - i; f = f * f * (3 - 2 * f)
    h = lambda n: ((math.sin(n * 127.1 + graine * 311.7) * 43758.5453) % 1) * 2 - 1
    return h(i) * (1 - f) + h(i + 1) * f


def wiggle(frequence, amplitude, graine=1, base=0.):
    """Expression wiggle() d'After Effects : base + bruit lisse. base et amplitude peuvent être des tuples."""
    def f(t):
        b = val(base, t)
        if isinstance(b, (tuple, list)):
            a = amplitude if isinstance(amplitude, (tuple, list)) else (amplitude,) * len(b)
            return tuple(bb + aa * _bruit(t * frequence, graine + 17 * k) for k, (bb, aa) in enumerate(zip(b, a)))
        return b + amplitude * _bruit(t * frequence, graine)
    return f


def boucle(anim, periode, debut=0.):
    """loopOut('cycle') : rejoue `anim` en boucle avec la période donnée."""
    return lambda t: val(anim, debut + ((t - debut) % periode) if t > debut else t)


class Voix:
    """Temps des mots de la voix (mots.json de comprendre.py) : synchroniser une animation sur ce que Zak dit.
    Voix('mots.json', source=[t0, t1]).t(12) = début du mot 12 dans le temps de la composition."""
    def __init__(self, chemin, source=None):
        m = json.load(open(chemin)); t0 = (source or [0])[0]
        self.mots = [dict(w, start=w['start'] - t0, end=w['end'] - t0) for w in m]
    def t(self, i, fin=False): return self.mots[i]['end' if fin else 'start']
    def texte(self, a, b): return ' '.join(w['w'] for w in self.mots[a:b + 1])
    def temps(self, a, b): return [w['start'] for w in self.mots[a:b + 1]]


# =============================================================== formes (chemins)
def rect(l, h, rayon=0):
    if not rayon: return [np.array([(-l / 2, -h / 2), (l / 2, -h / 2), (l / 2, h / 2), (-l / 2, h / 2)], float)], True
    r = min(rayon, l / 2, h / 2); pts = []
    for cx, cy, a0 in ((l / 2 - r, -h / 2 + r, -90), (l / 2 - r, h / 2 - r, 0), (-l / 2 + r, h / 2 - r, 90), (-l / 2 + r, -h / 2 + r, 180)):
        pts += [(cx + r * math.cos(math.radians(a0 + d)), cy + r * math.sin(math.radians(a0 + d))) for d in range(0, 91, 6)]
    return [np.array(pts)], True
def ellipse(l, h, n=128):
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return [np.stack([np.cos(a) * l / 2, np.sin(a) * h / 2], 1)], True
def points(pts, ferme=False): return [np.array(pts, float)], ferme
def svg(d, ferme=None):
    """Chemin SVG (M L H V C Q Z, absolu et relatif), échantillonné en polylignes."""
    jet = re.findall(r'[MLHVCQZmlhvcqz]|-?\d*\.?\d+(?:e-?\d+)?', d)
    sous, cur, p, i, cmd, fz = [], [], np.zeros(2), 0, 'M', False
    nb = lambda k: [float(x) for x in jet[i:i + k]]
    while i < len(jet):
        if re.match(r'[A-Za-z]', jet[i]): cmd = jet[i]; i += 1
        rel = cmd.islower(); c = cmd.upper(); o = p if rel else np.zeros(2)
        if c == 'Z':
            fz = True; cur and cur.append(cur[0]); continue
        if c == 'M':
            if cur: sous.append(np.array(cur))
            p = o + nb(2); i += 2; cur = [tuple(p)]; cmd = 'l' if rel else 'L'
        elif c == 'L': p = o + nb(2); i += 2; cur.append(tuple(p))
        elif c == 'H': p = np.array([o[0] + nb(1)[0], p[1]]); i += 1; cur.append(tuple(p))
        elif c == 'V': p = np.array([p[0], o[1] + nb(1)[0]]); i += 1; cur.append(tuple(p))
        elif c in 'CQ':
            k = 6 if c == 'C' else 4; v = nb(k); i += k
            ctrl = [p] + [o + v[j:j + 2] for j in range(0, k, 2)]
            for u in np.linspace(0, 1, 24)[1:]:
                if c == 'C': q = (1 - u) ** 3 * ctrl[0] + 3 * (1 - u) ** 2 * u * ctrl[1] + 3 * (1 - u) * u * u * ctrl[2] + u ** 3 * ctrl[3]
                else: q = (1 - u) ** 2 * ctrl[0] + 2 * (1 - u) * u * ctrl[1] + u * u * ctrl[2]
                cur.append(tuple(q))
            p = ctrl[-1]
        else: i += 1
    if cur: sous.append(np.array(cur))
    return sous, (fz if ferme is None else ferme)


def _rogner_trace(poly, debut, fin):
    """Trim paths : la portion [debut, fin] (0–1) de la longueur d'une polyligne."""
    if debut <= 0 and fin >= 1: return poly
    seg = np.hypot(*np.diff(poly, axis=0).T); L = np.r_[0, np.cumsum(seg)]; tot = L[-1]
    if tot == 0 or fin <= debut: return poly[:0]
    a, b = debut * tot, fin * tot
    pt = lambda s: np.array([np.interp(s, L, poly[:, 0]), np.interp(s, L, poly[:, 1])])
    mid = [poly[k] for k in range(len(poly)) if a < L[k] < b]
    return np.array([pt(a)] + mid + [pt(b)])


# =============================================================== effets (sur l'image RGBA prémultipliée)
class Effet:
    def __init__(self, **p): self.p = p
    def v(self, n, t, d=None): return val(self.p.get(n, d), t)


def _flou(im, r):
    if r <= .3: return im
    k = int(r * 3) * 2 + 1
    return cv2.GaussianBlur(im, (k, k), r, borderType=cv2.BORDER_CONSTANT)


class FlouGaussien(Effet):
    def appliquer(self, im, t, ctx): return _flou(im, self.v('rayon', t, 0))


class FlouDirectionnel(Effet):
    """Flou de mouvement directionnel (longueur en px, angle en degrés, 0 = horizontal)."""
    def appliquer(self, im, t, ctx):
        L = self.v('longueur', t, 0)
        if L < 1: return im
        a = math.radians(self.v('angle', t, 0)); n = int(L) | 1
        k = np.zeros((n, n), np.float32); c = n // 2
        for s in np.linspace(-c, c, n * 2):
            k[int(round(c + s * math.sin(a))), int(round(c + s * math.cos(a)))] = 1
        return cv2.filter2D(im, -1, k / k.sum(), borderType=cv2.BORDER_CONSTANT)


class OmbrePortee(Effet):
    """Ombre portée : distance (px), angle (degrés, 135 = vers le bas à droite), flou, opacite, couleur."""
    def appliquer(self, im, t, ctx):
        d, a = self.v('distance', t, 12), math.radians(self.v('angle', t, 135))
        col = couleur(self.v('couleur', t, '#000000')); op = self.v('opacite', t, .35)
        al = _flou(im[..., 3], self.v('flou', t, 10))
        M = np.float32([[1, 0, d * math.cos(a)], [0, 1, d * math.sin(a)]])
        al = cv2.warpAffine(al, M, (im.shape[1], im.shape[0])) * op
        om = np.dstack([al * col[0], al * col[1], al * col[2], al]).astype(np.float32)
        return im + om * (1 - im[..., 3:4])


class Lueur(Effet):
    """Glow : ajoute une version floutée des zones claires (seuil 0–1)."""
    def appliquer(self, im, t, ctx):
        s = self.v('seuil', t, .6); lum = im[..., :3].mean(axis=2, keepdims=True)
        claire = im * np.clip((lum - s) / max(1e-3, 1 - s), 0, 1)
        g = _flou(claire, self.v('rayon', t, 20)) * self.v('intensite', t, .8)
        out = im.copy(); out[..., :3] = np.minimum(1, im[..., :3] + g[..., :3]); out[..., 3] = np.maximum(im[..., 3], g[..., 3])
        return out


class Grain(Effet):
    """Grain photo animé (différent à chaque image, déterministe)."""
    def appliquer(self, im, t, ctx):
        f = int(round(t * ctx['ips'])); taille = max(1, int(self.v('taille', t, 1))); h, w = im.shape[:2]
        g = _bruit_grain(h, w, taille, int(self.v('graine', t, 0)))[f % 8]
        g = np.roll(g, ((f * 7919) % h, (f * 104729) % w), axis=(0, 1))
        out = im.copy(); out[..., :3] = np.clip(im[..., :3] + g[..., None] * self.v('intensite', t, .035) * im[..., 3:4], 0, 1)
        return out


@functools.lru_cache(maxsize=8)
def _bruit_grain(h, w, taille, graine):
    rng = np.random.default_rng(1000 + graine); out = []
    for _ in range(8):
        g = rng.standard_normal((h // taille + 1, w // taille + 1)).astype(np.float32)
        out.append(cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR if taille > 1 else cv2.INTER_NEAREST))
    return out


@functools.lru_cache(maxsize=8)
def _masque_vignette(h, w, force):
    y, x = np.ogrid[-1:1:h * 1j, -1:1:w * 1j]
    return (1 - force * np.clip((np.sqrt(x * x * .6 + y * y) - .35) / .9, 0, 1) ** 1.5)[..., None].astype(np.float32)


class Aberration(Effet):
    """Aberration chromatique : rouge et bleu décalés en sens opposés (px)."""
    def appliquer(self, im, t, ctx):
        d = self.v('decalage', t, 3); a = math.radians(self.v('angle', t, 0))
        if abs(d) < .2: return im
        out = im.copy(); h, w = im.shape[:2]
        for c, s in ((0, 1), (2, -1)):
            M = np.float32([[1, 0, s * d * math.cos(a)], [0, 1, s * d * math.sin(a)]])
            out[..., c] = cv2.warpAffine(im[..., c], M, (w, h))
        return out


class Vignette(Effet):
    def appliquer(self, im, t, ctx):
        out = im.copy(); out[..., :3] *= _masque_vignette(im.shape[0], im.shape[1], round(float(self.v('force', t, .2)), 3)); return out


class Niveaux(Effet):
    """Niveaux : noir, blanc (entrée 0–1), gamma ; plus `saturation` (1 = inchangée)."""
    def appliquer(self, im, t, ctx):
        a = np.maximum(im[..., 3:4], 1e-6); rgb = im[..., :3] / a
        n, b, g = self.v('noir', t, 0), self.v('blanc', t, 1), self.v('gamma', t, 1)
        rgb = np.clip((rgb - n) / max(1e-3, b - n), 0, 1) ** (1 / g)
        s = self.v('saturation', t, 1)
        if s != 1: m = rgb.mean(axis=2, keepdims=True); rgb = np.clip(m + (rgb - m) * s, 0, 1)
        out = im.copy(); out[..., :3] = rgb * im[..., 3:4]; return out


class Teinte(Effet):
    """Mélange vers une couleur (quantite 0–1), en gardant la luminosité (étalonnage chaud/froid)."""
    def appliquer(self, im, t, ctx):
        q = self.v('quantite', t, .2); col = np.array(couleur(self.v('couleur', t, '#B87333'))[:3], np.float32)
        lum = im[..., :3].mean(axis=2, keepdims=True) * 2
        out = im.copy(); out[..., :3] = im[..., :3] * (1 - q) + np.clip(lum * col, 0, 1) * im[..., 3:4] * q; return out


class Decaler(Effet):
    """Décale toute l'image (choc caméra, tremblé) SANS découvrir de bord : les bords sont prolongés en miroir
    (règle P-033). dx, dy en px, animables (ex. dy=choc(0.52))."""
    def appliquer(self, im, t, ctx):
        dx, dy = self.v('dx', t, 0), self.v('dy', t, 0)
        if abs(dx) < .01 and abs(dy) < .01: return im
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        return cv2.warpAffine(im, M, (im.shape[1], im.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


class Remplir(Effet):
    def appliquer(self, im, t, ctx):
        c = couleur(self.v('couleur', t, '#B87333')); out = im.copy()
        for k in range(3): out[..., k] = im[..., 3] * c[k]
        return out


# =============================================================== calques
FUSIONS = ('normal', 'ajout', 'ecran', 'produit', 'incrustation')


class Calque:
    """Calque générique. Paramètres animables (constante, K, ou fonction de t) :
    position (x, y) en px de la composition (centre par défaut), z (profondeur, caméra 2,5D), ancre (x, y) dans le
    contenu (centre par défaut), echelle (s ou (sx, sy)), rotation (degrés), opacite (0–1).
    debut / fin : présence dans le temps. parent : un autre calque (ou Nul) dont la transformation s'applique.
    effets : liste d'Effet. fusion : normal, ajout, ecran, produit, incrustation. masque : (chemin, ferme) en px du
    contenu (+ masque_contour = flou du bord, masque_inverse). cache : (calque, 'alpha' | 'alpha_inv' | 'luma').
    flou_mouvement : True pour un vrai flou de mouvement (sous-images de la transformation, voir Composition)."""
    def __init__(self, nom=None, debut=0., fin=None, position=None, z=0., ancre=None, echelle=1., rotation=0., opacite=1.,
                 parent=None, effets=None, fusion='normal', masque=None, masque_contour=0, masque_inverse=False, cache=None,
                 flou_mouvement=False, visible=True, decalage_temps=0.):
        self.nom = nom or self.__class__.__name__; self.debut, self.fin = debut, fin
        self.position, self.z, self.ancre, self.echelle, self.rotation, self.opacite = position, z, ancre, echelle, rotation, opacite
        self.parent, self.effets, self.fusion = parent, effets or [], fusion
        self.masque, self.masque_contour, self.masque_inverse, self.cache = masque, masque_contour, masque_inverse, cache
        self.flou_mouvement, self.visible, self.decalage_temps = flou_mouvement, visible, decalage_temps

    def present(self, t): return t >= self.debut and (self.fin is None or t < self.fin)
    def contenu(self, t, ctx):
        """→ (image RGBA prémultipliée float32, ancre par défaut (x, y)). À définir par chaque type de calque."""
        raise NotImplementedError

    def matrice(self, t, ctx, taille_contenu, ancre_defaut):
        """Matrice 3×3 contenu → composition (avec parents et projection de la caméra 2,5D)."""
        W, H = ctx['taille']
        ax, ay = val(self.ancre, t) if self.ancre is not None else ancre_defaut
        px, py = val(self.position, t) if self.position is not None else ((0, 0) if self.parent is not None else (W / 2, H / 2))
        s = val(self.echelle, t); sx, sy = s if isinstance(s, (tuple, list)) else (s, s)
        r = math.radians(val(self.rotation, t)); c, si = math.cos(r), math.sin(r)
        M = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]]) @ np.array([[c, -si, 0], [si, c, 0], [0, 0, 1]]) \
            @ np.diag([sx, sy, 1]) @ np.array([[1, 0, -ax], [0, 1, -ay], [0, 0, 1]])
        if self.parent is not None:
            P = self.parent.matrice(t, ctx, None, (0, 0)) if isinstance(self.parent, Nul) else self.parent._matrice_seule(t, ctx)
            M = P @ M
        cam = ctx.get('camera')
        if cam is not None:
            z = val(self.z, t) + (val(self.parent.z, t) if self.parent is not None else 0)
            k, cx, cy = cam.projection(t, z, ctx)
            M = np.array([[k, 0, cx - k * cx], [0, k, cy - k * cy], [0, 0, 1]]) @ np.array([[1, 0, -cam.dx(t)], [0, 1, -cam.dy(t)], [0, 0, 1]]) @ M
        return M

    def _matrice_seule(self, t, ctx):
        cam = ctx.pop('camera', None)
        try: return self.matrice(t, ctx, None, val(self.ancre, t) if self.ancre is not None else (0, 0))
        finally:
            if cam is not None: ctx['camera'] = cam


class Nul(Calque):
    """Objet nul : ne dessine rien, sert de parent (déplacer, tourner ou mettre à l'échelle un groupe)."""
    def __init__(self, **kw): kw.setdefault('visible', False); super().__init__(**kw)
    def matrice(self, t, ctx, taille_contenu, ancre_defaut): return Calque.matrice(self, t, {**ctx, 'camera': None}, None, (0, 0))
    def contenu(self, t, ctx): return np.zeros((1, 1, 4), np.float32), (0, 0)


class Camera:
    """Caméra 2,5D : zoom (distance focale en px ; défaut ≈ 50 mm pour 1080 de large), z (position de la caméra,
    négatif = recul), cible (x, y) de la composition, mise_au_point (z net), ouverture (flou par unité de z : 0 = tout net)."""
    def __init__(self, zoom=1500., z=0., cible=None, mise_au_point=0., ouverture=0.):
        self.zoom, self.z, self.cible, self.mise_au_point, self.ouverture = zoom, z, cible, mise_au_point, ouverture
    def dx(self, t): return (val(self.cible, t)[0] - self._W / 2) if self.cible is not None else 0
    def dy(self, t): return (val(self.cible, t)[1] - self._H / 2) if self.cible is not None else 0
    def projection(self, t, z, ctx):
        self._W, self._H = ctx['taille']; zoom = val(self.zoom, t)
        k = zoom / max(1., zoom + z - val(self.z, t))
        return k, self._W / 2, self._H / 2
    def flou(self, t, z):
        return abs(z - val(self.mise_au_point, t)) * val(self.ouverture, t)


class Solide(Calque):
    def __init__(self, couleur_='#141210', taille=None, **kw):
        super().__init__(**kw); self.couleur, self.taille = couleur_, taille
    def contenu(self, t, ctx):
        w, h = self.taille or ctx['taille']; c = couleur(val(self.couleur, t))
        im = np.empty((int(h), int(w), 4), np.float32); im[:] = (c[0] * c[3], c[1] * c[3], c[2] * c[3], c[3])
        return im, (w / 2, h / 2)


@functools.lru_cache(maxsize=64)
def _lire_image(chemin):
    im = cv2.imread(chemin, cv2.IMREAD_UNCHANGED)
    if im is None: raise FileNotFoundError(chemin)
    if im.ndim == 2: im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGRA)
    if im.shape[2] == 3: im = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA)
    im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA).astype(np.float32) / (65535 if im.dtype == np.uint16 else 255)
    im[..., :3] *= im[..., 3:4]
    return im


class Image_(Calque):
    """Image fixe (photo, rendu 3D, PNG détouré). `remplir=True` : couvre la composition (recadrage centré)."""
    def __init__(self, chemin, remplir=False, **kw): super().__init__(**kw); self.chemin, self.remplir = chemin, remplir
    def contenu(self, t, ctx):
        im = _lire_image(os.path.abspath(os.path.join(ctx['dossier'], self.chemin)))
        if self.remplir:
            W, H = ctx['taille']; s = max(W / im.shape[1], H / im.shape[0])
            im = cv2.resize(im, (int(round(im.shape[1] * s)), int(round(im.shape[0] * s))), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        return im, (im.shape[1] / 2, im.shape[0] / 2)


class Video(Calque):
    """Vidéo (rush, rendu 3D) : images extraites une fois au rythme de la composition. debut_source (s), vitesse."""
    def __init__(self, chemin, debut_source=0., vitesse=1., remplir=True, **kw):
        super().__init__(**kw); self.chemin, self.debut_source, self.vitesse, self.remplir = chemin, debut_source, vitesse, remplir
    def contenu(self, t, ctx):
        src = os.path.abspath(os.path.join(ctx['dossier'], self.chemin)); ips = ctx['ips']
        d = os.path.join(ctx['cache'], 'video_' + re.sub(r'\W', '_', os.path.basename(src)) + f'_{ips}')
        if not os.path.isdir(d):
            os.makedirs(d); import subprocess
            subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={ips}', '-q:v', '2', os.path.join(d, '%05d.jpg')], check=True)
        n = len(os.listdir(d)); k = min(n - 1, max(0, int(round((self.debut_source + (t - self.debut) * self.vitesse) * ips))))
        im = _lire_image(os.path.join(d, f'{k + 1:05d}.jpg'))
        if self.remplir:
            W, H = ctx['taille']; s = max(W / im.shape[1], H / im.shape[0])
            im = cv2.resize(im, (int(round(im.shape[1] * s)), int(round(im.shape[0] * s))), interpolation=cv2.INTER_AREA)
        return im, (im.shape[1] / 2, im.shape[0] / 2)


def _rasteriser(sous, ferme, taille, remplissage, trait, epaisseur, trace, decal):
    w, h = taille; S = 4                                      # sous-échantillonnage ×4 : bords propres
    al = np.zeros((h * S, w * S), np.uint8)
    polys = [(_rogner_trace(p, *trace) + decal) * S for p in sous]
    if remplissage is not None and ferme:
        cv2.fillPoly(al, [np.round(p).astype(np.int32) for p in polys if len(p) > 2], 255, cv2.LINE_AA)
    rempli = cv2.resize(al, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    al2 = np.zeros_like(al)
    if trait is not None and epaisseur > 0:
        for p in polys:
            if len(p) > 1: cv2.polylines(al2, [np.round(p).astype(np.int32)], ferme and trace == (0, 1), 255, max(1, int(epaisseur * S)), cv2.LINE_AA)
    contour = cv2.resize(al2, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return rempli, contour


class Forme(Calque):
    """Calque de forme : chemin = rect(l, h, rayon) | ellipse(l, h) | points([...], ferme) | svg('M … Z'),
    remplissage (couleur ou None), trait (couleur ou None), epaisseur, trace = (debut, fin) animables (trim paths)."""
    def __init__(self, chemin, remplissage='#141210', trait=None, epaisseur=0, trace_debut=0., trace_fin=1., **kw):
        super().__init__(**kw); self.chemin, self.remplissage, self.trait, self.epaisseur = chemin, remplissage, trait, epaisseur
        self.trace_debut, self.trace_fin = trace_debut, trace_fin
    def contenu(self, t, ctx):
        sous, ferme = val(self.chemin, t); ep = val(self.epaisseur, t)
        tout = np.vstack(sous); mn, mx = tout.min(0) - ep - 2, tout.max(0) + ep + 2
        w, h = int(math.ceil(mx[0] - mn[0])), int(math.ceil(mx[1] - mn[1]))
        rem, con = _rasteriser(sous, ferme, (w, h), self.remplissage, self.trait, ep, (val(self.trace_debut, t), val(self.trace_fin, t)), -mn)
        im = np.zeros((h, w, 4), np.float32)
        for a, c in ((rem, self.remplissage), (con, self.trait)):
            if c is None: continue
            c = couleur(val(c, t)); a = a * c[3]
            im[..., :3] = c[:3] * a[..., None] + im[..., :3] * (1 - a[..., None]); im[..., 3] = a + im[..., 3] * (1 - a)
        return im, (-mn[0], -mn[1])                            # ancre = origine du chemin


# --------------------------------------------------------------- texte et animateurs
def _police(nom):
    if os.path.isfile(nom): return nom
    for d in POLICES:
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.lower().startswith(nom.lower()): return os.path.join(d, f)
    raise FileNotFoundError(f'police {nom} introuvable dans {POLICES} (bash reel/setup.sh)')


@functools.lru_cache(maxsize=256)
def _fonte(chemin, taille, graisse, optique):
    f = ImageFont.truetype(chemin, int(round(taille)), layout_engine=ImageFont.Layout.RAQM)
    try:
        axes = f.get_variation_axes(); v = []
        for a in axes:
            n = a['name'].decode() if isinstance(a['name'], bytes) else a['name']
            v.append(graisse if n.lower().startswith('weight') else optique if n.lower().startswith('optical') and optique else a['default'])
        f.set_variation_by_axes([max(a['minimum'], min(a['maximum'], x)) for a, x in zip(axes, v)])
    except (OSError, AttributeError): pass
    return f


@functools.lru_cache(maxsize=2048)
def _tuile(texte, chemin, taille, graisse, optique, rgba):
    """Un morceau de texte rendu (RGBA prémultiplié float32) + décalage de son origine (ligne de base)."""
    f = _fonte(chemin, taille, graisse, optique); x0, y0, x1, y1 = f.getbbox(texte, anchor='ls')
    m = int(taille * .1) + 2; w, h = max(1, x1 - x0 + 2 * m), max(1, y1 - y0 + 2 * m)
    im = Image.new('L', (w, h), 0); ImageDraw.Draw(im).text((m - x0, m - y0), texte, font=f, fill=255, anchor='ls')
    a = np.asarray(im, np.float32) / 255 * rgba[3]
    return np.dstack([a * rgba[0], a * rgba[1], a * rgba[2], a]).astype(np.float32), (m - x0, m - y0)


class Animateur:
    """Animateur de texte (comme les animateurs After Effects) : chaque unité (car, mot, ligne) part des valeurs `de`
    et arrive à sa place, l'une après l'autre.
    par : 'car' | 'mot' | 'ligne' ; debut (s) ; decalage (s entre deux unités) ou temps=[t par unité] (synchro voix) ;
    duree (s) ; courbe ; ordre : 'normal' | 'inverse' | 'centre' | 'hasard' ;
    de = dict(opacite, x, y, echelle, rotation, flou, suivi) : valeurs de départ (décalages, sauf opacite et echelle).
    vers = dict(…) : valeurs d'ARRIVÉE pour une sortie (l'unité part de sa place et va vers `vers`)."""
    def __init__(self, par='car', debut=0., decalage=.04, duree=.4, courbe=None, de=None, vers=None, ordre='normal', temps=None):
        self.par, self.debut, self.decalage, self.duree, self.courbe = par, debut, decalage, duree, courbe or sortie(3)
        self.de, self.vers, self.ordre, self.temps = de or {}, vers or {}, ordre, temps
    def etat(self, i, n, t):
        """Valeurs (opacite, x, y, echelle, rotation, flou, suivi) de l'unité i sur n à l'instant t."""
        if self.temps is not None: t0 = self.temps[min(i, len(self.temps) - 1)]
        else:
            rang = {'normal': i, 'inverse': n - 1 - i, 'centre': abs(i - (n - 1) / 2),
                    'hasard': int((math.sin(i * 91.7) * 43758.5) % 1 * n)}[self.ordre]
            t0 = val(self.debut, t) + rang * self.decalage
        u = min(1., max(0., (t - t0) / max(1e-6, self.duree))); p = self.courbe(u)
        base = dict(opacite=1., x=0., y=0., echelle=1., rotation=0., flou=0., suivi=0.)
        if self.vers:
            return {k: base[k] + (self.vers[k] - base[k]) * p if k in self.vers else base[k] for k in base}
        return {k: self.de[k] + (base[k] - self.de[k]) * p if k in self.de else base[k] for k in base}


class Texte(Calque):
    """Texte en police variable. texte (\\n pour les lignes), police ('Inter', 'Fraunces'… ou chemin), taille (px),
    graisse (100–900, animable), optique, couleur, interlettrage (em, ex. −0,02), interligne (× taille),
    alignement ('gauche' | 'centre' | 'droite'), largeur_max (retour à la ligne auto), animateurs [Animateur].
    couleurs : {indice de mot: couleur} (le mot clé en cuivre) ; couleurs_car : {indice de caractère: couleur}
    (le point final en cuivre ; les espaces ne comptent pas)."""
    def __init__(self, texte, police='Inter', taille=120, graisse=700, optique=None, couleur_='#141210', interlettrage=0.,
                 interligne=1.08, alignement='centre', largeur_max=None, animateurs=None, couleurs=None, couleurs_car=None, **kw):
        super().__init__(**kw)
        self.texte, self.police, self.taille, self.graisse, self.optique = texte, police, taille, graisse, optique
        self.couleur, self.interlettrage, self.interligne, self.alignement = couleur_, interlettrage, interligne, alignement
        self.largeur_max, self.animateurs, self.couleurs, self.couleurs_car = largeur_max, animateurs or [], couleurs or {}, couleurs_car or {}

    def _disposition(self, t):
        """Unités placées : liste de dict(texte, x, y (ligne de base), car, mot, ligne, couleur) + boîte."""
        ch = _police(self.police); taille = val(self.taille, t); g = val(self.graisse, t); f = _fonte(ch, taille, g, self.optique)
        suivi = val(self.interlettrage, t) * taille; texte = val(self.texte, t)
        lignes = []
        for brut in texte.split('\n'):
            if self.largeur_max:
                cur = ''
                for w in brut.split(' '):
                    essai = (cur + ' ' + w).strip()
                    if cur and f.getlength(essai) + suivi * len(essai) > self.largeur_max: lignes.append(cur); cur = w
                    else: cur = essai
                lignes.append(cur)
            else: lignes.append(brut)
        unites, imot, ic = [], 0, 0
        for il, ligne in enumerate(lignes):
            larg = f.getlength(ligne) + suivi * max(0, len(ligne) - 1)
            x0 = {'gauche': 0, 'centre': -larg / 2, 'droite': -larg}[self.alignement]; y = il * taille * self.interligne
            for k, c in enumerate(ligne):
                if c == ' ': imot += 1; continue
                x = x0 + f.getlength(ligne[:k]) + suivi * k
                unites.append(dict(texte=c, x=x, y=y, car=ic, mot=imot, ligne=il, adv=f.getlength(c), ligne_txt=ligne, x_ligne=x0)); ic += 1
            imot += 1
        return unites, ch, taille, g

    def contenu(self, t, ctx):
        unites, ch, taille, g = self._disposition(t)
        col = couleur(val(self.couleur, t)); par = {a.par for a in self.animateurs} or {'car'}
        cle = 'car' if ('car' in par or self.couleurs_car) else 'mot' if 'mot' in par else 'ligne'
        groupes = {}
        for u in unites: groupes.setdefault(u[cle], []).append(u)
        n = {k: len({u[k] for u in unites}) for k in ('car', 'mot', 'ligne')}
        morceaux = []
        for gid, us in groupes.items():
            e = dict(opacite=1., x=0., y=0., echelle=1., rotation=0., flou=0., suivi=0.)
            for a in self.animateurs:
                s = a.etat(us[0][a.par] if a.par in us[0] else gid, n[a.par], t)
                e = dict(opacite=e['opacite'] * s['opacite'], x=e['x'] + s['x'], y=e['y'] + s['y'], echelle=e['echelle'] * s['echelle'],
                         rotation=e['rotation'] + s['rotation'], flou=e['flou'] + s['flou'], suivi=e['suivi'] + s['suivi'])
            if e['opacite'] <= .002: continue
            c = couleur(self.couleurs_car.get(us[0]['car'], self.couleurs.get(us[0]['mot'], self.couleur))) if cle == 'car' \
                else couleur(self.couleurs.get(us[0]['mot'], self.couleur))
            c = (c[0], c[1], c[2], c[3] * col[3])
            # une tuile par unité : le mot ou la ligne gardent leur crénage (la ligne garde ses espaces)
            txt, x_u = (us[0]['ligne_txt'], us[0]['x_ligne']) if cle == 'ligne' else (''.join(u['texte'] for u in us), us[0]['x'])
            tile, (ox, oy) = _tuile(txt, ch, taille, g, self.optique, c)
            morceaux.append((tile, x_u - ox + e['x'] + e['suivi'] * us[0][cle], us[0]['y'] - oy + e['y'], e, us))
        if not morceaux: return np.zeros((2, 2, 4), np.float32), (1, 1)
        marge = int(taille * .6)
        xs = [x for _, x, _, _, _ in morceaux] + [x + tl.shape[1] for tl, x, _, _, _ in morceaux]
        ys = [y for _, _, y, _, _ in morceaux] + [y + tl.shape[0] for tl, _, y, _, _ in morceaux]
        X0, Y0 = math.floor(min(xs)) - marge, math.floor(min(ys)) - marge
        W, H = math.ceil(max(xs)) - X0 + marge, math.ceil(max(ys)) - Y0 + marge
        im = np.zeros((H, W, 4), np.float32)
        for tile, x, y, e, us in morceaux:
            th, tw = tile.shape[:2]; cx, cy = x - X0 + tw / 2, y - Y0 + th / 2
            M = cv2.getRotationMatrix2D((tw / 2, th / 2), -e['rotation'], e['echelle']); M[0, 2] += cx - tw / 2; M[1, 2] += cy - th / 2
            part = cv2.warpAffine(tile * e['opacite'], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            if e['flou'] > .3: part = _flou(part, e['flou'])
            im = part + im * (1 - part[..., 3:4])
        # ancre par défaut : centre de la boîte du texte au repos (ne bouge pas avec les animateurs)
        repos = [u['x'] for u in unites] + [u['x'] + u['adv'] for u in unites]
        hy = [u['y'] for u in unites]
        ax = (min(repos) + max(repos)) / 2 - X0; ay = (min(hy) + max(hy)) / 2 - taille * .36 - Y0
        return im, (ax, ay)


class Precomp(Calque):
    """Précomposition : une Composition utilisée comme calque (temps local = (t − debut) × vitesse + decalage)."""
    def __init__(self, comp, vitesse=1., decalage=0., **kw): super().__init__(**kw); self.comp, self.vitesse, self.decalage = comp, vitesse, decalage
    def contenu(self, t, ctx):
        im = self.comp.image((t - self.debut) * self.vitesse + self.decalage, ctx_parent=ctx)
        return im, (im.shape[1] / 2, im.shape[0] / 2)


class Reglage(Calque):
    """Calque de réglage : applique ses effets à tout ce qui est en dessous (étalonnage, grain, vignette…)."""
    def contenu(self, t, ctx): return None, (0, 0)


# =============================================================== composition et rendu d'une image
class Composition:
    """Composition : taille (l, h), ips, duree (s), fond (couleur ou None = transparent), calques (du bas vers le haut),
    camera (Camera ou None), flou_mouvement = dict(angle=180, echantillons=8) pour les calques flou_mouvement=True,
    sons = [(t, nom_son_brooze, gain[, args])], musique (format son_brooze), voix (wav), son (fichier déjà mixé)."""
    def __init__(self, l=1080, h=1920, ips=30, duree=3., fond='#EDEBE7', camera=None, flou_mouvement=None):
        self.taille, self.ips, self.duree, self.fond, self.camera = (l, h), ips, duree, fond, camera
        self.flou_mouvement = dict(angle=180, echantillons=8, **(flou_mouvement or {}))
        self.calques, self.sons, self.musique, self.voix, self.son, self.silences = [], [], None, None, None, []
        self.dossier, self.cache = os.getcwd(), os.path.join(os.getcwd(), '_atelier_cache')

    def ajouter(self, calque): self.calques.append(calque); return calque

    def _ctx(self, ctx_parent=None):
        c = dict(taille=self.taille, ips=self.ips, dossier=(ctx_parent or {}).get('dossier', self.dossier),
                 cache=(ctx_parent or {}).get('cache', self.cache), camera=self.camera)
        return c

    def _placer(self, cq, t, ctx):
        im, ancre = cq.contenu(t, ctx)
        if cq.masque is not None:                              # masque en px du contenu (avant les marges d'effets)
            sous, ferme = val(cq.masque, t)
            m, _ = _rasteriser(sous, True, (im.shape[1], im.shape[0]), 1, None, 0, (0, 1), np.zeros(2))
            if val(cq.masque_contour, t) > .3: m = _flou(m, val(cq.masque_contour, t))
            if cq.masque_inverse: m = 1 - m
            im = im * m[..., None]
        if cq.effets:                                          # marge pour l'ombre, la lueur, les flous
            P = 80; im = cv2.copyMakeBorder(im, P, P, P, P, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0)); ancre = (ancre[0] + P, ancre[1] + P)
        for e in cq.effets: im = e.appliquer(im, t, ctx)
        W, H = self.taille
        temps = [t]
        if cq.flou_mouvement:
            fm = self.flou_mouvement; n = fm['echantillons']; ouv = fm['angle'] / 360 / self.ips
            temps = [t + (k / max(1, n - 1) - .5) * ouv for k in range(n)] if n > 1 else [t]
        Ms = [cq.matrice(tt, ctx, None, ancre) for tt in temps]
        coins = np.array([[0, 0, 1], [im.shape[1], 0, 1], [0, im.shape[0], 1], [im.shape[1], im.shape[0], 1]], float).T
        pts = np.hstack([M @ coins for M in Ms])
        cam = ctx.get('camera'); fl = cam.flou(t, val(cq.z, t)) if cam is not None and val(cam.ouverture, t) else 0
        m = int(fl * 3) + 2
        x0, y0 = max(0, int(math.floor(pts[0].min())) - m), max(0, int(math.floor(pts[1].min())) - m)
        x1, y1 = min(W, int(math.ceil(pts[0].max())) + m), min(H, int(math.ceil(pts[1].max())) + m)
        if x1 <= x0 or y1 <= y0: return None
        acc = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
        for M in Ms:
            M2 = (np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]]) @ M)[:2].astype(np.float32)
            acc += cv2.warpAffine(im, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        if len(Ms) > 1: acc /= len(Ms)
        if fl: acc = _flou(acc, fl)
        op = val(cq.opacite, t)
        return (acc * op if op != 1 else acc, x0, y0)

    def image(self, t, ctx_parent=None):
        """Image de la composition à l'instant t (RGBA prémultiplié float32, taille de la composition)."""
        ctx = self._ctx(ctx_parent); W, H = self.taille
        out = np.zeros((H, W, 4), np.float32)
        if self.fond is not None: c = couleur(self.fond); out[:] = (c[0] * c[3], c[1] * c[3], c[2] * c[3], c[3])
        rendus = {}
        def plein(R):                                          # zone utile → plein cadre (pour les caches)
            F = np.zeros((H, W, 4), np.float32)
            if R is not None: a, x0, y0 = R; F[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
            return F
        for cq in self.calques:
            tl = t - cq.decalage_temps
            if not cq.present(tl): continue
            if isinstance(cq, Reglage):
                op = val(cq.opacite, tl); avant = out
                for e in cq.effets: out = e.appliquer(out, tl, ctx)
                if op != 1: out = out * op + avant * (1 - op)
                continue
            if id(cq) not in rendus: rendus[id(cq)] = self._placer(cq, tl, ctx)
            R = rendus[id(cq)]
            if not cq.visible or R is None: continue
            S, x0, y0 = R
            B = out[y0:y0 + S.shape[0], x0:x0 + S.shape[1]]
            if cq.cache is not None:
                src, mode = cq.cache
                if not src.present(t - src.decalage_temps): C = None
                else:
                    if id(src) not in rendus: rendus[id(src)] = self._placer(src, t - src.decalage_temps, ctx)
                    C = plein(rendus[id(src)])[y0:y0 + S.shape[0], x0:x0 + S.shape[1]]
                if C is None: m = np.ones_like(S[..., 3:4]) if mode == 'alpha_inv' else np.zeros_like(S[..., 3:4])
                else: m = C[..., 3:4] if mode.startswith('alpha') else C[..., :3].mean(axis=2, keepdims=True)
                S = S * (1 - m if mode == 'alpha_inv' else m)
            a = S[..., 3:4]
            if cq.fusion == 'normal': B[..., :3] = S[..., :3] + B[..., :3] * (1 - a)
            elif cq.fusion == 'ajout': B[..., :3] = np.minimum(1, B[..., :3] + S[..., :3])
            elif cq.fusion == 'ecran': B[..., :3] = B[..., :3] + S[..., :3] - B[..., :3] * S[..., :3]
            elif cq.fusion == 'produit': B[..., :3] = B[..., :3] * (1 - a) + B[..., :3] * S[..., :3]
            elif cq.fusion == 'incrustation':
                c = S[..., :3] / np.maximum(a, 1e-6); b = B[..., :3]
                o = np.where(b < .5, 2 * b * c, 1 - 2 * (1 - b) * (1 - c))
                B[..., :3] = b * (1 - a) + np.clip(o, 0, 1) * a
            else: raise ValueError(f'fusion inconnue : {cq.fusion}')
            B[..., 3:4] = a + B[..., 3:4] * (1 - a)
        return out

    def image_8bits(self, t):
        im = self.image(t); a = im[..., 3:4]
        rgb = np.where(a > 0, im[..., :3], 0) if self.fond is not None else im[..., :3] / np.maximum(a, 1e-6)
        return (np.clip(rgb, 0, 1) * 255 + .5).astype(np.uint8)
