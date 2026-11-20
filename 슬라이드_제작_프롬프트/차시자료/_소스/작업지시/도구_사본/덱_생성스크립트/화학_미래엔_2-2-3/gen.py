# 2-2-3 그림 생성: slides.tpl.html 의 @@이름@@ 를 SVG 조각으로 바꿔 slides.html 을 만든다.
import math, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

CHI = {'H': 2.2, 'B': 2.0, 'C': 2.6, 'N': 3.0, 'O': 3.4, 'F': 4.0, 'S': 2.6, 'Cl': 3.2}
PLUS, MINUS = '#D7263D', '#1F6FD1'
K = 55  # 전기음성도 차이 1 당 화살표 길이(px)
F = {}


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
V31 = best_view(3, 1, 107)


def arw(x1, y1, x2, y2, col='ink', w=3, tail=True):
    """쌍극자 화살표 ⟼ : data-arw + 꼬리에서 15% 지점 수직 막대(길이 14)"""
    s = f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}"></g>'
    if tail:
        L = math.hypot(x2 - x1, y2 - y1) or 1
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        tx, ty = x1 + ux * L * 0.15, y1 + uy * L * 0.15
        c = {'ink': INK, 'plus': PLUS}.get(col, col)
        h = 7 if w <= 3 else 9
        s += f'<line x1="{f(tx - uy * h)}" y1="{f(ty + ux * h)}" x2="{f(tx + uy * h)}" y2="{f(ty - ux * h)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    return f'<g>{s}</g>'


def lab(x, y, tex, size=22, col=None, anchor='middle', mix=False, extra=''):
    fill = f' fill="{col}"' if col else ''
    key = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {key}="{tex}" data-size="{size}" data-anchor="{anchor}"{fill}{extra}></text>'


def mol(cx, cy, center, outer, n_lone=0, ang=None, L=110, yaw=0, pitch=0, orders=None, dirs=None,
        dip=True, off=26, sides=None, delta=False, dsize=22, summ=None, sum_g=None, dip_g=None, anim_out=None,
        lobes=False, scale=1.0, dlab_off=None, first_atom_center=False):
    """공-막대 + 결합 쌍극자 화살표(⟼). 반환 (svg, 정보)"""
    body = ballstick(cx, cy, center, outer, n_lone=n_lone, ang=ang, L=L, yaw=yaw, pitch=pitch, scale=scale,
                     extra_bond_orders=orders, dirs=dirs, lobes=lobes, anim_out=anim_out)
    if dirs is None:
        bd, ld = angle_dirs(n_lone, len(outer), ang)
    else:
        bd = dirs
    bd3 = [rot(norm(d), yaw, pitch) for d in bd]
    pos = []
    for el, d in zip(outer, bd3):
        l = L * scale * (0.82 if el == 'H' else 1.0)
        pos.append((cx + d[0] * l, cy - d[1] * l))
    out = ''
    tot = [0, 0, 0]
    info = {'pos': pos, 'c': (cx, cy)}
    gx = sum(p[0] for p in pos) / len(pos)
    gy = sum(p[1] for p in pos) / len(pos)
    arrows = ''
    dl = ''
    for k, (el, d, p) in enumerate(zip(outer, bd3, pos)):
        dchi = CHI[el] - CHI[center]
        for c in range(3):
            tot[c] += d[c] * dchi
        if abs(dchi) < 1e-6:
            continue
        # 화면 결합 방향
        vx, vy = p[0] - cx, p[1] - cy
        n = math.hypot(vx, vy) or 1
        ux, uy = vx / n, vy / n
        px, py = -uy, ux
        mx, my = (cx + p[0]) / 2, (cy + p[1]) / 2
        sd = (sides or {}).get(k)
        if sd is None:
            # 분자 바깥쪽(무게중심 반대)으로
            sd = 1 if (px * (mx - gx) + py * (my - gy)) >= 0 else -1
            if abs(px * (mx - gx) + py * (my - gy)) < 1e-3:
                sd = 1 if py < 0 else -1  # 위쪽
        ax, ay = mx + px * off * sd, my + py * off * sd
        ln = max(30, K * abs(dchi))
        s = 1 if dchi > 0 else -1  # + 면 결합 원자 쪽
        x1, y1 = ax - ux * ln / 2 * s, ay - uy * ln / 2 * s
        x2, y2 = ax + ux * ln / 2 * s, ay + uy * ln / 2 * s
        arrows += arw(x1, y1, x2, y2)
        if delta:
            o = dlab_off or 34
            # 결합 원자 쪽 δ 라벨: 결합 방향 바깥쪽
            r = R[el] * scale
            lx, ly = p[0] + ux * (r + 6) + px * sd * 4, p[1] + uy * (r + 6)
            t = '\\delta^-' if dchi > 0 else '\\delta^+'
            col = MINUS if dchi > 0 else PLUS
            dl += lab(p[0] - px * sd * (r + 14) + ux * 6, p[1] - py * sd * (r + 14) + uy * 6 + dsize * 0.36, t, dsize, col)
    if dip:
        g = f' class="step" data-g="{dip_g}"' if dip_g else ''
        out += f'<g{g}>{arrows}</g>'
    info['sum'] = tot
    return body + out, info, dl


