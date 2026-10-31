"""Reel « Red Bull = média » : un mur d'écrans (le contenu) et une canette générique (le produit dérivé).
Règle de monde : plus la caméra recule, plus la canette rapetisse devant ce qui la fait vendre. 100 % code (Atelier)."""
import math
from atelier import *
from atelier import val

IPS = 30; D = 46.9
INK, PAPER, CU, GLASS = '#141210', '#EDEBE7', '#B87333', '#0A0908'
voix = Voix('mots.json')
T = voix.t
COLS, ROWS, EW, EH, GAP = 3, 3, 360, 540, 30
CAN_Y = 1500                                   # la canette repose sous le mur (coordonnées du monde)

comp = Composition(1080, 1920, ips=IPS, duree=D, fond=INK)

# ---------- fond papier (charte) du recul jusqu'à la fusion ; l'encre revient pour « émotion »
comp.ajouter(Solide(PAPER, opacite=lambda t: val(K((T(16), 0, lin), (T(18) + .3, 1, lin), (T(98), 1, lin), (T(98) + 1.6, 0, doux)), t) * (0 if t > T(121) else 1)))

# ---------- caméra : (échelle, centre) du monde ; monde = Nul. Une suite de plans, chacun sur un sujet différent
def parcours(depart, evts):
    """depart = (S, cx, cy) ; evts = [(t0, t1, S, cx, cy, courbe)] : part de l'état précédent en t0, y arrive en t1, tient ensuite."""
    ks = [[], [], []]; etat = depart
    for (t0, t1, s_, x_, y_, cb) in evts:
        for k, (a_, b_) in enumerate(zip(etat, (s_, x_, y_))):
            ks[k] += [(t0, a_, cb), (t1, b_, tenir)]
        etat = (s_, x_, y_)
    return ks
EVTS = [
    (T(16), T(18) + .3, .58, 0, 250, sortie(3)),                  # recul : la canette rapetisse devant le mur
    (T(38), T(38) + .4, .6, 0, 270, doux),
    (T(40) - .3, T(40) + .3, 1.9, 0, 0, sortie(3)),               # « quel est leur vrai métier ? » : un seul écran
    (T(45) - .2, T(45) + .05, 1.5, 390, 570, expo(7)),            # « créer du contenu »
    (T(55) - .2, T(55) + .05, 1.9, -390, -570, expo(7)),          # F1
    (T(58) - .22, T(58) + .05, 1.9, 0, -570, expo(7)),            # sauts depuis l'espace
    (T(61) - .2, T(61) + .05, 1.9, 390, -570, expo(7)),           # breakdance
    (T(63) - .2, T(63) + .05, 1.25, 1500, CAN_Y, expo(7)),        # « ne te vendent même pas de la taurine » : la canette seule, barrée
    (T(72) - .3, T(72) + .25, .95, 0, 0, doux),                   # « ils vendent » : retour au mur
    (T(75) - .2, T(75) + .05, 1.8, -390, 0, expo(7)),             # adrénaline
    (T(77) - .2, T(77) + .05, 1.8, -390, 570, expo(7)),           # frisson
    (T(80) - .2, T(80) + .05, 1.8, 390, 0, expo(7)),              # dépassement de soi
    (T(82), T(83) + 1.4, .58, 0, 250, sortie(3)),                 # la canette revient, minuscule
    (T(83) + 1.5, T(98) - .1, .64, 0, 290, doux),
    (T(98), T(108), .9, 0, 0, doux),
    (T(121) + .25, T(121) + .4, 1.5, 0, CAN_Y, tenir),            # boucle : retour au cadrage du début
]
(ks, kx, ky) = parcours((1.58, 0, CAN_Y), EVTS)
S = K((0, 1.50, lin), (T(16) - .01, 1.58, lin), *ks); CX = K((0, 0, lin), *kx); CY = K((0, CAN_Y, lin), *ky)
monde = comp.ajouter(Nul(position=lambda t: (540 - val(S, t) * val(CX, t), 1000 - val(S, t) * val(CY, t)), echelle=lambda t: val(S, t)))

