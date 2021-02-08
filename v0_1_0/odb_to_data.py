'''get hysteresis loop from abaqus odb
# @Author: Mengsen.Wang
# @Date: 2021-01-24 10:50:47
# @Last Modified by: Mengsen.Wang
# @Last Modified time: 2021-01-24 10:50:47
'''
from visualization import *
from odbAccess import *
import sys

odb_name = 'SW02-210203-4.odb'
step_name = 'Step-2'
set_name = 'RP-1'
outfile_name = '{}.txt'.format(odb_name[0:-4])

# get odb name
odb = openOdb(odb_name)
# outfile
f = open(outfile_name, 'w')

myAssembly = odb.rootAssembly
# step name
frameRepository = odb.steps[step_name].frames
# set name
RefPointSet = myAssembly.nodeSets[set_name]

for i in range(len(frameRepository)):
    # [0]--x [1]--y [2]--z

    # extract set_name in directory force
    RForce = frameRepository[i].fieldOutputs['RF']
    RefPointRForce = RForce.getSubset(region=RefPointSet)
    RForceValues = RefPointRForce.values
    RF_x = RForceValues[0].data[0]

    # extract set_name in directory displace
    displacement = frameRepository[i].fieldOutputs['U']
    RefPointDisp = displacement.getSubset(region=RefPointSet)
    DispValue = RefPointDisp.values
    Disp_x = DispValue[0].data[0]
    # write file
    Disp_data = '\t' + '\t' + str(Disp_x)
    Force_data = '\t' + '\t' + str(RF_x)
    Disp = str(Disp_data)
    RF = str(Force_data)
    f.write(Disp)
    f.write(RF)
    f.write('\n')
