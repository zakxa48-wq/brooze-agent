"""Essai 3 (= essai 2 + une correction) — « Montre-le. » qui tombe VERS le papier (axe de profondeur), avec du poids.
Déterministe : l'image k ne dépend que de t = k/30 (graines fixes). Python + Pillow + numpy, son par son_brooze.py.
  python3 rendu.py <dossier_sortie> [--sans-poussee]      → essai.mp4 (1080×1920, 30 i/s, 3,0 s, h264 yuv420p + aac)
Essai 3, verdict 2 : mise à l'échelle centrée sur le mot, mot entier dans le cadre dès 0,3 s (voir CHUTE).
Changements demandés par le verdict 1 :
  1. chute en profondeur : échelle 1,093 → 1,0 (essai 3), même chute accélérée, dérive de 34 px ; flou d'échelle (16 sous-images)
     + traînée verticale proportionnelle à la vitesse (26 px au contact) ;
  2. ombre lisible : large, pâle, décalée quand le mot est haut ; dense (38 %), serrée, collée au contact ;
  3. choc caméra 11 px, amorti critique ;
  4. tenue vivante : poussée de caméra lente de 1,8 % (démarrage doux), mot immobile par rapport au papier ;
  5. taille finale ≥ 150 px (police 218, interlettrage −3,5 % pour garder des marges).
Inchangés : palette, point cuivre, papier et grain, son et son calage, contact à 0,507 s.
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
TEXTE, TAILLE_POLICE, INTERLETTRE = 'Montre-le', 218, -0.035
T_CONTACT = 15.2 / FPS        # contact entre les obturateurs des images 15 et 16 : l'image 16 est la première posée, nette
# Essai 3 : le mot doit être entier dans le cadre dès 0,3 s (1003 px de large → échelle ≤ 1,077), avec une chute
# qui accélère jusqu'au même contact. Une chute qui accélère parcourt moins de chemin avant 0,3 s qu'après, donc
# l'échelle de départ est plafonnée vers 1,1. Puissance 3 : la vitesse se concentre à la fin (vitesse au contact
# 0,50 /s d'échelle, contre 0,33 avec une chute en t² de même contrainte).
CHUTE = 0.557                 # durée de chute virtuelle (le mot est déjà en mouvement à t = 0)
PUISSANCE = 3.
ECHELLE_HAUT = 0.093          # à h = 1 : 1,093 × ; 1,070 × à 0,3 s → mot entier (rognage symétrique de 8 px avant)
CHOC_PX, CHOC_TAU = 11., 0.035
DERIVE_PX = 34.               # à h = 1 le mot est 34 px plus bas : il remonte vers sa place en tombant (perspective)
FLOU_V_PX = 26.               # traînée verticale à la vitesse de contact (flou directionnel en plus du flou d'échelle)
POUSSEE, POUSSEE_DEBUT = 0.018, T_CONTACT + 0.25
SOUS, OBTU = 16, 0.75

# ---------- le mot, rendu une fois en grand (2×), interlettrage serré ----------
SUR = 2
police = ImageFont.truetype('/root/.cache/brooze/polices/Inter.ttf', TAILLE_POLICE * SUR)
police.set_variation_by_axes([32, 800])
track = INTERLETTRE * TAILLE_POLICE * SUR
lw = int(police.getlength(TEXTE + '.') + 80 * SUR); lh = int(police.getbbox(TEXTE + '.')[3] + 40 * SUR)
m_encre = Image.new('L', (lw, lh)); m_point = Image.new('L', (lw, lh)); de, dp = ImageDraw.Draw(m_encre), ImageDraw.Draw(m_point)
for i, c in enumerate(TEXTE + '.'):
    x = 20 * SUR + police.getlength((TEXTE + '.')[:i]) + track * i      # crénage de la police + interlettrage
    (dp if c == '.' else de).text((x, 20 * SUR), c, font=police, fill=255)
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

def hauteur(t):
    """h(t) = 1 − (s/CHUTE)^PUISSANCE : chute qui accélère jusqu'au contact, déjà engagée à t = 0, 0 une fois posé."""
    if t >= T_CONTACT: return 0.
    s = CHUTE - T_CONTACT + t
    return 1 - (s / CHUTE) ** PUISSANCE

