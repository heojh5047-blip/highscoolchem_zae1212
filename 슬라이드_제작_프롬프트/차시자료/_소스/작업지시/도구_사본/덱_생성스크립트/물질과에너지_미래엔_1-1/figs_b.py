# 1-1b 그림
import math, random
from figs import *

F = {}

def wballoon(cx, cy, r, payload=True):
    s = f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(r)}" ry="{f(r * 1.08)}" fill="#FFFFFF" stroke="#8C99A6" stroke-width="2.5"/>'
    s += f'<ellipse cx="{f(cx - r * .35)}" cy="{f(cy - r * .4)}" rx="{f(r * .18)}" ry="{f(r * .28)}" fill="#EEF3F8"/>'
    return s

def cover():
    b = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    b += '<path d="M40 440 Q140 410 270 430 T500 430 L500 520 L40 520 Z" fill="#DDE8D5" opacity=".8"/>'
    # 처음 크기(점선)
    b += f'<ellipse cx="270" cy="230" rx="70" ry="76" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="7 6"/>'
    big = wballoon(270, 200, 150)
    pts = particles(150, 80, 240, 230, 14, 10, seed=5)
    pts = [p for p in pts if ((p[0] - 270) / 135) ** 2 + ((p[1] - 200) / 150) ** 2 < 1]
    b += f'<g data-anim="scale" data-from=".47" data-o="270,365" data-dur="2.2" data-delay=".4" data-ease="out">{big}{gas(pts, 10, 4, .6)}</g>'
    b += f'<path d="M270 362 V420" stroke="{MUTED}" stroke-width="2"/><rect x="254" y="420" width="32" height="26" rx="3" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>'
    b += tex(270, 488, '기상 관측 풍선', 22, fill=MUTED, mix=True)
    return svg(540, 540, b, label='기상 관측 풍선이 높이 올라가며 크게 부푼 모습과 지상에서의 처음 크기(점선)', cls='cover-fig', extra='data-audit="skip"').replace('style="width:540px" ', '')
F['COVER'] = cover()

def airbag():
    b = f'<circle cx="110" cy="150" r="70" fill="none" stroke="#5B6B7F" stroke-width="12"/><circle cx="110" cy="150" r="20" fill="#5B6B7F"/>'
    b += f'<path d="M110 150 L60 200 M110 150 L160 200" stroke="#5B6B7F" stroke-width="8"/>'
    pts = particles(150, 50, 240, 200, 14, 9, seed=9)
    pts = [p for p in pts if ((p[0] - 270) / 115) ** 2 + ((p[1] - 150) / 95) ** 2 < 1]
    bag = f'<ellipse cx="270" cy="150" rx="125" ry="105" fill="#F4F6F8" stroke="#8C99A6" stroke-width="2.5"/>' + gas(pts, 9, 4, .5)
    b += f'<g data-anim="scale" data-from=".15,.3" data-o="150,150" data-dur=".9" data-delay=".5" data-ease="out">{bag}</g>'
    b += tex(270, 290, '에어백 속 질소 기체', 20, fill=MUTED, mix=True)
    return svg(420, 300, b, 400, '자동차 운전대에서 에어백이 순식간에 부풀고 그 안에 질소 기체 분자가 가득 찬 모습')
F['AIRBAG'] = airbag()

def ideal_real():
    b = f'<rect x="10" y="10" width="260" height="200" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
    pts = particles(14, 14, 252, 192, 12, 10, seed=31)
    s = ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.5" fill="{GAS_E}"/>' for x, y in pts)
    b += f'<g data-anim="move" data-from="5,-3" data-rep="swing" data-dur=".6">{s}</g>'
    b += tex(140, 244, '(가) 이상 기체', 21, weight='700', mix=True)
    b += tex(140, 270, '분자 부피 0, 분자 사이 힘 없음', 19, fill=MUTED, mix=True)
    x0 = 310
    b += f'<rect x="{x0}" y="10" width="260" height="200" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
    pts = particles(x0 + 4, 14, 252, 192, 22, 13, seed=32)
    ln = ''
    for i, (a, c) in enumerate(pts):
        for (d, e) in pts[i + 1:]:
            if 0 < math.hypot(a - d, c - e) < 46:
                ln += line(a, c, d, e, MUTED, 1.6, '3 4')
    b += ln + gas(pts, 13, 1.5, .8)
    b += tex(x0 + 130, 244, '(나) 실제 기체 (높은 압력)', 21, weight='700', mix=True)
    b += tex(x0 + 130, 270, '분자의 크기, 분자 사이 인력(점선)', 19, fill=MUTED, mix=True)
    return svg(580, 280, b, 560, '이상 기체는 크기가 없는 점 입자로 서로 힘을 미치지 않고, 높은 압력의 실제 기체는 분자가 크기를 가지며 분자 사이에 인력이 작용하는 모습')
