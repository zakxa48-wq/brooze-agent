#!/usr/bin/env bash
# Prépare une session pour fabriquer des Reels : dépendances, modèles locaux, outils du skill brooze-direction.
# Idempotent : relançable sans risque. Usage : bash reel/setup.sh
set -euo pipefail
ici="$(cd "$(dirname "$0")" && pwd)"
cache="$HOME/.cache/brooze"
mkdir -p "$cache"

# Bibliothèques système de Manim (cairo, pango) : seulement si absentes
# + Tesseract (lecture du texte à l'écran des vidéos analysées par le cerveau) et pdftotext
manque=""
pkg-config --exists pangocairo 2>/dev/null || manque="$manque libpango1.0-dev libcairo2-dev pkg-config"
command -v tesseract >/dev/null && tesseract --list-langs 2>/dev/null | grep -q fra || manque="$manque tesseract-ocr tesseract-ocr-fra"
command -v pdftotext >/dev/null || manque="$manque poppler-utils"
if [ -n "$manque" ]; then
  (apt-get update -qq && apt-get install -y -qq $manque) >/dev/null 2>&1 || echo "apt indisponible : $manque absents"
fi
# python3 -m pip : installe pour le python3 du PATH (le « pip » nu peut viser un autre Python).
# setuptools de Debian casse la compilation de certains paquets (« install_layout ») : on en installe un récent à côté.
python3 -c "import manim" 2>/dev/null || python3 -m pip install --break-system-packages -q --ignore-installed setuptools wheel 2>&1 | grep -i error || true
python3 -m pip install --break-system-packages -q sherpa-onnx soundfile scipy pyloudnorm pillow numpy matplotlib opensimplex manim 2>&1 | grep -v -i warning || true
python3 -c "import cv2" 2>/dev/null || python3 -m pip install --break-system-packages -q opencv-python-headless 2>&1 | grep -i error || true
command -v yt-dlp >/dev/null || python3 -m pip install --break-system-packages -q yt-dlp trafilatura 2>&1 | grep -i error || true   # savoir : sous-titres YouTube, texte des pages (si le réseau les ouvre)
# three.js, p5, Remotion (+ React), simplex-noise, playwright-core : versions figées dans package.json
(cd "$ici/.." && npm install --silent >/dev/null)

# Polices variables libres (OFL, dépôt GitHub google/fonts) pour la typographie animée
pol="$cache/polices"; mkdir -p "$pol"
for f in "ofl/inter/Inter%5Bopsz,wght%5D.ttf" "ofl/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf" \
         "ofl/recursive/Recursive%5BCASL,CRSV,MONO,slnt,wght%5D.ttf" "ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf" \
         "ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf" "ofl/instrumentserif/InstrumentSerif-Regular.ttf" \
         "ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"; do
  n="$(basename "$f" | sed 's/%5B.*//;s/-Regular//;s/\.ttf//')"
  [ -s "$pol/$n.ttf" ] || curl -sfL "https://raw.githubusercontent.com/google/fonts/main/$f" -o "$pol/$n.ttf" || echo "police $n indisponible"
done

# Whisper small multilingue (ONNX int8), transcription 100 % locale. Hébergé sur GitHub (HuggingFace est bloqué ici).
if [ ! -f "$cache/sherpa-onnx-whisper-small/small-encoder.int8.onnx" ]; then
  curl -sL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 \
    | tar xj -C "$cache"
  rm -f "$cache"/sherpa-onnx-whisper-small/small-{encoder,decoder}.onnx   # seules les versions int8 servent
fi

# Whisper medium (int8, ~1 Go une fois décompressé) : plus juste sur les petits mots (tu/je, de/le), utilisé en priorité
if [ ! -f "$cache/sherpa-onnx-whisper-medium/medium-encoder.int8.onnx" ]; then
  curl -sL https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-medium.tar.bz2 \
    | tar xj -C "$cache" && rm -f "$cache"/sherpa-onnx-whisper-medium/medium-{encoder,decoder}.onnx || echo "Whisper medium indisponible : small utilisé"
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
python3 -c "import manim" 2>/dev/null && m=manim || m="SANS manim"
echo "OK : modèles et polices dans $cache, outils dans $outils, $m, three.js/Remotion/p5 dans node_modules"
