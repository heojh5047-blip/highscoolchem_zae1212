import sys, re, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *
F = {}
EQ, FIELD = '#E08A2C', '#2E9E6A'

def pill(x, y, tex, w=74, h=34, fill='#FFFFFF', stroke='#5B6B7F', size=20, mix=False):
    o = f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    return o + (T(x, y + 7, mix=tex, size=size) if mix else T(x, y + 7, tex=tex, size=size))

# ── 반응식 + 산화/환원 괄호 (교과서 그림 Ⅱ-18 꼴)
def rxn(terms, top, bot, W=600, size=26):
    xs, x = [], 10
    for tex, w in terms:
        xs.append(x + w / 2); x += w
    off = (W - x) / 2
    xs = [v + off for v in xs]
    o = []
    for (tex, w), cx in zip(terms, xs):
        o.append(T(round(cx), 78, tex=tex, size=size))
    (i, j) = top
    o.append(f'<g data-anim="draw" data-dur="1.0"><path d="M{xs[i]:.0f} 50 V28 H{xs[j]:.0f} V40" fill="none" stroke="{OX}" stroke-width="2.5"/></g>')
    o.append(f'<g data-arw="{xs[j]:.0f},38,{xs[j]:.0f},52,ox,2.5" data-delay="1"></g>')
    o.append(T(round((xs[i] + xs[j]) / 2), 22, mix='산화', size=24, weight=700, fill=OX, halo=True))
    (i, j) = bot
    o.append(f'<g data-anim="draw" data-dur="1.0" data-delay=".6"><path d="M{xs[i]:.0f} 90 V112 H{xs[j]:.0f} V100" fill="none" stroke="{RD}" stroke-width="2.5"/></g>')
    o.append(f'<g data-arw="{xs[j]:.0f},102,{xs[j]:.0f},88,rd,2.5" data-delay="1.6"></g>')
    o.append(T(round((xs[i] + xs[j]) / 2), 134, mix='환원', size=24, weight=700, fill=RD, halo=True))
    return ''.join(o)

F['RX_RESP'] = rxn([(r'\ce{C6H12O6}', 130), ('+', 34), (r'\ce{6O2}', 70), (r'\ce{->}', 70), (r'\ce{6CO2}', 86), ('+', 34), (r'\ce{6H2O}', 86)], (0, 4), (2, 6))
F['RX_PHOTO'] = rxn([(r'\ce{6CO2}', 86), ('+', 34), (r'\ce{6H2O}', 86), (r'\ce{->}', 70), (r'\ce{C6H12O6}', 130), ('+', 34), (r'\ce{6O2}', 70)], (2, 6), (0, 4))

# ── 마이토콘드리아 (세포 호흡)
def mito(cx=240, cy=160, rx=140, ry=78):
    o = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#F8DCCB" stroke="#C77B54" stroke-width="3"/>'
    o += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-14}" ry="{ry-14}" fill="#FBEAE0" stroke="#D99877" stroke-width="2"/>'
    d = f'M{cx-rx+26} {cy}'
    for k in range(9):
        x = cx - rx + 40 + k * 26
        d += f' L{x} {cy-36 if k%2==0 else cy+36}'
    o += f'<path d="{d}" fill="none" stroke="#C77B54" stroke-width="3" stroke-linejoin="round"/>'
    return o

def resp():
    o = mito()
    o += '<g data-anim="move" data-from="-34,0" data-dur="1.6" data-rep="loop" data-ease="lin">' + pill(66, 104, r'\ce{C6H12O6}', w=112) + pill(66, 222, r'\ce{O2}') + '</g>'
    o += T(66, 74, mix='포도당', size=19, fill=MUTED) + T(66, 260, mix='산소', size=19, fill=MUTED)
    o += '<g data-arw="124,110,150,128,ink,3"></g><g data-arw="104,214,138,196,ink,3"></g>'
    o += '<g data-arw="350,120,384,100,ink,3"></g><g data-arw="352,160,388,160,ink,3"></g><g data-arw="350,200,384,222,ink,3"></g>'
    o += '<g data-anim="move" data-from="-24,0" data-dur="1.6" data-rep="loop" data-ease="lin">' + pill(424, 94, r'\ce{CO2}') + pill(424, 160, r'\ce{H2O}') + '</g>'
    o += f'<g data-anim="pop" data-o="424,232" data-dur="1.2" data-rep="loop"><path d="M424 206 L432 222 L450 224 L436 236 L440 254 L424 244 L408 254 L412 236 L398 224 L416 222 Z" fill="#FDE7C2" stroke="{EQ}" stroke-width="2.5"/></g>'
    o += T(424, 280, mix='에너지', size=19, weight=700, fill=EQ)
    o += T(240, 270, mix='마이토콘드리아', size=19, fill='#A0623A')
    return o
