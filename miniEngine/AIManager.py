import pygame
from pyGraph import *
from SteeringBehaviours import *
from MapManager import *

class GraphManager:
    def __init__(self):
        graphs = {}

    def addGraph(self, graph, tag):
        self.graphs[tag] = graph

    def AStar(self, tagGraph, init, end, heuristic = 0):
        self.graphs[tag].AStar(init,end, heuristic)
        

class SwarmManager:
    def __init__(self):
        swarms = {}

    def addSwarm(self, lEntity, tag):
        self.swarms[tag] = lEntity

    def update(self):
        lSwarms = self.swarms.values()
        for s in lSwarms:
            self.updateSwarm(s)

class ArtificialIntelligenceManager:
    def __init__(self):
        self.mSwarmManager =  SwarmManager()

    def update(self):
        self.mSwarmManager.update()
