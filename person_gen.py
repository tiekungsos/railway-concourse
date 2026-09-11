import bpy, math, os
from mathutils import Matrix

bpy.ops.wm.read_factory_settings(use_empty=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'person.glb')

def mat(name, color, rough=0.7, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    return m

SKIN = mat('Skin', (0.72, 0.55, 0.42), 0.55)
COAT = mat('Coat', (0.16, 0.18, 0.22), 0.85)
TROUSER = mat('Trouser', (0.1, 0.1, 0.12), 0.9)
SHOE = mat('Shoe', (0.05, 0.045, 0.04), 0.5)
HAIR = mat('Hair', (0.12, 0.09, 0.06), 0.9)
HATM = mat('Hat', (0.09, 0.09, 0.1), 0.8)
EYE = mat('Eye', (0.04, 0.03, 0.025), 0.35)
MOUTH = mat('Mouth', (0.3, 0.14, 0.11), 0.7)
SHIRT = mat('Shirt', (0.85, 0.82, 0.74), 0.75)
TIE = mat('Tie', (0.07, 0.08, 0.12), 0.7)
VEST = mat('Vest', (0.38, 0.35, 0.3), 0.8)

def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True

def parent_keep(child, parent):
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()

def sph(name, r, loc, m, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=24, ring_count=16, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    smooth(o)
    o.data.materials.append(m)
    if parent:
        parent_keep(o, parent)
    return o

def cone(name, r_top, r_bot, length, loc, m, parent=None, bev=0.0, seg=20):
    bpy.ops.mesh.primitive_cone_add(vertices=seg, radius1=r_bot, radius2=r_top, depth=length, location=loc)
    o = bpy.context.active_object
    o.name = name
    if bev:
        mod = o.modifiers.new('b', 'BEVEL')
        mod.width = bev
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier='b')
    smooth(o)
    o.data.materials.append(m)
    if parent:
        parent_keep(o, parent)
    return o

def limb(name, r_top, r_bot, length, joint, m, parent=None):
    o = cone(name, r_top, r_bot, length, joint, m, parent, bev=0.01)
    o.data.transform(Matrix.Translation((0, 0, -length / 2)))
    return o

def cube(name, dims, loc, m, parent=None, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (dims[0] / 2, dims[1] / 2, dims[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bev:
        mod = o.modifiers.new('b', 'BEVEL')
        mod.width = bev
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier='b')
    o.data.materials.append(m)
    if parent:
        parent_keep(o, parent)
    return o

sph('Pelvis', 0.185, (0, 0, 0.97), TROUSER, scale=(1.05, 0.8, 0.85))
cone('CoatSkirt', 0.185, 0.225, 0.5, (0, 0, 0.95), COAT, bev=0.03)
torso = cone('Torso', 0.2, 0.165, 0.58, (0, 0, 1.29), COAT, bev=0.05)
torso.scale.y = 0.8
bpy.ops.object.transform_apply(scale=True)
sph('Shoulders', 0.125, (0, 0, 1.53), COAT, scale=(1.85, 0.9, 0.9))
cone('Collar', 0.072, 0.09, 0.07, (0, -0.005, 1.58), COAT)
cone('Neck', 0.05, 0.055, 0.1, (0, 0, 1.6), SKIN)
cube('ShirtV', (0.08, 0.025, 0.09), (0, -0.155, 1.545), SHIRT).rotation_euler.x = math.radians(18)
for s in (-1, 1):
    lp = cube(f'Lapel{s}', (0.045, 0.018, 0.34), (s * 0.052, -0.152, 1.33), COAT)
    lp.rotation_euler.z = math.radians(-s * 10)
for i in range(4):
    sph(f'Btn{i}', 0.011, (0, -0.166, 1.36 - i * 0.09), HATM, scale=(1, 0.5, 1))

head = sph('Head', 0.117, (0, -0.005, 1.72), SKIN, scale=(0.9, 0.88, 1.14))
nose = cone('Nose', 0.0, 0.016, 0.05, (0, -0.114, 1.705), SKIN, parent=head)
nose.rotation_euler.x = math.radians(-90)
sph('EarL', 0.02, (-0.104, 0, 1.72), SKIN, scale=(0.45, 0.8, 1), parent=head)
sph('EarR', 0.02, (0.104, 0, 1.72), SKIN, scale=(0.45, 0.8, 1), parent=head)
for s in (-1, 1):
    sph(f'Eye{s}', 0.016, (s * 0.043, -0.1, 1.732), EYE, parent=head)
    cube(f'Brow{s}', (0.042, 0.01, 0.011), (s * 0.044, -0.105, 1.756), HAIR, parent=head)
cube('Mouth', (0.036, 0.011, 0.012), (0, -0.109, 1.662), MOUTH, parent=head)
sph('Hair', 0.122, (0, 0.014, 1.745), HAIR, scale=(0.95, 0.98, 0.82), parent=head)

brim = cone('TopHat', 0.185, 0.185, 0.02, (0, 0.005, 1.80), HATM, parent=head)
parent_keep(cone('TopHatC', 0.115, 0.13, 0.19, (0, 0.005, 1.895), HATM), brim)
bwl = sph('Bowler', 0.128, (0, 0.005, 1.775), HATM, scale=(1, 1, 0.72), parent=head)
parent_keep(cone('BowlerB', 0.165, 0.165, 0.016, (0, 0.005, 1.745), HATM), bwl)
cap = sph('FlatCap', 0.132, (0, -0.01, 1.745), HATM, scale=(1.08, 1.05, 0.5), parent=head)
parent_keep(cube('FlatCapV', (0.14, 0.1, 0.018), (0, -0.135, 1.71), HATM), cap)

for s, sx in [('L', -1), ('R', 1)]:
    th = limb(f'Thigh{s}', 0.082, 0.065, 0.45, (sx * 0.105, 0, 0.95), TROUSER)
    sh = limb(f'Shin{s}', 0.06, 0.048, 0.44, (sx * 0.105, 0, 0.5), TROUSER, parent=th)
    cube(f'Foot{s}', (0.115, 0.28, 0.08), (sx * 0.105, -0.055, 0.04), SHOE, parent=sh, bev=0.025)
    sph(f'Shoulder{s}', 0.062, (sx * 0.215, 0, 1.5), COAT)
    au = limb(f'ArmU{s}', 0.06, 0.05, 0.3, (sx * 0.215, 0, 1.5), COAT)
    au.rotation_euler.z = math.radians(sx * 7)
    af = limb(f'ArmF{s}', 0.048, 0.04, 0.27, (sx * 0.235, 0, 1.2), COAT, parent=au)
    af.rotation_euler.x = math.radians(-8)
    sph(f'Hand{s}', 0.05, (sx * 0.235, -0.008, 0.905), SKIN, scale=(0.75, 0.9, 1.1), parent=af)

cane = cone('Cane', 0.013, 0.013, 0.85, (0.25, -0.02, 0.52), HATM, parent=bpy.data.objects['ArmFR'])
cone('CaneH', 0.013, 0.013, 0.12, (0.25, -0.075, 0.94), HATM, parent=cane).rotation_euler.x = math.radians(90)

bpy.ops.export_scene.gltf(filepath=OUT, export_format='GLB', export_apply=True)
print('EXPORTED', OUT)
