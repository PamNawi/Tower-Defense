import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *
from ParticleFunctions import *
from Tiles import *
from Animations import *
from HUD import*
from GameManager import *
from StageSelection import *

class Game:
    def __init__(self):
        global graph
        self.end = False
        self.mStageSelection = StageSelection()
        self.mGameManager = GameManager()

    def startGame(self):
        global PortalGraph
        mE.pushState()

        #self.mStageSelection.load()
        #self.mStageSelection.update()
        self.mGameManager.load()
        self.mGameManager.gameLoop()

        mE.popState()

    def printin(self):
        print "Start Cooldown"

    def loadMenuAnimations(self):
        mE.mAnimationManager.addAnimation(lImagesBackground[0],lImagesBackground[1],"Background")  
        mE.mAnimationManager.addAnimation(lImagesPlayButton[0],lImagesPlayButton[1],"PlayButton")
        mE.mAnimationManager.addAnimation(lImagesOptionsButton[0],lImagesOptionsButton[1],"OptionsButton")
        mE.mAnimationManager.addAnimation(lImagesQuitButton[0],lImagesQuitButton[1],"QuitButton")
        
        mE.mAnimationManager.addAnimation(lImagesButton[0],lImagesButton[1], "Button")
        mE.mAnimationManager.addAnimation(lImagesMouse[0],lImagesMouse[1], "Mouse")

    def menuLoop(self):
        global mE
        mE.cleanEntitys()
        self.loadMenuAnimations()
        
        self.mHud = HUD()
        self.background = Entity()
        mE.mEntityManager.addEntity(self.background, "Background", "BG")
        mE.mAnimationManager.setEntityAnimation(self.background, "Background")

        self.mHud.addButton(self.startGame, None, Vec2d(100,100), "PlayButton")
        self.mHud.addButton(self.startGame, None, Vec2d(140,170), "OptionsButton")
        self.mHud.addButton(self.endGame, None, Vec2d(180,240), "QuitButton")

        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyS[0], lImagesHPBarEnemyS[1], "CooldownBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyE[0], lImagesHPBarEnemyE[1], "CooldownBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyM[0], lImagesHPBarEnemyM[1], "CooldownBarMiddle")

        self.mHud.addCooldownButton(self.printin, None, Vec2d(500,500), "PlayButton")

        mE.mEntityManager.defineLayerOrder(["BG"])
        
        while not self.end:
            mE.update()
            self.mHud.update()
            mE.render()
        print "Acabou"

    def endGame(self):
        self.end = True
            
g = Game()
g.menuLoop()
