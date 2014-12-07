from Load import *

class HealthBar(Entity):
    def __init__(self, maxHealth, mdesloc = 1):
        Entity.__init__(self)
        self.maxHealth = maxHealth
        self.health = maxHealth

        self.start = Entity()
        self.end = Entity()
        self.middle = []
        for i in range(maxHealth):
            self.middle += [ Entity()]

        self.mdesloc = mdesloc

    def update(self):
        if(self.health <= 0 ):
            #He is dead jim
            return

    def takeDamage(self, damage):
        self.health += -damage

        #Remove the last "n damage" middle section
        nmiddle = self.middle[int(self.health):]
        self.middle = self.middle[:int(self.health)]

        for i in nmiddle:
            mE.mEntityManager.removeEntity(i, "HealthBarMiddle")
        

    def setPosition(self,position):
        Entity.setPosition(self,position)
        self.start.setPosition(position[0],position[1])

        desloc = 0
        for i in self.middle:
            i.setPosition(Vec2d(position[0] + desloc * self.mdesloc,position[1]))
            desloc +=1
            
        self.end.setPosition(position[0] + self.mdesloc , position[1])

    def setAnimation(self, startTag, endTag, middleTag):
        mE.mAnimationManager.setEntityAnimation(self.start, startTag)
        mE.mAnimationManager.setEntityAnimation(self.end, endTag)

        for i in self.middle:
            mE.mAnimationManager.setEntityAnimation(i, middleTag)

    def addToEntityManager(self):
        mE.mEntityManager.addEntity(self.start, "HealthBarStart", "UI")
        mE.mEntityManager.addEntity(self.end  , "HealthBarEnd", "UI")

        for i in self.middle:
            mE.mEntityManager.addEntity(i, "HealthBarMiddle", "UI")

        
        mE.mEntityManager.addEntity(self, "HealthBar", "UI")

    def removeEntityManager(self):
        mE.mEntityManager.removeEntity(self.start,"HealthBarStart")
        mE.mEntityManager.removeEntity(self.end,"HealthBarEnd")

        for i in self.middle:
            mE.mEntityManager.removeEntity(i, "HealthBarMiddle")

        mE.mEntityManager.removeEntity(self, "HealthBar")
    