F['IDEAL'] = ideal_real()

def three():
    b = ''
    for i, (lab, m, n) in enumerate([('(가) $\\ce{He}$ 4.0 g', '', 6), ('(나) $\\ce{O2}$ 32 g', '', 6), ('(다) $\\ce{CH4}$ 8.0 g', '', 3)]):
        x0 = 10 + i * 190
        b += f'<rect x="{x0}" y="10" width="170" height="150" rx="8" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
        b += gas(particles(x0 + 6, 16, 158, 138, n, 10, seed=60 + i), 10, 4, .6 + .1 * i)
        b += tex(x0 + 85, 192, lab, 20, mix=True)
    return svg(580, 205, b, 540, '같은 온도에서 부피가 같은 세 용기에 헬륨 4.0 g, 산소 32 g, 메테인 8.0 g이 들어 있고 분자 수 비가 2 대 2 대 1인 입자 모형')
F['THREE'] = three()

def hotair():
    b = f'<rect x="10" y="10" width="400" height="270" fill="{COLD}"/>'
    env = 'M210 40 C300 40 330 120 290 180 L250 222 H170 L130 180 C90 120 120 40 210 40 Z'
    out = particles(14, 14, 392, 262, 40, 8, seed=71)
    import re
    def inside(x, y):
        return ((x - 210) / 95) ** 2 + ((y - 130) / 105) ** 2 < 1.15
    outp = [p for p in out if not inside(*p)]
    b += gas(outp, 8, 3, .7)
    b += f'<path d="{env}" fill="{HOT}" stroke="{PLUS}" stroke-width="2.5"/>'
    inp = [p for p in particles(140, 55, 140, 150, 8, 8, seed=72) if inside(*p)]
    b += gas(inp, 8, 5, .45)
    b += f'<path d="M180 222 L190 250 H230 L240 222" fill="none" stroke="{MUTED}" stroke-width="2"/><rect x="190" y="250" width="40" height="22" fill="#C9A35A"/>'
    b += tex(210, 132, '뜨거운 공기', 20, mix=True, halo=True) + tex(350, 40, '바깥 공기', 20, mix=True, halo=True)
    return svg(420, 290, b, 400, '열기구 안의 뜨거운 공기는 분자가 드물고 바깥의 차가운 공기는 분자가 촘촘한 모습')
F['HOTAIR'] = hotair()

# ── 탐구 과정 카드
def balance(txt):
    b = f'<rect x="40" y="130" width="180" height="40" rx="6" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>'
    b += f'<rect x="60" y="138" width="100" height="26" rx="3" fill="#16233D"/>' + tex(110, 159, txt, 20, fill='#9BE7A8', mix=True)
    b += f'<rect x="60" y="118" width="140" height="10" rx="3" fill="#B7C2CE" stroke="{GLASS}" stroke-width="1.5"/>'
    b += f'<rect x="112" y="58" width="36" height="60" rx="6" fill="#F09A3E" stroke="#B0661A" stroke-width="2"/><rect x="118" y="44" width="24" height="14" fill="#8C99A6"/>'
    return b
