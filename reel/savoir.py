"""Savoir de l'agent Brooze : les CONNAISSANCES du monde (études, méthodes, livres, vidéos, articles), reliées entre elles.

Ce n'est pas un entraînement du modèle : c'est une mémoire écrite, organisée comme on organise un savoir. L'agent la
relit avant d'agir et l'enrichit chaque jour (séance d'apprentissage, CERVEAU.md § 8). Rien n'est jamais effacé.

Données (dépôt PRIVÉ brooze-voix, R = /home/user/brooze-voix) : R/data/cerveau/savoir/
  sources.jsonl        une ligne par source lue (étude, livre, vidéo, article…), avec sa nature et ce qui en a été lu
  affirmations.jsonl   ce que l'on sait : un énoncé, ses preuves pour/contre (sources pondérées), un niveau de confiance
  notions/<id>.md      une page par notion : définition et « ce que ça change dans mon travail » (écrits par l'agent),
                       puis un bloc automatique (affirmations, liens, sources)
  liens.jsonl          connexions entre notions (explique, precise, contredit, cause, exemple-de, outil-pour, oppose)
  questions.md         ce que l'agent cherche à comprendre (sa curiosité : nourrit la séance du jour)
  seances.jsonl        une ligne par séance d'apprentissage
  carte.md             vue d'ensemble régénérée : notions, niveaux, liens
  memoire.json         empreinte de tout ce qui a été appris (contrôle « ne rien oublier »)

Commandes (python3 reel/savoir.py <commande> R …) :
  etat       R                          chiffres du savoir, séance du jour faite ou non
  aujourdhui R                          code 0 si la séance du jour est faite, 1 sinon
  source     R '<json>'                 ajoute une source (refuse un doublon : même url ou même fichier) → S-xxxx
  notion     R <id> "<titre>" [--definition "…"]   crée la page d'une notion (si elle n'existe pas)
  affirmer   R '<json>'                 nouvelle affirmation, ou preuve ajoutée à une affirmation existante ("id")
  lier       R <notion-a> <notion-b> <relation> ["note"]
  chercher   R "<propos>" [--n 8]       notions et affirmations utiles pour un propos (+ notions voisines)
  rappel     R [--n 3]                  notions les moins revues récemment (à relire et consolider)
  revu       R <notion> ["ce qui a été consolidé"]
  seance     R '<json>'                 enregistre la séance d'apprentissage du jour
  carte      R                          régénère les blocs automatiques des notions et carte.md
  verifier   R                          rien d'oublié (toutes les ids d'hier existent), cohérence ; met à jour memoire.json
"""
import sys, os, json, re, datetime, math, hashlib

TYPES_SOURCE = {   # poids d'une preuve selon la nature de la source (avant le facteur « lu »)
    'meta-analyse': 3.0, 'etude': 2.0, 'mesure-compte': 2.5, 'doc-plateforme': 1.5, 'livre': 1.5,
    'praticien': 1.0, 'cours': 1.0, 'video': 0.75, 'article': 0.75, 'vendeur': 0.4, 'opinion': 0.25,
}
LU = {'complet': 1.0, 'extrait': 0.7, 'resume': 0.5}   # resume = seulement le résumé d'un moteur de recherche
NIVEAUX = ['réfutée', 'douteuse', 'à vérifier', 'probable', 'solide']
RELATIONS = ['explique', 'precise', 'contredit', 'cause', 'exemple-de', 'outil-pour', 'oppose', 'complete']
MOTS_VIDES = set('les des une un le la de du et en au aux pour par sur dans avec que qui est son ses ce cette ces pas plus '
                 'ne se sa leur leurs ou on il elle ils nous vous tu je the and of to in for on with is are be that this'.split())


def D(R):
    d = os.path.join(R, 'data', 'cerveau', 'savoir'); os.makedirs(os.path.join(d, 'notions'), exist_ok=True); return d
def aujourd(): return datetime.date.today().isoformat()
def lire(R, nom):
    p = os.path.join(D(R), nom)
    return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()] if os.path.exists(p) else []
