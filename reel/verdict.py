"""Verdict de qualité d'un Reel : UNE décision claire, ses raisons et TOUTES les conditions pour passer.

Rassemble ce que disent les juges (controle.py, cerveau.py comparer, l'évaluation indépendante du sceptique) en un seul
document que l'agent peut exécuter, puis suit chaque condition d'une tentative à l'autre (levée / non levée).

  python3 reel/verdict.py evaluer sorties/<id>     → sorties/<id>/verdict_N.md + verdict_N.json (N = tentative)
  python3 reel/verdict.py etat    sorties/<id>     → dernière décision, conditions encore ouvertes, tentatives

Entrées lues dans sorties/<id>/ (produites juste avant, sur le MÊME rendu) :
  controle.json      controle.py (bloquants techniques et d'engagement, points à justifier)
  comparer.json      cerveau.py comparer (raisons mesurées ; bloquant seulement s'il est « probante »)
  evaluation_N.json  l'évaluation indépendante (brooze-sceptique, AGENT_REEL.md § 5) :
    {"defauts": [{"priorite": "P1|P2|P3", "de": 12.0, "a": 36.0, "quoi": "ce qui ne va pas",
                  "preuve": "image / mesure qui le montre", "condition": "ce qui doit être vrai pour que ce soit levé (vérifiable)",
                  "piste": "comment s'y prendre (facultatif)", "nouveau_pourquoi": "tentative ≥ 2 : régression | pas visible avant | P1"}],
     "conditions_precedentes": {"V1-3": {"statut": "levée|non levée", "pourquoi": "ce qui a été vérifié, avec le temps exact"}},
     "justifications": {"<point à justifier>": "acceptée|refusée : pourquoi"}}
  reel.json          champ "justifications" (raisons écrites par l'agent pour les points non bloquants)

Règles du juge (équitable, pas arbitraire) :
  - Bloque : un bloquant de controle.py, une raison de comparer « probante », un P1 ou un P2 du sceptique, une condition
    précédente non levée, un point à justifier sans justification acceptée. P3 = conseil, ne bloque jamais.
  - Chaque raison dit : ce qui est mesuré ou vu, où (temps), la preuve, ce qui est exigé, la condition de passage.
  - Tentative ≥ 2 : le juge vérifie d'abord chaque condition précédente. Un NOUVEAU défaut n'est recevable que s'il est
    P1, une régression causée par la correction, ou invisible avant (dire pourquoi) : pas d'exigence qui bouge à chaque
    tentative. Un défaut nouveau sans « nouveau_pourquoi » est rétrogradé en P3 (conseil).
"""
import sys, os, json, glob, re, datetime

MOTS_JUSTIF = {'relance': ['relance', 'rythme'], 'durée': ['duree', 'durée'], 'lecture': ['lecture', 'texte'], 'boucle': ['boucle', 'jonction'],
               'gros texte': ['gros_textes', 'gros texte', 'titres'], 'transition': ['transition'], 'images réelles': ['images', 'reelles', 'réelles'],
               'clins': ['clins'], 'cadence': ['cadence', 'rythme'], '3d': ['3d', 'plans_3d']}


def charger(p):
    try: return json.load(open(p))
    except Exception: return None

def tentatives(d): return sorted(int(re.findall(r'verdict_(\d+)\.json$', f)[0]) for f in glob.glob(os.path.join(d, 'verdict_*.json')))


def justification(point, reel):
    js = (reel or {}).get('justifications') or {}
    p = point.lower()
    for k, mots in MOTS_JUSTIF.items():
        if k in p:
            for jk, jv in js.items():
                if any(m in (jk + ' ' + str(jv)).lower() for m in mots): return f'{jk} : {jv}'
    return None


