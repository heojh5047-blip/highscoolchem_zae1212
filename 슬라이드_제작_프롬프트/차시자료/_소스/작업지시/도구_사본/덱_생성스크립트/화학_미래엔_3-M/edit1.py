import sys
p=sys.argv[1]+'/slides.tpl.html'; s=open(p).read()
R=[]
def r(a,b):
    global s
    assert s.count(a)==1,(a[:60],s.count(a)); s=s.replace(a,b)
# A. 11 procedure (guide)
r('''    <div class="stage"><h3>① 평형 혼합물 만들기</h3><p>황산 구리(II) 수용액에 진한 염산을 스포이트로 조금씩 넣어 파란색과 노란색이 섞인 초록색이 되게 한다.</p></div>
    <div class="stage"><h3>② 나누어 담기</h3><p>같은 양씩 시험관 3개에 나누어 담는다. 하나는 실온에 두어 비교 기준으로 쓴다.</p></div>
    <div class="stage"><h3>③ 온도 바꾸기</h3><p>나머지 두 시험관을 얼음물과 뜨거운 물이 든 비커에 넣고, 몇 분 뒤 색을 비교한다.</p></div>''',
'''    <div class="stage"><h3>① 용액 넣기</h3><p>시험관에 황산 구리(II) 수용액을 5 mL 넣는다.</p></div>
    <div class="stage"><h3>② 염산 넣기</h3><p>진한 염산을 스포이트로 수용액의 색이 변할 때까지(초록색) 넣는다.</p></div>
    <div class="stage"><h3>③ 얼음물</h3><p>시험관을 얼음물이 든 비커에 넣은 후 색 변화를 관찰한다.</p></div>
    <div class="stage"><h3>④ 뜨거운 물</h3><p>시험관을 뜨거운 물이 든 비커에 넣은 후 색 변화를 관찰한다.</p></div>''')
# C. 12
r('''<p class="f22 cm39-tc">$\\ce{Hb(aq) + 4O2(g) &lt;=&gt; Hb(O2)4(aq)}$</p>''',
'''<p class="f22 cm39-tc">$\\ce{O2(g) &lt;=&gt; O2(aq)}$ <span class="small c-muted">(폐 속 산소 ⇌ 혈액에 녹은 산소)</span></p>''')
r('''<b>예시 글</b> 치료실의 압력을 높이고 순수한 산소를 들이마시면 혈액에 녹는 산소의 농도가 커진다. 반응물인 $\\ce{O2}$의 농도가 증가하므로 이를 감소시키는 정반응이 우세하게 진행되어 산소와 결합한 헤모글로빈이 많아지고, 조직에 산소를 더 많이 공급할 수 있다. 일산화 탄소에 중독되었을 때도 높은 농도의 산소가 헤모글로빈에 붙은 일산화 탄소를 밀어내는 쪽으로 평형이 이동한다.</div>
      <p class="small c-muted">채점 요소: 압력 증가 → $\\ce{O2}$ 농도 증가 · 정반응 우세 · 산소 공급 증가</p>''',
'''<b>예시 답안</b> 공기 중의 산소는 폐를 통해 혈액 속으로 녹아 들어가, 산소 기체와 혈액에 녹아 있는 산소가 화학 평형을 이룬다. 산소의 압력이 큰 치료실에서 치료를 받으면 평형이 이동하여 혈액 속으로 산소가 많이 녹아 들어간다. 혈액에 녹은 산소가 많아지면 유독 가스 중독의 치료 효과가 높아지고, 상처 부위의 회복도 빨라진다.</div>
      <p class="small c-muted">평가 기준: 화학 평형 이동과 관련지어 옳게 설명 100 % · 원리는 옳으나 평형 이동과 관련짓지 못함 50 %</p>''')
# D. 13(1)
r('''<div class="answer step">$\\ce{N2O4(g) &lt;=&gt; 2NO2(g)}$</div>''',
'''<div class="answer step">$\\ce{N2O4(g) &lt;=&gt;[\\text{에너지 흡수}][\\text{에너지 방출}] 2NO2(g)}$</div>''')
r('''<p class="small c-muted step">무색 ⇌ 적갈색 · 원자 수 N 2 = 2, O 4 = 4</p>''',
'''<p class="small c-muted step">가역 반응 · 무색 ⇌ 적갈색 · 정반응은 흡열 · 원자 수 N 2 = 2, O 4 = 4</p>''')
# E. 13(2)
r('''따라서 새 평형에서 $[\\ce{NO2}]$는 커지고 $[\\ce{N2O4}]$는 작아져 $K$가 커진다.</div>''',
'''따라서 새 평형에서 $[\\ce{NO2}]$는 커지고 $[\\ce{N2O4}]$는 작아져 $K$가 커진다.</div>
      <p class="small c-muted">평가 기준: 흡열 판단 + 근거를 든 $K$ 변화 100 % · 근거 없이 $K$ 변화만 70 % · 흡열·발열 판단만 30 %</p>''')
