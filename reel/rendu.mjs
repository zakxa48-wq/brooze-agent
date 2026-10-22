// Rend un Reel Brooze image par image (moteur.html) puis encode en H.264 + AAC.
// Usage :
//   node reel/rendu.mjs sorties/<id>/reel.json --controle 0.3,2.1,8   images de contrôle + planche, sans vidéo
//   node reel/rendu.mjs sorties/<id>/reel.json --brouillon             vidéo demi-définition, sans son, pour vérifier le mouvement
//   node reel/rendu.mjs sorties/<id>/reel.json                         final 1080×1920 avec mix.flac → reel.mp4
//   node reel/rendu.mjs sorties/<id>/reel.json --couverture            couverture.jpg (scène reel.couverture)
// reel.json : { fps, source: [t0, t1] (fenêtre de voix.wav), fin (durée après la voix), scenes: [...], couverture: {...} }
// Les temps des scènes sont relatifs au début du Reel ; "@12" = début du mot 12 moins 0,12 s, "@12>" = fin du mot 12.
import { chromium } from 'playwright-core';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ici = path.dirname(fileURLToPath(import.meta.url));
const [fichier, ...opts] = process.argv.slice(2);
if (!fichier) { console.error(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(0, 9).join('\n')); process.exit(1); }
const dossier = path.dirname(path.resolve(fichier));
const reel = JSON.parse(fs.readFileSync(fichier, 'utf8'));
const opt = n => { const i = opts.indexOf(n); return i < 0 ? null : (opts[i + 1] && !opts[i + 1].startsWith('--') ? opts[i + 1] : true); };
const fps = reel.fps ?? 30;

// Mots de la fenêtre, remis au temps du Reel
const tousMots = JSON.parse(fs.readFileSync(path.join(dossier, reel.mots ?? 'mots.json'), 'utf8'));
const [t0, t1] = reel.source ?? [0, tousMots.at(-1).end + .3];
const idx0 = tousMots.findIndex(m => m.start >= t0 - .02);
const mots = tousMots.filter(m => m.start >= t0 - .02 && m.end <= t1 + .05).map(m => ({ ...m, start: m.start - t0, end: m.end - t0 }));
const duree = +(t1 - t0 + (reel.fin ?? 0)).toFixed(3);
// "@i" → début du mot i (index dans mots.json d'origine) moins l'avance ; "@i>" → fin du mot
const temps = v => {
  if (typeof v !== 'string' || !v.startsWith('@')) return v;
  const fin = v.endsWith('>'), i = parseInt(v.slice(1)) - idx0;
  if (!mots[i]) throw new Error(`mot ${v} hors de la fenêtre source`);
  return +(fin ? mots[i].end : mots[i].start - .12).toFixed(3);
};
const resoudre = o => Array.isArray(o) ? o.map(resoudre) : o && typeof o === 'object'
  ? Object.fromEntries(Object.entries(o).map(([k, v]) => [k, ['mots', 'cuivre', 'raye'].includes(k) ? (Array.isArray(v) ? v.map(x => x - idx0) : v - idx0) : k === 'mot' ? v - idx0 : resoudre(v)]))
  : temps(o);
const scenes = resoudre(reel.scenes);

// Vidéos (rush de Zak, rendu 3D animé…) des scènes clip et plan : extraites en images au fps du Reel.
// plan.video accepte debut (s dans le rush), vitesse (0,5 = ralenti fondu), cadrage (0–1 : où recadrer en 9:16).
for (const [k, sc] of scenes.entries()) {
  if (!['clip', 'plan'].includes(sc.type) || !sc.video) continue;
  // durée utile = durée de la scène + la transition de sortie (le plan continue de vivre pendant qu'il part)
  const fin = scenes[k + 1]?.de ?? duree, debut = sc.debut ?? 0, vitesse = sc.vitesse ?? 1, cx = sc.cadrage ?? .5;
  const dureeScene = fin - sc.de + .8;
  const cle = `${path.basename(sc.video, path.extname(sc.video))}_${debut}_${vitesse}_${cx}`.replace(/[^\w.-]/g, '_');
  const dir = path.join(dossier, `_clip_${cle}`);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
    // ralenti : interpolation par fondu d'images (économique, sans saccade) ; recadrage 9:16 centré sur `cadrage`
    const ralenti = vitesse !== 1 ? `setpts=${(1 / vitesse).toFixed(4)}*PTS,minterpolate=fps=${fps}:mi_mode=blend,` : '';
    const vf = `${ralenti}fps=${fps},scale=-2:1920:force_original_aspect_ratio=increase,crop=1080:1920:(in_w-1080)*${cx}:0`;
    execFileSync('ffmpeg', ['-v', 'error', '-ss', String(debut), '-t', String(dureeScene * vitesse), '-i', path.resolve(dossier, sc.video),
      '-an', '-vf', vf, '-q:v', '2', path.join(dir, '%05d.jpg')]);
  }
  sc.dossier = pathToFileURL(dir).href; sc.n_images = fs.readdirSync(dir).length;
}
// Images (photos, rendus photoréalistes, calques détourés) : chemins relatifs au dossier du Reel
for (const sc of scenes.filter(s => s.type === 'plan')) {
  if (sc.image) sc.image = pathToFileURL(path.resolve(dossier, sc.image)).href;
  if (sc.profondeur) sc.profondeur = pathToFileURL(path.resolve(dossier, sc.profondeur)).href;
  for (const c of sc.calques ?? []) c.image = pathToFileURL(path.resolve(dossier, c.image)).href;
}
// Coups de zoom sur les mots forts : "@i" → attaque du mot i (1 image avant)
const punch = (reel.punch ?? []).map(v => typeof v === 'string' ? temps(v) + .12 - 1 / fps : v);

