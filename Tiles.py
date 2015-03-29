# -*- coding: cp1252 -*-
from Load import *
from Animations import *
from MonstersAnimations import *
from MonstersStats import *
from Maps import *
from HealthBar import *
from TowerFunctions import *

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
                mE.mGlobalVariables["General"].monstersComming()

                if(len(self.waves) - 1 < self.actualWave):
                    #mE.mJukebox.StopMusic()
                    mE.mJukebox.PlaySong("BossFight",True)
                    #mE.mJukebox.PlaySound("Heart")
                

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
        m.setPosition(self.position.x + tileWidth/2 -8, self.position.y + tileHeigth/2-8)
        m.recalculateRoute()
        #m.setPosition(Vec2d(m.lPositions[0][0],m.lPositions[0][1]))
		
        m.maxSpeed = statsMonster["Speed"];
        m.hp = HealthBar(statsMonster["HP"]);
        m.sounds = statsMonster["SoundList"]
        m.tag = statsMonster["AnimationTag"]
        m.hp.addToEntityManager()
        m.hp.setAnimation("EnemyHealthBarStart", "EnemyHealthBarEnd", "EnemyHealthBarMiddle")
        m.isDead = False
        m.setCollisionBlock(Vec2d(32,32))
        return m

    def gonnaSpawnMore(self):
        return self.gonnaSpawn

    def countTotalMonsters(self):
        self.nMonsters = 0
        for wave in self.waves:
            for monster in self.waves[wave]:
                self.nMonsters += monster

class Monster(PathFollowing):
    def __init__(self):
        PathFollowing.__init__(self, [])
        self.graphPosition = mE.mGlobalVariables["PortalCoord"]
        
        self.lines = Lines()
        self.desloc = random.randint(-15,15)

        self.route = None
        #self.recalculateRoute()
        self.maxSpeed = 1
        self.speed = 1

        self.poison = 0.0
        self.lastDamageByPoison = mE.getGameTime()

    def update(self):
        self.maxVelocity = self.maxSpeed
        PathFollowing.update(self)

        diffLastDamagePoison = mE.getGameTime() - self.lastDamageByPoison
        if(self.poison and diffLastDamagePoison > 1.0):
            self.takeDamage(1)
            self.lastDamageByPoison = mE.getGameTime()

        self.hp.setPosition(self.position)
        
        c = self.getCenterCollisionBlock()
        if(self.lines != None):
            if(len(self.lines.vertices) <= 1):
                mE.mPrimitiveManager.removePrimitive(self.lines,"MonsterRoute")
                self.lines = None
                return
                
            elif(distance(c,Vec2d(self.lines.vertices[1])) <= 30):
               self.lines.vertices =  self.lines.vertices[1:]
            
            self.lines.vertices =  ((c.x + self.desloc, c.y + self.desloc),) + self.lines.vertices[1:]

        if(abs(self.velocity.x) > abs(self.velocity.y)):
            if(self.velocity.x < 0):
                self.direction = "Left"
            else:
                self.direction = "Right"
        else:
            if(self.velocity.y > 0):
                self.direction = "Down"
            else:
                self.direction = "Up"
        mE.mAnimationManager.setEntityAnimation(self, self.tag+self.direction)
        

    def takeDamage(self, damage):
        if(self.hp.health > 0):
            self.hp.takeDamage(damage)
        if(self.hp.health <= 0):
            self.die()

    def die(self):
        global mE
        if(self.lines != None):
            mE.mPrimitiveManager.removePrimitive(self.lines,"MonsterRoute")
        mE.mEntityManager.removeEntity(self,"Monster")
        graph = mE.mGlobalVariables["Graph"]
        mE.mGlobalVariables["Money"] += 2
        self.convertPositionToGraph()
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
        oldRoute = self.route
        self.convertPositionToGraph()
        self.route = graph.aStar(self.graphPosition, CityCoord)
        if(not self.route):
            print "Não existe 1 rota"
            self.route = oldRoute
            return
        else:
            self.transformGraphRouteToScreenRoute()
            self.currentNode = 1         
        
    def transformGraphRouteToScreenRoute(self):
        lvPositions = []
        self.path.nodes = []
        for coord in self.route:
            lvPositions += [(coord[1] + tileWidth /2 + self.desloc , coord[2] + tileHeigth /2 + self.desloc)]
            self.path.addNode(Vec2d(coord[1] + tileWidth /2 -8, coord[2] + tileHeigth /2 - 16))
        c = self.getCenterCollisionBlock()
        self.lines.vertices =  ((c.x + self.desloc, c.y + self.desloc),) + tuple(lvPositions[1:])

    def convertPositionToGraph(self):
        x = int(self.position.x / tileWidth) * tileWidth
        y = int(self.position.y / tileHeigth) * tileHeigth
        self.graphPosition = (0, x, y)

