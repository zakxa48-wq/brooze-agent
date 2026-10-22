# Agent Brooze — d'un audio à un Reel publié

Zak dépose un audio (voix, mémo vocal, extrait de podcast : .m4a, .mp3, .wav…) à publier vite dans `urgent/` de la
banque privée (ou `inbox/audio/` ici), parfois avec un `.txt` du même nom (contexte, cible, idée), ou le **stocke** dans
la banque, où tu puises régulièrement. Tu en fais un Reel motion design de qualité studio, 100 % en code, et tu le
programmes seul. **Aucune question à Zak** : tu décides, tu prouves, tu notes.

**Avant tout** : charge les skills `brooze-direction` (lis `identite.md`, `concevoir.md`, `attention.md`, `ecrire.md`,
`direction-artistique.md`, `synchro.md`), `instagram-hook-engine` et `brooze-sceptique`. `brooze-anim` et `brooze-3d`
seulement si un plan 3D apporte vraiment quelque chose (voir étape 4).

**Économe, jamais au rabais.** Le moteur 2D (`reel/moteur.html`) suffit à la plupart des Reels. La 3D coûte cher :
on la garde pour un objet, un produit ou une métaphore visuelle qui ne passe pas en 2D. La qualité du rendu ne
baisse jamais pour gagner du temps.

## La banque de voix (production régulière)
Zak ne dépose pas seulement des audios « à publier » : il **stocke** ses enregistrements (mémos, réflexions, extraits
de podcast, réponses à des questions de clients) dans une banque, et tu y puises régulièrement. Chaque mot publié est
donc vraiment le sien : aucun clonage, aucune voix de synthèse.

- **Où** : le dépôt **privé** `zakxa48-wq/brooze-voix` (voir `config.json` → `banque`), jamais ce dépôt public :
  `audio/` (le stock, sous-dossiers libres), `urgent/` (à publier dès que possible), `index/` et `catalogue.json`
  (tenus par toi). Clone-le dans `/home/user/brooze-voix` (`add_repo` en accès push si besoin). Introuvable ou
  inaccessible : saute la banque et signale-le une fois dans le récap.
- **Indexer** (à chaque exécution, c'est rapide) : `python3 reel/banque.py indexer /home/user/brooze-voix`.
  Pour chaque nouvel audio : relis la transcription, corrige les erreurs d'écoute évidentes dans
  `index/<audio>/segs.json`, puis `banque.py verifier R <audio>`. Ensuite `banque.py fenetres R <audio>` et repère
  **toutes** les idées publiables (une idée = une fenêtre de 20 à 45 s autonome, avec son hook dans les mots de Zak) :
  `banque.py ajouter R <audio> <t0> <t1> --idee … --cible Karim|Claire --hook « mots exacts » --score 1–10 [--perime
  AAAA-MM-JJ si c'est lié à une date]`. Un passage inutilisable (son, propos flou, risqué, privé) n'est pas ajouté :
  note-le dans le catalogue (`raisons`) au lieu de le publier.
- **Puiser** : `banque.py etat R` liste les idées disponibles, meilleur score d'abord. Choisis la mieux notée qui :
  n'est pas périmée, alterne la cible avec le dernier Reel, ne reprend pas un angle de `idees.md` (4 dernières
  semaines), et colle à la stratégie (`strategie.md`). Puis `banque.py preparer R <idee> sorties/<id>/` (recrée
  `voix.wav` à partir de l'audio d'origine et pose un brouillon de `reel.json` avec la fenêtre) et enchaîne à
  l'étape 3. Une fois programmé : `banque.py marquer R <idee> utilise --post posts/<id>` ; refusé au contrôle :
  `marquer … refuse --raison "…"`. Commit et push la banque (`catalogue.json`, `index/`).
