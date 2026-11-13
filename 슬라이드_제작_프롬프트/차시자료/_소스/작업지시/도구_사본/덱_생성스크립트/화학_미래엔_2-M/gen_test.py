# 2-M 그림 생성: slides.tpl.html 의 @@이름@@ 를 SVG 조각으로 바꿔 slides.html 을 만든다.
import math, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

PLUS, MINUS, FIELD, EQUI = '#D7263D', '#1F6FD1', '#2E9E6A', '#E08A2C'
F = {}
CONTENT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/'


def lab(x, y, tex, size=22, col=None, anchor='middle', mix=False, extra=''):
    fill = f' fill="{col}"' if col else ''
    key = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {key}="{tex}" data-size="{size}" data-anchor="{anchor}"{fill}{extra}></text>'


def arw(x1, y1, x2, y2, col='ink', w=3, tail=True):
    s = f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}"></g>'
    if tail:
        L = math.hypot(x2 - x1, y2 - y1) or 1
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        tx, ty = x1 + ux * L * 0.15, y1 + uy * L * 0.15
        c = {'ink': INK, 'plus': PLUS}.get(col, col)
        h = 7 if w <= 3 else 9
        s += f'<line x1="{f(tx - uy * h)}" y1="{f(ty + ux * h)}" x2="{f(tx + uy * h)}" y2="{f(ty - ux * h)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    return f'<g>{s}</g>'


def bond_dip(a, b, off, ln, cen, col='ink', w=3):
    """a(δ+) → b(δ−) 결합 옆 쌍극자 화살표. cen 반대쪽으로 off 만큼"""
    ux, uy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    px, py = -uy, ux
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if px * (mx - cen[0]) + py * (my - cen[1]) < 0 or (abs(px * (mx - cen[0]) + py * (my - cen[1])) < 1e-6 and py > 0):
        px, py = -px, -py
    cx, cy = mx + px * off, my + py * off
    return arw(cx - ux * ln / 2, cy - uy * ln / 2, cx + ux * ln / 2, cy + uy * ln / 2, col, w)


def bar(x1, y1, x2, y2, order=1, w=7):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1
    px, py = -dy / n, dx / n
    offs = {1: [0], 2: [-4.5, 4.5]}[order]
    return ''.join(f'<line x1="{f(x1 + px * o)}" y1="{f(y1 + py * o)}" x2="{f(x2 + px * o)}" y2="{f(y2 + py * o)}" stroke="{BOND}" stroke-width="{w if order == 1 else 5}" stroke-linecap="round"/>' for o in offs)


def atom(x, y, el, r=None, label=None):
    r = r or R[el]
    l = '' if label is None else f',{label}'
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{l}"></g>'


def best_view(nb, nl=0, ang=None, L=100):
    bd, ld = angle_dirs(nl, nb, ang)
    best = None
    for yaw in range(-60, 61, 3):
        for pitch in (-10, -14, -18, -22):
            pts = [(0, 0)] + [(rot(norm(d), yaw, pitch)[0] * L, rot(norm(d), yaw, pitch)[1] * L) for d in bd + ld]
            m = min(math.hypot(p[0] - q[0], p[1] - q[1]) for i, p in enumerate(pts) for q in pts[i + 1:])
            if best is None or m > best[0]:
                best = (m, yaw, pitch)
    return best[1], best[2]


V4 = best_view(4)


# ───────── S1 표지: 물 분자 ─────────
def cover():
    s = '<circle cx="270" cy="250" r="230" fill="#EEF3F8"/>'
    O = (270, 200); h = math.radians(52.25); l = 130
    H1 = (270 - math.sin(h) * l, 200 + math.cos(h) * l); H2 = (270 + math.sin(h) * l, 200 + math.cos(h) * l)
    cen = (270, 250)
    mol = bar(*O, *H1) + bar(*O, *H2) + atom(*H1, 'H', 25) + atom(*H2, 'H', 25) + atom(*O, 'O', 34)
    mol += bond_dip(H1, O, 44, 78, cen) + bond_dip(H2, O, 44, 78, cen)
    mol += lab(270, 150, '\\delta^-', 30, MINUS) + lab(H1[0] - 6, H1[1] + 62, '\\delta^+', 30, PLUS) + lab(H2[0] + 6, H2[1] + 62, '\\delta^+', 30, PLUS)
    s += f'<g data-anim="rot" data-from="-28" data-o="270,250" data-dur="1.6" data-delay=".3" data-ease="soft">{mol}</g>'
    s += f'<g data-anim="fade" data-dur=".8" data-delay="1.9">{arw(270, 372, 270, 290, "plus", 5)}</g>'
    s += lab(270, 452, '극성 결합 + 굽은 형', 24, INK, mix=True, extra=' data-weight="700"')
    s += lab(270, 490, '→ 극성 분자', 24, FIELD, mix=True, extra=' data-weight="700"')
    return s
