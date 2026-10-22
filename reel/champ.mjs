// Rend le champ de cartes (reel/creations/champ.html) en vidéo 1080×1920 30 i/s, par morceaux reprenables.
// Usage : node reel/champ.mjs <dossier sortie> <env.json> [--t0 0] [--t1 48.3] [--test 12.5,40.5,...]
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const ici = path.dirname(fileURLToPath(import.meta.url));
const [dossier, envf, ...o] = process.argv.slice(2);
const opt = (n, d) => { const i = o.indexOf(n); return i < 0 ? d : o[i + 1]; };
const env = JSON.parse(fs.readFileSync(envf, 'utf8'));
const params = JSON.parse(opt('--params', '{}'));
const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--allow-file-access-from-files', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await nav.newPage({ viewport: { width: 1080, height: 1920 } });
await page.addInitScript(p => { window.CHAMP = p; }, { ...params, env });
page.on('pageerror', e => console.error('ERR', e.message));
await page.goto('file://' + path.join(ici, 'creations/champ.html'));
await page.waitForFunction(() => window.pret, null, { timeout: 60000 });
fs.mkdirSync(dossier, { recursive: true });
const test = opt('--test', null);
if (test) { for (const t of test.split(',').map(Number)) { await page.evaluate(t => window.renderAt(t), t); await page.screenshot({ path: path.join(dossier, `test_${t.toFixed(1)}.jpg`), type: 'jpeg', quality: 90 }); } await nav.close(); process.exit(0); }
const t0 = +opt('--t0', 0), t1 = +opt('--t1', 48.3), fps = 30;
const sortie = path.join(dossier, `champ_${t0}_${t1}.mp4`);
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', sortie], { stdio: ['pipe', 'inherit', 'inherit'] });
const debut = Date.now();
for (let f = Math.round(t0 * fps); f < Math.round(t1 * fps); f++) {
  await page.evaluate(t => window.renderAt(t), f / fps);
  const ok = ff.stdin.write(await page.screenshot({ type: 'jpeg', quality: 95 })); if (!ok) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 60 === 0) console.error('t', (f / fps).toFixed(1), Math.round((Date.now() - debut) / 1000) + 's');
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await nav.close(); console.log('OK', sortie);
