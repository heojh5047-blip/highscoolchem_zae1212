# 3-4 탄소 화합물의 유용성 — slides.tpl.html 의 @@이름@@ 자리에 그림 SVG를 넣어 slides.html 을 만든다.
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import f, half_w, INK, MUTED, EQUI, BOND

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학반응의세계_미래엔_3-4/cmp.html'
F = {}
FIELD, BF, PLUS, MINUS, GRAV = '#2E9E6A', '#7B4FC8', '#D7263D', '#1F6FD1', '#8C99A6'
GLASS, WATER, WEDGE = '#7E8B98', '#DDEEF8', '#9FC3DD'
ESTER_L, DYE, DCM = '#FFF1BF', '#9BD39B', '#F1F4F7'


def T(x, y, mix, size=20, anchor='middle', fill=None, weight=None, extra='', halo=False):
    if '<b>' in mix:
        mix = mix.replace('<b>', '').replace('</b>', ''); weight = weight or 700
    fl = f' fill="{fill}"' if fill else ''
    w = f' data-weight="{weight}"' if weight else ''
    h = ' data-halo="1"' if halo else ''
    return f'<text class="tex"{extra} x="{f(x)}" y="{f(y)}" data-mix="{mix}" data-size="{size}" data-anchor="{anchor}"{fl}{w}{h}></text>'


def TX(x, y, tex, size=24, anchor='middle', fill=None, extra=''):
    fl = f' fill="{fill}"' if fill else ''
    return f'<text class="tex"{extra} x="{f(x)}" y="{f(y)}" data-tex="{tex}" data-size="{size}" data-anchor="{anchor}"{fl}></text>'


def arw(x1, y1, x2, y2, col='ink', w=3, extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}"{extra}></g>'


def ln(x1, y1, x2, y2, col=INK, w=3, extra=''):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{extra}/>'


def rbox(x, y, w, h, col, op=.18, dash=False, extra='', rx=10):
    d = ' stroke-dasharray="6 5"' if dash else ''
    return f'<rect{extra} x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-width="2"{d}/>'


def ell(cx, cy, rx, ry, col=MINUS, extra=''):
    return f'<ellipse{extra} cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 5"/>'


def bracket(xl, xr, yt, yb, w=2.5, S=24):
    return (f'<path d="M{f(xl + 10)} {f(yt)} H{f(xl)} V{f(yb)} H{f(xl + 10)}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
            f'<path d="M{f(xr - 10)} {f(yt)} H{f(xr)} V{f(yb)} H{f(xr - 10)}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
            + TX(xr + 12, yb + 4, 'n', S, 'middle'))


def pill(x, y, tex, col=MINUS, size=22, w=None, extra=''):
    w = w or 70
    return (f'<g{extra}><rect x="{f(x - w / 2)}" y="{f(y - 22)}" width="{f(w)}" height="36" rx="18" fill="#fff" stroke="{col}" stroke-width="2"/>'
            + TX(x, y + 6, tex, size, fill=col) + '</g>')


# ───────── 구조식 (빈 기호 '' = 뼈대 꼭짓점: 라벨 없음, 선을 자르지 않음) ─────────
def lab_tex(sym):
    if sym in ('C', 'H', 'O', 'N', 'R'):
        return '\\mathrm{%s}' % sym
    return '\\ce{%s}' % sym


def sf2(atoms, bonds, S=24, col=INK, lw=3, gap=7):
    out = []
    for bd in bonds:
        i, j, o = bd[:3]
        s1, x1, y1 = atoms[i]
        s2, x2, y2 = atoms[j]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L

        def cut(sym):
            if sym == '':
                return 0
            hw, hh = half_w(sym, S) + 0.16 * S, 0.5 * S
            return 1 / math.sqrt((ux / hw) ** 2 + (uy / hh) ** 2)
        a, b = cut(s1), cut(s2)
        px, py = -uy, ux
        if o == 'in':  # 고리 안쪽 이중 결합: 바깥 선 + 안쪽 짧은 선
            cx, cy = bd[3]
            out.append(ln(x1, y1, x2, y2, col, lw))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            sgn = 1 if (px * (cx - mx) + py * (cy - my)) > 0 else -1
            k = 7 * sgn
            out.append(ln(x1 + ux * 9 + px * k, y1 + uy * 9 + py * k, x2 - ux * 9 + px * k, y2 - uy * 9 + py * k, col, lw))
            continue
        offs = {1: [0], 2: [-gap / 2, gap / 2], 3: [-gap, 0, gap]}[o]
        for k in offs:
            out.append(ln(x1 + ux * a + px * k, y1 + uy * a + py * k, x2 - ux * b + px * k, y2 - uy * b + py * k, col, lw))
    for sym, x, y in atoms:
        if sym:
            out.append(f'<text class="tex" x="{f(x)}" y="{f(y + 0.36 * S)}" data-tex="{lab_tex(sym)}" data-size="{S}" data-anchor="middle"></text>')
    return ''.join(out)


class Mol:
    """상대 좌표 분자. svg(cx,cy)는 원자 상자 가운데를 (cx,cy)에"""
    def __init__(self, S=22):
        self.a, self.b, self.dec, self.S = [], [], [], S

    def add(self, sym, x, y):
        self.a.append((sym, x, y)); return len(self.a) - 1

    def bond(self, i, j, o=1, c=None):
        self.b.append((i, j, o, c) if o == 'in' else (i, j, o))

    def ring(self, cx, cy, r):
        """뼈대 고리(꼭짓점 위). 꼭짓점 번호 0 위, 1 오른쪽 위(30°), 2 오른쪽 아래, 3 아래, 4 왼쪽 아래, 5 왼쪽 위"""
        ids = []
        for k, ang in enumerate((90, 30, -30, -90, -150, 150)):
            t = math.radians(ang)
            ids.append(self.add('', cx + r * math.cos(t), cy - r * math.sin(t)))
        for k in range(6):
            if k % 2 == 0:
                self.bond(ids[k], ids[(k + 1) % 6], 'in', (cx, cy))
            else:
                self.bond(ids[k], ids[(k + 1) % 6], 1)
        return ids

    def bbox(self):
        S = self.S
        xs = [x - (half_w(s, S) if s else 0) for s, x, y in self.a] + [x + (half_w(s, S) if s else 0) for s, x, y in self.a]
        ys = [y - (0.5 * S if s else 0) for s, x, y in self.a] + [y + (0.5 * S if s else 0) for s, x, y in self.a]
        return min(xs), min(ys), max(xs), max(ys)

    def svg(self, cx, cy):
        x0, y0, x1, y1 = self.bbox()
        dx, dy = cx - (x0 + x1) / 2, cy - (y0 + y1) / 2
        atoms = [(s, x + dx, y + dy) for s, x, y in self.a]
        s = ''.join(fn(dx, dy) for fn in self.dec if getattr(fn, 'under', True))
        s += sf2(atoms, self.b, self.S)
        s += ''.join(fn(dx, dy) for fn in self.dec if not getattr(fn, 'under', True))
        return s

    def P(self, i, dx=0, dy=0):
        _, x, y = self.a[i]; return x + dx, y + dy