F['COVER'] = cover()


# ───────── S7 01: 2-1-1 그림 다시 쓰기 ─────────
src = open(CONTENT + '2-1-1_화학_결합의_전기적_성질/slides.html', encoding='utf-8').read().split('\n')
q1a = re.search(r'<svg viewBox="0 0 300 210".*?</svg>', src[241]).group(0)
q1a = q1a.replace('<svg viewBox="0 0 300 210"', '<svg class="fig" viewBox="30 20 250 190" style="width:240px"', 1)
q1a = q1a.replace('aria-label="(−)극 관에 기체가 두 배 모인 전기 분해 장치"', 'aria-label="(가) 물의 전기 분해 장치. 물이 담긴 장치를 A로 표시"')
q1a = q1a.replace('</svg>', '<line x1="62" y1="126" x2="86" y2="126" stroke="#5B6B7F" stroke-width="2"/>' + lab(52, 133, '\\mathrm{A}', 22, anchor='end') + '</svg>')
q1b = re.search(r'<svg class="fig" viewBox="0 0 560 370".*?</svg>', src[282]).group(0).replace('viewBox="0 0 560 370" style="width:500px"', 'viewBox="90 10 390 360" style="width:360px"')
F['Q1A'] = q1a
F['Q1B'] = q1b


# ───────── S8 02: 전기음성도 표 ─────────
EN = {1: [('H', 2.2, 0)], 2: [('Li', 1.0, 0), ('Be', 1.6, 1), ('B', 2.0, 2), ('C', 2.6, 3), ('N', 3.0, 4), ('O', 3.4, 5), ('F', 4.0, 6)],
      3: [('Na', .9, 0), ('Mg', 1.3, 1), ('Al', 1.6, 2), ('Si', 1.9, 3), ('P', 2.2, 4), ('S', 2.6, 5), ('Cl', 3.2, 6)]}
def encol(v):
    t = (v - .9) / 3.1
    a, b = (0xF7, 0xEF, 0xA6), (0xE0, 0x7B, 0x3C)
    return '#%02X%02X%02X' % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def q02():
    x0, y0, w, h = 70, 40, 76, 66
    s = ''
    for k, g in enumerate(['1', '2', '13', '14', '15', '16', '17']):
        s += lab(x0 + k * w + w / 2, 28, g, 19, MUTED)
    s += lab(28, 28, '족', 19, MUTED, mix=True) + lab(28, 54, '주기', 19, MUTED, mix=True, extra=' data-overlap="ok"') if False else lab(40, 28, '족 →', 19, MUTED, mix=True, anchor='end')
    for p in (1, 2, 3):
        s += lab(40, y0 + (p - 1) * h + h / 2 + 7, str(p), 19, MUTED, anchor='end')
        for el, v, c in EN[p]:
            x, y = x0 + c * w, y0 + (p - 1) * h
            s += f'<rect x="{x + 2}" y="{y + 2}" width="{w - 4}" height="{h - 4}" rx="6" fill="{encol(v)}"/>'
            s += lab(x + w / 2, y + 30, f'\\mathrm{{{el}}}', 24) + lab(x + w / 2, y + 56, f'{v:.1f}', 19, '#5B4A2E')
    # 강조
    y2 = y0 + h
    s += f'<g class="step" data-g="p1"><rect x="{x0}" y="{y2}" width="{7 * w}" height="{h}" rx="8" fill="none" stroke="{FIELD}" stroke-width="3.5"/><g data-arw="{x0 + 20},{y0 + 3 * h + 22},{x0 + 7 * w - 20},{y0 + 3 * h + 22},field,3"></g>' + lab(x0 + 3.5 * w, y0 + 3 * h + 50, '같은 주기: 오른쪽으로 갈수록 커진다', 20, FIELD, mix=True) + '</g>'
    xs = x0 + 6 * w
    s += f'<g class="step" data-g="p2"><rect x="{xs}" y="{y2}" width="{w}" height="{2 * h}" rx="8" fill="none" stroke="{MINUS}" stroke-width="3.5"/><g data-arw="{xs + w + 22},{y2 + 10},{xs + w + 22},{y2 + 2 * h - 10},minus,3"></g>' + lab(x0 + 3.5 * w, y0 + 3 * h + 80, '같은 족: 아래로 갈수록 작아진다', 20, MINUS, mix=True) + '</g>'
    return s
