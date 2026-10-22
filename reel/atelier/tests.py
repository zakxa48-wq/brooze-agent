"""Tests de l'Atelier (à lancer après CHAQUE modification de l'outil) : python3 reel/atelier/tests.py [--complet]
Rapide : chaque démo se rend, l'image n'est pas vide, le rendu est déterministe (même t → mêmes pixels).
--complet : rend la démo mot_qui_tombe en vidéo et vérifie le geste avec courbe.py (non-régression des gestes)."""
import sys, os, json, subprocess, runpy
import numpy as np
ICI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(ICI))
import atelier
ok = True
def verif(cond, msg):
    global ok; ok &= bool(cond); print(('OK   ' if cond else 'ÉCHEC') + ' ' + msg)
for demo in sorted(f for f in os.listdir(os.path.join(ICI, 'demos')) if f.endswith('.py')):
    p = os.path.join(ICI, 'demos', demo); cwd = os.getcwd(); os.chdir(os.path.dirname(p))
    try: comp = runpy.run_path(p)['comp']; comp.dossier = os.path.dirname(p); comp.cache = os.path.join(comp.dossier, '_atelier_cache')
    finally: os.chdir(cwd)
    for t in (0., comp.duree / 2, comp.duree - 1 / comp.ips):
        a = comp.image_8bits(t); b = comp.image_8bits(t)
        verif(a.shape == (comp.taille[1], comp.taille[0], 3), f'{demo} t={t:.2f} : format')
        verif(np.array_equal(a, b), f'{demo} t={t:.2f} : déterministe')
        verif(a.std() > 2, f'{demo} t={t:.2f} : image non vide')
if '--complet' in sys.argv:
    v = os.path.join(ICI, 'demos', 'mot_qui_tombe.mp4')
    subprocess.run([sys.executable, ICI, os.path.join(ICI, 'demos', 'mot_qui_tombe.py'), '--sortie', v], check=True, capture_output=True)
    c = json.loads(subprocess.run([sys.executable, os.path.join(os.path.dirname(ICI), 'courbe.py'), v], capture_output=True, text=True).stdout)
    verif(c['duree_geste_s'] <= .2, f"geste lire-tomber-frapper : durée {c['duree_geste_s']} s ≤ 0,2")
    verif(c['arret_s'] <= 1.2 and c['tenue_s'] >= 1.5, f"arrêt {c['arret_s']} s, tenue {c['tenue_s']} s")
    verif(c['ecart_son_image_images'] is not None and abs(c['ecart_son_image_images']) <= 1, f"son à {c['ecart_son_image_images']} image du contact")
    verif(not c['lineaire'] and c['oscillations'] <= 1, 'mouvement non linéaire, sans rebond')
print('TOUT VA BIEN' if ok else 'DES TESTS ÉCHOUENT : ne pas utiliser cette version dans un Reel')
sys.exit(0 if ok else 1)
