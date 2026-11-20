# 1-1a 그림
import math, random
from figs import *

F = {}

# ── S1 표지: 실린더 + P V T n
def cover():
    b = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    x, y, w, h = 175, 150, 190, 290
    b += cylinder(x, y, w, h, .72, 16, seed=11, r=10, amp=5, dur=.65)
    top = y + h - h * .72
    b += arw(270, top - 118, 270, top - 62, 'ink', 4)
    b += tex(292, top - 92, 'P', 30, 'start')
    b += tex(316, top - 92, '압력', 22, 'start', fill=MUTED, mix=True)
    # V 치수선
    b += line(392, top, 392, y + h, MUTED, 2) + line(384, top, 400, top, MUTED, 2) + line(384, y + h, 400, y + h, MUTED, 2)
    b += tex(408, (top + y + h) / 2 + 2, 'V', 30, 'start') + tex(408, (top + y + h) / 2 + 30, '부피', 22, 'start', fill=MUTED, mix=True)
    # T 온도계
    b += f'<rect x="118" y="240" width="16" height="150" rx="8" fill="#fff" stroke="{GLASS}" stroke-width="2"/><rect x="122" y="300" width="8" height="90" fill="{PLUS}"/><circle cx="126" cy="398" r="14" fill="{PLUS}" stroke="{GLASS}" stroke-width="2"/>'
    b += tex(126, 224, 'T', 30) + tex(82, 300, '온도', 22, 'middle', fill=MUTED, mix=True)
    b += tex(270, 488, 'n', 30, 'end') + tex(278, 488, '기체의 양(몰수)', 22, 'start', fill=MUTED, mix=True)
    return svg(540, 540, b, label='피스톤이 달린 실린더 속에서 기체 분자가 무질서하게 움직이고, 둘레에 압력, 부피, 온도, 몰수 표시', cls='cover-fig', extra='data-audit="skip"').replace('style="width:540px" ', '')
F['COVER'] = cover()

# ── S2 세 가지 상태
def states():
    b = ''
    W = 300
    for i, (name, kind) in enumerate([('기체', 'g'), ('액체', 'l'), ('고체', 's')]):
        x0 = 10 + i * (W + 20)
        b += f'<rect x="{x0}" y="10" width="{W}" height="190" rx="10" fill="#fff" stroke="{GLASS}" stroke-width="2"/>'
        if kind == 'g':
            pts = particles(x0 + 6, 16, W - 12, 178, 9, 13, seed=4)
            b += gas(pts, 13, 7, .6)
        elif kind == 'l':
            pts = particles(x0 + 4, 74, W - 8, 124, 30, 13, seed=8, pad=1, dense=True)
            b += gas(pts, 13, 2, 1.1)
        else:
            s = ''
            for r_ in range(4):
                for c in range(9):
                    s += dot(x0 + 30 + c * 30, 200 - 22 - r_ * 30, 13)
            b += f'<g data-anim="move" data-from="1.6,0" data-rep="swing" data-dur=".18">{s}</g>'
        b += tex(x0 + W / 2, 236, name, 24, weight='700', mix=True)
    return svg(960, 250, b, 700, '기체는 입자 사이가 멀고 자유롭게 움직이며, 액체는 입자가 붙어서 무질서하게 움직이고, 고체는 입자가 규칙적으로 배열하여 제자리에서 진동하는 입자 모형')
F['STATES'] = states()

# ── S5 과자 봉지
def bag(cx, cy, w, h):
    return (f'<path d="M{f(cx - w / 2)} {f(cy - h / 2)} Q{f(cx)} {f(cy - h / 2 - h * .18)} {f(cx + w / 2)} {f(cy - h / 2)} '
            f'Q{f(cx + w / 2 + w * .14)} {f(cy)} {f(cx + w / 2)} {f(cy + h / 2)} Q{f(cx)} {f(cy + h / 2 + h * .18)} {f(cx - w / 2)} {f(cy + h / 2)} '
            f'Q{f(cx - w / 2 - w * .14)} {f(cy)} {f(cx - w / 2)} {f(cy - h / 2)} Z" fill="#FCE9B8" stroke="#C99A2E" stroke-width="3"/>'
            f'<path d="M{f(cx - w / 2)} {f(cy - h / 2)} H{f(cx + w / 2)} M{f(cx - w / 2)} {f(cy + h / 2)} H{f(cx + w / 2)}" stroke="#C99A2E" stroke-width="5" stroke-dasharray="3 4"/>')
def snack():
    b = '<path d="M300 210 L420 60 L470 120 L520 70 L600 210 Z" fill="#E7EEF5" stroke="#B9C6D3" stroke-width="2"/>'
    b += bag(120, 140, 120, 70)
    b += tex(120, 222, '평지', 22, mix=True) + tex(120, 248, '(약 1 기압)', 19, fill=MUTED, mix=True)
    b += arw(200, 140, 290, 140, 'ink', 3)
    b += f'<g data-anim="scale" data-from=".72" data-o="460,150" data-dur="1.6" data-delay=".5" data-ease="out">{bag(460, 150, 150, 100)}</g>'
    b += tex(460, 236, '산 정상', 22, mix=True) + tex(460, 262, '(약 0.7 기압)', 19, fill=MUTED, mix=True)
    return svg(600, 272, b, 520, '평지에서 납작하던 과자 봉지가 산 정상에서 크게 부푼 모습')
