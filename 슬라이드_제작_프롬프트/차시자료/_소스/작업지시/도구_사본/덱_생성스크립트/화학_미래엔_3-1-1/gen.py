import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학_미래엔_3-1-1')
from h import *
OUT='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/3-1-1_가역_반응과_화학_평형/slides.html'
S=[]
def add(s): S.append(s)

SEC0='Ⅲ. 화학 평형'; SECI='01 가역 반응과 화학 평형'

# ---------- 1. 표지 ----------
cov=''
cov+='<circle cx="270" cy="250" r="240" fill="#EEF3F8"/>'
# 플라스크(둥근 바닥) 몸통 + 목
cov+='<path d="M240 60 V128 A132 132 0 1 0 300 128 V60 Z" fill="#B5562A" fill-opacity=".16"/>'
cov+='<path d="M240 60 V128 A132 132 0 1 0 300 128 V60" fill="none" stroke="#7E8B98" stroke-width="4" stroke-linejoin="round"/>'
cov+='<rect x="230" y="40" width="80" height="30" rx="5" fill="#C9B79C" stroke="#8C7A5E" stroke-width="2.5"/>'
mols=[('a',212,205,-60),('a',330,300,200),('a',205,330,30),('b',318,205,-25),('b',270,382,0)]
for i,(k,x,y,th) in enumerate(mols):
    body=no2(x,y,24,th,lab=True) if k=='a' else n2o4(x,y,24,th,lab=True)
    if i in (0,3):
        cov+=f'<g data-anim="move" data-from="{6 if i==0 else -6},{-5 if i==0 else 5}" data-rep="swing" data-dur="1.1">{body}</g>'
    else: cov+=body
cov+=f'<g data-anim="draw" data-dur="1" data-delay=".4">{eqarrows(225,472,90)}</g>'
cov+=tex(160,481,'\\ce{2NO2}',26,mix=False)
cov+=tex(380,481,'\\ce{N2O4}',26,mix=False)
add(f'''<!-- ════════ 1. 표지 ════════ -->
<section class="slide cover" data-sec="{SEC0}" data-title="표지">
  <div class="cover-text">
    <div class="kicker">Ⅲ. 화학 평형 › 1. 화학 평형 › 01</div>
    <h1 class="cm311-h1">가역 반응과<br><span class="acc">화학 평형</span></h1>
    <p class="sub">반응이 멈춘 듯 보여도, 정말 멈춘 것일까?</p>
    <p class="meta">고등학교 화학 (미래엔) 97–101쪽</p>
  </div>
  <svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="마개를 닫은 플라스크 속 이산화 질소 분자와 사산화 이질소 분자, 아래에 가역 반응 화살표">
    {cov}
  </svg>
</section>''')

# ---------- 2. 대단원 도입 ----------
u=''
# 패널 틀
for i,(t,c) in enumerate([('생명 현상','#D7263D'),('자연','#8C7A5E'),('산업','#1F6FD1')]):
    x0=8+i*372
    u+=f'<rect x="{x0}" y="4" width="352" height="212" rx="14" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="2"/>'
    u+=tex(x0+176,34,t,20,weight=700,fill=INK)
