# 4-2-1 중화 반응의 양적 관계 덱 그림 생성 — python3 -I gen.py <출력 slides.html>
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

FIG = {}
NFILL = '#A7B3BF'
BTB_A, BTB_N, BTB_B = '#F6E58A', '#BFE3B4', '#AFCDF2'
SPEC = {'H': ('P', '\\ce{H+}', '#FFFFFF', 19), 'OH': ('M', '\\ce{OH-}', '#FFFFFF', 19),
        'Na': ('N', '\\ce{Na+}', INK, 19), 'Cl': ('N', '\\ce{Cl-}', INK, 19),
        'SO4': ('N', '\\ce{SO4^2-}', INK, 23), 'Ba': ('N', '\\ce{Ba^2+}', INK, 22)}


def svg(vb, w, label, body, extra=''):
    return f'<svg class="fig" viewBox="{vb}" style="width:{w}px" aria-label="{label}"{extra}>{body}</svg>'


def ion(x, y, k):
    t, lab, c, r = SPEC[k]
    return f'<g data-chg="{f(x)},{f(y)},{r},{t}"></g>' + tex(x, y + 18 * 0.36, lab, size=18, fill=c, weight=700)


def h2o(x, y):
    o = [atom(x, y - 4, 14, 'O', '-')]
    for a in (90 - 55, 90 + 55):
        hx, hy = pol(x, y - 4, 18, a)
        o.append(atom(hx, hy, 10, 'H', '-'))
    return ''.join(o)


def part(x, y, k):
    return h2o(x, y) if k == 'W' else ion(x, y, k)


def grid(cols, rows, x0, x1, y0, y1):
    pts = []
    for r in range(rows):
        for c in range(cols):
            pts.append((x0 + (x1 - x0) * (c + .5) / cols, y1 - (y1 - y0) * (r + .5) / rows))
    return pts


def place(kinds, pts, wrap=None):
    o = []
    for k, (x, y) in zip(kinds, pts):
        s = part(x, y, k)
        if wrap:
            s = wrap(k, x, y, s)
        o.append(s)
    return ''.join(o)


def legend_water(x, y):
    return h2o(x, y + 2) + tex(x + 24, y + 8, mix='물 분자', size=19, anchor='start', fill=MUTED)


# ───── 1 표지 ─────
def cover():
    o = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    o.append(beaker(60, 230, 170, 140, 120, BTB_A, '#D8C25A'))
    o.append(place(['H', 'Cl', 'Cl', 'H'], [(95, 160), (150, 160), (110, 205), (175, 205)]))
    o.append(tex(145, 262, '\\ce{HCl(aq)}', size=24))
    o.append(tex(270, 170, '+', size=36, weight=700, fill=MUTED))
    o.append(beaker(310, 230, 170, 140, 120, BTB_B, '#7FA6D8'))
    o.append(place(['Na', 'OH', 'OH', 'Na'], [(345, 160), (400, 160), (360, 205), (425, 205)]))
    o.append(tex(395, 262, '\\ce{NaOH(aq)}', size=24))
    o.append(arw(270, 285, 270, 330, 'ink', 4))
    o.append(beaker(150, 480, 240, 140, 368, BTB_N, '#8DC48A'))
    o.append(place(['Na', 'Cl', 'Na', 'Cl'], [(190, 400), (350, 400), (215, 450), (325, 450)]))
    for i, (x, y) in enumerate([(270, 404), (270, 452)]):
        o.append(f'<g data-anim="pop" data-o="{x},{y}" data-dur=".7" data-delay="{.6+i*.3:.1f}" data-ease="back">{h2o(x, y)}</g>')
    return f'<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="염산과 수산화 나트륨 수용액을 섞으면 수소 이온과 수산화 이온은 물이 되고 나트륨 이온과 염화 이온은 남는 입자 모형">{"".join(o)}</svg>'
FIG['cover'] = cover()


