# Sceptique, passe 3 : Red Bull = un média (reel.mp4, 46,8 s)

Verdict : **À REPRENDRE (1 régression P2)**. V2-1 et V2-5 levées, V2-7 levée sur la géométrie mais sa correction crée une collision.

## Conditions précédentes
| # | Statut | Preuve |
|---|---|---|
| V2-1 | levée | controle.json (15:20, après le rendu 15:09) : problemes = [], « glitchs : aucune alerte » ; _glitchs/rapport.json alertes = [] ; images rapides 12,47 / 24,5 / 32,7 = entrées de cartes |
| V2-5 | levée | 10 images distinctes entre 12 et 36 s ; plus longue image identique 21,6–24,3 s = 2,7 s (corrélation 10 i/s) ; mur 2,0 s (29,6–31,6) puis 2,5 s (33–35,5) ; dépenser 15,5–18,4 (pièces), ne pas vendre 21,5–24,4 (canette barrée), vendre 24,4–29 (frisson, dépassement), produit dérivé 32,5 (canette + étiquette) |
| V2-7 | levée (géométrie) | script reel_sceptique/suivi_pastille.py sur 1296 images 3,3–46,5 s : 1185 trouvées, pastille la plus haute y = 94 px (7,40 ; 8,47 ; 29,40 s), plus aucune coupée (27 images avant). 111 images non trouvées, regardées : voir défaut |

## Défaut recevable
- **P2, 14,43–15,43 ; 36,4–37,7 ; 42,70–43,47 s (régression de V2-7)** : la pastille, descendue à y ≈ 95–260 px, est recouverte par les gros titres « Créer du contenu. » et « vends une émotion. » (mention grisée, illisible), et disparaît 0,8 s à 42,7–43,47 s. 111 images, 3,7 s. Condition : à chaque image la mention est à pleine opacité, sans intersection avec un autre texte, sans trou > 0,1 s (même script). Piste : titres plus bas (y ≥ 330) ou mention fixe à opacité 1.

## Conseils (P3, ne bloquent pas)
Double exposition de boucle 46,0–46,4 (canette 2D+3D, double mention) ; presque noir 35,6–37,0 ; vide gris 4,8–5,8 ; pouls fixe 4,5 s (38–42,5) ; saut de style 3D→2D de la canette à 3,4 s et en CTA ; mention 0–3,4 s petite et grise, image 1 noire ; détails (pastille translucide sur cartes, pictos ×3, papier vignetté, sous-titres en zone IG).

## Ennui (planches 0,5 s sur tout le Reel, 0,1 s corrélation sur 11–37 s ; pas vu en temps réel)
Rythme nettement meilleur qu'en passe 2 : 12–36 s plus aucune chute, relances ≤ 2,5 s. Reste mou : 4,8–5,8, 35,6–37,0 (noir voulu), 38–42,5 (pouls). Ce qui retient : hook 3D 0–3,4, MÉDIAS 7,4–9,2, pièces 15,5–18,4, canette barrée 21,5–24,4, pouls.

## Autres constats
- 3D 0–3,4 s : canette propre, sans scintillement ; titre « boissons énergisantes » lisible, ne touche pas la mention.
- Synchro sous-titres/voix : mots.json et affichage concordent (« Red » 0,0 ; « En réalité » 4,8 ; « Abonne-toi » ≈ 43,5) à ≤ 0,2 s.
- Charte : nom Red Bull seulement en sous-titre, aucun logo ; mention présente (sauf trous ci-dessus) ; durée 46,7 s justifiée (45 s de voix continue).
- Boucle : fin canette 3D sur noir, début noir : acceptable hors double exposition.
