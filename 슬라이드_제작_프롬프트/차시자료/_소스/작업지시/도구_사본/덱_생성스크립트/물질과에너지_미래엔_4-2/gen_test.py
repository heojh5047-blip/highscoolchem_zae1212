# 4-2 일차 반응의 반감기 — tpl.html 의 @@이름@@ 자리에 그림을 넣어 slides.html 을 만든다.
import math, os, re, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/물질과에너지_미래엔_4-2/gen_out.html"
F = {}
BOND = '#9AA5B1'

def dim(x1, x2, y, lab, col=MUTED, size=20, extra=''):
    """가로 치수선(양 끝 화살촉) + 위 라벨"""
    o = f'<g{extra}><line x1="{f(x1 + 3)}" y1="{f(y)}" x2="{f(x2 - 3)}" y2="{f(y)}" stroke="{col}" stroke-width="2"/>'
    o += f'<polygon points="{f(x1)},{f(y)} {f(x1 + 9)},{f(y - 4.5)} {f(x1 + 9)},{f(y + 4.5)}" fill="{col}"/>'
    o += f'<polygon points="{f(x2)},{f(y)} {f(x2 - 9)},{f(y - 4.5)} {f(x2 - 9)},{f(y + 4.5)}" fill="{col}"/>'
    o += tex((x1 + x2) / 2, y - 9, lab, size, 'middle', INK, halo=True) + '</g>'
    return o

def spots(n, w, h, r, seed, pad=4):
    """상자(w×h) 안에 겹치지 않는 입자 자리 n개"""
    rnd = random.Random(seed); pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        x = rnd.uniform(r + pad, w - r - pad); y = rnd.uniform(r + pad, h - r - pad)
        if all((x - a) ** 2 + (y - b) ** 2 > (2 * r + 5) ** 2 for a, b in pts):
            pts.append((x, y))
    return pts

def dot(x, y, r, fill, stroke=None, extra=''):
    s = stroke or fill
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{fill}" stroke="{s}" stroke-width="1.5"{extra}/>'

def halfmarks(A, pts, col=MUTED):
    o = ''
    for (t, c) in pts:
        o += A.line(A.xr[0], c, t, c, col, 1.6, '5 5') + A.line(t, A.yr[0], t, c, col, 1.6, '5 5')
    return o

# ── S1 표지 ──
def cover():
    A = Axes(110, 410, 340, 260, (0, 4.2), (0, 1))
    o = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    o += A.frame(grid=False)
    o += tex(A.x0 + 12, A.Y(1) - 16, '농도', 22, 'start', INK)
    o += tex(A.X(4.2) + 22, A.y0 + 30, '시간', 22, 'end', INK)
    o += f'<g data-anim="fade" data-dur=".8" data-delay="1.4">' + halfmarks(A, [(1, .5), (2, .25), (3, .125)]) + '</g>'
    o += f'<path d="{A.path(lambda t: 0.5 ** t, 0, 4.2)}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" data-anim="draw" data-dur="1.4" data-delay=".2"/>'
    for (t, c) in [(0, 1), (1, .5), (2, .25), (3, .125)]:
        o += A.dot(t, c, INK, 6, '#fff')
    for i, lab in enumerate(['1', '\\tfrac{1}{2}', '\\tfrac{1}{4}', '\\tfrac{1}{8}']):
        o += tex(A.x0 - 12, A.Y(0.5 ** i) + 8, lab, 22, 'end', INK, mix=False)
    for i in range(3):
        o += f'<g data-anim="pop" data-o="{f(A.X(i + .5))},{f(A.y0 - 20)}" data-delay="{1.6 + .25 * i:.2f}" data-dur=".5">' + dim(A.X(i) + 2, A.X(i + 1) - 2, A.y0 - 20, '$t_{1/2}$', INK, 22) + '</g>'
    o += tex(270, 492, '반감기마다 농도가 절반으로', 22, 'middle', MUTED)
    return o
F['cover'] = cover()

