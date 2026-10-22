"""Mesure le MOUVEMENT d'un élément animé dans une courte vidéo (exercice de motion design) : utilisé par le coach
pour valider un essai sur des chiffres, pas seulement à l'œil.

Usage : python3 reel/courbe.py essai.mp4 [--fond auto|#rrggbb] [--graphique courbe.png]
Mesure, image par image, l'élément qui se distingue du fond (masque de contraste) :
  - position (centre), taille (hauteur de la boîte), vitesse en px/image (à l'échelle 1080×1920)
  - arret_s        : instant où l'élément s'immobilise pour de bon (vitesse < 1 px/image jusqu'à la fin)
  - impact_s       : instant où la vitesse retombe sous 20 % de son pic (fin du geste principal)
  - duree_geste_s  : durée du geste principal (vitesse au-dessus de 20 % du pic) : court = vif, long = mou
  - depassement    : dépassement de la position finale le long de l'axe du mouvement, en % de la course
  - oscillations   : nombre d'inversions de sens visibles (> 2 px) après l'impact (rebond)
  - lineaire       : vrai si la vitesse est quasi constante pendant le mouvement (mouvement mécanique)
  - flou_pendant   : rapport netteté directionnelle pendant la phase rapide / à l'arrêt (< 0,8 = flou de mouvement)
  - tenue_s        : durée de l'élément immobile et lisible avant la fin
  - son_attaque_s  : attaque sonore la plus forte ; ecart_son_image_images = (attaque − impact) en images
"""
import sys, json, subprocess
import numpy as np


def images(f, w=540):
    info = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                                      '-of', 'json', f], capture_output=True, text=True).stdout)['streams'][0]
    W, H = info['width'], info['height']; n, d = map(int, info['r_frame_rate'].split('/')); fps = n / d
    h = int(round(H * w / W / 2) * 2)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3).astype(np.float32), fps, W / w


def attaque(f):
    import soundfile as sf, tempfile, os
    t = tempfile.mktemp(suffix='.wav')
    if subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vn', '-ac', '1', '-ar', '48000', t], capture_output=True).returncode or not os.path.exists(t): return None
    x, sr = sf.read(t); os.remove(t)
    if len(x) == 0 or np.abs(x).max() < 1e-4: return None
    pas = int(sr * .005); e = np.array([np.sqrt((x[i:i + pas] ** 2).mean() + 1e-12) for i in range(0, len(x) - pas, pas)])
    db = 20 * np.log10(e + 1e-9); flux = np.diff(db, prepend=db[0])
    return round(float(np.argmax(flux) * .005), 3)


