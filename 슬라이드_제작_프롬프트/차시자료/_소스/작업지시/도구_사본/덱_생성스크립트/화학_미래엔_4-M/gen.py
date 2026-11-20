# 4-M 대단원 Ⅳ 마무리 덱 그림 생성 — python3 -I gen.py <출력 slides.html>
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

FIG = {}
PINK, PINK_S = '#E04A8B', '#B8326C'
TRI, ORA, MAG, PUR, SKY = '#5DBB63', '#F39C34', '#A23B72', '#8E5BB5', '#7FCDEE'


def svg(vb, w, label, body, extra=''):
    return f'<svg class="fig" viewBox="{vb}" style="width:{w}px" aria-label="{label}"{extra}>{body}</svg>'


def ion(x, y, k):
    sp = {'H': ('P', '\\ce{H+}', '#FFFFFF'), 'OH': ('M', '\\ce{OH-}', '#FFFFFF')}
    t, lab, c = sp[k]
    return f'<g data-chg="{f(x)},{f(y)},20,{t}"></g>' + tex(x, y + 6.5, lab, size=18, fill=c, weight=700)


def h2o(x, y):
    o = [atom(x, y - 4, 14, 'O', '-')]
    for a in (35, 145):
        hx, hy = pol(x, y - 4, 18, a)
        o.append(atom(hx, hy, 10, 'H', '-'))
    return ''.join(o)


# ── 도형(이름 없는 이온 모형) ──
def shp(kind, x, y, col, s=13):
    if kind == 't':
        return f'<polygon points="{f(x)},{f(y-s*1.1)} {f(x-s*1.05)},{f(y+s*0.75)} {f(x+s*1.05)},{f(y+s*0.75)}" fill="{col}"/>'
    if kind == 'c':
        return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(s)}" fill="{col}"/>'
    return f'<rect x="{f(x-s)}" y="{f(y-s)}" width="{f(2*s)}" height="{f(2*s)}" rx="2" fill="{col}"/>'


# ── 기구 ──
def erlen(cx, base, cid, level, color=WATER, stroke=WATER_S, w=80, neck=16, top=None, overlay=''):
    top = base - 130 if top is None else top
    ns = base - 85
    d = f'M{f(cx-neck)},{f(top)} L{f(cx-neck)},{f(ns)} L{f(cx-w)},{f(base-6)} Q{f(cx-w)},{f(base)} {f(cx-w+8)},{f(base)} L{f(cx+w-8)},{f(base)} Q{f(cx+w)},{f(base)} {f(cx+w)},{f(base-6)} L{f(cx+neck)},{f(ns)} L{f(cx+neck)},{f(top)}'
    o = [f'<defs><clipPath id="{cid}"><path d="{d} Z"/></clipPath></defs>']
    o.append(f'<g clip-path="url(#{cid})"><rect x="{f(cx-w)}" y="{f(level)}" width="{f(2*w)}" height="{f(base-level)}" fill="{color}"/>'
             f'<line x1="{f(cx-w)}" y1="{f(level)}" x2="{f(cx+w)}" y2="{f(level)}" stroke="{stroke}" stroke-width="2"/>{overlay}</g>')
    o.append(f'<path d="{d}" fill="none" stroke="{GLASS}" stroke-width="2.6" stroke-linejoin="round"/>')
    return ''.join(o)


def burette(cx, top, bot, level, anim=''):
    o = [f'<rect x="{f(cx-11)}" y="{f(level)}" width="22" height="{f(bot-level)}" fill="{WATER}" {anim}/>']
    o.append(f'<path d="M{f(cx-11)},{f(top)} L{f(cx-11)},{f(bot)} L{f(cx-3)},{f(bot+30)} M{f(cx+11)},{f(top)} L{f(cx+11)},{f(bot)} L{f(cx+3)},{f(bot+30)}" fill="none" stroke="{GLASS}" stroke-width="2.6"/>')
    for i in range(1, 9):
        yy = top + (bot - top) * i / 9
        o.append(f'<line x1="{f(cx-11)}" y1="{f(yy)}" x2="{f(cx-1)}" y2="{f(yy)}" stroke="{MUTED}" stroke-width="1.4"/>')
    o.append(f'<rect x="{f(cx-20)}" y="{f(bot+6)}" width="40" height="9" rx="3" fill="#C9D3DD" stroke="{GLASS}" stroke-width="1.6"/>')
    return ''.join(o)


