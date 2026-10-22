"""Sound design d'un Reel : partition construite depuis reel.json, mixée par son_brooze (skill brooze-direction).

Usage : python3 reel/son.py sorties/<id>/reel.json   → voix_reel.wav, partition.json, mix.flac (−14 LUFS, crête ≤ −1 dB)

Tout est synthétisé (aucun échantillon, aucune musique protégée). Les temps viennent des scènes et des mots calés :
le son tombe à l'image près. Sons automatiques :
  transition glisse / zoom  → whoosh centré sur la coupe        transition volet → glisse_douce
  transition whip           → whoosh court droite → gauche       punch (coups de zoom) → low_hit discret
  plan / clip (images réelles) → ambiance « airy » très basse, sauf sans_air
  slam                      → low_hit + snap à l'impact          duel → papier (A), snap (B)
  compteur                  → tick à chaque dixième d'anneau, lock si cuivre_fin
  telephone                 → glisse_tel pendant le défilement   liste → papier par point
  fin                       → shimmer + lock sur l'appel à l'action
reel.json peut ajouter : "sons": [{t, son, g, args}] (temps "@i" acceptés), "musique": {...} (format son_brooze),
"silences": [[a, b]] (silence total : le silence est un instrument), "sans_sons_auto": true.

Bruitages en plus (retour de Zak, 22/10 : « plus de SFX, sans en abuser ») :
  hook                      → aspiration (rev_whoosh) qui arrive sur le premier coup de zoom, si le Reel en a un tôt
  coupe franche entre images réelles → souffle très court et très bas (une coupe sur deux au plus, le limiteur décide)
  plan avec titre (mots)    → snap discret à l'apparition du premier mot
  mots-clés de la voix      → son contextuel au mot (LEXIQUE_SFX : « photo » → obturateur, « prix » → caisse…),
                              une fois par mot-clé ; "sfx_mots": false pour couper, {"mot": "son"} pour compléter
LIMITEUR DE DENSITÉ : les sons sont gardés par priorité (manuels > structure > coups de zoom > contexte > coupes),
jamais deux à moins de 0,6 s, au plus 2 dans une fenêtre de 3 s (ambiances, ticks de compteur et sons manuels exemptés).
Les sons écartés sont listés dans partition.json (« ecartes ») : l'agent vérifie qu'aucun son important n'y est.
"""
import sys, os, json, subprocess
import numpy as np, soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
SR = 48000
# mot dit (début du mot, minuscules sans ponctuation) → bruitage ; un son par mot-clé et par Reel, jamais inventé :
# le son illustre ce que Zak DIT à cet instant
LEXIQUE_SFX = {'photo': 'shutter', 'photos': 'shutter', 'photographie': 'shutter', 'photographies': 'shutter',
               'shoot': 'shutter', 'shot': 'shutter', 'prises': 'shutter', 'clic': 'tick', 'clique': 'tick',
               'prix': 'caisse', 'vendre': 'caisse', 'vend': 'caisse', 'vente': 'caisse', 'ventes': 'caisse',
               'réglé': 'lock', 'validé': 'lock', 'notification': 'beep', 'message': 'beep', 'écran': 'pop',
               'liste': 'papier_glisse', 'fiche': 'papier_glisse', 'écrit': 'trait', 'dessine': 'trait',
               'lumière': 'relais', 'tombe': 'air', 'verre': 'verre'}
GAIN_SFX = {'shutter': .4, 'tick': .3, 'caisse': .35, 'lock': .4, 'beep': .3, 'pop': .3, 'papier_glisse': .35,
            'trait': .3, 'relais': .35, 'air': .35, 'verre': .35}