F['Q02'] = q02()


# ───────── S9 03: F2, HCl, HF ─────────
def q03():
    s = ''
    items = [('F', 'F', 75, 0, '\\ce{F2}'), ('H', 'Cl', 245, 1.0, '\\ce{HCl}'), ('H', 'F', 415, 1.8, '\\ce{HF}')]
    y = 100
    for e1, e2, x, d, name in items:
        L = 54
        a, b = (x - L / 2, y), (x + L / 2, y)
        s += bar(*a, *b) + atom(*a, e1) + atom(*b, e2)
        s += lab(x, 36, name, 22)
        if d:
            s += f'<g class="step" data-g="d3">' + lab(a[0] - 4, y - 32, '\\delta^+', 22, PLUS) + lab(b[0] + 4, y - 36, '\\delta^-', 22, MINUS)
            ln = 55 * d
            s += f'<g data-anim="fade" data-on="step" data-dur=".8">{arw(x - ln / 2, y + 52, x + ln / 2, y + 52)}</g>'
            s += lab(x, y + 88, f'차이 {d:.1f}', 19, MUTED, mix=True) + '</g>'
        else:
            s += f'<g class="step" data-g="d3">' + lab(x, y + 60, '치우침 없음', 20, MUTED, mix=True) + lab(x, y + 88, '차이 0', 19, MUTED, mix=True) + '</g>'
    return s
F['Q03'] = q03()


# ───────── S10 04: 수직선 ─────────
def q04():
    s = '<line x1="30" y1="80" x2="510" y2="80" stroke="#5B6B7F" stroke-width="2.5"/>'
    s += '<g data-arw="540,80,566,80,muted,2.5"></g>' if False else ''
    k = 240
    SZ = 21
    pts = [('W', 0, '기준 0'), ('Z', 1.0, '+1.0'), ('X', 1.2, '+1.2'), ('Y', 1.8, '+1.8')]
    for i, (n, v, t) in enumerate(pts):
        x = 60 + k * v
        s += (f'<g data-anim="pop" data-o="{f(x)},80" data-on="step" data-dur=".5" data-delay="{.15 + .35 * i}"><circle cx="{f(x)}" cy="80" r="9" fill="{INK}"/></g>'
              + lab(x, 54, f'\\mathrm{{{n}}}', 24) + lab(x, 116, t, SZ, MUTED, mix=True))
    xz, xx = 60 + k * 1.0, 60 + k * 1.2
    s += f'<path d="M{f(xz)} 132 V140 H{f(xx)} V132" fill="none" stroke="{PLUS}" stroke-width="2.5"/>' + lab((xz + xx) / 2, 168, '0.2', SZ, PLUS)
    s += lab(510, 168, '전기음성도 →', SZ, MUTED, mix=True, anchor='end')
    return s
F['Q04'] = q04()


# ───────── S11 05: 분류도 ─────────
def diamond(x, y, w, h, text, size=18):
    return (f'<polygon points="{f(x)},{f(y - h / 2)} {f(x + w / 2)},{f(y)} {f(x)},{f(y + h / 2)} {f(x - w / 2)},{f(y)}" fill="#FCE4EC" stroke="#E8457F" stroke-width="2"/>'
            + lab(x, y - size * 0.55 + (0 if '||' in text else size * 0.55) + size * 0.36, text, size, INK, mix=True))