# ───────── 그림 ─────────

def h2o_dirs(ang=104.5):
    h = math.radians(ang / 2)
    return [(-math.sin(h), -math.cos(h), 0), (math.sin(h), -math.cos(h), 0)]


def center_delta(cx, cy, r, tex, col, dx=0, dy=-1, size=22, d=14):
    return lab(cx + dx * (r + d), cy + dy * (r + d) + size * 0.36, tex, size, col)


# 표지: 물
def cover():
    cx, cy, L, sc = 270, 230, 150, 1.5
    body, info, _ = mol(cx, cy, 'O', ['H', 'H'], dirs=h2o_dirs(), L=L, scale=sc, dip=False)
    (x1, y1), (x2, y2) = info['pos']
    s = f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>' + body
    # 결합 쌍극자: 바깥쪽
    arrs = ''
    for (px_, py_), sd in (((x1, y1), -1), ((x2, y2), 1)):
        vx, vy = cx - px_, cy - py_
        n = math.hypot(vx, vy); ux, uy = vx / n, vy / n
        nx, ny = -uy * sd, ux * sd
        mx, my = (cx + px_) / 2 + nx * 40, (cy + py_) / 2 + ny * 40
        ln = 1.2 * K * 1.4
        arrs += arw(mx - ux * ln / 2, my - uy * ln / 2, mx + ux * ln / 2, my + uy * ln / 2)
    s += f'<g data-anim="fade" data-dur=".6" data-delay=".4">{arrs}</g>'
    s += f'<g data-anim="fade" data-dur=".6" data-delay="1.4">{arw(270, 440, 270, 320, "plus", 6)}</g>'
    s += lab(x1 - 4, y1 + 64, '\\delta^+', 30, PLUS) + lab(x2 + 4, y2 + 64, '\\delta^+', 30, PLUS) + lab(270, cy - 52, '\\delta^-', 30, MINUS)
    s += lab(270, 500, '물 $\\ce{H2O}$: 극성 분자', 22, MUTED, mix=True)
    return s


F['COVER'] = cover()

# S4 연결: H–Cl 화살표, CO2, H2O
def s4():
    out = '<line x1="70" y1="70" x2="170" y2="70" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/><g data-atom="70,70,18,H"></g><g data-atom="170,70,29,Cl"></g>'
    out += lab(70, 36, '\\delta^+', 22, PLUS) + lab(170, 30, '\\delta^-', 22, MINUS) + arw(66, 122, 176, 122)
    out += lab(290, 78, '결합의 쌍극자 모멘트||$\\delta^+\\to\\delta^-$', 20, MUTED, mix=True, anchor='start')
    return out
F['S4A'] = s4()
b, _, _ = mol(110, 60, 'C', ['O', 'O'], L=80, orders={0: 2, 1: 2}, dip=False)
F['S4CO2'] = b
b, _, _ = mol(110, 40, 'O', ['H', 'H'], dirs=h2o_dirs(), L=84, dip=False)
F['S4H2O'] = b

# S6 H2, HF
F['S6H2'] = ('<line x1="90" y1="80" x2="170" y2="80" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/><g data-atom="90,80,18,H"></g><g data-atom="170,80,18,H"></g>'
             + lab(130, 150, '쌍극자 모멘트 $=0$', 21, MUTED, mix=True))
