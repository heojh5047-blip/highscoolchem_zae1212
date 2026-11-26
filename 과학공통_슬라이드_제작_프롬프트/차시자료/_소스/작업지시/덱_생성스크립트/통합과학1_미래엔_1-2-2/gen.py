# 1-2-2 그래프 path 계산 → slides.html 생성 (python gen.py)
import math, os
H=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(H,'../../../content/통합과학1_미래엔/1-2-2_신호와_정보/slides.html')
# 6장: 햇빛 세기 I=100 sin(pi(t-6)/12), 6<=t<=18, x=60+20t, y=250-1.9I
sun=['M60.0 250.0','L180.0 250.0']+[f"L{60+20*t:.1f} {250-1.9*100*math.sin(math.pi*(t-6)/12):.1f}" for t in [6+i*0.25 for i in range(1,48)]]+['L420.0 250.0','L540.0 250.0']
# 8장: f=50+40 sin(2 pi t/8), x=60+55t, y=250-2f / 디지털: 1초마다 10 단위로 반올림한 값을 1초 동안 유지
f=lambda t:50+40*math.sin(2*math.pi*t/8)
ana='M'+' L'.join(f"{60+55*t:.1f} {250-2*f(t):.1f}" for t in [i/20 for i in range(161)])
dig=' '.join(f"M{60+55*k:.1f} {250-2*round(f(k)/10)*10:.1f} L{60+55*(k+1):.1f} {250-2*round(f(k)/10)*10:.1f}" for k in range(8))
s=open(os.path.join(H,'slides.src.html'),encoding='utf-8').read()
s=s.replace('{SUN}',' '.join(sun)).replace('{ANA}',ana).replace('{DIG}',dig)
open(OUT,'w',encoding='utf-8').write(s); print('written')
