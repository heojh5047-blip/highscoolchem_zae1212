# 슬라이드 6–30 (gen.py 안에서 exec) — 교과서 97–101쪽 대조판
def T(tpl, **kw):
    for k,v in kw.items(): tpl=tpl.replace('[['+k+']]', v)
    return tpl
OLD=open('/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학_미래엔_3-1-1/gen2_old.py').read().split('\n')
def old(a,b): exec('\n'.join(OLD[a-1:b]), globals())
del S[5:]
SECA='01 · 가역 반응과 비가역 반응'; SECD='01 · 화학 평형'; SECE='01 · 화학 평형'
def patch(i,*pairs):
    for a,b in pairs:
        assert a in S[i], a[:60]; S[i]=S[i].replace(a,b)

# ---------- 6. 생각 열기: 변색 렌즈 ----------
def glasses(x,y,lens,op):
    o=''
    for dx in (0,120):
        o+=f'<ellipse cx="{x+dx}" cy="{y}" rx="50" ry="38" fill="{lens}" fill-opacity="{op}" stroke="#16233D" stroke-width="5"/>'
    o+=f'<path d="M{x+50} {y-6} Q{x+60} {y-18} {x+70} {y-6}" fill="none" stroke="#16233D" stroke-width="5"/>'
    o+=f'<path d="M{x-50} {y-10} L{x-80} {y-22} M{x+170} {y-10} L{x+200} {y-22}" stroke="#16233D" stroke-width="5" stroke-linecap="round"/>'
    return o
g=''
g+='<rect x="0" y="0" width="270" height="250" rx="16" fill="#FFF6D6"/><rect x="290" y="0" width="270" height="250" rx="16" fill="#EEF2F6"/>'
g+='<circle cx="226" cy="44" r="22" fill="#F2C230"/>'+''.join(f'<path d="M{226+30*math.cos(math.radians(a))} {44+30*math.sin(math.radians(a))} L{226+42*math.cos(math.radians(a))} {44+42*math.sin(math.radians(a))}" stroke="#F2C230" stroke-width="4" stroke-linecap="round"/>' for a in range(0,360,45))
g+=f'<g data-anim="fade" data-dur="1.2" data-delay=".5">{glasses(75,140,"#3A3F47",.75)}</g>'
g+=glasses(365,140,'#DDEEF8',.35)
g+=tex(135,226,'야외: 선글라스',21,weight=700,fill=INK)+tex(425,226,'실내: 안경',21,weight=700,fill=INK)
add(T('''<!-- ════════ 6. 생각 열기 ════════ -->
<section class="slide" data-sec="01 가역 반응과 화학 평형 · 도입" data-title="생각 열기: 변색 렌즈 안경">
  <h2><span class="tag">생각 열기</span>야외에서는 선글라스, 실내에서는 안경!</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px">
      <svg class="fig" viewBox="0 0 560 250" style="width:560px" aria-label="햇빛 아래에서 렌즈가 어두워진 안경과 실내에서 투명한 안경">[[G]]</svg>
    </div>
    <div class="col">
      <p class="f22">변색 렌즈 안경은 햇빛을 받으면 렌즈의 색이 어둡게 변해 선글라스 역할을 하고, 실내에서는 색이 없어져 안경으로 쓴다.</p>
      <p class="f22 mt12" data-q><b>Q</b> 장소에 따라 렌즈의 색이 변하는 까닭은 무엇일까?</p>
    </div>
  </div>
  <div class="answer step mt16">렌즈 속 물질이 햇빛을 받으면 색을 띠는 물질로 변하고, 햇빛이 없으면 다시 원래 물질로 되돌아간다. → 조건에 따라 <b>양쪽 방향</b>으로 일어나는 반응</div>
</section>''', G=g))

# ---------- 7. 연결: 소금과 메테인 ----------
def dish(cx,cy,cont=None,burner=False,dropper=False,w=70):
    o=''
    if burner:
        o+=f'<path d="M{cx-34} {cy+40} H{cx+34} M{cx-30} {cy+12} L{cx-40} {cy+92} M{cx+30} {cy+12} L{cx+40} {cy+92}" stroke="#5B6B7F" stroke-width="3"/>'
        o+=f'<path d="M{cx-22} {cy+120} H{cx+22} L{cx+16} {cy+92} H{cx-16} Z" fill="#EEF2F6" stroke="#16233D" stroke-width="2.5"/>'
        o+=f'<path d="M{cx} {cy+92} Q{cx-12} {cy+76} {cx} {cy+52} Q{cx+12} {cy+76} {cx} {cy+92} Z" fill="#F2A541" stroke="#E08A2C" stroke-width="1.5"/>'
    o+=f'<path d="M{cx-w} {cy} Q{cx} {cy+44} {cx+w} {cy} Z" fill="#FFFFFF" stroke="#7E8B98" stroke-width="3" stroke-linejoin="round"/>'
    if cont:
        o+=f'<path d="M{cx-w*.62} {cy+6} Q{cx} {cy+30} {cx+w*.62} {cy+6} Q{cx} {cy-4} {cx-w*.62} {cy+6} Z" fill="{cont}" stroke="#7E8B98" stroke-width="1.2"/>'
    if dropper:
        o+=f'<rect x="{cx-7}" y="{cy-96}" width="14" height="30" rx="6" fill="#E08A2C"/>'
        o+=f'<path d="M{cx-5} {cy-66} H{cx+5} L{cx+2} {cy-34} H{cx-2} Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/>'
        o+=f'<g data-anim="move" data-from="0,-14" data-dur=".9" data-delay=".5" data-rep="loop" data-ease="in"><ellipse cx="{cx}" cy="{cy-18}" rx="4" ry="5.5" fill="#6FA8DC"/></g>'
    return o
