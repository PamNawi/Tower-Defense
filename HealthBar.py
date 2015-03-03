from Load import *

from UIBar import *

class HealthBar(Bar):
    def __init__(self, maxHealth):
        Bar.__init__(self,maxHealth)
        self.maxHealth = maxHealth
        self.health = maxHealth
        tag = "HealBar"
        
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


class CooldownBar(Bar):
    def __init__(self, maxWMiddle, cooldownTime = 1.0):
        Bar.__init__(self,maxWMiddle)
        self.cooldownTime = cooldownTime
        tag = "CooldownBar"

        self.active = False
        self.lastActivation =  0.0 #mE.mGlobalVariables["GameTime"] - cooldownTime

        self.setPosition(Vec2d(0,0))

    def update(self):
        if(self.isActive()):
            #print (mE.getGameTime(),mE.mGlobalVariables["PausedTime"],self.lastActivation)
            diffLastActivation = mE.getGameTime() - self.lastActivation
            if(diffLastActivation >= self.cooldownTime):
                self.active = False

            #print diffLastActivation
            cooldown = int((self.maxMiddle * diffLastActivation)/ self.cooldownTime )
            #print cooldown
            desloc = 0
            position = (self.position.x,self.position.y)
            for i in self.middle[:cooldown]:
                i.setPosition(Vec2d(position[0]+desloc*self.wMiddle,position[1]))
                desloc += 1

            self.end.setPosition(position[0] + self.wMiddle * desloc, position[1])
            for i in self.middle[cooldown:]:
                i.setPosition(self.start.position)


    def activeCooldown(self):
        if (not self.isActive()):
            self.active = True
            self.lastActivation =  mE.getGameTime()
    def isActive(self):
        return self.active

    
    