# ───── 2 중단원 도입: 토양 ─────
def soil():
    o = [f'<rect x="0" y="170" width="520" height="120" rx="10" fill="#8B5E3C"/>']
    for i, y in enumerate((200, 232, 262)):
        o.append(f'<path d="M10,{y} Q130,{y-10} 260,{y} T510,{y}" fill="none" stroke="#6E4729" stroke-width="3" opacity=".7"/>')
    o.append(f'<path d="M30,52 L110,30 L132,104 L52,126 Z" fill="#EFE8D6" stroke="{GLASS}" stroke-width="2.5"/>')
    o.append(tex(82, 84, mix='석회||가루', size=19, weight=700))
    o.append('<g data-anim="move" data-from="-20,-70" data-dur="1.6" data-delay=".3" data-ease="out">')
    pts = rand_points(26, 150, 70, 380, 155, 14, 7)
    for x, y in pts:
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="4.5" fill="#FFFFFF" stroke="#B9C2CC" stroke-width="1"/>')
    o.append('</g>')
    o.append(f'<g data-anim="fade" data-dur=".8" data-delay="1.6"><rect x="140" y="163" width="260" height="9" rx="4" fill="#F7F4EC"/></g>')
    o.append(tex(260, 248, mix='산성화된 토양 (pH 5 정도)', size=21, weight=700, fill='#FFFFFF'))
    o.append(tex(500, 60, mix='염기성 물질을||뿌려 중화', size=19, anchor='end', fill=MUTED))
    return svg('0 0 520 300', 520, '산성화된 토양 위에 석회 가루를 뿌리는 모습', ''.join(o))
FIG['soil'] = soil()


# ───── 5 생각 열기: 드라이아이스 ─────
def dryice():
    o = []
    cols = [('#8E5BD0', '보라'), ('#3E7FD6', '파랑'), ('#43A047', '초록')]
    for i, (c, n) in enumerate(cols):
        x = 40 + i * 200
        o.append(f'<g opacity=".78"><rect x="{x+2}" y="110" width="96" height="148" fill="{c}"/></g>')
        o.append(f'<path d="M{x-6},70 L{x},76 L{x},260 L{x+100},260 L{x+100},76 L{x+106},70" fill="none" stroke="{GLASS}" stroke-width="2.6" stroke-linejoin="round"/>')
        o.append(f'<rect x="{x-10}" y="260" width="120" height="8" rx="3" fill="{GLASS}"/>')
        for j, (dx, dy) in enumerate([(22, 240), (52, 246), (76, 236)]):
            o.append(f'<rect x="{x+dx-9}" y="{dy-9}" width="18" height="16" rx="3" fill="#F4F6F8" stroke="#B9C2CC" stroke-width="1.2"/>')
        o.append(f'<g data-anim="fade" data-dur="1" data-delay="{.3+i*.4:.1f}"><g opacity=".85">'
                 f'<ellipse cx="{x+50}" cy="62" rx="58" ry="20" fill="#FFFFFF" stroke="#D5DCE3"/>'
                 f'<ellipse cx="{x+25}" cy="44" rx="30" ry="14" fill="#FFFFFF" stroke="#D5DCE3"/>'
                 f'<ellipse cx="{x+78}" cy="42" rx="26" ry="12" fill="#FFFFFF" stroke="#D5DCE3"/></g></g>')
        o.append(tex(x + 50, 296, mix=n, size=21, weight=700))
        if i < 2:
            o.append(arw(x + 120, 180, x + 176, 180, 'muted', 3))
    o.append(tex(300, 22, mix='시간이 지남 →', size=19, fill=MUTED))
    return svg('0 0 600 310', 520, '만능 지시약을 넣은 수산화 나트륨 수용액에 드라이아이스를 넣으면 보라, 파랑, 초록으로 색이 변한다', ''.join(o))
FIG['dryice'] = dryice()


# ───── 8 해 보기 153 단계 카드 ─────
BK = dict(x=30, base=270, w=200, h=175, lv=150)
SL = grid(4, 2, 34, 226, 156, 266)   # 8칸 (아래 줄부터)


def card153(kinds, pour, step_g=None):
    o = [beaker(BK['x'], BK['base'], BK['w'], BK['h'], BK['lv'], WATER, WATER_S)]
    if pour:
        o.append(f'<g data-anim="move" data-from="0,-26" data-dur="1" data-delay=".4" data-ease="out">')
        o.append(f'<rect x="72" y="4" width="116" height="30" rx="15" fill="#FDE8EA" stroke="#F2C6CD"/>')
        o.append(tex(130, 26, mix='묽은 염산', size=19, weight=700))
        o.append(ion(108, 62, 'H') + ion(152, 62, 'Cl'))
        o.append('</g>')
        o.append(arw(130, 86, 130, 118, 'ink', 3))
    body = place(kinds, SL)
    if step_g:
        body = f'<g class="step" data-g="{step_g}">{body}</g>'
    o.append(body)
    return ''.join(o)


