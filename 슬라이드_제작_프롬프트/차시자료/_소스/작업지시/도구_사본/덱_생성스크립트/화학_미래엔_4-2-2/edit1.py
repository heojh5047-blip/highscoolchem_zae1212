import sys
p='tpl.html'; s=open(p,encoding='utf-8').read()
R=[
('식초(약 1 M) 20 mL를 그대로 적정하면 0.1 M $\\ce{NaOH}$가 약 200 mL 필요해','식초(약 1 M) 10 mL를 그대로 적정하면 0.1 M $\\ce{NaOH}$가 약 110 mL 필요해'),
('묽힌 식초 20.0 mL를 피펫으로 삼각 플라스크에 옮기고','묽힌 식초 10.0 mL를 피펫으로 삼각 플라스크에 옮기고'),
('<button class="btn" data-s="10">10.0 mL</button><button class="btn on" data-s="20">20.0 mL</button>','<button class="btn on" data-s="10">10.0 mL</button><button class="btn" data-s="20">20.0 mL</button>'),
('<tr><td>1</td><td>0.50</td><td>20.55</td><td><span class="blank"><span class="step" data-g="r1">20.05</span></span></td></tr>\n    <tr><td>2</td><td>0.20</td><td>20.10</td><td><span class="blank"><span class="step" data-g="r1">19.90</span></span></td></tr>\n    <tr><td>3</td><td>1.00</td><td>21.05</td><td><span class="blank"><span class="step" data-g="r1">20.05</span></span></td></tr>',
 '<tr><td>1</td><td>1.18</td><td>12.09</td><td><span class="blank"><span class="step" data-g="r1">10.91</span></span></td></tr>\n    <tr><td>2</td><td>12.09</td><td>23.38</td><td><span class="blank"><span class="step" data-g="r1">11.29</span></span></td></tr>\n    <tr><td>3</td><td>23.38</td><td>34.48</td><td><span class="blank"><span class="step" data-g="r1">11.10</span></span></td></tr>'),
('$\\dfrac{20.05+19.90+20.05}{3}=20.00\\ \\text{mL}$','$\\dfrac{10.91+11.29+11.10}{3}=11.10\\ \\text{mL}$'),
('$V=20.0\\ \\text{mL}$ / $\\ce{NaOH}$ $n\'=1$, $M\'=0.1\\ \\text{M}$, $V\'=20.00\\ \\text{mL}$','$V=10.0\\ \\text{mL}$ / $\\ce{NaOH}$ $n\'=1$, $M\'=0.1\\ \\text{M}$, $V\'=11.10\\ \\text{mL}$'),
('$1\\times M\\times20.0=1\\times0.1\\times20.00$','$1\\times M\\times10.0=1\\times0.1\\times11.10$'),
('<div class="answer step">$M=0.100\\ \\text{M}$</div>','<div class="answer step">$M=0.111\\ \\text{M}$</div>'),
('$0.100\\ \\text{M}\\times10=1.00\\ \\text{M}$','$0.111\\ \\text{M}\\times10=1.11\\ \\text{M}$'),
('식초 1 L(= 1000 g) 속 아세트산: $1.00\\ \\text{mol}$','식초 1 L(= 1000 g) 속 아세트산: $1.11\\ \\text{mol}$'),
('$1.00\\ \\text{mol}\\times60\\ \\text{g/mol}=60\\ \\text{g}$','$1.11\\ \\text{mol}\\times60\\ \\text{g/mol}=66.6\\ \\text{g}$'),
('$\\dfrac{60\\ \\text{g}}{1000\\ \\text{g}}\\times100=6.0\\ \\%$','$\\dfrac{66.6\\ \\text{g}}{1000\\ \\text{g}}\\times100=6.66\\ \\%$'),
('예시 실험값 6.0 %는 표시값 범위 안이다.','예시 실험값 6.66 %는 표시값 범위 안이다.'),
('그래서 식초 적정에는 염기성에서 색이 변하는 페놀프탈레인을 쓴다. (까닭은 「화학 반응의 세계」에서)','식초 적정에서는 페놀프탈레인 용액 전체가 붉은색으로 변하는 순간을 중화점으로 본다. (중화점 액성이 다른 까닭은 다루지 않는다)'),
]
for a,b in R:
    n=s.count(a)
    if n!=1: sys.exit(f'count {n}: {a[:60]}')
    s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s); print('ok')
