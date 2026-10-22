"""Essai 4 — « Montre-le. » en TROIS TEMPS, un rôle chacun (retour de Zak sur l'essai 3, verdict-zak.md).
Déterministe : l'image k ne dépend que de t = k/30 (graines fixes). Python + Pillow + numpy, son par son_brooze.py.
  python3 rendu.py <dossier_sortie>      → essai.mp4 (1080×1920, 30 i/s, 3,0 s, h264 yuv420p + aac)
  1. LIRE   (0 → 0,317 s) : mot entier, net, en hauteur (échelle 1,26, ombre loin et pâle), immobile ; de 0,18 s à
     0,317 s il remonte de 1,5 % (anticipation), rien d'autre.
  2. TOMBER (0,317 → 0,517 s, 6 images) : chute en t³ de 1,28 à 1,0, flou d'échelle + traînée verticale forte (55 px).
  3. FRAPPER (0,517 s, dans l'obturateur de l'image 16) : arrêt sec, choc 12 px (montée 12 ms filée sur l'obturateur, retour amorti critique), ombre qui claque (diffuse jusqu'au bout, serrée et dense
     à l'image du contact), grave plus marqué ; puis la tenue vivante de l'essai 3 (poussée 1,8 %).
Mise en page : sur deux lignes, coupées au trait d'union (« Montre- / le. »). Calcul : sur une ligne, à ≥ 150 px de
haut, le mot fait 1 003 px de large et ne peut pas être lu entier au-dessus de 1,07× ; sur deux lignes, « Montre- »
fait 807 px et reste entier jusqu'à 1,29×.
Inchangés depuis l'essai 3 : palette, police (Inter 800, 218 px, −3,5 %), papier et grain, poussée de tenue, contact
pendant l'image 16 et son calé pendant l'affichage de cette image (16,5/30 s).
"""
import sys, os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/user/brooze-agent/reel/.outils')
import son_brooze as S

W, H, FPS, DUREE = 1080, 1920, 30, 3.0
N = int(round(FPS * DUREE))
PAPIER = np.array([0xED, 0xEB, 0xE7], np.float32); ENCRE = np.array([0x14, 0x12, 0x10], np.float32)
CUIVRE = np.array([0xB8, 0x73, 0x33], np.float32); OMBRE = np.array([0x2A, 0x24, 0x1E], np.float32)
LIGNES, TAILLE_POLICE, INTERLETTRE, INTERLIGNE = ['Montre-', 'le.'], 218, -0.035, 0.92
T_CONTACT = 15.5 / FPS        # contact au milieu de l'obturateur de l'image 16 : elle porte la fin de la traînée (le coup
                              # se SENT dans l'image la plus rapide), l'image 17 est la première posée et nette
T_ANTICIPE, T_CHUTE = T_CONTACT - 0.337, T_CONTACT - 0.2   # anticipation 0,18 → 0,317 s, chute de 0,2 s (6 images)
ECHELLE_LIRE, ANTICIPE = 1.26, 0.015  # échelle pendant la lecture ; remontée de 1,5 % juste avant de tomber
PUISSANCE = 3.                      # chute très accélérée : la vitesse se concentre sur les dernières images
CHOC_PX, CHOC_TAU = 12., 0.035
DERIVE_PX = 34.               # à h = 1 le mot est 34 px plus bas : il remonte vers sa place en tombant (perspective)
FLOU_V_PX = 55.               # traînée verticale à la vitesse de contact (flou directionnel en plus du flou d'échelle)
POUSSEE, POUSSEE_DEBUT = 0.018, T_CONTACT + 0.25
SOUS, OBTU = 16, 0.75

