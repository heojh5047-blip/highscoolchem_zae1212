# 4-1-2 pH 덱 그림 생성 — python3 -I gen.py <출력 slides.html>
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

FIG = {}
UI = ['#C62828', '#E53935', '#F4511E', '#FB8C00', '#FDD835', '#C0CA33', '#7CB342', '#43A047',
      '#00897B', '#0097A7', '#1E88E5', '#3949AB', '#5E35B1', '#6A1B9A', '#4A148C']
LP = '#FDE8EA'; LM = '#E3EEFB'
KW = 1e-14


def th_pH(C, base=False):
    h = (C + math.sqrt(C * C + 4 * KW)) / 2
    return 14 + math.log10(h) if base else -math.log10(h)


def svg(vb, w, label, body, extra=''):
    return f'<svg class="fig" viewBox="{vb}" style="width:{w}px" aria-label="{label}"{extra}>{body}</svg>'


def meter(x, y, w, h, reading, size=26):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#EEF2F6" stroke="{INK}" stroke-width="2"/>',
         f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="{h-40}" rx="5" fill="#E3F2E9" stroke="{INK}" stroke-width="1.5"/>',
         tex(x + w / 2, y + 14 + (h - 40) / 2 + size * 0.36, reading, size=size, weight=700)]
    return ''.join(o)


def probe(x, top, bot):
    return (f'<rect x="{x-6}" y="{top}" width="12" height="{bot-top-14}" rx="4" fill="#C9D3DD" stroke="{INK}" stroke-width="1.5"/>'
            f'<ellipse cx="{x}" cy="{bot-10}" rx="9" ry="12" fill="#F4F9FD" stroke="{INK}" stroke-width="1.5"/>')


