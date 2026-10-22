"""Bibliothèque de techniques maison (reel/techniques/techniques.json) : chacune testée, avec une démo rendue et une note.

  python3 reel/techniques.py liste [--toutes]          techniques actives (ou aussi retirées), meilleure note d'abord
  python3 reel/techniques.py ajouter '<json>'          nouvelle technique : id, nom, categorie, note (1–10), note_pourquoi,
                                                       demo (reel/techniques/demos/<id>.mp4, 2–3 s, 540 px), code, reglages, cout
  python3 reel/techniques.py utilisee <id> <reel> [--note N]     employée dans un Reel (la note suit le meilleur rendu)
  python3 reel/techniques.py decue <id> "<pourquoi>" [--reel id]  déception ; à la DEUXIÈME, la technique est retirée
Règles : une technique nouvelle par Reel ; pas de démo = pas dans la bibliothèque ; retirée = jamais réutilisée sans
nouvelle démo meilleure que l'ancienne.
"""
import sys, os, json, datetime
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'techniques', 'techniques.json')
charger = lambda: json.load(open(F)) if os.path.exists(F) else []
def sauver(T): json.dump(T, open(F, 'w'), ensure_ascii=False, indent=1)
a = sys.argv[1:]
if not a: sys.exit(__doc__)
T = charger(); auj = str(datetime.date.today())
trouver = lambda i: next((t for t in T if t['id'] == i), None) or sys.exit(f'technique inconnue : {i}')
if a[0] == 'liste':
    for t in sorted(T, key=lambda t: -(t.get('note') or 0)):
        if t['statut'] != 'active' and '--toutes' not in a: continue
        print(f"{t['note']:>4} · {t['statut']:7} · {t['categorie']:20} · {t['id']} — {t['nom']} ({len(t.get('apparu_dans', []))} Reels, "
              f"{len(t.get('deceptions', []))} déception(s))" + (f" · RETIRÉE : {t.get('retiree_pourquoi')}" if t['statut'] != 'active' else ''))
elif a[0] == 'ajouter':
    t = json.loads(a[1]); assert t.get('demo') and os.path.exists(os.path.join(os.path.dirname(F), t['demo'])), 'démo rendue obligatoire'
    t.setdefault('statut', 'active'); t.setdefault('apparu_dans', []); t.setdefault('deceptions', []); t.setdefault('cree_le', auj)
    T = [x for x in T if x['id'] != t['id']] + [t]; sauver(T); print('ajoutée :', t['id'])
elif a[0] == 'utilisee':
    t = trouver(a[1]); t.setdefault('apparu_dans', []).append(a[2])
    if '--note' in a: t['note'] = float(a[a.index('--note') + 1])
    sauver(T); print('noté')
elif a[0] == 'decue':
    t = trouver(a[1]); t.setdefault('deceptions', []).append(dict(date=auj, pourquoi=a[2], reel=a[a.index('--reel') + 1] if '--reel' in a else None))
    if len(t['deceptions']) >= 2:
        t['statut'] = 'retiree'; t['retiree_le'] = auj; t['retiree_pourquoi'] = ' / '.join(d['pourquoi'] for d in t['deceptions'])
        print(f"RETIRÉE (2 déceptions) : {t['id']} — note la raison dans principes.md")
    sauver(T)
else: sys.exit(__doc__)