F['P1'] = svg(260, 180, balance('25.43 g'), 220, '전자저울 위의 부탄가스 라이터, 25.43 g')
def trough(bubbles=True, level=True):
    b = f'<rect x="20" y="100" width="220" height="70" fill="{WATER}"/>'
    b += f'<path d="M14 80 V176 H246 V80" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    # 거꾸로 세운 눈금실린더
    lv = 60 if level else 40
    b += f'<rect x="110" y="{lv}" width="40" height="{150 - lv}" fill="{WATER}"/>'
    b += f'<rect x="110" y="12" width="40" height="{lv - 12}" fill="#F7F9FB"/>'
    b += f'<path d="M110 160 V12 H150 V160" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    for k in range(5):
        b += line(110, 26 + k * 24, 122, 26 + k * 24, MUTED, 1.5)
    if bubbles:
        b += f'<rect x="168" y="120" width="22" height="40" rx="4" fill="#F09A3E" stroke="#B0661A" stroke-width="2" transform="rotate(-25 179 140)"/>'
        bb = ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="#fff" stroke="{WATER_E}" stroke-width="1.5"/>' for x, y in [(160, 120), (148, 140), (138, 150), (130, 128)])
        b += f'<g data-anim="move" data-from="20,30" data-rep="loop" data-dur="1.4" data-ease="lin">{bb}</g>'
    else:
        b += line(60, 100, 200, 100, PLUS, 2, '6 4') + tex(56, 96, '높이 맞춤', 18, 'end', fill=PLUS, mix=True) if False else ''
    return b
F['P2'] = svg(260, 180, trough(True), 220, '물을 채워 거꾸로 세운 눈금실린더 아래에서 물속의 라이터 버튼을 눌러 기체를 모으는 수상 치환')
def level():
    b = f'<rect x="20" y="100" width="220" height="70" fill="{WATER}"/>'
    b += f'<path d="M14 80 V176 H246 V80" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<rect x="110" y="100" width="40" height="60" fill="{WATER}"/><rect x="110" y="12" width="40" height="88" fill="#F7F9FB"/>'
    b += f'<path d="M110 172 V12 H150 V172" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    for k in range(5):
        b += line(110, 26 + k * 24, 122, 26 + k * 24, MUTED, 1.5)
    b += line(30, 100, 236, 100, PLUS, 2, '6 4')
    b += tex(64, 90, '수면 높이', 21, fill=PLUS, mix=True) + tex(206, 90, '같게', 21, fill=PLUS, mix=True)
    return b
F['P3'] = svg(260, 180, level(), 220, '눈금실린더를 내려 안팎의 수면 높이를 맞춘 뒤 부피를 읽는 모습')
def p4():
    b = balance('25.20 g')
    b += f'<rect x="230" y="20" width="12" height="120" rx="6" fill="#fff" stroke="{GLASS}" stroke-width="2"/><rect x="233" y="70" width="6" height="70" fill="{PLUS}"/><circle cx="236" cy="148" r="10" fill="{PLUS}"/>'
    return b
F['P4'] = svg(260, 180, p4(), 220, '물기를 닦은 라이터의 나중 질량 25.20 g과 물의 온도를 재는 온도계')

# ── 에어백 반응 입자 모형
def react():
    b = ''
    Na, N = 24, 18
    def nan3(x, y):
        return (f'<g data-atom="{x},{y},{Na},Na"></g>' + ''.join(f'<g data-atom="{x + 46 + k * 30},{y},{N},N"></g>' for k in range(3)))
    b += nan3(40, 60) + nan3(40, 150)
    b += arw(250, 105, 320, 105, 'ink', 3.5)
    prod = f'<g data-atom="370,60,{Na},Na"></g><g data-atom="370,150,{Na},Na"></g>'
    n2 = ''
    for (x, y) in [(450, 50), (560, 105), (450, 160)]:
        n2 += f'<g data-atom="{x},{y},{N},N"></g><g data-atom="{x + 30},{y},{N},N"></g>'
    b += f'<g data-anim="move" data-from="-60,0" data-dur="1.2" data-delay=".5" data-ease="out">{prod}</g>'
    b += f'<g data-anim="move" data-from="-130,0" data-dur="1.4" data-delay=".5" data-ease="out">{n2}</g>'
    b += tex(115, 218, '$\\ce{2NaN3}$ (Na 2개, N 6개)', 20, mix=True)
    b += tex(470, 218, '$\\ce{2Na}$ + $\\ce{3N2}$ (Na 2개, N 6개)', 20, mix=True)
    return svg(660, 232, b, 640, '아자이드화 나트륨 2개가 나트륨 원자 2개와 질소 분자 3개로 분해되며 나트륨 2개와 질소 원자 6개가 보존되는 입자 모형')