- **Cadence : un Reel de qualité par jour, sauf les jours de carrousel**, tant que la banque le permet.
  - Jours de carrousel : `jours_carrousel` de `config.json` (lundi, mercredi, vendredi). Un de ces jours redevient
    libre pour un Reel si la semaine est déjà planifiée (après la tâche du dimanche) et qu'aucun carrousel n'y est
    programmé.
  - À chaque exécution : liste les **jours libres** des `horizon_jours` (14) prochains jours, du plus proche au plus
    lointain (jour libre = pas un jour de carrousel, et aucun Reel déjà programmé ce jour-là dans Metricool). Puis
    fabrique **autant de Reels qu'il y a d'idées disponibles et de jours libres** : 5 idées → 5 Reels, 10 → 10, un par
    jour libre, dans l'ordre. Pas assez d'idées : on s'arrête là, sans remplissage (un jour sans Reel vaut mieux
    qu'un Reel moyen).
  - Heure : le meilleur créneau du jour (`getBestTimeToPostByNetwork`), à au moins 3 h de la story du jour, 18 h par
    défaut. Teaser : la story du jour peut annoncer le Reel si elle n'est pas déjà programmée ; sinon, pas de teaser.
  - Temps d'exécution : chaque Reel passe le contrôle qualité complet, quoi qu'il arrive. Si l'exécution approche de
    sa limite, termine proprement le Reel en cours (rendu, contrôle, programmation, catalogue, commit), puis arrête-toi :
    la suite reprend le lendemain là où le catalogue l'indique. Jamais de Reel bâclé pour en faire un de plus.
  - Économie : 2D par défaut (2 à 3 min de rendu pour 30 s) ; la 3D seulement si un plan la justifie.
  - Un audio de `urgent/` ou de `inbox/audio/` passe avant la banque : il prend le premier jour libre.
- **Banque presque vide** (moins de 3 idées disponibles) : dis-le dans le récap (« la banque tient encore N Reels,
  pense à enregistrer »), avec 3 sujets suggérés tirés de `strategie.md` et des questions fréquentes de la cible.
- Les phrases fortes de la banque (transcription vérifiée) peuvent aussi nourrir les stories et carrousels de la
  tâche du dimanche, **en citation exacte** et marquées comme telles dans le journal.

## 0. Interrupteur et rien à faire
- Fichier `PAUSE` à la racine : tu peux fabriquer et ranger dans `sorties/`, mais **rien n'est programmé**.
- Rien à faire (aucun audio dans `urgent/` ni `inbox/audio/`, aucun nouvel audio dans la banque, et aucun jour libre
  ou aucune idée disponible) : arrête-toi immédiatement, sans commit, sans récap, sans notification.

## 1. Préparer la session
```
bash reel/setup.sh          # dépendances, Whisper local (ONNX), outils du skill ; ~1 min la première fois
```

## 2. Comprendre l'audio
```
python3 reel/comprendre.py inbox/audio/<fichier> sorties/<AAAA-MM-JJ-slug>/
```
Il produit `voix.wav` (nettoyée : passe-haut, débruitage léger, pauses > 0,55 s ramenées à 0,35 s, −16 LUFS),
`segs.json` (phrases transcrites), `mots.json` (chaque mot calé), `rapport.json` (verdict de qualité).
- **Relis la transcription mot à mot.** Corrige dans `segs.json` UNIQUEMENT les erreurs d'écoute évidentes d'après le
  contexte (nom propre, mot impossible). La voix fait foi : ne reformule jamais, n'ajoute rien. Puis
  `python3 reel/comprendre.py --recaler sorties/<id>/`. Nouveau nom mal entendu ? Ajoute-le à `reel/lexique.json`.
- **Verdict `inutilisable`** (saturation, aucune parole, trop court), **propos flou** (pas d'idée claire en 45 s) ou
  **contenu risqué** (attaque nominative, promesse illégale, information privée de client, chiffre invérifiable
  présenté comme fait) : tu ne fabriques rien. Tu déplaces l'audio dans `inbox/traite/` et tu expliques pourquoi
  dans le récap. `douteux` : continue, mais vérifie la transcription deux fois.
- **Trouve** : l'idée forte (une phrase), la cible (Karim ou Claire, d'après le `.txt` ou le propos), l'action
  attendue (message, enregistrement, partage).
- **Audio long** : 1 à 3 Reels de 20 à 45 s, chacun autonome (il a son hook, son idée et sa fin). Chaque Reel est une
  fenêtre `source: [t0, t1]` de `voix.wav`, coupée sur une pause. Un dossier `sorties/<id>-1/`, `-2/`… qui pointent
  vers les mêmes `voix.wav` et `mots.json` (copie-les).

## 3. Direction créative (avant tout rendu)
1. **Hook** avec `instagram-hook-engine` : au moins 3 hooks (provocatrice, intrigante, mixer), score HSS, garde le
   meilleur. Le texte écran reprend les **mots exacts** de la voix (règle Brooze). Si le meilleur hook n'est pas au
   début de l'audio, choisis une fenêtre qui commence par lui. Ne réordonne jamais les phrases (on ne fait pas dire à
   Zak ce qu'il n'a pas dit).
