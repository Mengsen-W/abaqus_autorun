'''
 * @Author: Mengsen.Wang
 * @Date: 2019-11-18 22:35:21
 * @Last Modified by:   Mengsen.Wang
 * @Last Modified time: 2019-11-18 22:35:21
'''
import os
import sys
from abaqus import *
from abaqusConstants import *
from odbAccess import *
from visualization import *
import sketch
import part
import assembly
import material
import visualization

# open odb file
odb = openOdb(path='E:/Code/Abaqus_Code/example.odb')

# open and write file to copy odb file
CopyFile = open("E:/Code/Abaqus_Code/CopyFile.txt","w")

# get the Assembly and print
# return dictionary
assembly = odb.rootAssembly
CopyFile.write(str((dir(assembly))))
CopyFile.close()

RS = odb.steps['Steps'].frames[1].fieldOutputs["U"].values
CopyFile = open("E:/Code/Abaqus_Code/distance.txt","w")

for i in RS:
    CopyFile.write('%d %7.4f %7.4f\n' % (i.nodeLabel,i.data[0],i.data[1]))
else:
    CopyFile.close()