F['REACT'] = react()

def wb():
    b = f'<rect x="10" y="10" width="420" height="300" fill="#F3F7FB"/>'
    b += '<path d="M10 280 Q120 262 220 278 T430 276 V310 H10 Z" fill="#DDE8D5"/>'
    b += wballoon(90, 225, 32) + f'<path d="M90 260 V278" stroke="{MUTED}" stroke-width="2"/>'
    b += tex(90, 302, '지상', 19, mix=True)
    b += f'<ellipse cx="300" cy="112" rx="32" ry="34.6" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>'
    b += f'<g data-anim="scale" data-from=".55" data-o="300,180" data-dur="1.8" data-delay=".4" data-ease="out">{wballoon(300, 105, 66)}</g>'
    b += f'<path d="M300 177 V200" stroke="{MUTED}" stroke-width="2"/>'
    b += tex(300, 228, '약 10 km 높이', 19, mix=True)
    b += f'<g data-arw="140,240,240,150,muted,2.5,d"></g>'
    return svg(440, 320, b, 400, '지상의 작은 기상 관측 풍선이 약 10 km 높이에서 약 세 배 부피로 커진 모습, 점선은 지상 크기')
F['WB'] = wb()

def q2():
    b = ''
    for i, (lab, m) in enumerate([('(가)', '$\\ce{O2}$ 1.6 g'), ('(나)', '기체 $\\mathrm{X}$ 2.2 g')]):
        x0 = 20 + i * 220
        b += f'<rect x="{x0}" y="20" width="180" height="140" rx="8" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
        b += gas(particles(x0 + 6, 26, 168, 128, 5, 10, seed=80 + i), 10, 3, .6 + .1 * i)
        b += tex(x0 + 90, 190, f'{lab} {m}', 20, mix=True)
    return svg(440, 205, b, 420, '같은 온도와 압력에서 부피가 같은 두 용기에 산소 1.6 g과 기체 X 2.2 g이 들어 있는 모습')
F['Q2'] = q2()

# ═══ 교과서 대조 후 교체: 휴대용 기체 통 탐구, 타이어, 장난감 ═══
def can(x, y, lab='용기 1', s=1.0):
    return (f'<rect x="{x}" y="{y}" width="{36 * s}" height="{70 * s}" rx="{8 * s}" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>'
            f'<rect x="{x + 6 * s}" y="{y + 22 * s}" width="{24 * s}" height="{26 * s}" fill="#fff" stroke="{GLASS}" stroke-width="1.2"/>'
            f'<rect x="{x + 12 * s}" y="{y - 12 * s}" width="{12 * s}" height="{12 * s}" fill="#8C99A6"/>' + tex(x + 18 * s, y + 42 * s, '?', 22))
def bal2(txt):
    b = f'<rect x="40" y="130" width="180" height="40" rx="6" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>'
    b += f'<rect x="60" y="138" width="100" height="26" rx="3" fill="#16233D"/>' + tex(110, 159, txt, 20, fill='#9BE7A8', mix=True)
    b += f'<rect x="60" y="118" width="140" height="10" rx="3" fill="#B7C2CE" stroke="{GLASS}" stroke-width="1.5"/>'
    return b + can(112, 46)
F['P1'] = svg(260, 180, bal2('처음 질량'), 220, '전자저울로 상표를 가린 기체 통의 처음 질량을 잰다')
def trough2():
    b = f'<rect x="60" y="100" width="190" height="70" fill="{WATER}"/>'
    b += f'<path d="M54 80 V176 H256 V80" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<rect x="150" y="56" width="44" height="104" fill="{WATER}"/><rect x="150" y="12" width="44" height="44" fill="#F7F9FB"/>'
    b += f'<path d="M150 162 V12 H194 V162" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    for k in range(5): b += line(150, 26 + k * 24, 162, 26 + k * 24, MUTED, 1.5)
    b += can(8, 70, s=.8)
    b += f'<path d="M23 60 Q30 30 80 40 Q120 50 120 120 Q120 168 172 166" fill="none" stroke="#B0661A" stroke-width="4"/>'
    bb = ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="#fff" stroke="{WATER_E}" stroke-width="1.5"/>' for x, y in [(172, 150), (168, 128), (176, 108), (170, 86)])
    b += f'<g data-anim="move" data-from="0,40" data-rep="loop" data-dur="1.4" data-ease="lin">{bb}</g>'
    b += tex(100, 30, '고무관', 21, mix=True)
    return b
