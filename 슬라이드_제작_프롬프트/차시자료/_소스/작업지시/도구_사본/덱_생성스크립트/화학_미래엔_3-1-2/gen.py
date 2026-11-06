import math, json, sys
out={}
def f(v): return ('%.1f'%v).rstrip('0').rstrip('.')
def no2(cx,cy,r,rot=0):
    d=1.35*r; s=''
    for a in (-67,67):
        q=math.radians(-90+a+rot); s+=f'<g data-atom="{f(cx+d*math.cos(q))},{f(cy+d*math.sin(q))},{r},O"></g>'
    return s+f'<g data-atom="{f(cx)},{f(cy)},{r},N"></g>'
def n2o4(cx,cy,r):
    d=1.35*r; dn=1.45*r; s=''; ns=''
    for sd in (-1,1):
        nx=cx+sd*dn/2; base=0 if sd>0 else 180
        for a in (-62,62):
            q=math.radians(base+a); s+=f'<g data-atom="{f(nx+d*math.cos(q))},{f(cy+d*math.sin(q))},{r},O"></g>'
        ns+=f'<g data-atom="{f(nx)},{f(cy)},{r},N"></g>'
    return s+ns
T=lambda x,y,m,size=20,anc='middle',fill='#16233D',extra='': f'<text class="tex" x="{f(x)}" y="{f(y)}" data-mix="{m}" data-size="{size}" data-anchor="{anc}" fill="{fill}"{extra}></text>'
# cover
c='<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
for i,(x,op,lab) in enumerate([(150,.45,'실험 1'),(390,.22,'실험 5')]):
    c+=f'<path d="M{x-20} 34 V74 A62 62 0 1 0 {x+20} 74 V34 Z" fill="#B5562A" fill-opacity="{op}"/><path d="M{x-20} 34 V74 A62 62 0 1 0 {x+20} 74 V34" fill="none" stroke="#7E8B98" stroke-width="4"/><rect x="{x-27}" y="20" width="54" height="20" rx="5" fill="#C9B79C" stroke="#8C7A5E" stroke-width="2.5"/>'
    c+=T(x,226,lab,22,extra=' data-weight="700"')
