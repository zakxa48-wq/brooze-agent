"""Reel « L'effet Koulechov » (storyboard de Zak) : illustration vectorielle 2D.
Règle de monde : le visage ne change JAMAIS (même calque, même pixel) ; seul l'objet à côté change, et l'émotion suit.
100 % code (Atelier), formes vectorielles, palette Brooze papier / encre / un seul cuivre par image."""
import math
from atelier import *
from atelier import val

IPS = 30; D = 41.39
INK, PAPER, CU, CARD, GREY = '#141210', '#EDEBE7', '#B87333', '#F5F1EA', '#A9A398'
SKIN, FRY = '#E4D3BC', '#F3E9CC'
voix = Voix('mots.json'); T = voix.t
comp = Composition(1080, 1920, ips=IPS, duree=D, fond=PAPER)
# pulsations du fond (derrière tout) : un « battement » d'encre à 5 % sur les mots appuyés, pour relancer l'œil sans toucher au visage
def battement(t0, a=.055):
    comp.ajouter(Solide(INK, debut=t0, fin=t0 + .5, opacite=K((t0, a, lin), (t0 + .45, 0, lin))))

for _i in (13, 18, 21, 24, 26, 30, 36, 38, 41, 46, 60, 63, 68, 71, 74, 77, 79, 83, 88, 91, 95): battement(T(_i))
T_SPLIT, T_ZOOM, T_TL, T_STAMP = T(10) - .05, T(57) - .05, T(84) - .25, T(110) + .1
T_LOOP = D - 1.0

# ---------- caméra du monde (monde = Nul ; rangées : -640 assiette, 0 tombe, 640 chiot)
S = K((0, 1.0, lin), (T_SPLIT, 1.0, doux), (T_SPLIT + .85, 1.25, sortie(3)), (T_ZOOM, 1.38, lin), (T_ZOOM + .95, .62, sortie(3)), (D, .62, lin))
CX = K((0, 0, lin), (T_SPLIT, 0, doux), (T_SPLIT + .85, -160, sortie(3)), (T_ZOOM, -160, doux), (T_ZOOM + .95, -150, sortie(3)), (T(75) - .1, -150, doux), (T(75) + .85, 65, sortie(3)), (D, 65, lin))
CY = K((0, 0, lin), (T_SPLIT, 0, doux), (T_SPLIT + .85, 640, sortie(3)), (T_ZOOM, 640, doux), (T_ZOOM + .95, 370, sortie(3)),
       (T_TL, 370, doux), (T_TL + .6, 2700, expo(6)), (D, 2700, lin))
def SS(t): return val(S, t) * ((1 + .07 * math.exp(-(t - T(68)) * 8)) if T(68) <= t < T(68) + 1.5 else 1)
monde = comp.ajouter(Nul(position=lambda t: (540 - SS(t) * val(CX, t), 960 - SS(t) * val(CY, t)), echelle=SS, fin=T_TL + .8))

def ressort_in(t0, dur=.45, de=0., a=1., f=3.0, am=.5):
    return K((t0, de, ressort(f, am)), (t0 + dur, a, lin))

# ---------- le visage (UN dessin, réutilisé tel quel : jamais animé)
def visage(parent, debut=0, fin=None, op=1):
    kw = dict(parent=parent, debut=debut, fin=fin, opacite=op)
    comp.ajouter(Forme(ellipse(40, 90), remplissage=SKIN, trait=INK, epaisseur=6, position=(-152, 20), **kw))
    comp.ajouter(Forme(ellipse(40, 90), remplissage=SKIN, trait=INK, epaisseur=6, position=(152, 20), **kw))
    comp.ajouter(Forme(ellipse(300, 400), remplissage=SKIN, trait=INK, epaisseur=7, position=(0, 0), **kw))
    comp.ajouter(Forme(svg('M -150 -50 C -150 -230 150 -230 150 -50 C 110 -120 -110 -120 -150 -50 Z'), remplissage=INK, trait=INK, epaisseur=4, position=(0, -20), **kw))
    for sx in (-1, 1):
        comp.ajouter(Forme(ellipse(62, 38), remplissage='#FBF8F2', trait=INK, epaisseur=5, position=(sx * 58, -22), **kw))
        comp.ajouter(Forme(ellipse(20, 20), remplissage=INK, position=(sx * 58, -22), **kw))
        comp.ajouter(Forme(points([(-34, 0), (34, 0)]), remplissage=None, trait=INK, epaisseur=9, position=(sx * 58, -78), **kw))
    comp.ajouter(Forme(points([(0, -30), (-12, 32), (10, 36)]), remplissage=None, trait=INK, epaisseur=5, position=(2, 30), **kw))
    comp.ajouter(Forme(points([(-42, 0), (42, 0)]), remplissage=None, trait=INK, epaisseur=9, position=(0, 112), **kw))

