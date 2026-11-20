import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

F = {}
# ── 표지: 다니엘 전지 + 전압계
F['COVER'] = cell('Zn', 'Cu', r'\ce{Zn}', r'\ce{Cu}', r'\ce{ZnSO4(aq)}', r'\ce{CuSO4(aq)}', 'w', 'cu', poles=True) + \
    '<rect x="234" y="0" width="92" height="0" fill="none"/>'

# ── 12홈판 (해 보기 금속의 반응성)
def wells(res=False):
    o = []
    cols = [(260, 'Mg', '마그네슘'), (350, 'Zn', '아연'), (440, 'Cu', '구리')]
    rows = [(84, r'\ce{CuSO4(aq)}', 'cu', 'A'), (172, r'\ce{ZnSO4(aq)}', 'w', 'B'), (260, r'\ce{MgSO4(aq)}', 'w', 'C')]
    o.append('<rect x="210" y="38" width="280" height="266" rx="16" fill="#F4F6F8" stroke="#9AA5B1" stroke-width="2"/>')
    for x, m, nm in cols:
        o.append(T(x, 26, mix=nm, size=18))
    for y, tex, sk, ab in rows:
        o.append(T(10, y + 6, mix=ab, size=20, weight=700, anchor='start'))
        o.append(T(36, y + 6, tex=tex, size=19, anchor='start'))
        for x, m, nm in cols:
            c, op = SOL[sk]
            o.append(f'<circle cx="{x}" cy="{y}" r="36" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2"/>')
            o.append(f'<circle cx="{x}" cy="{y}" r="33" fill="{c}" fill-opacity="{op}"/>')
            f, s = MET[m]
            o.append(f'<rect x="{x-14}" y="{y-14}" width="28" height="28" rx="3" fill="{f}" stroke="{s}" stroke-width="2"/>')
    if res:
        dep = {('A', 260): '#8A4B22', ('A', 350): '#8A4B22', ('B', 260): '#4A4F57'}
        for (ab, x), col in dep.items():
            y = {'A': 84, 'B': 172}[ab]
            o.append(f'<g class="step" data-g="w1"><g data-anim="fade" data-dur="1.4" data-on="step">')
            for dx, dy in [(-8, -6), (6, -9), (-4, 6), (8, 5), (0, -1), (-10, 9), (10, -2)]:
                o.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="3.6" fill="{col}"/>')
            o.append('</g></g>')
    return ''.join(o)
F['WELLS0'] = wells(False)
F['WELLS1'] = wells(True)

# ── 이온화 경향 계열
def series():
    el = [('K', '칼륨'), ('Ca', '칼슘'), ('Na', '나트륨'), ('Mg', '마그||네슘'), ('Al', '알루||미늄'), ('Zn', '아연'), ('Fe', '철'), ('Ni', '니켈'),
          ('Sn', '주석'), ('Pb', '납'), ('H', '수소'), ('Cu', '구리'), ('Hg', '수은'), ('Ag', '은'), ('Pt', '백금'), ('Au', '금')]
    o = ['<g data-arw="1080,40,40,40,ox,6"></g>', T(560, 26, mix='이온화 경향이 크다 · 전자를 잃고 산화되기 쉽다', size=20, weight=700, fill='#C2410C', halo=True)]
    for i, (s, nm) in enumerate(el):
        x = 50 + i * 68
        if s == 'H':
            o.append(f'<circle cx="{x}" cy="96" r="27" fill="#FFFFFF" stroke="#5B6B7F" stroke-width="2" stroke-dasharray="5 4"/>')
        else:
            o.append(f'<circle cx="{x}" cy="96" r="27" fill="#EEF1F4" stroke="#7E8B98" stroke-width="2"/>')
        o.append(T(x, 104, tex=r'\ce{' + s + '}', size=22))
        o.append(T(x, 148, mix=nm, size=18))
    return ''.join(o)
F['SERIES'] = series()

