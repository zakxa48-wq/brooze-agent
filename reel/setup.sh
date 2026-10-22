#!/usr/bin/env bash
# Prépare une session pour fabriquer des Reels : dépendances, modèles locaux, outils du skill brooze-direction.
# Idempotent : relançable sans risque. Usage : bash reel/setup.sh
set -euo pipefail
ici="$(cd "$(dirname "$0")" && pwd)"
cache="$HOME/.cache/brooze"
mkdir -p "$cache"

pip install --break-system-packages -q sherpa-onnx soundfile scipy pyloudnorm pillow numpy 2>&1 | grep -v -i warning || true
(cd "$ici/.." && npm install --silent >/dev/null)

# Whisper small multilingue (ONNX int8), transcription 100 % locale. Hébergé sur GitHub (HuggingFace est bloqué ici).
if [ ! -f "$cache/sherpa-onnx-whisper-small/small-encoder.int8.onnx" ]; then
  curl -sL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 \
    | tar xj -C "$cache"
  rm -f "$cache"/sherpa-onnx-whisper-small/small-{encoder,decoder}.onnx   # seules les versions int8 servent
fi

# Outils du skill brooze-direction (calage des mots, son, glitchs) : on les trouve sur place, on ne les copie pas
# dans ce dépôt public.
outils="$ici/.outils"
if [ ! -f "$outils/son_brooze.py" ]; then
  src="$( (find / -path '*brooze-direction/scripts/son_brooze.py' -not -path '/proc/*' 2>/dev/null || true) | head -1)"
  [ -n "$src" ] || { echo "ERREUR : skill brooze-direction introuvable (scripts/son_brooze.py)"; exit 1; }
  mkdir -p "$outils"
  for f in mots.py attaques.py son_brooze.py glitchs.py; do ln -sf "$(dirname "$src")/$f" "$outils/$f"; done
fi
echo "OK : modèles dans $cache, outils dans $outils"
