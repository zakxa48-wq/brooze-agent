# Charte Brooze (secours si le skill brooze-direction n'est pas chargé)

- Voix : « nous » pour l'agence, tutoiement. Court, direct, concret. On démontre au lieu de promettre.
  Jamais : parler d'IA ou d'outils, inventer, dénigrer, fausse urgence, jargon de gourou.
- Positionnement : studio vidéo qui parle d'acquisition. Vidéos à fort impact créées à partir de l'existant
  (images, rushs, angles). Cibles : PME, commerçants, associations.
- Avatars : Karim (38 ans, commerçant qui fait tout, « je publie, ça ne donne rien », pas le temps) ;
  Claire (32 ans, responsable com' de PME ou d'association, doit prouver le retour, peur de faire amateur).
  Léo (23 ans, créatif) partage mais n'achète pas : la forme l'impressionne, le fond parle à Karim ou Claire.
- Couleurs : papier #EDEBE7, carte #F7F6F2, studio #D7D6D3, encre #100E0D, encre-douce #6B675F, gris-ui #8A8780,
  cuivre #C8834A (UN seul élément par image), cuivre-profond #A16A38. ≈ 70 % clair, 25 % encre, 5 % cuivre.
  Interdits : noir pur plat, blanc pur en aplat, couleurs hors charte.
- Typo : Inter 800 (titres, interlettrage −3 à −5 %), Inter 700 (texte), Space Grotesk 700 capitales espacées
  (labels, wordmark). Jamais sous 34 px, 2 tailles max par image, pas d'emoji.
- Zone sûre story : y 220 à 1700.
- Logo : uniquement le vrai fichier (`assets/logo.*`), jamais redessiné, déformé ou recoloré.
- Marques réelles : par défaut, aucune (exemples = marques fictives). Exception unique, décidée par Zak le 23/10 : les **vidéos d'analyse ou de décryptage d'une vraie marque** (ex. « la
  stratégie marketing de Red Bull »). Dans ces vidéos seulement, le nom et le **logo officiel** de la marque analysée
  sont autorisés à l'écran, à titre d'illustration et de citation, aux conditions suivantes :
  - le vrai fichier officiel (déposé par Zak dans `brooze-voix/data/marques/<marque>/`, ou issu de la source officielle
    de la marque, source notée dans `credits.json`), **jamais déformé, recoloré, redessiné ni recréé** (pas de logo
    généré, pas de vectorisation maison) ; sans fichier officiel : le nom seul, en typo Brooze ;
  - rien ne laisse croire à un partenariat, un sponsoring ou une vidéo officielle de la marque : pas de logo en
    signature de fin ni à côté du logo Brooze comme un « × », mention « analyse indépendante » à l'écran ou dans la
    légende dès qu'un doute est possible ;
  - l'identité Brooze reste dominante (charte, typo, fin Brooze) ; le logo de la marque illustre, il ne remplit pas
    l'image et n'apparaît que sur le passage qui en parle ;
  - aucun propos ni chiffre sur la marque qui ne soit pas dans l'audio de Zak ou vérifiable avec une source citée ;
    pas de dénigrement ;
  - une vidéo qui n'est PAS une analyse de marque (exemples, mises en situation, faux posts) garde des **marques
    fictives**, comme avant.
  La vidéo est marquée `"analyse_marque": "<marque>"` dans reel.json et post.json ; le contrôle vérifie ces conditions.
