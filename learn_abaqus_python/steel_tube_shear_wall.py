#coding=utf-8
from abaqus import *
from abaqusConstants import *
from caeModules import *
import math
parameter=(('Model Name:','Model-NewShearWall'),('Cover(mm):','20'),('Length(wall)(mm):','1000'),('Thickness(wall)(mm):','200'),('Height(wall)(mm):','2000'),
	('Diameter(tube)(mm):','114'),('Thickness(tube)(mm):','4'),('Diameter(longitudinal bar)(mm):','10'),('Diameter(transversal bar)(mm):','6'),
	('Length(foundation)(mm):','3500'),('Thickness(foundation)(mm):','500'),('Height(foundation)(mm):','500'),
    ('Length(loadbeam)(mm):','1200'),('Thickness(loadbeam)(mm):','250'),('Height(loadbeam)(mm):','250'),
	('Yield stress(longitudinal bar)(N/mm):','400'),('Yield stress(transversal bar)(N/mm):','500'),('Yield stress(tube)(N/mm):','325'),
	('Displacement(maximum)(mm):','35'),('axial-load(KN):','3450000'),('offset(tube1)(mm):','400'),
	('offset(tube2)(mm):','230'),('Space between transversal bar','100'),('Mesh Size(mm):','50'),('Job Name:','Job-NewShearWall-01'))

modelname,cover,lwall,twall,hwall,dtube,ttube,dlbar,dtbar,lfd,tfd,hfd,lbl,tbl,hbl,fylbar,fytbar,fytube,dis,axld,offset1,offset2,space,meshsize,jobname=getInputs(fields=parameter,
	label='Please Input The Parameter',dialogTitle='Parameter Input')

viewportshow=session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=500,height=200)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
myModel=mdb.Model(name=modelname)
cover=float(cover)
lwall=float(lwall)
twall=float(twall)
hwall=float(hwall)
dtube=float(dtube)
ttube=float(ttube)
dlbar=float(dlbar)
dtbar=float(dtbar) 
lfd=float(lfd)
tfd=float(tfd)
hfd=float(hfd)
lbl=float(lbl)
tbl=float(tbl)
hbl=float(hbl)
fylbar=float(fylbar)
fytbar=float(fytbar)
fytube=float(fytube)
dis=float(dis)
axld=float(axld)
offset1=float(offset1)
offset2=float(offset2)
meshsize=float(meshsize)
space=float(space)

#part
##wall
s = myModel.ConstrainedSketch(name='A',sheetSize=lwall)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lwall/2, -twall/2), point2=(lwall/2, twall/2))
s.CircleByCenterPerimeter(center=(-offset1, 0), point1=(-offset1+dtube/2, 0))
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1+dtube/2, 0))
s.CircleByCenterPerimeter(center=(-offset2, 0), point1=(-offset2+dtube/2, 0))
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2+dtube/2, 0))
partwall = myModel.Part(name='wall', dimensionality=THREE_D,type=DEFORMABLE_BODY)
partwall = myModel.parts['wall']
partwall.BaseSolidExtrude(sketch=s, depth=hwall)
p = mdb.models['Model-NewShearWall'].parts['wall']
d = p.datums
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-lwall/2+cover)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=lwall/2-cover)
p.DatumPlaneByPrincipalPlane( principalPlane=XZPLANE, offset=-twall/2+cover)
p.DatumPlaneByPrincipalPlane( principalPlane=XZPLANE, offset=twall/2-cover)

p = mdb.models['Model-NewShearWall'].parts['wall']
c = p.cells
pickedCells = c.findAt(((1, 1, 1), ))
d = p.datums
p.PartitionCellByDatumPlane(datumPlane=d[5], cells=pickedCells)
pickedCells = c.findAt(((1, 1, 1), ))
p.PartitionCellByDatumPlane(datumPlane=d[4], cells=pickedCells)
pickedCells = c.findAt(((1, 1, 1), ))
p.PartitionCellByDatumPlane(datumPlane=d[3], cells=pickedCells)
pickedCells = c.findAt(((1, 1, 1), ))
p.PartitionCellByDatumPlane(datumPlane=d[2], cells=pickedCells)

##tube
s = myModel.ConstrainedSketch(name='A',sheetSize=dtube)
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube/2-ttube, 0)) 
parttube = myModel.Part(name='tube', dimensionality=THREE_D,type=DEFORMABLE_BODY)
parttube = myModel.parts['tube']
parttube.BaseSolidExtrude(sketch=s,depth=hwall+hbl+hfd)

##in-con
s = myModel.ConstrainedSketch(name='A',sheetSize=dtube)
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0, 0), point1=(dtube/2-ttube, 0)) 
partincon = myModel.Part(name='in-concrete', dimensionality=THREE_D,type=DEFORMABLE_BODY)
partincon = myModel.parts['in-concrete']
partincon.BaseSolidExtrude(sketch=s,depth=hwall+hbl+hfd)

