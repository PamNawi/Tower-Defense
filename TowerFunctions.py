from Load import *
from Tiles import *
#Towers Helper Methods:
def hit(tower, target):
    target.takeDamage(tower.damage)

def slow(tower,target):
    target.speed = 0.8
    chooseTargetWithoutSpeedModification(tower)

def poison(tower,target):
    target.poison = 10
    pass

def chooseTargetWithoutSpeedModification(tower):
        monsters = mE.mEntityManager.getTagEntitys("Monster")

        tower.target = None
        for m in monsters:
            if (distanceEntity(tower, m) < tower.range and m.speed >= 1):
                tower.target = m
                break;

dicTowers = {}
dicTowers["Hit"] = {"ChooseMethod" : None , "Cost" : 10,
                    "Slow" : 1, "PoisonDamage": 0, "HitDamage": 0.1,
                    "HP" : 15, "Effect": hit, "Cooldown": 0.5}

dicTowers["Slow"] = {"ChooseMethod" : chooseTargetWithoutSpeedModification,
                     "Cost" : 10,
                     "Slow" : 0.5, "PoisonDamage": 0, "HitDamage": 0.0,
                     "HP": 15, "Effect": slow, "Cooldown": 1.0}

