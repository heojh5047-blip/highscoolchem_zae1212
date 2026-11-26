# -*- coding: utf-8 -*-
"""3-4-1 gen.py의 전지 그림 도우미를 옮겨 온 것(3-4-3용 사본)."""
from h import *
M_R=30   # 금속 원자 Zn·Cu 반지름(덱 약속, 3-3-1 Zn 30 이어받음), 이온 Zn2+·Cu2+ 22
def an(kind,body,**k):
    a=' '.join(f'data-{x.replace("_","-")}="{v}"' for x,v in k.items())
    return f'<g data-anim="{kind}" {a}>{body}</g>'
def step(g,body): return f'<g class="step" data-g="{g}">{body}</g>'
def atom(x,y,r,el,lab=None): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}'+(f',{lab}' if lab is not None else '')+'"></g>'
def chg(x,y,r,s): return f'<g data-chg="{f(x)},{f(y)},{f(r)},{s}"></g>'
def elec(x,y,lab=True,r=9):
    return C(x,y,r,MINUS,1.5,'#DCE9FA')+(T(x,y+6,tex='e^-',size=18,fill=MINUS) if lab else '')
def circ(parts):
    import json
    return "<g data-circuit='"+json.dumps({"parts":parts,"stroke":3})+"'></g>"
MET={'Zn':('#C9D3DD','#7E8B98'),'Cu':('#E6C29C','#B0835A'),'Ni':('#B9BDB4','#7A7F74'),'Ag':('#DDE1E6','#8C99A6'),
     'Mg':('#EEF1F4','#9AA5B1'),'Co':('#A7B3C2','#6B7A8C'),'C':('#4A4F57','#2B2F35'),'Pt':('#B8BEC6','#7E8B98')}
SOLC={'w':('#DDEEF8',1),'cu':('#3E8ED0',.32),'cu2':('#3E8ED0',.14),'cu3':('#3E8ED0',.06),'mn':('#A24FB5',.35),'i':('#C9A46A',.35),'co':('#D98C9B',.3),'cr':('#E08A2C',.35)}
GLS='#7E8B98'
def beaker(x0,x1,top=120,bot=300):
    return (f'<path d="M{x0-6} {top} H{x0} V{bot-10} Q{x0} {bot} {x0+10} {bot} H{x1-10} Q{x1} {bot} {x1} {bot-10} V{top} H{x1+6}" '
            f'fill="none" stroke="{GLS}" stroke-width="3" stroke-linejoin="round"/>')
def sol(x0,x1,kind,top=160,bot=298):
    c,o=SOLC[kind]; return f'<rect x="{x0+2}" y="{top}" width="{x1-x0-4}" height="{bot-top}" fill="{c}" fill-opacity="{o}"/>'
def plate(cx,m,top=90,h=180,w=None):
    fl,st=MET[m]; w=w or (22 if m=='C' else 18 if m=='Pt' else 28)
    return R(cx-w/2,top,w,h,st,2,fl,3)
def bridge(x1=190,x2=370,top=112,bot=250,w=24,kind='tube'):
    d=f'M{x1} {bot} V{top} H{x2} V{bot}'
    if kind=='tube': return f'<path d="{d}" fill="none" stroke="#B9A98A" stroke-width="{w}"/><path d="{d}" fill="none" stroke="#F6F0E0" stroke-width="{w-6}"/>'
    return ''
def cell(Lm='Zn',Rm='Cu',Ltex=r'\ce{Zn}',Rtex=r'\ce{Cu}',Lsol=r'\ce{ZnSO4(aq)}',Rsol=r'\ce{CuSO4(aq)}',Lk='w',Rk='cu',
         e='r',poles=True,br=True,ions=None,ion_anim=True,flow=True,meter='V',reading=None,extra='',elab=True,blab=True):
    """viewBox 560×370: L 비커 40–230(전극 124), R 비커 330–520(전극 424). e='r' → 전자 L→R(L이 (−)극).
       ions=(음이온 tex, 양이온 tex) 염다리 이온 이동(음이온 → 산화 전극 쪽)."""
    o=[]
    mp=[["wire",[[124,90],[124,50],[262,50]]],["wire",[[298,50],[424,50],[424,90]]],["meter",[280,50],meter,{"r":18}]]
    o.append(circ(mp))
    o+= [beaker(40,230),beaker(330,520),sol(40,230,Lk),sol(330,520,Rk)]
    if br:
        o.append(bridge())
        if blab: o.append(T(280,142,mix='염다리',size=20,fill=MUTED))
    o.append(plate(124,Lm)); o.append(plate(424,Rm))
    if flow and e:
        dd='M124 90 V50 H262 M298 50 H424 V90' if e=='r' else 'M424 90 V50 H298 M262 50 H124 V90'
        o.append(f'<path d="{dd}" fill="none" stroke="{MINUS}" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow="1" data-speed="36"/>')
    if elab and e:
        if e=='r': o.append(A(160,26,232,26,'minus',3)+A(328,26,400,26,'minus',3))
        else: o.append(A(232,26,160,26,'minus',3)+A(400,26,328,26,'minus',3))
        o.append(T(152,34,tex='e^-',size=21,fill=MINUS,anchor='end')+T(408,34,tex='e^-',size=21,fill=MINUS,anchor='start'))
    if reading: o.append(T(280,92,mix=reading,size=20,weight=700,halo=True))
    o.append(T(104,112,tex=Ltex,size=22,anchor='end')); o.append(T(446,112,tex=Rtex,size=22,anchor='start'))
    o.append(T(135,288,tex=Lsol,size=20)); o.append(T(425,288,tex=Rsol,size=20))
    if br and ions:
        an_,ca_=ions; sL,sR=(1,-1) if e=='r' else (-1,1)
        # 음이온은 산화 전극(전자가 나가는 쪽) 쪽으로, 양이온은 환원 전극 쪽으로
        ax_end= 214 if e=='r' else 346; cx_end= 346 if e=='r' else 214
        ab=chg(ax_end,112,9,'-'); cb=chg(cx_end,112,9,'+')
        if ion_anim:
            o.append(an('move',ab,**{'from':f'{f(60*sL)},0','dur':'1.6','rep':'loop','ease':'lin'}))
            o.append(an('move',cb,**{'from':f'{f(60*sR)},0','dur':'1.6','rep':'loop','ease':'lin','delay':'.8'}))
        else: o.append(ab+cb)
        ya,yc=(170,206)
        if e=='r':
            o.append(T(280,ya,mix=f'← ${an_}$',size=20,fill=MINUS,halo=True)); o.append(T(280,yc,mix=f'${ca_}$ →',size=20,fill=PLUS,halo=True))
        else:
            o.append(T(280,ya,mix=f'${an_}$ →',size=20,fill=MINUS,halo=True)); o.append(T(280,yc,mix=f'← ${ca_}$',size=20,fill=PLUS,halo=True))
    if poles and e:
        neg,pos=(135,425) if e=='r' else (425,135)
        o.append(T(neg,326,mix='(−)극',size=21,weight=700)+T(neg,353,mix='산화 전극',size=20,weight=700,fill=OX))
        o.append(T(pos,326,mix='(+)극',size=21,weight=700)+T(pos,353,mix='환원 전극',size=20,weight=700,fill=RD))
    o.append(extra)
    return ''.join(o)
def cellsvg(label,width=560,vb=(560,370),**k): return svg(vb,width,label,[cell(**k)])

