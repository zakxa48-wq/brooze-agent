# Le cerveau de l'agent Brooze : apprendre, pratiquer, mesurer

**Ce que c'est, honnêtement** : une mémoire écrite et des règles qui grandissent avec les données de Zak et les
résultats du compte. Le modèle d'IA n'est pas entraîné. L'agent relit cette mémoire avant d'agir et la met à jour
après. Il sépare toujours ce qui est **mesuré** (chiffres, fichiers, dates) de ce qui est **supposé** (intuition), et
n'annonce jamais un succès sur les vues seules.

- **Données** : dépôt PRIVÉ `brooze-voix`, dossier `data/` (R = `/home/user/brooze-voix`). Jamais dans brooze-agent
  (public) : ni fiche, ni image clé, ni transcription, ni référence.
- **Outils** (code, ici) : `reel/cerveau.py` (analyse, fiches, recherche, comparaison, débriefs, progression),
  `reel/savoir.py` (connaissances du monde : sources, notions, affirmations, liens),
  `reel/techniques.py` (bibliothèque de techniques), `reel/controles/` (contrôles appris).
- **Qui fait quoi** :
  - **Brooze montage inbox** (3 h 41 et 15 h 41) : apprendre (§ 1), utiliser (§ 2), débriefer (§ 3), s'entraîner (§ 4).
    Chaque jour, au passage de 3 h 41 (rattrapée à 15 h 41 si besoin) : la séance d'apprentissage du savoir (§ 8).
  - **Brooze relevé stats** (tous les jours, 8 h 57) : le relevé brut dans brooze-kit (`data/`, `tools/analytics.py`)
    et l'alerte immédiate si quelque chose est grave. Elle n'a pas accès aux dépôts de l'agent.
  - **Brooze montage inbox, passage de 15 h 41** : la veille du compte (§ 5), la révision du dimanche (§ 6) et le bilan
    du 1er du mois (§ 7), directement avec Metricool (getAnalyticsDataByMetrics, getScheduledPosts), et en relisant
    les relevés de brooze-kit s'il est accessible (sinon Metricool suffit). Une seule source de vérité pour les
    chiffres bruts : les réponses Metricool enregistrées dans `brooze-voix/data/cerveau/releves/AAAA-MM-JJ.json`.

## 1. Apprendre (chaque exécution de montage, AVANT de produire)
1. `python3 reel/cerveau.py nouveaux R` liste ce que Zak a déposé depuis la dernière fois.
2. **Vidéo ou image** (`references/`, `mes-videos/`) : `cerveau.py analyser R <fichier>` (environ 2 à 3 min pour 40 s)
   → fiche avec mesures et une planche d'images clés. **Regarde la planche** (outil Read), lis la note `.txt` de Zak,
   puis `cerveau.py completer R <id> --resume "…" --efficace "…" --a-eviter "…" --tags "hook,rythme,…" --qualite N`.
   - `efficace` : ce qui la fait marcher, en principes transposables (« 3 coupes avant 1,5 s, chacune sur un accent »),
     jamais en description à recopier.
   - `a_eviter` : ce qu'elle fait mal ou ce qui serait une copie si on le reprenait.
   - `qualite` : 1 à 10, niveau de finition et d'efficacité **estimé** par l'agent (dire « estimé »). Les vidéos
     de `mes-videos/` validées par Zak servent de référence de niveau.
3. **Retour de Zak** (`retours/`) : `cerveau.py texte R <fichier>` (transcrit un mémo vocal) → en faire une **règle
   précise et datée** dans `principes.md` (type `retour de Zak`, confiance forte sur sa préférence), puis
   `completer … --regles "…"`. Un retour qui contredit une règle existante la corrige (et la note dans « Retirées »).
   Conversations et rendez-vous (`conversations-AAAA-MM.txt`) : reporte chaque ligne dans brooze-kit avec
   `python3 tools/analytics.py conv …` (attache brooze-kit avec add_repo si besoin) et dans `marketing.md`.
