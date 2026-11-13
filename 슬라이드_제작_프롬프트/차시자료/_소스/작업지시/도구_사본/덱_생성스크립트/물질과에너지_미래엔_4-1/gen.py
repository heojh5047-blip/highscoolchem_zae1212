# tpl.html 의 @@이름@@ 자리에 그림을 넣어 content/.../slides.html 을 만든다.
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/물질과에너지_미래엔/4-1_화학_반응_속도/slides.html'
F = {}

# ── S1 표지 ──
def cover():
    A = Axes(110, 400, 330, 250, (0, 1), (0, 1))
    r = lambda t: 0.88 * math.exp(-3.2 * t) + 0.04
    p = lambda t: 0.88 * (1 - math.exp(-3.2 * t)) + 0.04
    t0 = 0.22; c0 = r(t0); sl = -3.2 * 0.88 * math.exp(-3.2 * t0)
    o = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    o += A.frame(grid=False)
    o += tex(A.x0 + 10, A.Y(1) - 16, '농도', 22, 'start', INK)
    o += tex(A.X(1) + 22, A.y0 + 30, '시간', 22, 'end', INK)
    o += f'<path d="{A.path(r, 0, 1)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" data-anim="draw" data-dur="1.4" data-delay=".2"/>'
    o += f'<path d="{A.path(p, 0, 1)}" fill="none" stroke="{FIELD}" stroke-width="5" stroke-linecap="round" data-anim="draw" data-dur="1.4" data-delay=".4"/>'
    o += f'<g data-anim="fade" data-dur=".7" data-delay="1.7">' + A.line(t0 - 0.16, c0 - 0.16 * sl, t0 + 0.2, c0 + 0.2 * sl, PLUS, 4) + A.dot(t0, c0, PLUS, 7, '#fff') + '</g>'
    o += tex(A.X(0.62), A.Y(0.16) - 4, '반응물', 22, 'middle', INK)
    o += tex(A.X(0.66), A.Y(0.86) - 12, '생성물', 22, 'middle', FIELD)
    o += tex(A.X(0.47), A.Y(0.47), '접선', 22, 'start', PLUS)
    # 초시계
    cx, cy = 404, 150
    o += f'<g><rect x="{cx - 9}" y="{cy - 62}" width="18" height="14" rx="3" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="46" fill="#fff" stroke="{INK}" stroke-width="5"/>'
    for k in range(12):
        a = math.radians(k * 30)
        o += f'<line x1="{f(cx + 36 * math.sin(a))}" y1="{f(cy - 36 * math.cos(a))}" x2="{f(cx + 41 * math.sin(a))}" y2="{f(cy - 41 * math.cos(a))}" stroke="{MUTED}" stroke-width="2.5"/>'
    o += f'<g data-anim="spin" data-speed="60" data-o="{cx},{cy}"><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 32}" stroke="{PLUS}" stroke-width="4" stroke-linecap="round"/></g><circle cx="{cx}" cy="{cy}" r="5" fill="{INK}"/></g>'
    o += tex(270, 492, '농도–시간 그래프와 접선', 22, 'middle', MUTED)
    return o
F['cover'] = cover()

# ── S2 대단원 도입 그림 카드 ──
def fireworks():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#1E2A44"/>'
    for (cx, cy, col, n, L, d) in ((90, 70, '#F2C230', 14, 46, .2), (200, 58, '#E04A8B', 12, 40, .5), (230, 118, '#6EC1E4', 10, 30, .8)):
        rays = ''
        for k in range(n):
            a = 2 * math.pi * k / n
            rays += f'<line x1="{f(cx + 8 * math.cos(a))}" y1="{f(cy + 8 * math.sin(a))}" x2="{f(cx + L * math.cos(a))}" y2="{f(cy + L * math.sin(a))}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
            rays += f'<circle cx="{f(cx + (L + 6) * math.cos(a))}" cy="{f(cy + (L + 6) * math.sin(a))}" r="2.6" fill="{col}"/>'
        o += f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".7" data-delay="{d}" data-ease="back">{rays}</g>'
    o += '<path d="M60 166 Q 80 120 90 74" fill="none" stroke="#F2C230" stroke-width="2" stroke-dasharray="3 5" opacity=".6"/>'
    return o
