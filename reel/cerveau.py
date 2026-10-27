"""Cerveau de l'agent Brooze : une MÉMOIRE structurée qui grandit avec les données de Zak (pas un entraînement du modèle).

Les données vivent dans le dépôt PRIVÉ brooze-voix (R = /home/user/brooze-voix), jamais ici :
  R/data/references/  R/data/mes-videos/  R/data/retours/  R/data/docs/  R/data/connaissances/   ce que Zak dépose
  R/data/cerveau/     fiches.jsonl (une fiche par fichier analysé), principes.md, pratique.jsonl, progression.md,
                      index.json, images/ (planches à REGARDER), textes/ (transcriptions, textes extraits), entrainement/

Commandes (python3 reel/cerveau.py <commande> R …) :
  nouveaux   R                         fichiers déposés pas encore analysés (empreinte sha1)
  analyser   R <fichier>               vidéo ou image → fiche avec mesures + planche d'images clés (à regarder)
             [--categorie mes-videos|references|…] [--id ID]   (sinon déduite du dossier)
  texte      R <fichier>               retour ou document (audio, txt, md, pdf, image) → texte brut + fiche à compléter
  completer  R <id> [--resume …] [--efficace …] [--a-eviter …] [--tags a,b] [--qualite 1-10] [--regles …]
  chercher   R "<propos>" [--n 5]      fiches et principes les plus utiles pour un Reel (recherche texte + mesures)
  index      R                         reconstruit index.json (automatique après analyser / texte / completer)
  comparer   R <reel.mp4> [--n 5]      mesure un Reel et le compare aux meilleures fiches (rythme, lisibilité, finition)
  pratique   R '<json>'                ajoute un débrief à pratique.jsonl (voir CERVEAU.md pour les champs)
  recurrents R                         défauts revenus au moins 2 fois dans pratique.jsonl (→ règle + contrôle auto)
  progression R                        recalcule le tableau de bord hebdomadaire progression.md
Mesures vidéo : coupes (détection de plans), durée des plans, rythme des 3 premières secondes, mouvements de caméra
(flux optique), transitions (coupe, fondu, noir), palette, texte à l'écran (OCR : part du temps, taille, position,
animation), énergie du son, synchro coupes/son, transcription du hook (Whisper local), netteté et niveau sonore.
"""
import sys, os, json, re, hashlib, subprocess, math, datetime, glob, tempfile, shutil
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
CATEGORIES = ['references', 'mes-videos', 'retours', 'docs', 'connaissances']
EXT_VIDEO = ('.mp4', '.mov', '.m4v', '.webm', '.mkv', '.avi')
EXT_IMAGE = ('.jpg', '.jpeg', '.png', '.webp', '.heic')
EXT_AUDIO = ('.m4a', '.mp3', '.wav', '.aac', '.ogg', '.opus', '.flac')
EXT_TEXTE = ('.txt', '.md', '.pdf', '.csv')
LARGEUR = 180                       # analyse du mouvement et des coupes en basse définition (rapide, suffisant)


# ---------------------------------------------------------------- mémoire (fichiers)
def C(R): d = os.path.join(R, 'data', 'cerveau'); os.makedirs(os.path.join(d, 'images'), exist_ok=True); os.makedirs(os.path.join(d, 'textes'), exist_ok=True); return d
def sha1(f):
    h = hashlib.sha1()
    with open(f, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''): h.update(b)
    return h.hexdigest()[:12]
def fiches(R):
    p = os.path.join(C(R), 'fiches.jsonl')
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []
def ecrire_fiches(R, fs):
    with open(os.path.join(C(R), 'fiches.jsonl'), 'w') as f:
        for x in fs: f.write(json.dumps(x, ensure_ascii=False) + '\n')
def ranger(R, fiche):
    fs = [x for x in fiches(R) if x['id'] != fiche['id']] + [fiche]; ecrire_fiches(R, fs); construire_index(R); return fiche
def categorie_de(R, f):
    rel = os.path.relpath(os.path.abspath(f), os.path.join(R, 'data'))
    return rel.split(os.sep)[0] if rel.split(os.sep)[0] in CATEGORIES else 'hors-base'
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:40]


def cmd_nouveaux(R):
    vus = {x.get('sha1') for x in fiches(R)}; n = 0
    for cat in CATEGORIES:
        for f in sorted(glob.glob(os.path.join(R, 'data', cat, '**', '*'), recursive=True)):
            b = os.path.basename(f)
            if os.path.isdir(f) or b.upper().startswith('LISEZMOI') or b.startswith('.'): continue
            # un .txt posé à côté d'une vidéo/image du même nom est sa note, pas un fichier à part
            base = os.path.splitext(f)[0]
            if f.endswith('.txt') and any(os.path.exists(base + e) for e in EXT_VIDEO + EXT_IMAGE + EXT_AUDIO): continue
            if sha1(f) in vus: continue
            ext = os.path.splitext(f)[1].lower()
            action = 'analyser' if ext in EXT_VIDEO + EXT_IMAGE and cat != 'retours' else 'texte'
            print(f'{action:9} {os.path.relpath(f, R)}'); n += 1
    if not n: print('rien de nouveau')


