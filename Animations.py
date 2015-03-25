def loadListOfSprites(route, nFrames):
    lImages = []
    for i in range(1,nFrames+1):
        lImages += [([route+str(i)+".png"],1)]
    return lImages
    

#Main Menu
lImagesSplashScreen     = ([".//Resources//MainMenu//splashScreen.png"],1)
lImagesPlayButton       = ([".//Resources//MainMenu//playerButton.png"],1)
lImagesOptionsButton    = ([".//Resources//MainMenu//optionsButton.png"],1)
lImagesQuitButton       = ([".//Resources//MainMenu//quitButton.png"],1)
lImagesBackground       = ([".//Resources//MainMenu//background3.png"],1)

#UI
lImagesButton       = ([".//Resources//UI//button.png"],1)
lImagesMouse        = ([".//Resources//UI//mouse.png"],1)
lImagesMouseHit     = ([".//Resources//UI//mouseHit.png"],1)
lImagesMouseSlow    = ([".//Resources//UI//mouseSlow.png"],1)
lImagesMousePoison  = ([".//Resources//UI//mousePoison.png"],1)
lImagesTabBar       = ([".//Resources//UI//bartab3.png"],1)
lImagesBottomBar    = ([".//Resources//UI//bottomBar.png"],1)
lImagesMoneyBar     = ([".//Resources//UI//moneyUIBar.png"],1)

lImagesMuteButtonOn = ([".//Resources//UI//muteButtonOn.png"],1)
lImagesMuteButtonOff = ([".//Resources//UI//muteButtonOff.png"],1)


    #Progress Bar
lImagesProgressStart    =([".//Resources//UI//progressBarStart.png"],1)
lImagesProgressMiddle   =([".//Resources//UI//progressBarMiddle.png"],1)
lImagesProgressEnd      =([".//Resources//UI//progressBarEnd.png"],1)
lImagesProgressBarMF    =([".//Resources//UI//progressBarMiddleFluid.png"],1)
lImagesProgressBarEF    =([".//Resources//UI//progressBarEndFluid.png"],1)

    #Icons
lImagesSlowIcon     =([".//Resources//UI//slowTowerIcon.png"],1)
lImagesDamageIcon   =([".//Resources//UI//damageTowerIcon.png"],1)
lImagesPoisonIcon   =([".//Resources//UI//poisonTowerIcon.png"],1)
lImagesFarmIcon   =([".//Resources//UI//FarmTowerIcon.png"],1)

    #Skills
lImagesTimeStopIcon     =([".//Resources//UI//timeSkillIcon.png"],1)
lImagesHealIcon         =([".//Resources//UI//HealSkillIcon.png"],1)
lImagesFireBallIcon     =([".//Resources//UI//fireBallSkillIcon.png"],1)

    #HealthBars
lImagesHPBarEnemyS = ([".//Resources//UI//eHealthBarStart.png"],1)
lImagesHPBarEnemyE = ([".//Resources//UI//eHealthBarEnd.png"],1)
lImagesHPBarEnemyM = ([".//Resources//UI//eHealthBarMiddle.png"],1)
lImagesHPBarTowerS = ([".//Resources//UI//tHealthBarStart.png"],1)
lImagesHPBarTowerE = ([".//Resources//UI//tHealthBarEnd.png"],1)
lImagesHPBarTowerM = ([".//Resources//UI//tHealthBarMiddle.png"],1)

    #WorldMap Entitys
lImagesBackgroundWM     = ([".//Resources//StageSelection//worldMap.png"],1)
lImagesStageWM          = ([".//Resources//Tilesets//world//stage.png"],1)
lImagesStageOpenedWM    = ([".//Resources//Tilesets//world//stageOpened.png"],1)
lImagesStageBeatedWM    = ([".//Resources//Tilesets//world//stageBeated.png"],1)

lImagesGameOverWin    = ([".//Resources//UI//youWin.png"],1)
lImagesGameOverLose    = ([".//Resources//UI//youLose.png"],1)

    #Map Entitys
lImagesVillage  = ([".//Resources//Tilesets//fullcity.png"],1)
lImagesPortal = ([".//Resources//Tilesets//portal.png"],0.3)

    #Portal Particles
lImagesPortalParticle = ([".//Resources//portalParticle.png",
                          ".//Resources//portalParticle2.png",
                          ".//Resources//portalParticle3.png"],0.3)

lImagesSlowTower = ([".//Resources//Towers//slowTower.png"],0.3)
lImagesDamageTower = ([".//Resources//Towers//torreComum.png"],0.3)
lImagesPoisonTower = ([".//Resources//Towers//poisonTower.png"],0.3)
lImagesFarmTower = ([".//Resources//Towers//farmTower.png"],0.3)

#Projectiles
lImagesSimpleProjectil = ([".//Resources//Projectiles//normalProjectile.png"],1)
lImagesSlowProjectil = ([".//Resources//Projectiles//slowProjectile.png"],1)
lImagesPoisonProjectil = ([".//Resources//Projectiles//poisonProjectile.png"],1)
lImagesFarmProjectil = ([".//Resources//Projectiles//farmProjectile.png"],1)

#Projectiles Particles
lImagesCommonExplosion = ([".//resources//Projectiles//normalProjectileExplosionParticle.png"],1)
lImagesSlowParticle = ([".//resources//Projectiles//slowParticle.png",
                        ".//resources//Projectiles//slowParticle2.png",
                        ".//resources//Projectiles//slowParticle3.png"],0.3)

lImagesPoisonParticle = ([".//resources//Projectiles//poisonParticle.png"],1)
lImagesFarmParticle = ([".//resources//Projectiles//farmParticle.png"],1)


#Skills Particles
lImagesHealParticle =([".//Resources//Skills//HealParticle.png"],1)

#Extra Particles
lImagesSmokeParticle = ([".//Resources//smokeParticle.png",
                          ".//Resources//smokeParticle2.png",
                          ".//Resources//smokeParticle3.png",
                          ".//Resources//smokeParticle4.png",],0.3)