# ---------- contenus d'écran (coordonnées locales de l'écran, 300 × 440 utiles)
def streaks(c, nul, op, off, c1=PAPER):
    for k in range(6):
        y = -190 + k * 76; L = 70 + 30 * ((k * 5 + off) % 4); v = 520 + 90 * ((k + off) % 3); ph = 97 * k
        def ch(t, L=L, v=v, ph=ph, y=y):
            x = -150 + ((t * v + ph) % (300 + L))
            return points([(max(-150, x - L), y), (min(150, x), y)])
        c.ajouter(Forme(ch, remplissage=None, trait=CU if k == 2 else c1, epaisseur=7, parent=nul, opacite=op))
def espace(c, nul, op, off, c1=PAPER):
    arc = [(x, 760 - math.sqrt(580 ** 2 - x * x)) for x in range(-150, 151, 10)]
    c.ajouter(Forme(points(arc + [(150, 225), (-150, 225)], True), remplissage='#1A1714', trait=c1, epaisseur=4, parent=nul, opacite=op))
    c.ajouter(Forme(lambda t: points([(0, -210 + ((t * 140 + off * 70) % 330) - 110), (0, -210 + ((t * 140 + off * 70) % 330))]), remplissage=None, trait=c1, epaisseur=3, parent=nul, opacite=lambda t: .6 * val(op, t)))
    c.ajouter(Forme(ellipse(20, 20), remplissage=CU, parent=nul, opacite=op, position=lambda t: (0, -210 + ((t * 140 + off * 70) % 330))))
def break_(c, nul, op, off, c1=PAPER):
    c.ajouter(Forme(ellipse(250, 250), remplissage=None, trait=c1, epaisseur=3, parent=nul, opacite=lambda t: .35 * val(op, t)))
    for k in range(3):
        c.ajouter(Forme(points([(-115, 0), (115, 0)]), remplissage=None, trait=CU if k == 0 else c1, epaisseur=9, parent=nul, opacite=op,
                        rotation=lambda t, k=k: k * 60 + 260 * t * (1 if off % 2 else -1)))
def pouls(c, nul, op, off, c1=PAPER):
    def ch(t):
        pts = []
        for x in range(-150, 151, 5):
            u = ((x + 150 + t * 190 + off * 40) % 300) / 300
            y = -150 * math.exp(-((u - .5) * 24) ** 2) + 80 * math.exp(-((u - .56) * 30) ** 2)
            pts.append((x, y))
        return points(pts)
    c.ajouter(Forme(ch, remplissage=None, trait=CU, epaisseur=7, parent=nul, opacite=op))
KINDS = [streaks, espace, break_, pouls]

# ---------- le mur
A0 = T(18) + .05
ordre_allumage = [A0 + .3] + [A0 + .0, A0 + .1, A0 + .22, A0 + .12, A0 + .3, A0 + .05, A0 + .36, A0 + .2, A0 + .42, A0 + .15, A0 + .28, A0 + .5]
FUSION = T(98); FIN_FUSION = T(107)
ecrans = []
for i in range(COLS * ROWS):
    col, row = i % COLS, i // COLS
    gx, gy = (col - 1) * (EW + GAP), (row - 1) * (EH + GAP)
    t_on = ordre_allumage[i]
    # panneau qui se resserre en un seul grand écran pendant la fusion
    def pos(t, gx=gx, gy=gy):
        u = val(K((FUSION, 0, lin), (FIN_FUSION - .6, 1, entree(2))), t)
        return (gx * (1 - u), gy * (1 - u))
    nul = comp.ajouter(Nul(position=pos, parent=monde))
    def op(t, t_on=t_on, i=i):
        if t < t_on: return 0.
        u = t - t_on
        if u < .25: return 1. if int(u * 24) % 2 == 0 else .25
        return 1. if t < T(83) + 1 or t > T(83) + 1.4 else .45
    def opacite_verre(t, t_on=t_on): return 1. if t >= t_on else 0.
    base = 1. if i % 2 else .85
    comp.ajouter(Forme(rect(EW, EH, 26), remplissage=GLASS, trait='#3A342E', epaisseur=3, parent=nul, opacite=lambda t, o=opacite_verre: val(o, t)))
    KINDS[(i + row) % 4](comp, nul, lambda t, op=op, base=base: op(t) * base * val(K((FUSION + 1.2, 1, lin), (FUSION + 2.2, 0)), t), i)
    comp.ajouter(Forme(ellipse(22, 22), remplissage='#D8492F', parent=nul, position=(-140, -240), opacite=lambda t, t_on=t_on: (1. if int(t * 1.6 + t_on) % 2 == 0 else .2) * (1 if (t > T(45) and t < FUSION) else 0)))
    ecrans.append(nul)