C153 = {
    'a': ['Na', 'OH', 'Na', 'OH'],
    'b': ['Na', 'W', 'Na', 'OH', 'Cl'],
    'c': ['Na', 'W', 'Na', 'W', 'Cl', 'Cl'],
    'd': ['Na', 'W', 'Na', 'W', 'Cl', 'Cl', 'H', 'Cl'],
}
FIG['h1a'] = svg('18 0 230 290', 240, '(가) 수산화 나트륨 수용액: 나트륨 이온 2개, 수산화 이온 2개', card153(C153['a'], False))
FIG['h1b'] = svg('18 0 230 290', 240, '(나) 염산을 한 번 넣음: 나트륨 이온 2, 수산화 이온 1, 염화 이온 1, 물 분자 1', card153(C153['b'], True))
FIG['h1c'] = svg('18 0 230 290', 240, '(다) 염산을 두 번 넣음: 나트륨 이온 2, 염화 이온 2, 물 분자 2', card153(C153['c'], True, 'c3'))
FIG['h1d'] = svg('18 0 230 290', 240, '(라) 염산을 세 번 넣음: 나트륨 이온 2, 염화 이온 3, 수소 이온 1, 물 분자 2', card153(C153['d'], True, 'c4'))


# ───── 10 입자 수 막대 ─────
def bars10():
    data = {'H': [0, 0, 0, 1], 'Cl': [0, 1, 2, 3], 'Na': [2, 2, 2, 2], 'OH': [2, 1, 0, 0]}
    col = {'H': (PLUS, PLUS), 'Cl': ('#D5DCE3', GRAV), 'Na': (GRAV, '#6F7C89'), 'OH': (MINUS, MINUS)}
    lab = {'H': '\\ce{H+}', 'Cl': '\\ce{Cl-}', 'Na': '\\ce{Na+}', 'OH': '\\ce{OH-}'}
    X0, Y0, U = 70, 250, 62
    o = []
    for v in (1, 2, 3):
        y = Y0 - v * U
        o.append(f'<line x1="{X0}" y1="{y}" x2="980" y2="{y}" stroke="#E1E6EC" stroke-width="1.2"/>')
        o.append(tex(X0 - 10, y + 6, str(v), size=18, anchor='end', fill=MUTED))
    o.append(tex(X0 - 10, Y0 + 6, '0', size=18, anchor='end', fill=MUTED))
    for gi, gname in enumerate(['(가)', '(나)', '(다)', '(라)']):
        gx = 110 + gi * 225
        for bi, k in enumerate(['H', 'Cl', 'Na', 'OH']):
            x = gx + bi * 42
            v = data[k][gi]
            fc, sc = col[k]
            if v:
                o.append(f'<g data-anim="scale" data-from="1,0" data-o="{x+17},{Y0}" data-dur=".8" data-delay="{.2+gi*.25:.2f}" data-ease="out">'
                         f'<rect x="{x}" y="{Y0-v*U}" width="34" height="{v*U}" fill="{fc}" stroke="{sc}" stroke-width="1.5"/></g>')
            o.append(tex(x + 17, Y0 - v * U - 8, str(v), size=18, weight=700))
        o.append(tex(gx + 80, Y0 + 32, mix=gname, size=20, weight=700))
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="984" y2="{Y0}" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="40" stroke="{INK}" stroke-width="2"/>')
    o.append(tex(X0 + 8, 46, mix='입자 수', size=19, anchor='start', weight=700))
    for i, k in enumerate(['H', 'Cl', 'Na', 'OH']):
        lx = 560 + i * 105
        fc, sc = col[k]
        o.append(f'<rect x="{lx}" y="22" width="22" height="22" fill="{fc}" stroke="{sc}" stroke-width="1.5"/>')
        o.append(tex(lx + 30, 40, lab[k], size=19, anchor='start'))
    return svg('0 0 1000 300', 1000, '(가)부터 (라)까지 이온별 입자 수 막대: 나트륨 이온 2 일정, 염화 이온 0 1 2 3, 수산화 이온 2 1 0 0, 수소 이온 0 0 0 1', ''.join(o))
FIG['bars10'] = bars10()


