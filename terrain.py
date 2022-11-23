from classdec import *
from helper import *

def testRectTerrain(x1,y1,x2,y2,terrainList):
    terrainList.append(rectTerrain(x1,y1,x2,y2))
def testCircularTerrain(x,y,r,terrainList):
    terrainList.append(circularTerrain(x,y,r))

def checkTerrain(character,terrainList):
    #return values: 1 if character is on terrain's left edge, 2 if on right edge, 3 if on top edge, 4 if on bottom edge
    #circular terrain: 5 for lower-right, 6 for upper-right, 7 for lower-left, 8 for upper-left
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
        if isinstance(terrain,circularTerrain):
            dx=character.x-terrain.x
            dy=character.y-terrain.y
            dist=distance(character.x,character.y,terrain.x,terrain.y)
            mindist=character.radius+terrain.r
            if dx>0 and dy>0 and dist<mindist:
                return 5
            elif dx>0 and dy<0 and dist<mindist:
                return 6
            elif dx<0 and dy>0 and dist<mindist:
                return 7
            elif dx<0 and dy<0 and dist<mindist:
                return 8
            elif dx==0 and dy>0 and dist<mindist:
                return 4
            elif dx==0 and dy<0 and dist<mindist:
                return 3
            elif dx>0 and dy==0 and dist<mindist:
                return 2
            elif dx<0 and dy==0 and dist<mindist:
                return 1
    return 0

def drawTerrain(app,canvas):
    for terrain in app.terrainList:
        if isinstance(terrain,rectTerrain):
            canvas.create_rectangle(terrain.x1,terrain.y1,terrain.x2,terrain.y2,
            fill="white",outline="black")
        elif isinstance(terrain,circularTerrain):
            canvas.create_oval(terrain.x-terrain.r,terrain.y-terrain.r,
            terrain.x+terrain.r,terrain.y+terrain.r,fill="white",outline="black")

