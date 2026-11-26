# 3-2 탄소 화합물의 화학 반응 — slides.tpl.html 의 @@이름@@ 자리에 그림 SVG 내용을 넣어 slides.html 을 만든다.
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학반응의세계_미래엔/3-2_탄소_화합물의_화학_반응/slides.html'
import sys as _s; OUT = _s.argv[1] if len(_s.argv)>1 else OUT
F = {}
OX, RD, FIELD, PLUS, MINUS, GRAV = '#C2410C', '#0E7490', '#2E9E6A', '#D7263D', '#1F6FD1', '#8C99A6'
ORG, GRN = '#F2B32A', '#3E9A6A'


def T(x, y, mix, size=20, anchor='middle', fill=None, weight=None, extra='', halo=False):
    if '<b>' in mix:
        mix = mix.replace('<b>', '').replace('</b>', ''); weight = weight or 700
    fl = f' fill="{fill}"' if fill else ''
    w = f' data-weight="{weight}"' if weight else ''
    h = ' data-halo="1"' if halo else ''
    return f'<text class="tex"{extra} x="{f(x)}" y="{f(y)}" data-mix="{mix}" data-size="{size}" data-anchor="{anchor}"{fl}{w}{h}></text>'


def arw(x1, y1, x2, y2, col='ox', w=3, extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}"{extra}></g>'


def eq_arrow(x, y, w=44, col=INK):
    """가역 화살표 ⇌ (반쪽 화살촉 두 줄)"""
    return (f'<path d="M{f(x - w / 2)} {f(y - 5)} H{f(x + w / 2)} l-10 -8" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M{f(x + w / 2)} {f(y + 5)} H{f(x - w / 2)} l10 8" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')


# ── 표지: 아세트알데하이드 공-막대 ──
a, b = mol_alkane_like(2, 'CHO')
body, P = bs3d(a, b, 270, 245, k=95, yaw='auto', sc=1.45, anim='out')
ci = [i for i, (el, _) in enumerate(a) if el == 'O'][0]
# 포밀기 중심: O와 그 C, 그리고 그 C의 H
cx_ = sum(P[i][0] for i in range(len(a)) if i in (1, ci)) / 2
cy_ = sum(P[i][1] for i in range(len(a)) if i in (1, ci)) / 2
F['COVER'] = (f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>{body}'
              f'<circle cx="{f(cx_)}" cy="{f(cy_)}" r="92" fill="none" stroke="{EQUI}" stroke-width="3" stroke-dasharray="8 6" data-anim="fade" data-dur=".8" data-delay="1.5"/>'
              + T(270, 482, '아세트알데하이드 $\\ce{CH3CHO}$', 23, fill=INK, weight=700)
              + T(270, 514, '에탄올이 산화되어 생긴 물질', 20, fill=MUTED))


# ── S3 매실청 유리병 ──
def jar():
    s = ''
    s += '<rect x="110" y="40" width="200" height="36" rx="8" fill="#8A919C" stroke="#5B6B7F" stroke-width="2"/>'
    s += '<path d="M100 92 Q100 76 118 76 H302 Q320 76 320 92 V290 Q320 312 298 312 H122 Q100 312 100 290 Z" fill="#F7E7B5" fill-opacity=".9" stroke="#7E8B98" stroke-width="3"/>'
    s += '<path d="M104 130 H316" stroke="#E2C77A" stroke-width="2"/>'
    for (x, y) in ((150, 270), (200, 285), (255, 272), (175, 235), (235, 240), (285, 240), (140, 200), (205, 195), (265, 200), (165, 160), (245, 160)):
        s += f'<circle cx="{x}" cy="{y}" r="22" fill="#9CC46B" stroke="#6E9440" stroke-width="2"/>'
    k = 0
    for (x, y, r) in ((128, 225, 5), (300, 210, 6), (222, 150, 5), (190, 260, 4), (310, 160, 4)):
        s += (f'<g data-anim="move" data-from="0,60" data-dur="2.4" data-delay="{.2 + .4 * k:.1f}" data-rep="loop" data-ease="lin">'
              f'<circle cx="{x}" cy="{y - 70}" r="{r}" fill="#fff" stroke="#7E8B98" stroke-width="1.5"/></g>')
        k += 1
    s += T(210, 342, '오래 보관한 매실청', 20, fill=MUTED)
    s += T(360, 70, '기포', 20, anchor='start', fill=INK)
    s += f'<line x1="355" y1="76" x2="312" y2="110" stroke="{MUTED}" stroke-width="2"/>'
    s += T(338, 160, '술 냄새?', 20, anchor='start', fill=INK)
    s += T(338, 194, '시큼한 맛?', 20, anchor='start', fill=INK)
    return s
