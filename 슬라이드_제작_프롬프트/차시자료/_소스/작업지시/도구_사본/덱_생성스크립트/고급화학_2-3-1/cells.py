# -*- coding: utf-8 -*-
"""고급화학 2-3-1 결정 구조 정의(3D 좌표) — gen.py(그림)·calc.py(검산)가 함께 쓴다.
   입방: 모서리 a = 1, 분율 좌표 = 직교 좌표. 육방 밀집: a = 1, c = sqrt(8/3), 육각기둥 단위세포(원시 세포 3개)."""
import math, itertools
from fractions import Fraction as Fr
CH=math.sqrt(8/3)
CUBIC={
 'sc':  {'name':'단순 입방','basis':[((0,0,0),'M')]},
 'bcc': {'name':'체심 입방','basis':[((0,0,0),'M'),((.5,.5,.5),'M')]},
 'fcc': {'name':'면심 입방','basis':[((0,0,0),'M'),((.5,.5,0),'M'),((.5,0,.5),'M'),((0,.5,.5),'M')]},
 'nacl':{'name':'NaCl','basis':[((0,0,0),'Cl'),((.5,.5,0),'Cl'),((.5,0,.5),'Cl'),((0,.5,.5),'Cl'),((.5,0,0),'Na'),((0,.5,0),'Na'),((0,0,.5),'Na'),((.5,.5,.5),'Na')]},
 'cscl':{'name':'CsCl','basis':[((0,0,0),'Cl'),((.5,.5,.5),'Cs')]},
 'zns': {'name':'ZnS','basis':[((0,0,0),'S'),((.5,.5,0),'S'),((.5,0,.5),'S'),((0,.5,.5),'S'),((.25,.25,.25),'Zn'),((.75,.75,.25),'Zn'),((.75,.25,.75),'Zn'),((.25,.75,.75),'Zn')]},
 # 연습 문제 5 루틸(TiO2): 정방 a=b=1, c=0.645(296/459 pm), u=0.305
 'tio2':{'name':'TiO2','basis':[((0,0,0),'Ti'),((.5,.5,.5),'Ti'),((.305,.305,0),'O'),((.695,.695,0),'O'),((.805,.195,.5),'O'),((.195,.805,.5),'O')],'c':0.645},
}
CHARGE={'M':0,'Na':1,'Cl':-1,'Cs':1,'Zn':2,'S':-2,'Ti':4,'O':-2}
ION_R={'Na':97,'Cl':181,'Cs':167,'Zn':74,'S':184}   # 교과서 102쪽 pm
def near(a,b,e=1e-6): return abs(a-b)<e
def cubic_sites(key,lo=-1,hi=3):
    S=CUBIC[key]; cz=S.get('c',1.0); out=[]
    for i,j,k in itertools.product(range(lo,hi),repeat=3):
        for (x,y,z),t in S['basis']:
            out.append(((x+i,y+j,(z+k)*cz),t))
    return out
def hcp_sites(n=3):
    a1=(1,0,0); a2=(-.5,math.sqrt(3)/2,0); out=[]
    for i,j in itertools.product(range(-n,n+1),repeat=2):
        for k in range(-1,3):
            for fx,fy,fz in ((0,0,0),(1/3,2/3,.5)):
                x=(i+fx)*a1[0]+(j+fy)*a2[0]; y=(i+fx)*a1[1]+(j+fy)*a2[1]; z=(k+fz)*CH
                out.append(((x,y,z),'M'))
    return out
HEX=[(math.cos(math.radians(60*k)),math.sin(math.radians(60*k))) for k in range(6)]
def in_hex(x,y,e=1e-6):
    # 정육각형(꼭짓점 0°,60°…, 외접 반지름 1) 안·위인가 → (안?, 꼭짓점?, 변 위?)
    on_v=any(near(x,vx) and near(y,vy) for vx,vy in HEX)
    inside=True; on_e=False
    for k in range(6):
        (x1,y1),(x2,y2)=HEX[k],HEX[(k+1)%6]
        cr=(x2-x1)*(y-y1)-(y2-y1)*(x-x1)
        if cr<-e: inside=False
        if abs(cr)<e: on_e=True
    return inside,on_v,on_e and not on_v
