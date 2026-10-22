"""Vitrine de l'Atelier 0.1 : texte animé lettre par lettre, trait qui se dessine, caméra 2,5D, flou de mouvement,
cache de piste, ombre, grain, sons synthétisés. 3 s. Sert aussi de test de non-régression."""
from atelier import *

comp = Composition(1080, 1920, ips=30, duree=3.0, fond='#EDEBE7', camera=Camera(zoom=1500, z=K((0, -40), (3, 60, lin))))
# un cercle cuivre qui tombe derrière le texte (z = 300 : plus loin, plus petit), avec flou de mouvement
rond = comp.ajouter(Forme(ellipse(380, 380), remplissage='#B87333', z=0, flou_mouvement=True,
                          position=K((0, (540, -300), chute(3)), (.55, (540, 760))),
                          echelle=K((.55, (1, 1), lin), (.6, (1.15, .85), sortie(2)), (.8, (1, 1)))))
# le titre, lettre par lettre (animateur), au premier plan
titre = comp.ajouter(Texte("L'atelier", taille=230, graisse=K((.4, 300), (1.2, 850)), interlettrage=-.03, position=(540, 980),
                           animateurs=[Animateur(par='car', debut=.45, decalage=.045, duree=.5, courbe=sortie(4),
                                                 de=dict(opacite=0, y=90, flou=14, rotation=-6))],
                           effets=[OmbrePortee(distance=K((.5, 40), (1.2, 10)), flou=18, opacite=.25)]))
# un trait qui se dessine sous le titre (trim paths)
comp.ajouter(Forme(points([(-330, 0), (330, 0)]), remplissage=None, trait='#141210', epaisseur=10, position=(540, 1112),
                   trace_fin=K((1.1, 0, sortie(3)), (1.6, 1))))
# un sous-titre qui n'apparaît QUE dans le cercle (cache de piste alpha)
comp.ajouter(Texte('BROOZE', taille=58, graisse=800, couleur_='#141210', interlettrage=.12, position=(540, 760),
                   cache=(rond, 'alpha'), animateurs=[Animateur(par='car', debut=1.3, decalage=.05, duree=.4, de=dict(opacite=0, y=-20))]))
comp.ajouter(Reglage(effets=[Grain(intensite=.03), Vignette(force=.18)]))
comp.sons = [(.52, 'air', .5, dict(d=.3)), (.56, 'low_hit', .9), (.58, 'papier', .5), (1.1, 'trait', .4, dict(d=.5)), (1.3, 'pop', .3)]
