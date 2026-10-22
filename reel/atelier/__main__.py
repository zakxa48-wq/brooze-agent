"""Atelier Brooze — rendu d'une scène.

  python3 reel/atelier scene.py --image 0.5                 une image PNG (scene_0.50.png) pour vérifier
  python3 reel/atelier scene.py --planche [0,0.2,0.4,…]     planche d'images (scene_planche.jpg), auto si sans liste
  python3 reel/atelier scene.py --sortie essai.mp4          vidéo 1080×1920 H.264 + AAC (son de la scène)
        [--de 0 --a 1.5]  [--travailleurs 4]  [--demi]  (--demi : demi-définition pour un brouillon rapide)
  python3 reel/atelier --aide | --version

La scène est un script Python qui définit `comp` (voir `reel/atelier/LISEZMOI.md`). Les chemins de la scène sont
relatifs à son dossier. Son : `comp.son` (fichier déjà mixé) ou `comp.sons` / `comp.musique` / `comp.voix` (mixés par
son_brooze, synthétisés, −14 LUFS), sinon une piste silencieuse (Instagram veut une piste son).
"""
import sys, os, json, time, tempfile, subprocess, shutil, runpy
ICI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(ICI))
import numpy as np, cv2
import atelier

COMP = None


def charger(scene):
    scene = os.path.abspath(scene); d = os.path.dirname(scene)
    cwd = os.getcwd(); os.chdir(d)
    try: g = runpy.run_path(scene, run_name='__scene__')
    finally: os.chdir(cwd)
    comp = g.get('comp')
    if not isinstance(comp, atelier.Composition): sys.exit('la scène doit définir comp = Composition(...)')
    comp.dossier = d; comp.cache = os.path.join(d, '_atelier_cache')

    def regler(c):
        for cq in c.calques:
            if isinstance(cq, atelier.Precomp): cq.comp.dossier, cq.comp.cache = d, comp.cache; regler(cq.comp)
    regler(comp)
    return comp, scene


def _travail(args):
    scene, demi, idx, dossier = args
    global COMP
    if COMP is None: COMP = charger(scene)[0]
    for i in idx:
        im = COMP.image_8bits(i / COMP.ips)
        if demi: im = cv2.resize(im, (im.shape[1] // 2, im.shape[0] // 2), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(dossier, f'{i:05d}.png'), cv2.cvtColor(im, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_PNG_COMPRESSION, 1])
    return len(idx)


def mixer(comp, sortie_wav, duree):
    if comp.son: return os.path.join(comp.dossier, comp.son)
    if not (comp.sons or comp.musique or comp.voix): return None
    outils = os.path.join(os.path.dirname(ICI), '.outils', 'son_brooze.py')
    ev = [dict(t=s[0], son=s[1], g=s[2] if len(s) > 2 else 1., **({'args': s[3]} if len(s) > 3 else {})) for s in comp.sons]
    part = dict(duree=duree, evenements=ev, silences=comp.silences, fin=round(duree - .05, 3))
    if comp.musique: part['musique'] = comp.musique
    if comp.voix: part['voix'] = os.path.join(comp.dossier, comp.voix)
    d = os.path.dirname(sortie_wav); json.dump(part, open(os.path.join(d, 'partition.json'), 'w'))
    r = subprocess.run([sys.executable, outils, 'partition.json', os.path.basename(sortie_wav)], cwd=d, capture_output=True, text=True)
    if r.returncode: sys.exit('son_brooze : ' + r.stderr[-800:])
    return sortie_wav


def main(a):
    if not a or a[0] in ('--aide', '-h'): print(__doc__); return
    if a[0] == '--version': print(atelier.VERSION); return
    opt = lambda n, d=None: a[a.index(n) + 1] if n in a and a.index(n) + 1 < len(a) and not a[a.index(n) + 1].startswith('--') else (True if n in a else d)
    comp, scene = charger(a[0]); base = os.path.splitext(scene)[0]
    if opt('--image'):
        t = float(opt('--image')); im = comp.image_8bits(t)
        f = f'{base}_{t:.2f}.png'; cv2.imwrite(f, cv2.cvtColor(im, cv2.COLOR_RGB2BGR)); print(f); return
    if opt('--planche'):
        v = opt('--planche')
        ts = [float(x) for x in v.split(',')] if isinstance(v, str) else list(np.round(np.linspace(0, comp.duree - 1 / comp.ips, 12), 2))
        ims = [cv2.resize(comp.image_8bits(t), (270, 480), interpolation=cv2.INTER_AREA) for t in ts]
        for im, t in zip(ims, ts): cv2.putText(im, f'{t:.2f} s', (8, 22), cv2.FONT_HERSHEY_SIMPLEX, .6, (40, 40, 40), 2, cv2.LINE_AA)
        lignes = [np.hstack(ims[i:i + 6] + [np.full_like(ims[0], 34)] * (6 - len(ims[i:i + 6]))) for i in range(0, len(ims), 6)]
        f = f'{base}_planche.jpg'; cv2.imwrite(f, cv2.cvtColor(np.vstack(lignes), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90]); print(f); return
    sortie = opt('--sortie', base + '.mp4'); demi = bool(opt('--demi'))
    de, jusqua = float(opt('--de', 0)), float(opt('--a', comp.duree))
    idx = list(range(int(round(de * comp.ips)), int(round(jusqua * comp.ips))))
    n = int(opt('--travailleurs', os.cpu_count() or 2))
    tmp = tempfile.mkdtemp(prefix='atelier_'); t0 = time.time()
    lots = [(scene, demi, idx[k::n], tmp) for k in range(n)]
    if n > 1:
        import multiprocessing as mp
        with mp.get_context('fork').Pool(n) as p: p.map(_travail, lots)
    else: _travail(lots[0])
    duree = len(idx) / comp.ips
    son = mixer(comp, os.path.join(tmp, 'mix.flac'), comp.duree)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(comp.ips), '-start_number', str(idx[0]), '-i', os.path.join(tmp, '%05d.png')]
    cmd += ['-ss', str(de), '-t', str(duree), '-i', son] if son else ['-f', 'lavfi', '-t', str(duree), '-i', 'anullsrc=r=48000:cl=stereo']
    cmd += ['-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-maxrate', '14M', '-bufsize', '28M',
            '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', str(comp.ips), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
            '-shortest', '-movflags', '+faststart', os.path.abspath(sortie)]
    subprocess.run(cmd, check=True); shutil.rmtree(tmp)
    print(json.dumps(dict(video=os.path.abspath(sortie), images=len(idx), secondes=round(time.time() - t0, 1), version=atelier.VERSION), ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1:])
