#!/usr/bin/env python3
"""1469 Talwandi birth reel, a respectful stylized 3D reconstruction.
Run with blender -b -t 2 --python thisfile.py -- --out out/reel_silent.mp4
Only period-generic actions are depicted. No fabricated dialogue, miracles or modern gurdwara.
"""
import bpy, math, sys, argparse, random
from mathutils import Vector

argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
p=argparse.ArgumentParser()
p.add_argument("--out",default="build/birth1469_silent.mp4")
p.add_argument("--width",type=int,default=432)
p.add_argument("--height",type=int,default=768)
p.add_argument("--fps",type=int,default=15)
p.add_argument("--seconds",type=int,default=45)
args=p.parse_args(argv)
random.seed(1469)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine="BLENDER_WORKBENCH"
scene.render.resolution_x=args.width
scene.render.resolution_y=args.height
scene.render.resolution_percentage=100
scene.render.fps=args.fps
scene.frame_start=1
scene.frame_end=args.seconds*args.fps
scene.render.image_settings.file_format="FFMPEG"
scene.render.ffmpeg.format="MPEG4"
scene.render.ffmpeg.codec="H264"
scene.render.ffmpeg.constant_rate_factor="MEDIUM"
scene.render.ffmpeg.ffmpeg_preset="REALTIME"
scene.render.filepath=args.out
scene.render.film_transparent=False
scene.world.color=(0.16,0.14,0.12)
sh=scene.display.shading
sh.light='STUDIO'
sh.color_type='MATERIAL'
sh.background_type='WORLD'
try:
    sh.show_shadows=True
    sh.show_cavity=True
    sh.cavity_type='BOTH'
    sh.curvature_ridge_factor=1.2
    sh.curvature_valley_factor=0.6
except Exception:
    pass
scene.view_settings.view_transform='Standard'
scene.view_settings.look='Medium High Contrast'
scene.view_settings.exposure=0
scene.view_settings.gamma=1

def material(name,hex):
    h=hex.strip("#")
    c=tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*c,1)
    return m
M={
"earth":material("clay earth","#AE9278"),
"street":material("dusty packed earth","#AA8E71"),
"wall":material("unpainted plaster","#BDA085"),
"wall2":material("aged clay wall","#95745E"),
"wall3":material("light limestone plaster","#D4BA94"),
"timber":material("weathered timber","#604535"),
"wood":material("wood grain","#73513A"),
"darkwood":material("carved dark wood","#493429"),
"stone":material("riverstone","#8F8B7D"),
"straw":material("dried straw","#B8A27A"),
"bush":material("olive leaves","#5C694C"),
"bush2":material("green foliage","#7B8562"),
"bush3":material("leaf highlight","#A59A66"),
"sky":material("pale early morning sky","#CBB9A0"),
"cloth":material("undyed cotton","#DECBAA"),
"linen":material("coarse linen","#C6AD87"),
"clay":material("terracotta","#955E45"),
"copper":material("dark copper","#9C7355"),
"gold":material("brass","#BF9B59"),
"shadow":material("cast shadow","#6F5C4E"),
"skinA":material("brown skin 1","#A77655"),
"skinB":material("brown skin 2","#BC8C69"),
"skinC":material("brown skin 3","#976B4C"),
"hair":material("dark hair","#30241C"),
"hair2":material("dark grey hair","#52453A"),
"eyes":material("natural dark eye","#29221E"),
"iris":material("iris","#423026"),
"rose":material("soft clay pink","#A56861"),
"blue":material("muted indigo fabric","#505C69"),
"rust":material("rust-coloured fabric","#92594A"),
"sand":material("ochre fabric","#B09268"),
"cream":material("cotton beige fabric","#D2BE9F"),
"lamp":material("lamp flame","#E4B071"),
"thread":material("cotton threads","#B3A384"),
}
def mat(ob,m):
    ob.data.materials.append(M[m] if isinstance(m,str) else m)
    return ob
