from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=300,
                 height=180)
session.Viewport['Viewport: 1'].makeCurrent()
session.Viewport['Viewport: 1'].maxmize()