c1=dish(120,110,'#F4F6F8',burner=True)+''.join(f'<rect x="{x}" y="{y}" width="9" height="9" fill="#FFFFFF" stroke="#8C99A6" stroke-width="1.2" transform="rotate(20 {x} {y})"/>' for x,y in [(96,108),(112,112),(130,110),(146,106)])
c1+=tex(120,262,'소금물 → 증발 → 소금',20,fill=INK)
c2='<path d="M350 230 H470" stroke="#16233D" stroke-width="3"/><path d="M410 226 Q370 190 392 150 Q398 172 408 164 Q402 130 424 108 Q420 150 436 170 Q448 200 410 226 Z" fill="#F2A541" stroke="#E08A2C" stroke-width="2"/>'
c2+=tex(410,262,'메테인의 연소',20,fill=INK)
add(T('''<!-- ════════ 7. 연결 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="되돌아갈 수 있는 반응, 없는 반응">
  <h2><span class="tag alt">연결</span>원래 모습으로 되돌아갈 수 있을까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 540px">
      <svg class="fig" viewBox="0 0 540 280" style="width:540px" aria-label="소금물을 증발 접시에서 가열해 소금을 얻는 모습과 메테인이 타는 불꽃">[[C]]</svg>
    </div>
    <div class="col">
      <p class="f22">소금을 물에 녹인 뒤 물을 증발시키면 다시 소금이 석출된다.</p>
      <p class="f22 mt8">메테인($\\ce{CH4}$)이 연소하여 생긴 이산화 탄소와 물은 다시 메테인과 산소가 되기 매우 어렵다.</p>
      <div class="formula sm mt12">$\\ce{CH4(g) + 2O2(g) -&gt; CO2(g) + 2H2O(l)}$</div>
      <p class="f22 mt12" data-q><b>Q</b> 화학 반응 가운데 원래 모습으로 되돌아갈 수 있는 반응과 없는 반응을 어떻게 구분할까? → 해 보기로 관찰하자.</p>
    </div>
  </div>
</section>''', S=SECA, C=c1+c2))

# ---------- 8. 해 보기: 황산 구리(II)와 설탕 ----------
k1=dish(130,90,'#3E8ED0',burner=True)+tex(130,252,'파란색 → ?',30,fill=INK)
k2=dish(130,150,'#F4F6F8',dropper=True)+tex(130,252,'물을 넣으면?',30,fill=INK)
k3=dish(130,90,'#FFFFFF',burner=True)+tex(130,252,'흰색 → ?',30,fill=INK)
k4=dish(130,150,'#7A4A22',dropper=True)+tex(130,252,'물을 넣으면?',30,fill=INK)
cards=''.join(f'<div class="stage"><h3>{a}</h3><svg viewBox="0 0 260 266" style="height:170px" aria-label="{lab}">{c}</svg><p>{b}</p></div>' for a,b,c,lab in [
 ('1','증발 접시에 파란색 황산 구리(II) 오수화물을 담고 색이 변할 때까지 가열한다.',k1,'황산 구리(II) 오수화물을 증발 접시에서 가열'),
 ('2','1의 증발 접시에 물을 떨어뜨리고 색 변화를 관찰한다.',k2,'흰색 가루에 물을 떨어뜨림'),
 ('3','증발 접시에 백설탕을 담고 색이 변할 때까지 가열한다.',k3,'백설탕을 증발 접시에서 가열'),
 ('4','3의 증발 접시에 물을 떨어뜨리고 색 변화를 관찰한다.',k4,'갈색으로 변한 설탕에 물을 떨어뜨림')])
add(T('''<!-- ════════ 8. 해 보기 ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기: 황산 구리(II)와 설탕의 변화">
  <h2><span class="tag">해 보기</span>황산 구리(II)와 설탕의 변화 관찰하기 <span class="small c-muted">실험 영상</span></h2>
  <p class="small">탐구 능력 | 의사 결정 능력 · 준비물: 황산 구리(II) 오수화물, 백설탕, 증발 접시, 가열 장치, 스포이트, 비커, 물</p>
  <div class="cm311-s4 mt8">[[C]]</div>
  <div class="note q mt12"><b>안전</b> 실험복·보안경·실험용 고무장갑을 착용하고, 가열 장치는 안전 장갑을 끼고 다룬다. 남은 황산 구리(II) 오수화물은 고체 폐기물 수집 용기에 버린다.</div>
</section>''', C=cards))