# ── 볼타 장치(실험 1·2)
def volta(wire, bub):
    o = [beaker(40, 260, 70, 270), '<rect x="42" y="110" width="216" height="158" fill="#DDEEF8"/>']
    if wire:
        o.append('<path d="M103 40 V14 H197 V40" fill="none" stroke="#16233D" stroke-width="3"/>')
        o.append('<circle cx="103" cy="40" r="4" fill="#16233D"/><circle cx="197" cy="40" r="4" fill="#16233D"/>')
    o.append(plate(103, 'Zn', 40, 200, 26)); o.append(plate(197, 'Cu', 40, 200, 26))
    xs = 120 if bub == 'zn' else 180
    sgn = 1 if bub == 'zn' else -1
    o.append(f'<g class="step" data-g="{"v1" if bub=="zn" else "v2"}"><g data-anim="move" data-from="0,40" data-dur="1.6" data-rep="loop" data-on="step">')
    for dy, r in [(150, 6), (182, 5), (214, 7), (240, 5)]:
        o.append(f'<circle cx="{xs + sgn*(r-2)}" cy="{dy}" r="{r}" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/>')
    o.append('</g></g>')
    o.append(T(84, 100, mix='아연판', size=18, anchor='end')); o.append(T(216, 100, mix='구리판', size=18, anchor='start'))
    o.append(T(150, 262, mix='묽은 황산', size=18, fill='#5B6B7F'))
    return ''.join(o)
F['VOLTA1'] = volta(False, 'zn')
F['VOLTA2'] = volta(True, 'cu')

# ── 볼타 전지 확대 (S11)
def voltabig():
    o = ["<g data-circuit='{\"parts\":[[\"wire\",[[190,96],[190,50],[262,50]]],[\"wire\",[[298,50],[370,50],[370,96]]],[\"bulb\",[280,50],{\"r\":18,\"on\":true}]],\"stroke\":3}'></g>",
         beaker(110, 450, 120, 300), '<rect x="112" y="160" width="336" height="138" fill="#DDEEF8"/>',
         plate(190, 'Zn', 96, 180, 28), plate(370, 'Cu', 96, 180, 28),
         '<path d="M190 96 V50 H262 M298 50 H370 V96" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>',
         '<g data-arw="200,30,252,30,minus,3"></g><g data-arw="308,30,360,30,minus,3"></g>',
         T(226, 22, tex='e^-', size=20, fill='#1F6FD1'), T(334, 22, tex='e^-', size=20, fill='#1F6FD1'),
         '<g data-anim="move" data-from="-30,0" data-dur="1.4" data-delay=".4" data-ease="out"><g data-chg="236,214,11,+"></g>' + T(236, 246, tex=r'\ce{Zn^2+}', size=18, fill='#C2410C') + '</g>',
         '<g data-chg="300,186,10,+"></g>', T(300, 170, tex=r'\ce{H+}', size=18),
         '<g data-chg="318,238,10,+"></g>', T(296, 266, tex=r'\ce{H+}', size=18),
         '<g data-anim="move" data-from="0,40" data-dur="1.6" data-rep="loop"><circle cx="350" cy="186" r="6" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/><circle cx="346" cy="214" r="5" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/><circle cx="351" cy="242" r="7" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/></g>',
         T(344, 148, tex=r'\ce{H2}', size=18, anchor='end', fill='#0E7490'),
         T(182, 116, mix='아연판', size=19, anchor='end'), T(378, 116, mix='구리판', size=19, anchor='start'),
         T(170, 290, mix='묽은 황산', size=18, fill='#5B6B7F'),
         T(190, 328, mix='(−)극', size=20, weight=700), T(190, 354, mix='산화 전극', size=19, weight=700, fill='#C2410C'),
         T(370, 328, mix='(+)극', size=20, weight=700), T(370, 354, mix='환원 전극', size=19, weight=700, fill='#0E7490')]
    return ''.join(o)
F['VOLTABIG'] = voltabig()

