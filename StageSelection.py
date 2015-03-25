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
        self.gameOver = None
        
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

        mE.mEntityManager.defineLayerOrder(["BG","UI","GameOverScreen"])

    def loadSounds(self):
        mE.mJukebox.LoadSong(worldMapSong, "WorldMap")
        
        mE.mJukebox.LoadSound(victorySound, "Win")
        mE.mJukebox.LoadSound(worldMapSong, "Lose")
        
    def loadAnimations(self):
        mE.mAnimationManager.addAnimation(lImagesBackgroundWM[0],lImagesBackgroundWM[1],"Background")
        mE.mAnimationManager.addAnimation(lImagesStageWM[0],lImagesStageWM[1],"Stage")
        mE.mAnimationManager.addAnimation(lImagesStageOpenedWM[0],lImagesStageOpenedWM[1],"StageOpened")
        mE.mAnimationManager.addAnimation(lImagesStageBeatedWM[0],lImagesStageBeatedWM[1],"StageBeated")

        mE.mAnimationManager.addAnimation(lImagesGameOverWin[0],lImagesGameOverWin[1],"Win")
        mE.mAnimationManager.addAnimation(lImagesGameOverLose[0],lImagesGameOverLose[1],"Lose")

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
        self.end = False
        while not self.end:
            mE.update()
            self.mHUD.update()
            
            if(mE.keyboard.isPressed(pygame.K_ESCAPE)):
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

        self.gameOver = Entity()
        mE.mEntityManager.addEntity(self.gameOver, "GameOverScreen", "GameOverScreen")
        
        if(self.mGameManager.playerWins):
            print "The player win!"
            self.saveGame(idStage)
            mE.mAnimationManager.setEntityAnimation(self.gameOver, "Win")
        else:
            print "The player loose!"
            mE.mAnimationManager.setEntityAnimation(self.gameOver, "Lose")
        
        mE.mEntityManager.entitys["Button"] = []
        self.loadSaveGame()
        self.loadStageGraph()
        self.gameOverScreenUpdate(self.mGameManager.playerWins)
        self.update()

    def gameOverScreenUpdate(self, win = True):
        self.end = False
        if(win):
            mE.mJukebox.PlaySound("Win")
        else:
           mE.mJukebox.PlaySound("Lose")
           
        tIniLoop = mE.getGameTime()
        while not self.end:
            mE.update()
            
            if(mE.getGameTime() - tIniLoop >= 3.0  ):
                self.end = True
            if(mE.keyboard.isPressed(pygame.K_ESCAPE)):
                self.end = True
                
            mE.render()
        mE.mEntityManager.removeEntity(self.gameOver, "GameOverScreen")
        self.gameOver = None

    def saveGame(self, idStage):
        self.beatenStages[str(idStage)] = 2
        neighbors = self.stages[str(idStage)][1].split(",")
        if(neighbors != ['']):
            for neighbor in neighbors:
                if(neighbor == ''):
                    break
                if(self.beatenStages[neighbor] == 0):
                    self.beatenStages[neighbor] = 1

        #Saving the game state
        f =  open(".//resources//Saves//save.txt","w")
        for stage in self.beatenStages:
            f.write(str(stage) + "\t" + str(self.beatenStages[stage]) +"\n" )
        f.close()

    def loadSaveGame(self):
        self.beatenStages = {}
        f = open(".//resources//Saves//save.txt")
        save  = f.read().split("\n")

        for s in save:
            if(s != ""):
                s = s.split("\t")
                self.beatenStages[s[0]] = int(s[1])
        f.close()

    def createStage(self, idStage, positionWorldMap, lNextStages, beated):
        positionWorldMap = tuple( positionWorldMap.split(","))
        positionWorldMap = (int(positionWorldMap[0]), int(positionWorldMap[1]))

        params = {"idStage" : idStage}
        
        if(beated == 2):
            s = self.mHUD.addStageButton(self.startLevel, params, positionWorldMap, "StageBeated", Vec2d(64,64), beated)
        elif(beated == 1):
            s = self.mHUD.addStageButton(self.startLevel, params, positionWorldMap, "StageOpened", Vec2d(64,64), beated)
        elif(beated == 0):
            s = self.mHUD.addStageButton(self.startLevel, params, positionWorldMap, "Stage", Vec2d(64,64), beated)
        else:
            print "mah oi"