def rust():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<rect x="20" y="60" width="260" height="50" rx="4" fill="#9AA5B1" stroke="#6B7785" stroke-width="2"/>'
    for x in range(40, 280, 40):
        o += f'<circle cx="{x}" cy="72" r="4" fill="#6B7785"/><circle cx="{x}" cy="98" r="4" fill="#6B7785"/>'
    o += '<rect x="20" y="110" width="20" height="50" fill="#9AA5B1" stroke="#6B7785" stroke-width="2"/><rect x="260" y="110" width="20" height="50" fill="#9AA5B1" stroke="#6B7785" stroke-width="2"/>'
    spots = ''
    for (x, y, rx, ry) in ((70, 84, 22, 12), (150, 78, 16, 9), (205, 92, 26, 13), (250, 80, 12, 8), (30, 136, 8, 14), (270, 140, 7, 12)):
        spots += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#A5452B" opacity=".75"/><ellipse cx="{x + 3}" cy="{y - 2}" rx="{rx * .5}" ry="{ry * .5}" fill="#C46A3C" opacity=".8"/>'
    o += f'<g data-anim="fade" data-dur="2.2" data-delay=".4">{spots}</g>'
    return o
def fridge():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<rect x="80" y="14" width="140" height="148" rx="10" fill="#fff" stroke="#7E8B98" stroke-width="3"/>'
    o += '<line x1="80" y1="62" x2="220" y2="62" stroke="#7E8B98" stroke-width="3"/><line x1="96" y1="110" x2="204" y2="110" stroke="#C9D3DD" stroke-width="3"/>'
    o += '<circle cx="122" cy="96" r="12" fill="#E5533D"/><path d="M122 84 q 3 -6 8 -6" stroke="#3FA36B" stroke-width="3" fill="none"/>'
    o += '<path d="M150 104 h40 q -4 -18 -20 -18 q -16 0 -20 18 z" fill="#F2C230"/>'
    o += '<rect x="112" y="122" width="34" height="32" rx="4" fill="#DDEEF8" stroke="#9FC3DD" stroke-width="2"/><rect x="160" y="128" width="30" height="26" rx="4" fill="#E7A15E"/>'
    sf = ''
    for k in range(3):
        a = math.radians(60 * k)
        sf += f'<line x1="{f(150 - 14 * math.cos(a))}" y1="{f(38 - 14 * math.sin(a))}" x2="{f(150 + 14 * math.cos(a))}" y2="{f(38 + 14 * math.sin(a))}" stroke="{MINUS}" stroke-width="3" stroke-linecap="round"/>'
    o += f'<g data-anim="spin" data-speed="25" data-o="150,38">{sf}</g>'
    o += tex(250, 98, '4\\ {}^\\circ\\text{C}', 20, 'middle', MINUS, mix=False)
    return o
F['fire'] = fireworks(); F['rust'] = rust(); F['fridge'] = fridge()

# ── S5 생각 열기 카드 (240×150) ──
def tube(x, y, h=110, w=40, liq=0.55, fill=WATER, edge=WATER_E):
    ly = y + h * (1 - liq)
    o = f'<path d="M{x} {f(ly)} V{f(y + h - w / 2)} a{w / 2} {w / 2} 0 0 0 {w} 0 V{f(ly)} z" fill="{fill}" stroke="none"/>'
    o += f'<line x1="{x}" y1="{f(ly)}" x2="{x + w}" y2="{f(ly)}" stroke="{edge}" stroke-width="2"/>'
    o += f'<path d="M{x} {y} V{f(y + h - w / 2)} a{w / 2} {w / 2} 0 0 0 {w} 0 V{y}" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    return o
def c_ppt():
    o = tube(100, 14, 116, 40, .62)
    o += '<g data-anim="fade" data-dur="1" data-delay=".3"><path d="M101 108 V112 a19 19 0 0 0 38 0 V108 q -19 -6 -38 0 z" fill="#F4F6F8" stroke="#C9D3DD" stroke-width="1.5"/>'
    for (x, y) in ((110, 70), (126, 80), (116, 92), (130, 98), (108, 100)):
        o += f'<circle cx="{x}" cy="{y}" r="2.5" fill="#C9D3DD"/>'
    o += '</g>'
    o += tex(190, 112, '흰색 앙금', 19, 'middle', MUTED)
    return o