def carte(parent, x, debut=0, fin=None, op=1, l=280, h=420):
    n = Nul(parent=parent, position=(x, 0), debut=debut, fin=fin)
    comp.ajouter(n)
    comp.ajouter(Forme(rect(l, h, 30), remplissage=CARD, trait=INK, epaisseur=5, parent=n, debut=debut, fin=fin, opacite=op))
    return n

# ---------- les objets (coordonnées locales à la carte, 300 × 420)
def assiette(p, debut, fin=None, op=1):
    kw = dict(parent=p, debut=debut, fin=fin, opacite=op)
    comp.ajouter(Forme(ellipse(250, 70), remplissage='#FBF8F2', trait=INK, epaisseur=6, position=(0, 100), **kw))
    comp.ajouter(Forme(ellipse(170, 40), remplissage='#E9E3D8', trait=INK, epaisseur=3, position=(0, 100), **kw))
    for k in range(9):
        a = (k - 4) * 9
        comp.ajouter(Forme(rect(24, 130, 5), remplissage=FRY, trait=INK, epaisseur=4, position=((k - 4) * 21, 42 - abs(k - 4) * 3), rotation=a, **kw))
    for k in range(3):
        def v(t, k=k, ph=k * 1.7):
            pts = []
            for i in range(0, 61, 4):
                pts.append((math.sin(i / 9 + t * 4 + ph) * 9, -i))
            return points(pts)
        comp.ajouter(Forme(v, remplissage=None, trait=GREY, epaisseur=5, position=(-50 + k * 50, -52), **kw))

def tombe(p, debut, fin=None, op=1):
    kw = dict(parent=p, debut=debut, fin=fin, opacite=op)
    comp.ajouter(Forme(points([(-135, 120), (135, 120)]), remplissage=None, trait=INK, epaisseur=6, **kw))
    comp.ajouter(Forme(svg('M -75 120 L -75 -40 C -75 -150 75 -150 75 -40 L 75 120 Z'), remplissage=GREY, trait=INK, epaisseur=7, position=(0, -10), **kw))
    comp.ajouter(Forme(points([(0, -70), (0, 10)]), remplissage=None, trait=INK, epaisseur=9, position=(0, 0), **kw))
    comp.ajouter(Forme(points([(-24, -40), (24, -40)]), remplissage=None, trait=INK, epaisseur=9, position=(0, 0), **kw))
    for k in range(16):
        def ch(t, k=k):
            y = ((t * 520 + k * 61) % 330) - 170
            return points([(0, y), (-6, y + 34)])
        comp.ajouter(Forme(ch, remplissage=None, trait='#5E5A53', epaisseur=3, position=(-125 + k * 17, 0), **kw))

