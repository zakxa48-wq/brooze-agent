# Montage Brooze : des principes, pas un modèle

À lire avant chaque Reel, avec `AGENT_REEL.md`, `reel/OUTILS.md` et le registre des Reels de `journal.md`.
Ce fichier ne décrit **aucune** recette à refaire : il dit ce qui rend un montage bon. Chaque Reel invente sa
forme à partir de son propos. Si un Reel ressemble à un précédent, c'est raté, même s'il est réussi.

## 0. L'ordre des exigences
1. **Juste** : le texte est exactement la voix de Zak, au moment où il le dit. Rien d'inventé (chiffre, client,
   témoignage, propos).
2. **Naturel** : on le regarde sans y penser. Monté par un humain exigeant, pas généré.
3. **Original** : une idée visuelle née de CE propos, jamais vue dans les 5 derniers Reels.
4. **Impressionnant** : un moment qu'on a envie de montrer à quelqu'un.
5. **Économe** : le moyen le moins cher qui atteint 1 à 4, jamais au prix de la qualité.

## 0 bis. Analyser une vraie marque (décryptage)
Une vidéo qui décrypte la stratégie d'une vraie marque peut montrer son nom et son logo officiel (`charte.md` §
Marques réelles, décision de Zak du 23/10). Principe de montage : la marque est un **sujet d'étude**, pas une
signature. Son logo apparaît comme une pièce à conviction (posé, cité, tel quel, sur le passage qui en parle), jamais
comme l'habillage de la vidéo ; on montre la mécanique de sa stratégie avec le langage visuel Brooze, sans imiter sa
direction artistique, ses pubs ni ses images. Rien qui fasse croire à une vidéo officielle ou sponsorisée.

## 1. Partir du propos, pas d'un format
- Résume le propos en une phrase. Cherche **la règle de monde** qui le rend visible : quelle matière, quel lieu,
  quel geste, quelle loi physique le raconte mieux que des mots ? (« dire vs montrer » → un papier qu'on lit / une
  photo qu'on regarde ; « l'attention se perd en 1 s » → un objet qui tombe pendant exactement une seconde.)
- La vidéo **fait ce qu'elle dit** au moins une fois : c'est le moment partagé.
- Écarte les trois premières idées qui viennent : ce sont celles de tout le monde. Garde celle qui a une contrainte
  forte (un seul plan-séquence, une seule couleur, un seul objet qui se transforme, le texte comme matière…).
- **Structure** : choisis comment le Reel avance (révélation progressive, avant/après, compte à rebours,
  plan-séquence, boucle parfaite, montage parallèle, zoom continu, accumulation, rupture…). Pas deux fois la même
  structure dans les 5 derniers Reels.

## 2. L'image d'abord, le texte en soutien
- La voix porte le sens ; l'image le **montre** ; le texte à l'écran ne fait que l'ancrer. Peu de gros textes
  (le hook, un pivot, une phrase-titre au plus), des sous-titres justes pour le reste.
- Une image réelle ou crédible (rush de Zak, photo, rendu photoréaliste, matière procédurale bien éclairée) vaut
  mieux qu'un dessin. Le graphisme pur est une ponctuation, ou un parti pris assumé pour tout le Reel.
- Sources, de la moins chère à la plus chère : rushs et photos de Zak (`rushs.py`) → rendus existants
  → banques libres (si le réseau est ouvert, `stock.py`, crédits notés) → génératif en code (shaders, p5,
  procédural) → images photoréalistes fixes animées en relief → 3D animée. Les coûts réels sont dans `OUTILS.md`.

