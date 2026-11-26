# 3-3 화학 변화의 자발성 slides.html 생성기 (그림 좌표 계산)
import random, math, sys
OUT = sys.argv[1]
INK='#16233D'; MUT='#5B6B7F'; GL='#7E8B98'; WAT='#DDEEF8'; BLU='#3F7FD6'; GRV='#C9D2DC'
FLD='#2E9E6A'; EQU='#E08A2C'; BF='#7B4FC8'; PLUS='#D7263D'; MINUS='#1F6FD1'

def T(x,y,s,size=22,anchor=None,fill=None,halo=False,w=None,tex=False,cls='',g=None):
    a=f'<text class="tex{(" "+cls) if cls else ""}" x="{x:.0f}" y="{y:.0f}" {"data-tex" if tex else "data-mix"}="{s}" data-size="{size}"'
    if anchor: a+=f' data-anchor="{anchor}"'
    if halo: a+=' data-halo="1"'
    if w: a+=f' data-weight="{w}"'
    if g: a+=f' data-g="{g}"'
    if fill: a+=f' fill="{fill}"'
    return a+'></text>'
def A(x1,y1,x2,y2,col='ink',w=3,d=False,extra=''):
    return f'<g data-arw="{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f},{col},{w}{",d" if d else ""}"{extra}></g>'
def C(x,y,r,fill,stroke=None,sw=1.5,extra=''):
    s=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}"{s}{extra}/>'
def beaker(x,y,w,h,water=None):
    s=''
    if water is not None:
        s+=f'<path d="M{x+3} {y+water} L{x+3} {y+h-12} Q{x+3} {y+h-3} {x+12} {y+h-3} L{x+w-12} {y+h-3} Q{x+w-3} {y+h-3} {x+w-3} {y+h-12} L{x+w-3} {y+water} Z" fill="{WAT}"/>'
    s+=f'<path d="M{x-8} {y} Q{x} {y} {x} {y+8} L{x} {y+h-12} Q{x} {y+h} {x+12} {y+h} L{x+w-12} {y+h} Q{x+w} {y+h} {x+w} {y+h-12} L{x+w} {y}" fill="none" stroke="{GL}" stroke-width="3"/>'
    return s
def scatter(rng,n,x0,y0,x1,y1,dmin,tries=4000):
    pts=[]
    for _ in range(tries):
        if len(pts)>=n: break
        p=(rng.uniform(x0,x1),rng.uniform(y0,y1))
        if all((p[0]-q[0])**2+(p[1]-q[1])**2>=dmin*dmin for q in pts): pts.append(p)
    return pts
def grid(nx,ny,x0,y0,dx,dy):
    return [(x0+i*dx,y0+j*dy) for j in range(ny) for i in range(nx)]
def mv(inner,dx,dy,dur=1.4,delay=0,rep=None,ease=None,on=None):
    s=f'<g data-anim="move" data-from="{dx:.0f},{dy:.0f}" data-dur="{dur}"'
    if delay: s+=f' data-delay="{delay}"'
    if rep: s+=f' data-rep="{rep}"'
    if ease: s+=f' data-ease="{ease}"'
    if on: s+=f' data-on="{on}"'
    return s+'>'+inner+'</g>'

def tug(Hd,Hl,Hlab,Sd,Sl,Slab,W=520,Hh=150,gH=None,gS=None,lab=20):
    """줄다리기 그림: 오른쪽 = 자발적 방향. Hd/Sd = +1(오른쪽) / -1(왼쪽), 길이 = 영향의 크기(정성)."""
    cx=W/2; y1=48; y2=104
    s=f'<line x1="{cx}" y1="10" x2="{cx}" y2="{y2+16}" stroke="{MUT}" stroke-width="2" stroke-dasharray="6 5"/>'
    def row(d,l,labt,y,col,colh,g):
        st=f' class="step" data-g="{g}"' if g else ''
        x2=cx+d*l
        lx=cx+8 if d>0 else cx-8; an='start' if d>0 else 'end'
        return f'<g{st}>{A(cx,y,x2,y,col,6)}{T(lx,y-14,labt,lab,an,colh,True)}</g>'
    s+=row(Hd,Hl,Hlab,y1,'equi','#B35F0F',gH)
    s+=row(Sd,Sl,Slab,y2,'bfield',BF,gS)
    s+=T(8,Hh-8,'← 비자발적 방향',19,'start',MUT)+T(W-8,Hh-8,'자발적 방향 →',19,'end',MUT)
    return s

S=[]
def add(h): S.append(h)

# ───────── 1 표지
rng=random.Random(3)
left=grid(3,3,95,225,40,40); right=scatter(rng,9,330,200,470,345,40)
pts=''.join(C(x,y,14,BLU,'#2457A6',2) for x,y in left)
ptr=''.join(mv(C(x,y,14,BLU,'#2457A6',2),(400-x)*0.6,(272-y)*0.6,1.6,0.3,ease='out') for x,y in right)
add(f'''<!-- ════════ 1. 표지 ════════ -->
<section class="slide cover" data-sec="Ⅲ. 화학 변화의 자발성" data-title="표지">
  <div class="cover-text">
    <div class="kicker">Ⅲ. 화학 변화의 자발성 › 03</div>
    <h1>화학 변화의<br><span class="acc">자발성</span></h1>
    <p class="sub">저절로 일어나는 변화는 어느 방향으로 진행할까?</p>
    <p class="meta">고등학교 물질과 에너지 80–85쪽</p>
  </div>
  <svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="규칙적으로 모여 있던 입자들이 흩어지면서 엔트로피가 증가하는 모습">
    <circle cx="270" cy="270" r="250" fill="#EEF3F8"/>
    <rect x="66" y="196" width="148" height="148" rx="14" fill="#fff" stroke="#9FB0C2" stroke-width="3"/>
    <rect x="316" y="182" width="170" height="176" rx="14" fill="#fff" stroke="#9FB0C2" stroke-width="3"/>
    {pts}{ptr}
    {A(226,270,304,270,'field',5)}
    {T(265,250,'엔트로피 증가',22,'middle',FLD,w=700)}
    {T(265,304,'\\Delta S&gt;0',24,'middle',FLD,tex=True)}
    {T(140,384,'질서 있는 상태',22,'middle',INK)}
    {T(401,396,'무질서한 상태',22,'middle',INK)}
  </svg>
</section>''')

# ───────── 2 목표
add('''<!-- ════════ 2. 학습 목표 ════════ -->
<section class="slide" data-sec="03 화학 변화의 자발성" data-title="학습 목표">
  <h2>학습 목표</h2>
  <div class="std"><span class="code">[12물에03-03]</span>엔트로피의 의미를 이해하고, 엔탈피와 엔트로피의 변화로 화학 변화의 자발성을 설명할 수 있다.</div>
  <ol class="goals mt12">
    <li><b>엔트로피</b>의 의미를 설명할 수 있다.</li>
    <li><b>엔탈피와 엔트로피 변화</b>로 화학 변화의 자발성을 설명할 수 있다.</li>
  </ol>
  <h3 class="mt16">오늘의 흐름</h3>
  <div class="flow">
    <div class="fnode">자발적 변화</div><div class="farr">→</div>
    <div class="fnode hl">엔트로피 (무질서도·확률)</div><div class="farr">→</div>
    <div class="fnode">엔트로피 변화 $\\Delta S$</div><div class="farr">→</div>
    <div class="fnode hl">엔탈피·엔트로피와 자발성</div>
  </div>
  <div class="note mt16"><b>연계</b> 01에서 발열 반응은 $\\Delta H&lt;0$, 흡열 반응은 $\\Delta H&gt;0$임을 배웠다. 오늘은 엔탈피와 함께 <b>엔트로피</b>로 반응이 저절로 일어날지 판단한다.</div>
</section>''')

# ───────── 3 생각 열기 (사탕 병)
def jar(x,y,colors,shake=False):
    s=f'<rect x="{x+18}" y="{y}" width="124" height="22" rx="6" fill="#D9C7A7" stroke="#A88E62" stroke-width="2"/>'
    s+=f'<path d="M{x+22} {y+22} L{x+22} {y+34} Q{x} {y+40} {x} {y+64} L{x} {y+226} Q{x} {y+246} {x+20} {y+246} L{x+140} {y+246} Q{x+160} {y+246} {x+160} {y+226} L{x+160} {y+64} Q{x+160} {y+40} {x+138} {y+34} L{x+138} {y+22}" fill="#F7FBFE" stroke="{GL}" stroke-width="3"/>'
    c=''
    k=0
    for j in range(6):
        for i in range(6):
            cx=x+20+i*24+(12 if j%2 else 0)-6; cy=y+104+j*23
            col=colors[k]; k+=1
            c+=C(cx,cy,11,'#F28AB2' if col=='p' else '#F6CF3F','#C2577F' if col=='p' else '#C9A11E',1.5)
    if shake:
        return s+f'<g data-anim="rot" data-from="6" data-o="{x+80},{y+180}" data-rep="damp" data-dur="1.6" data-delay=".4">{c}</g>'
    return s+c
lay=['p']*18+['y']*18
mix=lay[:]; random.Random(7).shuffle(mix)
add(f'''<!-- ════════ 3. 생각 열기 ════════ -->
<section class="slide" data-sec="03 화학 변화의 자발성 · 도입" data-title="생각 열기: 섞인 사탕">
  <h2><span class="tag">생각 열기</span>흔들어 섞은 사탕, 다시 두 층으로 나뉠까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 520px">
      <svg class="fig" viewBox="0 0 520 330" style="width:520px" aria-label="분홍색 사탕과 노란색 사탕이 두 층으로 나뉜 병을 흔들면 사탕이 무질서하게 섞인다">
        {jar(20,24,lay)}{jar(340,24,mix,True)}
        {A(200,150,316,150,'ink',3)}
        {T(258,136,'흔든다',20,'middle')}
        {T(100,312,'(가) 흔들기 전',20,'middle')}
        {T(420,312,'(나) 흔든 뒤',20,'middle')}
      </svg>
    </div>
    <div class="col">
      <p class="f22">유리병에 분홍색 사탕과 노란색 사탕을 넣고 흔들면 사탕이 <b>무질서하게 섞인다</b>.</p>
      <p class="f22 mt16"><b>Q</b> 계속 흔들다 보면 사탕이 다시 두 층으로 나뉠 수도 있을까?</p>
      <div class="em33-pick mt12">
        <div class="card">㉠ 언젠가는<br>나뉜다</div><div class="card">㉡ 거의<br>나뉘지 않는다</div><div class="card">㉢ 모르겠다</div>
      </div>
      <div class="note puzzle mt16 step" data-ask="no">섞인 배열의 가짓수가 두 층 배열보다 훨씬 많아서, 흔들수록 <b>섞인 상태</b>가 될 가능성이 압도적으로 크다. 오늘 <b>확률</b>과 <b>엔트로피</b>로 설명해 보자.</div>
    </div>
  </div>
</section>''')