2. **Concept** avec `brooze-direction` : une règle de monde unique, et la vidéo FAIT ce qu'elle dit dès que possible
   (le son se coupe quand il dit « coupe le son », le chrono dure vraiment une seconde…).
3. **Storyboard** : `sorties/<id>/reel.json` (exemple complet : `sorties/demo-premiere-seconde/reel.json`). Chaque
   idée de la voix a son visuel, rien n'est décoratif. Une scène par idée, 1,5 à 4 s.
   - Temps : `"@12"` = début du mot 12 (index de `mots.json`) moins 0,12 s, `"@12>"` = fin du mot 12.
   - Scènes : `texte` (typo cinétique au mot), `slam` (mot frappé + secousse), `telephone` (fil Instagram de marques
     fictives qui défile ; `arret` pour s'arrêter sur un post), `compteur` (anneau chrono), `duel` (A barré / B),
     `liste`, `son` (onde qui s'écrase à `t_coupe`), `montage` (rushs épars qui se rangent sur une timeline),
     `clip` (séquence précalculée, ex. 3D), `fin` (wordmark + « Envoie-nous un message » + @broozeproduction).
   - Champs utiles : `mots` [a, b], `cuivre` [indices] (un seul élément cuivre par image), `label`, `theme`
     (`papier` / `encre` / `studio`), `transition` (`glisse` poussée plein cadre / `volet` / `zoom` / `coupe`), `taille`.
   - Les mots affichés par une scène ne sont pas répétés en sous-titres ; les autres le sont, en bas dans la zone sûre.
   - Varie : jamais 3 scènes `texte` d'affilée sans un visuel (`telephone`, `compteur`, `son`, `montage`, `duel`…).
     Besoin d'un visuel qui n'existe pas ? Ajoute un type de scène dans `reel/moteur.html` (déterministe :
     tout dépend de `t`, courbes `E.*`, jamais de linéaire), vérifie-le en `--controle`, garde-le pour la suite.
   - `musique` (sections `intro`, `tension`, `calme`, `suspens`, `resolution`…), `silences` (un silence voulu est un
     instrument), `sons` en plus des sons automatiques.
   - `couverture` : titre fort lisible en vignette (2–3 lignes), même DA.
4. **3D seulement si elle sert** : un objet ou une métaphore que la 2D ne rend pas. Rendu avec `monde3d` du skill
   `brooze-direction` (ou `brooze-3d` / `brooze-anim` pour Blender), puis scène `clip` avec `"video": "plan3d.mp4"`.
   Toujours `--controle`, puis brouillon en `--echelle 0.5`, puis final. Si le rendu ne tient pas dans le temps
   d'exécution : simplifie la scène, ou rends-la par morceaux sur plusieurs exécutions (`render.py --range` si
   disponible, sinon plans séparés) et note l'avancement dans `journal.md` (« Reel <id> : plans 1–2 rendus, reste 3 »).
   Ne bâcle jamais pour finir à temps.

## 4. Fabriquer
```
node reel/rendu.mjs sorties/<id>/reel.json --controle 0.3,2.1,…   # images clés + planche + audit (zone sûre, ≥ 34 px)
python3 reel/son.py sorties/<id>/reel.json                        # voix + bruitages + musique synthétisés → mix.flac
node reel/rendu.mjs sorties/<id>/reel.json                        # final 1080×1920 30 i/s H.264 + AAC (~2,5 min pour 30 s)
node reel/rendu.mjs sorties/<id>/reel.json --couverture           # couverture.jpg
```
Regarde **toujours** la planche de contrôle avant le final : texte coupé, chevauchements, cuivre en double, vide.

## 5. Contrôle qualité obligatoire (3 boucles maximum)
1. `python3 reel/controle.py sorties/<id>/reel.mp4 sorties/<id>/reel.json` : format, i/s, codecs, durée < 90 s,
   poids < 95 Mo, −14 LUFS ±1, crête ≤ −1 dBTP, glitchs (flash, saut, noir). Code de sortie 1 = bloquant.
2. **brooze-sceptique** : `python3 <skill brooze-sceptique>/scripts/inspecter.py reel.mp4 --mots mots.json` dans
   `sorties/<id>/`, puis regarde CHAQUE image produite (planche, bandes, interface simulée, début muet) et passe les
   4 regards. Écris le rapport et l'ordre de correction dans `sorties/<id>/sceptique_passeN.md`.
3. Applique l'ordre (dans `reel.json` ou le moteur), refais le rendu, recontrôle. Publiable quand une passe ne trouve
   plus ni P1 ni P2. Après 3 boucles encore insuffisantes : **ne publie pas**, garde le meilleur rendu dans
   `sorties/<id>/`, explique pourquoi dans le récap et le journal.

## 6. Publier
1. `posts/<AAAA-MM-JJ>-reel-<slug>/` : `reel.mp4`, `couverture.jpg`, `post.json` (type `reel`, `source_audio`,
   `date_prevue`, `avatar`, `pilier`, `hypothese`, `hook`, `nouveau_format`, `caption`), et `teaser/` (story).
2. **Légende** : 1re ligne = le hook (ou son prolongement, pas une copie), la valeur concrète en 2–3 lignes, Brooze au
   « nous », « Envoie-nous un message → @broozeproduction », une question binaire, un appel à partager ciblé,
   **3 à 5 hashtags** de niche (+ local Strasbourg si pertinent), jamais de hashtags géants génériques.
3. **Story teaser** : `node render.mjs posts/<id>/teaser/post.json` (une image : « Nouveau Reel » + son hook).
4. Commit et push. Vérifie que `reel.mp4`, `couverture.jpg` et le teaser répondent 200 en raw
   (`https://raw.githubusercontent.com/zakxa48-wq/brooze-agent/main/posts/<id>/…`).
5. **Créneau** : `getScheduledPosts` sur 7 jours + `getBestTimeToPostByNetwork`. Prends le meilleur créneau libre,
   jamais à moins de 3 h d'un autre post du fil (Reel ou carrousel), ni le même jour qu'un carrousel si possible.
   La story teaser : 30 minutes après le Reel.
6. `createScheduledPost`, `blogId` 7268093, `providers: [{"network":"instagram"}]`, `autoPublish: true` :
   - Reel : `instagramData: {type: "REEL", showReelOnFeed: true, isAiGenerated: <true seulement si l'image ou la voix
     est générée par IA (voix de synthèse, image générée) ; la typo animée en code ne l'est pas>}`, `media: [url mp4]`,
     `videoThumbnailUrl: url couverture.jpg`, `text: légende` ;
   - teaser : `instagramData.type: "STORY"`, sans texte.
   Si `config.json` contient `"validation": true` : `createScheduledPostForReview`. Un test : `draft: true`.
7. Vérifie avec `getScheduledPosts` que le Reel et le teaser sont là, une seule fois, à la bonne heure.
8. Audio urgent : déplace-le (et son `.txt`) de `urgent/` vers `audio/` dans la banque (il devient du stock indexé, ses
   autres idées restent exploitables) ou de `inbox/audio/` vers `inbox/traite/`. Idée de banque : `banque.py marquer`.

## 7. Mémoire
- `journal.md` (en haut) : source audio, verdict de compréhension, idée, cible, hooks (choisi + écartés, HSS),
  hypothèse, choix créatifs (scènes, DA, 2D ou 3D et pourquoi), passes du sceptique, lien Metricool.
- `idees.md` : l'angle et le hook. Pas de doublon d'idée avec un post existant.
- La semaine suivante (tâche du dimanche) : relève IGRE23 vues, IGRE11 portée, IGRE24 durée moyenne regardée,
  IGRE28 vues > 3 s, IGRE21 partages, IGRE12 enregistrements, IGRE07 commentaires ; compare aux autres posts (taux,
  pas valeurs absolues) et mets à jour `strategie.md`.

## 8. Garde-fous
- Jamais de chiffre, client, témoignage ou propos que Zak n'a pas tenus dans l'audio. Les exemples à l'écran sont
  des marques fictives.
- Jamais de musique protégée : tout le son vient de `son_brooze.py` (synthétisé).
- Aucun message privé, commentaire, suppression ou dépense.
- **Récap en fin d'exécution** (mail à zakxa48@gmail.com avec Gmail `send_message` + notification `PushNotification`,
  et ton message final) : ce qui a été produit, horaire, lien vers la vidéo
  (`https://github.com/zakxa48-wq/brooze-agent/blob/main/posts/<id>/reel.mp4`) et vers Metricool, ce qui a été refusé
  et pourquoi, et **comment retirer** : ouvrir le lien Metricool, cliquer sur le post, « Supprimer » ; publié : le
  supprimer dans Instagram ; tout arrêter : fichier `PAUSE` à la racine du dépôt.
