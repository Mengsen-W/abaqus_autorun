'''
 * @Author: Mengsen.Wang 
 * @Date: 2019-12-14 17:13:14
 * @Last Modified by:   Mengsen.Wang
 * @Last Modified time: 2019-12-14 17:13:14
'''
from abaqus import *
from abaqusConstants import *



mdb.JobFromInputFile(name='SW-1-0',
                     inputFileName='D:\\software\\SIMULIA\\Temp\\JinGuangZeSheerWall\\SW-2\\SW-1-0.inp',
                     type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
                     memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',
                     scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1,
                     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['SW-1-0'].submit(consistencyChecking=OFF, datacheckJob=True)

mdb.JobFromInputFile(name='SW-1-1',
                     inputFileName='D:\\software\\SIMULIA\\Temp\\JinGuangZeSheerWall\\SW-2\\SW-1-1.inp',
                     type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
                     memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',
                     scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1,
                     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['SW-1-1'].submit(consistencyChecking=OFF, datacheckJob=True)

mdb.JobFromInputFile(name='SW-1-2',
                     inputFileName='D:\\software\\SIMULIA\\Temp\\JinGuangZeSheerWall\\SW-2\\SW-1-2.inp',
                     type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
                     memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',
                     scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1,
                     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['SW-1-2'].submit(consistencyChecking=OFF, datacheckJob=True)

mdb.JobFromInputFile(name='SW-1-3',
                     inputFileName='D:\\software\\SIMULIA\\Temp\\JinGuangZeSheerWall\\SW-2\\SW-1-3.inp',
                     type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
                     memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',
                     scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1,
                     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['SW-1-3'].submit(consistencyChecking=OFF, datacheckJob=True)

mdb.JobFromInputFile(name='SW-2',
                     inputFileName='D:\\software\\SIMULIA\\Temp\\JinGuangZeSheerWall\\SW-2\\SW-2.inp',
                     type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
                     memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',
                     scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1,
                     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['SW-2'].submit(consistencyChecking=OFF, datacheckJob=True)

mdb.JobFromInputFile(name='SW-3',
                     inputFileName='D:\\software\\SIMULIA\\Temp\\JinGuangZeSheerWall\\SW-2\\SW-3.inp',
                     type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None,
                     memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                     explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, userSubroutine='',
                     scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1,
                     activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)
mdb.jobs['SW-3'].submit(consistencyChecking=OFF, datacheckJob=True)