def chiot(p, debut, fin=None, op=1):
    kw = dict(parent=p, debut=debut, fin=fin, opacite=op)
    comp.ajouter(Forme(points([(-135, 125), (135, 125)]), remplissage=None, trait=INK, epaisseur=5, **kw))
    queue = Nul(parent=p, position=(70, 55), rotation=lambda t: 22 * math.sin(t * 17), debut=debut, fin=fin); comp.ajouter(queue)
    comp.ajouter(Forme(ellipse(26, 90), remplissage='#FBF8F2', trait=INK, epaisseur=6, position=(10, -40), rotation=30, parent=queue, debut=debut, fin=fin, opacite=op))
    comp.ajouter(Forme(ellipse(170, 130), remplissage='#FBF8F2', trait=INK, epaisseur=7, position=(0, 70), **kw))
    comp.ajouter(Forme(ellipse(34, 60), remplissage='#FBF8F2', trait=INK, epaisseur=6, position=(-48, 120), **kw))
    comp.ajouter(Forme(ellipse(34, 60), remplissage='#FBF8F2', trait=INK, epaisseur=6, position=(32, 120), **kw))
    comp.ajouter(Forme(ellipse(130, 118), remplissage='#FBF8F2', trait=INK, epaisseur=7, position=(-8, -10), **kw))
    for sx in (-1, 1):
        comp.ajouter(Forme(ellipse(48, 84), remplissage=INK, trait=INK, epaisseur=3, position=(-8 + sx * 66, -32), rotation=sx * 24, **kw))
        comp.ajouter(Forme(ellipse(52, 28), remplissage=None, trait=None, epaisseur=0, position=(0, 0), **kw)) if False else None
        comp.ajouter(Forme(ellipse(18, 22), remplissage=INK, position=(-8 + sx * 26, -22), **kw))
    comp.ajouter(Forme(ellipse(26, 18), remplissage=INK, position=(-8, 4), **kw))
    comp.ajouter(Forme(svg('M -18 18 C -10 34 10 34 18 18'), remplissage=None, trait=INK, epaisseur=5, position=(-8, 4), **kw))
    comp.ajouter(Forme(ellipse(18, 26), remplissage=CU, trait=INK, epaisseur=3, position=(-8, 40), **kw))

OBJETS = {'assiette': assiette, 'tombe': tombe, 'chiot': chiot}

# ---------- 0. hook : le visage, gros plan, au centre (le MÊME dessin que partout)
BUMPS = [k * 1.4 for k in range(int((T_SPLIT - .6) / 1.4) + 1)]
fm = Nul(parent=monde, position=K((0, (0, -20), lin), (T_SPLIT, (0, -20), doux), (T_SPLIT + .85, (-360, 640), sortie(3))),
         echelle=lambda t: val(K((0, 1.7, lin), (T_SPLIT - .25, 2.1, doux), (T_SPLIT, 2.1, doux), (T_SPLIT + .85, 1.0, sortie(3))), t) * (1 + .06 * sum(math.exp(-(t - b) * 7) for b in BUMPS if t >= b)), fin=T_TL + .8)
comp.ajouter(fm)
# ondes cuivre qui partent du visage (relance toutes les 1,4 s : « ding » visuel), avant la séparation
t_r = 0.0
while t_r < T_SPLIT - .6:
    comp.ajouter(Forme(ellipse(560, 700), remplissage='#E9D2B8', trait=CU, epaisseur=14, position=(0, -20), parent=monde,
                       echelle=K((t_r, .75, sortie(3)), (t_r + 1.3, 1.9, lin)), opacite=K((t_r, .75, lin), (t_r + 1.3, 0, lin)),
                       debut=t_r, fin=t_r + 1.35))
    t_r += 1.4
# la carte du visage (rangée du chiot = rangée « vivante ») apparaît dès la séparation
ROW3 = Nul(parent=monde, position=(0, 640), debut=0, fin=T_TL + .8); comp.ajouter(ROW3)
c3f = comp.ajouter(Forme(rect(280, 420, 30), remplissage=CARD, trait=INK, epaisseur=5, parent=monde, position=(-360, 640),
                         opacite=K((T_SPLIT + .45, 0, lin), (T_SPLIT + .85, 1, doux)), fin=T_TL + .8))
visage(fm)   # (ajouté après la carte : au-dessus)
# carte objet, vivante, chaque objet glisse depuis la droite sur le mot qui l'annonce
c3o = comp.ajouter(Forme(rect(280, 420, 30), remplissage=CARD, trait=INK, epaisseur=5, parent=monde, position=(40, 640),
                         opacite=K((T_SPLIT + .45, 0, lin), (T_SPLIT + .85, 1, doux)), fin=T_TL + .8))
T_PLATE, T_TOMB, T_PUPPY = T(17) - .12, T(36) - .35, T(48) - .3
def entree_objet(t0, t1):
    return K((t0, (520, 0), tenir), (t0, (520, 0), expo(6)), (t0 + .5, (0, 0), tenir))
