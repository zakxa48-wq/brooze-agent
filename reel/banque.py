"""Banque de voix de Zak : on y puise régulièrement pour fabriquer des Reels avec SA vraie voix.

La banque est un dossier (idéalement un dépôt PRIVÉ, voir config.json → "banque") :
  audio/            les enregistrements de Zak, tels quels (sous-dossiers permis)
  index/<audio>/    segs.json, mots.json, rapport.json : transcription vérifiée et calée (jamais de .wav ici)
  catalogue.json    les audios indexés et les IDÉES repérées : fenêtre [t0, t1], idée, cible, hook, score, statut

Usage (R = racine de la banque) :
  python3 reel/banque.py indexer  R                 transcrit les nouveaux audios, affiche texte + fenêtres candidates
  python3 reel/banque.py fenetres R <audio>         fenêtres de 20 à 45 s coupées en fin de phrase, avec leur texte
  python3 reel/banque.py ajouter  R <audio> <t0> <t1> --idee "…" --cible Karim --hook "…" --score 8 [--perime AAAA-MM-JJ]
  python3 reel/banque.py etat     R                 idées disponibles (meilleur score d'abord), utilisées, refusées
  python3 reel/banque.py preparer R <idee> sorties/<id>/   voix.wav + segs/mots de l'audio + brouillon de reel.json
  python3 reel/banque.py marquer  R <idee> en_cours|utilise|refuse|dispo [--post sorties/<id>|posts/<id>] [--jour AAAA-MM-JJ] [--raison "…"]
                    en_cours = Reel commencé, réservé pour --jour (une exécution suivante le reprend, personne ne le refait)
  python3 reel/banque.py verifier R <audio>         après correction de index/<audio>/segs.json : recale les mots, marque vérifié
"""
import sys, os, json, hashlib, argparse, subprocess, shutil, datetime, re

ICI = os.path.dirname(os.path.abspath(__file__))
# Dossier de travail HORS des dépôts : l'audio brut de Zak ne doit jamais finir dans brooze-agent (public)
TRAVAIL = os.path.expanduser('~/.cache/brooze/travail')
EXT = ('.m4a', '.mp3', '.wav', '.aac', '.ogg', '.opus', '.flac', '.mp4', '.mov')


def charger(R):
    p = os.path.join(R, 'catalogue.json')
    return json.load(open(p)) if os.path.exists(p) else {'audios': {}, 'idees': []}


def sauver(R, c):
    json.dump(c, open(os.path.join(R, 'catalogue.json'), 'w'), ensure_ascii=False, indent=1)


def empreinte(f):
    h = hashlib.sha1()
    with open(f, 'rb') as x:
        for b in iter(lambda: x.read(1 << 20), b''): h.update(b)
    return h.hexdigest()[:12]


def ident(f):
    base = re.sub(r'[^a-z0-9]+', '-', os.path.splitext(os.path.basename(f))[0].lower()).strip('-')
    return f'{base[:40]}-{empreinte(f)[:6]}'


def fenetres(mots, mini=20., maxi=45.):
    """Fenêtres qui commencent au début d'une phrase et finissent à la fin d'une phrase, entre mini et maxi secondes."""
    fins = [i for i, m in enumerate(mots) if re.search(r'[.?!…]$', m['w'])]
    debuts = [0] + [i + 1 for i in fins if i + 1 < len(mots)]
    res = []
    for a in debuts:
        meilleure = None
        for b in fins:
            if b < a: continue
            d = mots[b]['end'] - mots[a]['start']
            if d > maxi: break
            if d >= mini: meilleure = b
        if meilleure is not None:
            t0 = max(0, mots[a]['start'] - .15); t1 = mots[meilleure]['end'] + .3
            res.append(dict(t0=round(t0, 2), t1=round(t1, 2), duree=round(t1 - t0, 1), mots=[a, meilleure],
                            texte=' '.join(m['w'] for m in mots[a:meilleure + 1])))
    return res