# ---------------------------------------------------------------- outils de mesure
def sonde(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', f], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def images_basses(f, fps, w=LARGEUR):
    """Toutes les images à `fps`, en basse définition RGB (n, h, w, 3)."""
    info = sonde(f); v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    W, H = int(v['width']), int(v['height'])
    rot = 0
    for sd in v.get('side_data_list', []) or []:
        if 'rotation' in sd: rot = abs(int(sd['rotation']))
    if rot in (90, 270): W, H = H, W
    h = int(round(H * w / W / 2) * 2)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'fps={fps},scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.uint8)
    return x.reshape(-1, h, w, 3), (W, H)


def image_pleine(f, t, dest):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', f, '-frames:v', '1', '-q:v', '3', dest], check=True)
    return dest


def coupes(fr, fps):
    """Coupes franches (pic isolé de différence d'histogramme) et transitions progressives (fondus, passages au noir)."""
    import cv2
    hs = []
    for im in fr:
        hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
        h = cv2.calcHist([hsv], [0, 1, 2], None, [12, 6, 6], [0, 180, 0, 256, 0, 256]); hs.append(cv2.normalize(h, h).flatten())
    d = np.array([0.] + [cv2.compareHist(hs[i - 1], hs[i], cv2.HISTCMP_BHATTACHARYYA) for i in range(1, len(hs))])
    px = np.array([0.] + [np.abs(fr[i].astype(np.int16) - fr[i - 1]).mean() / 255 for i in range(1, len(fr))])
    score = .65 * d + .35 * px * 2.5
    seuil = max(.32, np.median(score) * 5)
    cuts, trans = [], []
    for i in range(1, len(score)):
        voisins = np.r_[score[max(0, i - 3):i], score[i + 1:i + 4]]
        v = voisins.max() if len(voisins) else 0
        # pic franc, ou pic plus faible mais très isolé (même décor sous un autre cadrage)
        if (score[i] > seuil and score[i] > 2.2 * v) or (score[i] > max(.08, np.median(score) * 4) and score[i] > 4 * v):
            cuts.append(round(i / fps, 3))
    # progressif : fenêtre de 0,3–1,2 s où la somme des petites différences dépasse le seuil sans pic franc
    luma = fr.mean(axis=(1, 2, 3))
    i = 1
    while i < len(score):
        if score[i] > seuil * .25 and not any(abs(i / fps - c) < .15 for c in cuts):
            j = i
            while j + 1 < len(score) and score[j + 1] > seuil * .25 and (j + 1 - i) < 1.2 * fps: j += 1
            if (j - i + 1) >= .3 * fps and score[i:j + 1].sum() > seuil * 1.4:
                noir = luma[i:j + 1].min() < 14
                # filé (whip) : l'image du milieu est floue dans une seule direction
                rx, ry = [], []
                for k in range(max(0, i - 1), j + 1):
                    m = fr[k].astype(np.float32).mean(axis=2)
                    gx, gy = np.abs(np.diff(m, axis=1)).mean() + 1e-6, np.abs(np.diff(m, axis=0)).mean() + 1e-6
                    rx.append(gx / gy); ry.append(gy / gx)
                typ = 'noir' if noir else 'filé horizontal' if min(rx) < .72 else 'filé vertical' if min(ry) < .72 else 'fondu'
                trans.append(dict(t=round(i / fps, 2), d=round((j - i + 1) / fps, 2), type=typ))
                i = j
        i += 1
    return cuts, trans, score


def mouvement(fr, fps, bornes):
    """Mouvement de caméra par plan (flux optique Farneback) : panoramique, zoom, épaule (tremblement), fixe."""
    import cv2
    g = [cv2.cvtColor(im, cv2.COLOR_RGB2GRAY) for im in fr]; H, W = g[0].shape
    ys, xs = np.mgrid[0:H, 0:W]; cx, cy = xs - W / 2, ys - H / 2; rr = np.sqrt(cx ** 2 + cy ** 2) + 1e-6
    res = []
    for a, b in bornes:
        i0, i1 = int(a * fps) + 1, min(len(g) - 1, int(b * fps) - 1)
        if i1 - i0 < 2: res.append(dict(type='trop court')); continue
        pas = max(1, (i1 - i0) // 12); tx, ty, zo = [], [], []
        for i in range(i0, i1, pas):
            fl = cv2.calcOpticalFlowFarneback(g[i], g[min(i + 1, i1)], None, .5, 3, 13, 3, 5, 1.1, 0)
            tx.append(fl[..., 0].mean() * fps / W); ty.append(fl[..., 1].mean() * fps / H)
            zo.append(((fl[..., 0] * cx + fl[..., 1] * cy) / rr).mean() * fps / (W / 2))
        tx, ty, zo = map(np.array, (tx, ty, zo))
        pan, zoom = math.hypot(tx.mean(), ty.mean()), zo.mean()
        tremble = float(np.std(tx) + np.std(ty))
        if abs(zoom) > .04: t = 'zoom avant' if zoom > 0 else 'zoom arrière'
        elif pan > .06: t = 'panoramique ' + ('horizontal' if abs(tx.mean()) > abs(ty.mean()) else 'vertical')
        elif tremble > .05: t = 'épaule'
        elif pan > .015 or abs(zoom) > .012: t = 'dérive lente'
        else: t = 'quasi fixe'
        res.append(dict(type=t, pan=round(pan, 3), zoom=round(float(zoom), 3), tremble=round(tremble, 3)))
    return res


def palette(fr, k=5):
    import cv2
    px = fr[::max(1, len(fr) // 40)].reshape(-1, 3).astype(np.float32)
    px = px[np.random.default_rng(0).choice(len(px), min(len(px), 40000), replace=False)]
    _, lab, cen = cv2.kmeans(px, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.), 3, cv2.KMEANS_PP_CENTERS)
    parts = np.bincount(lab.flatten(), minlength=k) / len(lab)
    o = np.argsort(-parts)
    hsv = cv2.cvtColor(fr[::max(1, len(fr) // 40)].reshape(-1, 1, 3), cv2.COLOR_RGB2HSV).reshape(-1, 3)
    r, b = fr[..., 0].mean(), fr[..., 2].mean()
    return dict(couleurs=[dict(hex='#%02x%02x%02x' % tuple(int(c) for c in cen[i]), part=round(float(parts[i]), 2)) for i in o],
                luminosite=round(float(hsv[:, 2].mean() / 255), 2), saturation=round(float(hsv[:, 1].mean() / 255), 2),
                temperature='chaude' if r > b * 1.08 else 'froide' if b > r * 1.08 else 'neutre')


def ocr(img):
    """Mots détectés (tesseract fra+eng) avec boîtes, sur une image pleine définition."""
    r = subprocess.run(['tesseract', img, '-', '-l', 'fra+eng', '--psm', '11', 'tsv'], capture_output=True, text=True)
    mots = []
    for l in r.stdout.splitlines()[1:]:
        c = l.split('\t')
        if len(c) < 12 or not c[11].strip(): continue
        try: conf = float(c[10])
        except ValueError: continue
        w = c[11].strip()
        if conf < 70 or len(re.sub(r'\W', '', w)) < 2: continue
        mots.append(dict(w=w, x=int(c[6]), y=int(c[7]), l=int(c[8]), h=int(c[9])))
    return mots


def nettete(img):
    import cv2
    g = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    return float(cv2.Laplacian(g, cv2.CV_64F).var()) if g is not None else 0.


def son(f, cuts, duree):
    """Niveau (LUFS), énergie dans le temps, attaques, et part des coupes posées sur une attaque du son."""
    tmp = tempfile.mktemp(suffix='.wav')
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vn', '-ar', '48000', tmp], capture_output=True)
    if r.returncode or not os.path.exists(tmp): return dict(present=False)
    import soundfile as sf, pyloudnorm as pyln
    xs, sr = sf.read(tmp); os.remove(tmp)
    lufs = pyln.Meter(sr).integrated_loudness(xs)            # canaux d'origine : même mesure que controle.py
    x = xs.mean(axis=1) if xs.ndim > 1 else xs
    if len(x) < sr * .5 or np.abs(x).max() < 1e-4: return dict(present=False)
    pas = int(sr * .05); e = np.array([np.sqrt((x[i:i + pas] ** 2).mean() + 1e-12) for i in range(0, len(x) - pas, pas)])
    db = 20 * np.log10(e + 1e-9)
    flux = np.maximum(0, np.diff(db, prepend=db[0])); seuil = np.percentile(flux, 92)
    att = [i * .05 for i in range(1, len(flux) - 1) if flux[i] > max(seuil, 4) and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]]
    # une coupe est « sur la voix » si une attaque du son tombe entre 0,05 s avant et 0,2 s après : l'image peut
    # légitimement précéder le mot de 2 à 6 images (règle de montage), jamais le suivre de beaucoup
    proche = lambda c: any(-.05 <= a - c <= .2 for a in att)
    sync = sum(map(proche, cuts)) / len(cuts) if cuts else None
    hasard = min(1., len(att) * .25 / max(duree, .1))          # part attendue si les coupes tombaient au hasard
    t3 = db[:int(3 / .05)]
    return dict(present=True, lufs=round(float(lufs), 1), crete_db=round(float(20 * np.log10(np.abs(x).max())), 1),
                energie_3s_db=round(float(t3.mean()), 1) if len(t3) else None, energie_moy_db=round(float(db.mean()), 1),
                dynamique_db=round(float(np.percentile(db, 95) - np.percentile(db, 20)), 1), attaques_par_s=round(len(att) / duree, 2),
                coupes_sur_attaque=round(sync, 2) if sync is not None else None, coupes_sur_attaque_si_hasard=round(hasard, 2))


def hook(f, secondes=6.):
    """Transcription locale des premières secondes (Whisper ONNX, medium si présent)."""
    tmp = tempfile.mktemp(suffix='.wav')
    r = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-t', str(secondes), '-vn', '-ac', '1', '-ar', '48000', tmp], capture_output=True)
    if r.returncode or not os.path.exists(tmp): return ''
    try:
        sys.path.insert(0, ICI); import soundfile as sf, comprendre
        x, _ = sf.read(tmp)
        if np.abs(x).max() < 1e-3: return ''
        return comprendre.transcrire(x, [[0, len(x) / 48000]])[0][2]
    except Exception as e:
        return f'(transcription impossible : {e})'
    finally:
        os.path.exists(tmp) and os.remove(tmp)


def planche(images, legendes, dest, colonnes=6, largeur=240):
    from PIL import Image, ImageDraw
    ims = [Image.open(i).convert('RGB') for i in images]
    ims = [im.resize((largeur, int(im.height * largeur / im.width))) for im in ims]
    h = max(im.height for im in ims) + 24; lignes = math.ceil(len(ims) / colonnes)
    P = Image.new('RGB', (colonnes * (largeur + 6) + 6, lignes * (h + 6) + 6), (24, 22, 20)); d = ImageDraw.Draw(P)
    from PIL import ImageFont
    try: police = ImageFont.truetype(os.path.expanduser('~/.cache/brooze/polices/Inter.ttf'), 13)
    except OSError: police = None
    for k, (im, lg) in enumerate(zip(ims, legendes)):
        x, y = 6 + (k % colonnes) * (largeur + 6), 6 + (k // colonnes) * (h + 6)
        P.paste(im, (x, y)); d.text((x + 4, y + im.height + 5), lg, fill=(230, 222, 205), font=police)
    P.save(dest, quality=88)


# ---------------------------------------------------------------- analyse d'une vidéo
def mesurer_video(f, dossier_images, prefixe, hook_aussi=True):
    fps = 10
    fr, (W, H) = images_basses(f, fps)
    duree = len(fr) / fps
    info = sonde(f); v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    cuts, trans, _ = coupes(fr, fps)
    bornes = list(zip([0.] + cuts, cuts + [duree]))
    durees = [b - a for a, b in bornes]
    mv = mouvement(fr, fps, bornes)
    # images clés : début (0 ; 0,5 ; 1 ; 2 ; 3 s) puis milieu de chaque plan (24 au plus), en pleine définition
    tmp = tempfile.mkdtemp()
    ts = [t for t in (0.05, .5, 1., 2., 3.) if t < duree] + [(a + b) / 2 for a, b in bornes]
    if len(ts) > 30: ts = ts[:5] + [ts[5:][int(i)] for i in np.linspace(0, len(ts) - 6, 25)]
    imgs = [image_pleine(f, t, os.path.join(tmp, f'{k:03d}.jpg')) for k, t in enumerate(ts)]
    # texte à l'écran : OCR sur une image par seconde (et les images clés du début)
    ts_txt = sorted(set([round(t, 1) for t in np.arange(.2, duree, 1.)] + [round(t, 2) for t in ts[:5]]))
    lectures = []
    for t in ts_txt:
        im = image_pleine(f, t, os.path.join(tmp, 'ocr.jpg'))
        # sous 24 px (rapporté à 1920 de haut), c'est du texte DANS l'image (étiquette, papier), pas du texte posé
        m = [w for w in ocr(im) if w['h'] * 1920 / H >= 24]
        lectures.append(dict(t=t, mots=m))
    avec = [l for l in lectures if l['mots']]
    hauteurs = [w['h'] * 1920 / H for l in avec for w in l['mots']]
    ys = [(w['y'] + w['h'] / 2) / H for l in avec for w in l['mots']]
    zone = lambda y: 'haut' if y < .33 else 'milieu' if y < .66 else 'bas'
    zones = {z: round(sum(zone(y) == z for y in ys) / len(ys), 2) for z in ('haut', 'milieu', 'bas')} if ys else {}
    changements = sum(1 for a, b in zip(avec, avec[1:]) if {w['w'] for w in a['mots']} != {w['w'] for w in b['mots']})
    nets = [nettete(i) for i in imgs[5:] or imgs]
    s = son(f, cuts, duree)
    mesures = dict(
        duree_s=round(duree, 2), format=f'{W}×{H}', ips=round(eval(v.get('avg_frame_rate', '0/1')) if v.get('avg_frame_rate', '0/0') != '0/0' else 0, 2),
        debit_mbps=round(int(info['format'].get('bit_rate', 0)) / 1e6, 1),
        plans=len(bornes), duree_plan_moy_s=round(float(np.mean(durees)), 2), duree_plan_med_s=round(float(np.median(durees)), 2),
        duree_plan_min_s=round(min(durees), 2), duree_plan_max_s=round(max(durees), 2),
        coupes_3s=sum(c < 3 for c in cuts), premiere_coupe_s=cuts[0] if cuts else None, coupes=cuts,
        transitions=trans, transitions_progressives=len(trans),
        camera={t: sum(m['type'] == t for m in mv) for t in sorted({m['type'] for m in mv})}, camera_par_plan=[m['type'] for m in mv],
        palette=palette(fr),
        texte=dict(part_du_temps=round(len(avec) / max(1, len(lectures)), 2), hauteur_px_med=round(float(np.median(hauteurs)), 0) if hauteurs else None,
                   hauteur_px_min=round(float(np.percentile(hauteurs, 10)), 0) if hauteurs else None,
                   mots_par_image=round(float(np.mean([len(l['mots']) for l in avec])), 1) if avec else 0, zones=zones,
                   changements_par_s=round(changements / duree, 2),
                   premieres_3s=' '.join(w['w'] for l in lectures if l['t'] <= 3 for w in l['mots'])[:200]),
        nettete_med=round(float(np.median(nets)), 0), son=s)
    if hook_aussi: mesures['hook_transcrit'] = hook(f)
    os.makedirs(dossier_images, exist_ok=True)
    pl = os.path.join(dossier_images, f'{prefixe}.jpg')
    planche(imgs, [f'{t:.1f} s' + ('' if k < 5 else f' · {mv[k - 5]["type"]}' if k - 5 < len(mv) else '') for k, t in enumerate(ts)], pl)
    shutil.rmtree(tmp)
    return mesures, pl


def mesurer_image(f, dossier_images, prefixe):
    from PIL import Image
    import cv2
    im = Image.open(f).convert('RGB'); W, H = im.size
    a = np.asarray(im.resize((LARGEUR, int(H * LARGEUR / W))))[None]
    tmp = tempfile.mkdtemp(); j = os.path.join(tmp, 'i.jpg'); im.save(j, quality=95)
    m = ocr(j); g = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY).astype(np.float32)
    sal = np.abs(cv2.Laplacian(cv2.GaussianBlur(g, (0, 0), 3), cv2.CV_32F)); ys, xs = np.mgrid[0:H, 0:W]
    cx, cy = (sal * xs).sum() / sal.sum() / W, (sal * ys).sum() / sal.sum() / H
    os.makedirs(dossier_images, exist_ok=True); pl = os.path.join(dossier_images, f'{prefixe}.jpg'); im.thumbnail((900, 900)); im.save(pl, quality=88)
    shutil.rmtree(tmp)
    return dict(format=f'{W}×{H}', palette=palette(a), nettete=round(nettete(f), 0),
                texte=dict(mots=len(m), hauteur_px_med=round(float(np.median([w['h'] * 1920 / H for w in m])), 0) if m else None, extrait=' '.join(w['w'] for w in m)[:200]),
                centre_interet=dict(x=round(float(cx), 2), y=round(float(cy), 2))), pl


def note_jointe(f):
    t = os.path.splitext(f)[0] + '.txt'
    return open(t, encoding='utf-8', errors='replace').read().strip() if os.path.exists(t) else ''


def cmd_analyser(R, f, categorie=None, iid=None):
    f = os.path.abspath(f); cat = categorie or categorie_de(R, f); h = sha1(f)
    iid = iid or f'{cat}-{slug(os.path.splitext(os.path.basename(f))[0])}-{h[:6]}'
    ext = os.path.splitext(f)[1].lower()
    if ext in EXT_VIDEO: mes, pl = mesurer_video(f, os.path.join(C(R), 'images'), iid); genre = 'video'
    elif ext in EXT_IMAGE: mes, pl = mesurer_image(f, os.path.join(C(R), 'images'), iid); genre = 'image'
    else: sys.exit(f'{f} : ni vidéo ni image (utiliser « texte »)')
    ancienne = next((x for x in fiches(R) if x['id'] == iid), {})
    fiche = dict(id=iid, categorie=cat, genre=genre, fichier=os.path.relpath(f, R) if f.startswith(R) else f, sha1=h,
                 analyse_le=str(datetime.date.today()), note_de_zak=note_jointe(f), mesures=mes,
                 planche=os.path.relpath(pl, R),
                 # rempli par l'agent APRÈS avoir regardé la planche (completer) :
                 resume=ancienne.get('resume', ''), efficace=ancienne.get('efficace', ''), a_eviter=ancienne.get('a_eviter', ''),
                 tags=ancienne.get('tags', []), qualite=ancienne.get('qualite'), a_completer=not ancienne.get('resume'))
    ranger(R, fiche)
    print(json.dumps(fiche, ensure_ascii=False, indent=1))
    print(f'\n→ REGARDE la planche {pl}, puis : cerveau.py completer {R} {iid} --resume … --efficace … --a-eviter … --tags … --qualite N')


def cmd_texte(R, f, iid=None):
    f = os.path.abspath(f); cat = categorie_de(R, f); h = sha1(f); ext = os.path.splitext(f)[1].lower()
    iid = iid or f'{cat}-{slug(os.path.splitext(os.path.basename(f))[0])}-{h[:6]}'
    if ext in EXT_AUDIO or ext in EXT_VIDEO:
        sys.path.insert(0, ICI); import comprendre, soundfile as sf
        d = tempfile.mkdtemp(); comprendre.decoder(f, os.path.join(d, 'a.wav')); x, _ = sf.read(os.path.join(d, 'a.wav'))
        segs = comprendre.segmenter(x); texte = ' '.join(t for _, _, t in comprendre.transcrire(x, segs)); shutil.rmtree(d)
    elif ext == '.pdf':
        texte = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout
    elif ext in EXT_IMAGE:
        texte = subprocess.run(['tesseract', f, '-', '-l', 'fra+eng'], capture_output=True, text=True).stdout
    else:
        texte = open(f, encoding='utf-8', errors='replace').read()
    texte = texte.strip()
    out = os.path.join(C(R), 'textes', f'{iid}.txt'); open(out, 'w').write(texte)
    ancienne = next((x for x in fiches(R) if x['id'] == iid), {})
    fiche = dict(id=iid, categorie=cat, genre='retour' if cat == 'retours' else 'document', fichier=os.path.relpath(f, R), sha1=h,
                 analyse_le=str(datetime.date.today()), texte=os.path.relpath(out, R), extrait=texte[:400],
                 resume=ancienne.get('resume', ''), regles=ancienne.get('regles', []), tags=ancienne.get('tags', []),
                 a_completer=not ancienne.get('resume'))
    ranger(R, fiche)
    print(texte[:6000]); print(f'\n→ texte complet : {out}\n→ puis : cerveau.py completer {R} {iid} --resume … --regles "règle 1|règle 2" --tags …')


def cmd_completer(R, iid, **kw):
    fs = fiches(R); x = next((x for x in fs if x['id'] == iid), None)
    if not x: sys.exit(f'fiche inconnue : {iid}')
    for k, v in kw.items():
        if v is None: continue
        if k == 'tags': v = [t.strip() for t in v.split(',') if t.strip()]
        if k == 'regles': v = [t.strip() for t in v.split('|') if t.strip()]
        if k == 'qualite': v = float(v)
        x[k] = v
    x['a_completer'] = not x.get('resume'); x['complete_le'] = str(datetime.date.today())
    ecrire_fiches(R, fs); construire_index(R); print(f'{iid} complétée')


# ---------------------------------------------------------------- index et recherche
MOTS_VIDES = set('le la les un une des de du d l et ou à au aux en dans sur pour par avec sans ce cet cette ces qui que quoi '
                 'est sont a ont il elle on nous vous ils je tu ne pas plus se sa son ses leur leurs mon ma mes ton ta tes '
                 'the a an of to in and is it for on with'.split())
def jetons(t): return [w for w in re.findall(r"[a-zàâäçéèêëîïôöùûüœ0-9]+", (t or '').lower()) if w not in MOTS_VIDES and len(w) > 2]


def texte_fiche(x):
    m = x.get('mesures', {})
    morceaux = [x.get('resume', ''), x.get('efficace', ''), x.get('a_eviter', ''), ' '.join(x.get('tags', [])), x.get('note_de_zak', ''),
                x.get('extrait', ''), ' '.join(x.get('regles', [])), m.get('hook_transcrit', ''), (m.get('texte') or {}).get('premieres_3s', ''),
                ' '.join((m.get('camera') or {}).keys()), x.get('categorie', '')]
    return ' '.join(morceaux)


def principes(R):
    """Règles de principes.md : blocs « ### P-xxx — titre » suivis de lignes de détail."""
    p = os.path.join(C(R), 'principes.md')
    if not os.path.exists(p): return []
    blocs, cur = [], None
    for l in open(p, encoding='utf-8'):
        if l.startswith('### '): cur = dict(titre=l[4:].strip(), corps=''); blocs.append(cur)
        elif cur is not None and not l.startswith('## '): cur['corps'] += l
        elif l.startswith('## '): cur = None
    return blocs


def construire_index(R):
    docs = [dict(type='fiche', id=x['id'], j=jetons(texte_fiche(x))) for x in fiches(R)]
    docs += [dict(type='principe', id=p['titre'], j=jetons(p['titre'] + ' ' + p['corps'])) for p in principes(R)]
    df = {}
    for d in docs:
        for w in set(d['j']): df[w] = df.get(w, 0) + 1
    idx = dict(n=len(docs), df=df, docs=[dict(type=d['type'], id=d['id'], tf={w: d['j'].count(w) for w in set(d['j'])}, l=len(d['j'])) for d in docs],
               construit_le=datetime.datetime.now().isoformat(timespec='seconds'))
    json.dump(idx, open(os.path.join(C(R), 'index.json'), 'w'), ensure_ascii=False)
    return idx


def cmd_chercher(R, requete, n=5):
    idx = construire_index(R); q = jetons(requete); N = max(1, idx['n'])
    L = np.mean([d['l'] for d in idx['docs']]) if idx['docs'] else 1
    def bm25(d):
        s = 0.
        for w in q:
            if w in d['tf']:
                idf = math.log(1 + (N - idx['df'][w] + .5) / (idx['df'][w] + .5)); tf = d['tf'][w]
                s += idf * tf * 2.2 / (tf + 1.2 * (.25 + .75 * d['l'] / L))
        return s
    fs = {x['id']: x for x in fiches(R)}
    notes = sorted(((bm25(d), d) for d in idx['docs']), key=lambda x: -x[0])
    # bonus : fiches de Zak (mes-videos), bien notées, et retours récents
    def bonus(d):
        x = fs.get(d['id'], {}); b = 0
        if x.get('categorie') == 'mes-videos': b += .6
        if x.get('categorie') == 'retours': b += .8
        if x.get('qualite'): b += (x['qualite'] - 5) * .1
        return b
    fiches_top = sorted([(s + bonus(d), d) for s, d in notes if d['type'] == 'fiche'], key=lambda x: -x[0])[:n]
    princ_top = [(s, d) for s, d in notes if d['type'] == 'principe'][:n]
    print(f'# Pour : « {requete} »\n\n## Fiches')
    for s, d in fiches_top:
        x = fs[d['id']]; m = x.get('mesures', {})
        rythme = f"plans {m.get('duree_plan_moy_s')} s, {m.get('coupes_3s')} coupes < 3 s, texte {(m.get('texte') or {}).get('part_du_temps')}" if m.get('plans') else ''
        print(f"- [{s:.2f}] {x['id']} ({x['categorie']}{', qualité ' + str(x['qualite']) if x.get('qualite') else ''}) {rythme}\n"
              f"    efficace : {x.get('efficace') or '—'}\n    à éviter : {x.get('a_eviter') or '—'}")
    print('\n## Principes liés au propos')
    for s, d in [x for x in princ_top if x[0] > 0]: print(f'- [{s:.2f}] {d["id"]}')
    print('\n## Principes à confiance forte (toujours applicables)')
    for p in principes(R):
        if 'Confiance** : forte' in p['corps']: print(f"- {p['titre']}")
    if not fiches_top: print('(aucune fiche : la base est vide, rien à appliquer)')
    try:   # le savoir (connaissances du monde, reel/savoir.py) répond au même propos
        sys.path.insert(0, ICI); import savoir
        l = savoir.chercher(R, requete)
        print('\n## Savoir (connaissances reliées, savoir.py)'); print('\n'.join(l) if l else '(rien de connu : question à ajouter à savoir/questions.md)')
    except Exception as e: print(f'\n(savoir indisponible : {e})')


# ---------------------------------------------------------------- comparaison aux références (contrôle qualité)
def cmd_comparer(R, video, n=5):
    """Mesure un Reel et le compare aux MEILLEURES fiches vidéo (qualité ≥ 7, ou toutes à défaut) sur trois axes."""
    mes, pl = mesurer_video(video, tempfile.mkdtemp(), 'reel', hook_aussi=False)
    refs = [x for x in fiches(R) if x.get('genre') == 'video' and x.get('categorie') in ('references', 'mes-videos')]
    meilleures = sorted([x for x in refs if (x.get('qualite') or 0) >= 7], key=lambda x: -x['qualite'])[:n] or refs[:n]
    out = dict(reel=mes, planche=pl, references=[x['id'] for x in meilleures], axes={}, verdict='sans référence')
    if not meilleures:
        print(json.dumps(out, ensure_ascii=False, indent=1)); print('Aucune référence vidéo dans la base : comparaison impossible (non bloquant).'); return
    med = lambda k, sub=None: float(np.median([(x['mesures'].get(sub) or {}).get(k) if sub else x['mesures'].get(k) for x in meilleures
                                               if ((x['mesures'].get(sub) or {}).get(k) if sub else x['mesures'].get(k)) is not None] or [np.nan]))
    t = mes['texte']; s = mes.get('son', {})
    axes = {}
    # rythme : durée moyenne des plans et coupes des 3 premières secondes dans la bande des références (± 35 %)
    dp, ref_dp = mes['duree_plan_moy_s'], med('duree_plan_moy_s')
    axes['rythme'] = dict(reel=dict(duree_plan_moy_s=dp, coupes_3s=mes['coupes_3s']), ref=dict(duree_plan_moy_s=ref_dp, coupes_3s=med('coupes_3s')),
                          ok=bool(np.isnan(ref_dp) or dp <= ref_dp * 1.35) and mes['coupes_3s'] >= min(1, med('coupes_3s')))
    # lisibilité : texte assez grand (boîte OCR ≥ 20 px sur 1920 ≈ police ≥ 34 px : un mot sans jambage mesure ~0,55 × la
    # taille de police), pas plus chargé que les références
    h, ref_h = t.get('hauteur_px_min'), med('hauteur_px_min', 'texte')
    mpi, ref_mpi = t.get('mots_par_image') or 0, med('mots_par_image', 'texte')
    axes['lisibilite'] = dict(reel=dict(hauteur_px_min=h, mots_par_image=mpi), ref=dict(hauteur_px_min=ref_h, mots_par_image=ref_mpi),
                              ok=(h is None or h >= 20) and (np.isnan(ref_mpi) or mpi <= max(ref_mpi * 1.5, 4)))
    # finition : netteté, niveau sonore, synchro coupes/son
    nt, ref_nt = mes['nettete_med'], med('nettete_med')
    sync, ref_sync = s.get('coupes_sur_attaque'), med('coupes_sur_attaque', 'son')
    axes['finition'] = dict(reel=dict(nettete=nt, lufs=s.get('lufs'), coupes_sur_attaque=sync), ref=dict(nettete=ref_nt, coupes_sur_attaque=ref_sync),
                            ok=(np.isnan(ref_nt) or nt >= ref_nt * .6) and (s.get('lufs') is None or -16 <= s['lufs'] <= -12)
                            and (sync is None or np.isnan(ref_sync) or sync >= ref_sync - .2))
    # raisons explicites : ce qui est mesuré, ce qui est exigé, et comment passer (lu par reel/verdict.py)
    f = lambda v: None if v is None or (isinstance(v, float) and np.isnan(v)) else round(float(v), 2)
    raisons = []
    if not axes['rythme']['ok']:
        if not np.isnan(ref_dp) and dp > ref_dp * 1.35:
            raisons.append(dict(cle='comparer.rythme.duree_plan', mesure=f(dp), exige=f'≤ {f(ref_dp * 1.35)} s', quoi='plans trop longs en moyenne',
                                condition=f'durée moyenne des plans ≤ {f(ref_dp * 1.35)} s (couper ou relancer dans les plans longs)'))
        if mes['coupes_3s'] < min(1, med('coupes_3s')):
            raisons.append(dict(cle='comparer.rythme.coupes_3s', mesure=mes['coupes_3s'], exige='≥ 1', quoi='aucune coupe dans les 3 premières secondes',
                                condition='au moins une coupe ou un changement de plan avant 3 s'))
    if not axes['lisibilite']['ok']:
        if h is not None and h < 20:
            raisons.append(dict(cle='comparer.lisibilite.hauteur', mesure=h, exige='≥ 20 px (boîte OCR)', quoi='texte trop petit',
                                condition='plus petit texte lisible ≥ 20 px de haut (police ≥ 34 px)'))
        if not np.isnan(ref_mpi) and mpi > max(ref_mpi * 1.5, 4):
            raisons.append(dict(cle='comparer.lisibilite.mots', mesure=f(mpi), exige=f'≤ {f(max(ref_mpi * 1.5, 4))}', quoi='trop de mots à l écran à la fois',
                                condition=f'au plus {f(max(ref_mpi * 1.5, 4))} mots par image en moyenne'))
    if not axes['finition']['ok']:
        if not np.isnan(ref_nt) and nt < ref_nt * .6:
            raisons.append(dict(cle='comparer.finition.nettete', mesure=f(nt), exige=f'≥ {f(ref_nt * .6)}', quoi='image plus floue que les références',
                                condition=f'netteté médiane ≥ {f(ref_nt * .6)} (moins de flou global, textures plus fines)'))
        if s.get('lufs') is not None and not -16 <= s['lufs'] <= -12:
            raisons.append(dict(cle='comparer.finition.lufs', mesure=f(s['lufs']), exige='entre −16 et −12 LUFS', quoi='niveau sonore', condition='volume intégré entre −16 et −12 LUFS'))
        if sync is not None and not np.isnan(ref_sync) and sync < ref_sync - .2:
            raisons.append(dict(cle='comparer.finition.synchro', mesure=f(sync), exige=f'≥ {f(ref_sync - .2)}', quoi='coupes pas assez calées sur les attaques du son',
                                condition=f'part des coupes sur une attaque ≥ {f(ref_sync - .2)}'))
    # une comparaison n'est probante qu'avec assez de bonnes références : sinon elle informe, elle ne bloque pas
    probante = len([x for x in meilleures if (x.get('qualite') or 0) >= 7]) >= 3
    out['axes'] = axes; out['raisons'] = raisons; out['probante'] = probante
    out['verdict'] = 'au niveau' if not raisons else ('EN DESSOUS : boucle de correction' if probante else 'en dessous (indicatif : moins de 3 références de qualité ≥ 7, non bloquant)')
    js = json.dumps(out, ensure_ascii=False, indent=1, default=lambda o: None if isinstance(o, float) and np.isnan(o) else o)
    print(js)
    open(os.path.join(os.path.dirname(os.path.abspath(video)), 'comparer.json'), 'w').write(js)
    for r in raisons: print(f"- {r['quoi']} : mesuré {r['mesure']}, exigé {r['exige']} → {r['condition']}")
    if raisons and probante: sys.exit(1)


# ---------------------------------------------------------------- pratique et progression
def cmd_pratique(R, js):
    x = json.loads(js); x.setdefault('date', str(datetime.date.today()))
    with open(os.path.join(C(R), 'pratique.jsonl'), 'a') as f: f.write(json.dumps(x, ensure_ascii=False) + '\n')
    print('débrief ajouté')


def lire_pratique(R):
    p = os.path.join(C(R), 'pratique.jsonl')
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def cmd_recurrents(R):
    compte = {}
    for x in lire_pratique(R):
        for d in x.get('defauts', []):
            c = d.get('categorie') if isinstance(d, dict) else str(d)
            compte.setdefault(c, []).append(x.get('reel') or x.get('exercice') or x['date'])
    rec = {c: v for c, v in compte.items() if len(v) >= 2}
    if not rec: print('aucun défaut récurrent'); return
    for c, v in sorted(rec.items(), key=lambda x: -len(x[1])):
        print(f'{c} : {len(v)} fois ({", ".join(v)}) → règle dans principes.md + contrôle automatique')


def cmd_progression(R, stats=None):
    semaines = {}
    for x in lire_pratique(R):
        d = datetime.date.fromisoformat(x['date']); k = f'{d.isocalendar()[0]}-S{d.isocalendar()[1]:02d}'
        semaines.setdefault(k, []).append(x)
    techniques = os.path.join(ICI, 'techniques', 'techniques.json')
    nb_tech = len([t for t in json.load(open(techniques)) if t.get('statut') == 'active']) if os.path.exists(techniques) else 0
    lignes = ['# Progression (recalculée par `cerveau.py progression`, une ligne par semaine)', '',
              '| Semaine | Reels | Exercices | Boucles sceptique / Reel | P1 | P2 | Fabrication (min / Reel) | Techniques actives | Résultat Instagram (méd. vues > 3 s, rétention) |',
              '|---|---|---|---|---|---|---|---|---|']
    st = json.load(open(stats)) if stats and os.path.exists(stats) else {}
    for k in sorted(semaines):
        xs = semaines[k]; reels = [x for x in xs if x.get('reel')]; ex = [x for x in xs if x.get('exercice')]
        moy = lambda c: round(float(np.mean([x[c] for x in reels if x.get(c) is not None])), 1) if any(x.get(c) is not None for x in reels) else '—'
        p1 = sum(x.get('p1', 0) for x in reels); p2 = sum(x.get('p2', 0) for x in reels)
        lignes.append(f"| {k} | {len(reels)} | {len(ex)} | {moy('boucles')} | {p1} | {p2} | {moy('minutes')} | {nb_tech} | {st.get(k, '—')} |")
    lignes += ['', 'Lecture : moins de boucles et de défauts P1/P2, moins de minutes, plus de techniques maîtrisées = progrès.',
               'Deux semaines sans progrès → chercher pourquoi (journal) et changer de méthode (CERVEAU.md § Progression).']
    open(os.path.join(C(R), 'progression.md'), 'w').write('\n'.join(lignes) + '\n'); print('\n'.join(lignes))


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    cmd, R = a[0], os.path.abspath(a[1]); r = a[2:]
    def opt(n, d=None):
        return r[r.index(n) + 1] if n in r else d
    if cmd == 'nouveaux': cmd_nouveaux(R)
    elif cmd == 'analyser': cmd_analyser(R, r[0], opt('--categorie'), opt('--id'))
    elif cmd == 'texte': cmd_texte(R, r[0], opt('--id'))
    elif cmd == 'completer':
        cmd_completer(R, r[0], resume=opt('--resume'), efficace=opt('--efficace'), a_eviter=opt('--a-eviter'), tags=opt('--tags'),
                      qualite=opt('--qualite'), regles=opt('--regles'))
    elif cmd == 'chercher': cmd_chercher(R, r[0], int(opt('--n', 5)))
    elif cmd == 'index': i = construire_index(R); print(f"index : {i['n']} documents")
    elif cmd == 'comparer': cmd_comparer(R, r[0], int(opt('--n', 5)))
    elif cmd == 'pratique': cmd_pratique(R, r[0])
    elif cmd == 'recurrents': cmd_recurrents(R)
    elif cmd == 'progression': cmd_progression(R, opt('--stats'))
    else: sys.exit(__doc__)