# ---------- l'écran unique issu de la fusion (le « cadre ») : un grand cadre qui s'allume sur « émotion »
cadre_w, cadre_h = COLS * EW + (COLS - 1) * GAP, ROWS * EH + (ROWS - 1) * GAP
chaud = lambda t: val(K((T(107) - .1, 0, lin), (T(107) + .35, 1, doux), (T(109), .22, doux), (T(121), .22, lin), (T(121) + .25, 0)), t)
cad_op = lambda t: val(K((FUSION + 1.0, 0, lin), (FIN_FUSION, .0), (FIN_FUSION + .3, 1)), t) * (0 if t > T(121) + .25 else 1)
comp.ajouter(Forme(rect(cadre_w, cadre_h, 40), remplissage='#16120F', trait=CU, epaisseur=8, parent=monde, position=(0, 0), opacite=cad_op))
comp.ajouter(Image_('lueur_cuivre.png', parent=monde, position=(0, 0), echelle=1.5, opacite=lambda t: cad_op(t) * .5))
def pouls_geant(t):
    amp = val(K((FIN_FUSION, 0, lin), (T(107), 1.6, doux), (T(111), 1.0, doux), (T(121), 1.25)), t)
    pts = []
    for x in range(-560, 561, 8):
        u = ((x + 560 + t * 420) % 760) / 760
        pts.append((x, amp * (-520 * math.exp(-((u - .5) * 20) ** 2) + 260 * math.exp(-((u - .575) * 26) ** 2))))
    return points(pts)
comp.ajouter(Forme(pouls_geant, remplissage=None, trait=PAPER, epaisseur=16, parent=monde, position=(0, 0), opacite=cad_op))
# ---------- la canette (générique, aucune marque), enfant du monde
cx_can = lambda t: val(K((0, 0, lin), (T(34) - .1, 0, entree(3)), (T(35) + .5, 1500, lin), (T(35) + .6, 1500, lin), (T(83) - .3, 1500, lin), (T(83) + .2, -330, sortie(3)), (T(98), -330, lin), (T(121) + .3, -330, lin), (T(121) + .4, 0, tenir)), t)
cy_can = lambda t: CAN_Y
sc_can = K((0, 1, lin), (T(83), 1, lin), (T(94) - .1, 1, doux), (T(94) + .2, .52, ressort(3, .5)), (T(121) + .3, .52, lin), (T(121) + .4, 1, tenir))
can = comp.ajouter(Nul(position=lambda t: (cx_can(t), CAN_Y + 20 * math.sin(2 * math.pi * t / 4.5) * (1 if t < T(8) else 0)), echelle=sc_can, parent=monde))
# fantôme laissé par la canette (« sous-traitent »)
comp.ajouter(Forme(rect(210, 640, 34), remplissage=None, trait=INK, epaisseur=3, parent=monde, position=(0, CAN_Y),
                   opacite=lambda t: val(K((T(34), 0, lin), (T(34) + .5, .55, lin), (T(83) - .3, .55, lin), (T(83) + .25, 0)), t)))