const navigateur = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--allow-file-access-from-files', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const echelle = opt('--brouillon') ? .5 : 1;
const page = await navigateur.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: echelle });
page.on('pageerror', e => { console.error('Erreur moteur :', e.message); process.exit(4); });
await page.goto(pathToFileURL(path.join(ici, 'moteur.html')).href);

if (opt('--couverture')) {
  const c = reel.couverture;
  await page.evaluate(d => window.init(d), { fps, duree: 1, mots: [], scenes: [{ type: 'couverture', de: 0, theme: c.theme ?? 'encre', poussee: 0, transition: 'coupe', ...c }], sansSousTitres: true });
  await page.evaluate(() => window.rendre(0));
  const sortie = path.join(dossier, 'couverture.jpg');
  await page.screenshot({ path: sortie, type: 'jpeg', quality: 95 });
  console.log(JSON.stringify({ couverture: sortie, audit: await page.evaluate(() => window.audit()) }));
  await navigateur.close(); process.exit(0);
}

await page.evaluate(d => window.init(d), { fps, duree, mots, scenes, punch, sansSousTitres: reel.sous_titres === false });

const audits = new Map();
const noter = (t, pb) => pb.forEach(p => { if (!audits.has(p)) audits.set(p, t.toFixed(2)); });

if (opt('--controle')) {
  const ts = String(opt('--controle')).split(',').map(Number);
  const out = path.join(dossier, 'images'); fs.mkdirSync(out, { recursive: true });
  const fichiers = [];
  for (const t of ts) {
    await page.evaluate(t => window.rendre(t), t); noter(t, await page.evaluate(() => window.audit()));
    const f = path.join(out, `t${t.toFixed(2)}.jpg`); await page.screenshot({ path: f, type: 'jpeg', quality: 90 }); fichiers.push(f);
  }
  await planche(fichiers, path.join(dossier, 'planche_controle.jpg'), ts);
  console.log(JSON.stringify({ planche: path.join(dossier, 'planche_controle.jpg'), audit: [...audits].map(([p, t]) => `${t}s ${p}`) }, null, 1));
  await navigateur.close(); process.exit(0);
}

// Vidéo : images JPEG envoyées à ffmpeg par un tube
const N = Math.round(duree * fps);
const brouillon = !!opt('--brouillon');
const sortie = path.join(dossier, brouillon ? 'brouillon.mp4' : 'reel.mp4');
const mix = path.join(dossier, 'mix.flac');
if (!brouillon && !fs.existsSync(mix)) { console.error('mix.flac absent : lancer d\'abord python3 reel/son.py'); process.exit(2); }
const args = ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-'];
if (!brouillon) args.push('-i', mix);
// Débit plafonné : le grain et la caméra à l'épaule sur des images détaillées font exploser un encodage à qualité
// constante (240 Mo pour 41 s). 14 Mb/s ≈ 75 Mo pour 45 s, au-dessus de ce qu'Instagram garde après recompression.
args.push('-c:v', 'libx264', '-preset', brouillon ? 'veryfast' : 'slow', '-crf', brouillon ? '23' : '18', '-maxrate', '14M', '-bufsize', '28M', '-pix_fmt', 'yuv420p',
  '-profile:v', 'high', '-r', String(fps), '-movflags', '+faststart');
if (!brouillon) args.push('-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-shortest');
args.push(sortie);
const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
const debut = Date.now();
for (let f = 0; f < N; f++) {
  const t = f / fps;
  await page.evaluate(t => window.rendre(t), t);
  if (f % 6 === 0) noter(t, await page.evaluate(() => window.audit()));
  const img = await page.screenshot({ type: 'jpeg', quality: brouillon ? 80 : 94 });
  if (!ff.stdin.write(img)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % (fps * 5) === 0) process.stderr.write(`  ${t.toFixed(0)} s / ${duree.toFixed(0)} s (${((Date.now() - debut) / 1000).toFixed(0)} s écoulées)\n`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await navigateur.close();
console.log(JSON.stringify({ video: sortie, images: N, duree, secondes_de_rendu: Math.round((Date.now() - debut) / 1000), audit: [...audits].map(([p, t]) => `${t}s ${p}`) }, null, 1));

async function planche(fichiers, dest, ts) {
  const p = await navigateur.newPage({ viewport: { width: 1800, height: 1000 } });
  const html = path.join(dossier, '_planche.html');
  fs.writeFileSync(html, `<body style="margin:0;background:#222;display:flex;flex-wrap:wrap;gap:12px;padding:12px;font:20px sans-serif;color:#ccc">${fichiers.map((f, i) => `<div><img src="${pathToFileURL(f).href}" style="height:560px;display:block"><div>${ts[i]} s</div></div>`).join('')}</body>`);
  await p.goto(pathToFileURL(html).href); await p.waitForTimeout(300);
  await p.screenshot({ path: dest, type: 'jpeg', quality: 85, fullPage: true }); fs.unlinkSync(html); await p.close();
}