# ── S3 생각 열기: 유물 ──
def relic_bronze():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<ellipse cx="150" cy="88" rx="78" ry="52" fill="none" stroke="#9C6B3A" stroke-width="16"/>'
    o += '<ellipse cx="150" cy="88" rx="78" ry="52" fill="none" stroke="#B9874F" stroke-width="5" stroke-dasharray="10 14"/>'
    o += '<g data-anim="fade" data-dur="2" data-delay=".3">' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{b}" fill="#4FA38A" opacity=".85"/>' for x, y, a, b in ((96, 66, 10, 7), (196, 54, 9, 6), (220, 104, 8, 6), (120, 134, 11, 6), (176, 138, 8, 5))) + '</g>'
    return o
def relic_arrow():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<g transform="rotate(-28 150 88)"><polygon points="70,88 160,58 236,88 160,118" fill="#8C99A6" stroke="#5B6B7F" stroke-width="2.5"/><line x1="76" y1="88" x2="230" y2="88" stroke="#5B6B7F" stroke-width="2"/>'
    o += '<path d="M118 74 l12 6 M140 66 l10 8 M118 102 l12 -6 M140 110 l10 -8 M184 70 l-8 8 M184 106 l-8 -8" stroke="#6B7785" stroke-width="2"/></g>'
    return o
def relic_pot():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<path d="M114 22 h72 q-6 16 6 30 q40 34 18 80 q-14 22 -60 22 q-46 0 -60 -22 q-22 -46 18 -80 q12 -14 6 -30 z" fill="#C98B5A" stroke="#8A5A33" stroke-width="2.5"/>'
    o += '<path d="M104 78 q46 14 92 0 M98 98 q52 14 104 0" fill="none" stroke="#8A5A33" stroke-width="2" stroke-dasharray="6 5"/>'
    o += '<g data-anim="fade" data-dur="1.6" data-delay=".5"><path d="M196 60 l14 18 l-10 10 z" fill="#EEF3F8" stroke="#8A5A33" stroke-width="2"/></g>'
    return o
F['r_bronze'] = relic_bronze(); F['r_arrow'] = relic_arrow(); F['r_pot'] = relic_pot()

# ── S4 연결: 연대 측정·핵폐기물 ──
def ic_carbon():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<path d="M60 120 q10 -40 50 -46 q40 -6 70 10 q30 16 20 40 q-6 12 -40 12 h-80 q-24 0 -20 -16 z" fill="#3A3F47"/>'
    o += '<path d="M90 100 l20 10 M130 92 l16 18 M160 106 l14 6" stroke="#5B6470" stroke-width="3"/>'
    o += '<g data-anim="move" data-from="40,30" data-dur="1.4" data-ease="out"><circle cx="206" cy="66" r="34" fill="#fff" fill-opacity=".35" stroke="#16233D" stroke-width="6"/><line x1="230" y1="90" x2="262" y2="124" stroke="#16233D" stroke-width="10" stroke-linecap="round"/></g>'
    return o
def ic_waste():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<rect x="96" y="30" width="108" height="122" rx="10" fill="#F2C230" stroke="#9A7A12" stroke-width="2.5"/>'
    o += '<line x1="96" y1="62" x2="204" y2="62" stroke="#9A7A12" stroke-width="3"/><line x1="96" y1="120" x2="204" y2="120" stroke="#9A7A12" stroke-width="3"/>'
    cx, cy = 150, 91; s = ''
    for k in range(3):
        a1 = math.radians(-90 + 120 * k - 30); a2 = math.radians(-90 + 120 * k + 30)
        s += f'<path d="M{f(cx + 8 * math.cos(a1))} {f(cy + 8 * math.sin(a1))} L{f(cx + 24 * math.cos(a1))} {f(cy + 24 * math.sin(a1))} A24 24 0 0 1 {f(cx + 24 * math.cos(a2))} {f(cy + 24 * math.sin(a2))} L{f(cx + 8 * math.cos(a2))} {f(cy + 8 * math.sin(a2))} A8 8 0 0 0 {f(cx + 8 * math.cos(a1))} {f(cy + 8 * math.sin(a1))} z" fill="#16233D"/>'
    o += f'<g data-anim="spin" data-speed="24" data-o="{cx},{cy}">{s}</g><circle cx="{cx}" cy="{cy}" r="5" fill="#16233D"/>'
    return o