# ---------- 9. 결과 + 가역 반응 ----------
sq=lambda x,c,lab: f'<rect x="{x}" y="40" width="130" height="80" rx="10" fill="{c}" stroke="#7E8B98" stroke-width="2"/>'+tex(x+65,150,lab,20,fill=INK)
c=sq(20,'#3E8ED0','$\\ce{CuSO4*5H2O}$||파란색')+f'<g data-anim="fade" data-dur="1" data-delay=".6">{sq(390,"#F4F6F8","$\\ce{CuSO4}$||흰색")}</g>'
c+=eqarrows(180,80,180,lab_top='가열 (물이 빠져나감)',lab_bot='물을 떨어뜨림',size=19)
add(T('''<!-- ════════ 9. 가역 반응 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="가역 반응">
  <h2><span class="no">1</span>가역 반응</h2>
  <div class="row">
    <div class="col" style="flex:0 0 540px">
      <p class="f21" data-q><b>Q</b> 해 보기 결과, 가열 전 상태로 되돌아갈 수 있는 것은?</p>
      <svg class="fig mt8 step" data-g="v1" viewBox="0 0 540 196" style="width:520px" aria-label="파란색 황산 구리(II) 오수화물은 가열하면 흰색, 물을 떨어뜨리면 다시 파란색">[[C]]</svg>
      <p class="f21 step" data-g="v1">→ <span class="ans">황산 구리(II) 오수화물</span>: 가열하면 물 분자가 빠져나가 흰색이 되고, 물을 떨어뜨리면 다시 파란색이 된다.</p>
    </div>
    <div class="col">
      <p class="f21 step" data-g="v2">반응물이 생성물로 되는 반응을 <b class="c-field">정반응</b>, 생성물이 반응물로 되는 반응을 <b style="color:#7B4FC8">역반응</b>이라고 한다.</p>
      <p class="f21 mt8 step" data-g="v2"><mark>반응 조건에 따라 정반응과 역반응이 모두 일어날 수 있는 반응</mark>을 <b>가역 반응</b>이라고 하며, 하나의 반응식으로 나타낸다.</p>
      <p class="small mt8 step" data-g="v2">화살표: 정반응 $\\ce{-&gt;}$, 역반응 $\\ce{&lt;-}$, 가역 반응 $\\ce{&lt;=&gt;}$</p>
    </div>
  </div>
  <div class="formula sm mt8 step" data-g="v3">$\\ce{CuSO4*5H2O(s) &lt;=&gt; CuSO4(s) + 5H2O(l)}$<div class="unit">파란색 &nbsp;⇄&nbsp; 흰색</div></div>
  <p class="small mt8">수화물: 물 분자를 포함한 화합물. 황산 구리(II) 오수화물은 물 분자 5개를 포함한 황산 구리(II)이다.</p>
</section>''', S=SECA, C=c))

# ---------- 10. 비가역 반응: 설탕 ----------
c=dish(90,70,'#FFFFFF')+tex(90,150,'설탕 (흰색)',20,fill=INK)+arw(170,80,220,80,'ink',3)+tex(195,62,'가열',18,fill=MUTED)
c+=dish(300,70,'#7A4A22')+tex(300,150,'가열한 설탕 (갈색)',20,fill=INK)+arw(380,80,430,80,'ink',3)+tex(405,62,'물',18,fill='#1F6FD1')
c+=dish(510,70,'#7A4A22',w=60)+tex(510,150,'가열한 설탕 + 물',20,fill=INK)+tex(510,178,'여전히 갈색',20,fill='#D7263D',weight=700)
add(T('''<!-- ════════ 10. 비가역 반응 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="비가역 반응">
  <h2><span class="no">1</span>비가역 반응</h2>
  <svg class="fig" viewBox="0 0 600 190" style="width:600px" aria-label="흰색 설탕을 가열하면 갈색이 되고, 물을 넣어도 흰색으로 돌아가지 않음">[[C]]</svg>
  <p class="f22 mt8">흰색 설탕을 가열하면 높은 온도에서 물이 빠져나가고 설탕 분자의 결합 구조가 깨지면서 여러 화합물이 생겨 갈색으로 변한다.</p>
  <p class="f22 mt8" data-q><b>Q</b> 빠져나간 물을 다시 넣어 주면 흰색 설탕으로 돌아갈까?</p>
  <div class="answer step mt8">돌아가지 않는다. 이처럼 <mark>한 방향으로만 일어나는 반응</mark>을 <b>비가역 반응</b>이라고 한다.</div>
  <div class="note step mt12"><b>덧붙임</b> 중화 반응·앙금 생성 반응도 미시적으로는 역반응이 일어날 수 있지만, 정반응이 훨씬 우세하여 한쪽으로만 일어나는 것처럼 보이므로 비가역 반응으로 본다.</div>
</section>''', S=SECA, C=c))

# ---------- 11. 우리 주변 ----------
cv=cave(0,-34,0.5,drop=True,labels=False)
add(T('''<!-- ════════ 11. 우리 주변 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="우리 주변의 가역 반응과 비가역 반응">
  <h2><span class="no">1</span>우리 주변의 가역 반응과 비가역 반응</h2>
  <div class="row">
    <div class="col">
      <h3 class="c-field">가역 반응</h3>
      <div class="card"><p class="f21"><b>석회 동굴의 생성</b></p><p class="f21">$\\ce{CaCO3(s) + H2O(l) + CO2(g) &lt;=&gt; Ca(HCO3)2(aq)}$</p>
        <p class="small">정반응: 석회암이 녹아 동굴 생성 · 역반응: 종유석·석순 생성</p></div>
      <div class="card mt12"><p class="f21"><b>암모니아의 합성</b></p><p class="f21">$\\ce{N2(g) + 3H2(g) &lt;=&gt; 2NH3(g)}$</p></div>
    </div>
    <div class="col" style="flex:0 0 470px">
      <h3>비가역 반응</h3>
      <div class="card"><p class="f21"><b>메테인의 연소</b></p><p class="f21">$\\ce{CH4(g) + 2O2(g) -&gt; CO2(g) + 2H2O(l)}$</p></div>
      <div class="card mt12"><p class="f21"><b>마그네슘과 염산의 반응</b></p><p class="f21">$\\ce{Mg(s) + 2HCl(aq) -&gt; MgCl2(aq) + H2(g)}$</p><p class="small">수소 기체가 생성되어 빠져나간다.</p></div>
    </div>
  </div>
</section>''', S=SECA, CV=cv))

