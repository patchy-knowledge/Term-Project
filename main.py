from cmu_112_graphics import *
from classdec import *
from bullet import *
from helper import *
from terrain import *
from powerup import *
from time import *

#art assets are from Touhou 8: Imperishable Night
#retrieved from https://www.spriters-resource.com/download/34544/
#and https://en.touhouwiki.net/wiki/Category:Imperishable_Night_Images

def appStarted(app):
    app.timerDelay=10
    app.timePassed=0
    app.bulletList=[]
    app.playerBulletList=[]
    app.enemyList=[]
    app.powerupList=[]
    app.terrainList=[]
    app.character=Player(6,"Yuyuko",300,590,5)
    app.isFocus=False
    app.mode="Start"
    app.cleared=True
    app.scroll=0
    app.enemy=None
    app.keyHoldDict=dict()
    app.keyHoldDict["Up"]=False
    app.keyHoldDict["Down"]=False
    app.keyHoldDict["Left"]=False
    app.keyHoldDict["Right"]=False
    app.score=0
    app.pattern2gen=False
    app.grazeCount=0
    app.pattern2start=None
    app.stage=1
    app.initialized=False
    loadImage(app)

def loadImage(app):
    app.characterImage=app.loadImage('Yuyuko_char.png')
    app.cachedCharacterImage=ImageTk.PhotoImage(app.characterImage)
    app.enemyImage=app.loadImage('Reimu_enemy.png')
    app.cachedEnemyImage=ImageTk.PhotoImage(app.enemyImage)
    app.enemyBulletImage=app.loadImage('Reimu_shot.png')
    app.cachedEnemyBulletImage=ImageTk.PhotoImage(app.enemyBulletImage)
    app.stageBackground=app.loadImage('Stage_Background_Alt.png')
    app.playerBulletImage=app.loadImage('Yuyuko_shot.png')
    app.cachedPlayerBulletImage=ImageTk.PhotoImage(app.playerBulletImage)
    app.PowerIcon=app.loadImage('Power.png')
    app.ExtendIcon=app.loadImage('Extend.png')
    app.InvincibleIcon=app.loadImage('Invincible.png')
    app.TrackIcon=app.loadImage('Track.png')
    app.BombIcon=app.loadImage('Bomb.png')
    app.cachedPower=ImageTk.PhotoImage(app.PowerIcon)
    app.cachedExtend=ImageTk.PhotoImage(app.ExtendIcon)
    app.cachedInvincible=ImageTk.PhotoImage(app.InvincibleIcon)
    app.cachedTrack=ImageTk.PhotoImage(app.TrackIcon)
    app.cachedBomb=ImageTk.PhotoImage(app.BombIcon)
    app.terrainImage=app.loadImage("Rock_img.png")
    app.cachedTerrain=ImageTk.PhotoImage(app.terrainImage)

def checkMovements(app):
    cx=app.character.x
    cy=app.character.y
    if app.keyHoldDict["Up"] and checkTerrain(app.character,app.terrainList) not in (4,5,7) and not cy<0:
        if app.isFocus:
            app.character.y-=0.3*app.character.speed
        else:
            app.character.y-=app.character.speed
    if app.keyHoldDict["Down"] and checkTerrain(app.character,app.terrainList) not in (3,6,8) and not cy>app.height:
        if app.isFocus:
            app.character.y+=0.3*app.character.speed
        else:
            app.character.y+=app.character.speed
    if app.keyHoldDict["Left"] and checkTerrain(app.character,app.terrainList) not in (2,5,6) and not cx<0:
        if app.isFocus:
            app.character.x-=0.3*app.character.speed
        else:
            app.character.x-=app.character.speed
    if app.keyHoldDict["Right"] and checkTerrain(app.character,app.terrainList) not in (1,7,8) and not cx>0.75*app.width:
        if app.isFocus:
            app.character.x+=0.3*app.character.speed
        else:
            app.character.x+=app.character.speed