def cell_atoms(key):
    """단위세포 경계 안·위의 원자: [(pos, 종류, 몫 Fraction, 자리 이름)]"""
    out=[]
    if key=='hcp':
        for p,t in hcp_sites():
            ins,v,e=in_hex(p[0],p[1])
            if not ins or p[2]<-1e-6 or p[2]>CH+1e-6: continue
            zb=near(p[2],0) or near(p[2],CH)
            w=(Fr(1,3) if v else Fr(1,2) if e else Fr(1))*(Fr(1,2) if zb else Fr(1))
            place='꼭짓점' if (v and zb) else ('면 중심' if zb else '내부')
            out.append((p,t,w,place))
        return out
    cz=CUBIC[key].get('c',1.0)
    for p,t in cubic_sites(key):
        q=(p[0],p[1],p[2]/cz)
        if all(-1e-6<=c<=1+1e-6 for c in q):
            nb=sum(1 for c in q if near(c,0) or near(c,1))
            w=Fr(1,2**nb); place={3:'꼭짓점',2:'모서리',1:'면 중심',0:'내부'}[nb]
            if nb==0 and all(near(c,.5) for c in q): place='체심'
            out.append((p,t,w,place))
    return out
def count(key):
    d={}
    for p,t,w,pl in cell_atoms(key): d[t]=d.get(t,0)+w
    return d
def by_place(key):
    d={}
    for p,t,w,pl in cell_atoms(key):
        k=(t,pl); n,ww=d.get(k,(0,w)); d[k]=(n+1,w)
    return d
def sites(key): return hcp_sites() if key=='hcp' else cubic_sites(key)
def neighbors(key,center,ctype):
    """center 원자의 가장 가까운 이웃(금속: 같은 원자, 이온: 반대 전하). 반환 (거리, 이웃 목록)"""
    S=sites(key); ion=CHARGE[ctype]!=0
    cand=[(math.dist(center,p),p,t) for p,t in S if math.dist(center,p)>1e-6 and ((CHARGE[t]*CHARGE[ctype]<0) if ion else True)]
    dmin=min(c[0] for c in cand)
    return dmin,[(p,t) for d,p,t in cand if d<dmin+1e-6]
CENTER={'sc':((0,0,1),'M'),'bcc':((.5,.5,.5),'M'),'fcc':((.5,.5,1),'M'),'hcp':((0,0,CH),'M'),
        'nacl':((.5,.5,.5),'Na'),'cscl':((.5,.5,.5),'Cs'),'zns':((.25,.25,.25),'Zn')}
def packing(key):
    if key=='hcp':
        V=3*math.sqrt(3)/2*CH; r=.5; N=6
    else:
        V=1.0; N=float(sum(count(key).values()))
        dmin,_=neighbors(key,*CENTER[key]); r=dmin/2
    return N*4/3*math.pi*r**3/V, r
# ── 3D 투영 (직교 투영, 그림·실험실 같은 식)
def rot(p,yaw,pitch,ctr):
    x,y,z=p[0]-ctr[0],p[1]-ctr[1],p[2]-ctr[2]
    a,b=math.radians(yaw),math.radians(pitch)
    x1=x*math.cos(a)-y*math.sin(a); y1=x*math.sin(a)+y*math.cos(a)
    Y=y1*math.cos(b)-z*math.sin(b); Z=y1*math.sin(b)+z*math.cos(b)
    return x1,Y,Z   # 화면 x = x1, 깊이 Y(클수록 멂), 화면 위 = Z
def cube_frame(cz=1.0):
    V=[(x,y,z*cz) for x in (0,1) for y in (0,1) for z in (0,1)]
    E=[(i,j) for i in range(8) for j in range(i+1,8) if sum(a!=b for a,b in zip(V[i],V[j]))==1]
    F=[((0,-1,0),lambda v:v[1]==0),((0,1,0),lambda v:v[1]==1),((-1,0,0),lambda v:v[0]==0),((1,0,0),lambda v:v[0]==1),((0,0,-1),lambda v:v[2]==0),((0,0,1),lambda v:v[2]==cz)]
    faces=[(n,{i for i,v in enumerate(V) if f(v)}) for n,f in F]
    return V,E,faces
def hex_frame():
    V=[(x,y,z) for z in (0,CH) for x,y in HEX]
    E=[(k,(k+1)%6) for k in range(6)]+[(6+k,6+(k+1)%6) for k in range(6)]+[(k,k+6) for k in range(6)]
    faces=[((0,0,-1),set(range(6))),((0,0,1),set(range(6,12)))]
    for k in range(6):
        m=math.radians(60*k+30); faces.append(((math.cos(m),math.sin(m),0),{k,(k+1)%6,k+6,6+(k+1)%6}))
    return V,E,faces
def edge_hidden(E,faces,yaw,pitch):
    def nY(n):
        return rot((n[0],n[1],n[2]),yaw,pitch,(0,0,0))[1]
    out=[]
    for i,j in E:
        adj=[n for n,s in faces if i in s and j in s]
        out.append(all(nY(n)>1e-9 for n in adj))
    return out