## 2 bis. La 3D, par moments, magnifique (demande de Zak du 24/10)
- Chaque Reel contient **1 ou 2 moments 3D** de 2 à 5 s, jamais toute la vidéo. Ils tombent sur ce qui compte
  (l'image du hook, le pivot, la révélation) : la 3D est un **événement**, pas un décor.
- Le moment 3D doit être **le plus beau plan du Reel** : lumière sculptée, matières vraies, profondeur de champ, flou de
  mouvement, caméra qui a du poids. S'il n'atteint pas ce niveau, il ne part pas (on améliore, on ne remplace pas par
  du plat).
- Il raccorde avec le reste (même étalonnage, même grain, même lumière dominante) : on doit sentir un seul film.
- Il sert le propos : un objet, une matière ou une métaphore que la voix de Zak appelle, jamais une démonstration
  gratuite. Inventé pour CE Reel (registre : pas le même objet ni le même mouvement 3D que les 5 derniers).

## 3. Le naturel (ce qui enlève l'effet « mécanique »)
- **Rien n'est figé** : toute image vit (caméra à l'épaule, relief 2,5D, matière qui respire, lumière qui bouge),
  mais **rien n'est agité** : beaucoup de petits mouvements cohérents, pas un gros effet partout. Retour de Zak :
  « plus animé, pas extrême du tout, sinon ça fait pas pro ».