def q05():
    s = '<rect x="140" y="6" width="300" height="40" rx="8" fill="#E3E8F8" stroke="#8E9BD0" stroke-width="2"/>'
    s += lab(290, 34, '$\\ce{H2}$　　$\\ce{H2O}$　　$\\ce{CH4}$　　$\\ce{F2}$', 21, mix=True)
    s += '<line x1="290" y1="46" x2="290" y2="64" stroke="#5B6B7F" stroke-width="2"/>'
    s += diamond(290, 104, 200, 80, '비공유||전자쌍이||있는가?', 18)
    s += '<path d="M190 104 H125 V158" fill="none" stroke="#5B6B7F" stroke-width="2"/><path d="M390 104 H445 V158" fill="none" stroke="#5B6B7F" stroke-width="2"/>'
    s += lab(160, 96, '예', 19, MUTED, mix=True) + lab(420, 96, '아니요', 19, MUTED, mix=True)
    for x in (125, 445):
        s += diamond(x, 200, 180, 84, '무극성||공유 결합이||있는가?', 17)
        s += f'<path d="M{x - 90} 200 H{x - 95} V250" fill="none" stroke="#5B6B7F" stroke-width="2"/><path d="M{x + 90} 200 H{x + 95} V250" fill="none" stroke="#5B6B7F" stroke-width="2"/>'
        s += lab(x - 102, 190, '예', 18, MUTED, mix=True, anchor='end') + lab(x + 102, 190, '아니요', 18, MUTED, mix=True, anchor='start')
    ends = [(30, '(가)', '\\ce{F2}'), (220, '(나)', '\\ce{H2O}'), (350, '(다)', '\\ce{H2}'), (540, '(라)', '\\ce{CH4}')]
    for x, t, m in ends:
        s += f'<rect x="{x - 30}" y="250" width="60" height="32" rx="6" fill="#fff" stroke="#5B6B7F" stroke-width="2"/>' + lab(x, 273, t, 19, mix=True)
        s += f'<g class="step" data-g="e5">' + lab(x, 312, m, 22, FIELD) + '</g>'
    return s
F['Q05'] = q05()


# ───────── S12 06: CO2, CH2O, CCl4 ─────────
def q06():
    a = lambda d: (math.cos(math.radians(d)), math.sin(math.radians(d)), 0)
    s = ''
    m1 = ballstick(110, 100, 'C', ['O', 'O'], L=78, extra_bond_orders={0: 2, 1: 2}, lobes=False)
    m2 = ballstick(320, 104, 'C', ['O', 'H', 'H'], dirs=[a(90), a(212), a(328)], L=80, extra_bond_orders={0: 2}, lobes=False)
    m3 = ballstick(530, 104, 'C', ['Cl'] * 4, L=82, yaw=V4[0], pitch=V4[1], lobes=False)
    for i, (m, x, t) in enumerate([(m1, 110, '\\ce{CO2}'), (m2, 320, '\\ce{CH2O}'), (m3, 530, '\\ce{CCl4}')]):
        s += f'<g data-anim="pop" data-o="{x},100" data-dur=".6" data-delay="{.2 + .3 * i}">{m}</g>' + lab(x, 222, t, 22)
    return s
F['Q06'] = q06()


# ───────── S13 07: BeCl2, H2O ─────────
def q07():
    S = 34
    s = ''
    # 루이스 전자점식
    s += f'<g class="step" data-g="l7">'
    s += lewis_sym(54, 50, 'Cl', S, dots={'u': 2, 'd': 2, 'l': 2}) + lewis_sym(122, 50, 'Be', S, dots={'l': 2, 'r': 2}) + lewis_sym(190, 50, 'Cl', S, dots={'u': 2, 'd': 2, 'r': 2})
    s += lewis_sym(370, 50, 'H', S) + lewis_sym(420, 50, 'O', S, dots={'u': 2, 'd': 2, 'l': 2, 'r': 2}) + lewis_sym(470, 50, 'H', S)
    s += '</g>'
    s += f'<g class="step" data-g="m7">'
    s += ballstick(122, 168, 'Be', ['Cl', 'Cl'], L=80, arc=(0, 1), arc_label='180^\\circ', arc_r=40, lobes=False)
    s += ballstick(420, 150, 'O', ['H', 'H'], n_lone=2, L=80, arc=(0, 1), arc_label='104.5^\\circ', arc_r=34, lobes=True, arc_size=20)
    s += lab(122, 262, '선형', 20, MUTED, mix=True) + lab(420, 262, '굽은 형', 20, MUTED, mix=True) + '</g>'
    return s
