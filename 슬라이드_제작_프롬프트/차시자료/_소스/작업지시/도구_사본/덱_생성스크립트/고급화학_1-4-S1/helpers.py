import math, random, re, sys, os
INK='#16233D';PLUS='#D7263D';MINUS='#1F6FD1';FIELD='#2E9E6A';EQUI='#E08A2C';BF='#7B4FC8';MUTED='#5B6B7F';GRAV='#8C99A6'
HC={656:'#E8322B',486:'#21B5C9',434:'#3D4FE0',410:'#7B3FC4'}
def f(v): return ('%.1f'%v).rstrip('0').rstrip('.')
def T(x,y,tex=None,mix=None,size=20,anchor='middle',fill=None,halo=False,weight=None,extra=''):
    a=f'<text class="tex" x="{f(x)}" y="{f(y)}" '
    a+=(f'data-tex="{tex}" ' if tex is not None else f'data-mix="{mix}" ')
    a+=f'data-size="{size}" data-anchor="{anchor}"'
    if fill: a+=f' fill="{fill}"'
    if halo: a+=' data-halo="1"'
    if weight: a+=f' data-weight="{weight}"'
    return a+(' '+extra if extra else '')+'></text>'
def A(x1,y1,x2,y2,col='ink',w=3,d=False,extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if d else ""}"{(" "+extra) if extra else ""}></g>'
def L(x1,y1,x2,y2,col=INK,w=2,dash=None,extra=''):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def P(pts,col=INK,w=2.5,fill='none',dash=None,extra='',close=False):
    d='M'+' L'.join(f'{f(x)} {f(y)}' for x,y in pts)+(' Z' if close else '')
    return f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def C(cx,cy,r,col=INK,w=2,fill='none',dash=None,extra=''):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{fill}" stroke="{col}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' '+extra if extra else '')+'/>'
def nuc(x,y,r=12): return f'<g data-chg="{f(x)},{f(y)},{r},+"></g>'
def ele(x,y,r=9): return f'<g data-chg="{f(x)},{f(y)},{r},-"></g>'
def wl_rgb(w):
    if w<380 or w>750: return None
    if w<440: r,g,b=-(w-440)/60,0,1
    elif w<490: r,g,b=0,(w-440)/50,1
    elif w<510: r,g,b=0,1,-(w-510)/20
    elif w<580: r,g,b=(w-510)/70,1,0
    elif w<645: r,g,b=1,-(w-645)/65,0
    else: r,g,b=1,0,0
    fac=.3+.7*(w-380)/40 if w<420 else (1 if w<=700 else .3+.7*(750-w)/50)
    return '#%02X%02X%02X'%tuple(int(255*(c*fac)**.8) for c in (r,g,b))
def wcol(w):
    for k,v in HC.items():
        if abs(w-k)<2.5: return v
    return wl_rgb(w)
def rainbow(gid,x1,x2):
    st=''.join(f'<stop offset="{(w-400)/300:.3f}" stop-color="{wl_rgb(w)}"/>' for w in range(400,701,20))
    return f'<defs><linearGradient id="{gid}" x1="0" x2="1" y1="0" y2="0">{st}</linearGradient></defs>'
def wave(x1,y1,x2,y2,col,amp=6,lam=14,w=3):
    dx,dy=x2-x1,y2-y1; Ln=math.hypot(dx,dy); ux,uy=dx/Ln,dy/Ln; px,py=-uy,ux
    pts=[]; n=int(Ln/2)