3 bis. **Question de Zak** (`retours/question-AAAA-MM-JJ.txt`) : à chaque passage, une question sans réponse reçoit
   une réponse honnête dans le récap envoyé à Zak ET dans `journal.md` (« Réponse à la question du JJ/MM »), puis la
   ligne `RÉPONDU le JJ/MM` en bas du fichier. Une question n'est jamais un ordre de bâcler ou de presser un Reel.
4. **Document** (`docs/`) : `cerveau.py texte R <fichier>` → principes réutilisables (type `document`, confiance
   « à vérifier » tant que la pratique ou les chiffres ne les ont pas confirmés), avec la source exacte.
5. **Des fiches aux principes** : une règle `mesuré` naît quand **au moins 3 fiches** (ou 5 Reels pour les résultats)
   vont dans le même sens, chiffres à l'appui. En dessous : une ligne « piste » dans la fiche, pas un principe.
6. `bash outils/git_main.sh fin R "cerveau : N fiches, M principes"`.

## 2. Utiliser le cerveau en produisant (avant chaque Reel)
1. `python3 reel/cerveau.py chercher R "<propos du Reel, cible, ton>" --n 5` → les 5 fiches et principes utiles.
2. Dans `sorties/<id>/intention.md` et le journal : **lesquels tu appliques et pourquoi**, lesquels tu écartes.
3. **Inspiration, jamais copie** : d'une référence tu retiens un principe (rythme, tension, rapport texte/image), jamais
   un plan, un visuel, un texte, une musique ou un enchaînement reconnaissable. Test : si quelqu'un qui connaît la
   référence la reconnaîtrait dans le Reel, c'est une copie → refaire.
4. **Contrôle qualité, en plus de controle.py et du sceptique** :
   `python3 reel/cerveau.py comparer R sorties/<id>/reel.mp4` mesure le Reel et le compare aux meilleures fiches
   (qualité ≥ 7) sur le **rythme** (durée des plans, coupes des 3 premières secondes), la **lisibilité** (taille et
   quantité de texte) et la **finition** (netteté, niveau sonore, coupes sur la voix). « EN DESSOUS » = une boucle de
   correction de plus (dans la limite des 3 boucles). Sans référence vidéo dans la base : non bloquant, le dire.

## 3. Apprendre en pratiquant (après chaque Reel, publié ou non)
1. Débrief dans `pratique.jsonl` :
   `python3 reel/cerveau.py pratique R '{"reel": "<id>", "minutes": 95, "etapes_longues": ["rendu 3D 40 min"],
   "boucles": 2, "p1": 1, "p2": 3, "defauts": [{"categorie": "synchro", "detail": "…"}],
   "techniques": {"bien": ["relief-2-5d"], "decu": []}, "autrement": "…", "comparer": "au niveau"}'`
   Catégories de défauts (stables, pour compter) : `synchro`, `lisibilite`, `saccade`, `texte-trop-long`, `hook-mou`,
   `rythme`, `son`, `couleur`, `cadrage`, `redite`, `finition-3d`, `autre`.
2. `reel/techniques.py utilisee <id> <reel> [--note N]` pour chaque technique employée ; la technique nouvelle du Reel
   est ajoutée avec `techniques.py ajouter` (démo de 2–3 s en 540 px dans `reel/techniques/demos/`, note 1–10 et
   pourquoi). Une déception : `techniques.py decue <id> "pourquoi"` ; à la deuxième, elle est retirée automatiquement
   et la raison va dans `principes.md`.
3. `python3 reel/cerveau.py recurrents R` : un défaut vu **deux fois** devient une règle (`principes.md`, type
   `pratique`) **et** un contrôle automatique dans `reel/controles/` (voir son LISEZMOI), testé sur le Reel fautif.

