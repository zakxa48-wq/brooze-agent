# Montage Brooze : impressionnant, naturel, économe

À lire avant chaque storyboard de Reel, en plus de `AGENT_REEL.md`. Le but : un montage qu'on regarde « sans y penser »,
qui paraît filmé et monté par un humain exigeant, pas généré. Trois exigences, dans cet ordre : **naturel**,
**impressionnant**, **économe**. On ne sacrifie jamais la première pour les deux autres.

## 1. L'image d'abord, le texte en dernier
- **Au moins 60 % du temps à l'écran = des images réelles** (scène `plan`) : rushs ou photos de Zak, rendus
  photoréalistes, images de banque libres de droits. Les scènes graphiques (`texte`, `slam`, `duel`, `liste`,
  `compteur`…) servent de ponctuation, pas de décor.
- **Gros texte : 3 moments maximum par Reel** (le hook, le pivot, la phrase-titre), quelques mots, jamais une phrase
  entière qui s'écrit sur un fond vide. Le reste du texte, ce sont les **sous-titres** (en bas, sans cartouche sur
  les images, mot actif qui respire).
- **Pas de dessin quand une vraie image existe.** Les illustrations en code (paysages SVG, onde, timeline) restent
  possibles pour une idée abstraite, une seule fois par Reel au plus.
- Chaque idée de la voix a **une image qui la montre** (pas qui la décore) : « une liste interminable » → la caméra
  descend une vraie fiche technique qui n'en finit pas ; « coupe le son » → une main qui coupe le son d'un téléphone.