F['SNACK'] = snack()

# ── S7 기체의 압력: 상자 + 토리첼리
def pressure():
    b = f'<rect x="10" y="20" width="270" height="220" fill="#fff" stroke="{GLASS}" stroke-width="3"/>'
    pts = particles(14, 24, 262, 212, 13, 10, seed=21)
    b += gas(pts, 10, 5, .6, vel=18, vseed=3)
    # 벽 충돌 표시
    for (x, y, dx, dy) in [(280, 70, 1, 0), (280, 180, 1, 0), (10, 120, -1, 0), (140, 20, 0, -1), (200, 240, 0, 1), (60, 240, 0, 1)]:
        b += f'<g data-arw="{f(x - dx * 4)},{f(y - dy * 4)},{f(x + dx * 26)},{f(y + dy * 26)},plus,3"></g>'
    b += tex(145, 290, '(가) 분자가 벽에 충돌하여 미는 힘', 20, mix=True)
    # 토리첼리
    ox = 420
    b += f'<rect x="{ox - 80}" y="210" width="160" height="40" fill="#C3CBD3" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<path d="M{ox - 86} 180 V252 H{ox + 86} V180" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    b += f'<rect x="{ox - 14}" y="20" width="28" height="226" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
    b += f'<rect x="{ox - 11}" y="64" width="22" height="180" fill="#A9B4BF"/>'
    b += tex(ox + 2, 50, '진공', 18, 'middle', fill=MUTED, mix=True, halo=True)
    b += line(ox + 34, 64, ox + 34, 210, MUTED, 2) + line(ox + 27, 64, ox + 41, 64, MUTED, 2) + line(ox + 27, 210, ox + 41, 210, MUTED, 2)
    b += tex(ox + 46, 144, '760 mm', 20, 'start', mix=True)
    b += arw(ox - 60, 150, ox - 60, 204, 'ink', 3) + arw(ox + 64, 160, ox + 64, 204, 'ink', 3)
    b += tex(ox - 66, 136, '대기압', 19, 'middle', mix=True)
    b += tex(ox, 290, '(나) 토리첼리의 실험', 20, mix=True)
    b += tex(ox, 316, '수은', 18, fill=MUTED, mix=True)
    return svg(560, 330, b, 540, '상자 속 기체 분자가 벽에 충돌하여 압력을 만드는 모습과, 대기압이 수은 기둥 760 mm를 떠받치는 토리첼리의 실험')
F['PRESSURE'] = pressure()

# ── 주사기
def syringe(x0, y0, L, gl, parts=0, seed=1, finger=True, push=False, anim=None):
    H = 54
    s = ''
    if parts:
        pts = particles(x0 + 2, y0 + 2, gl - 4, H - 4, parts, 7, seed, pad=1)
        s += f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(gl)}" height="{H}" fill="#F3F6FA"/>'
        s += ''.join(dot(a, b_, 7) for a, b_ in pts)
    pl = (f'<rect x="{f(x0 + gl)}" y="{f(y0 + 3)}" width="9" height="{H - 6}" fill="#8C99A6"/>'
          f'<rect x="{f(x0 + gl + 9)}" y="{f(y0 + H / 2 - 5)}" width="{f(L - gl + 26)}" height="10" fill="#C9D3DD" stroke="{GLASS}" stroke-width="1.5"/>'
          f'<rect x="{f(x0 + L + 35)}" y="{f(y0 - 6)}" width="9" height="{H + 12}" rx="3" fill="#B7C2CE" stroke="{GLASS}" stroke-width="1.5"/>')
    if push:
        pl += arw(x0 + L + 98, y0 + H / 2, x0 + L + 52, y0 + H / 2, 'ink', 3)
    if anim:
        pl = f'<g data-anim="move" data-from="{anim},0" data-dur="1.3" data-delay=".5" data-ease="out">{pl}</g>'
    s += pl
    s += f'<path d="M{f(x0 + L)} {f(y0 - 4)} V{f(y0)} H{f(x0)} V{f(y0 + H)} H{f(x0 + L)} V{f(y0 + H + 4)}" fill="none" stroke="{GLASS}" stroke-width="2.5"/>'
    s += f'<rect x="{f(x0 - 14)}" y="{f(y0 + H / 2 - 7)}" width="14" height="14" fill="#fff" stroke="{GLASS}" stroke-width="2"/>'
    if finger:
        s += f'<ellipse cx="{f(x0 - 22)}" cy="{f(y0 + H / 2)}" rx="12" ry="20" fill="#F2C9A5" stroke="#C99A6F" stroke-width="2"/>'
    for k in range(1, 6):
        xx = x0 + L * k / 6
        s += line(xx, y0, xx, y0 + 10, MUTED, 1.5)
    return s
def syr_stage(parts):
    b = syringe(40, 22, 190, 190, parts, 5) + syringe(40, 120, 190, 95, parts, 5, push=True, anim=0 if not parts else None)
    b += tex(250, 98, '처음', 19, 'end', fill=MUTED, mix=True) + tex(250, 196, '누름', 19, 'end', fill=MUTED, mix=True)
    return b
