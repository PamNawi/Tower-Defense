import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *

from Load import *
from HealthBar import *

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
        self.mouseEntity.setCollisionBlock(Vec2d(4,4))
        #self.mouseEntity.setRadiusBoundingCircle(1)        

    def addButton(self, bFunction, bParams, bPosition, bTagAnimation, vecCollision):
        global mE
        b = Button()
        mE.mEntityManager.addEntity(b,"Button","UI")
        mE.mAnimationManager.setEntityAnimation(b, bTagAnimation)
        b.setRadiusBoundingCircle(5)
        b.setPosition(bPosition)
        b.function = bFunction
        b.params = bParams
        b.setCollisionBlock(vecCollision)

        return b


    def addCooldownButton(self, bFunction, bParams, bPosition, bTagAnimation, vecCollision, cooldown = 1.0):
        global mE
        b = CooldownButton()
        mE.mEntityManager.addEntity(b,"Button","UI")
        mE.mAnimationManager.setEntityAnimation(b, bTagAnimation)
        
        b.setRadiusBoundingCircle(5)
        b.setPosition(bPosition)
        b.function = bFunction
        b.params = bParams
        b.setCollisionBlock(vecCollision)

        addBarToEntityManager(b.cooldownBar)
        return b

    def addStageButton(self, bFunction, bParams, bPosition, bTagAnimation, vecCollision, beated):
        global mE
        b = Stage()
        mE.mEntityManager.addEntity(b,"Button","UI")
        mE.mAnimationManager.setEntityAnimation(b, bTagAnimation)
        b.setRadiusBoundingCircle(5)
        b.setPosition(bPosition)
        b.function = bFunction
        b.params = bParams
        b.setCollisionBlock(vecCollision)
        b.beated = beated

        return b

    def addTabBar(self, tabBar, tag):
        global mE
        self.tabBars[tag] = tabBar
        mE.mEntityManager.addEntity(tabBar, tag +"TabBar","UI")
        mE.mAnimationManager.setEntityAnimation(tabBar,"TabBar")

    def addEntityToTabBar(self, entity, tagTabBar):
        self.tabBars[tag].addEntity(entity)
        
         
    def update(self):
        global mE
        self.mouseEntity.setPosition(mE.mouse.getPosition())

        #Test for buttons
        if(mE.mouse.isPressed("LEFT")):
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

class CooldownButton(Button):
    def __init__(self, cooldown = 1.0):
        Button.__init__(self)
        self.cooldownBar = CooldownBar(18, cooldown)
        self.cooldownBar.setAnimation("CooldownBarStart","CooldownBarEnd", "CooldownBarMiddle")

    def startFunction(self):
        if(not self.cooldownBar.isActive()):
            if(self.params != None):
                self.function(self.params)
            else:
                self.function()

            #self.cooldownBar.activeCooldown()

    def update(self):
        Button.update(self)
        self.cooldownBar.update()

    def activeCooldown(self):
        self.cooldownBar.activeCooldown()            

class Stage(Button):
    def __init__(self):
        Button.__init__(self)
        self.id = 0
        self.lNextStages = []
        self.beated = False
        
    def startFunction(self):
        if(self.beated != 0):
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

    def disappear(self):
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

class TwinkleText(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.text = Text()


        self.content= ""
        self.lastTwinkle = mE.getGameTime()
        self.twinkleCooldown = 1.0

        self.active = True

        self.on = True
        self.nTwinkles = 3
        
    def update(self):
        if(self.nTwinkles < 0 ):
            self.stopTwinkle()
            
        if(self.active):
            diffLastTwinkle = mE.getGameTime() - self.lastTwinkle
            if(diffLastTwinkle >= self.twinkleCooldown):
                if(self.on):
                    self.text.content = self.content
                    self.nTwinkles += -1
                else:
                    self.text.content = ""
                self.on = not self.on
                self.lastTwinkle = mE.getGameTime()

    def stopTwinkle(self):
        self.active = False
        self.text.content = ""

    def startTwinkle(self, nTwinkles = 3):
        self.nTwinkles = nTwinkles
        self.active = True

    def setPosition(self, x, y = None):
        Entity.setPosition(self,x,y)

        self.text.setPosition(x,y)


def createTwinkleText(textContent, fontTag):
        tt = TwinkleText()
        tt.content = textContent

        mE.mTextManager.addText(tt.text,"TwinkleText")
        mE.mTextManager.setTextFont("TwinkleText", fontTag)

        return tt
        