def terrainTick(app):
    if app.timePassed%1000==0:
        for terrain in app.terrainList:
            terrain.y+=50
    cleanTerrain(app)
    if len(app.terrainList)==0:
        app.terrainList.append(circularTerrain(random.randint(100,500),random.randint(150,300),100))

def characterTick(app):
    if app.character.timer is not None:
        if app.character.timer<=0:
            if app.character.isInvincible:
                app.character.isInvincible=False
            app.character.timer=None
        else:
            app.character.timer-=app.timerDelay

def bulletTick(app):
    for Bullet in app.bulletList:
        if not Bullet.freeze:
            dx,dy=polar2cart(Bullet.direction,Bullet.speed)
            Bullet.x+=dx
            Bullet.y+=dy
        if not app.character.isInvincible:
            if checkCollision(app.character,Bullet,app):
                app.character.life-=1
                app.character.invincible=True
                app.character.timer=2000
                if app.character.life==0:
                    app.mode="end"
        if checkGraze(app.character,Bullet) and not Bullet.grazed:
            Bullet.grazed=True
            app.grazeCount+=1
        if Bullet.timer is not None:
            if Bullet.timer<=0:
                if Bullet.freeze:
                    Bullet.freeze=False
                Bullet.timer=None
            else:
                Bullet.timer-=app.timerDelay

def enemyTick(app):
    if app.enemy.health<=0:
        app.enemy=None
    if app.enemy is not None:
        if app.enemy.x<100:
            if 10<app.enemy.y<100:
                app.enemy.direction=80
            elif app.enemy.y<10:
                app.enemy.direction=45
            else:
                app.enemy.direction=-45
        elif app.enemy.x>500:
            if 10<app.enemy.y<100:
                app.enemy.direction=100
            elif app.enemy.y<10:
                app.enemy.direction=135
            else:
                app.enemy.direction=-135
        if app.enemy.y<10:
            if 100<app.enemy.x<500:
                app.enemy.direction=10
        elif app.enemy.y>100:
            if 100<app.enemy.x<500:
                app.enemy.direction=190
        newDir=random.randint(app.enemy.direction-5,app.enemy.direction+5)
        app.enemy.direction=newDir
        dx,dy=polar2cart(app.enemy.direction,app.enemy.speed)
        app.enemy.x+=dx
        app.enemy.y+=dy

def playerBulletTick(app):
    for playerBullet in app.playerBulletList:
        if app.enemy is not None:
            checkEnemyCollision(app.enemy,playerBullet,app.playerBulletList,app)
            if playerBullet.tracking:
                dx1=app.enemy.x-playerBullet.x
                dy1=app.enemy.y-playerBullet.y
                theta=cart2polar(dx1,dy1)[0]
                if theta<0:
                    playerBullet.direction=theta
                else:
                    playerBullet.direction=180+theta
        dx,dy=polar2cart(playerBullet.direction,playerBullet.speed)
        playerBullet.x+=dx
        playerBullet.y+=dy

def powerupTick(app):
    cleanPowerup(app)
    if len(app.powerupList)<=3:
        if app.timePassed%2500==0:
            if randgen(25):
                app.powerupList.append(powerup(random.randint(50,550),0,random.randint(2,4),"Power"))
        if app.timePassed%5000==0:
            if randgen(30):
                app.powerupList.append(powerup(random.randint(50,550),0,random.randint(2,4),"Extend"))
            if randgen(25):
                app.powerupList.append(powerup(random.randint(50,550),0,random.randint(2,4),"Track"))
        if app.timePassed%3000==0:
            if randgen(30):
                app.powerupList.append(powerup(random.randint(50,550),0,random.randint(2,4),"Bomb"))
        if app.timePassed%6000==0:
            if randgen(30):
                app.powerupList.append(powerup(random.randint(50,550),0,random.randint(2,4),"Invincible"))
    for Powerup in app.powerupList:
        Powerup.y+=Powerup.speed
        checkPowerupPickup(Powerup,app)
        