F['Q07'] = q07()


# ───────── S14 08: X, Y와 (가)–(다) ─────────
def q08_given():
    S = 40
    return lewis_sym(60, 46, 'X', S, dots={'u': 2, 'd': 2, 'l': 2, 'r': 1}) + lewis_sym(190, 46, 'Y', S, dots={'u': 2, 'd': 2, 'l': 1, 'r': 1})
F['Q08G'] = q08_given()
def q08_ans():
    S = 32
    s = lewis_sym(40, 50, 'H', S) + lewis_sym(85, 50, 'X', S, dots={'u': 2, 'd': 2, 'r': 2, 'l': 2}) + lab(62, 118, '(가) HX', 19, MUTED, mix=True)
    s += lewis_sym(170, 50, 'H', S) + lewis_sym(215, 50, 'Y', S, dots={'u': 2, 'd': 2, 'l': 2, 'r': 2}) + lewis_sym(260, 50, 'H', S) + lab(215, 118, '(나) $\\mathrm{H_2Y}$', 19, MUTED, mix=True)
    s += (lewis_sym(340, 50, 'X', S, dots={'u': 2, 'd': 2, 'l': 2, 'r': 2}) + lewis_sym(385, 50, 'Y', S, dots={'u': 2, 'd': 2, 'r': 2})
          + lewis_sym(430, 50, 'X', S, dots={'u': 2, 'd': 2, 'r': 2}) + lab(385, 118, '(다) $\\mathrm{YX_2}$', 19, MUTED, mix=True))
    return s
F['Q08A'] = q08_ans()


# ───────── S15 09: 전기장 속 AB2 ─────────
def q09():
    W, H = 520, 290
    s = f'<rect x="20" y="40" width="14" height="{H - 60}" fill="#8C99A6"/><rect x="{W - 34}" y="40" width="14" height="{H - 60}" fill="#8C99A6"/>'
    s += lab(27, 30, '(−)극', 20, MINUS, mix=True) + lab(W - 27, 30, '(+)극', 20, PLUS, mix=True)
    pts = [(130, 85), (270, 78), (400, 92), (110, 165), (250, 160), (390, 172), (150, 240), (300, 235)]
    import random
    rr = random.Random(4)
    for k, (x, y) in enumerate(pts):
        t = math.radians(52)
        b1 = (x + math.cos(t) * 34, y - math.sin(t) * 34); b2 = (x + math.cos(t) * 34, y + math.sin(t) * 34)
        g = (f'<line x1="{x}" y1="{y}" x2="{f(b1[0])}" y2="{f(b1[1])}" stroke="#9AA5B1" stroke-width="6" stroke-linecap="round"/>'
             f'<line x1="{x}" y1="{y}" x2="{f(b2[0])}" y2="{f(b2[1])}" stroke="#9AA5B1" stroke-width="6" stroke-linecap="round"/>'
             f'<circle cx="{f(b1[0])}" cy="{f(b1[1])}" r="13" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><circle cx="{f(b2[0])}" cy="{f(b2[1])}" r="13" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/>'
             f'<circle cx="{x}" cy="{y}" r="17" fill="#7B4FC8" stroke="#4E2F8A" stroke-width="2"/>')
        rt = rr.choice([-60, 70, 110, -120]) + rr.uniform(-10, 10)
        a0 = rr.uniform(-6, 6)
        s += f'<g transform="rotate({f(a0)} {x} {y})"><g data-anim="rot" data-from="{f(rt)}" data-o="{x},{y}" data-dur="1.4" data-delay=".3" data-ease="soft">{g}</g></g>'
    s += '<circle cx="150" cy="282" r="11" fill="#7B4FC8" stroke="#4E2F8A" stroke-width="2"/>' + lab(168, 289, '\\mathrm{A}', 20, anchor='start')
    s += '<circle cx="230" cy="282" r="9" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/>' + lab(246, 289, '\\mathrm{B}', 20, anchor='start')
    return s
