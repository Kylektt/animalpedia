import bpy, math
from pathlib import Path
root = Path(__file__).resolve().parents[2]
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(root / 'dist/assets/koala.glb'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
points=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
lo=Vector([min(p[i] for p in points) for i in range(3)])
hi=Vector([max(p[i] for p in points) for i in range(3)])
center=(lo+hi)/2; size=max(hi-lo)
print('BOUNDS',list(lo),list(hi))
bpy.ops.object.camera_add(location=center+Vector((1.6,-2.8,1.1))*size)
camera=bpy.context.object;camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=size*1.35
scene=bpy.context.scene;scene.camera=camera
for name,offset,power,extent in [('Key',(-2,-3,4),220,4),('Fill',(3,-1,2),120,3),('Rim',(0,3,3),180,2)]:
 bpy.ops.object.light_add(type='AREA',location=center+Vector(offset)*size)
 light=bpy.context.object;light.name=name;light.data.energy=power*size*size;light.data.shape='DISK';light.data.size=extent*size;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.75,0.8,0.85,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.4
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=900;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(root / 'dist/assets/koala-poster.png')
scene.view_settings.view_transform='Standard'
bpy.ops.render.render(write_still=True)
