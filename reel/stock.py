"""Images de banque libres de droits (Pexels) pour les plans que Zak n'a pas filmés.

NON TESTÉ dans l'environnement actuel : le réseau de l'environnement cloud bloque api.pexels.com et videos.pexels.com.
Pour l'activer : autoriser ces deux domaines (et images.pexels.com) dans les réglages réseau de l'environnement, et
ajouter la variable d'environnement PEXELS_API_KEY (clé gratuite sur pexels.com/api).

Usage :
  python3 reel/stock.py chercher "mains qui servent un café" [--photo] [--n 6]   résultats + liens d'aperçu
  python3 reel/stock.py prendre <id> sorties/<id>/ [--photo]                     télécharge en ≥ 1080 px de large
Chaque fichier pris est noté dans sorties/<id>/credits.json (source, auteur, licence) : la licence Pexels autorise
l'usage commercial sans attribution, mais pas de montrer une personne ou une marque identifiable comme si elle
recommandait Brooze. Préférer les plans sans visage, sans logo.
"""
import sys, os, json, urllib.request, urllib.parse

CLE = os.environ.get('PEXELS_API_KEY')


def api(url):
    if not CLE: sys.exit('PEXELS_API_KEY absente : banque d\'images désactivée (voir l\'en-tête de reel/stock.py).')
    req = urllib.request.Request(url, headers={'Authorization': CLE, 'User-Agent': 'brooze-agent'})
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)


def chercher(q, photo=False, n=6):
    base = 'https://api.pexels.com/v1/search' if photo else 'https://api.pexels.com/videos/search'
    d = api(f"{base}?{urllib.parse.urlencode(dict(query=q, orientation='portrait', per_page=n, locale='fr-FR'))}")
    for x in d.get('photos' if photo else 'videos', []):
        if photo: print(f"{x['id']} · {x['width']}×{x['height']} · {x['photographer']} · {x['src']['medium']}")
        else: print(f"{x['id']} · {x['width']}×{x['height']} · {x['duration']} s · {x['user']['name']} · aperçu {x['image']}")


def prendre(iid, dossier, photo=False):
    os.makedirs(dossier, exist_ok=True)
    if photo:
        x = api(f'https://api.pexels.com/v1/photos/{iid}'); url = x['src']['original']; auteur = x['photographer']; ext = '.jpg'
    else:
        x = api(f'https://api.pexels.com/videos/videos/{iid}'); auteur = x['user']['name']; ext = '.mp4'
        fichiers = sorted([f for f in x['video_files'] if (f.get('width') or 0) >= 1080], key=lambda f: f['width'])
        url = (fichiers or x['video_files'])[0]['link']
    dest = os.path.join(dossier, f'stock_{iid}{ext}')
    urllib.request.urlretrieve(url, dest)
    p = os.path.join(dossier, 'credits.json'); cr = json.load(open(p)) if os.path.exists(p) else []
    cr.append(dict(fichier=os.path.basename(dest), source=f'pexels:{iid}', auteur=auteur, licence='Pexels License', url=x.get('url')))
    json.dump(cr, open(p, 'w'), ensure_ascii=False, indent=1); print(dest)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    photo = '--photo' in a; n = int(a[a.index('--n') + 1]) if '--n' in a else 6
    if a[0] == 'chercher': chercher(a[1], photo, n)
    elif a[0] == 'prendre': prendre(a[1], a[2], photo)
    else: sys.exit(__doc__)