# ── 분극: 구리판 표면을 덮은 수소 기체
def polar():
    o = [beaker(40, 300, 70, 280), '<rect x="42" y="110" width="256" height="168" fill="#DDEEF8"/>',
         plate(110, 'Zn', 40, 200, 26), plate(230, 'Cu', 40, 200, 26)]
    o.append('<g data-anim="fade" data-dur="1.6">')
    for i, y in enumerate(range(120, 236, 14)):
        o.append(f'<circle cx="{213 - (i % 2) * 4}" cy="{y}" r="7" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/>')
    o.append('</g>')
    o.append('<g data-chg="170,170,10,+"></g><g data-chg="160,214,10,+"></g>')
    o.append('<g data-arw="178,170,198,170,plus,2.5"></g>')
    o.append('<line x1="186" y1="158" x2="200" y2="182" stroke="#D7263D" stroke-width="3"/><line x1="200" y1="158" x2="186" y2="182" stroke="#D7263D" stroke-width="3"/>')
    o.append(T(160, 252, tex=r'\ce{H+}', size=18))
    o.append(T(250, 128, mix='수소 기체가||구리판을 덮음', size=18, anchor='start', fill='#0E7490', halo=True))
    o.append(T(92, 100, mix='아연판', size=18, anchor='end')); o.append(T(170, 30, mix='구리판 표면 확대', size=18, fill='#5B6B7F'))
    return ''.join(o)
F['POLAR'] = polar()

# ── 다니엘 전지 (전구) + 이온 (S13)
dan_ions = ('<g data-anim="move" data-from="-26,0" data-dur="1.4" data-delay=".4" data-ease="out"><g data-chg="156,206,10,+"></g>' + T(156, 236, tex=r'\ce{Zn^2+}', size=18, fill='#C2410C') + '</g>'
            '<g data-anim="move" data-from="40,0" data-dur="1.4" data-delay=".4" data-ease="in"><g data-chg="470,214,10,+"></g>' + T(470, 244, tex=r'\ce{Cu^2+}', size=18, fill='#0E7490') + '</g>'
            '<g data-chg="84,200,10,-"></g>' + T(84, 186, tex=r'\ce{SO4^2-}', size=18) +
            '<g data-chg="470,176,10,-"></g>' + T(470, 166, tex=r'\ce{SO4^2-}', size=18, halo=True))
F['DANIELL'] = cell('Zn', 'Cu', r'\ce{Zn}', r'\ce{Cu}', r'\ce{ZnSO4(aq)}', r'\ce{CuSO4(aq)}', 'w', 'cu', dev='bulb', extra=dan_ions)

# ── 염다리 3단계 카드 (작게: viewBox 560 370을 그대로 줄여 씀 → 라벨 크게)
def bridge_card(stage):
    o = [beaker(40, 230), beaker(330, 520), sol(40, 230, 'w'), sol(330, 520, 'cu')]
    if stage > 0:
        o.append('<path d="M190 250 V112 H370 V250" fill="none" stroke="#B9A98A" stroke-width="30"/><path d="M190 250 V112 H370 V250" fill="none" stroke="#F6F0E0" stroke-width="24"/>')
    o.append(plate(124, 'Zn')); o.append(plate(424, 'Cu'))
    if stage == 0:
        o.append(T(135, 220, mix='양이온 증가', size=28, weight=700, fill='#D7263D', halo=True))
        o.append(T(135, 256, mix='(+) 전하 많음', size=26, halo=True))
        o.append(T(425, 220, mix='양이온 감소', size=28, weight=700, fill='#1F6FD1', halo=True))
        o.append(T(425, 256, mix='(−) 전하 많음', size=26, halo=True))
        o.append(T(280, 60, mix='전하 불균형 → 반응이 곧 멈춤', size=28, weight=700))
    else:
        o.append('<g data-anim="move" data-from="140,0" data-dur="1.6" data-on="step" data-ease="out"><g data-chg="232,112,12,-"></g>' + T(232, 84, tex=r'\ce{Cl-}', size=26, fill='#1F6FD1') + '</g>')
        o.append('<g data-anim="move" data-from="-140,0" data-dur="1.6" data-on="step" data-ease="out"><g data-chg="328,112,12,+"></g>' + T(328, 84, tex=r'\ce{K+}', size=26, fill='#D7263D') + '</g>')
        o.append('<g data-arw="300,150,220,150,minus,3"></g><g data-arw="260,180,340,180,plus,3"></g>')
        o.append(T(280, 230, mix='이온 이동', size=26, weight=700, halo=True))
        o.append(T(280, 330, mix='음이온 → 황산 아연 쪽 · 양이온 → 황산 구리(II) 쪽', size=24))
    return ''.join(o)
