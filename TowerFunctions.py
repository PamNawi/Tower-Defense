from Load import *
from Tiles import *
#Towers Helper Methods:
def hit(tower, target):
    projectile =  Projectile(target)
    mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
    mE.mAnimationManager.setEntityAnimation(projectile, "SimpleProjectil")
    projectile.tower = tower
    projectile.setCollisionBlock(Vec2d(10,10))
    projectile.setPosition(tower.position)
    
    #target.takeDamage(tower.damage)

def slow(tower,target):
    projectile =  SlowProjectile(target)
    mE.mEntityManager.addEntity(projectile, "Projectil", "Monsters")
    mE.mAnimationManager.setEntityAnimation(projectile, "SlowProjectil")
    projectile.tower = tower
    projectile.setCollisionBlock(Vec2d(10,10))
    projectile.setPosition(tower.position)
    chooseTargetWithoutSpeedModification(tower)
    #print target.speed * target.maxSpeed;

def poison(tower,target):
    target.poison = 10
    pass

def chooseTargetWithoutSpeedModification(tower):
        monsters = mE.mEntityManager.getTagEntitys("Monster")

        tower.target = None
        for m in monsters:
            if (distanceEntity(tower, m) < tower.range and m.speed >= 1):
                tower.target = m
                return;
def explode(projetile):
    pass

class Projectile(SteeringEntity):
    def __init__(self,target):
        SteeringEntity.__init__(self)
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

    def visualEffect(self):
        pass

    def destructionEffect(self):
        mE.mEntityManager.removeEntity(self, "Projectil")

class SlowProjectile(Projectile):
    def __init__(self,target):
        Projectile.__init__(self,target)
        self.mParticleManager  = mE.mParticleManager
        self.nextParticle = -1
                

    def effect(self):
        self.ePursuit.speed = 0.8

    def visualEffect(self):
        if(self.nextParticle < 0):
            self.mParticleManager.createParticle(self.position, "cascate", {"Dispersion": random.random() * 25 , "Velocity" : 1.0})
            self.nextParticle = 0
        self.nextParticle += -1

    def destructionEffect(self):
        mE.mEntityManager.removeEntity(self,"Projectil")
        explode(self)

dicTowers = {}
dicTowers["Hit"] = {"ChooseMethod" : None , "Cost" : 10,
                    "Slow" : 1, "PoisonDamage": 0, "HitDamage": 3,
                    "HP" : 15, "Effect": hit, "Cooldown": 1.0}

dicTowers["Slow"] = {"ChooseMethod" : chooseTargetWithoutSpeedModification,
                     "Cost" : 10,
                     "Slow" : 0.5, "PoisonDamage": 0, "HitDamage": 0.0,
                     "HP": 15, "Effect": slow, "Cooldown": 2.0}

