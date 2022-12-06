from classdec import *
from bullet import *
from helper import *
from terrain import *
from powerup import *
from time import *
import pygame
import shelve
#art assets are from Touhou 8: Imperishable Night
#retrieved from https://www.spriters-resource.com/download/34544/
#and https://en.touhouwiki.net/wiki/Category:Imperishable_Night_Images

class app:
    pass
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
    app.enemy=None
    app.score=0
    app.pattern2gen=False
    app.grazeCount=0
    app.pattern2start=None
    app.stage=1
    app.initialized=False
    app.character.experience=114514
    pygame.init()
    pygame.display.init()
    app.screen=pygame.display.set_mode((800,600))

def loadImage(app):
    app.backgroundImage=pygame.image.load('Stage_Background_Alt.png').convert()
    app.playerImage=pygame.image.load('Yuyuko_char.png').convert()
    app.playerImage.set_colorkey((0,0,0))
    app.playerShotImage=pygame.image.load('Yuyuko_Shot.png').convert()
    app.playerShotImage.set_colorkey((0,0,0))
    app.enemyImage=pygame.image.load('Reimu_enemy.png').convert()
    app.enemyImage.set_colorkey((0,0,0))
    app.enemyShotImage=pygame.image.load('Reimu_shot.png').convert()
    app.enemyShotImage.set_colorkey((0,0,0))
    app.extendImage=pygame.image.load('Extend.png').convert()
    app.extendImage.set_colorkey((0,0,0))
    app.bombImage=pygame.image.load('Bomb.png').convert()
    app.bombImage.set_colorkey((0,0,0))
    app.powerImage=pygame.image.load('Power.png').convert()
    app.powerImage.set_colorkey((0,0,0))
    app.invincibleImage=pygame.image.load('Invincible.png').convert()
    app.invincibleImage.set_colorkey((0,0,0))
    app.trackImage=pygame.image.load('Track.png').convert()
    app.trackImage.set_colorkey((0,0,0))
    app.rockImage=pygame.image.load('Rock_img.png').convert()
    app.rockImage.set_colorkey((0,0,0))

def marketInit(app):
    app.marketExtend=2
    app.marketBomb=5
    app.trackCost=100
    app.bombCost=100
    app.extendCost=100
    app.powerCost=10
    app.marketMessage=""

def saveFile(app):
    savedGame=shelve.open("save")
    savedGame["timePassed"]=app.timePassed
    savedGame["score"]=app.score
    savedGame["graze"]=app.grazeCount
    savedGame["stage"]=app.stage
    savedGame["marketExtend"]=app.marketExtend
    savedGame["marketBomb"]=app.marketBomb
    savedGame["charAttr"]=app.character.getAttr()
    playerBulletAttr=[]
    for pBullet in app.playerBulletList:
        playerBulletAttr.append(pBullet.getAttr())
    bulletAttr=[]
    for bullet in app.bulletList:
        bulletAttr.append(bullet.getAttr())
    savedGame["playerBulletAttr"]=playerBulletAttr
    savedGame["bulletAttr"]=bulletAttr
    if app.enemy is not None:
        savedGame["enemyAttr"]=app.enemy.getAttr()
    else:
        savedGame["enemyAttr"]=None
    terrainAttr=[]
    for terrain in app.terrainList:
        terrainAttr.append(terrain.getAttr())
    savedGame["terrainAttr"]=terrainAttr
    powerupAttr=[]
    for powerup in app.powerupList:
        powerupAttr.append(powerup.getAttr())
    savedGame["powerupAttr"]=powerupAttr
    savedGame.close()

