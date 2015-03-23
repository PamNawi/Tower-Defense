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
        self.lastSummon = mE.getGameTime()

        self.countTotalMonsters()

        self.monsters = []
        self.gonnaSpawn = True
        self.actualWave = 0
        self.newWave()
        
        tText = mE.mEntityManager.getTagEntitys("TwinkleText")[0]
        tText.content = "- Sharpen the arrows -"

        self.progressBar = ProgressBar(self.nMonsters)
        self.progressBar.addBarToEntityManager()
        self.progressBar.setAnimation("ProgressBarMF","ProgressBarEF", "ProgressBarMF", "ProgressBarStart", "ProgressBarEnd", "ProgressBarMiddle")
        self.progressBar.setPosition(Vec2d(75,10))
        #mE.mEntityManager.addEntity(self.progressBar , "LevelProgress", "UI")

    def update(self):
        if(self.nextParticle < 0):
            self.mParticleManager.createParticle(self.position,"spin",
                                                 {"CenterVelocity" : Vec2d(0,random.random() * -.6 -.1),
                                                  "CenterPosition" : self.position+(random.random() * 18 + 15,30),
                                                  "Angle"          : random.random() * 360,
                                                  "Radius"         : random.random() * 10,
                                                  "Step"           : 0.05,
                                                  "Dispersion"     : random.random() * 400})

            self.nextParticle = random.random() * 50
        self.nextParticle += -1

        if(mE.getGameTime()- self.lastSummon >= 1.0):
            self.summonNextMonster()
        
    def newWave(self):
        if(len(self.waves) - 1 < self.actualWave):
            self.gonnaSpawn = False
            return
        
        elif(mE.mEntityManager.getTagEntitys("Monster") == []):
            diffLastSummon = mE.getGameTime() - self.lastSummon
            tText = mE.mEntityManager.getTagEntitys("TwinkleText")[0]
            tText.content = "- Brace yourself -"
            tText.startTwinkle(1)
            if(diffLastSummon > 5.0):
                self.monsters = []
                tMonster = 0
                for i in self.waves[self.actualWave]:
                    self.monsters += [ lMonstersStats[tMonster]] *i #["EntityTag"] ] *i
                    tMonster += 1
                self.actualWave += 1
                self.lastSummon = mE.getGameTime() + 3.0
                mE.mJukebox.PlaySound("MonstersComing")

                if(len(self.waves) - 1 < self.actualWave):
                    mE.mJukebox.PlaySound("Heart")
                

    def summonNextMonster(self):
        #print "New Monster"
        #print self.monsters
        if(self.monsters):
            mE.mJukebox.PlaySound("Teleport")
            statsMonster = random.choice(self.monsters)
            self.monsters.remove(statsMonster)
            self.createMonster(statsMonster)
            self.lastSummon = mE.getGameTime()
            self.progressBar.summonNext()

            tText = mE.mEntityManager.getTagEntitys("TwinkleText")[0]
            tText.stopTwinkle()
        else:
            self.newWave()
    

    
    def createMonster(self,statsMonster):
        global mE
        global graph
        m = Monster()
        mE.mAnimationManager.setEntityAnimation(m, statsMonster["AnimationTag"]+"Down")
        mE.mEntityManager.addEntity(m,"Monster","Monsters")
        mE.mPrimitiveManager.addPrimitive(m.lines, "MonsterRoute")
        m.lines.color = (random.randint(0,255) ,random.randint(0,255),random.randint(0,255))
        m.setPosition(m.lPositions[0][0],m.lPositions[0][1])
		
        m.maxSpeed = statsMonster["Speed"];
        m.hp = HealthBar(statsMonster["HP"]);
        m.sounds = statsMonster["SoundList"]
        m.tag = statsMonster["AnimationTag"]
        m.hp.addToEntityManager()
        m.hp.setAnimation("EnemyHealthBarStart", "EnemyHealthBarEnd", "EnemyHealthBarMiddle")
        m.isDead = False
        m.setCenterBoundingCircle(16,16)
        m.setRadiusBoundingCircle(10)
        m.setCollisionBlock(Vec2d(32,32))
        return m

    def gonnaSpawnMore(self):
        return self.gonnaSpawn

    def countTotalMonsters(self):
        self.nMonsters = 0
        for wave in self.waves:
            for monster in self.waves[wave]:
                self.nMonsters += monster
        