# ───────── 4 연결: 흡열인데 저절로?
add(f'''<!-- ════════ 4. 연결 ════════ -->
<section class="slide" data-sec="03 화학 변화의 자발성 · 도입" data-title="연결: 흡열 반응도 저절로?">
  <h2><span class="tag alt">연결</span>발열 반응만 저절로 일어날까?</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>01·02에서 배운 것</h3>
        <p class="f21">물질은 엔탈피가 낮을수록 안정하다.</p>
        <p class="f21 mt8">→ 엔탈피가 낮아지는 <b>발열 반응</b>($\\Delta H&lt;0$)은 저절로 잘 일어난다.</p>
        <p class="f21 mt8">예: 메테인의 연소 $\\Delta H=-890\\ \\text{{kJ}}$, 철의 부식</p>
      </div>
    </div>
    <div class="col" style="flex:0 0 520px">
      <div class="card em33-cool"><h3>그런데…</h3>
        <svg class="fig" viewBox="0 0 480 170" style="width:470px" aria-label="휴대용 냉각 팩을 누르면 질산 암모늄이 물에 녹으면서 주위의 열을 흡수해 차가워진다">
          <rect x="140" y="30" width="200" height="120" rx="22" fill="#E3EEFB" stroke="#7FA6D6" stroke-width="3"/>
          <rect x="166" y="56" width="74" height="68" rx="10" fill="#fff" stroke="#9FB0C2" stroke-width="2"/>
          {''.join(C(178+i*16,74+j*16,5,'#F4F1EA','#B9AE96',1.2) for i in range(4) for j in range(3))}
          <rect x="252" y="56" width="62" height="68" rx="10" fill="{WAT}" stroke="#9FC3DD" stroke-width="2"/>
          {T(203,146,'질산 암모늄',19,'middle',INK)}{T(283,146,'물',19,'middle',INK)}
          <g data-anim="fade" data-dur=".8" data-delay=".5">{A(40,60,128,78,'equi',4)}{A(40,120,128,104,'equi',4)}{A(440,60,352,78,'equi',4)}{A(440,120,352,104,'equi',4)}</g>
          {T(30,30,'열 흡수',20,'start','#B35F0F',w=700)}
          {T(240,22,'휴대용 냉각 팩',20,'middle',INK,w=700)}
        </svg>
        <p class="f21">질산 암모늄이 물에 녹는 과정은 <b>흡열</b>($\\Delta H&gt;0$)인데도, 팩을 누르기만 하면 <b>저절로</b> 일어난다.</p>
      </div>
    </div>
  </div>
  <p class="f22 mt12"><b>Q</b> 흡열 반응도 저절로 일어날 수 있을까?</p>
  <div class="answer step">그렇다 — 반응의 방향을 정하는 요인은 엔탈피 하나가 아니다. 또 하나의 요인 = <b>엔트로피</b></div>
</section>''')

# ───────── 5 자발적 변화
drops=''.join(mv(C(x,y,6,'#FFFFFF','#5E9BD1',1.5),0,-40,1.2,0.3+i*0.25,rep='loop',ease='in') for i,(x,y) in enumerate([(422,110),(425,140),(428,170)]))
add(f'''<!-- ════════ 5. 자발적 변화 ════════ -->
<section class="slide" data-sec="03 · 자발적 변화와 엔트로피" data-title="자발적 변화">
  <h2><span class="no">1</span>자발적 변화</h2>
  <p class="f22">열은 온도가 높은 곳에서 낮은 곳으로 이동하고, 물은 위에서 아래로 흐른다. 이처럼 <mark>외부의 지속적인 도움 없이 스스로 일어나는 변화를 <b>자발적 변화</b></mark>라고 한다.</p>
  <div class="row mt12">
    <div class="col" style="flex:0 0 600px">
      <svg class="fig" viewBox="0 0 600 240" style="width:600px" aria-label="뜨거운 물체에서 차가운 물체로 열이 이동하고, 물은 높은 곳에서 낮은 곳으로 흐른다">
        <rect x="10" y="10" width="270" height="220" rx="12" fill="#fff" stroke="#D5DCE3" stroke-width="2"/>
        <rect x="320" y="10" width="270" height="220" rx="12" fill="#fff" stroke="#D5DCE3" stroke-width="2"/>
        <rect x="30" y="70" width="90" height="90" rx="8" fill="#FDE2E4" stroke="#D7263D" stroke-width="2.5"/>
        <rect x="170" y="70" width="90" height="90" rx="8" fill="#E3EEFB" stroke="#1F6FD1" stroke-width="2.5"/>
        <g data-anim="move" data-from="-30,0" data-dur="1" data-rep="loop" data-ease="lin">{A(102,115,186,115,'equi',5)}</g>
        {T(145,100,'열',20,'middle','#B35F0F',True,700)}
        {T(75,190,'뜨거운 물체',20,'middle')}{T(215,190,'차가운 물체',20,'middle')}
        {T(145,42,'열의 이동',21,'middle',INK,w=700)}
        <path d="M334 78 L410 78 L410 222 L334 222 Z" fill="#D8CBAE"/>
        <path d="M410 196 L576 196 L576 222 L410 222 Z" fill="#D8CBAE"/>
        <path d="M334 66 L404 66 Q416 66 418 80 L426 186 L576 186 L576 196 L410 196 L410 78 L334 78 Z" fill="#9CC9EE"/>
        <path d="M404 66 Q416 66 418 80 L426 186" fill="none" stroke="#5E9BD1" stroke-width="3"/>
        {drops}
        {A(470,160,540,160,'muted',3)}
        {T(504,146,'아래로 흐름',19,'middle',INK)}
        {T(372,104,'높은 곳',19,'middle',INK)}
        {T(455,42,'물의 흐름',21,'middle',INK,w=700)}
      </svg>
    </div>
    <div class="col">
      <div class="card tip"><h3>비자발적 변화</h3>
        <p class="f21">물이 수소와 산소로 분해되는 현상은 자발적이지 않다.</p>
        <div class="formula sm em33-fs">$\\ce{{2H2O(l) -> 2H2(g) + O2(g)}}$</div>
        <p class="f21">전류를 흘려 주면 분해되지만, 전류가 공급되지 않으면 분해되지 않는다.</p>
      </div>
    </div>
  </div>
  <p class="f22 mt12"><b>Q</b> 열이 차가운 물체에서 뜨거운 물체로 저절로 이동할 수 있을까?</p>
  <div class="answer step">없다 — 자발적 변화의 <b>반대 방향</b>은 저절로 일어나지 않는다.</div>
</section>''')

# ───────── 6 해 보기: 자발적 변화의 특징
rng=random.Random(11)
sm=scatter(rng,14,30,24,370,120,34)
smell=''.join(mv(C(x,y,7,'#C2410C',None),(200-x)*0.85,(150-y)*0.85,1.8,0.2+0.05*i,ease='out') for i,(x,y) in enumerate(sm))
ink_pts=scatter(random.Random(5),16,148,40,272,152,26)
ink=''.join(mv(C(x,y,7,BLU),(210-x)*0.8,(58-y)*0.8,1.8,0.2+0.05*i,ease='out') for i,(x,y) in enumerate(ink_pts))
add(f'''<!-- ════════ 6. 해 보기: 자발적 변화의 특징 ════════ -->
<section class="slide" data-sec="03 · 해 보기" data-title="해 보기: 자발적 변화의 특징">
  <h2><span class="tag">해 보기</span>자발적 변화의 특징 알아보기</h2>
  <div class="row">
    <div class="col" style="flex:0 0 420px">
      <svg class="fig" viewBox="0 0 400 200" style="width:400px" aria-label="(가) 접시 위 음식의 냄새 분자가 공기 중으로 퍼져 나간다">
        <rect x="4" y="4" width="392" height="192" rx="12" fill="#FFFBF5" stroke="#E5D8C2" stroke-width="2"/>
        <path d="M110 160 Q200 186 290 160 Z" fill="#E8DCC8" stroke="#B9A884" stroke-width="2"/>
        <ellipse cx="200" cy="158" rx="70" ry="10" fill="#A0522D"/>
        {smell}
        {T(14,188,'(가) 냄새가 공기 중으로 퍼져 나간다',19,'start')}
      </svg>
      <svg class="fig mt8" viewBox="0 0 400 200" style="width:400px" aria-label="(나) 물에 떨어뜨린 잉크가 물속으로 퍼져 나간다">
        {beaker(140,20,140,150,8)}
        {ink}
        {T(14,192,'(나) 잉크가 물속으로 퍼져 나간다',19,'start')}
      </svg>
    </div>
    <div class="col">
      <p class="f21" data-q><b>1</b> (가)와 (나)에서 일어나는 현상의 공통점을 입자의 관점에서 설명해 보자.</p>
      <p class="f21 step em33-a">→ <span class="ans">좁은 곳에 모여 있던 입자들이 넓은 공간으로 퍼져 나가 점점 더 무질서한 상태가 된다.</span></p>
      <p class="f21 mt12" data-q><b>2</b> (가)와 (나)에서와는 반대로 냄새나 잉크가 한쪽으로 다시 모이는 현상이 일어날 수 있는지 토의해 보자.</p>
      <p class="f21 step em33-a">→ <span class="ans">저절로는 일어나지 않는다. 퍼진 입자들이 한곳에 다시 모일 확률은 매우 작다.</span></p>
      <p class="f21 mt12" data-q><b>3</b> 일상생활에서 관찰할 수 있는 자발적 변화의 예를 더 찾아보자.</p>
      <p class="f21 step em33-a">→ <span class="ans">얼음이 실온에서 녹는다, 나무가 탄다, 각설탕이 물에 녹는다, 철이 녹슨다</span></p>
    </div>
  </div>
</section>''')