def c_mg():
    o = tube(100, 14, 116, 40, .7)
    o += '<rect x="112" y="76" width="6" height="46" rx="2" fill="#9AA5B1" transform="rotate(14 115 100)"/>'
    for k, (x, d) in enumerate(((116, .0), (124, .5), (110, 1.0), (128, 1.4))):
        o += f'<g data-anim="move" data-from="0,40" data-dur="1.6" data-delay="{d}" data-rep="loop" data-ease="lin"><circle cx="{x}" cy="{56 - k * 3}" r="4" fill="#fff" stroke="{MINUS}" stroke-width="1.5"/></g>'
    o += tex(190, 112, '기체 발생', 19, 'middle', MUTED)
    return o
def c_nail():
    o = '<path d="M30 74 h150 l26 6 -26 6 h-150 z" fill="#9AA5B1" stroke="#6B7785" stroke-width="2"/><rect x="18" y="58" width="14" height="44" rx="3" fill="#8C99A6" stroke="#6B7785" stroke-width="2"/>'
    spots = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="5" fill="#A5452B" opacity=".8"/>' for (x, y, rx) in ((60, 76, 12), (98, 82, 9), (136, 76, 14), (168, 80, 7)))
    o += f'<g data-anim="fade" data-dur="2" data-delay=".3">{spots}</g>'
    o += tex(120, 128, '붉은 녹', 19, 'middle', MUTED)
    return o
def c_cave():
    o = '<path d="M4 4 H236 V40 Q 200 52 170 40 Q 140 30 110 44 Q 70 56 40 40 Q 20 34 4 42 Z" fill="#B9A8A0"/>'
    for (x, L) in ((44, 60), (78, 36), (122, 74), (160, 46), (200, 58)):
        o += f'<path d="M{x - 9} 40 L{x} {40 + L} L{x + 9} 40 Z" fill="#D8CBBE" stroke="#A89584" stroke-width="1.5"/>'
    for (x, L) in ((60, 22), (124, 30), (196, 18)):
        o += f'<path d="M{x - 10} 146 L{x} {146 - L} L{x + 10} 146 Z" fill="#D8CBBE" stroke="#A89584" stroke-width="1.5"/>'
    o += '<rect x="4" y="144" width="232" height="6" fill="#B9A8A0"/>'
    return o
F['c_ppt'] = c_ppt(); F['c_mg'] = c_mg(); F['c_nail'] = c_nail(); F['c_cave'] = c_cave()

# ── S6 연결: 자동차와 비커 ──
def car(x, y, dashed=False):
    st = ' stroke-dasharray="5 4" fill-opacity=".25"' if dashed else ''
    return (f'<g{" opacity=.5" if dashed else ""}><path d="M{x} {y} h96 v-22 l-20 -18 h-46 l-18 18 h-12 z" fill="#4F6BD8" stroke="{INK}" stroke-width="2"{st}/>'
            f'<circle cx="{x + 22}" cy="{y + 2}" r="11" fill="#3A3F47"/><circle cx="{x + 74}" cy="{y + 2}" r="11" fill="#3A3F47"/></g>')
def s6_car():
    o = '<rect x="0" y="118" width="520" height="16" fill="#C9D3DD"/>'
    o += car(30, 110, True)
    o += f'<g data-anim="move" data-from="-300,0" data-dur="1.6" data-delay=".3" data-ease="out">{car(330, 110)}</g>'
    o += '<g data-arw="78,56,378,56,muted,2.5"></g><line x1="78" y1="46" x2="78" y2="66" stroke="#5B6B7F" stroke-width="2.5"/>'
    o += tex(228, 42, '이동 거리', 20, 'middle', MUTED)
    o += tex(78, 166, 't_1', 22, 'middle', INK, mix=False) + tex(378, 166, 't_2', 22, 'middle', INK, mix=False)
    return o
def beaker(x, y, w=120, h=120, liq=.7, fill=WATER, edge=WATER_E):
    ly = y + h * (1 - liq)
    o = f'<rect x="{x + 2}" y="{f(ly)}" width="{w - 4}" height="{f(y + h - ly - 2)}" fill="{fill}"/>'
    o += f'<line x1="{x + 2}" y1="{f(ly)}" x2="{x + w - 2}" y2="{f(ly)}" stroke="{edge}" stroke-width="2"/>'
    o += f'<path d="M{x - 6} {y} q 6 0 6 6 V{y + h - 6} q 0 6 6 6 H{x + w - 6} q 6 0 6 -6 V{y + 6} q 0 -6 6 -6" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    return o