F['SYR1'] = svg(340, 210, syr_stage(0), 300, '끝을 막은 주사기의 피스톤을 누르기 전과 누른 뒤')
F['SYR2'] = svg(340, 210, syr_stage(12), 300, '피스톤을 누르기 전과 뒤 모두 주사기 속 기체 분자는 12개이고 누른 뒤에는 좁은 공간에 모여 있음')

# ── S9 보일 그래프
def boyle_graph():
    g = G(70, 320, 400, 270, (0, 5), (0, 13.5))
    b = g.axes([0, 1, 2, 3, 4], [0, 3, 6, 9, 12], '$P$ [atm]', '$V$ [L]')
    b += f'<g class="step" data-g="r1"><rect x="{f(g.X(0))}" y="{f(g.Y(6))}" width="{f(g.X(1) - g.X(0))}" height="{f(g.Y(0) - g.Y(6))}" fill="{FIELD}" fill-opacity=".16" stroke="{FIELD}" stroke-width="2"/>'
    b += f'<rect x="{f(g.X(0))}" y="{f(g.Y(2))}" width="{f(g.X(3) - g.X(0))}" height="{f(g.Y(0) - g.Y(2))}" fill="{EQUI}" fill-opacity=".14" stroke="{EQUI}" stroke-width="2"/>'
    b += tex(g.X(.5), g.Y(4.2), '6.0', 20, halo=True) + tex(g.X(2.2), g.Y(1) + 7, '6.0', 20, halo=True) + '</g>'
    b += g.curve(lambda p: 6 / p, .46, 4.4, extra='data-anim="draw" data-dur="1.4" data-delay=".3"')
    b += g.pts([(.5, 12), (1, 6), (2, 3), (3, 2), (4, 1.5)])
    return svg(520, 360, b, 470, '온도가 일정할 때 압력이 커질수록 부피가 작아지는 반비례 곡선과 측정점 다섯 개, 두 점의 압력과 부피를 곱한 직사각형 넓이가 같음')
F['BOYLEG'] = boyle_graph()

def mini(kind, w=300, h=220, lab=True, zero=True):
    g = G(46, h - 40, w - 90, h - 80, (0, 1), (0, 1))
    b = ''
    if kind == 'VP':
        b += g.axes([], [], '$P$', '$V$', grid=False)
        b += g.curve(lambda p: .16 / p, .17, 1)
    elif kind == 'V1P':
        b += g.axes([], [], '$\\dfrac{1}{P}$', '$V$', grid=False)
        b += g.curve(lambda p: .95 * p, 0, 1)
    elif kind == 'VT':
        b += g.axes([], [], '$T$', '$V$', grid=False)
        b += g.curve(lambda p: .9 * p, 0, 1)
    elif kind == 'Vn':
        b += g.axes([], [], '$n$', '$V$', grid=False)
        b += g.curve(lambda p: .9 * p, 0, 1)
    if zero: b += tex(g.ox - 10, g.oy + 24, '0', 18, 'end')
    return b
F['MINI_VP'] = svg(300, 220, mini('VP'), 280, '부피와 압력의 반비례 곡선')
F['MINI_V1P'] = svg(300, 220, mini('V1P'), 280, '부피와 압력의 역수가 원점을 지나는 직선')

# ── S11 입자 해석 카드
def boyle_card(vfrac, collide=False, anim=None):
    b = cylinder(80, 70, 140, 170, vfrac, 12, seed=33, r=9, amp=3 if vfrac > .6 else 2, dur=.55, piston_anim=anim)
    if collide:
        top = 70 + 170 - 170 * vfrac
        for (x, y) in [(80, top + 25), (80, top + 60), (220, top + 40), (220, top + 70)]:
            dx = -1 if x == 80 else 1
            b += f'<g data-arw="{x - dx * 2},{f(y)},{x + dx * 22},{f(y)},plus,3"></g>'
        b += f'<g data-arw="{150 - 40},{240 + 3},{150 - 40},{240 + 24},plus,3"></g><g data-arw="{150 + 30},{240 + 3},{150 + 30},{240 + 24},plus,3"></g>'
    return svg(300, 270, b, 260, '실린더 속 기체 분자 12개')
F['BC1'] = boyle_card(1.0)
F['BC2'] = boyle_card(.5, anim=-85)
F['BC3'] = boyle_card(.5, collide=True)

# ── S14 탁구공
def pingpong():
    b = ''
    # 왼쪽: 찌그러진 공
    b += '<path d="M140 70 A60 60 0 1 1 96 170 Q125 128 104 92 A60 60 0 0 1 140 70 Z" fill="#FFF7E6" stroke="#C9A35A" stroke-width="3"/>'
    b += tex(150, 236, '찌그러진 탁구공', 20, mix=True)
    b += arw(240, 130, 300, 130, 'ink', 3)
    # 오른쪽: 비커 + 뜨거운 물
    b += f'<rect x="330" y="96" width="220" height="114" fill="#FCE3E3" opacity=".8"/>'
    b += f'<path d="M322 40 V214 H558 V40" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    b += '<path d="M380 82 q8 -14 0 -28 q-8 -14 0 -28 M440 82 q8 -14 0 -28 q-8 -14 0 -28 M500 82 q8 -14 0 -28 q-8 -14 0 -28" fill="none" stroke="#C9A0A0" stroke-width="2.5" stroke-linecap="round"/>'
    b += '<g data-anim="scale" data-from=".78,1" data-o="440,140" data-dur="1.6" data-delay=".6" data-ease="out"><circle cx="440" cy="140" r="56" fill="#FFF7E6" stroke="#C9A35A" stroke-width="3"/></g>'
    b += tex(440, 246, '뜨거운 물에 넣으면 펴진다', 20, mix=True)
    return svg(580, 260, b, 540, '찌그러진 탁구공을 뜨거운 물에 넣으면 둥글게 펴지는 모습')
