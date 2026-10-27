import math 

def calculatute(x0,x1,x2,y0,y1,y2):
    d1 = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    d2 = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return d2-d1

x0,x1,x2,y0,y1,y2 = list(map(int,input().split()))