F['ic_carbon'] = ic_carbon(); F['ic_waste'] = ic_waste()

# ── S5 해 보기: 기포가 나는 비커 ──
def s5_beaker():
    o = f'<rect x="60" y="80" width="150" height="130" fill="{WATER}"/><line x1="60" y1="80" x2="210" y2="80" stroke="{WATER_E}" stroke-width="2"/>'
    o += f'<path d="M50 30 q6 0 6 6 V212 q0 8 8 8 H206 q8 0 8 -8 V36 q0 -6 6 -6" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    rnd = random.Random(5)
    for k in range(9):
        x = 78 + k * 15 + rnd.uniform(-4, 4); y = 110 + rnd.uniform(0, 80); r = rnd.uniform(4, 7)
        o += f'<g data-anim="move" data-from="0,{f(rnd.uniform(40, 70))}" data-dur="{rnd.uniform(1.2, 2):.2f}" data-delay="{rnd.uniform(0, 1):.2f}" data-rep="loop" data-ease="lin"><circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#fff" stroke="{WATER_E}" stroke-width="2"/></g>'
    o += f'<line x1="186" y1="118" x2="236" y2="74" stroke="{MUTED}" stroke-width="1.5"/>'
    o += tex(240, 70, '$\\ce{N2}$ 기포', 20, 'start', INK)
    o += tex(135, 250, '$\\ce{NH4NO2}$ 수용액', 20, 'middle', INK)
    return o
F['s5'] = s5_beaker()

# ── S6 해 보기: 아질산 암모늄 그래프 ──
NH = [(0, .100), (1, .050), (2, .025), (3, .012), (4, .006)]
def s6():
    A = Axes(92, 300, 400, 240, (0, 4.4), (0, .1))
    o = A.frame(xt=[0, 1, 2, 3, 4], yt=[0, .025, .05, .075, .1], xl='$t$ [h]', yl='$[\\ce{NH4NO2}]$ [mol/L]', yfmt=lambda v: f'{v:.3f}')
    o += f'<path d="{A.path(lambda t: .1 * 0.5 ** t, 0, 4)}" fill="none" stroke="{INK}" stroke-width="3.5" data-anim="draw" data-dur="1.3"/>'
    for (t, c) in NH:
        o += A.dot(t, c, INK, 5.5, '#fff')
    o += '<g class="step" data-g="q2">' + halfmarks(A, [(1, .05), (2, .025)])
    o += dim(A.X(0), A.X(1), A.y0 - 16, '1 h', MUTED) + dim(A.X(1), A.X(2), A.y0 - 16, '1 h', MUTED) + '</g>'
    o += '<g class="step" data-g="q3">' + halfmarks(A, [(3, .0125)], FIELD) + dim(A.X(2), A.X(3), A.y0 - 16, '약 1 h', MUTED) + '</g>'
    return o
F['s6'] = s6()

