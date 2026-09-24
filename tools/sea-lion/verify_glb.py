"""Re-import the deliverable GLB, render under the original neutral studio rig."""
import bpy,json,sys,argparse
from pathlib import Path
from mathutils import Vector
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output_dir.resolve()
bpy.ops.wm.open_mainfile(filepath=str(OUT/'australian-sea-lion-experimental.blend'))
for ob in list(bpy.data.objects):
 if ob.type=='MESH' and ob.name!='Presentation ground':bpy.data.objects.remove(ob,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(OUT/'australian-sea-lion-experimental.glb'))
scene=bpy.context.scene;scene.cycles.samples=48
scene.render.filepath=str(OUT/'glb-roundtrip-three-quarter.png')
bpy.ops.render.render(write_still=True)
scene.camera.location=(0,-4,1);scene.camera.rotation_euler=(Vector((-.2,0,.56))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.camera.data.ortho_scale=2.45
scene.render.filepath=str(OUT/'glb-roundtrip-side.png');bpy.ops.render.render(write_still=True)