def readSaveFile(app):
    savedGame=shelve.open("save")
    app.timePassed=savedGame["timePassed"]
    app.score=savedGame["score"]
    app.grazeCount=savedGame["graze"]
    app.stage=savedGame["stage"]
    app.marketExtend=savedGame["marketExtend"]
    app.marketBomb=savedGame["marketBomb"]
    cspeed,cname,cx,cy,cr,cTrack,cPower,cInvincible,cLife,cBomb,cTimer,cExp=savedGame["charAttr"]
    app.character=Player(cspeed,cname,cx,cy,cr)
    app.character.canTrack=cTrack
    app.character.power=cPower
    app.character.isInvincible=cInvincible
    app.character.life=cLife
    app.character.bomb=cBomb
    app.character.timer=cTimer
    app.character.experience=cExp
    if savedGame["enemyAttr"] is not None:
        eSpeed,eName,ex,ey,er,eDir,eHealth=savedGame["enemyAttr"]
        app.enemy=Enemy(eSpeed,eName,eHealth,ex,ey,er)
        app.enemy.direction=eDir
    app.bulletList=[]
    for bulletAttr in savedGame["bulletAttr"]:
        if bulletAttr is not None:
            bx,by,bSpeed,bDir,br,bDamage,bLifetime,bFreeze,bGrazed,bTimer=bulletAttr
            newBullet=bullet(bx,by,bSpeed,bDir,br,bDamage,bLifetime)
            newBullet.freeze=bFreeze
            newBullet.grazed=bGrazed
            newBullet.timer=bTimer
        app.bulletList.append(newBullet)
    app.playerBullet=[]
    for pBulletAttr in savedGame["playerBulletAttr"]:
        if pBulletAttr is not None:
            px,py,pSpeed,pDir,pr,pDamage,pLifetime,pTrack=pBulletAttr
            newPBullet=playerShot(px,py,pSpeed,pDir,pr,pDamage,pLifetime,pTrack)
            app.playerBulletList.append(newPBullet)
    app.terrainList=[]
    for terrainAttr in savedGame["terrainAttr"]:
        if terrainAttr is not None:
            tx,ty,tr=terrainAttr
            app.terrainList.append(circularTerrain(tx,ty,tr))
    app.powerupList=[]
    for powerupAttr in savedGame["powerupAttr"]:
        if powerupAttr is not None:
            ux,uy,us,up=powerupAttr
            app.powerupList.append(powerup(ux,uy,us,up))
    savedGame.close()
    
def checkMovements(app):
    cx=app.character.x
    cy=app.character.y
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP] and checkTerrain(app.character,app.terrainList) not in (4,5,7) and not cy<0:
        if app.isFocus:
            app.character.y-=0.3*app.character.speed
        else:
            app.character.y-=app.character.speed
    if keys[pygame.K_DOWN] and checkTerrain(app.character,app.terrainList) not in (3,6,8) and not cy>600:
        if app.isFocus:
            app.character.y+=0.3*app.character.speed
        else:
            app.character.y+=app.character.speed
    if keys[pygame.K_LEFT] and checkTerrain(app.character,app.terrainList) not in (2,5,6) and not cx<0:
        if app.isFocus:
            app.character.x-=0.3*app.character.speed
        else:
            app.character.x-=app.character.speed
    if keys[pygame.K_RIGHT] and checkTerrain(app.character,app.terrainList) not in (1,7,8) and not cx>600:
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
        Bullet.lifetime-=app.timerDelay
        if Bullet.lifetime<=0:
            pattern1(Bullet.x,Bullet.y,3,5,3,1,114514,0,app)
            app.bulletList.remove(Bullet)
        if not Bullet.freeze:
            dx,dy=polar2cart(Bullet.direction,Bullet.speed)
            Bullet.x+=dx
            Bullet.y+=dy
        if not app.character.isInvincible:
            if checkCollision(app.character,Bullet,app):
                app.character.life-=1
                app.character.isInvincible=True
                app.character.timer=2000
                if app.character.life==0:
                    app.mode="End"
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
        
def drawPowerups(app):
    for powerup in app.powerupList:
        if powerup.type=="Invincible":
            app.screen.blit(app.invincibleImage,(powerup.x,powerup.y))
        elif powerup.type=="Bomb":
            app.screen.blit(app.bombImage,(powerup.x,powerup.y))
        elif powerup.type=="Track":
            app.screen.blit(app.trackImage,(powerup.x,powerup.y))
        elif powerup.type=="Extend":
            app.screen.blit(app.extendImage,(powerup.x,powerup.y))
        elif powerup.type=="Power":
            app.screen.blit(app.powerImage,(powerup.x,powerup.y))
    

def drawScore(app):
    font=pygame.font.SysFont(None,20)
    scoretext=f"Score: {app.score}\n Graze: {app.grazeCount}\n Life {app.character.life} {app.character.isInvincible}\n Bomb {app.character.bomb}\n Timers: {app.timePassed} {app.character.timer}\n"
    scoreObj=font.render(scoretext,True,(0,0,0))
    app.screen.blit(scoreObj,(700,300))

def drawTerrain(app):
    for terrain in app.terrainList:
        if isinstance(terrain,rectTerrain):
            pass
        elif isinstance(terrain,circularTerrain):    
            app.screen.blit(app.rockImage,(terrain.x-terrain.r,terrain.y-terrain.r))

def drawCharacters(app):
    offsetX=0.5*app.playerImage.get_width()
    offsetY=0.5*app.playerImage.get_height()
    app.screen.blit(app.playerImage,(app.character.x-offsetX,app.character.y-offsetY))
    pygame.draw.circle(app.screen,(255,255,255),(app.character.x,app.character.y),app.character.radius)
    if app.enemy is not None:
        app.screen.blit(app.enemyImage,(app.enemy.x,app.enemy.y))

