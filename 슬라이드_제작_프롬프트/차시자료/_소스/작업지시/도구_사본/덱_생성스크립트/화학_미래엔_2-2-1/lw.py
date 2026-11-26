# 2-2-1 루이스 전자점식 그림 도우미 (2-2-2 figs.py의 lewis_sym·dot_pair 좌표 규칙을 그대로 잇는다)
import math

INK = '#16233D'; MUTED = '#5B6B7F'; FIELD = '#2E9E6A'; EQUI = '#E08A2C'; PLUS = '#D7263D'; MINUS = '#1F6FD1'; GRAV = '#8C99A6'
ORDER = ['r', 'l', 'u', 'd', 'u', 'l', 'd', 'r']  # 교과서 그림 Ⅱ-10 순서


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def sx(el):
    """가로 자리 거리(배수) — 한 글자 0.70, 두 글자 0.95"""
    return 0.95 if len(el) > 1 else 0.70


def atom_sides(n, el=''):
    if el == 'He':
        return {'r': 2}
    d = {}
    for s in ORDER[:n]:
        d[s] = d.get(s, 0) + 1
    return d


def sym(x, y, el, S, cls='', fill=None):
    c = f' class="{cls}"' if cls else ''
    fl = f' fill="{fill}"' if fill else ''
    return f'<text{c} class="tex" x="{f(x)}" y="{f(y + 0.36 * S)}" data-tex="\\mathrm{{{el}}}" data-size="{f(S)}" data-anchor="middle"{fl}></text>'.replace('<text class="', '<text class="', 1) if not cls else f'<text class="tex {cls}" x="{f(x)}" y="{f(y + 0.36 * S)}" data-tex="\\mathrm{{{el}}}" data-size="{f(S)}" data-anchor="middle"{fl}></text>'


def side_pos(x, y, side, S, el):
    return {'u': (x, y - 0.75 * S), 'd': (x, y + 0.75 * S), 'l': (x - sx(el) * S, y), 'r': (x + sx(el) * S, y)}[side]


def dots(x, y, orient, n, S, col=INK):
    r = 0.1 * S
    if n == 1:
        return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col}"/>'
    o = 0.18 * S
    if orient == 'h':
        return f'<circle cx="{f(x - o)}" cy="{f(y)}" r="{f(r)}" fill="{col}"/><circle cx="{f(x + o)}" cy="{f(y)}" r="{f(r)}" fill="{col}"/>'
    return f'<circle cx="{f(x)}" cy="{f(y - o)}" r="{f(r)}" fill="{col}"/><circle cx="{f(x)}" cy="{f(y + o)}" r="{f(r)}" fill="{col}"/>'


def side_dots(x, y, el, sides, S):
    return ''.join(dots(*side_pos(x, y, s, S, el), 'h' if s in 'ud' else 'v', n, S) for s, n in sides.items() if n)


def shared_dots(x, y, orient, order, S):
    """공유 전자쌍 점: 단일 = 쌍 하나, 이중 = 2열×2, 삼중 = 2열×3 (교과서 그림 Ⅱ-12)"""
    r = 0.1 * S
    if order == 1:
        return dots(x, y, orient, 2, S)
    c = 0.15 * S
    rows = [-0.18 * S, 0.18 * S] if order == 2 else [-0.3 * S, 0, 0.3 * S]
    out = ''
    for a in (-c, c):
        for b in rows:
            px, py = (x + a, y + b) if orient == 'v' else (x + b, y + a)
            out += f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r)}" fill="{INK}"/>'
    return out


def box(x, y, w, h, kind, g=None, extra=''):
    col = FIELD if kind == 'shared' else EQUI
    cls = f' class="step" data-g="{g}"' if g else ''
    return f'<rect{cls} x="{f(x - w / 2)}" y="{f(y - h / 2)}" width="{f(w)}" height="{f(h)}" rx="{f(min(w, h) * .3)}" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.5"{extra}/>'


