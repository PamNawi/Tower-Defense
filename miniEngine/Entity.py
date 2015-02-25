from Vector2D import *
from collisionBlock import *
import pygame
import time

class Entity:
    def __init__(self):
        self.surface = None
        self.position = Vec2d(0,0)
        self.tag = ""
        self.rBoundingCircle = 0
        self.centerBoundingCircle = Vec2d(0,0)
        self.animations = {}
        self.layer = None

        self.collisionList = []
        self.collisionBlock = CollisionBlock()

    def setCollisionBlock(self, vecBottomCorner):
        self.collisionBlock.setRect(Vec2d(0,0),vecBottomCorner)
        self.collisionBlock.setPosition(self.position)

    def update(self):
        pass

    def setPosition(self,x,y = None):
        if(type(x) == tuple):
            self.position = Vec2d(x[0],x[1])
        elif(y == None):
            self.position = Vec2d(x.x , x.y)
        else:
            self.position = Vec2d(x,y)

        self.collisionBlock.setPosition(x,y)

    def setRadiusBoundingCircle(self, r):
        self.rBoundingCircle = r

    def setCenterBoundingCircle(self, x, y = None):
        if(type(x) == tuple):
            self.centerBoundingCircle = Vec2d(x[0],x[1])
        elif(y == None):
            self.centerBoundingCircle = Vec2d(x.y , x.y)
        else:
            self.centerBoundingCircle =  Vec2d(x,y)
            

    def startAnimation(self,tag):
        self.surface = self.animations[tag]


    def addCollisionBlock(self, cb):
        self.collisionList.append(cb)

def distanceEntity(e1, e2):
    return e1.position.get_distance(e2.position)

def distanceBoundingCircles(e1,e2):
    e1BC = e1.position + e1.centerBoundingCircle
    e2BC = e2.position + e2.centerBoundingCircle
    d = e1BC.get_distance(e2BC)
    return d

def isOnCollision(e1, e2):
    return e1.collisionBlock.collision(e2.collisionBlock)

class Animation:
    def __init__(self, lImages, speed):
        self.lImages = []
        for image in lImages:
            i = pygame.image.load(image)
            self.lImages += [i]

        self.nFrames = len(lImages)
        self.frame = 0
        self.speed = speed
        self.creationTime = time.clock()
        
    def getFrame(self):
        actualTime = time.clock()
        diffTime = (actualTime - self.creationTime) / self.speed
        actualFrame = diffTime / self.speed
        self.frame = (actualFrame)% self.nFrames
        return self.lImages[int(self.frame)]