def cmd_indexer(R):
    c = charger(R); deja = {a['sha1'] for a in c['audios'].values()}; nouveaux = []
    for racine, _, fichiers in os.walk(os.path.join(R, 'audio')):
        for f in sorted(fichiers):
            if not f.lower().endswith(EXT): continue
            chemin = os.path.join(racine, f); h = empreinte(chemin)
            if h in deja: continue
            aid = ident(chemin); travail = os.path.join(TRAVAIL, aid)
            subprocess.run([sys.executable, os.path.join(ICI, 'comprendre.py'), chemin, travail], check=True, stdout=subprocess.DEVNULL)
            dest = os.path.join(R, 'index', aid); os.makedirs(dest, exist_ok=True)
            for n in ('segs.json', 'mots.json', 'rapport.json'): shutil.copy(os.path.join(travail, n), dest)
            rap = json.load(open(os.path.join(dest, 'rapport.json')))
            c['audios'][aid] = dict(fichier=os.path.relpath(chemin, R), sha1=h, duree=rap['duree_voix'], verdict=rap['verdict'],
                                    raisons=rap['raisons'], indexe_le=str(datetime.date.today()), transcription_verifiee=False)
            # fichiers de Zak posés à côté de l'audio : contexte (.txt) et storyboard (.storyboard.md, à respecter au maximum)
            base = os.path.splitext(chemin)[0]
            for cle, ext in (('contexte', '.txt'), ('storyboard', '.storyboard.md')):
                if os.path.exists(base + ext): c['audios'][aid][cle] = os.path.relpath(base + ext, R)
            nouveaux.append(aid); deja.add(h)
    sauver(R, c)
    for aid in nouveaux:
        a = c['audios'][aid]
        print(f"\n=== {aid} · {a['duree']} s · verdict {a['verdict']} {a['raisons'] or ''}")
        print(json.load(open(os.path.join(R, 'index', aid, 'rapport.json')))['transcription'])
        if a.get('contexte'): print(f"contexte de Zak : {a['contexte']}")
        if a.get('storyboard'): print(f"STORYBOARD DE ZAK : {a['storyboard']} → un seul Reel qui le suit au maximum (AGENT_REEL.md § Storyboard)")
        print(f"→ vérifie la transcription (index/{aid}/segs.json), puis : banque.py fenetres R {aid}")
    if not nouveaux: print('Aucun nouvel audio.')


def cmd_fenetres(R, aid):
    mots = json.load(open(os.path.join(R, 'index', aid, 'mots.json')))
    for k, f in enumerate(fenetres(mots)):
        print(f"[{k}] {f['t0']:>7.2f} → {f['t1']:>7.2f} ({f['duree']} s) mots {f['mots']} : {f['texte']}")


def cmd_ajouter(R, a):
    c = charger(R)
    if a.audio not in c['audios']: sys.exit(f'audio inconnu : {a.audio}')
    # Pas deux idées sur des fenêtres qui se recouvrent à plus de 50 % dans le même audio
    for i in c['idees']:
        if i['audio'] == a.audio:
            rec = min(i['source'][1], a.t1) - max(i['source'][0], a.t0)
            if rec > .5 * min(i['source'][1] - i['source'][0], a.t1 - a.t0):
                sys.exit(f"recouvre l'idée {i['id']} ({i['idee']}) : choisis une autre fenêtre")
    iid = f"{a.audio}-{int(a.t0):04d}"
    c['idees'].append(dict(id=iid, audio=a.audio, source=[a.t0, a.t1], idee=a.idee, cible=a.cible, hook=a.hook,
                           score=a.score, perime=a.perime, statut='dispo', ajoute_le=str(datetime.date.today())))
    sauver(R, c); print(f'idée ajoutée : {iid}')


def cmd_etat(R):
    c = charger(R); auj = str(datetime.date.today())
    dispo = [i for i in c['idees'] if i['statut'] == 'dispo' and not (i.get('perime') and i['perime'] < auj)]
    print(f"{len(c['audios'])} audios · {len(c['idees'])} idées : {len(dispo)} disponibles, "
          f"{sum(i['statut'] == 'utilise' for i in c['idees'])} utilisées, {sum(i['statut'] == 'refuse' for i in c['idees'])} refusées")
    for i in [i for i in c['idees'] if i['statut'] == 'en_cours']:
        print(f"  EN COURS (à reprendre d'abord) · {i['id']} · {i.get('post', '?')} · jour réservé {i.get('jour', '?')}")
    non_verifies = [k for k, a in c['audios'].items() if not a.get('transcription_verifiee')]
    if non_verifies: print('transcriptions à vérifier :', ', '.join(non_verifies))
    sans_idee = [k for k, a in c['audios'].items() if a['verdict'] != 'inutilisable' and not any(i['audio'] == k for i in c['idees'])]
    if sans_idee: print('audios sans aucune idée repérée :', ', '.join(sans_idee))
    for i in sorted(dispo, key=lambda i: -i['score']):
        print(f"  {i['score']:>4} · {i['id']} · {i['cible']} · {i['source'][1] - i['source'][0]:.0f} s · {i['idee']} · « {i['hook']} »"
              + (f" · périme le {i['perime']}" if i.get('perime') else ''))


