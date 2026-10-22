"""Reel « Apple montre » v2 — trois images photoréalistes fixes, animées ensuite en 2,5D par le moteur du Reel.
Un téléphone GÉNÉRIQUE (aucun logo, aucune forme de marque), une fiche technique imprimée qui n'en finit pas, une table
en chêne. Usage : ~/blender-env/bin/python scene.py <objectifs|fiche|ecran|tout> [pct] [spp]"""
import sys, os, math, bpy
SKILL = [os.path.join(r, 'brooze-3d') for r in ['/root/.claude/skills/synced/' + d for d in os.listdir('/root/.claude/skills/synced')]
         if os.path.isdir(os.path.join(r, 'brooze-3d'))][0]
sys.path.insert(0, os.path.join(SKILL, 'scripts')); import b3d as B; from b3d import M, mm
from PIL import Image, ImageDraw, ImageFont
ICI = os.path.dirname(os.path.abspath(__file__)); POL = os.path.join(SKILL, 'assets', 'polices') + '/'
QUOI = sys.argv[1] if len(sys.argv) > 1 else 'tout'
PCT = int(sys.argv[2]) if len(sys.argv) > 2 else 30; SPP = int(sys.argv[3]) if len(sys.argv) > 3 else 24

# --- la fiche imprimée : des caractéristiques sans aucun chiffre (on ne les invente pas), en colonne, très longue ---
fiche_png = os.path.join(ICI, 'fiche.png')
if not os.path.exists(fiche_png):
    W, H = 900, 7200; im = Image.new('RGB', (W, H), (238, 235, 228)); d = ImageDraw.Draw(im)
    f_t = ImageFont.truetype(POL + 'inter800.ttf', 54); f_l = ImageFont.truetype(POL + 'inter700.ttf', 30); f_v = ImageFont.truetype(POL + 'space-grotesk_700.ttf', 28)
    d.text((60, 70), 'CARACTÉRISTIQUES TECHNIQUES', font=f_t, fill=(28, 26, 24))
    noms = ['Capteur principal', 'Ouverture', 'Stabilisation optique', 'Zoom optique', 'Mise au point', 'Mode nuit', 'Vidéo',
            'Ralenti', 'Processeur', 'Moteur neuronal', 'Mémoire vive', 'Stockage', 'Écran', 'Luminosité', 'Fréquence',
            'Verre avant', 'Châssis', 'Étanchéité', 'Batterie', 'Charge rapide', 'Charge sans fil', 'Haut-parleurs',
            'Micros', 'Réseau', 'Wi-Fi', 'Bluetooth', 'Localisation', 'Capteurs', 'Biométrie', 'Couleurs']
    vals = ['Avancé', 'Large', 'Oui', 'Optique', 'Rapide', 'Amélioré', 'Haute définition', 'Pro', 'Dernière génération',
            'Intégré', 'Élevée', 'Plusieurs options', 'Haute résolution', 'Élevée', 'Adaptative', 'Renforcé', 'Premium']
    y = 190; k = 0
    while y < H - 80:
        d.line((60, y - 18, W - 60, y - 18), fill=(200, 196, 188), width=2)
        d.text((60, y), noms[k % len(noms)], font=f_l, fill=(40, 38, 35))
        v = vals[(k * 7) % len(vals)]; tw = d.textlength(v, font=f_v); d.text((W - 60 - tw, y + 2), v, font=f_v, fill=(95, 92, 86))
        y += 74; k += 1
    im.save(fiche_png)

B.nouvelle_scene()
# --- matières ---
titane = B.M.metal_brosse((.42, .42, .43), .3); B.imperfections(titane, traces=.25)
dos = B.matiere('verre_dos_givre', (.035, .036, .04), 0, .32, .06, 900, coat=.6, coat_rug=.08, bosse=.01)
B.imperfections(dos, traces=.35, poussiere=.2)
bloc_photo = B.matiere('bloc_photo', (.02, .02, .023), 0, .12, .03, 600, coat=1, coat_rug=.02)
bague = B.M.metal_brosse((.62, .62, .63), .22)
lentille = B.matiere('lentille', (.002, .002, .004), 0, .02, coat=1, coat_rug=.01, film=380)
papier = B.matiere('papier_fiche', (1, 1, 1), 0, .82, .05, 120, sss=.08, sss_rayon=(.5, .5, .5), sheen=.08, image=fiche_png)

# --- le téléphone (dimensions d'un smartphone 6,1 pouces courant : 71,5 × 147,5 × 7,8 mm) ---
Lw, Lh, E = 71.5 * mm, 147.5 * mm, 7.8 * mm
corps = B.dalle('corps', Lw, Lh, 10 * mm, E, biseau=.6 * mm, segs=4, mat=titane, expo=2.6)
verre_dos = B.dalle('dos', Lw - 1.6 * mm, Lh - 1.6 * mm, 9.2 * mm, .25 * mm, 0, z0=E - .05 * mm, mat=dos, expo=2.6)
# bloc photo GÉNÉRIQUE : une pastille verticale à deux objectifs (pas la forme d'une marque)
bx, by = -Lw / 2 + 14 * mm, Lh / 2 - 26 * mm
blocp = B.dalle('bloc', 17 * mm, 34 * mm, 8.5 * mm, 1.1 * mm, .3 * mm, 3, z0=E + .2 * mm, mat=bloc_photo, expo=2.2); blocp.location = (bx, by, 0)
for k, dy in enumerate((7.6 * mm, -7.6 * mm)):
    B.cylindre(f'bague{k}', 6.2 * mm, 1.0 * mm, (bx, by + dy, E + 1.3 * mm), bague, biseau=.25 * mm)
    B.cylindre(f'verre{k}', 5.1 * mm, .4 * mm, (bx, by + dy, E + 2.15 * mm), lentille, biseau=.15 * mm)