# 1 생명: 폐 ↔ 조직, 적혈구
u+='<rect x="26" y="60" width="96" height="86" rx="12" fill="#FDE2E4" stroke="#E7A3AC" stroke-width="2"/>'
u+='<rect x="242" y="60" width="96" height="86" rx="12" fill="#FBEFD9" stroke="#E2BE85" stroke-width="2"/>'
u+=tex(74,110,'폐',20,fill=INK,weight=700)
u+=tex(290,110,'몸의 조직',19,fill=INK,weight=700)
u+='<path d="M124 86 H240" stroke="#D7263D" stroke-width="2" stroke-dasharray="6 5" fill="none"/>'
u+='<path d="M240 124 H124" stroke="#7B4FC8" stroke-width="2" stroke-dasharray="6 5" fill="none"/>'
rbc=lambda x,y: f'<ellipse cx="{x}" cy="{y}" rx="20" ry="13" fill="#E05A5A" stroke="#A63434" stroke-width="2"/><ellipse cx="{x}" cy="{y}" rx="9" ry="5" fill="#C94848"/>'
u+=f'<g data-anim="move" data-from="-74,0" data-dur="1.6" data-delay=".5" data-ease="soft">{rbc(182,86)}{atom(205,68,9,"O","-")}{atom(217,68,9,"O","-")}</g>'
u+=rbc(182,124)
u+=tex(182,184,'헤모글로빈 + 산소 $\\ce{&lt;=&gt;}$||산소 헤모글로빈',18,fill=MUTED)
# 2 자연: 석회 동굴
x0=380
u+=f'<path d="M{x0+18} 52 H{x0+334} V200 H{x0+18} Z" fill="#E7E0D2"/>'
u+=f'<path d="M{x0+48} 196 Q{x0+60} 92 {x0+176} 84 Q{x0+292} 92 {x0+304} 196 Z" fill="#FBFAF6" stroke="#B9AB90" stroke-width="2"/>'
for (sx,L) in [(120,40),(150,56),(190,34),(232,48)]:
    u+=f'<path d="M{x0+sx-9} 92 L{x0+sx} {92+L} L{x0+sx+9} 92 Z" fill="#CDBF9F" stroke="#9C8F78" stroke-width="1.5"/>'
for (sx,L) in [(150,30),(232,22),(100,18)]:
    u+=f'<path d="M{x0+sx-12} 196 L{x0+sx} {196-L} L{x0+sx+12} 196 Z" fill="#CDBF9F" stroke="#9C8F78" stroke-width="1.5"/>'
u+=f'<g data-anim="move" data-from="0,-20" data-dur="1" data-delay=".6" data-rep="loop" data-ease="in"><ellipse cx="{x0+150}" cy="{160}" rx="3.5" ry="5" fill="#6FA8DC"/></g>'
u+=tex(x0+176,74,'녹고 다시 쌓인다',18,fill=MUTED)
# 3 산업: 공장
x0=752
u+=f'<rect x="{x0+40}" y="110" width="110" height="80" fill="#EEF2F6" stroke="#16233D" stroke-width="2.5"/>'
u+=f'<rect x="{x0+62}" y="60" width="18" height="50" fill="#EEF2F6" stroke="#16233D" stroke-width="2.5"/>'
u+=f'<rect x="{x0+168}" y="96" width="44" height="94" rx="20" fill="#E3EEFB" stroke="#16233D" stroke-width="2.5"/>'
u+=f'<rect x="{x0+228}" y="126" width="80" height="64" fill="#EEF2F6" stroke="#16233D" stroke-width="2.5"/>'
u+=f'<path d="M{x0+150} 150 H{x0+168} M{x0+212} 150 H{x0+228}" stroke="#16233D" stroke-width="3"/>'
u+=f'<g data-anim="move" data-from="0,14" data-dur="1.4" data-delay=".3" data-ease="out"><circle cx="{x0+71}" cy="48" r="7" fill="#C9D3DD"/><circle cx="{x0+82}" cy="38" r="9" fill="#DDE3EA"/></g>'
u+=tex(x0+176,214-12,'$\\ce{N2 + 3H2 &lt;=&gt; 2NH3}$',19,fill=INK)
u+=tex(x0+268,116,'암모니아',18,fill=MUTED)
add(f'''<!-- ════════ 2. 대단원 도입 ════════ -->
<section class="slide" data-sec="{SEC0} · 도입" data-title="대단원 도입: 화학 평형">
  <h2><span class="tag ink">대단원 도입</span>Ⅲ. 화학 평형</h2>
  <div class="std"><span class="code">이 단원의 핵심 아이디어</span>화학 반응이 진행될 때 정반응 속도와 역반응 속도가 같아지면 <b>화학 평형</b>에 도달한다.</div>
  <p class="f21 mt8">이 단원에서는 다양한 생명 현상을 이해하는 핵심 원리이며 산업에서 중요하게 쓰이는 화학 평형을 알아본다.</p>
  <svg class="fig mt12" viewBox="0 0 1112 220" style="width:1112px" aria-label="폐와 몸의 조직 사이에서 산소와 결합하고 내놓는 적혈구, 녹고 다시 쌓이는 석회 동굴, 암모니아 합성 공장">
    {u}
  </svg>
  <div class="card q mt12"><p class="f21" data-q><b>Q</b> 염전에서는 바닷물의 물을 햇볕에 증발시켜 소금을 얻는다. 바닷물을 유리병에 담아 <b>밀폐</b>한 뒤 햇볕이 잘 드는 곳에 두면, 염전에서처럼 소금을 얻을 수 있을까?</p>
    <p class="f21 step cm311-a">→ 얻기 어렵다. 밀폐된 병 속에서는 물이 증발하는 만큼 수증기가 다시 응축하여 물의 양이 일정하게 유지된다. 그 까닭을 이 단원에서 알아보자.</p></div>
</section>''')

