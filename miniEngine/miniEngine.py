import pygame
import math
import sys
import time

from Input import *
from PrimitiveManager import *
from ESTManager import *
from AIManager import *
from Swarm import *
from graphFromMap import *

from Jukebox import *

pygame.init()
pygame.font.init()

class Renderer:
    def __init__(self, width = 800, height = 600):
        size = (width,height)
        self.screen = pygame.display.set_mode(size)
        self.width = width
        self.height = height
        
    def render(self, mEM , mPrM, mTexts, mMM , mPM, shakeVec = Vec2d(0,0)):
        self.screen.fill((0,0,0))

        self.onScreen = []
        
        self.renderMaps(mMM)
	self.renderAll(shakeVec)
        self.renderPrimitives(mPrM, shakeVec)
        self.renderEntitys(mEM)
        self.renderParticles(mPM)

        self.depthSort()
        self.renderAll(shakeVec)
        self.renderTexts(mTexts, shakeVec)

        #self.renderCollisionBlocks(mEM)
        pygame.display.flip()

    def isOnScreen(self, entity):
        if (entity.position[0] > 0 or entity.position[0] < self.width or entity.position[1] > 0 or entity.position[1] < self.height):
            return True
        return False

    def renderEntitys(self, mEM):
        #Get all tags and put on a list
        #For every tag on a layer
        #Remove the tag from this list
        lEntitys = []
        lTags = mEM.entitys.keys()
        for layer in mEM.layerOrder:
            for tag in mEM.layers[layer]:
                lEntitys += mEM.entitys[tag]
                lTags.remove(tag)

        #Now we have all others tags
        for tag in lTags:
            lEntitys += mEM.entitys[tag]
        #Render Entitys
        onScreen = []
        #get only who is on screen
        for e in lEntitys:
            if ( self.isOnScreen(e)):
                self.onScreen += [e]

    def renderCollisionBlocks(self, mEM):
        lEntitys = []
        lTags = mEM.entitys.keys()

        lCollisionBlocks = []
        for tag in lTags:
            for entity in mEM.entitys[tag]:
                lCollisionBlocks += [entity.collisionBlock.rect]
        for r in lCollisionBlocks:
            pygame.draw.rect(self.screen,(255,0,0),r)

    def renderParticles(self, mPM):
        lEntitys = mPM.getParticles()
        for e in lEntitys:
                if ( self.isOnScreen(e)):
                    self.onScreen += [e]

    def renderTexts(self, mTexts, shakeVec = Vec2d(0,0)):
        #Render all texts
        lTexts = mTexts.texts.values()
        for t in lTexts:
            self.screen.blit(t.font.render(t.content, t.antiAlias, t.color), (t.position.x + shakeVec.x , t.position.y + shakeVec.y))
        

    def renderMaps(self,mMM):
        #Same process as Entitys for Maps
        lMaps = []
        lTags = mMM.maps.keys()
        for layer in mMM.layers:
            lMaps += [mMM.maps[layer]]
            lTags.remove(layer)

        for tag in lTags:
            lMaps = mMM.maps[tag]
                
        #Render Maps
        for m in lMaps:
            mTiles = m.map
            for line in mTiles:
                for col in line:
                    if ( self.isOnScreen(col)):
                        #print (col.surface.creationTime,col.surface.speed, col)
                        self.onScreen += [col]

    def depthSort(self):
        pass

    def renderAll(self, shakeVec = Vec2d(0,0)):
        #If is on screen, render
        for e in self.onScreen:
            if e.surface != None:
                self.screen.blit(e.surface.getFrame(), (e.position[0] + shakeVec.x, e.position[1] + + shakeVec.y))
		self.onScreen = []


    def renderPrimitives(self, mPM, shakeVec = Vec2d(0,0)):
        lrects = mPM.primitives["Rect"].values()
        lpolys = mPM.primitives["Polygon"].values()
        lcircles = mPM.primitives["Circle"].values()
        lellipses = mPM.primitives["Ellipse"].values()
        llLine = mPM.primitives["Line"].values()
        llines = mPM.primitives["Lines"].values()
        
        for lr in lrects:
            for r in lr:
                pygame.draw.rect(self.screen,r.color,r.getRect())

        for lp in lpolys:
            for p in lp:
                pygame.draw.polygon(self.screen,p.color,p.vertices)

        for lc in lcircles:
            for c in lc:
                pygame.draw.circle(self.screen,c.color,c.position, c.radius, 1)

        for le in lellipses:
            for e in le:
                pygame.draw.ellipse(self.screen,e.color,pygame.Rect(e.rect.init, e.rect.end))

        for ll in llLine:
            for l in ll:
                try:
                    pygame.draw.line(self.screen, l.color, l.startPoint, l.endPoint)
                except:
                    pass

        for ll in llines:
            for l in ll:
                try:
                    pygame.draw.lines(self.screen, l.color, l.closed, l.vertices , 2)
                except:
                    pass
                
