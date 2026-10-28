# Sceptique, passe 2 (reel.mp4, 41,4 s)

Méthode : images extraites dans /tmp/eval2 (0, 3, 5, 7.5, 9, 12, 16, 19.5, 20.2, 22.4, 22.9, 24.6, 26, 29.3, 30.5, 33.2-34, 37, 39.5, 40.5, 41.3), diff d'image à 6 i/s, RMS audio par 50 ms.

## Ce qui est réellement corrigé
- Plus aucune alerte glitch ; relances max 1,8 s ; plus de plateau 18.8-28.0 : un événement net à 22.3-22.4 (énergie 26) sur « Koulechov ».
- Phrase 32-33 s : groupes « tu… » / « Le montage, » séparés, plus de fusion. Graisse 900 retirée du tampon, étiquette « piste 1 » à 40 px.

## Ce qu'un hater dirait encore
1. « Le mot Koulechov est caché derrière le sous-titre » (22.4-24.8) : preuve frame 22.9, régression P2.
2. « La boucle saute » : halo plein cadre à 41.33, rien à 0.0 ; visage 25 px plus haut (bbox 523 vs 548) ; coupe de taille à 40.9. P2.
3. « Il dit la phrase à moitié » : « dans lequel tu… » puis 0,45 s de silence puis « Le montage ». Source tronquée : acceptable, à signaler à Zak (P3).
4. « C'est un faux logo » : tampon typographique cadré, pas le fichier ; dépend de Zak.
5. Détails P3 : grille au-dessus de la zone sûre (y 105), visages qui dépassent leurs cartes, rebond de luminance 33.5, fin figée.

## Ennui
Zones les plus lentes (diff d'image < 3) : 21.2-22.2 s (grille qui ne fait que dériver, 1 s), 23.0-23.5, 24.2-24.6, 35.0-35.7 (timeline en croisière) et surtout 36.5-39.2 s : tampon + bouton quasi immobiles (diff 0,06-0,14, jusqu'à 1,4 s d'affilée) pendant l'appel à l'action. Le milieu (grille, 19-26 s) est répétitif : le même visage 6 fois sans changement d'émotion, par construction du propos. Aucun trou > 1,8 s côté relances, donc pas de bloquant, mais la fin s'essouffle. Le ton d'ensemble est propre, un peu « template » (cartes qui glissent), mais cohérent avec le storyboard 2D de Zak.

## Écarts de contexte
- Voix tronquée : acceptable (limite de la source), pas bloquante.
- 41,4 s : acceptable (voix entière).
- Logo typographique : bloquant tant que Zak n'a pas validé ou fourni le fichier ; la 2D est conforme au storyboard (acceptable).