def drawPowerups(app,canvas):
    for powerup in app.powerupList:
        if powerup.type=="Invincible":
            canvas.create_image(powerup.x,powerup.y,image=app.cachedInvincible)
        elif powerup.type=="Bomb":
            canvas.create_image(powerup.x,powerup.y,image=app.cachedBomb)
        elif powerup.type=="Track":
            canvas.create_image(powerup.x,powerup.y,image=app.cachedTrack)
        elif powerup.type=="Extend":
            canvas.create_image(powerup.x,powerup.y,image=app.cachedExtend)
        elif powerup.type=="Power":
            canvas.create_image(powerup.x,powerup.y,image=app.cachedPower)

def drawScore(app,canvas):
    canvas.create_text(650,50,font='Arial 20',text=f"Score\n {app.score}")
    canvas.create_text(650,150,font='Arial 20',text=f"Graze\n {app.grazeCount}")
    canvas.create_text(650,250,font='Arial 20',text=f"Life\n {app.character.life}")
    canvas.create_text(650,350,font='Arial 20',text=f"Bomb\n {app.character.bomb}")

def drawTerrain(app,canvas):
    for terrain in app.terrainList:
        if isinstance(terrain,rectTerrain):
            pass
        elif isinstance(terrain,circularTerrain):
            canvas.create_image(terrain.x,terrain.y,image=app.cachedTerrain)

def drawCharacters(app,canvas):
    canvas.create_image(app.character.x,app.character.y,image=app.cachedCharacterImage)
    canvas.create_oval(app.character.x-app.character.radius,app.character.y-app.character.radius,
    app.character.x+app.character.radius,app.character.y+app.character.radius,fill="white")
    if app.enemy is not None:
        canvas.create_image(app.enemy.x,app.enemy.y,image=app.cachedEnemyImage)

def drawBullets(app,canvas):
    for bullet in app.bulletList:
        canvas.create_image(bullet.x,bullet.y,image=app.cachedEnemyBulletImage)
    for playerBullet in app.playerBulletList:
        canvas.create_image(playerBullet.x,playerBullet.y,image=app.cachedPlayerBulletImage)

def stage1(app):
    if app.timePassed<15000:
        if app.timePassed%100==0:
            randomBullet(app,2,5,1,114)
    elif 15000<=app.timePassed<=15050: 
        app.enemy=Enemy(2,"Hakurei Reimu",191981,300,50,10)
    elif app.timePassed>15050:
        if app.enemy is not None:
            if app.timePassed%100==0:
                bossBullet(app,3,5,5,114514)
            if 20000<=app.timePassed<=23000:
                if app.timePassed%600==0:
                    pattern1(app.enemy.x,app.enemy.y,5,5,2,1,1000,random.randint(-10,10),app)
            if 23000<app.timePassed<30000:
                if app.timePassed%75==0:
                    bossBullet(app,3,5,5,114514)
            if 30000<=app.timePassed<=35000:
                if app.pattern2start==None:
                    app.pattern2start=app.timePassed
                    app.pattern2gencount=0
                    app.xyList=[]
                    for i in range(10):
                        app.xyList.append((100+i*40+random.randint(-10,10),100+random.randint(-20,20)))
                pattern2(app,app.xyList,5,90,5,1,114,100,50)
        else:
            #reset stage
            app.stage=2
            app.timePassed=0
            app.pattern2start=None
            app.initialized=False

