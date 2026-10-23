"""Règle P-033 (pratique) : un mouvement de caméra (choc, tremblé, poussée, recadrage) ne découvre jamais un bord vide.
Défaut vu à l'entraînement « mot qui tombe avec poids » (22/10, essai 2 en fabrication) : un choc de 11 px décalait
l'image sans papier hors champ → bande noire en haut du cadre pendant 5 images (et une mesure de courbe.py faussée).
Le contrôle cherche une bande quasi noire et uniforme sur un bord, PASSAGÈRE (absente de la plupart des images) :
un fond noir voulu, une scène sombre ou un letterbox constant ne sont pas signalés. Corrigé le 23/10 : la bande doit
trancher avec l'intérieur sur ≥ 80 % de la longueur du bord (sinon un objet clair près du bord d'une scène sombre
déclenchait une fausse alerte)."""
import subprocess, json
import numpy as np


def bandes(video, w=270):
    info = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                                      '-of', 'json', video], capture_output=True, text=True).stdout)['streams'][0]
    h = int(round(info['height'] * w / info['width'] / 2) * 2); n, d = map(int, info['r_frame_rate'].split('/')); fps = n / d
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
    res = []
    while True:
        b = p.stdout.read(w * h)
        if len(b) < w * h: break
        im = np.frombuffer(b, np.uint8).reshape(h, w).astype(np.float32)
        # (bande du bord, image juste à l'intérieur) : un bord découvert est noir, uniforme, et tranche avec l'intérieur
        bords = {'haut': (im[:2], im[4:10]), 'bas': (im[-2:], im[-10:-4]), 'gauche': (im[:, :2], im[:, 4:10]), 'droite': (im[:, -2:], im[:, -10:-4])}
        # un vrai bord découvert est sombre sur PRESQUE TOUTE la longueur du bord (≥ 80 % des lignes) ; une carte claire
        # qui passe près du bord d'une scène sombre ne l'est que sur une partie (fausse alerte vue sur Spotify, 23/10)
        def decouvert(v, dedans):
            axe = 0 if v.shape[0] <= 2 else 1
            ecart = dedans.mean(axis=axe) - v.mean(axis=axe)
            return bool(v.mean() < 12 and v.std() < 6 and (ecart > 25).mean() > .8)
        res.append({k: decouvert(v, dedans) for k, (v, dedans) in bords.items()})
    p.wait()
    return res, fps


def verifier(video, reel, mots, dossier):
    res, fps = bandes(video)
    if not res: return []
    pb = []
    for bord in ('haut', 'bas', 'gauche', 'droite'):
        drap = np.array([r[bord] for r in res])
        if drap.mean() > .5: continue          # bord noir la plupart du temps : choix de cadre, pas un accident
        i = 0
        while i < len(drap):
            if drap[i]:
                j = i
                while j + 1 < len(drap) and drap[j + 1]: j += 1
                pb.append(f"bord {bord} vide (noir) de {i / fps:.2f} s à {(j + 1) / fps:.2f} s : prolonger l'image hors champ (miroir, marge)")
                i = j + 1
            else: i += 1
    return pb[:5]


if __name__ == '__main__':
    import sys
    print('\n'.join(verifier(sys.argv[1], None, None, None)) or 'OK : aucun bord découvert')