def vitesse(t):
    """vitesse de chute normalisée (1 au contact), 0 une fois posé."""
    if t >= T_CONTACT: return 0.
    return ((CHUTE - T_CONTACT + t) / CHUTE) ** (PUISSANCE - 1)

def choc(t):
    """décalage caméra vertical (px) : plein au contact, retour amorti de façon critique (aucun dépassement)."""
    u = t - T_CONTACT
    if u < 0: return 0.
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
    """lumière en haut à gauche, plus haute que le mot : loin, large et pâle en haut ; dense et collée au contact."""
    h = hauteur(t); ech = 1 + .25 * h            # l'ombre grandit moins vite que le mot (elle est sur le papier)
    o = place(m_tout, ech, CENTRE[0] + 4 + 70 * h, CENTRE[1] + 6 + 150 * h + DERIVE_PX * h, flou=2.5 + 34 * h)
    return o * (0.38 - 0.18 * h)                 # 20 % en haut → 38 % au contact

def image(k):
    t = k / FPS
    enc = np.zeros((H, W), np.float32); pt = np.zeros((H, W), np.float32)
    sous = 1 if t - OBTU / FPS > T_CONTACT else SOUS
    for j in range(sous):   # obturateur 270°, traînant : [t − ¾ image, t] → flou d'échelle (radial)
        tj = t - OBTU / FPS * (1 - (j + .5) / sous)
        hj = hauteur(max(tj, 0.)); ech = 1 + ECHELLE_HAUT * hj
        vj = vitesse(max(tj, 0.))                       # 0 → 1 au contact
        cyj = CENTRE[1] + DERIVE_PX * hj - FLOU_V_PX * vj * ((j + .5) / sous - .5)
        enc += place(m_encre, ech, CENTRE[0], cyj); pt += place(m_point, ech, CENTRE[0], cyj)
    enc /= sous; pt /= sous
    a_o = ombre(t)[..., None]
    scene = FOND * (1 - a_o) + OMBRE * a_o
    a_e, a_p = enc[..., None], pt[..., None]
    scene = scene * (1 - a_e - a_p) + ENCRE * a_e + CUIVRE * a_p
    # caméra : poussée lente centrée sur le centre d'encre du mot + choc vertical (le mot reste fixe sur le papier) ;
    # le papier est prolongé de 64 px hors champ (miroir) pour que le choc ne découvre jamais de bord
    z = poussee(t); dy = choc(t); cx, cy = CENTRE_ENCRE; M = 64
    a = 1 / z; img = Image.fromarray(np.pad(np.clip(scene, 0, 255).astype(np.uint8), ((M, M), (M, M), (0, 0)), mode='reflect'))
    img = img.transform((W, H), Image.AFFINE, (a, 0, cx - cx * a + M, 0, a, cy - (cy + dy) * a + M), Image.BICUBIC)
    out = np.asarray(img, np.float32)
    # grain vivant (capteur : change à chaque image, graine = numéro d'image)
    g = np.random.default_rng(1000 + k).standard_normal((H // 2, W // 2)).astype(np.float32)
    out = out + (np.repeat(np.repeat(g, 2, 0), 2, 1) * 2.6)[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)

def son(chemin):   # inchangé depuis l'essai 1
    n = int(S.SR * DUREE); fx = np.zeros((n, 2))
    r = np.random.default_rng(5)
    salle = S.lp(r.standard_normal(n), 900) * 10 ** (-56 / 20); fx += np.stack([salle, np.roll(salle, 311)], 1)   # air de la pièce dès 0 s
    S.at(fx, S.air(16.5 / FPS, .18), 0.0)                      # la chute, coupée net avant le contact
    tc = 16.5 / FPS               # pendant l'affichage de la première image posée (16) : l'oreille et l'œil ensemble
    S.at(fx, S.choc_granit(1.0), tc)                           # le poids
    S.at(fx, S.low_hit(.55, 44), tc)                           # le grave sous le mot
    S.at(fx, S.papier(.5, 2600), tc)                           # la matière : papier
    fx = S.hp(fx, 30, 2)
    pic = np.abs(fx).max(); fx = fx / pic * 10 ** (-1.6 / 20)  # crête −1,6 dBFS, rien de limité
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
