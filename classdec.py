import cmu_112_graphics

class generic:
    def __init__(self,speed,health,x,y,radius):
        self.speed=speed
        self.health=health
        self.x=x
        self.y=y
        self.radius=radius
#performs a move in specified distance
    def moveX(self,magnitude):
        self.x+=magnitude
    
    def moveY(self,magnitude):
        self.y+=magnitude

#get functions

class Player(generic):
    #type of shotPattern and spellPattern should be int
    def __init__(self,speed,name,x,y,radius,shotPattern,spellPattern):
        #player's health is defaulted to 1 to ensure death upon impact
        super().__init__(speed,1,x,y,radius)
        self.name=name
        self.shotPattern=shotPattern
        self.spellPattern=spellPattern

class Enemy(generic):
    #enemies do not have spells
    def __init__(self,speed,name,health,x,y,radius,shotPattern):
        super().__init__(speed,health,x,y,radius)
        self.name=name
        self.shotPattern=shotPattern

class bullet:
    #direction is specified as angle in degrees: up/down=0/180, horizontal left/right=-+90
    def __init__(self,x,y,speed,direction,radius,damage,lifetime):
        self.x=x
        self.y=y
        self.speed=speed
        self.direction=direction
        self.radius=radius
        self.damage=damage
        self.lifetime=lifetime
        self.freeze=False
        self.age=0
    
    def freeze(self):
        self.freeze=True
    
    def unFreeze(self):
        self.freeze=False

class playerShot(bullet):
    pass

class enemyShot(bullet):
    pass