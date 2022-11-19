from classdec import *
from helper import *

terrainList=[]

def testRectTerrain(x1,y1,x2,y2):
    terrainList.append(rectTerrain(x1,y1,x2,y2))
def testCircularTerrain(x,y,r):
    terrainList.append(circularTerrain(x,y,r))

def checkTerrain(character):
    #return values: 1 if character is on terrain's left edge, 2 if on right edge, 3 if on top edge, 4 if on bottom edge
    #return 0 if not in contact with terrain
    for terrain in terrainList:
        if isinstance(terrain,rectTerrain):
            if delta(terrain.x1,character.x)<=5 and terrain.y1<=character.y<=terrain.y2:
                return 1
            elif delta(terrain.x2,character.x)<=5 and terrain.y1<=character.y<=terrain.y2:
                return 2
            elif delta(terrain.y1,character.y)<=5 and terrain.x1<=character.x<=terrain.x2:
                return 3
            elif delta(terrain.y2,character.y)<=5 and terrain.x1<=character.x<=terrain.x2:
                return 4
        #not done yet
        """elif isinstance(terrain,circularTerrain):
            dx=character.x-terrain.x
            dy=character.y-terrain.y
            dist=distance(character.x,character.y,terrain.x,terrain.y)
            mindist=character.radius+terrain.r
            if -45<=cart2polar(dx,dy)<45 and dist<=mindist:
                return 2
            elif """
    return 0