EXEMPTS = {'airy', 'bourdon'}


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
            elif k > 0 and tr == 'whip':     # panoramique filé : whoosh court qui traverse la stéréo de droite à gauche
                ev.append(dict(t=max(0, de - .16), son='whoosh', g=.6, args=dict(d=.34, pan=[.8, -.8], peak=.5)))
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
        for e in ev: e.setdefault('prio', 1)
        # coups de zoom sur les mots forts : un grave discret, à l'image de l'impact
        for tp in reel.get('punch', []):
            ev.append(dict(t=temps(tp) + .12, son='low_hit', g=.35, prio=2))
        # hook : une aspiration qui arrive sur le premier coup de zoom s'il tombe dans les 3 premières secondes
        p0 = min([temps(tp) + .12 for tp in reel.get('punch', [])] or [99])
        if p0 < 3: ev.append(dict(t=max(0, p0 - .45), son='rev_whoosh', g=.4, args=dict(d=.45), prio=2, ancre=p0))
        # coupes franches entre deux images réelles : un souffle très court (le limiteur en garde une sur deux au plus)
        for k, sc in enumerate(scenes):
            if k and sc.get('transition', 'glisse') == 'coupe' and sc['type'] in ('plan', 'clip') and scenes[k - 1]['type'] in ('plan', 'clip') and k % 2 == 0:
                ev.append(dict(t=max(0, sc['_de'] - .1), son='whoosh', g=.2, args=dict(d=.22, pan=[-.3, .3], peak=.6), prio=4))
            if sc['type'] == 'plan' and sc.get('mots'):      # titre posé sur l'image : il arrive avec son premier mot
                ev.append(dict(t=mots[sc['mots'][0] - idx0]['start'], son='snap', g=.3, prio=3))
        # sons contextuels sur les mots-clés dits
        lex = dict(LEXIQUE_SFX, **(reel['sfx_mots'] if isinstance(reel.get('sfx_mots'), dict) else {}))
        if reel.get('sfx_mots') is not False:
            vus = set()
            for m in mots:
                cle = m['w'].lower().strip(' .,!?;:«»"\'')
                if cle in lex and lex[cle] and cle not in vus:
                    vus.add(cle); ev.append(dict(t=m['start'], son=lex[cle], g=GAIN_SFX.get(lex[cle], .35), prio=3, mot=cle))
        # air : une ambiance très basse sous les images réelles (un plan réel sans air sonne faux)
        for k, sc in enumerate(scenes):
            if sc['type'] in ('plan', 'clip') and not sc.get('sans_air'):
                ev.append(dict(t=sc['_de'], son='airy', g=.18, args=dict(d=max(.3, sc['_a'] - sc['_de'] + .3))))
    for e in reel.get('sons', []):
        ev.append(dict(e, t=temps(e['t']), prio=0))
    ev, ecartes = limiter(ev)

    musique = reel.get('musique') or dict(bpm=96, tonalite='la', sections=[[0, duree - .3, 'intro']])
    musique = json.loads(json.dumps(musique))
    musique['sections'] = [[temps(a), temps(b), typ] for a, b, typ in musique['sections']]
    if 'accord_final' in musique: musique['accord_final'] = temps(musique['accord_final'])
    partition = dict(duree=duree, voix='voix_reel.wav', evenements=sorted(ev, key=lambda e: e['t']), musique=musique,
                     silences=[[temps(a), temps(b)] for a, b in reel.get('silences', [])], fin=round(duree - .1, 3), ecartes=ecartes)
    json.dump(partition, open(os.path.join(dossier, 'partition.json'), 'w'), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, os.path.join(ICI, '.outils', 'son_brooze.py'), 'partition.json', 'mix.flac'],
                       cwd=dossier, capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-1500:])
    if r.returncode: sys.exit(r.returncode)


def limiter(ev, ecart=.6, fenetre=3., maxi=2):
    """Garde les bruitages par priorité : jamais deux « moments sonores » à moins de `ecart` s, au plus `maxi` par
    `fenetre` s. Les sons au même instant (± 0,05 s, ex. low_hit + snap d'un slam) comptent pour un seul moment."""
    libres = [e for e in ev if e['son'] in EXEMPTS or e.get('prio') == 0 or e['son'] == 'tick']
    cand = sorted([e for e in ev if e not in libres], key=lambda e: (e.get('prio', 1), e['t']))
    moments, gardes, ecartes = [m['t'] for m in libres if m.get('prio') == 0], [], []
    for e in cand:
        t = e.get('ancre', e['t'])        # un son qui prépare un impact (rev_whoosh) compte au moment de l'impact
        if any(abs(t - m) < .05 for m in moments): gardes.append(e); continue
        trop_pres = any(abs(t - m) < ecart for m in moments)
        dense = any(sum(1 for m in moments if a <= m < a + fenetre) >= maxi for a in (t - fenetre + .01, t - fenetre / 2, t))
        if trop_pres or dense: ecartes.append(dict(t=round(e['t'], 2), son=e['son'], raison='trop près' if trop_pres else 'trop dense'))
        else: gardes.append(e); moments.append(t)
    for e in libres + gardes: e.pop('prio', None); e.pop('mot', None); e.pop('ancre', None)
    return libres + gardes, ecartes


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
