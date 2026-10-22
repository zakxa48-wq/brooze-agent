"""Sound design d'un Reel : partition construite depuis reel.json, mixée par son_brooze (skill brooze-direction).

Usage : python3 reel/son.py sorties/<id>/reel.json   → voix_reel.wav, partition.json, mix.flac (−14 LUFS, crête ≤ −1 dB)

Tout est synthétisé (aucun échantillon, aucune musique protégée). Les temps viennent des scènes et des mots calés :
le son tombe à l'image près. Sons automatiques :
  transition glisse / zoom  → whoosh centré sur la coupe        transition volet → glisse_douce
  slam                      → low_hit + snap à l'impact          duel → papier (A), snap (B)
  compteur                  → tick à chaque dixième d'anneau, lock si cuivre_fin
  telephone                 → glisse_tel pendant le défilement   liste → papier par point
  fin                       → shimmer + lock sur l'appel à l'action
reel.json peut ajouter : "sons": [{t, son, g, args}] (temps "@i" acceptés), "musique": {...} (format son_brooze),
"silences": [[a, b]] (silence total : le silence est un instrument), "sans_sons_auto": true.
"""
import sys, os, json, subprocess
import numpy as np, soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
SR = 48000


def main(fichier):
    dossier = os.path.dirname(os.path.abspath(fichier))
    reel = json.load(open(fichier))
    mots_tous = json.load(open(os.path.join(dossier, reel.get('mots', 'mots.json'))))
    t0, t1 = reel.get('source') or [0, mots_tous[-1]['end'] + .3]
    idx0 = next(i for i, m in enumerate(mots_tous) if m['start'] >= t0 - .02)
    mots = [dict(m, start=m['start'] - t0, end=m['end'] - t0) for m in mots_tous if m['start'] >= t0 - .02 and m['end'] <= t1 + .05]
    duree = round(t1 - t0 + reel.get('fin', 0), 3)

    def temps(v):
        if not (isinstance(v, str) and v.startswith('@')): return v
        i = int(v[1:].rstrip('>')) - idx0
        return mots[i]['end'] if v.endswith('>') else mots[i]['start'] - .12

    # Voix de la fenêtre, avec 10 ms de fondu aux bords
    x, _ = sf.read(os.path.join(dossier, 'voix.wav'))
    v = x[int(t0 * SR):int(t1 * SR)].copy(); f = int(.01 * SR); v[:f] *= np.linspace(0, 1, f); v[-f:] *= np.linspace(1, 0, f)
    sf.write(os.path.join(dossier, 'voix_reel.wav'), v.astype(np.float32), SR, subtype='FLOAT')

    scenes = reel['scenes']
    for k, sc in enumerate(scenes):
        sc['_de'] = temps(sc['de']); sc['_a'] = temps(scenes[k + 1]['de']) if k + 1 < len(scenes) else duree
    ev = []
    if not reel.get('sans_sons_auto'):
        for k, sc in enumerate(scenes):
            de, a, tr = sc['_de'], sc['_a'], sc.get('transition', 'glisse')
            if k > 0 and tr in ('glisse', 'zoom'):
                ev.append(dict(t=max(0, de - .22), son='whoosh', g=.55, args=dict(d=.45, pan=[-.6, .6])))
            elif k > 0 and tr == 'volet':
                ev.append(dict(t=max(0, de - .05), son='glisse_douce', g=.6, args=dict(d=.5)))
            typ = sc['type']
            if typ == 'slam':
                ti = temps(sc['t']) if 't' in sc else temps(f"@{sc['mots'][0]}") if 'mots' in sc else de
                ev += [dict(t=ti, son='low_hit', g=.85), dict(t=ti, son='snap', g=.5)]
            elif typ == 'duel':
                ev += [dict(t=temps(sc.get('ta', de + .1)), son='papier', g=.5), dict(t=temps(sc.get('tb', de + .9)), son='snap', g=.55)]
            elif typ == 'compteur':
                c0 = temps(sc.get('t0', de + .2)); c1 = temps(sc.get('t1', c0 + 1))
                ev += [dict(t=c0 + (c1 - c0) * i / 10, son='tick', g=.35) for i in range(10)]
                if sc.get('cuivre_fin'): ev.append(dict(t=c1, son='lock', g=.6))
            elif typ == 'telephone':
                fin_def = temps(sc['arret']) if sc.get('arret') is not None else a
                ev.append(dict(t=de, son='glisse_tel', g=.45, args=dict(d=max(.3, fin_def - de))))
                if sc.get('arret') is not None: ev.append(dict(t=fin_def, son='pop', g=.4))
            elif typ == 'liste':
                for i, it in enumerate(sc['items']):
                    ev.append(dict(t=temps(it['t']) if 't' in it else (temps(f"@{it['mot']}") if 'mot' in it else de + .3 + i * .5), son='papier', g=.45))
            elif typ == 'fin':
                tl = temps(sc.get('t_logo', de + .2))
                ev += [dict(t=tl, son='shimmer', g=.5, args=dict(d=.6)), dict(t=tl + .6, son='lock', g=.5)]
    for e in reel.get('sons', []):
        ev.append(dict(e, t=temps(e['t'])))

    musique = reel.get('musique') or dict(bpm=96, tonalite='la', sections=[[0, duree - .3, 'intro']])
    musique = json.loads(json.dumps(musique))
    musique['sections'] = [[temps(a), temps(b), typ] for a, b, typ in musique['sections']]
    if 'accord_final' in musique: musique['accord_final'] = temps(musique['accord_final'])
    partition = dict(duree=duree, voix='voix_reel.wav', evenements=sorted(ev, key=lambda e: e['t']), musique=musique,
                     silences=[[temps(a), temps(b)] for a, b in reel.get('silences', [])], fin=round(duree - .1, 3))
    json.dump(partition, open(os.path.join(dossier, 'partition.json'), 'w'), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, os.path.join(ICI, '.outils', 'son_brooze.py'), 'partition.json', 'mix.flac'],
                       cwd=dossier, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-1500:])
    if r.returncode: sys.exit(r.returncode)


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