# ---------- 3. 대단원 도입: 흐름 ----------
add(f'''<!-- ════════ 3. 단원의 흐름 ════════ -->
<section class="slide" data-sec="{SEC0} · 도입" data-title="단원의 흐름과 포트폴리오">
  <h2><span class="tag ink">대단원 도입</span>단원의 흐름</h2>
  <table class="tight cm311-map3">
    <tr><th style="width:230px">중단원</th><th>소단원</th><th style="width:150px">쪽</th></tr>
    <tr class="cm311-cur"><td rowspan="3"><b>1. 화학 평형</b></td><td class="l">01 가역 반응과 화학 평형</td><td><b>97쪽 (오늘)</b></td></tr>
    <tr><td class="l">02 화학 평형과 평형 상수</td><td>102쪽</td></tr>
    <tr><td class="l">03 화학 반응의 진행 방향 예측</td><td>106쪽</td></tr>
    <tr><td rowspan="3"><b>2. 화학 평형 이동</b></td><td class="l">01 농도·압력 변화와 화학 평형 이동</td><td>113쪽</td></tr>
    <tr><td class="l">02 온도 변화와 화학 평형 이동</td><td>120쪽</td></tr>
    <tr><td class="l">03 일상생활 속의 화학 평형 이동</td><td>124쪽</td></tr>
  </table>
  <h3 class="mt12">학습 연계</h3>
  <div class="flow">
    <div class="fnode"><b>중학교 과학</b><br><span class="small">화학 반응의 규칙성</span></div><div class="farr">→</div>
    <div class="fnode"><b>통합과학2</b><br><span class="small">변화와 다양성</span></div><div class="farr">→</div>
    <div class="fnode hl"><b>화학</b><br><span class="small">Ⅲ. 화학 평형 (지금)</span></div><div class="farr">→</div>
    <div class="fnode"><b>물질과 에너지 · 화학 반응의 세계</b><br><span class="small">화학 변화의 자발성 · 산 염기 평형</span></div>
  </div>
  <div class="note mt12"><b>포트폴리오</b> 이 단원을 배우며 나만의 특기를 발휘한 포트폴리오를 만들어 보자. — 108쪽 화학과 나의 미래 · 126쪽 생활 속 과학 이야기 · 134–135쪽 프로젝트</div>
</section>''')

