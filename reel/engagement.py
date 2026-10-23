"""Engagement et boucle d'un Reel (MONTAGE.md § 8, objectif de Zak du 23/10) : mesuré image par image.

Usage : python3 reel/engagement.py sorties/<id>/reel.mp4 [sorties/<id>/reel.json]   (aussi appelé par controle.py)
Écrit engagement.json, engagement.png (énergie de mouvement, zones mortes, relances) et jonction.jpg (la dernière
seconde suivie de la première : la boucle doit être invisible) dans le dossier de la vidéo.

Mesures (énergie = différence moyenne entre images voisines, floutées pour ignorer le grain, échelle 0–255) :
  - ouverture      : il se passe quelque chose dès l'image 1 (pas d'image noire, pas de fondu depuis le noir, mouvement
                     ou coupe dans la première demi-seconde)                                           → BLOQUANT
  - zones mortes   : plus de 2 s sous le seuil de mouvement (0,35)                                    → BLOQUANT
  - relances       : changement visuel significatif (coupe, ou image très différente de celle d'il y a 0,5 s) ;
                     un écart de plus de 3 s entre deux relances                                       → à justifier
  - cadence        : 3 plans de suite de même durée (± 20 %) sur plus de 5 s                           → à justifier
  - boucle         : raccord dernière → première image (couleur et image), mouvement des deux côtés, son qui ne
                     s'éteint pas à la fin ; carton de fin (scène `fin`) qui casse la boucle          → BLOQUANT
  - durée          : au-delà de 30 s                                                                   → à justifier
  - lecture        : chaque gros texte reste au moins 0,25 s par mot + 0,4 s, au plus 2,5 × ce temps + 1 s
  - revisionnage   : 1 ou 2 clins d'œil déclarés dans reel.json (`clins_d_oeil`)                      → à justifier
"""
import sys, os, json, subprocess, tempfile
import numpy as np, cv2

ICI = os.path.dirname(os.path.abspath(__file__))
SEUIL_MORT, ZONE_MORTE_S, SEUIL_RELANCE, ECART_RELANCE_S = .35, 2.0, 4.0, 3.0


def images(video, ips=10, w=180):
    info = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                      '-of', 'json', video], capture_output=True, text=True).stdout)['streams'][0]
    h = int(round(info['height'] * w / info['width'] / 2) * 2)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'fps={ips},scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3)


def son_bords(video):
    t = tempfile.mktemp(suffix='.wav')
    if subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vn', '-ac', '1', '-ar', '48000', t], capture_output=True).returncode: return None
    import soundfile as sf
    x, sr = sf.read(t); os.remove(t)
    if len(x) < sr: return None
    db = lambda s: float(20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9))
    return dict(debut_db=round(db(x[:int(.3 * sr)]), 1), fin_db=round(db(x[-int(.3 * sr):]), 1),
                fin_derniers_80ms_db=round(db(x[-int(.08 * sr):]), 1), moyenne_db=round(db(x), 1))