# ── S7 반감기: 오산화 이질소 ──
def s7():
    A = Axes(110, 330, 420, 262, (0, 380), (0, .1))
    o = A.frame(xt=[0, 100, 200, 300], yt=[0, .025, .05, .075, .1], xl='$t$ [s]', yl='$[\\ce{N2O5}]$ [mol/L]', yfmt=lambda v: f'{v:.4f}')
    o += f'<path d="{A.path(lambda t: .1 * 0.5 ** (t / 100), 0, 350)}" fill="none" stroke="{INK}" stroke-width="3.5" data-anim="draw" data-dur="1.3"/>'
    P = [(0, .1), (100, .05), (200, .025), (300, .0125)]
    boxes = [(300, 64), (262, 140), (370, 204), (470, 240)]
    n = [16, 8, 4, 2]
    base = spots(16, 58, 58, 4.5, 7, 3)
    for i, ((t, c), (bx, by)) in enumerate(zip(P, boxes)):
        g = f'<g data-anim="pop" data-o="{bx},{by}" data-delay="{.6 + .3 * i:.1f}" data-dur=".5">'
        g += f'<line x1="{f(A.X(t))}" y1="{f(A.Y(c))}" x2="{f(bx - 29)}" y2="{f(by + 29 if i else by)}" stroke="{MUTED}" stroke-width="1.2"/>'
        g += f'<rect x="{bx - 29}" y="{by - 29}" width="58" height="58" rx="6" fill="#fff" stroke="{GLASS}" stroke-width="2"/>'
        for (x, y) in base[:n[i]]:
            g += dot(bx - 29 + x, by - 29 + y, 4.5, INK)
        g += '</g>'
        o += g
    o += tex(boxes[0][0] + 40, boxes[0][1] + 6, '$\\ce{N2O5}$ 16개', 18, 'start', MUTED)
    for i, (t, c) in enumerate(P[1:]):
        o += f'<g class="step" data-g="h{i + 1}">' + halfmarks(A, [(t, c)]) + dim(A.X(t - 100), A.X(t), A.y0 - 16, '$t_{1/2}$', INK) + '</g>'
    return o
F['s7'] = s7()

# ── S8 처음 농도가 달라도 ──
def s8():
    A = Axes(100, 300, 430, 240, (0, 330), (0, .1))
    o = A.frame(xt=[0, 100, 200, 300], yt=[0, .025, .05, .075, .1], xl='$t$ [s]', yl='$[\\ce{N2O5}]$ [mol/L]', yfmt=lambda v: f'{v:.3f}')
    o += f'<path d="{A.path(lambda t: .1 * 0.5 ** (t / 100), 0, 300)}" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    o += A.dot(0, .1, INK, 5.5, '#fff') + A.dot(100, .05, INK, 5.5, '#fff')
    o += tex(A.X(150), A.Y(.05) - 14, '실험 1', 20, 'start', INK, halo=True)
    o += '<g class="step" data-g="b1">'
    o += f'<path d="{A.path(lambda t: .05 * 0.5 ** (t / 100), 0, 300)}" fill="none" stroke="{MINUS}" stroke-width="3.5" stroke-dasharray="9 6" data-anim="draw" data-dur="1.1" data-on="step"/>'
    o += A.dot(0, .05, MINUS, 5.5, '#fff') + A.dot(100, .025, MINUS, 5.5, '#fff')
    o += tex(A.X(150), A.Y(.0177) + 26, '실험 2', 20, 'start', MINUS, halo=True)
    o += halfmarks(A, [(100, .05), (100, .025)])
    o += dim(A.X(0), A.X(100), A.y0 - 16, '두 실험 모두 100 s', INK, 19)
    o += '</g>'
    return o
F['s8'] = s8()

# ── S9 반감기가 일정한 까닭: 입자 카드 ──
S9P = spots(16, 200, 120, 9, 11, 4)
def s9card(k):
    nA = 16 >> k
    o = f'<rect x="10" y="6" width="200" height="120" rx="10" fill="#fff" stroke="{GLASS}" stroke-width="2"/>'
    for i, (x, y) in enumerate(S9P):
        if i < nA:
            o += dot(10 + x, 6 + y, 9, INK)
        else:
            o += dot(10 + x, 6 + y, 9, FIELD, extra='' if i < (16 >> max(k - 1, 0)) or k == 0 else '')
    w = 180 * nA / 16
    o += f'<g data-anim="scale" data-from="0,1" data-o="20,156" data-dur=".8"><rect x="20" y="146" width="{f(w)}" height="20" rx="4" fill="{INK}"/></g>'
    o += f'<rect x="20" y="146" width="180" height="20" rx="4" fill="none" stroke="#C9D3DD" stroke-width="1.5" stroke-dasharray="4 3"/>'
    return o
for k in range(4):
    F[f's9_{k}'] = s9card(k)

