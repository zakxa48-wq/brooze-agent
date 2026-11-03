# Verdict, tentative 4 : **À REPRENDRE**

## Conditions de la tentative précédente

- V3-4 : **non levée** — Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (contraste ≥ 4,5:1 avec leur fond), n'intersectent la boîte d'aucun autre texte (gros titre, sous-titre, CTA) et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (aucune image à score < 0,6 hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s. · Collision avec les titres et trou 42,7–43,5 s corrigés (mention pleine à 42,7 / 43,0 / 43,5 s), mais la mention est à ≈ 49 % d'opacité (gris ≈ 109/255, contraste ≈ 3,8:1 < 4,5:1) pendant 14,23–15,43 s et 36,23–37,70 s ; grisée et peu lisible à 37,0 s.

## Pourquoi ce n'est pas publiable

### V4-4 · P2 · RÉGRESSION de V2-7 : la pastille « analyse indépendante / aucun lien avec la marque », descendue à y ≈ 95–260 px pour sortir du bord haut, tombe maintenant sous les gros titres : (a) 14,43–15,43 s « Créer du contenu. » est posé PAR-DESSUS les 2 lignes de la mention, qui sont grisées et illisibles ; (b) 36,4–37,7 s « vends une émotion. » idem, mention grisée sur noir et coupée par le titre ; (c) 42,70–43,47 s (0,8 s) la mention a disparu (écran quasi noir, CTA déjà là). Au total 111 images (3,7 s) où la mention obligatoire n'est ni entière ni lisible.
- où : 14.4–43.5 s · source : condition précédente
- preuve : Collision avec les titres et trou 42,7–43,5 s corrigés (mention pleine à 42,7 / 43,0 / 43,5 s), mais la mention est à ≈ 49 % d'opacité (gris ≈ 109/255, contraste ≈ 3,8:1 < 4,5:1) pendant 14,23–15,43 s et 36,23–37,70 s ; grisée et peu lisible à 37,0 s.
- exigé : —
- **condition pour passer** : Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (contraste ≥ 4,5:1 avec leur fond), n'intersectent la boîte d'aucun autre texte (gros titre, sous-titre, CTA) et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (aucune image à score < 0,6 hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s.
- piste : Garder la pastille en calque fixe et déplacer plutôt les gros titres « Créer du contenu. » (14,4) et « vends une émotion. » (36,4) sous y ≈ 330 px, ou les faire entrer plus bas ; garder la mention à opacité 1 pendant les fondus au noir 36–37,7 et 42,7–43,5.

### V4-5 · P2 · V3-4 NON LEVÉE : la mention « analyse indépendante / aucun lien avec la marque » n'est plus recouverte par les titres (ils sont descendus : « Créer du contenu. » y≈680, « vends une émotion. » y≈800+, plus aucune intersection) et ne disparaît plus à 42,7–43,5 s, MAIS elle est volontairement baissée à ≈ 49 % d'opacité pendant deux passages : 14,23–15,43 s (1,2 s, 37 images) et 36,23–37,70 s (1,5 s, 45 images). Texte gris (≈ 109/255 au lieu de ≈ 222), pastille quasi transparente (les cartes et le fond noir se voient à travers). Contraste mesuré ≈ 3,8:1, sous 4,5:1. À 37,0 s elle paraît bien grisée, à peine lisible sur noir.
- où : 14.2–37.7 s · source : évaluation indépendante
- preuve : Script OpenCV (reel_sceptique, images ffmpeg 540x960, correspondance du texte de la mention par différence de gaussiennes, multi-échelle 0,85–1,15, score ≥ 0,6) sur 3,4–46,3 s : mention trouvée à chaque image (score min 0,88 sur 3,4–46,0 ; seules les images 46,07–46,57 sont sous 0,6 = fondu de boucle 46,0–46,4 exempté, plus 46,4–46,57 hors plage). Mesure d'opacité sur les mêmes images : percentile 97 du texte = 211–228 partout sauf 109 sur 14,23–15,43 et 36,23–37,70 (108–109, constant, donc un palier de fondu volontaire) ; fond médian 9–10 ; contraste (L1+0,05)/(L2+0,05) = 3,8–3,9 sur ces deux plages contre 11–15 ailleurs (89 images sous 4,5, dont 46,1–46,3 en fondu de boucle). Images regardées (PNG) à 14,4 / 14,9 / 15,5 : texte gris sur pastille translucide, à 15,5 plein ; 36,4 / 36,9 / 37,0 / 37,6 : texte gris sur noir ; 42,7 / 43,0 / 43,5 : mention pleine et lisible (trou levé).
- exigé : —
- **condition pour passer** : Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (texte ≥ 200/255 sur fond ≤ 40/255, contraste ≥ 4,5:1), n'intersectent la boîte d'aucun autre texte et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (percentile 97 du texte ≥ 200 et contraste ≥ 4,5 à toutes les images 3,4–46,0 s, score ≥ 0,6 partout hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s.
- piste : Supprimer le palier d'opacité réduite sous les titres (la mention reste à opacité 1 pendant 14,23–15,43 et 36,23–37,70 ; les titres ne la touchent déjà plus) ; garder la pastille opaque (fond ≥ 85 %) pour que les cartes ne passent pas derrière le texte.

## Toutes les conditions à remplir pour la tentative suivante (et rien d'autre ne sera exigé, sauf P1 ou régression)

- [ ] V4-4 : Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (contraste ≥ 4,5:1 avec leur fond), n'intersectent la boîte d'aucun autre texte (gros titre, sous-titre, CTA) et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (aucune image à score < 0,6 hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s.
- [ ] V4-5 : Sur 3,4–46,3 s, à chaque image (1/30 s), les 2 lignes de la mention sont à pleine opacité (texte ≥ 200/255 sur fond ≤ 40/255, contraste ≥ 4,5:1), n'intersectent la boîte d'aucun autre texte et ne disparaissent jamais plus de 0,1 s ; vérifiable par le même script (percentile 97 du texte ≥ 200 et contraste ≥ 4,5 à toutes les images 3,4–46,0 s, score ≥ 0,6 partout hors fondu de boucle 46,0–46,4) et en regardant 14,4–15,5 et 36,4–37,7 s.

## Conseils (ne bloquent pas)

- V4-1 : plans trop longs en moyenne → durée moyenne des plans ≤ 3.48 s (couper ou relancer dans les plans longs) (indicatif : moins de 3 références de qualité ≥ 7)
- V4-2 : aucune coupe dans les 3 premières secondes → au moins une coupe ou un changement de plan avant 3 s (indicatif : moins de 3 références de qualité ≥ 7)
- V4-3 : trop de mots à l écran à la fois → au plus 4.65 mots par image en moyenne (indicatif : moins de 3 références de qualité ≥ 7)
- V4-6 : Boucle : double exposition canette 2D + canette 3D et double mention (2 lignes fantôme + ligne unique) ≈ 0,4 s. Toujours présent. → Conseil : fondu de boucle sans doublon de texte, ou raccord sec.
- V4-7 : Écran presque noir et vide 35,6–37,0 s entre « un produit » et « vends une émotion » ; la mention grisée y est la chose la plus visible. Mou, mais c'est la respiration avant la phrase-clé, tenue par la voix. → Conseil : un mouvement net toutes les 1,2 s.
- V4-8 : Fond gris quasi vide, petite canette coupée en bas, ≈ 1 s sur « En réalité, ». → Conseil : un sujet ≥ 1/4 de l'écran dès 5,0 s.
- V4-9 : Pouls : même cadre, même courbe blanche, 4,5 s ; seul le tracé bat. Tient grâce à la voix et aux sous-titres ; énergie sonore basse 38–43 s (engagement.png). → Conseil : un changement de cadrage ou d'échelle vers 40,3 s.
- V4-10 : Raccord de style : la canette 3D photoréaliste devient une canette 2D plate à 3,4 s et en CTA 43,5–46 s ; la 3D revient à 46,1 s. → Conseil : fondu enchaîné lent ou 3D conservée.
- V4-11 : Mention de début en ligne unique, grise et très petite (≈ 28 px) ; premier cadre sombre avec « Red » seul. → Conseil : mention plus contrastée.
- V4-12 : Détails template : pastille translucide laissant voir les bords de cartes derrière le texte (7,45 / 12,5 / 13,7 / 32,8 / 34,0 s) ; pictogrammes de cartes répétés ×3 dans le mur ; « MÉDIAS » traversé par des tiges blanches (7,4–9,2 s) légèrement brouillon ; sous-titres à y ≈ 79 % dans la zone d'interface Instagram. → Conseil.
