# 3-M 구조식 좌표 생성 → slides.tpl.html 의 {{KEY}} 자리를 채워 slides.html 로
import sys, math
sys.path.insert(0, sys.argv[1])
from figs import sf, box, chain_svg, f, INK, EQUI
OUT = {}
FIELD='#2E9E6A'; MINUS='#1F6FD1'; RD='#0E7490'

def fischer(cx, y0, top, d=56, S=24, boxtop=None):
    """세로 사슬: top(CHO|CH2OH) / H-C-OH / HO-C-H / H-C-OH / CH2OH"""
    a=[(top,cx,y0)]; b=[]
    rows=[('H','OH'),('HO','H'),('H','OH')]
    for k,(l,r) in enumerate(rows):
        y=y0+d*(k+1); a.append(('C',cx,y)); ci=len(a)-1
        b.append((ci-1 if k==0 else ci-3, ci,1))
        a.append((l,cx-d*1.05,y)); b.append((ci,len(a)-1,1))
        a.append((r,cx+d*1.05,y)); b.append((ci,len(a)-1,1))
    a.append(('CH2OH',cx,y0+d*4)); b.append((len(a)-4,len(a)-1,1))
    s=''
    if boxtop:
        w=boxtop; s+=box(cx-w/2,y0-0.62*S,w,1.24*S)
    return s+sf(a,b,S)

def ring(cx, cy, r=46, S=22, left=None, right=None, lx=None, rx=None):
    """평면 육각 고리: O(-60°) C1(0°) C2(60°) C3(120°) C4(180°) C5(240°). H 생략"""
    ang=[-60,0,60,120,180,240]; sym=['O','C','C','C','C','C']
    a=[(sym[i],cx+r*math.cos(math.radians(t)),cy+r*math.sin(math.radians(t))) for i,t in enumerate(ang)]
    b=[(i,(i+1)%6,1) for i in range(6)]
    # C2, C3 의 OH (아래로 비스듬히)
    a.append(('OH',a[2][1]+30,a[2][2]+44)); b.append((2,6,1))
    a.append(('HO',a[3][1]-30,a[3][2]+44)); b.append((3,7,1))
    if right: a.append((right,rx if rx else a[1][1]+56,cy)); b.append((1,len(a)-1,1))
    if left: a.append((left,lx if lx else a[4][1]-56,cy)); b.append((4,len(a)-1,1))
    return sf(a,b,S), a

# S9 자일란 반복 단위(괄호) — viewBox 0 0 260 220
s,a=ring(130,92,left='O',lx=40)
c1=a[1]
s+=f'<line x1="{f(c1[1]+11)}" y1="{f(c1[2])}" x2="232" y2="{f(c1[2])}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
s+=f'<line x1="{f(40-12)}" y1="92" x2="12" y2="92" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
s+='<path d="M30 30 H20 V190 H30" fill="none" stroke="#16233D" stroke-width="2.5"/><path d="M216 30 H226 V190 H216" fill="none" stroke="#16233D" stroke-width="2.5"/>'
s+='<text class="tex" x="240" y="196" data-tex="n" data-size="24" data-anchor="middle"></text>'
OUT['XYLAN']=s
OUT['XYLOSE']=fischer(110,30,'CHO',boxtop=86)
OUT['XYLITOL']=fischer(110,30,'CH2OH',boxtop=118)
# S11 큰 피셔 두 개 (viewBox 0 0 600 300): 자일로스 cx 130, 자일리톨 cx 470
OUT['XY2']=fischer(130,36,'CHO',boxtop=86)+fischer(470,36,'CH2OH',boxtop=118)
# S10 축합: 위 반응 전 (y=90), 아래 반응 후 (y=300) viewBox 0 0 560 400
s1,_=ring(110,86,right='OH',left='HO',lx=24); s2,_=ring(410,86,left='HO',right='OH',rx=496)  # 끝 OH까지 그려 자일로스 하나 = C5H10O5
OUT['COND_BEFORE']=s1+s2
s3,_=ring(110,290,left='HO',lx=24); s4,a4=ring(330,290,right='OH',rx=416)
# 연결 O: C1(A)=(156,290), C4(B)=(284,290) → O at 220
s5=sf([('C',156,290),('O',220,290),('C',284,290)],[(0,1,1),(1,2,1)],22).split('<text')[0]  # 선만
OUT['COND_AFTER']=s3+s4+s5+'<text class="tex" x="220" y="297.9" data-tex="\\mathrm{O}" data-size="22" data-anchor="middle"></text>'
# S6 세 사슬 (viewBox 0 0 1080 200), d=54 S=24
OUT['CH_ETH']=chain_svg(2,'OH',30,120,d=54,S=24)
OUT['CH_ALD']=chain_svg(2,'CHO',400,120,d=54,S=24)
OUT['CH_ACE']=chain_svg(2,'COOH',720,120,d=54,S=24)
tpl=open(sys.argv[2],encoding='utf-8').read()
for k,v in OUT.items(): tpl=tpl.replace('{{'+k+'}}',v)
assert '{{' not in tpl, [l for l in tpl.split('\n') if '{{' in l][:3]
open(sys.argv[3],'w',encoding='utf-8').write(tpl)
print('ok',len(tpl))
