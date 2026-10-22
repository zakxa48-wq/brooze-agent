"""Rushs et photos de Zak (dans la banque privée) : les indexer pour que l'agent les choisisse à l'œil.

La banque (dépôt privé brooze-voix) contient `rushs/` : vidéos et photos de Zak, de ses clients (avec accord) ou de
Brooze, rangées comme il veut. L'agent ne voit pas une vidéo : il regarde une PLANCHE (6 images datées) par rush,
puis décrit ce qu'il voit dans `rushs.json` (description, moments utiles, ambiance). C'est ce qui permet de monter
avec de vraies images.

Usage (R = racine de la banque) :
  python3 reel/rushs.py indexer R        nouveaux rushs → index/rushs/<id>.jpg (planche) + entrée dans rushs.json
  python3 reel/rushs.py liste   R        tous les rushs : décrits ou non, nombre d'utilisations
  python3 reel/rushs.py copier  R <id> <dossier>   copie le rush dans le dossier du Reel (chemin à mettre dans reel.json)
Après `indexer`, regarde chaque planche et complète dans rushs.json : "description", "moments" [[t0, t1, "ce qu'on y
voit"]], "ambiance", "personnes" (visages reconnaissables : accord requis avant usage), "a_eviter".
"""
import sys, os, json, subprocess, hashlib, re, shutil, datetime

EXT_V = ('.mp4', '.mov', '.m4v', '.webm', '.mkv', '.avi')
EXT_I = ('.jpg', '.jpeg', '.png', '.heic', '.webp')


def empreinte(f):
    h = hashlib.sha1()
    with open(f, 'rb') as x:
        for b in iter(lambda: x.read(1 << 20), b''): h.update(b)
    return h.hexdigest()[:10]


def sonde(f):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration', '-of', 'json', f],
                       capture_output=True, text=True)
    d = json.loads(r.stdout or '{}'); s = (d.get('streams') or [{}])[0]
    return dict(largeur=s.get('width'), hauteur=s.get('height'), duree=round(float(d.get('format', {}).get('duration', 0) or 0), 2),
                ips=s.get('r_frame_rate'))


def planche(f, dest, duree, video):
    if not video:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vf', 'scale=540:-2', dest], check=True); return
    n = 6; ts = [duree * (k + .5) / n for k in range(n)]
    tmp = dest + '_tmp'; os.makedirs(tmp, exist_ok=True)
    for k, t in enumerate(ts):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', f, '-frames:v', '1', '-vf',
                        f"scale=360:-2,drawtext=text='{t:.1f} s':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@.5",
                        os.path.join(tmp, f'{k}.jpg')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(tmp, '%d.jpg'), '-vf', 'tile=3x2:padding=6:color=0x222222',
                    '-frames:v', '1', dest], check=True)
    shutil.rmtree(tmp)


def charger(R):
    p = os.path.join(R, 'rushs.json')
    return json.load(open(p)) if os.path.exists(p) else {}


def indexer(R):
    cat = charger(R); connus = {v['sha1'] for v in cat.values()}; nouveaux = []
    os.makedirs(os.path.join(R, 'index', 'rushs'), exist_ok=True)
    for racine, _, fichiers in os.walk(os.path.join(R, 'rushs')):
        for f in sorted(fichiers):
            ext = os.path.splitext(f)[1].lower()
            if ext not in EXT_V + EXT_I: continue
            chemin = os.path.join(racine, f); h = empreinte(chemin)
            if h in connus: continue
            rid = re.sub(r'[^a-z0-9]+', '-', os.path.splitext(f)[0].lower()).strip('-')[:40] + '-' + h[:6]
            video = ext in EXT_V; meta = sonde(chemin)
            planche(chemin, os.path.join(R, 'index', 'rushs', f'{rid}.jpg'), meta['duree'], video)
            cat[rid] = dict(fichier=os.path.relpath(chemin, R), sha1=h, type='video' if video else 'photo', **meta,
                            indexe_le=str(datetime.date.today()), description='', moments=[], ambiance='', personnes='',
                            a_eviter='', utilisations=[])
            nouveaux.append(rid); connus.add(h)
    json.dump(cat, open(os.path.join(R, 'rushs.json'), 'w'), ensure_ascii=False, indent=1)
    for rid in nouveaux:
        print(f"{rid} · {cat[rid]['type']} · {cat[rid]['duree']} s · planche : index/rushs/{rid}.jpg → à décrire dans rushs.json")
    if not nouveaux: print('Aucun nouveau rush.')


def liste(R):
    cat = charger(R)
    if not cat: print('Aucun rush indexé (dépose des vidéos ou photos dans rushs/ de la banque).'); return
    for rid, v in cat.items():
        print(f"{rid} · {v['type']} · {v['duree']} s · {'décrit' if v['description'] else 'À DÉCRIRE'} · utilisé {len(v['utilisations'])} fois · {v['description'][:70]}")


def copier(R, rid, dossier):
    v = charger(R)[rid]; os.makedirs(dossier, exist_ok=True)
    dest = os.path.join(dossier, os.path.basename(v['fichier'])); shutil.copy(os.path.join(R, v['fichier']), dest)
    print(dest)


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    c, R = sys.argv[1], sys.argv[2]
    {'indexer': lambda: indexer(R), 'liste': lambda: liste(R), 'copier': lambda: copier(R, sys.argv[3], sys.argv[4])}[c]()