# ---------- 12. 확인하기 (99쪽) ----------
add('''<!-- ════════ 12. 확인하기 ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 가역 반응과 비가역 반응" data-tpl="check">
  <h2><span class="tag q">확인하기</span>가역 반응과 비가역 반응</h2>
  <ol class="cm311-ox">
    <li>반응물이 생성물로 되는 반응을 (<span class="blank"><span class="step">정반응</span></span>)(이)라 하고, 생성물이 반응물로 되는 반응을 (<span class="blank"><span class="step">역반응</span></span>)(이)라고 한다.</li>
    <li>반응 조건에 따라 정반응과 역반응이 모두 일어날 수 있는 반응을 (<span class="blank"><span class="step">가역</span></span>) 반응이라 하고, 한 방향으로만 일어나는 반응을 (<span class="blank"><span class="step">비가역</span></span>) 반응이라고 한다.</li>
  </ol>
  <div class="note mt28"><b>더 생각하기</b> 물을 끓이면 수증기가 되고, 수증기를 식히면 다시 물이 된다. 이 상태 변화도 두 방향으로 일어난다. 다음에는 이 변화로 '평형'을 알아본다.</div>
</section>''')

# ---------- 13–14. 밀폐된 병의 물, 동적 평형 ----------
old(86,110)
patch(-1,('<span class="tag alt">연결</span>닫힌 용기 속 물은 증발을 멈춘 것일까?','<span class="no">2</span>밀폐된 병 속의 물은 증발을 멈춘 것일까?'),
 ('<p class="f22">뚜껑 없는 비커의 물은 점점 줄어들지만, 마개를 닫은 용기의 물은 며칠이 지나도 수면의 높이가 변하지 않는다.</p>','<p class="f22">물이 든 병의 뚜껑을 닫아 밀폐하면 병 속의 물은 처음에는 줄어들지만, 오랜 시간이 지나면 <b>일정하게 유지</b>된다.</p>'),
 ('data-sec="01 · 화학 평형"','data-sec="01 · 화학 평형"'))
old(112,135)
patch(-1,('''  <p class="f22 mt8 step" data-g="d1"><mark>정반응 속도와 역반응 속도가 같아서 겉으로는 변화가 없어 보이지만, 실제로는 두 반응이 계속 일어나는 상태</mark>를 <b>동적 평형</b>이라고 한다.</p>
  <p class="f22 mt8 step" data-g="d2">물과 수증기 사이의 동적 평형을 <b>상평형</b>이라고 한다: $\\ce{H2O(l) &lt;=&gt; H2O(g)}$</p>''',
'''  <p class="f22 mt8 step" data-g="d1">이처럼 <mark>정반응 속도와 역반응 속도가 같아서 겉으로는 변화가 일어나지 않는 것처럼 보이는 상태</mark>를 <b>동적 평형</b>이라고 한다.</p>
  <p class="f21 mt8 step" data-g="d2"><b>상평형</b> 물과 수증기가 공존하는 것처럼, 물질의 상태 가운데 두 가지 이상이 동적 평형을 유지하는 것: $\\ce{H2O(l) &lt;=&gt; H2O(g)}$</p>'''),
 ('<span class="no">2</span>동적 평형 — 물과 수증기','<span class="no">2</span>동적 평형 — 물과 수증기'))

# ---------- 15. 해 보기: 동적 평형 상태 해석하기 ----------
def bottle(x,c0,c1,lab):
    o=f'<rect x="{x}" y="40" width="70" height="140" rx="10" fill="{c0}" fill-opacity="{0.85 if c0!="#FFFFFF" else 0}" stroke="#7E8B98" stroke-width="3"/><rect x="{x+8}" y="20" width="54" height="22" rx="4" fill="#3A3F47"/>'
    o+=arw(x+86,110,x+136,110,'field',4)
    o+=f'<rect x="{x+152}" y="40" width="70" height="140" rx="10" fill="{c1}" fill-opacity=".55" stroke="#7E8B98" stroke-width="3"/><rect x="{x+160}" y="20" width="54" height="22" rx="4" fill="#3A3F47"/>'
    o+=tex(x+35,206,lab,20,fill=INK)
    return o