# ---------- 4. 중단원 도입 ----------
b=''
b+='<path d="M150 330 C146 280 156 240 150 190" fill="none" stroke="#2E7D4F" stroke-width="6" stroke-linecap="round"/>'
b+='<path d="M150 270 C118 262 104 240 102 226 C126 228 144 246 150 270 Z" fill="#4CAF50"/>'
b+='<path d="M151 248 C180 236 196 216 198 202 C172 206 156 226 151 248 Z" fill="#4CAF50"/>'
petals=[(150,128,40),(116,146,34),(184,146,34),(128,176,32),(172,176,32),(150,156,30)]
for x,y,r in petals: b+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E46A9A" stroke="#B0436F" stroke-width="2"/>'
b+='<g data-anim="fade" data-dur="1" data-delay=".9" data-rep="alt">'+''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#5B7FD6" stroke="#3A57A8" stroke-width="2"/>' for x,y,r in petals[1:4:2])+'</g>'
b+='<path d="M262 96 Q232 112 214 132" fill="none" stroke="#9FC3DD" stroke-width="5" stroke-dasharray="8 6" stroke-linecap="round"/>'
b+='<path d="M270 128 Q240 140 222 156" fill="none" stroke="#9FC3DD" stroke-width="5" stroke-dasharray="8 6" stroke-linecap="round"/>'
b+=tex(266,80,'입김',20,fill='#1F6FD1',weight=700)
b+=tex(150,356,'온도에 따라 색이 변하는 장미',19,fill=MUTED)
add(f'''<!-- ════════ 4. 중단원 도입 ════════ -->
<section class="slide" data-sec="Ⅲ-1. 화학 평형 · 도입" data-title="중단원 도입: 화학 평형">
  <h2><span class="tag ink">중단원 도입</span>1. 화학 평형</h2>
  <div class="row">
    <div class="col">
      <div class="card q"><p class="f22" data-q>온도에 따라 색이 변하는 장미에 입김을 불면, 입김이 닿은 곳의 색이 변했다가 시간이 지나면 원래 색으로 되돌아온다. <b>Q</b> 우리 주변에 이렇게 변했다가 되돌아오는 것이 있을까?</p></div>
      <div class="row mt12" style="align-items:center"><div class="col" style="flex:0 0 250px"><p class="f21"><b>이전 학습 내용</b> 아는 것에 ✓</p></div><div class="col"><div class="chips"><button class="chk">화학 변화</button><button class="chk">반응물</button><button class="chk">생성물</button><button class="chk">화학 반응식</button></div></div></div>
      <table class="tight mt12 cm311-sub">
        <tr><th style="width:290px">소단원</th><th>배울 내용</th><th style="width:118px">쪽</th></tr>
        <tr class="cm311-cur"><td class="l">01 가역 반응과 화학 평형</td><td class="l">가역 반응과 동적 평형, 평형 상태의 특징</td><td><b>97 (오늘)</b></td></tr>
        <tr><td class="l">02 화학 평형과 평형 상수</td><td class="l">농도 자료로 평형 상수의 의미 설명</td><td>102</td></tr>
        <tr><td class="l">03 화학 반응의 진행 방향 예측</td><td class="l">반응 지수와 평형 상수 비교</td><td>106</td></tr>
      </table>
    </div>
    <div class="col" style="flex:0 0 330px">
      <svg class="fig" viewBox="0 0 330 360" style="width:300px" aria-label="입김이 닿은 꽃잎의 색이 변하는 장미">
        {b}
      </svg>
    </div>
  </div>
</section>''')

# ---------- 5. 학습 목표 ----------
add(f'''<!-- ════════ 5. 학습 목표 ════════ -->
<section class="slide" data-sec="{SECI}" data-title="학습 목표">
  <h2>학습 목표</h2>
  <div class="std"><span class="code">[12화학03-01]</span>가역 반응에서 나타나는 화학 평형 상태의 특징을 설명할 수 있다.</div>
  <ol class="goals mt12">
    <li>가역 반응에서 나타나는 <b>화학 평형 상태의 특징</b>을 설명할 수 있다.</li>
    <li>우리 주변에서 일어나는 <b>가역 반응</b>과 <b>비가역 반응</b>에 흥미와 호기심을 가질 수 있다.</li>
  </ol>
  <h3 class="mt16">오늘의 흐름</h3>
  <div class="flow">
    <div class="fnode">해 보기</div><div class="farr">→</div>
    <div class="fnode hl">가역·비가역 반응</div><div class="farr">→</div>
    <div class="fnode hl">동적 평형</div><div class="farr">→</div>
    <div class="fnode">모의실험</div><div class="farr">→</div>
    <div class="fnode hl">화학 평형</div>
  </div>
  <div class="card mt20"><h3>중단원 학습 목표 (1. 화학 평형)</h3>
    <p class="f21"><b>지식·이해</b> 가역 반응에서 나타나는 화학 평형 상태의 특징과 평형 상수의 의미를 설명할 수 있다.</p>
    <p class="f21"><b>과정·기능</b> 화학 반응에서 반응물과 생성물의 농도비의 규칙성을 추론할 수 있다.</p>
    <p class="f21"><b>가치·태도</b> 평형 상수와 반응 지수를 비교해 반응의 진행 방향을 예측하여 화학 평형의 유용성을 깨달을 수 있다.</p></div>
</section>''')