def grp_e(sym, S, d):
    """원자 → 원자단 라벨 중심까지 거리"""
    return d + max(0, half_w(sym, S) - 0.36 * S)


# ───────── 반응 구조식: 실험 1 (아세트산 + 아이소아밀 알코올) ─────────
def ester_rxn():
    S, d = 24, 56
    y0, y1 = 100, 272
    s = ''
    # 아세트산
    A = [('H', 36, y0), ('C', 92, y0), ('H', 92, y0 - d), ('H', 92, y0 + d), ('C', 148, y0), ('O', 148, y0 - d), ('O', 204, y0), ('H', 252, y0)]
    Ab = [(0, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 1), (4, 5, 2), (4, 6, 1), (6, 7, 1)]
    s += ell(228, y0, 46, 26) + sf2(A, Ab, S)
    s += TX(292, y0 + 9, '+', 26)
    B = [('H', 330, y0), ('O', 378, y0), ('C', 434, y0), ('H', 434, y0 - d), ('H', 434, y0 + d), ('C', 490, y0), ('H', 490, y0 - d), ('H', 490, y0 + d),
         ('C', 546, y0), ('H', 546, y0 + d), ('CH3', 546, y0 - d), ('CH3', 616, y0)]
    Bb = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (2, 4, 1), (2, 5, 1), (5, 6, 1), (5, 7, 1), (5, 8, 1), (8, 9, 1), (8, 10, 1), (8, 11, 1)]
    s += ell(330, y0, 22, 25) + sf2(B, Bb, S)
    s += T(148, y0 + d + 40, '아세트산', 19, fill=MUTED) + T(470, y0 + d + 40, '아이소아밀 알코올', 19, fill=MUTED)
    s += arw(36, y1, 188, y1, 'ink', 3) + T(112, y1 - 14, '진한 황산', 19, fill=MUTED)
    s += f'<g data-anim="move" data-from="120,-210" data-dur="1.2" data-delay=".5" data-ease="out">' + pill(112, y1 + 50, '\\ce{H2O}', MINUS, 22) + '</g>'
    P = [('H', 236, y1), ('C', 292, y1), ('H', 292, y1 - d), ('H', 292, y1 + d), ('C', 348, y1), ('O', 348, y1 - d), ('O', 404, y1),
         ('C', 460, y1), ('H', 460, y1 - d), ('H', 460, y1 + d), ('C', 516, y1), ('H', 516, y1 - d), ('H', 516, y1 + d),
         ('C', 572, y1), ('H', 572, y1 + d), ('CH3', 572, y1 - d), ('CH3', 642, y1)]
    Pb = [(0, 1, 1), (1, 2, 1), (1, 3, 1), (1, 4, 1), (4, 5, 2), (4, 6, 1), (6, 7, 1), (7, 8, 1), (7, 9, 1), (7, 10, 1), (10, 11, 1), (10, 12, 1),
          (10, 13, 1), (13, 14, 1), (13, 15, 1), (13, 16, 1)]
    s += '<g data-anim="fade" data-dur=".8" data-delay=".3">' + rbox(328, y1 - 20, 96, 40, FIELD) + sf2(P, Pb, S) + '</g>'
    s += T(376, y1 + 54, '새로 이어진 부분', 19, fill=FIELD, weight=700)
    s += T(740, y1 - 4, '아이소아밀||아세테이트', 19, fill=MUTED)
    return s


F['ESTER_RXN'] = ester_rxn()


# ───────── 실험 2: 살리실산 + 아세트산 무수물 ─────────
def sal(cx, cy, r=40, S=24, d=50, mode='acid'):
    """mode acid: 살리실산(−COOH, −OH) / asp: 아스피린(−COOH, −O−C(=O)−CH3) / est:R' 살리실산 에스터"""
    m = Mol(S)
    v = m.ring(cx, cy, r)
    x1, y1 = m.P(v[1]); x2, y2 = m.P(v[2])
    c = m.add('C', x1 + d * math.cos(math.radians(30)), y1 - d * math.sin(math.radians(30))); m.bond(v[1], c)
    cxp, cyp = m.P(c)
    o1 = m.add('O', cxp, cyp - d); m.bond(c, o1, 2)
    o = m.add('O', x2 + d * math.cos(math.radians(30)), y2 + d * math.sin(math.radians(30))); m.bond(v[2], o)
    ox, oy = m.P(o)
    return m, c, cxp, cyp, o, ox, oy


def aspirin_rxn():
    S, d = 24, 50
    s = ''
    # 살리실산
    m, c, cxp, cyp, o, ox, oy = sal(110, 130)
    oh = m.add('OH', cxp + 54, cyp); m.bond(c, oh)
    h = m.add('H', ox + 44, oy); m.bond(o, h)
    s += ell(ox + 44, oy, 21, 24)
    s += sf2(m.a, m.b, S)
    s += T(110, 228, '살리실산', 19, fill=MUTED)
    s += TX(292, 140, '+', 26)
    y = 130
    A = [('H3C', 338, y), ('C', 398, y), ('O', 398, y - d), ('O', 452, y), ('C', 506, y), ('O', 506, y - d), ('CH3', 566, y)]
    Ab = [(0, 1, 1), (1, 2, 2), (1, 3, 1), (3, 4, 1), (4, 5, 2), (4, 6, 1)]
    s += ell(512, y - 14, 92, 52) + sf2(A, Ab, S)
    s += T(452, 190, '아세트산 무수물', 19, fill=MUTED)
    y2 = 332
    s += arw(26, y2, 134, y2, 'ink', 3) + T(80, y2 - 14, '인산', 19, fill=MUTED)
    m2, c2, cx2, cy2, o2, ox2, oy2 = sal(236, 322)
    oh2 = m2.add('OH', cx2 + 54, cy2); m2.bond(c2, oh2)
    cc = m2.add('C', ox2 + 54, oy2); m2.bond(o2, cc)
    oo = m2.add('O', ox2 + 54, oy2 + d); m2.bond(cc, oo, 2)
    me = m2.add('CH3', ox2 + 54 + 62, oy2); m2.bond(cc, me)
    s += '<g data-anim="fade" data-dur=".8" data-delay=".3">' + rbox(ox2 - 18, oy2 - 20, 90, 40, FIELD) + sf2(m2.a, m2.b, S) + '</g>'
    s += T(190, 424, '아스피린', 19, fill=MUTED)
    s += TX(482, 340, '+', 26)
    y3 = 332
    B = [('H3C', 526, y3), ('C', 586, y3), ('O', 586, y3 - d), ('OH', 640, y3)]
    Bb = [(0, 1, 1), (1, 2, 2), (1, 3, 1)]
    s += ('<g data-anim="move" data-from="-40,-190" data-dur="1.2" data-delay=".5" data-ease="out">' + ell(584, y3 - 14, 88, 52)
          + sf2(B, Bb, S) + T(584, y3 + 62, '아세트산', 19, fill=MUTED) + '</g>')
    return s


