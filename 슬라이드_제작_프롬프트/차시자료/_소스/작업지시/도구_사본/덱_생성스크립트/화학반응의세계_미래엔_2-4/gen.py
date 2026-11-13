import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *
F = {}

def plating(coat=True, step='', ions=True, sol_lab=True):
    ex = ''
    if ions:
        ex += ('<g data-anim="move" data-from="110,0" data-dur="1.8" data-rep="loop" data-ease="lin">' + ion(250, 206, '+', r'\ce{Ag+}', fill=PLUS) + '</g>'
               '<g data-anim="move" data-from="110,0" data-dur="1.8" data-delay=".9" data-rep="loop" data-ease="lin">' + ion(262, 254, '+', r'\ce{Ag+}', fill=PLUS) + '</g>')
    ex += T(140, 108, mix='구리 펜던트', size=19, anchor='end') + T(414, 108, mix='은판', size=19, anchor='start')
    if sol_lab: ex += T(280, 288, tex=r'\ce{K[Ag(CN)2]}\ \text{용액}', size=19, fill=MUTED)
    return ecell(plus='R', Lel=pendant(170, 196, coat=coat, step=step), Rel=plate(390, 'Ag'), extra=ex)
F['COVER'] = plating()
F['PLATE'] = plating()

# ── 연결: 화학 전지 vs 전기 분해 (작은 그림 — 라벨 1.5배)
SC[0] = 1.5
F['MINIG'] = ecell(plus='R', dev='bulb', Lel=plate(170, 'Zn'), Rel=plate(390, 'Cu'), elab=False, extra=T(280, 250, mix='전해질', size=18, fill=MUTED))
F['MINIE'] = ecell(plus='L', Lel=plate(170, 'C'), Rel=plate(390, 'C'), elab=False, extra=T(280, 250, mix='전해질', size=18, fill=MUTED))
SC[0] = 1.0

# ── 생각 열기: 소금물에 전류
F['THINK'] = ecell(plus='L', Lel=plate(170, 'C'), Rel=plate(390, 'C'), poles=False, elab=False,
    extra=bubbles(170, [236, 206, 176, 146], 'h') + bubbles(390, [236, 206, 176, 146], 'h', side=-1) + T(280, 288, mix='소금물', size=19, fill=MUTED) +
    '<g data-anim="fade" data-dur="1.4" data-rep="alt"><path d="M150 104 q10 -10 0 -20 q-10 -10 0 -20" fill="none" stroke="#8FAE3A" stroke-width="3"/><path d="M182 104 q10 -10 0 -20 q-10 -10 0 -20" fill="none" stroke="#8FAE3A" stroke-width="3"/></g>' +
    T(206, 82, mix='냄새?', size=20, weight=700, anchor='start', fill='#5B7A1E', halo=True))