def s6_beak():
    import random
    rnd = random.Random(7)
    o = ''
    pts = [(rnd.uniform(14, 106), rnd.uniform(52, 132)) for _ in range(16)]
    for i, (bx, n) in enumerate(((40, 16), (330, 6))):
        o += beaker(bx, 20)
        for (px, py) in pts[:n]:
            o += f'<circle cx="{f(bx + px)}" cy="{f(py)}" r="6" fill="#3A4A66"/>'
    o += '<g data-arw="196,90,300,90,ink,3"></g>'
    o += tex(100, 172, 't_1', 22, 'middle', INK, mix=False) + tex(390, 172, 't_2', 22, 'middle', INK, mix=False)
    o += tex(248, 76, '농도 감소', 20, 'middle', MUTED)
    return o
F['s6_car'] = s6_car(); F['s6_beak'] = s6_beak()

# ── S7 입자 상자 (H2O2 분해) ──
def s7_boxes():
    slots = [(50, 58), (125, 52), (200, 62), (272, 54), (52, 150), (128, 156), (204, 146), (276, 154)]
    rots = [10, -25, 40, -10, -35, 15, -5, 30]
    boxes = [
        ('처음', ['p'] * 6 + [None, None]),
        ('조금 지난 뒤', ['p', 'p', 'w', 'p', 'o', 'p', 'w', None]),
        ('더 지난 뒤', ['w', 'o', 'w', 'p', 'w', 'o', 'w', 'p']),
    ]
    counts = ['$\\ce{H2O2}$ 6', '$\\ce{H2O2}$ 4, $\\ce{H2O}$ 2, $\\ce{O2}$ 1', '$\\ce{H2O2}$ 2, $\\ce{H2O}$ 4, $\\ce{O2}$ 2']
    o = ''
    for i, (name, kinds) in enumerate(boxes):
        bx = 15 + i * 370
        o += f'<rect x="{bx}" y="8" width="320" height="200" rx="12" fill="#fff" stroke="#9FB0C2" stroke-width="2.5"/>'
        prod = ''
        for (sx, sy), r, k in zip(slots, rots, kinds):
            x, y = bx + sx, 8 + sy
            if k == 'p': o += h2o2(x, y, r)
            elif k == 'w': prod += h2o(x, y, r)
            elif k == 'o': prod += o2(x, y, r)
        if prod:
            o += f'<g data-anim="pop" data-dur=".8" data-delay="{.3 + .5 * i}" data-ease="back" data-o="{bx + 160},108">{prod}</g>'
        o += tex(bx + 160, 238, name, 21, 'middle', INK)
        o += tex(bx + 160, 268, counts[i], 19, 'middle', MUTED)
        if i < 2:
            o += f'<g data-arw="{bx + 328},108,{bx + 362},108,ink,3"></g>'
    return o
F['s7'] = s7_boxes()

# ── S8 계수와 변화량 막대 ──
def s8_bars():
    o = ''
    rows = [('$\\ce{H2O2}$ 감소', 240, INK, '0.020\\ \\text{mol/L}'), ('$\\ce{H2O}$ 생성', 240, FIELD, '0.020\\ \\text{mol/L}'), ('$\\ce{O2}$ 생성', 120, FIELD, '0.010\\ \\text{mol/L}')]
    for i, (lab, L, col, val) in enumerate(rows):
        y = 34 + i * 58
        o += tex(130, y + 8, lab, 21, 'end', INK)
        o += f'<g data-anim="scale" data-from="0,1" data-o="146,{y}" data-dur="1" data-delay="{.3 + .25 * i}" data-ease="out"><rect x="146" y="{y - 16}" width="{L}" height="32" rx="5" fill="{col}" fill-opacity=".85"/></g>'
        o += tex(146 + L + 12, y + 8, val, 21, 'start', col, mix=False)
    o += f'<line x1="146" y1="4" x2="146" y2="176" stroke="{MUTED}" stroke-width="2"/>'
    return o
F['s8'] = s8_bars()