def titration(ox, oy, cid, pink_anim, blab, flab, fs=19):
    # ox,oy: 스탠드 받침 왼쪽 아래
    o = [f'<rect x="{f(ox)}" y="{f(oy-14)}" width="250" height="14" rx="4" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>']
    o.append(f'<line x1="{f(ox+215)}" y1="{f(oy-14)}" x2="{f(ox+215)}" y2="{f(oy-380)}" stroke="{GLASS}" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<line x1="{f(ox+120)}" y1="{f(oy-300)}" x2="{f(ox+215)}" y2="{f(oy-300)}" stroke="{GLASS}" stroke-width="5"/>')
    o.append(burette(ox + 110, oy - 380, oy - 220, oy - 340, ''))
    o.append(erlen(ox + 110, oy - 14, cid, oy - 50, overlay=f'<rect x="{f(ox+20)}" y="{f(oy-50)}" width="180" height="40" fill="{PINK}" opacity=".55" {pink_anim}/>'))
    o.append(tex(ox + 90, oy - 300, mix=blab, size=fs, anchor='end'))
    o.append(tex(ox + 110, oy + 26, mix=flab, size=fs))
    return ''.join(o)


def phbar(x0, x1, y, lo, hi, marks, w=34):
    """가로 pH 띠. marks = [(pH, 라벨, 위/아래, from_pH)]"""
    o = []
    n = 40
    def X(p): return x0 + (x1 - x0) * (p - lo) / (hi - lo)
    def col(p):
        if p <= 7:
            t = (p - 0) / 7; a = (0xF6, 0xC9, 0xCF); b = (0xE9, 0xED, 0xF1)
        else:
            t = (p - 7) / 7; a = (0xE9, 0xED, 0xF1); b = (0xC9, 0xDB, 0xF5)
        return '#%02X%02X%02X' % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    for i in range(n):
        p0 = lo + (hi - lo) * i / n; p1 = lo + (hi - lo) * (i + 1) / n
        o.append(f'<rect x="{f(X(p0))}" y="{f(y)}" width="{f(X(p1)-X(p0)+0.6)}" height="{w}" fill="{col((p0+p1)/2)}"/>')
    o.append(f'<rect x="{f(x0)}" y="{f(y)}" width="{f(x1-x0)}" height="{w}" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
    p = lo
    step = 1 if hi - lo <= 8 else 2
    while p <= hi + 1e-9:
        o.append(f'<line x1="{f(X(p))}" y1="{f(y+w)}" x2="{f(X(p))}" y2="{f(y+w+7)}" stroke="{MUTED}" stroke-width="1.5"/>')
        o.append(tex(X(p), y + w + 28, mix=f'{p:g}', size=19, fill=MUTED))
        p += step
    for (pv, lab, pos, fr) in marks:
        x = X(pv)
        if pos == 'up':
            g = f'<polygon points="{f(x)},{f(y-2)} {f(x-9)},{f(y-16)} {f(x+9)},{f(y-16)}" fill="{INK}"/>' + tex(x, y - 24, mix=lab, size=19, weight=700)
        else:
            g = f'<polygon points="{f(x)},{f(y+w+2)} {f(x-9)},{f(y+w+16)} {f(x+9)},{f(y+w+16)}" fill="{INK}"/>' + tex(x, y + w + 58, mix=lab, size=19, weight=700)
        if fr is not None:
            g = f'<g data-anim="move" data-from="{f(X(fr)-x)},0" data-dur="1.3" data-delay=".3" data-ease="out">{g}</g>'
        o.append(g)
    return ''.join(o)


# ───── 1 표지 ─────
def cover():
    o = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    # 세로 pH 띠 (위 0, 아래 14)
    x, y0, y1 = 70, 70, 470
    def Y(p): return y0 + (y1 - y0) * p / 14
    for i in range(28):
        p = 14 * (i + .5) / 28
        if p <= 7:
            t = p / 7; a = (0xF6, 0xC9, 0xCF); b = (0xE9, 0xED, 0xF1)
        else:
            t = (p - 7) / 7; a = (0xE9, 0xED, 0xF1); b = (0xC9, 0xDB, 0xF5)
        c = '#%02X%02X%02X' % tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3))
        o.append(f'<rect x="{x}" y="{f(Y(14*i/28))}" width="40" height="{f((y1-y0)/28+0.6)}" fill="{c}"/>')
    o.append(f'<rect x="{x}" y="{y0}" width="40" height="{y1-y0}" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
    o.append(tex(90, 56, mix='pH', size=22, weight=700))
    for p in (0, 7, 14):
        o.append(tex(124, Y(p) + 7, mix=str(p), size=19, anchor='start', fill=MUTED))
    o.append(tex(124, Y(3.2) + 7, mix='산성', size=19, anchor='start', fill=PLUS, weight=700))
    o.append(tex(124, Y(11) + 7, mix='염기성', size=19, anchor='start', fill=MINUS, weight=700))
    yy = Y(8.5)
    mk = f'<polygon points="{x-2},{f(yy)} {x-18},{f(yy-10)} {x-18},{f(yy+10)}" fill="{INK}"/>'
    o.append(f'<g data-anim="move" data-from="0,{f(Y(2)-yy)}" data-dur="1.8" data-delay=".3" data-ease="io">{mk}</g>')
    o.append(titration(205, 470, 'clip-cm49-01', 'data-anim="fade" data-dur="1.2" data-delay="1.6"',
                       '$\\ce{NaOH}$||표준 용액', '산 + 지시약'))
    return f'<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="pH 띠의 표시가 산성에서 중화점 쪽으로 움직이고, 뷰렛으로 수산화 나트륨 표준 용액을 넣은 삼각 플라스크의 용액이 지시약 때문에 붉은색이 되는 중화 적정">{"".join(o)}</svg>'
FIG['cover'] = cover()


# ───── 2 단원 지도 ─────
def unitmap():
    o = []
    o.append(tex(250, 24, mix='1. 물의 자동 이온화와 pH', size=19, fill=FIELD, weight=700))
    o.append(f'<path d="M90 42 V34 H410 V42" fill="none" stroke="{FIELD}" stroke-width="2.5"/>')
    o.append(tex(720, 24, mix='2. 중화 반응', size=19, fill=FIELD, weight=700))
    o.append(f'<path d="M560 42 V34 H880 V42" fill="none" stroke="{FIELD}" stroke-width="2.5"/>')
    o.append(f'<line x1="40" y1="58" x2="1080" y2="58" stroke="#C9D3DD" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<path d="M40 58 H1040" stroke="{FIELD}" stroke-width="6" stroke-linecap="round" fill="none" data-anim="draw" data-dur="1.6" data-delay=".3"/>')
    xs = [(130, '01 물의 자동 이온화와||몰농도'), (370, '02 pH'), (600, '01 중화 반응의||양적 관계'), (840, '02 중화 적정')]
    for x, lab in xs:
        o.append(f'<circle cx="{x}" cy="58" r="11" fill="{FIELD}"/>')
        o.append(tex(x, 100, mix=lab, size=18, fill=MUTED))
    o.append(f'<circle cx="1040" cy="58" r="16" fill="#FFE45C" stroke="{INK}" stroke-width="3"/>')
    o.append(tex(1040, 100, mix='오늘||대단원 마무리', size=18, weight=700))
    return svg('0 0 1112 150', 1112, '대단원 Ⅳ 단원 지도에서 네 소단원을 마치고 오늘은 대단원 마무리', ''.join(o))
FIG['unitmap'] = unitmap()


# ───── 5 pH 사다리 ─────
def ladder():
    o = []
    boxes = [(110, '$[\\ce{H+}]$'), (390, 'pH'), (670, 'pOH'), (950, '$[\\ce{OH-}]$')]
    cols = [PLUS, PLUS, MINUS, MINUS]
    for (x, lab), c in zip(boxes, cols):
        o.append(f'<rect x="{x-80}" y="40" width="160" height="56" rx="12" fill="#fff" stroke="{c}" stroke-width="2.5"/>')
        o.append(tex(x, 77, mix=lab, size=24, weight=700))
    for (a, b, lab) in [(190, 310, '$-\\log$'), (470, 590, '$14.00-$'), (750, 870, '$-\\log$')]:
        o.append(arw(a + 6, 60, b - 6, 60, 'ink', 2.5))
        o.append(arw(b - 6, 78, a + 6, 78, 'muted', 2.5))
        o.append(tex((a + b) / 2, 30, mix=lab, size=19))
    o.append(f'<path d="M110 100 Q110 150 530 150 Q950 150 950 100" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>')
    o.append(tex(530, 140, mix='$[\\ce{H+}][\\ce{OH-}]=K_\\mathrm{w}=1.0\\times10^{-14}$', size=20, halo=True))
    return svg('0 0 1060 165', 1060, '수소 이온 농도, pH, pOH, 수산화 이온 농도를 잇는 관계 사다리', ''.join(o))
FIG['ladder'] = ladder()


# ───── 7 문항 01 피펫 → 부피 플라스크 ─────
def fig01():
    o = []
    # 피펫
    px = 80
    o.append(f'<path d="M{px-4},30 L{px-4},90 Q{px-18},100 {px-18},130 Q{px-18},160 {px-4},170 L{px-4},230 L{px},246 L{px+4},230 L{px+4},170 Q{px+18},160 {px+18},130 Q{px+18},100 {px+4},90 L{px+4},30" fill="{WATER}" stroke="{GLASS}" stroke-width="2.4" stroke-linejoin="round"/>')
    o.append(f'<line x1="{px-9}" y1="62" x2="{px+9}" y2="62" stroke="{INK}" stroke-width="2"/>')
    o.append(tex(px + 26, 68, mix='25 mL', size=19, anchor='start'))
    o.append(tex(px, 282, mix='(가) 미지 농도의||염산 25 mL', size=19))
    o.append(arw(140, 160, 210, 160, 'ink', 3))
    body, cy, mark, tp = flask(330, 270, 'clip-cm49-07', level=None, R=70, neck=24, mark=None)
    lv = mark
    body2, _, _, _ = flask(330, 270, 'clip-cm49-07', level=lv, R=70, neck=24,
                           liq_anim='data-anim="scale" data-from="1,0.12" data-o="330,270" data-dur="1.6" data-delay=".4" data-ease="out"')
    o.append(body2)
    o.append(tex(330 + 20, mark - 12, mix='표시선', size=19, anchor='start', fill=MUTED))
    o.append(tex(330, 300, mix='(나) 500 mL 부피 플라스크', size=19))
    return svg('0 0 460 330', 430, '피펫으로 취한 염산 25 밀리리터를 500 밀리리터 부피 플라스크에 넣고 표시선까지 증류수를 채우는 과정', ''.join(o))
FIG['fig01'] = fig01()


# ───── 8 문항 02 커피 pH ─────
FIG['ph02'] = svg('0 0 560 150', 540, 'pH 띠 3에서 7 사이에 보통 커피 원두 pH 5.0과 발효 원두 pH 4.0 표시',
                  phbar(40, 520, 50, 3, 7, [(5.0, '보통 원두 5.0', 'up', 7.0), (4.0, '발효 원두 4.0', 'down', 7.0)]))


# ───── 10 문항 04 이온 모형 ─────
def fig04():
    o = [beaker(30, 260, 230, 220, 70)]
    pts = [('t', 70, 120, TRI), ('c', 140, 125, ORA), ('t', 215, 118, TRI), ('t', 65, 200, TRI), ('t', 135, 182, TRI),
           ('c', 210, 172, MAG), ('c', 100, 232, MAG), ('t', 190, 232, TRI)]
    g = ''.join(shp(k, x, y, c, 14) for k, x, y, c in pts)
    o.append(f'<g data-anim="pop" data-o="145,175" data-dur=".8" data-delay=".3" data-ease="back">{g}</g>')
    o.append(tex(145, 294, mix='혼합 용액', size=19))
    return svg('0 0 290 310', 290, '혼합 용액 속에 초록 세모 5개, 주황 동그라미 1개, 자주 동그라미 2개가 있는 이온 모형', ''.join(o))
FIG['fig04'] = fig04()


# ───── 11 문항 05 ─────
def fig05():
    o = []
    bx = [20, 230, 440]
    for x in bx:
        o.append(beaker(x, 230, 170, 170, 110))
    a = [('s', 55, 150, ORA), ('c', 105, 150, PUR), ('s', 155, 150, ORA), ('c', 55, 200, PUR), ('s', 105, 200, ORA), ('c', 155, 200, PUR),
         ('s', 80, 175, ORA), ('c', 130, 175, PUR)]
    a = [('s', 50, 140, ORA), ('c', 100, 140, PUR), ('s', 150, 140, ORA), ('c', 75, 175, PUR), ('s', 125, 175, ORA), ('c', 50, 210, PUR),
         ('s', 100, 210, ORA), ('c', 150, 210, PUR)]
    o.append(''.join(shp(k, x, y, c, 13) for k, x, y, c in a))
    o.append(tex(315, 88, mix='?', size=30, weight=700, fill=MUTED))
    ans = [('s', 260, 140, SKY), ('t', 310, 140, MAG), ('s', 360, 140, SKY), ('t', 285, 175, MAG), ('s', 335, 175, SKY),
           ('t', 260, 210, MAG), ('s', 310, 210, SKY), ('t', 360, 210, MAG), ('s', 385, 175, SKY), ('t', 385, 120, MAG)]
    ans = [('s', 258, 135, SKY), ('t', 300, 135, MAG), ('s', 342, 135, SKY), ('t', 384, 135, MAG),
           ('t', 279, 172, MAG), ('s', 321, 172, SKY), ('t', 363, 172, MAG),
           ('s', 258, 210, SKY), ('t', 321, 210, MAG), ('s', 384, 210, SKY)]
    g = ''.join(shp(k, x, y, c, 13) for k, x, y, c in ans)
    o.append(f'<g class="step" data-g="a5"><g data-anim="pop" data-o="320,172" data-dur=".8" data-on="step" data-ease="back">{g}</g></g>')
    c = [('s', 470, 135, SKY), ('c', 520, 135, PUR), ('s', 570, 135, SKY), ('c', 470, 172, PUR), ('t', 520, 174, MAG), ('c', 570, 172, PUR),
         ('s', 470, 210, SKY), ('c', 520, 210, PUR), ('s', 570, 210, SKY), ('s', 590, 98 + 75, SKY)]
    c = [('s', 465, 135, SKY), ('c', 505, 135, PUR), ('s', 545, 135, SKY), ('c', 585, 135, PUR),
         ('s', 485, 172, SKY), ('t', 525, 174, MAG), ('c', 565, 172, PUR),
         ('c', 465, 210, PUR), ('s', 525, 210, SKY), ('s', 585, 210, SKY)]
    o.append(''.join(shp(k, x, y, cc, 13) for k, x, y, cc in c))
    o.append(tex(105, 262, mix='(가) $\\mathrm{HA}(aq)$', size=19))
    o.append(tex(315, 262, mix='(나) $\\mathrm{BOH}(aq)$', size=19))
    o.append(tex(525, 262, mix='(다) 혼합 용액', size=19))
    return svg('0 0 640 275', 640, '(가) 주황 네모 4개와 보라 동그라미 4개, (나) 빈 비커, (다) 하늘색 네모 5개, 보라 동그라미 4개, 자주 세모 1개', ''.join(o))
FIG['fig05'] = fig05()


# ───── 13 문항 07 ─────
def fig07():
    o = [balance(20, 140, 140, '1\\ \\text{g}')]
    o.append(tex(90, 250, mix='$\\ce{NaOH}$ 1 g', size=19))
    o.append(arw(170, 170, 210, 170, 'ink', 3))
    b, cy, mark, tp = flask(285, 230, 'clip-cm49-13', level=None, R=55, neck=20)
    b, cy, mark, tp = flask(285, 230, 'clip-cm49-13', level=mark, R=55, neck=20)
    o.append(b)
    o.append(tex(285, 262, mix='250 mL', size=19))
    o.append(arw(355, 170, 395, 170, 'ink', 3))
    o.append(burette(445, 20, 150, 50, 'data-anim="scale" data-from="1,0.62" data-o="445,150" data-dur="1.6" data-delay=".5"'))
    o.append(tex(470, 70, mix='30 mL', size=19, anchor='start'))
    o.append(erlen(445, 262, 'clip-cm49-13b', 232, top=190, w=56, neck=12))
    o.append(tex(445, 290, mix='$\\ce{H2SO4}(aq)$ 10 mL', size=19))
    return svg('0 0 560 300', 540, '수산화 나트륨 1 그램을 녹여 250 밀리리터 수용액을 만들고, 뷰렛으로 30 밀리리터를 황산 10 밀리리터에 넣는 과정', ''.join(o))
FIG['fig07'] = fig07()


# ───── 14 문항 08 ─────
FIG['fig08'] = ('<svg class="fig" viewBox="0 0 290 470" style="width:240px" aria-label="뷰렛으로 0.05 M 수산화 나트륨 수용액을 묽힌 식초가 든 삼각 플라스크에 넣으면 중화점에서 색이 변하는 장치">'
                + titration(25, 420, 'clip-cm49-14', 'data-anim="fade" data-dur="1.2" data-delay=".8"',
                            '$\\ce{NaOH}(aq)$||0.05 M', '묽힌 식초 20 mL', 22) + '</svg>')


# ───── 15 문항 09 ─────
def fig09():
    o = [beaker(40, 220, 120, 150, 190)]
    o.append(tex(100, 252, mix='(가)', size=19))
    o.append(tex(30, 150, mix='$a$ M||$\\ce{NaOH}(aq)$||20 mL', size=19, anchor='start'))
    o.append(arw(185, 120, 275, 120, MINUS if False else 'ink', 3))
    o.append(tex(230, 104, mix='물 첨가', size=19))
    o.append(beaker(300, 220, 140, 170, 90, liq_anim='data-anim="scale" data-from="1,0.23" data-o="370,220" data-dur="1.6" data-delay=".4" data-ease="out"'))
    o.append(tex(370, 132, mix='pH 13.0||$\\ce{NaOH}(aq)$||100 mL', size=19))
    o.append(tex(370, 252, mix='(나)', size=19))
    return svg('0 0 470 270', 440, '(가) a 몰농도 수산화 나트륨 수용액 20 밀리리터에 물을 넣어 (나) pH 13.0인 100 밀리리터 수용액을 만듦', ''.join(o))
FIG['fig09'] = fig09()


# ───── 16 실험 설계 10(1) 저울 ─────
def fig10a():
    o = [balance(30, 70, 200, '9.0\\ \\text{g}', read_anim='class="step" data-g="b10"')]
    o.append(tex(130, 30, mix='포도당 0.05 몰', size=19))
    return svg('0 0 260 165', 260, '전자저울로 포도당 0.05 몰의 질량을 잼', ''.join(o))
FIG['fig10a'] = fig10a()


# ───── 17 실험 설계 10(2) 단계 카드 ─────
def fig10b():
    o = []
    W = 270
    for i, lab in enumerate(['(가) 비커에서 녹이기', '(나) 부피 플라스크에 붓기', '(다) 표시선까지 채우기', '(라) 흔들어 섞기']):
        x0 = i * W + 5
        o.append(f'<rect x="{x0}" y="5" width="{W-10}" height="250" rx="12" fill="#fff" stroke="#C9D3DD" stroke-width="2"/>')
        o.append(tex(x0 + (W - 10) / 2, 240, mix=lab, size=19, weight=700))
    # (가)
    o.append(beaker(70, 200, 140, 130, 120))
    o.append(f'<line x1="120" y1="50" x2="165" y2="190" stroke="{GLASS}" stroke-width="5" stroke-linecap="round"/>')
    # (나) 비커 기울여 붓기
    b, cy, mark, tp = flask(400, 210, 'clip-cm49-17a', level=180, R=45, neck=18, top=90)
    o.append(b)
    o.append(f'<path d="M378,80 L422,80 L403,102 L403,118 L397,118 L397,102 Z" fill="none" stroke="{GLASS}" stroke-width="2.2"/>')
    pour = (f'<g transform="rotate(-50 330 70)">{beaker(300, 95, 70, 60, 70)}</g>'
            f'<path d="M357,67 Q380,62 398,90" fill="none" stroke="{WATER_S}" stroke-width="4"/>')
    o.append(f'<g data-anim="move" data-from="-30,-14" data-dur="1.2" data-delay=".4" data-ease="out">{pour}</g>')
    # (다)
    b, cy, mark, tp = flask(675, 210, 'clip-cm49-17b', level=None, R=45, neck=18, top=60)
    b, cy, mark, tp = flask(675, 210, 'clip-cm49-17b', level=mark, R=45, neck=18, top=60)
    o.append(b)
    o.append(tex(700, mark + 6, mix='표시선', size=19, anchor='start', fill=MUTED))
    o.append(f'<path d="M600,60 L612,40 L622,60" fill="none" stroke="{GLASS}" stroke-width="2.4"/><rect x="590" y="60" width="44" height="58" rx="10" fill="{WATER}" stroke="{GLASS}" stroke-width="2.4"/>')
    o.append(tex(612, 145, mix='씻기병', size=19, fill=MUTED))
    # (라)
    b, cy, mark, tp = flask(945, 210, 'clip-cm49-17c', level=None, R=45, neck=18, top=60, stopper=True)
    b, cy, mark, tp = flask(945, 210, 'clip-cm49-17c', level=mark, R=45, neck=18, top=60, stopper=True)
    o.append(f'<g data-anim="rot" data-from="-160" data-o="945,150" data-dur="1.4" data-delay=".6" data-ease="soft">{b}</g>')
    o.append(f'<path d="M880,90 A70 70 0 0 1 1010,90" fill="none" stroke="{MUTED}" stroke-width="2.4"/>')
    o.append(arw(1004, 82, 1012, 96, 'muted', 2.4))
    return svg('0 0 1080 260', 1080, '표준 용액 만들기 네 단계: 비커에서 녹이기, 부피 플라스크에 붓기, 표시선까지 채우기, 마개를 닫고 흔들어 섞기', ''.join(o))
FIG['fig10b'] = fig10b()


# ───── 19 제산제 중화 ─────
def fig11():
    o = [f'<rect x="10" y="10" width="420" height="190" rx="20" fill="#FBEFF1" stroke="#E8B9C1" stroke-width="2"/>']
    o.append(tex(220, 40, mix='위 속', size=19, fill=MUTED))
    for (x, y) in [(60, 80), (60, 140)]:
        o.append(ion(x, y, 'H'))
    for (x, y) in [(380, 80), (380, 140)]:
        o.append(ion(x, y, 'OH'))
    o.append(tex(60, 190, mix='위산', size=19, fill=PLUS))
    o.append(tex(380, 190, mix='제산제', size=19, fill=MINUS))
    o.append(arw(95, 110, 180, 110, 'ink', 3))
    o.append(arw(345, 110, 260, 110, 'ink', 3))
    for i, (x, y) in enumerate([(220, 82), (220, 140)]):
        o.append(f'<g data-anim="pop" data-o="{x},{y}" data-dur=".7" data-delay="{.5+i*.3:.1f}" data-ease="back">{h2o(x, y)}</g>')
    o.append(tex(220, 190, mix='물', size=19))
    return svg('0 0 440 210', 420, '위산의 수소 이온과 제산제의 수산화 이온이 만나 물이 되는 중화 반응', ''.join(o))
FIG['fig11'] = fig11()


# ───── 20 사성암 물 pH ─────
FIG['ph12'] = svg('0 0 560 160', 540, 'pH 띠 7에서 9 사이에 루르드 7.9, 트라코테 8.2, 사성암 바위틈 물 8.8 표시',
                  phbar(40, 520, 60, 7, 9, [(7.9, '루르드 7.9', 'up', 7.0), (8.2, '트라코테 8.2', 'down', 7.0), (8.8, '사성암 8.8', 'up', 7.0)]))


# ───── 22 CCUS 모식도 ─────
def ccus():
    o = [f'<rect x="0" y="0" width="1000" height="150" fill="#EAF4FB"/>',
         f'<rect x="0" y="150" width="1000" height="140" fill="#F3DDB6"/>',
         f'<line x1="0" y1="150" x2="1000" y2="150" stroke="#C9A66B" stroke-width="2"/>']
    # 공장
    o.append(f'<rect x="40" y="80" width="130" height="70" fill="#8C99A6"/><rect x="70" y="30" width="20" height="50" fill="#5B6B7F"/><rect x="110" y="40" width="20" height="40" fill="#5B6B7F"/>')
    o.append(tex(105, 122, mix='공장', size=19, fill='#FFFFFF', weight=700))
    # 포집 장치
    o.append(f'<rect x="250" y="60" width="70" height="90" rx="10" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>')
    o.append(tex(285, 50, mix='포집', size=20, weight=700))
    o.append(f'<path d="M170,110 H250" stroke="{GLASS}" stroke-width="10" fill="none"/>')
    # 파이프 → 저장 / 활용
    o.append(f'<path d="M320,120 H520 V250" stroke="{GLASS}" stroke-width="10" fill="none"/>')
    o.append(f'<ellipse cx="520" cy="262" rx="70" ry="20" fill="#DDEEF8" stroke="{GLASS}" stroke-width="2.5"/>')
    o.append(tex(620, 270, mix='저장 (땅속·바닷속)', size=20, anchor='start', weight=700))
    o.append(f'<path d="M320,100 H700 V90" stroke="{GLASS}" stroke-width="10" fill="none"/>')
    o.append(f'<rect x="700" y="30" width="270" height="100" rx="12" fill="#fff" stroke="{FIELD}" stroke-width="2.5"/>')
    o.append(tex(835, 62, mix='활용', size=20, weight=700, fill=FIELD))
    o.append(tex(835, 92, mix='연료, 화학 제품,', size=19))
    o.append(tex(835, 117, mix='시멘트 등 건축 자재', size=19))
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}"/>' for x, y in [(370, 120), (440, 120), (520, 190)])
    o.append(f'<g data-anim="move" data-from="-60,0" data-dur="1.6" data-delay=".3" data-rep="loop" data-ease="lin">{dots}</g>')
    dots2 = ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}"/>' for x, y in [(400, 100), (560, 100), (640, 100)])
    o.append(f'<g data-anim="move" data-from="-60,0" data-dur="1.6" data-delay=".3" data-rep="loop" data-ease="lin">{dots2}</g>')
    o.append(tex(200, 200, mix='배기가스에서 $\\ce{CO2}$만||분리·정제', size=19, fill=MUTED))
    return svg('0 0 1000 290', 900, '공장 배기가스에서 이산화 탄소만 포집해 땅속이나 바닷속에 저장하거나 연료, 화학 제품, 건축 자재로 활용하는 탄소 포집·활용·저장 모식도', ''.join(o))