# F. project 1
r('''<td class="l">약 50–100 기압 — 튼튼한 설비·압축 비용</td>''','''<td class="l">100 기압 이상을 견디는 설비가 필요</td>''')
r('''<td class="l">너무 낮으면 반응이 느림 → 약 200–300 °C + 촉매</td>''','''<td class="l">너무 낮으면 반응이 느려 비효율적 → 알맞은 온도를 찾거나 촉매로 반응 속도를 높임</td>''')
# G. project 2
r('''<p class="step" data-g="x1"><b>덧붙일 점</b> 고압 반응기·압축기, 열교환기로 반응열을 빼내 온도를 일정하게, 누출 감지 장치</p>''',
'''<p class="step" data-g="x1"><b>예시 답안</b> 수득률을 높이려면 기체를 고압에서 반응시켜야 하므로 100 기압 이상을 견디면서 온도 조절까지 되는 설비를 마련한다.</p>''')
r('''<p class="step" data-g="x1"><b>덧붙일 점</b> 높은 압력·적당히 낮은 온도·촉매, 생성물을 냉각해 분리, 남은 기체 재순환</p>''',
'''<p class="step" data-g="x1"><b>예시 답안</b> 수득률을 높이려면 압력은 높이고 온도는 낮춰야 하지만, 반응 속도를 생각해 알맞은 촉매 물질을 찾아야 한다.</p>''')
r('''<p class="step" data-g="x1"><b>덧붙일 점</b> 반응열을 회수해 공장 난방·발전에 다시 쓰기, 냉각수 온도 기준 지키기</p>''',
'''<p class="step" data-g="x1"><b>예시 답안</b> 반응열을 식히는 냉각수로 바닷물을 쓸 때 인근 바다의 수온이 너무 높아지지 않게 하고, 발생하는 열을 인근 지역 난방에 쓰는 방법을 찾는다.</p>''')
r('''반응열을 버리지 않고 회수해 쓰면 온도 조절과 바다 수온 문제를 함께 줄일 수 있다.''','''반응열을 인근 지역 난방 등에 회수해 쓰면 설비 온도 조절과 바다 수온 문제를 함께 줄일 수 있다.''')
# H. project 3 table
a=s.index('<table class="tight cm39-plan cm39-big mt8">'); b=s.index('</table>',a)+8
s=s[:a]+'''<table class="tight cm39-plan cm39-big mt8">
    <tr><th>구분</th><th>내용 (예시 답안)</th><th>담당 부서</th></tr>
    <tr><td>공장 부지 선정 분야</td><td class="l"><span class="step" data-g="p1">냉각수나 가용 재생 에너지를 공급받기 적합한 위치인가?</span></td><td><span class="step" data-g="p1">관리 1팀</span></td></tr>
    <tr><td>설비 제작 설치 분야</td><td class="l"><span class="step" data-g="p2">높은 압력을 견딜 수 있는 설비 제작이 가능한 업체를 선정했는가?</span></td><td><span class="step" data-g="p2">관리 2팀</span></td></tr>
    <tr><td>관련 물질 공급 분야</td><td class="l"><span class="step" data-g="p3">반응 속도를 향상시킬 수 있는 촉매 물질 개발이 기한 내 가능한가?</span></td><td><span class="step" data-g="p3">연구 1팀</span></td></tr>
    <tr><td>환경 인증 및 관련 법령 분야</td><td class="l"><span class="step" data-g="p4">주변 지역 주민과의 합의와 시설에 대한 혐오를 줄이고 시설을 활용한 지역 친화적인 사업을 계획하고 있는가?</span></td><td><span class="step" data-g="p4">환경 1팀</span></td></tr>
  </table>'''+s[b:]
open(p,'w').write(s)
f=sys.argv[1]+'/figs.py'; t=open(f).read()
t=t.replace("(240,'#5FA86B','실온',None,None)","(240,'#5FA86B','처음(실온)',None,None)")
t=t.replace("'초록색 평형 혼합물을 세 시험관에 나누어 얼음물에서는 파란색, 실온은 초록색, 뜨거운 물에서는 노란색이 진해진다'","'초록색 평형 혼합물(처음, 실온)을 얼음물에 넣으면 파란색이, 뜨거운 물에 넣으면 노란색이 진해진다'")
open(f,'w').write(t); print('done')
