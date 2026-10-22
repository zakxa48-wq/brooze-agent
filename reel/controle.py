"""Contrôle technique d'un Reel avant publication (le contrôle éditorial, lui, passe par brooze-sceptique).

Usage : python3 reel/controle.py sorties/<id>/reel.mp4 [sorties/<id>/reel.json]
Vérifie : 1080×1920, 30 ou 60 i/s, H.264 yuv420p, AAC, durée < 90 s, poids < 95 Mo, son à −14 LUFS ±1 et crête vraie
≤ −1 dBTP, aucun flash ni saut d'image (glitchs.py du skill, coupes déclarées = débuts de scène), puis extrait les images
clés (début, chaque transition, fin) dans une planche à regarder. Écrit controle.json ; code de sortie 1 si un critère
bloquant échoue.
"""
import sys, os, json, subprocess, re

ICI = os.path.dirname(os.path.abspath(__file__))


def sonde(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', video], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def volume(video):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', video, '-filter_complex', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    bloc = r.stderr[r.stderr.rfind('Summary:'):]
    lufs = float(re.search(r'I:\s+(-?[\d.]+) LUFS', bloc).group(1))
    pic = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', bloc).group(1))
    return lufs, pic


def main(video, reel_json=None):
    dossier = os.path.dirname(os.path.abspath(video))
    info = sonde(video); v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next((s for s in info['streams'] if s['codec_type'] == 'audio'), None)
    fps = eval(v['r_frame_rate']); duree = float(info['format']['duration']); poids = int(info['format']['size']) / 1e6
    lufs, pic = volume(video) if a else (None, None)
    ok, pb = [], []
    def critere(cond, texte): (ok if cond else pb).append(texte)
    critere((v['width'], v['height']) == (1080, 1920), f"format {v['width']}×{v['height']}")
    critere(round(fps) in (30, 60), f'{fps:.2f} i/s')
    critere(v['codec_name'] == 'h264' and v.get('pix_fmt') == 'yuv420p', f"vidéo {v['codec_name']} {v.get('pix_fmt')}")
    critere(a is not None and a['codec_name'] == 'aac', f"son {a['codec_name'] if a else 'absent'}")
    critere(duree < 90, f'durée {duree:.1f} s')
    critere(poids < 95, f'poids {poids:.1f} Mo')
    if a:
        critere(abs(lufs + 14) <= 1, f'volume {lufs:.1f} LUFS (cible −14)')
        critere(pic <= -1, f'crête vraie {pic:.1f} dBTP (max −1)')

    # Coupes attendues = débuts de scène (dans le temps du Reel)
    coupes, cles, pb_montage, montage = [], [0.3], [], {}
    if reel_json:
        reel = json.load(open(reel_json))
        mots = json.load(open(os.path.join(dossier, reel.get('mots', 'mots.json'))))
        t0 = (reel.get('source') or [0])[0]
        def temps(x):
            if isinstance(x, str) and x.startswith('@'):
                m = mots[int(x[1:].rstrip('>'))]; return (m['end'] if x.endswith('>') else m['start'] - .12) - t0
            return x
        debuts = [temps(s['de']) for s in reel['scenes']][1:]
        # Montage (MONTAGE.md) : part d'images réelles, nombre de gros textes, transitions répétées.
        # Avertissements non bloquants : l'agent les corrige ou les justifie dans le journal.
        bornes = [temps(x['de']) for x in reel['scenes']] + [duree]
        reel_s = sum(bornes[k + 1] - bornes[k] for k, x in enumerate(reel['scenes']) if x['type'] in ('plan', 'clip'))
        gros = sum(1 for x in reel['scenes'] if x['type'] in ('texte', 'slam', 'barre', 'specs') or (x['type'] == 'plan' and x.get('mots')))
        trs = [x.get('transition', 'glisse') for x in reel['scenes'][1:]]
        types_tr = {t for t in trs if t != 'coupe'}
        part = reel_s / duree
        montage = dict(part_images_reelles=round(part, 2), gros_textes=gros, transitions=sorted(types_tr))
        (ok if part >= .6 else pb_montage).append(f'images réelles {part:.0%} du temps (objectif ≥ 60 %)')
        (ok if gros <= 3 else pb_montage).append(f'{gros} moments de gros texte (objectif ≤ 3)')
        (ok if len(types_tr) <= 2 else pb_montage).append(f"types de transition hors coupe : {', '.join(sorted(types_tr)) or 'aucun'} (objectif ≤ 2)")
        coupes = [round(d, 2) for d in debuts]
        for d in debuts: cles += [d - .05, d + .2, d + .6]
    cles.append(duree - .1)
    sortie_g = os.path.join(dossier, '_glitchs')
    arg = ['--sortie', sortie_g] + (['--coupes', ','.join(map(str, coupes))] if coupes else [])
    g = subprocess.run([sys.executable, os.path.join(ICI, '.outils', 'glitchs.py'), video] + arg, capture_output=True, text=True)
    rapport_g = {}
    if os.path.exists(os.path.join(sortie_g, 'rapport.json')):
        rapport_g = json.load(open(os.path.join(sortie_g, 'rapport.json')))
    sans_alerte = g.returncode == 0 and 'aucune alerte' in g.stdout
    critere(sans_alerte, 'glitchs : aucune alerte' if sans_alerte else 'glitchs : alertes FLASH/SAUT/NOIR/COUPE, voir les bandes')

    # Planche des images clés
    imgs = os.path.join(dossier, '_cles'); os.makedirs(imgs, exist_ok=True)
    for f in os.listdir(imgs): os.remove(os.path.join(imgs, f))
    cles = sorted(set(round(max(0, min(duree - .05, c)), 2) for c in cles))
    for i, c in enumerate(cles):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(c), '-i', video, '-frames:v', '1', '-vf', 'scale=270:480',
                        os.path.join(imgs, f'{i:03d}.jpg')], check=True)
    cols = 8
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(imgs, '%03d.jpg'), '-vf',
                    f'tile={cols}x{(len(cles) + cols - 1) // cols}:padding=6:color=0x222222', '-frames:v', '1',
                    os.path.join(dossier, 'planche_cles.jpg')], check=True)
    res = dict(video=video, ok=ok, problemes=pb, montage=montage, a_justifier=pb_montage, glitchs=rapport_g or g.stdout[-800:], images_cles=cles,
               planche=os.path.join(dossier, 'planche_cles.jpg'), bandes=sortie_g)
    json.dump(res, open(os.path.join(dossier, 'controle.json'), 'w'), ensure_ascii=False, indent=1, default=str)
    print(json.dumps(dict(ok=ok, problemes=pb, a_justifier=pb_montage, planche=res['planche'], glitchs_sortie=g.stdout[-1200:]), ensure_ascii=False, indent=1))
    sys.exit(1 if pb else 0)


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3): sys.exit(__doc__)
    main(*sys.argv[1:])