def ecrire(R, nom, xs):
    with open(os.path.join(D(R), nom), 'w', encoding='utf-8') as f:
        for x in xs: f.write(json.dumps(x, ensure_ascii=False) + '\n')
def ajouter(R, nom, x):
    with open(os.path.join(D(R), nom), 'a', encoding='utf-8') as f: f.write(json.dumps(x, ensure_ascii=False) + '\n')
def suivant(xs, p): return f"{p}-{max([int(x['id'].split('-')[1]) for x in xs] + [0]) + 1:04d}"
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('é', 'e').replace('è', 'e').replace('à', 'a')).strip('-')[:50]
def jetons(t): return [w for w in re.findall(r"[a-zàâäçéèêëîïôöùûüœ0-9]+", (t or '').lower()) if w not in MOTS_VIDES and len(w) > 2]
def page(R, n): return os.path.join(D(R), 'notions', n + '.md')
def notions(R): return sorted(f[:-3] for f in os.listdir(os.path.join(D(R), 'notions')) if f.endswith('.md'))
def titre(R, n):
    l = open(page(R, n), encoding='utf-8').readline().strip(); return l[2:] if l.startswith('# ') else n


# ---------------------------------------------------------------- confiance : elle s'affine, elle ne bascule pas
def poids(src, sens=1):
    return round(TYPES_SOURCE.get(src.get('type'), 0.5) * LU.get(src.get('lu'), 0.5), 2)

def evaluer(a, srcs):
    """Score = somme des preuves pondérées. Niveau déduit du score, avec deux freins :
    - « solide » exige au moins 2 sources indépendantes dont une de poids ≥ 2 (étude, méta-analyse, mesure du compte) ;
    - une nouvelle preuve ne déplace le niveau que d'UN cran (une source ne retourne jamais tout le savoir)."""
    pour = sum(p['poids'] for p in a['preuves'] if p['sens'] > 0); contre = sum(p['poids'] for p in a['preuves'] if p['sens'] < 0)
    s = pour - contre
    n = 0 if s <= -2 else 1 if s <= -0.5 else 2 if s < 1.5 else 3 if s < 4 else 4
    if n == 4:
        fortes = [p for p in a['preuves'] if p['sens'] > 0 and p['poids'] >= 2]
        if len({p['source'] for p in a['preuves'] if p['sens'] > 0}) < 2 or not fortes: n = 3
    if 'niveau' in a and a['niveau'] in NIVEAUX:
        avant = NIVEAUX.index(a['niveau']); n = max(avant - 1, min(avant + 1, n))
    return round(pour, 2), round(contre, 2), NIVEAUX[n], pour >= 1.5 and contre >= 1.5


# ---------------------------------------------------------------- commandes
def cmd_source(R, js):
    x = json.loads(js); srcs = lire(R, 'sources.jsonl')
    for k in ('titre', 'type', 'lu'):
        if not x.get(k): sys.exit(f'champ manquant : {k}  (type ∈ {list(TYPES_SOURCE)} ; lu ∈ {list(LU)})')
    if x['type'] not in TYPES_SOURCE: sys.exit(f'type inconnu : {x["type"]} ({list(TYPES_SOURCE)})')
    if x['lu'] not in LU: sys.exit(f'lu inconnu : {x["lu"]} ({list(LU)})')
    cle = x.get('url') or x.get('fichier') or x['titre']
    for s in srcs:
        if (s.get('url') or s.get('fichier') or s['titre']).rstrip('/') == cle.rstrip('/'):
            # même source relue plus complètement : on garde la même id et on note ce qui a été lu en plus
            if LU[x['lu']] > LU.get(s['lu'], 0):
                s.setdefault('relectures', []).append(dict(date=aujourd(), lu=x['lu'], resume=x.get('resume', ''))); s['lu'] = x['lu']
                ecrire(R, 'sources.jsonl', srcs); print(f"{s['id']} (déjà connue, relue : {x['lu']})")
            else: print(f"{s['id']} (déjà connue)")
            return s['id']
    x['id'] = suivant(srcs, 'S'); x.setdefault('ajoute', aujourd()); x.setdefault('origine', 'web')
    ajouter(R, 'sources.jsonl', x); print(x['id']); return x['id']