F['Q09'] = q09()
def q09cmp():
    s = ''
    # 선형 B–A–B
    y = 60
    s += bar(40, y, 160, y) + f'<circle cx="40" cy="{y}" r="13" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><circle cx="160" cy="{y}" r="13" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><circle cx="100" cy="{y}" r="17" fill="#7B4FC8" stroke="#4E2F8A" stroke-width="2"/>'
    s += arw(92, y - 34, 50, y - 34) + arw(108, y - 34, 150, y - 34)
    s += lab(100, y + 54, '선형: 합 $=0$', 19, MUTED, mix=True)
    # 굽은 형
    cx, cy = 290, 40
    t = math.radians(52)
    b1 = (cx - math.sin(t) * 52, cy + math.cos(t) * 52); b2 = (cx + math.sin(t) * 52, cy + math.cos(t) * 52)
    s += bar(cx, cy, *b1) + bar(cx, cy, *b2)
    s += f'<circle cx="{f(b1[0])}" cy="{f(b1[1])}" r="13" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><circle cx="{f(b2[0])}" cy="{f(b2[1])}" r="13" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="17" fill="#7B4FC8" stroke="#4E2F8A" stroke-width="2"/>'
    s += arw(cx, cy + 20, cx, cy + 58, 'plus', 5)
    s += lab(cx + 30, y + 54, '굽은 형: 합 $\\neq 0$', 19, MUTED, mix=True)
    return s
F['Q09C'] = q09cmp()


# ───────── S16 10: 루이스의 정육면체 ─────────
def cubes():
    s = ''
    for i, (el, n) in enumerate([('C', 4), ('N', 5), ('O', 6), ('F', 7)]):
        x0 = 30 + i * 150; y0 = 50; a = 76; dx, dy = 26, -22
        fr = [(x0, y0), (x0 + a, y0), (x0 + a, y0 + a), (x0, y0 + a)]
        bk = [(x + dx, y + dy) for x, y in fr]
        s += f'<polygon points="{" ".join(f"{f(x)},{f(y)}" for x, y in bk)}" fill="none" stroke="#9AA5B1" stroke-width="2"/>'
        for p, q in zip(fr, bk):
            s += f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" stroke="#9AA5B1" stroke-width="2"/>'
        s += f'<polygon points="{" ".join(f"{f(x)},{f(y)}" for x, y in fr)}" fill="none" stroke="{INK}" stroke-width="2.5"/>'
        verts = [fr[3], fr[2], bk[3], bk[2], fr[0], fr[1], bk[0], bk[1]]
        dots = ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="7" fill="{INK}"/>' for x, y in verts[:n])
        s += f'<g data-anim="pop" data-o="{f(x0 + a / 2 + 13)},{f(y0 + a / 2 - 11)}" data-dur=".6" data-delay="{.2 + .3 * i}">{dots}</g>'
        s += lab(x0 + a / 2 + 13, y0 + a + 40, f'\\mathrm{{{el}}}', 24) + lab(x0 + a / 2 + 13, y0 + a + 66, f'점 {n}개', 19, MUTED, mix=True)
    return s
F['CUBE'] = cubes()


# ───────── S18 11: 바다 위 기름 막 ─────────
def sea():
    s = '<rect x="0" y="0" width="440" height="80" fill="#F4F8FB"/><rect x="0" y="80" width="440" height="170" fill="#DDEEF8"/>'
    s += '<circle cx="380" cy="30" r="18" fill="#FFE45C" stroke="#E08A2C" stroke-width="2"/>'
    for x in (120, 200, 280):
        s += f'<g data-arw="{x + 40},14,{x},68,equi,2.5"></g>'
    s += '<g data-anim="scale" data-from=".15,1" data-o="220,82" data-dur="1.6" data-delay=".3" data-ease="out"><rect x="50" y="74" width="340" height="14" rx="7" fill="#F2C14E" stroke="#C9971E" stroke-width="1.5"/></g>'
    s += lab(220, 66, '기름 막', 20, '#8A6510', mix=True, extra=' data-halo="1"')
    s += '<path d="M330 190 q14 -10 28 0 q14 10 0 20 q-14 10 -28 0 q-14 -10 0 -20z" fill="#F2C14E" stroke="#C9971E" stroke-width="1.5"/>'
    s += lab(345, 236, '가라앉는 기름 덩어리', 19, MUTED, mix=True)
    # 물 분자 몇 개
    for x, y in ((70, 150), (150, 200), (230, 160)):
        s += bar(x, y, x - 14, y + 12, w=4) + bar(x, y, x + 14, y + 12, w=4) + f'<circle cx="{x}" cy="{y}" r="9" fill="#E5533D"/><circle cx="{x - 14}" cy="{y + 12}" r="6" fill="#F4F6F8" stroke="#8C99A6" stroke-width="1.2"/><circle cx="{x + 14}" cy="{y + 12}" r="6" fill="#F4F6F8" stroke="#8C99A6" stroke-width="1.2"/>'
    s += lab(150, 240, '물(극성)', 19, MUTED, mix=True)
    return s
