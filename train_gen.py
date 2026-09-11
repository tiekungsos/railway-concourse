import bpy, math, os

bpy.ops.wm.read_factory_settings(use_empty=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'train.glb')

def mat(name, color, metal=0.0, rough=0.6, emit=None, estr=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if emit:
        key = 'Emission Color' if 'Emission Color' in b.inputs else 'Emission'
        b.inputs[key].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = estr
    return m

BODY = mat('Body', (0.075, 0.14, 0.11), metal=0.35, rough=0.42)
BAND = mat('Band', (0.78, 0.74, 0.62), rough=0.55)
ROOF = mat('Roof', (0.55, 0.57, 0.58), rough=0.6)
GLASS = mat('Glass', (0.04, 0.07, 0.09), metal=0.55, rough=0.12)
DARK = mat('Dark', (0.07, 0.075, 0.08), rough=0.7)
RED = mat('Red', (0.42, 0.1, 0.07), rough=0.55)
METAL = mat('Metal', (0.42, 0.44, 0.46), metal=0.85, rough=0.35)
LIGHT = mat('Light', (0.9, 0.8, 0.6), emit=(1.0, 0.8, 0.5), estr=4.0)

def box(name, dims, loc, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (dims[0] / 2, dims[1] / 2, dims[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bev:
        mod = o.modifiers.new('b', 'BEVEL')
        mod.width = bev
        mod.segments = 3
        bpy.ops.object.modifier_apply(modifier='b')
    if m:
        o.data.materials.append(m)
    return o

def cyl(name, r, d, loc, m, rot=(0, 0, 0), bev=0.0):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    if bev:
        mod = o.modifiers.new('b', 'BEVEL')
        mod.width = bev
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier='b')
    if m:
        o.data.materials.append(m)
    return o

L, W = 19.0, 2.82

box('body', (L, W, 2.62), (0, 0, 2.31), BODY, bev=0.16)
box('roof', (18.6, 2.56, 0.5), (0, 0, 3.74), ROOF, bev=0.2)
box('winband', (18.75, W + 0.05, 0.78), (0, 0, 2.86), GLASS, bev=0.05)
box('band', (18.7, W + 0.04, 0.3), (0, 0, 2.3), BAND)
box('gutter', (18.8, W + 0.07, 0.07), (0, 0, 3.3), BAND)

for i in range(9):
    px = -8.0 + i * 2.0
    for sy in (-1, 1):
        box(f'pillar_{i}_{sy}', (0.5, 0.06, 0.82), (px, sy * 1.435, 2.86), BODY)

for dx in (-6.6, 6.6):
    for sy in (-1, 1):
        box(f'door_{dx}_{sy}', (1.4, 0.07, 2.3), (dx, sy * 1.415, 2.05), DARK)
        box(f'doorwin_{dx}_{sy}', (1.0, 0.08, 0.6), (dx, sy * 1.415, 2.85), GLASS)
        cyl(f'grab_{dx}_{sy}_a', 0.02, 1.6, (dx + 0.72, sy * 1.46, 1.9), METAL)
        cyl(f'grab_{dx}_{sy}_b', 0.02, 1.6, (dx - 0.72, sy * 1.46, 1.9), METAL)

for ex in (-1, 1):
    x = ex * (L / 2)
    box(f'cabwin_{ex}', (0.08, 2.15, 0.72), (x + ex * 0.02, 0, 2.92), GLASS)
    box(f'cabwin_div_{ex}', (0.1, 0.06, 0.72), (x + ex * 0.03, 0, 2.92), BODY)
    box(f'blind_{ex}', (0.1, 0.55, 0.22), (x + ex * 0.04, 0, 3.42), DARK)
    box(f'bufbeam_{ex}', (0.22, 2.45, 0.38), (x - ex * 0.06, 0, 1.28), RED)
    for by in (-0.82, 0.82):
        cyl(f'buffer_{ex}_{by}', 0.1, 0.5, (x + ex * 0.2, by, 1.32), METAL, rot=(0, math.radians(90), 0))
        cyl(f'bufhead_{ex}_{by}', 0.23, 0.1, (x + ex * 0.42, by, 1.32), METAL, rot=(0, math.radians(90), 0), bev=0.02)
        cyl(f'lamp_{ex}_{by}', 0.09, 0.08, (x + ex * 0.05, by * 0.62, 1.95), LIGHT, rot=(0, math.radians(90), 0))
    cyl(f'marker_{ex}', 0.055, 0.07, (x + ex * 0.05, -0.62, 3.55), LIGHT, rot=(0, math.radians(90), 0))
    box(f'coupler_{ex}', (0.75, 0.34, 0.3), (x + ex * 0.3, 0, 0.95), DARK)
    box(f'hook_{ex}', (0.3, 0.1, 0.5), (x + ex * 0.62, 0, 0.72), METAL)

box('under', (17.8, 2.3, 0.5), (0, 0, 0.72), DARK)
box('fuel', (2.4, 1.7, 0.55), (0.5, 0, 0.62), DARK)
for bx in (-4.2, 4.2):
    box(f'batt_{bx}', (1.7, 0.95, 0.5), (bx, 0, 0.6), DARK)

for bx in (-6.3, 6.3):
    box(f'bogie_{bx}', (3.1, 2.15, 0.5), (bx, 0, 0.58), DARK, bev=0.06)
    for sy in (-1, 1):
        box(f'bframe_{bx}_{sy}', (3.0, 0.09, 0.34), (bx, sy * 1.12, 0.55), DARK)
        for j in (-1, 0, 1):
            cyl(f'spring_{bx}_{sy}_{j}', 0.1, 0.3, (bx + j * 0.5, sy * 1.13, 0.78), METAL)
    for wx in (-0.95, 0.95):
        ax = bx + wx
        cyl(f'axle_{ax}', 0.05, 1.85, (ax, 0, 0.42), METAL, rot=(math.radians(90), 0, 0))
        for sy in (-1, 1):
            cyl(f'wheel_{ax}_{sy}', 0.42, 0.13, (ax, sy * 0.75, 0.42), METAL, rot=(math.radians(90), 0, 0), bev=0.03)

for rx in (-4.8, 4.8):
    box(f'exhaust_{rx}', (0.9, 0.8, 0.22), (rx, 0, 4.05), DARK)
cyl('pipe', 0.05, 2.6, (-8.2, 0.9, 4.05), METAL, rot=(0, math.radians(90), 0))

bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('EXPORTED', OUT)