F['JAR'] = jar()


# ── S5 발효: 막걸리 병 / 입자 / 식 ──
def bottle():
    s = '<path d="M120 20 h40 v34 q30 18 30 52 v100 q0 14 -14 14 h-72 q-14 0 -14 -14 v-100 q0 -34 30 -52 z" fill="#F4F1E8" stroke="#7E8B98" stroke-width="3"/>'
    s += '<rect x="116" y="8" width="48" height="16" rx="4" fill="#2E9E6A"/>'
    s += '<path d="M93 120 h94 v96 q0 10 -10 10 h-74 q-10 0 -10 -10 z" fill="#FFFFFF" stroke="none"/>'
    for k, (x, y) in enumerate(((115, 200), (150, 190), (170, 210), (135, 170))):
        s += (f'<g data-anim="move" data-from="0,40" data-dur="1.8" data-delay="{.3 * k:.1f}" data-rep="loop" data-ease="lin">'
              f'<circle cx="{x}" cy="{y - 40}" r="4" fill="#fff" stroke="#7E8B98" stroke-width="1.4"/></g>')
    s += T(140, 262, '막걸리', 28, fill=INK, weight=700)
    return s
F['BOTTLE'] = bottle()


def fermen():
    s = ''
    # 포도당 아이콘
    s += '<polygon points="70,40 115,66 115,118 70,144 25,118 25,66" fill="#FFF3D6" stroke="#E08A2C" stroke-width="3"/>'
    s += T(70, 100, '포도당', 22, fill=INK, weight=700)
    s += T(70, 184, '1 분자', 21, fill=MUTED)
    s += arw(132, 92, 182, 92, 'ink', 3)
    # 에탄올 2, 이산화 탄소 2
    ae, be = mol_alkane_like(2, 'OH')
    k = 0
    for (cx, cy) in ((262, 52), (262, 146)):
        bdy, _ = bs3d(ae, be, cx, cy, k=36, yaw='auto', sc=.55, labels=False)
        s += f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.4 + .2 * k:.1f}" data-ease="back">{bdy}</g>'; k += 1
    co = [('O', (-1.16, 0, 0)), ('C', (0, 0, 0)), ('O', (1.16, 0, 0))]
    for (cx, cy) in ((415, 52), (415, 146)):
        bdy, _ = bs3d(co, [(0, 1, 2), (1, 2, 2)], cx, cy, k=36, yaw=0, pitch=0, sc=.55, labels=False)
        s += f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".6" data-delay="{.4 + .2 * k:.1f}" data-ease="back">{bdy}</g>'; k += 1
    s += T(262, 214, '에탄올 2', 21, fill=MUTED)
    s += T(415, 214, '이산화 탄소 2', 21, fill=MUTED)
    s += T(340, 108, '+', 28, fill=INK)
    return s
F['FERM'] = fermen()


# ── 구조식 세 개 + 산화 화살표 ──
def three(specs, W, y0, d=56, S=26, gap=110, g0='a', names=None, labels=None, ox_lab=True):
    widths = [chain_width(n, fg, d) for n, fg in specs]
    total = sum(widths) + gap * (len(specs) - 1)
    x = (W - total) / 2
    s = ''
    xs = []
    for k, ((n, fg), w) in enumerate(zip(specs, widths)):
        lab = labels[k] if labels else None
        s += chain_svg(n, fg, x, y0, d, S, g=f'{g0}{k + 1}', label=lab, lab_size=20, box_anim=' data-anim="draw" data-on="step" data-dur=".8"')
        xs.append((x, x + w))
        if names:
            s += T(x + w / 2, y0 + d + 52, names[k], 21, fill=INK, weight=700)
        x += w + gap
    for k in range(len(specs) - 1):
        x1, x2 = xs[k][1] + 22, xs[k + 1][0] - 22
        s += arw(x1, y0, x2, y0, 'ox', 4, f' data-anim="draw" data-dur=".7" data-delay="{.3 + .5 * k:.1f}"')
        if ox_lab:
            s += T((x1 + x2) / 2, y0 - 14, '<b>산화</b>', 20, fill=OX)
    return s


