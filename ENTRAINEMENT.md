# Séances d'entraînement coachées

Zak (ou une session qu'il mandate, le **coach**) peut demander une séance : un exercice de motion design très court
(≈ 3 s) sur UN savoir-faire précis. L'agent (l'**élève**) fait des essais ; **seul le coach valide**. Rien n'est publié.

Ce que « apprendre » veut dire ici, honnêtement : l'agent ne change pas de modèle. Ce qu'il retient, c'est ce qui est
écrit dans sa mémoire à la fin de la séance : une technique validée (code + démo + réglages) dans la bibliothèque,
des règles tirées de ses erreurs dans `principes.md`, et un contrôle automatique si l'erreur peut se mesurer. C'est ce
qui fait qu'il ne refera pas la même erreur la séance suivante, comme un carnet de travail très bien tenu.

## Déroulé
Dossier de séance : `brooze-voix/data/cerveau/entrainement/<AAAA-MM-JJ>-<savoir-faire>/`
1. `consigne.md` (écrit par le coach) : le savoir-faire visé, le contenu imposé, les **critères chiffrés** et les
   critères à l'œil.
2. L'élève lit sa mémoire d'abord (`cerveau.py chercher`, `techniques.py liste`, `principes.md`) et note dans
   `essai-1/notes.md` ce qu'il en applique. Puis il fabrique **en code, de façon déterministe** (même `t` = même image).
3. Pour chaque essai N, dans `essai-N/` : `essai.mp4` (1080×1920, 30 i/s, ≈ 3 s ; on le versionne, c'est court),
   `planche.jpg` (une image toutes les 0,1 s pendant le geste, puis la tenue), `courbe.json` + `courbe.png`
   (`python3 reel/courbe.py essai.mp4 --graphique courbe.png`), `notes.md` (ce qu'il a changé depuis l'essai
   précédent et pourquoi), le code source (`source/`). L'Atelier (`reel/atelier`) est le choix par défaut pour ces
   exercices courts ; s'il lui manque une fonction, l'ajouter fait partie de l'exercice (démo, tests, VERSIONS.md). Il pousse sur main et **attend** le verdict.
4. Le coach écrit `essai-N/verdict.md` : critère par critère (chiffre mesuré → OK / à reprendre), ce qu'il voit à
   l'œil, et l'**ordre de correction** précis. Verdict : `VALIDÉ` ou `À REPRENDRE`.
5. À chaque essai repris, l'élève ne corrige QUE ce que le verdict demande (un essai = une hypothèse), et explique.
6. **Après VALIDÉ** (et seulement là), l'élève range ce qu'il a appris :
   - si le geste se généralise : une fonction dans `reel/atelier/gestes.py` (valeurs animées, pas de visuel) + sa
     démo dans `reel/atelier/demos/` + `tests.py --complet` ;
   - `techniques.py ajouter` : la technique validée (démo = l'essai validé en 540 px, code dans
     `reel/techniques/code/<id>/`, réglages exacts, note donnée par le coach) ;
   - `principes.md` : une règle par erreur corrigée pendant la séance (type `pratique`, preuve = essais et chiffres,
     confiance moyenne tant qu'elle n'a pas servi dans un vrai Reel) ;
   - `reel/controles/` : un contrôle automatique si l'erreur se mesure ;
   - `cerveau.py pratique` avec `"exercice"`, le nombre d'essais et les défauts de chaque essai ;
   - `bilan.md` de la séance : essais, ce qui a changé entre chacun, ce qui est maintenant en mémoire (liens).
7. Une séance qui n'aboutit pas après 5 essais s'arrête : bilan honnête de ce qui bloque, rien n'entre dans la
   bibliothèque, l'erreur devient une piste de travail.
