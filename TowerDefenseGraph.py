from Load import *

class TowerDefenseGraph(GraphFromMap):
    def __init__(self):
        GraphFromMap.__init__(self)
        self.verticeWeight = {}
        self.verticeDeaths = {}
        self.heuristic = self.nawiDistance


    def addVertice(self,node):
        GraphFromMap.addVertice(self,node)
        self.verticeWeight[node] = 0
        self.verticeDeaths[node] = 0

    def changeWeight(self,node, weight):
        self.verticeWeight[node] = weight

    def addWeightNode(self,node, weight):
        self.verticeWeight[node] += weight

    def addDeath(self,node):
        self.verticeDeaths[node] += 100

    def nawiDistance(self, start, goal):
        d = self.manhattanDistance(start, goal)
        w = self.verticeWeight[start] + self.verticeDeaths[start]
        return d * w
        
        