def cmd_notion(R, n, t, definition=None):
    n = slug(n)
    if os.path.exists(page(R, n)): print(f'{n} (existe déjà : la compléter plutôt que la refaire)'); return n
    open(page(R, n), 'w', encoding='utf-8').write(
        f"# {t}\n\n**Définition** : {definition or '(à écrire avec ses propres mots, à partir des sources)'}\n\n"
        f"## Ce que ça change dans mon travail\n(compétence concrète : quand l'utiliser, comment, sur quel moment d'un Reel)\n\n"
        f"## Ce que j'en comprends\n(synthèse qui s'affine avec chaque source ; on précise, on nuance, on ne réécrit pas tout)\n\n"
        f"<!-- auto -->\n<!-- /auto -->\n")
    print(n); return n


def similaires(a_txt, affs, seuil=.45):
    q = set(jetons(a_txt)); out = []
    for a in affs:
        e = set(jetons(a['enonce']))
        if q and e:
            j = len(q & e) / len(q | e)
            if j >= seuil: out.append((round(j, 2), a))
    return sorted(out, key=lambda x: -x[0])


def cmd_affirmer(R, js):
    """{"notion": "…", "enonce": "…", "source": "S-0001", "sens": 1|-1, "note": "ce que la source dit exactement"}
    ou {"id": "A-0003", "source": …, "sens": …, "note": …} pour ajouter une preuve à ce qu'on savait déjà.
    "nouvelle": true seulement si une affirmation proche existe mais dit vraiment autre chose."""
    x = json.loads(js); affs = lire(R, 'affirmations.jsonl'); srcs = {s['id']: s for s in lire(R, 'sources.jsonl')}
    if x.get('source') not in srcs: sys.exit(f"source inconnue : {x.get('source')} (l'ajouter d'abord avec « source »)")
    sens = 1 if int(x.get('sens', 1)) > 0 else -1; src = srcs[x['source']]
    preuve = dict(source=src['id'], sens=sens, poids=poids(src), note=x.get('note', ''), date=aujourd())
    if 'id' not in x:
        if not x.get('notion') or not x.get('enonce'): sys.exit('il faut "notion" et "enonce" (ou "id" d\'une affirmation existante)')
        if not os.path.exists(page(R, slug(x['notion']))): sys.exit(f"notion inconnue : {x['notion']} (la créer avec « notion », ou en choisir une existante)")
        proches = similaires(x['enonce'], affs)
        if proches and not x.get('nouvelle'):
            print('Affirmations proches déjà connues : ajoute ta source comme preuve de l\'une d\'elles ("id"), '
                  'ou relance avec "nouvelle": true si elle dit vraiment autre chose :')
            for j, a in proches[:5]: print(f"  {a['id']} [{a['niveau']}] ({j}) {a['enonce']}")
            sys.exit(1)
        a = dict(id=suivant(affs, 'A'), notion=slug(x['notion']), enonce=x['enonce'], preuves=[preuve], cree=aujourd(), historique=[])
        a['pour'], a['contre'], niv, a['contestee'] = evaluer(dict(preuves=a['preuves']), srcs)
        a['niveau'] = niv; a['historique'].append(dict(date=aujourd(), niveau=niv, cause=f"création ({src['id']})"))
        affs.append(a)
    else:
        a = next((y for y in affs if y['id'] == x['id']), None)
        if not a: sys.exit(f"affirmation inconnue : {x['id']}")
        if any(p['source'] == src['id'] for p in a['preuves']): print(f"{a['id']} : {src['id']} y est déjà (une source ne compte qu'une fois)"); return
        a['preuves'].append(preuve); avant = a['niveau']
        a['pour'], a['contre'], a['niveau'], a['contestee'] = evaluer(a, srcs)
        if a['niveau'] != avant or sens < 0:
            a['historique'].append(dict(date=aujourd(), niveau=a['niveau'], cause=f"{'contre' if sens < 0 else 'pour'} ({src['id']})"))
    ecrire(R, 'affirmations.jsonl', affs)
    print(f"{a['id']} [{a['niveau']}{', contestée' if a['contestee'] else ''}] pour {a['pour']} / contre {a['contre']} : {a['enonce']}")