F['PING'] = pingpong()

# ── S15 샤를 V–t 그래프
def charles_graph():
    W, H = 600, 370
    x0, x1 = -300, 260
    ox_px, pw = 40, 520
    X = lambda t: ox_px + (t - x0) / (x1 - x0) * pw
    oy, ph = 300, 250
    Y = lambda v: oy - v / 5.6 * ph
    b = ''
    for t in [-273, -200, -100, 100, 200]:
        b += line(X(t), oy, X(t), oy - ph, '#E3E8EE', 1.2)
    for v in [1, 2, 3, 4, 5]:
        b += line(X(x0), Y(v), X(x1), Y(v), '#E3E8EE', 1.2)
    b += arw(X(x0), oy, X(x1) + 22, oy, 'muted', 2)
    b += arw(X(0), oy + .01, X(0), oy - ph - 22, 'muted', 2)
    for t in [-273, -200, -100, 100, 200]:
        b += line(X(t), oy, X(t), oy + 6, MUTED, 2) + tex(X(t), oy + 28, f'{t}'.replace('-', '-'), 18)
    b += tex(X(0) - 8, oy + 24, '0', 18, 'end')
    for v in [1, 2, 3, 4, 5]:
        b += line(X(0) - 6, Y(v), X(0), Y(v), MUTED, 2) + tex(X(0) - 10, Y(v) + 6, f'{v}', 18, 'end')
    b += tex(X(x1) + 20, oy + 52, '$t$ [°C]', 20, 'end', mix=True)
    b += tex(X(0) + 12, oy - ph - 14, '$V$ [L]', 20, 'start', mix=True)
    k = .01
    b += f'<line x1="{f(X(-273))}" y1="{f(Y(0))}" x2="{f(X(-73))}" y2="{f(Y(2))}" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="7 6" class="step" data-g="c1"/>'
    b += line(X(-73), Y(2), X(250), Y(5.23), INK, 3, extra='data-anim="draw" data-dur="1.2" data-delay=".3"')
    b += ''.join(f'<circle cx="{f(X(t))}" cy="{f(Y(k * (t + 273)))}" r="6" fill="{INK}"/>' for t in [-73, 0, 27, 127, 227])
    b += f'<g class="step" data-g="c1"><circle cx="{f(X(-273))}" cy="{f(Y(0))}" r="7" fill="#fff" stroke="{PLUS}" stroke-width="3"/>' + tex(X(-273) + 4, Y(0) - 22, '$-273$ °C', 20, 'start', fill=PLUS, mix=True, halo=True) + '</g>'
    return svg(W, H, b, 560, '압력이 일정할 때 기체의 부피가 섭씨 온도에 따라 직선으로 늘어나고, 그 직선을 연장하면 영하 273도에서 부피가 0이 되는 그래프')
F['CHARG'] = charles_graph()

# ── S16 온도 눈금 + V–T
def scales():
    b = ''
    top, bot = 56, 300
    Y = lambda T: bot - T / 400 * (bot - top)
    for x, lab in [(90, '°C'), (250, 'K')]:
        b += f'<rect x="{x - 10}" y="{top - 10}" width="20" height="{bot - top + 20}" rx="10" fill="#fff" stroke="{GLASS}" stroke-width="2"/>'
        b += tex(x, top - 18, lab, 22, mix=True, weight='700')
    for T, c in [(0, '-273'), (273, '0'), (373, '100')]:
        y = Y(T)
        b += line(80, y, 260, y, MUTED, 1.5, '4 4')
        b += tex(74, y + 6, c, 19, 'end') + tex(272, y + 6, str(T), 19, 'start')
    b += tex(170, Y(0) - 8, '절대 영도', 18, fill=PLUS, mix=True, halo=True)
    b += tex(170, Y(273) - 8, '물의 어는점', 18, fill=MUTED, mix=True, halo=True)
    b += tex(170, Y(373) - 8, '물의 끓는점', 18, fill=MUTED, mix=True, halo=True)
    return svg(330, 316, b, 300, '섭씨 온도 눈금과 절대 온도 눈금을 나란히 놓은 그림: 영하 273도는 0 K, 0도는 273 K, 25도는 298 K, 100도는 373 K')
F['SCALES'] = scales()
def vt_graph():
    g = G(60, 250, 300, 200, (0, 500), (0, 5.5))
    b = g.axes([0, 100, 200, 300, 400, 500], [0, 1, 2, 3, 4, 5], '$T$ [K]', '$V$ [L]', xfmt=lambda v: None if v in (100, 300, 500) else f(v))
    b += g.curve(lambda T: .01 * T, 0, 500, extra='data-anim="draw" data-dur="1.2" data-delay=".3"')
    b += g.pts([(200, 2), (273, 2.73), (300, 3), (400, 4), (500, 5)], 5)
    return svg(420, 300, b, 380, '압력이 일정할 때 기체의 부피와 절대 온도가 원점을 지나는 직선')