F['S6HF'] = ('<line x1="80" y1="80" x2="180" y2="80" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/><g data-atom="80,80,18,H"></g><g data-atom="180,80,24,F"></g>'
             + lab(80, 44, '\\delta^+', 22, PLUS) + lab(180, 38, '\\delta^-', 22, MINUS)
             + f'<g data-anim="fade" data-dur=".6" data-delay=".6">{arw(80, 136, 180, 136)}</g>')

# S7 CO2 큰 그림
def s7():
    cx, cy = 260, 120
    body, info, _ = mol(cx, cy, 'C', ['O', 'O'], L=130, orders={0: 2, 1: 2}, dip=False)
    (x1, y1), (x2, y2) = info['pos']
    a = 0.8 * K * 1.4
    s = body
    s += f'<g data-anim="fade" data-dur=".5" data-delay=".5">{arw(cx - 20, 62, cx - 20 - a, 62)}{arw(cx + 20, 62, cx + 20 + a, 62)}</g>'
    s += lab(x1, cy + 64, '\\delta^-', 24, MINUS) + lab(x2, cy + 64, '\\delta^-', 24, MINUS) + lab(cx, cy + 64, '\\delta^+', 24, PLUS)
    s += f'<g class="step" data-g="c7">' + lab(cx, 214, '크기 같고 방향 반대 → 합 $=0$', 22, None, mix=True) + '</g>'
    return s
F['S7'] = s7()

# S8 H2O 큰 그림
def s8():
    cx, cy, L = 250, 80, 130
    body, info, _ = mol(cx, cy, 'O', ['H', 'H'], dirs=h2o_dirs(), L=L, dip=False)
    (x1, y1), (x2, y2) = info['pos']
    s = body
    arrs = ''
    for (px_, py_), sd in (((x1, y1), -1), ((x2, y2), 1)):
        vx, vy = cx - px_, cy - py_
        n = math.hypot(vx, vy); ux, uy = vx / n, vy / n
        nx, ny = -uy * sd, ux * sd
        mx, my = (cx + px_) / 2 + nx * 30, (cy + py_) / 2 + ny * 30
        ln = 1.2 * K * 1.2
        arrs += arw(mx - ux * ln / 2, my - uy * ln / 2, mx + ux * ln / 2, my + uy * ln / 2)
    s += f'<g data-anim="fade" data-dur=".5" data-delay=".5">{arrs}</g>'
    s += lab(x1 - 4, y1 + 46, '\\delta^+', 24, PLUS) + lab(x2 + 4, y2 + 46, '\\delta^+', 24, PLUS) + lab(cx + 46, cy - 18, '\\delta^-', 24, MINUS)
    s += (f'<g class="step" data-g="s8"><g data-anim="fade" data-dur=".6" data-delay=".2">{arw(cx, 206, cx, 122, "plus", 5)}</g>'
          + lab(cx + 16, 226, '분자의 쌍극자 모멘트', 20, PLUS, anchor='start', mix=True) + '</g>')
    return s
F['S8'] = s8()

# S10/S12 NH3, CH4
def tetra(center, outer, nl, cx, cy, view, ang=None, L=110, dip=True, dip_g=None, lobes=False):
    return mol(cx, cy, center, outer, n_lone=nl, ang=ang, L=L, yaw=view[0], pitch=view[1], dip=dip, dip_g=dip_g, off=20, lobes=lobes)

b, i_nh3, _ = tetra('N', ['H'] * 3, 1, 160, 110, V31, ang=107, L=128, dip=True, dip_g='a10', lobes=True)
F['S10NH3'] = b
b, i_ch4, _ = tetra('C', ['H'] * 4, 0, 160, 125, V4, L=128, dip=True, dip_g='a10')
F['S10CH4'] = b

def sum_box(x, y, info, col_g=None, delay=.3, scale=1.0, z=False):
    """합 벡터: 같은 시점 투영. info['sum'] (3D)"""
    sx, sy, sz = info['sum']
    m = math.sqrt(sx * sx + sy * sy + sz * sz)
    if m < 0.05:
        return lab(x, y + 8, '합 $=0$', 22, PLUS, mix=True)
    return None