# ---------- le mot, rendu une fois en grand (2×), interlettrage serré ----------
SUR = 2
police = ImageFont.truetype('/root/.cache/brooze/polices/Inter.ttf', TAILLE_POLICE * SUR)
police.set_variation_by_axes([32, 800])
track = INTERLETTRE * TAILLE_POLICE * SUR
larg = lambda l: police.getlength(l) + track * (len(l) - 1)
pas_ligne = INTERLIGNE * TAILLE_POLICE * SUR
lw = int(max(larg(l) for l in LIGNES) + 80 * SUR); lh = int(police.getbbox('Mg')[3] + pas_ligne * (len(LIGNES) - 1) + 40 * SUR)
m_encre = Image.new('L', (lw, lh)); m_point = Image.new('L', (lw, lh)); de, dp = ImageDraw.Draw(m_encre), ImageDraw.Draw(m_point)
for n, ligne in enumerate(LIGNES):   # lignes centrées, le point final en cuivre
    x0 = (lw - larg(ligne)) / 2
    for i, c in enumerate(ligne):
        x = x0 + police.getlength(ligne[:i]) + track * i      # crénage de la police + interlettrage
        (dp if c == '.' and n == len(LIGNES) - 1 else de).text((x, 20 * SUR + n * pas_ligne), c, font=police, fill=255)
m_encre, m_point = np.asarray(m_encre, np.float32) / 255, np.asarray(m_point, np.float32) / 255
m_tout = np.maximum(m_encre, m_point)
ys, xs = np.nonzero(m_tout > .5)
cx_mot, cy_mot = (xs.min() + xs.max()) / 2 / SUR, (ys.min() + ys.max()) / 2 / SUR
LARGEUR_MOT, HAUTEUR_MOT = (xs.max() - xs.min()) / SUR, (ys.max() - ys.min()) / SUR
CENTRE = np.array([W / 2, H * 0.47])
# centre d'encre (barycentre des pixels) du mot posé, dans le cadre : point fixe de la poussée caméra
CENTRE_ENCRE = CENTRE + (np.array([(m_tout * np.arange(m_tout.shape[1])).sum() / m_tout.sum(), (m_tout * np.arange(m_tout.shape[0])[:, None]).sum() / m_tout.sum()]) / SUR - [cx_mot, cy_mot])