FIG['ccus'] = ccus()


# ───── 23 광물 탄산화 ─────
def carb():
    o = []
    o.append(f'<path d="M150,20 V215" stroke="{GLASS}" stroke-width="7" fill="none"/>')
    o.append(tex(140, 30, mix='$\\ce{CO2}(g)$', size=22, anchor='end'))
    o.append(beaker(70, 290, 220, 200, 130, color='#EEF2F6', stroke='#C9D3DD'))
    bub = ''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#fff" stroke="{MUTED}" stroke-width="1.6"/>' for x, y in [(160, 200), (175, 172), (158, 150)])
    o.append(f'<g data-anim="move" data-from="0,40" data-dur="1.3" data-rep="loop" data-ease="lin">{bub}</g>')
    ppt = ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#FFFFFF" stroke="#9AA5B1" stroke-width="1.2"/>' for x, y in
                  [(100, 280), (118, 276), (136, 281), (154, 277), (172, 281), (190, 276), (208, 280), (226, 277), (244, 281), (262, 278), (110, 268), (146, 268), (182, 268), (220, 268), (252, 268)])
    o.append(f'<g data-anim="fade" data-dur="1.4" data-delay="1.2">{ppt}</g>')
    o.append(tex(320, 200, mix='$\\ce{Ca(OH)2}(aq)$||염기성 용액', size=22, anchor='start'))
    o.append(tex(320, 282, mix='흰 앙금 $\\ce{CaCO3}(s)$', size=22, anchor='start'))
    o.append(arw(312, 276, 270, 274, 'muted', 2))
    return svg('0 0 520 310', 440, '이산화 탄소 기체를 수산화 칼슘 수용액에 넣으면 흰 앙금 탄산 칼슘이 생기는 반응', ''.join(o))
FIG['carb'] = carb()


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    out = re.sub(r'@@(\w+)@@', lambda m: FIG[m.group(1)], tpl)
    open(sys.argv[1], 'w', encoding='utf-8').write(out)
    print('ok', len(out), out.count('data-anim='))
