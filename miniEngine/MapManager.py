from Entity import *
from ESTManager import *

class MapManager:
    def __init__(self):
        self.maps = {}
        self.layers = []
        
    def addMap(self, newMap, tag):
        self.maps[tag] = newMap

    def update(self, updateOnPause = None):
        lMaps = self.maps.values()
        for m in lMaps:
            m.update(updateOnPause)

    def setMapLayers(self,layerOrder):
        self.layers = layerOrder

    def getTiles(self, tileTag , mapTile = None):
        #If you choose the map tile return ONLY the list with tiles
        #Else you get a list with this format = [(map1, tiles1),... , (mapN, tilesN)]
        lTiles = []
        if mapTile == None:
            maps = self.maps.values()
            for m in maps:
                tiles = []
                if(m.mEntityManager.entitys.has_key(tileTag)):
                    tiles += m.mEntityManager.entitys[tileTag]
                if(tiles):
                    lTiles += [(m, tiles)]

        else:
            if(self.maps[mapTile].entitys.has_key(tileTag) ):
                lTiles = self.maps[mapTile].entitys[tileTag]
        return lTiles

    def getCollisions(self, entity, tag):
        lCollisions = []
        maps = self.maps.values()
        for m in maps:
            if(m.mEntityManager.entitys.has_key(tag)):
                tiles = m.mEntityManager.entitys[tag]
                for t in tiles:
                    if(isOnCollision(entity, t)):
                        lCollisions += [ t ]
        return lCollisions
                                                 
            
                
        

class Map:
    def __init__(self, width = 32, height = 32, shiftX = 100, shiftY = 100):
        self.map = [[]]
        self.width = width
        self.height = height
        self.mAnimationManager = AnimationManager()
        self.mEntityManager = EntityManager()
        self.mTileFactory = {}
        self.shiftX = shiftX
        self.shiftY = shiftY
        self.lIgnore = ['']
        self.isometricMap = False

    def placeTile(self, i ,j, tag):
        t = self.createTile(tag)
        t.setPosition(j * self.width + self.shiftX, i * self.height + self.shiftY)
        t.setCollisionBlock(Vec2d(self.width,self.height))
        return t

    def placeIsometricTile(self, i, j, tag):
        t = self.createTile(tag)
        isoPos = toIsometricCoordinates(i * self.width, j * self.height)
        t.setPosition(isoPos)
        t.setPosition(t.position[0] + self.shiftX, t.position[1] + self.shiftY)
        return t
    
    def loadMap(self, fileMap):
        f = open(fileMap).read().split('\n')
        i = 0
        self.map = [0] * len(f)
        for line in f:
            j = 0
            l = line.split('\t')
            self.map[i] = []
            for col in l:
                if(col not in self.lIgnore):
                    self.map[i] += [self.placeTile(i,j, col)]
                j += 1
            i += 1
            
    def loadIsometricMap(self, fileMap):
        f = open(fileMap).read().split('\n')
        i = 0
        self.map = [0] * len(f)
        for line in f:
            j = 0
            l = line.split('\t')
            self.map[i] = []
            for col in l:
                if(col not in self.lIgnore):
                    self.map[i] += [self.placeIsometricTile(i,j, col)]
                j += 1
            i += 1
        self.isometricMap = True


    def createTile(self, tag):
        dic = self.mTileFactory[tag]
        tile = dic["TileType"](dic["TileParams"])
        self.mAnimationManager.setEntityAnimation(tile, dic["Animation"])
        self.mEntityManager.addEntity(tile,tag)
        return tile

    def getTileCoordinate(self, screenPosition):
        x = screenPosition[0]
        y = screenPosition[1]
        i = (x - self.shiftX) % self.width
        j = (y - self.shiftY) % self.height
        return self.map[i][j]

    def getTileIsometric(self, screenPosition):
        position = toCartesianCoordinates(screenPosition[0], screenPosition[1])
        return self.getTileCoordinate(position)

    def createFactoryTile(self, tileType, paramsTile, tagAnimationTile, tag):
        self.mTileFactory[tag] = {"TileType" : tileType, "TileParams": paramsTile, "Animation" : tagAnimationTile}

    def update(self, updateOnPause):
        self.mEntityManager.update(updateOnPause)

    def toScreenCoordinate(self,position):
        if(self.isometricMap):
            position = toIsometricCoordinates(position[0] * self.width ,position[1] * self.self.height)
            position[0] += self.shiftX
            position[1] += self.shiftY
        else:
            position = (position[0] * self.width + self.shiftX, position[1] * self.height + self.shiftY)
        return position

    def toMapCoordinate(self,position):
        position = (position[0] - self.shiftX, position[1] - self.shiftY)
        if(self.isometricMap):
            position = toCartesianCoordinates(position[0], position[1])
        position = (position[0] / self.width , position[1] / self.height)
        return position

class Tile(Entity):
    def __init__(self, dicParams):
        Entity.__init__(self)
    
def toIsometricCoordinates(cartX,cartY):
    isoX = cartX - cartY;
    isoY = (cartX + cartY) / 2
    return (isoX, isoY)

def toCartesianCoordinates(isoX, isoY):
    cartX = (2 * isoY + isoX)/2
    cartY = (2 * isoY - isoX)/2
    return(cartX, cartY)

