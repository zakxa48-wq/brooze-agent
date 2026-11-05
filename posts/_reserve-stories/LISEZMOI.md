# Réserve de stories (filet de sécurité : jamais un jour sans story)

Des stories **intemporelles, déjà rendues et contrôlées** (note ≥ 8 sur tous les critères d'AGENT.md § 7), prêtes à
partir n'importe quel jour. Une story = un dossier `R-NNN-<slug>/` (post.json, 01.png, éventuellement 02.png) poussé
sur main (URL raw en 200). `reserve.json` tient l'état : `[{id, angle, pilier, role, cree_le, utilisee_le: null}]`.

- **Niveau** : au moins **7** stories disponibles (une semaine entière). En dessous de 4 : on la remplit à la
  prochaine exécution, avant toute autre production.
- **Intemporelle** : aucune date, aucun « cette semaine », aucune référence à un post récent ; sources inépuisables
  et vraies : citations exactes de la banque de voix (marquées comme telles), méthode Brooze, coulisses, principes du
  cerveau (règles de montage, d'attention), questions directes à la cible, mini-exercices (« filme ça ce soir »).
- **Pas de doublon** : un angle de la réserve n'est pas déjà dans `idees.md` sur les 4 dernières semaines ; quand une
  story de réserve part, son angle entre dans `idees.md`.
- **Utilisation** : la plus ancienne disponible dont l'angle n'a pas été vu depuis 4 semaines et qui équilibre
  attirer / prouver / convertir (`data/cerveau/marketing.md`).

## Depuis le 02/11
Les nouvelles stories de réserve suivent `LIGNE_EDITORIALE.md` § 3 : une vraie chose apprise ou un vrai jeu (quiz, vrai ou faux, illusion expliquée, mini-expérience, histoire inventée annoncée comme telle), une émotion nommée dans `post.json`, reliée à Brooze en une ligne.

## 05/11 : réserve de l'ancien cap retirée
Décision de Zak : plus aucune story de l'ancien cap ne part (celles qui étaient programmées du 06 au 08/11 sont passées
en brouillon dans Metricool). Les stories de réserve non utilisées sont marquées `retiree_le` dans `reserve.json` et ne
se programment plus jamais. La réserve se reconstruit **uniquement** avec des stories du nouveau cap
(`LIGNE_EDITORIALE.md` § 3), chacune contrôlée (note ≥ 8, émotion ressentie). Tant qu'elle est vide, un jour sans story
est normal : on ne bouche jamais un trou avec l'ancien style.
