from Load import *
from Sounds import *

class GeneralVoices(Entity):
    def __init__(self):
        self.lastCall = {}

        self.lastCall["EvilLaugh"] = mE.getGameTime()
        self.lastCall["MonstersComing"] = mE.getGameTime()
        self.lastCall["UnderAttack"] = mE.getGameTime()
        self.loadSounds()

    def loadSounds(self):
        #General Sounds
        mE.mJukebox.LoadSound(coming, "MonstersComing")
        mE.mJukebox.LoadSound(bringDown , "BringDown")
        mE.mJukebox.LoadSound(laugh, "EvilLaugh")
        mE.mJukebox.LoadSound(underAttack, "UnderAttack")

    def laugh(self):
        diffLastLaugh = mE.getGameTime() - self.lastCall["EvilLaugh"]
        if(diffLastLaugh > 120):
            mE.mJukebox.PlaySound("EvilLaugh")
            self.lastCall["EvilLaugh"] = mE.getGameTime()

    def bringDown(self):
        diffLastLaugh = mE.getGameTime() - self.lastCall["UnderAttack"]
        if(diffLastLaugh > 20):
            mE.mJukebox.PlaySound(random.choice(["BringDown","UnderAttack"]))
            self.lastCall["UnderAttack"] = mE.getGameTime()

    def monstersComming(self):
        mE.mJukebox.PlaySound("MonstersComing")

    
        
