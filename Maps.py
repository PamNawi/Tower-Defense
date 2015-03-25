walkable = ["0", "1", "3","4", "tg" , "b0", "b1", "b2", "b3", "b4", "b5" , "b9", "b10"]
walkable += ["s", "s1", "tsg"]
tileWidth   = 50
tileHeigth  = 50

#MapFormat:
#nameMap = (list of layers on map, file with waves)
#Map 1
layersMap1 = [ ".//resources//Maps//mapa0.txt"]
layersMap2 = [ ".//resources//Maps//mapa1.txt"]
layersMap3 = [ ".//resources//Maps//mapa2.txt"]
layersMap4 = [ ".//resources//Maps//mapa3.txt"]
layersMap5 = [ ".//resources//Maps//mapa4.txt"]
layersMap6 = [ ".//resources//Maps//mapa5.txt"]
layersMap7 = [ ".//resources//Maps//mapa6.txt"]
layersMap8 = [ ".//resources//Maps//mapa7.txt"]

map1 = (layersMap1,".//Resources//Maps//waves0.txt", "Forest")
map2 = (layersMap2,".//Resources//Maps//waves1.txt", "Forest")
map3 = (layersMap3,".//Resources//Maps//waves2.txt", "Plains")
map4 = (layersMap4,".//Resources//Maps//waves3.txt", "Swamp")
map5 = (layersMap5,".//Resources//Maps//waves4.txt", "Forest")
map6 = (layersMap6,".//Resources//Maps//waves5.txt", "Forest")
map7 = (layersMap7,".//Resources//Maps//waves6.txt", "Beach")
map8 = (layersMap8,".//Resources//Maps//waves7.txt", "Beach" )

#Put this map on list of maps in game
lMaps = [ map1, map2, map3, map4, map5, map6, map7, map8 ]

def loadListOfSprites(route, nFrames):
    lImages = []
    for i in range(1,nFrames+1):
        lImages += [([route+str(i)+".png"],1)]
    return lImages

tilesets = {}

#Forest tileset basic
tilesets["Forest"] = {}
tilesets["Forest"]["Grass0"]     =   {"Animation":   ([".//Resources//Tilesets//forest//grass0.png"],1),      "Symbol": "0"}
tilesets["Forest"]["Grass1"]     =   {"Animation":   ([".//Resources//Tilesets//forest//grass1.png"],1),      "Symbol": "1"}
tilesets["Forest"]["Rock"]      =   {"Animation":   ([".//Resources//Tilesets//forest//rock.png"],1),       "Symbol": "r"}
tilesets["Forest"]["Tree"]      =   {"Animation":   ([".//Resources//Tilesets//forest//tree.png"],1),       "Symbol": "t"}
tilesets["Forest"]["TallGrass"] =   {"Animation":   ([".//Resources//Tilesets//forest//tallgrass.png"],1),  "Symbol": "tg"}

tilesets["Forest"]["CuttedTree"] = {"Animation":   ([".//Resources//Tilesets//forest//cuttedTree.png"],1),  "Symbol": "ct"}
lImagesWaterForest = loadListOfSprites(".//Resources//Tilesets//forest//water//water",13)
i = 0
for t in lImagesWaterForest:
    tilesets["Forest"]["Water"+str(i)] =  {"Animation" : t, "Symbol": "w"+str(i)}
    i+= 1
    
lImagesBrigde= loadListOfSprites(".//Resources//Tilesets//forest//brigde//brigde",13)
i = 0
for t in lImagesBrigde:
    tilesets["Forest"]["Brigde"+str(i)] =  {"Animation" : t, "Symbol": "b"+str(i)}
    i+= 1

    #Beach tileset basic
tilesets["Beach"] = {}
tilesets["Beach"]["Sand0"]     =   {"Animation":   ([".//Resources//Tilesets//beachTiles//sand0.png"],1),      "Symbol": "s"}
tilesets["Beach"]["Sand1"]     =   {"Animation":   ([".//Resources//Tilesets//beachTiles//sand1.png"],1),      "Symbol": "s1"}
tilesets["Beach"]["Rock"]      =   {"Animation":   ([".//Resources//Tilesets//beachTiles//rock.png"],1),       "Symbol": "r"}
tilesets["Beach"]["Tree"]      =   {"Animation":   ([".//Resources//Tilesets//beachTiles//tree.png"],1),       "Symbol": "t"}
tilesets["Beach"]["TallGrass"] =   {"Animation":   ([".//Resources//Tilesets//beachTiles//tallgrass.png"],1),  "Symbol": "tg"}

