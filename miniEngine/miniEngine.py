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

pygame.init()
pygame.font.init()

class Renderer:
    def __init__(self, width = 800, height = 600):
        size = (width,height)
        self.screen = pygame.display.set_mode(size)
        self.width = width
        self.height = height
        
    def render(self, mEM , mPrM, mTexts, mMM , mPM):
        self.screen.fill((0,0,0))

        self.onScreen = []
        
        self.renderMaps(mMM)
        self.renderEntitys(mEM)
        self.renderParticles(mPM)

        self.depthSort()
        self.renderAll()
        self.renderPrimitives(mPrM)
        self.renderTexts(mTexts)
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

    def renderParticles(self, mPM):
        lEntitys = mPM.getParticles()
        for e in lEntitys:
                if ( self.isOnScreen(e)):
                    self.onScreen += [e]

    def renderTexts(self, mTexts):
        #Render all texts
        lTexts = mTexts.texts.values()
        for t in lTexts:
            self.screen.blit(t.font.render(t.content, t.antiAlias, t.color), (t.position.x , t.position.y))
        

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

    def renderAll(self):
        #If is on screen, render
        for e in self.onScreen:
            if e.surface != None:
                self.screen.blit(e.surface.getFrame(), (e.position[0], e.position[1]))


    def renderPrimitives(self, mPM):
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
                pygame.draw.circle(self.screen,c.color,c.position, c.radius)

        for le in lellipses:
            for e in le:
                pygame.draw.ellipse(self.screen,e.color,pygame.Rect(e.rect.init, e.rect.end))

        for ll in llLine:
            for l in ll:
                pygame.draw.line(self.screen, l.color, l.startPoint, l.endPoint)

        for ll in llines:
            for l in ll:
                pygame.draw.lines(self.screen, l.color, l.closed, l.vertices)    
                
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

        self.mGlobalVariables = {}
        pygame.key.set_repeat(100,100)

        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.nParticles = nParticles

        self.stateStack = []

    def render(self):
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
        self.mEntityManager.update()
        self.mMapManager.update()
        self.mParticleManager.update()
        
        self.endGame = self.treatEvents()
        self.mouse.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        self.keyboard.update(pygame.key.get_pressed())


    def pushState(self):
        state = (self.mEntityManager, self.mAnimationManager, self.mPrimitiveManager, self.mTextManager, self.mSwarmManager, self.mMapManager, self.mParticleManager)
        self.stateStack.append(state)
        
        self.mEntityManager = EntityManager()
        self.mAnimationManager = AnimationManager()
        self.mPrimitiveManager = PrimitiveManager()
        self.mTextManager = TextManager()
        self.mSwarmManager = SwarmManager()
        self.mMapManager = MapManager()
        self.mParticleManager = ParticleManager(self.nParticles)

    def popState(self):
        state = self.stateStack.pop()

        self.mEntityManager = state[0]
        self.mAnimationManager = state[1]
        self.mPrimitiveManager = state[2]
        self.mTextManager = state[3]
        self.mSwarmManager = state[4]
        self.mMapManager = state[5]
        self.mParticleManager = state[6]


    def setGlobalVariable(self, tag, value = None):
        self.mGlobalVariables[tag] = value     
