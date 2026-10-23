"""charte.md § Marques réelles (décision de Zak du 23/10) : un vrai logo n'est permis que dans une vidéo d'analyse de
cette marque, posé tel quel, jamais en fin de vidéo, avec une mention d'indépendance si le doute est possible.
Vérifie ce qui se vérifie dans reel.json ; le reste (logo non retouché, aucun air officiel) se juge sur la planche."""
import os, re


def verifier(video, reel, mots, dossier):
    pb = []
    marque = reel.get('analyse_marque')
    logos = [s for s in reel.get('scenes', []) if re.search(r'marques?/|logo', str(s.get('image', '')) + str(s.get('video', '')), re.I)
             and 'brooze' not in str(s.get('image', '')).lower()]
    if logos and not marque:
        pb.append('logo de marque réelle sans "analyse_marque" : interdit hors vidéo d\'analyse (exemples = marques fictives)')
    if marque:
        for s in logos:
            im = str(s.get('image', ''))
            if not re.search(r'marques?/', im): pb.append(f'logo {im} hors de data/marques/ : fichier officiel non prouvé')
            if any(k in s for k in ('etalonnage', 'teinte', 'calques')) or s.get('echelle_x') or s.get('echelle_y'):
                pb.append(f'logo {im} retouché (étalonnage, teinte, calques ou échelle non uniforme) : à poser tel quel')
        if reel.get('scenes') and logos and reel['scenes'][-1] in logos:
            pb.append('logo de la marque en fin de vidéo : ressemble à une signature officielle')
        cap = str(reel.get('legende', '')) + str(reel.get('caption', ''))
        if 'indépendant' not in cap.lower() and not reel.get('mention_independante_a_l_ecran'):
            pb.append('« analyse indépendante » absente de la légende et de l\'écran : l\'ajouter (ou noter mention_independante_a_l_ecran)')
    return pb