##fd-con
s = myModel.ConstrainedSketch(name='A',sheetSize=lfd)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lfd/2, -tfd/2), point2=(lfd/2, tfd/2)) 
s.CircleByCenterPerimeter(center=(-offset1, 0), point1=(-offset1+dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1+dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(-offset2, 0), point1=(-offset2+dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2+dtube/2, 0)) 
partfoundation = myModel.Part(name='foundation', dimensionality=THREE_D,type=DEFORMABLE_BODY)
partfoundation = myModel.parts['foundation']
partfoundation.BaseSolidExtrude(sketch=s,depth=hfd)

##lb-con
s = myModel.ConstrainedSketch(name='A',sheetSize=lbl)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-lbl/2, -tbl/2), point2=(lbl/2, tbl/2)) 
s.CircleByCenterPerimeter(center=(-offset1, 0), point1=(-offset1+dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(offset1, 0), point1=(offset1+dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(-offset2, 0), point1=(-offset2+dtube/2, 0)) 
s.CircleByCenterPerimeter(center=(offset2, 0), point1=(offset2+dtube/2, 0)) 
partloadbeam = myModel.Part(name='loadbeam', dimensionality=THREE_D,type=DEFORMABLE_BODY)
partloadbeam = myModel.parts['loadbeam']
partloadbeam.BaseSolidExtrude(sketch=s,depth=hbl)

##rebar
s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(hwall-2*cover, 0.0))
p = myModel.Part(name='lsteel', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['lsteel']
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(lfd-2*cover, 0.0))
p = myModel.Part(name='f-lsteel', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['f-lsteel']
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(0, 0), point2=(hfd-2*cover, tfd/2+dtube/2))
p = myModel.Part(name='f-hoop', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['f-hoop']
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(0.0, 0.0), point2=(lbl-2*cover, 0.0))
p = myModel.Part(name='l-lsteel', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['l-lsteel']
p.BaseWire(sketch=s)

s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-(tbl/2-cover),-(hbl/2-cover)), point2=((tbl/2-cover),(hbl/2-cover)))
p = myModel.Part(name='l-hoop', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['l-hoop']
p.BaseWire(sketch=s)


#size def
hooplength=float(offset1-offset2)
hoopwidth=float(twall-2*cover)
hooplength2=float(3*offset2/2-offset1/2)

##hoop
s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-hooplength/2, -hoopwidth/2), point2=(hooplength/2, hoopwidth/2))
p = myModel.Part(name='hoop1', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['hoop1']
p.BaseWire(sketch=s)

##hoop
s = myModel.ConstrainedSketch(name='A',sheetSize=3000)
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-hooplength2/2, -hoopwidth/2), point2=(hooplength2/2, hoopwidth/2))
p = myModel.Part(name='hoop2', dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = myModel.parts['hoop2']
p.BaseWire(sketch=s)

#material,need revise
a=mdb.models['Model-NewShearWall']
a.Material(name='in-concrete')
a.materials['in-concrete'].Elastic(table=((37500.0, 0.2), ))
a.materials['in-concrete'].Density(table=((2.5e-09, ), ))
a.Material(name='out-concrete')
a.materials['out-concrete'].Elastic(table=((35500.0, 0.2), ))
a.materials['out-concrete'].Density(table=((2.5e-09, ), ))
a.Material(name='cover-concrete')
a.materials['cover-concrete'].Elastic(table=((35500.0, 0.2), ))
a.materials['cover-concrete'].Density(table=((2.5e-09, ), ))
a.Material(name='rigid-body')
a.materials['rigid-body'].Elastic(table=((38000, 0.2), ))
a.materials['rigid-body'].Density(table=((2.5e-09, ), ))
a.Material(name='tube')
a.materials['tube'].Density(table=((7.85e-09, ), ))
a.materials['tube'].Elastic(table=((200000, 0.3), ))
a.materials['tube'].Plastic(table=((fytube, 0), ))
a.Material(name='rebar-l')
a.materials['rebar-l'].Density(table=((7.85e-09, ), ))
a.materials['rebar-l'].Elastic(table=((200000, 0.3), ))
a.materials['rebar-l'].Plastic(hardening=ISOTROPIC,table=((fylbar, 0.0), ))
a.Material(name='rebar-t')
a.materials['rebar-t'].Density(table=((7.85e-09, ), ))
a.materials['rebar-t'].Elastic(table=((200000, 0.3), ))
a.materials['rebar-t'].Plastic(hardening=ISOTROPIC,table=((fytbar, 0.0), ))
a.Material(name='rebar-rigid')
a.materials['rebar-rigid'].Density(table=((7.85e-09, ), ))
a.materials['rebar-rigid'].Elastic(table=((200000, 0.3), ))
a.materials['rebar-rigid'].Plastic(table=((400, 0.0), )) #此处属性暂按HRB400计，以实际为准

#section
mdb.models['Model-NewShearWall'].HomogeneousSolidSection(name='in-con', 
    material='in-concrete', thickness=None)
mdb.models['Model-NewShearWall'].HomogeneousSolidSection(name='out-con', 
    material='out-concrete', thickness=None)
mdb.models['Model-NewShearWall'].HomogeneousSolidSection(name='cover-con', 
    material='cover-concrete', thickness=None)
mdb.models['Model-NewShearWall'].HomogeneousSolidSection(name='rigid-body', 
    material='rigid-body', thickness=None)
mdb.models['Model-NewShearWall'].HomogeneousSolidSection(name='tube', 
    material='tube', thickness=None)
mdb.models['Model-NewShearWall'].TrussSection(name='rebar-l', 
    material='rebar-l', area=3.1415926/4*dlbar*dlbar)
mdb.models['Model-NewShearWall'].TrussSection(name='rebar-t', 
    material='rebar-t', area=3.1415926/4*dtbar*dtbar)
mdb.models['Model-NewShearWall'].TrussSection(name='rebar-rigid', 
    material='rebar-rigid', area=100) #此处属性暂按S=100计，以实际为准

#property
p = mdb.models['Model-NewShearWall'].parts['foundation']
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(region=region, sectionName='rigid-body', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['loadbeam']
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(region=region, sectionName='rigid-body', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['wall']
c = p.cells
cells = c.findAt(((1, 1, 0), ))
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='out-con', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
cells = c.findAt(((1, twall/2-1, 0), ),((1, -twall/2+1, 0), ),
    ((lwall/2-1, 1, 0), ), ((-lwall/2+1, 1, 0), ))
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='cover-con', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['tube']
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(region=region, sectionName='tube', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['in-concrete']
region = regionToolset.Region(cells=p.cells[:])
p.SectionAssignment(region=region, sectionName='in-con', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['lsteel']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-l', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['hoop1']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-t', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['hoop2']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-t', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['f-lsteel']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-rigid', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['l-lsteel']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-rigid', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['f-hoop']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-rigid', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

p = mdb.models['Model-NewShearWall'].parts['l-hoop']
region = regionToolset.Region(edges=p.edges[:])
p.SectionAssignment(region=region, sectionName='rebar-rigid', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

#assembly
a = myModel.rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a.DatumCsysByDefault(CARTESIAN)
p = myModel.parts['wall']
a.Instance(name='wall', part=p, dependent=ON)
p = myModel.parts['foundation']
a.Instance(name='foundation', part=p, dependent=ON)
p = myModel.parts['loadbeam']
a.Instance(name='loadbeam', part=p, dependent=ON)
p = myModel.parts['tube']
a.Instance(name='tube1', part=p, dependent=ON)
a.Instance(name='tube2', part=p, dependent=ON)
a.Instance(name='tube3', part=p, dependent=ON)
a.Instance(name='tube4', part=p, dependent=ON)
p = myModel.parts['in-concrete']
a.Instance(name='in-concrete1', part=p, dependent=ON)
a.Instance(name='in-concrete2', part=p, dependent=ON)
a.Instance(name='in-concrete3', part=p, dependent=ON)
a.Instance(name='in-concrete4', part=p, dependent=ON)
p = myModel.parts['lsteel']
for i in range(1,15):
    i=str(i)
    a.Instance(name='lsteel-'+i, part=p, dependent=ON)
hoopnum=int((hwall-2*cover)/space)+1
p = myModel.parts['hoop1']
for i in range(1,hoopnum+1):
    a.Instance(name='hoop11-'+str(i), part=p, dependent=ON)
    a.Instance(name='hoop12-'+str(i), part=p, dependent=ON)
    a.Instance(name='hoop13-'+str(i), part=p, dependent=ON)
    a.Instance(name='hoop14-'+str(i), part=p, dependent=ON)
p = myModel.parts['hoop2']
for i in range(1,hoopnum+1):
    a.Instance(name='hoop21-'+str(i), part=p, dependent=ON)
    a.Instance(name='hoop22-'+str(i), part=p, dependent=ON)

lhoopnum=int((lbl/2-offset1-dtube/2-2*cover)/50)+1
fhoopnum=int((lfd/2-offset1-dtube/2-2*cover)/50)+1
midhoopnum=int((2*offset2-dtube-2*cover)/50)+1

p = myModel.parts['l-hoop']
for i in range(1,lhoopnum+1):
    a.Instance(name='lhoop1-'+str(i), part=p, dependent=ON)
    a.Instance(name='lhoop2-'+str(i), part=p, dependent=ON)
for i in range(1,midhoopnum+1):
    a.Instance(name='lhoop3-'+str(i), part=p, dependent=ON)
p = myModel.parts['f-hoop']
for i in range(1,fhoopnum+1):
    a.Instance(name='fhoop1-'+str(i), part=p, dependent=ON)
    a.Instance(name='fhoop2-'+str(i), part=p, dependent=ON)
    a.Instance(name='fhoop3-'+str(i), part=p, dependent=ON)
    a.Instance(name='fhoop4-'+str(i), part=p, dependent=ON)
for i in range(1,midhoopnum+1):
    a.Instance(name='fhoop5-'+str(i), part=p, dependent=ON)
    a.Instance(name='fhoop6-'+str(i), part=p, dependent=ON)

for i in range(1,midhoopnum+1):
    a = mdb.models['Model-NewShearWall'].rootAssembly
    a.rotate(instanceList=('lhoop3-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=-90.0)
    a.rotate(instanceList=('fhoop5-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=90.0)
    a.rotate(instanceList=('fhoop6-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=90.0)

for i in range(1,lhoopnum+1):
    a = mdb.models['Model-NewShearWall'].rootAssembly
    a.rotate(instanceList=('lhoop1-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=-90.0)
    a.rotate(instanceList=('lhoop2-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=-90.0)

for i in range(1,fhoopnum+1):
    a = mdb.models['Model-NewShearWall'].rootAssembly
    a.rotate(instanceList=('fhoop1-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=90.0)
    a.rotate(instanceList=('fhoop2-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=90.0)
    a.rotate(instanceList=('fhoop3-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=90.0)
    a.rotate(instanceList=('fhoop4-'+str(i), ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 1, 0.0), angle=90.0)

p = myModel.parts['f-lsteel']
for i in range(1,9):
    a.Instance(name='f-lsteel-'+str(i), part=p, dependent=ON)
p = myModel.parts['l-lsteel']
for i in range(1,5):
    a.Instance(name='l-lsteel-'+str(i), part=p, dependent=ON)

#install
a.translate(instanceList=('foundation', ), vector=(0.0, 0.0, -hfd))
a.translate(instanceList=('loadbeam', ), vector=(0.0, 0.0, hwall))
a.translate(instanceList=('tube1', ), vector=(offset1, 0.0, -hfd))
a.translate(instanceList=('tube2', ), vector=(-offset1, 0.0, -hfd))
a.translate(instanceList=('tube3', ), vector=(offset2, 0.0, -hfd))
a.translate(instanceList=('tube4', ), vector=(-offset2, 0.0, -hfd))
a.translate(instanceList=('in-concrete1', ), vector=(offset1, 0.0, -hfd))
a.translate(instanceList=('in-concrete2', ), vector=(-offset1, 0.0, -hfd))
a.translate(instanceList=('in-concrete3', ), vector=(offset2, 0.0, -hfd))
a.translate(instanceList=('in-concrete4', ), vector=(-offset2, 0.0, -hfd))
for i in range(1,15):
    i=str(i)
    a.rotate(instanceList=('lsteel-'+i, ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 1, 0.0), angle=-90.0)

a.translate(instanceList=('lsteel-1', ), vector=(-(offset1*1.5-offset2/2), twall/2-cover, cover))
a.translate(instanceList=('lsteel-2', ), vector=(offset1*1.5-offset2/2, twall/2-cover, cover))
a.translate(instanceList=('lsteel-3', ), vector=(-(offset1*1.5-offset2/2), -(twall/2-cover), cover))
a.translate(instanceList=('lsteel-4', ), vector=(offset1*1.5-offset2/2, -(twall/2-cover), cover))

a.translate(instanceList=('lsteel-5', ), vector=(-(offset1+offset2)/2, twall/2-cover, cover))
a.translate(instanceList=('lsteel-6', ), vector=((offset1+offset2)/2, twall/2-cover, cover))
a.translate(instanceList=('lsteel-7', ), vector=(-(offset1+offset2)/2, -(twall/2-cover), cover))
a.translate(instanceList=('lsteel-8', ), vector=((offset1+offset2)/2, -(twall/2-cover), cover))

a.translate(instanceList=('lsteel-9', ), vector=(-(offset2*1.5-offset1/2), twall/2-cover, cover))
a.translate(instanceList=('lsteel-10', ), vector=(offset2*1.5-offset1/2, twall/2-cover, cover))
a.translate(instanceList=('lsteel-11', ), vector=(-(offset2*1.5-offset1/2), -(twall/2-cover), cover))
a.translate(instanceList=('lsteel-12', ), vector=(offset2*1.5-offset1/2, -(twall/2-cover), cover))

a.translate(instanceList=('lsteel-13', ), vector=(0, twall/2-cover, cover))
a.translate(instanceList=('lsteel-14', ), vector=(0, -(twall/2-cover), cover))

for i in range(1,hoopnum+1):
    a.translate(instanceList=('hoop11-'+str(i), ), vector=(offset1, 0, cover+(i-1)*space))
    a.translate(instanceList=('hoop12-'+str(i), ), vector=(-offset1, 0, cover+(i-1)*space+dtbar))
    a.translate(instanceList=('hoop13-'+str(i), ), vector=(offset2, 0, cover+(i-1)*space+dtbar))
    a.translate(instanceList=('hoop14-'+str(i), ), vector=(-offset2, 0, cover+(i-1)*space))    
    a.translate(instanceList=('hoop21-'+str(i), ), vector=((hooplength2)/2, 0, cover+(i-1)*space))
    a.translate(instanceList=('hoop22-'+str(i), ), vector=(-(hooplength2)/2, 0, cover+(i-1)*space+dtbar))

for i in range(1,fhoopnum+1):
    a.translate(instanceList=('fhoop1-'+str(i), ), vector=(lfd/2-cover-(i-1)*50, -(tfd/2-cover), -cover))
    a.translate(instanceList=('fhoop2-'+str(i), ), vector=(lfd/2-cover-(i-1)*50, -(dtube/2+cover), -cover))
    a.translate(instanceList=('fhoop3-'+str(i), ), vector=(-(lfd/2-cover-(i-1)*50), -(tfd/2-cover), -cover))
    a.translate(instanceList=('fhoop4-'+str(i), ), vector=(-(lfd/2-cover-(i-1)*50), -(dtube/2+cover), -cover))

for i in range(1,lhoopnum+1):
    a.translate(instanceList=('lhoop1-'+str(i), ), vector=(lbl/2-cover-(i-1)*50, 0, hwall+hbl/2))
    a.translate(instanceList=('lhoop2-'+str(i), ), vector=(-(lbl/2-cover-(i-1)*50), 0, hwall+hbl/2))
for i in range(1,midhoopnum+1):
    a.translate(instanceList=('lhoop3-'+str(i), ), vector=(((-1)**i)*(int(i/2))*50, 0, hwall+hbl/2))
    a.translate(instanceList=('fhoop5-'+str(i), ), vector=(((-1)**i)*(int(i/2))*50, -(dtube/2+cover), -cover))
    a.translate(instanceList=('fhoop6-'+str(i), ), vector=(((-1)**i)*(int(i/2))*50, -(tfd/2-cover), -cover))

a.translate(instanceList=('f-lsteel-1', ), vector=(-lfd/2+cover, tfd/2-cover, -cover))
a.translate(instanceList=('f-lsteel-2', ), vector=(-lfd/2+cover, -(tfd/2-cover), -cover))
a.translate(instanceList=('f-lsteel-3', ), vector=(-lfd/2+cover, -(tfd/2-cover), -hfd+cover))
a.translate(instanceList=('f-lsteel-4', ), vector=(-lfd/2+cover, tfd/2-cover, -hfd+cover))
a.translate(instanceList=('f-lsteel-5', ), vector=(-lfd/2+cover, -(dtube/2+cover), -cover))
a.translate(instanceList=('f-lsteel-6', ), vector=(-lfd/2+cover, dtube/2+cover, -cover))
a.translate(instanceList=('f-lsteel-7', ), vector=(-lfd/2+cover, dtube/2+cover, -hfd+cover))
a.translate(instanceList=('f-lsteel-8', ), vector=(-lfd/2+cover, -(dtube/2+cover), -hfd+cover))

a.translate(instanceList=('l-lsteel-1', ), vector=(-lbl/2+cover, -(tbl/2-cover), hwall+hbl-cover))
a.translate(instanceList=('l-lsteel-2', ), vector=(-lbl/2+cover, tbl/2-cover, hwall+hbl-cover))
a.translate(instanceList=('l-lsteel-3', ), vector=(-lbl/2+cover, -(tbl/2-cover), hwall+cover))
a.translate(instanceList=('l-lsteel-4', ), vector=(-lbl/2+cover, tbl/2-cover, hwall+cover))

ins=(a.instances['lsteel-1'],)
for i in range(2,15):
    ins=ins+(a.instances['lsteel-'+str(i)],)
for i in range(1,hoopnum+1):
    ins=ins+(a.instances['hoop11-'+str(i)],)
    ins=ins+(a.instances['hoop12-'+str(i)],)
    ins=ins+(a.instances['hoop13-'+str(i)],)
    ins=ins+(a.instances['hoop14-'+str(i)],)
    ins=ins+(a.instances['hoop21-'+str(i)],)
    ins=ins+(a.instances['hoop22-'+str(i)],)
a.InstanceFromBooleanMerge(name='merge-rebar', instances=ins,originalInstances=DELETE, domain=GEOMETRY)
e = a.instances['merge-rebar-1'].edges
region1=regionToolset.Region(edges=e[:])
mdb.models['Model-NewShearWall'].EmbeddedRegion(name='steel-embed', 
    embeddedRegion=region1, hostRegion=None, weightFactorTolerance=1e-06, 
    absoluteTolerance=0.0, fractionalTolerance=0.05, toleranceMethod=BOTH)

ins=(a.instances['l-lsteel-1'],)
for i in range(2,5):
    ins=ins+(a.instances['l-lsteel-'+str(i)],)
for i in range(1,lhoopnum+1):
    ins=ins+(a.instances['lhoop1-'+str(i)],)
    ins=ins+(a.instances['lhoop2-'+str(i)],)
for i in range(1,midhoopnum+1):
    ins=ins+(a.instances['lhoop3-'+str(i)],)
a.InstanceFromBooleanMerge(name='merge-rebar-l', instances=ins,originalInstances=DELETE, domain=GEOMETRY)
e = a.instances['merge-rebar-l-1'].edges
region1=regionToolset.Region(edges=e[:])
mdb.models['Model-NewShearWall'].EmbeddedRegion(name='l-steel-embed', 
    embeddedRegion=region1, hostRegion=None, weightFactorTolerance=1e-06, 
    absoluteTolerance=0.0, fractionalTolerance=0.05, toleranceMethod=BOTH)

ins=(a.instances['f-lsteel-1'],)
for i in range(2,9):
    ins=ins+(a.instances['f-lsteel-'+str(i)],)
for i in range(1,fhoopnum+1):
    ins=ins+(a.instances['fhoop1-'+str(i)],)
    ins=ins+(a.instances['fhoop2-'+str(i)],)
    ins=ins+(a.instances['fhoop3-'+str(i)],)
    ins=ins+(a.instances['fhoop4-'+str(i)],)  
for i in range(1,midhoopnum+1):
    ins=ins+(a.instances['fhoop5-'+str(i)],)
    ins=ins+(a.instances['fhoop6-'+str(i)],)
a.InstanceFromBooleanMerge(name='merge-rebar-f', instances=ins,originalInstances=DELETE, domain=GEOMETRY)
e = a.instances['merge-rebar-f-1'].edges
region1=regionToolset.Region(edges=e[:])
mdb.models['Model-NewShearWall'].EmbeddedRegion(name='f-steel-embed', 
    embeddedRegion=region1, hostRegion=None, weightFactorTolerance=1e-06, 
    absoluteTolerance=0.0, fractionalTolerance=0.05, toleranceMethod=BOTH)

#interaction
a1 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a1.instances['wall'].faces
side1Faces1 = s1.findAt(((1, 1, hwall), ),((1, twall/2-1, hwall), ),((1, -twall/2+1, hwall), ),
    ((lwall/2-1, 1, hwall), ), ((-lwall/2+1, 1, hwall), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a1 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a1.instances['loadbeam'].faces
side1Faces1 = s1.findAt(((1, 1, hwall), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='wall-loadbeam', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a2 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a2.instances['foundation'].faces
side1Faces1 = s1.findAt(((1, 1, 0), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a2 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a2.instances['wall'].faces
side1Faces1 = s1.findAt(((1, 1, 0), ),((1, twall/2-1, 0), ),((1, -twall/2+1, 0), ),
    ((lwall/2-1, 1, 0), ), ((-lwall/2+1, 1, 0), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='wall-foundation', master=region2, 
    slave=region1, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube1'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['wall'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='wall-tube1', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube2'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['wall'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='wall-tube2', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube3'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['wall'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='wall-tube3', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube4'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['wall'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='wall-tube4', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube1'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2, 0, -1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['foundation'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2, 0, -1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='fd-tube1', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube2'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2, 0, -1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['foundation'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2, 0, -1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='fd-tube2', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube3'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2, 0, -1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['foundation'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2, 0, -1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='fd-tube3', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube4'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2, 0, -1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['foundation'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2, 0, -1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='fd-tube4', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube1'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2, 0, hwall+1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['loadbeam'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2, 0, hwall+1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='lb-tube1', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube2'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2, 0, hwall+1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['loadbeam'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2, 0, hwall+1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='lb-tube2', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube3'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2, 0, hwall+1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['loadbeam'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2, 0, hwall+1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='lb-tube3', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube4'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2, 0, hwall+1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['loadbeam'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2, 0, hwall+1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='lb-tube4', master=region1, 
    slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube1'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2-ttube, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['in-concrete1'].faces
side1Faces1 = s1.findAt(((offset1+dtube/2-ttube, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='incon-tube1', master=region2, 
    slave=region1, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube2'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2-ttube, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['in-concrete2'].faces
side1Faces1 = s1.findAt(((-offset1+dtube/2-ttube, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='incon-tube2', master=region2, 
    slave=region1, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube3'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2-ttube, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['in-concrete3'].faces
side1Faces1 = s1.findAt(((offset2+dtube/2-ttube, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='incon-tube3', master=region2, 
    slave=region1, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['tube4'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2-ttube, 0, hwall-1), ))
region1=regionToolset.Region(side1Faces=side1Faces1)
a4 = mdb.models['Model-NewShearWall'].rootAssembly
s1 = a4.instances['in-concrete4'].faces
side1Faces1 = s1.findAt(((-offset2+dtube/2-ttube, 0, hwall-1), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Tie(name='incon-tube4', master=region2, 
    slave=region1, positionToleranceMethod=COMPUTED, adjust=ON, 
    tieRotations=ON, thickness=ON)

#mesh
p = mdb.models['Model-NewShearWall'].parts['wall']
f,e,d =p.faces,p.edges,p.datums
t = p.MakeSketchTransform(sketchPlane=f.findAt((1,1,0)),
	sketchUpEdge=e.findAt((lwall/2,0,0)))
s = mdb.models['Model-NewShearWall'].ConstrainedSketch(name='__profile__', 
    sheetSize=4000, gridSpacing=50, transform=t)
g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.Line(point1=(-offset1-dtube/2,-twall/2),point2=(-offset1-dtube/2,twall/2))
s.Line(point1=(-offset1,-twall/2),point2=(-offset1,twall/2))
s.Line(point1=(-offset1+dtube/2,-twall/2),point2=(-offset1+dtube/2,twall/2))
s.Line(point1=(-offset2-dtube/2,-twall/2),point2=(-offset2-dtube/2,twall/2))
s.Line(point1=(-offset2,-twall/2),point2=(-offset2,twall/2))
s.Line(point1=(-offset2+dtube/2,-twall/2),point2=(-offset2+dtube/2,twall/2))
s.Line(point1=(offset1-dtube/2,-twall/2),point2=(offset1-dtube/2,twall/2))
s.Line(point1=(offset1,-twall/2),point2=(offset1,twall/2))
s.Line(point1=(offset1+dtube/2,-twall/2),point2=(offset1+dtube/2,twall/2))
s.Line(point1=(offset2-dtube/2,-twall/2),point2=(offset2-dtube/2,twall/2))
s.Line(point1=(offset2,-twall/2),point2=(offset2,twall/2))
s.Line(point1=(offset2+dtube/2,-twall/2),point2=(offset2+dtube/2,twall/2))
s.Line(point1=(-lwall/2,-dtube/2),point2=(lwall/2,-dtube/2))
s.Line(point1=(-lwall/2,dtube/2),point2=(lwall/2,dtube/2))
s.Line(point1=(-offset1-dtube/2,dtube/2),point2=(-offset1+dtube/2,-dtube/2))
s.Line(point1=(-offset1-dtube/2,-dtube/2),point2=(-offset1+dtube/2,dtube/2))
s.Line(point1=(-offset2-dtube/2,dtube/2),point2=(-offset2+dtube/2,-dtube/2))
s.Line(point1=(-offset2-dtube/2,-dtube/2),point2=(-offset2+dtube/2,dtube/2))
s.Line(point1=(offset1-dtube/2,dtube/2),point2=(offset1+dtube/2,-dtube/2))
s.Line(point1=(offset1-dtube/2,-dtube/2),point2=(offset1+dtube/2,dtube/2))
s.Line(point1=(offset2-dtube/2,dtube/2),point2=(offset2+dtube/2,-dtube/2))
s.Line(point1=(offset2-dtube/2,-dtube/2),point2=(offset2+dtube/2,dtube/2))
s.Line(point1=(-lwall/2,0),point2=(lwall/2,0))
p = mdb.models['Model-NewShearWall'].parts['wall']
f1,e1,d2 =p.faces,p.edges,p.datums
pickedFaces = f1.findAt((1,1,0))
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s,
	sketchUpEdge=e.findAt((lwall/2,0,0)))
s.unsetPrimaryObject()
del mdb.models['Model-NewShearWall'].sketches['__profile__']

p = mdb.models['Model-NewShearWall'].parts['wall']
d = p.datums
p.DatumPlaneByPrincipalPlane( principalPlane=XZPLANE, offset=0)
p.DatumPlaneByPrincipalPlane( principalPlane=XZPLANE, offset=dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=XZPLANE, offset=-dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-lwall/2+cover)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-offset1-dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-offset1)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-offset1+dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-offset2-dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-offset2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-offset2+dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=0)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=lwall/2-cover)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=offset1+dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=offset1)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=offset1-dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=offset2+dtube/2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=offset2)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=offset2-dtube/2)
for i in range(13,31):
    d2 = p.datums
    p.PartitionCellByDatumPlane(datumPlane=d2[i], cells=p.cells[:])

p = mdb.models['Model-NewShearWall'].parts['wall']
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

##钢管
p = mdb.models['Model-NewShearWall'].parts['tube']
d = p.datums
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
p1= d.keys()[-1]
p.PartitionFaceByDatumPlane(datumPlane=d[p1], faces=p.faces[0])
e = p.edges
pickedEdges = e.findAt(((dtube/2, 0.0, hwall/2), ))
p.seedEdgeByNumber(edges=pickedEdges, number=40, constraint=FIXED)
e = p.edges
pickedEdges = e.findAt(((0.0, -dtube/2, hwall+hfd+hbl), ))
p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FIXED)
pickedEdges = e.findAt(((0.0, -dtube/2+ttube, hwall+hfd+hbl), ))
p.seedEdgeByNumber(edges=pickedEdges, number=8, constraint=FIXED)

p.generateMesh()

##管内混凝土
p = mdb.models['Model-NewShearWall'].parts['in-concrete']
e = p.edges
pickedEdges = e.findAt(((0.0, -dtube/2+ttube, 0), ))
p.seedEdgeByNumber(edges=pickedEdges, number=8, constraint=FIXED)
d = p.datums
p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
p1= d.keys()[-1]
p.PartitionFaceByDatumPlane(datumPlane=d[p1], faces=p.faces[0])
e = p.edges
pickedEdges = e.findAt(((dtube/2-ttube, 0.0, hwall/2), ))
p.seedEdgeByNumber(edges=pickedEdges, number=20, constraint=FIXED)
p.generateMesh()

f1 = a.instances['foundation'].faces
faces1 = f1.findAt(((-1, -1, -hfd), ))
f2 = a.instances['in-concrete1'].faces
faces2 = f2.findAt(((offset1, -1, -hfd), ))
f3 = a.instances['in-concrete2'].faces
faces3 = f3.findAt(((-offset1, -1, -hfd), ))
f4 = a.instances['in-concrete3'].faces
faces4 = f4.findAt(((offset2, -1, -hfd), ))
f5 = a.instances['in-concrete4'].faces
faces5 = f5.findAt(((-offset2, -1, -hfd), ))

f6 = a.instances['tube1'].faces
faces6 = f6.findAt(((offset1+dtube/2, 0, -hfd), ))
f7 = a.instances['tube2'].faces
faces7 = f7.findAt(((-offset1+dtube/2, 0, -hfd), ))
f8 = a.instances['tube3'].faces
faces8 = f8.findAt(((offset2+dtube/2, 0, -hfd), ))
f9 = a.instances['tube4'].faces
faces9 = f9.findAt(((-offset2+dtube/2, 0, -hfd), ))
a.Set(faces=faces1+faces2+faces3+faces4+faces5+faces6+faces7+faces8+faces9, name='fd-bottom')

p = mdb.models['Model-NewShearWall'].parts['foundation']
f,e,d =p.faces,p.edges,p.datums
t = p.MakeSketchTransform(sketchPlane=f.findAt((1,1,0)),
    sketchUpEdge=e.findAt((lfd/2,0,0)))
s = mdb.models['Model-NewShearWall'].ConstrainedSketch(name='__profile__', 
    sheetSize=4000, gridSpacing=50, transform=t)
g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.Line(point1=(-offset1-dtube/2,-tfd/2),point2=(-offset1-dtube/2,tfd/2))
s.Line(point1=(-offset1,-tfd/2),point2=(-offset1,tfd/2))
s.Line(point1=(-offset1+dtube/2,-tfd/2),point2=(-offset1+dtube/2,tfd/2))
s.Line(point1=(-offset2-dtube/2,-tfd/2),point2=(-offset2-dtube/2,tfd/2))
s.Line(point1=(-offset2,-tfd/2),point2=(-offset2,tfd/2))
s.Line(point1=(-offset2+dtube/2,-tfd/2),point2=(-offset2+dtube/2,tfd/2))
s.Line(point1=(offset1-dtube/2,-tfd/2),point2=(offset1-dtube/2,tfd/2))
s.Line(point1=(offset1,-tfd/2),point2=(offset1,tfd/2))
s.Line(point1=(offset1+dtube/2,-tfd/2),point2=(offset1+dtube/2,tfd/2))
s.Line(point1=(offset2-dtube/2,-tfd/2),point2=(offset2-dtube/2,tfd/2))
s.Line(point1=(offset2,-tfd/2),point2=(offset2,tfd/2))
s.Line(point1=(offset2+dtube/2,-tfd/2),point2=(offset2+dtube/2,tfd/2))
s.Line(point1=(-lfd/2,-dtube/2),point2=(lfd/2,-dtube/2))
s.Line(point1=(-lfd/2,dtube/2),point2=(lfd/2,dtube/2))
s.Line(point1=(-offset1-dtube/2,dtube/2),point2=(-offset1+dtube/2,-dtube/2))
s.Line(point1=(-offset1-dtube/2,-dtube/2),point2=(-offset1+dtube/2,dtube/2))
s.Line(point1=(-offset2-dtube/2,dtube/2),point2=(-offset2+dtube/2,-dtube/2))
s.Line(point1=(-offset2-dtube/2,-dtube/2),point2=(-offset2+dtube/2,dtube/2))
s.Line(point1=(offset1-dtube/2,dtube/2),point2=(offset1+dtube/2,-dtube/2))
s.Line(point1=(offset1-dtube/2,-dtube/2),point2=(offset1+dtube/2,dtube/2))
s.Line(point1=(offset2-dtube/2,dtube/2),point2=(offset2+dtube/2,-dtube/2))
s.Line(point1=(offset2-dtube/2,-dtube/2),point2=(offset2+dtube/2,dtube/2))
s.Line(point1=(-lfd/2,0),point2=(lfd/2,0))
p = mdb.models['Model-NewShearWall'].parts['foundation']
f1,e1,d2 =p.faces,p.edges,p.datums
pickedFaces = f1.findAt((1,1,0))
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s,
    sketchUpEdge=e.findAt((lfd/2,0,0)))
s.unsetPrimaryObject()
del mdb.models['Model-NewShearWall'].sketches['__profile__']

p = mdb.models['Model-NewShearWall'].parts['foundation']
p.seedPart(size=1000, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

elemType1 = mesh.ElemType(elemCode=T3D2, elemLibrary=STANDARD)
p = mdb.models['Model-NewShearWall'].parts['lsteel']
e = p.edges[:]
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

p = mdb.models['Model-NewShearWall'].parts['hoop1']
e = p.edges[:]
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

p = mdb.models['Model-NewShearWall'].parts['hoop2']
e = p.edges[:]
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

p = mdb.models['Model-NewShearWall'].parts['merge-rebar']
e = p.edges[:]
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

p = mdb.models['Model-NewShearWall'].parts['merge-rebar-l']
e = p.edges[:]
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()
p = mdb.models['Model-NewShearWall'].parts['merge-rebar-f']
e = p.edges[:]
pickedRegions =(e, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))
p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

#step
mdb.models['Model-NewShearWall'].StaticStep(name='Step-1', previous='Initial', 
    timePeriod=1.0, maxNumInc=500, initialInc=0.01, minInc=1e-12, maxInc=1.0, 
    nlgeom=ON)

mdb.models['Model-NewShearWall'].StaticStep(name='Step-2', previous='Step-1', 
    timePeriod=1.0, maxNumInc=100000, initialInc=0.01, minInc=1e-12, 
    maxInc=0.3)

#load&bc
p = mdb.models['Model-NewShearWall'].parts['loadbeam']
d = p.datums
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=-lbl/2+meshsize)
p.DatumPlaneByPrincipalPlane( principalPlane=YZPLANE, offset=lbl/2-meshsize)
d2 = p.datums
p.PartitionCellByDatumPlane(datumPlane=d2[4], cells=p.cells[:])
p.PartitionCellByDatumPlane(datumPlane=d2[3], cells=p.cells[:])

a2 = mdb.models['Model-NewShearWall'].rootAssembly
f1 = a2.instances['loadbeam'].faces
faces1 = f1.findAt(((1, -1, hwall+hbl), ))
f2 = a2.instances['in-concrete1'].faces
faces2 = f2.findAt(((offset1, -1, hwall+hbl), ))
f3 = a2.instances['in-concrete2'].faces
faces3 = f3.findAt(((-offset1, -1, hwall+hbl), ))
f4 = a2.instances['in-concrete3'].faces
faces4 = f4.findAt(((offset2, -1, hwall+hbl), ))
f5 = a2.instances['in-concrete4'].faces
faces5 = f5.findAt(((-offset2, -1, hwall+hbl), ))

f6 = a2.instances['tube1'].faces
faces6 = f6.findAt(((offset1+dtube/2, 0, hwall+hbl), ))
f7 = a2.instances['tube2'].faces
faces7 = f7.findAt(((-offset1+dtube/2, 0, hwall+hbl), ))
f8 = a2.instances['tube3'].faces
faces8 = f8.findAt(((offset2+dtube/2, 0, hwall+hbl), ))
f9 = a2.instances['tube4'].faces
faces9 = f9.findAt(((-offset2+dtube/2, 0, hwall+hbl), ))
a2.Surface(side1Faces=faces1+faces2+faces3+faces4+faces5+faces6+faces7+faces8+faces9, name='lb-top')

a = mdb.models['Model-NewShearWall'].rootAssembly
rp2= a.ReferencePoint(point=(0, 0, hwall+hbl))
v2 = (a.referencePoints[rp2.id], )
region1=regionToolset.Region(referencePoints=v2)
region2=a1.surfaces['lb-top']
mdb.models['Model-NewShearWall'].Coupling(name='axial-loading', 
    controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
    couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
    ur2=ON, ur3=ON)
region = regionToolset.Region(referencePoints=v2)
mdb.models['Model-NewShearWall'].ConcentratedForce(name='axial-loading', 
    createStepName='Step-1', region=region, cf3=-axld, 
    distributionType=UNIFORM, field='', localCsys=None)

p = mdb.models['Model-NewShearWall'].parts['loadbeam']
f,e,d =p.faces,p.edges,p.datums
t = p.MakeSketchTransform(sketchPlane=f.findAt((1,1,0)),
    sketchUpEdge=e.findAt((lbl/2,0,0)))
s = mdb.models['Model-NewShearWall'].ConstrainedSketch(name='__profile__', 
    sheetSize=4000, gridSpacing=50, transform=t)
s.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.Line(point1=(-offset1-dtube/2,-tbl/2),point2=(-offset1-dtube/2,tbl/2))
s.Line(point1=(-offset1,-tbl/2),point2=(-offset1,tbl/2))
s.Line(point1=(-offset1+dtube/2,-tbl/2),point2=(-offset1+dtube/2,tbl/2))
s.Line(point1=(-offset2-dtube/2,-tbl/2),point2=(-offset2-dtube/2,tbl/2))
s.Line(point1=(-offset2,-tbl/2),point2=(-offset2,tbl/2))
s.Line(point1=(-offset2+dtube/2,-tbl/2),point2=(-offset2+dtube/2,tbl/2))
s.Line(point1=(offset1-dtube/2,-tbl/2),point2=(offset1-dtube/2,tbl/2))
s.Line(point1=(offset1,-tbl/2),point2=(offset1,tbl/2))
s.Line(point1=(offset1+dtube/2,-tbl/2),point2=(offset1+dtube/2,tbl/2))
s.Line(point1=(offset2-dtube/2,-tbl/2),point2=(offset2-dtube/2,tbl/2))
s.Line(point1=(offset2,-tbl/2),point2=(offset2,tbl/2))
s.Line(point1=(offset2+dtube/2,-tbl/2),point2=(offset2+dtube/2,tbl/2))
s.Line(point1=(-lbl/2,-dtube/2),point2=(lbl/2,-dtube/2))
s.Line(point1=(-lbl/2,dtube/2),point2=(lbl/2,dtube/2))
s.Line(point1=(-lbl/2,0),point2=(lbl/2,0))
s.Line(point1=(-offset1-dtube/2,dtube/2),point2=(-offset1+dtube/2,-dtube/2))
s.Line(point1=(-offset1-dtube/2,-dtube/2),point2=(-offset1+dtube/2,dtube/2))
s.Line(point1=(-offset2-dtube/2,dtube/2),point2=(-offset2+dtube/2,-dtube/2))
s.Line(point1=(-offset2-dtube/2,-dtube/2),point2=(-offset2+dtube/2,dtube/2))
s.Line(point1=(offset1-dtube/2,dtube/2),point2=(offset1+dtube/2,-dtube/2))
s.Line(point1=(offset1-dtube/2,-dtube/2),point2=(offset1+dtube/2,dtube/2))
s.Line(point1=(offset2-dtube/2,dtube/2),point2=(offset2+dtube/2,-dtube/2))
s.Line(point1=(offset2-dtube/2,-dtube/2),point2=(offset2+dtube/2,dtube/2))
p = mdb.models['Model-NewShearWall'].parts['loadbeam']
f1 =p.faces
pickedFaces = f1.findAt((1,1,0))
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s,
    sketchUpEdge=e.findAt((lbl/2,0,0)))
s.unsetPrimaryObject()
del mdb.models['Model-NewShearWall'].sketches['__profile__']

p = mdb.models['Model-NewShearWall'].parts['loadbeam']
p.seedPart(size=200, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

#load
mdb.models['Model-NewShearWall'].TabularAmplitude(name='Amp-1', timeSpan=STEP, 
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 0.1), (2.0, 0.0), (3.0, 
    -0.1), (4.0, 0.0), (5.0, 0.2), (6.0, 0.0), (7.0, -0.2), (8.0, 0.0), (9.0, 
    0.3), (10.0, 0.0), (11.0, -0.3), (12.0, 0.0), (13.0, 0.4), (14.0, 0.0), (
    15.0, -0.4), (16.0, 0.0), (17.0, 0.5), (18.0, 0.0), (19.0, -0.5), (20.0, 
    0.0), (21.0, 0.6), (22.0, 0.0), (23.0, -0.6), (24.0, 0.0), (25.0, 0.7), (
    26.0, 0.0), (27.0, -0.7), (28.0, 0.0), (29.0, 0.8), (30.0, 0.0), (31.0, 
    -0.8), (32.0, 0.0), (33.0, 0.9), (34.0, 0.0), (35.0, -0.9), (36.0, 0.0), (
    37.0, 1.0), (38.0, 0.0), (39.0, -1.0), (40.0, 0.0)))
rp1= a.ReferencePoint(point=(-lbl/2, 0, (hwall+hwall+hbl)/2))
v1 = (a.referencePoints[rp1.id], )
region1=regionToolset.Region(referencePoints=v1)
s1 = a.instances['loadbeam'].faces
side1Faces1 = s1.findAt(((-lbl/2, -1, (hwall+hwall+hbl)/2), ))
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-NewShearWall'].Coupling(name='lateral-loading', 
    controlPoint=region1, surface=region2, influenceRadius=WHOLE_SURFACE, 
    couplingType=KINEMATIC, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, 
    ur2=ON, ur3=ON)
region = regionToolset.Region(referencePoints=v1)
mdb.models['Model-NewShearWall'].DisplacementBC(name='lateral-loading', 
    createStepName='Step-2', region=region, u1=dis, u2=UNSET, u3=UNSET, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

##bd
a = mdb.models['Model-NewShearWall'].rootAssembly
region = a.sets['fd-bottom']
mdb.models['Model-NewShearWall'].EncastreBC(name='bottom-encastre', createStepName='Initial', 
    region=region, localCsys=None)

f1 = a1.instances['wall'].faces
faces1 = f1.findAt(((lwall/2-cover+1, -twall/2, 1), ),((-lwall/2+cover+1, -twall/2, 1), ),((-offset1-dtube/2+1, -twall/2, 1), ),((-offset1+1, -twall/2, 1), ),
    ((-offset1+dtube/2+1, -twall/2, 1), ),((-offset2-dtube/2+1, -twall/2, 1), ),((-offset2+1, -twall/2, 1), ),((-offset2+dtube/2+1, -twall/2, 1), ),
((1, -twall/2, 1), ),((offset1+dtube/2+1, -twall/2, 1), ),((offset1+1, -twall/2, 1), ),((offset1-dtube/2+1, -twall/2, 1), ),((offset2+dtube/2+1, -twall/2, 1), ),
((offset2+1, -twall/2, 1), ),((offset2-dtube/2+1, -twall/2, 1), ),((lwall/2-1, -twall/2, 1), ),((-lwall/2+1, -twall/2, 1), ))
region = regionToolset.Region(faces=faces1)
mdb.models['Model-NewShearWall'].DisplacementBC(name='wall-y1', 
    createStepName='Initial', region=region, u1=UNSET, u2=SET, u3=UNSET, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, 
    fieldName='', localCsys=None)

faces1 = f1.findAt(((lwall/2-cover+1, twall/2, 1), ),((-lwall/2+cover+1, twall/2, 1), ),((-offset1-dtube/2+1, twall/2, 1), ),((-offset1+1, twall/2, 1), ),
    ((-offset1+dtube/2+1, twall/2, 1), ),((-offset2-dtube/2+1, twall/2, 1), ),((-offset2+1, twall/2, 1), ),((-offset2+dtube/2+1, twall/2, 1), ),
((1, twall/2, 1), ),((offset1+dtube/2+1, twall/2, 1), ),((offset1+1, twall/2, 1), ),((offset1-dtube/2+1, twall/2, 1), ),((offset2+dtube/2+1, twall/2, 1), ),
((offset2+1, twall/2, 1), ),((offset2-dtube/2+1, twall/2, 1), ),((lwall/2-1, twall/2, 1), ),((-lwall/2+1, twall/2, 1), ))

region = regionToolset.Region(faces=faces1)
mdb.models['Model-NewShearWall'].DisplacementBC(name='wall-y2', 
    createStepName='Initial', region=region, u1=UNSET, u2=SET, u3=UNSET, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, 
    fieldName='', localCsys=None)

mdb.Job(name=jobname, model='Model-NewShearWall', description='', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=4, numDomains=4, 
    numGPUs=0)