bt=bottle(20,'#B5562A','#C77A4E','$\\ce{NO2(g)}$')+bottle(330,'#FFFFFF','#D79A72','$\\ce{N2O4(g)}$')
bt+=tex(10,24,'(가)',20,anchor='start',weight=700)+tex(320,24,'(나)',20,anchor='start',weight=700)
bt+=tex(130,240,'색이 점점 옅어지다가 일정',19,fill=MUTED)+tex(440,240,'색이 점점 진해지다가 일정',19,fill=MUTED)
add(T('''<!-- ════════ 15. 해 보기: 동적 평형 해석 ════════ -->
<section class="slide" data-sec="01 · 해 보기" data-title="해 보기: 동적 평형 상태 해석하기">
  <h2><span class="tag">해 보기</span>가역 반응에서 동적 평형 상태 해석하기 <span class="small c-muted">모의실험</span></h2>
  <p class="f21">적갈색 이산화 질소($\\ce{NO2}$)가 반응하여 무색 사산화 이질소($\\ce{N2O4}$)를 생성하는 반응은 가역적이다: $\\ce{2NO2(g) &lt;=&gt; N2O4(g)}$. 일정한 온도에서 각 기체를 뚜껑 있는 유리병에 넣고 닫아 두었다.</p>
  <div class="row mt8">
    <div class="col" style="flex:0 0 580px"><svg class="fig" viewBox="0 0 580 250" style="width:560px" aria-label="(가) 적갈색 이산화 질소 병은 색이 옅어지고, (나) 무색 사산화 이질소 병은 색이 진해짐">[[C]]</svg></div>
    <div class="col">
      <p class="f21"><b>Q</b> 1. (가)에서 색이 점점 옅어지고, (나)에서 색이 점점 진해지는 까닭은?</p>
      <p class="f21 step cm311-a">→ (가) 적갈색 $\\ce{NO2}$가 무색 $\\ce{N2O4}$로 되는 <b>정반응 속도</b>가 역반응 속도보다 빠르기 때문이다. (나) 반대로 <b>역반응 속도</b>가 정반응 속도보다 빠르기 때문이다.</p>
      <p class="f21 mt12"><b>Q</b> 2. 시간이 충분히 흐른 뒤 색이 일정하게 유지되는 까닭은?</p>
      <p class="f21 step cm311-a">→ (가)와 (나) 모두 시간이 충분히 흐르면 정반응 속도와 역반응 속도가 <span class="ans">같아지는</span> 동적 평형 상태에 도달하여 두 기체의 농도가 일정하게 유지되기 때문이다.</p>
    </div>
  </div>
</section>''', C=bt))

# ---------- 16. 실험실 (모의실험) ----------
old(285,316)
patch(-1,('<span class="tag">실험실</span>평형에 도달하기','<span class="tag">해 보기</span>모의실험: 평형에 도달하기'),('data-title="실험실: 평형에 도달하기"','data-title="모의실험: 평형에 도달하기"'),('data-sec="01 · 화학 평형"','data-sec="01 · 해 보기"'))

# ---------- 17. 화학 평형: 입자 ----------
old(168,182)
cards=[('(가) 초기 상태','$\\ce{NO2}$ 12개 · 적갈색',no2_card(12,0,.5,150,0,21)),
       ('평형 상태','$\\ce{NO2}$ 2개, $\\ce{N2O4}$ 5개 · 색 일정',no2_card(2,5,.2,60,60,26,anim=True)),
       ('(나) 초기 상태','$\\ce{N2O4}$ 6개 · 무색',no2_card(0,6,0,0,150,27))]
st=''.join(f'<div class="stage"><h3>{a}</h3><svg viewBox="0 0 300 272" style="height:212px" aria-label="밀폐 용기 속 이산화 질소와 사산화 이질소 분자">{c}</svg><p class="key">{b}</p></div>' for a,b,c in cards)
st=st.replace('<div class="stage"><h3>평형 상태','<div class="stage cm311-eqc"><h3>→ 평형 상태 ←')
add(T('''<!-- ════════ 17. 화학 평형 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="화학 평형: 2NO₂ ⇌ N₂O₄">
  <h2><span class="no">3</span>화학 평형 — $\\ce{2NO2(g) &lt;=&gt; N2O4(g)}$</h2>
  <p class="f21">일정한 온도에서 밀폐 용기에 (가) $\\ce{NO2}$만 넣으면 정반응이 우세하여 색이 연해지고, (나) $\\ce{N2O4}$만 넣으면 역반응이 우세하여 색이 진해진다. 두 경우 모두 시간이 지나면 색이 일정해진다.</p>
  <div class="stages mt8">[[C]]</div>
  <p class="small mt8">$\\mathrm{N}$ 원자 수: $12=2+5\\times2=6\\times2$ (보존) · 모형: $\\mathrm{N}$ 파란 공, $\\mathrm{O}$ 빨간 공 · 화살표 길이 = 반응 속도</p>
  <div class="answer step mt8">평형 상태에서도 정반응과 역반응은 <b>같은 속도로 계속</b> 일어난다(동적 평형).</div>
</section>''', S=SECE, C=st))

# ---------- 18. 농도 그래프 (그림 III-5 꼴) ----------
def kin(m0, n=80,tmax=3.2,kr=0.1):
    m=m0; dt=0.0005; t=0; out=[(0,1-2*m,m)]
    steps=int(tmax/dt); every=steps//n
    for i in range(1,steps+1):
        nn=1-2*m; m+=dt*3*(nn*nn-kr*m); t+=dt
        if i%every==0: out.append((t,1-2*m,m))
    return out