def main(f, fond='auto', graphique=None):
    fr, fps, k = images(f)
    if fond == 'auto':
        bord = np.concatenate([fr[-1][:4].reshape(-1, 3), fr[-1][-4:].reshape(-1, 3), fr[-1][:, :4].reshape(-1, 3), fr[-1][:, -4:].reshape(-1, 3)])
        bg = np.median(bord, axis=0)
    else:
        bg = np.array([int(fond[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
    pos, taille, net = [], [], []
    for im in fr:
        c = np.abs(im - bg).sum(axis=2)
        m = c > 90
        ys, xs = np.nonzero(m)
        if len(xs) < 20: pos.append((np.nan, np.nan)); taille.append(np.nan); net.append(np.nan); continue
        # centre PONDÉRÉ par le contraste (sous-pixel) : un masque binaire fait sauter le centre d'une colonne entière
        # quand un bord de lettre franchit un pixel (faux mouvement sur une poussée de caméra lente)
        wgt = np.clip(c - 40, 0, 200); sw = wgt.sum()
        gy, gx = np.mgrid[0:c.shape[0], 0:c.shape[1]]
        pos.append(((wgt * gx).sum() / sw * k, (wgt * gy).sum() / sw * k))
        prof = wgt.sum(axis=1); cum = np.cumsum(prof) / prof.sum()
        ix = np.arange(len(cum)); taille.append((np.interp(.98, cum, ix) - np.interp(.02, cum, ix)) * k)   # sous-pixel aussi
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        g = im[y0:y1, x0:x1].mean(axis=2)
        net.append(min(np.abs(np.diff(g, axis=1)).mean(), np.abs(np.diff(g, axis=0)).mean()) if g.shape[0] > 2 and g.shape[1] > 2 else np.nan)
    P = np.array(pos); T = np.array(taille); N = np.array(net)
    v = np.r_[0, np.hypot(*np.diff(P, axis=0).T)]; v = np.nan_to_num(v)
    vt = np.r_[0, np.abs(np.diff(T))]; vt = np.nan_to_num(vt); vit = np.maximum(v, vt)        # translation ou échelle
    n = len(fr); pic = int(np.argmax(vit))
    arret = n - 1
    for i in range(n - 1, -1, -1):
        if vit[i] >= 1.0: arret = min(n - 1, i + 1); break
    else: arret = 0
    impact = next((i for i in range(pic, n) if vit[i] < .2 * vit[pic]), arret)
    debut_geste = next((i for i in range(pic, -1, -1) if vit[i] < .2 * vit[pic]), 0)   # le geste = vitesse > 20 % du pic
    fin = P[-1]; depart = P[np.argmax(~np.isnan(P[:, 0]))]
    axe = fin - depart; course = float(np.hypot(*axe))
    if course > 5:
        u = axe / course; proj = (P - depart) @ u
        depassement = max(0., float(np.nanmax(proj[pic:]) - course)) / course * 100
        d = np.diff(proj[impact:]); d = d[np.abs(d) > 2]
    else:
        tl = T[-1]; course = float(np.nanmax(np.abs(T - tl))) or 1.
        depassement = max(0., float(np.nanmax(T[pic:]) - tl)) / max(1., abs(tl - np.nanmin(T))) * 100 if tl > np.nanmin(T) else 0.
        d = np.diff(T[impact:]); d = d[np.abs(d) > 2]
    oscillations = int(np.sum(np.diff(np.sign(d)) != 0)) if len(d) > 1 else 0
    mouv = vit[1:arret + 1]; mouv = mouv[mouv > 1]
    lineaire = bool(len(mouv) >= 4 and np.std(mouv) / (np.mean(mouv) + 1e-6) < .15)
    rapide = vit > .5 * vit[pic] if vit[pic] > 0 else np.zeros(n, bool)
    flou = float(np.nanmean(N[rapide]) / np.nanmean(N[arret:])) if rapide.any() and arret < n else None
    att = attaque(f)
    res = dict(images=n, ips=round(fps, 2), duree_s=round(n / fps, 2), pic_vitesse_px=round(float(vit[pic]), 1), pic_s=round(pic / fps, 3),
               impact_s=round(impact / fps, 3), duree_geste_s=round((impact - debut_geste) / fps, 3), arret_s=round(arret / fps, 3), tenue_s=round((n - 1 - arret) / fps, 2),
               course_px=round(course, 1), depassement_pct=round(depassement, 1), oscillations=oscillations, lineaire=lineaire,
               flou_pendant=round(flou, 2) if flou is not None else None, taille_finale_px=round(float(T[-1]), 0) if not np.isnan(T[-1]) else None,
               son_attaque_s=att, ecart_son_image_images=round((att - impact / fps) * fps, 1) if att is not None else None)
    if graphique:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        t = np.arange(n) / fps
        fig, ax = plt.subplots(2, 1, figsize=(7, 4.5), sharex=True)
        ax[0].plot(t, vit, color='#B87333'); ax[0].set_ylabel('vitesse (px/image)'); ax[0].axvline(impact / fps, ls='--', c='k', lw=.8)
        if att is not None: ax[0].axvline(att, ls=':', c='r', lw=1)
        ax[1].plot(t, P[:, 0], label='x'); ax[1].plot(t, P[:, 1], label='y'); ax[1].plot(t, T, label='taille'); ax[1].legend(); ax[1].set_xlabel('s')
        fig.tight_layout(); fig.savefig(graphique, dpi=110)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    main(a[0], a[a.index('--fond') + 1] if '--fond' in a else 'auto', a[a.index('--graphique') + 1] if '--graphique' in a else None)
