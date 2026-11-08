// Génère les post.json de la semaine du 09/11 (illusions : carrousel + stories). Usage : node outils/gen_semaine_0911.mjs
import fs from 'node:fs';
const E = '#100E0D', G = '#8A8780', C = '#C8834A', P = '#EDEBE7', K = '#F7F6F2';
const svg = (w, h, body) => `<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
// Müller-Lyer
const ml = (guides) => {
  const x0 = 224, x1 = 664, f = (x, y, d) => `<path d="M${x + d * 34} ${y - 34} L${x} ${y} L${x + d * 34} ${y + 34}" />`;
  return svg(888, 560, `<g stroke="${E}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M${x0} 180 H${x1}"/>${f(x0, 180, 1)}${f(x1, 180, -1)}
    <path d="M${x0} 390 H${x1}"/>${f(x0, 390, -1)}${f(x1, 390, 1)}</g>
    ${guides ? `<g stroke="${C}" stroke-width="6" stroke-dasharray="4 16" stroke-linecap="round"><path d="M${x0} 70 V500"/><path d="M${x1} 70 V500"/></g>` : ''}`);
};
// Ebbinghaus
const ebb = (reveal) => {
  let b = '';
  const cx1 = 222, cx2 = 666, cy = 280;
  for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3; b += `<circle cx="${cx1 + 148 * Math.cos(a)}" cy="${cy + 148 * Math.sin(a)}" r="64" fill="${G}"/>`; }
  for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4 + .2; b += `<circle cx="${cx2 + 92 * Math.cos(a)}" cy="${cy + 92 * Math.sin(a)}" r="22" fill="${G}"/>`; }
  b += `<circle cx="${cx1}" cy="${cy}" r="46" fill="${E}"/><circle cx="${cx2}" cy="${cy}" r="46" fill="${E}"/>`;
  if (reveal) b += `<g fill="none" stroke="${C}" stroke-width="7" stroke-dasharray="3 14" stroke-linecap="round"><circle cx="${cx1}" cy="${cy}" r="58"/><circle cx="${cx2}" cy="${cy}" r="58"/></g>`;
  return svg(888, 560, b);
};
// Delboeuf
const del = () => svg(888, 560, `<g fill="none" stroke="${G}" stroke-width="7"><circle cx="210" cy="280" r="92"/><circle cx="640" cy="280" r="200"/></g>
  <circle cx="210" cy="280" r="58" fill="${E}"/><circle cx="640" cy="280" r="58" fill="${E}"/>`);
// Hermann
const herm = () => { let b = ''; for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) b += `<rect x="${44 + i * 210}" y="${44 + j * 210}" width="170" height="170" rx="10" fill="${E}"/>`; return svg(888, 888, b); };
// Point aveugle
const blind = () => svg(888, 520, `<g stroke="${E}" stroke-width="14" stroke-linecap="round"><path d="M130 260 H210 M170 220 V300"/></g><circle cx="730" cy="260" r="30" fill="${E}"/>`);
// Stroop
const stroop = () => { const rows = [['CLAIR', E], ['FONCÉ', P], ['FONCÉ', E], ['CLAIR', P], ['CLAIR', E], ['FONCÉ', P]];
  return svg(888, 900, rows.map(([m, c], i) => `<text x="444" y="${130 + i * 132}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="104" letter-spacing="-3" fill="${c}">${m}</text>`).join('')); };
// Mina : grille de carrés
const grille = (mode) => { let b = ''; const n = [5, 6];
  for (let i = 0; i < n[0]; i++) for (let j = 0; j < n[1]; j++) { const x = 70 + i * 164, y = 50 + j * 150, tilt = (mode === 3 && i === 3 && j === 3);
    b += tilt ? `<rect x="${x}" y="${y}" width="110" height="110" rx="8" fill="${C}" transform="rotate(14 ${x + 55} ${y + 55})"/>` : `<rect x="${x}" y="${y}" width="110" height="110" rx="8" fill="${G}" opacity=".55"/>`; }
  if (mode === 1) b += `<circle cx="444" cy="975" r="26" fill="${E}"/>`; return svg(888, mode === 1 ? 1010 : 940, b); };

const D = '/home/user/brooze-agent/posts/';
const ecrire = (id, o) => { fs.mkdirSync(D + id, { recursive: true }); fs.writeFileSync(D + id + '/post.json', JSON.stringify(o, null, 2)); };
const cta = (titre, texte, bouton) => ({ layout: 'cta', theme: 'encre', titre, taille: 't-m', texte, bouton });

