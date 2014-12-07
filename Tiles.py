from Load import *
from Animations import *

from MonstersAnimations import *
from MonstersStats import *
from Maps import *
from HealthBar import *

class Portal(Tile):
    def __init__(self, dicParams):
        Tile.__init__(self,dicParams)
        self.mParticleManager = dicParams["ParticleManager"]
        self.waves = dicParams["Waves"]        
        
        self.nextParticle = -1
        self.mParticleManager.addUpdateFunction(lImagesPortalParticle[0],lImagesPortalParticle[1] , spin, "spin")
        self.lastSummon = 0.0

        self.actualWave = 0
        self.newWave()

    def update(self):
        if(self.nextParticle < 0):
            self.mParticleManager.createParticle(self.position,"spin",
                                                 {"CenterVelocity" : Vec2d(0,random.random() * -.6),
                                                  "CenterPosition" : self.position+(32,32+13),
                                                  "Angle"          : random.random() * 360,
                                                  "Radius"         : random.random() * 10,
                                                  "Step"           : 0.05,
                                                  "Dispersion"     : random.random() * 400})

            self.nextParticle = random.random() * 50
        self.nextParticle += -1

        if(time.clock() - self.lastSummon >= 1.0):
            self.lastSummon = time.clock()
            self.summonNextMonster()
        
    def newWave(self):
        self.monsters = []
        tMonster = 0
        for i in self.waves[self.actualWave]:
            self.monsters += [ lMonstersStats[tMonster]["EntityTag"] ] *i
            tMonster += 1
        self.actualWave += 1

    def summonNextMonster(self):
        #print self.monsters
        if(self.monsters):
            tag = random.choice(self.monsters)
            self.monsters.remove(tag)
            self.createMonster(tag)

    
    def createMonster(self,tag):
        global mE
        global graph
        m = Monster()
        mE.mAnimationManager.setEntityAnimation(m, tag)
        mE.mEntityManager.addEntity(m,"Monster","Monsters")
        mE.mPrimitiveManager.addPrimitive(m.lines, "MonsterRoute")
        m.setPosition(m.lPositions[0][0],m.lPositions[0][1])
        
        m.setCenterBoundingCircle(16,16)
        m.setRadiusBoundingCircle(10)
        return m

class Monster(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.graphPosition = mE.mGlobalVariables["PortalCoord"]
        self.lines = Lines()
        self.recalculateRoute()
        
        self.maxSpeed = 1
        self.speed = 1
        
        self.hp = HealthBar(10)
        self.hp.addToEntityManager()
        self.hp.setAnimation("EnemyHealthBarStart", "EnemyHealthBarEnd", "EnemyHealthBarMiddle")
        self.isDead = False
        self.rBoundingCircle = 16

        
        self.poison = 0.0
        self.timePoison = -1
        
    def update(self):
        self.move()
        
        if(self.hp.health <= 0):
            self.die()

        
        self.hp.setPosition(self.position)

    def takeDamage(self, damage):
        self.hp.takeDamage(damage)

    def move(self):
        if(self.lPositions):
            nextPosition = self.lPositions[0]
            if(nextPosition == self.position):
                self.lPositions = self.lPositions[1:]
                
                if(len(self.lPositions) > 0):
                    nextPosition = self.lPositions[0]
                    self.graphPosition = (0, nextPosition[0] - tileWidth /4 , nextPosition[1] - tileHeigth /4)
                    self.lines.vertices = tuple(self.lPositions)
                else:
                    self.hp.health = 0
                    return

            if(nextPosition[0] > self.position[0]):
                self.setPosition(self.position[0] + self.maxSpeed * self.speed, self.position[1])

            if(nextPosition[1] > self.position[1]):
                self.setPosition(self.position[0], self.position[1]+ self.maxSpeed * self.speed)

            if(nextPosition[0] < self.position[0]):
                self.setPosition(self.position[0] - self.maxSpeed * self.speed, self.position[1])

            if(nextPosition[1] < self.position[1]):
                self.setPosition(self.position[0], self.position[1]- self.maxSpeed * self.speed)

            self.lines.vertices = ((self.position.x, self.position.y),) + self.lines.vertices[1:] + (mE.mGlobalVariables["CityCoord"],)
            
    def die(self):
        global mE
        mE.mPrimitiveManager.removePrimitive(self.lines,"MonsterRoute")
        mE.mEntityManager.removeEntity(self,"Monster")
        graph = mE.mGlobalVariables["Graph"]
        graph.addDeath(self.graphPosition)
        self.isDead = True
        self.hp.removeEntityManager()

    def recalculateRoute(self):
        CityCoord       = mE.mGlobalVariables["CityCoord"]
        graph           = mE.mGlobalVariables["Graph"]
        self.path = graph.aStar(self.graphPosition, CityCoord)
        self.transformGraphRouteToScreenRoute()
        self.lines.vertices = tuple(self.lPositions)
        
    def transformGraphRouteToScreenRoute(self):
        self.lPositions = []
        for coord in self.path:
            self.lPositions += [(coord[1] + tileWidth /4, coord[2] + tileHeigth /4)]

class Tower(Entity):
    def __init__(self, radiusRange = 100):
        Entity.__init__(self)
        self.graphPosition = (-1,-1,-1)

        self.hp = HealthBar(10)
        self.hp.addToEntityManager()
        self.hp.setAnimation("TowerHealthBarStart", "TowerHealthBarEnd", "TowerHealthBarMiddle")
        self.rBoundingCircle = 32
        
        self.target = None
        self.range = radiusRange

        self.cooldownShoot = 0.5
        self.lastShoot = time.clock() - self.cooldownShoot

        self.towerEffect = None
        self.chooseTargetMethod = self.chooseTarget
        self.tag = ""

    def update(self):            
        if(time.clock() - self.lastShoot >= self.cooldownShoot):
            #If don't have a target, choose one
            if(self.target == None or self.target.isDead):
                self.chooseTargetMethod()
            #If have choose a target, go get him!
            if(self.target != None):
                self.lastlastShoot = time.clock()
                self.towerEffect(self,self.target)


        lMonsters = mE.mEntityManager.getTagEntitys("Monster")
        for m in lMonsters:
            if isOnCollision(m,self):
                self.hp.takeDamage(0.1)
        if(self.hp.health <= 0 ):
            self.die()

    def transformScreenPositionToGraph(self):
        self.graphPosition = (0,int(self.position[0] / tileWidth), int(self.position[1] / tileHeigth))
        return self.graphPosition

    def setPosition(self,position):
        position = (int(position[0]/tileWidth) , int(position[1] / tileHeigth))
        Entity.setPosition(self, position[0] * tileWidth, position[1] * tileHeigth)
        
        self.hp.setPosition(self.position)        
        self.graphPosition = (0,self.position.x, self.position.y)

    def chooseTarget(self):
        monsters = mE.mEntityManager.getTagEntitys("Monster")

        self.target = None
        for m in monsters:
            if (distanceEntity(self, m) < self.range):
                self.target = m
                break;

    def die(self):
        global mE
        mE.mEntityManager.removeEntity(self,self.tag)
        graph = mE.mGlobalVariables["Graph"]
        graph.addDeath(self.graphPosition)
        graph.addWeightNode(self.graphPosition,-100)
        self.isDead = True
        self.hp.removeEntityManager()