# ---------- 동굴 그림 ----------
def cave(x0,y0,s=1.0,drop=True,labels=True):
    T=lambda x,y:(x0+x*s,y0+y*s)
    def P(x,y): a,b=T(x,y); return f'{f(a)} {f(b)}'
    o=''
    a,b=T(0,40); o+=f'<rect x="{f(a)}" y="{f(b)}" width="{f(520*s)}" height="{f(290*s)}" fill="#E7E0D2"/>'
    o+=f'<path d="M{P(0,40)} H{f(T(520,0)[0])}" stroke="#7FB06A" stroke-width="{f(6*s)}"/>'
    # 빗물 스밈
    for xx in (120,330,430):
        o+=f'<path d="M{P(xx,44)} Q{P(xx+14,80)} {P(xx-4,118)}" fill="none" stroke="#6FA8DC" stroke-width="{f(2.5*s)}" stroke-dasharray="{f(6*s)} {f(5*s)}"/>'
    # 동굴 빈 곳
    o+=f'<path d="M{P(60,310)} Q{P(70,140)} {P(260,128)} Q{P(450,140)} {P(460,310)} Z" fill="#FBFAF6" stroke="#B9AB90" stroke-width="{f(2.5*s)}"/>'
    tips=[]
    for (sx,L) in [(170,58),(215,84),(262,44),(310,72),(360,40)]:
        top=136 if 150<sx<380 else 150
        o+=f'<path d="M{P(sx-12,top)} L{P(sx,top+L)} L{P(sx+12,top)} Z" fill="#CDBF9F" stroke="#9C8F78" stroke-width="{f(1.8*s)}"/>'
        tips.append((sx,top+L))
    for (sx,L) in [(215,50),(310,40),(150,26),(395,30)]:
        o+=f'<path d="M{P(sx-16,310)} L{P(sx,310-L)} L{P(sx+16,310)} Z" fill="#CDBF9F" stroke="#9C8F78" stroke-width="{f(1.8*s)}"/>'
    if drop:
        a,b=T(215,232)
        o+=f'<g data-anim="move" data-from="0,{f(-60*s)}" data-dur="1.1" data-delay=".5" data-rep="loop" data-ease="in"><ellipse cx="{f(a)}" cy="{f(b)}" rx="{f(4.5*s)}" ry="{f(6.5*s)}" fill="#6FA8DC"/></g>'
    if labels:
        o+=tex(*T(460,92),'빗물',19,fill='#1F6FD1',halo=True)
        o+=tex(*T(80,92),'석회암',19,fill=MUTED,halo=True)
        o+=tex(*T(330,236),'종유석',19,fill=INK,halo=True,anchor='start')
        o+=tex(*T(150,272),'석순',19,fill=INK,halo=True,anchor='end')
    return o

# ---------- 6. 생각 열기 ----------
add(f'''<!-- ════════ 6. 생각 열기 ════════ -->
<section class="slide" data-sec="{SECI} · 도입" data-title="생각 열기: 석회 동굴">
  <h2><span class="tag">생각 열기</span>석회암을 녹인 물이 다시 돌을 만든다?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 520px">
      <svg class="fig" viewBox="0 0 520 330" style="width:520px" aria-label="석회암 지대 아래의 동굴 단면, 천장의 종유석과 바닥의 석순, 떨어지는 물방울">
        {cave(0,0)}
      </svg>
    </div>
    <div class="col">
      <p class="f22">이산화 탄소가 녹은 빗물이 석회암 지대에 스며들면 석회암이 녹아 동굴이 생긴다. 그런데 그 동굴 천장에는 다시 돌고드름(<b>종유석</b>)이 자라고, 바닥에는 돌기둥(<b>석순</b>)이 쌓인다.</p>
      <p class="f22 mt12" data-q><b>Q</b> 석회암을 녹인 물이 다시 돌을 만드는 까닭은 무엇일까?</p>
      <div class="card mt8"><p class="f21"><b>(가)</b> 녹는 반응과 쌓이는 반응은 서로 관계없는 다른 반응이다.</p></div>
      <div class="card mt8"><p class="f21"><b>(나)</b> 같은 반응이 조건에 따라 앞으로도, 거꾸로도 일어난다.</p></div>
    </div>
  </div>
  <div class="answer step mt12"><b>(나)</b> — 같은 반응이 양쪽 방향으로 일어난다. 이런 반응을 <b>가역 반응</b>이라고 한다.</div>
</section>''')