b, i, _ = tetra('N', ['H'] * 3, 1, 160, 100, V31, ang=107, L=128, lobes=True)
F['S12NH3'] = b + f'<g class="step" data-g="b12"><g data-anim="fade" data-dur=".6" data-delay=".2">{arw(272, 230, 272, 150, "plus", 5)}</g>' + lab(272, 254, '합 $\\neq0$', 21, PLUS, mix=True) + '</g>'
b, i, _ = tetra('C', ['H'] * 4, 0, 160, 115, V4, L=128)
F['S12CH4'] = b + '<g class="step" data-g="b12">' + lab(160, 244, '합 $=0$', 22, PLUS, mix=True) + '</g>'

# S13 비교 6개 (작게: L 90)
def s13(key):
    if key == 'CO2':
        return mol(170, 80, 'C', ['O', 'O'], L=92, orders={0: 2, 1: 2}, off=24)[0]
    if key == 'HCN':
        return mol(170, 80, 'C', ['H', 'N'], L=92, orders={1: 3}, off=24, sides={0: 1, 1: 1})[0]
    if key == 'BCl3':
        return mol(170, 110, 'B', ['Cl'] * 3, L=74, off=20)[0]
    if key == 'CH2O':
        a = lambda d: (math.cos(math.radians(d)), math.sin(math.radians(d)), 0)
        return mol(170, 112, 'C', ['O', 'H', 'H'], dirs=[a(90), a(210), a(330)], L=80, orders={0: 2}, off=20)[0]
    if key == 'CH4':
        return mol(170, 108, 'C', ['H'] * 4, L=82, yaw=V4[0], pitch=V4[1], off=18)[0]
    if key == 'CH3Cl':
        return mol(170, 118, 'C', ['Cl', 'H', 'H', 'H'], L=80, yaw=V4[0], pitch=V4[1], off=18)[0]
for k in ('CO2', 'HCN', 'BCl3', 'CH2O', 'CH4', 'CH3Cl'):
    F['S13' + k] = s13(k)

# S15/S16 F2, HF
F['F2'] = '<line x1="80" y1="70" x2="180" y2="70" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/><g data-atom="80,70,24,F"></g><g data-atom="180,70,24,F"></g>'
F['HF'] = '<line x1="80" y1="70" x2="180" y2="70" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/><g data-atom="80,70,18,H"></g><g data-atom="180,70,24,F"></g>'


# 평행판 + 분자 배치
def plates(W, H, left='(-)극', right='(+)극'):
    lt = '(−)극' if left == '(-)극' else '(+)극'
    rt = '(+)극' if right == '(+)극' else '(−)극'
    s = f'<rect x="20" y="40" width="14" height="{H - 60}" fill="#8C99A6"/><rect x="{W - 34}" y="40" width="14" height="{H - 60}" fill="#8C99A6"/>'
    s += lab(27, 30, lt, 20, MINUS if '−' in lt else PLUS, mix=True) + lab(W - 27, 30, rt, 20, PLUS if '+' in rt else MINUS, mix=True)
    return s


def diat(x, y, a, e1, e2, d=46, lab1=True, anim=None):
    """이원자 분자: 중심 x,y, 각도 a(도, e1 → e2 방향), 원자 e1, e2"""
    t = math.radians(a)
    ux, uy = math.cos(t), math.sin(t)
    x1, y1, x2, y2 = x - ux * d / 2, y - uy * d / 2, x + ux * d / 2, y + uy * d / 2
    l = '' if lab1 else ',-'
    s = f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/>'
    s += f'<g data-atom="{f(x1)},{f(y1)},{R[e1]},{e1}{l}"></g><g data-atom="{f(x2)},{f(y2)},{R[e2]},{e2}{l}"></g>'
    if anim:
        s = f'<g data-anim="rot" data-from="{anim}" data-o="{f(x)},{f(y)}" data-dur="1.4" data-delay=".3" data-ease="soft">{s}</g>'
    return s