# ── S13 방사성 탄소 그래프 (S14에서 다시 씀) ──
def c14(mark=False):
    A = Axes(100, 290, 450, 230, (0, 21500), (0, 1))
    T = 5730
    o = A.frame(xt=[0, T, 2 * T, 3 * T], yt=[0, .25, .5, .75, 1], xl='$t$ [년]', yl='남은 비율 (대기 = 1)', yfmt=lambda v: f'{v:.2f}' if v not in (0, 1) else f'{v:.0f}', ts=20)
    o += f'<path d="{A.path(lambda t: 0.5 ** (t / T), 0, 20000)}" fill="none" stroke="{INK}" stroke-width="3.5" data-anim="draw" data-dur="1.4"/>'
    o += halfmarks(A, [(T, .5), (2 * T, .25), (3 * T, .125)])
    for i in range(3):
        o += A.dot((i + 1) * T, 0.5 ** (i + 1), INK, 5.5, '#fff')
    o += A.dot(0, 1, INK, 5.5, '#fff')
    o += tex(A.X(T) + 10, A.Y(.5) - 12, '\\tfrac{1}{2}', 22, 'start', INK, mix=False, halo=True)
    o += tex(A.X(2 * T) + 10, A.Y(.25) - 12, '\\tfrac{1}{4}', 22, 'start', INK, mix=False, halo=True)
    o += tex(A.X(3 * T) + 10, A.Y(.125) - 14, '\\tfrac{1}{8}', 22, 'start', INK, mix=False, halo=True)
    if mark:
        v = 0.5 ** (3000 / T)
        o += '<g class="step" data-g="m1">' + A.line(3000, 0, 3000, v, PLUS, 2, '4 4') + A.line(0, v, 3000, v, PLUS, 2, '4 4') + A.dot(3000, v, PLUS, 7, PLUS)
        o += tex(A.X(3000) + 12, A.Y(v) - 10, '3000년 → 약 0.7', 20, 'start', PLUS, halo=True) + '</g>'
    return o
F['c14'] = c14(); F['c14m'] = c14(True)

# ── S15 조사·발표 과정 아이콘 ──
def ic_search():
    o = '<rect x="4" y="4" width="252" height="132" rx="12" fill="#EEF3F8"/>'
    o += '<rect x="86" y="16" width="64" height="108" rx="10" fill="#16233D"/><rect x="92" y="28" width="52" height="82" rx="3" fill="#E3EEFB"/>'
    o += '<g data-anim="pop" data-o="170,70" data-dur=".6"><circle cx="160" cy="62" r="20" fill="#fff" fill-opacity=".6" stroke="#16233D" stroke-width="5"/><line x1="174" y1="76" x2="194" y2="98" stroke="#16233D" stroke-width="7" stroke-linecap="round"/></g>'
    o += '<rect x="40" y="40" width="34" height="46" rx="3" fill="#fff" stroke="#5B6B7F" stroke-width="2"/><path d="M46 52 h22 M46 62 h22 M46 72 h16" stroke="#9AA5B1" stroke-width="2"/>'
    return o
def ic_share():
    o = '<rect x="4" y="4" width="252" height="132" rx="12" fill="#EEF3F8"/>'
    for (x, c) in ((70, '#1F6FD1'), (130, '#2E9E6A'), (190, '#E08A2C')):
        o += f'<circle cx="{x}" cy="58" r="16" fill="{c}"/><path d="M{x - 26} 112 q0 -34 26 -34 q26 0 26 34 z" fill="{c}"/>'
    o += '<g data-anim="pop" data-o="130,24" data-dur=".6" data-delay=".3"><rect x="104" y="10" width="52" height="26" rx="8" fill="#fff" stroke="#5B6B7F" stroke-width="2"/><circle cx="118" cy="23" r="3" fill="#5B6B7F"/><circle cx="130" cy="23" r="3" fill="#5B6B7F"/><circle cx="142" cy="23" r="3" fill="#5B6B7F"/></g>'
    return o