# ---------- le papier : fibres fixes (le grain vivant est ajouté après la caméra) ----------
def bruit_basse(freq, graine):
    r = np.random.default_rng(graine); g = r.standard_normal((H // freq + 2, W // freq + 2)).astype(np.float32)
    return np.asarray(Image.fromarray(g).resize((W + 2 * freq, H + 2 * freq), Image.BICUBIC))[:H, :W]
fibres = (bruit_basse(90, 1) * 1.1 + bruit_basse(6, 2) * 1.4)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vign = -10 * (((xx - W / 2) / (W * .75)) ** 2 + ((yy - H / 2) / (H * .75)) ** 2)
FOND = PAPIER[None, None, :] + (fibres + vign)[..., None]

H_HAUT = (ECHELLE_LIRE * (1 + ANTICIPE) - 1)       # « hauteur » = échelle − 1
def hauteur(t):
    """échelle − 1 : lecture immobile, anticipation (remontée douce), chute en t^PUISSANCE, 0 une fois posé."""
    if t >= T_CONTACT: return 0.
    h_lire = ECHELLE_LIRE - 1
    if t < T_ANTICIPE: return h_lire
    if t < T_CHUTE:
        u = (t - T_ANTICIPE) / (T_CHUTE - T_ANTICIPE); return h_lire + (H_HAUT - h_lire) * u * u * (3 - 2 * u)
    u = (t - T_CHUTE) / (T_CONTACT - T_CHUTE)
    return H_HAUT * (1 - u ** PUISSANCE)

def vitesse(t):
    """vitesse de chute normalisée (1 au contact), 0 en lecture et une fois posé."""
    if t >= T_CONTACT or t < T_CHUTE: return 0.
    return ((t - T_CHUTE) / (T_CONTACT - T_CHUTE)) ** (PUISSANCE - 1)

CHOC_MONTEE = 0.012           # la caméra encaisse le coup en 12 ms (pas de téléportation), puis revient
def choc(t):
    """décalage caméra vertical (px) : montée très courte au contact, puis retour amorti de façon critique (aucun
    dépassement). Intégré sur l'obturateur (voir image) : l'image du contact porte le filé vertical du choc."""
    u = t - T_CONTACT
    if u < 0: return 0.
    if u < CHOC_MONTEE: return CHOC_PX * math.sin(math.pi / 2 * u / CHOC_MONTEE)
    u -= CHOC_MONTEE
    return CHOC_PX * (1 + u / CHOC_TAU) * math.exp(-u / CHOC_TAU)

def poussee(t):
    """zoom caméra lent pendant la tenue : démarrage doux (ease-in-out), 1 → 1 + POUSSEE à la fin."""
    u = min(1., max(0., (t - POUSSEE_DEBUT) / (DUREE - POUSSEE_DEBUT)))
    return 1 + POUSSEE * u * u * (3 - 2 * u)

def place(m, ech, cx, cy, flou=0):
    """masque (2×) à l'échelle ech, centre du mot en (cx, cy), dans le repère du papier (1080×1920)."""
    a = SUR / ech; ox = cx - ech * cx_mot; oy = cy - ech * cy_mot
    img = Image.fromarray(m if m.dtype == np.uint8 else (m * 255).astype(np.uint8))
    out = img.transform((W, H), Image.AFFINE, (a, 0, -ox * a, 0, a, -oy * a), Image.BICUBIC)
    if flou > .5: out = out.filter(ImageFilter.GaussianBlur(flou))
    return np.asarray(out, np.float32) / 255

def ombre(t):
    """lumière en haut à gauche. En hauteur : loin, large, pâle. Pendant la chute elle reste diffuse jusqu'au bout
    (racine de la hauteur), puis CLAQUE : serrée et dense à l'image du contact."""
    h = (hauteur(t) / H_HAUT) ** .5
    o = place(m_tout, 1 + .25 * h * H_HAUT, CENTRE[0] + 4 + 70 * h, CENTRE[1] + 6 + 150 * h + DERIVE_PX * h, flou=2.5 + 34 * h)
    return o * (0.40 - 0.22 * h)                 # 18 % en hauteur → 40 % au contact

def image(k):
    t = k / FPS
    enc = np.zeros((H, W), np.float32); pt = np.zeros((H, W), np.float32)
    sous = SOUS if T_CHUTE < t and t - OBTU / FPS < T_CONTACT else 1   # sous-images seulement pendant la chute
    for j in range(sous):   # obturateur 270°, traînant : [t − ¾ image, t] → flou d'échelle (radial)
        tj = t - OBTU / FPS * (1 - (j + .5) / sous)
        hj = hauteur(max(tj, 0.)); ech = 1 + hj
        vj = vitesse(max(tj, 0.))                       # 0 → 1 au contact
        cyj = CENTRE[1] + DERIVE_PX * hj / H_HAUT - FLOU_V_PX * vj * ((j + .5) / sous - .5)
        enc += place(m_encre, ech, CENTRE[0], cyj); pt += place(m_point, ech, CENTRE[0], cyj)
    enc /= sous; pt /= sous
    a_o = ombre(t)[..., None]
    scene = FOND * (1 - a_o) + OMBRE * a_o
    a_e, a_p = enc[..., None], pt[..., None]
    scene = scene * (1 - a_e - a_p) + ENCRE * a_e + CUIVRE * a_p
    # caméra : poussée lente centrée sur le centre d'encre du mot + choc vertical (le mot reste fixe sur le papier) ;
    # le papier est prolongé de 64 px hors champ (miroir) pour que le choc ne découvre jamais de bord (P-033).
    # Pendant le choc, la caméra est intégrée sur l'obturateur (8 sous-images) : filé vertical du coup.
    cx, cy = CENTRE_ENCRE; M = 64
    src = Image.fromarray(np.pad(np.clip(scene, 0, 255).astype(np.uint8), ((M, M), (M, M), (0, 0)), mode='reflect'))
    temps_cam = [t - OBTU / FPS * (1 - (j + .5) / 8) for j in range(8)] if 0 < t - T_CONTACT < .1 else [t]
    out = np.zeros((H, W, 3), np.float32)
    for tc in temps_cam:
        z = poussee(tc); dy = choc(tc); a = 1 / z
        out += np.asarray(src.transform((W, H), Image.AFFINE, (a, 0, cx - cx * a + M, 0, a, cy - (cy + dy) * a + M), Image.BICUBIC), np.float32)
    out /= len(temps_cam)
    # grain vivant (capteur : change à chaque image, graine = numéro d'image)
    g = np.random.default_rng(1000 + k).standard_normal((H // 2, W // 2)).astype(np.float32)
    out = out + (np.repeat(np.repeat(g, 2, 0), 2, 1) * 2.6)[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

def limiteur(x, reduction_db, anticipe=.002, relache=.06):
    """limiteur de crête transparent : gain ≤ 1 calculé à l'avance (2 ms), retour exponentiel (60 ms). Ne touche
    que les crêtes au-dessus du seuil ; pas d'écrêtage, pas de saturation (le signal n'est jamais déformé)."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    env = np.abs(x).max(1); seuil = env.max() * 10 ** (-reduction_db / 20)
    g = np.minimum(1., seuil / np.maximum(env, 1e-9))
    n = int(anticipe * S.SR); g = minimum_filter1d(g, 2 * n + 1); g = uniform_filter1d(g, n + 1)
    k = 1 - math.exp(-1 / (relache * S.SR)); y = np.empty_like(g); v = 1.
    for i in range(len(g)):
        v = g[i] if g[i] < v else v + (1 - v) * k; y[i] = v
    return x * np.minimum(y, g)[:, None]

def son(chemin):   # essai 4 : grave plus marqué, souffle limité à la chute
    n = int(S.SR * DUREE); fx = np.zeros((n, 2))
    r = np.random.default_rng(5)
    salle = S.lp(r.standard_normal(n), 900) * 10 ** (-56 / 20); fx += np.stack([salle, np.roll(salle, 311)], 1)   # air de la pièce dès 0 s
    S.at(fx, S.air(.26, .2), 16.5 / FPS - .26)                 # la chute (6 images), coupée net avant le contact
    tc = 16.5 / FPS               # pendant l'affichage de la première image posée (16) : l'oreille et l'œil ensemble
    S.at(fx, S.choc_granit(1.0), tc)                           # le poids
    S.at(fx, S.low_hit(1.0, 40), tc)                           # le grave sous le mot (plus marqué qu'à l'essai 3)
    S.at(fx, S.tampon(.5), tc)                                 # corps mat du coup
    S.at(fx, S.papier(.5, 2600), tc)                           # la matière : papier
    fx = S.hp(fx, 30, 2)
    fx = limiteur(fx, 10.)                                      # −10 dB sur les seules crêtes : le grave gagne en présence
    pic = np.abs(fx).max(); fx = fx / pic * 10 ** (-1.6 / 20)  # crête −1,6 dBFS, sans écrêtage ni saturation
    import soundfile as sf; sf.write(chemin, fx.astype(np.float32), S.SR)

if __name__ == '__main__':
    # --sans-poussee : rendu de CONTRÔLE (mesure du geste seul), identique à tout point de vue sauf la poussée de tenue
    if '--sans-poussee' in sys.argv: sys.argv.remove('--sans-poussee'); POUSSEE = 0.
    sortie = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(sortie, exist_ok=True)
    print(f'mot : {LARGEUR_MOT:.0f} × {HAUTEUR_MOT:.0f} px (encre seule, à l\'échelle 1)', file=sys.stderr)
    wav = os.path.join(sortie, '_son.wav'); son(wav)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-i', wav, '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                           '-t', str(DUREE), '-movflags', '+faststart', os.path.join(sortie, 'essai.mp4')], stdin=subprocess.PIPE)
    for k in range(N): ff.stdin.write(image(k).tobytes())
    ff.stdin.close(); ff.wait(); os.remove(wav)
