# Mot qui tombe avec du poids (typo cinétique, hook)

Validé par le coach le 22/10/2026 (séance « mot qui tombe avec poids », essai 3, note 7/10). Code = celui de l'essai
validé, sans retouche : `python3 rendu.py <dossier>` → `essai.mp4` (1080×1920, 30 i/s, 3,0 s, son synthétisé).

## Le geste
Le mot tombe VERS le papier (axe de profondeur), pas le long de l'écran : échelle 1,093 → 1,0 avec une chute en t³
(`h = 1 − (s/0,557)³`, déjà engagée à 0 s), 34 px de dérive verticale. Contact à 0,507 s, placé ENTRE deux
obturateurs pour que l'image 16 soit la première image posée et nette. Puis rien ne rebondit.

## Réglages exacts
| Élément | Réglage |
|---|---|
| mot | Inter 800 (opsz 32), 218 px, interlettrage −3,5 %, encre #141210, point #B87333 ; 152 px de haut mesurés |
| flou | 16 sous-images, obturateur 270° traînant (flou d'échelle) + traînée verticale ∝ vitesse (26 px au contact) |
| ombre | lumière haut-gauche ; en haut : décalée (+70, +150 px), flou 36 px, 20 % ; au contact : (+4, +6 px), flou 2,5 px, 38 % |
| choc | caméra 11 px vers le bas, plein à l'image du contact, retour critique `11·(1 + u/τ)·e^(−u/τ)`, τ = 35 ms |
| tenue | poussée caméra 1,8 % en smoothstep de 0,76 s à la fin, centrée sur le barycentre de l'encre (mot fixe sur le papier) |
| papier | #EDEBE7, fibres fixes faibles, vignettage −10, grain capteur ±2,6 renouvelé à chaque image ; prolongé hors champ (miroir 64 px) |
| son | air de pièce −56 dBFS dès 0 s ; `air` coupé net ; `choc_granit` + `low_hit(44 Hz)` + `papier` à 16,5/30 s ; crête −1,6 dBFS |

## Mesures de l'essai validé (`reel/courbe.py`)
arrêt 0,667 s · tenue 2,3 s · dépassement 1,1 % · 0 oscillation · non linéaire · flou 0,73 · son −0,5 image · 152 px.

## Limites connues
- Un mot de ≥ 150 px de haut fait ~1 000 px de large : il ne peut pas partir de beaucoup plus que 1,1× s'il doit être
  entier dès 0,3 s avec une chute qui accélère. La profondeur repose alors surtout sur l'ombre. Piste du coach :
  mot plus court, ou caméra qui recule pendant la chute.
- Coût : ~1 min de rendu pour 3 s (Python, 4 cœurs).