# ───── 1 표지 ─────
def cover():
    o = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    o.append(beaker(130, 400, 200, 190, 250, WATER, WATER_S, ticks=3))
    o.append(meter(300, 70, 180, 100, '\\text{pH}\\ 3.00', 30))
    o.append('<g data-anim="move" data-from="0,-60" data-dur="1.2" data-delay=".3" data-ease="out">')
    o.append(f'<path d="M390,170 C390,215 250,140 250,175" fill="none" stroke="{INK}" stroke-width="3"/>')
    o.append(probe(250, 175, 385))
    o.append('</g>')
    o.append('<g data-anim="pop" data-o="270,440" data-dur=".9" data-delay=".9" data-ease="back">')
    for i in range(15):
        o.append(f'<rect x="{150+i*16}" y="420" width="16" height="28" fill="{UI[i]}"/>')
    o.append(f'<rect x="150" y="420" width="240" height="28" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    for p in (0, 7, 14):
        o.append(tex(158 + p * 16, 476, str(p), size=22, weight=700))
    o.append('</g>')
    o.append(tex(230, 300, '\\ce{HCl(aq)}', size=24, fill=MUTED))
    return f'<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="염산에 pH 측정기 전극을 담가 pH 3.00을 읽는 모습과 pH 0–14 색표">{"".join(o)}</svg>'
FIG['cover'] = cover()


# ───── 3 생각 열기 칠판 ─────
def board3():
    o = [f'<rect x="10" y="10" width="560" height="190" rx="10" fill="#2F5D50" stroke="#8B6B43" stroke-width="10"/>']
    o.append(tex(290, 80, '[\\ce{H+}]=0.0000000001\\ \\text{M}', size=32, fill='#FFFFFF'))
    o.append('<g data-anim="fade" data-dur=".8" data-delay=".9">')
    o.append(tex(290, 150, mix='이면 $[\\ce{OH-}]$는?', size=30, fill='#FFF6B0'))
    o.append('</g>')
    return svg('0 0 580 210', 560, '칠판에 수소 이온 농도 0.0000000001 M이 적혀 있다', ''.join(o))
FIG['board3'] = board3()


# ───── 5 양면 자 ─────
def ruler():
    x0, U, y = 130, 54, 85
    o = [f'<line x1="{x0}" y1="{y}" x2="{x0+14*U}" y2="{y}" stroke="{INK}" stroke-width="2.5"/>']
    for p in range(15):
        x = x0 + p * U
        o.append(f'<line x1="{x}" y1="{y-8}" x2="{x}" y2="{y+8}" stroke="{INK}" stroke-width="2"/>')
        o.append(tex(x, 120, str(p), size=20, weight=700))
        if p % 2 == 0:
            o.append(tex(x, 62, f'10^{{{-p if p else 0}}}', size=19, fill=PLUS))
    o.append(tex(102, 62, '[\\ce{H+}]', size=20, anchor='end', fill=PLUS, weight=700))
    o.append(tex(102, 120, '\\text{pH}', size=20, anchor='end', weight=700))
    o.append('<g data-anim="pop" data-o="' + f'{x0+4*U},{y}' + '" data-dur=".8" data-delay=".8" data-ease="back">')
    o.append(f'<rect x="{x0+4*U-34}" y="38" width="68" height="94" rx="10" fill="none" stroke="{EQUI}" stroke-width="3"/>')
    o.append('</g>')
    return svg('0 0 920 140', 900, '수소 이온 농도와 pH를 나란히 적은 양면 자', ''.join(o))
FIG['ruler'] = ruler()


# ───── 6 14칸 막대 (중성) ─────
def bar14(ph, w=520, y=10, lab=True, anim=True, U=None, x0=0):
    U = U or w / 14
    o = []
    a = f' data-anim="scale" data-from="0,1" data-o="{f(x0)},{y}" data-dur="1" data-delay=".4" data-ease="out"' if anim else ''
    o.append(f'<g{a}><rect x="{f(x0)}" y="{y}" width="{f(ph*U)}" height="38" fill="{PLUS}" opacity=".85"/></g>')
    o.append(f'<rect x="{f(x0+ph*U)}" y="{y}" width="{f((14-ph)*U)}" height="38" fill="{MINUS}" opacity=".85"/>')
    o.append(f'<rect x="{f(x0)}" y="{y}" width="{f(14*U)}" height="38" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    if lab:
        o.append(tex(x0 + ph * U / 2, y + 26, f'\\text{{pH}}\\ {ph}', size=20, fill='#FFFFFF', weight=700))
        o.append(tex(x0 + ph * U + (14 - ph) * U / 2, y + 26, f'\\text{{pOH}}\\ {14-ph}', size=20, fill='#FFFFFF', weight=700))
    return ''.join(o)


def neutral_bar():
    o = [bar14(7, U=36, x0=20, y=14)]
    for p in (0, 7, 14):
        o.append(tex(20 + p * 36, 80, str(p), size=19, fill=MUTED))
    o.append(tex(272, 112, mix='막대 전체 = 14.00 (25 °C)', size=19, fill=MUTED))
    return svg('0 0 544 124', 520, '길이 14인 막대를 pH 7과 pOH 7이 나누어 가진다', ''.join(o))
FIG['nbar'] = neutral_bar()


# ───── 7 pH 측정기와 pH 시험지 ─────
def measure():
    o = [beaker(55, 300, 130, 130, 205, '#FFF6D9', '#E8D9A0', ticks=2)]
    o.append(meter(20, 20, 170, 96, '\\text{pH}\\ 4.00', 26))
    o.append('<g data-anim="move" data-from="0,-45" data-dur="1.1" data-delay=".3" data-ease="out">')
    o.append(f'<path d="M105,116 C105,140 140,130 140,150" fill="none" stroke="{INK}" stroke-width="3"/>')
    o.append(probe(140, 150, 290))
    o.append('</g>')
    o.append(tex(110, 326, mix='pH 측정기', size=20, weight=700))
    # 시험지
    o.append(f'<rect x="262" y="40" width="30" height="190" rx="3" fill="#FBFBF6" stroke="{MUTED}" stroke-width="1.5"/>')
    o.append(f'<g data-anim="fade" data-dur="1" data-delay="1"><rect x="262" y="170" width="30" height="60" rx="3" fill="{UI[4]}" stroke="{MUTED}" stroke-width="1.5"/></g>')
    o.append(tex(277, 262, mix='pH 시험지', size=20, weight=700))
    for i in range(15):
        r, c = divmod(i, 8)
        x = 330 + c * 27; yy = 70 + r * 80
        o.append(f'<rect x="{x}" y="{yy}" width="25" height="25" rx="3" fill="{UI[i]}" stroke="{INK}" stroke-width="1"/>')
        o.append(tex(x + 12.5, yy + 46, str(i), size=18))
    o.append(tex(438, 50, mix='색표', size=20, weight=700))
    o.append(arw(298, 200, 380, 200, 'muted', 2))
    o.append(tex(438, 262, mix='색을 비교해 pH를 읽는다', size=19, fill=MUTED))
    return svg('0 0 560 340', 540, 'pH 측정기의 전극을 용액에 담가 숫자로 읽고, pH 시험지 색을 색표와 비교한다', ''.join(o))
FIG['measure'] = measure()


# ───── 8 물질의 pH 색 띠 ─────
def scale8():
    x0, W = 56, 62
    o = []
    cx = lambda p: x0 + W * p + W / 2
    for i in range(15):
        o.append(f'<rect x="{x0+i*W}" y="122" width="{W}" height="40" fill="{UI[i]}"/>')
        o.append(tex(x0 + i * W + W / 2, 149, str(i), size=20, weight=700, fill='#FFFFFF' if i not in (3, 4, 5) else INK))
    o.append(f'<rect x="{x0}" y="122" width="{15*W}" height="40" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    o.append(tex(48, 149, '\\text{pH}', size=20, anchor='end', weight=700))
    icons = []
    # 레몬 2
    x = cx(2); icons.append(f'<ellipse cx="{x}" cy="88" rx="28" ry="20" fill="#F7D84A" stroke="#C9A71E" stroke-width="2"/>')
    icons.append(tex(x, 40, mix='레몬', size=19))
    x = cx(4); icons.append(f'<circle cx="{x}" cy="88" r="22" fill="#E04434" stroke="#A92B1F" stroke-width="2"/><path d="M{x-10},68 L{x},74 L{x+10},68" fill="none" stroke="#3E8E3E" stroke-width="3"/>')
    icons.append(tex(x, 40, mix='토마토', size=19))
    x = cx(6); icons.append(f'<path d="M{x-14},60 L{x+14},60 L{x+14},66 L{x+20},76 L{x+20},110 L{x-20},110 L{x-20},76 L{x-14},66 Z" fill="#FFFFFF" stroke="{MUTED}" stroke-width="2"/>')
    icons.append(tex(x, 40, mix='우유', size=19))
    x = cx(9); icons.append(f'<rect x="{x-24}" y="70" width="48" height="40" rx="4" fill="#F2F2F2" stroke="{MUTED}" stroke-width="2"/><rect x="{x-24}" y="80" width="48" height="12" fill="#5B9BD5"/>')
    icons.append(tex(x, 40, mix='제빵 소다', size=19))
    x = cx(12); icons.append(f'<path d="M{x-28},96 Q{x},116 {x+28},96 Z" fill="#DDEEF8" stroke="{MUTED}" stroke-width="2"/><circle cx="{x-8}" cy="86" r="7" fill="none" stroke="#7FB3D5" stroke-width="2"/><circle cx="{x+8}" cy="80" r="9" fill="none" stroke="#7FB3D5" stroke-width="2"/>')
    icons.append(tex(x, 40, mix='비눗물', size=19))
    x = cx(13.5); icons.append(f'<path d="M{x-10},58 L{x+10},58 L{x+10},66 L{x+20},74 L{x+20},112 L{x-20},112 L{x-20},74 L{x-10},66 Z" fill="#D9442F" stroke="#8E2A1E" stroke-width="2"/>')
    icons.append(tex(x - 14, 22, mix='하수구', size=19), )
    icons.append(tex(x - 14, 44, mix='세척액', size=19))
    o.append('<g data-anim="pop" data-o="500,85" data-dur=".9" data-delay=".4" data-ease="back">' + ''.join(icons) + '</g>')
    o.append(arw(495, 196, 70, 196, 'plus', 3))
    o.append(arw(555, 196, 975, 196, 'minus', 3))
    o.append(tex(525, 203, mix='중성', size=20, weight=700, fill=GRAV))
    o.append(tex(280, 228, mix='산성이 강해짐', size=20, weight=700, fill=PLUS))
    o.append(tex(770, 228, mix='염기성이 강해짐', size=20, weight=700, fill=MINUS))
    return svg('0 0 1000 240', 960, '몇 가지 물질의 pH: 레몬, 토마토, 우유는 산성 쪽, 제빵 소다, 비눗물, 하수구 세척액은 염기성 쪽', ''.join(o))
FIG['scale8'] = scale8()


# ───── 9 자료 읽기 사다리 ─────
def ladder():
    o = [tex(140, 24, '[\\ce{H+}]\\ [\\text{M}]', size=20, weight=700, fill=PLUS), tex(360, 24, '\\text{pH}', size=20, weight=700)]
    rows = [(70, '1.0\\times10^{-4}', '4.00', '토마토'), (160, '1.0\\times10^{-5}', '5.00', ''), (250, '1.0\\times10^{-6}', '6.00', '우유')]
    for y, c, p, n in rows:
        o.append(tex(140, y + 8, c, size=22))
        o.append(tex(360, y + 8, p, size=22, weight=700))
        if n:
            o.append(tex(420, y + 8, mix=n, size=20, anchor='start', fill=MUTED))
    for i, (y1, y2) in enumerate(((84, 140), (174, 230))):
        o.append(f'<g data-anim="fade" data-dur=".6" data-delay="{.5+i*.8}">')
        o.append(arw(140, y1, 140, y2, 'muted', 2.5))
        o.append(tex(154, (y1 + y2) / 2 + 8, '\\times 1/10', size=20, anchor='start', fill=MUTED))
        o.append(arw(360, y1, 360, y2, 'ink', 2.5))
        o.append(tex(374, (y1 + y2) / 2 + 7, '+1', size=20, anchor='start', weight=700))
        o.append('</g>')
    return svg('0 0 520 280', 470, '토마토에서 우유로: 수소 이온 농도가 10분의 1씩 두 번 줄면 pH는 1씩 두 번 커진다', ''.join(o))
FIG['ladder'] = ladder()


# ───── 10 네 값 잇기 ─────
def four():
    o = []
    for x, y, t, c, fc in ((40, 30, '[\\ce{H+}]', PLUS, LP), (360, 30, '\\text{pH}', PLUS, LP), (40, 200, '[\\ce{OH-}]', MINUS, LM), (360, 200, '\\text{pOH}', MINUS, LM)):
        o.append(f'<rect x="{x}" y="{y}" width="160" height="60" rx="10" fill="{fc}" stroke="{c}" stroke-width="2.5"/>')
        o.append(tex(x + 80, y + 39, t, size=26, weight=700, fill=c))
    for yy, ya, yb in ((30, 50, 72), (200, 220, 242)):
        o.append(arw(208, ya, 352, ya, 'ink', 2.5))
        o.append(arw(352, yb, 208, yb, 'ink', 2.5))
        o.append(tex(280, ya - 8, '-\\log', size=20))
    o.append(tex(280, 102, '10^{-\\text{pH}}', size=20, fill=MUTED))
    o.append(tex(280, 272, '10^{-\\text{pOH}}', size=20, fill=MUTED))
    o.append(f'<line x1="120" y1="94" x2="120" y2="196" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="6 5"/>')
    o.append(f'<line x1="440" y1="94" x2="440" y2="196" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="6 5"/>')
    o.append(tex(130, 140, '[\\ce{H+}][\\ce{OH-}]', size=20, anchor='start'))
    o.append(tex(130, 168, '=1.0\\times10^{-14}', size=20, anchor='start'))
    o.append(tex(450, 140, '\\text{pH}+\\text{pOH}', size=20, anchor='start'))
    o.append(tex(450, 168, '=14.00', size=20, anchor='start'))
    return svg('0 0 640 290', 560, '수소 이온 농도, pH, 수산화 이온 농도, pOH를 잇는 관계', ''.join(o))
FIG['four'] = four()


def bars3():
    o = []
    U = 30
    for i, ph in enumerate((3, 7, 11)):
        y = 14 + i * 74
        o.append(bar14(ph, U=U, x0=20, y=y))
        kind, col = (('산성', PLUS), ('중성', GRAV), ('염기성', MINUS))[i]
        o.append(tex(452, y + 27, mix=kind, size=20, anchor='start', weight=700, fill=col))
    for p in (0, 14):
        o.append(tex(20 + p * U, 240, str(p), size=19, fill=MUTED))
    return svg('0 0 530 250', 470, 'pH 3, 7, 11일 때 길이 14인 막대를 pH와 pOH가 나누어 가진다', ''.join(o))
FIG['bars3'] = bars3()


# ───── 15 예측 ─────
def predict():
    o = [beaker(40, 170, 110, 110, 110, WATER, WATER_S)]
    o.append(tex(95, 200, '\\text{pH}\\ 3.00', size=20, weight=700, fill=PLUS))
    o.append(tex(95, 46, mix='염산', size=20))
    o.append(arw(170, 120, 300, 120, 'ink', 3))
    o.append(tex(235, 104, mix='1000배로', size=19, fill=MUTED))
    o.append(tex(235, 150, mix='묽힘', size=19, fill=MUTED))
    o.append(beaker(320, 170, 150, 140, 60, WATER, WATER_S))
    o.append('<g data-anim="pop" data-o="395,200" data-dur=".8" data-delay=".5" data-ease="back">' + tex(395, 205, '\\text{pH}\\ ?', size=22, weight=700) + '</g>')
    o.append(arw(490, 120, 620, 120, 'ink', 3))
    o.append(tex(555, 104, mix='계속', size=19, fill=MUTED))
    o.append(tex(555, 150, mix='묽히면', size=19, fill=MUTED))
    o.append(beaker(640, 170, 200, 150, 40, WATER, WATER_S))
    o.append('<g data-anim="pop" data-o="740,200" data-dur=".8" data-delay="1" data-ease="back">' + tex(740, 205, '\\text{pH}\\ ?', size=22, weight=700) + '</g>')
    return svg('0 0 880 220', 820, 'pH 3.00인 염산을 1000배로 묽히고 계속 묽히는 과정', ''.join(o))
FIG['predict'] = predict()


# ───── 17 과정 카드 ─────
def card1():
    o = [tex(120, 34, mix='50 mL 비커 5개', size=19, fill=MUTED)]
    for i, L in enumerate('ABCDE'):
        x = 14 + i * 44
        o.append(beaker(x, 140, 34, 52))
        o.append(tex(x + 17, 170, mix=L, size=20, weight=700))
    return svg('0 0 240 190', 230, '비커 다섯 개에 A부터 E까지 표시', ''.join(o))


def card2():
    o = [beaker(70, 160, 100, 110, 115, WATER, WATER_S, ticks=3, liq_anim='data-anim="scale" data-from="1,0" data-o="120,160" data-dur="1.1" data-delay=".4" data-ease="out"')]
    o.append(tex(120, 34, mix='A', size=22, weight=700))
    o.append(tex(120, 186, '0.1\\ \\text{M}\\ \\ce{HCl(aq)}\\ 10\\ \\text{mL}', size=19))
    return svg('0 0 240 200', 230, '비커 A에 0.1 M 염산 10 mL', ''.join(o))


def card3():
    o = [beaker(10, 180, 70, 70, 150, WATER, WATER_S)]
    o.append(tex(45, 200, mix='A', size=20, weight=700))
    fl, cy, mark, tp = flask(170, 190, 'clip-cm412-17a', level=178, R=42, neck=16, top=60, mark=110)
    o.append(fl)
    o.append('<g data-anim="move" data-from="-125,40" data-dur="1.3" data-delay=".4" data-ease="io">')
    o.append(f'<rect x="166" y="22" width="8" height="74" rx="2" fill="#F4F9FD" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<rect x="162" y="6" width="16" height="20" rx="6" fill="#D94A6A" stroke="#8E2A3E" stroke-width="1.5"/>')
    o.append(f'<rect x="167.5" y="80" width="5" height="14" fill="{WATER_S}"/>')
    o.append('</g>')
    o.append(tex(205, 46, '1\\ \\text{mL}', size=19, anchor='start'))
    o.append(tex(170, 210, mix='10 mL 부피 플라스크', size=19))
    return svg('0 0 260 220', 240, '피펫으로 비커 A의 염산 1 mL를 덜어 10 mL 부피 플라스크에 넣는다', ''.join(o))


def card4():
    o = ['<g data-anim="rot" data-from="16" data-o="120,190" data-dur=".5" data-rep="damp" data-delay=".4">']
    fl, cy, mark, tp = flask(120, 190, 'clip-cm412-17b', level=94, R=46, neck=18, top=52, mark=94, stopper=True)
    o.append(fl)
    o.append('</g>')
    o.append(tex(156, 100, mix='표시선', size=19, anchor='start', fill=MUTED))
    o.append(tex(120, 214, mix='증류수 → 마개 → 흔들기', size=19))
    return svg('0 0 240 225', 230, '표시선까지 증류수를 채우고 마개를 닫아 흔든다', ''.join(o))
FIG['c1'] = card1(); FIG['c2'] = card2(); FIG['c3'] = card3(); FIG['c4'] = card4()


# ───── 18 연쇄 희석 ─────
def chain():
    o = []
    concs = ['0.1', '0.01', '0.001', '0.0001', '0.00001']
    for i, L in enumerate('ABCDE'):
        x = 60 + i * 200
        o.append(beaker(x, 140, 80, 90, 90 + i * 0, WATER, WATER_S))
        o.append(tex(x + 40, 172, mix=L, size=22, weight=700))
        o.append(f'<g class="step" data-g="ch">{tex(x+40, 206, mix=concs[i] + " M", size=20, fill=PLUS, weight=700)}</g>')
        if i < 4:
            o.append(f'<g data-anim="fade" data-dur=".5" data-delay="{.4+i*.5}">')
            o.append(arw(x + 94, 96, x + 186, 96, 'ink', 2.5))
            o.append(tex(x + 140, 82, '\\times 1/10', size=20))
            o.append(tex(x + 140, 126, mix='1 → 10 mL', size=19, fill=MUTED))
            o.append('</g>')
    return svg('0 0 1000 220', 960, '비커 A부터 E까지 차례로 10배씩 희석한다', ''.join(o))
FIG['chain'] = chain()


# ───── 21 결과 막대그래프 ─────
MEAS_HCL = [1.07, 2.04, 2.97, 4.05, 5.09]


def bargraph(vals, labels, ymax, step, vb_w=520, vb_h=320, title_x='[\\ce{HCl}]\\ [\\text{M}]', ylab='\\text{측정한 pH}',
             anim=True, col=PLUS, valfmt='{:.2f}', show_val=True, cid=''):
    X0, Y0, top = 76, vb_h - 60, 34
    n = len(vals)
    sp = (vb_w - X0 - 30) / n
    s = (Y0 - top) / ymax
    o = []
    for v in range(0, ymax + 1, step):
        y = Y0 - v * s
        if v:
            o.append(f'<line x1="{X0}" y1="{f(y)}" x2="{vb_w-16}" y2="{f(y)}" stroke="#D5DCE3" stroke-width="1.5" stroke-dasharray="4 4"/>')
        o.append(tex(X0 - 10, y + 7, f'{v:.1f}' if step < 2 or ymax < 8 else str(v), size=18, anchor='end', fill=MUTED))
    for i, v in enumerate(vals):
        cx = X0 + sp * (i + .5)
        a = f' data-anim="scale" data-from="1,0" data-o="{f(cx)},{Y0}" data-dur=".9" data-delay="{.3+i*.2:.1f}" data-ease="out"' if anim else ''
        o.append(f'<g{a}><rect x="{f(cx-20)}" y="{f(Y0-v*s)}" width="40" height="{f(v*s)}" fill="{col}" opacity=".85"/></g>')
        if show_val:
            o.append(tex(cx, Y0 - v * s - 8, valfmt.format(v), size=18, weight=700))
        o.append(tex(cx, Y0 + 24, labels[i], size=18) if '^' in labels[i] else tex(cx, Y0 + 24, mix=labels[i], size=18))
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{vb_w-12}" y2="{Y0}" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{top-14}" stroke="{INK}" stroke-width="2"/>')
    o.append(tex(X0 - 4, 18, ylab, size=19, anchor='start', weight=700))
    if title_x:
        o.append(tex(vb_w - 14, vb_h - 10, title_x, size=19, anchor='end'))
    return ''.join(o)


FIG['res1'] = svg('0 0 520 320', 500, '측정한 pH 막대그래프: A 1.07, B 2.04, C 2.97, D 4.05, E 5.09',
                  bargraph(MEAS_HCL, ['0.1', '0.01', '0.001', '10^{-4}', '10^{-5}'], 6, 1))


# ───── 23 이론 곡선 ─────
def curves():
    X0, Y0, top = 76, 286, 40
    kx = lambda k: X0 + (k - 1) * 50
    py = lambda p: Y0 - p * (Y0 - top) / 14
    o = []
    for p in (0, 7, 14):
        o.append(tex(X0 - 10, py(p) + 7, str(p), size=18, anchor='end', fill=MUTED))
    o.append(f'<line x1="{X0}" y1="{f(py(7))}" x2="{kx(10)+10}" y2="{f(py(7))}" stroke="{GRAV}" stroke-width="2" stroke-dasharray="7 5"/>')
    o.append(tex(kx(10) + 8, py(7) - 10, mix='중성', size=19, anchor='end', fill=GRAV))
    for k in (1, 3, 5, 7, 9):
        o.append(f'<line x1="{kx(k)}" y1="{Y0}" x2="{kx(k)}" y2="{Y0+6}" stroke="{INK}" stroke-width="2"/>')
        o.append(tex(kx(k), Y0 + 28, f'10^{{-{k}}}', size=18))
    for base, col, name, ly in ((False, PLUS, '염산', 66), (True, MINUS, '$\\ce{NaOH}$ 수용액', 30)):
        pts = []
        for j in range(91):
            k = 1 + j / 10
            pts.append(f'{f(kx(k))},{f(py(th_pH(10**-k, base)))}')
        o.append(f'<g data-anim="draw" data-dur="1.6" data-delay=".3"><polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="3.5"/></g>')
        for k in range(1, 11):
            o.append(f'<circle cx="{f(kx(k))}" cy="{f(py(th_pH(10**-k, base)))}" r="4.5" fill="{col}"/>')
    o.append(tex(kx(2) + 14, py(2) + 26, mix='염산', size=20, anchor='start', weight=700, fill=PLUS))
    o.append(tex(kx(2) + 14, py(12) - 14, mix='$\\ce{NaOH}$ 수용액', size=20, anchor='start', weight=700, fill=MINUS))
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{kx(10)+16}" y2="{Y0}" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{top-14}" stroke="{INK}" stroke-width="2"/>')
    o.append(tex(X0 + 8, 24, '\\text{pH}', size=19, anchor='start', weight=700))
    o.append(tex(kx(10) + 16, Y0 + 52, mix='몰농도 [M]', size=19, anchor='end'))
    return svg('0 0 560 345', 500, '염산과 수산화 나트륨 수용액을 10배씩 희석할 때 이론 pH: 둘 다 7에 다가간다', ''.join(o))
FIG['curves'] = curves()


# ───── 26 충치와 pH ─────
def tooth():
    x = lambda p: 60 + (p - 3.5) * 110
    o = [f'<rect x="{f(x(3.5))}" y="30" width="{f(x(5.5)-x(3.5))}" height="210" fill="{PLUS}" opacity=".08"/>',
         f'<line x1="{f(x(5.5))}" y1="30" x2="{f(x(5.5))}" y2="240" stroke="{PLUS}" stroke-width="2" stroke-dasharray="6 5"/>']
    o.append(tex(x(4.5), 56, mix='법랑질이 녹는 범위', size=19, fill=PLUS, weight=700))
    o.append(tex(x(4.5), 80, mix='(pH 5.0–5.5 이하)', size=19, fill=PLUS))
    o.append(f'<g data-anim="scale" data-from="0,1" data-o="{f(x(6.4))},124" data-dur="1" data-delay=".3" data-ease="out"><rect x="{f(x(6.4))}" y="110" width="{f(x(7.0)-x(6.4))}" height="28" rx="6" fill="{FIELD}" opacity=".85"/></g>')
    o.append(tex(x(6.7), 100, mix='침 6.4–7.0', size=19, weight=700, fill=FIELD))
    o.append(f'<g data-anim="scale" data-from="0,1" data-o="{f(x(4.5))},189" data-dur="1" data-delay="1" data-ease="out"><rect x="{f(x(4.0))}" y="175" width="{f(x(4.5)-x(4.0))}" height="28" rx="6" fill="{PLUS}" opacity=".85"/></g>')
    o.append(tex(x(4.25), 166, mix='음식물 찌꺼기', size=19, weight=700, fill=PLUS))
    o.append(tex(x(4.5) + 8, 196, mix='4.0–4.5', size=19, weight=700, fill=PLUS, anchor='start'))
    o.append(arw(x(6.4) - 6, 140, x(4.5) + 80, 178, 'plus', 2.5, extra='data-delay=".7"'))
    o.append(tex(x(5.5) + 16, 210, mix='뮤탄스균이 산을 만듦', size=19, anchor='start', fill=PLUS))
    o.append(f'<line x1="{f(x(3.5))}" y1="244" x2="{f(x(7.5))}" y2="244" stroke="{INK}" stroke-width="2.5"/>')
    for p in (4, 5, 6, 7):
        o.append(f'<line x1="{f(x(p))}" y1="238" x2="{f(x(p))}" y2="250" stroke="{INK}" stroke-width="2"/>')
        o.append(tex(x(p), 272, str(p), size=19, weight=700))
    o.append(tex(x(7.5), 272, '\\text{pH}', size=19, anchor='end', weight=700))
    return svg('0 0 520 285', 500, '침의 pH 6.4–7.0, 음식물 찌꺼기 4.0–4.5, pH 5.0–5.5 이하에서 법랑질이 녹는다', ''.join(o))
FIG['tooth'] = tooth()


# ───── 29 문항 08 ─────
def q08():
    o = [beaker(20, 170, 130, 120, 70, WATER, WATER_S), beaker(220, 170, 130, 120, 70, WATER, WATER_S), beaker(470, 170, 150, 140, 50, WATER, WATER_S)]
    for cx, a, b, n in ((85, '2\\ \\text{M}', '200\\ \\text{mL}', '(가)'), (285, '1\\ \\text{M}', '500\\ \\text{mL}', '(나)'), (545, '', '1\\ \\text{L}', '(다)')):
        if a:
            o.append(tex(cx, 100, a, size=20))
        o.append(tex(cx, 126, '\\ce{NaOH(aq)}', size=20))
        o.append(tex(cx, 152, b, size=20))
        o.append(tex(cx, 200, mix=n, size=20, weight=700))
    o.append(tex(185, 120, '+', size=30, weight=700, fill=MUTED))
    o.append(arw(370, 112, 450, 112, 'ink', 3))
    o.append(tex(410, 92, mix='증류수 첨가', size=19, fill=MUTED))
    return svg('0 0 640 215', 600, '2 M 수산화 나트륨 수용액 200 mL와 1 M 500 mL를 섞고 증류수를 더해 1 L로 만든다', ''.join(o))
FIG['q08'] = q08()

FIG['q10'] = svg('0 0 440 300', 420, '용액 A–D의 pH 막대그래프: A 2.0, B 4.0, C 5.0, D 6.0',
                 bargraph([2.0, 4.0, 5.0, 6.0], ['A', 'B', 'C', 'D'], 6, 2, vb_w=440, vb_h=300, title_x='', ylab='\\text{pH}', anim=False, col='#5B9BD5', show_val=False))

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    out = re.sub(r'@@(\w+)@@', lambda m: FIG[m.group(1)], tpl)
    open(sys.argv[1], 'w', encoding='utf-8').write(out)
    print('wrote', sys.argv[1], len(out))
