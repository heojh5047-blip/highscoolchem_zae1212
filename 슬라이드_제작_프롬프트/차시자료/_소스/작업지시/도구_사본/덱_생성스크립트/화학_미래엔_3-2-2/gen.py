import math, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import *
OUT = sys.argv[1]
RED = '#D9608A'; BLUE = '#3B6FD1'
def mixc(fr):
    a = (217, 96, 138); b = (59, 111, 209)
    return '#%02X%02X%02X' % tuple(round(a[i]+(b[i]-a[i])*fr) for i in range(3))
PURP = mixc(0.5)
COLD = ('#E3EEFB', '#9FC3DD'); HOT = ('#FDE2E4', '#E8A0A8'); ROOM = ('#DDEEF8', '#9FC3DD')

def bath_back(x, y, w, h, kind, ice=True):
    fill, edge = {'cold': COLD, 'hot': HOT, 'room': ROOM}[kind]
    top = y+h*0.22
    s = f'<path d="M{f(x+4)} {f(top)} H{f(x+w-4)} V{f(y+h-8)} Q{f(x+w-4)} {f(y+h-3)} {f(x+w-9)} {f(y+h-3)} H{f(x+9)} Q{f(x+4)} {f(y+h-3)} {f(x+4)} {f(y+h-8)} Z" fill="{fill}"/>'
    s += f'<path d="M{f(x+4)} {f(top)} H{f(x+w-4)}" stroke="{edge}" stroke-width="2.5"/>'
    if kind == 'cold' and ice:
        for k, (dx, dy, a) in enumerate([(0.12, 0.02, 12), (0.68, 0.05, -15), (0.2, 0.42, 28), (0.74, 0.5, -8)]):
            cx, cy = x+w*dx+12, top+h*dy+14
            s += f'<rect x="{f(cx-12)}" y="{f(cy-12)}" width="24" height="24" rx="5" fill="#FFFFFF" stroke="{edge}" stroke-width="2" transform="rotate({a} {f(cx)} {f(cy)})"/>'
    return s
def bath_front(x, y, w, h, kind, steam=True, anim=False):
    s = f'<path d="M{f(x-6)} {f(y-4)} Q{f(x)} {f(y)} {f(x)} {f(y+8)} V{f(y+h-8)} Q{f(x)} {f(y+h)} {f(x+8)} {f(y+h)} H{f(x+w-8)} Q{f(x+w)} {f(y+h)} {f(x+w)} {f(y+h-8)} V{f(y)}" fill="none" stroke="{GL}" stroke-width="3.5" stroke-linejoin="round"/>'
    if kind == 'hot' and steam:
        st = ''
        for k in range(3):
            sx = x+w*(0.25+0.25*k)
            st += f'<path d="M{f(sx)} {f(y-8)} q-8 -10 0 -20 q8 -10 0 -20" fill="none" stroke="{MU}" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>'
        s += f'<g data-anim="move" data-from="0,10" data-dur="1.6" data-rep="loop">{st}</g>' if anim else st
    return s
def ttube(x, ytop, ybot, w, color, level, over=None, overattr='', g=None):
    ex = f'<path d="LIQ" fill="{over}"{overattr}/>' if over else ''
    if g: ex = f'<g class="step" data-g="{g}">{ex}</g>'
    return tube(x, ytop, ybot, w, color, level, ex)
def hd(x1, x2, y, w=3, gap=7):  # half arrows equilibrium
    return halfarrows(x1, x2, y, w, gap)
H = {}