# ───────── 7 무질서해지는 변화 (그림 Ⅲ-4)
rng=random.Random(21)
solvL=scatter(random.Random(2),26,52,70,228,234,30);
cl=scatter(rng,18,64,188,150,232,17)
sp=scatter(random.Random(9),18,402,70,578,232,32)
def solv(pts,dx=0): return ''.join(C(x+dx,y,6,'#E3E8EE','#C9D2DC',1) for x,y in pts)
cl_s=''.join(C(x,y,8,BLU,'#2457A6',1.5) for x,y in cl)
sp_s=''.join(mv(C(x,y,8,BLU,'#2457A6',1.5),(107-x)+(x-490)*0.15,(210-y)*0.9,1.8,0.3,ease='out') for (x,y) in sp)
add(f'''<!-- ════════ 7. 무질서해지는 변화 ════════ -->
<section class="slide" data-sec="03 · 자발적 변화와 엔트로피" data-title="무질서해지는 변화">
  <h2><span class="no">1</span>무질서해지는 변화는 자발적이다</h2>
  <div class="row">
    <div class="col" style="flex:0 0 640px">
      <svg class="fig" viewBox="0 0 640 290" style="width:640px" aria-label="용질 입자가 한쪽에 모여 있는 비커에서 용질이 고르게 퍼진 비커로 가는 것은 자발적 변화이고, 반대는 비자발적 변화이다">
        {beaker(40,50,200,200,16)}{beaker(390,50,200,200,16)}
        {solv(solvL)}{solv(solvL,350)}
        {cl_s}{sp_s}
        {A(262,120,370,120,'field',5)}{A(370,176,262,176,'muted',5)}
        {T(316,100,'자발적 변화',20,'middle','#1B7A4E',w=700)}
        {T(316,210,'비자발적 변화',20,'middle',MUT,w=700)}
        {T(140,280,'용질 입자가 모여 있음',19,'middle')}{T(490,280,'고르게 퍼짐',19,'middle')}
        <circle cx="200" cy="30" r="8" fill="{BLU}"/>{T(214,37,'용질',19,'start')}
        <circle cx="290" cy="30" r="6" fill="#E3E8EE" stroke="#C9D2DC"/>{T(302,37,'용매',19,'start')}
      </svg>
    </div>
    <div class="col">
      <p class="f21">냄새 분자가 공기 중으로, 잉크 분자가 물속으로 퍼져 나갈 때 점점 더 <b>무질서한 상태</b>가 된다.</p>
      <p class="f21 mt8">이처럼 무질서해지는 변화는 <b>자발적</b>으로 일어나지만, 그 반대의 현상은 자발적으로 일어나지 않는다.</p>
      <div class="note mt12"><b>오개념 바로잡기</b> 자발적 변화가 냄새나 잉크가 확산하는 것처럼 항상 빠르게 일어나는 것은 아니다. 철이 부식되는 것처럼 <b>천천히</b> 진행되는 자발적 변화도 있다.</div>
    </div>
  </div>
  <p class="f22 mt8"><b>Q</b> 자발적 변화라면 빠르게 일어날까?</p>
  <div class="answer step">아니다 — 자발성은 변화의 <b>방향</b>, 빠르기는 <b>반응 속도</b>(Ⅳ 단원)의 문제이다.</div>
</section>''')

# ───────── 8 엔트로피
cols=['#F28AB2','#6FA8DC','#F6CF3F','#7FCB9A','#C79BE0','#F4A261']
lined=grid(4,3,48,60,44,48)
scat=scatter(random.Random(4),12,296,40,496,180,40)
p8=''.join(C(x,y,15,cols[i%6],'#5B6B7F',1.5) for i,(x,y) in enumerate(lined))
p8r=''.join(mv(C(x,y,15,cols[i%6],'#5B6B7F',1.5),(lined[i][0]+250-x)*0.7,(lined[i][1]-y)*0.7,1.6,0.3,ease='out') for i,(x,y) in enumerate(scat))
add(f'''<!-- ════════ 8. 엔트로피 ════════ -->
<section class="slide" data-sec="03 · 자발적 변화와 엔트로피" data-title="엔트로피">
  <h2><span class="no">2</span>엔트로피 — 무질서도의 척도</h2>
  <p class="f22">오랜 기간 수많은 관찰을 통해 과학자들은 자발적 변화에서 공통적으로 <b>엔트로피</b>라고 부르는 성질이 증가하는 경향이 있음을 알게 되었다.</p>
  <div class="formula mt12" style="text-align:left"><mark><b>엔트로피</b>(entropy)란 무질서도를 나타내는 척도로, 기호 $S$로 표시한다.</mark></div>
  <div class="row mt12">
    <div class="col" style="flex:0 0 540px">
      <svg class="fig" viewBox="0 0 540 230" style="width:540px" aria-label="줄을 맞춰 선 사람들이 흩어지면 질서 있는 상태에서 무질서한 상태가 되어 엔트로피가 증가한다">
        <rect x="18" y="26" width="196" height="160" rx="12" fill="#fff" stroke="#D5DCE3" stroke-width="2"/>
        <rect x="280" y="20" width="236" height="176" rx="12" fill="#fff" stroke="#D5DCE3" stroke-width="2"/>
        {p8}{p8r}
        {A(222,106,270,106,'field',5)}
        {T(116,216,'질서 있는 상태',19,'middle')}{T(398,222,'무질서한 상태',19,'middle')}
      </svg>
    </div>
    <div class="col">
      <p class="f21">엔트로피가 <b>증가</b>한다 = 질서 있는 상태에서 무질서한 상태가 된다.</p>
      <p class="f21 mt12"><b>Q</b> 자연계의 변화는 왜 무질서해지는 방향으로 진행할까?</p>
      <div class="answer step em33-left">확률과 관계가 있다 — 어떤 상태가 무질서해진다는 것은 그 상태로 존재할 <b>확률이 크다</b>는 뜻이다.</div>
    </div>
  </div>
</section>''')

# ───────── 9 동전 4개
counts=[1,4,6,4,1]; X0=70; BW=70; GAP=26; Y0=250; SC=26
bars=''
for k,c in enumerate(counts):
    x=X0+k*(BW+GAP); h=c*SC
    st='#B35F0F' if k in (0,4) else '#2457A6'
    fill='#FCE6CF' if k in (0,4) else '#CFE0F5'
    bars+=f'<g data-anim="scale" data-from="1,0" data-o="{x+BW/2},{Y0}" data-dur="1" data-delay="{0.2+0.15*k}"><rect x="{x}" y="{Y0-h}" width="{BW}" height="{h}" fill="{fill}" stroke="{st}" stroke-width="2.5"/></g>'
    bars+=T(x+BW/2,Y0-h-10,str(c),22,'middle',INK,w=700)
    bars+=T(x+BW/2,Y0+28,str(k),21,'middle')
add(f'''<!-- ════════ 9. 무질서도와 확률 ════════ -->
<section class="slide" data-sec="03 · 자발적 변화와 엔트로피" data-title="무질서도와 확률: 동전 4개">
  <h2><span class="no">2</span>무질서도와 확률 — 동전 4개 던지기</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px">
      <p class="f21">동전 4개를 동시에 던지면 나올 수 있는 경우는 $2^4=16$가지이다.</p>
      <svg class="fig mt8" viewBox="0 0 560 320" style="width:520px" aria-label="동전 4개를 던질 때 앞면의 수 0, 1, 2, 3, 4가 나오는 경우의 수는 1, 4, 6, 4, 1이다">
        <line x1="50" y1="{Y0}" x2="540" y2="{Y0}" stroke="{MUT}" stroke-width="2.5"/>
        {bars}
        {T(300,310,'앞면의 수',20,'middle',MUT)}
        {T(30,24,'경우의 수',20,'start',MUT)}
        {T(105,150,'모두||뒷면',19,'middle','#B35F0F')}{T(489,150,'모두||앞면',19,'middle','#B35F0F')}
        {T(297,40,'앞면과 뒷면이 섞임',20,'middle','#2457A6',w=700)}
      </svg>
    </div>
    <div class="col">
      <p class="f21" data-q>모두 같은 면이 나올 확률은?</p>
      <div class="formula sm step">$\\dfrac{{1+1}}{{16}}=\\dfrac{{2}}{{16}}=\\dfrac{{1}}{{8}}$</div>
      <p class="f21 mt8" data-q>앞면과 뒷면이 섞여 나올 확률은?</p>
      <div class="formula sm step">$\\dfrac{{4+6+4}}{{16}}=\\dfrac{{14}}{{16}}=\\dfrac{{7}}{{8}}$</div>
      <p class="f21 mt8"><b>Q</b> 동전의 개수가 늘어나면 모두 같은 면이 나올 확률은 어떻게 될까?</p>
      <div class="answer step em33-left">점점 작아진다 — 동전 10개이면 $2\\div2^{{10}}\\approx0.2\\ \\%$뿐이다. 섞인(무질서한) 상태가 압도적으로 많이 나온다.</div>
    </div>
  </div>
</section>''')

# ───────── 10 실험실
add('''<!-- ════════ 10. 실험실 ════════ -->
<section class="slide" data-sec="03 · 실험실" data-title="실험실: 동전 던지기와 확률">
  <h2><span class="tag">실험실</span>동전 던지기 — 무질서한 상태가 될 확률</h2>
  <div class="lab" data-lab="em33coin">
    <div class="lab-ctl" style="flex-basis:400px">
      <div class="ctl"><div class="lbl"><span>동전의 수 $N$</span><output data-o="n"></output></div>
        <input type="range" min="2" max="12" step="1" value="4" data-i="n" aria-label="동전의 수"></div>
      <div class="em33-seg"><button class="btn em33-act" data-act="one">1번 던지기</button><button class="btn em33-act" data-act="hund">100번 던지기</button><button class="btn" data-act="reset">초기화</button></div>
      <table class="readout em33-read">
        <tr><th>던진 횟수</th><td><output data-o="tot"></output></td></tr>
        <tr><th>모두 같은 면</th><td><output data-o="same"></output></td></tr>
        <tr class="hl"><th>이론 확률</th><td><output data-o="th"></output></td></tr>
      </table>
      <output class="kind em33-msg" data-o="msg"></output>
    </div>
    <div class="col" style="flex:0 0 660px">
      <div class="lab-fig" style="width:660px;height:290px">
        <svg viewBox="0 0 660 290" width="660" height="290" aria-label="마지막으로 던진 동전들과, 앞면의 수에 따른 실험 비율 막대와 이론 확률 점"></svg>
        <div class="ov" data-ov="ya" style="transform:none"></div>
        <div class="ov" data-ov="xa" style="transform:none"></div>
      </div>
      <table class="tight em33-log mt8"><thead><tr><th>동전 수</th><th>던진 횟수</th><th>모두 같은 면 (회)</th><th>실험 비율</th><th>이론 확률</th></tr></thead><tbody data-o="log"></tbody></table>
    </div>
  </div>
</section>''')

# ───────── 11 확인하기
add('''<!-- ════════ 11. 확인하기 ════════ -->
<section class="slide" data-sec="03 · 확인하기" data-title="확인하기: 엔트로피" data-tpl="check">
  <h2><span class="tag q">확인하기</span>엔트로피의 뜻 확인하기</h2>
  <p class="f22" data-q><b>1</b> 무질서도를 나타내는 척도를 ( <span class="blank"><span class="step">엔트로피</span></span> )(이)라고 한다.</p>
  <p class="f22 mt16" data-q><b>2</b> 무질서도가 증가하면 엔트로피가 ( 증가한다, 감소한다 ).</p>
  <div class="answer step">증가한다</div>
  <div class="board mt16" style="min-height:220px"></div>
</section>''')

# ───────── 12 엔트로피 변화
def mini_solid(x,y):
    return ''.join(C(x+i*20,y+j*20,7,BLU) for i in range(3) for j in range(3))
