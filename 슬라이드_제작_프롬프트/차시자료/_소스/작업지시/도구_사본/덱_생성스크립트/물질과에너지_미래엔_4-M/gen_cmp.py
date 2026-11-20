# 4-M 그림 좌표 생성: tpl.html의 {{NAME}}을 채워 slides.html을 만든다
import math, sys, re
W='/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/물질과에너지_미래엔_4-M/'
OUT='/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/물질과에너지_미래엔_4-M/cmp.html'
F={}
def path(pts): return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
ke=math.log(2)/4
def conc(t,tau,ka,D=80,first=0):
    s=0;k=0
    while k*tau<=t+1e-9:
        tp=t-k*tau; s+=D*ka/(ka-ke)*(math.exp(-ke*tp)-math.exp(-ka*tp)); k+=1
    return s
# ── S3 반감기 띠 그림 (540x170): X0 50, Y0 140, W 460, H 110, 4 반감기
X0,Y0,Wd,H=50,140,460,110
pts=[(X0+Wd*i/200, Y0-H*0.5**(4*i/200)) for i in range(201)]
F['S3CURVE']=path(pts)
g=''
for k in (1,2,3):
    x=X0+Wd*k/4; y=Y0-H*0.5**k
    g+=f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{y:.1f}" stroke="#5B6B7F" stroke-width="1.6" stroke-dasharray="5 5"/><line x1="{X0}" y1="{y:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="#5B6B7F" stroke-width="1.6" stroke-dasharray="5 5"/>'
F['S3DASH']=g
# ── S5 분포 곡선 (250x300): 가로 0–7, f ∝ sqrt(E) e^{-E/kT}
X0,Y0,Wd,H=26,250,214,200
def f(E,kT): return math.sqrt(E)*math.exp(-E/kT)/(kT**1.5)
mx=max(f(i/100,1) for i in range(1,701))
def P(kT,a=0,b=7):
    return [(X0+Wd*E/7, Y0-H*0.92*f(E,kT)/mx) for E in [a+(b-a)*i/160 for i in range(161)]]
F['S5T1']=path(P(1)); F['S5T2']=path(P(1.7))
Ea=3.6
for nm,kT in (('S5A1',1),('S5A2',1.7)):
    p=P(kT,Ea,7); F[nm]=path(p)+f' L{X0+Wd:.1f} {Y0} L{X0+Wd*Ea/7:.1f} {Y0} Z'
F['S5EA']=f'{X0+Wd*Ea/7:.1f}'; F['S5EAC']=f'{X0+Wd*2.4/7:.1f}'
# ── 혈중 농도 그래프 공통: 시간 0–T 시간, 농도 0–YM
def blood(Wv,Hv,x0,y0,T,YM,tau,ka,n=None):
    pts=[]
    for i in range(301):
        t=T*i/300
        c=conc(t,tau,ka) if n is None else sum(80*ka/(ka-ke)*(math.exp(-ke*(t-k*tau))-math.exp(-ka*(t-k*tau))) for k in range(n) if t>=k*tau)
        pts.append((x0+Wv*t/T, y0-Hv*min(c,YM)/YM))
    return pts
# S9 한 번 복용 (470x270) x0 56 y0 232 W 396 H 196, 0–24 h, YM 100, 기준 30, 독성 100(위 경계 밖이면 표시만)
p=blood(396,196,56,232,24,110,999,0.8,n=1)
F['S9CURVE']=path(p)
# 최대 점
im=max(range(len(p)),key=lambda i:-p[i][1]); F['S9MX']=f'{p[im][0]:.1f}'; F['S9MY']=f'{p[im][1]:.1f}'
cmax=conc(24*im/300,999,0.8)
# 최대의 절반 되는 시점
th=None
for i in range(im,301):
    t=24*i/300; c=sum(80*0.8/(0.8-ke)*(math.exp(-ke*t)-math.exp(-0.8*t)) for _ in [0])
    if c<=cmax/2: th=(56+396*t/24, 232-196*c/110); break
F['S9HX']=f'{th[0]:.1f}'; F['S9HY']=f'{th[1]:.1f}'
F['S9Y30']=f'{232-196*30/110:.1f}'; F['S9Y100']=f'{232-196*100/110:.1f}'
F['S9BH']=f'{(196*70/110):.1f}'; F['S9Y100L']=f'{232-196*100/110-8:.1f}'; F['S9Y30L']=f'{232-196*30/110-8:.1f}'
F['S9MXL']=f'{p[im][0]+12:.1f}'; F['S9MYL']=f'{p[im][1]-6:.1f}'; F['S9HXL']=f'{th[0]+10:.1f}'; F['S9HYL']=f'{th[1]-8:.1f}'
print('S9 cmax',cmax,'tmax',24*im/300,'half at',th)
# S10 두 그래프 (500x230): x0 50 y0 196 W 430 H 170, 0–48 h, YM 140
for nm,tau in (('S10A',4),('S10B',12)):
    p=blood(430,170,50,196,48,140,tau,0.8)
    F[nm]=path(p)
F['S10Y30']=f'{196-170*30/140:.1f}'; F['S10Y30T']=f'{196-170*30/140+6:.1f}'; F['S10Y100T']=f'{196-170*100/140+6:.1f}'; F['S10Y30L']=f'{196-170*30/140+20:.1f}'; F['S10Y100L']=f'{196-170*100/140-8:.1f}'; F['S10Y100']=f'{196-170*100/140:.1f}'
# S11 감소 곡선 (420x250) x0 56 y0 214 W 340 H 180: 0–12 h, 100에서 시작
p=[(56+340*t/12, 214-180*(0.5**(t/4))) for t in [12*i/150 for i in range(151)]]
F['S11CURVE']=path(p)
tpl=open(W+'tpl.html',encoding='utf-8').read()
miss=set(re.findall(r'\{\{(\w+)\}\}',tpl))-set(F)
if miss: sys.exit('missing '+str(miss))
out=re.sub(r'\{\{(\w+)\}\}',lambda m:F[m.group(1)],tpl)
open(OUT,'w',encoding='utf-8').write(out); print('ok',len(out))