# ---------- 7. 연결 ----------
R1H=18; R1O=24
def h2m(x,y): return atom(x-12,y,R1H,'H')+atom(x+12,y,R1H,'H')
def o2m(x,y): return atom(x-15,y,R1O,'O')+atom(x+15,y,R1O,'O')
c7=''
c7+='<rect x="6" y="10" width="220" height="200" rx="16" fill="#F7F9FB" stroke="#C9D3DD" stroke-width="2"/>'
c7+='<rect x="334" y="10" width="220" height="200" rx="16" fill="#F7F9FB" stroke="#C9D3DD" stroke-width="2"/>'
# before: H2 at (70,60),(150,150); O2 at (130,80)? choose
bH=[(66,62),(160,160)]; bO=(150,72)
c7+=h2m(*bH[0])+h2m(*bH[1])+o2m(*bO)
# after water molecules at (400,70) and (490,150) O center, H at 104.5
def water1(x,y,th=90):
    d=30; o=''
    for s in (-52.25,52.25):
        a=math.radians(th+s); o+=atom(x+d*math.cos(a),y+d*math.sin(a),R1H,'H')
    return o+atom(x,y,R1O,'O')
# animated: atoms move from before positions
afterW=[(400,62),(486,140)]
moves=[]
def wpos(x,y,th=90):
    d=30; hs=[]
    for s in (-52.25,52.25):
        a=math.radians(th+s); hs.append((x+d*math.cos(a),y+d*math.sin(a)))
    return hs
ha=wpos(*afterW[0]); hb=wpos(*afterW[1])
Hbefore=[(bH[0][0]-12,bH[0][1]),(bH[0][0]+12,bH[0][1]),(bH[1][0]-12,bH[1][1]),(bH[1][0]+12,bH[1][1])]
Hafter=[ha[0],ha[1],hb[0],hb[1]]
Obefore=[(bO[0]-15,bO[1]),(bO[0]+15,bO[1])]; Oafter=list(afterW)
for (b0,a0) in zip(Hbefore,Hafter):
    c7+=f'<g data-anim="move" data-from="{f(b0[0]-a0[0])},{f(b0[1]-a0[1])}" data-dur="1.4" data-delay=".6" data-ease="io">{atom(a0[0],a0[1],R1H,"H")}</g>'
for (b0,a0) in zip(Obefore,Oafter):
    c7+=f'<g data-anim="move" data-from="{f(b0[0]-a0[0])},{f(b0[1]-a0[1])}" data-dur="1.4" data-delay=".6" data-ease="io">{atom(a0[0],a0[1],R1O,"O")}</g>'
c7+=arw(244,110,316,110,'ink',3)
c7+=tex(116,238,'반응 전: $\\ce{H2}$ 2개, $\\ce{O2}$ 1개',19,fill=MUTED)
c7+=tex(444,238,'반응 후: $\\ce{H2O}$ 2개',19,fill=MUTED)
add(f'''<!-- ════════ 7. 연결 ════════ -->
<section class="slide" data-sec="{SECI} · 도입" data-title="지금까지 본 반응은 한 방향">
  <h2><span class="tag alt">연결</span>지금까지 본 반응은 한 방향이었다</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px">
      <svg class="fig" viewBox="0 0 560 250" style="width:560px" aria-label="수소 분자 두 개와 산소 분자 한 개가 반응하여 물 분자 두 개가 되는 입자 모형">
        {c7}
      </svg>
      <div class="formula sm mt8">$\\ce{{2H2 + O2 -> 2H2O}}$<div class="unit">원자 수: $\\mathrm{{H}}$ 4 = 4, $\\mathrm{{O}}$ 2 = 2</div></div>
    </div>
    <div class="col">
      <p class="f22">중학교에서 수소와 산소가 반응하여 물이 생기는 반응을 반응물 → 생성물 한 방향으로 나타냈다.</p>
      <p class="f22 mt12" data-q><b>Q</b> 생성물인 물이 저절로 다시 수소와 산소로 돌아갈 수 있을까?</p>
      <div class="card tip step mt12" data-g="a1"><p class="f21">보통 조건에서는 거의 일어나지 않는다. 물을 수소와 산소로 나누려면 전기 분해처럼 에너지를 따로 넣어 주어야 한다.</p></div>
      <div class="answer step mt12" data-g="a2">→ 그런데 어떤 반응은 생성물이 쉽게 반응물로 되돌아간다. 반응의 <b>방향</b>을 나누어 생각해 보자.</div>
    </div>
  </div>
</section>''')

