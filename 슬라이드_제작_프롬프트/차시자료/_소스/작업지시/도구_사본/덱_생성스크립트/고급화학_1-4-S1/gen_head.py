# -*- coding: utf-8 -*-
"""고급화학 1-4-S1 그림 생성 머리(1-4-2 gen_head 사본 = 1-2-1·1-2-2 lewis 도우미): tpl.html의 {{KEY}}를 SVG로 바꿔 slides.html을 만든다."""
import math, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
# ★ 출력 경로: 반드시 이 덱(1-4-S1) 폴더
DECK='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/고급화학/1-4-S1_심화_친핵성_치환_제거_반응과_첨가_반응/'
OUT=DECK+'slides.html'
assert OUT.endswith('고급화학/1-4-S1_심화_친핵성_치환_제거_반응과_첨가_반응/slides.html') and '1-4-2' not in OUT and '1-4-1' not in OUT and '1-4-S2' not in OUT
exec(open(os.path.join(HERE,'helpers.py'),encoding='utf-8').read())
FIG={}
BOND='#9AA5B1'
def svg(vb,w,label,body,cls='fig',extra=''):
    return f'<svg class="{cls}" viewBox="{vb}" style="width:{w}px" aria-label="{label}"{(" "+extra) if extra else ""}>'+''.join(body)+'</svg>'
def G(body,attrs=''):
    return f'<g {attrs}>'+''.join(body if isinstance(body,list) else [body])+'</g>'
def an(kind,body,**kw):
    a=f'data-anim="{kind}"'+''.join(f' data-{k.replace("_","-")}="{v}"' for k,v in kw.items())
    return G(body,a)

# ═════ 루이스 구조 도우미 ═════
VAL={'H':1,'B':3,'C':4,'N':5,'O':6,'F':7,'P':5,'Cl':7,'S':6,'I':7,'Na':1,'K':1}
SIDE={'r':0,'u':90,'l':180,'d':270}
def _b(el,S,ux,uy):
    rx=(0.62 if len(el)>1 else 0.40)*S; ry=0.46*S
    return 1/math.sqrt((ux/rx)**2+(uy/ry)**2)
def _bg(a,S,ux,uy):
    if not a.get('grp'): return _b(a['el'],S,ux,uy)
    if a['grp']=='_': return -0.10*S   # 보이지 않는 연결점(고리 꼭짓점)
    rx=gw(a['grp'],S)/2+0.04*S; ry=0.46*S
    return 1/math.sqrt((ux/rx)**2+(uy/ry)**2)
def _dir(a):
    a=SIDE.get(a,a); t=math.radians(a); return math.cos(t),-math.sin(t)
