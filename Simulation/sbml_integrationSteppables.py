from PlayerPython import * 
import CompuCellSetup
from PySteppables import *
import CompuCell
import sys

from PySteppablesExamples import MitosisSteppableBase
            

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        for cell in self.cellList:
            cell.targetVolume=100
            cell.lambdaVolume=2.0
        
        

class GrowthSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        self.scalarCycBField = self.createScalarFieldCellLevelPy("CycB")
        
    def start(self):
        modelFile = './Simulation/BIOMD0000000195_url.xml'  
        
        initialConditions = {}
#             initialConditions['SPECIES_NAME1'] = species_val1
#             initialConditions['SPECIES_NAME2'] = species_val2
        
        stepSize = 0.5
        
        self.addSBMLToCellIds(_modelFile=modelFile, _modelName='cellcycle', _ids=[1], _stepSize=stepSize,
                              _initialConditions=initialConditions)
        
        for cell in self.cellList:
            cell.dict['lastCycB'] = 0
            
            
    def step(self,mcs):
        self.timestepSBML()
        for cell in self.cellList:
            state = self.getSBMLState(_modelName='cellcycle', _cell=cell)   
            self.scalarCycBField[cell] = float(state["CycB"])
                
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,_simulator,_frequency=1):
        MitosisSteppableBase.__init__(self,_simulator, _frequency)
        self.scalarCycBField = self.createScalarFieldCellLevelPy("CycB")
    
    def step(self,mcs):
        cells_to_divide = []
        
        
        
        for cell in self.cellList:
            state = self.getSBMLState(_modelName='cellcycle', _cell=cell)   

            print "            cycB",state["CycB"]
        
            if float(state["CycB"]) < 0.5 and cell.dict['lastCycB'] >= 0.5:
                cells_to_divide.append(cell)
            cell.dict['lastCycB'] = float(state["CycB"])
            
        for cell in cells_to_divide:
            self.divideCellRandomOrientation(cell)

    def updateAttributes(self):
#         self.parentCell.targetVolume /= 2.0              
        self.cloneParent2Child()            
        