mini_mix=''.join(C(x,y,7,c) for (x,y),c in zip(grid(4,3,112,46,20,20),[BLU,'#F4A261']*6))
add(f'''<!-- ════════ 12. 엔트로피 변화 ════════ -->
<section class="slide" data-sec="03 · 엔트로피 변화" data-title="엔트로피 변화 ΔS">
  <h2><span class="no">3</span>엔트로피 변화 $\\Delta S$</h2>
  <p class="f22">어떤 변화가 일어날 때 엔트로피 변화($\\Delta S$)는 최종 상태의 엔트로피에서 초기 상태의 엔트로피를 뺀 값이다.</p>
  <div class="formula mt8">$\\Delta S=S_\\text{{최종}}-S_\\text{{초기}}$<div class="unit">$S_\\text{{최종}}$: 최종 상태의 엔트로피 · $S_\\text{{초기}}$: 초기 상태의 엔트로피</div></div>
  <div class="row mt8">
    <div class="card em33-sign" style="flex:1 1 0"><p class="f22 center">엔트로피가 <b>증가</b>하면 <b class="c-field">$\\Delta S&gt;0$</b></p></div>
    <div class="card em33-sign" style="flex:1 1 0"><p class="f22 center">엔트로피가 <b>감소</b>하면 <b class="c-muted">$\\Delta S&lt;0$</b></p></div>
  </div>
  <p class="f21 mt12">엔트로피가 증가하는 변화 — 다음 세 가지를 차례로 알아보자.</p>
  <div class="stages mt8">
    <div class="stage"><svg viewBox="0 0 300 110" aria-label="고체 입자가 흩어지는 모습"><g data-anim="pop" data-o="150,55" data-dur=".7" data-delay=".2" data-ease="back">{mini_solid(40,36)}{A(104,56,160,56,'field',3)}{C(196,40,7,BLU)}{C(230,70,7,BLU)}{C(262,34,7,BLU)}{C(210,92,7,BLU)}{C(258,84,7,BLU)}</g></svg><h3>㉠ 분자의 움직임이 활발해질 때</h3></div>
    <div class="stage"><svg viewBox="0 0 300 110" aria-label="두 물질이 섞이는 모습"><g data-anim="pop" data-o="150,55" data-dur=".7" data-delay=".5" data-ease="back">{''.join(C(30+i*20,36+j*20,7,BLU if j<2 else '#F4A261') for i in range(3) for j in range(4) if j!=3)}{A(102,56,150,56,'field',3)}{''.join(C(180+i*20,26+j*20,7,[BLU,'#F4A261'][(i+j)%2]) for i in range(4) for j in range(3))}</g></svg><h3>㉡ 순수한 두 물질이 섞일 때</h3></div>
    <div class="stage"><svg viewBox="0 0 300 110" aria-label="입자 하나가 여러 입자로 나뉘는 모습"><g data-anim="pop" data-o="150,55" data-dur=".7" data-delay=".8" data-ease="back"><rect x="40" y="30" width="56" height="50" rx="6" fill="#E8E4DA" stroke="#B9AE96" stroke-width="2"/>{A(110,56,160,56,'field',3)}<rect x="176" y="56" width="36" height="30" rx="5" fill="#E8E4DA" stroke="#B9AE96" stroke-width="2"/>{C(236,30,8,'#3A3F47')}{C(262,62,8,'#3A3F47')}{C(236,90,8,'#3A3F47')}</g></svg><h3>㉢ 입자 수가 증가할 때</h3></div>
  </div>
  <p class="f21 mt8"><b>Q</b> 이 세 경우에 엔트로피는 어떻게 변할까? <span class="step">→ <span class="ans">모두 증가한다($\\Delta S&gt;0$)</span></span></p>
</section>''')

# ───────── 13 분자의 움직임 (그림 Ⅲ-6)
bx=[(40,40),(370,40),(700,40)]
sol=''.join(C(bx[0][0]+38+i*30,bx[0][1]+78+j*30,12,'#7E6BC4','#4E3E94',1.5) for i in range(5) for j in range(4))
sol=f'<g data-anim="move" data-from="1.5,0" data-rep="swing" data-dur=".18">{sol}</g>'
liq_pts=scatter(random.Random(13),18,bx[1][0]+26,bx[1][1]+92,bx[1][0]+214,bx[1][1]+182,25)
liq=''.join(C(x,y,12,'#7E6BC4','#4E3E94',1.5) for x,y in liq_pts)
gas_pts=[(760,80),(870,96),(800,150),(900,170),(745,200),(840,214)]
gas=''.join(mv(C(x,y,12,'#7E6BC4','#4E3E94',1.5),[-14,18,12,-16,16,-12][i],[10,-12,14,8,-10,-14][i],1.1+0.2*i,rep='alt',ease='io') for i,(x,y) in enumerate(gas_pts))
add(f'''<!-- ════════ 13. 분자의 움직임 ════════ -->
<section class="slide" data-sec="03 · 엔트로피 변화" data-title="분자의 움직임이 활발해질 때">
  <h2><span class="no">3</span>㉠ 분자의 움직임이 활발해질 때</h2>
  <svg class="fig" viewBox="0 0 1000 270" style="width:1000px" aria-label="고체는 입자가 규칙적으로 배열하고, 액체는 불규칙하게 붙어 있으며, 기체는 자유롭게 흩어진다. 고체에서 액체, 기체로 갈수록 엔트로피가 증가한다">
    {beaker(bx[0][0],bx[0][1],240,200)}{beaker(bx[1][0],bx[1][1],240,200)}{beaker(bx[2][0],bx[2][1],240,200)}
    {sol}{liq}{gas}
    {A(290,112,350,112,'field',4)}{A(350,170,290,170,'muted',4)}{A(620,112,680,112,'field',4)}{A(680,170,620,170,'muted',4)}
    {T(320,96,'\\Delta S&gt;0',20,'middle',FLD,tex=True)}{T(320,200,'\\Delta S&lt;0',20,'middle',MUT,tex=True)}
    {T(650,96,'\\Delta S&gt;0',20,'middle',FLD,tex=True)}{T(650,200,'\\Delta S&lt;0',20,'middle',MUT,tex=True)}
    {T(160,264,'고체',21,'middle',w=700)}{T(490,264,'액체',21,'middle',w=700)}{T(820,264,'기체',21,'middle',w=700)}
  </svg>
  <div class="row mt8">
    <div class="col">
      <p class="f21">물질이 열을 흡수하여 온도가 높아지거나 상태 변화가 일어나면 분자 운동이 활발해져 무질서도가 증가 → 엔트로피 <b>증가</b>.</p>
      <p class="f21 mt8"><b>Q</b> 고체, 액체, 기체의 엔트로피 크기 순서는? <span class="step">→ <span class="ans">$S_\\text{{고체}}&lt;S_\\text{{액체}}&lt;S_\\text{{기체}}$</span></span></p>
      <p class="f21 mt8"><b>Q</b> 융해·기화와 액화·응고에서 $\\Delta S$의 부호는? <span class="step">→ <span class="ans">융해·기화 $\\Delta S&gt;0$, 액화·응고 $\\Delta S&lt;0$</span></span></p>
    </div>
    <div class="col" style="flex:0 0 330px">
      <div class="note"><b>드라이아이스의 승화</b><br>$\\ce{{CO2(s) -> CO2(g)}}$<br>고체가 바로 기체가 되므로 엔트로피가 <b>크게</b> 증가한다.</div>
    </div>
  </div>
</section>''')

# ───────── 14 두 물질이 섞일 때 (그림 Ⅲ-7)
top=[(x,y) for (x,y) in grid(7,3,62,92,26,24)]
bot=[(x,y) for (x,y) in grid(7,3,62,164,26,24)]
lay_s=''.join(C(x,y,11,BLU,'#2457A6',1.2) for x,y in top)+''.join(C(x,y,11,'#F4A261','#C46A1F',1.2) for x,y in bot)
allpos=top+bot
perm=list(range(len(allpos))); random.Random(17).shuffle(perm)
colsP=[BLU]*21+['#F4A261']*21
mix_s=''
for i,j in enumerate(perm):
    x,y=allpos[j]; x+=320
    ox,oy=allpos[i]; ox+=320
    st='#2457A6' if colsP[i]==BLU else '#C46A1F'
    mix_s+=mv(C(x,y,11,colsP[i],st,1.2),ox-x,oy-y,1.6,0.4,ease='io')
add(f'''<!-- ════════ 14. 두 물질이 섞일 때 ════════ -->
<section class="slide" data-sec="03 · 엔트로피 변화" data-title="순수한 두 물질이 섞일 때">
  <h2><span class="no">3</span>㉡ 순수한 두 물질이 섞일 때</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px">
      <svg class="fig" viewBox="0 0 560 250" style="width:560px" aria-label="두 층으로 나뉜 두 물질이 섞이면 무질서도가 커져 엔트로피가 증가한다">
        {beaker(40,60,200,170)}{beaker(360,60,200,170)}
        {lay_s}{mix_s}
        {A(252,110,342,110,'field',4)}{A(342,170,252,170,'muted',4)}
        {T(297,94,'\\Delta S&gt;0',20,'middle',FLD,tex=True)}{T(297,200,'\\Delta S&lt;0',20,'middle',MUT,tex=True)}
        {T(140,40,'섞이기 전',20,'middle')}{T(460,40,'섞인 뒤',20,'middle')}
      </svg>
      <div class="note mt8"><b>오개념 바로잡기</b> 용해 과정에서 엔트로피가 항상 증가하는 것은 아니다. <b>기체가 용해</b>하는 과정에서는 엔트로피가 <b>감소</b>한다.</div>
    </div>
    <div class="col">
      <p class="f21">순수한 두 물질이 섞이면 무질서도가 커지므로 엔트로피가 <b>증가</b>한다.</p>
      <p class="f21 mt8">설탕이 물에 녹을 때는 설탕 분자가 더 넓은 공간으로 퍼지므로 무질서해진다. → 고체나 액체의 <b>용해</b> 과정에서 엔트로피 증가</p>
      <p class="f21 mt8">입자들이 농도나 밀도 차에 의해 액체나 기체 속으로 <b>확산</b>할 때도 엔트로피가 증가한다.</p>
      <p class="f21 mt12"><b>Q</b> 탄산음료를 만들 때 이산화 탄소가 물에 녹는 과정 $\\ce{{CO2(g) -> CO2(aq)}}$의 $\\Delta S$ 부호는?</p>
      <div class="answer step">$\\Delta S&lt;0$ <span class="small">— 자유롭게 움직이던 기체 분자가 용액 속에 갇힌다</span></div>
    </div>
  </div>
</section>''')