def ic_present():
    o = '<rect x="4" y="4" width="252" height="132" rx="12" fill="#EEF3F8"/>'
    o += '<rect x="70" y="16" width="150" height="84" rx="6" fill="#fff" stroke="#5B6B7F" stroke-width="2.5"/><line x1="145" y1="100" x2="145" y2="126" stroke="#5B6B7F" stroke-width="3"/>'
    o += '<path d="M84 86 q30 -58 66 -46 q30 10 58 -10" fill="none" stroke="#16233D" stroke-width="3" data-anim="draw" data-dur="1"/>'
    o += '<circle cx="44" cy="62" r="13" fill="#7B4FC8"/><path d="M24 122 q0 -40 20 -40 q20 0 20 40 z" fill="#7B4FC8"/><line x1="58" y1="88" x2="88" y2="70" stroke="#16233D" stroke-width="3"/>'
    return o
F['ic_search'] = ic_search(); F['ic_share'] = ic_share(); F['ic_present'] = ic_present()

# ── S16 사례 아이콘 ──
def ic_wine():
    o = '<rect x="4" y="4" width="252" height="112" rx="12" fill="#EEF3F8"/>'
    o += '<path d="M118 14 h24 v24 q16 10 16 30 v38 h-56 v-38 q0 -20 16 -30 z" fill="#5A1F35" stroke="#3A1222" stroke-width="2"/><rect x="108" y="62" width="44" height="26" rx="3" fill="#F4ECD8"/>'
    o += '<g data-anim="move" data-from="-30,0" data-dur="1.2" data-ease="out"><circle cx="186" cy="56" r="22" fill="#fff" fill-opacity=".4" stroke="#16233D" stroke-width="5"/><line x1="202" y1="72" x2="222" y2="94" stroke="#16233D" stroke-width="7" stroke-linecap="round"/></g>'
    return o
def ic_pill():
    o = '<rect x="4" y="4" width="252" height="112" rx="12" fill="#EEF3F8"/>'
    o += '<g transform="rotate(-30 110 60)"><rect x="66" y="44" width="88" height="34" rx="17" fill="#fff" stroke="#5B6B7F" stroke-width="2"/><path d="M110 44 h27 a17 17 0 0 1 0 34 h-27 z" fill="#D7263D"/></g>'
    o += '<g data-anim="fade" data-dur="1" data-delay=".3"><circle cx="196" cy="58" r="30" fill="#fff" stroke="#5B6B7F" stroke-width="2"/><line x1="196" y1="58" x2="196" y2="36" stroke="#16233D" stroke-width="3"/><line x1="196" y1="58" x2="212" y2="66" stroke="#16233D" stroke-width="3"/></g>'
    return o
def ic_drum():
    o = '<rect x="4" y="4" width="252" height="112" rx="12" fill="#EEF3F8"/>'
    for x in (80, 150):
        o += f'<rect x="{x}" y="22" width="56" height="78" rx="6" fill="#F2C230" stroke="#9A7A12" stroke-width="2"/><line x1="{x}" y1="44" x2="{x + 56}" y2="44" stroke="#9A7A12" stroke-width="2.5"/><line x1="{x}" y1="78" x2="{x + 56}" y2="78" stroke="#9A7A12" stroke-width="2.5"/><circle cx="{x + 28}" cy="61" r="9" fill="#16233D"/>'
    return o
F['ic_wine'] = ic_wine(); F['ic_pill'] = ic_pill(); F['ic_drum'] = ic_drum()