# ── S10 측정 방법 아이콘 (260×150) ──
def flask(x, y, w=90, h=100, neck=24, liq=.35, fill=WATER, edge=WATER_E):
    # 삼각 플라스크: 목 (x+w/2±neck/2, y..y+30), 몸통 아래 너비 w
    cx = x + w / 2; nb = y + 34
    ly = y + h - (h - 34) * liq * 1.6
    lw = (ly - nb) / (y + h - nb) * (w / 2 - neck / 2) + neck / 2
    o = f'<path d="M{f(cx - lw)} {f(ly)} L{x + 2} {y + h - 2} H{x + w - 2} L{f(cx + lw)} {f(ly)} Z" fill="{fill}"/>'
    o += f'<line x1="{f(cx - lw)}" y1="{f(ly)}" x2="{f(cx + lw)}" y2="{f(ly)}" stroke="{edge}" stroke-width="2"/>'
    o += f'<path d="M{f(cx - neck / 2)} {y} V{nb} L{x} {y + h} H{x + w} L{f(cx + neck / 2)} {nb} V{y}" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>'
    return o
def bubbles(pts, d0=0.0, dist=30, dur=1.5):
    o = ''
    for k, (x, y) in enumerate(pts):
        o += f'<g data-anim="move" data-from="0,{dist}" data-dur="{dur}" data-delay="{f(d0 + .4 * k)}" data-rep="loop" data-ease="lin"><circle cx="{x}" cy="{y}" r="4" fill="#fff" stroke="{MINUS}" stroke-width="1.5"/></g>'
    return o
def m_gas():
    o = flask(20, 30, 90, 104)
    o += '<rect x="56" y="22" width="18" height="12" rx="2" fill="#5B6B7F"/>'
    o += '<path d="M65 22 V12 H150" fill="none" stroke="#7E8B98" stroke-width="4"/>'
    o += '<rect x="150" y="2" width="96" height="20" rx="3" fill="#fff" stroke="#7E8B98" stroke-width="2.5"/>'
    o += '<g data-anim="move" data-from="-50,0" data-dur="2" data-delay=".3" data-ease="out"><rect x="190" y="4" width="6" height="16" fill="#5B6B7F"/><line x1="196" y1="12" x2="250" y2="12" stroke="#5B6B7F" stroke-width="4"/></g>'
    for k in range(1, 8):
        o += f'<line x1="{150 + 12 * k}" y1="22" x2="{150 + 12 * k}" y2="{16 if k % 2 else 13}" stroke="{MUTED}" stroke-width="1.5"/>'
    o += '<rect x="40" y="122" width="22" height="5" rx="2" fill="#9AA5B1"/>'
    o += bubbles([(52, 112), (62, 104), (46, 118)], dist=26)
    o += tex(186, 62, '기체 부피·압력', 21, 'middle', MUTED)
    return o
def m_mass():
    o = flask(80, 4, 90, 100, liq=.35)
    o += '<path d="M115 4 q10 -8 20 0 v6 h-20 z" fill="#F4F6F8" stroke="#C9D3DD" stroke-width="2"/>'
    for (x, y) in ((100, 96), (114, 98), (128, 95), (142, 97), (108, 92)):
        o += f'<rect x="{x}" y="{y}" width="9" height="7" rx="2" fill="#F4F6F8" stroke="#9AA5B1" stroke-width="1.2"/>'
    o += '<rect x="40" y="104" width="170" height="16" rx="4" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><rect x="30" y="120" width="190" height="26" rx="5" fill="#5B6B7F"/>'
    o += '<rect x="122" y="122" width="94" height="22" rx="3" fill="#E6F4EA"/>'
    o += tex(169, 141, '120.00', 20, 'middle', INK, mix=False, extra=' data-audit="skip"')
    return o
def m_color():
    o = f'<rect x="30" y="24" width="140" height="90" rx="10" fill="#B5562A" fill-opacity=".55" stroke="{GLASS}" stroke-width="3"/>'
    o += '<rect x="186" y="44" width="54" height="50" rx="6" fill="#5B6B7F"/><circle cx="186" cy="69" r="8" fill="#F2C230"/>'
    o += '<path d="M240 69 h12" stroke="#5B6B7F" stroke-width="4"/>'
    o += tex(100, 140, '적갈색 진하기', 19, 'middle', MUTED)
    return o
def m_ppt():
    o = '<rect x="40" y="118" width="170" height="24" fill="#fff" stroke="#C9D3DD" stroke-width="2"/>'
    o += '<path d="M112 122 L138 140 M138 122 L112 140" stroke="#16233D" stroke-width="4" stroke-linecap="round"/>'
    o += beaker(70, 20, 110, 96, .8, fill='#F3E9B5', edge='#D9C77A')
    o += '<g data-anim="fade" data-dur="2" data-delay=".4"><rect x="72" y="41" width="106" height="73" fill="#EFE3A2" opacity=".85"/></g>'
    return o