# ---------- COVER 540x540 ----------
c = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
c += ttube(270, 60, 238, 56, PURP, 130)
c += A(236, 160, 160, 222, 'minus', 3.5)+A(304, 160, 380, 222, 'plus', 3.5)
c += T(150, 176, '온도를||낮춤', 22, 'middle', MINUS, ' data-weight="700"')+T(390, 176, '온도를||높임', 22, 'middle', PLUS, ' data-weight="700"')
c += bath_back(60, 270, 170, 170, 'cold')+ttube(145, 232, 416, 50, PURP, 320, RED, ' data-anim="fade" data-dur="1.4" data-delay=".6"')+bath_front(60, 270, 170, 170, 'cold')
c += bath_back(310, 270, 170, 170, 'hot')+ttube(395, 232, 416, 50, PURP, 320, BLUE, ' data-anim="fade" data-dur="1.4" data-delay="1.2"')+bath_front(310, 270, 170, 170, 'hot')
c += T(145, 470, '얼음물', 22, 'middle', INK)+T(395, 470, '뜨거운 물', 22, 'middle', INK)
H['COVER'] = c

# ---------- S3 thermochromic mugs 560x300 ----------
def mug(x, y, body, handle=True):
    s = f'<path d="M{x+150} {y+40} q48 0 48 44 q0 44 -48 44" fill="none" stroke="{body}" stroke-width="16"/>' if handle else ''
    s += f'<path d="M{x} {y} H{x+150} V{y+150} Q{x+150} {y+170} {x+130} {y+170} H{x+20} Q{x} {y+170} {x} {y+150} Z" fill="{body}"/>'
    return s
m = '<rect x="0" y="0" width="560" height="300" rx="18" fill="#F4F6F8"/>'
m += mug(40, 90, '#3A3F47')+T(115, 290, '차가울 때', 21)
m += mug(320, 90, '#3A3F47')
pat = mug(320, 90, '#F7E3B5', False)
pat += ''.join(f'<path d="M{f(cx)} {f(cy-14)} l4 9 10 1 -8 7 3 10 -9 -5 -9 5 3 -10 -8 -7 10 -1 Z" fill="{PLUS}"/>' for cx, cy in [(360, 140), (420, 175), (380, 215), (450, 125), (445, 225)])
m += f'<g data-anim="fade" data-dur="1.8" data-delay=".6">{pat}</g>'
m += f'<ellipse cx="395" cy="92" rx="75" ry="9" fill="#8A5A3C"/>'
st = ''.join(f'<path d="M{sx} 70 q-9 -12 0 -24 q9 -12 0 -24" fill="none" stroke="{MU}" stroke-width="3" stroke-linecap="round" opacity=".75"/>' for sx in (365, 395, 425))
m += f'<g data-anim="move" data-from="0,12" data-dur="1.6" data-rep="loop">{st}</g>'
m += T(395, 290, '뜨거운 음료를 부으면', 21)
m += A(240, 175, 300, 175, 'ink', 3)
H['MUG'] = m

# ---------- S4 endo / exo panels 300x250 ----------
def thermo(x, y0, y1, level, anim_from):
    s = f'<rect x="{x-7}" y="{y0}" width="14" height="{y1-y0}" rx="7" fill="#fff" stroke="{MU}" stroke-width="2"/><circle cx="{x}" cy="{y1+8}" r="12" fill="{PLUS}"/>'
    col = f'<rect x="{x-3.5}" y="{level}" width="7" height="{y1+4-level}" fill="{PLUS}"/>'
    s += f'<g data-anim="scale" data-from="1,{anim_from}" data-o="{x},{y1+4}" data-dur="1.6" data-delay=".5" data-ease="out">{col}</g>'
    return s
def panel(kind):
    s = f'<rect x="0" y="0" width="300" height="250" rx="16" fill="{"#E3EEFB" if kind=="endo" else "#FDE2E4"}"/>'
    s += beaker(95, 70, 110, 140, '#DDEEF8')
    s += thermo(170, 30, 170, 120 if kind == 'endo' else 60, 0.55 if kind == 'endo' else 1.6)
    if kind == 'endo':
        s += A(28, 120, 88, 150, 'equi', 4)+A(28, 200, 88, 175, 'equi', 4)+T(18, 104, '에너지 흡수', 22, 'start', '#B45F06', ' data-weight="700"')
        s += T(150, 238, '주변 온도가 낮아진다', 22, 'middle', MINUS, ' data-weight="700"')
    else:
        s += A(100, 150, 36, 120, 'equi', 4)+A(100, 175, 36, 200, 'equi', 4)+T(18, 104, '에너지 방출', 22, 'start', '#B45F06', ' data-weight="700"')
        s += T(150, 238, '주변 온도가 높아진다', 22, 'middle', PLUS, ' data-weight="700"')
    return s
