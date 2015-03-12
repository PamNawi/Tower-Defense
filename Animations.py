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
lImagesBackground       = ([".//Resources//MainMenu//background2.png"],1)

#UI
lImagesButton       = ([".//Resources//UI//button.png"],1)
lImagesMouse        = ([".//Resources//UI//mouse.png"],1)
lImagesMouseHit     = ([".//Resources//UI//mouseHit.png"],1)
lImagesMouseSlow    = ([".//Resources//UI//mouseSlow.png"],1)
lImagesMousePoison  = ([".//Resources//UI//mousePoison.png"],1)
lImagesTabBar       = ([".//Resources//UI//bartab3.png"],1)
lImagesBottomBar    = ([".//Resources//UI//bottomBar.png"],1)
lImagesMoneyBar     = ([".//Resources//UI//moneyUIBar.png"],1)

    #Icons
lImagesSlowIcon     =([".//Resources//UI//slowTowerIcon.png"],1)
lImagesDamageIcon   =([".//Resources//UI//damageTowerIcon.png"],1)
lImagesPoisonIcon   =([".//Resources//UI//poisonTowerIcon.png"],1)

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

    #Map Entitys
lImagesGrass    = ([".//Resources//Tilesets//grass.png"],1)
lImagesGraph    = ([".//Resources//Tilesets//grass.png"],1)
lImagesVillage  = ([".//Resources//Tilesets//fullcity.png"],1)
lImagesPortal = ([".//Resources//Tilesets//portal.png"],0.3)

        #Obstacles
lImagesRock = ([".//Resources//Tilesets//rock.png"],1)
lImagesTree0 = ([".//Resources//Tilesets//tree.png"],1)
lImagesTallGrass = ([".//Resources//Tilesets//tallgrass.png"],1)

        #Brigde
lImagesBrigde= loadListOfSprites(".//Resources//Tilesets//brigde//brigde",13)
lImagesWater = loadListOfSprites(".//Resources//Tilesets//water//water",13)

    #Portal Particles
lImagesPortalParticle = ([".//Resources//portalParticle.png",
                          ".//Resources//portalParticle2.png",
                          ".//Resources//portalParticle3.png"],0.3)

lImagesSlowTower = ([".//Resources//Towers//slowTower.png"],0.3)
lImagesDamageTower = ([".//Resources//Towers//torreComum.png"],0.3)
lImagesPoisonTower = ([".//Resources//Towers//poisonTower.png"],0.3)

#Projectiles
lImagesSimpleProjectil = ([".//Resources//Projectiles//normalProjectile.png"],1)
lImagesSlowProjectil = ([".//Resources//Projectiles//slowProjectile.png"],1)

#Projectiles Particles
lImagesCommonExplosion = ([".//resources//Projectiles//normalProjectileExplosionParticle.png"],1)