def objet_vivant(nom, debut, fin, mode='droite', punches=()):
    def pos(t):
        dx = dy = 0
        if mode == 'droite': dx = val(K((debut, 640, expo(7)), (debut + .5, 0, tenir)), t)
        if mode == 'haut': dy = val(K((debut, -900, ressort(2.6, .4)), (debut + .7, 0, lin)), t)
        sortie_x = val(K((fin - .5, 0, entree(2.2)), (fin, 640, tenir)), t) if fin < 900 else 0
        return (40 + dx - sortie_x, 640 + dy + 16 * math.sin(t * 5.5) * min(1, max(0, (t - debut - .5) * 2)))
    def ech(t):
        b = val(K((debut, .2, ressort(3.2, .5)), (debut + .6, 1, lin)), t) if mode == 'bas' else 1
        return b * (1 + .1 * sum(math.exp(-(t - q) * 8) for q in punches if t >= q))
    n = Nul(parent=monde, position=pos, echelle=ech, debut=debut, fin=fin + .05 if fin < 900 else None)
    comp.ajouter(n); OBJETS[nom](n, debut, fin + .05 if fin < 900 else None)
    return n
# l'assiette sort quand la tombe arrive (et réciproquement) : la tombe entre sur la voix « tombe »
objet_vivant('assiette', T_PLATE, T_TOMB, 'droite', (T(21), T(24), T(26) - .05))
objet_vivant('tombe', T_TOMB, T_PUPPY, 'haut', (T(38), T(41) - .05))
objet_vivant('chiot', T_PUPPY, 9999, 'bas', (T(53), T(56) - .05))

# point d'interrogation (cuivre, le seul de l'image) qui rebondit sur « quelle émotion »
qm = comp.ajouter(Texte('?', police='Inter', taille=230, graisse=800, couleurs={0: CU}, position=(690, 300), debut=T(6), fin=T_SPLIT + .1,
                        echelle=ressort_in(T(6), .6, .2, 1.0), rotation=lambda t: 8 * math.sin((t - T(6)) * 5),
                        opacite=K((T_SPLIT - .15, 1, lin), (T_SPLIT + .1, 0, lin))))
# ---------- 3. la rangée triple après « Pourtant » (le visage cloné 3 fois)
def rangee(y, nom, t0, mot_emotion, t_mot):
    r = Nul(parent=monde, position=(0, y), debut=t0, fin=T_TL + .8); comp.ajouter(r)
    sc = ressort_in(t0, .55, .6, 1.0)
    rr = Nul(parent=r, echelle=sc, debut=t0, fin=T_TL + .8); comp.ajouter(rr)
    carte(rr, -360, t0); fn = Nul(parent=rr, position=(-360, 0), debut=t0); comp.ajouter(fn); visage(fn, t0)
    co = carte(rr, 40, t0); on = Nul(parent=rr, position=(40, 0), debut=t0); comp.ajouter(on); OBJETS[nom](on, t0)
    # « + » entre visage et objet, « = émotion » à droite
    tp = T(76)
    comp.ajouter(Texte('+', police='Inter', taille=90, graisse=800, position=(-128, 0), parent=rr,
                       opacite=K((tp, 0, lin), (tp + .25, 1, lin)), echelle=ressort_in(tp, .5, .3, 1.0), debut=t0))
    ta = T(76) + .3
    comp.ajouter(Forme(svg('M -360 240 L -360 275 L 470 275 L 470 70'), remplissage=None, trait=INK, epaisseur=7, position=(0, 0), parent=rr,
                       trace_fin=K((ta, 0, doux), (ta + .7, 1, lin)), debut=t0))
    comp.ajouter(Forme(points([(-22, 30), (0, 0), (22, 30)]), remplissage=None, trait=INK, epaisseur=7, position=(470, 62), parent=rr,
                       opacite=K((ta + .6, 0, lin), (ta + .7, 1, lin)), debut=t0))
    comp.ajouter(Texte('=', police='Inter', taille=90, graisse=800, position=(232, 0), parent=rr,
                       opacite=K((t_mot - .1, 0, lin), (t_mot + .15, 1, lin)), debut=t0))
    comp.ajouter(Texte(mot_emotion, police='Inter', taille=100, graisse=800, position=(470, 0), parent=rr,
                       opacite=K((t_mot, 0, lin), (t_mot + .2, 1, lin)), echelle=ressort_in(t_mot, .5, .5, 1.0), debut=t0))
