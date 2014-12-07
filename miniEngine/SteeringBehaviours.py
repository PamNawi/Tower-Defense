from Vector2D import *
from ESTManager import *
import random

class SteeringEntity(Entity):
    def __init__(self, maxVelocity = 5, mass = 1 ):
        Entity.__init__(self)
        self.force = Vec2d(0,0)
        self.aceleration = Vec2d(0,0)
        self.velocity = Vec2d(0,0)
        self.maxVelocity = maxVelocity
        self.mass = mass

        self.initSteeringValues()

    def initSteeringValues(self, slowingRadius = 10, wanderAngle = 1.0, wanderingRadius = 10, wanderingDistance = 10, angleChange = 5, ePursuit = Entity(), eEvade = Entity()):
        self.wSeek = 0.0
        self.wFlee = 0.0
        self.wArrival = 0.0
        self.wWander = 0.0
        self.wPursuit = 0.0
        self.wEvade = 0.0
        self.wSwarm = 1.0
        
        self.slowingRadius = slowingRadius

        self.wanderAngle = wanderAngle
        self.wanderingRadius = wanderingRadius
        self.wanderingDistance = wanderingDistance
        self.angleChange = angleChange
        
        self.targetPosition = Vec2d(400,300)
        self.runningPosition = Vec2d(200,200)
        self.ePursuit = ePursuit
        self.eEvade = eEvade


        self.swarmForce = Vec2d(0.0,0.0)

    def update(self):
        self.updateSteering();

    def updateSteering(self):
        self.force = (0,0)
        self.sumForces()
        self.aceleration = self.force * (1/self.mass)
        self.velocity = self.velocity + self.aceleration        
        self.velocity = self.velocity.normalized() * self.maxVelocity
        self.position = self.position + self.velocity

    def sumForces(self):
        self.force = self.wSeek         * self.Seek(self.targetPosition)
        self.force += self.wArrival     * self.Arrival(self.targetPosition)
        self.force += self.wFlee        * self.Flee(self.runningPosition)
        self.force += self.wWander      * self.Wander()
        self.force += self.wPursuit     * self.Pursuit(self.ePursuit)
        self.force += self.wEvade       * self.Evade(self.eEvade)
        self.force += self.wSwarm       * self.swarmForce
        
    
    def Seek(self, position):
        desired =  position - self.position
        desired.normalized()
        desired = desired * self.maxVelocity

        return desired - self.velocity

    def Flee(self, position):
        desired = self.position - position 
        desired.normalized()
        desired = desired * self.maxVelocity

        return desired - self.velocity

    def Arrival(self, position):
        desired = position - self.position;
        distance = desired.get_length()
        desired.normalized()

        if(distance <= self.slowingRadius):
            desired = desired * (self.maxVelocity * distance / self.slowingRadius)
        else:
            desired = desired * self.maxVelocity
        return desired - self.velocity

    def Wander(self):
        circleCenter = self.velocity
        circleCenter.normalized()
        circleCenter  = circleCenter  * self.wanderingDistance

        displacement = Vec2d(0,-1)
        displacement = displacement * self.wanderingRadius

        wanderAngle = self.setAngle(displacement,self.wanderAngle)
        wanderAngle += random.random() * self.angleChange - self.angleChange * 0.5;

        return circleCenter + displacement

    def Pursuit(self, e2):
        distance = e2.position - self.position
        updatesNeeded = distance.get_length() * (1/self.maxVelocity)
        tv = self.velocity
        tv = tv.normalized() * updatesNeeded
        return self.Seek(e2.position + tv)

    def Evade(self, e2):
        distance = e2.position - self.position
        updatesNeeded = distance.get_length() * (1/self.maxVelocity)
        tv = self.velocity
        tv = tv.normalized() * updatesNeeded
        return self.Flee(e2.position + tv)

    def setAngle(self, vector, value):
        lenght = vector.get_length()
        vector.x = math.cos(value) * lenght
        vector.y = math.sin(value) * lenght
        return vector

    def toString(self):
        s = ""
        s += "Force: "+str(self.force)
        s += "\nAceleration: "+ str(self.aceleration)
        s += "\nPosition: "+ str(self.position)
        return s
