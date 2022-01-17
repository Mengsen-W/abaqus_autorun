'''firewalld
 * @Author: Mengsen.Wang
 * @Date: 2019-12-15 09:56:27
 * @Last Modified by:   Mengsen.Wang
 * @Last Modified time: 2019-12-28 20:56:18
'''
# coding=utf-8
from abaqus import *
from abaqusConstants import *
from caeModules import *
import math


class MyModel:
    """MyModel Class"""
    """init public members"""
    diameterLongitudinalBar = 10
    betweenLongitudinalBar = 80
    diameterTransversalBar = 8
    betweenTransversalBar = 80
    yieldStressLongitudinalBar = 400
    yieldStressTransversalBar = 300
    displacement = 35
    axialLoad = 3000000
    meshSize = 50
    jobName = 'SheerWall-Job'

    """setting parameters """
    parameters = (
        ("Model Name:", "ShearWall"),
        ("Diameter(longitudinal bar)(mm):", "10"),
        ("Diameter(transversal bar)(mm):", "8"),
        ("Yield stress(longitudinal bar)(N/mm):", "400"),
        ("Space between longitudinal bar", "80"),
        ("Yield stress(transversal bar)(N/mm):", "300"),
        ("Space between transversal bar", "80"),
        ("Displacement(maximum)(mm):", "35"),
        ("axial-load(KN):", "3000000"),
        ("Mesh Size(mm):", "50"),
        ("Job Name:", "Job-NewShearWall-01"),
    )

    def __init__(self):
        self.Input()

    def Input(self):
        """Input Parameters"""
        (modelName,
         diameterLongitudinalBar, betweenLongitudinalBar,
         diameterTransversalBar, betweenTransversalBar,
         yieldStressLongitudinalBar, yieldStressTransversalBar,
         displacement, axialLoad, meshSize, jobName,
         ) = getInputs(
            fields=self.parameters, label="Please Input The Parameter", dialogTitle="Parameter Input"
        )
        myModel = mdb.Model(name=modelName)
        self.diameterLongitudinalBar = float(diameterLongitudinalBar)
        self.betweenLongitudinalBar = float(betweenLongitudinalBar)
        self.diameterTransversalBar = float(diameterTransversalBar)
        self.betweenTransversalBar = float(betweenTransversalBar)
        self.yieldStressLongitudinalBar = float(yieldStressLongitudinalBar)
        self.yieldStressTransversalBar = float(yieldStressTransversalBar)
        self.displacement = float(displacement)
        self.axialLoad = float(axialLoad)
        self.meshSize = float(meshSize)
        self.jobName = "SheerWall-Job"

class Foundation(MyModel):
    """Foundation Class"""
    """init Foundation member """
    coverFoundation = 20.0
    longFoundation = 1200.0
    highFoundation = 600.0
    thicknessFoundation = 600.0

    """Show parameters"""
    parameters = (
        ("Length(foundation)(mm):", "1200"),
        ("Thickness(foundation)(mm):", "600"),
        ("Height(foundation)(mm):", "600"),
        ("Cover(foundation)(mm):", "20"),
    )

    def __init__(self):
        self.Input()

    def Input(self):
        """Input Parameters"""
        (coverFoundation, longFoundation, thicknessFoundation, highFoundation,) = getInputs(
            fields=self.parameters, label="Please Input The Parameter", dialogTitle="Parameter Input")
        self.coverFoundation = float(coverFoundation)
        self.longFoundation = float(longFoundation)
        self.thicknessFoundation = float(thicknessFoundation)
        self.highFoundation = float(highFoundation)


class SheerWall(MyModel):

    """Sheer Wall Class"""

    """Init public members"""
    modelName = "SheerWall"
    coverSheerWall = 20.0
    longSheerWall = 800.0
    highSheerWall = 1200.0
    thicknessSheerWall = 200.0

    """setting parameters """
    parameters = (
        ("Cover(wall)(mm):", "20"),
        ("Length(wall)(mm):", "800"),
        ("Thickness(wall)(mm):", "200"),
        ("Height(wall)(mm):", "1200"),
    )

    def __init__(self):
        self.Input()

    def Input(self):
        """Input Parameters"""
        (coverSheerWall, longSheerWall, highSheerWall, thicknessSheerWall,) = getInputs(
            fields=self.parameters, label="Please Input The Parameter", dialogTitle="Parameter Input")
        self.coverSheerWall = float(coverSheerWall)
        self.longSheerWall = float(longSheerWall)
        self.highSheerWall = float(highSheerWall)
        self.thicknessSheerWall = float(thicknessSheerWall)


class LoadBeam(MyModel):
    """LoadBeam Class"""
    """init public members"""
    coverLoadBeam = 20.0
    longLoadBeam = 1000.0
    highLoadBeam = 600.0
    thicknessLoadBeam = 600.0

    """setting parameters """
    parameters = (
        ("Length(loadbeam)(mm):", "1000"),
        ("Thickness(loadbeam)(mm):", "300"),
        ("Height(loadbeam)(mm):", "600"),
        ("Cover(loadbeam)(mm):", "20"),
    )

    def __init__(self):
        self.Input()

    def Input(self):
        """Input Parameters"""
        (coverLoadBeam, longLoadBeam, highLoadBeam, thicknessLoadBeam,) = getInputs(
            fields=self.parameters, label="Please Input The Parameter", dialogTitle="Parameter Input")
        self.coverLoadBeam = float(coverLoadBeam)
        self.longLoadBeam = float(longLoadBeam)
        self.highLoadBeam = float(highLoadBeam)
        self.thicknessLoadBeam = float(thicknessLoadBeam)


class InteractionInstance:
    pass


class StepMyModel:
    pass


class BoundaryLoad:
    pass


class MashMyModel:
    pass


class JobMyModel:
    pass


sheerwall = MyModel()