# ───────── 15 입자 수 증가 (그림 Ⅲ-8)
def co2(x,y,ang=0):
    a=math.radians(ang); dx=16*math.cos(a); dy=16*math.sin(a)
    return (f'<line x1="{x-dx:.1f}" y1="{y-dy:.1f}" x2="{x+dx:.1f}" y2="{y+dy:.1f}" stroke="#9AA5B1" stroke-width="5" stroke-linecap="round"/>'
            f'<g data-atom="{x-dx:.1f},{y-dy:.1f},12,O,-"></g><g data-atom="{x+dx:.1f},{y+dy:.1f},12,O,-"></g><g data-atom="{x:.1f},{y:.1f},12,C,-"></g>')
blk=''.join(f'<rect x="{40+i*22}" y="{70+j*22}" width="20" height="20" rx="3" fill="#EFEADF" stroke="#B9AE96" stroke-width="1.5"/>' for i in range(6) for j in range(6))
cao=''.join(f'<rect x="{336+i*22}" y="{170+j*22}" width="20" height="20" rx="3" fill="#F7F4EC" stroke="#B9AE96" stroke-width="1.5"/>' for i in range(4) for j in range(3))
mol=[(350,60,20),(450,50,-30),(540,90,60),(470,120,10),(560,170,-50),(420,140,80)]
mols=''.join(mv(co2(x,y,a),(380-x)*0.9,(200-y)*0.9,1.6,0.3+0.1*i,ease='out') for i,(x,y,a) in enumerate(mol))
add(f'''<!-- ════════ 15. 입자 수 증가 ════════ -->
<section class="slide" data-sec="03 · 엔트로피 변화" data-title="입자 수가 증가할 때">
  <h2><span class="no">3</span>㉢ 입자 수가 증가할 때</h2>
  <div class="formula">$\\ce{{CaCO3(s) -> CaO(s) + CO2(g)}}$</div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 600px">
      <svg class="fig" viewBox="0 0 600 260" style="width:600px" aria-label="탄산 칼슘 고체가 분해되면 산화 칼슘 고체와 함께 이산화 탄소 기체 분자들이 생겨 흩어진다">
        {blk}{cao}{mols}
        {A(196,150,300,150,'field',4)}{A(300,200,196,200,'muted',4)}
        {T(248,134,'\\Delta S&gt;0',20,'middle',FLD,tex=True)}{T(248,232,'\\Delta S&lt;0',20,'middle',MUT,tex=True)}
        {T(106,232,'\\ce{CaCO3(s)}',21,'middle',tex=True)}{T(380,254,'\\ce{CaO(s)}',21,'middle',tex=True)}
        {T(590,30,'\\ce{CO2(g)}',21,'end',tex=True)}
        <g data-atom="40,26,10,C,-"></g>{T(56,33,'C',19,'start')}<g data-atom="92,26,10,O,-"></g>{T(108,33,'O',19,'start')}
      </svg>
    </div>
    <div class="col">
      <p class="f21">화학 반응에서 <b>입자 수가 증가</b>하면 엔트로피가 증가한다.</p>
      <p class="f21 mt8">특히 기체의 엔트로피는 액체나 고체보다 훨씬 크므로, <b>기체 분자 수의 증가</b>는 엔트로피 증가에 매우 큰 영향을 미친다.</p>
      <div class="note mt8"><b>엔트로피와 물질의 양</b> 엔트로피는 물질의 양에 의존한다 — 분자의 수 또는 물질의 양이 늘어나면 증가한다.</div>
      <p class="f21 mt8"><b>Q</b> 탄산 칼슘의 열분해에서 엔트로피가 크게 증가하는 까닭은? <span class="step">→ <span class="ans">입자 수가 늘고 <b>기체</b>($\\ce{{CO2}}$)가 생성되기 때문</span></span></p>
    </div>
  </div>
</section>''')

# ───────── 16 해 보기: 부호 예측
def snow(cx,cy):
    s=''
    for k in range(6):
        a=math.radians(60*k); x2=cx+48*math.cos(a); y2=cy+48*math.sin(a)
        s+=f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#7FA6D6" stroke-width="4" stroke-linecap="round"/>'
        for t in (0.5,0.75):
            px=cx+48*t*math.cos(a); py=cy+48*t*math.sin(a)
            for sgn in (-1,1):
                b=a+sgn*math.radians(45)
                s+=f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px+12*math.cos(b):.1f}" y2="{py+12*math.sin(b):.1f}" stroke="#7FA6D6" stroke-width="3" stroke-linecap="round"/>'
    return s
bub=''.join(mv(C(x,y,5,'#fff','#7E8B98',1.5),0,40,1.4,0.2*i,rep='loop',ease='lin') for i,(x,y) in enumerate([(140,60),(156,80),(146,100)]))
def n2(x,y): return f'<g data-atom="{x-9},{y},12,N,-"></g><g data-atom="{x+9},{y},12,N,-"></g>'
def h2(x,y): return f'<g data-atom="{x-8},{y},10,H,-"></g><g data-atom="{x+8},{y},10,H,-"></g>'
def nh3(x,y): return f'<g data-atom="{x-12},{y+8},9,H,-"></g><g data-atom="{x+12},{y+8},9,H,-"></g><g data-atom="{x},{y+14},9,H,-"></g><g data-atom="{x},{y-2},12,N,-"></g>'
add(f'''<!-- ════════ 16. 해 보기: 부호 예측 ════════ -->
<section class="slide" data-sec="03 · 해 보기" data-title="해 보기: 엔트로피 변화의 부호 예측">
  <h2><span class="tag">해 보기</span>엔트로피 변화의 부호 예측하기</h2>
  <p class="f21" data-q>다음 변화가 일어날 때 엔트로피가 어떻게 변하는지 쓰고, 그렇게 답한 까닭을 써 보자.</p>
  <div class="stages mt8">
    <div class="stage"><svg viewBox="0 0 300 140" aria-label="눈 결정"><rect x="4" y="4" width="292" height="132" rx="10" fill="#EEF4FB"/><g data-anim="rot" data-from="-30" data-o="150,70" data-dur="1.6" data-ease="out">{snow(150,70)}</g></svg>
      <h3>① 공기 중의 수증기가 얼어 눈 결정이 된다.</h3>
      <p class="f21 center">$\\ce{{H2O(g) -> H2O(s)}}$</p>
      <p class="f21 step em33-a">→ <span class="ans">감소($\\Delta S&lt;0$)</span> 자유롭게 움직이던 기체 분자가 규칙적인 고체가 된다.</p></div>
    <div class="stage"><svg viewBox="0 0 300 140" aria-label="시험관 속 아연에서 수소 기체 거품이 생긴다"><path d="M120 10 L120 118 Q120 132 134 132 L166 132 Q180 132 180 118 L180 10" fill="none" stroke="{GL}" stroke-width="3"/><path d="M123 40 L123 118 Q123 129 134 129 L166 129 Q177 129 177 118 L177 40 Z" fill="{WAT}"/><path d="M132 126 L140 112 L152 116 L164 108 L170 126 Z" fill="#8FA3B8" stroke="#5C6F82" stroke-width="1.5"/>{bub}{T(196,64,'\\ce{HCl(aq)}',19,'start',tex=True)}{T(196,122,'\\ce{Zn(s)}',19,'start',tex=True)}</svg>
      <h3>② 아연과 염산이 반응하여 수소 기체가 발생한다.</h3>
      <p class="f21 center">$\\ce{{Zn(s) + 2HCl(aq) -> ZnCl2(aq) + H2(g)}}$</p>
      <p class="f21 step em33-a">→ <span class="ans">증가($\\Delta S&gt;0$)</span> 물질의 양은 약간 줄지만, 기체가 생성되는 영향이 더 크다.</p></div>
    <div class="stage"><svg viewBox="0 0 300 140" aria-label="질소 분자 1개와 수소 분자 3개가 암모니아 분자 2개가 된다">{n2(40,44)}{h2(40,82)}{h2(80,62)}{h2(80,104)}{A(118,74,170,74,'ink',3)}{nh3(214,52)}{nh3(254,92)}<g data-atom="212,16,9,N,-"></g>{T(225,22,'N',18,'start')}<g data-atom="252,16,8,H,-"></g>{T(264,22,'H',18,'start')}{T(66,134,'기체 4분자',19,'middle')}{T(234,134,'기체 2분자',19,'middle')}</svg>
      <h3>③ 질소와 수소를 반응시켜 암모니아를 합성한다.</h3>
      <p class="f21 center">$\\ce{{N2(g) + 3H2(g) -> 2NH3(g)}}$</p>
      <p class="f21 step em33-a">→ <span class="ans">감소($\\Delta S&lt;0$)</span> 기체 분자 수가 4에서 2로 줄어든다.</p></div>
  </div>
</section>''')

# ───────── 17 확인하기
add('''<!-- ════════ 17. 확인하기 ════════ -->
<section class="slide" data-sec="03 · 확인하기" data-title="확인하기: 엔트로피 변화" data-tpl="check">
  <h2><span class="tag q">확인하기</span>엔트로피 변화 확인하기</h2>
  <p class="f22" data-q><b>1</b> 에탄올이 증발하는 것은 엔트로피가 ( 증가하는, 감소하는 ) 변화이다.</p>
  <div class="answer step">증가하는 <span class="small">— 액체가 기체가 된다</span></div>
  <p class="f22 mt16"><b>2</b> $\\ce{2A(g) -> 2B(g) + C(g)}$의 반응에서 엔트로피 변화($\\Delta S$)의 부호를 예측해 보자.</p>
  <p class="f21 mt8 step">기체 분자 수: 반응물 2 → 생성물 3, 기체 분자 수가 증가한다.</p>
  <div class="answer step">$\\Delta S&gt;0$</div>
  <div class="board mt12" style="min-height:120px"></div>
</section>''')