tilesets["Beach"]["CuttedTree"] = {"Animation":   ([".//Resources//Tilesets//beachTiles//cuttedTree.png"],1),  "Symbol": "ct"}

lImagesWaterBeach = loadListOfSprites(".//Resources//Tilesets//beachTiles//water//w",13)
i = 0
for t in lImagesWaterBeach:
    tilesets["Beach"]["Water"+str(i)] =  {"Animation" : t, "Symbol": "w"+str(i)}
    i+= 1

    #Plains tileset basic
tilesets["Plains"] = {}
tilesets["Plains"]["Grass0"]     =   {"Animation":   ([".//Resources//Tilesets//plains//grass0.png"],1),      "Symbol": "0"}
tilesets["Plains"]["Grass1"]     =   {"Animation":   ([".//Resources//Tilesets//plains//grass1.png"],1),      "Symbol": "1"}
tilesets["Plains"]["Rock"]      =   {"Animation":   ([".//Resources//Tilesets//plains//rock.png"],1),       "Symbol": "r"}
tilesets["Plains"]["Tree"]      =   {"Animation":   ([".//Resources//Tilesets//plains//tree.png"],1),       "Symbol": "t"}
tilesets["Plains"]["TallGrass"] =   {"Animation":   ([".//Resources//Tilesets//plains//tallgrass.png"],1),  "Symbol": "tg"}

tilesets["Plains"]["CuttedTree"] = {"Animation":   ([".//Resources//Tilesets//plains//cuttedTree.png"],1),  "Symbol": "ct"}
tilesets["Plains"]["Flower"] = {"Animation":   ([".//Resources//Tilesets//plains//flowers.png"],1),  "Symbol": "f"}

i = 0
for t in lImagesWaterForest:
    tilesets["Plains"]["Water"+str(i)] =  {"Animation" : t, "Symbol": "w"+str(i)}
    i+= 1

i = 0
for t in lImagesBrigde:
    tilesets["Plains"]["Brigde"+str(i)] =  {"Animation" : t, "Symbol": "b"+str(i)}
    i+= 1
    
lImagesFence= loadListOfSprites(".//Resources//Tilesets//plains//Fence//",9)
i = 0
for t in lImagesFence:
    tilesets["Plains"]["Fence"+str(i)] =  {"Animation" : t, "Symbol": "f"+str(i)}
    i+= 1
	
#Swamp tileset basic
tilesets["Swamp"] = {}
tilesets["Swamp"]["Grass0"]     =   {"Animation":   ([".//Resources//Tilesets//Swamp//grass0.png"],1),      "Symbol": "0"}
tilesets["Swamp"]["Grass1"]     =   {"Animation":   ([".//Resources//Tilesets//Swamp//grass1.png"],1),      "Symbol": "1"}
tilesets["Swamp"]["Rock"]      =   {"Animation":   ([".//Resources//Tilesets//Swamp//rock.png"],1),       "Symbol": "r"}
tilesets["Swamp"]["Tree"]      =   {"Animation":   ([".//Resources//Tilesets//Swamp//tree.png"],1),       "Symbol": "t"}
tilesets["Swamp"]["TallGrass"] =   {"Animation":   ([".//Resources//Tilesets//Swamp//tallgrass.png"],1),  "Symbol": "tg"}

tilesets["Swamp"]["CuttedTree"] = {"Animation":   ([".//Resources//Tilesets//Swamp//cuttedTree.png"],1),  "Symbol": "ct"}
tilesets["Swamp"]["CuttedTree"] = {"Animation":   ([".//Resources//Tilesets//Swamp//waterTree.png"],1),  "Symbol": "wt"}
lImagesWaterSwamp = loadListOfSprites(".//Resources//Tilesets//Swamp//water//water",13)
i = 0
for t in lImagesWaterSwamp:
    tilesets["Swamp"]["Water"+str(i)] =  {"Animation" : t, "Symbol": "w"+str(i)}
    i+= 1
    
i = 0
for t in lImagesBrigde:
    tilesets["Swamp"]["Brigde"+str(i)] =  {"Animation" : t, "Symbol": "b"+str(i)}
    i+= 1