def graph(m0,anim=True,W=560,H=210,cap=None):
    K=kin(m0); X0,Y0,X1,Y1=64,202,W-24,20; tmax=3.2; t1=1.5
    X=lambda t:X0+(X1-X0)*t/tmax; sc=lambda v:Y0-v*176
    o=f'<rect x="{f(X(t1))}" y="{Y1}" width="{f(X1-X(t1))}" height="{Y0-Y1}" fill="#FFE45C" fill-opacity=".25"/>'
    o+=f'<path d="M{f(X(t1))} {Y1} V{Y0}" stroke="#5B6B7F" stroke-width="2" stroke-dasharray="6 5"/>'
    o+=arw(X0,Y0,X1+14,Y0,'ink',2)+arw(X0,Y0,X0,Y1-10,'ink',2)
    o+=tex(X(t1),Y0+24,'$t_1$',20)+tex(X1+6,Y0+26,'시간',19,anchor='end',fill=INK)+tex(X0-8,Y0+22,'0',18,anchor='end',fill=INK)
    o+=tex((X(t1)+X1)/2,Y1+22,'화학 평형',19,fill='#8A6D00',weight=700)+tex(X0+12,Y1+4,'농도',19,anchor='start',fill=INK)
    A=' data-anim="draw" data-dur="1.6" data-delay=".3"' if anim else ''
    o+=f'<path d="{path([(X(t),sc(a)) for t,a,b in K])}" fill="none" stroke="{NO2C}" stroke-width="4"{A}/>'
    o+=f'<path d="{path([(X(t),sc(b)) for t,a,b in K])}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-dasharray="12 6"{A}/>'
    ea,eb=K[-1][1],K[-1][2]
    o+=tex(X1-4,sc(eb)-9,'$[\\ce{N2O4}]$',20,anchor='end',fill=INK)
    o+=tex(X1-4,sc(ea)-8,'$[\\ce{NO2}]$',20,anchor='end',fill=NO2C)
    if cap: o+=tex(X0+150,Y1+4,cap,19,anchor='start',fill=MUTED)
    return o
EQ=kin(0)[-1]
add(T('''<!-- ════════ 18. 그래프 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="시간에 따른 농도 변화">
  <h2><span class="no">3</span>시간에 따른 농도 변화</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px">
      <svg class="fig" viewBox="0 0 560 240" style="width:520px" aria-label="이산화 질소만 넣었을 때 농도-시간 그래프">[[G1]]</svg>
      <svg class="fig mt8" viewBox="0 0 560 240" style="width:520px" aria-label="사산화 이질소만 넣었을 때 농도-시간 그래프">[[G2]]</svg>
    </div>
    <div class="col">
      <p class="small">위: $\\ce{NO2}$만 넣었을 때 · 아래: $\\ce{N2O4}$만 넣었을 때 (눈금 없는 정성 그래프)</p>
      <p class="f21 mt12"><b>Q</b> ① $t_1$ 이후 두 물질의 농도는?</p>
      <p class="f21 step cm311-a">→ 각각 <span class="ans">일정</span>하다. 두 농도가 같지는 않다.</p>
      <p class="f21 mt12"><b>Q</b> ② $t_1$ 이후 정반응 속도와 역반응 속도는?</p>
      <p class="f21 step cm311-a">→ <span class="ans">같다</span>.</p>
      <p class="f21 mt12"><b>Q</b> ③ 두 경우의 평형 상태를 비교하면?</p>
      <p class="f21 step cm311-a">→ 어느 쪽에서 출발해도 <span class="ans">화학 평형</span>에 도달한다.</p>
    </div>
  </div>
</section>''', S=SECE, G1=graph(0,cap='$\\ce{NO2}$만 넣었을 때'), G2=graph(0.5,cap='$\\ce{N2O4}$만 넣었을 때')))

# ---------- 19. 특징 ----------
add(T('''<!-- ════════ 19. 특징 ════════ -->
<section class="slide" data-sec="[[S]]" data-title="화학 평형의 특징">
  <h2><span class="no">3</span>화학 평형의 특징</h2>
  <p class="f22">가역 반응에서 <mark>정반응 속도와 역반응 속도가 같아 반응물과 생성물의 농도가 변하지 않고 일정하게 유지되는 상태</mark>를 <b>화학 평형</b>이라고 한다.</p>
  <table class="tight mt12 cm311-feat">
    <tr><th style="width:250px">보는 수준</th><th>화학 평형의 특징</th></tr>
    <tr><td><b>거시적</b><br><span class="small">눈으로 관찰</span></td><td class="l">· 반응물의 농도와 생성물의 농도가 일정하게 유지된다(색 일정).<br>· 겉으로는 변화를 관찰할 수 없어 반응이 정지한 것처럼 보인다.</td></tr>
    <tr><td><b>미시적</b><br><span class="small">입자 수준</span></td><td class="l"><span class="step" data-g="f2">· 정반응 속도와 역반응 속도가 같은 <b>동적 평형</b> 상태이다 — 두 반응은 계속 일어난다.</span></td></tr>
  </table>
  <div class="note mt12 step" data-g="f3"><b>평형 농도</b> 화학 평형 상태에서 반응물과 생성물의 농도. 온도·압력 같은 외부 조건이 일정하면 변하지 않는다. 평형 농도는 <b>일정</b>하지만 반응물과 생성물이 <b>같은</b> 것은 아니다.</div>
</section>''', S=SECE))