F['ETOX'] = three([(2, 'OH'), (2, 'CHO'), (2, 'COOH')], 1040, 120, names=['에탄올', '아세트알데하이드', '아세트산'],
                  labels=['$\\ce{-OH}$', '$\\ce{-CHO}$', '$\\ce{-COOH}$'], g0='e')
F['MEOX'] = three([(1, 'OH'), (1, 'CHO'), (1, 'COOH')], 900, 116, names=['메탄올', '폼알데하이드', '폼산'],
                  labels=['$\\ce{-OH}$', '$\\ce{-CHO}$', '$\\ce{-COOH}$'], g0='m')


# ── S7 공-막대: H 2개 떠남, O 1개 붙음 ──
def s7():
    s = ''
    mols = [mol_alkane_like(2, 'OH'), mol_alkane_like(2, 'CHO'), mol_alkane_like(2, 'COOH')]
    cxs = [150, 500, 850]
    for k, ((aa, bb), cx) in enumerate(zip(mols, cxs)):
        bdy, _ = bs3d(aa, bb, cx, 128, k=60, yaw='auto', sc=.86)
        s += bdy
    s += T(150, 240, '에탄올 $\\ce{C2H6O}$', 21, fill=INK)
    s += T(500, 240, '아세트알데하이드 $\\ce{C2H4O}$', 21, fill=INK)
    s += T(850, 240, '아세트산 $\\ce{C2H4O2}$', 21, fill=INK)
    for k, (x1, x2) in enumerate(((268, 378), (622, 728))):
        s += arw(x1, 140, x2, 140, 'ox', 4)
        s += T((x1 + x2) / 2, 176, '<b>산화</b>', 20, fill=OX)
    # 떠나는 H 2개
    s += ('<g data-anim="move" data-from="-60,40" data-dur="1.2" data-delay=".4" data-ease="out">'
          '<g data-atom="304,82,14.4,H,-"></g><g data-atom="340,82,14.4,H,-"></g></g>')
    s += T(362, 90, '$\\ce{H}$ 2개 잃음', 19, anchor='start', fill=OX)
    # 붙는 O 1개
    s += ('<g data-anim="move" data-from="0,-50" data-dur="1.2" data-delay="1.2" data-ease="out">'
          '<g data-atom="660,92,19.2,O"></g></g>')
    s += T(686, 100, '$\\ce{O}$ 1개 얻음', 19, anchor='start', fill=OX)
    return s
F['S7'] = s7()


# ── S8 작은 공-막대 세 개 ──
def small(n, fg):
    aa, bb = mol_alkane_like(n, fg)
    bdy, _ = bs3d(aa, bb, 150, 108, k=48, yaw='auto', sc=.9)
    return bdy
F['M_OH'] = small(2, 'OH'); F['M_CHO'] = small(2, 'CHO'); F['M_COOH'] = small(2, 'COOH')