def stage2(app):
    if not app.initialized:
        app.enemyImage=app.loadImage('Marisa_enemy.png')
        app.enemyBulletImage=app.loadImage('Marisa_shot.png')
        app.cachedEnemyImage=ImageTk.PhotoImage(app.enemyImage)
        app.cachedEnemyBulletImage=ImageTk.PhotoImage(app.enemyBulletImage)
    if app.timePassed<20000:
        if app.timePassed%75==0:
            randomBullet(app,4,4,10,114514)
    elif 20000<app.timePassed<20050:
        app.enemy=Enemy(3,"Kirisame Marisa",114514,300,50,10)
    elif app.timePassed>20050:
        if app.enemy is not None:
            if app.timePassed%66==0:
                bossBullet(app,4,4,5,114514)
            if 23000<app.timePassed<30000:
                if app.pattern2start is None:
                    app.pattern2start=app.timePassed
                    app.pattern2gencount=0
                    app.xyList=[]
                    for i in range(15):
                        app.xyList.append((100+random.randint(-20,20),40*i))
                pattern2(app,app.xyList,3,0,4,1,1000,100,50)
                if app.timePassed%500==0:
                    pattern1(app.enemy.x,app.enemy.y,3,4,3,1,1000,random.randint(-20,20),app)
        else:
            #reset stage
            app.stage=3
            app.timePassed=0
            app.pattern2start=None
            app.initialized=False

def stage3(app):
    if not app.initialized:
        app.enemyImage=app.loadImage('Tenshi_enemy.png')
        app.enemyBulletImage=app.loadImage('Tenshi_shot.png')
        app.cachedEnemyImage=ImageTk.PhotoImage(app.enemyImage)
        app.cachedEnemyBulletImage=ImageTk.PhotoImage(app.enemyBulletImage)
    if app.timePassed<15000:
        if app.timePassed%66==0:
            randomBullet(app,2,5,1,1145)
        elif 15000<=app.timePassed<=15050:
            app.enemy=Enemy(1.5,"Hinanawi Tenshi",198893,300,50,10)
        elif app.timePassed>15050:
            if app.enemy is not None:
                if app.timePassed%50==0:
                    bossBullet(app,3,5,5,1145)
                if 20000<app.timePassed<25000 or 30000<app.timePassed<35000:
                    if app.pattern2start is None:
                        app.pattern2start=app.timePassed
                        app.pattern2gencount=0
                        app.xyList=[]
                        for i in range(15):
                            app.xyList.append((30+35*i+random.randint(-10,10),100))
                    pattern2(app,app.xyList,2,90,5,10,114,150,50)
                    if app.timePassed%400==0:
                        pattern1(app.enemy.x,app.enemy.y,2.5,5,2,10,100,random.randint(-10,10),app)
        else:
            #ends
            app.mode="End"
            
def Start_redrawAll(app,canvas):
    canvas.create_text(300,300,font="Helvetica", text="Press any key to start")

def Start_keyPressed(app,event):
    app.mode="Game"

def Game_redrawAll(app,canvas):
    canvas.create_image(300,300,image=ImageTk.PhotoImage(app.stageBackground))
    drawTerrain(app,canvas)
    drawCharacters(app,canvas)
    if app.enemy is not None:
        canvas.create_text(300,50,font="Arial 26", text=app.enemy.health)
    drawBullets(app,canvas)
    drawScore(app,canvas)
    drawPowerups(app,canvas)

def Game_keyPressed(app,event):
    if event.key=="Space":
        app.character.isFiring=not app.character.isFiring
    if event.key=="z":
        app.isFocus=not app.isFocus
    if event.key=="f":
        freeze(app,app.character.x,app.character.y-80,80)
    if event.key=="x":
        bomb(app)
    if event.key in ("Up","Down","Left","Right"):
        app.keyHoldDict[event.key]=True
        
def Game_keyReleased(app,event):
    if event.key in ("Up","Down","Left","Right"):
        app.keyHoldDict[event.key]=False
        
def Game_timerFired(app):
    app.timePassed+=app.timerDelay
    if app.enemy is not None:
        enemyTick(app)
    checkMovements(app)
    if app.character.isFiring:
        firePlayerBullet(app.character.canTrack,app)
    characterTick(app)
    powerupTick(app)
    bulletTick(app)
    playerBulletTick(app)
    terrainTick(app)
    clean(app,app.bulletList,app.playerBulletList) 
    if app.stage==1:
        stage1(app)
    elif app.stage==2:
        stage2(app)
    elif app.stage==3:
        stage3(app)
    print(app.timePassed)
runApp(height=600,width=800)
    
