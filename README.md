# Agent marketing Brooze

Agent autonome qui crée et publie sur Instagram (@broozeproduction) 3 stories et 2 carrousels par semaine,
de l'idée à la mise en ligne, avec la charte Brooze.

- `AGENT.md` : les consignes suivies à chaque exécution.
- `render.mjs` + `templates/slide.html` : le moteur visuel (texte JSON → images à la charte).
- `journal.md` / `strategie.md` : la mémoire de l'agent, mise à jour à chaque post.
- `inbox/` : dépose ici photos, captures et notes (`notes.md`). L'agent les utilise en priorité.
- `inbox/audio/` : dépose un audio (+ un `.txt` facultatif : contexte, cible, idée) → l'agent en fait un Reel motion
  design et le programme seul (`AGENT_REEL.md`, chaîne `reel/`). Traité → `inbox/traite/`.
- **Banque de voix** (dépôt privé `zakxa48-wq/brooze-voix`) : `audio/` = ton stock d'enregistrements, l'agent y puise
  2 Reels par semaine avec ta vraie voix ; `urgent/` = à publier vite. Gérée par `reel/banque.py`.
- `assets/logo.png` ou `assets/logo.svg` : le vrai logo (absent = wordmark seul).
- Créer un fichier `PAUSE` à la racine arrête toute publication.

Rendu : `npm install && node render.mjs posts/<id>/post.json`

Reels : `bash reel/setup.sh`, puis `reel/comprendre.py` (nettoyage + Whisper local + calage), `reel/rendu.mjs`
(moteur `reel/moteur.html`), `reel/son.py` (sound design synthétisé), `reel/controle.py` (contrôle technique).
