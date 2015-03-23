# -*- coding: cp1252 -*-
#
NSpritesMonsters = 3

def loadDictImagesEnemys( Route, tag):
    rImages = ".//Resources//Monsters//"+Route+"//"
    lDown   = [rImages+"0.png",rImages+"1.png",rImages+"2.png"]
    lUp     = [rImages+"9.png",rImages+"10.png",rImages+"11.png"]
    lRight  = [rImages+"6.png",rImages+"7.png",rImages+"8.png"]
    lLeft   = [rImages+"3.png",rImages+"4.png",rImages+"5.png"]
    dicImages = { "Up": (lUp,0.4), "Down": (lDown, 0.4), "Right" : (lRight, 0.4), "Left": (lLeft,0.4), tag: tag}
    return dicImages

#Small Enemys
lImagesBoneDullahan     = loadDictImagesEnemys("Pequeno//BoneDullahan","BoneDullahan")
lImagesDullahan         = loadDictImagesEnemys("Pequeno//Dullahan","Dullahan")
lImagesFlameRat         = loadDictImagesEnemys("Pequeno//FlameRat","FlameRat")
lImagesHeartBreaker1    = loadDictImagesEnemys("Pequeno//HeartBreaker1","HeartBreaker1")
lImagesHeartBreaker2    = loadDictImagesEnemys("Pequeno//HeartBreaker2","HeartBreaker2")
lImagesLizardman1       = loadDictImagesEnemys("Pequeno//Lizardman1","Lizardman1")
lImagesLizardman2       = loadDictImagesEnemys("Pequeno//Lizardman2","Lizardman2")
lImagesMetalGolem1      = loadDictImagesEnemys("Pequeno//MetalGolem1","MetalGolem1")
lImagesMetalGolem2      = loadDictImagesEnemys("Pequeno//MetalGolem2","MetalGolem2")
lImagesMetalGuardian    = loadDictImagesEnemys("Pequeno//MetalGuardian","MetalGuardian")
lImagesMonsterVine      = loadDictImagesEnemys("Pequeno//MonsterVine","MonsterVine")
lImagesOrcAssassin      = loadDictImagesEnemys("Pequeno//OrcAssassin","OrcAssassin")
lImagesOrcShaman1       = loadDictImagesEnemys("Pequeno//OrcShaman1","OrcShaman1")
lImagesOrcShaman2       = loadDictImagesEnemys("Pequeno//OrcShaman2","OrcShaman2")
lImagesOrcShaman3       = loadDictImagesEnemys("Pequeno//OrcShaman3","OrcShaman3")
lImagesOrcShaman4       = loadDictImagesEnemys("Pequeno//OrcShaman4","OrcShaman4")
lImagesOrcSoldier       = loadDictImagesEnemys("Pequeno//OrcSoldier","OrcSoldier")
lImagesProserpina       = loadDictImagesEnemys("Pequeno//Proserpina","Proserpina")
lImagesRat1             = loadDictImagesEnemys("Pequeno//Rat1","Rat1")
lImagesRat2             = loadDictImagesEnemys("Pequeno//Rat2","Rat2")

#Medium Enemys

lImagesDarkGoddess      = loadDictImagesEnemys("Médio//DarkGoddess",NSpritesMonsters)
lImagesEvilGoddess      = loadDictImagesEnemys("Médio//EvilGoddess",NSpritesMonsters)
lImagesMedusa           = loadDictImagesEnemys("Médio//Medusa",NSpritesMonsters)
lImagesSlimeKing1       = loadDictImagesEnemys("Médio//SlimeKing",NSpritesMonsters)
lImagesSlimeKing2       = loadDictImagesEnemys("Médio//SlimeKing2",NSpritesMonsters)
lImagesSlimeKing3       = loadDictImagesEnemys("Médio//SlimeKing3",NSpritesMonsters)
lImagesVampire          = loadDictImagesEnemys("Médio//Vampire",NSpritesMonsters)
lImagesZoiao            = loadDictImagesEnemys("Médio//Zoiao",NSpritesMonsters)

lImagesTombstone        = ([".//Resources//Monsters//tombstone.png"],1)
