# Sceptique, passe 4 : L'effet Koulechov

Mesures sur reel.mp4 (1240 images, 1080x1920, extraites avec ffmpeg, lues avec opencv, masque trait noir somme RVB < 150, y < 1400).

## Conditions précédentes
| id | statut | mesure |
|---|---|---|
| V3-3 | non levée | image 0 : x 209-870 / y 547-1323 (661x777). Image 1239 (41.30 s) : x 193-886 / y 528-1341 (694x814). Écart -16 / +16 / -19 / +18 px (+5 %), tolérance 2 px. Résidu tampon/bouton après 41.0 : levé. mouvement_fin 2,54 : levé. Gel > 1,2 s : levé (diff min 0,18 à 39.67). |
| V3-4 | non levée | écart 16-19 px par bord pour ±3. Halo absent aux deux bouts (levé). Plus de saut d'une image à la fin (41.27 -> 41.30 : 1 px), mais gonflement +5 % en 5 images de 40.87 à 41.03 (206 -> 192 en x gauche), puis maintien à cette taille. |

C'est une régression de la correction : en tentative 3 le visage final avait la même échelle que l'image 0 (+3/+4 px de décalage), en tentative 4 il est 5 % plus grand.

## Ce qu'un hater dirait
« La vidéo boucle mal : à la fin le visage grossit et à la relance il rapetisse et un cartouche "Regarde" apparaît. » (jonction.jpg le montre : visage de droite plus large et plus haut, sans pastille.)

## ORDRE DE CORRECTION (unique)
P2 · Raccord de boucle, 40.87-41.33 s
- Faire : supprimer le gonflement final (ou le ramener à l'échelle de l'image 0) : le visage de la dernière image doit mesurer x 209-870 / y 547-1323, avec la même pulsation que l'image 0.
- Valider : bbox masque noir de l'image 1239 = bbox de l'image 0 à ±2 px (pas ±3, cible V3-3), pas d'écart de bbox > 3 px entre images consécutives de 40.8 à 41.33, halo absent aux deux bouts.

## Passe ennui (conseils, ne bloquent pas)
- 36.4-39.4 s : deux plateaux presque plats sur engagement.png pendant « Abonne-toi » (déjà V3-7).
- 40.0-40.37 s : tampon effacé, fond quasi vide 0,37 s, puis coupe sèche vers le visage (diff 16,6 à 40.37).
- Sous-titre « Regarde » présent à 0.0, absent à la dernière image (pop au raccord).
- Wordmark non officiel : confirmation de Zak à obtenir.
- Poussée de caméra 11-18 s et blocs timeline 32.8-34.2 coupés par les bords : non remesurés, supposés inchangés.