# rangée vivante (chiot) : mêmes « + » et « = » que les deux autres, ajoutés au monde
def formule_vivante(y, mot, t_mot, t0):
    tp = T(76)
    comp.ajouter(Texte('+', police='Inter', taille=90, graisse=800, position=(-128, y), parent=monde, debut=t0, fin=T_TL + .8,
                       opacite=K((tp, 0, lin), (tp + .25, 1, lin)), echelle=ressort_in(tp, .5, .3, 1.0)))
    comp.ajouter(Texte('=', police='Inter', taille=90, graisse=800, position=(232, y), parent=monde, debut=t0, fin=T_TL + .8,
                       opacite=K((t_mot - .1, 0, lin), (t_mot + .15, 1, lin))))
    comp.ajouter(Texte(mot, police='Inter', taille=100, graisse=800, position=(470, y), parent=monde, debut=t0, fin=T_TL + .8,
                       opacite=K((t_mot, 0, lin), (t_mot + .2, 1, lin)), echelle=ressort_in(t_mot, .5, .5, 1.0)))
formule_vivante(640, 'attendri', T(78) + .75, T_ZOOM)
ta3 = T(76) + .3
comp.ajouter(Forme(svg('M -360 880 L -360 915 L 470 915 L 470 710'), remplissage=None, trait=INK, epaisseur=7, parent=monde, debut=T_ZOOM, fin=T_TL + .8,
                   trace_fin=K((ta3, 0, doux), (ta3 + .7, 1, lin))))
comp.ajouter(Forme(points([(-22, 30), (0, 0), (22, 30)]), remplissage=None, trait=INK, epaisseur=7, position=(470, 702), parent=monde, debut=T_ZOOM, fin=T_TL + .8,
                   opacite=K((ta3 + .6, 0, lin), (ta3 + .7, 1, lin))))
rangee(-640, 'assiette', T(57) + .22, 'faim', T(78) - .05)
rangee(0, 'tombe', T(57) + .5, 'triste', T(78) + .35)

# relances de la grille : anneaux cuivre sur les trois visages (jamais changé / Koulechov / cerveau / émotion), mot KOULECHOV
def anneaux(t0):
    for k, y in enumerate((-640, 0, 640)):
        a = t0 + .1 * k
        comp.ajouter(Forme(ellipse(310, 410), remplissage=None, trait=CU, epaisseur=9, position=(-360, y), parent=monde, debut=a, fin=a + .65,
                           echelle=K((a, 1.0, sortie(3)), (a + .6, 1.35, lin)), opacite=K((a, .9, lin), (a + .6, 0, lin))))
for _t in (T(62), T(69), T(71), T(74)): anneaux(_t)
comp.ajouter(Texte('KOULECHOV', police='Inter', taille=100, graisse=800, position=(540, 1338), debut=T(68), fin=T(75) + .15,
                   echelle=ressort_in(T(68), .5, .6, 1.0), opacite=K((T(68), 0, lin), (T(68) + .12, 1, lin), (T(75) - .2, 1, lin), (T(75) + .1, 0, lin))))