c+=T(270,128,'평형',20,fill='#5B6B7F')
c+='<g data-anim="move" data-from="0,-14" data-dur="1.2" data-delay=".6" data-ease="out"><rect x="110" y="236" width="320" height="92" rx="16" fill="#FFFCEB" stroke="#E0C44A" stroke-width="3"/>'+T(270,294,'$K=\\dfrac{[\\ce{N2O4}]}{[\\ce{NO2}]^2}\\approx 212$',28)+'</g>'
c+='<g data-anim="move" data-from="5,-4" data-rep="swing" data-dur="1.1">'+no2(150,384,24)+'</g>'
c+='<g data-anim="draw" data-dur="1" data-delay=".4"><path d="M222 380 H298 l-10 -7" fill="none" stroke="#2E9E6A" stroke-width="3" stroke-linecap="round"/><path d="M298 394 H222 l10 7" fill="none" stroke="#7B4FC8" stroke-width="3" stroke-linecap="round"/></g>'
c+=n2o4(390,389,24)
c+=T(150,478,'$\\ce{2NO2}$',24)+T(390,478,'$\\ce{N2O4}$',24)
out['COVER']=c
# S9 two plots 520x330 each
D=[(0.047,0.467),(0.051,0.551),(0.046,0.448),(0.045,0.428),(0.053,0.595)]
def plot(kind):
    X0,Y0,X1,Y1=78,262,500,26
    xm=0.06 if kind=='a' else 3.2e-3
    X=lambda v:X0+(X1-X0)*v/xm; Y=lambda v:Y0-(Y0-Y1)*v/0.7
    s=''
    for v in (0.2,0.4,0.6):
        s+=f'<path d="M{X0} {f(Y(v))} H{X1}" stroke="#E2E7EC" stroke-width="1.5"/>'+T(X0-8,Y(v)+6,f'{v:.1f}',18,'end')
    ticks=(0.02,0.04,0.06) if kind=='a' else (1e-3,2e-3,3e-3)
    for v in ticks:
        lab=f'{v:.2f}' if kind=='a' else f'{v*1e3:.1f}'
        s+=f'<path d="M{f(X(v))} {Y0} V{Y1}" stroke="#E2E7EC" stroke-width="1.5"/>'+T(X(v),Y0+24,lab,18)
    s+=f'<g data-arw="{X0},{Y0},{X1+20},{Y0},ink,2"></g><g data-arw="{X0},{Y0},{X0},{Y1-16},ink,2"></g>'+T(X0-8,Y0+24,'0',18,'end')
    s+=T(X0+8,Y1-2,'$[\\ce{N2O4}]$ [mol/L]',19,'start')
    if kind=='a':
        s+=T(X1+16,Y0-12,'$[\\ce{NO2}]$ [mol/L]',19,'end')
        pts=' '.join(f'{f(X(x))},{f(Y(212*x*x))}' for x in [i*0.0575/40 for i in range(41)])
        s+=f'<polyline class="step" data-g="p1" points="{pts}" fill="none" stroke="#5B6B7F" stroke-width="2.5" stroke-dasharray="8 6"/>'
        s+=f'<g class="step" data-g="p1">'+T(X(0.017),Y(0.5),'$[\\ce{N2O4}]\\propto[\\ce{NO2}]^2$ (곡선)',19,'middle','#5B6B7F',' data-halo="1"')+'</g>'
        for x,y in D: s+=f'<circle cx="{f(X(x))}" cy="{f(Y(y))}" r="6" fill="#B5562A" stroke="#fff" stroke-width="1.5"/>'
    else:
        s+=T(X1+16,Y0-12,'$[\\ce{NO2}]^2$ [$\\times10^{-3}$]',19,'end')
        s+=f'<g class="step" data-g="p2"><path d="M{X0} {Y0} L{f(X(3.1e-3))} {f(Y(212*3.1e-3))}" stroke="#16233D" stroke-width="2.5" data-anim="draw" data-on="step"/>'+T(X(1.3e-3),Y(0.5),'기울기 ≈ 212 = $K$',20,'middle','#16233D',' data-halo="1" data-weight="700"')+'</g>'
        for x,y in D: s+=f'<g data-anim="pop" data-dur=".5" data-delay="{.3+.12*D.index((x,y))}" data-o="{f(X(x*x))},{f(Y(y))}"><circle cx="{f(X(x*x))}" cy="{f(Y(y))}" r="6" fill="#16233D" stroke="#fff" stroke-width="1.5"/></g>'
    return s
out['PLOTA']=plot('a'); out['PLOTB']=plot('b')
# S22 graph 04: 420x280
X0,Y0,X1,Y1=62,240,400,24
Y=lambda v:Y0-(Y0-Y1)*v/9
s=''
for v in (2,4,6,8): s+=f'<path d="M{X0} {f(Y(v))} H{X1}" stroke="#C9D3DD" stroke-width="1.5" stroke-dasharray="4 4"/>'+T(X0-8,Y(v)+6,str(v),18,'end')
for i in range(1,7): s+=f'<path d="M{X0+i*48} {Y0} V{Y1+10}" stroke="#C9D3DD" stroke-width="1.5" stroke-dasharray="4 4"/>'
s+=f'<g data-arw="{X0},{Y0},{X1+10},{Y0},ink,2"></g><g data-arw="{X0},{Y0},{X0},{Y1-10},ink,2"></g>'+T(X0-8,Y0+22,'0',18,'end')+T(X1+6,Y0+26,'시간',19,'end')+T(X0+8,Y1-2,'양 [mol]',19,'start')
def cur(a,b,col,lab,ly,dash=''):
    pts=' '.join(f'{f(X0+i*(X1-X0)/60)},{f(Y(b+(a-b)*math.exp(-i/9)))}' for i in range(61))
    return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3.5"{dash} data-anim="draw" data-dur="1.4" data-delay=".3"/>'+T(X0+70,ly,lab,20,'middle',col,' data-halo="1"')
s+=cur(8,4,'#16233D','$\\mathrm{A}$',Y(6.3))+cur(0,4,'#2E9E6A','$\\mathrm{B}$',Y(2.6))+cur(0,2,'#2E9E6A','$\\mathrm{C}$',Y(0.6),' stroke-dasharray="10 6"')
out['G04']=s
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False)