H['ENDO'] = panel('endo'); H['EXO'] = panel('exo')

# ---------- S6 heat glove icon ----------
H['GLOVE'] = '<path d="M38 112 V70 Q30 40 42 30 Q52 24 58 40 L62 52 V24 Q64 10 82 10 Q104 10 108 30 L112 74 Q114 92 108 112 Z" fill="#F2A65A" stroke="#16233D" stroke-width="3.5" stroke-linejoin="round"/><path d="M38 96 H110" stroke="#16233D" stroke-width="3"/><path d="M50 104 H100" stroke="#C2410C" stroke-width="3" stroke-dasharray="6 5"/>'

# ---------- S7 process cards (300x264) ----------
p1 = beaker(70, 100, 150, 130, RED)
p1 += f'<g class="step" data-g="q1"><path d="M74 145.5 H216 V222 Q216 228 210 228 H80 Q74 228 74 222 Z" fill="{PURP}" data-anim="fade" data-on="step" data-dur="1.4" data-delay=".4"/></g>'
p1 += '<path d="M150 40 L210 92" stroke="#8C99A6" stroke-width="6" stroke-linecap="round"/><ellipse cx="140" cy="34" rx="20" ry="11" fill="#8C99A6"/><ellipse cx="140" cy="31" rx="14" ry="6" fill="#fff" stroke="#C9D3DD"/>'
p1 += T(176, 28, '$\\ce{CaCl2}$', 24, 'start', INK, ' data-halo="1"')+T(145, 252, '50 mL', 24, 'middle', MU)
H['P1'] = p1
p2 = bath_back(60, 96, 180, 160, 'cold')+ttube(150, 40, 240, 48, PURP, 150, RED, ' data-anim="fade" data-on="step" data-dur="1.4" data-delay=".4"', 'q2')+bath_front(60, 96, 180, 160, 'cold')
p2 += T(290, 80, '얼음물', 24, 'end', MINUS, ' data-weight="700"')+T(100, 60, '5 mL', 24, 'end', MU)
H['P2'] = p2
p3 = bath_back(60, 96, 180, 160, 'hot')+ttube(150, 40, 240, 48, RED, 150, BLUE, ' data-anim="fade" data-on="step" data-dur="1.4" data-delay=".4"', 'q3')+bath_front(60, 96, 180, 160, 'hot', anim=True)
p3 += T(296, 32, '뜨거운 물', 24, 'end', PLUS, ' data-weight="700"')
H['P3'] = p3

# ---------- S9 direction diagram 560x200 ----------
d = ttube(280, 20, 176, 44, PURP, 70)
d += A(252, 100, 112, 100, 'minus', 3.5)+A(308, 100, 448, 100, 'plus', 3.5)
d += T(182, 84, '온도를 낮춤', 26, 'middle', MINUS, ' data-weight="700"')+T(378, 84, '온도를 높임', 26, 'middle', PLUS, ' data-weight="700"')
d += '<g class="step" data-g="d1">'+ttube(70, 20, 176, 44, RED, 70)+T(70, 198, '발열 쪽', 24, 'middle', BF, ' data-weight="700"')+'</g>'
d += '<g class="step" data-g="d2">'+ttube(490, 20, 176, 44, BLUE, 70)+T(490, 198, '흡열 쪽', 24, 'middle', FIELD, ' data-weight="700"')+'</g>'
H['DIR'] = d

