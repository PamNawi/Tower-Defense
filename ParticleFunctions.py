#On this file is defined the funtions for particles:
from math import *
import sys
sys.path.insert(0, './/miniEngine/')
from Vector2D import *

def sum(dicParams):
    p = dicParams["Particle"]
    velocity = dicParams["Velocity"]
    p.position += Vec2d(velocity, velocity)
    return dicParams


def spin(dicParams):
    p           = dicParams["Particle"]
    cVelocity   = dicParams["CenterVelocity"]
    cPosition   = dicParams["CenterPosition"]
    angle       = dicParams["Angle"]
    radius      = dicParams["Radius"]
    step        = dicParams["Step"]
    dispersion  = dicParams["Dispersion"]

    dicParams["CenterPosition"] += dicParams["CenterVelocity"]
    x = sin(angle) * radius + cPosition.x
    y = cos(angle) * radius + cPosition.y

    p.setPosition(x,y)

    dicParams["Angle"] += dicParams["Step"]
    dicParams["Dispersion"] += -1

    if(dicParams["Dispersion"] <= 0):
        p.disposable = True
    return dicParams

def cascate(dicParams):
    p           = dicParams["Particle"]
    velocity    = dicParams["Velocity"]
    
    p.setPosition(p.position.x,p.position.y+ velocity)

    
    dicParams["Dispersion"] += -1
    if(dicParams["Dispersion"] <= 0):
        p.disposable = True
    return dicParams
