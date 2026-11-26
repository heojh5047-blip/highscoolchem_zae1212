import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
R = [
# S6
("""  <p class="small mt12">이산화 탄소($\\ce{CO2}$), 탄산수소 나트륨($\\ce{NaHCO3}$)처럼 탄소를 포함해도 보통 탄소 화합물로 다루지 않는 물질도 있다.</p>""",
 """  <p class="small mt12">이산화 탄소($\\ce{CO2}$), 탄산염($\\ce{NaHCO3}$, $\\ce{CaCO3}$)처럼 탄소를 포함한 간단한 물질은 무기 화합물로 따로 다루기도 한다.</p>"""),
# S7
("""    <tr><th>탄소 화합물이 들어 있음</th><td class="l">구강 청결제(에탄올), 네일 리무버(아세톤), 소독용 알코올(에탄올), 식초(아세트산), 설탕, 비누, 아스피린, 치약(글리세롤 등), 빵(녹말)</td></tr>
    <tr><th>들어 있지 않음</th><td class="l">물 $\\ce{H2O}$, 소금 $\\ce{NaCl}$, 제빵 소다 $\\ce{NaHCO3}$ (탄소가 있지만 탄소 화합물로 다루지 않음)</td></tr>""",
 """    <tr><th>탄소 화합물이 들어 있음</th><td class="l">구강 청결제(살리실산 메틸), 네일 리무버(아세톤 $\\ce{C3H6O}$), 소독용 알코올(에탄올 $\\ce{C2H6O}$), 식초(아세트산 $\\ce{C2H4O2}$), 제빵 소다(탄산수소 나트륨 $\\ce{NaHCO3}$), 비누(스테아르산 나트륨), 아스피린, 치약(탄산 칼슘 $\\ce{CaCO3}$), 빵(녹말), 설탕 $\\ce{C12H22O11}$</td></tr>
    <tr><th>들어 있지 않음</th><td class="l">물 $\\ce{H2O}$, 소금 $\\ce{NaCl}$</td></tr>"""),
("""  <div class="answer step"><span class="small">예시</span> 휘발유, 샴푸, 비닐봉지, 페트병, 화장품</div>""",
 """  <div class="answer step"><span class="small">예시</span> 플라스틱 컵(폴리프로필렌), 책(셀룰로오스, 염료), 운동화(나일론)</div>"""),
# S22
("""<td><span class="blank"><span class="step" data-g="r1">끓는점이 높다</span></span></td></tr>""",
 """<td><span class="blank"><span class="step" data-g="r1">극성 분자 (메탄올 독성, 에탄올 살균)</span></span></td></tr>"""),
("""<td><span class="blank"><span class="step" data-g="r2">기체·휘발성</span></span></td>""",
 """<td><span class="blank"><span class="step" data-g="r2">기체·액체, 쉽게 증발</span></span></td>"""),
("""<td><span class="blank"><span class="step" data-g="r2">다른 물질을 환원</span></span></td></tr>""",
 """<td><span class="blank"><span class="step" data-g="r2">자극적 냄새, 환원성이 강함</span></span></td></tr>"""),
("""<td><span class="blank"><span class="step" data-g="r3">잘 섞임</span></span></td>""",
 """<td><span class="blank"><span class="step" data-g="r3">잘 녹음</span></span></td>"""),
("""<td><span class="blank"><span class="step" data-g="r3">$\\ce{CO2}$ 발생(탄산수소 나트륨)</span></span></td></tr>""",
 """<td><span class="blank"><span class="step" data-g="r3">폼산은 환원성도 · $\\ce{NaHCO3}$와 $\\ce{CO2}$</span></span></td></tr>"""),
("""아세트알데하이드는 $25\\ {}^\\circ\\text{C}$에서 기체지만 끓는점이 실온에 가까워 쉽게 액화한다.</p>""",
 """폼알데하이드는 실온에서 기체, 아세트알데하이드는 끓는점이 약 $20\\ {}^\\circ\\text{C}$라 액체로 보관하지만 쉽게 증발한다(실험실은 $25\\ {}^\\circ\\text{C}$ 기준이라 기체로 표시).</p>"""),
# S23
("""      <p class="f21 step rm31-a">→ <span class="ans">작용기</span>이다. 작용기가 같으면 탄소 수가 달라도 성질이 비슷하고, 작용기가 다르면 성질이 달라진다.</p>""",
 """      <p class="f21 step rm31-a">→ 작용기가 같은 탄소 화합물은 공통적인 성질을 나타낸다. 즉, 성질을 결정하는 것은 <span class="ans">작용기</span>이다.</p>"""),
("""      <p class="f21 step rm31-a">→ <span class="ans">프로판알 $\\ce{C2H5CHO}$</span>. 두 물질 모두 물에 녹지만, 프로판알은 다른 물질을 환원시키는 성질이 있고 아세톤($\\ce{CH3COCH3}$)은 없다. 끓는점은 프로판알 $49\\ {}^\\circ\\text{C}$, 아세톤 $56\\ {}^\\circ\\text{C}$이다.</p>""",
 """      <p class="f21 step rm31-a">→ <span class="ans">프로판알 $\\ce{C2H5CHO}$</span>(프로피온알데하이드, $\\ce{CH3CH2CHO}$): 자극적인 과일 향이 나는 무색 액체, 소독제·세제에 쓰고 다른 물질을 환원시킨다. 아세톤($\\ce{CH3COCH3}$): 특유의 냄새가 나는 액체, 탄소 화합물을 잘 녹여 용매·네일 리무버로 쓴다. → 분자식이 같아도 작용기가 다르면 성질이 다르다.</p>"""),
# S28
("""  <div class="answer step"><span class="small">예시</span> 향수, 섬유 유연제, 과일 향 음료·사탕, 향초</div>""",
 """  <div class="answer step"><span class="small">예시</span> 향수, 식품 첨가물, 모기 퇴치제 — 탄소 수 8인 옥탄알데하이드는 오렌지 향, 9인 노난알데하이드는 장미 향</div>"""),
# S29
("""  <div class="answer step" data-g="fa">산성(카복실기)과 다른 물질을 환원시키는 성질(포밀기)을 함께 나타낸다.</div>""",
 """  <div class="answer step" data-g="fa">알데하이드와 카복실산의 성질을 모두 나타낸다 — 산성(카복실기)과 다른 물질을 환원시키는 성질(포밀기).</div>"""),
# S35
("""aria-label="(가) 메테인, (나) 에테인, (다) 아세트산 공-막대 모형">""",
 """aria-label="(가) 메테인, (나) 에탄올, (다) 아세트산 공-막대 모형">"""),
("""  <div class="answer step"><b>정답 ① ㄱ</b> <span class="small">(나)는 탄화수소인 에테인 — 물에 거의 녹지 않는다. (다)는 아세트산</span></div>""",
 """  <div class="answer step"><b>정답 ⑤ ㄱ, ㄴ, ㄷ</b> <span class="small">(가) 메테인 — LNG의 주성분, (나) 에탄올 — 물에 잘 녹는다, (다) 아세트산 — 물에 잘 녹는다</span></div>"""),
# S36
("""(가)와 (라)는 작용기 $\\ce{-OH}$를 가진 알코올, (나)와 (다)는 작용기 $\\ce{-COOH}$를 가진 카복실산이다. 작용기가 같으면 탄소 수가 달라도 성질이 비슷하기 때문이다.</div>""",
 """메탄올(가)과 프로판올(라)은 작용기 $\\ce{-OH}$를 가진 알코올이므로 성질이 비슷하고, 아세트산(나)과 폼산(다)은 작용기 $\\ce{-COOH}$를 가진 카복실산이므로 성질이 비슷하기 때문이다.</div>"""),
# S37
("""<p class="small mt8 step">예시: 포도당은 $\\ce{-OH}$가 많아 물에 잘 녹아 혈액으로 운반된다.""",
 """<p class="small mt8 step">예시: 탄수화물을 먹으면 $\\ce{-OH}$를 여러 개 갖는 포도당으로 분해되고, 포도당은 물에 잘 녹아 혈액에 녹아 몸에 흡수되어 쓰인다."""),
]
for a, b in R:
    n = s.count(a)
    if n != 1:
        sys.exit(f'MISS({n}): {a[:80]}')
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('ok', len(R))
