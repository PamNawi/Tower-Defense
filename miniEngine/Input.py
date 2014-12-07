import pygame
from Vector2D import *

class Mouse:
    def __init__(self):
        self.position = (0,0)
        self.buttonPress = {}
        self.buttonPress["LEFT"] = False
        self.buttonPress["CENTER"] = False
        self.buttonPress["RIGHT"] = False

    def getPosition(self):
        return Vec2d( self.position[0], self.position[1])

    def isPressed(self, button):
        if(self.buttonPress[button] == True):
            return True
        return False

    def update(self, position, buttonState):
        self.position = position
        self.buttonPress["LEFT"] = buttonState[0]
        self.buttonPress["CENTER"] = buttonState[1]
        self.buttonPress["RIGHT"] = buttonState[2]
    
class Keyboard:
    def __init__(self):
        self.key = []

    def isPressed(self,key):
        if(self.key[key] != 0):
            return True
        return False

    def update(self,keyState):
        self.key = keyState
        #print self.key