# ---------- S11 figure III-12 redraw 940x290 ----------
g = ttube(110, 40, 250, 50, PURP, 110)
g += A(150, 150, 280, 150, 'minus', 4)+T(215, 132, '온도를 낮춤', 21, 'middle', MINUS, ' data-weight="700"')
g += bath_back(300, 90, 200, 190, 'cold')+ttube(400, 40, 262, 50, PURP, 150, RED, ' data-anim="fade" data-dur="1.4" data-delay=".5"')+bath_front(300, 90, 200, 190, 'cold')
g += A(520, 150, 650, 150, 'plus', 4)+T(585, 132, '온도를 높임', 21, 'middle', PLUS, ' data-weight="700"')
g += bath_back(670, 90, 200, 190, 'hot')+ttube(770, 40, 262, 50, RED, 150, BLUE, ' data-anim="fade" data-dur="1.4" data-delay="1.4"')+bath_front(670, 90, 200, 190, 'hot')
g += T(400, 26, '얼음물', 21, 'middle', MINUS, ' data-weight="700"')+T(770, 26, '뜨거운 물', 21, 'middle', PLUS, ' data-weight="700"')
H['FIG12'] = g

# ---------- S13 particle boxes (300x250) ----------
def pbox(kind, na, nb, seed, anim):
    fill, edge = {'cold': COLD, 'hot': HOT, 'room': ROOM}[kind]
    s = f'<rect x="0" y="0" width="300" height="250" rx="16" fill="{fill}"/>'
    s += f'<rect x="30" y="20" width="240" height="210" rx="12" fill="{NO2C}" fill-opacity="{0.06*na:.2f}"/><rect x="30" y="20" width="240" height="210" rx="12" fill="none" stroke="{GL}" stroke-width="3"/>'
    mol = grid(['a']*na+['b']*nb, 40, 30, 220, 190, 12, seed)
    s += f'<g data-anim="move" data-from="{anim}" data-dur="1.4" data-rep="alt" data-ease="io">{mol}</g>'
    return s
H['BX1'] = pbox('cold', 2, 5, 11, '3,-3'); H['BX2'] = pbox('room', 6, 3, 3, '-3,3'); H['BX3'] = pbox('hot', 10, 1, 5, '3,3')
H['LEG13'] = no2(24, 24, 12)+T(52, 31, '$\\ce{NO2}$', 20, 'start')+n2o4(150, 24, 12)+T(186, 31, '$\\ce{N2O4}$', 20, 'start')

# ---------- S15 graph 600x380 ----------
def gx(t): return 100+t/100*460
def gy(l): return 177-l/2.4*133
gr = f'<rect x="100" y="44" width="460" height="266" fill="#FBFCFD"/>'
for l in (-2, -1, 0, 1, 2):
    gr += f'<path d="M100 {f(gy(l))} H560" stroke="#E2E8EE" stroke-width="1.5"/>' if l else f'<path d="M100 {f(gy(0))} H560" stroke="{MU}" stroke-width="1.5" stroke-dasharray="5 5"/>'
for t in (0, 25, 50, 75, 100):
    gr += f'<path d="M{f(gx(t))} 310 V316" stroke="{INK}" stroke-width="2"/>'+T(gx(t), 340, str(t), 19, 'middle')
for l, lab in ((-2, '10^{-2}'), (0, '1'), (2, '10^{2}')):
    gr += f'<path d="M94 {f(gy(l))} H100" stroke="{INK}" stroke-width="2"/>'+T(88, gy(l)+7, f'${lab}$', 19, 'end')
gr += A(100, 310, 580, 310, 'ink', 2)+A(100, 310, 100, 30, 'ink', 2)
gr += T(580, 368, '온도 $t$ [°C]', 19, 'end')+T(110, 24, '$K$ (25 °C 값 = 1, 로그 눈금)', 19, 'start')
def curve(fn):
    pts = []
    for i in range(0, 101, 2):
        T_ = i+273; pts.append((gx(i), gy(max(-2.5, min(2.5, math.log10(fn(T_)))))))
    return 'M'+' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