## 2. D'où viennent les images (de la moins chère à la plus chère)
| Source | Coût | Quand |
|---|---|---|
| Rushs et photos de Zak (`brooze-voix/rushs/`, indexés par `reel/rushs.py`) | ~0 | toujours en premier : c'est le positionnement Brooze (créer à partir de l'existant) |
| Rendus déjà faits (`brooze-kit/projets/*/img`, `*/livraison`, anciens Reels) | ~0 | quand un objet existant sert l'idée (jamais comme preset : pas le même plan deux fois en 4 semaines) |
| Image de banque libre de droits (`reel/stock.py`, si le réseau l'autorise) | ~0 | lieux, gestes, foules, ambiances que Zak n'a pas filmés ; licence notée dans `credits.json` |
| **Image fixe photoréaliste** (skill `brooze-3d`, Blender Cycles) animée en 2,5D | 2–6 min par image | un objet ou une métaphore précise ; on rend UNE image (fond + objet détouré pour la parallaxe), la caméra du moteur fait le reste |
| Plan 3D animé (Cycles ou `monde3d`) | 20 min à plusieurs heures | seulement le plan-signature d'un Reel, si rien d'autre ne le rend |

**Règle économique** : une image photoréaliste fixe + une caméra vivante (`plan` avec `cadre`, `main`, `calques`)
donne 90 % de l'effet d'un plan 3D animé pour 5 % du temps de calcul. Budget par Reel : 30 min de calcul au total ;
au-delà, simplifier (moins d'images, `spp` plus bas avec débruitage, résolution 1080×1920 seulement pour les plans
plein cadre).

## 3. Le naturel (ce qui enlève l'effet « mécanique »)
- **Caméra à l'épaule** sur tout plan réel (`main` 0,6–1) : dérive lente + micro-tremblement. Jamais deux plans qui
  bougent exactement pareil : varie le `cadre` (poussée, recul, glissé latéral, bascule vers un détail).
- **Ressorts, pas de courbes fixes** : le moteur fait arriver les mots au ressort avec de petites variations
  (déjà en place). Ne pas tout synchroniser sur la même image : un léger décalage est humain.
- **Couper sur la voix** : une coupe tombe sur une attaque de mot ou une respiration (`attaques.py`), jamais au
  milieu d'une syllabe. L'image peut arriver 2 à 4 images AVANT le mot (le cerveau l'attend), jamais après.
- **J-cut / L-cut** : le son du plan suivant (bruitage, ambiance) commence avant l'image, ou le son du plan précédent
  déborde après la coupe. Dans `sons`, place l'ambiance 0,2–0,4 s avant la coupe.
- **Durée des plans** : 1,2 à 2,5 s en moyenne ; un plan qui porte une phrase-clé peut tenir 3–4 s s'il bouge.
  Un moment « nerveux » par Reel (3–4 coupes de 0,25–0,4 s sur un mot), validé par Zak sur le Reel 8.
- **Transitions** : la coupe franche est la transition par défaut entre deux images réelles. `whip` (panoramique
  filé) pour un changement d'idée énergique, `fondu` pour un passage doux ou temporel, `glisse` / `volet` pour les
  scènes graphiques. **Deux types de transition maximum par Reel**, sinon ça fait « template ».
- **Coups de zoom** (`punch: ["@12", …]`) sur 2 à 4 mots forts, pas plus. Ils remplacent avantageusement un gros
  texte.
- **Couleur cohérente** : un seul `etalonnage` pour tout le Reel (sauf rupture voulue), grain et vignette du moteur
  par-dessus : c'est ce qui fait « un film » au lieu d'un collage.

## 3 bis. Animé, pas agité (retour de Zak, 22/10 : « plus animé, pas extrême, moins d'image fixe »)
- **Aucune image ne doit paraître figée** : chaque plan tiré d'un rendu 3D reçoit sa carte de profondeur et le moteur
  lui donne un vrai relief (parallaxe par pixel, en WebGL). Coût : 2 à 5 s de calcul par carte.
  - Scène écrite en code : `import profondeur` puis `profondeur.rendre('plan_prof.png')` juste après `B.rendre(...)`.
  - Scène sauvegardée : `~/blender-env/bin/python reel/profondeur.py scene.blend plan_prof.png`.
  - Photo réelle sans 3D : pas de carte inventée ; caméra à l'épaule + `cadre` suffisent.
- **Amplitude** : `relief` 1 par défaut (≈ 1 % de l'image d'orbite) ; 1,4 au maximum pour le plan-signature, 0,6
  pour un plan calme. Jamais d'orbite rapide, jamais deux plans de suite avec la même `orbite`.
- Ce qui fait « pro » : beaucoup de petits mouvements cohérents (épaule + relief + coups de zoom sur 2–4 mots).
  Ce qui fait « amateur » : un effet fort partout (zooms à chaque phrase, secousses, transitions variées).

## 4. L'impressionnant (sans effets gratuits)
- **Un effet signature par Reel** (règle Brooze) : une parallaxe profonde sur un rendu, un match cut (même forme d'un
  plan à l'autre), un ralenti sur un geste, une coupe du son… pas tout à la fois.
- **La vidéo fait ce qu'elle dit** : c'est le moment qu'on partage.
- **Match cut** : aligner la forme ou le mouvement du dernier instant d'un plan sur le premier du suivant (un
  rond → un rond, une main qui descend → un objet qui tombe). Le `cadre` final du plan A = le `cadre` initial du B.
- **Parallaxe** : rends l'objet détouré (PNG avec alpha, `B.rendre` avec film transparent) + le fond séparément ;
  `calques: [{"image": "objet.png", "profondeur": 1.8}]`. Le décalage de profondeur est ce qui « fait vrai ».

## 5. Le son qui va avec (plus de bruitages, jamais trop)
- Une ambiance discrète sous les plans réels (`airy`, `bourdon` très bas) : un plan réel sans air sonne faux.
- Whoosh sur chaque `whip` ; sur une coupe franche, un souffle très court et très bas, une coupe sur deux au plus.
- **Palette automatique** (`reel/son.py`) : aspiration du hook vers le premier coup de zoom, grave sous les coups de
  zoom, snap à l'arrivée d'un titre posé sur une image, **sons contextuels sur les mots dits** (`LEXIQUE_SFX` :
  « photo » → obturateur, « prix » → caisse, « liste » / « fiche » → papier, « message » → bip…). Complète le
  lexique quand un mot revient ; `sfx_mots: {"mot": "son"}` dans reel.json pour un Reel précis.
- **Limiteur de densité** : jamais deux bruitages à moins de 0,6 s, au plus 2 par fenêtre de 3 s, gardés par
  priorité (manuels > structure > coups de zoom > contexte > coupes). Cible : un moment sonore toutes les 2 à 3 s,
  sous la voix (le mixage la protège). Lis `partition.json` → `ecartes` : si un son important a sauté, déplace ou
  retire un son moins utile plutôt que de forcer.
- Musique sérieuse et tendue (retour de Zak sur le Reel 10), coupée sur 1 ou 2 moments forts.

## 6. Contrôle supplémentaire (en plus de `controle.py` et du sceptique)
- `python3 reel/controle.py` affiche la **part d'images réelles** et le **nombre de gros textes** du storyboard :
  moins de 60 % d'images réelles ou plus de 3 gros textes = à justifier dans le journal, sinon corriger.
- Regarde la planche en vignettes : si on voit surtout du texte, c'est raté, même si chaque image est jolie.
- Chasse au mécanique : deux plans de suite avec le même mouvement de caméra, des mots qui tombent tous pareil,
  une transition répétée 4 fois → corriger.

## 7. Leçons de fabrication (Reel Apple v2, 22/10)
- **Variété** : 6 images pour 41 s, c'était trop peu (le sceptique : « ça tourne en rond »). Viser une image distincte
  toutes les 4 à 5 s, et jamais la même image 5 s d'affilée sous deux cadrages proches. Un angle de caméra de plus
  sur une scène 3D déjà construite coûte ~3 min : c'est le moyen le moins cher d'ajouter de la variété.
- **Une idée de monde aide le montage** : ici, le papier = ce qu'on DIT (fiche technique), la photo = ce qu'on MONTRE.
  Chaque retour d'une image a alors un sens au lieu d'être une répétition.
- **Écran 3D** : vérifier l'orientation de l'image affichée avec une mire (« HAUT » + un coin coloré) en 4 s de rendu
  avant tout rendu final ; une rotation du téléphone de 180° change le sens de lecture pour la caméra. Les panneaux
  de lumière se reflètent en rectangles blancs sur un écran brillant : verre « antireflet » (Coat ~0,2, Specular
  ~0,12) pour le plan concerné, en gardant un reflet discret.
- **Poids** : grain + caméra à l'épaule + images détaillées = débit énorme à qualité constante (240 Mo pour 41 s) ;
  le rendu plafonne maintenant à 14 Mb/s (~70 Mo).
- **Temps réels mesurés** (4 cœurs, sans carte graphique) : image photoréaliste 1080×1920 à 48–64 spp : 2 à 4 min ;
  test à 25 % et 16 spp : 4 s (toujours tester avant) ; rendu du Reel de 41 s en images réelles : ~7 min.