class MiniEngine:
    def __init__(self, width = 1024, height = 768, nParticles = 1000):
        self.mEntityManager = EntityManager()
        self.mAnimationManager = AnimationManager()
        self.mPrimitiveManager = PrimitiveManager()
        self.mRenderer = Renderer(width, height)
        self.mTextManager = TextManager()
        self.mSwarmManager = SwarmManager()
        self.mMapManager = MapManager()
        self.mParticleManager = ParticleManager(nParticles)

        self.mJukebox = Jukebox()

        self.mGlobalVariables = {}
        pygame.key.set_repeat(100,100)

        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.nParticles = nParticles

        self.stateStack = []

        self.pause = False
        self.updateOnPause = []
        self.mGlobalVariables["GameTime"] = 0.0
        self.mGlobalVariables["PausedTime"] = 0.0
        self.mGlobalVariables["ActualPauseTime"] = 0.0
        self.mGlobalVariables["LastPause"] = 0.0

        self.mGlobalVariables["ScreenShake"] = False
        self.mGlobalVariables["tScreenShaking"] = 0.0
        self.mGlobalVariables["tStartShaking"]= 0.0

    def render(self):
        if(self.mGlobalVariables["ScreenShake"]):
            t = self.getGameTime()
            diffTShaking = t -  self.mGlobalVariables["tScreenShaking"]
            if(diffTShaking < self.mGlobalVariables["tStartShaking"]):#still shaking
                amplitude = self.getAmplitudeShaking()
                vecShake = amplitude * 16 * Vec2d(random.random(),random.random())
                self.mRenderer.render(self.mEntityManager, self.mPrimitiveManager, self.mTextManager, self.mMapManager, self.mParticleManager, vecShake)
                return
            else:
                self.mGlobalVariables["ScreenShake"] = False
                
        self.mRenderer.render(self.mEntityManager, self.mPrimitiveManager, self.mTextManager, self.mMapManager, self.mParticleManager)


    def treatEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
               # Set the x, y postions of the mouse click
               self.mouse.update(event.pos, pygame.mouse.get_pressed())


    def cleanEntitys(self):
        self.mEntityManager.entitys = {}
               
    def update(self):
        self.getGameTime()
        #self.printTime()
        
        if(not self.pause):
            self.mEntityManager.update()
            self.mMapManager.update()
        else:
            self.mEntityManager.update(self.updateOnPause)
            self.mMapManager.update(self.updateOnPause)

        self.mParticleManager.update() 
        self.endGame = self.treatEvents()
        self.mouse.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        self.keyboard.update(pygame.key.get_pressed())

    def pushState(self):
        self.mJukebox.StopMusic()
        self.mJukebox.ToggleSound(False)
        state = (self.mEntityManager, self.mAnimationManager, self.mPrimitiveManager, self.mTextManager, self.mSwarmManager, self.mMapManager, self.mParticleManager, self.mJukebox)
        self.stateStack.append(state)
        
        self.mEntityManager = EntityManager()
        self.mAnimationManager = AnimationManager()
        self.mPrimitiveManager = PrimitiveManager()
        self.mTextManager = TextManager()
        self.mSwarmManager = SwarmManager()
        self.mMapManager = MapManager()
        self.mParticleManager = ParticleManager(self.nParticles)
        self.mJukebox = Jukebox()

    def popState(self):
        self.mJukebox.StopMusic()
        state = self.stateStack.pop()

        self.mEntityManager = state[0]
        self.mAnimationManager = state[1]
        self.mPrimitiveManager = state[2]
        self.mTextManager = state[3]
        self.mSwarmManager = state[4]
        self.mMapManager = state[5]
        self.mParticleManager = state[6]
        self.mJukebox = state[7]

    def setGlobalVariable(self, tag, value = None):
        self.mGlobalVariables[tag] = value

    def getGameTime(self):
        if(self.pause):
            self.mGlobalVariables["ActualPauseTime"] =   time.clock() - self.mGlobalVariables["LastPause"]
            self.mGlobalVariables["GameTime"] = time.clock() - self.mGlobalVariables["PausedTime"] - self.mGlobalVariables["ActualPauseTime"]
        else:
            self.mGlobalVariables["GameTime"] = time.clock() - self.mGlobalVariables["PausedTime"]
        return self.mGlobalVariables["GameTime"]

    def getActualPauseTime(self):
        self.mGlobalVariables["ActualPauseTime"] =   time.clock() - self.mGlobalVariables["LastPause"]
        return self.mGlobalVariables["ActualPauseTime"]

    def pauseGame(self):
        self.getGameTime()
        self.mGlobalVariables["LastPause"] = time.clock()
        self.mGlobalVariables["ActualPauseTime"] = 0.0
        self.pause = True

    def unpauseGame(self):
        self.mGlobalVariables["PausedTime"] += self.mGlobalVariables["ActualPauseTime"]
        self.mGlobalVariables["ActualPauseTime"] = 0.0
        self.getGameTime()
        self.pause = False


    def printTime(self):
        print(self.mGlobalVariables["GameTime"],self.mGlobalVariables["PausedTime"],self.mGlobalVariables["ActualPauseTime"], time.clock())


    def activeScreenShake(self,time , frequency = 60):            
        self.mGlobalVariables["ScreenShake"] = True
        self.mGlobalVariables["tScreenShaking"] = time
        self.mGlobalVariables["tStartShaking"]= self.getGameTime()
        self.mGlobalVariables["ShakingFrequency"] = frequency
        sampleCount = int(time * frequency)
        self.samples = []
        for i in range(sampleCount):
            if(random.randint(0,3) % 2 == 0):
                self.samples +=[-1]
            else:
                self.samples +=[1]

    def decay (self, t):
        endShaking = self.mGlobalVariables["tScreenShaking"]  + self.mGlobalVariables["tStartShaking"]
        if(t >= endShaking ): return 0;
 
        return (endShaking - t) / endShaking;

    def getAmplitudeShaking(self):
        t = self.getGameTime() - self.mGlobalVariables["tStartShaking"]
        s = t
        s0 = int(s)
        s1 = s0 + 1

        k = self.decay(t)

        return (self.noise(s0) + (s - s0)*(self.noise(s1) - self.noise(s0))) * k;

    def noise(self, s):
        if( s >= len(self.samples)):
            return 0
        else:
            return self.samples[s]