F['ASPIRIN_RXN'] = aspirin_rxn()


# ───────── 실험 3: 나일론 ─────────
def nylon_unit(x0, y, S=24, d=None, hl=True):
    """[−N(H)−(CH2)6−N(H)−C(=O)−(CH2)4−C(=O)−]n, x0 = 왼쪽 괄호"""
    e6 = grp_e('(CH2)6', S, 46)
    s = ''
    xN1 = x0 + 40
    xG6 = xN1 + e6 + 14
    xN2 = xG6 + e6 + 14
    xC1 = xN2 + 54
    xG4 = xC1 + e6 + 14
    xC2 = xG4 + e6 + 14
    xr = xC2 + 40
    A = [('N', xN1, y), ('H', xN1, y - 52), ('(CH2)6', xG6, y), ('N', xN2, y), ('H', xN2, y - 52), ('C', xC1, y), ('O', xC1, y - 52),
         ('(CH2)4', xG4, y), ('C', xC2, y), ('O', xC2, y - 52)]
    Ab = [(0, 1, 1), (0, 2, 1), (2, 3, 1), (3, 4, 1), (3, 5, 1), (5, 6, 2), (5, 7, 1), (7, 8, 1), (8, 9, 2)]
    if hl:
        s += rbox(xN2 - 16, y - 20, xC1 - xN2 + 32, 40, FIELD)
    s += sf2(A, Ab, S)
    s += ln(x0 - 12, y, xN1 - 15, y) + ln(xC2 + 15, y, xr + 12, y)
    s += bracket(x0, xr, y - 78, y + 34, S=S)
    return s, xr, (xN2 + xC1) / 2


def nylon_rxn():
    S = 24
    s = ''
    y = 110
    e6 = grp_e('(CH2)6', S, 46)
    s += TX(22, y + 8, 'n', 24)
    xH1 = 50; xN1 = 92; xG = xN1 + e6 + 14; xN2 = xG + e6 + 14; xH2 = xN2 + 44
    A = [('H', xH1, y), ('N', xN1, y), ('H', xN1, y - 52), ('(CH2)6', xG, y), ('N', xN2, y), ('H', xN2, y - 52), ('H', xH2, y)]
    Ab = [(0, 1, 1), (1, 2, 1), (1, 3, 1), (3, 4, 1), (4, 5, 1), (4, 6, 1)]
    s += ell(xH2, y, 20, 24) + sf2(A, Ab, S)
    s += T(xG, y + 62, '헥사메틸렌다이아민', 19, fill=MUTED)
    xp = xH2 + 40
    s += TX(xp, y + 9, '+', 26) + TX(xp + 32, y + 8, 'n', 24)
    xCl1 = xp + 70; xC1 = xCl1 + 52; xG4 = xC1 + e6 + 14; xC2 = xG4 + e6 + 14; xCl2 = xC2 + 52
    B = [('Cl', xCl1, y), ('C', xC1, y), ('O', xC1, y - 52), ('(CH2)4', xG4, y), ('C', xC2, y), ('O', xC2, y - 52), ('Cl', xCl2, y)]
    Bb = [(0, 1, 1), (1, 2, 2), (1, 3, 1), (3, 4, 1), (4, 5, 2), (4, 6, 1)]
    s += ell(xCl1, y, 25, 24) + sf2(B, Bb, S)
    s += T(xG4, y + 62, '염화 아디프산', 19, fill=MUTED)
    y2 = 280
    s += arw(22, y2, 108, y2, 'ink', 3)
    u, xr, xm = nylon_unit(140, y2, S)
    s += '<g data-anim="fade" data-dur=".8" data-delay=".3">' + u + '</g>'
    s += T(xm, y2 + 64, '나일론', 19, fill=MUTED)
    s += ('<g data-anim="move" data-from="-150,-150" data-dur="1.2" data-delay=".5" data-ease="out">' + TX(xr + 74, y2 + 9, '+\\ 2n\\,\\ce{HCl}', 24, fill=MINUS)
          + T(xr + 82, y2 + 44, '염화 수소', 19, fill=MUTED) + '</g>')
    return s, max(xCl2 + 30, xr + 140)


F['NYLON_RXN'], _w = nylon_rxn()
print('nylon width', _w)
_q, _xr, _ = nylon_unit(30, 100, 24, hl=False)
F['Q12'] = _q
print('q12 width', _xr + 40)


# ───────── 표지: 아스피린 공-막대 (평면) ─────────
def cover():
    R = {'C': 24, 'O': 24, 'H': 18}
    bc = 64
    cx, cy = 214, 258
    pos, bonds = [], []

    def at(el, x, y):
        pos.append((el, x, y)); return len(pos) - 1

    def dirp(i, ang, L):
        _, x, y = pos[i]; t = math.radians(ang); return x + L * math.cos(t), y - L * math.sin(t)
    ring = [at('C', cx + bc * math.cos(math.radians(a)), cy - bc * math.sin(math.radians(a))) for a in (90, 30, -30, -90, -150, 150)]
    for k in range(6):
        bonds.append((ring[k], ring[(k + 1) % 6], 2 if k % 2 == 0 else 1))
    for k, a in ((0, 90), (3, -90), (4, -150), (5, 150)):
        h = at('H', *dirp(ring[k], a, 52)); bonds.append((ring[k], h, 1))
    c7 = at('C', *dirp(ring[1], 30, bc)); bonds.append((ring[1], c7, 1))
    o7 = at('O', *dirp(c7, 90, 60)); bonds.append((c7, o7, 2))
    o8 = at('O', *dirp(c7, -30, 60)); bonds.append((c7, o8, 1))
    h8 = at('H', *dirp(o8, 30, 46)); bonds.append((o8, h8, 1))
    acetyl = []
    o9 = at('O', *dirp(ring[2], -30, 60)); bonds.append((ring[2], o9, 1)); acetyl.append(o9)
    c10 = at('C', *dirp(o9, -90, 62)); bonds.append((o9, c10, 1))
    o10 = at('O', *dirp(c10, -150, 60)); bonds.append((c10, o10, 2))
    c11 = at('C', *dirp(c10, -30, 64)); bonds.append((c10, c11, 1))
    acetyl += [c10, o10, c11]
    for a in (30, -40, -110):
        h = at('H', *dirp(c11, a, 50)); bonds.append((c11, h, 1)); acetyl.append(h)
    acetyl_set = set(acetyl) - {o9}
    stat, mov = '', ''
    for i, j, o in bonds:
        _, x1, y1 = pos[i]; _, x2, y2 = pos[j]
        dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy); px, py = -dy / n, dx / n
        offs = [0] if o == 1 else [-4.5, 4.5]
        w = 7 if o == 1 else 5
        sb = ''.join(f'<line x1="{f(x1 + px * q)}" y1="{f(y1 + py * q)}" x2="{f(x2 + px * q)}" y2="{f(y2 + py * q)}" stroke="{BOND}" stroke-width="{w}" stroke-linecap="round"/>' for q in offs)
        if i in acetyl_set or j in acetyl_set or (i == o9 and j == c10):
            mov += sb
        else:
            stat += sb
    for k, (el, x, y) in enumerate(pos):
        sa = f'<g data-atom="{f(x)},{f(y)},{R[el]},{el}"></g>'
        if k in acetyl_set:
            mov += sa
        else:
            stat += sa
    xs = [p[1] for p in pos]; ys = [p[2] for p in pos]
    print('cover bbox', min(xs), max(xs), min(ys), max(ys))
    s = stat + f'<g data-anim="move" data-from="110,60" data-dur="1.3" data-delay=".3" data-ease="out">{mov}</g>'
    _, xo, yo = pos[o9]; _, xc, yc = pos[c11]
    s += rbox(xo - 34, yo - 30, (xc - xo) + 92, (yc - yo) + 92, FIELD, op=.10, dash=True, extra=' data-anim="fade" data-dur=".6" data-delay="1.5"')
    s += T(262, 506, '아스피린 (합성 의약품)', 20, fill=INK)
    return s


