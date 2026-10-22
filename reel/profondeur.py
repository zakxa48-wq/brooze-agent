"""Carte de profondeur d'un rendu Blender (blanc = proche, noir = loin), pour la parallaxe 2,5D du moteur (scène plan).

Deux usages, avec le Python de Blender (~/blender-env/bin/python) :
  1. dans une scène écrite en code, après le rendu de l'image :
       sys.path.insert(0, '<brooze-agent>/reel'); import profondeur
       B.rendre('plan.png'); profondeur.rendre('plan_prof.png')       # même caméra, même cadrage, ~1–3 s
  2. sur une scène sauvegardée (.blend, par exemple celles des exemples du skill brooze-3d) :
       ~/blender-env/bin/python reel/profondeur.py scene.blend plan_prof.png [--pct 100]
Puis dans reel.json : {"type": "plan", "image": "plan.png", "profondeur": "plan_prof.png", "relief": 1, …}.
La profondeur est normalisée sur les objets visibles (le premier plan blanc, le fond noir) et légèrement lissée par
le moteur : pas besoin d'une carte parfaite, il faut une carte juste en gros volumes.
"""
import sys, os, bpy
from mathutils import Vector


def _bornes(cam):
    """Distance mini et maxi des objets visibles à la caméra (coins des boîtes englobantes)."""
    o = cam.matrix_world.translation; d = []
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH' or ob.hide_render: continue
        for c in ob.bound_box:
            d.append((ob.matrix_world @ Vector(c) - o).length)
    d.sort()
    if not d: return .1, 10.
    # le sol et les décors très grands tirent le maximum vers l'infini : on prend le 90e centile
    return max(1e-3, d[0] * .9), d[int(len(d) * .9)]


def rendre(chemin, pct=None):
    s = bpy.context.scene; cam = s.camera; proche, loin = _bornes(cam)
    m = bpy.data.materials.new('_profondeur'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    cd = nt.nodes.new('ShaderNodeCameraData'); mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = proche; mr.inputs['From Max'].default_value = loin
    mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0; mr.clamp = True
    em = nt.nodes.new('ShaderNodeEmission'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(cd.outputs['View Distance'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], em.inputs['Color'])
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    vl = bpy.context.view_layer; ancien = (vl.material_override, s.cycles.samples, s.cycles.use_denoising, s.view_settings.view_transform,
                                           s.view_settings.look, s.render.film_transparent, s.render.image_settings.color_depth,
                                           s.render.resolution_percentage, s.world)
    vl.material_override = m; s.cycles.samples = 8; s.cycles.use_denoising = False
    s.view_settings.view_transform = 'Standard'; s.view_settings.look = 'None'; s.render.film_transparent = False
    s.render.image_settings.color_depth = '16'; s.world = None
    if pct: s.render.resolution_percentage = pct
    s.render.filepath = os.path.abspath(chemin); bpy.ops.render.render(write_still=True)
    (vl.material_override, s.cycles.samples, s.cycles.use_denoising, s.view_settings.view_transform, s.view_settings.look,
     s.render.film_transparent, s.render.image_settings.color_depth, s.render.resolution_percentage, s.world) = ancien
    print(f'PROFONDEUR {chemin} : {proche:.3f}–{loin:.3f} m')


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a[0]))
    pct = int(a[a.index('--pct') + 1]) if '--pct' in a else None
    rendre(a[1], pct)
