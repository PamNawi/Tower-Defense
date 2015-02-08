import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *

from Load import *


class HUD:
    def __init__(self):
        self.texts = {}
        self.tabBars = {}
        self.loadEntitys()

    def loadEntitys(self):
        global mE
        self.mouseEntity = Entity()
        mE.mEntityManager.addEntity(self.mouseEntity, "Mouse")
        mE.mAnimationManager.setEntityAnimation(self.mouseEntity, "Mouse")
        self.mouseEntity.setRadiusBoundingCircle(1)        

    def addButton(self, bFunction, bParams, bPosition, bTagAnimation):
        global mE
        b = Button()
        mE.mEntityManager.addEntity(b,"Button")
        mE.mAnimationManager.setEntityAnimation(b, bTagAnimation)
        b.setRadiusBoundingCircle(5)
        b.setPosition(bPosition)
        b.function = bFunction
        b.params = bParams

    def addTabBar(self, tabBar, tag):
        global mE
        self.tabBars[tag] = tabBar
        mE.mEntityManager.addEntity(tabBar, tag +"TabBar")
        mE.mAnimationManager.setEntityAnimation(tabBar,tag)

    def addEntityToTabBar(self, entity, tagTabBar):
        self.tabBars[tag].addEntity(entity)
        
         
    def update(self):
        global mE
        self.mouseEntity.setPosition(mE.mouse.getPosition())

        #Test for buttons
        lButtons = mE.mEntityManager.collision("Mouse","Button")
        if(lButtons):
            lButtons[0][1].startFunction()

        #Update all texts
        for t in self.texts:
            self.texts[t][0].content = str(mE.mGlobalVariables[self.texts[t][1]])

    def addText(self, text, variableTag, fontTag, tag):
        mE.mTextManager.addText(text, tag)
        mE.mTextManager.setTextFont(tag, fontTag)
        self.texts[tag] = (text,variableTag)
        

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