# ── S14 은거울 반응식 (구조식) ──
def silver():
    d, S, y0 = 54, 26, 120
    s = ''
    x0 = 24
    s += chain_svg(2, 'CHO', x0, y0, d, S, label=None)
    ax1 = x0 + 3 * d
    s += T(ax1 + 22, y0 + 9, '$\\ce{+ 2Ag+ + 2OH-}$', 26, anchor='start', fill=INK)
    s += arw(ax1 + 250, y0, ax1 + 320, y0, 'ink', 3)
    x1 = ax1 + 344
    s += chain_svg(2, 'COOH', x1, y0, d, S, label=None)
    ax2 = x1 + 4 * d
    s += T(ax2 + 20, y0 + 9, '$\\ce{+ 2Ag + H2O}$', 26, anchor='start', fill=INK)
    # 은 원자 두 개 (생성)
    for k, x in enumerate((ax2 + 64, ax2 + 98)):
        s += f'<g data-anim="pop" data-o="{x},{y0 - 40}" data-dur=".6" data-delay="{.8 + .25 * k:.2f}" data-ease="back"><g data-atom="{x},{y0 - 40},15,Ag,-"></g></g>'
    # 산화 괄호 (아래)
    xa, xb = x0 + 2 * d, x1 + 2 * d
    s += f'<path d="M{xa} {y0 + 44} V{y0 + 74} H{xb} V{y0 + 44}" fill="none" stroke="{OX}" stroke-width="2.5"/>'
    s += T((xa + xb) / 2, y0 + 82, '<b>산화</b> $\\ce{-CHO -> -COOH}$', 21, fill=OX, halo=True)
    # 환원 괄호 (위)
    xc, xd = ax1 + 68, ax2 + 80
    s += f'<path d="M{xc} {y0 - 22} V{y0 - 88} H{xd} V{y0 - 64}" fill="none" stroke="{RD}" stroke-width="2.5"/>'
    s += T((xc + xd) / 2, y0 - 80, '<b>환원</b> $\\ce{Ag+ -> Ag}$', 21, fill=RD, halo=True)
    s += T(x0 + 1.5 * d, y0 + 128, '아세트알데하이드', 20, fill=MUTED)
    s += T(x1 + 2 * d, y0 + 128, '아세트산', 20, fill=MUTED)
    return s
F['SILVER'] = silver()


# ── S15 포도당 고리 ⇌ 사슬 ──
def ring():
    S = 24
    A = [('O', 240, 150), ('C', 240, 236), ('C', 170, 276), ('C', 100, 236), ('C', 100, 150), ('C', 170, 110),
         ('CH2OH', 170, 40), ('OH', 312, 270), ('OH', 170, 350), ('HO', 32, 270), ('HO', 32, 116)]
    B = [(5, 0, 1), (0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1), (1, 7, 1), (2, 8, 1), (3, 9, 1), (4, 10, 1)]
    s = ''
    boxes = [(170 + 4, 40 - 16, 42, 32), (312 - 22, 270 - 16, 44, 32), (170 - 22, 350 - 16, 44, 32), (32 - 22, 270 - 16, 44, 32), (32 - 22, 116 - 16, 44, 32)]
    for (x, y, w, h) in boxes:
        s += box(x, y, w, h, g='r1', anim=' data-anim="draw" data-on="step" data-dur=".7"')
    s += sf(A, B, S)
    s += T(170, 396, '고리 구조 (고리의 $\\ce{H}$ 생략)', 19, fill=MUTED)
    return s


def chainG():
    S, d, x = 22, 46, 110
    A, B = [], []
    def ad(sym, xx, yy):
        A.append((sym, xx, yy)); return len(A) - 1
    c1 = ad('C', x, 70); o = ad('O', x, 24); B.append((c1, o, 2)); h = ad('H', x + d, 70); B.append((c1, h, 1))
    prev = c1
    rows = [('H', 'OH'), ('HO', 'H'), ('H', 'OH'), ('H', 'OH')]
    oh_pos = []
    for k, (l, r) in enumerate(rows):
        y = 116 + 46 * k
        c = ad('C', x, y); B.append((prev, c, 1))
        li = ad(l, x - d, y); B.append((c, li, 1))
        ri = ad(r, x + d, y); B.append((c, ri, 1))
        oh_pos.append((x + d, y) if r == 'OH' else (x - d, y))
        prev = c
    c6 = ad('C', x, 300); B.append((prev, c6, 1))
    B.append((c6, ad('H', x - d, 300), 1)); B.append((c6, ad('H', x + d, 300), 1))
    oo = ad('OH', x, 346); B.append((c6, oo, 1)); oh_pos.append((x, 346))
    s = ''
    for (xx, yy) in oh_pos:
        s += box(xx - 20, yy - 15, 40, 30, g='r1', anim=' data-anim="draw" data-on="step" data-dur=".7"')
    s += box(x - 16, 24 - 16, d + 32, 46 + 32, g='r2', cls='', anim=' data-anim="draw" data-on="step" data-dur=".7"')
    s += sf(A, B, S)
    s += T(x + 6, 396, '사슬 구조', 19, fill=MUTED)
    return s
F['RING'] = ring(); F['CHAIN'] = chainG(); F['EQARR'] = eq_arrow(40, 60, 56)