# ---------- 20. 확인하기 (101쪽) ----------
add('''<!-- ════════ 20. 확인하기 ════════ -->
<section class="slide" data-sec="01 · 확인하기" data-title="확인하기: 화학 평형" data-tpl="check">
  <h2><span class="tag q">확인하기</span>화학 평형</h2>
  <ol class="cm311-ox">
    <li>가역 반응에서 반응물과 생성물의 농도가 변하지 않고 일정하게 유지되는 상태를 (<span class="blank"><span class="step">화학 평형</span></span>)(이)라고 한다.</li>
    <li>화학 평형 상태에서 정반응 속도와 역반응 속도가 같다. (○, ×) <span class="blank"><span class="step">○</span></span></li>
  </ol>
  <h3 class="mt28">더 생각하기 — 친구의 말이 옳을까?</h3>
  <ol class="cm311-ox" start="3">
    <li>"평형에 도달하면 반응이 멈춰." <span class="blank"><span class="step">× — 두 반응이 같은 속도로 계속 일어난다.</span></span></li>
    <li>"평형에서는 반응물과 생성물의 농도가 같아져." <span class="blank"><span class="step">× — 농도는 일정할 뿐 같지 않다.</span></span></li>
  </ol>
</section>''')

# ---------- 21–24. 모형 활동 (물 옮기기) ----------
old(318,346)
add(T('''<!-- ════════ 21. 모형 활동: 과정 ════════ -->
<section class="slide" data-sec="01 · 모형 활동" data-title="모형 활동: 물 옮기기 (과정)">
  <h2><span class="tag">모형 활동</span>물 옮기기로 동적 평형 모형 만들기</h2>
  <p class="f21"><b>목표</b> 겉보기 변화가 없어도 두 방향의 이동이 계속됨을 확인한다. <span class="small">준비물: 100 mL 눈금실린더 2개, 굵기가 다른 유리관 2개, 물</span></p>
  <div class="cm311-s4 mt8">[[C]]</div>
  <div class="note q mt8"><b>안전</b> 보안경, 끝을 다듬은 유리관 사용. 깨진 유리는 전용 통에, 물은 개수대에 버린다.</div>
</section>''', C=st))
old(375,468)
for i in (-3,-2,-1):
    S[i]=S[i].replace('data-sec="01 · 탐구"','data-sec="01 · 모형 활동"').replace('<span class="tag">탐구</span>','<span class="tag">모형 활동</span>').replace('data-title="탐구:','data-title="모형 활동:')
patch(-3,('물 옮기기 모형 실험실','물 옮기기 모형 실험실'))

# ---------- 25. 소단원 마무리 ----------
add('''<!-- ════════ 25. 소단원 마무리 ════════ -->
<section class="slide" data-sec="01 · 소단원 마무리" data-title="소단원 마무리">
  <h2><span class="tag">소단원 마무리</span>창의력 키우기 · 디지털 소양 키우기</h2>
  <div class="row">
    <div class="col">
      <div class="card"><h3>창의력 키우기</h3>
        <p class="f21" data-q>일상생활에서 가역 반응과 비가역 반응의 예를 찾아보자.</p>
        <p class="f21 mt8 step cm311-a">예) 가역: 토양의 성질에 따라 수국꽃의 색이 변하는 것, 변색 렌즈, 석회 동굴<br>비가역: 녹색 채소를 물에 오래 끓이면 녹황색으로 변하는 것, 종이의 연소, 달걀 삶기</p>
      </div>
    </div>
    <div class="col">
      <div class="card"><h3>디지털 소양 키우기</h3>
        <p class="f21" data-q>화학 반응이 화학 평형에 도달했는지 알 수 있는 방법을 조사한 뒤, 가역 반응 실험 영상을 찾아보고 그 반응이 화학 평형에 도달했는지 판단해 보자.</p>
        <p class="f21 mt8 step cm311-a">예) 평형에 도달하면 반응물과 생성물의 농도가 일정해진다. 색이 변하는 반응은 색도계로 색이 더 이상 변하지 않는지 확인하고, 색이 변하지 않는 반응은 분광 광도계로 농도 변화를 감지해 판단한다.</p>
        <p class="small mt8">영상이나 자료를 쓸 때는 출처를 밝힌다.</p>
      </div>
    </div>
  </div>
</section>''')