F['SEA'] = sea()


# ───────── S20·S21 인지질 이중층 ─────────
HEAD, TAIL = '#F2A541', '#B39B6B'
def lipid(x, yh, down=True, r=10, tl=44):
    sgn = 1 if down else -1
    y1 = yh + sgn * r
    s = ''.join(f'<path d="M{x + o} {y1} q{3 * sgn} {tl / 4} 0 {tl / 2} q{-3 * sgn} {tl / 4} 0 {tl / 2 * sgn * sgn}" fill="none" stroke="{TAIL}" stroke-width="2.5"/>'
                for o in (-4, 4)) if False else ''
    for o in (-4, 4):
        s += f'<line x1="{x + o}" y1="{y1}" x2="{x + o}" y2="{y1 + sgn * tl}" stroke="{TAIL}" stroke-width="3" stroke-linecap="round"/>'
    s += f'<circle cx="{x}" cy="{yh}" r="{r}" fill="{HEAD}" stroke="#B9731E" stroke-width="1.5"/>'
    return s
def bilayer(W=520, top=60, gap=8, n=None, anim=True, x0=24, dx=26, tl=44):
    n = n or int((W - 2 * x0) / dx) + 1
    yt = top; yb = top + 2 * (10 + tl) + gap
    up = ''.join(lipid(x0 + i * dx, yt, True, tl=tl) for i in range(n))
    dn = ''.join(lipid(x0 + i * dx, yb, False, tl=tl) for i in range(n))
    s = f'<rect x="0" y="{yt + 10}" width="{W}" height="{yb - yt - 20}" fill="#FFF6E0"/>'
    if anim:
        s += f'<g data-anim="move" data-from="0,-34" data-dur="1.2" data-delay=".3" data-ease="out">{up}</g><g data-anim="move" data-from="0,34" data-dur="1.2" data-delay=".3" data-ease="out">{dn}</g>'
    else:
        s += up + dn
    return s, yt, yb
def s20():
    W = 520
    s = f'<rect x="0" y="0" width="{W}" height="270" fill="#DDEEF8"/>'
    b, yt, yb = bilayer(W, top=60)
    s += b
    s += lab(W / 2, 30, '물 (세포 밖)', 20, '#1F5F8B', mix=True) + lab(W / 2, 258, '물 (세포 안)', 20, '#1F5F8B', mix=True)
    s += lab(W / 2, (yt + yb) / 2 + 7, '무극성 환경', 20, '#8A6510', mix=True, extra=' data-halo="1"')
    return s
F['S20'] = s20()
def s21():
    W = 560
    s = f'<rect x="0" y="0" width="{W}" height="290" fill="#DDEEF8"/>'
    b, yt, yb = bilayer(W, top=80, anim=False, dx=28, tl=36)
    s += b
    s += lab(30, 40, '세포 밖', 19, '#1F5F8B', mix=True, anchor='start') + lab(30, 280, '세포 안', 19, '#1F5F8B', mix=True, anchor='start')
    # 통과
    for x, t in ((150, '\\ce{O2}'), (240, '\\ce{CO2}')):
        s += lab(x, 44, t, 22) + f'<g data-anim="move" data-from="0,-40" data-dur="1.4" data-delay=".4" data-ease="out"><g data-arw="{x},56,{x},262,field,3.5"></g></g>'
    # 막힘
    for x, t in ((340, '\\ce{K+}'), (420, '\\ce{Cl-}'), (510, '\\ce{C6H12O6}')):
        s += lab(x, 44, t, 22) + f'<g data-arw="{x},56,{x},{yt - 16},muted,3"></g>' + lab(x, yt - 1, '✕', 24, PLUS, mix=True, extra=' data-weight="700" data-halo="1"')
    return s
