from pyGraph import *

class GraphFromMap(Graph):
    def __init__(self):
        Graph.__init__(self)
        self.map = []
        self.walkable = []

    def loadGrid(self,nLayers, tamI, tamJ):
        self.map = [[["0"]*tamJ]*tamI]*nLayers
        self.loadGraph()

    def loadGraph(self, tileWidth, tileHeigth):
        k = 0
        for layer in self.map:
            i = 0
            for linha in layer:
                j = 0
                for coluna in linha:
                    self.addVertice(self.convertToScreenPosition((k,i,j)))
                    #verifica se e possivel andar nos vizinhos se sim anda neles
                    ''' 
                    0   v1  0
                    v2  v   v3
                    0   v4  0
                    '''
                    if(self.isWalkable(k,i,j)):
                        #v1
                        if(self.isWalkable(k,i-1,j)):
                           self.addEdge(self.convertToScreenPosition((k,i,j)),self.convertToScreenPosition((k,i-1,j)))
                        #v2
                        if(self.isWalkable(k,i, j-1)):
                            self.addEdge(self.convertToScreenPosition((k,i,j)),self.convertToScreenPosition((k,i,j-1)))
                        #v3
                        if(self.isWalkable(k,i, j+1)):
                            self.addEdge(self.convertToScreenPosition((k,i,j)),self.convertToScreenPosition((k,i,j+1)))
                        #v4
                        if(self.isWalkable(k,i+1,j)):
                            self.addEdge(self.convertToScreenPosition((k,i,j)),self.convertToScreenPosition((k,i+1,j)))
                        #v5
                        if(self.isWalkable(k-1,i,j)):
                            self.addEdge(self.convertToScreenPosition((k,i,j)),self.convertToScreenPosition((k-1,i,j)))
                        #v6
                        if(self.isWalkable(k+1,i,j)):
                            self.addEdge(self.convertToScreenPosition((k,i,j)),self.convertToScreenPosition((k+1,i,j)))                        
                    j += 1
                i+= 1
            k += 1        
        
    def loadGraphFromMaps(self, lMaps, tileWidth, tileHeigth):
        self.loadMaps(lMaps)
        self.tileWidth = tileWidth
        self.tileHeigth = tileHeigth
        self.loadGraph(tileWidth, tileHeigth)

    def isWalkable(self, layer, i, j):
        nLayers = len(self.map)-1
        
        if(layer >= 0 and layer <= nLayers):
            nLines = len(self.map[layer])
            if( i >= 0 and i < nLines):
                nCols = len(self.map[layer][i])
                if(j >= 0 and j < nCols and self.map[layer][i][j] in self.walkable):
                    return True
        return False        

    def loadMaps(self,lMaps):
        self.map = []
        for layer in lMaps:
            self.map += [self.loadLayer(layer)]

    def loadLayer(self, fileMap):
        f = open(fileMap).read().split('\n')
        i = 0
        layer = []
        for line in f:
            j = 0
            l = line.split('\t')
            layer += [l]
        return layer

    def convertToScreenPosition(self,node):
        return (node[0], node[2] * self.tileWidth, node[1] *self.tileHeigth)
        
