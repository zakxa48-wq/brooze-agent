"""Planche : une image toutes les 0,1 s pendant le geste (0–0,8 s), puis la tenue (1,2 · 2,0 · 2,9 s)."""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
f, sortie = sys.argv[1], sys.argv[2]
temps = [round(.1 * i, 1) for i in range(9)] + [1.2, 2.0, 2.9]
w, h = 270, 480
r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3)
pl = Image.new('RGB', (6 * w + 7 * 8, 2 * (h + 30) + 3 * 8), (40, 40, 40)); d = ImageDraw.Draw(pl)
police = ImageFont.truetype('/root/.cache/brooze/polices/Inter.ttf', 20)
for i, t in enumerate(temps):
    x, y = 8 + (i % 6) * (w + 8), 8 + (i // 6) * (h + 38)
    pl.paste(Image.fromarray(fr[min(len(fr) - 1, int(round(t * 30)))]), (x, y + 30)); d.text((x, y + 4), f'{t:.1f} s', fill=(230, 230, 230), font=police)
pl.save(sortie, quality=90)