# ───────── 18 연결: 두 가지 경향
add(f'''<!-- ════════ 18. 연결: 두 경향 ════════ -->
<section class="slide" data-sec="03 · 화학 변화의 자발성" data-title="연결: 두 가지 경향">
  <h2><span class="tag alt">연결</span>자발성을 정하는 두 가지 경향</h2>
  <div class="row">
    <div class="col">
      <div class="em33-bubble">물질은 엔탈피가 낮을수록 안정해.</div>
      <p class="f21 mt12">화학 반응이 일어나면 물질이 가진 엔탈피와 엔트로피가 달라진다. 자연계에서 일어나는 변화는 두 경향을 가진다.</p>
      <div class="row mt8">
        <div class="card em33-hcard" style="flex:1 1 0"><h3>엔탈피를 낮추려는 방향</h3><p class="f22 center">$\\Delta H&lt;0$</p><p class="small">안정해지려는 경향</p></div>
        <div class="card em33-scard" style="flex:1 1 0"><h3>엔트로피를 높이려는 방향</h3><p class="f22 center">$\\Delta S&gt;0$</p><p class="small">무질서해지려는 경향</p></div>
      </div>
      <p class="f21 mt8">→ 이 두 요인이 <b>함께 작용</b>하여 특정한 반응의 자발성을 결정한다.</p>
    </div>
    <div class="col" style="flex:0 0 400px">
      <div class="card tip"><h3>계와 주위</h3>
        <svg class="fig" viewBox="0 0 360 170" style="width:360px" aria-label="반응이 일어나는 비커 속 물질은 계, 그 바깥은 주위이다">
          <rect x="6" y="6" width="348" height="158" rx="12" fill="#F7F9FB" stroke="#9FB0C2" stroke-width="2" stroke-dasharray="7 5"/>
          {beaker(130,40,100,110,30)}
          {T(180,108,'계',24,'middle',INK,w=700)}
          {T(24,40,'주위',22,'start',MUT,w=700)}
        </svg>
        <p class="f21">반응이 직접 일어나는 영역 또는 물질을 <b>계</b>, 계를 제외한 외부의 모든 영역을 <b>주위</b>라고 한다. 여기에서는 <b>계의</b> 엔탈피와 엔트로피만 다룬다.</p>
      </div>
    </div>
  </div>
  <p class="f22 mt8"><b>Q</b> 두 경향이 서로 반대 방향이면 자발성은 어떻게 정해질까?</p>
  <div class="answer step">영향이 <b>더 큰 쪽</b>이 자발성을 결정한다.</div>
</section>''')

TUGNOTE='<p class="small c-muted">화살표 길이는 영향의 크고 작음만 나타낸다(크기 비례 아님).</p>'
# ───────── 19 모두 유리
p_no2=lambda x,y: f'<g data-atom="{x-30},{y+10},24,O"></g><g data-atom="{x+30},{y+10},24,O"></g><g data-atom="{x},{y-8},24,N"></g>'
mol19=(p_no2(70,70)+p_no2(70,150)+A(140,110,196,110,"ink",3)
       +mv('<g data-atom="248,48,24,N"></g><g data-atom="288,48,24,N"></g>',-178,20,1.4,0.4,ease="io")
       +mv('<g data-atom="244,104,24,O"></g><g data-atom="284,104,24,O"></g>',-204,-34,1.4,0.4,ease="io")
       +mv('<g data-atom="244,158,24,O"></g><g data-atom="284,158,24,O"></g>',-204,2,1.4,0.4,ease="io"))
add(f'''<!-- ════════ 19. 모두 유리 ════════ -->
<section class="slide" data-sec="03 · 화학 변화의 자발성" data-title="두 요인이 모두 유리한 반응">
  <h2><span class="no">4</span>엔탈피와 엔트로피 변화가 모두 자발성에 유리한 반응</h2>
  <div class="formula sm">이산화 질소의 분해 &nbsp; $\\ce{{2NO2(g) -> N2(g) + 2O2(g)}}\\quad\\Delta H=-66.4\\ \\text{{kJ}}$</div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 440px">
      <svg class="fig" viewBox="0 0 330 210" style="width:330px" aria-label="이산화 질소 분자 2개가 질소 분자 1개와 산소 분자 2개로 바뀐다. 기체 분자 수가 2에서 3으로 늘어난다">
        {mol19}
        {T(70,206,'기체 2분자',19,'middle')}{T(266,206,'기체 3분자',19,'middle')}
      </svg>
      <p class="f21 mt8 step" data-g="h">엔탈피 <b>감소</b>($\\Delta H&lt;0$) → 자발성에 유리</p>
      <p class="f21 step" data-g="s">기체 분자 수가 증가하여 엔트로피 <b>증가</b>($\\Delta S&gt;0$) → 유리</p>
    </div>
    <div class="col">
      <svg class="fig" viewBox="0 0 560 150" style="width:560px" aria-label="엔탈피 요인과 엔트로피 요인이 모두 자발적 방향을 향한다">
        {tug(1,220,'엔탈피 감소 $\\Delta H&lt;0$',1,200,'엔트로피 증가 $\\Delta S&gt;0$',560,150,'h','s')}
      </svg>
      {TUGNOTE}
      <p class="f21 mt8"><b>Q</b> 이 반응은 자발적일까?</p>
      <div class="answer step">두 요인 모두 유리 → <b>항상 자발적</b>이다.</div>
    </div>
  </div>
</section>''')

# ───────── 20 모두 불리
add(f'''<!-- ════════ 20. 모두 불리 ════════ -->
<section class="slide" data-sec="03 · 화학 변화의 자발성" data-title="두 요인이 모두 불리한 반응">
  <h2><span class="no">4</span>엔탈피와 엔트로피 변화가 모두 자발성에 불리한 반응</h2>
  <div class="formula sm">과산화 수소의 생성 &nbsp; $\\ce{{2H2O(l) + O2(g) -> 2H2O2(l)}}\\quad\\Delta H=+196.4\\ \\text{{kJ}}$</div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 440px">
      <p class="f21" data-q>물과 산소가 반응하여 과산화 수소가 되는 반응에서 두 요인을 판단해 보자.</p>
      <p class="f21 mt8 step" data-g="h">엔탈피 <b>증가</b>($\\Delta H&gt;0$) → 자발성에 불리</p>
      <p class="f21 step" data-g="s">반응이 진행될수록 기체의 양이 줄어들어 엔트로피가 크게 <b>감소</b>($\\Delta S&lt;0$) → 불리</p>
      <div class="note mt12">반대로 과산화 수소는 물과 산소로 <b>저절로 분해</b>되는 경향이 있다. → 소단원 마무리</div>
    </div>
    <div class="col">
      <svg class="fig" viewBox="0 0 560 150" style="width:560px" aria-label="엔탈피 요인과 엔트로피 요인이 모두 비자발적 방향을 향한다">
        {tug(-1,220,'엔탈피 증가 $\\Delta H&gt;0$',-1,220,'엔트로피 감소 $\\Delta S&lt;0$',560,150,'h','s')}
      </svg>
      {TUGNOTE}
      <p class="f21 mt8"><b>Q</b> 이 반응은 자발적일까?</p>
      <div class="answer step">두 요인 모두 불리 → <b>항상 비자발적</b>이다.</div>
      <p class="f21 mt8"><b>Q</b> 역반응 $\\ce{{2H2O2(l) -> 2H2O(l) + O2(g)}}$은? <span class="step">→ <span class="ans">$\\Delta H&lt;0$, $\\Delta S&gt;0$ → 항상 자발적</span></span></p>
    </div>
  </div>
</section>''')

# ───────── 21 엔탈피 유리 (중화)
ion=lambda x,y,r,lab,fill,st: C(x,y,r,fill,st,2.5)+T(x,y+7,lab,19,'middle',tex=True)
# 간단히: 물 분자 하나 (O 24, H 18)
mol21=(ion(60,46,26,'\\ce{H+}','#FBE3E6','#D7263D')+ion(60,124,30,'\\ce{OH-}','#E3EEFB','#1F6FD1')
       +A(110,88,166,88,'ink',3)
       +f'<g data-anim="pop" data-o="236,88" data-dur=".8" data-delay=".6" data-ease="back"><g data-atom="210,106,18,H"></g><g data-atom="262,106,18,H"></g><g data-atom="236,82,24,O"></g></g>')
add(f'''<!-- ════════ 21. 엔탈피 유리 ════════ -->
<section class="slide" data-sec="03 · 화학 변화의 자발성" data-title="엔탈피 변화가 유리한 반응">
  <h2><span class="no">4</span>엔탈피 변화가 자발성에 유리한 반응</h2>
  <div class="formula sm">산과 염기의 중화 반응 &nbsp; $\\ce{{H+(aq) + OH-(aq) -> H2O(l)}}\\quad\\Delta H=-55.8\\ \\text{{kJ}}$</div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 430px">
      <svg class="fig" viewBox="0 0 300 200" style="width:300px" aria-label="수소 이온과 수산화 이온 두 입자가 물 분자 하나가 된다">
        {mol21}
        {T(60,190,'2 입자',19,'middle')}{T(236,190,'1 입자',19,'middle')}
      </svg>
      <p class="f21 step" data-g="s">전체 입자 수가 감소하여 엔트로피 <b>감소</b>($\\Delta S&lt;0$) → 불리</p>
      <p class="f21 step" data-g="h">엔탈피가 <b>더 크게</b> 낮아짐($\\Delta H&lt;0$) → 유리, 영향이 더 큼</p>
    </div>
    <div class="col">
      <p class="small em33-cap">엔탈피 감소 영향이 더 큰 경우</p>
      <svg class="fig" viewBox="0 0 560 150" style="width:560px" aria-label="엔탈피 감소 화살표가 엔트로피 감소 화살표보다 길어 반응이 자발적이다">
        {tug(1,240,'엔탈피 감소',-1,110,'엔트로피 감소',560,150,'h','s')}
      </svg>
      <p class="small em33-cap">(비교) 엔탈피 감소 영향이 더 작은 경우 → 비자발적</p>
      <svg class="fig" viewBox="0 0 560 150" style="width:560px" aria-label="엔탈피 감소 화살표가 엔트로피 감소 화살표보다 짧으면 반응이 비자발적이다">
        {tug(1,110,'엔탈피 감소',-1,240,'엔트로피 감소',560,150)}
      </svg>
    </div>
  </div>
  <div class="answer step">엔탈피를 낮추려는 경향이 엔트로피가 감소하는 경향보다 크면 반응이 <b>자발적</b>으로 일어난다.</div>
</section>''')

# ───────── 22 엔트로피 유리 (냉각 팩)
crys=''.join(f'<rect x="{30+i*24}" y="{70+j*24}" width="22" height="22" rx="3" fill="#F4F1EA" stroke="#B9AE96" stroke-width="1.5"/>' for i in range(3) for j in range(3))
wpts=scatter(random.Random(31),16,170,30,330,180,30)
wat=''.join(C(x,y,8,'#D6E6F2','#A9C4DA',1.2) for x,y in wpts)
ions=[(205,62,'P'),(290,92,'M'),(230,150,'M'),(312,160,'P')]
ion_s=''
for i,(x,y,t) in enumerate(ions):
    body=(C(x,y,26,'#FBE3E6','#D7263D',2.5)+T(x,y+7,'\\ce{NH4+}',18,'middle',tex=True)) if t=='P' else (C(x,y,26,'#E3EEFB','#1F6FD1',2.5)+T(x,y+7,'\\ce{NO3-}',18,'middle',tex=True))
    ion_s+=mv(body,(100-x)*0.8,(105-y)*0.8,1.6,0.3+0.1*i,ease='out')
