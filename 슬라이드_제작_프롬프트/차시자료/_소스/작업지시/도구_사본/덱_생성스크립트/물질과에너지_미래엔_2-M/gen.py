import math
def water(ox,oy,th,L=35,rO=14,rH=11,half=52.25):
    hs=[(ox+L*math.cos(math.radians(th+s*half)),oy+L*math.sin(math.radians(th+s*half))) for s in(-1,1)]
    out=''.join(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#9AA5B1" stroke-width="5" stroke-linecap="round"/>' for x,y in hs)
    out+=f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="{rO}" fill="#E5533D" stroke="#9B2C22" stroke-width="2"/>'
    out+=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rH}" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2"/>' for x,y in hs)
    return out,hs
def hb(h,o,rH=11,rO=14):
    dx,dy=o[0]-h[0],o[1]-h[1];d=math.hypot(dx,dy);ux,uy=dx/d,dy/d
    return f'<line x1="{h[0]+ux*(rH+3):.1f}" y1="{h[1]+uy*(rH+3):.1f}" x2="{o[0]-ux*(rO+3):.1f}" y2="{o[1]-uy*(rO+3):.1f}" stroke="#5B6B7F" stroke-width="3" stroke-dasharray="6 5"/>'
def along(o,h,dist=101):
    dx,dy=h[0]-o[0],h[1]-o[1];d=math.hypot(dx,dy);return (o[0]+dx/d*dist,o[1]+dy/d*dist)
# S3 figure, viewBox 320x300
A=(110,120);sa,ha=water(*A,20)
B=along(A,ha[0]);C=along(A,ha[1])
sb,hb_=water(*B,-80);sc,hc=water(*C,140)
D=along(C,hc[1]) if False else None
print('B',B,'C',C)
# 4th: O of A accepts H from E
E=(A[0]-75,A[1]-55)
th=math.degrees(math.atan2(A[1]-E[1],A[0]-E[0]))+52.25
se,he=water(*E,th)
print('E H',he)
s3=sa+sb+sc+se+hb(ha[0],B)+hb(ha[1],C)+hb(he[0],A)
open('s3.svg','w').write(s3)
# bezier intersections for S6
def bez(p,t):
    return tuple((1-t)**3*p[0][i]+3*(1-t)**2*t*p[1][i]+3*(1-t)*t*t*p[2][i]+t**3*p[3][i] for i in(0,1))
def xat(p,y):
    lo,hi=0,1
    for _ in range(60):
        m=(lo+hi)/2
        if bez(p,m)[1]>y: lo=m
        else: hi=m
    return bez(p,lo)
W=[(70,282),(230,276),(330,215),(390,46)]
S=[(70,286),(250,282),(360,232),(430,64)]
print('W760',xat(W,110),'S760',xat(S,110))
# at x=300 y of each
def yat(p,x):
    lo,hi=0,1
    for _ in range(60):
        m=(lo+hi)/2
        if bez(p,m)[0]<x: lo=m
        else: hi=m
    return bez(p,lo)
print('W300',yat(W,320),'S300',yat(S,320))