F['VTG'] = vt_graph()

# ── S17 저온·고온 실린더
def charles_cyl():
    b = cylinder(40, 90, 150, 200, .48, 10, seed=41, r=9, bg=COLD, amp=2, dur=.9, vel=14)
    b += tex(115, 330, '낮은 온도', 20, mix=True)
    b += arw(220, 230, 280, 230, 'ink', 3)
    b += f'<g data-anim="move" data-from="0,0" data-dur="1"></g>'
    b += cylinder(310, 90, 150, 200, .75, 10, seed=41, r=9, bg=HOT, amp=5, dur=.45, vel=28, piston_anim=54)
    b += tex(385, 330, '높은 온도', 20, mix=True)
    return svg(500, 345, b, 470, '같은 압력에서 온도를 높이면 분자 운동이 빨라지고 피스톤이 올라가 부피가 커지는 모습').replace('<g data-anim="move" data-from="0,0" data-dur="1"></g>', '')
F['CHCYL'] = charles_cyl()

# ── S20 세 기체 같은 분자 수
def avog_boxes():
    b = ''
    rnd = random.Random(7)
    for i, (name, kind) in enumerate([('\\ce{He}', 'He'), ('\\ce{N2}', 'N2'), ('\\ce{CO2}', 'CO2')]):
        x0 = 10 + i * 200
        b += f'<rect x="{x0}" y="10" width="180" height="170" rx="8" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
        pts = particles(x0 + 14, 20, 152, 150, 6, 22, seed=50 + i)
        s1, s2 = '', ''
        for k, (px, py) in enumerate(pts):
            a = rnd.uniform(0, math.pi)
            ca, sa = math.cos(a), math.sin(a)
            if kind == 'He':
                m = f'<g data-atom="{f(px)},{f(py)},9,He,-"></g>'
            elif kind == 'N2':
                m = f'<g data-atom="{f(px - 7 * ca)},{f(py - 7 * sa)},11,N,-"></g><g data-atom="{f(px + 7 * ca)},{f(py + 7 * sa)},11,N,-"></g>'
            else:
                m = f'<g data-atom="{f(px - 15 * ca)},{f(py - 15 * sa)},10,O,-"></g><g data-atom="{f(px + 15 * ca)},{f(py + 15 * sa)},10,O,-"></g><g data-atom="{f(px)},{f(py)},10,C,-"></g>'
            if k % 2: s1 += m
            else: s2 += m
        b += f'<g data-anim="move" data-from="4,-3" data-rep="swing" data-dur=".7">{s1}</g><g data-anim="move" data-from="-3,4" data-rep="swing" data-dur=".8">{s2}</g>'
        b += tex(x0 + 90, 212, f'${name}$ 분자 6개', 20, mix=True)
    return svg(600, 230, b, 560, '같은 온도와 압력에서 부피가 같은 세 용기에 헬륨 원자, 질소 분자, 이산화 탄소 분자가 각각 6개씩 들어 있는 모습')
F['AVOG'] = avog_boxes()
def balloon():
    b = '<g data-anim="scale" data-from=".7" data-o="110,190" data-dur="1.6" data-delay=".4" data-ease="out"><ellipse cx="110" cy="110" rx="70" ry="84" fill="#F7C6CF" stroke="#D7263D" stroke-width="2.5"/><path d="M104 194 L110 186 L116 194 Z" fill="#D7263D"/></g>'
    b += '<path d="M110 196 Q100 216 112 236" fill="none" stroke="#8C99A6" stroke-width="2"/>'
    b += '<ellipse cx="110" cy="122" rx="49" ry="59" fill="none" stroke="#D7263D" stroke-width="2" stroke-dasharray="6 5" opacity=".6"/>'
    b += tex(110, 268, '공기를 더 불어 넣으면', 19, mix=True)
    return svg(220, 280, b, 200, '풍선에 공기를 더 불어 넣으면 풍선이 커지는 모습, 점선은 처음 크기')
F['BALLOON'] = balloon()

def vn_graph():
    g = G(70, 280, 330, 220, (0, 2.6), (0, 50))
    b = g.axes([0, .5, 1, 1.5, 2], [0, 11.2, 22.4, 33.6, 44.8], '$n$ [mol]', '$V$ [L]', size=18)
    b += g.curve(lambda n: 22.4 * n, 0, 2.15, extra='data-anim="draw" data-dur="1.2" data-delay=".3"')
    b += g.pts([(.5, 11.2), (1, 22.4), (1.5, 33.6), (2, 44.8)])
    return svg(460, 330, b, 430, '0도, 1기압에서 기체의 부피가 몰수에 비례하는 직선, 1몰은 22.4 L')
F['VNG'] = vn_graph()