class Mol:
    """atoms: {id: (el, x, y)}, bonds: [(a, b, order)], lone: {id: {side: n}}"""

    def __init__(self, atoms, bonds, lone, S):
        self.a, self.b, self.lone, self.S = atoms, bonds, lone, S

    def bpos(self, a, b):
        ea, xa, ya = self.a[a]; eb, xb, yb = self.a[b]; S = self.S
        if abs(ya - yb) < 1e-6:
            if xa > xb: (ea, xa, ya), (eb, xb, yb) = (eb, xb, yb), (ea, xa, ya)
            return ((xa + sx(ea) * S + xb - sx(eb) * S) / 2, ya, 'v')
        if ya > yb: (ea, xa, ya), (eb, xb, yb) = (eb, xb, yb), (ea, xa, ya)
        return (xa, (ya + 0.75 * S + yb - 0.75 * S) / 2, 'h')

    def svg_dots(self, hl=None, lone_hl=None):
        S = self.S; out = ''
        for a, b, o in self.b:
            x, y, ori = self.bpos(a, b)
            out += shared_dots(x, y, ori, o, S)
        for i, (el, x, y) in self.a.items():
            out += sym(x, y, el, S) + side_dots(x, y, el, self.lone.get(i, {}), S)
        if hl:
            out += self.boxes(hl, lone_hl if lone_hl else hl)
        return out

    def boxes(self, g_sh, g_lo, which='both'):
        S = self.S; out = ''
        if which in ('both', 'shared'):
            for a, b, o in self.b:
                x, y, ori = self.bpos(a, b)
                L = 0.85 * S if o == 1 else (0.85 * S if o == 2 else 1.05 * S)
                W = 0.55 * S if o == 1 else 0.78 * S
                out += box(x, y, W, L, 'shared', g_sh) if ori == 'v' else box(x, y, L, W, 'shared', g_sh)
        if which in ('both', 'lone'):
            for i, (el, x, y) in self.a.items():
                for s, n in self.lone.get(i, {}).items():
                    if n == 2:
                        px, py = side_pos(x, y, s, S, el)
                        out += box(px, py, 0.85 * S, 0.55 * S, 'lone', g_lo) if s in 'ud' else box(px, py, 0.55 * S, 0.85 * S, 'lone', g_lo)
        return out

    def svg_lines(self, show_lone=True, cls=''):
        S = self.S; out = ''
        for a, b, o in self.b:
            out += bondline(self.a[a], self.a[b], o, S, cls)
        for i, (el, x, y) in self.a.items():
            out += sym(x, y, el, S) + (side_dots(x, y, el, self.lone.get(i, {}), S) if show_lone else '')
        return out


def hw(el):
    return 0.46 if len(el) == 1 else 0.68


def bondline(A, B, order, S, cls=''):
    ea, xa, ya = A; eb, xb, yb = B
    c = f' class="{cls}"' if cls else ''
    if abs(ya - yb) < 1e-6:
        if xa > xb: (ea, xa, ya), (eb, xb, yb) = (eb, xb, yb), (ea, xa, ya)
        x1, x2 = xa + hw(ea) * S, xb - hw(eb) * S
        offs = {1: [0], 2: [-0.12 * S, 0.12 * S], 3: [-0.18 * S, 0, 0.18 * S]}[order]
        return ''.join(f'<line{c} x1="{f(x1)}" y1="{f(ya + o)}" x2="{f(x2)}" y2="{f(ya + o)}" stroke="{INK}" stroke-width="{f(max(2.5, S * .075))}" stroke-linecap="round"/>' for o in offs)
    if ya > yb: (ea, xa, ya), (eb, xb, yb) = (eb, xb, yb), (ea, xa, ya)
    y1, y2 = ya + 0.52 * S, yb - 0.52 * S
    offs = {1: [0], 2: [-0.12 * S, 0.12 * S], 3: [-0.18 * S, 0, 0.18 * S]}[order]
    return ''.join(f'<line{c} x1="{f(xa + o)}" y1="{f(y1)}" x2="{f(xa + o)}" y2="{f(y2)}" stroke="{INK}" stroke-width="{f(max(2.5, S * .075))}" stroke-linecap="round"/>' for o in offs)


def tex(x, y, s, size=20, anchor='middle', mix=True, extra=''):
    k = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {k}="{s}" data-size="{size}" data-anchor="{anchor}"{extra}></text>'


def arrow_r(x1, x2, y, col='#8C99A6', w=5):
    return f'<g data-arw="{f(x1)},{f(y)},{f(x2)},{f(y)},{col},{w}"></g>'


def bohr(cx, cy, Z, shells, R=(28, 56), lab=None, inner_col=GRAV, outer=None, nuc=15, er=5.5):
    """shells: 껍질별 전자 수. outer: 바깥 껍질 전자 각도 목록(°, 수학 방향) — 없으면 고르게."""
    out = ''
    for k, n in enumerate(shells):
        r = R[k]
        out += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{MUTED}" stroke-width="1.5"/>'
    out += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{nuc}" fill="{PLUS}"/>'
    out += tex(cx, cy + 6, f'{Z}+', 17, extra=' fill="#FFFFFF" data-weight="700"')
    for k, n in enumerate(shells):
        r = R[k]; last = k == len(shells) - 1
        angs = outer if (last and outer is not None) else [90 + 360 * i / n for i in range(n)] if n > 2 else ([0, 180] if n == 2 else [0])
        if not last and n == 2:
            angs = [45, 225]
        col = MINUS if last else inner_col
        for a in angs:
            t = math.radians(a)
            out += f'<circle cx="{f(cx + r * math.cos(t))}" cy="{f(cy - r * math.sin(t))}" r="{er}" fill="{col}"/>'
    return out


def lewis_angles(n, el=''):
    """보어 모형 바깥 껍질 전자 각도를 루이스 점 자리와 맞춘다 (오른쪽 0°, 위 90°)."""
    base = {'r': 0, 'u': 90, 'l': 180, 'd': 270}
    sides = atom_sides(n, el); out = []
    for s, k in sides.items():
        out += [base[s]] if k == 1 else [base[s] - 14, base[s] + 14]
    return out