F['m_gas'] = m_gas(); F['m_mass'] = m_mass(); F['m_color'] = m_color(); F['m_ppt'] = m_ppt()

# ── S11·S12·S14 과산화 수소 농도–시간 ──
cH = lambda t: 0.8 ** (t / 100)
DATA = [(0, 1.00), (100, 0.80), (200, 0.64), (300, 0.51), (400, 0.41)]
def h2o2_axes(x0=86, y0=286, w=420, h=240):
    return Axes(x0, y0, w, h, (0, 400), (0, 1.0))
def h2o2_base(A, anim=True, ts=18):
    o = A.frame(xt=[0, 100, 200, 300, 400], yt=[0, .2, .4, .6, .8, 1.0], xl='$t$ [s]', yl='$[\\ce{H2O2}]$ [mol/L]', yfmt=lambda v: f'{v:.1f}', ts=ts)
    an = ' data-anim="draw" data-dur="1.4" data-delay=".2"' if anim else ''
    o += f'<path d="{A.path(cH, 0, 400)}" fill="none" stroke="{INK}" stroke-width="3.5"{an}/>'
    for (t, c) in DATA:
        o += A.dot(t, c, INK, 5, '#fff')
    return o
def s11():
    A = h2o2_axes()
    o = h2o2_base(A)
    for i in range(4):
        (t1, c1), (t2, c2) = DATA[i], DATA[i + 1]
        o += f'<g class="step" data-g="a{i + 1}">' + A.line(t1, c1, t2, c2, MUTED, 3, '7 5') + '</g>'
    return o
F['s11'] = s11()
def s12():
    A = h2o2_axes()
    o = h2o2_base(A, anim=False)
    k = math.log(1.25) / 100
    s = -k * 0.64
    o += '<g class="step" data-g="b0">' + A.line(0, 0.64 - 200 * s, 380, 0.64 + 180 * s, PLUS, 3.5, extra=' data-anim="draw" data-dur=".9" data-on="step"') + A.dot(200, 0.64, PLUS, 6, PLUS)
    o += A.dot(0, 0.93, PLUS, 5, '#fff') + A.dot(300, 0.50, PLUS, 5, '#fff')
    o += tex(A.X(0) + 14, A.Y(0.93) + 28, '(0, 0.93)', 18, 'start', PLUS, halo=True)
    o += tex(A.X(300) + 10, A.Y(0.50) - 14, '(300, 0.50)', 18, 'start', PLUS, halo=True)
    o += '</g>'
    s0 = -k
    o += '<g class="step" data-g="b2">' + A.line(0, 1.0, 380, 1.0 + 380 * s0, PLUS, 3, '9 6') + A.dot(300, 0.33, PLUS, 5, '#fff')
    o += tex(A.X(300) - 12, A.Y(0.33) + 30, '(300, 0.33)', 18, 'middle', PLUS, halo=True) + '</g>'
    return o
F['s12'] = s12()
def s14():
    A = Axes(70, 230, 330, 190, (0, 400), (0, 1.0))
    o = A.frame(xt=[0, 100, 200, 300, 400], yt=[0, .2, .4, .6, .8, 1.0], xl='$t$ [s]', yl='$[\\ce{H2O2}]$ [mol/L]', yfmt=lambda v: f'{v:.1f}')
    o += f'<path d="{A.path(cH, 0, 400)}" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    for (t, c) in DATA[:3]:
        o += A.dot(t, c, INK, 5, '#fff')
    for i in range(2):
        (t1, c1), (t2, c2) = DATA[i], DATA[i + 1]
        o += A.line(t1, c1, t2, c2, MUTED, 3, '7 5')
    return o
F['s14'] = s14()

# ── S16 차수별 v–[A] ──
def s16(kind):
    A = Axes(40, 166, 200, 126, (0, 1), (0, 1))
    o = A.frame(grid=False, xl='$[\\ce{A}]$', yl='$v$')
    fn = {0: lambda x: 0.45, 1: lambda x: 0.95 * x, 2: lambda x: 0.95 * x * x}[kind]
    o += f'<path d="{A.path(fn, 0, 1)}" fill="none" stroke="{INK}" stroke-width="3.5" data-anim="draw" data-dur="1" data-delay="{.3 + .3 * kind}"/>'
    for x in (0.45, 0.9):
        o += f'<line x1="{f(A.X(x))}" y1="{f(A.y0)}" x2="{f(A.X(x))}" y2="{f(A.Y(fn(x)))}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>' + A.dot(x, fn(x), PLUS, 5, PLUS)
    o += tex(A.X(.45), A.y0 + 24, 'c', 18, 'middle', MUTED, mix=False) + tex(A.X(.9), A.y0 + 24, '2c', 18, 'middle', MUTED, mix=False)
    return o