def cmd_preparer(R, iid, dossier):
    c = charger(R); i = next((x for x in c['idees'] if x['id'] == iid), None)
    if not i: sys.exit(f'idée inconnue : {iid}')
    a = c['audios'][i['audio']]; os.makedirs(dossier, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(ICI, 'comprendre.py'), '--nettoyer', os.path.join(R, a['fichier']), dossier], check=True)
    # reprise d'un Reel en cours : voix.wav (non versionnée) est recréée, la transcription corrigée du Reel est gardée
    for n in ('segs.json', 'mots.json', 'rapport.json'):
        if not os.path.exists(os.path.join(dossier, n)): shutil.copy(os.path.join(R, 'index', i['audio'], n), dossier)
    mots = json.load(open(os.path.join(dossier, 'mots.json')))
    dedans = [k for k, m in enumerate(mots) if m['start'] >= i['source'][0] - .02 and m['end'] <= i['source'][1] + .05]
    brouillon = dict(id=os.path.basename(dossier.rstrip('/')), fps=30, source=i['source'], fin=2.4, banque=dict(idee=iid, audio=a['fichier']),
                     avatar=i['cible'], idee=i['idee'], hook=dict(choisi=i['hook'], ecartes=[]), hypothese='', scenes=[],
                     musique=dict(bpm=96, tonalite='la', sections=[]), silences=[], couverture=dict(theme='encre', label='', titre=''))
    if a.get('storyboard'):                                    # storyboard de Zak : copié dans le Reel, à suivre au maximum
        shutil.copy(os.path.join(R, a['storyboard']), os.path.join(dossier, 'storyboard_zak.md')); brouillon['storyboard_zak'] = 'storyboard_zak.md'
        print('storyboard de Zak copié : storyboard_zak.md (à respecter au maximum)')
    p = os.path.join(dossier, 'reel.json')
    if not os.path.exists(p): json.dump(brouillon, open(p, 'w'), ensure_ascii=False, indent=2)
    print(f"prêt : {dossier} · mots {dedans[0]}–{dedans[-1]} de la fenêtre :")
    print(' '.join(f"{k}:{mots[k]['w']}" for k in dedans))


def cmd_verifier(R, aid):
    c = charger(R); a = c['audios'][aid]; travail = os.path.join(TRAVAIL, aid)
    subprocess.run([sys.executable, os.path.join(ICI, 'comprendre.py'), '--nettoyer', os.path.join(R, a['fichier']), travail], check=True)
    shutil.copy(os.path.join(R, 'index', aid, 'segs.json'), travail)
    subprocess.run([sys.executable, os.path.join(ICI, 'comprendre.py'), '--recaler', travail], check=True, stdout=subprocess.DEVNULL)
    shutil.copy(os.path.join(travail, 'mots.json'), os.path.join(R, 'index', aid))
    a['transcription_verifiee'] = True; sauver(R, c); print(f'{aid} : mots recalés, transcription vérifiée')


def cmd_marquer(R, iid, statut, post, raison, jour=None):
    c = charger(R); i = next((x for x in c['idees'] if x['id'] == iid), None)
    if not i: sys.exit(f'idée inconnue : {iid}')
    i.update(statut=statut, date=str(datetime.date.today()), **({'post': post} if post else {}), **({'raison': raison} if raison else {}), **({'jour': jour} if jour else {}))
    sauver(R, c); print(f'{iid} → {statut}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    for n in ('indexer', 'etat'): sp.add_parser(n).add_argument('R')
    x = sp.add_parser('fenetres'); x.add_argument('R'); x.add_argument('audio')
    x = sp.add_parser('ajouter'); x.add_argument('R'); x.add_argument('audio'); x.add_argument('t0', type=float); x.add_argument('t1', type=float)
    for o in ('--idee', '--cible', '--hook'): x.add_argument(o, required=True)
    x.add_argument('--score', type=float, required=True); x.add_argument('--perime')
    x = sp.add_parser('preparer'); x.add_argument('R'); x.add_argument('idee'); x.add_argument('dossier')
    x = sp.add_parser('marquer'); x.add_argument('R'); x.add_argument('idee'); x.add_argument('statut', choices=['en_cours', 'utilise', 'refuse', 'dispo']); x.add_argument('--jour')
    x.add_argument('--post'); x.add_argument('--raison')
    x = sp.add_parser('verifier'); x.add_argument('R'); x.add_argument('audio')
    a = ap.parse_args()
    {'indexer': lambda: cmd_indexer(a.R), 'etat': lambda: cmd_etat(a.R), 'fenetres': lambda: cmd_fenetres(a.R, a.audio),
     'ajouter': lambda: cmd_ajouter(a.R, a), 'preparer': lambda: cmd_preparer(a.R, a.idee, a.dossier),
     'marquer': lambda: cmd_marquer(a.R, a.idee, a.statut, a.post, a.raison, a.jour), 'verifier': lambda: cmd_verifier(a.R, a.audio)}[a.cmd]()
