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
        self.mHUD = HUD()
        pass

    def load(self):
        print "Loading Stage Selection"
        self.loadAnimations()
        self.loadSounds()
        self.loadSaveGame()
        self.loadStageGraph()
        self.mHUD.loadEntitys()

        self.background = Entity()
        mE.mEntityManager.addEntity(self.background,"Background", "BG")
        mE.mAnimationManager.setEntityAnimation(self.background, "Background")

        mE.mEntityManager.defineLayerOrder(["BG"])

    def loadSounds(self):
        mE.mJukebox.LoadSong(worldMapSong, "WorldMap")
        
    def loadAnimations(self):
        mE.mAnimationManager.addAnimation(lImagesBackgroundWM[0],lImagesBackgroundWM[1],"Background")
        mE.mAnimationManager.addAnimation(lImagesStageWM[0],lImagesStageWM[1],"Stage")
        mE.mAnimationManager.addAnimation(lImagesStageOpenedWM[0],lImagesStageOpenedWM[1],"StageOpened")
        mE.mAnimationManager.addAnimation(lImagesStageBeatedWM[0],lImagesStageBeatedWM[1],"StageBeated")

    def loadStageGraph(self):
        stageGraph = ".//resources//StageSelection//Stages.txt"
        f = open(stageGraph)
        fstages = f.read()
        fstages = fstages.split("\n")
        for stage in fstages:
            s = stage.split("\t")
            self.stages[s[0]] = [s[1],s[2]]
            self.createStage(s[0], s[1], s[2], self.beatenStages[s[0]])
        f.close()
            
    def update(self):
        
        mE.mJukebox.PlaySong("WorldMap")
        
        while not self.end:
            mE.update()
            self.mHUD.update()

            if(mE.keyboard.isPressed(pygame.K_SPACE)):
                self.end = True
                
            mE.render()
        print "Acabou"

    def startLevel(self, params):
        global PortalGraph
        mE.pushState()
        idStage = int(params["idStage"])
        self.mGameManager.actualLevel = idStage
        self.mGameManager.load()
        self.mGameManager.gameLoop()

        mE.popState()

    def loadSaveGame(self):
        self.beatenStages = {}
        f = open(".//resources//Saves//save.txt")
        save  = f.read().split("\n")

        for s in save:
            s = s.split("\t")
            self.beatenStages[s[0]] = int(s[1])

    def createStage(self, idStage, positionWorldMap, lNextStages, beated):
        positionWorldMap = tuple( positionWorldMap.split(","))
        positionWorldMap = (int(positionWorldMap[0]), int(positionWorldMap[1]))

        params = {"idStage" : idStage}
        
        if(beated == 2):
            s = self.mHUD.addStageButton(self.startLevel, params, positionWorldMap, "StageBeated", Vec2d(64,64), beated)
        elif(beated == 1):
            s = self.mHUD.addStageButton(self.startLevel, params, positionWorldMap, "StageOpened", Vec2d(64,64), beated)
        else:
            s = self.mHUD.addStageButton(self.startLevel, params, positionWorldMap, "Stage", Vec2d(64,64), beated)
