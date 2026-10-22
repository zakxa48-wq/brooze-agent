# Agent marketing Brooze

Agent autonome qui crée et publie sur Instagram (@broozeproduction) 3 stories et 2 carrousels par semaine,
de l'idée à la mise en ligne, avec la charte Brooze.

- `AGENT.md` : les consignes suivies à chaque exécution.
- `render.mjs` + `templates/slide.html` : le moteur visuel (texte JSON → images à la charte).
- `journal.md` / `strategie.md` : la mémoire de l'agent, mise à jour à chaque post.
- `inbox/` : dépose ici photos, captures et notes (`notes.md`). L'agent les utilise en priorité.
- `assets/logo.png` ou `assets/logo.svg` : le vrai logo (absent = wordmark seul).
- Créer un fichier `PAUSE` à la racine arrête toute publication.

Rendu : `npm install && node render.mjs posts/<id>/post.json`