def drawBullets(app):
    for bullet in app.bulletList:
        app.screen.blit(app.enemyShotImage,(bullet.x,bullet.y))
    for playerBullet in app.playerBulletList:
        app.screen.blit(app.playerShotImage,(playerBullet.x,playerBullet.y))

def stage1(app):
    if app.timePassed<15000:
        if app.timePassed%100==0:
            randomBullet(app,2,5,1,114514)
    elif 15000<=app.timePassed<=15050: 
        app.enemy=Enemy(2,"Hakurei Reimu",191981,300,50,10)
    elif app.timePassed>15050:
        if app.enemy is not None:
            if app.timePassed%100==0:
                bossBullet(app,3,5,5)
            if 20000<=app.timePassed<=23000:
                if app.timePassed%600==0:
                    pattern1(app.enemy.x,app.enemy.y,6,5,2,1,114514,random.randint(-10,10),app)
            if 23000<app.timePassed<30000:
                if app.timePassed%75==0:
                    bossBullet(app,3,5,5)
            if 30000<=app.timePassed<=35000:
                if app.pattern2start==None:
                    app.pattern2start=app.timePassed
                    app.pattern2gencount=0
                    app.xyList=[]
                    for i in range(10):
                        app.xyList.append((100+i*40+random.randint(-10,10),100+random.randint(-20,20)))
                pattern2(app,app.xyList,5,90,5,1,114514,100,50)
        else:
            #reset stage
            app.stage=2
            app.timePassed=0
            app.pattern2start=None
            app.initialized=False

def stage2(app):
    if not app.initialized:
        app.enemyImage=pygame.image.load('Marisa_enemy.png').convert()
        app.enemyShotImage=pygame.image.load('Marisa_shot.png').convert()
    if app.timePassed<20000:
        if app.timePassed%75==0:
            randomBullet(app,4,4,10,114514)
    elif 20000<app.timePassed<20050:
        app.enemy=Enemy(3,"Kirisame Marisa",114514,300,50,10)
    elif app.timePassed>20050:
        if app.enemy is not None:
            if app.timePassed%66==0:
                bossBullet(app,4,4,5)
            if 23000<app.timePassed<30000:
                if app.pattern2start is None:
                    app.pattern2start=app.timePassed
                    app.pattern2gencount=0
                    app.xyList=[]
                    for i in range(15):
                        app.xyList.append((100+random.randint(-20,20),40*i))
                pattern2(app,app.xyList,3,0,4,1,114514,100,50)
                if app.timePassed%500==0:
                    pattern1(app.enemy.x,app.enemy.y,5,4,3,1,114514,random.randint(-20,20),app)
        else:
            #reset stage
            app.stage=3
            app.timePassed=0
            app.pattern2start=None
            app.initialized=False

def stage3(app):
    if not app.initialized:
        app.enemyImage=pygame.image.load('Tenshi_enemy.png').convert()
        app.enemyShotImage=pygame.image.load('Tenshi_shot.png').convert()
    if app.timePassed<15000:
        if app.timePassed%66==0:
            randomBullet(app,2,5,1,114514)
        elif 15000<=app.timePassed<=15050:
            app.enemy=Enemy(1.5,"Hinanawi Tenshi",198893,300,50,10)
        elif app.timePassed>15050:
            if app.enemy is not None:
                if app.timePassed%50==0:
                    bossBullet(app,3,5,5)
                if 20000<app.timePassed<25000 or 30000<app.timePassed<35000:
                    if app.pattern2start is None:
                        app.pattern2start=app.timePassed
                        app.pattern2gencount=0
                        app.xyList=[]
                        for i in range(15):
                            app.xyList.append((30+35*i+random.randint(-10,10),100))
                    pattern2(app,app.xyList,2,90,5,10,114514,150,50)
                    if app.timePassed%400==0:
                        pattern1(app.enemy.x,app.enemy.y,5,5,2,10,114514,random.randint(-10,10),app)
        else:
            #ends
            app.mode="End"
            
def Start_redrawAll(app):
    app.screen.fill("white")
    font=pygame.font.SysFont(None,24)
    startimg=font.render('Press S for new game, Press R to read save',True,(0,0,0))
    app.screen.blit(startimg,(300,300))
    pygame.display.flip()

def Start_keyPressed(app):
    keys=pygame.key.get_pressed()
    if keys[pygame.K_s]:
        app.mode="Game"
    elif keys[pygame.K_r]:
        readSaveFile(app)
        app.mode="Game"

def End_redrawAll(app):
    font=pygame.font.SysFont(None,24)
    endimg=font.render(f'Game over!\nDamage score: {app.score}, Graze: {app.grazeCount}\nTotal score: {app.score+25*app.grazeCount}',True,(0,0,0))
    app.screen.blit(endimg,(300,300))

