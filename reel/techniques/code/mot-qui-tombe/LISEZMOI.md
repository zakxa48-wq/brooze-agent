# Mot qui tombe avec du poids (typo cinétique, hook) — LIRE, TOMBER, FRAPPER

Validé par le coach le 22/10/2026 (séance « mot qui tombe avec poids », **essai 4, note 8/10**), après le retour de
Zak sur l'essai 3 (« manque d'impact et de vitesse, dézoom réparti sans rôle »). Code = celui de l'essai validé, sans
retouche : `python3 rendu.py <dossier>` → `essai.mp4` (1080×1920, 30 i/s, 3,0 s, son synthétisé).
La version de l'essai 3 (7/10, une ligne, dézoom de 9 % étalé sur 0,5 s) est remplacée : elle n'avait pas d'impact.

## Le geste : trois temps, un rôle chacun
1. **LIRE (0 → 0,317 s)** : mot entier, net, immobile, en hauteur (échelle 1,26, ombre loin et pâle). De 0,18 s à
   0,317 s il remonte de 1,5 % (anticipation, smoothstep), rien d'autre.
2. **TOMBER (0,317 → 0,517 s, 6 images)** : chute en t³ de 1,28 à 1,0 ; flou d'échelle + traînée verticale forte.
3. **FRAPPER** : contact au milieu de l'obturateur de l'image 16 (elle porte la fin de la traînée, c'est là que le
   coup se sent), image 17 posée et secouée ; choc 12 px ; ombre qui claque ; grave marqué. Puis tenue vivante.

## Réglages exacts
| Élément | Réglage |
|---|---|
| mot | Inter 800 (opsz 32), 218 px, interlettrage −3,5 %, encre #141210, point #B87333 ; 161 px de haut par ligne |
| mise en page | **deux lignes centrées, coupées au trait d'union (« Montre- / le. »), interligne 0,92** — voir « À juger » |
| temps | `T_CONTACT = 15,5/30` ; anticipation à `T_CONTACT − 0,337` ; chute à `T_CONTACT − 0,2` ; `PUISSANCE = 3` |
| échelle | lecture 1,26 ; anticipation +1,5 % (1,28) ; dérive 34 px proportionnelle à la hauteur |
| flou | 16 sous-images pendant la chute seulement, obturateur 270° traînant + traînée verticale ∝ vitesse² (55 px au contact) |
| ombre | lumière haut-gauche ; suit la RACINE de la hauteur (diffuse jusqu'au bout) : 18 %, (+70, +150 px), flou 36 px → au contact 40 %, (+4, +6 px), flou 2,5 px |
| choc | 12 px : montée 12 ms (sinus) puis `12·(1 + u/τ)·e^(−u/τ)`, τ = 35 ms ; caméra intégrée sur l'obturateur (8 sous-images) pendant 0,1 s |
| tenue | poussée caméra 1,8 % en smoothstep de 0,77 s à la fin, centrée sur le barycentre de l'encre |
| papier | #EDEBE7, fibres fixes faibles, vignettage −10, grain ±2,6 renouvelé à chaque image ; prolongé hors champ (miroir 64 px) |
| son | air de pièce −56 dBFS ; `air(0,26)` coupé net ; à 16,5/30 s : `choc_granit(1)` + `low_hit(1,0, 40 Hz)` + `tampon(0,5)` + `papier(0,5)` ; **limiteur de crête transparent −10 dB** (anticipation 2 ms, retour 60 ms) puis crête −1,6 dBFS → −14,2 LUFS |

## Mesures de l'essai validé (`reel/courbe.py`)
durée du geste 0,10 s · pic 50,9 px/image · arrêt 0,70 s · tenue 2,27 s · dépassement 0,5 % · 0 oscillation ·
non linéaire · flou 0,77 · son −0,5 image · crête −1,4 dBFS · grave < 120 Hz +3,4 dB par rapport à l'essai 3.

## À juger selon le mot (réserve du coach, soumise à Zak)
- **La coupure sur deux lignes** vient d'un calcul : pour être lu ENTIER à ~1,3×, le texte doit faire ≤ 830 px de
  large posé ; « Montre-le. » sur une ligne à ≥ 150 px de haut en fait 1 003. Sur deux lignes, « le. » est un peu
  orphelin. Pour un autre mot : s'il tient sur une ligne à ≤ 830 px, une ligne ; sinon couper à un endroit naturel
  (trait d'union, entre deux mots) en évitant une ligne très courte, ou réduire l'échelle de lecture (≥ 1,2).
- Le limiteur rend l'impact fort (−14,2 LUFS sur 3 s) : à écouter sur téléphone, et à doser sous une voix.

## Coût
~1 min de rendu pour 3 s (Python + Pillow, 4 cœurs).
