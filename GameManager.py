import sys
sys.path.insert(0, './/miniEngine/')
from miniEngine import *
from ParticleFunctions import *
from Tiles import *
from Animations import *
from HUD import *
from Maps import *
from TowerDefenseGraph import *
from TowerFunctions import *

class GameManager:
    def __init__(self):
        self.mHUD = HUD()
        self.actualLevel = 0
        self.portalTiles = None
        self.cityTiles = None

        pass

    def load(self):
        mE.setGlobalVariable("Money",100)
        mE.mGlobalVariables["EndGame"] = False
        
        self.loadAnimations()
        self.loadUI()
        self.loadMap()

    def loadAnimations(self):
        #Especial Tiles Animations
        mE.mAnimationManager.addAnimation(lImagesPortal[0], lImagesPortal[1], "Portal")
        mE.mAnimationManager.addAnimation(lImagesVillage[0], lImagesVillage[1], "Village")
            #Towers
        mE.mAnimationManager.addAnimation(lImagesSlowTower[0], lImagesSlowTower[1], "SlowTower")
        mE.mAnimationManager.addAnimation(lImagesDamageTower[0], lImagesDamageTower[1], "HitTower")

        #Enemys Animation
        for mAni in lMonstersStats:
            mE.mAnimationManager.addAnimation(mAni["Animation"][0], mAni["Animation"][1], mAni["AnimationTag"])
            
        #UI
        mE.mAnimationManager.addAnimation(lImagesTabBar[0],lImagesTabBar[1], "TabBar")
        mE.mAnimationManager.addAnimation(lImagesBottomBar[0],lImagesBottomBar[1], "BottomBar")

            #Icons
        mE.mAnimationManager.addAnimation(lImagesSlowIcon[0], lImagesSlowIcon[1], "SlowIcon")
        mE.mAnimationManager.addAnimation(lImagesDamageIcon[0], lImagesDamageIcon[1], "DamageIcon")

            #HealthBars Enemys
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyS[0], lImagesHPBarEnemyS[1], "EnemyHealthBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyE[0], lImagesHPBarEnemyE[1], "EnemyHealthBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarEnemyM[0], lImagesHPBarEnemyM[1], "EnemyHealthBarMiddle")

            #HealthBars Towers
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerS[0], lImagesHPBarTowerS[1], "TowerHealthBarStart")
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerE[0], lImagesHPBarTowerE[1], "TowerHealthBarEnd")
        mE.mAnimationManager.addAnimation(lImagesHPBarTowerM[0], lImagesHPBarTowerM[1], "TowerHealthBarMiddle")

            #HealthBar City
        mE.mEntityManager.defineLayerOrder(["Towers", "Monsters", "UI"])
        
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

        #Create the bottomBar
        bottomBar = Entity()
        mE.mEntityManager.addEntity(bottomBar,"BottomBar","UI")
        mE.mAnimationManager.setEntityAnimation(bottomBar, "BottomBar")
        bottomBar.setPosition(3 *64 ,8*64)

        #Create the SlowButton
        slowButton = CooldownButton()
        slowButton.setCenterBoundingCircle(16,16)
        slowButton.setRadiusBoundingCircle(20)
        self.mHUD.addButton(self.showTowerStats, "Slow",Vec2d(3*64+29,8*64 +26),"SlowIcon")
        
        #Create Damage Icon
        damageIcon = CooldownButton()
        damageIcon.setCenterBoundingCircle(16,16)
        damageIcon.setRadiusBoundingCircle(20)
        self.mHUD.addButton(self.showTowerStats, "Hit", Vec2d(3 *64 +73 ,8*64 + 26), "DamageIcon")

        #Add TabBar for tower stats
        self.tabBar = TabBar()
        self.tabBar.setMinDesloc(800,80)
        self.tabBar.setMaxDesloc(800-180,80)
        self.tabBar.vecMaxSpeedDesloc  = 10
        self.mHUD.addTabBar(self.tabBar, "TabBar")

        #Create the texts for tower stats
        font = pygame.font.Font(None,18)
        mE.mTextManager.addFont(font, "None14")

        self.addTextTabBar((840,87),"TowerStats")
        mE.mTextManager.texts["TowerStats"].content = "Tower Stats"

        self.addTextTabBar((810,120),"TowerType")
        self.addTextTabBar((810,150),"TowerDamage")
        self.addTextTabBar((810,180),"TowerHP")
        self.addTextTabBar((810,210),"TowerCooldown")
        self.addTextTabBar((810,240),"TowerCost")

        #Add texts to HUD
        self.moneyUI = Text()
        self.mHUD.addText(self.moneyUI, "Money", "None14", "MoneyUI")
                
    def addTextTabBar(self, position, tag):
        t = Text()
        t.setPosition(position)
        self.tabBar.addEntity(t)
        mE.mTextManager.addText(t,tag)
        mE.mTextManager.setTextFont(tag, "None14")
        
    def loadMap(self):
        global graph
        global lMaps
        global PortalGraph
        global mE
       
        self.actualMap = lMaps[self.actualLevel]
        mapFile = self.actualMap[0]
        waveFile = self.actualMap[1]

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
            mMap = Map(64,64, 0,0)
            mMap.mAnimationManager.addAnimation(lImagesGrass[0],lImagesGrass[1],"0")
            mMap.mAnimationManager.addAnimation(lImagesMountain[0],lImagesMountain[1],"1")
            
            mMap.mAnimationManager.addAnimation(lImagesPortal[0],lImagesPortal[1],"3")            
            mMap.mAnimationManager.addAnimation(lImagesVillage[0],lImagesVillage[1],"4")

            #Trees  
            mMap.mAnimationManager.addAnimation(lImagesTree0[0],lImagesTree0[1],"t")


            mMap.createFactoryTile(Tile, {}, "1", "1")
            mMap.createFactoryTile(Tile, {}, "0", "0")
            
            mMap.createFactoryTile(Portal, {"ParticleManager": mE.mParticleManager , "Waves": self.waves}, "3", "3")
            mMap.createFactoryTile(City, {}, "4", "4")

            mMap.createFactoryTile(Tile, {}, "t", "t")
            
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
        
    def gameLoop(self):
        self.end = False

        while not self.end:
            mE.update()
            
            if(mE.keyboard.isPressed(pygame.K_ESCAPE)):
                self.end = True

            if(self.canPutTower()):
                if(mE.mouse.isPressed("LEFT")):
                    self.createTower("Slow",mE.mouse.getPosition())
                if(mE.mouse.isPressed("RIGHT")):
                    self.createTower("Hit",mE.mouse.getPosition())

            if(mE.keyboard.isPressed(pygame.K_SPACE)):
                self.tabBar.desappear()

            if(mE.mGlobalVariables["EndGame"]):
                print "Game Over"
                break

            self.mHUD.update()
            mE.render()

    def canPutTower(self):
        lCollisionTowerMouse = mE.mEntityManager.collision("Mouse", "Tower")
        if(not lCollisionTowerMouse):
            return True
        return False
    
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
            t.tag = "Tower"
            t.setPosition(position)
            t.setCenterBoundingCircle(32,32)
            t.setRadiusBoundingCircle(32)

            t.towerEffect   = dicTowers[tag]["Effect"]
            t.hp.maxHealth  = dicTowers[tag]["HP"]
            t.hp.health     = dicTowers[tag]["HP"]
            t.slow          = dicTowers[tag]["Slow"]
            t.poison        = dicTowers[tag]["PoisonDamage"]
            t.damage        = dicTowers[tag]["HitDamage"]
            t.cooldownShoot = dicTowers[tag]["Cooldown"]
                    
            if(dicTowers[tag]["ChooseMethod"] != None):
                t.chooseTargetMethod = dicTowers[tag]["ChooseMethod"]

            #Put on Graph
            graph = mE.mGlobalVariables["Graph"]
            graph.addWeightNode(t.graphPosition,50)
            self.recalculateRouteAllMonsters()
            return t

    def recalculateRouteAllMonsters(self):
        monsters = mE.mEntityManager.getTagEntitys("Monster")
        for m in monsters:
            m.recalculateRoute()

    def showTowerStats(self,params):
        tTowerType = mE.mTextManager.texts["TowerType"]
        tTowerType.content = "Tower Type: " + params

        tTowerDamage = mE.mTextManager.texts["TowerDamage"]
        tTowerDamage.content = "Damage: " + str(dicTowers[params]["HitDamage"])

        tTowerHP = mE.mTextManager.texts["TowerHP"]
        tTowerHP.content = "HP: " + str(dicTowers[params]["HP"])

        tTowerCooldown = mE.mTextManager.texts["TowerCooldown"]
        tTowerCooldown.content = "Cooldown: " + str(dicTowers[params]["Cooldown"])

        tTowerCost = mE.mTextManager.texts["TowerCost"]
        tTowerCost.content = "Cost: "+ str(dicTowers[params]["Cost"])
        
        self.tabBar.appear()
            
        