# ---------- 8. 가역 반응 ----------
c8=''
L=24
# 왼쪽 NO2 두 개 → 오른쪽 N2O4
nA=(70,96); nB=(70,186)
c8+=no2(*nA,L,-90,lab=True)
c8+=no2(*nB,L,90,lab=True)
c8+=tex(70,150,'+',28,fill=INK)
c8+=eqarrows(160,141,160,lab_top='정반응',lab_bot='역반응',size=20)
# N2O4 at right; animated from two NO2 coming together
c8+=f'<g data-anim="pop" data-o="440,141" data-dur=".9" data-delay=".8" data-ease="back">{n2o4(440,141,L,0,lab=True)}</g>'
c8+=tex(70,272,'$\\ce{2NO2}$ (적갈색)',20,fill=NO2C)
c8+=tex(440,272,'$\\ce{N2O4}$ (무색)',20,fill=INK)
add(f'''<!-- ════════ 8. 가역 반응 ════════ -->
<section class="slide" data-sec="01 · 가역 반응과 비가역 반응" data-title="가역 반응">
  <h2><span class="no">1</span>가역 반응</h2>
  <p class="f22"><mark>정반응과 역반응이 모두 일어날 수 있는 반응</mark>을 <b>가역 반응</b>이라고 하고, 화살표 $\\ce{{&lt;=&gt;}}$로 나타낸다.</p>
  <div class="row mt12">
    <div class="col" style="flex:0 0 560px">
      <svg class="fig" viewBox="0 0 560 290" style="width:560px" aria-label="이산화 질소 분자 두 개가 결합하여 사산화 이질소가 되는 정반응과 그 역반응">
        {c8}
      </svg>
      <div class="formula sm">$\\ce{{2NO2(g) &lt;=&gt; N2O4(g)}}$</div>
    </div>
    <div class="col">
      <div class="card"><h3>용어</h3>
        <p class="f21"><b class="c-field">정반응</b> 반응물이 생성물로 되는 반응 (화학 반응식의 왼쪽 → 오른쪽)</p>
        <p class="f21 mt8"><b style="color:#7B4FC8">역반응</b> 생성물이 다시 반응물로 되는 반응 (오른쪽 → 왼쪽)</p>
        <p class="f21 mt8"><b>가역 반응</b> 정반응과 역반응이 모두 일어나는 반응</p>
      </div>
      <div class="note step mt12">가역 반응식에서도 왼쪽을 반응물, 오른쪽을 생성물이라고 부르지만, <b>두 방향의 반응이 모두</b> 일어난다.</div>
    </div>
  </div>
  <p class="small mt8">그림 범례: $\\mathrm{{N}}$ 파란 공, $\\mathrm{{O}}$ 빨간 공</p>
</section>''')