# ── S26 정리표 미니 그래프
F['M_VP'] = svg(210, 130, mini('VP', 210, 130, zero=False), 170, '반비례 곡선')
F['M_VT'] = svg(210, 130, mini('VT', 210, 130, zero=False), 170, '원점을 지나는 직선')
F['M_VN'] = svg(210, 130, mini('Vn', 210, 130, zero=False), 170, '원점을 지나는 직선')

# ── S27 확인 문제 01
def q1_graph():
    g = G(70, 300, 380, 250, (0, 4), (0, 8))
    b = g.axes([0, 1, 2, 3], [0, 2, 6], '$P$ [atm]', '$V$ [L]', xfmt=lambda v: None if v == 3 else f(v))
    b += g.curve(lambda p: 6 / p, .78, 3.8)
    for (p, v, lab) in [(1, 6, 'A'), (2, 3, 'B'), (3, 2, 'C')]:
        b += line(g.X(p), g.Y(v), g.X(p), g.Y(0), MUTED, 1.8, '5 5') + line(g.X(p), g.Y(v), g.X(0), g.Y(v), MUTED, 1.8, '5 5')
        b += f'<circle cx="{f(g.X(p))}" cy="{f(g.Y(v))}" r="6" fill="{INK}"/>' + tex(g.X(p) + 12, g.Y(v) - 12, f'\\mathrm{{{lab}}}', 22, 'start')
    b += tex(g.X(0) - 10, g.Y(3) + 7, '㉠', 20, 'end', mix=True) + tex(g.X(3), g.Y(0) + 27, '㉡', 20, mix=True)
    return svg(500, 350, b, 470, '일정한 온도에서 일정량의 기체의 부피와 압력 곡선 위의 세 점 A, B, C')
F['Q1G'] = q1_graph()

# ── S29 확인 문제 03
def q3_graph():
    g = G(70, 280, 360, 230, (0, 750), (0, 7))
    b = g.axes([0, 300, 600], [], '$T$ [K]', '$V$ [L]', grid=False)
    b += g.curve(lambda T: .01 * T, 0, 640) + g.curve(lambda T: .005 * T, 0, 660, c=EQUI)
    b += tex(g.X(560), g.Y(6.3), '(가)', 20, 'end', mix=True) + tex(g.X(660), g.Y(3.0) - 14, '(나)', 20, 'middle', mix=True, fill='#A65A10')
    b += line(g.X(300), g.Y(0), g.X(300), g.Y(3), MUTED, 1.6, '5 5') + line(g.X(600), g.Y(0), g.X(600), g.Y(6), MUTED, 1.6, '5 5')
    return svg(480, 330, b, 440, '같은 압력에서 기체 가와 나의 부피가 절대 온도에 비례하는 두 직선, 가의 기울기가 나의 두 배')
F['Q3G'] = q3_graph()

# ═══ 교과서 대조 후 추가·교체 그림 ═══
def steam():
    b = f'<rect x="20" y="90" width="150" height="110" rx="14" fill="#E9EDF2" stroke="{GLASS}" stroke-width="3"/>'
    b += f'<rect x="24" y="150" width="142" height="46" rx="8" fill="{WATER}"/>'
    b += ''.join(f'<path d="M{x} 236 q-12 -18 0 -30 q8 10 6 18 q10 -8 4 -22 q16 12 4 34 Z" fill="#F09A3E" stroke="#C2410C" stroke-width="1.5"/>' for x in (60, 95, 130))
    b += tex(95, 128, '물 → 수증기', 19, mix=True)
    b += f'<path d="M170 120 H250 V150" fill="none" stroke="{GLASS}" stroke-width="10"/>'
    b += cylinder(236, 150, 120, 120, .55, 7, seed=91, r=8, bg=HOT, amp=4, dur=.45, piston_anim=30).replace(f'<path d="M236 120', f'<path d="M236 120')
    b += arw(296, 130, 296, 70, 'ink', 4) + tex(312, 92, '피스톤을 민다', 19, 'start', mix=True)
    b += f'<circle cx="480" cy="150" r="70" fill="none" stroke="{MUTED}" stroke-width="6"/><circle cx="480" cy="150" r="10" fill="{MUTED}"/>'
    b += f'<g data-anim="spin" data-o="480,150" data-speed="60"><path d="M480 80 V220 M410 150 H550 M430 100 L530 200 M530 100 L430 200" stroke="{MUTED}" stroke-width="3"/></g>'
    b += line(296, 98, 420, 110, MUTED, 4) + tex(480, 250, '바퀴를 돌린다', 19, mix=True)
    return svg(570, 270, b, 540, '보일러에서 물을 끓여 만든 수증기가 실린더의 피스톤을 밀고, 그 움직임이 바퀴를 돌리는 증기 기관 모식도')
F['STEAM'] = steam()