def cmd_lier(R, a, b, rel, note=''):
    a, b = slug(a), slug(b)
    for n in (a, b):
        if not os.path.exists(page(R, n)): sys.exit(f'notion inconnue : {n}')
    if rel not in RELATIONS: sys.exit(f'relation inconnue : {rel} ({RELATIONS})')
    ls = lire(R, 'liens.jsonl')
    if any(l['a'] == a and l['b'] == b and l['relation'] == rel for l in ls): print('lien déjà connu'); return
    ajouter(R, 'liens.jsonl', dict(a=a, b=b, relation=rel, note=note, date=aujourd())); print(f'{a} —{rel}→ {b}')


def voisins(R, n):
    return [(l['b'] if l['a'] == n else l['a'], l['relation'], l.get('note', '')) for l in lire(R, 'liens.jsonl') if n in (l['a'], l['b'])]


def chercher(R, requete, n=8):
    """Activation : les notions qui répondent au propos, pondérées par la confiance de ce qu'elles contiennent, puis
    leurs voisines directes (comme un souvenir en appelle un autre). Renvoie les lignes à afficher."""
    q = set(jetons(requete)); affs = lire(R, 'affirmations.jsonl'); conf = {'solide': 1.0, 'probable': .8, 'à vérifier': .5, 'douteuse': .2, 'réfutée': .1}
    if not q or not notions(R): return []
    score = {}
    for no in notions(R):
        txt = open(page(R, no), encoding='utf-8').read().split('<!-- auto -->')[0]
        j = jetons(txt + ' ' + no.replace('-', ' ')); s = sum(1 for w in j if w in q) / (1 + math.log(1 + len(j)))
        for a in affs:
            if a['notion'] == no: s += conf[a['niveau']] * len(q & set(jetons(a['enonce']))) * .5
        if s > 0: score[no] = s
    for no, s in list(score.items()):
        for v, _, _ in voisins(R, no): score[v] = max(score.get(v, 0), s * .4)
    lignes = []
    for no, s in sorted(score.items(), key=lambda x: -x[1])[:n]:
        lignes.append(f"- [{s:.2f}] **{titre(R, no)}** (`notions/{no}.md`)")
        ch = open(page(R, no), encoding='utf-8').read()
        m = re.search(r'## Ce que ça change dans mon travail\n(.+?)\n\n', ch, re.S)
        if m and not m.group(1).startswith('('): lignes.append(f"    → {' '.join(m.group(1).split())[:400]}")
        for a in sorted([a for a in affs if a['notion'] == no and a['niveau'] in ('solide', 'probable', 'à vérifier')],
                        key=lambda a: -NIVEAUX.index(a['niveau']))[:3]:
            lignes.append(f"    {a['id']} [{a['niveau']}{', contestée' if a.get('contestee') else ''}] {a['enonce']}")
        for v, r, _ in voisins(R, no)[:3]: lignes.append(f"    lien : {r} → {v}")
    return lignes


def cmd_chercher(R, requete, n=8):
    l = chercher(R, requete, n)
    print(f'# Savoir utile pour : « {requete} »'); print('\n'.join(l) if l else '(rien de connu sur ce sujet : bonne question pour la prochaine séance → questions.md)')


def revues(R):
    p = os.path.join(D(R), 'revues.json'); return json.load(open(p)) if os.path.exists(p) else {}