# ---------- 26–28. 문항 ----------
add('''<!-- ════════ 26. 중단원 마무리 01 ════════ -->
<section class="slide" data-sec="01 · 중단원 마무리" data-title="중단원 마무리 01">
  <h2><span class="tag q">중단원 마무리 01</span>가역 반응</h2>
  <p class="f22">가역 반응에 대한 설명으로 옳은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?</p>
  <div class="row mt8">
    <div class="col">
      <div class="bogi"><p>ㄱ. 정반응과 역반응이 모두 일어난다.</p><p>ㄴ. 가역 반응은 $\\ce{&lt;=&gt;}$를 사용해 하나의 화학 반응식으로 나타낼 수 있다.</p><p>ㄷ. 메테인의 연소 반응은 가역 반응이다.</p></div>
      <div class="choices"><span>① ㄱ</span><span>② ㄷ</span><span>③ ㄱ, ㄴ</span><span>④ ㄴ, ㄷ</span><span>⑤ ㄱ, ㄴ, ㄷ</span></div>
    </div>
    <div class="col stack" style="flex:0 0 380px"><div class="board" style="min-height:230px"></div></div>
  </div>
  <div class="answer step mt12"><b>정답 ③ ㄱ, ㄴ</b> <span class="small">ㄷ: 메테인의 연소는 한 방향으로만 일어나는 비가역 반응이다.</span></div>
</section>''')
add(T('''<!-- ════════ 27. 중단원 마무리 02 ════════ -->
<section class="slide" data-sec="01 · 중단원 마무리" data-title="중단원 마무리 02">
  <h2><span class="tag q">중단원 마무리 02</span>밀폐 용기 속 $\\ce{NO2}$의 변화</h2>
  <p class="f21">다음은 $\\ce{NO2(g)}$가 반응하여 $\\ce{N2O4(g)}$를 생성하는 반응이다. $\\ce{2NO2(g) &lt;=&gt; N2O4(g)}$ (적갈색 → 무색)<br>일정한 온도에서 밀폐된 용기에 $\\ce{NO2(g)}$를 넣었을 때 일어나는 변화에 대한 설명으로 <b>옳지 않은</b> 것은? (단, 용기의 부피는 일정하다.)</p>
  <div class="row mt8">
    <div class="col">
      <div class="choices cm311-col">
        <span>① 용기 내부의 색이 점점 옅어진다.</span>
        <span>② $\\ce{NO2(g)}$의 농도는 처음보다 감소한다.</span>
        <span>③ 용기 내부의 전체 기체 분자 수가 처음보다 감소한다.</span>
        <span>④ 시간이 지나도 $\\ce{NO2(g)}$가 생성되는 반응은 일어나지 않는다.</span>
        <span>⑤ 시간이 충분히 흐른 후 용기 내부의 색이 일정하게 유지된다.</span>
      </div>
    </div>
    <div class="col stack" style="flex:0 0 360px"><div class="board" style="min-height:200px"></div></div>
  </div>
  <div class="answer step mt8"><b>정답 ④</b> <span class="small">역반응($\\ce{N2O4}$ 분해 → $\\ce{NO2}$ 생성)도 계속 일어나 평형에서는 정반응 속도와 같다. ③: $\\ce{NO2}$ 2개가 $\\ce{N2O4}$ 1개가 되므로 분자 수가 준다.</span></div>
</section>'''))
add('''<!-- ════════ 28. 확인 문제 01 ════════ -->
<section class="slide" data-sec="01 · 확인 문제" data-title="확인 문제 01 (서술형)">
  <h2><span class="tag q">확인 문제 01</span>서술형</h2>
  <div class="row stretch" style="height:250px">
    <div class="col stack">
      <p class="f22">물이 든 병의 뚜껑을 닫아 오래 두었더니 물의 양이 더 이상 변하지 않았다. 이 상태를 <b>동적 평형</b>이라고 하는 까닭을 <b>증발 속도</b>와 <b>응축 속도</b>를 사용하여 서술하시오.</p>
      <div class="board mt8"></div>
    </div>
  </div>
  <div class="answer step cm311-left"><b>예시 답안</b> 물의 양이 일정하여 겉으로는 변화가 없어 보이지만, 물의 증발과 수증기의 응축은 계속 일어나고 있으며 증발 속도와 응축 속도가 같기 때문이다.<br><span class="small">채점 요소: ① 겉보기 변화 없음 ② 증발과 응축이 계속 일어남 ③ 두 속도가 같음</span></div>
</section>''')

# ---------- 29. 함께 풀어 보기 ----------
add('''<!-- ════════ 29. 함께 풀어 보기 ════════ -->
<section class="slide" data-sec="01 가역 반응과 화학 평형 · 마무리" data-title="함께 풀어 보기">
  <h2><span class="tag ink">함께 풀어 보기</span>1. 화학 평형 — 핵심 내용 정리</h2>
  <div class="cm311-map">
    <div class="cm311-node cm311-main"><b>1 가역 반응과 화학 평형</b> <span class="small">(97쪽 · 오늘)</span>
      <p class="f21 mt8" data-q>(1) ① 가역 반응: <span class="blank"><span class="step">정반응</span></span>와/과 <span class="blank"><span class="step">역반응</span></span>이/가 모두 일어날 수 있는 반응</p>
      <p class="f21">② 비가역 반응: 한 방향으로만 일어나는 반응</p>
      <p class="f21" data-q>(2) <span class="blank"><span class="step">화학 평형</span></span>: 가역 반응에서 반응물과 생성물의 농도가 일정하게 유지되어 겉으로는 변화가 일어나지 않는 것처럼 보이는 동적 평형 상태</p>
      <p class="small mt8">덧붙임: 밀폐된 병 속 물과 수증기처럼 두 가지 이상의 상태가 동적 평형을 유지하는 것 = 상평형</p>
    </div>
    <div class="cm311-arr">→</div>
    <div class="cm311-node cm311-dim">2 화학 평형과 평형 상수<br><span class="small">(102쪽)</span></div>
    <div class="cm311-arr">→</div>
    <div class="cm311-node cm311-dim">3 화학 반응의 진행 방향 예측<br><span class="small">(106쪽)</span></div>
  </div>
  <p class="small mt12">교과서 「함께 풀어 보기」의 빈칸 1–3이 이 소단원 몫이다. 핵심 내용으로 간단한 문제를 만들어 친구들과 함께 풀어 보자.</p>
</section>''')

# ---------- 30. 스스로 점검하기 ----------
old(547,561)