add(f'''<!-- ════════ 22. 엔트로피 유리 ════════ -->
<section class="slide" data-sec="03 · 화학 변화의 자발성" data-title="엔트로피 변화가 유리한 반응">
  <h2><span class="no">4</span>엔트로피 변화가 자발성에 유리한 반응</h2>
  <div class="formula sm">휴대용 냉각 팩 &nbsp; $\\ce{{NH4NO3(s) -> NH4+(aq) + NO3-(aq)}}\\quad\\Delta H=+25\\ \\text{{kJ}}$</div>
  <div class="row mt8">
    <div class="col" style="flex:0 0 430px">
      <svg class="fig" viewBox="0 0 350 200" style="width:350px" aria-label="질산 암모늄 고체가 물에 녹아 암모늄 이온과 질산 이온이 물 분자 사이로 퍼진다">
        <rect x="156" y="16" width="188" height="178" rx="14" fill="#F1F7FC" stroke="#9FC3DD" stroke-width="2"/>
        {crys}{wat}{ion_s}
        {T(70,160,'\\ce{NH4NO3(s)}',19,'middle',tex=True)}<circle cx="30" cy="30" r="8" fill="#D6E6F2" stroke="#A9C4DA"/>{T(44,36,'물 분자',19,'start',MUT)}{A(112,104,150,104,'ink',3)}
        
      </svg>
      <p class="f21 step" data-g="h">엔탈피 <b>증가</b>($\\Delta H&gt;0$) → 불리</p>
      <p class="f21 step" data-g="s">입자 수가 늘고 이온들이 물 분자에 섞여 들어가 입자 운동이 자유로워짐 → 엔트로피 크게 <b>증가</b>($\\Delta S&gt;0$) → 유리, 영향이 더 큼</p>
    </div>
    <div class="col">
      <p class="small em33-cap">엔트로피 증가 영향이 더 큰 경우</p>
      <svg class="fig" viewBox="0 0 560 150" style="width:560px" aria-label="엔트로피 증가 화살표가 엔탈피 증가 화살표보다 길어 반응이 자발적이다">
        {tug(-1,110,'엔탈피 증가',1,240,'엔트로피 증가',560,150,'h','s')}
      </svg>
      <p class="small em33-cap">(비교) 엔트로피 증가 영향이 더 작은 경우 → 비자발적</p>
      <svg class="fig" viewBox="0 0 560 150" style="width:560px" aria-label="엔트로피 증가 화살표가 엔탈피 증가 화살표보다 짧으면 반응이 비자발적이다">
        {tug(-1,240,'엔탈피 증가',1,110,'엔트로피 증가',560,150)}
      </svg>
    </div>
  </div>
  <div class="answer step">엔트로피를 높이려는 경향이 엔탈피가 증가하는 경향보다 크면 <b>자발적</b> → 흡열 반응도 저절로 일어날 수 있다</div>
</section>''')

# ───────── 23 네 경우 정리
add('''<!-- ════════ 23. 네 경우 정리 ════════ -->
<section class="slide" data-sec="03 · 화학 변화의 자발성" data-title="네 가지 경우 정리">
  <h2><span class="no">4</span>엔탈피·엔트로피 변화와 자발성 — 네 가지 경우</h2>
  <table class="tight em33-four mt8">
    <tr><th></th><th>엔트로피 증가 $\\Delta S&gt;0$ <span class="small">(유리)</span></th><th>엔트로피 감소 $\\Delta S&lt;0$ <span class="small">(불리)</span></th></tr>
    <tr><th>엔탈피 감소<br>$\\Delta H&lt;0$ <span class="small">(유리)</span></th>
      <td class="em33-yes"><span class="step"><b>항상 자발적</b><br><span class="small">예: $\\ce{2NO2(g) -> N2(g) + 2O2(g)}$</span></span></td>
      <td><span class="step"><b>엔탈피 감소 영향이 더 크면 자발적</b><br><span class="small">예: 중화 반응 $\\ce{H+(aq) + OH-(aq) -> H2O(l)}$</span></span></td></tr>
    <tr><th>엔탈피 증가<br>$\\Delta H&gt;0$ <span class="small">(불리)</span></th>
      <td><span class="step"><b>엔트로피 증가 영향이 더 크면 자발적</b><br><span class="small">예: 냉각 팩 $\\ce{NH4NO3(s) -> NH4+(aq) + NO3-(aq)}$</span></span></td>
      <td class="em33-no"><span class="step"><b>항상 비자발적</b><br><span class="small">예: $\\ce{2H2O(l) + O2(g) -> 2H2O2(l)}$</span></span></td></tr>
  </table>
  <p class="f22 mt16"><b>Q</b> 발열 반응이면 모두 자발적일까?</p>
  <div class="answer step">아니다 — 엔트로피 변화가 함께 작용한다. 발열 반응이 모두 자발적인 것은 아니고, <b>흡열 반응도 자발적</b>일 수 있다.</div>
</section>''')

# ───────── 24 확인하기
add('''<!-- ════════ 24. 확인하기 ════════ -->
<section class="slide" data-sec="03 · 확인하기" data-title="확인하기: 자발성 판단" data-tpl="check">
  <h2><span class="tag q">확인하기</span>화학 변화의 자발성 판단하기</h2>
  <p class="f22" data-q><b>1</b> 엔트로피는 증가하고 엔탈피가 감소하는 반응은 항상 ( 자발적이다, 비자발적이다 ).</p>
  <div class="answer step">자발적이다</div>
  <p class="f22 mt16" data-q><b>2</b> 다음 반응의 자발성을 판단해 보자. &nbsp; $\\ce{2A(g) -> B(g)}\\quad\\Delta H&gt;0$</p>
  <p class="f21 mt8 step">기체 분자 수 2 → 1: 엔트로피 감소($\\Delta S&lt;0$) — 불리 · 엔탈피 증가($\\Delta H&gt;0$) — 불리</p>
  <div class="answer step">두 요인 모두 불리 → 항상 비자발적</div>
  <div class="board mt12" style="min-height:110px"></div>
</section>''')

# ───────── 25 소단원 마무리
bub25=''.join(mv(C(x,y,5,'#fff','#7E8B98',1.5),0,30,1.6,0.3*i,rep='loop',ease='lin') for i,(x,y) in enumerate([(92,70),(106,92),(96,112)]))
add(f'''<!-- ════════ 25. 소단원 마무리 ════════ -->
<section class="slide" data-sec="03 · 소단원 마무리" data-title="소단원 마무리">
  <h2><span class="tag">소단원 마무리</span>자발성으로 생활 속 변화 설명하기</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>창의력 키우기</h3>
        <div class="row"><div class="col" style="flex:0 0 190px">
          <svg class="fig" viewBox="0 0 190 200" style="width:190px" aria-label="과산화 수소가 든 갈색 병 속에서 산소 기포가 생긴다">
            <rect x="74" y="10" width="44" height="26" rx="4" fill="#5B6B7F"/>
            <path d="M80 36 L80 52 Q40 60 40 96 L40 180 Q40 192 52 192 L140 192 Q152 192 152 180 L152 96 Q152 60 112 52 L112 36 Z" fill="#B5562A" opacity=".85" stroke="#7A3315" stroke-width="2.5"/>
            {bub25}
            <rect x="58" y="120" width="76" height="40" rx="5" fill="#fff"/>
            {T(96,147,'\\ce{H2O2}',20,'middle',tex=True)}
          </svg></div>
          <div class="col"><p class="f21" data-q>시약용이나 소독용 과산화 수소에는 과산화 수소의 분해를 늦추는 물질인 인산을 첨가하기도 한다. 이처럼 과산화 수소에 인산을 첨가하는 까닭을 화학 반응의 자발성을 이용하여 설명해 보자.</p></div></div>
        <p class="f21 mt8 step em33-a">→ <span class="ans">$\\ce{{2H2O2(l) -> 2H2O(l) + O2(g)}}$은 엔탈피가 감소하고($\\Delta H&lt;0$) 기체가 생겨 엔트로피가 증가하므로($\\Delta S&gt;0$) <b>항상 자발적</b>이다. 보관하는 동안에도 저절로 분해되므로, 인산을 넣어 분해를 늦춰 농도를 오래 유지한다.</span></p>
      </div>
    </div>
    <div class="col" style="flex:0 0 420px">
      <div class="card"><h3>디지털 소양 키우기</h3>
        <p class="f21" data-q>일상생활 속에서 엔트로피가 증가하는 변화를 찾아 사진을 찍고, 공유 플랫폼을 활용하여 공유해 보자.</p>
        <p class="f21 mt8 step em33-a">→ <span class="ans">예: 장작이 탄다, 도미노가 무너진다, 컵 속 얼음이 녹는다, 커피에 각설탕이 녹는다</span></p>
        <p class="small mt8 step">사진마다 "무엇이 더 무질서해졌는지" 한 줄 설명을 함께 올린다.</p>
      </div>
    </div>
  </div>
</section>''')

# ───────── 26 대단원 마무리 08
add('''<!-- ════════ 26. 대단원 마무리 08 ════════ -->
<section class="slide" data-sec="03 · 대단원 마무리" data-title="대단원 마무리 08">
  <h2><span class="tag q">대단원 마무리 08</span>엔트로피에 대한 설명</h2>
  <p class="f22">엔트로피에 대한 설명으로 옳지 <u>않은</u> 것은?</p>
  <div class="row mt8">
    <div class="col">
      <div class="choices em33-ch1">
        <span>① 무질서도를 나타내는 척도이다.</span>
        <span>② 엔트로피의 크기는 물질의 양과 관계가 없다.</span>
        <span>③ 순수한 두 물질이 섞일 때 엔트로피가 증가한다.</span>
        <span>④ 온도가 높아져 분자 운동이 활발해지면 엔트로피가 증가한다.</span>
        <span>⑤ 기체가 더 넓은 공간으로 퍼져 나갈 때 엔트로피가 증가한다.</span>
      </div>
    </div>
    <div class="col stack" style="flex:0 0 420px">
      <p class="f21 step">엔트로피는 물질의 양에 의존하는 성질 — 분자의 수 또는 물질의 양이 늘어나면 엔트로피는 증가한다.</p>
      <div class="board mt8" style="min-height:160px"></div>
    </div>
  </div>
  <div class="answer step"><b>정답 ②</b></div>
</section>''')