def jtube(cx, gasH, dh, lab1, lab2):
    # J자 관: 왼쪽 짧은 막힌 관(기체), 오른쪽 긴 열린 관
    L, Rr, bot = cx - 40, cx + 40, 250
    b = f'<path d="M{L} 40 V{bot} Q{L} {bot + 30} {cx} {bot + 30} Q{Rr} {bot + 30} {Rr} {bot} V10" fill="none" stroke="{GLASS}" stroke-width="16" stroke-linecap="round"/>'
    b += f'<path d="M{L} 40 V{bot} Q{L} {bot + 30} {cx} {bot + 30} Q{Rr} {bot + 30} {Rr} {bot} V10" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round"/>'
    hg_left = 40 + gasH
    hg_right = hg_left - dh
    b += f'<path d="M{L} {hg_left} V{bot} Q{L} {bot + 30} {cx} {bot + 30} Q{Rr} {bot + 30} {Rr} {bot} V{hg_right}" fill="none" stroke="#A9B4BF" stroke-width="10"/>'
    b += f'<rect x="{L - 5}" y="36" width="10" height="{gasH + 4}" fill="#F6C9B0"/>'
    b += f'<line x1="{L - 9}" y1="36" x2="{L + 9}" y2="36" stroke="{GLASS}" stroke-width="4"/>'
    if dh:
        b += line(Rr + 18, hg_right, Rr + 18, hg_left, MUTED, 2) + line(Rr + 12, hg_right, Rr + 24, hg_right, MUTED, 2) + line(Rr + 12, hg_left, Rr + 24, hg_left, MUTED, 2)
        b += tex(Rr + 28, (hg_left + hg_right) / 2 + 6, '760 mm', 18, 'start', mix=True)
        b += line(L - 8, hg_left, Rr + 8, hg_left, MUTED, 1.5, '4 4')
    b += arw(Rr, 0 + 2, Rr, max(14, hg_right - 26), 'ink', 2.5) if False else ''
    b += tex(cx, 316, lab1, 19, mix=True) + tex(cx, 342, lab2, 19, mix=True)
    return b
def jtubes():
    b = jtube(90, 120, 0, '기체의 압력: 1 기압', '기체의 부피: $2V$')
    b += jtube(300, 60, 140, '기체의 압력: 2 기압', '기체의 부피: $V$')
    b += arw(170, 160, 220, 160, 'ink', 3) + tex(195, 146, '수은', 18, mix=True)
    return svg(450, 352, b, 430, '보일의 J자 관 실험: 막힌 쪽 기체가 1기압일 때 부피 2V, 수은을 더 넣어 수은 기둥 높이 차가 760 mm가 되면 2기압, 부피 V')
F['JTUBE'] = jtubes()

def boyle_rel():
    g = G(64, 270, 320, 220, (0, 5), (0, 1.25))
    b = g.axes([], [], '압력', '부피', grid=False)
    for p, lab in [(1, 'P'), (2, '2P'), (4, '4P')]:
        b += line(g.X(p), g.oy, g.X(p), g.oy + 6, MUTED, 2) + tex(g.X(p), g.oy + 26, lab, 19)
    for v, lab in [(1, 'V'), (.5, '\\tfrac{1}{2}V'), (.25, '\\tfrac{1}{4}V')]:
        b += line(g.ox - 6, g.Y(v), g.ox, g.Y(v), MUTED, 2) + tex(g.ox - 10, g.Y(v) + 7, lab, 19, 'end')
    b += tex(g.ox - 10, g.oy + 24, '0', 18, 'end')
    b += f'<g class="step" data-g="r1"><rect x="{f(g.X(0))}" y="{f(g.Y(1))}" width="{f(g.X(1) - g.X(0))}" height="{f(g.Y(0) - g.Y(1))}" fill="{FIELD}" fill-opacity=".16" stroke="{FIELD}" stroke-width="2"/>'
    b += f'<rect x="{f(g.X(0))}" y="{f(g.Y(.25))}" width="{f(g.X(4) - g.X(0))}" height="{f(g.Y(0) - g.Y(.25))}" fill="{EQUI}" fill-opacity=".14" stroke="{EQUI}" stroke-width="2"/></g>'
    b += g.curve(lambda p: 1 / p, .82, 4.8, extra='data-anim="draw" data-dur="1.4" data-delay=".3"')
    b += g.pts([(1, 1), (2, .5), (4, .25)])
    return svg(420, 310, b, 420, '일정한 온도에서 기체의 압력이 P, 2P, 4P일 때 부피가 V, 2분의 1 V, 4분의 1 V로 줄어드는 반비례 곡선')
F['BOYREL'] = boyle_rel()

def egg():
    b = '<ellipse cx="120" cy="130" rx="48" ry="62" fill="#FBF3E4" stroke="#C9A35A" stroke-width="3"/>'
    b += tex(120, 236, '냉장고에서 꺼낸 달걀', 19, mix=True)
    b += arw(190, 130, 250, 130, 'ink', 3)
    b += f'<rect x="276" y="90" width="230" height="120" fill="#FCE3E3" opacity=".85"/>'
    b += f'<path d="M268 40 V214 H514 V40" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    b += '<path d="M330 82 q8 -14 0 -28 q-8 -14 0 -28 M450 82 q8 -14 0 -28 q-8 -14 0 -28" fill="none" stroke="#C9A0A0" stroke-width="2.5" stroke-linecap="round"/>'
    b += '<ellipse cx="390" cy="148" rx="42" ry="54" fill="#FBF3E4" stroke="#C9A35A" stroke-width="3"/>'
    b += '<path d="M372 98 L384 116 L376 128 L392 142" fill="none" stroke="#7A5A20" stroke-width="2.5" data-anim="draw" data-dur=".8" data-delay="1"/>'
    b += '<g data-anim="move" data-from="0,24" data-rep="loop" data-dur="1.6" data-ease="lin"><circle cx="370" cy="96" r="4" fill="#fff" stroke="#9FC3DD" stroke-width="1.5"/><circle cx="380" cy="84" r="3" fill="#fff" stroke="#9FC3DD" stroke-width="1.5"/></g>'
    b += tex(390, 236, '뜨거운 물에 넣으면 깨진다', 19, mix=True)
    return svg(530, 250, b, 520, '냉장고에서 꺼낸 달걀을 바로 뜨거운 물에 넣으면 달걀 속 기체의 부피가 늘어나 껍데기가 깨지는 모습')