class Monster(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.path = None
        self.graphPosition = mE.mGlobalVariables["PortalCoord"]
        self.lines = Lines()
        
        self.desloc = random.randint(-15,15)
        self.recalculateRoute()
        
        self.maxSpeed = 1
        self.speed = 1
        self.rBoundingCircle = 16

        self.poison = 0.0
        self.lastDamageByPoison = mE.getGameTime()
        
    def update(self):
        self.move()
        diffLastDamagePoison = mE.getGameTime() - self.lastDamageByPoison
        if(self.poison and diffLastDamagePoison > 1.0):
            self.takeDamage(1)
            self.lastDamageByPoison = mE.getGameTime()
        
        if(self.hp.health <= 0):
            self.die()

        self.hp.setPosition(self.position)

    def takeDamage(self, damage):
        if(self.hp.health > 0):
            self.hp.takeDamage(damage)

    def move(self):
        if(self.lPositions):
            error = 5
            nextPosition =  self.lPositions[0]
            npTop =     (nextPosition[0] + error, nextPosition[1] + error)
            npBottom =  (nextPosition[0] - error, nextPosition[1] - error)
            c = self.getCenterCollisionBlock()
            
            if( npTop[0] >= self.position[0] and npTop[1] >= self.position[1]  and npBottom[0] <= self.position[0] and npBottom[1] <= self.position[1] ):
                self.lPositions = self.lPositions[1:]
            #if(tNextPosition[0] >= self.position[0] and tNextPosition[1] >= self.position[1] and
            #   bNextPosition[0] <= self.position[0] and nextPosition[1] <= self.position[0]):
            #    self.lPositions = self.lPositions[1:]
                
                if(len(self.lPositions) > 0):
                    nextPosition = self.lPositions[0]
                    self.graphPosition = (0, nextPosition[0] - tileWidth /4 , nextPosition[1] - tileHeigth /4)
                    c = self.getCenterCollisionBlock()
                    self.lines.vertices = ((c.x, c.y),) + self.lines.vertices[2:]
                else:
                    self.hp.health = 0
                    return

            realSpeed = self.maxSpeed * self.speed
            
            if(nextPosition[0] > self.position[0]):
                self.setPosition(self.position[0] + realSpeed, self.position[1])
                mE.mAnimationManager.setEntityAnimation(self, self.tag+"Right")

            if(nextPosition[1] > self.position[1]):
                self.setPosition(self.position[0], self.position[1]+ realSpeed)
                mE.mAnimationManager.setEntityAnimation(self, self.tag+"Down")

            if(nextPosition[0] < self.position[0]):
                self.setPosition(self.position[0] - realSpeed, self.position[1])
                mE.mAnimationManager.setEntityAnimation(self, self.tag+"Left")

            if(nextPosition[1] < self.position[1]):
                self.setPosition(self.position[0], self.position[1] - realSpeed)
                mE.mAnimationManager.setEntityAnimation(self, self.tag+"Up")

            c = self.getCenterCollisionBlock()
            self.lines.vertices =  ((c.x + self.desloc, c.y + self.desloc),) + self.lines.vertices[1:]
            
    def die(self):
        global mE
        mE.mPrimitiveManager.removePrimitive(self.lines,"MonsterRoute")
        mE.mEntityManager.removeEntity(self,"Monster")
        graph = mE.mGlobalVariables["Graph"]
        mE.mGlobalVariables["Money"] += 1
        graph.addDeath(self.graphPosition)
        self.isDead = True
        self.hp.removeEntityManager()
        if(self.sounds):
            mE.mJukebox.PlaySound(random.choice(self.sounds))

        tomb = Entity()
        mE.mEntityManager.addEntity(tomb, "Tombstone", "Tombstone")
        mE.mAnimationManager.setEntityAnimation(tomb, "Tombstone")
        tomb.setPosition(self.getCenterCollisionBlock())
        

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
        
    def transformGraphRouteToScreenRoute(self):
        self.lPositions = []
        for coord in self.path:
            self.lPositions += [(coord[1] + tileWidth /4, coord[2] + tileHeigth /4)]

        lvPositions = []
        for coord in self.path:
            lvPositions += [(coord[1] + tileWidth /2 + self.desloc , coord[2] + tileHeigth /2 + self.desloc)]
        self.lines.vertices = tuple(lvPositions)


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
        self.lastShoot = mE.mGlobalVariables["GameTime"] - self.cooldownShoot

        self.towerEffect = None
        self.chooseTargetMethod = chooseTarget
        self.tag = ""

    def update(self):            
        if(mE.mGlobalVariables["GameTime"] - self.lastShoot >= self.cooldownShoot):
            #If don't have a target, choose one
            if(self.target == None or (self.target != None and (self.target.isDead or distanceEntity(self, self.target) < self.range))):
                self.chooseTargetMethod(self)
            #If have choose a target, go get him!
            if(self.target != None):
                self.chooseTargetMethod(self)
                self.lastlastShoot = time.clock()
                self.towerEffect(self,self.target)
            self.lastShoot = mE.mGlobalVariables["GameTime"]


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
        self.setCollisionBlock(Vec2d(tileWidth *2,tileHeigth*2))
        self.isDead = False

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
        self.setCollisionBlock(Vec2d(tileWidth *2,tileHeigth*2))


    def die(self):
        mE.mGlobalVariables["EndGame"] = True
        self.isDead = True
