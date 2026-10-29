# Verdict, tentative 5 : **À REPRENDRE**

## Conditions de la tentative précédente

- V4-3 : **levée** — bbox du visage à la dernière image = bbox à la première (écart <= 2 px, même échelle) ; aucun résidu de tampon ou de bouton sur le visage après 41.0 ; mouvement_fin >= 0,5 (boucle.mouvement_fin) ; plus de 1,2 s sans changement entre 39.3 et 42.4 interdit. · Mesure pleine résolution 1080x1920, masque trait noir (somme RVB<150, y<1400). Image 0 (0.00 s) : x 209-870 / y 547-1323. Dernière image 1238 (41.27 s) : x 208-870 / y 547-1322. Écarts : gauche -1, droite 0, haut 0, bas -1 px (<= 2 px, levé). Cuivre résiduel (teinte 5-25, S>120, V>120) : 0 px à 40.2, 40.37, 40.5, 41.0, 41.3 (levé). mouvement_fin 2,9 >= 0,5 (controle.json engagement.boucle ; diff 41.23=0,76) (levé). Plus long run de diff < 0,5 entre 39.3 et la fin : 37.67-38.70 est avant 39.3 et dure 1,03 s ; après 39.3, diff minimum 0,028 à 40.3 (1 seule image), pas de gel > 1,2 s (levé). Raccord dernière image -> image 0 : 662x775 -> 661x776 puis contraction douce de 661 à 640 en 8 images (continu).
- V4-4 : **non levée** — bbox du contour du visage à la dernière image = bbox de l'image 0 à +-3 px à 1080 de large (le halo peut subsister s'il est présent aussi à l'image 0, ou absent aux deux) ; pas de coupe sèche de taille entre 40.8 et 41.33 s. · Bbox +-3 px : levée (-1/0/0/-1). Halo absent aux deux bouts : levé. MAIS sous-condition « pas de saut de taille > 3 px entre images consécutives de 40.8 à la fin » : non levée. Largeur/hauteur par image : 40.90 686x805 -> 40.93 694x813 (+8/+8) ; 40.93 -> 40.97 +3/+4 ; 41.00 -> 41.03 -4/-5 ; 41.03 -> 41.07 684x802 (-8/-10) ; 41.07 -> 41.10 675x792 (-9/-10) ; 41.10 -> 41.13 -7/-9. Le visage enfle de 659 à 697 px de large (+5,8 %) de 40.63 à 40.97 puis se dégonfle à 662 à 41.20 : pulsation ample, plus grosse que le seuil, sur 0,5 s. Plus de coupe sèche d'une image, mais 4 images dépassent 3 px (40.93, 41.07, 41.10, 41.13).

## Pourquoi ce n'est pas publiable

### V5-3 · P2 · Boucle : le raccord n'est pas à ±2 px. Dernière image (41.33 s) : contour du visage x 202-876, y 523-1313 ; première image (0 s) : x 209-869, y 548-1322, soit visage ~2-4 % plus grand et ~25 px plus haut au sommet. En plus, la dernière image est dominée par un halo cuivre qui sort du cadre alors que l'image 0 n'a aucun halo et réintroduit la pastille « Regarde » : le saut est lisible. Le visage se redimensionne aussi en coupe sèche à 40.9 s (visible sur la planche 40.5 -> 41.1).
- où : 41.0–41.3 s · source : condition précédente
- preuve : Bbox +-3 px : levée (-1/0/0/-1). Halo absent aux deux bouts : levé. MAIS sous-condition « pas de saut de taille > 3 px entre images consécutives de 40.8 à la fin » : non levée. Largeur/hauteur par image : 40.90 686x805 -> 40.93 694x813 (+8/+8) ; 40.93 -> 40.97 +3/+4 ; 41.00 -> 41.03 -4/-5 ; 41.03 -> 41.07 684x802 (-8/-10) ; 41.07 -> 41.10 675x792 (-9/-10) ; 41.10 -> 41.13 -7/-9. Le visage enfle de 659 à 697 px de large (+5,8 %) de 40.63 à 40.97 puis se dégonfle à 662 à 41.20 : pulsation ample, plus grosse que le seuil, sur 0,5 s. Plus de coupe sèche d'une image, mais 4 images dépassent 3 px (40.93, 41.07, 41.10, 41.13).
- exigé : —
- **condition pour passer** : bbox du contour du visage à la dernière image = bbox de l'image 0 à +-3 px à 1080 de large (le halo peut subsister s'il est présent aussi à l'image 0, ou absent aux deux) ; pas de coupe sèche de taille entre 40.8 et 41.33 s.
- piste : Caler l'échelle finale sur celle de l'image 0 (x 209-869) et faire naître le halo dès 0.0 (ou l'éteindre sur les 6 dernières images) ; remplacer la coupe de 40.9 par un glissé.

## Toutes les conditions à remplir pour la tentative suivante (et rien d'autre ne sera exigé, sauf P1 ou régression)

- [ ] V5-3 : bbox du contour du visage à la dernière image = bbox de l'image 0 à +-3 px à 1080 de large (le halo peut subsister s'il est présent aussi à l'image 0, ou absent aux deux) ; pas de coupe sèche de taille entre 40.8 et 41.33 s.

## Conseils (ne bloquent pas)

- V5-1 : plans trop longs en moyenne → durée moyenne des plans ≤ 3.48 s (couper ou relancer dans les plans longs) (indicatif : moins de 3 références de qualité ≥ 7)
- V5-2 : aucune coupe dans les 3 premières secondes → au moins une coupe ou un changement de plan avant 3 s (indicatif : moins de 3 références de qualité ≥ 7)
- V5-4 : Plateau quasi immobile de 1,03 s (diff d'image < 0,5) pendant « ton audience pour toi » : sous le seuil de 1,2 s, donc conforme ; reste le seul vrai creux de la fin. → Un mouvement visible au moins toutes les 1,0 s entre 36.3 et 39.3, hors clic.
- V5-5 : Poussée de caméra qui rogne l'oreille gauche (V3-5) : non remesuré cette passe, supposé inchangé. → Sur 11.0-18.5 s, aucun pixel sombre du visage/des cartes sur x < 24 ni x > 1056.
- V5-6 : Pastilles de sous-titres dimensionnées au groupe entier ; la pastille « Regarde » est présente à 0.0 et absente à la dernière image : elle « pop » au raccord (jonction.jpg). → Largeur de pastille = largeur du texte, ou entrée en fondu depuis la dernière image.
- V5-7 : Wordmark typographique, pas le fichier officiel (V3-9). → Zak confirme par écrit le wordmark typographique, ou fichier officiel utilisé.
- V5-8 : Fantôme du tampon/bouton puis visage ; non régressé (aucun pixel cuivre mesuré à 40.2, 40.37, 40.5, 41.0, 41.3). → Sans objet