F['EGG'] = egg()

def tdata():
    W, H = 560, 340
    x0, x1 = -273, 380
    X = lambda t: 50 + (t - x0) / (x1 - x0) * 470
    oy, ph = 280, 230
    Y = lambda v: oy - v / 6.8 * ph
    b = ''
    for t in [-273, -182, -91, 91, 182, 273, 364]:
        b += line(X(t), oy, X(t), oy - ph, '#E3E8EE', 1.2)
    for v in [2, 4, 6]:
        b += line(X(x0), Y(v), X(x1), Y(v), '#E3E8EE', 1.2)
    b += arw(X(x0), oy, X(x1) + 18, oy, 'muted', 2) + arw(X(0), oy + .01, X(0), oy - ph - 20, 'muted', 2)
    for t in [-273, -182, -91, 91, 182, 273, 364]:
        b += line(X(t), oy, X(t), oy + 6, MUTED, 2) + tex(X(t), oy + 26, f'{t}', 18)
    b += tex(X(0) - 6, oy + 24, '0', 18, 'end')
    for v in [2, 4, 6]:
        b += line(X(0) - 6, Y(v), X(0), Y(v), MUTED, 2) + tex(X(0) - 10, Y(v) + 6, f'{v}V', 18, 'end')
    b += tex(X(x1) + 18, oy + 50, '온도 [°C]', 20, 'end', mix=True) + tex(X(0) + 12, oy - ph - 12, '부피(상댓값)', 20, 'start', mix=True)
    b += f'<g class="step" data-g="c0">' + line(X(0), Y(3), X(364), Y(7 * 0 + 3 + 364 / 91), INK, 3) + ''.join(f'<circle cx="{f(X(t))}" cy="{f(Y(3 + t / 91))}" r="6" fill="{INK}"/>' for t in [0, 91, 182, 273]) + '</g>'
    b += f'<g class="step" data-g="c1">' + line(X(-273), Y(0), X(0), Y(3), MUTED, 2.5, '7 6') + f'<circle cx="{f(X(-273))}" cy="{f(Y(0))}" r="7" fill="#fff" stroke="{PLUS}" stroke-width="3"/>' + tex(X(-273) + 6, Y(0) - 20, '$-273$ °C', 20, 'start', fill=PLUS, mix=True, halo=True) + '</g>'
    return svg(W, H, b, 540, '압력과 기체의 양이 일정할 때 온도 0, 91, 182, 273도에서 부피가 3V, 4V, 5V, 6V인 직선과, 연장하면 영하 273도에서 부피 0')
F['TDATA'] = tdata()

def vt_pair(kind):
    g = G(60, 210, 262, 175, (0, 4.2), (0, 3.6))
    b = g.axes([], [], '온도 [°C]' if kind == 'a' else '온도 [K]', '부피 [L]', grid=False)
    labs = ['-273', '0', '273', '546'] if kind == 'a' else ['0', '273', '546', '819']
    for i, lab in enumerate(labs):
        if kind == 'b' and i == 0: continue
        b += line(g.X(i), g.oy, g.X(i), g.oy + 6, MUTED, 2) + tex(g.X(i), g.oy + 26, lab, 18)
    for v in (1, 2, 3):
        b += line(g.ox - 6, g.Y(v), g.ox, g.Y(v), MUTED, 2) + tex(g.ox - 10, g.Y(v) + 7, ('' if v == 1 else str(v)) + 'V_0', 18, 'end')
    if kind == 'b':
        b += tex(g.ox - 10, g.oy + 24, '0', 18, 'end')
        b += line(g.X(0), g.Y(0), g.X(3.2), g.Y(3.2), INK, 3, extra='data-anim="draw" data-dur="1.2" data-delay=".3"')
    else:
        b += line(g.X(0), g.Y(0), g.X(1), g.Y(1), MUTED, 2.5, '7 6') + line(g.X(1), g.Y(1), g.X(3.2), g.Y(3.2), INK, 3)
        b += f'<circle cx="{f(g.X(0))}" cy="{f(g.Y(0))}" r="6" fill="#fff" stroke="{PLUS}" stroke-width="3"/>'
    b += tex(g.X(2.2), g.Y(1.3), '기울기$=\\dfrac{V_0}{273}$', 18, 'start', mix=True, halo=True)
    return b
F['VTA'] = svg(360, 250, vt_pair('a'), 340, '섭씨 온도와 기체의 부피: 영하 273도에서 부피 0으로 연장되는 직선, 0도에서 V0')
F['VTB'] = svg(360, 250, vt_pair('b'), 340, '절대 온도와 기체의 부피: 원점을 지나는 직선')