import random
random.seed(7)
PTS6 = [(95, 85), (205, 75), (100, 170), (210, 165), (110, 250), (215, 245)]
def field_panel(polar, W=300, H=290, flip=False, anim=False, e=('H', 'F'), lab1=True, pts=PTS6, rnd=None):
    s = plates(W, H, '(+)극' if flip else '(-)극', '(-)극' if flip else '(+)극')
    rr = random.Random(rnd or 3)
    for k, (x, y) in enumerate(pts):
        if polar:
            a = (180 if flip else 0) + rr.uniform(-8, 8)  # e1(H) 왼쪽 → (−)극 쪽
            # e1 → e2 방향 a: e1 가 a 반대쪽. a=0 이면 e1 왼쪽.
            fr = rr.choice([-70, 80, 120, -110]) if anim else None
            s += diat(x, y, a, e[0], e[1], lab1=lab1, anim=fr)
        else:
            a = rr.uniform(0, 360)
            s += diat(x, y, a, e[0], e[1], lab1=lab1)
    return s
F['S18A'] = field_panel(True, anim=True)
F['S18B'] = field_panel(False, e=('F', 'F'), rnd=11)
F['S18C'] = field_panel(True, flip=True, rnd=5)
F['S18D'] = field_panel(False, e=('F', 'F'), rnd=19)

# Q09: A 8개 정렬, 라벨 없음 (Cl 색 + H 색)
PTS8 = [(150, 80), (300, 92), (110, 165), (230, 150), (380, 160), (160, 240), (290, 228), (410, 250)]
def q09():
    s = plates(520, 300)
    s += lab(150, 52, '\\mathrm{A}', 22)
    rr = random.Random(2)
    for (x, y) in PTS8:
        s += diat(x, y, rr.uniform(-10, 10), 'H', 'Cl', d=48, lab1=False)
    return s
F['Q09'] = q09()

# Q08: CH2O 평면 삼각형
a = lambda d: (math.cos(math.radians(d)), math.sin(math.radians(d)), 0)
F['Q08'] = ballstick(180, 120, 'C', ['O', 'H', 'H'], dirs=[a(90), a(212), a(328)], L=100, extra_bond_orders={0: 2}, lobes=False)


# 물줄기와 대전체
def stream(sign):
    s = ''
    # 수도꼭지(뷰렛 꼭지) 단순 도식
    s += '<rect x="78" y="10" width="44" height="34" rx="6" fill="#C9D2DB" stroke="#7E8B98" stroke-width="2"/><rect x="92" y="44" width="16" height="18" fill="#C9D2DB" stroke="#7E8B98" stroke-width="2"/>'
    s += '<line x1="100" y1="64" x2="100" y2="290" stroke="#8C99A6" stroke-width="2" stroke-dasharray="6 6"/>'
    s += '<path d="M100 64 C100 130 108 170 150 230 C168 255 176 272 180 292" fill="none" stroke="#7FB6E0" stroke-width="9" stroke-linecap="round" data-anim="draw" data-dur="1.4" data-delay=".4"/>'
    # 대전체 막대
    col = MINUS if sign == '-' else PLUS
    s += f'<rect x="196" y="186" width="150" height="26" rx="6" fill="#EEF1F4" stroke="{col}" stroke-width="2.5"/>'
    for k in range(4):
        xx = 222 + k * 32
        s += f'<line x1="{xx - 7}" y1="199" x2="{xx + 7}" y2="199" stroke="{col}" stroke-width="3"/>'
        if sign == '+':
            s += f'<line x1="{xx}" y1="192" x2="{xx}" y2="206" stroke="{col}" stroke-width="3"/>'
    s += lab(272, 246, '(−)대전체' if sign == '-' else '(+)대전체', 21, col, mix=True)
    # 확대 원 + 물 분자
    s += '<circle cx="245" cy="98" r="74" fill="#fff" stroke="#8C99A6" stroke-width="2"/><line x1="150" y1="170" x2="196" y2="140" stroke="#8C99A6" stroke-width="1.5" stroke-dasharray="4 4"/>'
    # 물 분자: (−) → H 가 대전체(아래 오른쪽) 쪽, (+) → O 가 대전체 쪽
    if sign == '-':
        dirs = [rot(d, 0, 0) for d in h2o_dirs()]
        body = ballstick(240, 76, 'O', ['H', 'H'], dirs=dirs, L=48, lobes=False)
        mol_ = f'<g data-anim="rot" data-from="-90" data-o="240,76" data-dur="1.2" data-delay="1.4" data-ease="soft">{body}</g>'
        mol_ += lab(200, 148, '\\delta^+', 20, PLUS) + lab(280, 148, '\\delta^+', 20, PLUS) + lab(274, 50, '\\delta^-', 20, MINUS)
    else:
        dirs = [(-d[0], -d[1], 0) for d in h2o_dirs()]
        body = ballstick(250, 118, 'O', ['H', 'H'], dirs=dirs, L=48, lobes=False)
        mol_ = f'<g data-anim="rot" data-from="90" data-o="250,118" data-dur="1.2" data-delay="1.4" data-ease="soft">{body}</g>'
        mol_ += lab(206, 58, '\\delta^+', 20, PLUS) + lab(294, 58, '\\delta^+', 20, PLUS) + lab(284, 146, '\\delta^-', 20, MINUS)
    return s + mol_
