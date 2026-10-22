# Contrôles appris

Quand le même défaut revient deux fois dans `data/cerveau/pratique.jsonl` (`cerveau.py recurrents`), l'agent écrit
une règle dans `principes.md` ET un contrôle ici, pour qu'il ne revienne plus. `controle.py` les exécute tous.

Un fichier = un défaut : `reel/controles/<defaut>.py` avec
```python
def verifier(video, reel, mots, dossier):   # reel = reel.json chargé, mots = mots.json chargé
    return []                                # liste de problèmes, en français, avec le temps exact ; vide = OK
```
En tête du fichier : la règle (P-NNN de principes.md), les deux Reels où le défaut est apparu, la date.
Un contrôle qui bloque à tort deux fois est corrigé ou retiré (et noté dans principes.md).