def evaluer(d):
    d = os.path.abspath(d); n = (tentatives(d) or [0])[-1] + 1
    prec = charger(os.path.join(d, f'verdict_{n - 1}.json')) if n > 1 else None
    ctl = charger(os.path.join(d, 'controle.json')); cmp_ = charger(os.path.join(d, 'comparer.json')); reel = charger(os.path.join(d, 'reel.json'))
    ev = charger(os.path.join(d, f'evaluation_{n}.json'))
    manque = [nom for nom, x in (('controle.json', ctl), (f'evaluation_{n}.json (évaluation indépendante du sceptique)', ev)) if x is None]
    if manque: sys.exit('Verdict impossible, il manque : ' + ', '.join(manque) + '. Un verdict se rend sur le rendu final, tous les juges passés.')
    raisons, k = [], 0
    def ajoute(**r):
        nonlocal k; k += 1; r['id'] = f'V{n}-{k}'; raisons.append(r)

    # 1. controle.py
    for p in (ctl.get('problemes') or []) + ((ctl.get('engagement') or {}).get('bloquants') or []):
        ajoute(source='controle.py', bloque=True, priorite='P1', quoi=p, ou='', preuve='controle.json', exige='aucun bloquant',
               condition=f'controle.py ne signale plus : « {p} »')
    for p in ctl.get('a_justifier') or []:
        j = justification(p, reel); avis = ((ev or {}).get('justifications') or {}).get(p, '')
        refusee = avis.lower().startswith('refus')
        if j and not refusee: continue
        m = re.search(r'(\d+\.?\d*)\s*[–-]\s*(\d+\.?\d*) s', p) or re.search(r'à (\d+\.?\d*) s', p)
        ou = (f'{m.group(1)}–{m.group(2)} s' if m.lastindex == 2 else f'{m.group(1)} s') if m else 'tout le Reel'
        ajoute(source='controle.py (à justifier)', bloque=True, priorite='P2', quoi=p, ou=ou, preuve='controle.json',
               exige='corrigé, ou justifié dans reel.json « justifications » et accepté par l\'évaluation',
               condition=('justification refusée : ' + avis) if refusee else f'corriger, ou écrire pourquoi ce Reel fait exception (reel.json → justifications)')
    # 2. comparer
    if cmp_:
        for r in cmp_.get('raisons') or []:
            ajoute(source='cerveau.py comparer', bloque=bool(cmp_.get('probante')), priorite='P2' if cmp_.get('probante') else 'P3',
                   quoi=r['quoi'], ou='', preuve=f"mesuré {r['mesure']} (références : {', '.join(cmp_.get('references') or [])})", exige=r['exige'],
                   condition=r['condition'] + ('' if cmp_.get('probante') else ' (indicatif : moins de 3 références de qualité ≥ 7)'))
    # 3. conditions précédentes
    suivi = {}
    for c in (prec or {}).get('raisons', []):
        if not c.get('bloque'): continue
        st = ((ev.get('conditions_precedentes') or {}).get(c['id']) or {})
        mesurable = c['source'].startswith('controle.py') or c['source'].startswith('cerveau.py')
        if mesurable:   # vérifié par la machine : levée si la même raison n'apparaît plus
            leve = not any(r['quoi'] == c['quoi'] for r in raisons)
            suivi[c['id']] = dict(statut='levée' if leve else 'non levée', pourquoi='vérifié par ' + c['source'], condition=c['condition'])
        else:
            statut = st.get('statut') or 'non vérifiée'
            suivi[c['id']] = dict(statut=statut, pourquoi=st.get('pourquoi', ''), condition=c['condition'])
            if statut != 'levée':
                ajoute(source='condition précédente', bloque=True, priorite=c['priorite'], quoi=c['quoi'], ou=c.get('ou', ''),
                       preuve=st.get('pourquoi') or 'l\'évaluation ne dit pas si elle est levée (la vérifier)', exige=c['exige'], condition=c['condition'], piste=c.get('piste', ''))
    # 4. évaluation indépendante
    for x in ev.get('defauts') or []:
        pr = x.get('priorite', 'P3').upper(); note = ''
        if n > 1 and pr in ('P2',) and not x.get('nouveau_pourquoi'):
            pr, note = 'P3', ' (nouveau sans justification : rétrogradé en conseil, règle du juge équitable)'
        ou = f"{x['de']:.1f}–{x['a']:.1f} s" if isinstance(x.get('de'), (int, float)) and isinstance(x.get('a'), (int, float)) else str(x.get('de', ''))
        if not x.get('condition'): sys.exit(f"défaut sans condition de passage : « {x.get('quoi')} ». Le juge doit dire ce qui le lèvera.")
        ajoute(source='évaluation indépendante' + note, bloque=pr in ('P1', 'P2'), priorite=pr, quoi=x['quoi'], ou=ou, preuve=x.get('preuve', ''),
               exige=x.get('exige', ''), condition=x['condition'], piste=x.get('piste', ''), nouveau=x.get('nouveau_pourquoi', ''))

    bloquantes = [r for r in raisons if r['bloque']]
    decision = 'PUBLIABLE' if not bloquantes else 'À REPRENDRE'
    progres = None
    if suivi: progres = sum(v['statut'] == 'levée' for v in suivi.values())
    out = dict(tentative=n, date=datetime.datetime.now().isoformat(timespec='minutes'), decision=decision, raisons=raisons, suivi=suivi, conditions_levees=progres)
    json.dump(out, open(os.path.join(d, f'verdict_{n}.json'), 'w'), ensure_ascii=False, indent=1)

    L = [f'# Verdict, tentative {n} : **{decision}**', '']
    if suivi:
        L += ['## Conditions de la tentative précédente', '']
        L += [f"- {cid} : **{v['statut']}** — {v['condition']}{' · ' + v['pourquoi'] if v['pourquoi'] else ''}" for cid, v in suivi.items()] + ['']
    if bloquantes:
        L += ['## Pourquoi ce n\'est pas publiable', '']
        for r in bloquantes:
            L += [f"### {r['id']} · {r['priorite']} · {r['quoi']}", f"- où : {r['ou'] or '—'} · source : {r['source']}", f"- preuve : {r['preuve'] or '—'}",
                  f"- exigé : {r['exige'] or '—'}", f"- **condition pour passer** : {r['condition']}"] + ([f"- piste : {r['piste']}"] if r.get('piste') else []) + ['']
        L += ['## Toutes les conditions à remplir pour la tentative suivante (et rien d\'autre ne sera exigé, sauf P1 ou régression)', '']
        L += [f"- [ ] {r['id']} : {r['condition']}" for r in bloquantes] + ['']
    conseils = [r for r in raisons if not r['bloque']]
    if conseils: L += ['## Conseils (ne bloquent pas)', ''] + [f"- {r['id']} : {r['quoi']} → {r['condition']}" for r in conseils] + ['']
    open(os.path.join(d, f'verdict_{n}.md'), 'w').write('\n'.join(L))
    print('\n'.join(L)); sys.exit(0 if decision == 'PUBLIABLE' else 1)


def etat(d):
    t = tentatives(d)
    if not t: print('aucun verdict'); return
    v = charger(os.path.join(d, f'verdict_{t[-1]}.json'))
    print(f"tentative {t[-1]} : {v['decision']}")
    for r in v['raisons']:
        if r['bloque']: print(f"  [ ] {r['id']} {r['condition']}")
    hist = [charger(os.path.join(d, f'verdict_{i}.json')) for i in t]
    print('levées par tentative :', [h.get('conditions_levees') for h in hist])


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    {'evaluer': evaluer, 'etat': etat}.get(sys.argv[1], lambda d: sys.exit(__doc__))(sys.argv[2])