# ───── 11 중화 반응 모형 ─────
def mix3(acid, base, prod, labs, vb_w=1000, pops=()):
    o = []
    o.append(beaker(40, 220, 200, 160, 100, WATER, WATER_S))
    o.append(place(acid, grid(2, 2, 44, 236, 104, 216)))
    o.append(tex(140, 254, labs[0], size=21))
    o.append(tex(290, 160, '+', size=34, weight=700, fill=MUTED))
    o.append(beaker(340, 220, 200, 160, 100, WATER, WATER_S))
    o.append(place(base, grid(2, 2, 344, 536, 104, 216)))
    o.append(tex(440, 254, labs[1], size=21))
    o.append(arw(570, 160, 650, 160, 'ink', 3))
    o.append(beaker(680, 220, 290, 160, 100, WATER, WATER_S))
    pts = grid(3, 2, 684, 966, 104, 216)

    def wrap(k, x, y, s):
        if k == 'W':
            return f'<g data-anim="pop" data-o="{f(x)},{f(y)}" data-dur=".7" data-delay=".8" data-ease="back">{s}</g>'
        return s
    o.append(place(prod, pts, wrap))
    o.append(tex(825, 254, labs[2], size=21))
    return ''.join(o)


FIG['m11'] = svg('0 0 1000 270', 1000, '염산 비커와 수산화 나트륨 수용액 비커를 섞으면 물 분자, 나트륨 이온, 염화 이온이 있는 용액이 된다',
                 mix3(['H', 'Cl', 'Cl', 'H'], ['Na', 'OH', 'OH', 'Na'], ['Na', 'W', 'Cl', 'Cl', 'W', 'Na'],
                      ['\\ce{HCl(aq)}', '\\ce{NaOH(aq)}', '\\text{섞은 용액}']) + legend_water(850, 22))


# ───── 13 염: 증발 접시 ─────
def salt():
    o = []
    for x1, x2 in ((150, 120), (270, 300)):
        o.append(f'<line x1="{x1}" y1="182" x2="{x2}" y2="282" stroke="{INK}" stroke-width="3.5"/>')
    o.append(f'<rect x="100" y="176" width="220" height="8" rx="2" fill="#B9C2CC" stroke="{MUTED}" stroke-width="1.5"/>')
    o.append(f'<path d="M120,118 L300,118 Q296,174 210,176 Q124,174 120,118 Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.8"/>')
    import random as _r
    rnd = _r.Random(3)
    for i in range(10):
        x = 160 + i * 9 + rnd.uniform(-2, 2); y = 152 - abs(i - 4.5) * 1.2 + rnd.uniform(-3, 3)
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="11" height="11" fill="#F4F6F8" stroke="#8C99A6" stroke-width="1.2" transform="rotate({rnd.choice([0,12,-10,20])} {f(x+5)} {f(y+5)})"/>')
    o.append(f'<g data-anim="move" data-from="0,12" data-dur="1.6" data-rep="loop" data-ease="lin" data-flow="1"><g opacity=".6">'
             f'<path d="M180,104 q-9,-13 0,-26 q9,-13 0,-26" fill="none" stroke="{GRAV}" stroke-width="2.5"/>'
             f'<path d="M235,104 q-9,-13 0,-26 q9,-13 0,-26" fill="none" stroke="{GRAV}" stroke-width="2.5"/></g></g>')
    o.append(f'<path d="M193,262 Q210,204 227,262 Z" fill="#7FB2F0" stroke="#3E7FD6" stroke-width="2"/>')
    o.append(f'<path d="M202,262 Q210,226 218,262 Z" fill="#FFFFFF" opacity=".8"/>')
    o.append(f'<rect x="180" y="262" width="60" height="18" rx="3" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>')
    o.append(tex(306, 140, mix='증발 접시', size=19, anchor='start', fill=MUTED))
    o.append(tex(256, 66, mix='물 증발', size=19, anchor='start', fill=MUTED))
    o.append(tex(246, 240, mix='가열', size=19, anchor='start', fill=MUTED))
    o.append(arw(96, 128, 158, 152, 'muted', 2))
    o.append(tex(96, 116, mix='흰색 결정', size=19, anchor='middle', weight=700))
    return svg('0 0 420 290', 420, '완전히 중화한 혼합 용액을 증발 접시에서 가열하면 물이 증발하고 흰색 결정이 남는다', ''.join(o))
FIG['salt'] = salt()