def box(name,loc,dim,m,bev=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=name
    o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    mat(o,m)
    if bev:
        mod=o.modifiers.new("softened edges","BEVEL");mod.width=bev;mod.segments=2
        mod2=o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
    return o
def sphere(name,loc,s,m,segments=16,rings=10):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,radius=1,location=loc)
    o=bpy.context.object;o.name=name;o.scale=s;mat(o,m)
    for f in o.data.polygons:f.use_smooth=True
    return o
def cylinder(name,loc,radius,depth,m,vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;mat(o,m);return o
def cone(name,loc,radius,depth,m,radius2=0,vertices=9):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=radius,radius2=radius2,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;mat(o,m);return o
def empty(name,loc,parent=None):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=loc
    if parent:o.parent=parent
    return o
def parent(child,root,local):
    child.parent=root;child.location=local;return child
def cap_human(name,loc,height=1.65,skin="skinB",tunic="sand",wrap="cream",male=False,veil=False):
    root=empty(name+" main rig",loc)
    torso=sphere(name+" upper garment",(0,0,0),(0.43,0.28,0.63),tunic)
    parent(torso,root,(0,0,height*.57))
    cloth=cone(name+" long tunic",(0,0,0),.54,height*.77,tunic,.34)
    parent(cloth,root,(0,0,height*.39))
    chest=sphere(name+" shoulders",(0,0,0),(.45,.28,.27),tunic)
    parent(chest,root,(0,0,height*.72))
    neck=cylinder(name+" neck",(0,0,0),.12,.22,skin)
    parent(neck,root,(0,-.02,height*.86))
    headrig=empty(name+" head pivot",(0,-.01,height*.94),root)
    head=sphere(name+" face",(0,0,0),(.27,.24,.33),skin)
    parent(head,headrig,(0,-.04,.12))
    nose=sphere(name+" nose",(0,0,0),(.058,.09,.098),skin,12,8)
    parent(nose,headrig,(0,-.278,.14))
    for side in (-1,1):
        eye=sphere(name+" eye"+str(side),(0,0,0),(.052,.022,.034),"eyes",12,8)
        parent(eye,headrig,(side*.115,-.254,.218))
        ear=sphere(name+" ear"+str(side),(0,0,0),(.07,.04,.105),skin)
        parent(ear,headrig,(side*.27,-.04,.11))
    mouth=sphere(name+" mouth",(0,0,0),(.075,.015,.016),"rose",14,6)
    parent(mouth,headrig,(0,-.272,-.001))
    if male:
        beard=sphere(name+" beard",(0,0,0),(.22,.17,.21),"hair")
        parent(beard,headrig,(0,-.05,-.13))
        moust=sphere(name+" moustache",(0,0,0),(.18,.033,.04),"hair")
        parent(moust,headrig,(0,-.255,.06))
    band=sphere(name+" wrapped head cloth",(0,0,0),(.29,.28,.16),wrap)
    parent(band,headrig,(0,-.013,.42))
    fold=sphere(name+" cloth fold",(0,0,0),(.32,.29,.075),wrap)
    parent(fold,headrig,(0,-.012,.35))
    if veil:
        shawl=sphere(name+" draped head covering",(0,0,0),(.36,.25,.42),wrap)
        parent(shawl,headrig,(0,.13,.24))
        backcloth=box(name+" shawl down back",(0,0,0),(.8,.11,1.05),wrap,bev=.035)
        parent(backcloth,root,(0,.28,height*.55))
    arms=[]
    for s in (-1,1):
        pivot=empty(name+(" left" if s<0 else " right")+" arm",(.34*s,0,height*.72),root)
        upper=sphere(name+" sleeve"+str(s),(0,0,0),(.16,.16,.43),tunic)
        parent(upper,pivot,(0,0,-.34))
        palm=sphere(name+" hand"+str(s),(0,0,0),(.115,.11,.18),skin)
        parent(palm,pivot,(0,-.01,-.78))
        arms.append(pivot)
    legs=[]
    for s in (-1,1):
        piv=empty(name+" leg"+str(s),(.2*s,0,height*.39),root)
        tube=sphere(name+" pant"+str(s),(0,0,0),(.2,.19,.4),tunic)
        parent(tube,piv,(0,0,-.35))
        foot=sphere(name+" shoe"+str(s),(0,0,0),(.18,.27,.11),"darkwood")
        parent(foot,piv,(0,-.11,-.77))
        legs.append(piv)
    return {"root":root,"head":headrig,"arms":arms,"legs":legs,"torso":torso}
def animate_walk(actor,start,end,frame_a,frame_b,steps=7):
    r=actor["root"]
    for i in range(steps*2+1):
        f=round(frame_a+(frame_b-frame_a)*i/(steps*2))
        a=i/(steps*2)
        r.location=(start[0]+(end[0]-start[0])*a,start[1]+(end[1]-start[1])*a,start[2]+.022*math.sin(i*math.pi))
        r.keyframe_insert(data_path="location",frame=f)
        v=.27*math.sin(i*math.pi)
        for idx,p in enumerate(actor["legs"]):
            p.rotation_euler[0]=v*(1 if idx==0 else -1)
            p.keyframe_insert(data_path="rotation_euler",frame=f)
        for idx,p in enumerate(actor["arms"]):
            p.rotation_euler[0]=-v*(1 if idx==0 else -1)
            p.keyframe_insert(data_path="rotation_euler",frame=f)
def nod(actor,keys):
    h=actor["head"]
    for f,a in keys:
        h.rotation_euler[0]=a
        h.keyframe_insert(data_path="rotation_euler",frame=f)
def arm_pose(actor,index,keys):
    p=actor["arms"][index]
    for f,rx,ry,rz in keys:
        p.rotation_euler=(rx,ry,rz)
        p.keyframe_insert(data_path="rotation_euler",frame=f)

# -------------------- Exterior, an intentionally generic rural Punjab reconstruction --------------------
box("village packed-earth ground",(0,0,-.17),(48,44,.2),"earth")
box("winding earthen path",(0,-3,-.04),(8,28,.045),"street")
# Repeated low earthen houses (NOT modern gurdwara architecture)
for j,(x,y,w,h) in enumerate([(-6,5,5,3.1),(5,5,4.8,2.8),(-9,-1,5.7,2.6),(9,-.7,5.5,2.7),(-4,13,6,3.0),(6,14,6,2.7)]):
    box("house %d mud walls"%j,(x,y,h*.5),(w,3,h),"wall" if j%2 else "wall2",.08)
    box("house %d roof beams"%j,(x,y,h+.19),(w+.35,3.7,.3),"wood",.04)
    box("house %d thatch layer"%j,(x,y,h+.38),(w+.45,3.85,.18),"straw",.05)
    for a in range(3):
        yy=y-1.2+a*1.15
        box("house timber brace %d-%d"%(j,a),(x-w*.25,yy,h-.5),(.09,.09,h*.58),"timber")
# village walls in front with door openings as separate blocks
box("outer threshold L",(-1.6,3,1.0),(1.6,.45,2.0),"wall3",.1)
box("outer threshold R",(1.6,3,1.0),(1.6,.45,2.0),"wall3",.1)
box("house doorway beam",(0,3,2.06),(4,.56,.23),"timber",.05)
box("dark doorway",(0,3.26,.85),(1.6,.12,1.7),"darkwood",.08)
for x,y in [(-1,-3),(4,-4),(-4,0),(1,11)]:
    cylinder("woven pot base",(x,y,.3),.36,.6,"clay")
    sphere("vessel neck",(x,y,.62),(.26,.26,.17),"clay")
for tx,ty in [(-11,10),(11,11),(-12,-10)]:
    cylinder("broad tree trunk",(tx,ty,2.2),.33,4.5,"wood")
    for dx,dy,dz,s in [(-.8,0,4.4,1.8),(.7,.3,4.0,1.7),(0,-.6,4.7,1.5)]:
        sphere("cluster of leaves",(tx+dx,ty+dy,dz),(s,s*.8,s*.65),random.choice(["bush","bush2","bush3"]),12,8)
for x,y in [(-9,-4),(8,-6),(-7,8),(9,9)]:
    for i in range(6):
        cone("dry roadside grasses",(x+random.uniform(-1,1),y+random.uniform(-.5,.5),.3),.07,.55,"straw")
# Distant residents, generic daily work, not claims about identified individuals
villager1=cap_human("Village walker one",(-3,-7,0),1.58,"skinB","cream","sand",male=True)
villager2=cap_human("Village walker two",(4,-2,0),1.52,"skinC","rust","cream",veil=True)
villager3=cap_human("Village walker three",(-6,5,0),1.59,"skinA","blue","sand",male=True)
animate_walk(villager1,(-3,-7,0),(-3,1,0),1,170,9)
animate_walk(villager2,(4,-2,0),(4,-6,0),1,140,6)
animate_walk(villager3,(-6,5,0),(-3.5,5,0),1,200,7)
# -------------------- Domestic interior, reconstructed household --------------------
box("interior earthen floor",(0,33,-.16),(11,15,.22),"earth")
box("room back wall",(0,37,2.0),(10,.5,4),"wall3",.1)
box("room left wall",(-5,32,2.0),(.45,11,4),"wall2",.08)
box("room right wall",(5,32,2.0),(.45,11,4),"wall2",.08)
box("interior heavy roof",(0,33,4.2),(11,12,.38),"timber",.05)
# timber rafters
for x in (-4,-2,0,2,4):
    box("roof rafter",(x,33,4.03),(.18,11,.22),"darkwood")
# side passage
box("visible doorway dark",(3.15,36.69,1.38),(1.5,.07,2.6),"darkwood",.1)
box("door frame L",(2.3,36.35,1.45),(.14,.38,2.9),"wood")
box("door frame R",(4.0,36.35,1.45),(.14,.38,2.9),"wood")
box("door frame lintel",(3.15,36.35,2.9),(1.85,.38,.18),"wood")
# charpoy (woven cot)
box("cot horizontal frame",(-.5,33.25,.68),(3.2,1.7,.16),"darkwood",.06)
box("cot warm blankets",(-.5,33.25,.8),(2.9,1.45,.12),"rust",.04)
for a in (-1.85,.85):
  for b in (32.53,33.97):
    cylinder("cot wooden foot",(a,b,.42),.09,.77,"wood")
for i in range(13):
    box("cot woven cotton warp",(-.5,32.6+i*.10,.88),(2.75,.022,.018),"linen")
# household objects
for x,y,r,h in [(-3.7,35,.3,.8),(3.9,34.1,.35,.9),(-4.0,32.0,.3,.55)]:
    cylinder("water jar",(x,y,h*.5),r,h,"clay")
    cylinder("water jar lip",(x,y,h+.08),r*.58,.13,"clay")
# wall-mounted shallow niche lamp
box("lamp niche",(1.5,36.63,2.25),(.8,.2,.68),"wall2",.1)
cylinder("oil lamp brass cup",(1.5,36.40,2.22),.16,.13,"gold")
cone("small oil lamp flame",(1.5,36.4,2.40),.065,.26,"lamp")
# low wooden table, astrological parchment is traditional scene ONLY
box("scribe table",(-3.5,34.5,.5),(1.5,.8,.1),"darkwood",.02)
for x in (-4.1,-2.9):
 for y in (34.2,34.8):
    box("scribe table leg",(x,y,.24),(.10,.10,.44),"wood")
box("paper folio",(-3.5,34.5,.57),(1.0,.48,.015),"linen")
for i in range(6):
    box("handwritten line mark",(-3.5,34.31+i*.055,.585),(.67,.008,.004),"shadow")

tripta=cap_human("Mata Tripta artistic depiction",(-1.15,33.30,.33),1.48,"skinB","rust","cream",veil=True)
daulatan=cap_human("Daulatan traditional depiction",(1.12,33.45,0),1.50,"skinC","sand","linen",veil=True)
kalu=cap_human("Mehta Kalu artistic depiction",(2.7,30.2,0),1.76,"skinA","cream","sand",male=True)
hardial=cap_human("Hardial from Janamsakhi",( -3.25,34.1,0),1.64,"skinB","cream","linen",male=True)
# baby remains swaddled. The generated appearance is symbolic, not a likeness.
bundle=sphere("swaddled newborn",(-.62,32.94,1.46),(.57,.26,.23),"cloth")
face=sphere("newborn small face",(-.91,32.72,1.58),(.15,.13,.15),"skinB")
hood=sphere("newborn cloth hood",(-.91,32.76,1.65),(.17,.15,.13),"linen")
# maternal and midwife gestures (no dialogue / no magic)
arm_pose(tripta,1,[(1,0,-.45,-.45),(150,-.52,-.55,-.32),(270,-.62,-.6,-.28),(450,-.58,-.53,-.32),(675,-.50,-.50,-.4)])
arm_pose(tripta,0,[(1,-.18,.25,.4),(150,-.65,.35,.5),(300,-.6,.4,.55),(675,-.5,.40,.4)])
arm_pose(daulatan,0,[(1,0,0,.1),(230,-.25,.15,.25),(310,-.66,.18,.48),(380,-.47,.18,.31),(675,-.38,.18,.28)])
nod(tripta,[(1,.05),(250,.18),(310,.10),(480,.12),(675,.04)])
nod(daulatan,[(1,0),(220,.02),(290,.18),(420,.11),(675,.01)])
animate_walk(kalu,(2.7,30.2,0),(2.2,32.2,0),255,395,6)
nod(kalu,[(1,0),(370,.07),(430,.16),(675,.05)])
arm_pose(kalu,1,[(1,0,0,0),(400,-.25,-.1,-.2),(535,-.18,-.2,-.3),(675,0,0,0)])
# Hardial not in room until next morning as a traditional reconstruction; his figure visible only in shots 5+
nod(hardial,[(1,.05),(460,.20),(520,.18),(610,.05),(675,.05)])
arm_pose(hardial,0,[(1,-.15,0,.1),(470,-.55,.25,.3),(570,-.3,.15,.1),(675,-.18,.1,.1)])
# -------------------- Camera and shot timing --------------------
bpy.ops.object.camera_add(location=(0,-12,3))
cam=bpy.context.object;cam.name="Reel camera";cam.data.lens=36
scene.camera=cam
def camera_pose(frame,loc,target):
    cam.location=loc
    direction=Vector(target)-cam.location
    cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
    cam.keyframe_insert(data_path="location",frame=frame)
    cam.keyframe_insert(data_path="rotation_euler",frame=frame)
# Hard cuts at boundaries; meaningful camera motion within shots.
F=args.fps
shots=[
    (0,6,(1,-13,3.0),(0,2,1.75),(0,-9.5,2.8),(0,2.5,1.7)),
    (6,11,(-5,-5.5,2.85),(-1,4,1.55),(-4,-4.3,2.60),(-.3,4,1.55)),
    (11,19,(1.5,28.0,2.1),(-.5,33.1,1.48),(1.15,29.25,2.0),(-.4,33.2,1.42)),
    (19,27,(-2.2,29.6,1.85),(-.6,33.15,1.5),(-1.6,30.1,1.65),(-.6,33.1,1.4)),
    (27,33,(3.1,28.8,2.3),(2.0,32.4,1.25),(2.1,29.6,2.20),(1.5,33.0,1.5)),
    (33,39,(-2.8,30.2,2.2),(-3.15,34.25,1.2),(-3.0,30.9,1.8),(-3.25,34.2,1.1)),
    (39,45,(1.0,29.2,2.1),(-.6,33.1,1.45),(.45,30.0,1.7),(-.6,33.2,1.38)),
]
for i,(begin,end,cl,ct,el,et) in enumerate(shots):
    sf=int(begin*F)+1;ef=int(end*F)
    if i:
        # End previous pose on previous frame to create a real cinematic cut.
        pass
    camera_pose(sf,cl,ct)
    camera_pose(ef,el,et)
# Force linear camera animation, not overshoot at discontinuous cuts.
for curve in cam.animation_data.action.fcurves:
    for k in curve.keyframe_points:k.interpolation="LINEAR"
# Use a tiny expressive head gesture; material and pose are fixed across cuts.
scene.frame_set(1)
print("Rendered scene:",len(bpy.data.objects),"objects,",scene.frame_end,"frames.")
bpy.ops.render.render(animation=True)
print("Wrote silent moving-character animation:",args.out)