F['o0'] = s16(0); F['o1'] = s16(1); F['o2'] = s16(2)

# ── S23 탐구 과정 아이콘 ──
def p1():
    o = flask(70, 26, 100, 110, liq=.0)
    for (x, y) in ((92, 126), (106, 128), (120, 125), (134, 127), (148, 126), (100, 120)):
        o += f'<rect x="{x}" y="{y}" width="9" height="7" rx="2" fill="#F4F6F8" stroke="#9AA5B1" stroke-width="1.2"/>'
    o += tube(118, 52, 74, 18, .6)
    o += '<rect x="106" y="16" width="28" height="14" rx="3" fill="#5B6B7F"/><path d="M120 16 V6 H200 V24" fill="none" stroke="#16233D" stroke-width="3"/>'
    o += '<rect x="186" y="24" width="56" height="34" rx="6" fill="#16233D"/><rect x="192" y="30" width="44" height="14" rx="2" fill="#9BD86F"/>'
    o += tex(214, 80, '압력 센서', 18, 'middle', MUTED)
    return o
def p2():
    o = f'<g transform="rotate(-24 120 90)">' + flask(70, 26, 100, 110, liq=.32) + '<rect x="106" y="16" width="28" height="14" rx="3" fill="#5B6B7F"/></g>'
    o += bubbles([(118, 118), (132, 112), (106, 122)], dist=22)
    o += tex(214, 40, '10 s마다', 18, 'middle', MUTED) + tex(214, 64, '기록', 18, 'middle', MUTED)
    return o
def p3():
    o = ''
    for i, c in enumerate(('0.50', '1.00', '1.50', '2.00')):
        x = 12 + i * 62
        o += beaker(x + 6, 40, 46, 70, .6)
        o += tex(x + 29, 138, c, 21, 'middle', INK, mix=False)
    o += tex(130, 26, '[\\ce{HCl}]_0\\ (\\text{M})', 21, 'middle', MUTED, mix=False)
    return o
def p4():
    A = Axes(44, 116, 180, 80, (0, 300), (0, 1))
    o = A.frame(grid=False, xl='$t$', yl='$P$', ls=18)
    fn = lambda t: 1 - math.exp(-t / 100)
    o += f'<path d="{A.path(fn, 0, 300)}" fill="none" stroke="{INK}" stroke-width="3"/>'
    o += A.line(0, 0, 110, 1.1, PLUS, 3) + A.dot(0, 0, PLUS, 5, PLUS)
    return o
F['p1'] = p1(); F['p2'] = p2(); F['p3'] = p3(); F['p4'] = p4()

# ── S27 시간 눈금 띠 ──
def s27_scale():
    x0, x1, y = 40, 1060, 70
    lo, hi = -15, 12
    X = lambda e: x0 + (e - lo) / (hi - lo) * (x1 - x0)
    o = f'<defs><linearGradient id="grad-em41-27" x1="0" x2="1"><stop offset="0" stop-color="#FDE2E4"/><stop offset="1" stroke-color="#E3EEFB" stop-color="#E3EEFB"/></linearGradient></defs>'
    o += f'<rect x="{x0}" y="{y - 12}" width="{x1 - x0}" height="24" rx="12" fill="url(#grad-em41-27)" stroke="#C9D3DD" stroke-width="1.5"/>'
    for e in range(lo, hi + 1, 3):
        o += f'<line x1="{f(X(e))}" y1="{y + 12}" x2="{f(X(e))}" y2="{y + 20}" stroke="{MUTED}" stroke-width="2"/>'
        o += tex(X(e), y + 42, f'10^{{{e}}}', 18, 'middle', MUTED, mix=False)
    o += tex(x1, y + 74, '시간 [s]', 18, 'end', MUTED)
    marks = [(-14, '결합이 끊어짐', 1), (-3, '앙금 생성', 0), (2, '마그네슘 + 염산', 1), (7, '철의 녹', 0), (11, '종유석', 1)]
    for (e, lab, up) in marks:
        x = X(e)
        o += f'<circle cx="{f(x)}" cy="{y}" r="7" fill="{PLUS if e == -14 else INK}"/>'
        if up:
            o += f'<line x1="{f(x)}" y1="{y - 12}" x2="{f(x)}" y2="{y - 28}" stroke="{MUTED}" stroke-width="1.5"/>' + tex(x, y - 34, lab, 19, 'middle', INK)
        else:
            o += f'<line x1="{f(x)}" y1="{y + 12}" x2="{f(x)}" y2="{y + 52}" stroke="{MUTED}" stroke-width="1.5"/>' + tex(x, y + 76, lab, 19, 'middle', INK)
    return o
