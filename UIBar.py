from Load import *

class Bar(Entity):
    def __init__(self, maxMiddle):
        Entity.__init__(self)

        self.start = Entity()
        self.end = Entity()
        self.middle = []
        self.maxMiddle = maxMiddle
        for i in range(maxMiddle):
            self.middle += [ Entity()]

        #Wmiddle = width of the middle bar
        self.wMiddle = 1

        tag = "Bar"

    def setPosition(self,position):
        Entity.setPosition(self,position)
        self.start.setPosition(position)

        desloc = 0
        for i in self.middle:
            i.setPosition(Vec2d(position[0]+desloc*self.wMiddle,position[1]))
            desloc += 1
        desloc +=1
        self.end.setPosition(position[0] + self.wMiddle * desloc, position[1])

    def setAnimation(self, startTag, endTag, middleTag):
        mE.mAnimationManager.setEntityAnimation(self.start, startTag)
        mE.mAnimationManager.setEntityAnimation(self.end, endTag)

        for i in self.middle:
            mE.mAnimationManager.setEntityAnimation(i, middleTag)

def addBarToEntityManager(bar):
    global mE
    mE.mEntityManager.addEntity(bar.start,  bar.tag+"Start",  "UI")
    mE.mEntityManager.addEntity(bar.end,    bar.tag+"End",    "UI")

    for i in bar.middle:
        mE.mEntityManager.addEntity(i,      bar.tag+"Middle", "UI")

    mE.mEntityManager.addEntity(bar,        bar.tag, "UI")
    
def removeBarFromEntityManager(bar):
    global mE
    mE.mEntityManager.removeEntity(bar.start,   bar.tag+"Start")
    mE.mEntityManager.removeEntity(bar.end,     bar.tag+"End")

    for i in self.middle:
        mE.mEntityManager.removeEntity(i,       bar.tag+"Middle")

    mE.mEntityManager.removeEntity(bar, bar.tag)
        