## 4. S'entraîner (quand il n'y a rien à produire)
S'il n'y a ni Reel en cours, ni audio, ni jour libre avec une idée, et qu'il reste du temps : un exercice, **sans
rien publier** (30 min maximum, puis récap court, sans mail) :
- refaire un ancien Reel autrement (autre concept, autre technique) sur sa voix d'origine ;
- ou tester une technique nouvelle sur un extrait déjà utilisé.
Mesure (controle.py, sceptique, `cerveau.py comparer`) et compare au **meilleur rendu précédent** du même extrait.
Range l'exercice dans `data/cerveau/entrainement/AAAA-MM-JJ-<sujet>/exercice.md` (but, méthode, mesures, verdict,
planche), débrief `pratique` avec `"exercice": "<sujet>"`. Ce qui est meilleur rejoint la bibliothèque de techniques.
Les vidéos d'exercice ne sont pas versionnées.

## 5. Veille quotidienne du compte (passage de 15 h 41 de Brooze montage inbox, chaque jour)
1. Relevé brooze-kit habituel (`docs/analyse-donnees.md` § 1 : reels + compte, `ingest`, `check`), puis en plus :
   `getAnalyticsDataByMetrics` connecteur `posts` (carrousels) et `stories` sur 7 jours, et `getScheduledPosts` sur
   les 3 derniers jours (statut de chaque publication programmée).
2. Pour chaque post de moins de 7 jours : vues, vues > 3 s (IGRE28), durée moyenne (IGRE24), rétention, partages,
   enregistrements, commentaires, abonnés gagnés ; comparé **à âge égal** à la médiane du compte et du même format.
3. **Détecter** :
   - un post qui décolle (≥ 2× la médiane du format à âge égal) ou s'effondre (≤ 0,5×) ;
   - un pic ou une chute d'abonnés ;
   - une publication programmée qui n'est pas partie (statut d'erreur ou toujours en attente après l'heure) ;
   - des commentaires qui reviennent (le nombre est mesuré ; le **texte** des commentaires et des messages n'est pas
     lisible par Metricool : Zak les copie dans `retours/` s'il veut que l'agent les connaisse).
4. **Réagir** :
   - `veille.md` (en haut) : le relevé et les détections, mesuré ou supposé ;
   - `principes.md` / `strategie.md` (brooze-agent) : seulement ce que les chiffres montrent, avec les règles
     d'honnêteté (âge égal, médianes, pas de conclusion forte sous 5 Reels comparables) ;
   - sujets réclamés par l'audience (retours de Zak, questions qui reviennent) → `idees.md` de brooze-agent, section
     « Demandés par l'audience », pour la tâche du dimanche et la banque ;
   - format qui surperforme nettement (≥ 2× sur au moins 2 posts) → une demande « variante originale (pas une
     copie) » dans `veille.md` § Demandes ; la tâche de montage la traite au prochain jour libre ;
   - publication échouée → la reprogrammer **une seule fois** au prochain bon créneau (`createScheduledPost`, mêmes
     médias et texte), le noter dans `veille.md` et le journal de brooze-agent ;
5. **Jamais** : répondre à un commentaire ou un message, liker, suivre, supprimer, dépenser.
6. **Alerte** (PushNotification, et mail seulement si urgent) **uniquement** si : post viral (≥ 3× la médiane),
   chute forte (abonnés ou vues ≤ 0,4× sur 3 jours), échec de publication, commentaire ou message signalé qui demande
   une réponse humaine. Sinon : rien.

## 6. Révision du dimanche (passage de 15 h 41 du dimanche)
1. **Résultats × choix** : pour chaque Reel de plus de 7 jours, relie ses stats (IGRE24, IGRE28, IGRE12, IGRE21, et
   conversations de `marketing.md`) à ses choix (registre de `journal.md` : hook, concept, structure, technique,
   durée des plans de sa fiche). Écris le constat dans `principes.md` comme `mesuré` seulement à partir de **5 Reels
   comparables** ; avant, une ligne « piste » avec les chiffres.
   **Revisionnage** (objectif de Zak du 23/10) : pour chaque Reel, `revisionnage = IGRE24 / durée` (au-dessus de 1 :
   des gens le regardent plus d'une fois), rétention IGRE27, vues > 3 s IGRE28, croisés avec ses mesures
   d'engagement (`engagement.json` : écart max entre relances, raccord de boucle, durée, clins d'œil) ; ce qui fait
   vraiment monter le revisionnage sur le compte → `principes.md` (`mesuré` à partir de 5 Reels comparables).
