from Vector2D import *
import pygame
import time

class Primitive():
    def __init__(self):
        self.color = (0,0,0)
        self.width = 0

class Rect(Primitive):
    def __init__(self):
        Primitive.__init__(self)
        self.init = (0,0)
        self.end = (0,0)

    def getRect(self):
        return (self.init[0],self.init[1], self.end[0], self.init[1])

class Polygon(Primitive):
    def __init__(self):
        Primitive.__init__(self)
        self.vertices = ((0,0),(10,0), (0,10))

    def getVertices(self):
        return self.vertices

    def addVertice(self, v):
        self.vertices += v

class Circle(Primitive):
    def __init__(self):
        Primitive.__init__(self)
        self.position = (0,0)
        self.radius = 10

    def getPosition(self):
        return self.position

    def getRadius(self):
        return self.radius

class Ellipse(Primitive):
    def __init__(self):
        Primitive.__init__(self)
        self.rect = Rect()

class Line(Primitive):
    def __init__(self):
        Primitive.__init__(self)
        self.startPoint = (0,0)
        self.endPoint = (100,100)

class Lines(Primitive):
    def __init__(self):
        Primitive.__init__(self)
        self.closed = False
        self.vertices  = ((0,0),(100,100))

class PrimitiveManager():
    def __init__(self):
        self.primitives = {}
        self.primitives["Rect"]     = {}
        self.primitives["Polygon"]  = {}
        self.primitives["Circle"]   = {}
        self.primitives["Ellipse"]  = {}
        self.primitives["Line"]     = {}
        self.primitives["Lines"]    = {}

    def addPrimitive(self, primitive, tag):
        if isinstance(primitive,Rect):
            if(self.primitives["Rect"].has_key(tag)):
               self.primitives["Rect"][tag] += [primitive]
            else:
               self.primitives["Rect"][tag] = [primitive]

        elif isinstance(primitive,Polygon):
            if(self.primitives["Polygon"].has_key(tag)):
                self.primitives["Polygon"][tag] += [primitive]
            else:
                self.primitives["Polygon"][tag] = [primitive]

        elif isinstance(primitive,Circle):
            if(self.primitives["Circle"].has_key(tag)):
                self.primitives["Circle"][tag] += [primitive]
            else:
                self.primitives["Circle"][tag] = [primitive]

        elif isinstance(primitive,Ellipse):
            if(self.primitives["Ellipse"].has_key(tag)):
                self.primitives["Ellipse"][tag] += [primitive]
            else:
                self.primitives["Ellipse"][tag] = [primitive]

        elif isinstance(primitive,Line):
            if(self.primitives["Line"].has_key(tag)):
                self.primitives["Line"][tag] += [primitive]
            else:
                self.primitives["Line"][tag] = [primitive]

        elif isinstance(primitive, Lines):
            if(self.primitives["Lines"].has_key(tag)):
               self.primitives["Lines"][tag] += [primitive]
            else:
               self.primitives["Lines"][tag] = [primitive]

        else:
            print "Nao existe nenhuma primitiva desse tipo!"


    def removePrimitive(self,primitive,tag):
        
        if isinstance(primitive,Rect):
            self.primitives["Rect"][tag].remove(primitive)

        elif isinstance(primitive,Polygon):
            self.primitives["Polygon"][tag].remove(primitive)

        elif isinstance(primitive,Circle):
            self.primitives["Circle"][tag].remove(primitive)

        elif isinstance(primitive,Ellipse):
            self.primitives["Ellipse"][tag].remove(primitive)

        elif isinstance(primitive,Line):
            self.primitives["Line"][tag].remove(primitive)

        elif isinstance(primitive, Lines):
            self.primitives["Lines"][tag].remove(primitive)

        else:
            print "Nao existe nenhuma primitiva desse tipo!"
        