# ── S16 과정 카드 ──
def vial(x, y, w=70, h=110, liq=None, liqh=50, cap=False, extra=''):
    s = ''
    if liq:
        s += f'<rect x="{x + 3}" y="{y + h - liqh}" width="{w - 6}" height="{liqh - 3}" rx="6" fill="{liq}"/>'
    s += f'<path d="M{x} {y} V{y + h - 8} q0 8 8 8 h{w - 16} q8 0 8 -8 V{y}" fill="none" stroke="#7E8B98" stroke-width="3"/>'
    if cap:
        s += f'<rect x="{x - 4}" y="{y - 18}" width="{w + 8}" height="20" rx="4" fill="#16233D"/>'
    return s + extra


def p1():
    s = vial(110, 80, liq='#EEF3F8', liqh=56)
    s += '<ellipse cx="145" cy="168" rx="22" ry="8" fill="#7A4E2D" fill-opacity=".55"/>'
    s += '<path d="M139 6 h12 v40 l-6 14 l-6 -14 z" fill="#DDEEF8" stroke="#7E8B98" stroke-width="2"/><rect x="134" y="0" width="22" height="12" rx="4" fill="#5B6B7F"/>'
    s += '<g data-anim="move" data-from="0,-40" data-dur="1" data-delay=".3" data-rep="loop" data-ease="in"><path d="M145 106 q-6 9 0 13 q6 -4 0 -13z" fill="#9FC3DD"/></g>'
    s += T(178, 40, '진한 암모니아수', 25, anchor='start', fill=INK)
    s += T(190, 176, '갈색 앙금', 25, anchor='start', fill='#7A4E2D')
    s += T(145, 226, '질산 은 수용액', 25, fill=MUTED)
    return s


def p2():
    s = vial(115, 70, liq='#EEF3F8', liqh=84, cap=True)
    s += T(150, 226, '포도당 + KOH', 25, fill=MUTED)
    s += T(150, 36, '2 mL씩', 25, fill=INK)
    return s


def p3():
    s = '<path d="M60 70 V200 q0 10 10 10 H230 q10 0 10 -10 V70" fill="#FDE2E4" fill-opacity=".8" stroke="#7E8B98" stroke-width="3"/>'
    s += '<rect x="63" y="100" width="174" height="106" fill="#F9C9CF" fill-opacity=".6"/>'
    s += vial(115, 80, w=70, h=110, liq='#EEF3F8', liqh=84, cap=True)
    for x in (90, 150, 210):
        s += f'<path d="M{x} 60 q-8 -12 0 -24 q8 -12 0 -24" fill="none" stroke="{MUTED}" stroke-width="2" data-anim="fade" data-rep="alt" data-dur="1.2"/>'
    s += T(150, 240, '60 °C 물', 25, fill=MUTED)
    return s
F['P1'] = p1(); F['P2'] = p2(); F['P3'] = p3()


# ── S19 / S21 음주 측정기 관 ──
def tube(green=0, anim=False):
    s = ''
    x0, x1, y = 90, 860, 60
    s += f'<rect x="{x0}" y="{y - 30}" width="{x1 - x0}" height="60" rx="14" fill="#F7F9FB" stroke="#7E8B98" stroke-width="3"/>'
    s += f'<rect x="{x0 - 40}" y="{y - 26}" width="44" height="52" rx="8" fill="#16233D"/>'
    s += f'<rect x="{x1 - 4}" y="{y - 26}" width="44" height="52" rx="8" fill="#16233D"/>'
    gx0, gx1 = 110, 700
    s += f'<rect x="{gx0}" y="{y - 24}" width="{gx1 - gx0}" height="48" rx="8" fill="{ORG}"/>'
    if green:
        gw = (gx1 - gx0) * green
        an = ' data-anim="fade" data-dur="1.6" data-delay=".5"' if anim else ''
        s += f'<rect x="{gx1 - gw}" y="{y - 24}" width="{gw}" height="48" rx="8" fill="{GRN}"{an}/>'
    for k in range(14):
        s += f'<circle cx="{120 + 42 * k}" cy="{y - 8 + 16 * (k % 2)}" r="4" fill="#fff" fill-opacity=".45"/>'
    s += f'<path d="M725 {y} q12 -26 34 -16 q20 -18 40 0 q24 -6 30 16 q8 22 -14 26 q-14 18 -38 8 q-26 12 -40 -8 q-20 -4 -12 -26z" fill="#FFFFFF" stroke="#9AA5B1" stroke-width="2"/>'
    s += T(405, y + 64, '다이크로뮴산 칼륨 + 황산 용액을 흡수시킨 실리카 젤', 19, fill=MUTED)
    s += T(780, y + 64, '에탄올을 적신 솜', 19, fill=MUTED)
    s += T(70, y + 64, '마개', 19, fill=MUTED)
    return s