F['STR_M'] = stream('-')
F['STR_P'] = stream('+')


# 전자레인지: 전기장 방향과 물 분자
def mw(flip, swing=False):
    s = ''
    yy = [50, 150]
    for y in yy:
        if flip:
            s += f'<g data-arw="250,{y + 40},30,{y + 40},muted,2.5"></g>'
        else:
            s += f'<g data-arw="30,{y + 40},250,{y + 40},muted,2.5"></g>'
    s += lab(140, 30, '전기장 방향', 20, MUTED, mix=True)
    for k, (x, y) in enumerate([(80, 140), (200, 140)]):
        # 분자 쌍극자가 전기장 방향을 따름: O(δ−) 이 전기장 반대쪽(+ 쪽)... 단순화: 쌍극자 화살표 = 전기장 반대
        dirs = [(-math.cos(math.radians(52.25)), math.sin(math.radians(52.25)) * (-1), 0)]
        ang = 0 if not flip else 180
        h = math.radians(52.25)
        # 굽은 물: H 두 개가 오른쪽(전기장이 오른쪽이면 H 가 오른쪽)
        d1 = (math.cos(h), math.sin(h), 0)
        d2 = (math.cos(h), -math.sin(h), 0)
        if flip:
            d1 = (-d1[0], d1[1], 0); d2 = (-d2[0], d2[1], 0)
        body = ballstick(x, y, 'O', ['H', 'H'], dirs=[d1, d2], L=46, lobes=False)
        if swing:
            body = f'<g data-anim="rot" data-from="40" data-o="{x},{y}" data-rep="swing" data-dur=".7" data-ease="sine">{body}</g>'
        s += body
    return s
F['MW1'] = mw(False)
F['MW2'] = mw(True)
F['MW3'] = mw(False, swing=True).replace('전기장 방향', '계속 바뀜')


# 유리병
def vial(x, top, bot, lab_side=False):
    s = f'<rect x="{x + 18}" y="20" width="84" height="30" rx="5" fill="#2E3A48"/>'
    s += f'<rect x="{x + 10}" y="52" width="100" height="190" rx="14" fill="#fff" stroke="#7E8B98" stroke-width="2.5"/>'
    s += f'<rect x="{x + 13}" y="120" width="94" height="58" fill="{top}"/>'
    s += f'<path d="M{x + 13} 178 L{x + 107} 178 L{x + 107} 226 Q{x + 107} 239 {x + 94} 239 L{x + 26} 239 Q{x + 13} 239 {x + 13} 226 Z" fill="{bot}"/>'
    s += f'<line x1="{x + 13}" y1="178" x2="{x + 107}" y2="178" stroke="#9FC3DD" stroke-width="1.5"/>'
    return s
def vials():
    s = ''
    s += vial(110, '#F4F7FA', '#DDEEF8')
    s += lab(112, 154, '헥세인', 20, None, anchor='end', mix=True) + lab(112, 214, '물', 20, None, anchor='end', mix=True)
    s += '<line x1="114" y1="148" x2="128" y2="148" stroke="#5B6B7F" stroke-width="1.5"/><line x1="114" y1="208" x2="128" y2="208" stroke="#5B6B7F" stroke-width="1.5"/>'
    s += lab(170, 276, '(가)', 21, mix=True)
    s += '<g class="step" data-g="v2"><g data-arw="246,140,290,140,muted,3"></g>' + vial(300, '#F4F7FA', '#DDEEF8') + \
         f'<g data-anim="fade" data-dur="1" data-delay=".3"><path d="M313 178 L407 178 L407 226 Q407 239 394 239 L326 239 Q313 239 313 226 Z" fill="#9CCDEB"/></g>' + lab(360, 276, '(나)', 21, mix=True) + '</g>'
    s += '<g class="step" data-g="v3"><g data-arw="436,140,480,140,muted,3"></g>' + vial(490, '#F4F7FA', '#9CCDEB') + \
         f'<g data-anim="fade" data-dur="1" data-delay=".3"><rect x="503" y="120" width="94" height="58" fill="#C0287F"/></g>' + lab(550, 276, '(다)', 21, mix=True) + '</g>'
    return s