# ---------- 4. la timeline (générique : aucune interface de logiciel reconnaissable)
TL = Nul(echelle=.92, position=K((T_TL, (540, 3000), expo(6)), (T_TL + .7, (540, 1000), tenir)), debut=T_TL, fin=T_STAMP + .4); comp.ajouter(TL)
def fade_tl(t): return val(K((T_STAMP - .35, 1, lin), (T_STAMP, 0, lin)), t)
BL = [(150, GREY), (230, INK), (110, '#CFC9BE'), (190, INK), (130, GREY), (140, '#CFC9BE')]
inverse_t = T(101)
def mixc(c1, c2, u):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * u) for x, y in zip(a, b))
for ligne, (y, hh) in enumerate(((-250, 170), (-60, 170))):
    x0 = -490; xs = []
    for k, (w, c) in enumerate(BL): xs.append((x0 + w / 2, w, c)); x0 += w + 6
    for k, (cx0, w, c) in enumerate(xs):
        if ligne == 0 and k == 3: c = CU
        # permutations rapides à partir de « l'ordre » (mot 97), en rythme
        beats = [T(97), T(98) + .1, T(99) + .15, T(100) + .05, T(101) + .0, T(102) + .15, T(104) + .0, T(106) + .1]
        autre = xs[(k + 2 + ligne) % len(xs)][0]; autre2 = xs[(k + 3) % len(xs)][0]
        a1 = xs[(k + 1 + ligne) % len(xs)][0]
        x = K((T(88) - .01, cx0, ressort(2.6, .55)), (T(88) + .35, a1, ressort(2.6, .55)), (T(92) - .01, a1, ressort(2.6, .55)), (T(92) + .35, cx0, ressort(2.6, .55)),
              (beats[0] - .01, cx0, ressort(2.6, .55)), (beats[0] + .35, autre, ressort(2.6, .55)), (beats[1] + .35, cx0 + (autre - cx0) * .0 + (autre2 - cx0) * .3 + 0, ressort(2.6, .55)),
              (beats[2] + .35, autre2, ressort(2.6, .55)), (beats[4] + .35, cx0, ressort(2.6, .55)), (beats[5] + .35, autre, ressort(2.6, .55)), (beats[7] + .4, cx0, lin))
        apres = (PAPER if c == INK else INK) if c in (INK, GREY) else c
        fond = c if c == CU else (lambda t, c=c, apres=apres: mixc(c, apres, min(1, max(0, (t - inverse_t) / .5))))
        comp.ajouter(Forme(rect(w, hh, 14), remplissage=fond, trait=INK, epaisseur=5, position=lambda t, x=x, y=y: (val(x, t), y), parent=TL, opacite=fade_tl, debut=T_TL, fin=T_STAMP + .4))
# piste son (ligne d'onde) et tête de lecture
comp.ajouter(Forme(lambda t: points([(x, math.sin(x / 11 + t * 5) * (8 + 16 * abs(math.sin(x / 70)))) for x in range(-490, 491, 6)]),
                   remplissage=None, trait=INK, epaisseur=5, position=(0, 170), parent=TL, opacite=fade_tl, debut=T_TL, fin=T_STAMP + .4))
comp.ajouter(Forme(points([(0, -310), (0, 230)]), remplissage=None, trait=INK, epaisseur=8,
                   position=lambda t: (-490 + 980 * ((t - T_TL) / (T_STAMP - T_TL)) , 0), parent=TL, opacite=fade_tl, debut=T_TL, fin=T_STAMP + .4))
comp.ajouter(Texte('piste 1', police='Inter', taille=40, graisse=600, position=(-400, -380), parent=TL, opacite=fade_tl, debut=T_TL, fin=T_STAMP + .4))

# ---------- 5. tampon Brooze (wordmark typographique Space Grotesk 700 capitales : le fichier logo n'est pas fourni) + clic « abonne-toi »
t_clac = T(110) + .12
ST = Nul(position=lambda t: (540, 760), rotation=-7, debut=T_STAMP - .5, fin=T_LOOP + .4,
         echelle=K((T_STAMP - .5, 3.2, entree(2)), (t_clac, 1.0, tenir), (t_clac, 1.0, ressort(4, .35)), (t_clac + .3, 1.0, lin))); comp.ajouter(ST)
def fade_end(t): return val(K((T_LOOP - .6, 1, lin), (T_LOOP - .1, 0, lin)), t)
def op_st(t): return min(val(K((T_STAMP - .5, 0, lin), (t_clac - .05, 1, lin)), t), fade_end(t))
comp.ajouter(Texte('BROOZE', police='SpaceGrotesk', taille=170, graisse=700, interlettrage=.12, position=(0, -30), parent=ST, opacite=op_st, debut=T_STAMP - .5, fin=T_LOOP + .4))
comp.ajouter(Texte('PRODUCTION', police='SpaceGrotesk', taille=56, graisse=700, interlettrage=.4, position=(0, 85), parent=ST, opacite=op_st, debut=T_STAMP - .5, fin=T_LOOP + .4))

t_btn, t_clic = T(112) - .1, T(116) + .55
BT = Nul(position=lambda t: (540, 1250), echelle=K((t_btn, .6, ressort(3.2, .5)), (t_btn + .5, 1.0, tenir), (t_clic - .08, 1.0, entree(2)), (t_clic, .93, ressort(3, .5)), (t_clic + .25, 1.0, lin)),
         debut=t_btn, fin=T_LOOP + .4); comp.ajouter(BT)