class Tower(Entity):
    def __init__(self, radiusRange = 100):
        Entity.__init__(self)
        self.graphPosition = (-1,-1,-1)

        self.hp = None
        self.rBoundingCircle = 32
        
        self.target = None
        self.range = radiusRange

        self.cooldownShoot = 0.5
        self.lastShoot = mE.mGlobalVariables["GameTime"] - self.cooldownShoot
 
        self.towerEffect = None
        self.chooseTargetMethod = chooseTarget
        self.tag = ""

    def update(self):
        healthPercentage = (self.hp.health) / self.hp.maxHealth
        if(healthPercentage <= 0.5):
            mE.mParticleManager.createParticle(self.position,"Smoke",
                                                 {"CenterVelocity" : Vec2d(0,random.random() * -.8 -.1),
                                                  "CenterPosition" : self.position+(random.random() * 18 + 15,30),
                                                  "Angle"          : random.random() *360,
                                                  "Radius"         : random.random() * 10,
                                                  "Step"           : 0.05,
                                                  "Dispersion"     : random.random() * 100})


        
        if(mE.getGameTime() - self.lastShoot >= self.cooldownShoot):
            #If don't have a target, choose one
            if(self.target == None or (self.target != None and (self.target.isDead or distanceEntity(self, self.target) < self.range))):
                self.chooseTargetMethod(self)
            #If have choose a target, go get him!
            if(self.target != None):
                self.chooseTargetMethod(self)
                self.lastlastShoot = time.clock()
                self.towerEffect(self,self.target)
            self.lastShoot = mE.getGameTime()

        lMonsters = mE.mEntityManager.getTagEntitys("Monster")
        for m in lMonsters:
            if isOnCollision(m,self):
                self.hp.takeDamage(0.6)
                if(healthPercentage < 1.0):
                    mE.mGlobalVariables["General"].bringDown()
                            
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
        mE.mEntityManager.removeEntity(self,"Tower")
        graph = mE.mGlobalVariables["Graph"]
        graph.addDeath(self.graphPosition)
        graph.addWeightNode(self.graphPosition,-100)
        self.isDead = True
        self.hp.removeEntityManager()
        mE.mJukebox.PlaySound("TowerDown")


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


        self.lastShoot = mE.getGameTime() # - self.cooldownShoot
        self.cooldownShoot = 5.0
        self.damage = 1
        self.range =  100
        self.target = None

    def update(self):
        lMonsters = mE.mEntityManager.getTagEntitys("Monster")
        for m in lMonsters:
            if isOnCollision(m,self):
                self.hp.takeDamage(0.1)
    
        if(self.hp.health <= 0 ):
            self.die()

        if(self.hp.health == 5):
            mE.mGlobalVariables["General"].laugh()

        diffLastShoot = mE.getGameTime() -  self.lastShoot
        if(diffLastShoot  >= self.cooldownShoot):
            if(self.target == None or (self.target != None and (self.target.isDead or distanceEntity(self, self.target) < self.range))):
                chooseTarget(self)

            if(self.target != None):
                chooseTarget(self)
                self.lastShoot = mE.getGameTime()
                projectile =  Projectile(self.target)
                mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
                mE.mAnimationManager.setEntityAnimation(projectile, "SimpleProjectil")
                projectile.tower = self
                projectile.setCollisionBlock(Vec2d(10,10))
                projectile.setPosition(self.position + Vec2d(25,25))
            
            

    def setPosition(self,x,y):
        Tile.setPosition(self,x,y)
        self.hp.setPosition(self.position)
        self.setCollisionBlock(Vec2d(tileWidth *2,tileHeigth*2))


    def die(self):
        mE.mGlobalVariables["EndGame"] = True
        self.isDead = True