- **Ressorts et inerties**, pas de courbes fixes ni de linéaire ; de petites variations entre éléments.
- **Couper sur la voix** (attaque d'un mot, respiration), jamais au milieu d'une syllabe. L'image peut précéder le
  mot de 2 à 4 images, jamais le suivre. Son en J-cut / L-cut.
- **Rythme** : il suit l'énergie de la voix, pas une grille. Varier la durée des plans ; un moment nerveux et un
  moment qui respire valent mieux qu'un tempo constant.
- **Transitions** : la coupe franche par défaut ; une transition « visible » doit avoir une raison (mouvement
  continu, match cut, changement d'idée). Peu de types différents par Reel, sinon ça fait « template ».
- **Couleur** : une intention d'étalonnage pour tout le Reel (ou une rupture voulue) : c'est ce qui fait un film.

## 4. L'impressionnant (sans effets gratuits)
- **Un effet signature par Reel**, inventé ou poussé pour ce propos, et différent de ceux des 5 derniers Reels.
- **Une technique nouvelle par Reel** (`OUTILS.md`) : shader, simulation, typographie variable animée, geometry
  nodes, particules, rendu Manim d'un raisonnement, match cut 3D… Tester petit (une image, 2 s) avant d'y engager
  le rendu final. Ce qui marche rejoint `OUTILS.md` (§ « Appris ») pour les Reels suivants, comme technique, jamais
  comme plan à refaire.
- Ce qui impressionne : la précision (synchro à l'image, matière crédible, lumière juste), la surprise (la règle du
  monde qui se révèle), l'économie (une seule idée poussée au bout). Pas l'accumulation.

## 5. Le son
- Un plan sans air sonne faux : une ambiance discrète sous les images.
- Des bruitages qui **racontent** (le geste, la matière, le mot dit), dosés par le limiteur de `son.py` ; un silence
  voulu vaut un bruitage. Musique synthétisée, sérieuse, coupée sur 1 ou 2 moments forts.
- Ce que le son doit éviter : un whoosh à chaque coupe, un impact à chaque phrase, une musique qui couvre la voix.

## 5 bis. Engager et boucler (objectif de Zak du 23/10 : qu'on la regarde en boucle sans jamais s'ennuyer)
Sans changer le style ni la charte Brooze. Mesuré par `reel/engagement.py` (appelé par controle.py) : graphique
`engagement.png` (énergie de mouvement image par image) et `jonction.jpg` (fin → début) à regarder à chaque contrôle.
1. **Première demi-seconde** : un mouvement ou un changement visuel dès l'image 1. Jamais d'ouverture statique, jamais
   de fondu depuis le noir. *(bloquant)*
2. **Relances** : un changement visuel significatif toutes les 1,5 à 3 s (cadrage, échelle, couleur, mouvement, couche
   nouvelle), en variant le TYPE de relance ; **aucune zone morte de plus de 2 s** *(bloquant)* ; plus de 3 s sans
   relance = à justifier.
3. **Rythme vivant** : alterner plans courts et respirations voulues, accélérer vers le moment clé ; jamais la même
   cadence plus de 5 s (3 plans de même durée de suite = à justifier).
4. **Profondeur** : 2 à 3 couches à l'écran (un fond qui vit, le sujet, un détail), micro-animations discrètes, sans
   surcharge ni perte de lisibilité (l'Atelier et le relief 2,5D sont faits pour ça).
5. **Récompenser le revisionnage** : 1 ou 2 détails qu'on ne remarque qu'au 2e visionnage, liés au propos, jamais
   gratuits ; déclarés dans `reel.json` : `"clins_d_oeil": [{"t": 12.4, "quoi": "…"}]`.
6. **Boucle parfaite** : la dernière image et le dernier son s'enchaînent avec la première image (raccord de cadrage,
   de couleur et de mouvement ; `"boucle": true` → la musique déborde et se prolonge dans le début, sans fondu final),
   et la fin relance la question du début. **Pas de carton de fin** (scène `fin`) *(bloquant)* : le CTA arrive avant
   la fin, en surimpression (`"cta": {"de": "@40", "a": "@44>", "texte": "Envoie-nous un message"}`), et repart avant
   la dernière image.
7. **Durée** : la plus courte possible pour l'idée (souvent 15 à 30 s) : choisir la fenêtre de voix la plus dense et
   couper ce qui ne sert pas (sans jamais réordonner ni changer les mots de Zak). Au-delà de 30 s = à justifier.
8. **Lecture** : chaque gros texte reste au moins 0,25 s par mot + 0,4 s, jamais au-delà de 2,5 × ce temps + 1 s.
9. **Passe « ennui » du sceptique** : la vidéo regardée 3 fois d'affilée (planche de la boucle + `engagement.png` +
   `jonction.jpg`), chaque moment où l'attention baisse noté avec son temps, puis corrigé.
10. **Mesure** : la durée moyenne regardée rapportée à la durée (IGRE24 / durée : au-dessus de 1 = revisionnages), la
   rétention (IGRE27) et les vues > 3 s (IGRE28) sont suivies par Reel ; ce qui augmente vraiment le revisionnage
   sur le compte de Zak va dans `principes.md` (CERVEAU.md § 6), distingué des intuitions.

## 6. Contrôle (en plus de `controle.py` et du sceptique)
- `controle.py` signale les déséquilibres (part d'images réelles, gros textes, variété de transitions) : ce sont
  des alertes à justifier dans le journal, pas des règles de forme.
- Planche en vignettes : si on voit surtout du texte, ou si elle ressemble à la planche d'un Reel précédent, c'est
  raté.
- Chasse au mécanique : deux plans de suite qui bougent pareil, des mots qui tombent tous pareil, un effet répété.
- Chasse à la redite : relis le registre ; concept, effet signature, structure doivent tous être neufs.

## 7. Leçons de fabrication (techniques, pas des plans à refaire)
- **Variété** : une image distincte toutes les 4 à 5 s environ ; la même image 5 s sous deux cadrages proches,
  ça « tourne en rond ». Un angle de plus sur une scène 3D déjà construite coûte quelques minutes.
- **Une idée de monde aide le montage** : chaque retour d'une image a alors un sens au lieu d'être une répétition.
- **Écran 3D** : vérifier l'orientation de l'image affichée avec une mire en 4 s de rendu ; verre « antireflet »
  (Coat ~0,2, Specular ~0,12) si les panneaux de lumière s'y reflètent.
- **Relief 2,5D** : carte de profondeur (`reel/profondeur.py`) + champ `profondeur` d'un `plan` ; `relief` 0,6–1,4.
- **Poids** : le rendu plafonne à 14 Mb/s (~70 Mo pour 40 s).
- **Synchro du texte** : Whisper medium, relecture des pronoms et des questions, affinage des attaques, sous-titres
  révélés mot par mot, groupes qui ne finissent jamais sur un petit mot.
