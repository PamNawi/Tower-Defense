import os
import random
import pygame
from Vector2D import *

class CollisionBlock:
	def __init__(self):
		self.rect = None

	def setRect(self,  topCorner, bottomCorner):
		self.rect = pygame.Rect(topCorner.x,topCorner.y, bottomCorner.x, bottomCorner.y)

	def move(self, deslocX, deslocY):
		self.rect.move(deslocX, deslocY)

	def setCenterPosition(self, x, y):
		deslocCenterX = x - self.rect.centerx
		deslocCenterY = y - self.rect.centery

		self.move(deslocCenterX, deslocCenterY)

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
