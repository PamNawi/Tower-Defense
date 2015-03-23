import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *
from ParticleFunctions import *
from Tiles import *
from Animations import *
from HUD import*
from GameManager import *
from StageSelection import *

from OptionsScreen import *

class Game:
    def __init__(self):
        global graph
        self.end = False
        self.mStageSelection = StageSelection()
        self.mGameManager = GameManager()
        self.tIniLoop = mE.getGameTime()

        self.oScreen = OptionsScreen()

    def startGame(self):
        global PortalGraph
        mE.pushState()

        self.mStageSelection.load()
        self.mStageSelection.update()

        mE.popState()
        mE.mJukebox.PlaySong("MenuSong")

    def showOptions(self):
        self.oScreen.showElements()

    def load(self):
        self.loadMenuAnimations()
        self.loadMenuSounds()

        self.splash = Entity()
        mE.mEntityManager.addEntity(self.splash, "SplashScreen", "SplashScreen")
        mE.mAnimationManager.setEntityAnimation(self.splash, "SplashScreen")
        
        self.mHud = HUD()
        self.background = Entity()
        mE.mEntityManager.addEntity(self.background, "Background", "BG")
        mE.mAnimationManager.setEntityAnimation(self.background, "Background")

        self.mHud.addButton(self.startGame, None, Vec2d(100 + 44,100 + 200), "PlayButton", Vec2d(192,64))
        self.mHud.addButton(self.showOptions, None, Vec2d(140 + 44,170 + 200), "OptionsButton", Vec2d(192,64))
        self.mHud.addButton(self.endGame, None, Vec2d(180 + 44,240 + 200), "QuitButton", Vec2d(192,64))

        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyS[0], lImagesHPBarEnemyS[1], "CooldownBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyE[0], lImagesHPBarEnemyE[1], "CooldownBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyM[0], lImagesHPBarEnemyM[1], "CooldownBarMiddle")

        self.oScreen.loadElements()
        mE.mEntityManager.defineLayerOrder(["Splash","BG"])
        
    def loadMenuAnimations(self):

        mE.mAnimationManager.addAnimation(lImagesSplashScreen[0],lImagesSplashScreen[1],"SplashScreen")
        mE.mAnimationManager.addAnimation(lImagesBackground[0],lImagesBackground[1],"Background")  
        mE.mAnimationManager.addAnimation(lImagesPlayButton[0],lImagesPlayButton[1],"PlayButton")
        mE.mAnimationManager.addAnimation(lImagesOptionsButton[0],lImagesOptionsButton[1],"OptionsButton")
        mE.mAnimationManager.addAnimation(lImagesQuitButton[0],lImagesQuitButton[1],"QuitButton")
        
        mE.mAnimationManager.addAnimation(lImagesButton[0],lImagesButton[1], "Button")
        mE.mAnimationManager.addAnimation(lImagesMouse[0],lImagesMouse[1], "Mouse")

    def loadMenuSounds(self):
        mE.mJukebox.LoadSong(menuSong, "MenuSong")
        mE.mJukebox.LoadSound(bubbleSound, "BubbleSound")

        mE.mJukebox.PlaySound("BubbleSound")
        
    def menuLoop(self):
        global mE
        self.end = False        

        mE.mJukebox.PlaySong("MenuSong")
        while not self.end:
            mE.update()
            if(mE.getGameTime() - self.tIniLoop >= 3.0 and self.splash != None):
                mE.mEntityManager.removeEntity(self.splash, "SplashScreen")
                self.splash = None
            self.mHud.update()
            mE.render()
        print "Acabou"

    def endGame(self):
        self.end = True
            
g = Game()
g.load()
g.menuLoop()