F['RESP'] = resp()

# ── 엽록체 (광합성)
def photo():
    o = '<circle cx="64" cy="54" r="26" fill="#F2C230" stroke="#D9A21B" stroke-width="2"/>'
    for k in range(8):
        a = k * math.pi / 4
        o += f'<line x1="{64+math.cos(a)*34:.0f}" y1="{54+math.sin(a)*34:.0f}" x2="{64+math.cos(a)*44:.0f}" y2="{54+math.sin(a)*44:.0f}" stroke="#D9A21B" stroke-width="3" stroke-linecap="round"/>'
    o += '<g data-anim="draw" data-dur="1.2" data-rep="loop"><path d="M102 74 L128 90 L118 98 L150 116" fill="none" stroke="#E08A2C" stroke-width="3.5" stroke-linejoin="round"/></g>'
    o += T(150, 70, mix='빛에너지', size=19, weight=700, fill=EQ, anchor='start')
    o += '<ellipse cx="240" cy="170" rx="132" ry="74" fill="#D7ECC4" stroke="#5E9B3A" stroke-width="3"/>'
    for gx, gy in [(178, 150), (232, 186), (290, 148), (300, 196), (190, 196)]:
        for k in range(4):
            o += f'<rect x="{gx-18}" y="{gy-14+k*7}" width="36" height="6" rx="3" fill="#6FAE45" stroke="#4C8A2B" stroke-width="1"/>'
    o += '<g data-anim="move" data-from="-34,0" data-dur="1.6" data-rep="loop" data-ease="lin">' + pill(56, 140, r'\ce{CO2}') + pill(56, 220, r'\ce{H2O}') + '</g>'
    o += '<g data-arw="96,144,122,152,ink,3"></g><g data-arw="96,216,124,204,ink,3"></g>'
    o += '<g data-arw="358,140,388,124,ink,3"></g><g data-arw="358,200,388,216,ink,3"></g>'
    o += '<g data-anim="move" data-from="-24,0" data-dur="1.6" data-rep="loop" data-ease="lin">' + pill(424, 112, r'\ce{C6H12O6}', w=112) + pill(424, 228, r'\ce{O2}') + '</g>'
    o += T(424, 82, mix='포도당', size=19, fill=MUTED) + T(424, 266, mix='산소', size=19, fill=MUTED)
    o += T(240, 270, mix='엽록체', size=19, fill='#4C8A2B')
    return o
F['PHOTO'] = photo()

# ── 광합성 ↔ 세포 호흡 순환 (단계 카드)
def cycle():
    o = []
    o.append('<rect x="70" y="80" width="300" height="100" rx="16" fill="#E8F4DD" stroke="#5E9B3A" stroke-width="3"/>')
    o.append(T(220, 122, mix='광합성', size=24, weight=700) + T(220, 156, mix='엽록체', size=19, fill='#4C8A2B'))
    o.append('<rect x="630" y="80" width="300" height="100" rx="16" fill="#FBEAE0" stroke="#C77B54" stroke-width="3"/>')
    o.append(T(780, 122, mix='세포 호흡', size=24, weight=700) + T(780, 156, mix='마이토콘드리아', size=19, fill='#A0623A'))
    o.append('<g class="step" data-g="c1"><g data-arw="150,22,190,74,equi,4"></g>' + T(138, 22, mix='빛에너지', size=20, weight=700, fill=EQ, anchor='end') +
             '<g data-anim="draw" data-dur="1.2" data-on="step"><g data-arw="376,110,624,110,ink,4"></g></g>' + T(500, 98, mix='포도당 + 산소', size=21, weight=700, halo=True) +
             T(220, 212, mix='물 → 산소 (산화)', size=19, weight=700, fill=OX) + T(220, 240, mix='이산화 탄소 → 포도당 (환원)', size=19, weight=700, fill=RD) + '</g>')
    o.append('<g class="step" data-g="c2"><g data-arw="850,74,890,22,equi,4"></g>' + T(902, 30, mix='에너지 방출', size=20, weight=700, fill=EQ, anchor='start') +
             '<g data-anim="draw" data-dur="1.2" data-on="step"><g data-arw="624,154,376,154,ink,4"></g></g>' + T(500, 176, mix='이산화 탄소 + 물', size=21, weight=700, halo=True) +
             T(780, 212, mix='포도당 → 이산화 탄소 (산화)', size=19, weight=700, fill=OX) + T(780, 240, mix='산소 → 물 (환원)', size=19, weight=700, fill=RD) + '</g>')
    return ''.join(o)
