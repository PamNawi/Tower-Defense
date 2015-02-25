# -*- coding: cp1252 -*-
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
                                                  "CenterPosition" : self.position+(25,25),
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
            self.monsters += [ lMonstersStats[tMonster]] *i #["EntityTag"] ] *i
            tMonster += 1
        self.actualWave += 1

    def summonNextMonster(self):
        #print self.monsters
        if(self.monsters):
            statsMonster = random.choice(self.monsters)
            self.monsters.remove(statsMonster)
            self.createMonster(statsMonster)

    
    def createMonster(self,statsMonster):
        global mE
        global graph
        m = Monster()
        mE.mAnimationManager.setEntityAnimation(m, statsMonster["AnimationTag"])
        mE.mEntityManager.addEntity(m,"Monster","Monsters")
        mE.mPrimitiveManager.addPrimitive(m.lines, "MonsterRoute")
        m.lines.color = (random.randint(0,255) ,random.randint(0,255),random.randint(0,255))
        m.setPosition(m.lPositions[0][0],m.lPositions[0][1])
		
        m.maxSpeed = statsMonster["Speed"];
        m.hp = HealthBar(statsMonster["HP"]);
        m.hp.addToEntityManager()
        m.hp.setAnimation("EnemyHealthBarStart", "EnemyHealthBarEnd", "EnemyHealthBarMiddle")
        m.isDead = False
        m.setCenterBoundingCircle(16,16)
        m.setRadiusBoundingCircle(10)
        m.setCollisionBlock(Vec2d(32,32))
        return m

class Monster(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.path = None
        self.graphPosition = mE.mGlobalVariables["PortalCoord"]
        self.lines = Lines()
        self.recalculateRoute()
        
        self.maxSpeed = 1
        self.speed = 1
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
            error = 5
            nextPosition =  self.lPositions[0]
            npTop =     (nextPosition[0] + error, nextPosition[1] + error)
            npBottom =  (nextPosition[0] - error, nextPosition[1] - error)
            
            if( npTop[0] >= self.position[0] and npTop[1] >= self.position[1]  and npBottom[0] <= self.position[0] and npBottom[1] <= self.position[1] ):
                self.lPositions = self.lPositions[1:]
            #if(tNextPosition[0] >= self.position[0] and tNextPosition[1] >= self.position[1] and
            #   bNextPosition[0] <= self.position[0] and nextPosition[1] <= self.position[0]):
            #    self.lPositions = self.lPositions[1:]
                
                if(len(self.lPositions) > 0):
                    nextPosition = self.lPositions[0]
                    self.graphPosition = (0, nextPosition[0] - tileWidth /4 , nextPosition[1] - tileHeigth /4)
                    self.lines.vertices = tuple(self.lPositions)
                else:
                    self.hp.health = 0
                    return

            realSpeed = self.maxSpeed * self.speed
            
            if(nextPosition[0] > self.position[0]):
                self.setPosition(self.position[0] + realSpeed, self.position[1])

            if(nextPosition[1] > self.position[1]):
                self.setPosition(self.position[0], self.position[1]+ realSpeed)

            if(nextPosition[0] < self.position[0]):
                self.setPosition(self.position[0] - realSpeed, self.position[1])

            if(nextPosition[1] < self.position[1]):
                self.setPosition(self.position[0], self.position[1] - realSpeed)

            self.lines.vertices = ((self.position.x, self.position.y),) + self.lines.vertices[1:] + (mE.mGlobalVariables["CityCoord"],)
            
    def die(self):
        global mE
        mE.mPrimitiveManager.removePrimitive(self.lines,"MonsterRoute")
        mE.mEntityManager.removeEntity(self,"Monster")
        graph = mE.mGlobalVariables["Graph"]
        mE.mGlobalVariables["Money"] += 1
        graph.addDeath(self.graphPosition)
        self.isDead = True
        self.hp.removeEntityManager()

    def recalculateRoute(self):
        CityCoord       = mE.mGlobalVariables["CityCoord"]
        graph           = mE.mGlobalVariables["Graph"]
        oldRoute = self.path
        self.path = graph.aStar(self.graphPosition, CityCoord)
        if(not self.path):
            print "Não existe 1 rota"
            self.path = oldRoute
            return
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
        self.chooseTargetMethod = chooseTarget
        self.tag = ""

    def update(self):            
        if(time.clock() - self.lastShoot >= self.cooldownShoot):
            #If don't have a target, choose one
            if(self.target == None or (self.target != None and (self.target.isDead or distanceEntity(self, self.target) < self.range))):
                self.chooseTargetMethod(self)
            #If have choose a target, go get him!
            if(self.target != None):
                self.chooseTargetMethod(self)
                self.lastlastShoot = time.clock()
                self.towerEffect(self,self.target)
            self.lastShoot = time.clock() 


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


    def die(self):
        global mE
        mE.mEntityManager.removeEntity(self,self.tag)
        graph = mE.mGlobalVariables["Graph"]
        graph.addDeath(self.graphPosition)
        graph.addWeightNode(self.graphPosition,-100)
        self.isDead = True
        self.hp.removeEntityManager()


def chooseTarget(self):
    monsters = mE.mEntityManager.getTagEntitys("Monster")

    self.target = None
    for m in monsters:
        if (distanceEntity(self, m) < self.range):
            self.target = m
            break;

class City(Tile):
    def __init__(self,dicParams):
        Tile.__init__(self,dicParams)

        self.hp = HealthBar(10)
        self.hp.addToEntityManager()
        self.hp.setAnimation("TowerHealthBarStart", "TowerHealthBarEnd", "TowerHealthBarMiddle")
        self.rBoundingCircle = 32
        self.setCollisionBlock(Vec2d(tileWidth,tileHeigth))

    def update(self):
        lMonsters = mE.mEntityManager.getTagEntitys("Monster")
        for m in lMonsters:
            if isOnCollision(m,self):
                self.hp.takeDamage(0.1)
        if(self.hp.health <= 0 ):
            self.die()

    def setPosition(self,x,y):
        Tile.setPosition(self,x,y)
        self.hp.setPosition(self.position)


    def die(self):
        mE.mGlobalVariables["EndGame"] = True
