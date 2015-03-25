from Load import *
from TowerFunctions import *

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
    print "OOOOOOO STOP"
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
            t.hp.heal((dicTowers[t.tag]["HP"]-t.hp.health))

            nParticles = random.randint(0,10) + 5
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
            
            

def FireBall(params):
    print "KILL WITH FIRE"
    pass

dicSkills  = {}

dicSkills["TimeStop"] = {"Range": 10000, "Function":TimeStop}
dicSkills["Heal"] = {"Range": 100, "Function": Heal}
dicSkills["FireBall"] = {"Range": 100, "Function": FireBall}

'''if(mE.keyboard.isPressed(pygame.K_UP) and  mE.pause):
    self.pauseUI.content = ""
    mE.unpauseGame()
if(mE.keyboard.isPressed(pygame.K_DOWN) and not mE.pause):
    self.pauseUI.content = "PAUSE"
    mE.pauseGame()'''
