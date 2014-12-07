import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *

from Load import *


class HUD:
    def __init__(self):
        self.loadEntitys()

    def loadEntitys(self):
        global mE
        self.mouseEntity = Entity()
        mE.mEntityManager.addEntity(self.mouseEntity, "Mouse")
        mE.mAnimationManager.setEntityAnimation(self.mouseEntity, "Mouse")
        self.mouseEntity.setRadiusBoundingCircle(1)        

        '''t = TabBar()
        t.setMinDesloc(800,80)
        t.setMaxDesloc(800-180,80)
        mE.mEntityManager.addEntity(t,"TabBar")
        mE.mAnimationManager.setEntityAnimation(t, "BarTab")
        
        #b = TabBar()
        #b.setMinDesloc(200,520)
        b.setMaxDesloc(200,520)
        mE.mEntityManager.addEntity(b,"BottomBar")
        mE.mAnimationManager.setEntityAnimation(b,"BottomBar")
        
        e = createEntity(None)
        e.setPosition(800,0)
        t.addEntity(e)
        
        #self.addButton(t.appear,None, Vec2d(100,100),"Button")
        #self.addButton(t.desappear, None, Vec2d(300,100), "Button")'''
        pass

    def addButton(self, bFunction, bParams, bPosition, bTagAnimation):
        global mE
        b = Button()
        mE.mEntityManager.addEntity(b,"Button")
        mE.mAnimationManager.setEntityAnimation(b, bTagAnimation)
        b.setRadiusBoundingCircle(5)
        b.setPosition(bPosition)
        b.function = bFunction
        b.params = bParams

        
    def update(self):
        global mE
        self.mouseEntity.setPosition(mE.mouse.getPosition())

        lButtons = mE.mEntityManager.collision("Mouse","Button")

        if(lButtons):
            lButtons[0][1].startFunction()

def createEntity(params):
    e = Entity()
    mE.mEntityManager.addEntity(e,"Entity")
    mE.mAnimationManager.setEntityAnimation(e, "Aqua1")
    e.setPosition(Vec2d(random.random() * 800, random.random()* 600))
    return e


class Button(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.function = None
        self.params = {}

    def startFunction(self):
        if(self.params != None):
            self.function(self.params)
        else:
            self.function()


class TabBar(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.vecMinDesloc = Vec2d(0,0)
        self.vecMaxDesloc = Vec2d(100,0)
        self.vecSpeedDesloc = Vec2d(0,0)
        self.vecMaxSpeedDesloc = 1

        self.open = False
        self.objects = []

    def appear(self):
        if(not self.open):
            if(self.vecMaxDesloc.x > self.position.x):
                x = self.vecMaxSpeedDesloc
            elif(self.vecMaxDesloc.x < self.position.x):
                x = -self.vecMaxSpeedDesloc
            else:
                x = 0

            if(self.vecMaxDesloc.y > self.position.y):
                y = self.vecMaxSpeedDesloc
            elif(self.vecMaxDesloc.y < self.position.y):
                y = -self.vecMaxSpeedDesloc
            else:
                y = 0

            self.open = True
            self.vecSpeedDesloc = Vec2d(x,y)

    def desappear(self):
        if(self.open):
            if(self.vecMinDesloc.x > self.position.x):
                x = self.vecMaxSpeedDesloc
            elif(self.vecMinDesloc.x < self.position.x):
                x = -self.vecMaxSpeedDesloc
            else:
                x = 0

            if(self.vecMinDesloc.y > self.position.y):
                y = self.vecMaxSpeedDesloc
            elif(self.vecMinDesloc.y < self.position.y):
                y = -self.vecMaxSpeedDesloc
            else:
                y = 0

            self.vecSpeedDesloc = Vec2d(x,y)
            self.open = False

    def addEntity(self, entity):
        self.objects += [entity]

    def update(self):
        if((self.position == self.vecMaxDesloc) and self.open or (self.position == self.vecMinDesloc) and not self.open):
            self.vecSpeedDesloc = Vec2d(0,0)
        self.position = self.position + self.vecSpeedDesloc

        for o in self.objects:
            o.position = o.position + self.vecSpeedDesloc


    def setMinDesloc(self, x, y = None):
        if( y == None):
            self.vecMinDesloc = x

        else:
            self.vecMinDesloc = Vec2d(x,y)
        self.setPosition(x,y)


    def setMaxDesloc(self, x, y = None):
        if( y == None):
            self.vecMaxDesloc = x

        else:
            self.vecMaxDesloc = Vec2d(x,y)