def cmd_rappel(R, n=3):
    rv = revues(R); affs = lire(R, 'affirmations.jsonl')
    def age(no):
        d = rv.get(no, {}).get('date') or '2000-01-01'; return (datetime.date.today() - datetime.date.fromisoformat(d)).days
    cand = sorted(notions(R), key=lambda no: -age(no))[:n]
    print('# À relire et consolider (les moins revues) : relire la page, ses sources, ses liens ; préciser la synthèse,')
    print('#   relier à ce qui a été appris depuis, noter ce que ça change ; puis « revu ».')
    for no in cand: print(f"- {no} (revue il y a {age(no) if age(no) < 9000 else 'jamais'} j, {sum(a['notion'] == no for a in affs)} affirmations)")


def cmd_revu(R, no, quoi=''):
    no = slug(no); rv = revues(R)
    if not os.path.exists(page(R, no)): sys.exit(f'notion inconnue : {no}')
    rv[no] = dict(date=aujourd(), quoi=quoi, fois=rv.get(no, {}).get('fois', 0) + 1)
    json.dump(rv, open(os.path.join(D(R), 'revues.json'), 'w'), ensure_ascii=False, indent=1); print(f'{no} revue')


def cmd_seance(R, js):
    """{"duree_min": 20, "requetes": [...], "sources": ["S-…"], "notions_nouvelles": [...], "affirmations": ["A-…"],
        "liens": n, "revues": [...], "change": "ce que ça change concrètement dans le travail", "questions_ouvertes": [...],
        "limites": "ce qui n'a pas pu être lu (réseau, paywall…)"}"""
    x = json.loads(js); x.setdefault('date', aujourd()); ajouter(R, 'seances.jsonl', x); print(f"séance du {x['date']} enregistrée")


def cmd_aujourdhui(R):
    fait = any(s.get('date') == aujourd() for s in lire(R, 'seances.jsonl'))
    print('séance du jour : faite' if fait else 'séance du jour : PAS ENCORE FAITE'); sys.exit(0 if fait else 1)


def cmd_carte(R):
    affs = lire(R, 'affirmations.jsonl'); srcs = {s['id']: s for s in lire(R, 'sources.jsonl')}
    for no in notions(R):
        ch = open(page(R, no), encoding='utf-8').read()
        b = ['<!-- auto -->', '## Ce que l\'on sait (régénéré par savoir.py, ne pas éditer ce bloc)']
        for a in sorted([a for a in affs if a['notion'] == no], key=lambda a: -NIVEAUX.index(a['niveau'])):
            b.append(f"- **{a['id']}** [{a['niveau']}{', contestée' if a.get('contestee') else ''}] {a['enonce']}")
            for p in a['preuves']:
                s = srcs.get(p['source'], {}); b.append(f"  - {'pour' if p['sens'] > 0 else 'CONTRE'} · {p['source']} · {s.get('type')} · lu {s.get('lu')} · {s.get('titre', '')[:90]} : {p['note'][:160]}")
        v = voisins(R, no)
        if v: b += ['', '## Liens'] + [f"- {r} → [{t}](./{t}.md){' : ' + nt if nt else ''}" for t, r, nt in v]
        b.append('<!-- /auto -->')
        avant = ch.split('<!-- auto -->')[0].rstrip() + '\n\n'
        open(page(R, no), 'w', encoding='utf-8').write(avant + '\n'.join(b) + '\n')
    c = ['# Carte du savoir (régénérée par `savoir.py carte`)', '',
         f"{len(srcs)} sources · {len(affs)} affirmations · {len(notions(R))} notions · {len(lire(R, 'liens.jsonl'))} liens", '',
         '| Notion | Affirmations (solide / probable / à vérifier / douteuse-réfutée) | Liens |', '|---|---|---|']
    for no in notions(R):
        aa = [a for a in affs if a['notion'] == no]; k = lambda *ns: sum(a['niveau'] in ns for a in aa)
        c.append(f"| [{titre(R, no)}](notions/{no}.md) | {k('solide')} / {k('probable')} / {k('à vérifier')} / {k('douteuse', 'réfutée')} | {len(voisins(R, no))} |")
    open(os.path.join(D(R), 'carte.md'), 'w', encoding='utf-8').write('\n'.join(c) + '\n'); print('\n'.join(c[:3]))


