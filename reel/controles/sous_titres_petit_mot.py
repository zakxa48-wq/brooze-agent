"""Règle P-001 (texte = voix, lisible) : un groupe de sous-titres ne finit jamais sur un petit mot (« Cet | appareil »).
Défaut vu sur le Reel Apple v2 (22/10) et corrigé dans comprendre.py ; contrôle ajouté pour qu'il ne revienne pas."""
import re
PETITS = set('le la les l un une des du de d au aux ce cet cette ces mon ma mes ton ta tes son sa ses notre votre nos vos leur leurs '
             'je tu il elle on nous vous ils elles ne n qui que qu et ou à en y se s pour par sur avec dans très plus'.split())


def verifier(video, reel, mots, dossier):
    pb = []
    for k in range(len(mots) - 1):
        w, n = mots[k], mots[k + 1]
        if w.get('g') == n.get('g') or re.search(r'[.?!,;:…»"]$', w['w']): continue
        if re.sub(r"[^\w']", '', w['w'].lower()).split("'")[0] in PETITS:
            pb.append(f"« {w['w']} | {n['w']} » à {w['start']:.1f} s")
    return pb[:5]