F['S21'] = s21()


# ───────── S22 비누 ─────────
def soap_glyph(x, y, ang, tl=26, r=6, head=HEAD):
    t = math.radians(ang)
    ux, uy = math.cos(t), math.sin(t)
    return (f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x + ux * tl)}" y2="{f(y + uy * tl)}" stroke="{TAIL}" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{f(x + ux * (tl + r))}" cy="{f(y + uy * (tl + r))}" r="{r}" fill="{head}" stroke="#B9731E" stroke-width="1.2"/>')
def soap_big():
    s = '<line x1="60" y1="70" x2="60" y2="200" stroke="#B39B6B" stroke-width="10" stroke-linecap="round"/><circle cx="60" cy="46" r="26" fill="#F2A541" stroke="#B9731E" stroke-width="2"/>'
    s += '<path d="M100 20 H108 V72 H100" fill="none" stroke="#5B6B7F" stroke-width="2"/>' + lab(116, 53, '극성 (친수성)', 19, MUTED, mix=True, anchor='start')
    s += '<path d="M100 82 H108 V200 H100" fill="none" stroke="#5B6B7F" stroke-width="2"/>' + lab(116, 140, '무극성 (소수성)', 19, MUTED, mix=True, anchor='start')
    return s
F['SOAP'] = soap_big()
def wash(k):
    s = '<rect x="0" y="0" width="300" height="170" fill="#DDEEF8"/><rect x="0" y="142" width="300" height="28" fill="#D9C7A8"/>'
    if k == 1:
        s += '<path d="M90 142 Q90 96 150 96 Q210 96 210 142 Z" fill="#F2C14E" stroke="#C9971E" stroke-width="1.5"/>'
        g = ''.join(soap_glyph(150 + 42 * math.cos(math.radians(a)), 142 - 33 * math.sin(math.radians(a)), -a, 26) for a in (20, 50, 90, 130, 160))
        s += f'<g data-anim="move" data-from="0,-30" data-dur="1.1" data-delay=".3" data-ease="out">{g}</g>'
        s += ''.join(soap_glyph(x, y, a, 20) for x, y, a in ((40, 40, 200), (260, 50, -30)))
    elif k == 2:
        g = '<path d="M110 120 Q100 70 160 64 Q220 70 205 118 Q180 140 150 136 Q120 136 110 120 Z" fill="#F2C14E" stroke="#C9971E" stroke-width="1.5"/>'
        g += ''.join(soap_glyph(157 + 36 * math.cos(math.radians(a)), 100 - 27 * math.sin(math.radians(a)), -a, 28) for a in (0, 40, 90, 140, 180, 220, 320))
        s += f'<g data-anim="move" data-from="0,26" data-dur="1.2" data-delay=".3" data-ease="out">{g}</g>'
    else:
        g = '<circle cx="150" cy="78" r="26" fill="#F2C14E" stroke="#C9971E" stroke-width="1.5"/>'
        g += ''.join(soap_glyph(150 + 22 * math.cos(math.radians(a)), 78 + 22 * math.sin(math.radians(a)), a, 22) for a in range(0, 360, 36))
        s += f'<g data-anim="move" data-from="-60,30" data-dur="1.4" data-delay=".3" data-ease="out">{g}</g>'
    return s
for k in (1, 2, 3):
    F[f'W{k}'] = wash(k)


# ───────── 끼워 넣기 ─────────
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, 'slides.tpl.html'), encoding='utf-8').read()
miss = set(re.findall(r'@@([A-Za-z0-9_]+)@@', tpl)) - set(F)
if miss:
    print('없는 그림', miss)
out = re.sub(r'@@([A-Za-z0-9_]+)@@', lambda m: F.get(m.group(1), ''), tpl)
dst = "/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학_미래엔_2-M/regen.html"
open(dst, 'w', encoding='utf-8').write(out)
print('ok', len(out), 'V4', V4)