corps = '#27241F'
comp.ajouter(Forme(rect(210, 560, 34), remplissage=corps, parent=can, position=(0, 0), trait='#4A443C', epaisseur=3,
                   effets=[OmbrePortee(distance=30, angle=90, flou=40, opacite=.5, couleur='#000000')]))
comp.ajouter(Forme(rect(26, 500, 13), remplissage='#F2EEE8', parent=can, position=(-66, 0), opacite=.62, effets=[FlouGaussien(rayon=6)]))
comp.ajouter(Forme(rect(50, 540, 24), remplissage='#1B2A55', parent=can, position=(52, 0), opacite=.45, effets=[FlouGaussien(rayon=12)]))
comp.ajouter(Forme(rect(210, 40, 0), remplissage=CU, parent=can, position=(0, 40)))
comp.ajouter(Forme(points([(-84, -270), (84, -270), (62, -320), (-62, -320)], True), remplissage='#1E1B18', parent=can))
comp.ajouter(Forme(ellipse(124, 26), remplissage='#B9B3AA', parent=can, position=(0, -326)))
comp.ajouter(Forme(ellipse(78, 12), remplissage='#4C4842', parent=can, position=(0, -326)))
comp.ajouter(Forme(rect(210, 16, 8), remplissage='#1A1814', parent=can, position=(0, 272)))
# étiquette « produit dérivé » (forme pure, sans texte), seulement quand elle est tombée du mur
comp.ajouter(Forme(points([(-70, -40), (70, -40), (70, 40), (-70, 40), (-100, 0)], True), remplissage=CU, trait=INK, epaisseur=3, parent=monde,
                   position=(-330 + 105, CAN_Y - 70), rotation=14, echelle=.55, opacite=lambda t: val(K((T(94), 0, lin), (T(94) + .25, 1)), t) * (0 if t > T(121) else 1)))


# « ne te vendent même pas de la taurine » : la canette seule, barrée d'un trait de cuivre qui se dessine
comp.ajouter(Forme(points([(-170, -330), (170, 330)]), remplissage=None, trait=CU, epaisseur=22, parent=monde, position=(1500, CAN_Y),
                   trace_fin=lambda t: val(K((T(66) - .1, 0, lin), (T(66) + .35, 1, expo(6))), t),
                   opacite=lambda t: 1. if (t > T(66) - .1 and t < T(72)) else 0.))
# « ils dépensent des milliards » : des piles de pièces qui montent (aucun chiffre), sur le papier
PILE0, PILE1 = T(48) - .05, T(55) - .12
comp.ajouter(Solide(PAPER, opacite=lambda t: 1. if (t >= PILE0 and t < PILE1) else 0.))
pile = comp.ajouter(Nul(position=(540, 1000), echelle=K((PILE0, 1.0, lin), (PILE1, 1.1, doux))))
HAUT = [9, 15, 11, 6, 13]
for c_, h_ in enumerate(HAUT):
    for j_ in range(h_):
        ta = PILE0 + .05 + j_ * .07 + c_ * .09
        def py(t, j_=j_, ta=ta):
            u = max(0., 1 - (t - ta) / .2)
            return 500 - j_ * 40 - 260 * u * u
        comp.ajouter(Forme(rect(150, 34, 17), remplissage=CU, trait=INK, epaisseur=3, parent=pile,
                           position=lambda t, c_=c_, py=py: ((c_ - 2) * 175, py(t)),
                           opacite=lambda t, ta=ta: 1. if (t >= ta and t < PILE1) else 0.))

# ---------- lumière d'ambiance (dégradés pré-calculés : un flou de 250 px coûterait 2 s par image)
comp.ajouter(Image_('lueur_cuivre.png', position=(540, 980), opacite=lambda t: .55 if (t < T(16) or t > T(122) + .3) else 0.))
comp.ajouter(Image_('lueur_papier.png', position=(540, 1000), opacite=lambda t: .55 * chaud(t), fusion='ajout'))