def Game_redrawAll(app):
    app.screen.blit(app.backgroundImage,(0,0))
    blankRect=(600,0,200,600)
    pygame.draw.rect(app.screen,(255,255,255),blankRect)
    drawTerrain(app)
    drawCharacters(app)
    if app.enemy is not None:
        font=pygame.font.SysFont(None,20)
        healthmsg=font.render(str(app.enemy.health),True,(0,0,0))
        app.screen.blit(healthmsg,(300,50))
    drawBullets(app)
    drawScore(app)
    drawPowerups(app)
    pygame.display.flip()

def Market_keyPressed(app):
    keys=pygame.key.get_pressed()
    if keys[pygame.K_1]:
        if app.character.canTrack:
            app.marketMessage="Tracking ability already obtained"
        elif app.character.experience//app.trackCost==0:
            app.marketMessage="Not enough experience!"
        else:
            app.marketMessage=f"Successfully purchased tracking ability, used {app.trackCost} experience"
            app.character.canTrack=True
            app.character.experience-=app.trackCost
    elif keys[pygame.K_2]:
        if app.marketBomb<=0:
            app.marketMessage="Sold out!"
        elif app.character.experience//app.bombCost==0:
            app.marketMessage="Not enough experience!"
        else:
            app.marketMessage=f"Successfully purchased bomb, used {app.bombCost} experience"
            app.character.bomb+=1
            app.marketBomb-=1
            app.character.experience-=app.bombCost
    elif keys[pygame.K_3]:
        if app.marketExtend<=0:
            app.marketMessage="Sold out!"
        elif app.character.experience//app.extendCost==0:
            app.marketMessage="Not enough experience!"
        else:
            app.marketMessage=f"Successfully purchased extra life, used {app.extendCost} experience"
            app.character.life+=1
            app.marketExtend-=1
            app.character.experience-=app.extendCost
    elif keys[pygame.K_4]:
        if app.character.experience//app.powerCost==0:
            app.marketMessage="Not enough experience!"
        else:
            app.marketMessage=f"Successfully purchased 0.05 power, used {app.powerCost} experience"
            app.character.power+=0.05
            app.character.experience-=app.powerCost
    elif keys[pygame.K_s]:
        saveFile(app)
        app.marketMessage="Saved game!"
    elif keys[pygame.K_m]:
        app.mode="Game"

def Market_redrawAll(app):
    trackcount=0
    if not app.character.canTrack: trackcount=1
    font=pygame.font.SysFont(None,16)
    marketmsg=f"1. Tracking ability: remaining {trackcount}, cost {app.trackCost}, available {min(trackcount,app.character.experience//app.trackCost)}\n"
    marketmsg+=f"2. Extra bomb: remaining {app.marketBomb}, cost {app.bombCost}, available {min(app.marketBomb,app.character.experience//app.bombCost)}\n"
    marketmsg+=f"3. Extra life: remaining {app.marketExtend}, cost {app.extendCost}, available {min(app.marketExtend,app.character.experience//app.extendCost)}\n"
    marketmsg+=f"4. Power up 0.05, current power {app.character.power}, cost {app.powerCost}, available {app.character.experience//app.powerCost}"
    marketExtraMsgObj=font.render(app.marketMessage)
    marketmsgObj=font.render(marketmsg,True,(0,0,0))
    app.screen.blit(marketmsgObj,(300,200))
    app.screen.blit(marketExtraMsgObj,(300,500))
    pygame.display.flip()

def Game_keyPressed(app):
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        app.character.isFiring=not app.character.isFiring
    if keys[pygame.K_z]:
        app.isFocus=not app.isFocus
    if keys[pygame.K_f]:
        freeze(app,app.character.x,app.character.y-80,80)
    if keys[pygame.K_x]:
        bomb(app)
    if keys[pygame.K_m]:
        app.mode="Market"
        
def Game_timerFired(app):
    app.timePassed+=app.timerDelay
    if app.enemy is not None:
        enemyTick(app)
    Game_keyPressed(app)
    Game_redrawAll(app)
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

def main(app):
    appStarted(app)
    loadImage(app)
    marketInit(app)
    clock=pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if app.mode=="Start":
            Start_redrawAll(app)
            Start_keyPressed(app)
        elif app.mode=="Game":
            Game_timerFired(app)
            if app.stage==1:
                stage1(app)
            elif app.stage==2:
                stage2(app)
            elif app.stage==3:
                stage3(app)
        elif app.mode=="Market":
            Market_redrawAll(app)
            Market_keyPressed(app)
        pygame.display.update()
        clock.tick(60)

newApp=app()
main(app)