F['BR0'] = bridge_card(0)
F['BR1'] = bridge_card(1)

# ── 전위차 비유: 높은 곳 → 낮은 곳 (S17)
F['POT'] = ('<rect x="20" y="70" width="180" height="230" fill="#E3EEFB" stroke="#9FC3DD" stroke-width="2"/>'
            '<rect x="200" y="210" width="320" height="90" fill="#E3EEFB" stroke="#9FC3DD" stroke-width="2"/>'
            '<path d="M200 70 C260 70 270 210 330 210" fill="none" stroke="#5B6B7F" stroke-width="3" stroke-dasharray="7 6"/>'
            '<g data-anim="move" data-from="-200,-140" data-dur="1.8" data-rep="loop" data-ease="in"><circle cx="360" cy="196" r="14" fill="#1F6FD1"/>' + T(360, 203, tex='e^-', size=18, fill='#FFFFFF') + '</g>'
            '<line x1="540" y1="70" x2="540" y2="210" stroke="#5B6B7F" stroke-width="2"/><line x1="530" y1="70" x2="550" y2="70" stroke="#5B6B7F" stroke-width="2"/><line x1="530" y1="210" x2="550" y2="210" stroke="#5B6B7F" stroke-width="2"/>'
            + T(530, 150, mix='전위차', size=20, weight=700, anchor='end', halo=True) +
            T(110, 56, mix='전기적 위치 에너지 높음', size=19) + T(420, 196 - 40, mix='낮음', size=19) +
            T(110, 200, mix='(−)극', size=22, weight=700) + T(360, 270, mix='(+)극', size=22, weight=700))

# ── 표준 수소 전극 (S19)
she_extra = ('<rect x="104" y="76" width="40" height="190" rx="18" fill="#FFFFFF" fill-opacity=".35" stroke="#7E8B98" stroke-width="2"/>'
             '<g data-arw="40,96,100,96,ink,3"></g>' + T(36, 86, tex=r'\ce{H2}(g)', size=19, anchor='start') + T(40, 146, mix='1 atm', size=18, anchor='start') +
             '<g data-anim="move" data-from="0,30" data-dur="1.8" data-rep="loop"><circle cx="116" cy="236" r="5" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/><circle cx="132" cy="214" r="4" fill="#FFFFFF" stroke="#7FA8C9" stroke-width="2"/></g>'
             '<g data-chg="72,248,10,+"></g>' + T(72, 232, tex=r'\ce{H+}', size=18, halo=True) + T(44, 190, mix='백금판', size=18, anchor='start', halo=True) +
             '<g data-chg="470,210,10,+"></g>' + T(470, 196, tex=r'\ce{Cu^2+}', size=18, halo=True))
F['SHE'] = cell('Pt', 'Cu', r'', r'\ce{Cu}', r'1\ \text{M}\ \ce{H+}(aq)', r'1\ \text{M}\ \ce{CuSO4}(aq)', 'w', 'cu', extra=she_extra)

# ── 해 보기 반쪽 전지 셋
def halfcells():
    o = []
    for i, (m, tex, s, sk) in enumerate([('Zn', r'\ce{Zn}', r'\ce{ZnSO4(aq)}', 'w'), ('Cu', r'\ce{Cu}', r'\ce{CuSO4(aq)}', 'cu'), ('Fe', r'\ce{Fe}', r'\ce{FeSO4(aq)}', 'fe')]):
        x0 = 20 + i * 180
        o.append(beaker(x0, x0 + 130, 70, 220)); o.append(sol(x0, x0 + 130, sk, 100, 218)); o.append(plate(x0 + 65, m, 40, 150, 24))
        o.append(T(x0 + 65, 28, tex=tex, size=22)); o.append(T(x0 + 65, 252, tex=s, size=19))
    return ''.join(o)
F['HALF3'] = halfcells()

