// Rend une composition Remotion (React) en vidéo, avec le Chromium local (sans compte, sans réseau).
// Usage : node reel/remotion.mjs <entree.jsx> <IdComposition> <sortie.mp4|sortie.png> [--image N] [--props '{"a":1}']
// La vidéo obtenue entre ensuite dans le Reel comme une scène `clip` ou un `plan` avec `video`.
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import path from 'node:path';
const [entree, id, sortie, ...o] = process.argv.slice(2);
if (!sortie) { console.error('Usage : node reel/remotion.mjs entree.jsx Id sortie.mp4 [--image N] [--props JSON]'); process.exit(1); }
const opt = n => { const i = o.indexOf(n); return i < 0 ? null : o[i + 1]; };
const serveUrl = await bundle({ entryPoint: path.resolve(entree) });
// Chromium « headless shell » de Playwright : le Chromium complet refuse l'ancien mode headless dont Remotion a besoin
const base = { serveUrl, id, inputProps: JSON.parse(opt('--props') ?? '{}'),
  browserExecutable: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', chromiumOptions: { gl: 'swiftshader' } };
const composition = await selectComposition(base);
if (sortie.endsWith('.png') || opt('--image')) await renderStill({ ...base, composition, output: sortie, frame: Number(opt('--image') ?? 0) });
else await renderMedia({ ...base, composition, codec: 'h264', crf: 16, outputLocation: sortie, concurrency: 2 });
console.log(JSON.stringify({ sortie, images: composition.durationInFrames, fps: composition.fps }));
