import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *

from Load import *

from GameManager import *

class StageSelection:
    def __init__(self):
        self.end = False
        self.mGameManager = GameManager()
        self.stages = {}
        pass

    def load(self):
        print "Loading Stage Selection"
        self.loadAnimations()
        self.loadStageGraph()
        self.loadHUD()

        self.background = Entity()
        mE.mEntityManager.addEntity(self.background,"Background", "BG")
        mE.mAnimationManager.setEntityAnimation(self.background, "Background")

        mE.mEntityManager.defineLayerOrder(["BG"])
        
    def loadAnimations(self):
        mE.mAnimationManager.addAnimation(lImagesBackground[0],lImagesBackground[1],"Background")  
    
    def loadHUD(self):
        pass

    def loadStageGraph(self):
        stageGraph = ".//resources//StageSelection//Stages.txt"
        f = open(stageGraph)
        fstages = f.read()
        fstages = fstages.split("\n")
        for stage in fstages:
            s = stage.split("\t")
            self.stages[s[0]] = [ s[1],s[2]]
            print self.stages
        

    def update(self):
        while not self.end:
            mE.update()
            #self.mHud.update()
            mE.render()

            if(mE.keyboard.isPressed(pygame.K_SPACE)):
                self.end = True
        print "Acabou"

    def startLevel(self):
        global PortalGraph
        mE.pushState()
        
        self.mGameManager.load()
        self.mGameManager.gameLoop()

        mE.popState()