# ---------- 9. 해 보기: 황산 구리 ----------
def tube(cx,cy,fillc,rot=-10,crys=True,drops=False,lamp=False,dropper=False,warm=False):
    o=f'<g transform="rotate({rot} {cx} {cy})">'
    # 시험관: 입구 왼쪽, 바닥 오른쪽
    x0=cx-95; x1=cx+95; r=18
    o+=f'<path d="M{x0} {cy-r} H{x1-r} A{r} {r} 0 0 1 {x1-r} {cy+r} H{x0}" fill="#FFFFFF" fill-opacity=".6" stroke="{GLASS}" stroke-width="3"/>'
    if crys:
        o+=f'<path d="M{x1-70} {cy+r-2} Q{x1-60} {cy+2} {x1-40} {cy+4} Q{x1-20} {cy+2} {x1-r+8} {cy+r-6} A{r} {r} 0 0 1 {x1-r} {cy+r-1} Z" fill="{fillc}" stroke="#7E8B98" stroke-width="1"/>'
    if drops:
        for dx in (18,34,52):
            o+=f'<g data-anim="fade" data-dur=".6" data-delay="{1+dx/40:.1f}"><ellipse cx="{x0+dx}" cy="{cy+r-5}" rx="3.5" ry="3" fill="#6FA8DC"/></g>'
    o+='</g>'
    if lamp:
        lx=cx+50
        o+=f'<path d="M{lx-30} {cy+120} H{lx+30} L{lx+22} {cy+76} H{lx-22} Z" fill="#EEF2F6" stroke="#16233D" stroke-width="2.5"/>'
        o+=f'<rect x="{lx-4}" y="{cy+64}" width="8" height="12" fill="#8C99A6"/>'
        o+=f'<path d="M{lx} {cy+64} Q{lx-14} {cy+48} {lx} {cy+26} Q{lx+14} {cy+48} {lx} {cy+64} Z" fill="#F2A541" stroke="#E08A2C" stroke-width="1.5"/>'
    if dropper:
        dx,dy=dropper
        o+=f'<rect x="{dx-7}" y="{dy-40}" width="14" height="34" rx="6" fill="#E08A2C"/>'
        o+=f'<path d="M{dx-5} {dy-6} H{dx+5} L{dx+2} {dy+34} H{dx-2} Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/>'
        o+=f'<g data-anim="move" data-from="0,-22" data-dur=".9" data-delay=".5" data-rep="loop" data-ease="in"><ellipse cx="{dx}" cy="{dy+50}" rx="4" ry="5.5" fill="#6FA8DC"/></g>'
    return o
t1=tube(150,70,'#F4F6F8',drops=True,lamp=True)
t1+=tex(150,262,'흰색 가루 + 입구에 물방울',19,fill=INK)
t2=tube(140,138,'#3E8ED0',rot=90,dropper=(140,42))
t2+=tex(150,262,'다시 푸른색, 시험관이 따뜻해짐',19,fill=INK)
add(f'''<!-- ════════ 9. 해 보기: 황산 구리 ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기: 황산 구리(II) 오수화물">
  <h2><span class="tag">해 보기</span>황산 구리(II) 오수화물의 색 변화</h2>
  <div class="stages c2">
    <div class="stage"><h3>① 푸른색 결정을 가열한다</h3>
      <svg viewBox="0 0 300 272" style="height:220px" aria-label="기울인 시험관 속 흰색 가루를 알코올램프로 가열, 입구에 물방울">{t1}</svg></div>
    <div class="stage"><h3>② 식힌 흰색 가루에 물을 떨어뜨린다</h3>
      <svg viewBox="0 0 300 272" style="height:220px" aria-label="스포이트로 물을 떨어뜨리자 다시 푸른색이 된 시험관">{t2}</svg></div>
  </div>
  <div class="formula sm mt12 step" data-g="c1">$\\ce{{CuSO4*5H2O(s) &lt;=&gt; CuSO4(s) + 5H2O(g)}}$
    <div class="unit"><span class="c-field"><b>정반응</b>(가열): 푸른색 → 흰색</span> &nbsp;·&nbsp; <span style="color:#7B4FC8"><b>역반응</b>(물 첨가): 흰색 → 푸른색</span></div></div>
  <div class="note q mt12"><b>안전</b> 보안경·장갑을 쓰고, 시험관 입구는 사람이 없는 쪽으로 약간 아래로 향하게 한다. 남은 황산 구리(II)는 중금속 폐액통에 모은다.</div>
</section>''')

exec(open('/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학_미래엔_3-1-1/gen2.py').read())
open(OUT,'w').write('\n\n'.join(S)+'\n')
print('ok',len(S))