# ── 수직선: 표준 환원 전위
def eline():
    o = ['<g data-arw="30,70,540,70,ink,3"></g>']
    for v, s in [(-0.76, r'\ce{Zn}'), (-0.45, r'\ce{Fe}'), (0.0, r'\text{표준 수소 전극}'), (0.34, r'\ce{Cu}')]:
        x = 330 + v * 300
        o.append(f'<line x1="{x:.0f}" y1="58" x2="{x:.0f}" y2="82" stroke="#16233D" stroke-width="3"/>')
        o.append(T(f'{x:.0f}', 40, tex=s, size=20))
        o.append(T(f'{x:.0f}', 110, mix=f'{v:+.2f} V'.replace('+0.00', '0.00').replace('-', '−'), size=19))
    o.append(T(540, 140, tex=r'E^\circ', size=20, anchor='end'))
    return ''.join(o)
F['ELINE'] = eline()

# ── 탐구: 6홈판 전지 설계도
def hex6():
    o = ['<rect x="20" y="30" width="520" height="220" rx="18" fill="#F4F6F8" stroke="#9AA5B1" stroke-width="2"/>']
    W = [(110, 'Mg', r'\ce{MgSO4(aq)}', 'w'), (280, 'Cu', r'\ce{CuSO4(aq)}', 'cu'), (450, 'Zn', r'\ce{ZnSO4(aq)}', 'w')]
    for x, m, s, sk in W:
        c, op = SOL[sk]
        o.append(f'<circle cx="{x}" cy="150" r="58" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2"/><circle cx="{x}" cy="150" r="54" fill="{c}" fill-opacity="{op}"/>')
        f, st = MET[m]
        o.append(f'<rect x="{x-30}" y="96" width="16" height="96" rx="2" fill="{f}" stroke="{st}" stroke-width="2"/>')
        o.append(T(x + 14, 236, tex=s, size=18))
    o.append('<path d="M128 150 H262" stroke="#E6DFC9" stroke-width="16" stroke-linecap="round"/><path d="M128 150 H262" stroke="#C9B98F" stroke-width="2" stroke-dasharray="4 4"/>')
    o.append(T(290, 70, mix='거름종이 염다리($\\ce{KCl}$ 포화 용액)', size=18, anchor='start'))
    o.append('<line x1="300" y1="76" x2="200" y2="142" stroke="#5B6B7F" stroke-width="1.5"/>')
    o.append("<g data-circuit='{\"parts\":[[\"wire\",[[88,96],[88,24],[162,24]]],[\"wire\",[[198,24],[258,24],[258,96]]],[\"meter\",[180,24],\"V\",{\"r\":16}]],\"stroke\":3}'></g>")
    o.append(T(110, 286, mix='(−)극 · 마그네슘판', size=19, weight=700)); o.append(T(280, 286, mix='(+)극 · 구리판', size=19, weight=700))
    o.append(T(450, 286, mix='(다른 모둠 금속판)', size=18, fill='#5B6B7F'))
    return ''.join(o)
F['HEX6'] = hex6()

SC[0] = 1.3
# ── 대단원 마무리 05: B → A 전자
F['Q05'] = cell('A', 'B', r'\mathrm{A}', r'\mathrm{B}', r'1\ \text{M}\ \mathrm{A}^{2+}(aq)', r'1\ \text{M}\ \mathrm{B}^{2+}(aq)', 'w', 'w', e='l', dev='bulb', poles=False, flow=False)
F['Q05A'] = cell('A', 'B', r'\mathrm{A}', r'\mathrm{B}', r'1\ \text{M}\ \mathrm{A}^{2+}(aq)', r'1\ \text{M}\ \mathrm{B}^{2+}(aq)', 'w', 'w', e='l', dev='bulb', poles=False, flow=True, elab=False)
SC[0] = 1.45
# ── 07: Cu 왼쪽, X 오른쪽 (극 표시 없음)
F['Q07'] = cell('Cu', 'X', r'\ce{Cu}(s)', r'\mathrm{X}(s)', r'1\ \text{M}\ \ce{Cu^2+}(aq)', r'1\ \text{M}\ \mathrm{X}^{m+}(aq)', 'cu', 'w', dev='bulb', poles=False, flow=False, elab=False)

SC[0] = 1.0
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tpl.html'), encoding='utf-8').read()
def rep(m):
    k = m.group(1)
    return F[k]
out = re.sub(r'@@([A-Z0-9]+)@@', rep, tpl)
dst = sys.argv[1]
open(dst, 'w', encoding='utf-8').write(out)
print('ok', len(out), out.count('<section'))
