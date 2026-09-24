"""Check the portable mouse asset structure without optional packages."""
import json, struct, hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
path=root/'spinifex-hopping-mouse-original.glb';raw=path.read_bytes()
magic,version,total=struct.unpack_from('<4sII',raw,0)
assert magic==b'glTF' and version==2 and total==len(raw)
size,kind=struct.unpack_from('<II',raw,12);assert kind==0x4E4F534A
doc=json.loads(raw[20:20+size]);assert not doc.get('extensionsRequired')
assert all('uri' not in image and 'bufferView' in image for image in doc['images'])
assert all('uri' not in buffer for buffer in doc['buffers'])
assert not doc.get('animations') and not doc.get('cameras')
triangles=sum(doc['accessors'][p['indices']]['count']//3 for m in doc['meshes'] for p in m['primitives'])
assert triangles<=150000 and len(raw)<=15000000
textured=[m for m in doc['materials'] if 'baseColorTexture' in m.get('pbrMetallicRoughness',{})]
assert textured and all('normalTexture' in m for m in textured)
report={'glbVersion':version,'embeddedImages':len(doc['images']),'externalURIs':0,'meshCount':len(doc['meshes']),'materialCount':len(doc['materials']),'triangles':triangles,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'glbReimportPreviewFiles':[str(p.name) for p in sorted(root.glob('glb-roundtrip-*.png'))]}
(root/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