def analyser(video, reel=None, mots=None, dossier=None, ips=10):
    dossier = dossier or os.path.dirname(os.path.abspath(video))
    fr = images(video, ips)
    g = np.array([cv2.GaussianBlur(cv2.cvtColor(x, cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 2) for x in fr])
    n = len(g); duree = n / ips
    e = np.r_[0, np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))]
    lisse = np.convolve(e, np.ones(5) / 5, mode='same')                       # énergie lissée sur 0,5 s
    k = int(.5 * ips); chg = np.r_[[0] * k, [np.abs(g[i] - g[i - k]).mean() for i in range(k, n)]]
    coupes = [i for i in range(1, n) if e[i] > max(6., 5 * np.median(e[max(0, i - 5):i + 6]))]
    bloquants, a_justifier = [], []

    # 1. ouverture
    luma0 = float(fr[0].mean()); luma = fr[:int(.6 * ips)].mean(axis=(1, 2, 3))
    fondu_noir = luma0 < 14 or (luma[-1] > luma0 * 2.2 and luma0 < 40)
    vivant = lisse[1:int(.5 * ips) + 1].max() > .6 or any(c <= .5 * ips for c in coupes)
    ouverture = dict(luma_image_1=round(luma0, 1), fondu_depuis_noir=bool(fondu_noir), mouvement_premiere_demi_seconde=bool(vivant))
    if fondu_noir: bloquants.append('ouverture : image 1 noire ou fondu depuis le noir')
    if not vivant: bloquants.append('ouverture : rien ne bouge dans la première demi-seconde')

    # 2. zones mortes et relances
    mortes, i = [], 0
    while i < n:
        if lisse[i] < SEUIL_MORT:
            j = i
            while j + 1 < n and lisse[j + 1] < SEUIL_MORT: j += 1
            if (j - i + 1) / ips > ZONE_MORTE_S: mortes.append([round(i / ips, 1), round((j + 1) / ips, 1)])
            i = j + 1
        else: i += 1
    for a, b in mortes: bloquants.append(f'zone morte de {b - a:.1f} s ({a:.1f}–{b:.1f} s) : ajouter une relance (cadrage, échelle, couleur, mouvement, couche)')
    rel = sorted(set([c / ips for c in coupes] + [i / ips for i in range(k, n) if chg[i] > SEUIL_RELANCE and chg[i] >= chg[max(0, i - 3):i + 4].max()]))
    fusion = []
    for t in rel:
        if not fusion or t - fusion[-1] > .4: fusion.append(round(t, 2))
    bornes = [0.] + fusion + [duree]
    ecarts = [(round(a, 1), round(b, 1)) for a, b in zip(bornes, bornes[1:]) if b - a > ECART_RELANCE_S]
    for a, b in ecarts: a_justifier.append(f'pas de relance pendant {b - a:.1f} s ({a}–{b} s) : viser une relance toutes les 1,5 à 3 s')

    # 3. cadence (plans de même durée trop longtemps)
    pl = np.diff([0.] + [c / ips for c in coupes] + [duree])
    for s in range(len(pl) - 2):
        bloc = pl[s:s + 3]
        if bloc.max() <= bloc.min() * 1.2 and bloc.sum() > 5:
            debut = float(sum(pl[:s])); a_justifier.append(f'cadence monotone {debut:.1f}–{debut + bloc.sum():.1f} s (3 plans de ~{bloc.mean():.1f} s) : alterner courts et respirations'); break

    # 4. boucle
    d_img = float(np.abs(g[-1] - g[0]).mean())
    h0 = cv2.calcHist([cv2.cvtColor(fr[0], cv2.COLOR_RGB2HSV)], [0, 1], None, [16, 8], [0, 180, 0, 256])
    h1 = cv2.calcHist([cv2.cvtColor(fr[-1], cv2.COLOR_RGB2HSV)], [0, 1], None, [16, 8], [0, 180, 0, 256])
    d_coul = float(cv2.compareHist(cv2.normalize(h0, h0), cv2.normalize(h1, h1), cv2.HISTCMP_BHATTACHARYYA))
    mouv_fin, mouv_debut = float(lisse[-int(.5 * ips):].mean()), float(lisse[1:int(.5 * ips) + 1].mean())
    s = son_bords(video)
    boucle = dict(ecart_image=round(d_img, 1), ecart_couleur=round(d_coul, 2), mouvement_fin=round(mouv_fin, 2), mouvement_debut=round(mouv_debut, 2), son=s)
    if reel and reel.get('scenes') and reel['scenes'][-1].get('type') == 'fin':
        bloquants.append('boucle : carton de fin (scène « fin ») : il casse la boucle → CTA avant la fin ou en surimpression, dernière image raccord avec la première')
    if d_coul > .45: a_justifier.append(f'boucle : couleurs de la dernière et de la première image trop différentes ({d_coul:.2f})')
    if mouv_fin < SEUIL_MORT: a_justifier.append('boucle : la fin est immobile, la reprise se verra (garder le mouvement jusqu\'à la dernière image)')
    if s and s['fin_derniers_80ms_db'] < s['moyenne_db'] - 18: a_justifier.append('boucle : le son s\'éteint à la fin (fondu) → le prolonger dans le début (reel.json "boucle": true)')

    # 5. durée, lecture, revisionnage
    if duree > 30.5: a_justifier.append(f'durée {duree:.1f} s : la plus courte possible pour l\'idée (souvent 15–30 s), couper ce qui ne sert pas')
    lecture = []
    if reel and mots:
        t0 = (reel.get('source') or [0])[0]
        def tps(x):
            if isinstance(x, str) and x.startswith('@'):
                m = mots[int(x[1:].rstrip('>'))]; return (m['end'] if x.endswith('>') else m['start'] - .12) - t0
            return x
        sc = reel['scenes']; deb = [tps(x['de']) for x in sc] + [duree]
        for kk, x in enumerate(sc):
            if not x.get('mots'): continue
            a, b = x['mots'] if isinstance(x['mots'], list) else (x['mots'], x['mots'])
            nb = b - a + 1; besoin = .25 * nb + .4; dur = deb[kk + 1] - deb[kk]
            lecture.append(dict(t=round(deb[kk], 1), mots=nb, affiche_s=round(dur, 2), besoin_s=round(besoin, 2)))
            if dur < besoin: a_justifier.append(f'lecture : texte de {nb} mots à {deb[kk]:.1f} s affiché {dur:.2f} s (il faut {besoin:.2f} s)')
            elif dur > besoin * 2.5 + 1 and not x.get('video'): a_justifier.append(f'lecture : texte à {deb[kk]:.1f} s tenu {dur:.1f} s pour {nb} mots (trop long, il s\'use)')
    if reel is not None and not reel.get('clins_d_oeil'):
        a_justifier.append('revisionnage : aucun clin d\'œil déclaré (reel.json "clins_d_oeil": [{"t": …, "quoi": …}]), en glisser 1 ou 2 liés au propos')

    res = dict(duree_s=round(duree, 2), ouverture=ouverture, zones_mortes=mortes, relances=fusion,
               ecart_max_relances_s=round(max(np.diff(bornes)), 2), coupes_s=[round(c / ips, 2) for c in coupes], boucle=boucle,
               lecture=lecture, bloquants=bloquants, a_justifier=a_justifier)
    # graphique et jonction (à regarder)
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        t = np.arange(n) / ips; fig, ax = plt.subplots(figsize=(10, 2.6))
        ax.plot(t, lisse, color='#C8834A', lw=1.3); ax.axhline(SEUIL_MORT, color='k', ls=':', lw=.8)
        for a, b in mortes: ax.axvspan(a, b, color='red', alpha=.2)
        for r in fusion: ax.axvline(r, color='#100E0D', lw=.5, alpha=.5)
        ax.set_yscale('symlog', linthresh=1); ax.set_xlabel('s'); ax.set_ylabel('énergie'); ax.set_xlim(0, duree)
        fig.tight_layout(); fig.savefig(os.path.join(dossier, 'engagement.png'), dpi=110); plt.close(fig)
    except Exception: pass
    idx = list(range(max(0, n - ips), n)) + list(range(0, min(n, ips)))
    tuiles = [cv2.resize(fr[i], (135, 240)) for i in idx[::2]]
    cv2.imwrite(os.path.join(dossier, 'jonction.jpg'), cv2.cvtColor(np.hstack(tuiles), cv2.COLOR_RGB2BGR))
    json.dump(res, open(os.path.join(dossier, 'engagement.json'), 'w'), ensure_ascii=False, indent=1)
    return res


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    reel = json.load(open(a[1])) if len(a) > 1 else None
    mots = json.load(open(os.path.join(os.path.dirname(a[1]), reel.get('mots', 'mots.json')))) if reel else None
    r = analyser(a[0], reel, mots)
    print(json.dumps({k: r[k] for k in ('duree_s', 'zones_mortes', 'ecart_max_relances_s', 'boucle', 'bloquants', 'a_justifier')}, ensure_ascii=False, indent=1))
    sys.exit(1 if r['bloquants'] else 0)