ecrire('2026-11-11-illusions-trois-essais', {
  type: 'carrousel', date_prevue: '2026-11-11T18:00:00+01:00', avatar: 'Karim', pilier: 'Démonstration', role: 'attirer',
  hypothese: "Si un jeu d'illusions où le lecteur se trompe lui-même (carrousel visuel, sujet hors business relié au cadrage) pour Karim, alors les enregistrements et partages / portée seront plus hauts que sur le quiz du 02/11, parce que se tromper devant l'évidence donne envie de la montrer à quelqu'un.",
  nouveau_format: true,
  emotion: { quoi: 'surprise', comment: "les deux lignes qu'on jurait inégales sont pareilles, puis les deux ronds", ou: 'diapos 2 et 4' },
  test_ose: { quoi: "Carrousel 100 % jeu d'illusions, sans conseil avant l'avant-dernière diapo", pourquoi: "Koulechov a montré que vivre une expérience bat une leçon", risque: "Sujet jugé hors métier, peu de messages", garde_fou: 'Diapos 6 et 7 relient au cadrage vidéo et invitent à écrire', mesure: 'enregistrements + partages / portée supérieurs à ceux du carrousel du 02/11 (quiz)', arret: "Deux jeux consécutifs sans partage ni enregistrement : retour à un carrousel plus proche du métier" },
  direction_artistique: 'Cartes claires, dessin géométrique net en encre et gris, un seul pointillé cuivre pour la vérité.',
  slides: [
    { layout: 'visuel', label: 'Jeu · 3 illusions', titre: 'Laquelle est la plus *longue* ?', texte: 'Choisis dans ta tête avant de glisser.', svg: ml(false), h: 680 },
    { layout: 'visuel', theme: 'studio', label: 'Réponse', titre: 'Pareilles.', texte: 'Les petites flèches ont décidé à ta place.', svg: ml(true), h: 680 },
    { layout: 'visuel', label: 'Deuxième essai', titre: 'Quel rond noir est le plus grand ?', svg: ebb(false), h: 680 },
    { layout: 'visuel', theme: 'studio', label: 'Réponse', titre: 'Identiques.', texte: 'Ce qui entoure change ce que tu vois.', svg: ebb(true), h: 680 },
    { layout: 'visuel', label: 'Dernier essai', titre: 'Même rond. Deux cadres.', texte: 'Dans le cadre serré, il paraît souvent plus gros. Dans le cadre large, plus petit.', svg: del(), h: 680 },
    { layout: 'phrase', theme: 'studio', label: 'Ce que ça change pour toi', titre: 'Ton cerveau ne *mesure* pas. Il compare.', taille: 't-l', texte: 'Une vidéo, c’est un cadre : ce qu’on met autour de ton produit compte autant que le produit.' },
    cta('Ton cadre, on le travaille avec toi.', 'À partir de ce que tu as déjà filmé.', 'Envoie-nous un message'),
  ],
  caption: "Deux lignes, laquelle est la plus longue ? Tu viens de te faire avoir, nous aussi la première fois.\n\nTon œil ne mesure pas : il compare avec ce qui entoure. Une vidéo marche pareil, le cadre autour d'un produit change ce qu'on en voit. C'est notre métier : cadrer ce que tu as déjà filmé.\n\nEnvoie-nous un message → @broozeproduction\n\nTu avais trouvé la 1re, ou tu t'es fait avoir ? Envoie ce carrousel à quelqu'un qui est sûr de ses yeux.\n\n#illusion #video #strasbourg"
});

const story = (id, date, o) => ecrire(id, { type: 'story', date_prevue: date, role: 'attirer', nouveau_format: true, ...o });
story('2026-11-09-ghost-grille', '2026-11-09T12:00:00+01:00', {
  avatar: 'Karim', pilier: 'Démonstration', hypothese: "Une illusion à regarder (grille d'Hermann) obtient plus de réponses / portée qu'une affirmation, parce qu'on veut dire ce qu'on voit.",
  emotion: { quoi: 'curiosité puis surprise', comment: "des points gris apparaissent là où il n'y en a pas", ou: 'image 1' },
  slides: [
    { layout: 'visuel', label: 'Regarde les croisements', titre: 'Combien de points *gris* vois-tu ?', texte: 'Compte-les avant de passer.', svg: herm(), h: 900, taille: 't-m' },
    { layout: 'phrase', theme: 'studio', label: 'Réponse', titre: 'Zéro. Ton œil les fabrique.', taille: 't-l', texte: 'Ton cerveau relie ce qu’il voit pour compléter. Le montage fait pareil avec deux plans : on en fait une histoire.' },
    { layout: 'cta', theme: 'encre', titre: 'Tu en as vu combien ? Réponds en message.', taille: 't-m', bouton: 'Réponds en message' },
  ]});
