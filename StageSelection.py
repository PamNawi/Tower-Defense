import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *

from Load import *

from GameManager import *

class StageSelection:
    def __init__(self):
        self.mGameManager = GameManager()
        pass

    def load(self):
        print "Loading Stage Selection"
        self.loadHUD()

    def loadHUD(self):
        pass


    def update(self):
        pass

    def startLevel(self):
        global PortalGraph
        mE.pushState()
        
        self.mGameManager.load()
        self.mGameManager.gameLoop()

        mE.popState()
