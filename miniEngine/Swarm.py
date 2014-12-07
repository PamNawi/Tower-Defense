from SteeringBehaviours import *

class Swarm:
    def __init__(self, wAlignment = 0.0 , wCohesion = 0.0, wSeparation = 0.0, radiusNeighborhood = 75):
        self.lEntitys = []
        self.wAlignment = wAlignment
        self.wCohesion = wCohesion
        self.wSeparation = wSeparation
        self.radiusNeighborhood = radiusNeighborhood

        self.wSwarmForce = 1.0

    def addSteeringEntity(self, entity):
        self.lEntitys += [ entity]

    def update(self):
        for e in self.lEntitys:
            neighbors = self.getNeighborhood(e)
            e.swarmForce = Vec2d(0,0)
            e.swarmForce += self.wAlignment     * self.computeAlignment(e,neighbors)
            e.swarmForce += self.wCohesion      * self.computeCohesion(e,neighbors)
            e.swarmForce += self.wSeparation    * self.computeSeparation(e,neighbors)

    def computeAlignment(self, entity, neighbors):
        v = Vec2d(0,0)
        neighborCount = len(neighbors);
        if(neighborCount > 0):
            for e in neighbors:
                v += e.velocity
            v = v * (1/neighborCount)
            v.normalized()
        return v        

    def computeCohesion(self, entity, neighbors):
        v = Vec2d(0,0)
        neighborCount = len(neighbors)
        if(neighborCount > 0 ):
            for e in neighbors:
                v += e.position
            v = v *(1/neighborCount)
            v = Vec2d(v[0] - entity.position[0], v[1] - entity.position[1]).normalized()
        return v
    
    def computeSeparation(self, entity, neighbors):
        v = Vec2d(0,0)
        neighborCount = len(neighbors)
        if(neighborCount > 0 ):
            for e in neighbors:
                v += entity.position - e.position
            v = v * (1/neighborCount) * -1
            v = v.normalized()
        return v

    def getNeighborhood(self, entity):
        neighbors = []
        for e in self.lEntitys:
            if(e != entity):
                if(distanceEntity(e,entity) < self.radiusNeighborhood):
                    neighbors += [e]
        return neighbors


class SwarmManager:
    def __init__(self):
        self.swarms = {}

    def addSwarm(self, swarm, tag):
        self.swarms[tag] = swarm

    def update(self):
        lSwarms = self.swarms.values()
        for s in lSwarms:
            s.update()