def op_bt(t): return min(val(K((t_btn, 0, lin), (t_btn + .25, 1, lin)), t), fade_end(t))
cible_btn = lambda t: INK if t < t_clic else CU
comp.ajouter(Forme(rect(560, 150, 75), remplissage=cible_btn, trait=INK, epaisseur=6, parent=BT, opacite=op_bt, debut=t_btn, fin=T_LOOP + .4))
comp.ajouter(Texte('Abonne-toi', police='Inter', taille=64, graisse=800, couleur_=PAPER, position=(0, 0), parent=BT, opacite=op_bt, debut=t_btn, fin=T_LOOP + .4,
                   ))
curseur = Nul(position=K((t_btn + .2, (820, 1700), expo(5)), (t_clic - .05, (600, 1290), tenir)), debut=t_btn + .2, fin=T_LOOP + .4); comp.ajouter(curseur)
comp.ajouter(Forme(points([(0, 0), (0, 70), (18, 54), (32, 86), (44, 80), (31, 49), (54, 47)], True), remplissage=INK, trait=PAPER, epaisseur=5, parent=curseur,
                   opacite=lambda t: min(val(K((t_btn + .2, 0, lin), (t_btn + .45, 1, lin)), t), fade_end(t)), debut=t_btn + .2, fin=T_LOOP + .4))
# anneau de clic
comp.ajouter(Forme(ellipse(60, 60), remplissage=None, trait=INK, epaisseur=5, position=(600, 1290),
                   echelle=K((t_clic, .4, expo(7)), (t_clic + .4, 2.6, lin)), opacite=K((t_clic, .9, lin), (t_clic + .4, 0, lin)), debut=t_clic, fin=t_clic + .45))

# ---------- boucle : le visage du tout début revient, identique au pixel (même fonction, même place, même taille)
# même position, même échelle (1,7 × 1,06) et même halo que la toute première image : la boucle est sans raccord visible
T_FIN = D - .05
BF = [T_LOOP - .05, T_LOOP + .5]
def bosse(t, b):
    u = t - b
    return 0. if u < 0 else math.exp(-u * 7) * min(1., u / .14)   # montée douce : jamais de coupe de taille
# la caméra du moteur (reel/moteur.html : dérive de 18 px vers le haut, zoom de couverture) bouge le plan pendant tout le Reel :
# on la compense sur le visage final pour qu'il retombe pile sur celui de la première image (boucle sans raccord)
def doux_m(p): return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2
def cam_g(t): return doux_m(min(1., max(0., t / D)))
def cam_c(t): return 1.002 + 2 * 18 * cam_g(t) / 1920
def ech_fb(t):
    base = 1.7 * (1 + .06 * sum(bosse(t, b) for b in BF) + .06 * doux_m(min(1, max(0, (t - (T_LOOP + .2)) / (T_FIN - T_LOOP - .2)))))   # gonflement étalé sur 1,1 s (avant : 0,05 s = saut de 6 % sur les 3 dernières images)
    return base * cam_c(0) / cam_c(t)
def pos_fb(t): return (540, 960 + (cam_c(0) * (940 - 960) + 18 * cam_g(t)) / cam_c(t) - 3.5 * cam_g(t))   # -3,5 px : écart mesuré sur le rendu (tentative 3)
fb = Nul(position=pos_fb, echelle=ech_fb, debut=T_LOOP - .05, opacite=1); comp.ajouter(fb)
for _b in (T_LOOP - .05, T_LOOP + .1):   # halos éteints avant la dernière image (comme à l'image 0)
    comp.ajouter(Forme(ellipse(560, 700), remplissage='#E9D2B8', trait=CU, epaisseur=14, position=(540, 940),
                       echelle=K((_b, .75, sortie(3)), (_b + .75, 1.5, lin)), opacite=K((_b, .75, lin), (_b + .75, 0, lin)), debut=_b, fin=_b + .8))
visage(fb, T_LOOP - .05, None)

# ---------- son (sons de la scène ; la voix et le mix final sont refaits par son.py depuis reel.json)
comp.sons = []
comp.voix = None
