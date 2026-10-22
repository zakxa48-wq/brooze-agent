"""La technique validée « mot-qui-tombe » (essai 4, 8/10) refaite avec l'Atelier et ses gestes : même consigne,
pour vérifier que l'outil sait la reproduire (test de non-régression des gestes)."""
from atelier import *
from atelier.gestes import lire_tomber_frapper, choc, poussee_tenue

IPS = 30; CONTACT = 15.5 / IPS                                 # milieu de l'obturation de l'image 16 (P-035)
g = lire_tomber_frapper(CONTACT)
comp = Composition(1080, 1920, ips=IPS, duree=3.0, fond='#EDEBE7')
comp.ajouter(Texte('Montre-\nle.', taille=218, graisse=800, interlettrage=-.035, interligne=1.0, position=lambda t: (540, 960 + g['descente'](t)),
                   couleurs_car={9: '#B87333'}, echelle=lambda t: g['echelle'](t) * poussee_tenue(.76, 3.0)(t),
                   flou_mouvement=True,
                   effets=[FlouDirectionnel(longueur=g['trainee'], angle=90), OmbrePortee(distance=g['ombre_distance'], angle=60, flou=g['ombre_flou'], opacite=g['ombre_opacite'])]))
comp.ajouter(Reglage(effets=[Decaler(dy=lambda t: -choc(CONTACT, amplitude=11)(t)), Grain(intensite=.03)]))
comp.flou_mouvement = dict(angle=270, echantillons=12)
comp.sons = [(CONTACT - .3, 'air', .5, dict(d=.3)), (CONTACT + .033, 'low_hit', 1.0), (CONTACT + .033, 'tampon', .6)]
