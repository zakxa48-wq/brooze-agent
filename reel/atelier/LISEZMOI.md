# Atelier Brooze — le « After Effects » de l'agent, en code

Un compositeur de calques **en plus** des autres outils (moteur HTML, Blender, three.js, Remotion, Manim…). L'agent
le mobilise **quand c'est le plus pertinent** : typo cinétique précise (lettre par lettre, mot par mot calé sur la
voix), compositing de plusieurs calques (images, vidéos, formes, textes), caches et masques, caméra 2,5D, flou de
mouvement réel, effets. Le résultat est une vidéo 1080×1920 qui devient un plan de Reel (`plan.video` / `clip` du
moteur) ou un Reel entier. Il ne remplace pas la méthode : il s'ajoute à la boîte à outils.

**Quand le prendre** : un geste qu'il faut régler à l'image près (courbe de vitesse, flou, choc, synchro voix), un
plan composé de plusieurs couches, une animation de texte par unité, un cache. **Quand ne pas le prendre** : une
image photoréaliste (Blender), une scène 3D vraie (three.js / Blender), un plan simple image + caméra (moteur HTML,
plus rapide), une démonstration mathématique (Manim).

Version : `python3 reel/atelier --version` · historique : `VERSIONS.md` · tests : `python3 reel/atelier/tests.py`.

## Commandes
```
python3 reel/atelier scene.py --image 0.5          # une image pour vérifier (scene_0.50.png)
python3 reel/atelier scene.py --planche            # 12 images réparties (ou --planche 0,0.2,0.45,…)
python3 reel/atelier scene.py --sortie plan.mp4    # vidéo H.264 + AAC, rendu en parallèle (4 cœurs ≈ 0,1–0,3 s / image)
        [--de 0 --a 1.5] [--demi] [--travailleurs N]
python3 reel/courbe.py plan.mp4                    # mesurer le geste (vitesse, arrêt, dépassement, flou, synchro son)
```

## Écrire une scène (Python)
```python
from atelier import *
from atelier.gestes import lire_tomber_frapper, choc     # savoir-faire validés (voir gestes.py)
voix = Voix('mots.json', source=[12.4, 40.1])            # temps des mots de Zak, dans le temps de la scène

comp = Composition(1080, 1920, ips=30, duree=4.0, fond='#EDEBE7', camera=Camera(zoom=1500))
fond = comp.ajouter(Image_('3d/rendus/table.png', remplir=True, echelle=K((0, 1.0), (4, 1.04, lin))))
titre = comp.ajouter(Texte(voix.texte(3, 5), taille=150, graisse=800, couleurs={1: '#B87333'},
        animateurs=[Animateur(par='mot', temps=voix.temps(3, 5), duree=.25, de=dict(opacite=0, y=40, flou=10))]))
comp.ajouter(Reglage(effets=[Grain(intensite=.03), Vignette(force=.15)]))
comp.voix = 'voix_reel.wav'; comp.sons = [(voix.t(4), 'low_hit', .7)]
```

### Valeurs animées
- constante · `K((t0, v0, courbe), (t1, v1, courbe), …)` (images clés ; la courbe régit le segment qui PART de la clé)
  · fonction `lambda t: …` (expression) · `wiggle(freq, amplitude, graine, base)` · `boucle(anim, periode)`.
- Courbes : `lin`, `doux`, `entree(p)`, `sortie(p)`, `chute(p)`, `expo(f)`, `bezier(x1, y1, x2, y2)` (graphique de
  vitesse d'After Effects), `ressort(frequence, amortissement)`, `tenir`.
- `Voix(mots.json, source)` : `.t(i)` début du mot i, `.temps(a, b)`, `.texte(a, b)` — la synchro voix est native.

### Calques (paramètres communs)
`position (x, y)`, `z`, `ancre`, `echelle` (s ou (sx, sy)), `rotation`, `opacite`, `debut`/`fin`, `parent` (calque ou
`Nul`), `effets=[…]`, `fusion` (`normal`, `ajout`, `ecran`, `produit`, `incrustation`), `masque=(chemin)` +
`masque_contour` + `masque_inverse`, `cache=(calque, 'alpha' | 'alpha_inv' | 'luma')`, `flou_mouvement=True`,
`visible=False` (sert seulement de cache ou de parent), `decalage_temps`.
- `Solide(couleur)`, `Image_(chemin, remplir)`, `Video(chemin, debut_source, vitesse)`, `Precomp(composition)`,
  `Nul()`, `Reglage(effets)` (calque de réglage : agit sur tout ce qui est dessous).
- `Texte(texte, police, taille, graisse (animable, polices variables), interlettrage, interligne, alignement,
  largeur_max, couleurs {mot: couleur}, couleurs_car {caractère: couleur}, animateurs)`.
  `Animateur(par='car' | 'mot' | 'ligne', debut, decalage | temps=[…], duree, courbe, de=dict(opacite, x, y,
  echelle, rotation, flou, suivi), vers=dict(…) pour une sortie, ordre='normal' | 'inverse' | 'centre' | 'hasard')`.
- `Forme(chemin, remplissage, trait, epaisseur, trace_debut, trace_fin)` ; chemins : `rect(l, h, rayon)`,
  `ellipse(l, h)`, `points([...], ferme)`, `svg('M … C … Z')` ; `trace_*` = trim paths (un trait qui se dessine).
- `Camera(zoom, z, cible, mise_au_point, ouverture)` : profondeur de champ et parallaxe selon le `z` des calques.

### Effets
`FlouGaussien(rayon)`, `FlouDirectionnel(longueur, angle)`, `OmbrePortee(distance, angle, flou, opacite, couleur)`,
`Lueur(seuil, rayon, intensite)`, `Grain(intensite, taille)`, `Aberration(decalage, angle)`, `Vignette(force)`,
`Niveaux(noir, blanc, gamma, saturation)`, `Teinte(couleur, quantite)`, `Remplir(couleur)`, `Decaler(dx, dy)` (choc ou
tremblé sans bord découvert, P-033). Tous les paramètres sont animables.

### Son
`comp.sons = [(t, 'nom son_brooze', gain, {args})]`, `comp.musique` (sections son_brooze), `comp.voix` (wav), ou
`comp.son` (un mix déjà fait). Mixé à −14 LUFS par son_brooze ; sinon piste silencieuse.

## Faire grandir l'outil (règles)
L'Atelier s'améliore au fil des Reels, comme la bibliothèque de techniques :
1. **Un besoin réel d'abord** : on ajoute une fonction quand un Reel ou une séance d'entraînement en a besoin (noté
   dans `intention.md` ou le débrief), jamais « au cas où ».
2. **Petit et testé** : la fonction a une démo dans `demos/` (2–3 s) qui l'utilise, `tests.py` passe (déterministe,
   image non vide), et `tests.py --complet` ne régresse pas.
3. **Versionné** : `VERSION` (0.x.y : y = correctif, x = nouvelle fonction) et une ligne dans `VERSIONS.md` (quoi,
   pourquoi, quel Reel ou quelle séance, mesure avant/après si c'est une amélioration de rendu).
4. **Un geste validé** (séance coachée ou Reel validé) peut entrer dans `gestes.py` : il renvoie des valeurs animées,
   jamais un visuel tout fait, et cite sa technique et ses principes.
5. Ce qui déçoit deux fois (fonction lente, rendu moins bon que le moteur HTML) est retiré ou réécrit, et noté.
6. Performance : mesurer (`secondes` dans la sortie de rendu) ; une optimisation ne change aucun pixel (tests).