story('2026-11-10-mina', '2026-11-10T12:00:00+01:00', {
  avatar: 'Claire', pilier: 'Fiction annoncée', hypothese: "Une mini-fiction en 3 images (« Petite histoire inventée ») obtient plus de passages jusqu'à la dernière image que les stories sans récit.",
  emotion: { quoi: 'tendresse et sourire', comment: 'un petit point qui scrolle et s’arrête sur le seul carré penché', ou: 'image 3' },
  test_ose: { quoi: 'Première fiction en story, personnage récurrent possible (Mina)', pourquoi: 'les histoires gardent jusqu’au bout', risque: 'Perçue comme enfantine ou hors sujet', garde_fou: 'Fiction annoncée et reliée au métier en dernière image', mesure: 'passages vers l’image suivante / portée, sorties / portée', arret: 'Sorties élevées sur 2 fictions : on arrête' },
  slides: [
    { layout: 'visuel', label: 'Petite histoire inventée', titre: 'Mina scrolle.', texte: 'Des centaines de carrés pareils. Elle ne s’arrête sur aucun.', svg: grille(1), h: 1000, taille: 't-m' },
    { layout: 'visuel', label: 'Petite histoire inventée', titre: 'Et puis, un seul est penché.', svg: grille(3), h: 900, taille: 't-m' },
    { layout: 'cta', theme: 'encre', titre: 'Mina s’arrête. Pas pour le plus beau : pour celui qui sort du rang.', taille: 't-m', texte: 'Envoie ça à celui qui poste comme tout le monde.', bouton: 'Envoie-le à quelqu’un' },
  ]});
story('2026-11-12-stroop', '2026-11-12T12:00:00+01:00', {
  avatar: 'Claire', pilier: 'Démonstration', hypothese: "Un petit test à faire à voix haute (effet Stroop) obtient plus de réponses / portée qu'une question, parce qu'il crée une sensation vécue.",
  emotion: { quoi: 'frustration qui se résout, rire', comment: 'on bute en disant la teinte à voix haute', ou: 'image 1' },
  slides: [
    { layout: 'visuel', fond: 'studio', label: 'Dis à voix haute la teinte', titre: 'Pas le mot : clair ou *foncé* ?', texte: 'Le plus vite possible, de haut en bas.', svg: stroop(), h: 900, taille: 't-m' },
    { layout: 'phrase', theme: 'studio', label: 'Si tu as ralenti', titre: 'Normal : lire est automatique.', taille: 't-l', texte: 'Un texte à l’écran est lu avant d’être jugé. Chez Brooze : cinq mots maximum par image.' },
    { layout: 'cta', theme: 'encre', titre: 'Tu as buté combien de fois ? Dis-le-nous.', taille: 't-m', bouton: 'Réponds en message' },
  ]});
story('2026-11-14-point-aveugle', '2026-11-14T12:00:00+01:00', {
  avatar: 'Karim', pilier: 'Mini-expérience', hypothese: "Une mini-expérience à faire chez soi (point aveugle) obtient plus de réponses / portée qu'un quiz à regarder, parce qu'elle fait agir.",
  emotion: { quoi: 'émerveillement', comment: 'le rond disparaît vraiment', ou: 'image 1' },
  slides: [
    { layout: 'visuel', label: 'Mini-expérience · 20 secondes', titre: 'Ferme l’œil gauche. Fixe la *croix*.', texte: 'Approche ou éloigne le téléphone doucement, sans quitter la croix des yeux.', svg: blind(), h: 520, taille: 't-m' },
    { layout: 'phrase', theme: 'studio', label: 'Le rond a disparu ?', titre: 'Ton cerveau comble les trous.', taille: 't-l', texte: 'Tu as un point aveugle dans chaque œil, et tu ne le vois jamais. Un montage bien fait se remarque pareil : jamais.' },
    { layout: 'cta', theme: 'encre', titre: 'Il a disparu pour toi ? Réponds OUI ou NON.', taille: 't-m', bouton: 'Réponds en message' },
  ]});