def s27_pulse():
    def pulse(cx, cy, col):
        d = 'M' + ' L'.join(f'{f(cx + u)} {f(cy - 22 * math.exp(-(u / 14) ** 2) * math.cos(u / 3.2))}' for u in range(-40, 41, 2))
        return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3"/>'
    o = f'<line x1="20" y1="90" x2="300" y2="90" stroke="#C9D3DD" stroke-width="2" stroke-dasharray="6 5"/>'
    o += f'<g data-anim="move" data-from="-120,0" data-dur="1.4" data-delay=".3" data-ease="out">{pulse(210, 90, EQUI)}</g>'
    o += f'<g data-anim="move" data-from="-120,0" data-dur="1.4" data-delay=".7" data-ease="out">{pulse(100, 90, MINUS)}</g>'
    o += tex(210, 44, '반응 시작 펄스', 18, 'middle', EQUI) + tex(100, 140, '관찰 펄스', 18, 'middle', MINUS)
    o += '<g data-arw="112,160,198,160,muted,2"></g><g data-arw="198,160,112,160,muted,2"></g>'
    o += tex(155, 186, '\\Delta t', 20, 'middle', MUTED, mix=False)
    o += atom(352, 90, 20, 'I', '-') + atom(392, 90, 20, 'I', '-')
    o += f'<line x1="300" y1="90" x2="326" y2="90" stroke="#C9D3DD" stroke-width="2" stroke-dasharray="6 5"/>'
    o += tex(372, 140, '분자', 18, 'middle', MUTED)
    return o
F['s27a'] = s27_scale(); F['s27b'] = s27_pulse()

# ── S29 확인 문제 01 그래프 ──
def catmull(pts, n=12):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t ** 3) for k in (0, 1)))
    out.append(pts[-1])
    return out
def s29():
    A = Axes(80, 260, 400, 210, (0, 60), (0, 0.8))
    o = A.frame(xt=[0, 20, 40, 60], yt=[0, .2, .4, .6, .8], xl='$t$ [s]', yl='$[\\ce{A}]$ [mol/L]', yfmt=lambda v: f'{v:.1f}')
    pts = [(0, .8), (20, .5), (40, .3), (60, .2)]
    cur = catmull(pts)
    o += '<path d="M' + ' L'.join(f'{f(A.X(x))} {f(A.Y(y))}' for x, y in cur) + f'" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    for (t, c) in pts:
        o += A.dot(t, c, INK, 5, '#fff')
        o += f'<line x1="{f(A.x0)}" y1="{f(A.Y(c))}" x2="{f(A.X(t))}" y2="{f(A.Y(c))}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 4"/>'
    o += tex(A.X(20) + 10, A.Y(.5) - 10, '0.50', 18, 'start', INK, mix=False, halo=True) + tex(A.X(40) + 10, A.Y(.3) - 10, '0.30', 18, 'start', INK, mix=False, halo=True)
    o += tex(A.X(0) + 14, A.Y(.8) + 24, '0.80', 18, 'start', INK, mix=False, halo=True) + tex(A.X(60) - 6, A.Y(.2) - 14, '0.20', 18, 'middle', INK, mix=False, halo=True)
    return o
F['s29'] = s29()

exec(open(os.path.join(HERE, 'gen_add.py'), encoding='utf-8').read())
tpl = open(os.path.join(HERE, 'tpl.html'), encoding='utf-8').read()
def rep(m):
    k = m.group(1)
    if k not in F: raise KeyError(k)
    return F[k]
html = re.sub(r'@@(\w+)@@', rep, tpl)
open(OUT, 'w', encoding='utf-8').write(html)
print('slides.html', len(html))