# ── S17 과학 마당: 생성기 → 의약품 → 촬영 ──
def s17():
    o = ''
    # 생성기
    o += f'<rect x="20" y="40" width="110" height="130" rx="14" fill="#E3EEFB" stroke="{MUTED}" stroke-width="2.5"/><rect x="48" y="66" width="54" height="80" rx="6" fill="#C9D3DD" stroke="{MUTED}" stroke-width="2"/>'
    o += tex(75, 112, '\\ce{^{68}_{32}Ge}', 22, 'middle', INK, mix=False)
    o += tex(75, 198, '생성기', 20, 'middle', INK) + tex(75, 222, '반감기 약 270일', 19, 'middle', MUTED)
    o += '<g data-arw="140,105,210,105,ink,3"></g>' + tex(175, 92, '추출', 19, 'middle', INK)
    # 의약품
    o += f'<g data-anim="move" data-from="-60,0" data-dur="1" data-delay=".4" data-ease="out"><rect x="226" y="70" width="70" height="70" rx="10" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/><rect x="232" y="100" width="58" height="34" rx="4" fill="#FDE2E4"/>'
    o += tex(261, 124, '\\ce{^{68}_{31}Ga}', 22, 'middle', INK, mix=False) + '</g>'
    o += tex(261, 198, '방사성 의약품', 20, 'middle', INK) + tex(261, 222, '반감기 약 68분', 19, 'middle', MUTED)
    o += '<g data-arw="306,105,370,105,ink,3"></g>' + tex(338, 92, '주사', 19, 'middle', INK)
    # PET
    o += f'<circle cx="440" cy="105" r="62" fill="#EEF3F8" stroke="{MUTED}" stroke-width="12"/><circle cx="440" cy="105" r="40" fill="#fff" stroke="{MUTED}" stroke-width="2"/>'
    o += f'<g data-anim="spin" data-speed="40" data-o="440,105">' + ''.join(f'<rect x="{f(440 + 62 * math.cos(math.radians(a)) - 4)}" y="{f(105 + 62 * math.sin(math.radians(a)) - 4)}" width="8" height="8" fill="{PLUS}"/>' for a in range(0, 360, 45)) + '</g>'
    o += tex(440, 198, '양전자 방출', 20, 'middle', INK) + tex(440, 222, '단층 촬영', 20, 'middle', INK)
    return o
F['s17'] = s17()

# ── S20 확인 문제 01 그래프 ──
def s20():
    A = Axes(80, 270, 380, 220, (0, 80), (0, .8))
    o = A.frame(xt=[0, 20, 40, 60, 80], yt=[0, .2, .4, .6, .8], xl='$t$ [s]', yl='$[\\ce{A}]$ [mol/L]', yfmt=lambda v: f'{v:.1f}' if v else '0')
    o += f'<path d="{A.path(lambda t: .8 * 0.5 ** (t / 20), 0, 60)}" fill="none" stroke="{INK}" stroke-width="3.5" data-anim="draw" data-dur="1.2"/>'
    for (t, c) in ((0, .8), (20, .4), (40, .2), (60, .1)):
        o += A.dot(t, c, INK, 5.5, '#fff')
        o += f'<line x1="{f(A.x0)}" y1="{f(A.Y(c))}" x2="{f(A.X(t))}" y2="{f(A.Y(c))}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 4"/>'
    o += tex(A.X(60) + 10, A.Y(.1) - 12, '0.10', 18, 'start', INK, mix=False, halo=True)
    return o
F['s20'] = s20()

# ── S22 대단원 마무리 04 입자 모형 ──
def s22box(x0, nA, nB, seed, lab):
    o = f'<rect x="{x0}" y="10" width="210" height="160" rx="12" fill="#F4F8FC" stroke="{GLASS}" stroke-width="3"/>'
    pts = spots(nA + nB, 210, 160, 11, seed, 8)
    rnd = random.Random(seed + 1); idx = list(range(len(pts))); rnd.shuffle(idx)
    for j, i in enumerate(idx):
        x, y = pts[i]
        o += dot(x0 + x, 10 + y, 11, INK if j < nA else FIELD)
    o += tex(x0 + 105, 198, lab, 21, 'middle', INK)
    return o
def s22():
    o = s22box(10, 2, 12, 3, '(가)') + s22box(250, 1, 6, 9, '(나)')
    o += f'<rect x="478" y="40" width="80" height="78" rx="8" fill="#fff" stroke="#C9D3DD" stroke-width="1.5"/>'
    o += dot(498, 64, 11, INK) + tex(518, 71, '$\\mathrm{A}$', 21, 'start', INK) + dot(498, 96, 11, FIELD) + tex(518, 103, '$\\mathrm{B}$', 21, 'start', INK)
    return o
F['s22'] = s22()

tpl = open(os.path.join(HERE, 'tpl.html'), encoding='utf-8').read()
def rep(m):
    k = m.group(1)
    if k not in F: raise KeyError(k)
    return F[k]
html = re.sub(r'@@(\w+)@@', rep, tpl)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('slides.html', len(html))