F['VIALS'] = vials()


# 용해 모식도: 아래 물 분자(작게, 라벨 없음) + 위 헥세인(회색 타원)
def mix_model():
    s = '<rect x="10" y="10" width="300" height="250" rx="8" fill="#fff" stroke="#7E8B98" stroke-width="2"/>'
    rr = random.Random(4)
    for k in range(9):
        x = 40 + (k % 5) * 58 + (14 if k >= 5 else 0)
        y = 28 + (k // 5) * 38
        a = rr.uniform(-20, 20)
        s += f'<ellipse cx="{x}" cy="{y}" rx="24" ry="11" transform="rotate({f(a)} {x} {y})" fill="#C9D2DB" stroke="#8C99A6" stroke-width="1.5"/>'
    s += '<line x1="12" y1="118" x2="308" y2="118" stroke="#9FC3DD" stroke-width="2"/>'
    s += '<rect x="12" y="119" width="296" height="139" fill="#DDEEF8"/>'
    pts = [(50, 150), (120, 145), (190, 152), (260, 146), (80, 210), (150, 205), (225, 212), (285, 208)]
    for k, (x, y) in enumerate(pts):
        a = rr.uniform(0, 360)
        h = math.radians(52.25)
        ds = []
        for sgn in (1, -1):
            t = math.radians(a) + sgn * h
            ds.append((math.cos(t), math.sin(t), 0))
        for d in ds:
            s += f'<line x1="{x}" y1="{y}" x2="{f(x + d[0] * 17)}" y2="{f(y - d[1] * 17)}" stroke="#9AA5B1" stroke-width="4"/>'
        s += f'<g data-atom="{x},{y},12,O,-"></g>'
        for d in ds:
            s += f'<g data-atom="{f(x + d[0] * 17)},{f(y - d[1] * 17)},8,H,-"></g>'
    s += '<g data-anim="fade" data-dur=".8" data-delay=".6">'
    for (a_, b_) in ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7), (0, 4), (1, 5), (2, 6), (3, 7)):
        (x1, y1), (x2, y2) = pts[a_], pts[b_]
        s += f'<line x1="{f(x1 + (x2 - x1) * .3)}" y1="{f(y1 + (y2 - y1) * .3)}" x2="{f(x1 + (x2 - x1) * .7)}" y2="{f(y1 + (y2 - y1) * .7)}" stroke="#2E9E6A" stroke-width="2" stroke-dasharray="4 3"/>'
    s += '</g>'
    s += lab(160, 104, '헥세인(무극성)', 20, None, mix=True) + lab(160, 250, '물(극성) — 분자 사이 강한 인력', 19, '#1B5E3F', mix=True)
    return s
F['MIX'] = mix_model()


