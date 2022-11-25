import math

#does the job but not quite well
def cart2polar(x,y):
    if x==0:
        if y<0:
            return(-90,y)
        else:
            return(90,y)
    r=math.sqrt(x**2+y**2)
    theta=math.atan(y/x)/math.pi*180
    return(theta,r)

def polar2cart(theta,r):
    x=r*math.cos(theta/180*math.pi)
    y=r*math.sin(theta/180*math.pi)
    return(x,y)

def distance(x1,y1,x2,y2):
    return(math.sqrt((x2-x1)**2+(y2-y1)**2))

def delta(a,b):
    return abs(a-b)

