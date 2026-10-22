# Boîte à outils créative (tout en local, sans compte payant)

Installés par `bash reel/setup.sh`. Tous testés dans l'environnement des tâches (4 cœurs, sans carte graphique : le
WebGL passe par SwiftShader, plus lent qu'un GPU mais exact). Règle : **tout plan venu d'un outil devient une vidéo
1080×1920 30 i/s** (ou une image), puis entre dans `reel.json` comme `plan` (`video` ou `image`) ou `clip`. Le moteur
ajoute caméra, sous-titres, transitions ; `son.py` le son. Teste toujours petit (une image, 2 s) avant le rendu final.

| Outil | Pour quoi | Coût indicatif | Point d'entrée |
|---|---|---|---|
| Moteur HTML (`reel/moteur.html`) | typo cinétique, plans image + caméra, relief 2,5D, transitions | 40 s ≈ 12 min | `node reel/rendu.mjs` |
| three.js + shaders GLSL | 3D temps réel stylisée, matières en shader, particules, déformations, post-traitements | quelques s par image en 1080×1920 | page HTML déterministe (temps = image / fps), capture Playwright comme `rendu.mjs` |
| Remotion (React) | mise en page animée complexe, data, interfaces, compositions multicouches | ~0,3 s par image | `node reel/remotion.mjs entree.jsx Id sortie.mp4` |
| Manim | raisonnement visuel : schémas qui se construisent, transformations de formes, équations, graphes | 1–2 s pour 1 s en `-qh` | `manim -qh --fps 30 -r 1080,1920 scene.py Classe` |
| p5.js / canvas 2D | génératif, tracés, systèmes de particules 2D, textures dessinées | rapide | page HTML + capture, ou `noLoop()` + `redraw()` par image |
| Procédural Python (numpy, opensimplex, Pillow, scipy) | textures, bruits, champs de flux, simulations simples (fluides 2D, ressorts, croissance) | rapide | script → images PNG numérotées → ffmpeg |
| Blender (bpy 5) + geometry nodes | photoréalisme, objets, matières, éclairage ; instanciation, dispersion, croissance, déformations procédurales | 2–4 min / image 1080×1920 à 48–64 spp | skill `brooze-3d`, `~/blender-env/bin/python` ; geometry nodes via `bpy.data.node_groups.new(type='GeometryNodeTree')` |
| ffmpeg avancé | `xfade`, `displace`, `v360`, `lut3d`, `chromashift`/`rgbashift`, `dblur`, `minterpolate` (ralenti), `zscale`, `libplacebo` | rapide | filtres sur les plans avant le moteur |
| Polices variables | axes animés (graisse, largeur, optique, « SOFT/WONK »), texte qui respire avec la voix | — | `~/.cache/brooze/polices/` : Inter, Fraunces, Recursive, SpaceGrotesk, BricolageGrotesque, InstrumentSerif, JetBrainsMono ; CSS `font-variation-settings` |

## Navigateur et WebGL
- Chromium complet (Playwright) : `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` avec
  `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist --allow-file-access-from-files`.
- Remotion exige le « headless shell » : `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
  (déjà réglé dans `reel/remotion.mjs`).
- three.js : `import * as THREE from 'file:///home/user/brooze-agent/node_modules/three/build/three.module.js'`,
  `new THREE.WebGLRenderer({ preserveDrawingBuffer: true })`, et **aucune horloge** : chaque image est calculée depuis
  `t`, jamais `requestAnimationFrame` ni `Date.now()` (sinon le rendu image par image saccade).

## Règles communes
- Déterministe : même `t` → même image (graines fixes pour le hasard). Sinon les rendus par morceaux ne se raccordent pas.
- Charte Brooze : palette, typographies et ton de `brooze-direction` ; une technique nouvelle ne change pas l'identité.
- Rien d'inventé à l'écran : pas de faux chiffres dans un graphe Manim, pas de faux logos dans une interface Remotion.
- Libre de droits : polices OFL (Google Fonts), aucune image ni son téléchargés sans licence notée.

## Banques d'images libres (réseau à ouvrir par Zak)
Bloquées tant que Zak ne les autorise pas dans les réglages de l'environnement (menu de l'environnement cloud →
Modifier → Accès réseau → Domaines autorisés, en gardant « Autoriser les gestionnaires de paquets » coché) :
`api.pexels.com`, `images.pexels.com`, `videos.pexels.com`, `pixabay.com`, `cdn.pixabay.com`.
Clés lues dans l'environnement : `PEXELS_API_KEY`, `PIXABAY_API_KEY` (gratuites, à ajouter comme variables
d'environnement de l'environnement cloud). Sans elles, `reel/stock.py` s'arrête proprement : on passe à la source
suivante.

## Appris (techniques validées, à réutiliser comme savoir-faire, jamais comme plan)
- Relief 2,5D par carte de profondeur Blender + parallaxe WebGL par pixel (Reel Apple v3, 22/10).
- Mot qui tombe avec du poids : chute en profondeur en t³, contact entre deux obturateurs, ombre qui se pose, choc 11 px
  amorti critique, poussée de tenue 1,8 % (entraînement du 22/10, 7/10 ; `reel/techniques/code/mot-qui-tombe/`).
