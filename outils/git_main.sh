#!/usr/bin/env bash
# Toujours travailler et pousser sur main, quelle que soit la branche de sortie de la session (claude/…).
# Les liens raw des vidéos (Metricool) et la mémoire entre exécutions (journal, catalogue, état des rendus) n'existent
# que sur main : un commit poussé ailleurs est perdu pour la suite.
#   bash outils/git_main.sh debut <dépôt>              au début : se placer sur main à jour (jamais sur claude/…)
#   bash outils/git_main.sh fin <dépôt> "message"      commit + push sur main, avec reprise et VÉRIFICATION
set -uo pipefail
action="$1"; depot="$(cd "$2" && pwd)"; message="${3:-Mise à jour}"
cd "$depot"
git config user.name >/dev/null || git config user.name "Agent Brooze"
git config user.email >/dev/null || git config user.email "agent@broozeproduction.fr"
# certaines sessions clonent sans la branche main dans les références suivies
git config --get-all remote.origin.fetch | grep -q 'refs/heads/\*' || git config --add remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
recuperer() { for d in 2 4 8 16 0; do git fetch -q origin main && return 0; [ "$d" = 0 ] && return 1; sleep "$d"; done; }

if [ "$action" = debut ]; then
  recuperer || { echo "ÉCHEC : impossible de récupérer origin/main"; exit 1; }
  if [ -n "$(git status --porcelain)" ]; then git stash -q -u; garde=1; else garde=0; fi
  git checkout -q -B main origin/main && git branch -q --set-upstream-to=origin/main main
  [ "$garde" = 1 ] && { git stash pop -q || echo "ATTENTION : conflit au retour des fichiers locaux (git stash list)"; }
  echo "OK : $(basename "$depot") sur main @ $(git rev-parse --short HEAD)"; exit 0
fi

[ "$action" = fin ] || { sed -n 2,7p "$0"; exit 2; }
# garde-fou : jamais d'audio dans le dépôt public
if [ "$(basename "$depot")" = brooze-agent ]; then
  git add -A
  audio="$(git diff --cached --name-only | grep -Ei '\.(wav|flac|m4a|mp3|aac|ogg|opus)$' || true)"
  [ -n "$audio" ] && { echo "REFUS : audio dans brooze-agent (public) :"; echo "$audio"; git reset -q; exit 3; }
else
  git add -A
fi
git diff --cached --quiet || git commit -q -m "$message" || { echo "ÉCHEC du commit"; exit 1; }
[ "$(git rev-parse --abbrev-ref HEAD)" = main ] || echo "ATTENTION : branche locale $(git rev-parse --abbrev-ref HEAD), poussée quand même sur main"
for d in 2 4 8 16 0; do
  recuperer && git rebase -q origin/main 2>/dev/null || { git rebase --abort 2>/dev/null; echo "ÉCHEC : conflit avec origin/main, résoudre puis relancer"; exit 1; }
  git push -q origin HEAD:main 2>&1 && break
  [ "$d" = 0 ] && { echo "ÉCHEC du push sur main"; exit 1; }; sleep "$d"
done
distant="$(git ls-remote origin refs/heads/main | cut -f1)"
[ "$distant" = "$(git rev-parse HEAD)" ] || { echo "ÉCHEC : main distant ($distant) ≠ HEAD local"; exit 1; }
echo "OK : poussé sur main @ ${distant:0:7}"
