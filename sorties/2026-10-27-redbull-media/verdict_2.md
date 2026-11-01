# Verdict, tentative 2 : **À REPRENDRE**

## Conditions de la tentative précédente

- V1-1 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-2 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-3 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-4 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-5 : **levée** — corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications) · vérifié par controle.py (à justifier)
- V1-6 : **non levée** — entre 12 et 36 s, au moins 6 images visuellement différentes (cadrage, échelle ou sujet), aucune ne restant plus de 4 s, et chaque idée dite par Zak (dépenser, ne pas vendre, vendre) a son image propre · Entre 12 et 36 s on compte bien ≥ 6 images différentes (mur zoomé, carte pendule, carte roue, pièces, canette barrée, cartes F1 / frisson / dépassement) et dépenser / ne pas vendre / vendre-émotion ont chacune leur image. Mais le mur 3x3 reste 5,4 s (29,6–35,0) avec un simple zoom 1,12→1,05 : la condition « aucune ne reste plus de 4 s » n'est pas tenue, et « produit dérivé » n'a pas d'image propre.
- V1-7 : **levée** — au moins un tiers de la durée sur fond clair (papier de la charte), OU une justification de direction artistique dans reel.json « justifications » (« palette ») acceptée par l'évaluation suivante · Mesure sur 10 images/s : fond clair visible sur les bords 20,6 s sur 46,7 s (44 %) : 5,4–12,5 ; 15,4–18,4 ; 20,6–24,7 ; 29,2–34,3. Seuil d'un tiers (15,6 s) tenu. Le chiffre de 63 % de la justification est inexact (les gros plans de cartes noires, 12,5–15,4 et 24,7–29 s, couvrent l'écran) mais la 1re branche de la condition suffit.
- V1-8 : **levée** — entre 6 et 8 s, un sujet occupe au moins un quart de l'écran · 6,5 s (t6.5.png) : la grille de 9 cartes occupe 3/4 de la largeur et 56 % de la hauteur ; 7,0 et 7,5 s idem. Voir P3 4,8–5,8 s.
- V1-9 : **levée** — mention lisible : au moins 28 px de haut, contraste suffisant, visible au moins 3 s (charte § Marques réelles) · Taille, contraste et durée OK : pastille sombre, texte clair ≈ 46 px de corps de 3,4 s à 46,3 s (≈ 43 s), avant cela ligne grise ≈ 28 px de 0 à 3,4 s (crops m*.png, top20.png). MAIS la pastille est coupée par le bord haut à ≈ 10 moments : nouveau P2 (régression).

## Pourquoi ce n'est pas publiable

### V2-1 · P1 · glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes
- où : — · source : controle.py
- preuve : controle.json
- exigé : aucun bloquant
- **condition pour passer** : controle.py ne signale plus : « glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes »

### V2-5 · P2 · grille de 9 cartes sombres presque identiques : on regarde la même image pendant 24 s, l'attention tombe
- où : 12.0–36.0 s · source : condition précédente
- preuve : Entre 12 et 36 s on compte bien ≥ 6 images différentes (mur zoomé, carte pendule, carte roue, pièces, canette barrée, cartes F1 / frisson / dépassement) et dépenser / ne pas vendre / vendre-émotion ont chacune leur image. Mais le mur 3x3 reste 5,4 s (29,6–35,0) avec un simple zoom 1,12→1,05 : la condition « aucune ne reste plus de 4 s » n'est pas tenue, et « produit dérivé » n'a pas d'image propre.
- exigé : —
- **condition pour passer** : entre 12 et 36 s, au moins 6 images visuellement différentes (cadrage, échelle ou sujet), aucune ne restant plus de 4 s, et chaque idée dite par Zak (dépenser, ne pas vendre, vendre) a son image propre
- piste : remplacer la grille par une suite de plans : zoom sur UNE carte à la fois, puis un plan large ; ou refaire le passage en 3D

### V2-7 · P2 · RÉGRESSION de V1-9 : la mention « analyse indépendante / aucun lien avec la marque » est lisible (pastille de 46 px de corps) mais elle bouge avec la caméra et sort du cadre : la 1re ligne est coupée par le bord haut de l'image, lettres tranchées.
- où : 3.4–46.3 s · source : évaluation indépendante
- preuve : Détection par script (lignes 0–3 px, pastille sombre + pixels de texte) : 7,3–7,5 ; 8,2–8,5 ; 12,5–12,7 ; 19,0–19,1 ; 23,5–23,9 ; 25,2 ; 27,2 ; 28,8 ; 29,2–29,5 ; 32,6–32,8 s, soit 27 images (≈2,7 s) ; images extraites c7.4, c8.3, c23.7, c29.4, c32.7 : « analyse indépendante » tranché en haut. t33.png : pastille dépassant du cadre.
- exigé : —
- **condition pour passer** : Sur 3,4–46,3 s, à chaque image (1/30 s), la pastille entière, les 2 lignes comprises, reste dans le cadre avec au moins 40 px de marge au-dessus (script : aucune image où la ligne 0–3 px contient du texte ou une pastille tranchée).
- piste : Sortir la mention de la couche caméra (calque fixe au-dessus du monde, y ≥ 60 px), sans zoom ni décalage de plan.

## Toutes les conditions à remplir pour la tentative suivante (et rien d'autre ne sera exigé, sauf P1 ou régression)

- [ ] V2-1 : controle.py ne signale plus : « glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes »
- [ ] V2-5 : entre 12 et 36 s, au moins 6 images visuellement différentes (cadrage, échelle ou sujet), aucune ne restant plus de 4 s, et chaque idée dite par Zak (dépenser, ne pas vendre, vendre) a son image propre
- [ ] V2-7 : Sur 3,4–46,3 s, à chaque image (1/30 s), la pastille entière, les 2 lignes comprises, reste dans le cadre avec au moins 40 px de marge au-dessus (script : aucune image où la ligne 0–3 px contient du texte ou une pastille tranchée).

## Conseils (ne bloquent pas)

- V2-2 : plans trop longs en moyenne → durée moyenne des plans ≤ 3.48 s (couper ou relancer dans les plans longs) (indicatif : moins de 3 références de qualité ≥ 7)
- V2-3 : aucune coupe dans les 3 premières secondes → au moins une coupe ou un changement de plan avant 3 s (indicatif : moins de 3 références de qualité ≥ 7)
- V2-4 : trop de mots à l écran à la fois → au plus 4.65 mots par image en moyenne (indicatif : moins de 3 références de qualité ≥ 7)
- V2-6 : V1-6 non levée : le même mur 3x3 de cartes noires reste 5,4 s à l'écran (6,5 s si on compte le recadrage dès 28,5 s), seul le zoom bouge de 1,04 à 1,12. L'idée « produit dérivé / vendre » n'a pas d'image propre : on revoit le mur du début (5,9–12,5 s), avec une canette minuscule en bas. → Entre 12 et 36 s, aucune image (même composition, hors simple zoom < 15 %) ne dépasse 4 s : le passage 29,6–35,0 est découpé en au moins 2 plans de sujet différent (ex. gros plan canette + étiquette de prix occupant ≥ 1/4 de l'écran ; un seul écran en plein cadre ; mur qui se fond en un cadre) ; et « produit dérivé » (≈ 32–33 s) a une image propre.
- V2-8 : Écran presque noir : un fantôme de carte quasi invisible, 1,8 s, entre « ne vends pas un produit » et « vends une émotion ». Voulu (le vide avant l'émotion) mais mou, et l'énergie sonore y est basse. → Conseil : un mouvement net (la carte qui se resserre ou s'allume) toutes les 1,2 s.
- V2-9 : Écran presque vide (fond gris, canette minuscule coupée en bas) pendant environ 1 s sur « En réalité, ». Même défaut que V1-8, décalé à 4,8 s ; V1-8 (6–8 s) est bien levé. → Conseil : un sujet ≥ 1/4 de l'écran dès 5,0 s.
- V2-10 : Le mur reste quasiment fixe 3,3 s après la fin de « MÉDIAS » ; seuls les sous-titres changent (sous-traitent tout à 100 %). → Conseil : un événement visuel à ≈ 10,5 s.
- V2-11 : Fin : la canette 2D, plus pauvre que la 3D du début, reste presque immobile 2,5–3 s avec le faux bouton « Envoie-nous un message → ». Raccord de boucle : double exposition (contour 2D + canette 3D) vers 46,4–46.7 s. → Conseil seulement : fin de carte CTA acceptable.
- V2-12 : Détails : (a) mention 0–3,4 s en gris sombre (≈ 4:1) sur noir, corps ≈ 28 px, lue de justesse ; (b) sous-titres à y ≈ 79 % et mention en haut dans les zones de l'interface Instagram ; (c) sous-titre mot à mot à des abscisses variables (« une », « de leurs » décalés à gauche) ; (d) 3 pictogrammes répétés ×3 dans 9 cartes : aspect « template » ; (e) fond « papier » gris à fort vignettage, loin du #EDEBE7 de la charte. → Conseil.
