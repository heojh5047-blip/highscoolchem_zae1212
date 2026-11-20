import sys
reps = [
("예시: 이산화 탄소 약 96.5 %, 질소 약 3.5 % → $P_{\\ce{CO2}}\\approx0.965\\times90\\approx87$ 기압, $P_{\\ce{N2}}\\approx3$ 기압. 이산화 탄소의 부분 압력만으로도 지구 대기압의 약 87배이다.",
 "예시: 부피비 이산화 탄소 96.5 %, 질소 3.5 % → 몰분율 0.965, 0.035. 금성 대기압 약 90 기압이므로 $P_{\\ce{CO2}}=90\\times0.965=86.85$ 기압, $P_{\\ce{N2}}=90\\times0.035=3.15$ 기압."),
("<b>예시</b> 부분 압력 법칙 — 각 기체의 부분 압력은 (몰분율 $\\times$ 전체 압력)이다. 깊이",
 "<b>예시</b> 부분 압력 법칙 — 일정한 온도와 부피에서 각 기체의 양(mol)은 부분 압력에 비례하므로, 압력을 보며 기체를 정한 비율로 채운다. 깊이"),
("→ 저녁 숨 쉬는 공기", "→ 저녁 LPG(프로페인 $+$ 뷰테인)로 요리"),
]
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (p, a[:30])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
print("ok")