cE = curve(lambda T_: math.exp(-50000/8.314*(1/T_-1/298)))
cX = curve(lambda T_: math.exp(6856*(1/T_-1/298)))
gr += f'<path d="{cE}" fill="none" stroke="{BLUE}" stroke-width="4" data-anim="draw" data-dur="1.6" data-delay=".3"/>'
gr += f'<path d="{cX}" fill="none" stroke="{NO2C}" stroke-width="4" data-anim="draw" data-dur="1.6" data-delay=".9"/>'
for t in (0, 25, 80):
    gr += f'<circle cx="{f(gx(t))}" cy="{f(gy(math.log10(math.exp(6856*(1/(t+273)-1/298)))))}" r="6" fill="{NO2C}"/>'
gr += T(560, 72, '정반응 흡열', 20, 'end', BLUE, ' data-weight="700" data-halo="1"')
gr += T(560, 262, '정반응 발열', 20, 'end', NO2C, ' data-weight="700" data-halo="1"')
H['GRAPH'] = gr

# ---------- S19 car 460x250 ----------
car = '<rect x="0" y="0" width="460" height="250" rx="16" fill="#F4F6F8"/><path d="M0 214 H460" stroke="#8C99A6" stroke-width="3"/>'
car += '<path d="M150 186 V150 Q152 132 172 128 L222 92 Q232 86 250 86 H330 Q352 86 364 102 L388 128 Q426 132 432 156 V186 Z" fill="#3B5BA9"/>'
car += '<path d="M232 126 L256 98 H296 V126 Z M306 98 H334 Q344 98 352 108 L366 126 H306 Z" fill="#DDEEF8"/>'
car += ''.join(f'<circle cx="{x}" cy="190" r="24" fill="#2B2F36"/><circle cx="{x}" cy="190" r="10" fill="#C9D3DD"/>' for x in (200, 380))
car += f'<rect x="364" y="140" width="56" height="30" rx="6" fill="#FDE2E4" stroke="{PLUS}" stroke-width="2"/>'+T(392, 162, '고온', 19, 'middle', PLUS, ' data-weight="700"')
cloud = '<path d="M130 186 q-30 6 -40 -12 q-30 4 -36 -22 q-26 -14 -6 -34 q2 -26 34 -24 q20 -22 46 -4 q26 -6 30 18 q22 12 6 34 q4 30 -34 44 Z" fill="#C9D3DD" opacity=".9"/>'
car += f'<g data-anim="move" data-from="40,4" data-dur="1.8" data-delay=".3" data-ease="out">{cloud}'+T(96, 150, '$\\ce{NO}$', 24, 'middle', INK, ' data-weight="700"')+'</g>'
car += T(300, 40, '엔진 내부는 온도가 매우 높다', 20, 'middle', INK, ' data-halo="1"')
H['CAR'] = car

# ---------- S21 spoon 280x200 ----------
sp = '<rect x="0" y="0" width="280" height="200" rx="16" fill="#F4F6F8"/>'
sp += f'<path d="M40 150 L170 80" stroke="#F2C230" stroke-width="14" stroke-linecap="round"/><ellipse cx="205" cy="62" rx="44" ry="28" fill="#F2C230" transform="rotate(-28 205 62)"/>'
sp += f'<g data-anim="fade" data-dur="1.6" data-delay=".6"><path d="M40 150 L170 80" stroke="{PLUS}" stroke-width="14" stroke-linecap="round" opacity=".85"/><ellipse cx="205" cy="62" rx="44" ry="28" fill="{PLUS}" opacity=".85" transform="rotate(-28 205 62)"/></g>'
sp += T(140, 186, '뜨거우면 붉게 변하는 숟가락(예)', 19, 'middle', INK)
H['SPOON'] = sp

# ---------- S23 problem 01 boxes 640x250 ----------
def sbox(x, items, seed):
    s = f'<rect x="{x}" y="10" width="230" height="200" rx="14" fill="#F4F6F8" stroke="#8C99A6" stroke-width="5"/>'
    s += grid(items, x+12, 22, 206, 176, 12, seed)
    return s
b1 = sbox(20, ['b']*3+['a']*4, 21)+sbox(390, ['b']+['a']*8, 8)
b1 += A(268, 110, 372, 110, 'ink', 4)
b1 += T(135, 242, '25 °C', 21)+T(505, 242, '100 °C', 21)
H['P01'] = b1
H['LEG23'] = H['LEG13']