# ───── 14 혼합 용액의 액성: 상자 3개 ─────
def ratio():
    sets = [('3', '2', ['Cl', 'W', 'Na', 'Cl', 'H', 'W', 'Na', 'Cl'], '산성', PLUS),
            ('2', '2', ['Cl', 'W', 'Na', 'Na', 'W', 'Cl'], '중성', GRAV),
            ('2', '3', ['Na', 'W', 'Cl', 'Na', 'OH', 'W', 'Cl', 'Na'], '염기성', MINUS)]
    o = []
    for i, (h, oh, kinds, nm, c) in enumerate(sets):
        x = 20 + i * 360
        o.append(tex(x + 160, 26, mix=f'$\\ce{{H+}}$ {h}개 + $\\ce{{OH-}}$ {oh}개', size=20, weight=700))
        o.append(f'<rect x="{x}" y="42" width="320" height="170" rx="12" fill="#F7FAFC" stroke="{GLASS}" stroke-width="2"/>')
        pts = grid(4, 2, x + 6, x + 314, 48, 206)

        def wrap(k, px, py, s, i=i):
            if k == 'W':
                return f'<g data-anim="pop" data-o="{f(px)},{f(py)}" data-dur=".6" data-delay="{.4+i*.3:.1f}" data-ease="back">{s}</g>'
            return s
        o.append(place(kinds, pts, wrap))
        o.append(f'<g class="step" data-g="r{i+1}">' + tex(x + 160, 244, mix=f'남는 이온 → {nm}' if nm != '중성' else '남는 $\\ce{H+}$·$\\ce{OH-}$ 없음 → 중성', size=21, weight=700, fill=c) + '</g>')
    return svg('0 0 1100 260', 1060, '수소 이온과 수산화 이온의 수를 다르게 섞은 세 혼합 용액의 입자 모형: 산성, 중성, 염기성', ''.join(o))
FIG['ratio'] = ratio()


# ───── 17 해 보기 155: 비커 4개 ─────
def hb155():
    o = []
    specs = [('(가)', '0.1\\ \\text{M}\\ \\ce{HCl(aq)}', '100\\ \\text{mL}', 1, ['H', 'Cl'], None),
             ('(나)', '0.2\\ \\text{M}\\ \\ce{HCl(aq)}', '100\\ \\text{mL}', 1, ['H', 'Cl', 'Cl', 'H'], 'b'),
             ('(다)', '0.1\\ \\text{M}\\ \\ce{HCl(aq)}', '200\\ \\text{mL}', 2, ['H', 'Cl', 'Cl', 'H'], 'c'),
             ('(라)', '0.1\\ \\text{M}\\ \\ce{H2SO4(aq)}', '100\\ \\text{mL}', 1, ['H', 'SO4', 'H'], 'd')]
    for i, (nm, c, v, m, kinds, g) in enumerate(specs):
        x = 40 + i * 265
        lv = 230 - 80 * m
        o.append(beaker(x, 230, 180, 195, lv, WATER, WATER_S))
        if m == 1:
            pts = [(x + 50, 196), (x + 130, 196)] if len(kinds) == 2 else ([(x + 45, 172), (x + 135, 172), (x + 45, 212), (x + 135, 212)] if len(kinds) == 4 else [(x + 40, 200), (x + 90, 186), (x + 140, 200)])
            if len(kinds) == 4:
                pts = [(x + 50, 172), (x + 130, 172), (x + 50, 212), (x + 130, 212)]
        else:
            pts = [(x + 55, 110), (x + 125, 150), (x + 55, 210), (x + 125, 190)]
        body = place(kinds, pts)
        if g:
            body = f'<g class="step" data-g="{g}"><g data-anim="pop" data-o="{x+90},{230-40*m}" data-dur=".6" data-ease="back">{body}</g></g>'
        o.append(body)
        o.append(tex(x + 90, 262, mix=f'{nm} ${c}$', size=19, weight=700))
        o.append(tex(x + 90, 288, v, size=19))
    return svg('0 0 1080 300', 1060, '농도와 부피가 다른 산 수용액 (가)부터 (라)까지의 이온 모형', ''.join(o))
FIG['hb155'] = hb155()


# ───── 19·20 그림 IV-6, IV-7 ─────
FIG['m19'] = svg('0 0 1000 270', 1000, '0.1 M 염산 100 mL와 0.1 M 수산화 나트륨 수용액 100 mL가 완전히 중화하는 모형',
                 mix3(['H', 'Cl'], ['Na', 'OH'], ['Na', 'W', 'Cl'],
                      ['\\ce{HCl(aq)}', '\\ce{NaOH(aq)}', '\\ce{H2O(l) + NaCl(aq)}']) + legend_water(850, 22))
