import cmu_112_graphics

class generic:
    def __init__(self,speed,health,x,y,radius):
        self.speed=speed
        self.health=health
        self.x=x
        self.y=y
        self.radius=radius
        self.isInvincible=False
#performs a move in specified distance
    def moveX(self,magnitude):
        self.x+=magnitude
    
    def moveY(self,magnitude):
        self.y+=magnitude

class Player(generic):
    #type of shotPattern and spellPattern should be int
    def __init__(self,speed,name,x,y,radius,shotPattern,spellPattern):
        #player's health is defaulted to 1 to ensure death upon impact
        super().__init__(speed,1,x,y,radius)
        self.name=name
        self.shotPattern=shotPattern
        self.spellPattern=spellPattern
        self.timer=0
        self.canTrack=False
        self.power=1
        self.isFiring=False
        self.isInvincible=False

class Enemy(generic):
    #enemies do not have spells
    def __init__(self,speed,name,health,x,y,radius,shotPattern):
        super().__init__(speed,health,x,y,radius)
        self.name=name
        self.shotPattern=shotPattern
        self.direction=0

class bullet:
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
        self.grazed=False
    
    def freeze(self):
        self.freeze=True
    
    def unFreeze(self):
        self.freeze=False

class playerShot(bullet):
    def __init__(self,x,y,speed,direction,radius,damage,lifetime,tracking):
        super().__init__(x,y,speed,direction,radius,damage,lifetime)
        self.tracking=tracking

class enemyShot(bullet):
    pass

class rectTerrain:
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2

class circularTerrain:
    def __init__(self,x,y,r):
        self.x=x
        self.y=y
        self.r=r

class powerup:
    def __init__(self,x,y,speed,powertype):
        self.x=x
        self.y=y
        self.speed=speed
        self.r=15
        self.type=powertype