# ---------- S25 problem 04 tubes 360x230 ----------
q4 = ''
for x, kind, col, gname, lab in ((90, 'cold', RED, 'r1', '㉠'), (270, 'hot', BLUE, 'r1', '㉡')):
    q4 += bath_back(x-75, 70, 150, 150, kind)+ttube(x, 20, 200, 42, '#F4F6F8', 110, col, ' data-anim="fade" data-on="step" data-dur="1.2"', gname)+bath_front(x-75, 70, 150, 150, kind)
    q4 += T(x+34, 60, lab, 22, 'start', INK, ' data-weight="700"')
H['P04'] = q4

# ---------- S26 rigid box with He 300x220 ----------
rb = '<rect x="20" y="20" width="260" height="180" rx="10" fill="#fff" stroke="#5B6B7F" stroke-width="6"/>'+T(266, 190, '1 L', 20, 'end', MU)
import random
rnd = random.Random(4)
pos = [(60, 60), (120, 90), (200, 60), (240, 120), (90, 150), (170, 150), (150, 60), (60, 110)]
for k, (x, y) in enumerate(pos[:3]):
    rb += f'<circle cx="{x}" cy="{y}" r="16" fill="#8C99A6"/>'+T(x, y+7, 'A', 19, 'middle', '#fff', ' data-weight="700"')
for x, y in pos[3:]:
    rb += f'<circle cx="{x}" cy="{y}" r="11" fill="#2E9E6A"/>'
he = ''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="{HE}" stroke="#7FA9C2" stroke-width="1.5"/>' for x, y in [(100, 40), (215, 95), (130, 120), (250, 170), (45, 180), (190, 180)])
rb += f'<g class="step" data-g="he"><g data-anim="move" data-from="0,-30" data-on="step" data-dur="1"> {he}</g></g>'
H['P06'] = rb

# ---------- S28 map tube 260x200 ----------
mt = ttube(130, 10, 190, 46, PURP, 60)
mt += A(100, 120, 16, 120, 'minus', 3.5)+A(160, 120, 244, 120, 'plus', 3.5)
mt += T(56, 100, '낮춤', 32, 'middle', MINUS, ' data-weight="700"')+T(204, 100, '높임', 32, 'middle', PLUS, ' data-weight="700"')
H['MAPT'] = mt

# ---------- S22 video frame 600x230 ----------
def amp(x, y, op):
    return f'<rect x="{x-22}" y="{y}" width="44" height="120" rx="16" fill="{NO2C}" fill-opacity="{op}"/><rect x="{x-22}" y="{y}" width="44" height="120" rx="16" fill="none" stroke="{GL}" stroke-width="3"/>'
v = '<rect x="4" y="4" width="592" height="222" rx="14" fill="#2B2F36"/><rect x="18" y="16" width="564" height="176" rx="8" fill="#F4F6F8"/>'
v += bath_back(70, 50, 160, 136, 'cold')+amp(150, 40, .12)+bath_front(70, 50, 160, 136, 'cold')
v += bath_back(370, 50, 160, 136, 'hot')+amp(450, 40, .75)+bath_front(370, 50, 160, 136, 'hot', anim=True)
v += T(242, 100, '얼음물', 24, 'start', MINUS, ' data-weight="700"')+T(362, 150, '뜨거운 물', 24, 'end', PLUS, ' data-weight="700"')
v += '<path d="M30 206 H570" stroke="#5B6B7F" stroke-width="4"/><path d="M30 206 H250" stroke="#D7263D" stroke-width="4"/><circle cx="250" cy="206" r="7" fill="#D7263D"/>'
H['VID'] = v

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slides.html.tpl'), encoding='utf-8').read()
for k, v in H.items(): src = src.replace('[['+k+']]', v)
left = re.findall(r'\[\[[A-Za-z0-9:]+\]\]', src)
if left: print('UNFILLED', left)
open(OUT, 'w', encoding='utf-8').write(src)
print('ok', len(src))