def lewis(atoms,bonds,S=34,check=True,name='',num=None,fcshow=True,bw=2.6,elcol=None,showlp=True):
    """atoms: [dict(el,x,y,lp=[방향],rad=[방향],fc=정수,fcp='ur',oct=8,col=None)]
    bonds: [(i,j,차수,모양)] 모양 'l' 선, 'd' 점(전자쌍), 'p' 선+점선(공명 혼성), 'q' 점선만"""
    s=[]
    elec=[0]*len(atoms); bsum=[0]*len(atoms)
    for (i,j,o,st) in bonds:
        a,b=atoms[i],atoms[j]
        dx,dy=b['x']-a['x'],b['y']-a['y']; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
        ba=_bg(a,S,ux,uy)+0.10*S; bb=_bg(b,S,ux,uy)+0.10*S
        x1,y1=a['x']+ux*ba,a['y']+uy*ba; x2,y2=b['x']-ux*bb,b['y']-uy*bb
        if st=='n':
            for k in (i,j): bsum[k]+=o; elec[k]+=2*o
            continue
        if st=='h':
            s.append(L(x1,y1,x2,y2,INK,bw,dash='4 5',extra='stroke-linecap="round"')); continue
        if st=='d':
            mx,my=(a['x']+b['x'])/2,(a['y']+b['y'])/2
            offs={1:[0],2:[-0.14*S,0.14*S],3:[-0.26*S,0,0.26*S]}[o]
            for t in offs:
                cx,cy=mx+ux*t,my+uy*t
                for sg in (-1,1): s.append(f'<circle cx="{f(cx+px*sg*0.18*S)}" cy="{f(cy+py*sg*0.18*S)}" r="{f(0.1*S)}" fill="{INK}"/>')
        else:
            offs={1:[0],2:[-0.12*S,0.12*S],3:[-0.17*S,0,0.17*S]}[o if st not in 'pq' else (2 if st=='p' else 1)]
            for k,t in enumerate(offs):
                dash=None
                if st=='p' and k==1: dash='5 4'
                if st=='q': dash='6 5'
                s.append(L(x1+px*t,y1+py*t,x2+px*t,y2+py*t,INK,bw,dash=dash,extra='stroke-linecap="round"'))
        for k in (i,j): bsum[k]+=o; elec[k]+=2*o
    for k,a in enumerate(atoms):
        el=a['el']; x,y=a['x'],a['y']
        if a.get('grp'):   # 축약 원자단(CH3 등): 글자만, 검산은 formula()로
            if a['grp']!='_': s.append(T(x,y+0.36*S,tex='\\ce{'+a['grp']+'}',size=S,fill=a.get('col') or elcol))
            continue
        for d in a.get('lp',[]):
            ux,uy=_dir(d); bd=_b(el,S,ux,uy)+0.26*S; cx,cy=x+ux*bd,y+uy*bd; px,py=-uy,ux
            if showlp:
                for sg in (-1,1): s.append(f'<circle cx="{f(cx+px*sg*0.18*S)}" cy="{f(cy+py*sg*0.18*S)}" r="{f(0.1*S)}" fill="{INK}"/>')
            elec[k]+=2
        for d in a.get('rad',[]):
            ux,uy=_dir(d); bd=_b(el,S,ux,uy)+0.26*S
            s.append(f'<circle cx="{f(x+ux*bd)}" cy="{f(y+uy*bd)}" r="{f(0.1*S)}" fill="{INK}"/>'); elec[k]+=1
        s.append(T(x,y+0.36*S,tex='\\mathrm{'+el+'}',size=S,fill=a.get('col') or elcol))
        nl=len(a.get('lp',[])); nr=len(a.get('rad',[]))
        fcal=VAL[el]-2*nl-nr-bsum[k]
        if check:
            need=a.get('oct',2 if el=='H' else 8)
            if need is not None and elec[k]!=need: sys.exit(f'[{name}] {el}{k} 전자 {elec[k]} ≠ {need}')
            if a.get('fc',0)!=fcal: sys.exit(f'[{name}] {el}{k} 형식 전하 {fcal} ≠ {a.get("fc",0)}')
        fc=a.get('fc',0)
        if fc and fcshow:
            p=a.get('fcp','ur'); w2=(0.98 if len(el)>1 else 0.80)*S
            ox={'ur':w2,'ul':-w2,'dr':w2,'dl':-w2,'u':0,'d':0,'r':w2*1.25,'l':-w2*1.25}[p]
            oy={'ur':-0.74*S,'ul':-0.74*S,'dr':0.74*S,'dl':0.74*S,'u':-1.25*S,'d':1.25*S,'r':-0.2*S,'l':-0.2*S}[p]
            col=PLUS if fc>0 else MINUS
            tx={1:'+',-1:'-',2:'2+',-2:'2-'}[fc]
            rr=12 if abs(fc)==1 else 15
            s.append(C(x+ox,y+oy,rr,col,1.8,fill='#fff'))
            s.append(T(x+ox,y+oy+6.3,tex=tx,size=18,fill=col,weight=700))
        if num is not None and num[k] is not None:
            s.append(T(x,y-1.25*S,tex=num[k],size=19,fill=MUTED))
    return ''.join(s)
def bracket(x1,y1,x2,y2,ch='-',size=22):
    s=P([(x1+9,y1),(x1,y1),(x1,y2),(x1+9,y2)],INK,2.2)+P([(x2-9,y1),(x2,y1),(x2,y2),(x2-9,y2)],INK,2.2)
    return s+T(x2+4,y1+size*0.55,tex=ch,size=size,anchor='start',weight=700)
def rarrow(x1,x2,y,col=INK,w=2.4):
    return (L(x1+2,y,x2-2,y,col,w)+P([(x1+10,y-6),(x1,y),(x1+10,y+6)],col,w,extra='stroke-linecap="round"')
            +P([(x2-10,y-6),(x2,y),(x2-10,y+6)],col,w,extra='stroke-linecap="round"'))
def hbox(x,y,w,h,kind,g=None,extra=''):
    col=FIELD if kind=='s' else EQUI
    cls=f' class="step" data-g="{g}"' if g else ''
    return f'<rect{cls} x="{f(x-w/2)}" y="{f(y-h/2)}" width="{f(w)}" height="{f(h)}" rx="8" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.5"{(" "+extra) if extra else ""}/>'
def A_(el,x,y,**k):
    d=dict(el=el,x=x,y=y); d.update(k); return d
def hatom(x,y,cloud=34,lab=True,ncol=PLUS):
    s=f'<circle cx="{f(x)}" cy="{f(y)}" r="{cloud}" fill="{MINUS}" fill-opacity=".14" stroke="{MINUS}" stroke-opacity=".35" stroke-width="1.2"/>'
    s+=nuc(x,y,9)
    return s

# ═══ S1 표지
