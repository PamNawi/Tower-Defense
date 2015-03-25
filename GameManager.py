import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *
from ParticleFunctions import *
from Tiles import *
from Animations import *
from Sounds import *
from HUD import *
from Maps import *
from TowerDefenseGraph import *
from TowerFunctions import *
from SkillsFunctions import *
from Descriptions import *

class GameManager:
    def __init__(self):
        self.mHUD = HUD()
        self.actualLevel = 0
        self.portalTiles = None
        self.cityTiles = None

        self.selectedTower = ""
        self.selectedSkill = ""

        mE.updateOnPause = ["Mouse", "Button","InfoTabBar", "SkillTimeStop"]
        self.playerWins = True
        pass

    def load(self):
        mE.setGlobalVariable("Money",100)
        mE.mGlobalVariables["EndGame"] = False
        
        self.loadAnimations()
        self.loadUI()
        self.loadMap()
        self.loadSounds()
        self.loadParticles()

    def loadParticles(self):
        mE.mParticleManager.addUpdateFunction(lImagesSlowParticle[0],    lImagesSlowParticle[1], cascate , "cascate")
        #Explosions
        mE.mParticleManager.addUpdateFunction(lImagesCommonExplosion[0], lImagesCommonExplosion[1], explosion , "commonExplosion")
        mE.mParticleManager.addUpdateFunction(lImagesSlowParticle[0],  lImagesSlowParticle[1], explosion , "slowExplosion")
        mE.mParticleManager.addUpdateFunction(lImagesPoisonParticle[0],  lImagesPoisonParticle[1], explosion , "poisonExplosion")
        mE.mParticleManager.addUpdateFunction(lImagesFarmParticle[0],  lImagesFarmParticle[1], explosion , "farmExplosion")

        mE.mParticleManager.addUpdateFunction(lImagesHealParticle[0], lImagesHealParticle[1], spin , "healParticle")
        
        mE.mParticleManager.addUpdateFunction(lImagesSmokeParticle[0], lImagesSmokeParticle[1], spin , "Smoke")
        
    def loadSounds(self):
        mE.mJukebox.LoadSong(levelSong, "LevelSong")
        mE.mJukebox.LoadSong(bossFight, "BossFight")
        
        mE.mJukebox.LoadSound(newTowerSound, "NewTower")
        mE.mJukebox.LoadSound(error, "Error")
        mE.mJukebox.LoadSound(damage, "Damage")
        mE.mJukebox.LoadSound(magic, "Magic")
        mE.mJukebox.LoadSound(teleport, "Teleport")
        mE.mJukebox.LoadSound(coming, "MonstersComing")
        mE.mJukebox.LoadSound(heart, "Heart")
        mE.mJukebox.LoadSound(heal, "Heal")
        mE.mJukebox.LoadSound(timeRunning, "TimeRunning")
        mE.mJukebox.LoadSound(alarmClock, "AlarmClock")

        for monsterSound in lMonstersSounds:
            mE.mJukebox.LoadSound(monsterSound[0], monsterSound[1])
        

    def loadAnimations(self):
        #Especial Tiles Animations
        mE.mAnimationManager.addAnimation(lImagesPortal[0], lImagesPortal[1], "Portal")
        mE.mAnimationManager.addAnimation(lImagesVillage[0], lImagesVillage[1], "Village")
        
            #Towers
        mE.mAnimationManager.addAnimation(lImagesSlowTower[0], lImagesSlowTower[1], "SlowTower")
        mE.mAnimationManager.addAnimation(lImagesDamageTower[0], lImagesDamageTower[1], "HitTower")
        mE.mAnimationManager.addAnimation(lImagesPoisonTower[0], lImagesPoisonTower[1], "PoisonTower")
        mE.mAnimationManager.addAnimation(lImagesFarmTower[0], lImagesFarmTower[1], "FarmTower")

        #Enemys Animation
        for mAni in lMonstersStats:
            mE.mAnimationManager.addAnimation(mAni["Animation"]["Up"][0], mAni["Animation"]["Up"][1], mAni["AnimationTag"]+"Up")
            mE.mAnimationManager.addAnimation(mAni["Animation"]["Down"][0], mAni["Animation"]["Down"][1], mAni["AnimationTag"]+"Down")
            mE.mAnimationManager.addAnimation(mAni["Animation"]["Left"][0], mAni["Animation"]["Left"][1], mAni["AnimationTag"]+"Left")
            mE.mAnimationManager.addAnimation(mAni["Animation"]["Right"][0], mAni["Animation"]["Right"][1], mAni["AnimationTag"]+"Right")

        mE.mAnimationManager.addAnimation(lImagesTombstone[0],lImagesTombstone[1], "Tombstone")
            
        #UI
        mE.mAnimationManager.addAnimation(lImagesMouse[0],lImagesMouse[1], "Mouse")
        mE.mAnimationManager.addAnimation(lImagesMouseHit[0],lImagesMouseHit[1], "MouseHit")
        mE.mAnimationManager.addAnimation(lImagesMouseSlow[0],lImagesMouseSlow[1], "MouseSlow")
        mE.mAnimationManager.addAnimation(lImagesMousePoison[0],lImagesMousePoison[1], "MousePoison")

        mE.mAnimationManager.addAnimation(lImagesMuteButtonOn[0],lImagesMuteButtonOn[1], "MuteButtonON")
        mE.mAnimationManager.addAnimation(lImagesMuteButtonOff[0],lImagesMuteButtonOff[1], "MuteButtonOFF")
        
        mE.mAnimationManager.addAnimation(lImagesTabBar[0],lImagesTabBar[1], "TabBar")
        mE.mAnimationManager.addAnimation(lImagesBottomBar[0],lImagesBottomBar[1], "BottomBar")
        mE.mAnimationManager.addAnimation(lImagesMoneyBar [0],lImagesMoneyBar[1], "MoneyUIBar")

            #Icons
        mE.mAnimationManager.addAnimation(lImagesSlowIcon[0], lImagesSlowIcon[1], "SlowIcon")
        mE.mAnimationManager.addAnimation(lImagesDamageIcon[0], lImagesDamageIcon[1], "DamageIcon")
        mE.mAnimationManager.addAnimation(lImagesPoisonIcon[0], lImagesPoisonIcon[1], "PoisonIcon")
        mE.mAnimationManager.addAnimation(lImagesFarmIcon[0], lImagesFarmIcon[1], "FarmIcon")

        
        mE.mAnimationManager.addAnimation(lImagesTimeStopIcon[0], lImagesTimeStopIcon[1], "TimeStopIcon")
        mE.mAnimationManager.addAnimation(lImagesHealIcon[0], lImagesHealIcon[1], "HealIcon")
        mE.mAnimationManager.addAnimation(lImagesFireBallIcon[0], lImagesFireBallIcon[1], "FireBallIcon")

            #HealthBars Enemysself.selectedSkill
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyS[0], lImagesHPBarEnemyS[1], "EnemyHealthBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyE[0], lImagesHPBarEnemyE[1], "EnemyHealthBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyM[0], lImagesHPBarEnemyM[1], "EnemyHealthBarMiddle")

            #HealthBars Towers
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerS[0], lImagesHPBarTowerS[1], "TowerHealthBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerE[0], lImagesHPBarTowerE[1], "TowerHealthBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerM[0], lImagesHPBarTowerM[1], "TowerHealthBarMiddle")


            #CooldownBars Towers
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerS[0], lImagesHPBarTowerS[1], "CooldownBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerE[0], lImagesHPBarTowerE[1], "CooldownBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerM[0], lImagesHPBarTowerM[1], "CooldownBarMiddle")

            #ProgressBar
        mE.mAnimationManager.addAnimation(lImagesProgressStart[0], lImagesProgressStart[1], "ProgressBarStart")
        mE.mAnimationManager.addAnimation(lImagesProgressMiddle[0], lImagesProgressMiddle[1], "ProgressBarMiddle")
        mE.mAnimationManager.addAnimation(lImagesProgressEnd[0], lImagesProgressEnd[1], "ProgressBarEnd")
        mE.mAnimationManager.addAnimation(lImagesProgressBarMF[0], lImagesProgressBarMF[1], "ProgressBarMF")
        mE.mAnimationManager.addAnimation(lImagesProgressBarEF[0], lImagesProgressBarEF[1], "ProgressBarEF")

            #Projectiles
        mE.mAnimationManager.addAnimation(lImagesSimpleProjectil[0],lImagesSimpleProjectil[1], "SimpleProjectil")
        mE.mAnimationManager.addAnimation(lImagesSlowProjectil[0],lImagesSlowProjectil[1], "SlowProjectil")   
        mE.mAnimationManager.addAnimation(lImagesPoisonProjectil[0],lImagesPoisonProjectil[1], "PoisonProjectil")     
        mE.mAnimationManager.addAnimation(lImagesFarmProjectil[0],lImagesFarmProjectil[1], "FarmProjectil")                          

            #HealthBar City
        mE.mEntityManager.defineLayerOrder(["Tombstone","Towers", "Monsters", "BackUI", "UI"])
        
    def setPortalCoordinates(self):
        self.portalTiles = mE.mMapManager.getTiles("3")
        
        mapPortal = self.portalTiles[0][0]
        portalCoord = self.portalTiles[0][1][0]
        portalCoord = mapPortal.toMapCoordinate(portalCoord.position)
        portalCoord = (0,portalCoord[0] * tileWidth,portalCoord[1] * tileHeigth)
        
        #Create a global variable PortalCoord who have the position of the portal
        mE.setGlobalVariable("PortalCoord",    portalCoord)
        mE.setGlobalVariable("PortalMapCoord", mapPortal)

    def setCityCoordinates(self): #Do the same thing with City Coordinates
        self.cityTiles = mE.mMapManager.getTiles("4")

        mapCity = self.cityTiles[0][0]
        cityCoord = self.cityTiles[0][1][0]
        cityCoord = mapCity.toMapCoordinate(cityCoord.position)
        cityCoord = (0,cityCoord[0] * tileWidth, cityCoord[1] * tileHeigth)

        mE.setGlobalVariable("CityCoord",   cityCoord)
        mE.setGlobalVariable("CityMapCoor", mapCity)

    def loadUI(self):
        self.mHUD.loadEntitys()

        #Load the fonts
        mE.mTextManager.addFont(pygame.font.Font(None,16), "None14")
        mE.mTextManager.addFont(pygame.font.Font(None,20), "None20")
        mE.mTextManager.addFont(pygame.font.Font(None,28), "None32")

        #Create the bottomBar
        bottomBar = Entity()
        mE.mEntityManager.addEntity(bottomBar,"BottomBar","UI")
        mE.mAnimationManager.setEntityAnimation(bottomBar, "BottomBar")
        bottomBar.setPosition(50 ,686)
        self.icons = {}

        #Create the SlowIcon
        slowButton = self.mHUD.addCooldownButton(self.selectTower, "Slow",Vec2d(79,712),"SlowIcon", Vec2d(34,34), )
        slowButton.cooldownBar.setPosition(Vec2d(86,751))
        self.icons["Slow"] = slowButton
        
        #Create DamageIcon
        hitButton = self.mHUD.addCooldownButton(self.selectTower, "Hit", Vec2d(123 , 712), "DamageIcon", Vec2d(34,34))
        hitButton.cooldownBar.setPosition(Vec2d(130,751))
        self.icons["Hit"] = hitButton

        #Create PoisonIcon
        poisonButton = self.mHUD.addCooldownButton(self.selectTower, "Poison", Vec2d(167 , 712), "PoisonIcon", Vec2d(34,34), cooldown = 15.0)
        poisonButton.cooldownBar.setPosition(Vec2d(174,751))
        self.icons["Poison"] = poisonButton

        #Create FarmIcon
        farmButton = self.mHUD.addCooldownButton(self.selectTower, "Farm", Vec2d(211, 712), "FarmIcon", Vec2d(34,34))
        farmButton.cooldownBar.setPosition(Vec2d(218,751))
        self.icons["Farm"] = farmButton

        #Create the bottomBar
        skillBar = Entity()
        mE.mEntityManager.addEntity(skillBar,"BottomBar","UI")
        mE.mAnimationManager.setEntityAnimation(skillBar, "BottomBar")
        skillBar.setPosition(424 + 180,686)
        self.skillIcons = {}

        #Create the TimeStopIcon
        timeStopButton = self.mHUD.addCooldownButton(self.selectSkill, "TimeStop",Vec2d(79-50+ 424+180,712),"TimeStopIcon", Vec2d(34,34), cooldown = 60.0)
        timeStopButton.cooldownBar.setPosition(Vec2d(86-50+ 424+180,751))
        self.skillIcons["TimeStop"] = timeStopButton

        #Create the HealIcon
        healButton = self.mHUD.addCooldownButton(self.selectSkill, "Heal",Vec2d(123-50+ 424+180,712),"HealIcon", Vec2d(34,34), cooldown = 30.0)
        healButton.cooldownBar.setPosition(Vec2d(130-50+ 424+180,751))
        self.skillIcons["Heal"] = healButton

        #Create the FireBallIcon
        fireBallButton = self.mHUD.addCooldownButton(self.selectSkill, "FireBall",Vec2d(167-50+ 424+180,712),"FireBallIcon", Vec2d(34,34), cooldown = 30.0)
        fireBallButton.cooldownBar.setPosition(Vec2d(174-50+ 424+180,751))
        self.skillIcons["FireBall"] = fireBallButton
        
        
        #Add TabBar for tower stats
        self.tabBar = TabBar()
        tabBarPos = (1024, 80)
        self.tabBar.setMinDesloc(tabBarPos[0],tabBarPos[1])
        self.tabBar.setMaxDesloc(tabBarPos[0]-180,tabBarPos[1])
        self.tabBar.vecMaxSpeedDesloc  = 10
        self.mHUD.addTabBar(self.tabBar, "Info")

        #Create the texts for tower stats
        self.addTextTabBar((tabBarPos[0] +10,120),"Description0")      
        self.addTextTabBar((tabBarPos[0] +10,140),"Description1")
        self.addTextTabBar((tabBarPos[0] +10,160),"Description2")

        self.pauseUI = Text()
        self.pauseUI.setPosition(500, 200)
        mE.mTextManager.addText(self.pauseUI,"PauseUI")
        mE.mTextManager.setTextFont("PauseUI", "None32")

        #Add a circle around the mouse
        self.circle = Circle()
        self.circle.color = (55,151,125)
        mE.mPrimitiveManager.addPrimitive(self.circle, "MouseCircle")

        #Add the Twinkle little text
        self.tText = createTwinkleText("- Shapen the arrows - ","None32")
        self.tText.startTwinkle()
        self.tText.setPosition(400,200)

        mE.mEntityManager.addEntity(self.tText, "TwinkleText")

        #Add the money ui bar
        moneyBar = Entity()
        mE.mEntityManager.addEntity(moneyBar,"MoneyUIBar","UI")
        mE.mAnimationManager.setEntityAnimation(moneyBar, "MoneyUIBar")
        moneyBar.setPosition(424,710)

        #Add texts to HUD
        self.moneyUI = Text()
        self.moneyUI.color = (255,255,255)
        self.mHUD.addText(self.moneyUI, "Money", "None32", "MoneyUI")
        self.moneyUI.setPosition(470, 725)

        #Create Mute Button
        self.muteButton = self.mHUD.addButton(toggleSound,None, Vec2d(960,6), "MuteButtonON", Vec2d(34,34))
        self.muteButton.params = self.muteButton

    def addTextTabBar(self, position, tag):
        t = Text()
        t.color = (255,255,255)
        t.setPosition(position)
        self.tabBar.addEntity(t)
        mE.mTextManager.addText(t,tag)
        mE.mTextManager.setTextFont(tag, "None14")
        
      
    def gameLoop(self):
        self.end = False

        mE.mJukebox.PlaySong("LevelSong")
        #mE.mJukebox.PlaySong("BossFight")
        while not self.end:
            mE.update()
            
            if(mE.keyboard.isPressed(pygame.K_ESCAPE)):
                self.selectedTower = ""
                mouse = self.mHUD.mouseEntity
                mE.mAnimationManager.setEntityAnimation(mouse,"Mouse")
                #self.end = True

            if(self.selectedTower != "" and self.canPutTower()):
                mousePosition = mE.mouse.getPosition()
                self.circle.position = (mousePosition[0], mousePosition[1])
                self.circle.radius = dicTowers[self.selectedTower]["Range"]
                if(mE.mouse.isPressed("LEFT")):
                    self.createTower(self.selectedTower, mousePosition)

            elif(self.selectedSkill != "" and self.canCastSkill()):
                mousePosition = mE.mouse.getPosition()
                self.circle.position = (mousePosition[0], mousePosition[1])
                self.circle.radius = dicSkills[self.selectedSkill]["Range"]
                if(mE.mouse.isPressed("LEFT")):
                    self.castSkill(self.selectedSkill, mousePosition)

            else:
                self.circle.position = (-2,-2)
                self.circle.radius = (1)

            if(self.isOver()):
                break
                print "Game Over"
                
            self.showInfo()
            self.addTimeCash()

            #print self.tText.text.content

            self.mHUD.update()
            mE.render()

    def canPutTower(self):
        mouse = self.mHUD.mouseEntity
        lCollisionTowerMouse =  mE.mEntityManager.collision("Mouse", "Tower")
        lCollisionMouseWalkable = []
        for t in walkable:
            lCollisionMouseWalkable += mE.mMapManager.getCollisions(mouse, t)
        if(not lCollisionTowerMouse and not self.icons[self.selectedTower].cooldownBar.isActive() and lCollisionMouseWalkable):
            return True
        return False

    def canCastSkill(self):
        mouse = self.mHUD.mouseEntity
        lCollisionMouseWalkable = []
        for t in walkable:
            lCollisionMouseWalkable += mE.mMapManager.getCollisions(mouse, t) 
        if(not self.skillIcons[self.selectedSkill].cooldownBar.isActive() and lCollisionMouseWalkable):
            return True
        return False

    def showInfo(self):
        lCollisionIconMouse = mE.mEntityManager.collision("Mouse", "Button")
        if(lCollisionIconMouse):
            button = lCollisionIconMouse[0][1]
            if(button != self.muteButton):
                self.showDescription(button.params)
        else:
            self.tabBar.disappear()

    def addTimeCash(self):
        pass

    def castSkill(self, tag, position = Vec2d(0,0)):
        params = {"Position": position, "Range": dicSkills[tag]["Range"]}
        dicSkills[tag]["Function"](params)

        self.skillIcons[self.selectedSkill].activeCooldown()
    
    def createTower(self,tag,position = Vec2d(0,0)):
        global mE
        global dicTowers
        #If have money
        if(mE.mGlobalVariables["Money"] >= dicTowers[tag]["Cost"]):
            #Update the UI
            mE.mGlobalVariables["Money"] += -dicTowers[tag]["Cost"]
            self.moneyUI.content = "Money: " + str(mE.mGlobalVariables["Money"])

            #Create the tower
            t = Tower()
            mE.mAnimationManager.setEntityAnimation(t, tag+"Tower")
            mE.mEntityManager.addEntity(t,"Tower", "Towers")
            t.tag = tag

            t.towerEffect   = dicTowers[tag]["Effect"]
            #t.hp.maxHealth  = dicTowers[tag]["HP"]
            #t.hp.health     = dicTowers[tag]["HP"]
            t.slow          = dicTowers[tag]["Slow"]
            t.poison        = dicTowers[tag]["PoisonDamage"]
            t.damage        = dicTowers[tag]["HitDamage"]
            t.cooldownShoot = dicTowers[tag]["Cooldown"]
            t.range         = dicTowers[tag]["Range"]

            t.hp = HealthBar(dicTowers[tag]["HP"])
            t.hp.addToEntityManager()
            t.hp.setAnimation("TowerHealthBarStart", "TowerHealthBarEnd", "TowerHealthBarMiddle")
                    
            if(dicTowers[tag]["ChooseMethod"] != None):
                t.chooseTargetMethod = dicTowers[tag]["ChooseMethod"]

            t.setCollisionBlock(Vec2d(tileWidth,tileHeigth))
            t.setPosition(position)
            t.setCenterBoundingCircle(32,32)
            t.setRadiusBoundingCircle(32)

            #Put on Graph
            graph = mE.mGlobalVariables["Graph"]
            graph.addWeightNode(t.graphPosition,50)
            self.recalculateRouteAllMonsters()

            #Start iconCooldown
            self.icons[self.selectedTower].activeCooldown()
            mE.mJukebox.PlaySound("NewTower")
            return t
        else:
            mE.mJukebox.PlaySound("Error")

    def recalculateRouteAllMonsters(self):
        monsters = mE.mEntityManager.getTagEntitys("Monster")
        for m in monsters:
            m.recalculateRoute()

    
    def selectTower(self,params):
        self.selectedSkill = ""
        self.selectedTower = params
        mouse = self.mHUD.mouseEntity
        mE.mAnimationManager.setEntityAnimation(mouse,"Mouse"+ params)

    def selectSkill(self,params):
        self.selectedSkill = params
        self.selectedTower = ""
        mouse = self.mHUD.mouseEntity
        mE.mAnimationManager.setEntityAnimation(mouse, "Mouse")

    def showDescription(self, params):
        tDescription0 = mE.mTextManager.texts["Description0"]
        tDescription0.content = Descriptions[params][0]
        
        tDescription1 = mE.mTextManager.texts["Description1"]
        tDescription1.content = Descriptions[params][1]
        
        tDescription2 = mE.mTextManager.texts["Description2"]
        tDescription2.content = Descriptions[params][2]
        
        self.tabBar.appear()
        

    def loadTileset(self, tileset, mMap):
        global tilesets
        for tile in tilesets[tileset]:
            animation = tilesets[tileset][tile]["Animation"]
            symbol = tilesets[tileset][tile]["Symbol"]
            mMap.mAnimationManager.addAnimation( animation[0], animation[1], tile )
            mMap.createFactoryTile(Tile, {}, tile, symbol)

        mMap.mAnimationManager.addAnimation(lImagesPortal[0],lImagesPortal[1],"Portal")            
        mMap.mAnimationManager.addAnimation(lImagesVillage[0],lImagesVillage[1],"City")
                
        mMap.createFactoryTile(Portal, {"ParticleManager": mE.mParticleManager , "Waves": self.waves}, "Portal", "3")
        mMap.createFactoryTile(City, {}, "City", "4")

    def loadMap(self):
        global graph
        global lMaps
        global PortalGraph
        global mE
       
        self.actualMap = lMaps[self.actualLevel]
        mapFile = self.actualMap[0]
        waveFile = self.actualMap[1]
        tileset = self.actualMap[2]


        #Load the wave
        f = open(waveFile).read().split('\n')

        self.nWaves = len(f)-1
        self.waves = {}
        i = 0
        for line in f:
            l = line.split('\t')
            self.waves[i] = []
            for enemy in l:
                self.waves[i] += [int(enemy)]
            i +=1
            
        #Load the map
        i = 0
        for m in mapFile:
            mMap = Map(tileWidth,tileHeigth, 0,0)

            self.loadTileset(tileset, mMap)

            mMap.loadMap(m)
            mE.mMapManager.addMap(mMap, m)
            i += 1

        #Put the layers on order...
        mE.mMapManager.setMapLayers(mapFile)
        
        graph = TowerDefenseGraph()
        graph.walkable = walkable
        graph.loadGraphFromMaps(mapFile, tileWidth, tileHeigth)
        mE.mGlobalVariables["Graph"] = graph
        
        self.setPortalCoordinates()
        self.setCityCoordinates()

    def isOver(self):
        #if there is no monster alive
        monster = mE.mEntityManager.getTagEntitys("Monster")
        #if there is no monster to spawn
        pTile = self.portalTiles[0][1][0]
        if(not pTile.gonnaSpawnMore() and monster == []):
            #the player wins
            self.playerWins = True
            return True
        if(mE.mGlobalVariables["EndGame"]):
            self.playersWins = False
            return True
        #if the city has no more hp
        #the player loose
        self.playerWins = False

        return False
    def saveGame(self):
        pass

def toggleSound(button):
    
    if(mE.mJukebox.music_on):
        print "Desligando o audio"
        mE.mAnimationManager.setEntityAnimation(button, "MuteButtonOFF")
        mE.mJukebox.ToggleMusic(False)
        mE.mJukebox.ToggleSound(False)
        mE.mJukebox.StopMusic()
    else:
        print "Ligando o audio"
        mE.mAnimationManager.setEntityAnimation(button, "MuteButtonON")
        mE.mJukebox.ToggleMusic()
        mE.mJukebox.ToggleSound()
        mE.mJukebox.PlaySong("LevelSong")
