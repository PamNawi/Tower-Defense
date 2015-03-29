from Load import *
from Tiles import *
#Towers Helper Methods:
def hit(tower, target):
    projectile =  Projectile(target)
    mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
    mE.mAnimationManager.setEntityAnimation(projectile, "SimpleProjectil")
    projectile.tower = tower
    projectile.setCollisionBlock(Vec2d(10,10))
    projectile.setPosition(tower.position + Vec2d(25,25))
    
    #target.takeDamage(tower.damage)

def slow(tower,target):
    projectile =  SlowProjectile(target)
    mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
    mE.mAnimationManager.setEntityAnimation(projectile, "SlowProjectil")
    projectile.tower = tower
    projectile.setCollisionBlock(Vec2d(10,10))
    projectile.setPosition(tower.position + Vec2d(25,25))
    chooseTargetWithoutSpeedModification(tower)
    mE.mJukebox.PlaySound("Magic")
    #print target.speed * target.maxSpeed;

def poison(tower,target):
    projectile =  PoisonProjectile(target)
    mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
    mE.mAnimationManager.setEntityAnimation(projectile, "PoisonProjectil")
    projectile.tower = tower
    projectile.setCollisionBlock(Vec2d(10,10))
    projectile.setPosition(tower.position + Vec2d(25,25))

def money(tower,target):
    projectile =  GoldProjectile(target)
    mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
    mE.mAnimationManager.setEntityAnimation(projectile, "FarmProjectil")
    projectile.tower = tower
    projectile.setCollisionBlock(Vec2d(10,10))
    projectile.setPosition(tower.position + Vec2d(25,25))
    
def chooseTargetWithoutSpeedModification(tower):
    monsters = mE.mEntityManager.getTagEntitys("Monster")

    tower.target = None
    for m in monsters:
        if (distanceEntity(tower, m) < tower.range and m.speed >= 1):
            tower.target = m
            return

def chooseTargetWithoutPoison(tower):
    monsters = mE.mEntityManager.getTagEntitys("Monster")

    tower.target = None
    for m in monsters:
        if (distanceEntity(tower, m) < tower.range and m.poison == 0):
            tower.target = m
            return

def sendMoneyToCity(tower):
    cityTiles = mE.mMapManager.getTiles("4")[0][1][0]
    tower.target = cityTiles
    return
    
            
def explode(projectile):
    nParticles = int(random.random() * 50)
    #print projectile.position
    for i in range(0, nParticles):
        v = Vec2d(random.random() * 10 - 5, random.random() * 10 - 5)
        projectile.mParticleManager.createParticle(projectile.position, "commonExplosion", {"Dispersion": random.random() * 25, "Velocity": v})

class Projectile(SteeringEntity):
    def __init__(self,target):
        SteeringEntity.__init__(self)
        self.mParticleManager  = mE.mParticleManager
        self.ePursuit = target

    def sumForces(self):
        self.force = self.Pursuit(self.ePursuit)

    def update(self):
        if(self.ePursuit == None):
            self.destructionEffect()
        else:
            SteeringEntity.update(self)
            #if on collision with target
            #make the effect
            if(isOnCollision(self,self.ePursuit)):
                self.effect()
                self.destructionEffect()
            self.visualEffect()

    def effect(self):
        self.ePursuit.takeDamage(self.tower.damage)
        mE.mJukebox.PlaySound("Damage")

    def visualEffect(self):
        pass

    def destructionEffect(self):
        explode(self)
        mE.mEntityManager.removeEntity(self, "Projectil")

class SlowProjectile(Projectile):
    def __init__(self,target):
        Projectile.__init__(self,target)
        self.nextParticle = -1
                

    def effect(self):
        self.ePursuit.maxVelocity = 0.8

    def visualEffect(self):
        if(self.nextParticle < 0):
            self.mParticleManager.createParticle(self.position, "cascate", {"Dispersion": random.random() * 25 , "Velocity" : 1.0})
            self.nextParticle = 0
        self.nextParticle += -1

    def destructionEffect(self):
        mE.mEntityManager.removeEntity(self,"Projectil")
        nParticles = int(random.random() * 50)
        #print projectile.position
        for i in range(0, nParticles):
            v = Vec2d(random.random() * 10 - 5, random.random() * 10 - 5)
            self.mParticleManager.createParticle(self.position, "slowExplosion", {"Dispersion": random.random() * 25, "Velocity": v})

class PoisonProjectile(Projectile):
    def __init__(self,target):
        Projectile.__init__(self,target)

    def effect(self):
        self.ePursuit.poison = 0.1

    def destructionEffect(self):
        mE.mEntityManager.removeEntity(self,"Projectil")
        nParticles = int(random.random() * 50)
        for i in range(0, nParticles):
            v = Vec2d(random.random() * 10 - 5, random.random() * 10 - 5)
            self.mParticleManager.createParticle(self.position, "poisonExplosion", {"Dispersion": random.random() * 25, "Velocity": v})

class GoldProjectile(Projectile):
    def __init__(self,target):
        Projectile.__init__(self,target)

    def effect(self):
        mE.mGlobalVariables["Money"] += 1

    def destructionEffect(self):
        mE.mEntityManager.removeEntity(self,"Projectil")
        nParticles = int(random.random() * 10)
        for i in range(0, nParticles):
            v = Vec2d(random.random() * 10 - 5, random.random() * 10 - 5)
            self.mParticleManager.createParticle(self.position, "farmExplosion", {"Dispersion": random.random() * 25, "Velocity": v})
        

dicTowers = {}
dicTowers["Hit"] = {"ChooseMethod" : None , "Cost" : 10,
                    "Slow" : 1, "PoisonDamage": 0, "HitDamage": 3,
                    "HP" : 15, "Effect": hit, "Cooldown": 1.0, "Range": 100}

dicTowers["Slow"] = {"ChooseMethod" : chooseTargetWithoutSpeedModification,
                     "Cost" : 10,
                     "Slow" : 0.5, "PoisonDamage": 0, "HitDamage": 0.0,
                     "HP": 15, "Effect": slow, "Cooldown": 2.0, "Range":100}


dicTowers["Poison"] = {"ChooseMethod" : chooseTargetWithoutPoison,
                     "Cost" : 10,
                     "Slow" : 0.0, "PoisonDamage": 1, "HitDamage": 0.0,
                     "HP": 15, "Effect": poison, "Cooldown": 5.0, "Range":100}

dicTowers["Farm"] = {"ChooseMethod" : sendMoneyToCity,
                     "Cost" : 20,
                     "Slow" : 0.0, "PoisonDamage": 0, "HitDamage": 0.0,
                     "HP": 1, "Effect": money, "Cooldown": 15.0, "Range":100}
