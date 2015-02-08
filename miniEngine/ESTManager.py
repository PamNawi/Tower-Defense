import pygame
from Vector2D import *
from Entity import *
from ParticleManager import *

class AnimationManager:
    def __init__(self):
        self.animations = {}

    def addAnimation(self, lImages, speed, aTag):
        a = Animation(lImages, speed)
        self.animations[aTag] = a

    def setEntityAnimation(self, entity, aTag):
        entity.animations[aTag] = self.animations.get(aTag)
        entity.surface = self.animations.get(aTag)

    def addEntityAnimation(self, entity, aTag):
        entity.animations[aTag] = self.animations.get(aTag)

class EntityManager:
    def __init__(self, ):
        self.entitys = {}

        self.layers = {}
        self.layerOrder = []

    def addEntity(self, entity, tag , layer = None):
        try:
            self.entitys[tag] += [entity]
        except KeyError:
            self.entitys[tag] = [entity]
            if(layer != None):
                entity.layer = layer
                #Add tag to a layer
                try:
                    self.layers[layer] += [tag]
                except KeyError:
                    self.layers[layer] = [tag]

    def removeEntity(self, entity, tag):
        self.entitys[tag].remove(entity)        

    def update(self):
        lEntitys = self.entitys.values()
        for l in lEntitys:
            for e in l:
                e.update()

    def getTagEntitys(self, tag):
        if(self.entitys.has_key(tag)):
           return self.entitys[tag]
        return []

    def collision(self, tag1, tag2):
        if( not self.entitys.has_key(tag1) or not self.entitys.has_key(tag2)):
            return []
        lEntitys1 = self.entitys[tag1]
        lEntitys2 = self.entitys[tag2]

        lCollisions = []
        for e in lEntitys1:
            for e2 in lEntitys2:
                if(isOnCollision(e, e2)):
                   lCollisions += [(e,e2)]
        return lCollisions

    def defineLayerOrder(self, layerOrder):
        self.layerOrder = layerOrder
        for layer in layerOrder:
            if not self.layers.has_key(layer):
                self.layers[layer] = []
    
class Text:
    def __init__(self):
        self.position = Vec2d(0,0)

        self.content = ""
        self.font = None

        self.color = (0,0,0)
        self.antiAlias = 1

    def setPosition(self, x ,y = None):
        if(type(x) == tuple):
            self.position = Vec2d(x[0],x[1])
        elif(y == None):
            self.position = Vec2d(x.x , x.y)
        else:
            self.position = Vec2d(x,y)

class TextManager:
    def __init__(self):
        self.texts = {}
        self.fonts = {}

    def addText(self, text, tag):
        self.texts[tag] = text

    def addFont(self, font, tag):
        self.fonts[tag] = font

    def setTextFont(self, tagText, tagFont):
        self.texts[tagText].font = self.fonts[tagFont]
        