def empreinte(R):
    return dict(sources=sorted(s['id'] for s in lire(R, 'sources.jsonl')), affirmations=sorted(a['id'] for a in lire(R, 'affirmations.jsonl')),
                notions=notions(R), liens=sorted(f"{l['a']}|{l['relation']}|{l['b']}" for l in lire(R, 'liens.jsonl')))

def cmd_verifier(R):
    p = os.path.join(D(R), 'memoire.json'); avant = json.load(open(p)) if os.path.exists(p) else {}
    now = empreinte(R); perdus = {k: sorted(set(avant.get(k, [])) - set(v)) for k, v in now.items()}
    srcs = {s['id'] for s in lire(R, 'sources.jsonl')}; probs = []
    for a in lire(R, 'affirmations.jsonl'):
        if not os.path.exists(page(R, a['notion'])): probs.append(f"{a['id']} : notion absente {a['notion']}")
        probs += [f"{a['id']} : source absente {x['source']}" for x in a['preuves'] if x['source'] not in srcs]
    isolees = [no for no in notions(R) if not voisins(R, no)]
    if any(perdus.values()):
        print('OUBLI DÉTECTÉ (à restaurer depuis git avant toute autre chose) :', {k: v for k, v in perdus.items() if v}); sys.exit(1)
    if probs: print('Incohérences :\n  ' + '\n  '.join(probs)); sys.exit(1)
    json.dump(dict(now, verifie_le=aujourd()), open(p, 'w'), ensure_ascii=False)
    print(f"OK : rien d'oublié ({len(now['sources'])} sources, {len(now['affirmations'])} affirmations, {len(now['notions'])} notions, {len(now['liens'])} liens)")
    if len(isolees) > 0 and len(notions(R)) > 1: print(f"notions sans lien (à relier à ce qu'on sait) : {', '.join(isolees)}")


def cmd_etat(R):
    srcs = lire(R, 'sources.jsonl'); affs = lire(R, 'affirmations.jsonl'); ss = lire(R, 'seances.jsonl')
    print(f"{len(srcs)} sources ({sum(s.get('origine') == 'zak' for s in srcs)} de Zak) · {len(affs)} affirmations · "
          f"{len(notions(R))} notions · {len(lire(R, 'liens.jsonl'))} liens · {len(ss)} séances")
    for niv in reversed(NIVEAUX): print(f"  {niv:11} {sum(a['niveau'] == niv for a in affs)}")
    print('séance du jour :', 'faite' if any(s.get('date') == aujourd() for s in ss) else 'PAS ENCORE FAITE')
    sem = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    print(f"7 derniers jours : {sum(s.get('ajoute', '') >= sem for s in srcs)} sources, {sum(a.get('cree', '') >= sem for a in affs)} affirmations nouvelles")


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    cmd, R = a[0], os.path.abspath(a[1]); r = a[2:]
    def opt(n, d=None): return r[r.index(n) + 1] if n in r else d
    if cmd == 'etat': cmd_etat(R)
    elif cmd == 'aujourdhui': cmd_aujourdhui(R)
    elif cmd == 'source': cmd_source(R, r[0])
    elif cmd == 'notion': cmd_notion(R, r[0], r[1], opt('--definition'))
    elif cmd == 'affirmer': cmd_affirmer(R, r[0])
    elif cmd == 'lier': cmd_lier(R, r[0], r[1], r[2], r[3] if len(r) > 3 else '')
    elif cmd == 'chercher': cmd_chercher(R, r[0], int(opt('--n', 8)))
    elif cmd == 'rappel': cmd_rappel(R, int(opt('--n', 3)))
    elif cmd == 'revu': cmd_revu(R, r[0], r[1] if len(r) > 1 else '')
    elif cmd == 'seance': cmd_seance(R, r[0])
    elif cmd == 'carte': cmd_carte(R)
    elif cmd == 'verifier': cmd_verifier(R)
    else: sys.exit(__doc__)
