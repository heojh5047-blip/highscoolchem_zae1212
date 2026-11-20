import sys
p='slides.tpl.html'; t=open(p,encoding='utf-8').read()
R=[
(r'(예) <span class="ans">2.5 cm</span>', r'(예) <span class="ans">약 4 cm</span>'),
(r'$\dfrac{2.5\ \text{cm}}{10}=$ <span class="ans">$0.25\ \text{cm}$</span>', r'$\dfrac{4\ \text{cm}}{10}=$ <span class="ans">약 $0.4\ \text{cm}$</span>'),
(r'$0.25\ \text{cm}\times6.02\times10^{23}=1.505\times10^{23}\ \text{cm}=$ <span class="ans">$1.505\times10^{18}\ \text{km}$</span>',
 r'$6.02\times10^{23}\times4\times10^{-6}\ \text{km}=$ <span class="ans">$2.408\times10^{18}\ \text{km}$</span>'),
(r'<li>모둠별로 1 몰의 개수를 체험할 수 있는 활동을 만들어 발표해 보자.</li>',
 r'<li>모둠별로 1 몰의 개수를 체험할 수 있는 활동을 만들어 발표해 보자. <span class="step small c-muted">(예) 쌀알 1 몰은 80억 명이 하루 세 끼 밥을 먹어도 약 $3.4\times10^{7}$년 동안 먹을 양</span></li>'),
(r'약 <b>100억 배</b>', r'약 <b>160억 배</b>'),
(r'<b>추가 상식 — 원자량·분자량·화학식량</b> <b>원자량</b>: 탄소-12 원자의 질량을 12로 정하고 이를 기준으로 나타낸 원자의 상대적 질량',
 r'<b>추가 상식 — 원자량·분자량·화학식량 (지난 교육과정의 용어)</b> <b>원자량</b>: 탄소-12 원자의 질량을 12로 정하고 이를 기준으로 나타낸 원자의 상대적 질량'),
(r'— 혼동하지 말자.</div>', r'— 혼동하지 말자. 아보가드로수가 상수로 정해지면서 기준 원소가 없어져, 지금 교과서는 이 용어들 대신 <b>몰질량(g/mol)</b>을 쓴다.</div>'),
(r'(예) 9 m × 8 m × 3 m = <span class="ans">$216\ \text{m}^3=216000\ \text{L}$</span>',
 r'(예) 7.66 m × 10.97 m × 2.29 m ≈ <span class="ans">$1.92\times10^{8}\ \text{cm}^3\approx192429\ \text{L}$</span>'),
(r'$\dfrac{216000\ \text{L}}{22.4\ \text{L/mol}}\approx$ <span class="ans">$9.64\times10^{3}\ \text{mol}$</span>',
 r'$\dfrac{192429\ \text{L}}{22.4\ \text{L/mol}}\approx$ <span class="ans">$8590.6\ \text{mol}$</span>'),
(r'$9.64\times10^{3}\ \text{mol}\times28\ \text{g/mol}\approx$ <span class="ans">$2.7\times10^{5}\ \text{g}$</span> (약 270 kg)',
 r'$8590.6\ \text{mol}\times28\ \text{g/mol}\approx$ <span class="ans">$240536.8\ \text{g}$</span> (약 241 kg)'),
(r'<span class="small c-muted">(0.1 몰로 정했을 때의 예)</span>', r'<span class="small c-muted">(모둠마다 정한 양의 예)</span>'),
(r'<td>63.5</td><td>0.1</td><td><span class="blank"><span class="step" data-g="r2">6.35</span></span></td><td><span class="blank"><span class="step" data-g="r2">$6.02\times10^{22}$',
 r'<td>63.5</td><td>0.05</td><td><span class="blank"><span class="step" data-g="r2">3.2</span></span></td><td><span class="blank"><span class="step" data-g="r2">$3.01\times10^{22}$'),
(r'<td>18</td><td>0.1</td><td><span class="blank"><span class="step" data-g="r3">1.8</span></span></td><td><span class="blank"><span class="step" data-g="r3">$6.02\times10^{22}$',
 r'<td>18</td><td>3</td><td><span class="blank"><span class="step" data-g="r3">54</span></span></td><td><span class="blank"><span class="step" data-g="r3">$1.806\times10^{24}$'),
(r'<td>58.5</td><td>0.1</td><td><span class="blank"><span class="step" data-g="r4">5.85</span></span></td><td><span class="blank"><span class="step" data-g="r4">$6.02\times10^{22}$',
 r'<td>58.5</td><td>0.2</td><td><span class="blank"><span class="step" data-g="r4">11.7</span></span></td><td><span class="blank"><span class="step" data-g="r4">$1.204\times10^{23}$'),
(r'<td>46</td><td>0.1</td><td><span class="blank"><span class="step" data-g="r6">4.6</span></span></td><td><span class="blank"><span class="step" data-g="r6">$6.02\times10^{22}$',
 r'<td>46</td><td>1</td><td><span class="blank"><span class="step" data-g="r6">46</span></span></td><td><span class="blank"><span class="step" data-g="r6">$6.02\times10^{23}$'),
(r'같은 양(mol)이면 입자 수가 같고, 질량은 몰질량에 비례한다.', r'입자 수는 양(mol)에 비례한다 — 탄소와 포도당은 질량이 달라도 0.1 몰이면 입자 수가 $6.02\times10^{22}$개로 같다. 질량 $=$ 양(mol) $\times$ 몰질량.'),
]
for a,b in R:
    n=t.count(a)
    if n!=1: sys.exit(f'count {n}: {a[:60]}')
    t=t.replace(a,b)
open(p,'w',encoding='utf-8').write(t); print('ok')