# ───────── 27 대단원 마무리 09
ice=''.join(C(40+i*22+(11 if j%2 else 0),56+j*20,9,'#BFE3F2','#7FB3CC',1.2) for i in range(5) for j in range(5))
ice=f'<g data-anim="move" data-from="1,0" data-rep="swing" data-dur=".2">{ice}</g>'
wl=scatter(random.Random(41),18,236,64,350,152,21)
wliq=''.join(C(x,y,9,'#BFE3F2','#7FB3CC',1.2) for x,y in wl)
vg=[(450,60),(520,74),(480,120),(550,140),(440,156),(510,40)]
vap=''.join(mv(C(x,y,9,'#BFE3F2','#7FB3CC',1.2),[12,-10,14,-12,10,-14][i],[-8,12,-10,8,-12,10][i],1+0.2*i,rep='alt',ease='io') for i,(x,y) in enumerate(vg))
add(f'''<!-- ════════ 27. 대단원 마무리 09 ════════ -->
<section class="slide" data-sec="03 · 대단원 마무리" data-title="대단원 마무리 09">
  <h2><span class="tag q">대단원 마무리 09</span>융해와 기화의 엔트로피 변화 비교</h2>
  <p class="f22">그림은 1 기압에서 얼음을 가열할 때 나타나는 상태 변화를 모형으로 나타낸 것이다.</p>
  <svg class="fig mt8" viewBox="0 0 600 200" style="width:600px" aria-label="얼음이 0 도에서 물이 되는 과정 (가)와 물이 100 도에서 수증기가 되는 과정 (나)">
    <rect x="20" y="36" width="140" height="130" rx="14" fill="#fff" stroke="#9FB0C2" stroke-width="2.5"/>
    <rect x="222" y="36" width="140" height="130" rx="14" fill="#fff" stroke="#9FB0C2" stroke-width="2.5"/>
    <rect x="424" y="26" width="156" height="150" rx="14" fill="#fff" stroke="#9FB0C2" stroke-width="2.5"/>
    {ice}{wliq}{vap}
    {A(168,100,214,100,'ink',3)}{A(370,100,416,100,'ink',3)}
    {T(191,84,'(가)',19,'middle')}{T(191,130,'0 °C',19,'middle')}{T(393,84,'(나)',19,'middle')}{T(393,130,'100 °C',19,'middle')}
    {T(90,192,'얼음',19,'middle')}{T(292,192,'물',19,'middle')}{T(502,196,'수증기',19,'middle')}
  </svg>
  <div class="row mt8">
    <div class="col">
      <p class="f21" data-q>과정 (가)와 (나)의 엔트로피 변화 $\\Delta S_\\text{{(가)}}$와 $\\Delta S_\\text{{(나)}}$의 크기를 등호 또는 부등호($&gt;$, $=$, $&lt;$)를 사용하여 비교해 보자. <span class="small">(단, 비교하는 물질의 질량은 같다.)</span></p>
      <p class="f21 mt8 step">(가) 융해, (나) 기화 — 둘 다 $\\Delta S&gt;0$</p>
      <p class="f21 step">기체는 분자가 자유롭게 움직여 액체보다 훨씬 무질서하다 → 기화의 엔트로피 증가가 더 크다.</p>
    </div>
    <div class="col stack" style="flex:0 0 300px"><div class="board" style="min-height:120px"></div></div>
  </div>
  <div class="answer step">$\\Delta S_\\text{{(가)}}&lt;\\Delta S_\\text{{(나)}}$</div>
</section>''')

# ───────── 28 대단원 마무리 10
add('''<!-- ════════ 28. 대단원 마무리 10 ════════ -->
<section class="slide" data-sec="03 · 대단원 마무리" data-title="대단원 마무리 10">
  <h2><span class="tag q">대단원 마무리 10</span>세 반응의 공통적인 성질</h2>
  <p class="f22">(가)~(다)는 우리 주위에서 볼 수 있는 반응의 열화학 반응식이다. 반응 (가)~(다)에서 나타나는 공통적인 성질로 옳은 것은?</p>
  <div class="row mt8">
    <div class="col" style="flex:0 0 640px">
      <table class="em33-eqt em33-box">
        <tr><td>(가)</td><td class="l">$\\ce{CO2(s) -> CO2(g)}$</td><td>$\\Delta H=25.2\\ \\text{kJ}$</td></tr>
        <tr><td>(나)</td><td class="l">$\\ce{2C(s) + O2(g) -> 2CO(g)}$</td><td>$\\Delta H=-221.0\\ \\text{kJ}$</td></tr>
        <tr><td>(다)</td><td class="l">$\\ce{2H2O2(l) -> 2H2O(l) + O2(g)}$</td><td>$\\Delta H=-196.4\\ \\text{kJ}$</td></tr>
      </table>
      <div class="choices mt12"><span>① 흡열 반응이다.</span><span>② 엔탈피가 감소한다.</span><span>③ 엔트로피가 증가한다.</span><span>④ 비자발적인 반응이다.</span><span>⑤ 기체 입자 수가 감소한다.</span></div>
    </div>
    <div class="col stack">
      <p class="f21 step">기체의 양(mol): (가) 0 → 1, (나) 1 → 2, (다) 0 → 1 — 모두 <b>증가</b></p>
      <p class="f21 mt8 step">①은 (가)만, ②는 (나)와 (다)만 해당한다.</p>
      <div class="board mt8" style="min-height:90px"></div>
    </div>
  </div>
  <div class="answer step"><b>정답 ③</b> <span class="small">(세 반응 모두 기체가 늘어나 엔트로피가 증가한다)</span></div>
</section>''')

# ───────── 29 대단원 마무리 11 서술형
add('''<!-- ════════ 29. 대단원 마무리 11 ════════ -->
<section class="slide" data-sec="03 · 대단원 마무리" data-title="대단원 마무리 11 (서술형)">
  <h2><span class="tag q">대단원 마무리 11</span><span class="tag q">서술형</span>흡열 반응이 자발적으로 일어나는 까닭</h2>
  <p class="f22" data-q>휴대용 냉각 팩 속에서 질산 암모늄이 물에 용해되는 반응은 흡열 반응이며, 자발적으로 일어난다. 이 반응에서 나타나는 엔트로피 변화를 입자 관점에서 설명하고, 이를 근거로 흡열 반응이 어떻게 자발적으로 일어날 수 있는지 설명해 보자.</p>
  <div class="board mt8" style="min-height:120px"></div>
  <div class="answer step em33-left"><b>예시 답안</b> 고체 질산 암모늄이 물에 녹아 $\\ce{NH4+}$과 $\\ce{NO3-}$으로 나뉘면 입자 수가 늘고, 이온들이 물 분자 사이로 섞여 들어가 자유롭게 움직이므로 무질서도가 커져 엔트로피가 크게 증가한다($\\Delta S&gt;0$). 엔탈피는 증가하지만($\\Delta H&gt;0$), 엔트로피를 높이려는 경향이 엔탈피가 증가하는 경향보다 크므로 반응이 자발적으로 일어난다.</div>
  <div class="note mt8 step" data-ask="no"><b>채점 요소</b> ① 입자 수 증가, 이온이 물에 섞여 입자 운동이 자유로워짐 ② 엔트로피 증가($\\Delta S&gt;0$) ③ 엔트로피 증가의 영향이 엔탈피 증가의 영향보다 큼</div>
</section>''')

# ───────── 30 스스로 정리
add('''<!-- ════════ 30. 스스로 정리 ════════ -->
<section class="slide" data-sec="03 화학 변화의 자발성 · 마무리" data-title="스스로 정리">
  <h2><span class="tag ink">스스로 정리</span>화학 변화의 자발성 — 개념 지도</h2>
  <div class="em33-map">
    <div class="em33-node em33-dim">01 화학 반응과 엔탈피<br><span class="small">$\\Delta H=H_\\text{생성물}-H_\\text{반응물}$</span></div>
    <div class="em33-node em33-dim">02 반응 경로와 반응 엔탈피<br><span class="small">헤스 법칙</span></div>
    <div class="em33-node em33-main"><b>03 화학 변화의 자발성</b><br>자발적 변화: 외부의 지속적인 도움 없이 스스로 일어나는 변화</div>
  </div>
  <table class="tight mt12 em33-sum">
    <tr><th>무질서도의 척도</th><td class="l" data-q>❻ <span class="blank"><span class="step">엔트로피</span></span> (기호 $S$)</td></tr>
    <tr><th>엔트로피 변화</th><td class="l" data-q>$\\Delta S=$ ⓐ <span class="blank em33-wide"><span class="step">$S_\\text{최종}-S_\\text{초기}$</span></span></td></tr>
    <tr><th>엔트로피가 커질 때</th><td class="l" data-q>분자 움직임이 활발해질 때, 순수한 두 물질이 섞일 때, 입자 수가 증가할 때는 엔트로피가 ❼ <span class="blank"><span class="step">증가</span></span>함.</td></tr>
    <tr><th>자발성의 방향</th><td class="l" data-q>❽ <span class="blank"><span class="step">엔탈피</span></span>이/가 감소하면서 안정해지려는 방향 + ❾ <span class="blank"><span class="step">엔트로피</span></span>이/가 증가하면서 무질서해지려는 방향</td></tr>
    <tr><th>판단</th><td class="l" data-q>$\\Delta H&lt;0$, $\\Delta S&gt;0$인 반응은 항상 ⓑ <span class="blank"><span class="step">자발적</span></span>이다.</td></tr>
  </table>
  <p class="small mt8">❻–❾는 교과서 88쪽 대단원 마무리 개념 정리의 빈칸 번호, ⓐ ⓑ는 덧붙인 빈칸이다.</p>
</section>''')

# ───────── 31 스스로 점검하기
add('''<!-- ════════ 31. 스스로 점검하기 ════════ -->
<section class="slide" data-sec="03 화학 변화의 자발성 · 마무리" data-title="스스로 점검하기">
  <h2><span class="tag q">스스로 점검하기</span>오늘 배운 것 점검하기</h2>
  <div class="chips col1">
    <button class="chk">[지식·이해] 엔탈피와 엔트로피의 의미를 알고, 엔탈피와 엔트로피 변화로 화학 변화의 자발성을 설명했다.</button>
    <button class="chk">[과정·기능] 상태 변화·혼합·입자 수 변화로 엔트로피 변화의 부호를 예측하고, 동전 실험실로 무질서도와 확률의 관계를 확인했다.</button>
    <button class="chk">[가치·태도] 주변에서 일어나는 변화를 엔탈피와 엔트로피 변화로 설명할 수 있음을 이해하여 화학의 중요성을 인식했다.</button>
  </div>
  <div class="card mt16">
    <p class="f21"><b>Q</b> 드라이아이스가 승화할 때 $\\Delta S$의 부호는? <span class="step">→ <span class="ans">$\\Delta S&gt;0$</span></span></p>
    <p class="f21 mt8"><b>Q</b> $\\Delta H&lt;0$이고 $\\Delta S&lt;0$인 반응이 자발적이려면? <span class="step">→ <span class="ans">엔탈피 감소의 영향이 엔트로피 감소의 영향보다 커야 한다</span></span></p>
    <p class="f21 mt8"><b>Q</b> 자발적 변화는 항상 빠르게 일어날까? <span class="step">→ <span class="ans">아니다 (예: 철의 부식)</span></span></p>
  </div>
  <div class="note puzzle mt16"><b>다음 시간</b> 대단원 Ⅲ 마무리 — 엔탈피, 헤스 법칙, 엔트로피를 하나의 개념 지도로 이어 보자.</div>
</section>''')

open(OUT,'w',encoding='utf-8').write('\n\n'.join(S)+'\n')
print(len(S),'slides')