B.cylindre('flash', 2.2 * mm, .3 * mm, (bx + 12.5 * mm, by, E + .2 * mm), B.matiere('flash', (.75, .7, .55), 0, .2, coat=1))
# écran (face avant, côté z = 0) : une photo « incroyable » prise avec le téléphone (rendu Brooze du Reel 10)
ecran = B.dalle('ecran', Lw - 3.4 * mm, Lh - 3.4 * mm, 8.6 * mm, .2 * mm, 0, z0=-.15 * mm, mat=B.M.ecran(os.path.join(ICI, 'photo_ecran.jpg'), 1.0), expo=2.6)
B.projeter_uv(ecran, 'Z')
tel = [corps, verre_dos, blocp, ecran] + [o for o in bpy.data.objects if o.name.startswith(('bague', 'verre', 'flash'))]
racine = B.grouper('telephone', tel)

# --- la fiche : une bande de papier longue (90 × 720 mm à l'échelle de l'image), légèrement ondulée ---
bpy.ops.mesh.primitive_plane_add(size=1); fiche = bpy.context.object; fiche.name = 'fiche'
fiche.scale = (.09, .72, 1); B.appliquer(fiche); fiche.data.materials.append(papier)
bpy.ops.object.modifier_add(type='SUBSURF'); fiche.modifiers[-1].subdivision_type = 'SIMPLE'; fiche.modifiers[-1].levels = 6; fiche.modifiers[-1].render_levels = 6
B.deformer(fiche, .0009, .12, graine=3)

table = B.sol('bois', taille=3.0)
B.monde((.010, .009, .008), 1.0)


def pose(quoi):
    if quoi == 'objectifs':      # dos vers le haut, gros plan sur les objectifs, lumière rasante chaude
        racine.location = (0, 0, 0); racine.rotation_euler = (0, 0, math.radians(-18))
        fiche.location = (.16, .05, .0025); fiche.rotation_euler = (0, 0, math.radians(8))
        bpy.context.view_layer.update()
        B.studio('macro', [blocp], 1.4)
        lentilles = [o for o in bpy.data.objects if o.name.startswith(('bague', 'verre', 'flash', 'bloc'))]
        B.cadrer(lentilles, focale=100, azimut=-35, hauteur=22, remplissage=.62, f=4.0)
    elif quoi == 'fiche':        # la fiche vue de dessus, en plongée, qui file hors du cadre
        racine.location = (.13, -.2, 0); racine.rotation_euler = (0, 0, math.radians(25))
        fiche.location = (0, 0, .0025); fiche.rotation_euler = (0, 0, math.radians(-4))
        B.studio('plongee', [fiche], 1.0)
        B.camera((.02, -.33, .36), (0, -.02, 0), focale=50, f=5.6, mise_au_point=None)
    elif quoi == 'ecran':        # face vers le haut, écran allumé sur une photo, trois-quarts, faible profondeur de champ
        racine.location = (0, 0, E); racine.rotation_euler = (math.pi, 0, math.radians(-20))
        fiche.location = (.24, .3, .0025); fiche.rotation_euler = (0, 0, math.radians(-30))   # hors du reflet de l'écran
        B.studio('produit', [corps], 1.6)
        pe = ecran.active_material.node_tree.nodes['Principled BSDF'].inputs   # verre antireflet : un reflet discret, l'image lisible
        pe['Coat Weight'].default_value = .18; pe['Specular IOR Level'].default_value = .12
        B.camera((.11, -.17, .2), (0, .005, .004), focale=60, f=2.8)

    elif quoi == 'dessus':       # à plat, vu du dessus : le téléphone allumé posé à côté de la fiche (flat lay)
        racine.location = (.0, -.005, E); racine.rotation_euler = (math.pi, 0, math.radians(-6))
        fiche.location = (-.085, .03, .0025); fiche.rotation_euler = (0, 0, math.radians(4))
        # vu de dessus, un écran très brillant ne montre plus que les reflets des lumières : verre traité antireflet
        pe = ecran.active_material.node_tree.nodes['Principled BSDF'].inputs
        pe['Coat Weight'].default_value = .0; pe['Specular IOR Level'].default_value = .08; pe['Roughness'].default_value = .3
        B.studio('plongee', [corps, fiche], 1.1)
        # caméra légèrement inclinée (pas pile au-dessus) : les panneaux de lumière ne se reflètent plus dans l'écran
        B.camera((-.012, -.13, .30), (-.013, .0, 0), focale=55, f=5.6)


if __name__ == '__main__':
    os.makedirs(os.path.join(ICI, 'rendus'), exist_ok=True)
    for q in (['objectifs', 'fiche', 'ecran', 'dessus'] if QUOI == 'tout' else [QUOI]):
        for o in [o for o in bpy.data.objects if o.type in ('LIGHT', 'CAMERA')]: bpy.data.objects.remove(o, do_unlink=True)
        pose(q); B.reglages(spp=SPP, pct=PCT)
        B.rendre(os.path.join(ICI, 'rendus', f'{q}.png'))
