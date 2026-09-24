"""Original Spinifex hopping mouse study. Blender 5.2+. No external assets.
Usage: blender --background --python build_mouse.py -- --output-dir ./output
Blender +X forward, +Z up; exported GLB uses +Y up.
"""
import bpy, math, random, json, os, sys, argparse
import numpy as np
from mathutils import Vector
from pathlib import Path
random.seed(821)
parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';assets=[]
def basic(name,col,rough=.65):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes.clear();p=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');o=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],o.inputs['Surface']);p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;return m
skin=basic('Sandy tawny fur and pale underside',(.36,.24,.12),.83)
n=skin.node_tree.nodes;l=skin.node_tree.links;p=next(x for x in n if x.type=='BSDF_PRINCIPLED')
geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Normal'],sep.inputs[0])
dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(.78,0,-.7);l.new(geo.outputs['Normal'],dot.inputs[0])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.1;ramp.color_ramp.elements[0].color=(.29,.18,.075,1);ramp.color_ramp.elements[1].position=.6;ramp.color_ramp.elements[1].color=(.77,.72,.59,1);
# Keep head crown tawny: ventral head fur is pale, but the forehead has no mask.
position=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],position.inputs[0]);head=n.new('ShaderNodeMapRange');head.clamp=True;head.interpolation_type='SMOOTHSTEP';head.inputs['From Min'].default_value=.95;head.inputs['From Max'].default_value=1.2;l.new(position.outputs['Z'],head.inputs['Value']);headwhite=n.new('ShaderNodeMath');headwhite.operation='MULTIPLY';headwhite.inputs[1].default_value=-1;l.new(sep.outputs['Z'],headwhite.inputs[0]);mask=n.new('ShaderNodeMixRGB');l.new(head.outputs[0],mask.inputs[0]);l.new(dot.outputs['Value'],mask.inputs[1]);l.new(headwhite.outputs[0],mask.inputs[2]);l.new(mask.outputs[0],ramp.inputs[0])
t=n.new('ShaderNodeTexCoord');vec=n.new('ShaderNodeVectorMath');vec.operation='MULTIPLY';vec.inputs[1].default_value=(45,170,170);l.new(t.outputs['Generated'],vec.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2;noise.inputs['Detail'].default_value=2;l.new(vec.outputs[0],noise.inputs[0])
grain=n.new('ShaderNodeValToRGB');grain.color_ramp.elements[0].position=.23;grain.color_ramp.elements[0].color=(.11,.08,.045,1);grain.color_ramp.elements[1].position=.72;grain.color_ramp.elements[1].color=(1,1,1,1);l.new(noise.outputs['Fac'],grain.inputs[0])
mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.7;l.new(ramp.outputs[0],mix.inputs[1]);l.new(grain.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.35;bump.inputs['Distance'].default_value=.002;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
cream=basic('Ivory guard hairs',(.64,.56,.39),.85)
pink=basic('Warm pink inner ears and feet',(.38,.215,.145),.72)
eye=basic('Glossy near black brown eyes',(.008,.005,.003),.14)
nosemat=basic('Pink brown nose leather',(.30,.135,.09),.47)
dark=basic('Dark fine details',(.052,.032,.016),.65)
def mesh(name,verts,faces,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
 for f in me.polygons:f.use_smooth=True
 assets.append(ob);return ob
def ball(name,loc,scale,mat=skin):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 for f in o.data.polygons:f.use_smooth=True
 assets.append(o);return o
def catmull(points,steps=7):
 rr=[]
 for i in range(len(points)-1):
  a=np.array(points[max(0,i-1)]);b=np.array(points[i]);c=np.array(points[i+1]);d=np.array(points[min(len(points)-1,i+2)])
  for k in range(steps):
   t=k/steps;rr.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 rr.append(np.array(points[-1]));return rr
def loft(name,sections,mat=skin,radial=32,steps=6):
 ss=catmull(sections,steps);vs=[]
 for i,s in enumerate(ss):
  tang=Vector(ss[min(i+1,len(ss)-1)][:3]-ss[max(0,i-1)][:3]).normalized();side=tang.cross(Vector((0,0,1))).normalized()
  if side.length<.1:side=Vector((0,1,0))
  up=tang.cross(side).normalized()
  for j in range(radial):
   a=2*math.pi*j/radial;vs.append(tuple(Vector(s[:3])+side*(s[3]*math.cos(a))+up*(s[4]*math.sin(a))))
 faces=[]
 for i in range(len(ss)-1):
  for j in range(radial):faces.append((i*radial+j,i*radial+(j+1)%radial,(i+1)*radial+(j+1)%radial,(i+1)*radial+j))
 faces.append(tuple(reversed(range(radial))));faces.append(tuple((len(ss)-1)*radial+j for j in range(radial)))
 return mesh(name,vs,faces,mat)
def curve(name,pts,radius,mat=dark):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=5;cu.bevel_depth=radius;cu.bevel_resolution=1
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for i,(p,co) in enumerate(zip(sp.bezier_points,pts)):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=1-.88*i/(len(pts)-1)
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat);assets.append(ob);return ob
# The arched rump and narrow neck are blended into one furred surface.
body=ball('Rump',(-.22,0,.52),(.45,.295,.49));parts=[body,ball('Chest',(.04,0,.87),(.25,.22,.36)),ball('Neck',(.13,0,1.08),(.19,.17,.23)),ball('Head',(.29,0,1.22),(.285,.183,.218)),loft('Tapered muzzle',[(.35,0,1.21,.15,.14),(.48,0,1.16,.119,.105),(.61,0,1.10,.062,.056),(.68,0,1.08,.022,.026)])]
for sg in [-1,1]:
 parts.append(ball('Powerful hind thigh',(-.21,sg*.20,.36),(.25,.17,.26)))
 parts.append(loft('Long folded hind leg',[(-.20,sg*.24,.36,.10,.12),(-.39,sg*.275,.16,.057,.058),(-.28,sg*.29,.083,.047,.043),(.04,sg*.30,.065,.028,.035)]))
 parts.append(loft('Small forearm',[(.14,sg*.14,.96,.048,.064),(.24,sg*.19,.77,.042,.047),(.40,sg*.16,.73,.026,.027)]))
bpy.ops.object.select_all(action='DESELECT')
for ob in parts:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body.data.remesh_voxel_size=.007;bpy.ops.object.voxel_remesh()
sm=body.modifiers.new('Natural anatomical transitions','SMOOTH');sm.factor=.6;sm.iterations=5;bpy.ops.object.modifier_apply(modifier=sm.name)
d=body.modifiers.new('Web geometry budget','DECIMATE');d.ratio=.39;bpy.ops.object.modifier_apply(modifier=d.name)
for f in body.data.polygons:f.use_smooth=True
assets=[body]
# Long delicate toes extend from the narrow hind foot; small hands curl inward.
for sg in [-1,1]:
 loft('Hind foot',[(.015,sg*.30,.068,.026,.035),(.13,sg*.305,.065,.038,.025),(.24,sg*.31,.047,.035,.019),(.29,sg*.31,.039,.012,.008)],pink,24,5)
 for k in range(3):
  y=sg*(.283+k*.027);end=.36-(abs(k-1)*.035)
  loft('Hind toe',[(.21,y,.045,.012,.012),(.29,y,.034,.011,.009),(end,y,.031,.004,.005)],pink,12,4)
  curve('Hind claw',[(end-.012,y,.038),(end+.008,y,.025),(end+.012,y,.022)],.0035,cream)
 ball('Forepaw',(.407,sg*.153,.721),(.042,.033,.026),pink)
 for k in range(4):
  y=sg*(.129+k*.016)
  curve('Forefinger',[(.412,y,.72),(.447,y,.699),(.447,y,.675)],.0075,pink)
  curve('Foreclaw',[(.447,y,.68),(.452,y,.672)],.0025,cream)
 # Tall thin oval pinnae with shallow cupped centers. Mouth of cup faces forwards.
 cx=.125;cy=sg*.146;cz=1.405;vs=[];faces=[];R=48;K=9
 for k in range(K):
  r=k/(K-1)
  for j in range(R):
   a=2*math.pi*j/R
   y=cy+sg*(.135*r*math.cos(a)+.048*r*math.sin(a));z=cz+.215*r*math.sin(a)
   x=cx+.020+.085*r*r-.055*r*math.sin(a)
   vs.append((x,y,z))
 for k in range(K-1):
  for j in range(R):faces.append((k*R+j,k*R+(j+1)%R,(k+1)*R+(j+1)%R,(k+1)*R+j))
 ear=mesh('Cupped inner ear',vs,faces,pink);sol=ear.modifiers.new('Thin ear pinna','SOLIDIFY');sol.thickness=.018
 rimpts=[]
 for j in range(R+1):
  a=2*math.pi*j/R;rimpts.append((cx+.105-.055*math.sin(a),cy+sg*(.135*math.cos(a)+.048*math.sin(a)),cz+.215*math.sin(a)))
 rim=curve('Soft furred ear rim',rimpts,.0075,skin)
 for point in rim.data.splines[0].bezier_points:point.radius=1
 # Eye rims support large lateral eyes instead of human-facing cartoon eyes.
 ball('Eye rim',(.365,sg*.150,1.265),(.079,.047,.079),dark)
 ball('Large dark eye',(.378,sg*.179,1.266),(.065,.032,.067),eye)
 curve('Upper eyelid',[(.324,sg*.177,1.291),(.374,sg*.189,1.332),(.421,sg*.167,1.302)],.006,skin)
 curve('Mouth crease',[(.672,sg*.008,1.056),(.618,sg*.035,1.039),(.561,sg*.056,1.049)],.0018,dark)
 for k in range(12):
  x=.58+(k%4)*.02;y=sg*(.041+(k//4)*.009);z=1.085+(k%3-1)*.015
  length=random.uniform(.29,.43)
  curve('Fine vibrissa',[(x,y,z),(x+.06,y+sg*length*.45,z+.022),(x-.01,y+sg*length,z+random.uniform(-.07,.08))],.0009,cream if k%3==0 else dark)
ball('Nose',(.677,0,1.08),(.032,.032,.022),nosemat)
for sg in [-1,1]:ball('Nostril',(.704,sg*.012,1.082),(.003,.005,.003),dark)
# Long flexible tail ending in a fine dark brush, not a rat's blunt bare tube.
loft('Long tail',[(-.59,0,.33,.040,.04),(-.80,.04,.17,.03,.028),(-1.01,.16,.078,.022,.021),(-1.24,.39,.066,.018,.018),(-1.40,.69,.068,.015,.015),(-1.37,.92,.073,.009,.010),(-1.26,1.05,.085,.003,.004)],pink,28,8)
for i in range(70):
 a=random.uniform(0,2*math.pi);offset=random.uniform(-.04,.03);length=random.uniform(.11,.24)
 curve('Dark tail tuft',[(-1.39+offset,.91+offset,.078),(-1.31+offset+length*.5,1.02+length*.35,.077+math.sin(a)*.025),(-1.25+offset+length,1.10+length*.3,.08+math.sin(a)*.032)],.0013,dark)
# Convert curves and bake fur to ordinary embedded glTF PBR textures.
for ob in list(assets):
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 if ob.type=='CURVE':bpy.ops.object.convert(target='MESH')
 for mod in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
skinobs=[ob for ob in assets if ob.data.materials[0]==skin]
bpy.ops.object.select_all(action='DESELECT')
for ob in skinobs:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.008);bpy.ops.object.mode_set(mode='OBJECT')
for kind in ['BaseColor','Normal']:
 img=bpy.data.images.new('Mouse_'+kind,width=2048,height=2048,alpha=False)
 if kind=='Normal':img.colorspace_settings.name='Non-Color'
 tex=n.new('ShaderNodeTexImage');tex.image=img;n.active=tex;scene.render.bake.margin=10;scene.cycles.samples=8
 if kind=='BaseColor':scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True;bpy.ops.object.bake(type='DIFFUSE')
 else:bpy.ops.object.bake(type='NORMAL')
 img.filepath_raw=str(OUT/('mouse-'+kind.lower()+'.png'));img.file_format='PNG';img.save();img.pack()
col=bpy.data.images['Mouse_BaseColor'];normal=bpy.data.images['Mouse_Normal'];n.clear();p=n.new('ShaderNodeBsdfPrincipled');p.inputs['Roughness'].default_value=.8;o=n.new('ShaderNodeOutputMaterial');l.new(p.outputs[0],o.inputs['Surface']);ct=n.new('ShaderNodeTexImage');ct.image=col;l.new(ct.outputs[0],p.inputs['Base Color']);nt=n.new('ShaderNodeTexImage');nt.image=normal;nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.6;l.new(nt.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal'])
animal=[o for o in scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
for ob in animal:ob.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join();body=bpy.context.object;body.name='Spinifex hopping mouse original';body.data.name='Spinifex hopping mouse mesh'
glb=OUT/'spinifex-hopping-mouse-original.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False)
vs=[body.matrix_world@v.co for v in body.data.vertices];mi=[min(v[i] for v in vs) for i in range(3)];ma=[max(v[i] for v in vs) for i in range(3)]
meta={'commonName':'Spinifex hopping mouse','scientificName':'Notomys alexis','representation':'Original naturalistic procedural study; not a scan or anatomically validated specimen','blenderBounds':{'min':mi,'max':ma},'gltfBounds':{'min':[mi[0],mi[2],-ma[1]],'max':[ma[0],ma[2],-mi[1]]},'triangles':sum(len(f.vertices)-2 for f in body.data.polygons),'glbBytes':glb.stat().st_size,'cameraOrbit':'42deg 78deg 105%','cameraTarget':'-0.30m 0.85m -0.20m','hotspots':{'senses':{'position':[.39,1.27,.205],'normal':[.3,0,.95]},'desert':{'position':[.09,.9,.21],'normal':[.3,0,.95]},'movement':{'position':[.15,.07,.32],'normal':[.2,.5,.8]}}}
(OUT/'asset-metadata.json').write_text(json.dumps(meta,indent=2))
# Save editable asset, then reimport exported GLB for all preview renders.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'spinifex-hopping-mouse-original.blend'))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.ops.import_scene.gltf(filepath=str(glb))
ground=basic('Preview ground',(.31,.35,.36),.9);bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,.007));bpy.context.object.data.materials.append(ground)
scene.world.use_nodes=True;bg=scene.world.node_tree.nodes.get('Background')
if not bg:
 scene.world.node_tree.nodes.clear();bg=scene.world.node_tree.nodes.new('ShaderNodeBackground');wo=scene.world.node_tree.nodes.new('ShaderNodeOutputWorld');scene.world.node_tree.links.new(bg.outputs[0],wo.inputs[0])
bg.inputs[0].default_value=(.62,.68,.73,1);bg.inputs[1].default_value=.55
for name,loc,power,size,color in [('Soft key',(3,-4,5),480,4,(1,.92,.81)),('Cool fill',(-2,3,3),300,3,(.8,.9,1)),('Rim',(-3,-2,4),350,3,(1,.95,.86))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.size=size;o.data.color=color;o.rotation_euler=(Vector((-.2,0,.7))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';scene.cycles.samples=40
views={'three-quarter':((3,-4,2.35),2.65,(-.30,.24,.85)),'side':((0,-5,1.75),2.75,(-.32,.12,.85)),'front':((4,-.2,1.8),2.35,(-.2,.24,.84))}
for name,(loc,scale,target) in views.items():
 cam.location=loc;cam.data.ortho_scale=scale;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/('glb-roundtrip-'+name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(meta))
