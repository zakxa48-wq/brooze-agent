import { chromium } from '/home/user/brooze-agent/node_modules/playwright-core/index.mjs';
import path from 'node:path';
const ici = path.dirname(new URL(import.meta.url).pathname);
const [w, h, ...ls] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--allow-file-access-from-files'] });
for (const l of ls) {
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  p.on('console', m => console.log(l, m.text())); p.on('pageerror', e => console.log(l, 'ERR', e.message));
  await p.goto(`file://${ici}/scene.html?l=${l}&w=${w}&h=${h}`);
  await p.waitForFunction('window.FINI === true', null, { timeout: 120000 });
  await p.locator('canvas').screenshot({ path: `${ici}/${l}_${w}x${h}.png` });
  console.log('ok', l);
}
await b.close();