F['CYCLE'] = cycle()

# ── 연결: 산화·환원 반응이 쓰이는 곳
def link():
    o = ['<circle cx="260" cy="180" r="74" fill="#F4F6F8" stroke="#16233D" stroke-width="3"/>',
         T(260, 172, mix='산화·환원', size=22, weight=700) + T(260, 202, mix='(전자의 이동)', size=19, fill=MINUS)]
    nodes = [(96, 60, '세포 호흡', '#FBEAE0', '#C77B54'), (424, 60, '광합성', '#E8F4DD', '#5E9B3A'),
             (96, 300, '화학 전지', '#EEF3F8', '#5B6B7F'), (424, 300, '전기 분해', '#EEF3F8', '#5B6B7F')]
    for k, (x, y, t, f, s) in enumerate(nodes):
        o.append(f'<line x1="260" y1="180" x2="{x}" y2="{y}" stroke="#9AA5B1" stroke-width="2.5" stroke-dasharray="6 5"/>')
    for k, (x, y, t, f, s) in enumerate(nodes):
        o.append(f'<g data-anim="pop" data-o="{x},{y}" data-dur=".8" data-delay="{.3+k*.25:.2f}"><rect x="{x-80}" y="{y-28}" width="160" height="56" rx="14" fill="{f}" stroke="{s}" stroke-width="2.5"/>' + T(x, y + 8, mix=t, size=21, weight=700) + '</g>')
    return ''.join(o)
F['LINK'] = link()

# ── 수소 연료 전지 (2-2 그림 꼴)
def fuel(big=False):
    o = ['<g data-circuit=\'{"parts":[["wire",[[175,110],[175,60],[262,60]]],["wire",[[298,60],[385,60],[385,110]]],["bulb",[280,60],{"r":18,"on":true}]],"stroke":3}\'></g>',
         '<rect x="120" y="120" width="320" height="170" rx="8" fill="#EEF3F8" stroke="#5B6B7F" stroke-width="2"/><rect x="190" y="120" width="180" height="170" fill="#EFE6C8"/>',
         '<rect x="160" y="110" width="30" height="180" rx="3" fill="#F6E1D6" stroke="#C2410C" stroke-width="3"/><rect x="370" y="110" width="30" height="180" rx="3" fill="#D6ECF0" stroke="#0E7490" stroke-width="3"/>',
         '<g data-anim="move" data-from="-30,0" data-dur="1.8" data-rep="loop" data-ease="lin"><g data-arw="44,170,116,170,ink,3"></g></g>',
         '<g data-anim="move" data-from="30,0" data-dur="1.8" data-rep="loop" data-ease="lin"><g data-arw="516,170,444,170,ink,3"></g></g><g data-arw="444,250,516,250,ink,3"></g>',
         T(80, 158, tex=r'\ce{H2}', size=20) + T(70, 200, mix='수소 공급', size=18) + T(480, 158, tex=r'\ce{O2}', size=20) + T(490, 200, mix='산소 공급', size=18) +
         T(480, 238, tex=r'\ce{H2O}', size=20) + T(490, 280, mix='물 생성', size=18),
         '<g data-anim="move" data-from="-40,0" data-dur="2.2" data-rep="loop" data-ease="lin"><g data-chg="236,196,10,+"></g><g data-arw="250,196,290,196,plus,2.5"></g><g data-chg="290,240,10,+"></g><g data-arw="304,240,344,240,plus,2.5"></g>' +
         T(236, 178, tex=r'\ce{H+}', size=18, fill=PLUS, halo=True) + '</g>',
         T(280, 282, mix='전해질 막', size=18, fill=MUTED),
         '<path d="M175 110 V60 H262 M298 60 H385 V110" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>',
         '<g data-arw="190,40,244,40,minus,3"></g><g data-arw="316,40,370,40,minus,3"></g>' + T(217, 30, tex='e^-', size=20, fill=MINUS) + T(343, 30, tex='e^-', size=20, fill=MINUS),
         T(175, 322, mix='(−)극', size=20, weight=700) + T(175, 348, mix='산화 전극', size=19, weight=700, fill=OX) +
         T(385, 322, mix='(+)극', size=20, weight=700) + T(385, 348, mix='환원 전극', size=19, weight=700, fill=RD)]
    return ''.join(o)
