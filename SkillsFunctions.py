from Load import *
from TowerFunctions import *

class FireBall(Projectile):
    def __init__(self,target):
        Projectile.__init__(self,target)
        #Choose a random position on the border of the map to come alive
        b = random.randint(0,3)
        if(b == 0):
            #Right
            self.setPosition(-10, random.randint(0,768))
            pass
        elif(b == 1):
            #Top
            self.setPosition(random.randint(0,1024), -10)
            pass
        elif(b == 2):
            #Left
            self.setPosition(1034, random.randint(0, 768))
        else:
            #Bottom
            self.setPosition(random.randint(0,1024), 778)
            pass
        self.maxVelocity = 20
    def effect(self):
        self.ePursuit.takeDamage(25)
        mE.mJukebox.PlaySound("Explosion")

    def visualEffect(self):
        nParticles = random.randint(0,2)
        for i in range(nParticles):
            self.mParticleManager.createParticle(self.position + Vec2d(random.randint(0,10),random.randint(0,10)), "MeteorCascate", {"Dispersion": random.random() * 25 , "Velocity" : 1.0})

    def destructionEffect(self):
        nParticles = random.randint(0,15)
        for i in range(nParticles):
            mE.mParticleManager.createParticle(self.position,"Smoke",
                                                 {"CenterVelocity" : Vec2d(0,random.random() * -.8 -.1),
                                                  "CenterPosition" : self.position+(random.random() * 18 + 15,30),
                                                  "Angle"          : random.random() *360,
                                                  "Radius"         : random.random() * 10,
                                                  "Step"           : 0.05,
                                                  "Dispersion"     : random.random() * 100})
        
        Projectile.destructionEffect(self)
        mE.activeScreenShake(1.0, 100)        

class TimeSkill(Entity):
    def __init__(self):
        Entity.__init__(self)

    def update(self):
        stoppedTime = mE.getActualPauseTime()
        if(stoppedTime > 6.0):
            mE.unpauseGame()
            mE.mJukebox.PlaySound("AlarmClock")
            mE.mEntityManager.removeEntity(self,"SkillTimeStop")
        pass

def TimeStop(params):
    ts = TimeSkill()
    mE.mEntityManager.addEntity(ts, "SkillTimeStop")
    mE.pauseGame()
    mE.mJukebox.PlaySound("TimeRunning")
    
    pass

def Heal(params):
    #Get All towers on the range and heal all
    towers = mE.mEntityManager.getTagEntitys("Tower")
    e = Entity()
    e.setPosition(params["Position"])

    for t in towers:
        if(distanceEntity(e, t) <= dicSkills["Heal"]["Range"] + 64):
            t.hp.heal()

            nParticles = random.randint(0,5) + 5
            for i in range(nParticles):
                position = t.getCenterCollisionBlock()
                mE.mParticleManager.createParticle(position, "healParticle",
                                                   {"CenterVelocity" : Vec2d(0,random.random() * -1.5 -.5),
                                                  "CenterPosition" : position+(random.random() * 5 - 5, 10),
                                                  "Angle"          : random.random() * 360,
                                                  "Radius"         : random.random() * 20,
                                                  "Step"           : 0.10,
                                                  "Dispersion"     : random.random() * 100})
    mE.mJukebox.PlaySound("Heal")
            
            

def castFireBall(params):
    #Get All monsters on the range and attack with the fireball
    monsters = mE.mEntityManager.getTagEntitys("Monster")

    e = Entity()
    e.setPosition(params["Position"])

    for m in monsters:
        if (distanceEntity(e, m) <= dicSkills["FireBall"]["Range"]):
            fb = FireBall(m)
            mE.mEntityManager.addEntity(fb, "Projectil", "Monster")
            mE.mAnimationManager.setEntityAnimation(fb, "FireBall")
            fb.setCollisionBlock(Vec2d(10,10))

dicSkills  = {}

dicSkills["TimeStop"] = {"Range": 10000, "Function":TimeStop}
dicSkills["Heal"] = {"Range": 100, "Function": Heal}
dicSkills["FireBall"] = {"Range": 100, "Function": castFireBall}

