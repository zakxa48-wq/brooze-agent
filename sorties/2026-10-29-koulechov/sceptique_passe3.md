# Sceptique, passe 3 : L'effet Koulechov

Mesures faites sur reel.mp4 (images extraites avec ffmpeg, lues en pleine résolution). Détail complet dans evaluation_3.json.

## Ce qu'un sceptique écrirait en commentaire
« Le tampon Brooze n'est pas leur vrai logo, c'est juste de la typo. » · « La fin reste figée une seconde et demie sur "Abonne-toi". » · « Le visage glisse hors de l'écran à gauche pendant les 3 scènes. »

## Verdict
**À reprendre, de peu** : le raccord de boucle est à 1 px de la tolérance (bord bas du visage +4 px, +3 px en haut) et la toute dernière image a un saut de taille de 4-5 px. Tout le reste est levé.

## Conditions précédentes
| id | statut | mesure |
|---|---|---|
| V1-1 à V1-7, V1-11, V1-12, V1-14, V1-15 | levées | controle.json sans problème ni alerte ; justifications durée/3D acceptables ; relances max 1,8 s ; grille centrée (écart 1,9 %) |
| V1-13 / V2-3 | **non levée** | image 0 : x 209-870, y 547-1323 ; image 1239 (41.30 s) : x 208-870, y 550-1327 ; dy +3 haut / +4 bas (seuil exigé 2-3 px, stable de 100 à 450 de seuil). Levés : aucun résidu après 41.0, mouvement_fin 2,14, gel max 0,5 s |
| V2-6 | **non levée** | halo absent aux deux bouts (ok) ; mais bord bas +4 px et saut de taille d'une image à 41.27 -> 41.30 (hauteur 767 -> 777, 4-5 px par bord) |
| V1-16 / V2-4 | levées | tampon sans cadre, glyphes = Space Grotesk 700 (rendu de comparaison avec les polices du dépôt), plus de 900, charte.md l.13 nomme Space Grotesk 700 capitales comme typo du wordmark. Suffisant pour un wordmark texte ; fichier officiel absent : Zak à confirmer avant mise en ligne (P3) |
| V2-5 | levée | mot y 1324-1405, pastille y 1470-1571 : écart 65 px, mot lisible en entier (22.9, 23.4, 24.0, 24.6 s) |

## Ce qui tient
Hook visage + « Regarde » dès 0.0 ; storyboard de Zak suivi scène par scène (frites, tombe, chiot, 3 rangées avec flèches, timeline, tampon + bouton) ; sous-titres mot à mot lisibles ; pivot KOULECHOV net ; -14 LUFS, crête -1,4 dBTP ; aucune alerte de glitch ; boucle visuellement propre (visage et halo identiques).

## ORDRE DE CORRECTION
P2-1 · Boucle (V1-13, V2-3, V2-6)
- Où : dernière image 41.30 s
- Faire : décaler le visage final de -3,5 px en y (haut 550 -> 547, bas 1327 -> 1323) et lisser la pulsation sur 41.0-41.33 pour qu'il n'y ait plus de saut de 4-5 px entre 41.27 et 41.30.
- Valider : bbox masque noir y < 1400 de l'image 1239 = bbox image 0 (209-870 / 547-1323) à ±2 px ; écart de bbox entre images consécutives <= 2 px de 40.8 à 41.33.

## Défauts P3 (conseils, ne bloquent pas)
1. 11.4-18.2 s : oreille gauche rognée au bord x=0 par la poussée de caméra, marge droite 15-35 px. Valider : aucun pixel sombre x < 24 ou x > 1056.
2. 22.4-22.87 s : KOULECHOV affiché 0,4 s avant d'être dit (voix à 22.87). Faire entrer le mot plein à 22.8.
3. 36.3-39.1 s : CTA quasi figée (1,05 s puis 1,45 s, diff <= 0,15). Micro-animation toutes les 1,2 s.
4. 0-3 s : pastilles de sous-titres plus larges que le mot (« À » seul dans une grande pastille) ; sous-titre déjà présent à 0.0 alors qu'absent à la dernière image.
5. 32.8-34.2 s : blocs de timeline coupés par les bords pendant l'inversion.
6. Wordmark : demander à Zak une confirmation écrite ou le fichier officiel.

## Ennui (passe « ennui »)
- 0.0-1.4 s : visage calme avec halo ; tient grâce à la pulsation et à la voix, correct (c'est le choix de Zak).
- 7.3-18.2 s : trois paires visage/objet de même composition pendant ~11 s ; l'attention baisse surtout vers 15.5-18.2 (scène du chiot, poussée lente + oreille rognée). Les relances (0,5-1 s) évitent la zone morte mais la composition ne change pas.
- 36.3-37.35 s : 1,05 s figé sur le tampon.
- 37.65-39.1 s : 1,45 s figé juste après le clic, pendant « ton audience pour toi. Abonne-toi. » : la plus forte baisse du Reel, au moment du CTA.
- 39.3-39.8 s : 0,5 s presque figé avant la reprise du halo (acceptable).
- Rien d'autre : de 18.8 à 34 s la grille, les flèches et la timeline relancent toutes les 0,5-1,5 s.

## Limite
Son non écouté au-delà de controle.json (-14 LUFS, -1,4 dBTP, fin -24 dB contre début -16 dB).
