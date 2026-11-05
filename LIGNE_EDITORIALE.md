# Ligne éditoriale Brooze (décision de Zak du 02/11) — à lire avant TOUT contenu

S'applique aux Reels, stories et carrousels. Elle passe avant les habitudes des semaines précédentes, jamais avant les
garde-fous (vérité, marques, charte, sécurité) ni le storyboard d'un audio de Zak.

## 1. Le cap : une communauté engagée, pas un catalogue de conseils
Le Reel qui a le mieux marché à ce jour, **Koulechov** (01/11, 1 364 vues à J+1, environ 8 fois la médiane du compte),
ne donnait pas une leçon : il faisait **vivre une expérience** au spectateur (le même visage, trois objets, et il voit
lui-même l'émotion changer), puis la leçon tombait d'elle-même. Apple et Sound design, les deux autres qui décollent,
sont aussi des démonstrations où la vidéo fait ce qu'elle dit. C'est l'angle à suivre (n = 3, donc une piste forte,
pas une loi : on continue de mesurer) :
- **Pas 100 % sérieux** : jeux, expériences, défis, devinettes, pièges visuels, « fais le test », illusions,
  avant/après à deviner, mini-fictions. Le ton reste celui de Brooze (direct, malin, jamais bouffon), mais on a le
  droit de sourire, de surprendre, de piéger gentiment.
- **Le spectateur participe** : il devine, il se trompe, il compte, il compare, il se reconnaît, il répond. Une
  question qu'on a envie de trancher vaut mieux qu'une affirmation.
- **Instructif pour tout le monde**, pas seulement pour les commerçants : perception, attention, psychologie,
  cinéma, pub, design, son, histoire des images, petites expériences du quotidien. Quelqu'un qui n'a pas d'entreprise
  doit aussi repartir avec quelque chose (et avoir envie de l'envoyer à un ami).
- **Toujours relié à Brooze** : la leçon se raccroche à ce que fait le studio (attirer l'œil, raconter, monter, faire
  ressentir), en une ligne, sans forcer. Le divertissement attire, le lien avec le métier fait venir les bons clients.

## 2. Une émotion, toujours
Chaque contenu (Reel, story, carrousel) est conçu pour provoquer **une émotion nommée** : curiosité, surprise, rire,
choc (doux), émerveillement, tendresse, nostalgie, tristesse, fierté, frustration qui se résout, soulagement…
- Elle est déclarée dans `post.json` / `reel.json` : `"emotion": {"quoi": "surprise", "comment": "le visage qu'on
  croyait triste est le même que le joyeux", "ou": "diapo 4" ou "à 12 s"}`.
- Au contrôle, l'évaluateur dit quelle émotion il a ressentie et où, sans lire la déclaration d'abord. Aucune
  émotion ressentie = **refusé** (P2), même si tout le reste est propre. Une émotion différente de celle visée mais
  forte = acceptée, notée.
- Varier : pas la même émotion trois contenus de suite. Le « choc » ne passe jamais par la peur, la honte, la fausse
  urgence ou une image violente : c'est un renversement, une révélation, un chiffre vrai qui étonne.

## 3. Stories : courtes, instructives, créatives
**Depuis le 05/11** : plus aucune story de l'ancien cap (réserve retirée, programmées passées en brouillon). Les
stories reprennent seulement avec celles-ci, sans obligation d'une par jour.
- Une idée par jour, lisible en 2 secondes par image, qui apprend vraiment quelque chose (même hors business) ou fait
  jouer : quiz en 2 images (question → réponse), « devine avant de passer », illusion d'optique expliquée, vrai ou
  faux, mini-expérience à faire chez soi, coulisse d'un plan, « ce que ton cerveau fait quand… ».
- **Histoires fictives instructives** autorisées, très créatives (une fable en 2 ou 3 images, un personnage récurrent,
  un « et si… »), à une condition stricte : **la fiction se voit**. Elle est annoncée ou évidente (« Petite histoire
  inventée : », un personnage qui ne peut pas être réel, un monde stylisé) et ne se présente **jamais** comme un vrai
  client de Brooze, un vrai témoignage ou un vrai résultat. Aucun chiffre inventé présenté comme vrai.
- Les stories d'une semaine peuvent former une **série** (épisodes, personnage, défi sur 3 jours).
- La réserve de stories (`posts/_reserve-stories/`) suit la même ligne : les nouvelles stories de réserve sont
  fabriquées ainsi, les anciennes restent valables jusqu'à épuisement.

## 4. Carrousels : bien plus visuels, mieux designés, divertissants
**Un seul par semaine** (décision du 05/11) : tout le soin de la semaine va dans celui-là.
- **Visuel d'abord** : au moins 2 diapos sur 3 portent une image forte (rendu 3D, illustration en code, photo ou
  rush de Zak, schéma animé figé, montage d'images), pas seulement du texte sur fond uni. Le texte ancre, l'image
  raconte. Les mises en page actuelles (`cover`, `phrase`, `point`, `duel`, `liste`, `cta`) ne suffisent pas : en
  créer de nouvelles dans `templates/slide.html` (image pleine page avec légende, avant/après côte à côte, image
  annotée, grille de choix, révélation sur deux diapos, bande dessinée en cases…), dans la charte, vérifiées au rendu.
  Les images viennent des mêmes outils que les Reels (`reel/OUTILS.md` : three.js, Blender, Atelier, p5, procédural).
- **Divertissant** : un carrousel est un petit jeu ou une petite histoire qu'on fait défiler (on veut voir la diapo
  suivante) : énigme et réponse, test « laquelle ? », expérience en images, fiction en cases, « 5 images, une seule est
  retouchée ».
