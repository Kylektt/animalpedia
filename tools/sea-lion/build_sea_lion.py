"""Original experimental Australian sea lion mesh. Blender 5.2, no external assets.
Run: blender --background --python build_sea_lion.py
Coordinates in Blender: +X forward, +Z up. GLB exports Y-up.
"""
import bpy, math, random, json, os, sys, argparse
import numpy as np
from mathutils import Vector
from mathutils.noise import noise_vector
from pathlib import Path
random.seed(194)
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for x in bpy.data.materials: bpy.data.materials.remove(x)
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world.color=(.3,.3,.3)
scene.view_settings.view_transform='AgX'
assets=[]

def basic(name,color,rough=.55):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes.clear();p=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
skin=basic('Ash-grey and cream short coat',(.28,.24,.18),.68)
n=skin.node_tree.nodes;l=skin.node_tree.links;p=next(x for x in n if x.type=='BSDF_PRINCIPLED')
t=n.new('ShaderNodeTexCoord');geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Normal'],sep.inputs[0])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=(.41,.315,.19,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(.19,.175,.145,1)
# Use local surface up/down and forward-facing normal to blend the female coat.
mathn=n.new('ShaderNodeMath');mathn.operation='MULTIPLY_ADD';mathn.inputs[1].default_value=.5;mathn.inputs[2].default_value=.5;anterior=n.new('ShaderNodeMath');anterior.operation='MULTIPLY';anterior.inputs[1].default_value=-.8;l.new(sep.outputs['X'],anterior.inputs[0]);coat=n.new('ShaderNodeMath');coat.operation='ADD';l.new(sep.outputs['Z'],coat.inputs[0]);l.new(anterior.outputs[0],coat.inputs[1]);l.new(coat.outputs[0],mathn.inputs[0]);l.new(mathn.outputs[0],ramp.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=19;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.7;l.new(t.outputs['Generated'],noise.inputs['Vector'])
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.27;l.new(ramp.outputs['Color'],mix.inputs[1]);l.new(noise.outputs['Color'],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
mapn=n.new('ShaderNodeVectorMath');mapn.operation='MULTIPLY';mapn.inputs[1].default_value=(20,140,140);l.new(t.outputs['Generated'],mapn.inputs[0])
fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=3;fine.inputs['Detail'].default_value=2;l.new(mapn.outputs[0],fine.inputs[0])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.45;bump.inputs['Distance'].default_value=.003;l.new(fine.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
grain=n.new('ShaderNodeValToRGB');grain.color_ramp.elements[0].position=.3;grain.color_ramp.elements[0].color=(.15,.12,.09,1);grain.color_ramp.elements[1].position=.7;grain.color_ramp.elements[1].color=(1,1,1,1);l.new(fine.outputs['Fac'],grain.inputs[0])
coatgrain=n.new('ShaderNodeMixRGB');coatgrain.blend_type='MULTIPLY';coatgrain.inputs[0].default_value=.72;l.new(mix.outputs[0],coatgrain.inputs[1]);l.new(grain.outputs[0],coatgrain.inputs[2]);l.new(coatgrain.outputs[0],p.inputs['Base Color'])
eye=basic('Dark brown eyes',(.009,.005,.002),.13)
nosemat=basic('Nose leather',(.012,.01,.008),.38)
lip=basic('Mouth and nostril creases',(.035,.022,.013),.7)
whiskmat=basic('Ivory grey vibrissae',(.06,.046,.028),.62)

def mesh(name,verts,faces,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 assets.append(ob);return ob

def catmull(points,steps=8):
 result=[]
 for i in range(len(points)-1):
  a=np.array(points[max(0,i-1)]);b=np.array(points[i]);c=np.array(points[i+1]);d=np.array(points[min(len(points)-1,i+2)])
  for k in range(steps):
   t=k/steps;result.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 result.append(np.array(points[-1]));return result

def loft(name,sections,radial=64,steps=6,mat=skin,body=False):
 # Sections x,y,z,width,sagittal_radius. Transport frame along the centerline.
 ss=catmull(sections,steps);vs=[]
 for i,s in enumerate(ss):
  tang=Vector(ss[min(i+1,len(ss)-1)][:3]-ss[max(0,i-1)][:3]).normalized()
  side=Vector((0,1,0)) if body else tang.cross(Vector((0,0,1))).normalized()
  if side.length<.1:side=Vector((1,0,0))
  up=tang.cross(side).normalized()
  for j in range(radial):
   a=2*math.pi*j/radial;pos=Vector(s[:3])+side*(s[3]*math.cos(a))+up*(s[4]*math.sin(a))
   if body:
    # shallow natural neck and shoulder folds, never bead-like rings
    fold=math.exp(-((pos.x-.24)/.12)**2)*math.exp(-((pos.z-.57)/.28)**2)
    pos+=up*(.006*math.sin(pos.z*95+pos.y*9)*fold*max(0,-math.sin(a)))
    pos.z=max(.042,pos.z)
   vs.append(tuple(pos))
 faces=[]
 for i in range(len(ss)-1):
  for j in range(radial):faces.append((i*radial+j,i*radial+(j+1)%radial,(i+1)*radial+(j+1)%radial,(i+1)*radial+j))
 faces.append(tuple(reversed(range(radial))));faces.append(tuple((len(ss)-1)*radial+j for j in range(radial)))
 return mesh(name,vs,faces,mat)

def uvball(name,loc,scale,mat=skin):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc);ob=bpy.context.object;ob.name=name;ob.data.name=name+' mesh';ob.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(mat)
 for p in ob.data.polygons:p.use_smooth=True
 assets.append(ob);return ob

def curve(name,points,radius,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=8;cu.bevel_depth=radius;cu.bevel_resolution=2
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for i,(p,co) in enumerate(zip(sp.bezier_points,points)):
  p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=1-(i/(len(points)-1))*.85
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat);assets.append(ob);return ob

body=loft('Continuous body neck and head',[
(-.83,0,.16,.025,.035),(-.70,0,.19,.12,.105),(-.52,0,.24,.205,.18),(-.26,0,.30,.265,.25),(-.02,0,.38,.285,.29),(.17,0,.52,.245,.26),(.27,0,.72,.19,.20),(.31,0,.91,.143,.148),(.38,0,1.025,.12,.115),(.47,0,1.068,.12,.100),(.57,0,1.053,.102,.088),(.68,0,1.02,.061,.047),(.702,0,1.018,.005,.006)],steps=7,body=True)
# Muzzle pads, lower jaw and brows are merged into the continuous skin.
parts=[body,uvball('Left muzzle pad',(.648,-.045,1.005),(.076,.057,.049)),uvball('Right muzzle pad',(.648,.045,1.005),(.076,.057,.049)),uvball('Lower jaw',(.593,0,.96),(.096,.069,.034))]
for sg in [-1,1]:parts.append(uvball('Brow',(.511,sg*.104,1.073),(.062,.021,.03)))
bpy.ops.object.select_all(action='DESELECT')
for ob in parts:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join()
body.data.remesh_voxel_size=.0045;bpy.ops.object.voxel_remesh()
sm=body.modifiers.new('Sculpt relaxation','SMOOTH');sm.factor=.5;sm.iterations=5;bpy.ops.object.modifier_apply(modifier=sm.name)
mod=body.modifiers.new('Web mesh budget','DECIMATE');mod.ratio=.24;bpy.ops.object.modifier_apply(modifier=mod.name)
for f in body.data.polygons:f.use_smooth=True
assets=[body]
# Smooth flippers taper into a broad blade, with fine digit seams.
for sg in [-1,1]:
 loft(('Left' if sg<0 else 'Right')+' foreflipper',[(.12,sg*.18,.47,.065,.085),(.15,sg*.26,.34,.084,.056),(.13,sg*.34,.17,.081,.028),(.02,sg*.42,.064,.10,.017),(-.16,sg*.49,.046,.082,.012),(-.30,sg*.51,.05,.012,.008)],radial=40,steps=6)
 for k in range(3):
  curve('Foreflipper digit crease',[(.0+k*.009,sg*(.385+k*.025),.07),(-.12,sg*(.425+k*.027),.063),(-.25+k*.022,sg*(.46+k*.018),.058)],.0012,lip)
 loft(('Left' if sg<0 else 'Right')+' rear flipper',[(-.73,sg*.055,.155,.075,.065),(-.85,sg*.085,.11,.075,.037),(-1.00,sg*.16,.075,.09,.017),(-1.17,sg*.22,.06,.09,.014),(-1.25,sg*.235,.057,.013,.006)],radial=40,steps=5)
 for k in range(4):
  curve('Rear flipper digit crease',[(-.94,sg*(.11+k*.025),.089),(-1.09,sg*(.13+k*.03),.08),(-1.22,sg*(.16+k*.032),.066)],.001,lip)
 # Tiny rolled ear flaps behind eyes.
 ear=uvball('External ear pinna',(.354,sg*.133,1.006),(.028,.018,.014));ear.rotation_euler[1]=-.4
 uvball('Ear aperture',(.351,sg*.157,1.004),(.011,.0028,.005),lip)
 # Small oblique eyes and surrounding lids.
 uvball('Eye',(.524,sg*.108,1.053),(.031,.020,.022),eye)
 curve('Upper eyelid',[(.492,sg*.11,1.058),(.513,sg*.127,1.074),(.54,sg*.117,1.068),(.551,sg*.104,1.051)],.0045,skin)
 curve('Lower eyelid',[(.492,sg*.11,1.054),(.516,sg*.125,1.037),(.54,sg*.114,1.04),(.551,sg*.104,1.051)],.0032,skin)
 # Mouth corner is a shallow dark crease, no smile exaggeration.
 curve('Closed mouth',[(.697,sg*.005,.986),(.662,sg*.048,.974),(.61,sg*.068,.967),(.566,sg*.069,.977)],.0021,lip)
 # Tapered, curved vibrissae, anchored in follicle pores.
 for k in range(17):
  row=k//6;col=k%6
  x=.634+col*.009; y=sg*(.048+row*.014);z=1.012-row*.012+(col%2)*.004
  length=random.uniform(.13,.23);endx=x-random.uniform(.01,.12)
  pts=[(x,y,z),(x+.015, y+sg*length*.38,z+.016-row*.009),(endx+.025,y+sg*length*.76,z+.006-row*.017),(endx,y+sg*length,z-.019-row*.019)]
  uvball('Whisker follicle',(x,y,z),(.0025,.0015,.002),lip)
  curve('Vibrissa',pts,random.uniform(.0006,.00095),whiskmat)
# Blunt triangular leather nose, with paired narrow nostrils.
nose=mesh('Triangular nose leather',[(.719,0,1.04),(.713,-.039,1.036),(.724,-.031,1.01),(.732,0,.997),(.724,.031,1.01),(.713,.039,1.036),(.725,0,1.021)],[(0,1,6),(1,2,6),(2,3,6),(3,4,6),(4,5,6),(5,0,6)],nosemat)
solid=nose.modifiers.new('Nose thickness','SOLIDIFY');solid.thickness=.008
sub=nose.modifiers.new('Soft nose','SUBSURF');sub.levels=2
for sg in [-1,1]:curve('Nostril',[(.728,sg*.012,1.031),(.733,sg*.023,1.023),(.735,sg*.018,1.012)],.0038,lip)
curve('Philtrum',[(.732,0,1.003),(.718,0,.989),(.699,0,.984)],.0017,lip)

# Material baking for embedded, renderer-independent PBR.
meshassets=[]
for ob in list(assets):
 if ob.name not in bpy.data.objects:continue
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 if ob.type=='CURVE':bpy.ops.object.convert(target='MESH')
 for mod in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
 for v in ob.data.vertices:
  world=ob.matrix_world@v.co
  if world.z>.8:world.z=.8+(world.z-.8)*.84
  if world.x>.55 and world.z>.8:world.z+=min(.035,(world.x-.55)*.20)
  v.co=ob.matrix_world.inverted()@world
 meshassets.append(ob)
skinobs=[ob for ob in meshassets if ob.data.materials and ob.data.materials[0]==skin]
bpy.ops.object.select_all(action='DESELECT')
for ob in skinobs:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object
body.data.remesh_voxel_size=.0035;bpy.ops.object.voxel_remesh()
relax=body.modifiers.new('Blend flipper roots','SMOOTH');relax.factor=.38;relax.iterations=3;bpy.ops.object.modifier_apply(modifier=relax.name)
reduce=body.modifiers.new('Final web budget','DECIMATE');reduce.ratio=.115;bpy.ops.object.modifier_apply(modifier=reduce.name)
for poly in body.data.polygons:poly.use_smooth=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
for kind,size in [('BaseColor',2048),('Normal',2048)]:
 img=bpy.data.images.new('SeaLion_'+kind,width=size,height=size,alpha=False)
 if kind=='Normal':img.colorspace_settings.name='Non-Color'
 tex=n.new('ShaderNodeTexImage');tex.image=img;n.active=tex
 scene.render.bake.margin=12;scene.cycles.samples=8
 if kind=='BaseColor':
  scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True;bpy.ops.object.bake(type='DIFFUSE')
 else:bpy.ops.object.bake(type='NORMAL')
 img.filepath_raw=str(OUT/('sea-lion-'+kind.lower()+'.png'));img.file_format='PNG';img.save();img.pack()
# Replace procedural nodes with baked glTF-compatible graph.
col=bpy.data.images['SeaLion_BaseColor'];norm=bpy.data.images['SeaLion_Normal']
n.clear();p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=.72;out=n.new('ShaderNodeOutputMaterial');l.new(p.outputs['BSDF'],out.inputs['Surface'])
ct=n.new('ShaderNodeTexImage');ct.image=col;l.new(ct.outputs['Color'],p.inputs['Base Color'])
nt=n.new('ShaderNodeTexImage');nt.image=norm;nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55;l.new(nt.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal'])
# Export only the animal, excluding presentation lighting and floor.
animal=[o for o in scene.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in animal:o.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object;body.name='Australian sea lion experimental';body.data.name='Australian sea lion mesh';animal=[body]
bpy.ops.export_scene.gltf(filepath=str(OUT/'australian-sea-lion-experimental.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False)
verts=[o.matrix_world@v.co for o in animal for v in o.data.vertices]
mins=[min(v[i] for v in verts) for i in range(3)];maxs=[max(v[i] for v in verts) for i in range(3)]
meta={'scientificName':'Neophoca cinerea','representation':'Original experimental adult female; no anatomical scan; not expert validated','blenderBounds':{'min':mins,'max':maxs},'gltfBounds':{'min':[mins[0],mins[2],-maxs[1]],'max':[maxs[0],maxs[2],-mins[1]]},'meshObjects':1,'materialPrimitives':5,'triangles':sum(len(p.vertices)-2 for o in animal for p in o.data.polygons),'glbBytes':(OUT/'australian-sea-lion-experimental.glb').stat().st_size}
(OUT/'asset-metadata.json').write_text(json.dumps(meta,indent=2))
# Neutral studio render; this floor is not included in GLB.
groundmat=basic('Studio ground',(.25,.285,.29),.85)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,.021));floor=bpy.context.object;floor.name='Presentation ground';floor.data.materials.append(groundmat)
world=scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.62,.69,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45

def area(name,loc,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
area('Large soft key',(2,-3,4),350,3.2,(1,.89,.75));area('Cool fill',(-1,3,2),230,2.5,(.73,.84,1));area('Rim',(-2,-1,3),230,2,(1,.95,.85))
bpy.ops.object.camera_add();cam=bpy.context.object;cam.data.type='ORTHO';scene.camera=cam;cam.data.lens=55
scene.cycles.samples=48
views={'three-quarter':((2.5,-3.3,1.9),2.45,(-.2,0,.56)),'side':((.0,-4,1.0),2.45,(-.2,0,.56)),'front':((4,0,1.5),1.85,(.1,0,.57)),'rear':((-3.5,-2,1.4),2.45,(-.2,0,.56))}
for name,(loc,scale,target) in views.items():
 cam.location=loc;cam.data.ortho_scale=scale;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
cam.location=views['three-quarter'][0];cam.data.ortho_scale=2.45;cam.rotation_euler=(Vector((-.2,0,.56))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'australian-sea-lion-experimental.blend'))
print(json.dumps(meta))
