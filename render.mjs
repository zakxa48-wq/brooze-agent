// Rend un post Brooze (carrousel ou story) en PNG + une planche de contrôle.
// Usage : node render.mjs posts/<id>/post.json
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ici = path.dirname(fileURLToPath(import.meta.url));
const fichier = process.argv[2];
if (!fichier) { console.error('Usage : node render.mjs posts/<id>/post.json'); process.exit(1); }
const post = JSON.parse(fs.readFileSync(fichier, 'utf8'));
const dossier = path.dirname(path.resolve(fichier));
const format = post.type === 'story' ? 'story' : 'carrousel';
const H = format === 'story' ? 1920 : 1350;

// Contrôles de charte avant rendu
const erreurs = [];
post.slides.forEach((s, i) => {
  const tout = JSON.stringify(s).replace(/\*\*.+?\*\*/g, '');
  const cuivres = (tout.match(/\*[^*]+?\*/g) || []).length;
  if (cuivres > 1) erreurs.push(`diapo ${i + 1} : ${cuivres} accents cuivre (1 maximum)`);
  if (/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u.test(tout)) erreurs.push(`diapo ${i + 1} : emoji interdit à l'image`);
});
if (format === 'carrousel' && (post.slides.length < 2 || post.slides.length > 10)) erreurs.push('un carrousel a 2 à 10 diapos');
if (erreurs.length) { console.error('Charte non respectée :\n- ' + erreurs.join('\n- ')); process.exit(2); }

const navigateur = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await navigateur.newPage({ viewport: { width: 1080, height: H }, deviceScaleFactor: 1 });
const sorties = [];
const alertes = [];

for (const [i, s] of post.slides.entries()) {
  // Vrai logo seulement s'il a été déposé dans assets/ : jamais d'imitation en ligne
  const logo = ['logo.svg', 'logo.png'].map(f => path.join(ici, 'assets', f)).find(f => fs.existsSync(f));
  const slide = { format, logo: logo ? pathToFileURL(logo).href : null, compteur: format === 'carrousel' ? `${String(i + 1).padStart(2, '0')}/${String(post.slides.length).padStart(2, '0')}` : '', ...s };
  // Fichier temporaire à côté du gabarit pour que les polices se chargent en chemin relatif
  const gabarit = fs.readFileSync(path.join(ici, 'templates/slide.html'), 'utf8')
    .replace('<div id="racine"></div>', `<div id="racine"></div><script>window.SLIDE = ${JSON.stringify(slide).replace(/</g, '\\u003c')};</script>`);
  const tmp = path.join(ici, 'templates/_rendu.html');
  fs.writeFileSync(tmp, gabarit);
  await page.goto(pathToFileURL(tmp).href);
  await page.evaluate(() => document.fonts.ready);

  // Débordements : un élément de texte qui sort de la zone utile
  const debords = await page.evaluate(() => {
    const m = document.querySelector('.marge').getBoundingClientRect();
    return [...document.querySelectorAll('.marge *')]
      .filter(e => e.children.length === 0 && e.textContent.trim())
      .filter(e => { const r = e.getBoundingClientRect(); return r.bottom > m.bottom + 1 || r.right > m.right + 1 || r.top < m.top - 1; })
      .map(e => e.textContent.trim().slice(0, 40));
  });
  if (debords.length) alertes.push(`diapo ${i + 1} déborde : ${debords.join(' | ')}`);

  const sortie = path.join(dossier, `${String(i + 1).padStart(2, '0')}.png`);
  await page.screenshot({ path: sortie });
  sorties.push(sortie);
}

// Planche de contrôle : toutes les diapos côte à côte, plus la vignette 3:4 de la grille pour la 1re
const vignettes = sorties.map(f => `<img src="${pathToFileURL(f).href}">`).join('');
await page.setViewportSize({ width: 1600, height: 900 });
await page.setContent(`<body style="margin:0;background:#2b2a28;display:flex;flex-wrap:wrap;gap:16px;padding:16px">
  <style>img{height:${format === 'story' ? 520 : 400}px}</style>${vignettes}</body>`);
await page.waitForTimeout(300);
await page.screenshot({ path: path.join(dossier, 'planche.png'), fullPage: true });
await navigateur.close();

console.log(JSON.stringify({ images: sorties, planche: path.join(dossier, 'planche.png'), alertes }, null, 2));
if (alertes.length) process.exit(3);
