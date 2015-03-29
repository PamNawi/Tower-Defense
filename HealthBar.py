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

        self.setPosition(self.position)

    def heal(self, healPower = None):
        if(healPower == None):
            self.health = self.maxHealth
        else:
            self.health += healPower
            if(self.heal > self.maxHealth):
                self.heal = self.maxHealth
        self.setPosition(self.position)

    def setPosition(self, position):
        Entity.setPosition(self,position)

        self.start.setPosition(position)
        desloc = 1
        
        for mid in self.middle[:int(self.health)]:
            mid.setPosition(Vec2d(position[0]+desloc * self.wMiddle, position[1]))
            desloc +=1
        for mid in self.middle[int(self.health):]:
            mid.setPosition(Vec2d(-100,-100))
        self.end.setPosition(position[0] + self.wMiddle * desloc, position[1])

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

            self.end.setPosition(position[0] + self.wMiddle * desloc +1, position[1])
            for i in self.middle[cooldown:]:
                i.setPosition(self.start.position)


    def activeCooldown(self):
        if (not self.isActive()):
            self.active = True
            self.lastActivation =  mE.getGameTime()
    def isActive(self):
        return self.active

class ProgressBar(Bar):
    def __init__(self, totalMonsters = 100):
        Bar.__init__(self, totalMonsters)

        self.totalMonsters = totalMonsters
        self.actualMonster = 0
        self.tag = "LevelProgress"

        for m in self.middle:
            m.setPosition(self.position)

        self.backStart = Entity()
        self.backEnd = Entity()

        self.backMiddle = []
        for i in range(self.totalMonsters):
            self.backMiddle += [ Entity()]

        self.wMidle = 2
        
            
    def summonNext(self):
        if(self.actualMonster < self.totalMonsters):
            self.actualMonster += 1
            desloc = 1

            for m in self.middle[self.actualMonster:]:
                m.setPosition(Vec2d(self.position.x, self.position.y))
            for m in self.middle[:self.actualMonster]:
                m.setPosition(Vec2d(self.position.x+desloc *self.wMiddle, self.position.y))
                desloc+=1

            self.setFluidPosition()

    def setFluidPosition(self):
        self.start.setPosition(self.position + Vec2d(7,3))
        for m in self.middle[self.actualMonster:]:
            m.setPosition(Vec2d(self.position.x + 7, self.position.y + 3))
        desloc = 1
        for m in self.middle[:self.actualMonster]:
            m.setPosition(Vec2d(self.position.x+ desloc * self.wMiddle + 7, self.position.y + 3))
            desloc+=1

        self.end.setPosition(self.position.x+self.wMiddle * desloc + 7, self.position.y +3 )

    def setPosition(self,position):
        Entity.setPosition(self,position)
        self.setFluidPosition()
        
        self.start.setPosition(position + Vec2d(7,3))
        for m in self.middle[self.actualMonster:]:
            m.setPosition(Vec2d(self.position.x + 7, self.position.y + 3))
        desloc = 1
        for m in self.middle[:self.actualMonster]:
            m.setPosition(Vec2d(self.position.x+desloc * self.wMiddle + 7, self.position.y + 3))
            desloc+=1

        self.end.setPosition(self.position.x+self.wMiddle * desloc + 7, self.position.y +3 )

        self.backStart.setPosition(position )
        desloc = 1
        for m in self.backMiddle:
            m.setPosition(Vec2d(self.position.x + desloc * self.wMiddle + 7, self.position.y ))
            desloc +=1

        self.backEnd.setPosition(self.position.x + desloc * self.wMiddle +7, self.position.y)


    def setAnimation(self,startTag, endTag, middleTag, backStartTag, backEndTag, backMiddleTag):
        Bar.setAnimation(self,startTag, endTag, middleTag)

        mE.mAnimationManager.setEntityAnimation(self.backStart,backStartTag)
        mE.mAnimationManager.setEntityAnimation(self.backEnd,backEndTag)
        
        for m in self.backMiddle:
            mE.mAnimationManager.setEntityAnimation(m,backMiddleTag)

    def addBarToEntityManager(self):
        global mE
        addBarToEntityManager(self)

        mE.mEntityManager.addEntity(self.backStart, self.tag+"Back", "BackUI")
        mE.mEntityManager.addEntity(self.backEnd, self.tag+"Back", "BackUI")

        for m in self.backMiddle:
            mE.mEntityManager.addEntity(m, self.tag+"Back", "BackUI")
    