F['FUEL'] = fuel()

# ── 미생물 연료 전지
def mfc():
    o = ['<g data-circuit=\'{"parts":[["wire",[[90,110],[90,52],[262,52]]],["wire",[[298,52],[430,52],[430,110]]],["bulb",[280,52],{"r":17,"on":true}]],"stroke":3}\'></g>',
         '<rect x="30" y="96" width="460" height="176" rx="8" fill="#FFFFFF" stroke="#5B6B7F" stroke-width="2.5"/>',
         '<rect x="32" y="98" width="228" height="172" fill="#EFE3CF"/><rect x="260" y="98" width="228" height="172" fill="#DDEEF8"/>',
         '<line x1="260" y1="98" x2="260" y2="270" stroke="#7E8B98" stroke-width="4" stroke-dasharray="8 6"/>',
         '<rect x="78" y="110" width="24" height="140" rx="3" fill="#4A4F57" stroke="#16233D" stroke-width="2"/><rect x="418" y="110" width="24" height="140" rx="3" fill="#4A4F57" stroke="#16233D" stroke-width="2"/>',
         '<path d="M90 110 V52 H262 M298 52 H430 V110" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>',
         '<g data-arw="116,32,176,32,minus,3"></g><g data-arw="344,32,404,32,minus,3"></g>' + T(146, 24, tex='e^-', size=20, fill=MINUS) + T(374, 24, tex='e^-', size=20, fill=MINUS)]
    mic = '<g data-anim="move" data-from="3,0" data-dur=".5" data-rep="swing">'
    for x, y, a in [(126, 150, 20), (150, 186, -30), (122, 222, 10), (176, 150, 60), (190, 220, -10)]:
        mic += f'<rect x="{x-12}" y="{y-6}" width="24" height="12" rx="6" fill="#9CCB8A" stroke="#4C8A2B" stroke-width="2" transform="rotate({a} {x} {y})"/>'
    o.append(mic + '</g>')
    o.append(T(176, 126, mix='폐수 속 유기물', size=20, weight=700))
    o.append(T(196, 258, mix='미생물', size=20, fill='#4C8A2B', halo=True))
    o.append('<g data-anim="move" data-from="-44,0" data-dur="2" data-rep="loop" data-ease="lin"><g data-chg="282,180,10,+"></g>' + T(282, 162, tex=r'\ce{H+}', size=20, fill=PLUS, halo=True) + '</g>')
    o.append(T(232, 214, tex=r'\ce{CO2}', size=20, halo=True))
    o.append(T(356, 132, tex=r'\ce{O2}', size=21, halo=True) + '<g data-arw="374,140,410,150,ink,2.5"></g>')
    o.append(T(356, 236, tex=r'\ce{H2O}', size=21, halo=True) + '<g data-arw="410,214,378,224,ink,2.5"></g>')
    o.append(T(260, 296, mix='분리막', size=20, fill=MUTED))
    o.append(T(90, 296, mix='(−)극', size=21, weight=700) + T(90, 320, mix='산화 전극', size=20, weight=700, fill=OX))
    o.append(T(430, 296, mix='(+)극', size=21, weight=700) + T(430, 320, mix='환원 전극', size=20, weight=700, fill=RD))
    return ''.join(o)