FIG['m20'] = svg('0 0 1000 270', 1000, '0.1 M 황산 100 mL와 0.2 M 수산화 나트륨 수용액 100 mL가 완전히 중화하는 모형',
                 mix3(['H', 'SO4', 'H'], ['Na', 'OH', 'OH', 'Na'], ['Na', 'W', 'SO4', 'Na', 'W'],
                      ['\\ce{H2SO4(aq)}', '\\ce{2NaOH(aq)}', '\\ce{2H2O(l) + Na2SO4(aq)}']) + legend_water(850, 22))


# ───── 21 가수 ─────
def gasu():
    o = []
    o.append(f'<rect x="10" y="20" width="150" height="70" rx="12" fill="#FDF1F3" stroke="#F2C6CD" stroke-width="2"/>')
    o.append(tex(85, 52, '\\ce{H2SO4}', size=24, weight=700))
    o.append(tex(85, 78, mix='1개', size=19, fill=MUTED))
    o.append(arw(170, 55, 230, 55, 'ink', 3))
    o.append(ion(275, 55, 'SO4'))
    for i, y in enumerate((30, 82)):
        o.append(f'<g data-anim="move" data-from="-60,{55-y}" data-dur="1" data-delay=".4" data-ease="out">{ion(345, y, "H")}</g>')
    o.append(tex(400, 62, mix='$\\ce{H+}$ 2개 → 2가 산', size=20, anchor='start', weight=700, fill=PLUS))
    o.append(f'<rect x="10" y="140" width="150" height="70" rx="12" fill="#EEF4FC" stroke="#C5D8F2" stroke-width="2"/>')
    o.append(tex(85, 172, '\\ce{Ba(OH)2}', size=24, weight=700))
    o.append(tex(85, 198, mix='1개', size=19, fill=MUTED))
    o.append(arw(170, 175, 230, 175, 'ink', 3))
    o.append(ion(275, 175, 'Ba'))
    for i, y in enumerate((150, 202)):
        o.append(f'<g data-anim="move" data-from="-60,{175-y}" data-dur="1" data-delay=".9" data-ease="out">{ion(345, y, "OH")}</g>')
    o.append(tex(400, 182, mix='$\\ce{OH-}$ 2개 → 2가 염기', size=20, anchor='start', weight=700, fill=MINUS))
    return svg('0 0 640 230', 640, '황산 1개는 수소 이온 2개, 수산화 바륨 1개는 수산화 이온 2개를 내놓는다', ''.join(o))
FIG['gasu'] = gasu()


# ───── 23·24 연습 ─────
def prac(acid, base, ions_a, label):
    o = [beaker(30, 220, 170, 150, 120, WATER, WATER_S)]
    o.append(place(ions_a, [(70, 160), (160, 160), (115, 200)][:len(ions_a)] if len(ions_a) == 3 else [(75, 175), (155, 175)]))
    o.append(tex(115, 252, acid[0], size=20))
    o.append(tex(115, 278, acid[1], size=20))
    o.append(f'<rect x="300" y="34" width="22" height="150" rx="4" fill="{BTB_B}" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<rect x="300" y="34" width="22" height="40" rx="4" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<path d="M305,184 L311,206 L317,184" fill="{GLASS}"/>')
    o.append(arw(290, 120, 215, 150, 'muted', 2.5, dash=True))
    o.append(tex(340, 100, base[0], size=20, anchor='start'))
    o.append(tex(340, 128, base[1], size=20, anchor='start'))
    o.append(tex(340, 160, mix='부피 = ? mL', size=20, anchor='start', weight=700, fill=MINUS))
    return svg('0 0 520 290', 470, label, ''.join(o))


FIG['p23'] = prac(['0.4\\ \\text{M}\\ \\ce{HCl(aq)}', '100\\ \\text{mL}'], ['0.1\\ \\text{M}', '\\ce{Ba(OH)2(aq)}'], ['H', 'Cl'],
                  '0.4 M 염산 100 mL에 0.1 M 수산화 바륨 수용액을 넣어 완전히 중화한다')
FIG['p24'] = prac(['0.2\\ \\text{M}\\ \\ce{H2SO4(aq)}', '100\\ \\text{mL}'], ['0.1\\ \\text{M}', '\\ce{Ba(OH)2(aq)}'], ['H', 'H', 'SO4'],
                  '0.2 M 황산 100 mL에 0.1 M 수산화 바륨 수용액을 넣어 완전히 중화한다')