# ---------- signature : « MÉDIAS » dont les lettres sont des fenêtres sur le contenu
mini = Composition(1080, 1920, ips=IPS, duree=D, fond=INK)
mn = mini.ajouter(Nul(position=(540, 660)))
for k, (kd, sx) in enumerate([(0, -380), (1, 0), (2, 380)]):
    n = mini.ajouter(Nul(position=(sx, 0), parent=mn, echelle=1.9))
    KINDS[[0, 2, 3][k]](mini, n, 1., k, PAPER)
plaque_op = lambda t: val(K((T(24), 0, lin), (T(24) + .12, 1, lin), (T(32) - .2, 1, lin), (T(32) + .15, 0)), t)
comp.ajouter(Forme(rect(1000, 380, 30), remplissage=PAPER, trait=INK, epaisseur=4, position=(540, 660), opacite=plaque_op))
titre = comp.ajouter(Texte('MÉDIAS', police='Inter', taille=270, graisse=K((T(24), 500, lin), (T(24) + .5, 900)), interlettrage=-.04, position=(540, 660), visible=False))
fen = comp.ajouter(Precomp(mini, position=(540, 960), cache=(titre, 'alpha'),
                           opacite=lambda t: val(K((T(24), 0, lin), (T(24) + .12, 1, lin), (T(32) - .2, 1, lin), (T(32) + .15, 0)), t)))

# ---------- les 3 scènes de l'extrême en plein écran (F1, espace, breakdance) : pas de calque supplémentaire, la caméra y va.

# ---------- boîtier de visée (fin) : cadre qui se resserre sur « l'image »
def coins(t):
    u = val(K((T(108), 0, lin), (T(121), 1, doux)), t)
    return u
for sx in (-1, 1):
    for sy in (-1, 1):
        def ch(t, sx=sx, sy=sy):
            u = coins(t); w = 470 - 170 * u; h = 600 - 180 * u
            return points([(sx * w, sy * (h - 90)), (sx * w, sy * h), (sx * (w - 90), sy * h)])
        comp.ajouter(Forme(ch, remplissage=None, trait=PAPER, epaisseur=7, position=(540, 980),
                           opacite=lambda t: val(K((T(108) + .1, 0, lin), (T(108) + .6, .9), (T(121) - .1, .9, lin), (T(121) + .2, 0)), t)))
comp.ajouter(Forme(ellipse(26, 26), remplissage='#D8492F', position=(150, 330),
                   opacite=lambda t: (1. if int(t * 1.6) % 2 == 0 else .15) * val(K((T(108), 0, lin), (T(108) + .5, 1, lin), (T(121) - .1, 1), (T(121) + .15, 0)), t)))

# ---------- extinction de l'écran puis retour au noir (la boucle raccorde avec la première image)
comp.ajouter(Forme(rect(1400, 8), remplissage=PAPER, position=(540, 1000), opacite=lambda t: val(K((T(121) - .05, 0, lin), (T(121) + .02, 1, lin), (T(121) + .17, 0)), t)))
comp.ajouter(Solide(INK, opacite=lambda t: val(K((T(121) + .1, 0, lin), (T(121) + .3, 1, lin), (T(122) + .1, 1, lin), (T(122) + .6, 0)), t)))
# mention de charte (marque réelle analysée) : discrète, en haut, toute la durée
mention_op = lambda t: 0 if (t > T(121) + .1 and t < T(121) + .9) else 1
comp.ajouter(Forme(rect(900, 150, 28), remplissage=INK, position=(540, 225), opacite=lambda t: .88 * mention_op(t)))
comp.ajouter(Texte('analyse indépendante', police='Inter', taille=48, graisse=700, interlettrage=.02, couleur_=PAPER, position=(540, 200), opacite=mention_op))
comp.ajouter(Texte('aucun lien avec la marque', police='Inter', taille=48, graisse=700, interlettrage=.02, couleur_=PAPER, position=(540, 252), opacite=mention_op))
comp.ajouter(Reglage(effets=[Grain(intensite=.035), Vignette(force=.28)]))