# ── 이온화 경향과 제련 방법
def series():
    el = ['K', 'Ca', 'Na', 'Mg', 'Al', 'Zn', 'Fe', 'Ni', 'Sn', 'Pb', 'Cu', 'Hg', 'Ag', 'Pt', 'Au']
    o = ['<g data-arw="1060,30,40,30,ox,5"></g>', T(550, 20, mix='이온화 경향이 크다 · 산화되기 쉽다 · 이온을 환원시키기 어렵다', size=19, weight=700, fill=OX, halo=True)]
    for i, s in enumerate(el):
        x = 60 + i * 70
        o.append(f'<circle cx="{x}" cy="84" r="26" fill="#EEF1F4" stroke="#7E8B98" stroke-width="2"/>')
        o.append(T(x, 92, tex=r'\ce{' + s + '}', size=22))
    bands = [(26, 374, '#FDE2E4', '용융액의 전기 분해', 'b1'), (376, 724, '#FFF1D6', '탄소 등으로 환원', 'b2'), (726, 1094, '#E3F2EA', '쉽게 환원 · 금, 백금은 홑원소로 산출', 'b3')]
    for x0, x1, c, t, g in bands:
        o.append(f'<g class="step" data-g="{g}"><rect x="{x0}" y="124" width="{x1-x0}" height="44" rx="8" fill="{c}" stroke="#9AA5B1" stroke-width="1.5"/>' + T((x0+x1)//2, 153, mix=t, size=20, weight=700) + '</g>')
    return ''.join(o)
F['SERIES'] = series()

# ── 염화 나트륨 용융액
def molten():
    ex = (bubbles(170, [236, 206, 176, 146], 'cl') + T(214, 136, tex=r'\ce{Cl2}(g)', size=19, anchor='start', halo=True) +
          '<g data-anim="move" data-from="0,30" data-dur="2.2" data-rep="loop"><circle cx="410" cy="170" r="7" fill="#C9CED6" stroke="#7E8B98" stroke-width="2"/><circle cx="414" cy="200" r="6" fill="#C9CED6" stroke="#7E8B98" stroke-width="2"/></g>' +
          T(426, 172, tex=r'\ce{Na}(l)', size=19, anchor='start', halo=True) +
          '<g data-anim="move" data-from="-70,0" data-dur="1.8" data-rep="loop" data-ease="lin">' + ion(330, 222, '+', r'\ce{Na+}(l)', fill=PLUS) + '</g>' +
          '<g data-anim="move" data-from="70,0" data-dur="1.8" data-rep="loop" data-ease="lin">' + ion(232, 252, '-', r'\ce{Cl-}(l)', ly=282, fill=MINUS) + '</g>' +
          T(410, 288, mix='염화 나트륨 용융액', size=18, fill=MUTED) +
          T(150, 108, mix='흑연 전극', size=18, anchor='end', fill=MUTED) + T(410, 108, mix='철 전극', size=18, anchor='start', fill=MUTED))
    return ecell(plus='L', solk='melt', Lel=plate(170, 'C'), Rel=plate(390, 'Fe'), extra=ex)
F['MOLTEN'] = molten()

# ── 염화 나트륨 수용액
def aqnacl():
    ex = (bubbles(170, [236, 206, 176, 146], 'cl') + T(150, 140, tex=r'\ce{Cl2}(g)', size=19, anchor='end', halo=True) +
          bubbles(390, [236, 206, 176, 146], 'h', side=-1) + T(410, 140, tex=r'\ce{H2}(g)', size=19, anchor='start', halo=True) +
          '<g data-anim="move" data-from="60,0" data-dur="1.8" data-rep="loop" data-ease="lin">' + ion(236, 220, '-', r'\ce{Cl-}', ly=250, fill=MINUS) + '</g>' +
          ion(300, 190, '+', r'\ce{Na+}', fill=PLUS) +
          T(440, 196, tex=r'\ce{H2O}', size=19, anchor='start', halo=True) +
          '<g data-anim="fade" data-dur="1.4" data-delay=".6">' + ion(430, 246, '-', r'\ce{OH-}', lx=452, ly=252, fill=MINUS) + '</g>' +
          T(280, 288, mix='진한 염화 나트륨 수용액', size=18, fill=MUTED))
    return ecell(plus='L', solk='w', Lel=plate(170, 'C'), Rel=plate(390, 'C'), extra=ex)
SC[0] = 1.2
F['AQNACL'] = aqnacl()
SC[0] = 1.0

# ── 구리의 정제
def refine(q=False):
    if not q:
        ex = ('<g data-anim="move" data-from="-30,0" data-dur="1.6" data-rep="loop" data-ease="out">'
              '<g data-arw="190,176,216,176,ox,2.5"></g><g data-arw="190,210,216,210,ox,2.5"></g><g data-arw="190,244,216,244,ox,2.5"></g></g>' +
              T(222, 183, tex=r'\ce{Cu^2+}', size=18, anchor='start', halo=True) + T(222, 217, tex=r'\ce{Zn^2+}', size=18, anchor='start', halo=True) +
              T(222, 251, tex=r'\ce{Fe^2+}', size=18, anchor='start', halo=True) +
              '<g data-anim="move" data-from="-40,0" data-dur="1.6" data-rep="loop" data-ease="in"><g data-arw="338,160,374,160,rd,2.5"></g><g data-arw="338,232,374,232,rd,2.5"></g></g>' +
              T(332, 166, tex=r'\ce{Cu^2+}', size=18, anchor='end', halo=True) + T(332, 238, tex=r'\ce{Cu^2+}', size=18, anchor='end', halo=True) +
              '<path d="M136 296 Q150 274 170 276 Q190 274 204 296 Z" fill="#9AA0A8" stroke="#6B7280" stroke-width="1.5"/>' +
              T(212, 290, mix='찌꺼기($\\ce{Ag}$, $\\ce{Au}$, $\\ce{Pt}$)', size=18, anchor='start', halo=True) +
              T(450, 290, tex=r'\ce{CuSO4}(aq)', size=18, fill=MUTED) +
              T(150, 98, mix='불순물을||포함한 구리', size=18, anchor='end') + T(410, 98, mix='순수한||구리', size=18, anchor='start'))
        return ecell(plus='L', solk='cu', Lel=plate(170, 'Cu', specks=True), Rel=plate(390, 'Cu', w=22), extra=ex)
    ex = ('<g data-arw="190,186,230,186,ink,2.5"></g>' + T(238, 193, tex=r'\mathrm{X}^{2+}', size=20, anchor='start', halo=True) +
          '<g data-arw="190,228,226,240,ink,2.5"></g>' + T(234, 252, tex=r'\ce{Cu^2+}', size=20, anchor='start', halo=True) +
          '<g data-arw="330,214,372,204,ink,2.5"></g>' + T(324, 222, tex=r'\ce{Cu^2+}', size=20, anchor='end', halo=True) +
          '<path d="M136 296 Q150 274 170 276 Q190 274 204 296 Z" fill="#9AA0A8" stroke="#6B7280" stroke-width="1.5"/>' +
          T(212, 292, mix='금속 $\\mathrm{Y}$', size=20, anchor='start', halo=True) +
          T(420, 290, tex=r'1\ \text{M}\ \ce{CuSO4}(aq)', size=19, fill=MUTED) +
          T(150, 98, mix='불순물이||포함된 구리', size=20, anchor='end'))
    return ecell(plus='L', solk='cu', Lel=plate(170, 'Cu', specks=True), Rel=plate(390, 'Cu', w=22), flow=False, elab=False, rdox=False, extra=ex)
F['REFINE'] = refine()
SC[0] = 1.25
F['Q10'] = refine(True)
SC[0] = 1.0

# ── 알루미늄 제련 (해 보기 결과 예시)
def alum():
    o = ["<g data-circuit='{\"parts\":[[\"wire\",[[138,50],[280,50],[280,112]]],[\"wire\",[[122,50],[36,50],[36,236],[70,236]]],[\"bat\",[130,50],{\"dir\":\"h\",\"pos\":\"right\",\"signs\":true}]],\"stroke\":3}'></g>",
         '<rect x="70" y="140" width="420" height="170" rx="6" fill="#4A4F57" stroke="#16233D" stroke-width="2"/>',
         '<rect x="84" y="150" width="392" height="146" fill="#F9DDB0"/>',
         '<rect x="84" y="262" width="392" height="34" fill="#D5DAE0" stroke="#9AA5B1" stroke-width="1.5"/>',
         '<rect x="226" y="112" width="108" height="104" rx="4" fill="#4A4F57" stroke="#16233D" stroke-width="2"/>',
         bubbles(334, [206, 186, 166], 'h', side=1), bubbles(226, [206, 186, 166], 'h', side=-1),
         '<path d="M280 112 V50 H138" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>',
         '<path d="M122 50 H36 V236 H70" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>',
         '<g data-arw="250,30,170,30,minus,3"></g>', T(210, 22, tex='e^-', size=20, fill=MINUS),
         '<g data-arw="20,110,20,170,minus,3"></g>', T(14, 100, tex='e^-', size=20, fill=MINUS, anchor='start'),
         T(280, 168, mix='탄소', size=19, fill='#FFFFFF', weight=700),
         T(350, 96, mix='(+)극', size=19, weight=700, anchor='start'), T(350, 120, mix='산화 전극', size=19, weight=700, anchor='start', fill=OX),
         T(300, 250, mix='산화 알루미늄 + 빙정석(용융)', size=18, halo=True),
         T(390, 284, mix='용융 알루미늄', size=18, weight=700),
         T(200, 336, mix='탄소 벽 = (−)극', size=19, weight=700), T(360, 336, mix='환원 전극', size=19, weight=700, fill=RD),
         T(396, 210, tex=r'\ce{CO2}(g)', size=18, anchor='start', halo=True)]
    return ''.join(o)
F['ALUM'] = alum()

# ── 자료실: 함석의 흠집
F['GALV'] = ('<rect x="40" y="170" width="480" height="60" fill="#8C8F94" stroke="#5B6B7F" stroke-width="2"/>'
             '<rect x="40" y="140" width="210" height="30" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/>'
             '<rect x="310" y="140" width="210" height="30" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/>'
             '<path d="M170 140 C200 52 360 52 390 140 H310 V170 H250 V140 Z" fill="#DDEEF8" fill-opacity=".85" stroke="#9FC3DD" stroke-width="2"/>'
             + T(96, 162, mix='아연', size=19, weight=700) + T(462, 162, mix='아연', size=19, weight=700) + T(470, 210, mix='철', size=20, weight=700, fill='#FFFFFF') +
             '<g data-anim="move" data-from="10,40" data-dur="1.6" data-rep="loop" data-ease="out"><g data-chg="214,98,11,+"></g>' + T(186, 92, tex=r'\ce{Zn^2+}', size=19, anchor='end', fill=OX, halo=True) + '</g>'
             '<g data-arw="226,138,216,112,ox,2.5"></g>'
             '<path d="M150 200 H276" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 13" stroke-linecap="round" data-anim="dash" data-flow data-speed="30"/>'
             '<g data-arw="150,186,266,186,minus,3"></g>' + T(124, 192, tex='e^-', size=20, fill='#FFFFFF') +
             T(322, 88, tex=r'\ce{O2},\ \ce{H2O}', size=19, anchor='start', halo=True) + '<g data-arw="318,96,288,164,rd,2.5"></g>' +
             T(350, 132, tex=r'\ce{OH-}', size=19, anchor='start', fill=RD, halo=True) +
             T(280, 252, mix='흠집 — 철이 드러남', size=18, fill=MUTED))

# ── 도금 활용 아이콘
F['USE_AU'] = ('<circle cx="120" cy="82" r="50" fill="#E9C46A" stroke="#B8860B" stroke-width="3"/><circle cx="120" cy="82" r="30" fill="none" stroke="#B8860B" stroke-width="2"/>'
               '<path d="M96 30 L120 6 L144 30" fill="none" stroke="#B8860B" stroke-width="3"/><path d="M98 66 Q108 58 116 66" fill="none" stroke="#FFF4C8" stroke-width="5" stroke-linecap="round"/>')
F['USE_SN'] = ('<rect x="70" y="40" width="100" height="100" fill="#C9CED6" stroke="#7E8B98" stroke-width="3"/><ellipse cx="120" cy="40" rx="50" ry="14" fill="#E4E8EC" stroke="#7E8B98" stroke-width="3"/>'
               '<ellipse cx="120" cy="140" rx="50" ry="14" fill="#C9CED6" stroke="#7E8B98" stroke-width="3"/><line x1="70" y1="80" x2="170" y2="80" stroke="#9AA5B1" stroke-width="2"/><line x1="70" y1="104" x2="170" y2="104" stroke="#9AA5B1" stroke-width="2"/>')
F['USE_CR'] = ('<rect x="96" y="120" width="48" height="36" rx="6" fill="#B8BEC6" stroke="#7E8B98" stroke-width="3"/><rect x="108" y="36" width="24" height="88" rx="6" fill="#DDE1E6" stroke="#7E8B98" stroke-width="3"/>'
               '<path d="M120 50 H188 Q204 50 204 66 V84" fill="none" stroke="#7E8B98" stroke-width="18" stroke-linecap="round"/><path d="M120 50 H188 Q204 50 204 66 V84" fill="none" stroke="#E4E8EC" stroke-width="12" stroke-linecap="round"/>'
               '<rect x="104" y="18" width="32" height="12" rx="4" fill="#B8BEC6" stroke="#7E8B98" stroke-width="2"/><path d="M114 44 V112" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')

# ── 탐구 과정 카드
F['P1'] = ('<rect x="20" y="96" width="260" height="96" rx="14" fill="#F4F6F8" stroke="#9AA5B1" stroke-width="2"/>'
           + ''.join(f'<circle cx="{x}" cy="{y}" r="18" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2"/>' for x in (70, 150, 230) for y in (124, 166)) +
           '<g data-anim="fade" data-dur="1.4"><circle cx="70" cy="124" r="15" fill="#DDEEF8"/></g>'
           '<rect x="62" y="18" width="16" height="58" rx="4" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2"/><rect x="58" y="10" width="24" height="14" rx="6" fill="#5B6B7F"/><path d="M66 76 L70 92 L74 76 Z" fill="#7E8B98"/>'
           '<g data-anim="move" data-from="0,-14" data-dur="1.2" data-rep="loop" data-ease="in"><circle cx="70" cy="100" r="4" fill="#9FC3DD"/></g>'
           + T(100, 50, tex=r'\ce{K[Ag(CN)2]}\ \text{용액}', size=18, anchor='start'))
F['P2'] = ('<rect x="70" y="10" width="160" height="46" rx="6" fill="#5B6B7F"/>' + ''.join(f'<rect x="{x}" y="18" width="42" height="30" rx="4" fill="#E9C46A" stroke="#16233D" stroke-width="1.5"/>' for x in (80, 129, 178)) +
           '<path d="M226 34 Q262 40 214 118" fill="none" stroke="#D7263D" stroke-width="4"/><path d="M74 34 Q40 40 96 118" fill="none" stroke="#16233D" stroke-width="4"/>'
           '<ellipse cx="150" cy="150" rx="92" ry="34" fill="#DDEEF8" stroke="#7E8B98" stroke-width="2"/>'
           '<rect x="200" y="112" width="24" height="52" rx="3" fill="#DDE1E6" stroke="#8C99A6" stroke-width="2"/>'
           '<line x1="96" y1="118" x2="96" y2="132" stroke="#5B6B7F" stroke-width="3"/><circle cx="96" cy="146" r="16" fill="#D9925E" stroke="#A0623A" stroke-width="2.5"/>'
           + T(264, 70, mix='(+)극', size=19, weight=700, anchor='end', fill=PLUS) + T(36, 70, mix='(−)극', size=19, weight=700, anchor='start', fill=MINUS) +
           T(262, 196, mix='은판', size=18, anchor='end') + T(38, 196, mix='구리 펜던트', size=18, anchor='start'))
F['P3'] = ('<line x1="110" y1="30" x2="110" y2="70" stroke="#5B6B7F" stroke-width="3"/><circle cx="110" cy="96" r="26" fill="#E4E8EC" stroke="#8C99A6" stroke-width="3"/>'
           '<path d="M98 82 Q106 76 114 82" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
           '<path d="M220 150 V96 Q220 84 232 84 H252 Q264 84 264 96 V150 Z" fill="#F4F9FC" stroke="#7E8B98" stroke-width="2"/><path d="M232 84 L214 58 L170 70" fill="none" stroke="#7E8B98" stroke-width="3"/>'
           '<g data-anim="move" data-from="30,-10" data-dur="1.2" data-rep="loop" data-ease="lin"><circle cx="146" cy="82" r="3.5" fill="#9FC3DD"/><circle cx="140" cy="92" r="3" fill="#9FC3DD"/><circle cx="150" cy="96" r="3" fill="#9FC3DD"/></g>'
           + T(110, 156, mix='은색 펜던트', size=18) + T(242, 176, mix='증류수', size=18))

F['RES'] = '<tr><td>은</td><td>3개</td><td>10분</td><td>0.49 mmol</td><td>+53.4 mg</td><td>−53.0 mg</td><td><span class="step" data-g="s0">109</span></td></tr><tr><td>은</td><td>3개</td><td>20분</td><td>1.01 mmol</td><td>+108.4 mg</td><td>−109.3 mg</td><td><span class="step" data-g="s0">107</span></td></tr><tr><td>은</td><td>1개</td><td>20분</td><td>0.24 mmol</td><td>+26.4 mg</td><td>−26.3 mg</td><td><span class="step" data-g="s0">110</span></td></tr><tr><td>구리</td><td>3개</td><td>20분</td><td>1.01 mmol</td><td>+31.9 mg</td><td>−31.9 mg</td><td><span class="step" data-g="s0">32</span></td></tr>'
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tpl.html'), encoding='utf-8').read()
out = re.sub(r'@@([A-Z0-9_]+)@@', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('ok', len(out), out.count('<section'))