F['MFC'] = mfc()

# ── 항산화제 / 바이타민 C 와 활성 산소
def antiox(name='항산화제', eon=False, step=''):
    o = []
    d1 = 'M30 230 ' + ' '.join(f'Q{30+40*k+20} {230-36 if k%2==0 else 230+36} {30+40*(k+1)} 230' for k in range(11))
    d2 = 'M30 230 ' + ' '.join(f'Q{30+40*k+20} {230+36 if k%2==0 else 230-36} {30+40*(k+1)} 230' for k in range(11))
    for k in range(22):
        x = 40 + k * 20
        if (x - 30) % 40 in (0,):
            continue
        o.append(f'<line x1="{x}" y1="214" x2="{x}" y2="246" stroke="#B9C2CC" stroke-width="3"/>')
    o.append(f'<path d="{d1}" fill="none" stroke="#7B4FC8" stroke-width="5"/><path d="{d2}" fill="none" stroke="#2E9E6A" stroke-width="5"/>')
    o.append(T(480, 286, tex=r'\text{DNA}', size=23, anchor='end'))
    o.append('<g data-anim="move" data-from="-60,-40" data-dur="1.4" data-ease="out"><circle cx="200" cy="100" r="24" fill="#E5533D" stroke="#A33022" stroke-width="2.5"/><circle cx="214" cy="88" r="4.5" fill="#FFFFFF"/>' +
             T(200, 60, mix='활성 산소', size=23, weight=700, halo=True) + '</g>')
    o.append('<g data-arw="200,128,200,186,plus,3,d"></g>' + T(214, 166, mix='공격', size=23, fill=PLUS, anchor='start', halo=True))
    o.append('<rect x="340" y="74" width="120" height="54" rx="12" fill="#FBE3BC" stroke="#E08A2C" stroke-width="2.5"/>' + T(400, 108, mix=name, size=23, weight=700))
    if eon:
        o.append(f'<g class="step" data-g="{step}"><g data-anim="move" data-from="40,0" data-dur="1.2" data-on="step"><g data-arw="334,100,232,100,minus,3.5"></g>' + T(283, 88, tex='e^-', size=24, fill=MINUS, halo=True) + '</g>'
                 + T(400, 154, mix='자신은 산화', size=23, weight=700, fill=OX) + '</g>')
    return ''.join(o)
F['ANTI'] = antiox()
F['ANTI_E'] = antiox(eon=True, step='a2')
F['VITC'] = antiox('바이타민 C', eon=True, step='v2')

# ── 전기뱀장어
def eel():
    o = ['<path d="M40 150 C110 90 170 210 250 150 S390 100 440 140" fill="none" stroke="#5E7C55" stroke-width="40" stroke-linecap="round"/>',
         '<path d="M40 150 C110 90 170 210 250 150 S390 100 440 140" fill="none" stroke="#8DAA7E" stroke-width="18" stroke-linecap="round" stroke-dasharray="10 8"/>',
         '<circle cx="452" cy="134" r="6" fill="#FFFFFF" stroke="#16233D" stroke-width="2"/><circle cx="453" cy="134" r="2.5" fill="#16233D"/>',
         '<g data-anim="fade" data-dur=".5" data-rep="alt"><path d="M472 112 L490 98 L484 118 L506 106" fill="none" stroke="#E08A2C" stroke-width="4" stroke-linejoin="round"/><path d="M476 162 L496 172 L484 180 L506 192" fill="none" stroke="#E08A2C" stroke-width="4" stroke-linejoin="round"/></g>',
         T(250, 58, mix='전기뱀장어', size=21, weight=700),
         '<line x1="300" y1="196" x2="276" y2="164" stroke="#5B6B7F" stroke-width="2"/>' + T(300, 220, mix='몸속 전기 기관', size=19, fill=MUTED)]
    return ''.join(o)
F['EEL'] = eel()