- **Design** : une direction artistique par carrousel (pas un gabarit qui change seulement de mots), cohérente avec la
  charte (≈ 70 % clair, un seul cuivre par image, Inter/Space Grotesk), et une planche qui donne envie au premier coup
  d'œil. Contrôle : la planche ne doit pas ressembler à celle des 3 carrousels précédents.

## 5. Oser, avec un risque géré
- **Un test osé par semaine environ** (Reel, story ou carrousel) : un format jamais fait, un ton plus drôle, une
  fiction, une rupture de rythme, un défi lancé à la communauté, une expérience interactive, un sujet hors business.
- Chaque test est déclaré : `"test_ose": {"quoi": "…", "pourquoi": "…", "risque": "…", "garde_fou": "…",
  "mesure": "indicateur et seuil", "arret": "ce qui fait arrêter"}`, noté dans `strategie.md` (hypothèses) et
  `journal.md`.
- **Ce qu'on peut oser** : la forme, le ton, l'humour, la fiction annoncée, le format, le sujet (tant qu'il se relie au
  métier), la longueur, la participation demandée.
- **Ce qu'on n'ose jamais** : tout ce qui touche aux garde-fous (rien d'inventé présenté comme vrai, marques réelles
  hors analyse, dénigrement, moquerie d'une personne ou d'un groupe, politique, religion, drame réel, peur ou fausse
  urgence, contenu choquant ou sexuel, sujets de santé présentés comme conseils), ni la charte, ni la voix de Zak.
- Un test qui déçoit n'est pas un échec : il est noté (mesuré, pas supposé) et on en tire une règle. Un signal négatif
  net (commentaires négatifs, désabonnements visibles dans la veille) arrête la série et se signale à Zak.

## 6. Ce qui ne change pas
Vérité (aucun chiffre, client, témoignage ou propos inventé présenté comme réel ; la fiction se voit), voix de Zak
dans les Reels (jamais modifiée, jamais réordonnée), charte, marques fictives hors analyse, pas de musique protégée,
contrôle qualité et verdict avant toute sortie.