F['TUBE0'] = tube(0)
F['TUBE1'] = tube(.42, True)


# ── S24 시약병 ──
def reagent():
    s = '<rect x="98" y="16" width="64" height="30" rx="6" fill="#5B6B7F"/>'
    s += '<path d="M110 46 h40 v24 q60 20 60 70 v130 q0 14 -14 14 h-132 q-14 0 -14 -14 v-130 q0 -50 60 -70 z" fill="#E9D9B8" fill-opacity=".7" stroke="#7E8B98" stroke-width="3"/>'
    s += '<rect x="66" y="140" width="128" height="94" rx="6" fill="#fff" stroke="#9AA5B1" stroke-width="2"/>'
    s += T(92, 180, '<b>아세트</b>', 22, anchor='start', fill=INK)
    s += T(92, 218, '$\\ce{CH3C}$', 22, anchor='start', fill=INK)
    s += '<path d="M150 146 q20 30 0 50 q22 18 6 34 L194 232 V140 Z" fill="#E9D9B8" stroke="none"/>'
    return s
F['REAGENT'] = reagent()

# ── S22 은거울 본뜨기 / 전자식 음주 측정기 ──
def star(cx, cy, R, r):
    pts = []
    for k in range(10):
        a = math.radians(-90 + 36 * k); rr = R if k % 2 == 0 else r
        pts.append(f'{f(cx + rr * math.cos(a))},{f(cy + rr * math.sin(a))}')
    return ' '.join(pts)


def stencil():
    s = '<rect x="20" y="30" width="150" height="110" rx="6" fill="#EEF6FB" stroke="#7E8B98" stroke-width="3"/>'
    s += f'<polygon points="{star(95, 85, 40, 17)}" fill="#F2C230" stroke="#B58E12" stroke-width="2"/>'
    s += T(95, 172, '스티커 붙이기', 21, fill=MUTED)
    s += arw(186, 85, 236, 85, 'ink', 3)
    s += '<g data-anim="fade" data-dur="1.2" data-delay=".6"><rect x="252" y="30" width="150" height="110" rx="6" fill="#AEB4BD" stroke="#8A919C" stroke-width="3"/>'
    s += f'<polygon points="{star(327, 85, 40, 17)}" fill="#EEF6FB" stroke="#8A919C" stroke-width="2"/></g>'
    s += T(327, 172, '은거울 반응 뒤 떼기', 21, fill=MUTED)
    return s


def breath():
    s = '<rect x="150" y="30" width="200" height="120" rx="16" fill="#F7F9FB" stroke="#7E8B98" stroke-width="3"/>'
    s += '<rect x="20" y="78" width="130" height="24" rx="8" fill="#DDEEF8" stroke="#9FC3DD" stroke-width="2"/>'
    s += '<g data-anim="move" data-from="-90,0" data-dur="1.4" data-rep="loop" data-ease="lin" data-flow="1"><circle cx="120" cy="90" r="5" fill="#9FB0C2"/><circle cx="96" cy="90" r="5" fill="#9FB0C2"/></g>'
    s += T(70, 66, '날숨', 21, fill=MUTED)
    s += '<rect x="170" y="50" width="16" height="80" fill="#5B6B7F"/><rect x="314" y="50" width="16" height="80" fill="#5B6B7F"/>'
    s += T(250, 82, '에탄올 산화', 20, fill=OX)
    s += T(250, 116, '→ 전류', 20, fill=INK)
    s += '<rect x="196" y="156" width="108" height="40" rx="6" fill="#16233D"/>'
    s += T(250, 184, '0.03 %', 22, fill='#8FE3B0', weight=700)
    return s
F['STENCIL'] = stencil(); F['BREATH'] = breath()


tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
left = re.findall(r'@@\w+@@', out)
assert not left, left
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', len(out))
