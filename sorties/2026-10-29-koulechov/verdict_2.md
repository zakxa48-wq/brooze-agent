# Verdict, tentative 2 : **À REPRENDRE**

## Conditions de la tentative précédente

- V1-1 : **levée** — controle.py ne signale plus : « glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes » · vérifié par controle.py
- V1-2 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-3 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-4 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-5 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-6 : **levée** — justification refusée : refusée : mouvement_fin 0,03 vs 2,62 au début, écart_image 14,7, visage 15 % plus grand à la fin ; défaut P2 41.0–42.39. · vérifié par controle.py (à justifier)
- V1-7 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-11 : **levée** — Un changement visuel net (>= 1 élément qui apparaît/bouge/change d'échelle, énergie engagement.png > 2) posé à 22.39 ±0.15 s sur « Koulechov », ET aucun intervalle sans relance > 3,5 s entre 18.8 et 28.0 (relances.json). · pic d'énergie 26,2 à 22.3-22.4 s (KOULECHOV apparaît, seuil > 2), écart max de relances 1.5 s sur 18.8-28.0 (controle.json). Effet secondaire : le mot est collé sur la pastille de sous-titres (nouveau défaut P2).
- V1-12 : **levée** — L'audio contient « montres » entre 32.92 et 33.13 (ré-extraire la prise ou rendre le raccord naturel) ; les sous-titres lisent « L'ordre dans lequel tu le montres. » puis « Le montage, c'est… » sans fusion ; mots.json à jour et un groupe de sous-titres ne mélange pas deux phrases. · fusion supprimée : mots.json groupes « tu… » g41 et « Le montage, » g42 séparés, frames 32.95 « tu… » puis 33.25 « Le montage, ». « montres » absent de l'audio (RMS -62 dB de 32.85 à 33.25) : impossible à lever côté montage, voir justification. Trou de 0,45 s signalé en P3.
- V1-13 : **non levée** — bbox du visage à la dernière image = bbox à la première (écart <= 2 px, même échelle) ; aucun résidu de tampon ou de bouton sur le visage après 41.0 ; mouvement_fin >= 0,5 (boucle.mouvement_fin) ; plus de 1,2 s sans changement entre 39.3 et 42.4 interdit. · bbox visage : dernière image x 202-876 y 523-1313 vs image 0 x 209-869 y 548-1322 (écart ~25 px à 1080 > tolérance) et halo présent à la fin, absent au début. Levées : pas de pastille ni tampon sur le visage à 40.5-41.1, mouvement_fin 4,63, aucun gel > 1,2 s entre 39.3 et 41.33 (diff 0,10 de 39.5 à 39.8 seulement 0,5 s).
- V1-14 : **levée** — Au moins une relance visible (réaction du visage, objet qui réagit, cadrage) entre 7.0 et 9.5 s ; les trois entrées d'objet ne partagent pas le même mouvement et la même durée de plan à ±0,5 s. · relances 7.3, 8.3, 8.9, 9.3, 9.8 entre 7.0 et 9.5 ; diff d'image 8.0 = 10,5, 8.3 = 13,0 ; entrées d'objet à 5.9/11.1/15.0 avec durées de plan différentes (4.8 / 3.6 / 3.2 s) : contrôle visuel des frames 7.5, 9, 12, 16.
- V1-15 : **levée** — Boîte englobante du contenu centrée à ±5 % de la largeur sur 19.5–25.0 (ou le vide est occupé par un élément voulu). · grille centrée : cartes x 265-780 sur 1080 (centre 522, écart 3 % < 5 %) à 22.9 s ; vide de droite occupé ensuite par les flèches/annotations. Voir P3 zone sûre.
- V1-16 : **non levée** — Soit le vrai fichier logo est utilisé tel quel, soit Zak valide par écrit la version typographique comme « wordmark » (Space Grotesk 700 caps, ou Inter 800) ; plus aucune graisse 900. · graisse 900 corrigée en 800 (scene.py l.230, Inter 800 + PRODUCTION 600) ; mais le tampon cadré (rect incliné, double filet) reste un logo recomposé en typographie, sans fichier ni validation écrite de Zak. Dépendance externe : à signaler à Zak, voir justification.

## Pourquoi ce n'est pas publiable

### V2-3 · P2 · Raccord de boucle visible : le visage final (largeur 247 px à 360 de large, haut 161) est ~15 % plus grand que le visage de la 1re image (largeur 215, haut 186) et décalé ; la première image réintroduit le sous-titre « Regarde » et le halo. À 41.0–41.4 un résidu du bouton (pastille cuivre couleur chair) et le fantôme du tampon traversent le visage. Le clin d'œil déclaré (« même dessin, même place, même taille ») est faux à la mesure. En plus, 39.5→41.4 est immobile (énergie ~0 sur engagement.png) alors que la voix est finie à ~39.3 : ~3 s de vide avant la reprise.
- où : 41.0–42.4 s · source : condition précédente
- preuve : bbox visage : dernière image x 202-876 y 523-1313 vs image 0 x 209-869 y 548-1322 (écart ~25 px à 1080 > tolérance) et halo présent à la fin, absent au début. Levées : pas de pastille ni tampon sur le visage à 40.5-41.1, mouvement_fin 4,63, aucun gel > 1,2 s entre 39.3 et 41.33 (diff 0,10 de 39.5 à 39.8 seulement 0,5 s).
- exigé : —
- **condition pour passer** : bbox du visage à la dernière image = bbox à la première (écart <= 2 px, même échelle) ; aucun résidu de tampon ou de bouton sur le visage après 41.0 ; mouvement_fin >= 0,5 (boucle.mouvement_fin) ; plus de 1,2 s sans changement entre 39.3 et 42.4 interdit.
- piste : Faire revenir le visage à la taille exacte de l'ouverture en glissant pendant que le bouton repart (sans pastille chair), garder une micro-animation (clignement, halo qui commence à enfler) jusqu'à la dernière image, et raccourcir les 3 s de queue après la voix.

### V2-4 · P2 · « Logo » Brooze Production du tampon : recomposé en typo (Inter 900 « BROOZE » + « PRODUCTION » en capitales espacées dans un cadre incliné), fichier logo « non fourni » (scene.py l. 194). La charte : « uniquement le vrai fichier, jamais redessiné ». Un tampon recréé peut être pris pour le logo officiel de l'agence, et la graisse 900 sort de la charte (Inter 800 max).
- où : 35.6–37.0 s · source : condition précédente
- preuve : graisse 900 corrigée en 800 (scene.py l.230, Inter 800 + PRODUCTION 600) ; mais le tampon cadré (rect incliné, double filet) reste un logo recomposé en typographie, sans fichier ni validation écrite de Zak. Dépendance externe : à signaler à Zak, voir justification.
- exigé : —
- **condition pour passer** : Soit le vrai fichier logo est utilisé tel quel, soit Zak valide par écrit la version typographique comme « wordmark » (Space Grotesk 700 caps, ou Inter 800) ; plus aucune graisse 900.
- piste : Demander le fichier à Zak ; en attendant, passer au wordmark Space Grotesk de la charte sans cadre imitant un logo, en gardant le tampon comme geste (CLAC) autour d'un mot, pas d'un faux logo.

### V2-5 · P2 · Le mot-pivot « KOULECHOV » (Inter 800, 100 px, posé à y≈1428) est coupé en deux par la pastille de sous-titre (y≈1470-1570) : la moitié basse des lettres est masquée ou fantomatique, et le sous-titre répète « l'effet Koulechov. » juste dessous. Élément ajouté par la correction de V1-11, donc régression : le moment censé être le pivot ressemble à un bug de calques.
- où : 22.4–24.8 s · source : évaluation indépendante
- preuve : frame 22.9 s en pleine résolution (1080x1920) : lettres K-O-U-L-E-C-H-O-V rognées à mi-hauteur par la pastille ; frame 24.6 : même collision avec « une émotion » ; scene.py l.189 position=(540,1428) vs sous-titres en bas.
- exigé : —
- **condition pour passer** : Sur les images 22.4-24.8 s, aucune intersection entre la boîte du mot KOULECHOV et la pastille de sous-titre (écart >= 40 px, vérifiable en pleine résolution), le mot restant lisible en entier.
- piste : Remonter le mot à y≈1250 (sous la grille, au-dessus des sous-titres) ou le faire disparaître avant l'arrivée de la pastille ; ou supprimer la pastille pendant ce mot.

### V2-6 · P2 · Boucle : le raccord n'est pas à ±2 px. Dernière image (41.33 s) : contour du visage x 202-876, y 523-1313 ; première image (0 s) : x 209-869, y 548-1322, soit visage ~2-4 % plus grand et ~25 px plus haut au sommet. En plus, la dernière image est dominée par un halo cuivre qui sort du cadre alors que l'image 0 n'a aucun halo et réintroduit la pastille « Regarde » : le saut est lisible. Le visage se redimensionne aussi en coupe sèche à 40.9 s (visible sur la planche 40.5 -> 41.1).
- où : 41.0–41.3 s · source : évaluation indépendante
- preuve : mesure sur F_last (41.33 s) et F_0 (0.0 s), masque noir y<1350 : bbox 202-876/523-1313 contre 209-869/548-1322 ; image 40.9 (visage grand + halo) contre 41.1 (visage plus petit, anneau cuivre) ; engagement.json boucle.ecart_image 11.6 (vs 14.7 avant : mieux, non nul).
- exigé : —
- **condition pour passer** : bbox du contour du visage à la dernière image = bbox de l'image 0 à +-3 px à 1080 de large (le halo peut subsister s'il est présent aussi à l'image 0, ou absent aux deux) ; pas de coupe sèche de taille entre 40.8 et 41.33 s.
- piste : Caler l'échelle finale sur celle de l'image 0 (x 209-869) et faire naître le halo dès 0.0 (ou l'éteindre sur les 6 dernières images) ; remplacer la coupe de 40.9 par un glissé.

## Toutes les conditions à remplir pour la tentative suivante (et rien d'autre ne sera exigé, sauf P1 ou régression)

- [ ] V2-3 : bbox du visage à la dernière image = bbox à la première (écart <= 2 px, même échelle) ; aucun résidu de tampon ou de bouton sur le visage après 41.0 ; mouvement_fin >= 0,5 (boucle.mouvement_fin) ; plus de 1,2 s sans changement entre 39.3 et 42.4 interdit.
- [ ] V2-4 : Soit le vrai fichier logo est utilisé tel quel, soit Zak valide par écrit la version typographique comme « wordmark » (Space Grotesk 700 caps, ou Inter 800) ; plus aucune graisse 900.
- [ ] V2-5 : Sur les images 22.4-24.8 s, aucune intersection entre la boîte du mot KOULECHOV et la pastille de sous-titre (écart >= 40 px, vérifiable en pleine résolution), le mot restant lisible en entier.
- [ ] V2-6 : bbox du contour du visage à la dernière image = bbox de l'image 0 à +-3 px à 1080 de large (le halo peut subsister s'il est présent aussi à l'image 0, ou absent aux deux) ; pas de coupe sèche de taille entre 40.8 et 41.33 s.

## Conseils (ne bloquent pas)

- V2-1 : plans trop longs en moyenne → durée moyenne des plans ≤ 3.48 s (couper ou relancer dans les plans longs) (indicatif : moins de 3 références de qualité ≥ 7)
- V2-2 : aucune coupe dans les 3 premières secondes → au moins une coupe ou un changement de plan avant 3 s (indicatif : moins de 3 références de qualité ≥ 7)
- V2-7 : Conséquence de la voix tronquée : trou audio de 0,45 s (RMS -56 à -65 dB de 32.85 à 33.25 s) pendant lequel le sous-titre « tu… » est affiché sans aucun son, puis « Le » est affiché à 33.135 alors que l'audio ne reprend qu'à 33.30 (0,17 s d'avance). Honnêtement géré (ellipse, groupes séparés), mais audible. → Conseil : décaler « Le » à 33.30 et raccourcir le trou à <= 0,2 s ; idéal : demander à Zak de ré-enregistrer « montres » (1 s).
- V2-8 : Inversion de la timeline : la luminance de la zone fait encore un rebond d'une image (162,3 -> 178,7 -> 171,1 -> 177,7 -> 173,5 -> 175,1), pas monotone. Ressemble à un accroc. → Conseil : luminance monotone, rebond <= 2 unités.
- V2-9 : Grille 3x2 : la carte du haut démarre à y≈105 px (et ≈55 px pendant le zoom à 22.4), au-dessus de la zone sûre story (y >= 220), sous l'en-tête Instagram. Les visages débordent aussi de leur carte (oreilles et cheveux hors cadre), pas les objets. → Conseil : tout le contenu entre y 220 et 1700, visage contenu dans sa carte.
- V2-10 : Ennui de fin : de 36.5 à 39.2 s l'image est quasi figée (diff d'image 0,06-0,14) hormis le clic à 37.3-37.6 ; 1,4 s d'immobilité totale 37.8-39.2 sur le tampon et le bouton, pendant la CTA « manipuler ton audience pour toi. Abonne-toi. ». Le fondu du tampon à 35.8-36.4 superpose aussi un tampon géant translucide sur la timeline (0,6 s de bouillie). → Conseil : une micro-animation (tampon qui vibre, curseur qui se déplace, bouton qui pulse) toutes les 1,2 s.