# 디카페인
def decaf():
    s = '<rect x="20" y="40" width="200" height="180" rx="16" fill="#F3E9DF" stroke="#8B5A2B" stroke-width="2.5"/>'
    s += lab(120, 30, '커피 원두', 20, None, mix=True)
    rr = random.Random(9)
    tri = [(60, 90), (150, 80), (100, 150), (180, 170), (60, 190)]
    for (x, y) in tri:
        s += f'<polygon points="{x},{y - 12} {x - 11},{y + 8} {x + 11},{y + 8}" fill="#8B5A2B"/>'
    caf = [(110, 100), (170, 125), (80, 135), (130, 190)]
    for k, (x, y) in enumerate(caf):
        tx, ty = 330 + (k % 2) * 60, 100 + (k // 2) * 60
        s += f'<g data-anim="move" data-from="{x - tx},{y - ty}" data-dur="1.6" data-delay="{.4 + k * .25:.2f}" data-ease="soft"><circle cx="{tx}" cy="{ty}" r="12" fill="#E8A33D" stroke="#9A5B00" stroke-width="2"/></g>'
    s += '<path d="M232 230 C300 250 380 250 460 214" fill="none" stroke="#5B6B7F" stroke-width="3" stroke-dasharray="8 6"/>'
    s += '<rect x="290" y="60" width="160" height="140" rx="16" fill="none" stroke="#5B6B7F" stroke-width="2" stroke-dasharray="7 5"/>'
    s += lab(370, 52, '$\\ce{CO2}$ 용매(무극성)', 20, None, mix=True)
    s += '<g data-arw="226,130,282,130,ink,3"></g>'
    s += '<circle cx="40" cy="270" r="10" fill="#E8A33D" stroke="#9A5B00" stroke-width="2"/>' + lab(58, 277, '카페인(약한 극성)', 19, None, anchor='start', mix=True)
    s += '<polygon points="270,258 259,278 281,278" fill="#8B5A2B"/>' + lab(292, 277, '맛·향 성분(극성)', 19, None, anchor='start', mix=True)
    return s
F['DECAF'] = decaf()


# 외투 + 세탁 표시
def jacket():
    s = '<path d="M100 40 L140 30 Q160 52 180 30 L220 40 L262 120 L236 132 L222 104 L222 250 L98 250 L98 104 L84 132 L58 120 Z" fill="#E86A5C" stroke="#9E3A30" stroke-width="2.5" stroke-linejoin="round"/>'
    for y in (90, 130, 170, 210):
        s += f'<path d="M100 {y} Q160 {y + 10} 220 {y}" fill="none" stroke="#9E3A30" stroke-width="2"/>'
    s += '<line x1="160" y1="46" x2="160" y2="250" stroke="#9E3A30" stroke-width="2"/>'
    # 물세탁 표시
    s += '<path d="M300 70 L312 120 L378 120 L390 70" fill="none" stroke="#16233D" stroke-width="3"/><path d="M296 70 Q311 58 326 70 Q341 82 356 70 Q371 58 386 70" fill="none" stroke="#1F6FD1" stroke-width="3"/>'
    s += '<circle cx="345" cy="100" r="40" fill="none" stroke="#2E9E6A" stroke-width="4" opacity=".0"/>'
    s += lab(345, 152, '물세탁 ○', 21, '#1B5E3F', mix=True)
    s += '<circle cx="345" cy="210" r="30" fill="none" stroke="#16233D" stroke-width="3"/>' + lab(345, 220, '\\mathrm{F}', 26)
    s += '<line x1="315" y1="180" x2="375" y2="240" stroke="#D7263D" stroke-width="4"/><line x1="375" y1="180" x2="315" y2="240" stroke="#D7263D" stroke-width="4"/>'
    s += lab(345, 272, '드라이클리닝 ×', 21, PLUS, mix=True)
    return s
F['JACKET'] = jacket()


# 계산 화학자 화면
def screen():
    s = '<rect x="20" y="20" width="340" height="220" rx="12" fill="#1E2A3A"/><rect x="34" y="34" width="312" height="192" rx="6" fill="#F4F7FA"/>'
    s += '<rect x="160" y="240" width="60" height="26" fill="#8C99A6"/><rect x="120" y="264" width="140" height="10" rx="4" fill="#5B6B7F"/>'
    body, info, _ = mol(190, 92, 'O', ['H', 'H'], dirs=h2o_dirs(), L=78, dip=False)
    s += f'<g data-anim="rot" data-from="-30" data-o="190,110" data-dur="1.6" data-delay=".3" data-ease="soft">{body}</g>'
    s += f'<g data-anim="fade" data-dur=".6" data-delay="1.6">{arw(190, 206, 190, 140, "plus", 5)}</g>'
    return s
F['SCREEN'] = screen()


# ───────── 끼워 넣기 ─────────
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, 'slides.tpl.html'), encoding='utf-8').read()
miss = set(re.findall(r'@@([A-Za-z0-9_]+)@@', tpl)) - set(F)
if miss:
    print('없는 그림', miss)
out = re.sub(r'@@([A-Za-z0-9_]+)@@', lambda m: F.get(m.group(1), ''), tpl)
dst = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/2-2-3_분자_구조에_따른_물질의_성질/slides.html'
open(dst, 'w', encoding='utf-8').write(out)
print('ok', len(out), 'V4', V4, 'V31', V31)