# (표지 캡션의 "아세틸기"는 범위 밖 용어 — 아래에서 바꿈)
F['COVER'] = cover()


# ───────── 생각 열기: 생활 속 합성 물질 카드 ─────────
def card_icon(kind, x, y):
    if kind == 'pill':
        return (f'<rect x="{f(x - 34)}" y="{f(y - 14)}" width="68" height="28" rx="14" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
                f'<path d="M{f(x)} {f(y - 14)} H{f(x + 20)} A14 14 0 0 1 {f(x + 20)} {f(y + 14)} H{f(x)} Z" fill="{PLUS}" fill-opacity=".75"/>'
                f'<circle cx="{f(x - 42)}" cy="{f(y + 22)}" r="13" fill="#fff" stroke="{INK}" stroke-width="2.5"/><line x1="{f(x - 50)}" y1="{f(y + 22)}" x2="{f(x - 34)}" y2="{f(y + 22)}" stroke="{INK}" stroke-width="2"/>')
    if kind == 'soap':
        return (f'<rect x="{f(x - 26)}" y="{f(y - 20)}" width="52" height="58" rx="10" fill="#E3EEFB" stroke="{INK}" stroke-width="2.5"/>'
                f'<rect x="{f(x - 10)}" y="{f(y - 34)}" width="20" height="14" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
                + ''.join(f'<circle cx="{f(x + dx)}" cy="{f(y + dy)}" r="{r}" fill="#fff" stroke="{MINUS}" stroke-width="2"/>' for dx, dy, r in ((36, -24, 9), (46, -4, 6), (30, -44, 5))))
    if kind == 'tire':
        return (f'<circle cx="{f(x)}" cy="{f(y + 6)}" r="38" fill="#3A4452"/><circle cx="{f(x)}" cy="{f(y + 6)}" r="18" fill="#C9D1DA" stroke="#fff" stroke-width="2"/>'
                + ''.join(f'<line x1="{f(x + 30 * math.cos(math.radians(a)))}" y1="{f(y + 6 + 30 * math.sin(math.radians(a)))}" x2="{f(x + 37 * math.cos(math.radians(a)))}" y2="{f(y + 6 + 37 * math.sin(math.radians(a)))}" stroke="#8C99A6" stroke-width="3"/>' for a in range(0, 360, 30)))
    if kind == 'paint':
        return (f'<path d="M{f(x - 30)} {f(y - 18)} V{f(y + 32)} Q{f(x)} {f(y + 42)} {f(x + 30)} {f(y + 32)} V{f(y - 18)}" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
                f'<ellipse cx="{f(x)}" cy="{f(y - 18)}" rx="30" ry="9" fill="#F08A5D" stroke="{INK}" stroke-width="2.5"/>'
                f'<path d="M{f(x - 30)} {f(y - 16)} Q{f(x - 36)} {f(y + 8)} {f(x - 26)} {f(y + 12)}" fill="none" stroke="#F08A5D" stroke-width="7" stroke-linecap="round"/>')
    return ''


