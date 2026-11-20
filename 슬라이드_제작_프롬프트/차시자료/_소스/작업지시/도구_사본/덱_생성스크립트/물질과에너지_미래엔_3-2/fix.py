import sys
D='/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/물질과에너지_미래엔/3-2_반응_경로와_반응_엔탈피/'
def rep(fn,pairs):
    s=open(D+fn,encoding='utf-8').read()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: sys.exit(f'{fn}: {n}x {a[:60]}')
        s=s.replace(a,b)
    open(D+fn,'w',encoding='utf-8').write(s)
rep('slides.html',[
('간이 열량계(스타이로폼 컵·뚜껑), 온도계, 젓개, 전자저울, 눈금실린더, 약숟가락, 시약포지, 고체 수산화 나트륨($\\ce{NaOH(s)}$), $1.0\\ \\text{M}$ 염산($\\ce{HCl(aq)}$), 증류수',
 '수산화 나트륨($\\ce{NaOH(s)}$), $1.0\\ \\text{M}$ 염산($\\ce{HCl(aq)}$), 증류수, 간이 열량계, 비커, 전자저울, 온도계, 시약포지, 약숟가락, 젓개, 실험복, 보안경, 실험용 장갑'),
('<p class="f21">고체 수산화 나트륨이 물에 녹은 후 염산과 반응하는 [경로 1]</p>',
 '<p class="f21">고체 수산화 나트륨이 물에 녹아 수산화 나트륨 수용액이 되고, 이 수용액이 염산과 반응하는 [경로 1]</p>'),
('<td>22.0</td><td>32.1</td><td>22.0</td><td>28.5</td><td>22.0</td><td>33.6</td>',
 '<td>20.8</td><td>30.3</td><td>21.1</td><td>27.6</td><td>21.0</td><td>32.4</td>'),
('data-g="r1">10.1</span>','data-g="r1">9.5</span>'),
('data-g="r1">11.6</span>','data-g="r1">11.4</span>'),
('data-g="r2">4.41</span>','data-g="r2">4.150</span>'),
('data-g="r2">5.57</span>','data-g="r2">5.569</span>'),
('data-g="r2">9.94</span>','data-g="r2">9.768</span>'),
('data-g="r3">−44.1</span>','data-g="r3">−41.50</span>'),
('data-g="r3">−55.7</span>','data-g="r3">−55.69</span>'),
('data-g="r3">−99.4</span>','data-g="r3">−97.68</span>'),
('온도는 <b>예시 값</b>(실험실의 기본 조건과 같은 값)이다.',
 '온도는 지도서의 <b>예시 값</b>이다. 실험실 기본 조건(스타이로폼, $\\ce{NaOH}$ 4.0 g)으로 측정하면 같은 온도 변화가 나온다.'),
('$Q=4.2\\times104\\times10.1=4.41\\times10^{3}\\ \\text{J}$<br>$\\Delta H_1=-\\dfrac{4.41\\ \\text{kJ}}{0.10\\ \\text{mol}}=-44.1\\ \\text{kJ/mol}$',
 '$Q=4.2\\times104\\times9.5=4149.6\\ \\text{J}$<br>$\\Delta H_1=-\\dfrac{4.150\\ \\text{kJ}}{0.10\\ \\text{mol}}=-41.50\\ \\text{kJ/mol}$'),
('$Q=4.2\\times204\\times6.5=5.57\\times10^{3}\\ \\text{J}$<br>$\\Delta H_2=-\\dfrac{5.57\\ \\text{kJ}}{0.10\\ \\text{mol}}=-55.7\\ \\text{kJ/mol}$',
 '$Q=4.2\\times204\\times6.5=5569.2\\ \\text{J}$<br>$\\Delta H_2=-\\dfrac{5.569\\ \\text{kJ}}{0.10\\ \\text{mol}}=-55.69\\ \\text{kJ/mol}$'),
('$Q=4.2\\times204\\times11.6=9.94\\times10^{3}\\ \\text{J}$<br>$\\Delta H_3=-\\dfrac{9.94\\ \\text{kJ}}{0.10\\ \\text{mol}}=-99.4\\ \\text{kJ/mol}$',
 '$Q=4.2\\times204\\times11.4=9767.5\\ \\text{J}$<br>$\\Delta H_3=-\\dfrac{9.768\\ \\text{kJ}}{0.10\\ \\text{mol}}=-97.68\\ \\text{kJ/mol}$'),
('\\Delta H_1=-44.1\\ \\text{kJ}$</span>','\\Delta H_1=-41.50\\ \\text{kJ}$</span>'),
('\\Delta H_2=-55.7\\ \\text{kJ}$</span>','\\Delta H_2=-55.69\\ \\text{kJ}$</span>'),
('\\Delta H_3=-99.4\\ \\text{kJ}$</span>','\\Delta H_3=-97.68\\ \\text{kJ}$</span>'),
('경로 1은 44.1과 55.7을 이어 붙인 막대, 경로 2는 99.4 막대로','경로 1은 41.50과 55.69를 이어 붙인 막대, 경로 2는 97.68 막대로'),
('<rect x="100" y="22" width="353" height="40" fill="#8DB8EC"/><rect x="453" y="22" width="446" height="40" fill="#1F6FD1"/>',
 '<rect x="100" y="22" width="332" height="40" fill="#8DB8EC"/><rect x="432" y="22" width="446" height="40" fill="#1F6FD1"/>'),
('<rect x="100" y="92" width="795" height="40" fill="#C2410C"/>','<rect x="100" y="92" width="781" height="40" fill="#C2410C"/>'),
('x="276" y="50" data-tex="\\Delta H_1=-44.1"','x="266" y="50" data-tex="\\Delta H_1=-41.50"'),
('x="676" y="50" data-tex="\\Delta H_2=-55.7"','x="655" y="50" data-tex="\\Delta H_2=-55.69"'),
('x="498" y="120" data-tex="\\Delta H_3=-99.4"','x="490" y="120" data-tex="\\Delta H_3=-97.68"'),
('x="908" y="50" data-tex="-99.8"','x="887" y="50" data-tex="-97.19"'),
('$\\Delta H_1+\\Delta H_2=(-44.1)+(-55.7)=-99.8\\ \\text{kJ}$ ≈ $\\Delta H_3=-99.4\\ \\text{kJ}$ (차이 약 0.4 %)',
 '$\\Delta H_1+\\Delta H_2=(-41.50)+(-55.69)=-97.19\\ \\text{kJ}$ ≈ $\\Delta H_3=-97.68\\ \\text{kJ}$ (실험 오차를 고려하면 대체로 같다)'),
('예: 1층에서 5층까지 계단으로 가든 엘리베이터로 가든 높이 차는 같다 · 용돈을 두 번에 나누어 저금해도 한 번에 저금해도 늘어난 금액은 같다',
 '예: 두 도시 사이를 다른 길로 여행해도 두 도시의 위치는 같다 · 직소 퍼즐을 다른 순서로 맞춰도 완성된 그림은 같다 · 계단과 엘리베이터 중 어느 쪽으로 올라도 높이 차는 같다'),
('예: 연탄·숯불에서 생기는 일산화 탄소 — 흑연과 일산화 탄소의 완전 연소 반응식으로 $\\ce{C(s) + 1/2O2(g) -> CO(g)}$의 $\\Delta H=-110.5\\ \\text{kJ}$를 구하고, 쓴 반응식의 출처와 계산 과정을 함께 올린다.',
 '예: 냉장고 속 얼음의 승화 — 융해 엔탈피 6.01 kJ/mol과 증발 엔탈피 40.67 kJ/mol을 더해 승화 엔탈피 46.68 kJ/mol을 구하고, 쓴 값의 출처와 계산 과정을 함께 올린다.'),
])
rep('labs.js',[
("   참값(교과서 76쪽): 용해 −44.5, 중화 −55.8, 직접 −100.3 kJ/mol. 용액 질량: 용해 100 + w, 중화·직접 200 + w (g).\n   열량계 효율(덱 설정): 스타이로폼 0.995, 유리 비커 0.80.",
 "   기준값(지도서 79쪽 결과 예시, 간이 열량계): 용해 −41.50, 중화 −55.69, 직접 −97.68 kJ/mol(교과서 76쪽 −44.5, −55.8, −100.3보다 조금 작다).\n   용액 질량: 용해 100 + w, 중화·직접 200 + w (g). 열량계 효율(덱 설정): 스타이로폼 1(지도서 예시와 같음), 유리 비커 0.80."),
("H:44.5,","H:41.50,"),("H:55.8,","H:55.69,"),("H:100.3,","H:97.68,"),
("foam:{name:'스타이로폼',eff:0.995,","foam:{name:'스타이로폼',eff:1,"),
])
print('ok')