# ───── 27 위와 작은창자 ─────
def gut():
    o = []
    o.append(f'<path d="M90,30 C60,30 45,70 60,115 C75,160 150,175 185,145 C205,128 198,102 183,96 C168,90 158,110 148,117 C125,132 103,110 110,72 C114,50 110,30 90,30 Z" fill="#F8C9CF" stroke="#C26A77" stroke-width="2.5"/>')
    d = 'M185,145 C215,160 238,152 245,128 C252,105 268,98 282,113 C296,132 282,166 252,180'
    o.append(f'<path d="{d}" fill="none" stroke="#E6A15C" stroke-width="20" stroke-linecap="round"/>')
    o.append(f'<path d="{d}" fill="none" stroke="#F6D2A8" stroke-width="14" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="338" cy="84" rx="46" ry="19" fill="#F3E3B8" stroke="#B8975A" stroke-width="2" transform="rotate(-12 338 84)"/>')
    o.append(arw(312, 104, 284, 122, 'minus', 3))
    o.append(tex(96, 86, mix='위', size=20, weight=700))
    o.append(tex(96, 214, mix='염산, pH 1~2', size=19, fill=PLUS, weight=700))
    o.append(tex(338, 56, mix='이자', size=19, weight=700))
    o.append(tex(262, 214, mix='작은창자', size=19, weight=700))
    o.append(tex(345, 148, mix='염기성||소화액', size=19, fill=MINUS, weight=700))
    return svg('0 0 400 230', 400, '위의 염산이 작은창자로 내려가면 이자에서 나온 염기성 소화액과 만난다', ''.join(o))
FIG['gut'] = gut()


# ───── 28 01 학생 대화 ─────
def talk():
    o = []
    texts = ['$\\ce{H+}$과 $\\ce{OH-}$은||알짜 이온이야.',
             '산 수용액에 염기 수용액을||넣으면 혼합 수용액의||$\\ce{H+}$ 농도는 증가해.',
             '반응하는 $\\ce{OH-}$의 양(mol)과||생성되는 $\\ce{H2O}$의||양(mol)은 같아.']
    for i, t in enumerate(texts):
        x = 15 + i * 330
        o.append(f'<rect x="{x}" y="8" width="300" height="118" rx="18" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<path d="M{x+130},126 L{x+150},150 L{x+165},126" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
        o.append(f'<line x1="{x+131}" y1="126" x2="{x+164}" y2="126" stroke="#FFFFFF" stroke-width="3"/>')
        o.append(tex(x + 150, 42 if i == 0 else 38, mix=t, size=20))
        o.append(tex(x + 150, 176, mix=f'학생 {"ABC"[i]}', size=20, weight=700))
    return svg('0 0 1000 190', 960, '학생 세 명의 대화', ''.join(o))
FIG['talk'] = talk()


# ───── 33 함께 풀어 보기 그림 ─────
def map3():
    o = []
    sets = [('(가)', ['Na', 'OH', 'Na', 'OH'], False), ('(나)', ['Na', 'W', 'Na', 'OH', 'Cl'], True), ('(다)', ['Na', 'W', 'Na', 'W', 'Cl', 'Cl'], True)]
    for i, (nm, kinds, pour) in enumerate(sets):
        x = 15 + i * 215
        o.append(beaker(x, 222, 170, 122, 126, WATER, WATER_S))
        o.append(place(kinds, grid(3, 2, x + 4, x + 166, 130, 218)))
        o.append(tex(x - 4, 30, mix=nm, size=20, weight=700, anchor='start'))
        if pour:
            o.append(tex(x + 120, 30, mix='염산', size=19, fill=MUTED))
            o.append(ion(x + 95, 66, 'H') + ion(x + 145, 66, 'Cl'))
        if i < 2:
            o.append(arw(x + 178, 176, x + 207, 176, 'muted', 3))
    return svg('0 0 640 232', 640, '수산화 나트륨 수용액에 염산을 넣어 가는 (가), (나), (다)의 입자 모형', ''.join(o))
FIG['map3'] = map3()

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    out = re.sub(r'@@(\w+)@@', lambda m: FIG[m.group(1)], tpl)
    open(sys.argv[1], 'w', encoding='utf-8').write(out)
    print('wrote', sys.argv[1], len(out))
