import os
import random
import pygame
from Vector2D import *

class CollisionBlock:
	def __init__(self):
		self.rect =  pygame.Rect(0, 0, -1, -1)
		self.center = Vec2d(0,0)
		
	def setRect(self, topCorner, bottomCorner):
                self.rect = pygame.Rect(topCorner.x,topCorner.y, topCorner.x+bottomCorner.x, topCorner.y+bottomCorner.y)
                self.center = Vec2d( (topCorner.x + bottomCorner.x)/2 , (topCorner.y + bottomCorner.y)/2 )

        def setPosition(self, x,y =None):
                if(type(x) == tuple):
                        self.rect.centerx = x[0] + self.center.x
                        self.rect.centery = x[1] + self.center.y
                elif(y == None):
                        self.rect.centerx = x.x + self.center.x
                        self.rect.centery = x.y + self.center.y
                else:
                        self.rect.centerx = x + self.center.x
                        self.rect.centery = y + self.center.y

	def collision(self, other):
		return self.rect.colliderect(other.rect)

class listCollisionBlock:
        def __init__(self):
                self.collisionBlocks = {}

        def createCollisionBlock(self, topCorner, bottomCorner, tagCollisionBlock):
                cb = CollisionBlock()
                cb.setRect(topCorner, bottomCorner)
                self.collisionBlocks[tagCollisionBlock] = cb

        def moveCollisionBlock(self, deslocX, deslocY, tagCollisionBlock):
                self.collisionBlocks[tagCollisionBlock].move(deslocX, deslocY)

        def setCollisionBlockCenter(self, x, y, tagCollisionBlock):
                self.collisionBlocks[tagCollisionBlock].setCenterPosition(x,y)


        def moveAll(self, deslocX, deslocY):
                for tag in self.collisionBlocks:
                        self.collisionBlocks[tag].move(deslocX,deslocY)

        def getCollisionList(self, other):
                listCollision = []
                if(other is listCollisionBlock):
                        for tag in self.collisionBlocks:
                                listCollision += other.getCollisionList(self.collisionBlocks[tag])

                elif(other is CollisionBlock):
                        for tag in self.collisionBlocks:
                                if(self.collisionBlocks[tag].collision(other)):
                                        listCollision += [tag]
                return listCollision
