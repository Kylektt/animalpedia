"""Original experimental red kangaroo mesh. Blender 5.2, no external assets.
Run: blender --background --python build_kangaroo.py
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
skin=basic('Red-brown and cream short coat',(.28,.24,.18),.68)
n=skin.node_tree.nodes;l=skin.node_tree.links;p=next(x for x in n if x.type=='BSDF_PRINCIPLED')
t=n.new('ShaderNodeTexCoord');geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Normal'],sep.inputs[0])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.12;ramp.color_ramp.elements[0].color=(.57,.44,.29,1);ramp.color_ramp.elements[1].position=.53;ramp.color_ramp.elements[1].color=(.32,.092,.018,1)
# Use local surface up/down and forward-facing normal to blend the female coat.
mathn=n.new('ShaderNodeMath');mathn.operation='MULTIPLY_ADD';mathn.inputs[1].default_value=.5;mathn.inputs[2].default_value=.5;anterior=n.new('ShaderNodeMath');anterior.operation='MULTIPLY';anterior.inputs[1].default_value=-1.5;l.new(sep.outputs['X'],anterior.inputs[0]);coat=n.new('ShaderNodeMath');coat.operation='ADD';l.new(sep.outputs['Z'],coat.inputs[0]);l.new(anterior.outputs[0],coat.inputs[1]);l.new(coat.outputs[0],mathn.inputs[0]);l.new(mathn.outputs[0],ramp.inputs[0])
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
  side=Vector((0,1,0));side=(side-tang*side.dot(tang)).normalized()
  if side.length<.1:side=Vector((1,0,0))
  up=tang.cross(side).normalized()
  for j in range(radial):
   a=2*math.pi*j/radial;pos=Vector(s[:3])+side*(s[3]*math.cos(a))+up*(s[4]*math.sin(a))
   if body:
    # shallow natural neck and shoulder folds, never bead-like rings
    fold=0
    pos+=up*(.006*math.sin(pos.z*95+pos.y*9)*fold*max(0,-math.sin(a)))
    pos.z=max(.032,pos.z)
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

inner=basic('Inner ear soft brown',(.13,.075,.045),.9)
cream=basic('Pale muzzle markings',(.50,.43,.33),.82)
claw=basic('Dark keratin claws',(.037,.025,.017),.56)
body=loft('Continuous torso neck and head',[
(-.42,0,.39,.065,.08),(-.30,0,.55,.20,.22),(-.22,0,.71,.24,.28),(-.08,0,.87,.20,.22),(.055,0,1.015,.15,.18),(.15,0,1.16,.09,.12),(.215,0,1.285,.075,.105),(.245,0,1.37,.087,.107),(.30,0,1.405,.088,.09),(.38,0,1.36,.067,.076),(.46,0,1.305,.047,.049),(.497,0,1.294,.015,.02)],radial=56,steps=6,body=True)
loft('Powerful balancing tail',[(-.32,0,.45,.15,.14),(-.54,0,.305,.12,.10),(-.78,.012,.175,.077,.065),(-1.02,.022,.099,.056,.045),(-1.25,.02,.06,.031,.022),(-1.48,.04,.048,.008,.008)],radial=40,steps=8,body=True)
for sg in [-1,1]:
 # Hind limbs: high muscular thigh, backward-sloping shin, elongated foot.
 loft(('Left' if sg<0 else 'Right')+' hind leg',[(-.23,sg*.16,.72,.14,.18),(-.055,sg*.22,.565,.17,.195),(.05,sg*.235,.425,.12,.115),(-.08,sg*.24,.285,.061,.068),(-.235,sg*.25,.12,.044,.05),(-.18,sg*.255,.067,.035,.032)],radial=44,steps=7)
 loft('Long hind foot',[(-.22,sg*.25,.09,.039,.04),(-.09,sg*.253,.062,.05,.031),(.09,sg*.255,.051,.045,.024),(.26,sg*.258,.047,.031,.019),(.31,sg*.255,.043,.005,.008)],radial=32,steps=6)
 # Dominant fourth toe plus the smaller lateral digit.
 curve('Hind toe crease',[(-.015,sg*.277,.077),(.16,sg*.277,.068),(.265,sg*.272,.059)],.0014,lip)
 loft('Hind foot claw',[(.263,sg*.255,.052,.014,.008),(.32,sg*.252,.04,.011,.008),(.34,sg*.252,.034,.001,.001)],radial=16,steps=4,mat=claw)
 loft('Smaller outer toe',[(.115,sg*.282,.05,.017,.014),(.21,sg*.296,.045,.015,.012),(.244,sg*.295,.043,.002,.002)],radial=20,steps=4)
 # Relaxed small arms, with elbow bend and narrow wrist.
 loft(('Left' if sg<0 else 'Right')+' forearm',[(.075,sg*.12,1.01,.055,.068),(.13,sg*.19,.90,.049,.054),(.13,sg*.19,.79,.04,.037),(.175,sg*.15,.655,.025,.026),(.255,sg*.105,.634,.026,.02)],radial=32,steps=6)
 uvball('Palm',(.267,sg*.098,.624),(.032,.025,.025))
 for k in range(4):
  y=sg*(.078+k*.012)
  curve('Front digit',[(.278,y,.629),(.313,y,.609),(.319,y,.586)],.0065,skin)
  curve('Front claw',[(.319,y,.586),(.317,y,.575),(.309,y,.572)],.0032,claw)
 # Ear: a thick closed lance-shaped shell with a darker inset cupped surface.
 vs=[];fs=[];rows=22;across=14
 for back in [False,True]:
  for i in range(rows):
   t=i/(rows-1);w=.055*math.sin(math.pi*t)**.72+.007*(1-t)
   xc=.238-.045*t;yc=sg*(.063+.065*t);z=1.439+.25*t
   for j in range(across):
    u=-1+2*j/(across-1);x=xc+(.016*u*u-.007 if not back else -.019)
    vs.append((x,yc+u*w,z+.008*(1-u*u)))
 for back in range(2):
  off=back*rows*across
  for i in range(rows-1):
   for j in range(across-1):
    f=(off+i*across+j,off+(i+1)*across+j,off+(i+1)*across+j+1,off+i*across+j+1)
    fs.append(tuple(reversed(f)) if back else f)
 for i in range(rows-1):
  for j in [0,across-1]:
   a=i*across+j;b=(i+1)*across+j;fs.append((a,b,b+rows*across,a+rows*across))
 for i in [0,rows-1]:
  for j in range(across-1):
   a=i*across+j;fs.append((a,a+1,a+1+rows*across,a+rows*across))
 mesh('Upright ear shell',vs,fs,skin)
 iv=[];iff=[]
 for i in range(17):
  t=.11+.78*i/16;w=.038*math.sin(math.pi*t)**.9
  for j in range(10):
   u=-1+2*j/9;iv.append((.238-.045*t+.009*u*u-.005,sg*(.063+.065*t)+u*w,1.439+.25*t+.008*(1-u*u)))
 for i in range(16):
  for j in range(9):iff.append((i*10+j,(i+1)*10+j,(i+1)*10+j+1,i*10+j+1))
 mesh('Inner ear cup',iv,iff,inner)
 # Small almond eyes, bony brow, pale cheek and lip stripe.
 uvball('Eye',(.335,sg*.080,1.37),(.025,.016,.016),eye)
 curve('Upper eyelid',[(.309,sg*.083,1.374),(.33,sg*.094,1.388),(.354,sg*.078,1.376)],.0038,skin)
 curve('Lower eyelid',[(.309,sg*.082,1.369),(.332,sg*.094,1.354),(.354,sg*.078,1.376)],.0027,skin)
 curve('Closed mouth',[(.496,sg*.005,1.278),(.46,sg*.034,1.266),(.406,sg*.049,1.266)],.002,lip)
 for k in range(5):
  y=sg*(.035+k*.003);x=.456-k*.006;z=1.287+(k%2)*.009
  curve('Fine facial vibrissa',[(x,y,z),(x+.01,y+sg*.025,z+.003),(x-.02,y+sg*.065,z-.012)],.0006,whiskmat)
uvball('Nasal leather',(.497,0,1.297),(.023,.037,.023),nosemat)
for sg in [-1,1]:uvball('Nostril',(.513,sg*.022,1.30),(.007,.009,.005),lip)
curve('Philtrum',[(.517,0,1.29),(.505,0,1.278),(.491,0,1.274)],.0015,lip)

# Convert curves, blend original skin meshes, unwrap and bake portable textures.
meshassets=[]
for ob in list(assets):
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 if ob.type=='CURVE':bpy.ops.object.convert(target='MESH')
 for mod in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
 meshassets.append(ob)
skinobs=[ob for ob in meshassets if ob.data.materials[0]==skin]
bpy.ops.object.select_all(action='DESELECT')
for ob in skinobs:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object
body.data.remesh_voxel_size=.004;bpy.ops.object.voxel_remesh()
sm=body.modifiers.new('Sculpt relaxation','SMOOTH');sm.factor=.4;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
mod=body.modifiers.new('Web budget','DECIMATE');mod.ratio=.15;bpy.ops.object.modifier_apply(modifier=mod.name)
for poly in body.data.polygons:poly.use_smooth=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
for kind in ['BaseColor','Normal']:
 img=bpy.data.images.new('Kangaroo_'+kind,width=2048,height=2048,alpha=False)
 if kind=='Normal':img.colorspace_settings.name='Non-Color'
 tex=n.new('ShaderNodeTexImage');tex.image=img;n.active=tex;scene.render.bake.margin=12;scene.cycles.samples=8
 if kind=='BaseColor':
  scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True;bpy.ops.object.bake(type='DIFFUSE')
 else:bpy.ops.object.bake(type='NORMAL')
 img.filepath_raw=str(OUT/('kangaroo-'+kind.lower()+'.png'));img.file_format='PNG';img.save();img.pack()
col=bpy.data.images['Kangaroo_BaseColor'];norm=bpy.data.images['Kangaroo_Normal'];n.clear()
p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=.76;out=n.new('ShaderNodeOutputMaterial');l.new(p.outputs['BSDF'],out.inputs['Surface'])
ct=n.new('ShaderNodeTexImage');ct.image=col;l.new(ct.outputs['Color'],p.inputs['Base Color'])
nt=n.new('ShaderNodeTexImage');nt.image=norm;nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.55;l.new(nt.outputs['Color'],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal'])
animal=[o for o in scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
for ob in animal:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object;body.name='Red kangaroo experimental';body.data.name='Red kangaroo mesh';animal=[body]
bpy.ops.export_scene.gltf(filepath=str(OUT/'red-kangaroo-experimental.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False)
verts=[body.matrix_world@v.co for v in body.data.vertices];mins=[min(v[i] for v in verts) for i in range(3)];maxs=[max(v[i] for v in verts) for i in range(3)]
meta={'scientificName':'Osphranter rufus','representation':'Original experimental adult male; no anatomical scan; not expert validated','blenderBounds':{'min':mins,'max':maxs},'gltfBounds':{'min':[mins[0],mins[2],-maxs[1]],'max':[maxs[0],maxs[2],-mins[1]]},'triangles':sum(len(p.vertices)-2 for p in body.data.polygons),'glbBytes':(OUT/'red-kangaroo-experimental.glb').stat().st_size,'meshObjects':1}
(OUT/'asset-metadata.json').write_text(json.dumps(meta,indent=2))
# Reimport the exported GLB before every inspection render.
bpy.data.objects.remove(body,do_unlink=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'red-kangaroo-experimental.glb'))
groundmat=basic('Studio ground',(.25,.285,.29),.85)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,.025));floor=bpy.context.object;floor.name='Presentation ground';floor.data.name='Studio floor';floor.data.materials.append(groundmat)
world=scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.62,.69,1);world.node_tree.nodes['Background'].inputs[1].default_value=.45

def area(name,loc,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc);ob=bpy.context.object;ob.name=name;ob.data.energy=power;ob.data.shape='DISK';ob.data.size=size;ob.data.color=color;ob.rotation_euler=(Vector((-.2,0,.8))-ob.location).to_track_quat('-Z','Y').to_euler()
area('Large soft key',(2,-3,4),350,3.2,(1,.89,.75));area('Cool fill',(-1,3,2),230,2.5,(.73,.84,1));area('Rim',(-2,-1,3),230,2,(1,.95,.85))
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Inspection camera';cam.data.type='ORTHO';scene.camera=cam;scene.cycles.samples=48
views={'three-quarter':((2.8,-4,2.1),2.55,(-.35,0,.91)),'side':((0,-4,1.2),2.55,(-.35,0,.9)),'front':((4,0,1.8),2.25,(.0,0,.91))}
for name,(loc,scale,target) in views.items():
 cam.location=loc;cam.data.ortho_scale=scale;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
cam.location=views['three-quarter'][0];cam.data.ortho_scale=2.55;cam.rotation_euler=(Vector((-.35,0,.91))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'red-kangaroo-experimental.blend'))
print(json.dumps(meta))