def think():
    s = ''
    items = [('pill', '의약품'), ('soap', '합성 세제'), ('tire', '타이어'), ('paint', '페인트')]
    for k, (kind, name) in enumerate(items):
        cx = 120 + (k % 2) * 240
        cy = 92 + (k // 2) * 160
        s += (f'<g data-anim="pop" data-o="{f(cx)},{f(cy)}" data-dur=".6" data-delay="{.2 + .25 * k:.2f}" data-ease="back">'
              f'<rect x="{f(cx - 100)}" y="{f(cy - 72)}" width="200" height="146" rx="16" fill="#fff" stroke="#D5DCE3" stroke-width="2"/>'
              + card_icon(kind, cx, cy - 14) + T(cx, cy + 58, f'<b>{name}</b>', 20, fill=INK) + '</g>')
    return s


F['THINK'] = think()


# ───────── 나일론 개발 연표 ─────────
def timeline():
    s = ''
    y = 70
    s += f'<line x1="30" y1="{y}" x2="1050" y2="{y}" stroke="{MUTED}" stroke-width="3" data-anim="draw" data-dur="1.4"/>'
    ev = [(100, '옛날', '면, 모, 비단||(천연 섬유)', '식물·동물을 길러야 해||대량 생산이 어렵다'),
          (310, '산업 혁명 이후', '섬유 수요||급격히 증가', '새로운 섬유를||만들려는 연구'),
          (530, '1935년', '캐러더스||나일론 개발', '축합 중합 반응으로 만든||최초의 합성 섬유'),
          (750, '제2차 세계 대전', '낙하산, 스타킹', '비단을 대신해||널리 쓰임'),
          (960, '오늘날', '폴리에스터, 아크릴', '자동차·항공 우주·||의료 기기 신소재')]
    for k, (x, when, what, why) in enumerate(ev):
        hl = (k == 2)
        col = FIELD if hl else INK
        g = f'<g data-anim="fade" data-dur=".5" data-delay="{.3 + .3 * k:.1f}">'
        g += f'<circle cx="{x}" cy="{y}" r="{12 if hl else 9}" fill="{col if hl else "#fff"}" stroke="{col}" stroke-width="3"/>'
        g += T(x, y - 26, f'<b>{when}</b>', 20, fill=col)
        g += T(x, y + 44, what, 20, fill=INK, weight=700 if hl else None)
        g += T(x, y + 118, why, 19, fill=MUTED)
        s += g + '</g>'
    return s


F['TIMELINE'] = timeline()


# ───────── 나일론이 바꾼 것: 아이콘 ─────────
def ic_parachute(x, y):
    return (f'<path d="M{x - 54} {y - 6} A54 44 0 0 1 {x + 54} {y - 6} Q{x + 27} {y - 16} {x} {y - 6} Q{x - 27} {y - 16} {x - 54} {y - 6} Z" fill="#F2C230" stroke="{INK}" stroke-width="2.5"/>'
            + ''.join(ln(x + dx, y - 8, x, y + 44, INK, 1.8) for dx in (-54, -20, 20, 54))
            + f'<rect x="{x - 9}" y="{y + 40}" width="18" height="22" rx="4" fill="{MINUS}"/>')


def ic_shirt(x, y):
    return f'<path d="M{x - 22} {y - 40} L{x - 56} {y - 22} L{x - 44} {y + 2} L{x - 32} {y - 6} V{y + 50} H{x + 32} V{y - 6} L{x + 44} {y + 2} L{x + 56} {y - 22} L{x + 22} {y - 40} Q{x} {y - 24} {x - 22} {y - 40} Z" fill="#B07CD8" fill-opacity=".8" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'


def ic_brush(x, y):
    s = f'<rect x="{x - 66}" y="{y + 6}" width="104" height="16" rx="8" fill="#5AA9E6" stroke="{INK}" stroke-width="2.5"/>'
    s += f'<rect x="{x + 30}" y="{y + 4}" width="40" height="20" rx="5" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
    s += ''.join(ln(x + 34 + 6 * k, y + 2, x + 34 + 6 * k, y - 26, '#7E8B98', 3) for k in range(7))
    return s


def ic_gear(x, y):
    s = ''.join(f'<rect x="{x - 8}" y="{y - 46}" width="16" height="16" rx="3" fill="#8C99A6" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 45))
    s += f'<circle cx="{x}" cy="{y}" r="34" fill="#8C99A6" stroke="{INK}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="13" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    return s


F['IC_PARA'] = ic_parachute(80, 70)
F['IC_SHIRT'] = ic_shirt(80, 64)
F['IC_BRUSH'] = ic_brush(80, 70)
F['IC_GEAR'] = ic_gear(80, 66)


# ───────── 네 칸 만화 ─────────
def comic(panels, w=250, h=150, gap=16):
    s = ''
    for k, (head, body, icon) in enumerate(panels):
        x = (k % 2) * (w + gap) + 4
        y = (k // 2) * (h + gap) + 4
        s += f'<g data-anim="fade" data-dur=".5" data-delay="{.2 + .35 * k:.2f}">'
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        s += f'<circle cx="{x + 22}" cy="{y + 22}" r="14" fill="{INK}"/>' + T(x + 22, y + 29, f'<b>{k + 1}</b>', 18, fill='#fff')
        s += T(x + w / 2 + 14, y + 30, f'<b>{head}</b>', 19, fill=INK)
        s += T(x + w / 2, y + 66, body, 18, fill=INK)
        s += icon(x, y, w, h) if icon else ''
        s += '</g>'
    return s


def i_head(x, y, w, h, col='#F6B26B'):
    cx, cy = x + 40, y + h - 30
    return (f'<circle cx="{cx}" cy="{cy - 6}" r="13" fill="{col}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{cx - 18} {cy + 22} Q{cx} {cy + 4} {cx + 18} {cy + 22}" fill="{col}" stroke="{INK}" stroke-width="2"/>')


F['COMIC_ASP'] = comic([
    ('머리가 아파서…', '살리실산을 먹었는데||이번엔 속이 아파.', i_head),
    ('호프만 (1899년)', '살리실산의 부작용을||줄인 아스피린을 합성', lambda x, y, w, h: i_head(x, y, w, h, '#76B7E5')),
    ('합성 의약품의 시작', '최초의 합성 의약품 이후||다양한 의약품이 생산되어||사람들의 건강을 지킴', None),
    ('오늘날', '신약 개발은 화학 연구의||중요한 축 — 화학 산업이||인류 복지에 이바지', None)])
F['COMIC_PET'] = comic([
    ('무겁고 깨지는 병', '유리병은 무거워 옮기기||어렵고 깨지면 위험해.', i_head),
    ('PET 병의 등장', '테레프탈산과 에틸렌||글리콜의 축합 중합으로||가볍고 질긴 PET 병', None),
    ('생활의 변화', '음료를 싸고 안전하게||멀리까지 나를 수||있게 되었다', None),
    ('새로운 숙제', '버려진 병이 쌓인다 →||분리배출·재활용, 분해||되는 플라스틱 연구', lambda x, y, w, h: i_head(x, y, w, h, '#9BD39B'))])


# ───────── 실험 기구 ─────────
def beaker(x, y, w, h, liq=None, lvl=.5, extra='', layers=None):
    """x,y 왼쪽 위. layers: [(색, 비율 아래부터)]"""
    s = ''
    if layers:
        yb = y + h - 3
        for col, fr in layers:
            hh = (h - 6) * fr
            s += f'<rect x="{f(x + 3)}" y="{f(yb - hh)}" width="{f(w - 6)}" height="{f(hh)}" fill="{col}"/>'
            yb -= hh
    elif liq:
        hh = (h - 6) * lvl
        s += f'<rect x="{f(x + 3)}" y="{f(y + h - 3 - hh)}" width="{f(w - 6)}" height="{f(hh)}" fill="{liq}"/>'
    s += f'<path d="M{f(x - 6)} {f(y)} H{f(x)} V{f(y + h - 6)} Q{f(x)} {f(y + h)} {f(x + 6)} {f(y + h)} H{f(x + w - 6)} Q{f(x + w)} {f(y + h)} {f(x + w)} {f(y + h - 6)} V{f(y)} H{f(x + w + 6)}" fill="none" stroke="{GLASS}" stroke-width="3"{extra}/>'
    return s


def rbf(cx, cy, r, liq=None, lvl=.45, neck=48, foil=False):
    s = ''
    if liq:
        yl = cy + r - 2 * r * lvl
        dy = yl - cy
        dx = math.sqrt(max(0, (r - 2) ** 2 - dy ** 2))
        large = 1 if yl < cy else 0
        s += f'<path d="M{f(cx - dx)} {f(yl)} A{f(r - 2)} {f(r - 2)} 0 {large} 0 {f(cx + dx)} {f(yl)} Z" fill="{liq}"/>'
    nw = r * .32
    a = math.asin(nw / r)
    yt = cy - r * math.cos(a)
    s += (f'<path d="M{f(cx - nw)} {f(yt - neck)} V{f(yt)} A{f(r)} {f(r)} 0 1 0 {f(cx + nw)} {f(yt)} V{f(yt - neck)}" fill="none" stroke="{GLASS}" stroke-width="3"/>')
    if foil:
        s += f'<path d="M{f(cx - nw - 5)} {f(yt - neck + 10)} V{f(yt - neck - 6)} Q{f(cx)} {f(yt - neck - 16)} {f(cx + nw + 5)} {f(yt - neck - 6)} V{f(yt - neck + 10)} Z" fill="#C9D1DA" stroke="#7E8B98" stroke-width="2"/>'
    return s


def hotplate(x, y, w):
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="22" rx="5" fill="#5B6B7F"/>'
            f'<rect x="{f(x + 10)}" y="{f(y - 6)}" width="{f(w - 20)}" height="7" rx="3" fill="#D7263D" fill-opacity=".75"/>'
            f'<circle cx="{f(x + w - 18)}" cy="{f(y + 11)}" r="5" fill="#fff"/>')


def thermo(x, y1, y2):
    return (f'<line x1="{f(x)}" y1="{f(y1)}" x2="{f(x)}" y2="{f(y2)}" stroke="{GLASS}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{f(x)}" y1="{f(y1 + (y2 - y1) * .45)}" x2="{f(x)}" y2="{f(y2)}" stroke="{PLUS}" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{f(x)}" cy="{f(y2)}" r="6" fill="{PLUS}"/>')


def bubbles(pts, col=MINUS, extra=''):
    return f'<g{extra}>' + ''.join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="#fff" stroke="{col}" stroke-width="1.8"/>' for x, y, r in pts) + '</g>'


def sepfun(cx, y0, wtop=70, H=150, layers=None, open_=False):
    """원뿔꼴 분별 깔때기. layers: [(색, 높이 비율 아래부터)]"""
    s = ''
    tip = y0 + H

    def half(yy):
        return wtop * (tip - yy) / H
    if layers:
        yb = tip - 6
        for col, fr in layers:
            yt = yb - (H - 12) * fr
            s += f'<path d="M{f(cx - half(yt) + 3)} {f(yt)} L{f(cx + half(yt) - 3)} {f(yt)} L{f(cx + half(yb) - 3)} {f(yb)} L{f(cx - half(yb) + 3)} {f(yb)} Z" fill="{col}"/>'
            yb = yt
    s += f'<path d="M{f(cx - 10)} {f(y0 - 20)} V{f(y0)} H{f(cx - wtop)} L{f(cx - 6)} {f(tip)} V{f(tip + 40)} M{f(cx + 6)} {f(tip + 40)} V{f(tip)} L{f(cx + wtop)} {f(y0)} H{f(cx + 10)} V{f(y0 - 20)}" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<rect x="{f(cx - 13)}" y="{f(y0 - 32)}" width="26" height="14" rx="4" fill="#C9D1DA" stroke="{GLASS}" stroke-width="2"/>'
    rot = 0 if open_ else 90
    s += f'<g transform="rotate({rot} {f(cx)} {f(tip + 20)})"><rect x="{f(cx - 20)}" y="{f(tip + 16)}" width="40" height="8" rx="3" fill="#5B6B7F"/></g>'
    return s, tip


def ffunnel(cx, y0, w=70, h=60):
    return (f'<path d="M{f(cx - w)} {f(y0)} L{f(cx - 6)} {f(y0 + h)} V{f(y0 + h + 40)} M{f(cx + 6)} {f(y0 + h + 40)} V{f(y0 + h)} L{f(cx + w)} {f(y0)}" fill="none" stroke="{GLASS}" stroke-width="3"/>'
            f'<path d="M{f(cx - w + 8)} {f(y0 + 3)} L{f(cx)} {f(y0 + h - 4)} L{f(cx + w - 8)} {f(y0 + 3)}" fill="#fff" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 4"/>')


def crystals(cx, cy, n=7, spread=40):
    s = ''
    for k in range(n):
        x = cx + (k - n / 2) * spread / n * 2 + (k % 2) * 4
        y = cy + (k % 3) * 5
        s += f'<path d="M{f(x)} {f(y - 7)} L{f(x + 6)} {f(y)} L{f(x)} {f(y + 7)} L{f(x - 6)} {f(y)} Z" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
    return s


# 실험 1 과정 ①–③
def e1_1():
    s = rbf(130, 140, 58, ESTER_L, .38, foil=False)
    for k, (x, col) in enumerate(((60, '#fff'), (130, '#fff'), (200, '#fff'))):
        s += f'<g data-anim="move" data-from="0,-26" data-dur=".7" data-delay="{.2 + .3 * k:.1f}" data-ease="out"><path d="M{x} 6 V40 L{x + 3} 52 L{x + 6} 40 V6 Z" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/><circle cx="{x + 3}" cy="60" r="4" fill="{MINUS}" fill-opacity=".6"/></g>'
    return s


def e1_2(temp='40–50 °C', liq=ESTER_L):
    s = beaker(40, 92, 180, 118, WATER, .62)
    s += rbf(130, 160, 40, liq, .42, neck=40, foil=True)
    s += hotplate(24, 214, 212)
    s += thermo(204, 46, 176)
    s += f'<line x1="250" y1="20" x2="250" y2="214" stroke="#5B6B7F" stroke-width="5"/><line x1="250" y1="66" x2="150" y2="66" stroke="#5B6B7F" stroke-width="4"/>'
    s += T(196, 30, temp, 21, fill=PLUS, weight=700)
    return s


def e1_3():
    s = rbf(130, 140, 58, '#F2D9A6', .38)
    s += thermo(186, 30, 150)
    s += T(186, 22, '실온', 19, fill=MINUS, weight=700)
    s += arw(60, 40, 60, 110, 'minus', 3) + T(60, 30, '식힘', 19, fill=MINUS)
    return s


F['E1_1'], F['E1_2'], F['E1_3'] = e1_1(), e1_2(), e1_3()


# 실험 1 과정 ④–⑥
def e1_4():
    s = rbf(110, 150, 58, '#F2D9A6', .38)
    s += bubbles([(96, 160, 5), (118, 170, 4), (132, 152, 6), (104, 176, 3)], extra=' data-anim="move" data-from="0,14" data-dur="1.4" data-rep="loop"')
    s += f'<rect x="184" y="40" width="22" height="70" rx="3" fill="#F08A5D"/>'
    s += f'<rect x="184" y="140" width="22" height="70" rx="3" fill="#9BD39B" data-anim="fade" data-dur=".8" data-delay=".6"/>'
    s += arw(195, 114, 195, 136, 'ink', 2.5)
    s += T(212, 82, '산성', 20, fill=PLUS, anchor='start') + T(212, 182, '중성', 20, fill=FIELD, anchor='start')
    return s


def e1_5():
    s, tip = sepfun(120, 50, 72, 150, layers=[(WATER, .45), (ESTER_L, .32)])
    s += f'<g data-anim="move" data-from="0,30" data-dur="1.2" data-delay=".3" data-ease="soft">{T(200, 104, "위층", 19, fill=INK, anchor="start")}</g>'
    s += T(176, 158, '아래층', 19, fill=MINUS, anchor='start')
    s += ln(150, 98, 194, 98, MUTED, 1.5) + ln(120, 152, 170, 152, MUTED, 1.5)
    return s


def e1_6():
    s, tip = sepfun(90, 36, 60, 120, layers=[(ESTER_L, .36)], open_=True)
    s += beaker(56, 210 - 52, 68, 50, WATER, .4)
    s += f'<circle cx="90" cy="{tip + 46}" r="3.5" fill="{MINUS}" data-anim="move" data-from="0,-8" data-dur=".8" data-rep="loop"/>'
    s += f'<rect x="176" y="120" width="56" height="88" rx="10" fill="{ESTER_L}" stroke="{GLASS}" stroke-width="3"/><rect x="186" y="104" width="36" height="18" rx="4" fill="#5B6B7F"/>'
    s += arw(130, 80, 176, 130, 'muted', 2.5)
    return s


F['E1_4'], F['E1_5'], F['E1_6'] = e1_4(), e1_5(), e1_6()


# 실험 2 과정 ①–④
def e2_2():
    s = rbf(130, 140, 58, '#F2F2F2', .38)
    for k in range(3):
        x = 104 + 26 * k
        s += f'<path d="M{x} 50 q8 -12 0 -24 q-8 -12 0 -24" fill="none" stroke="{MUTED}" stroke-width="2.5" data-anim="move" data-from="0,16" data-dur="1.4" data-delay="{.2 * k:.1f}" data-rep="loop"/>'
    s += T(214, 40, '기체', 21, fill=MUTED, weight=700)
    return s


def e2_3():
    s = beaker(36, 84, 190, 126, '#E3EEFB', .6)
    for k, (x, y) in enumerate(((60, 150), (196, 156), (70, 186), (186, 190))):
        s += f'<rect x="{x - 12}" y="{y - 12}" width="24" height="24" rx="4" fill="#fff" stroke="{WEDGE}" stroke-width="2" transform="rotate({15 * k} {x} {y})"/>'
    s += rbf(130, 150, 44, '#F2F2F2', .40, neck=40)
    s += crystals(130, 176, 6, 26)
    s += T(130, 240, '얼음물', 21, fill=MINUS)
    return s


def e2_4():
    s = ffunnel(130, 40, 70, 58)
    s += crystals(130, 62, 6, 30)
    s += beaker(82, 150, 96, 64, WATER, .3)
    s += f'<circle cx="130" cy="142" r="3.5" fill="{MINUS}" data-anim="move" data-from="0,-8" data-dur=".8" data-rep="loop"/>'
    s += T(222, 116, '결정', 21, fill=INK, anchor='middle') + ln(206, 104, 150, 66, MUTED, 1.5)
    s += T(222, 26, '거름종이', 21, fill=MUTED) + ln(206, 32, 186, 44, MUTED, 1.5)
    return s


F['E2_1'] = e1_2('70–80 °C', '#F2F2F2')
F['E2_2'], F['E2_3'], F['E2_4'] = e2_2(), e2_3(), e2_4()


# 실험 3 과정 ①–④
def e3_beaker(kind):
    if kind == 1:
        s = beaker(60, 70, 140, 140, DYE, .55)
        s += T(130, 50, '증류수 50 mL', 21, fill=MUTED)
    elif kind == 2:
        s = beaker(60, 70, 140, 140, DCM, .55)
        s += T(130, 50, '다이클로로메테인', 21, fill=MUTED)
    elif kind == 3:
        s = beaker(60, 70, 140, 140, layers=[(DCM, .45), (DYE, .32)])
        s += ln(150, 10, 112, 196, GLASS, 5)
        s += f'<g data-anim="move" data-from="-6,-50" data-dur="1.2" data-rep="loop"><path d="M136 30 q-6 10 -3 22" fill="none" stroke="{DYE}" stroke-width="6" stroke-linecap="round"/></g>'
        s += T(206, 126, '수용액', 21, fill=FIELD, anchor='start') + T(206, 178, '유기||용액', 21, fill=MUTED, anchor='start')
    else:
        s = beaker(60, 110, 140, 104, layers=[(DCM, .45), (DYE, .32)])
        y_if = 110 + 104 - 3 - (104 - 6) * .45
        s += ln(40, 30, 220, 30, GLASS, 6)
        s += f'<path d="M130 {f(y_if)} C126 {f(y_if - 40)}, 136 70, 130 34" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
        s += f'<path d="M130 {f(y_if)} C126 {f(y_if - 40)}, 136 70, 130 34" fill="none" stroke="#5B8F5B" stroke-width="3" stroke-linecap="round" data-anim="draw" data-dur="1.6" data-delay=".3"/>'
        s += f'<line x1="100" y1="{f(y_if)}" x2="160" y2="{f(y_if)}" stroke="#5B8F5B" stroke-width="3"/>'
        s += T(204, y_if + 6, '경계면', 21, fill=INK, anchor='start') + T(40, 20, '유리 막대', 21, fill=MUTED, anchor='start')
    return s


F['E3_1'], F['E3_2'], F['E3_3'], F['E3_4'] = (e3_beaker(k) for k in (1, 2, 3, 4))


# ───────── 실험실: 반응물·생성물 구조 (S=22) ─────────
LS, LD = 22, 44


def m_acid(R):
    m = Mol(LS)
    c = m.add('C', 0, 0); o1 = m.add('O', 0, -LD); m.bond(c, o1, 2)
    r = m.add(R, -grp_e(R, LS, LD), 0); m.bond(r, c)
    o = m.add('O', LD, 0); m.bond(c, o)
    h = m.add('H', LD + 40, 0); m.bond(o, h)
    m.dec.append(hl_fn('e', LD + 20, 0, 36, 22))
    return m


def m_alc(R):
    m = Mol(LS)
    h = m.add('H', 0, 0); o = m.add('O', 40, 0); m.bond(h, o)
    r = m.add(R, 40 + grp_e(R, LS, LD), 0); m.bond(o, r)
    m.dec.append(hl_fn('e', 0, 0, 19, 22))
    return m


def m_sal(mode='acid', R=None):
    m = Mol(LS)
    v = m.ring(0, 0, 34)
    x1, y1 = m.P(v[1]); x2, y2 = m.P(v[2])
    c = m.add('C', x1 + 40 * math.cos(math.radians(30)), y1 - 40 * math.sin(math.radians(30))); m.bond(v[1], c)
    cx, cy = m.P(c)
    o1 = m.add('O', cx, cy - LD); m.bond(c, o1, 2)
    o = m.add('O', x2 + 40 * math.cos(math.radians(30)), y2 + 40 * math.sin(math.radians(30))); m.bond(v[2], o)
    ox, oy = m.P(o)
    if mode == 'acid':
        oc = m.add('O', cx + LD, cy); m.bond(c, oc); hc = m.add('H', cx + LD + 40, cy); m.bond(oc, hc)
        h = m.add('H', ox + 40, oy); m.bond(o, h)
        m.dec.append(hl_fn('e', cx + LD + 20, cy, 36, 22))
        m.dec.append(hl_fn('a', ox + 40, oy, 19, 22))
    elif mode == 'est':
        oc = m.add('O', cx + LD, cy); m.bond(c, oc)
        r = m.add(R, cx + LD + grp_e(R, LS, LD), cy); m.bond(oc, r)
        h = m.add('H', ox + 40, oy); m.bond(o, h)
        m.dec.append(new_fn(cx - 14, cy - 18, LD + 28, 36))
    else:  # 아스피린
        oc = m.add('OH', cx + grp_e('OH', LS, LD), cy); m.bond(c, oc)
        cc = m.add('C', ox + LD, oy); m.bond(o, cc)
        oo = m.add('O', ox + LD, oy + LD); m.bond(cc, oo, 2)
        me = m.add('CH3', ox + LD + grp_e('CH3', LS, LD), oy); m.bond(cc, me)
        m.dec.append(new_fn(ox - 14, oy - 18, LD + 28, 36))
    return m


def m_anh():
    m = Mol(LS)
    o = m.add('O', 0, 0)
    c1 = m.add('C', -LD, 0); c2 = m.add('C', LD, 0); m.bond(c1, o); m.bond(o, c2)
    m.bond(c1, m.add('O', -LD, -LD), 2); m.bond(c2, m.add('O', LD, -LD), 2)
    m.bond(m.add('H3C', -LD - grp_e('H3C', LS, LD), 0), c1); m.bond(c2, m.add('CH3', LD + grp_e('CH3', LS, LD), 0))
    m.dec.append(hl_fn('a', LD + 10, -14, 74, 44))
    return m


def m_diam():
    m = Mol(LS)
    e = grp_e('(CH2)6', LS, LD)
    g = m.add('(CH2)6', 0, 0)
    for sx in (-1, 1):
        n = m.add('N', sx * e, 0); m.bond(g, n) if sx > 0 else m.bond(n, g)
        m.bond(n, m.add('H', sx * e, -LD))
        h = m.add('H', sx * (e + 40), 0); m.bond(n, h)
    m.dec.append(hl_fn('n', e + 40, 0, 19, 22))
    return m


def m_adip():
    m = Mol(LS)
    e = grp_e('(CH2)4', LS, LD)
    g = m.add('(CH2)4', 0, 0)
    for sx in (-1, 1):
        c = m.add('C', sx * e, 0); m.bond(g, c) if sx > 0 else m.bond(c, g)
        m.bond(c, m.add('O', sx * e, -LD), 2)
        cl = m.add('Cl', sx * (e + LD + 4), 0); m.bond(c, cl)
    m.dec.append(hl_fn('n', -(e + LD + 4), 0, 23, 22))
    return m


def m_ester(R, R2):
    m = Mol(LS)
    c = m.add('C', 0, 0); m.bond(c, m.add('O', 0, -LD), 2)
    m.bond(m.add(R, -grp_e(R, LS, LD), 0), c)
    o = m.add('O', LD, 0); m.bond(c, o)
    m.bond(o, m.add(R2, LD + grp_e(R2, LS, LD), 0))
    m.dec.append(new_fn(-14, -18, LD + 28, 36))
    return m


def hl_fn(role, x, y, rx, ry):
    def fn(dx, dy):
        return f'<g data-hl="{role}">{ell(x + dx, y + dy, rx, ry)}</g>'
    fn.under = True
    return fn


def new_fn(x, y, w, h):
    def fn(dx, dy):
        return rbox(x + dx, y + dy, w, h, FIELD)
    fn.under = True
    return fn


ACID_R = {'aa': 'CH3', 'ba': 'CH3CH2CH2'}
ALC_R = {'me': 'CH3', 'et': 'CH2CH3', 'ia': 'CH2CH2CH(CH3)2'}
SLOT_A, SLOT_B, SLOT_P = (165, 100), (490, 100), (325, 300)


def lab_fig():
    s = ''
    s += '<rect x="8" y="8" width="634" height="176" rx="14" fill="#F7F9FB" stroke="#D5DCE3" stroke-width="2"/>'
    s += '<rect x="8" y="232" width="634" height="138" rx="14" fill="#F4FAF6" stroke="#BFE0CD" stroke-width="2"/>'
    s += T(20, 32, '반응물 ①', 18, anchor='start', fill=MUTED) + T(345, 32, '반응물 ②', 18, anchor='start', fill=MUTED)
    s += T(20, 256, '생성물', 18, anchor='start', fill=FIELD)
    s += TX(327, 110, '+', 26)
    s += '<g data-k="arrow">' + arw(325, 188, 325, 228, 'ink', 3) + '</g>'
    reac = {}
    for k, R in ACID_R.items():
        reac[('A', k)] = m_acid(R)
    reac[('A', 'sa')] = m_sal('acid')
    reac[('A', 'ac')] = m_adip()
    for k, R in ALC_R.items():
        reac[('B', k)] = m_alc(R)
    reac[('B', 'an')] = m_anh()
    reac[('B', 'hd')] = m_diam()
    for (side, k), m in reac.items():
        cx, cy = SLOT_A if side == 'A' else SLOT_B
        x0, y0, x1, y1 = m.bbox()
        print('reac', side, k, round(x1 - x0), round(y1 - y0))
        s += f'<g data-r="{side}{k}" style="display:none">{m.svg(cx, cy)}</g>'
    prods = {}
    for a, R in ACID_R.items():
        for b, R2 in ALC_R.items():
            prods[f'{a}_{b}'] = m_ester(R, R2)
    for b, R2 in ALC_R.items():
        prods[f'sa_{b}'] = m_sal('est', R2)
    prods['sa_an'] = m_sal('asp')
    for k, m in prods.items():
        x0, y0, x1, y1 = m.bbox()
        print('prod', k, round(x1 - x0), round(y1 - y0))
        s += f'<g data-p="{k}" style="display:none"><g>{m.svg(*SLOT_P)}</g></g>'
    u, xr, _ = nylon_unit(0, 0, LS)
    # 나일론: 괄호 포함 너비 계산 후 가운데
    s += f'<g data-p="ac_hd" style="display:none"><g transform="translate({f(SLOT_P[0] - (xr + 28) / 2)},{f(SLOT_P[1] + 22)})">{u}</g></g>'
    print('nylon lab width', xr + 28)
    s += f'<g data-b="w" style="display:none">{pill(560, 214, chr(92) + "ce{H2O}", MINUS, 22, 76)}</g>'
    s += f'<g data-b="ac" style="display:none">{pill(556, 214, chr(92) + "ce{CH3COOH}", MINUS, 22, 132)}</g>'
    s += f'<g data-b="hcl" style="display:none">{pill(560, 214, "2n" + chr(92) + "," + chr(92) + "ce{HCl}", MINUS, 22, 104)}</g>'
    return s


F['LAB'] = lab_fig()


def cmp18():
    LSs = 24
    m1 = m_sal('acid'); m1.S = LSs; m1.dec = [hl_fn('a', 0, 0, 0, 0)][:0]
    m2 = m_sal('asp'); m2.S = LSs
    s = m1.svg(160, 100) + m2.svg(160, 352)
    s += arw(160, 206, 160, 244, 'ink', 3)
    s += T(160, 196, '살리실산', 20, fill=MUTED) + T(160, 470, '아스피린', 20, fill=MUTED)
    return s


F['CMP18'] = cmp18()

tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
miss = set(re.findall(r'@@(\w+)@@', tpl)) - set(F)
assert not miss, miss
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', len(out))
