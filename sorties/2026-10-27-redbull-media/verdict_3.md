# Verdict, tentative 3 : **À REPRENDRE**

## Conditions de la tentative précédente

- V2-1 : **levée** — controle.py ne signale plus : « glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes » · vérifié par controle.py
- V2-5 : **levée** — entre 12 et 36 s, au moins 6 images visuellement différentes (cadrage, échelle ou sujet), aucune ne restant plus de 4 s, et chaque idée dite par Zak (dépenser, ne pas vendre, vendre) a son image propre · 12–36 s, images toutes les 0,5 s + corrélation à 10 i/s : 12,5–15,4 cartes zoomées (pendule, roue), 15,5–18,4 barres de pièces (« dépensent »), 18,4–21,4 carte F1 / espace, 21,5–24,4 canette barrée (« ne te vendent même pas »), 24,4–29 gros plans de cartes frisson / dépassement (« ils vendent… »), 29–29,6 canette, 29,6–31,6 mur, 31,6–33 canette + étiquette de prix (« le produit dérivé » à 32,5 s), 33–35,5 mur qui converge : 10 images distinctes. Plus longue image identique : 21,6–24,3 s = 2,7 s (≤ 4 s) ; le mur n'est plus que 2,0 s (29,6–31,6) puis 2,5 s (33–35,5). Dépenser, ne pas vendre, vendre (adrénaline, frisson) et produit dérivé ont chacune leur image.
- V2-7 : **levée** — Sur 3,4–46,3 s, à chaque image (1/30 s), la pastille entière, les 2 lignes comprises, reste dans le cadre avec au moins 40 px de marge au-dessus (script : aucune image où la ligne 0–3 px contient du texte ou une pastille tranchée). · Script de suivi de la pastille sur les 1296 images de 3,3 à 46,5 s : 1185 images trouvées, pastille entière à y ≥ 94 px (minimum à 7,40 / 8,47 / 29,40 s), plus aucun bord tranché (contre 27 images avant). Les 111 images non trouvées (14,43–15,43 ; 36,4–37,7 ; 42,7–43,47 ; 46,07–46,47 s) ont été regardées : pastille dans le cadre mais cachée par un titre ou absente : traité comme défaut P2 distinct (régression), voir défauts.

## Pourquoi ce n'est pas publiable

### V3-4 · P2 · RÉGRESSION de V2-7 : la pastille « analyse indépendante / aucun lien avec la marque », descendue à y ≈ 95–260 px pour sortir du bord haut, tombe maintenant sous les gros titres : (a) 14,43–15,43 s « Créer du contenu. » est posé PAR-DESSUS les 2 lignes de la mention, qui sont grisées et illisibles ; (b) 36,4–37,7 s « vends une émotion. » idem, mention grisée sur noir et coupée par le titre ; (c) 42,70–43,47 s (0,8 s) la mention a disparu (écran quasi noir, CTA déjà là). Au total 111 images (3,7 s) où la mention obligatoire n'est ni entière ni lisible.
- où : 14.4–43.5 s · source : évaluation indépendante
- preuve : Script OpenCV sur les 1296 images 3,3–46,5 s (correspondance de contours multi-échelle de la mention, score ≥ 0,6) : 1185 images trouvées, pastille la plus haute à y = 94 px (7,40 ; 8,47 ; 29,40 s) donc la géométrie V2-7 est tenue ; les 111 images à score < 0,6 forment exactement 14,43–15,43 ; 36,4–37,7 ; 42,7–43,47 ; 46,07–46,47 s. Images regardées à 14,5 / 14,9 / 15,0 / 15,4 / 36,5 / 36,9 / 37,0 / 37,6 / 42,7 / 42,9 / 43,1 / 43,3 : titre blanc 800 par-dessus le texte gris de la mention ; 42,9–43,3 aucune mention.
- exigé : —
- **condition pour passer** : Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (contraste ≥ 4,5:1 avec leur fond), n'intersectent la boîte d'aucun autre texte (gros titre, sous-titre, CTA) et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (aucune image à score < 0,6 hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s.
- piste : Garder la pastille en calque fixe et déplacer plutôt les gros titres « Créer du contenu. » (14,4) et « vends une émotion. » (36,4) sous y ≈ 330 px, ou les faire entrer plus bas ; garder la mention à opacité 1 pendant les fondus au noir 36–37,7 et 42,7–43,5.

## Toutes les conditions à remplir pour la tentative suivante (et rien d'autre ne sera exigé, sauf P1 ou régression)

- [ ] V3-4 : Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (contraste ≥ 4,5:1 avec leur fond), n'intersectent la boîte d'aucun autre texte (gros titre, sous-titre, CTA) et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (aucune image à score < 0,6 hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s.

## Conseils (ne bloquent pas)

- V3-1 : plans trop longs en moyenne → durée moyenne des plans ≤ 3.48 s (couper ou relancer dans les plans longs) (indicatif : moins de 3 références de qualité ≥ 7)
- V3-2 : aucune coupe dans les 3 premières secondes → au moins une coupe ou un changement de plan avant 3 s (indicatif : moins de 3 références de qualité ≥ 7)
- V3-3 : trop de mots à l écran à la fois → au plus 4.65 mots par image en moyenne (indicatif : moins de 3 références de qualité ≥ 7)
- V3-5 : Boucle : double exposition canette 2D + canette 3D et double mention (pastille 2 lignes fantôme + ligne unique) pendant ≈ 0,4 s. → Conseil : fondu de boucle sans doublon de texte, ou raccord sec 2D→3D.
- V3-6 : Écran presque noir 35,6–37,0 s (carte fantôme, luma ≈ 10) entre « ne vends pas un produit » et « vends une émotion ». → Conseil : un mouvement net toutes les 1,2 s.
- V3-7 : Fond gris quasi vide, canette minuscule coupée en bas, ≈ 1 s sur « En réalité, ». → Conseil : un sujet ≥ 1/4 de l'écran dès 5,0 s.
- V3-8 : Le pouls (même cadre, même courbe blanche) reste 4,5 s ; seul le tracé bat. Tient grâce à l'audio et aux sous-titres mais c'est le plus long plan fixe du Reel. → Conseil : un changement de cadrage ou d'échelle à ≈ 40,3 s.
- V3-9 : Raccord de style : la canette 3D photoréaliste devient d'un coup une canette 2D plate (anneau blanc, aplat) ; même objet, deux niveaux de finition. Revient à 43,5–46 s (CTA 2D) puis la 3D reparaît à 46,1 s. → Conseil : garder la 3D jusqu'à 5,0 s ou un fondu enchaîné lent.
- V3-10 : Mention de début en ligne unique grise très petite (corps ≈ 28 px, contraste ≈ 4:1) ; premier cadre quasi noir avec seulement « Red » en sous-titre. → Conseil : mention plus contrastée ; image 1 plus riche que du noir.
- V3-11 : Détails : pastille translucide laissant voir les bords des cartes à 13,8 et 32,8 s ; 3 pictogrammes répétés ×3 dans le mur (effet template) ; fond papier gris vignetté loin du #EDEBE7 ; sous-titres à y ≈ 79 % dans la zone d'interface Instagram. → Conseil.
