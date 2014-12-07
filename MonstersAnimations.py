# -*- coding: cp1252 -*-
#
NSpritesMonsters = 3

def loadListImagesEnemys( Route, nFrames, frameSpeed = 0.4):
    lImages = []
    for i in range(0,nFrames):
        lImages += [".//Resources//Monsters//"+Route+"//"+str(i)+".png"]
    return (lImages, frameSpeed)
    

#Small Enemys
lImagesBoneDullahan     = loadListImagesEnemys("Pequeno//BoneDullahan",NSpritesMonsters)
lImagesDullahan         = loadListImagesEnemys("Pequeno//Dullahan",NSpritesMonsters)
lImagesFlameRat         = loadListImagesEnemys("Pequeno//FlameRat",NSpritesMonsters)
lImagesHeartBreaker1    = loadListImagesEnemys("Pequeno//HeartBreaker1",NSpritesMonsters)
lImagesHeartBreaker2    = loadListImagesEnemys("Pequeno//HeartBreaker2",NSpritesMonsters)
lImagesLizardman1       = loadListImagesEnemys("Pequeno//Lizardman1",NSpritesMonsters)
lImagesLizardman2       = loadListImagesEnemys("Pequeno//Lizardman2",NSpritesMonsters)
lImagesMessenger        = loadListImagesEnemys("Pequeno//Messenger",NSpritesMonsters)
lImagesMetalGolem1      = loadListImagesEnemys("Pequeno//MetalGolem1",NSpritesMonsters)
lImagesMetalGolem2      = loadListImagesEnemys("Pequeno//MetalGolem2",NSpritesMonsters)
lImagesMetalGuardian    = loadListImagesEnemys("Pequeno//MetalGuardian",NSpritesMonsters)
lImagesMonsterVine      = loadListImagesEnemys("Pequeno//MonsterVine",NSpritesMonsters)
lImagesOrcAssassin      = loadListImagesEnemys("Pequeno//OrcAssassin",NSpritesMonsters)
lImagesOrcShaman1       = loadListImagesEnemys("Pequeno//OrcShaman1",NSpritesMonsters)
lImagesOrcShaman2       = loadListImagesEnemys("Pequeno//OrcShaman2",NSpritesMonsters)
lImagesOrcShaman3       = loadListImagesEnemys("Pequeno//OrcShaman3",NSpritesMonsters)
lImagesOrcShaman4       = loadListImagesEnemys("Pequeno//OrcShaman4",NSpritesMonsters)
lImagesOrcSoldier       = loadListImagesEnemys("Pequeno//OrcSoldier",NSpritesMonsters)
lImagesProserpina       = loadListImagesEnemys("Pequeno//Proserpina",NSpritesMonsters)
lImagesRat1             = loadListImagesEnemys("Pequeno//Rat1",NSpritesMonsters)
lImagesRat2             = loadListImagesEnemys("Pequeno//Rat2",NSpritesMonsters)

#Medium Enemys

lImagesDarkGoddess      = loadListImagesEnemys("Médio//DarkGoddess",NSpritesMonsters)
lImagesEvilGoddess      = loadListImagesEnemys("Médio//EvilGoddess",NSpritesMonsters)
lImagesMedusa           = loadListImagesEnemys("Médio//Medusa",NSpritesMonsters)
lImagesSlimeKing1       = loadListImagesEnemys("Médio//SlimeKing",NSpritesMonsters)
lImagesSlimeKing2       = loadListImagesEnemys("Médio//SlimeKing2",NSpritesMonsters)
lImagesSlimeKing3       = loadListImagesEnemys("Médio//SlimeKing3",NSpritesMonsters)
lImagesVampire          = loadListImagesEnemys("Médio//Vampire",NSpritesMonsters)
lImagesZoiao            = loadListImagesEnemys("Médio//Zoiao",NSpritesMonsters)
