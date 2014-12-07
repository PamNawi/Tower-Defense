from Entity import *

class Particle(Entity):
    def __init__(self,surface = None, position = Vec2d(0,0), updateFunction = None, updateFunctionParams = (0,0) ):
        self.surface = surface
        self.position = position
        self.updateFunction = updateFunction
        self.updateFunctionParams = updateFunctionParams
        self.disposable = True
        self.tag = "Particle"

    def update(self):
        self.updateFunctionParams = self.updateFunction(self.updateFunctionParams)

    def createParticle(self, surface, position, updateFunction, dicFunctionParams):
       self.surface = surface
       self.position = position
       self.updateFunction = updateFunction
       self.updateFunctionParams = dicFunctionParams
       self.updateFunctionParams["Particle"] = self
       self.disposable = False

class ParticleManager:
    def __init__(self, nParticles = 1000):
        self.notUsedParticles = []
        self.particles = []
        for i in range(nParticles):
            self.notUsedParticles += [Particle()]

        self.updateFunctions = {}

    def addUpdateFunction(self, surface, aniSpeed, func, tag, paramsFunc = None):
        self.updateFunctions[tag] = (Animation(surface, aniSpeed),func, paramsFunc)

    def update(self):
        i = 0
        for p in self.particles:
            p.update()
            if p.disposable == True:
                self.notUsedParticles.append(p)
                self.particles.remove(p)
            i += 1
            

    def createParticle(self, position, tag, params = None):
        #Get one particle in not used or the first in the used
        #simulating something like a circular list
        p = self.getNextParticle()
        if(params == None):
            p.createParticle(self.updateFunctions[tag][0],position,self.updateFunctions[tag][1],self.updateFunctions[tag][2])
        else:
            p.createParticle(self.updateFunctions[tag][0],position,self.updateFunctions[tag][1],params)

        #put this particle on live particles
        self.particles.append(p)
        #print self.particles
        
    def getParticles(self):
        return self.particles

    def getNextParticle(self): 
        if(self.notUsedParticles):
            return self.notUsedParticles.pop()
        else:
            return self.particles.pop(0)

'''p = ParticleManager()
p.addUpdateFunction(0,sum,"sum",[1])
p.createParticle((0,0),"sum")
while(1):
    p.update()'''