F['P2'] = svg(260, 180, trough2(), 220, '기체 통에 연결한 고무관으로 물을 채워 거꾸로 세운 눈금실린더에 기체를 모으는 수상 치환')
F['P4'] = svg(260, 180, bal2('나중 질량') + f'<rect x="230" y="20" width="12" height="120" rx="6" fill="#fff" stroke="{GLASS}" stroke-width="2"/><rect x="233" y="70" width="6" height="70" fill="{PLUS}"/><circle cx="236" cy="148" r="10" fill="{PLUS}"/>', 220, '기체 통의 나중 질량과 실험실 온도를 잰다')

def tire(case):
    b = (f'<rect x="0" y="0" width="210" height="210" rx="14" fill="{COLD}"/>' if case == 'T' else '')
    b += f'<circle cx="110" cy="110" r="86" fill="#3A3F47"/><circle cx="110" cy="110" r="50" fill="#C9D3DD" stroke="{GLASS}" stroke-width="3"/><circle cx="110" cy="110" r="10" fill="{MUTED}"/>'
    if case == 'T': b += tex(30, 30, '❄', 22, mix=True)
    pts = [(110 + 68 * math.cos(a), 110 + 68 * math.sin(a)) for a in [i * math.pi / 5 for i in range(10)]]
    keep = pts if case == 'T' else pts[::2]
    b += ''.join(dot(x, y, 7) for x, y in keep)
    if case == 'n':
        b += '<path d="M180 160 l20 14 M186 150 l22 8" stroke="#F09A3E" stroke-width="3" stroke-linecap="round"/>'
    b += f'<rect x="218" y="70" width="80" height="80" rx="12" fill="#FFF6D6" stroke="#E9C93A" stroke-width="2"/>'
    b += f'<path d="M258 86 L282 132 H234 Z" fill="none" stroke="#C2410C" stroke-width="4" stroke-linejoin="round"/>' + tex(258, 128, '!', 22, fill='#C2410C')
    b += tex(258, 172, '경고등', 18, mix=True)
    return svg(310, 210, b, 290, '타이어 속 공기 분자 모형과 타이어 공기압 경고등')
F['TIRE_N'] = tire('n')
F['TIRE_T'] = tire('T')

def toy():
    b = f'<ellipse cx="120" cy="230" rx="44" ry="40" fill="#EAF2FB" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<ellipse cx="120" cy="60" rx="34" ry="32" fill="#EAF2FB" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<path d="M114 92 V250 M126 92 V250" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<path d="M92 76 Q120 98 148 76 Q150 60 140 48 Q120 60 100 48 Q90 60 92 76 Z" fill="#E04A8B" opacity=".85"/>'
    b += f'<rect x="115" y="100" width="10" height="150" fill="#E04A8B" opacity=".85"/>'
    b += f'<path d="M78 236 Q120 274 162 236 L162 244 Q120 272 78 244 Z" fill="#E04A8B" opacity=".85"/>'
    b += f'<path d="M66 214 Q50 250 80 276 Q120 296 160 276 Q190 250 174 214" fill="none" stroke="#F2C9A5" stroke-width="14" stroke-linecap="round" opacity=".9"/>'
    b += tex(220, 240, '손으로 감싸면', 19, 'start', mix=True) + arw(212, 200, 212, 90, 'plus', 3) + tex(220, 150, '액체가 위로', 19, 'start', mix=True)
    return svg(340, 300, b, 300, '아래쪽 유리 구를 손으로 감싸면 액체가 관을 따라 위쪽 유리 구로 이동하는 장난감')
F['TOY'] = toy()

def pvnt_flow():
    return ''