2. **Consolidation de principes.md** : fusionner les doublons ; renforcer (et dater « Vérifié le ») les règles
   confirmées par la pratique ou les chiffres ; baisser d'un cran la confiance de celles jamais vérifiées depuis 4
   semaines ; retirer celles que les faits contredisent (section « Retirées », avec la preuve).
3. `python3 reel/cerveau.py progression R` (tableau par semaine). Ajoute à la main la colonne résultat Instagram
   (médianes de la semaine). **Deux semaines sans progrès** (boucles, défauts, minutes, résultats) : cherche pourquoi
   dans les débriefs, écris un diagnostic dans `progression.md` et change de méthode (autre ordre d'étapes, autre
   outil, plus de références, plus d'entraînement) — puis vérifie l'effet deux semaines plus tard.

## 7. Bilan du 1er du mois (passage de 15 h 41 du 1er)
1. **Entonnoir** du mois écoulé dans `marketing.md` : vues → taps du lien en bio (IGAC12 avec contactButtonType) →
   conversations (déclarées par Zak) → qualifiées → rendez-vous (déclarés dans `retours/`). Le **point de blocage** est
   l'étape où le taux chute le plus par rapport au mois précédent (ou, sans historique, par rapport à l'étape d'avant).
2. **CTA** : chaque CTA est une hypothèse, **un seul changement à la fois**, jugé sur les conversations amenées
   (≥ 5 posts) : mot-clé en message (« RUSH »), question en commentaire, lien en bio, offre concrète (« on transforme
   3 de tes vidéos »). Tableau dans `marketing.md`.
3. **Équilibre éditorial** : part des posts pour attirer, prouver, convertir, et conversations par type ; ajuster les
   proportions sur les conversations, pas les likes.
4. **Profil** : bio, stories à la une, posts épinglés → propositions **au texte exact**, jamais appliquées par l'agent.
5. **Mail à Zak (15 lignes maximum)** : conversations qualifiées du mois et évolution ; les 3 contenus qui en ont le
   plus amené et pourquoi (mesuré ou supposé, dit comme tel) ; le point de blocage ; **une** décision stratégique pour
   le mois suivant ; les propositions de profil en une ligne chacune.
6. La décision va dans `decisions.md` avec sa date limite (le 4) ; le relevé du 4 (ou après) l'applique dans
   `strategie.md` s'il n'y a pas de `retours/objection-AAAA-MM.txt`, et le note. Avec une objection : non appliquée,
   la raison de Zak devient un principe.

## 8. Le savoir : apprendre du monde, chaque jour (séance d'apprentissage)
Le cerveau a deux mémoires. `principes.md` dit **comment Brooze travaille** (règles tirées de la pratique, des
retours de Zak et des chiffres du compte). Le **savoir** (`data/cerveau/savoir/`, outil `reel/savoir.py`) dit **ce que
l'on sait du monde** : psychologie de l'attention, perception, montage, motion design, 3D et lumière, son,
copywriting, Instagram, marketing des PME, vente d'un studio. Il est fait de **notions** reliées entre elles, chacune
portant des **affirmations** avec leurs preuves (sources pondérées) et ce qu'elle change dans le travail.

**Séance quotidienne, obligatoire** : au passage de 3 h 41, juste après le filet des stories, 20 minutes, avant la
production. `python3 reel/savoir.py aujourdhui R` répond « faite » ou non ; si elle a été sautée, le passage de 15 h 41
la fait avant la veille. Un jour sans séance n'existe pas (sauf réseau et recherche totalement indisponibles : noter
pourquoi dans `seances.jsonl`).
1. **Se souvenir d'abord** : `savoir.py verifier R` (rien d'oublié depuis hier ; un oubli se restaure depuis git avant
   tout), `savoir.py etat R`, `savoir.py rappel R` (3 notions les moins revues).
