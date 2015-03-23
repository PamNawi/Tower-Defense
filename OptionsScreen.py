import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *
from ParticleFunctions import *
from Tiles import *
from Animations import *
from HUD import*
from GameManager import *
from StageSelection import *

class OptionsScreen:
    def __init__(self):
        pass

    def loadElements(self):
        pass

    def showElements(self):
        #Add all elements to EntityManager
        pass

    def hideElements(self):
        #Just remove all elements from EntityManager
        pass

    def saveOptions(self):
        pass

    def loadOptions(self):
        pass