def eel2():
    o = []
    for k in range(5):
        x = 30 + k * 84
        o.append(f'<rect x="{x}" y="50" width="70" height="86" rx="10" fill="#F5EFE0" stroke="#8DAA7E" stroke-width="2.5"/>')
        o.append(f'<line x1="{x+6}" y1="58" x2="{x+6}" y2="128" stroke="{PLUS}" stroke-width="4"/>')
        o.append(f'<g data-anim="move" data-from="-18,0" data-dur="1.2" data-delay="{k*.15:.2f}" data-rep="loop" data-ease="lin"><g data-arw="{x+10},93,{x+40},93,plus,3"></g></g>')
    o.append(T(65, 34, tex=r'\ce{Na+}', size=19, fill=PLUS))
    o.append(T(470, 100, mix='…', size=30, weight=700))
    o.append('<path d="M30 150 V162 H520 V150" fill="none" stroke="#5B6B7F" stroke-width="2.5"/>')
    o.append(T(30, 186, mix='세포 하나 약 0.15 V', size=19, weight=700, anchor='start'))
    o.append(T(390, 186, mix='수천 개 직렬 연결', size=19, weight=700))
    return ''.join(o)
F['EEL2'] = eel2()

# ── 미래 전지 조건 아이콘
def icon(kind):
    if kind == 'den':
        return ('<rect x="30" y="20" width="90" height="56" rx="8" fill="#FFFFFF" stroke="#16233D" stroke-width="3"/><rect x="120" y="36" width="10" height="24" rx="2" fill="#16233D"/>'
                '<path d="M80 26 L62 50 H76 L68 70 L92 44 H78 Z" fill="#F2C230" stroke="#B8860B" stroke-width="2"/>')
    if kind == 'safe':
        return ('<path d="M80 12 L118 26 V48 Q118 74 80 88 Q42 74 42 48 V26 Z" fill="#E3EEFB" stroke="#1F6FD1" stroke-width="3"/>'
                '<path d="M62 50 L76 64 L100 38" fill="none" stroke="#1F6FD1" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == 'res':
        return ('<path d="M24 84 L46 50 L66 62 L84 34 L110 58 L136 84 Z" fill="#C9CED6" stroke="#5B6B7F" stroke-width="3" stroke-linejoin="round"/>'
                '<circle cx="62" cy="72" r="6" fill="#E6C29C"/><circle cx="96" cy="66" r="6" fill="#C9D3DD"/><circle cx="114" cy="76" r="5" fill="#8C8F94"/>')
    if kind == 'env':
        o = ''
        for k in range(3):
            a0 = k * 120 - 80
            x1, y1 = 80 + 30 * math.cos(math.radians(a0)), 52 + 30 * math.sin(math.radians(a0))
            x2, y2 = 80 + 30 * math.cos(math.radians(a0 + 80)), 52 + 30 * math.sin(math.radians(a0 + 80))
            o += f'<path d="M{x1:.1f} {y1:.1f} A30 30 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{FIELD}" stroke-width="6" stroke-linecap="round"/>'
            ax, ay = 80 + 30 * math.cos(math.radians(a0 + 96)), 52 + 30 * math.sin(math.radians(a0 + 96))
            o += f'<g data-arw="{x2:.1f},{y2:.1f},{ax:.1f},{ay:.1f},field,6"></g>'
        return o
    if kind == 'life':
        return ('<circle cx="80" cy="50" r="34" fill="#FFFFFF" stroke="#16233D" stroke-width="3"/><line x1="80" y1="50" x2="80" y2="28" stroke="#16233D" stroke-width="4" stroke-linecap="round"/>'
                '<line x1="80" y1="50" x2="98" y2="58" stroke="#16233D" stroke-width="4" stroke-linecap="round"/><circle cx="80" cy="50" r="4" fill="#16233D"/>')
for k in ['den', 'safe', 'res', 'env', 'life']:
    F['IC_' + k.upper()] = f'<g data-anim="pop" data-o="80,50" data-dur=".8" data-on="step">{icon(k)}</g>'

# ── 디지털 소양: 제련 전력량 막대 (조사 예시)
def bars():
    o = ['<line x1="150" y1="20" x2="150" y2="140" stroke="#5B6B7F" stroke-width="2"/>']
    o.append(T(140, 56, mix='알루미늄', size=20, anchor='end') + T(140, 116, mix='구리(정제)', size=20, anchor='end'))
    o.append('<g data-anim="scale" data-from="0,1" data-o="150,50" data-dur="1.4"><rect x="150" y="34" width="378" height="30" fill="#FDE7C2" stroke="#E08A2C" stroke-width="2"/></g>')
    o.append('<g data-anim="scale" data-from="0,1" data-o="150,110" data-dur="1.4"><rect x="150" y="94" width="11" height="30" fill="#FDE7C2" stroke="#E08A2C" stroke-width="2"/></g>')
    o.append(T(520, 84, mix='약 13–15 kWh', size=19, weight=700, anchor='end') + T(172, 116, mix='약 0.3–0.5 kWh', size=19, weight=700, anchor='start'))
    o.append(T(340, 162, mix='금속 1 kg을 얻는 데 드는 전력량 (조사 예시)', size=18, fill=MUTED))
    return ''.join(o)
F['BARS'] = bars()

# ── 탐구 결과 표: labs.js 모형과 같은 계산 (JS Math.round)
def jround(x): return math.floor(x + 0.5)
NEG = {'Zn': ('아연', -0.76, [3,4,4,4,2]), 'Mg': ('마그네슘', -2.37, [4,3,4,4,1]), 'Fe': ('철', -0.45, [2,5,5,5,4]), 'H2': ('수소', 0.00, [4,2,3,5,4])}
POS = {'O2': ('산소(공기)', 1.23, [5,4,5,5,3]), 'Cu': ('구리 이온', 0.34, [2,4,3,3,3]), 'Ag': ('은 이온', 0.80, [2,4,1,3,3])}
ELY = {'aq': ('수용액', [-1,1,1,1,0]), 'org': ('유기 액체', [0,-2,0,-1,0]), 'sol': ('고체', [1,2,-1,0,1])}
USE = {'ph': ('스마트폰', [2,2,3,1,1,2]), 'ev': ('전기 자동차', [2,3,3,1,1,2]), 'ess': ('전력 저장 장치', [1,1,3,3,2,2])}
def jhash(s):
    a = 7
    for c in s: a = (a * 31 + ord(c)) % 9973
    return a
def model(u, n, p, e, r):
    N, P, L = NEG[n], POS[p], ELY[e]
    E = P[1] - N[1]; Vm = E * (0.90 + (jhash(u+n+p+e+r) % 61) / 1000)
    s = [(N[2][k] + P[2][k]) / 2 + L[1][k] for k in range(5)]
    if r == 'y': s[3] += 1
    if n == 'Mg' and e == 'aq': s[1] -= 1
    vs = 5 if E >= 3 else 4 if E >= 2 else 3 if E >= 1.5 else 2 if E >= 1 else 1
    sc = [vs] + [max(1, min(5, jround(x))) for x in s]
    w = USE[u][1]; tot = jround(sum(a*b for a, b in zip(w, sc)) / (5 * sum(w)) * 100)
    return E, Vm, sc, tot, (sc[2] + sc[3] + sc[4]) / 3
DES = [('ph','Zn','O2','aq','n'), ('ev','Mg','O2','sol','y'), ('ess','Fe','O2','aq','y'), ('ess','Mg','O2','aq','n'), ('ph','Zn','Ag','org','n')]
rows = []
for i, d in enumerate(DES):
    E, Vm, sc, tot, sus = model(*d)
    rows.append(f'<tr><td>{"①②③④⑤"[i]}</td><td>{USE[d[0]][0]}</td><td>{NEG[d[1]][0]} / {POS[d[2]][0]}</td><td>{ELY[d[3]][0]}{" · 재활용" if d[4]=="y" else ""}</td><td>{E:.2f}</td>' + ''.join(f'<td>{v}</td>' for v in sc) + f'<td class="step" data-g="rs"><b>{tot}</b></td></tr>')
    print(d, round(E,2), round(Vm,2), sc, tot, round(sus,1))
for u in ('ph','ev','ess'): print('Fe-air', u, model(u,'Fe','O2','aq','y')[3])
F['RES'] = ''.join(rows)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tpl.html'), encoding='utf-8').read()
out = re.sub(r'@@([A-Z0-9_]+)@@', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('ok', len(out), out.count('<section'))