2. **Choisir quoi apprendre** (`savoir/questions.md`, tenu par l'agent) : ce qui a manqué pendant le dernier Reel
   (`pratique.jsonl`), ce que la veille n'explique pas, les principes « à vérifier », le propos des **prochains Reels**
   (apprendre en avance ce qu'ils vont demander : Koulechov → perception, montage soviétique, études de réplication),
   ce que Zak a déposé dans `data/connaissances/` ou `data/docs/`. Une ou deux questions par séance, approfondies
   plutôt que survolées ; varier les domaines d'une semaine à l'autre.
3. **YouTube d'abord** (demande de Zak du 27/10) : chaque séance commence par YouTube, et la majorité des sources
   absorbées en viennent : conférences et cours, monteurs et motion designers reconnus, chaînes de vulgarisation
   scientifique, décryptages de pubs, créateurs qui montrent leurs chiffres. Pour chaque vidéo : la transcription
   complète (`yt-dlp --skip-download --write-auto-subs --sub-langs "fr.*,en.*" --sub-format vtt <url>`, `lu: complet`),
   les idées extraites avec le minutage, et la vidéo jugée pour ce qu'elle est (`type` selon l'auteur : chercheur qui
   présente son étude → `etude` si l'étude est citée et retrouvée, praticien reconnu → `praticien`, sinon `video`).
   Prioriser YouTube pour la quantité ne veut pas dire le croire davantage : une affirmation forte vue sur YouTube est
   recoupée par une étude ou par les chiffres du compte avant de monter à `solide`. Sans accès au réseau, les
   transcriptions sont impossibles : noter les vidéos trouvées par WebSearch (`lu: resume`) dans `questions.md`
   (« à transcrire ») pour les reprendre dès que le réseau est ouvert.
   **Lire une vidéo YouTube** (règle de Zak du 27/10), dans cet ordre :
   1. le **connecteur vidIQ** d'abord (`vidiq_video_transcript`, chargé avec ToolSearch ; il passe par son API, pas
      par le réseau de l'environnement) → transcription complète, `lu: complet` ;
   2. en secours, `yt-dlp` (sous-titres) puis la page elle-même ;
   3. si tout échoue : `lu: resume`, la vidéo reste dans la file `savoir.py a-lire`.
   **Réseau** : le mode est « Limité » ; domaines ouverts le 27/10 : youtube.com et sous-domaines, ytimg.com,
   googlevideo.com, wikipedia.org, wikimedia.org, arxiv.org, openalex.org, doi.org, ncbi.nlm.nih.gov, plos.org,
   frontiersin.org, academic.oup.com, researchgate.net, nature.com, springer.com, sciencedirect.com, tandfonline.com,
   sagepub.com, apa.org. Un domaine utile refusé se **signale** (récap + `questions.md`, avec le domaine exact), il ne
   se contourne jamais (pas de miroir, pas de proxy, pas de copie tierce d'un article payant).
   **File de lecture** : chaque séance commence par `savoir.py a-lire` (sources lues seulement en résumé) : en relire
   au moins 2 en entier, mettre à jour la source (`source` avec le même lien et `lu: complet`), corriger les notes des
   preuves si la lecture complète dit autre chose (sens compris), puis `savoir.py recalculer`. Une affirmation ne
   reste jamais durablement fondée sur des résumés.
   **Puis compléter ailleurs** : WebSearch (études : Google Scholar, PubMed, arXiv, revues ; vidéos YouTube de
   praticiens reconnus ; livres ; documentation officielle des plateformes ; cours ; articles d'experts), plusieurs
   sources de natures différentes par question, en français et en anglais. Lire vraiment quand le réseau le permet :
   WebFetch pour une page, `yt-dlp --skip-download --write-auto-subs --sub-langs "fr.*,en.*" --sub-format vtt <url>`
   pour les sous-titres d'une vidéo, `pypdf` pour un PDF. Le champ `lu` dit honnêtement ce qui a été lu : `complet`,
   `extrait`, ou `resume` (seulement le résumé du moteur de recherche, poids divisé par deux).
4. **Juger la source** avant de la croire (`type`) : `meta-analyse` > `etude` (évaluée par des pairs : taille de
   l'échantillon, réplication) > `mesure-compte` (les chiffres du compte de Zak, qui pèsent lourd) > `livre`,
   `doc-plateforme` > `praticien`, `cours` > `video`, `article` > `vendeur` (chiffres d'un outil qui vend quelque
   chose, souvent sans données) > `opinion`. Un chiffre sans source traçable n'est jamais une preuve.
5. **Relier à ce qu'on sait déjà, puis intégrer** :
   - `savoir.py chercher R "<sujet>"` d'abord : on rattache à une notion existante plutôt que d'en ouvrir une nouvelle ;
   - `savoir.py source R '{"titre","type","lu","url"|"fichier","auteurs","annee","resume"}'` ;
   - `savoir.py affirmer R '{"id": "A-…", "source", "sens": 1|-1, "note"}'` : de préférence une **preuve de plus**
     (pour ou contre) sur une affirmation connue. Nouvelle affirmation seulement si elle dit vraiment autre chose
     (l'outil montre les affirmations proches et refuse le doublon) ;
   - une nouvelle notion (`savoir.py notion`) reçoit au moins un lien (`savoir.py lier`) vers ce qu'on savait :
     une connaissance isolée ne sert pas ;
   - réécrire la page de la notion **en précisant**, jamais de zéro : « Ce que j'en comprends » (synthèse dans ses mots,
     nuances, conditions où ça marche ou pas) et « Ce que ça change dans mon travail » (la compétence : quand, comment,
     sur quel moment d'un Reel, d'une story, d'un CTA). C'est là que le savoir devient compétence.
6. **La confiance s'affine, elle ne bascule pas** (calculée par l'outil) : `à vérifier` → `probable` → `solide` (au
   moins 2 sources indépendantes dont une étude ou une mesure du compte). Une nouvelle preuve déplace le niveau d'un
   seul cran ; une contradiction sérieuse marque l'affirmation `contestée` et se garde (avec ses deux côtés) jusqu'à
   ce que de nouvelles preuves tranchent. On ne change jamais tout parce qu'une source le dit.
7. **Consolider** : relire les 3 notions du rappel, les relier à ce qui a été appris depuis, préciser leur synthèse,
   `savoir.py revu R <notion> "ce qui a été consolidé"`. Une affirmation devenue `probable` ou `solide` qui change la
   pratique entre dans `principes.md` (type `document`, avec l'id `A-…`), et la règle devient vérifiable sur le compte.
8. **Clore** : `savoir.py carte R`, `savoir.py verifier R`, `savoir.py seance R '{…}'` (requêtes, sources, notions,
   affirmations, liens, revues, ce que ça change, questions ouvertes, limites), questions nouvelles dans
   `questions.md`, push de brooze-voix.

**Comment le savoir se voit** : pas en parlant de soi. L'agent n'écrit jamais qu'il « réfléchit », « ressent » ou
« mémorise » ; il ne joue pas un rôle. Le savoir se voit dans ses **choix** : `cerveau.py chercher` affiche aussi le
savoir lié au propos, et l'intention d'un Reel cite les affirmations qui la fondent (« ouverture sans visage pendant
1,2 s, A-0007 probable : … »). Le récap dit en une ou deux lignes ce qui a été appris, d'où ça vient et ce que ça change,
ou « rien de neuf qui change la pratique » quand c'est le cas.

**Ce que Zak dépose** (`data/connaissances/` : études, PDF, liens, vidéos YouTube, méthodes, notes) passe par la même
intégration, avec `"origine": "zak"` : lu en entier, relié, jamais pris pour vérité absolue (son avis sur sa propre
pratique, lui, va dans `principes.md` comme retour de Zak).

## 9. Honnêteté (toujours)
- « Mesuré » = chiffre ou fichier cité ; « supposé » = tout le reste, et c'est écrit.
- Jamais de succès annoncé sur les vues ; l'objectif est la conversation qualifiée.
- Pas de conclusion forte sous 5 Reels comparables (8 posts par groupe pour les comparaisons de brooze-kit).
- Une règle contredite par les faits est retirée, même si elle venait de l'agent.
