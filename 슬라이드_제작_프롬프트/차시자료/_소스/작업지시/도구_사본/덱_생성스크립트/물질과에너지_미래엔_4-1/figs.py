# 4-1 화학 반응 속도 — 그림 SVG 조각 생성 (tpl.html 의 @@이름@@ 자리에 들어감)
import math

INK = '#16233D'; PLUS = '#D7263D'; MINUS = '#1F6FD1'; FIELD = '#2E9E6A'; EQUI = '#E08A2C'
MUTED = '#5B6B7F'; GLASS = '#7E8B98'; WATER = '#DDEEF8'; WATER_E = '#9FC3DD'

def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s

def tex(x, y, s, size=20, anchor='start', fill=None, halo=False, mix=True, extra=''):
    a = f' data-anchor="{anchor}"' if anchor != 'start' else ''
    fl = f' fill="{fill}"' if fill else ''
    h = ' data-halo="1"' if halo else ''
    key = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {key}="{s}" data-size="{size}"{a}{fl}{h}{extra}></text>'

class Axes:
    """x0,y0 = 원점(화면 좌표), w,h = 축 길이, 값 범위"""
    def __init__(s, x0, y0, w, h, xr, yr):
        s.x0, s.y0, s.w, s.h = x0, y0, w, h
        s.xr, s.yr = xr, yr
    def X(s, v): return s.x0 + (v - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w
    def Y(s, v): return s.y0 - (v - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h
    def frame(s, xt=(), yt=(), xl='', yl='', xfmt=None, yfmt=None, grid=True, ts=18, ls=20, xl_dx=0, yl_pos='top'):
        o = ''
        if grid:
            for v in xt[1:]:
                o += f'<line x1="{f(s.X(v))}" y1="{f(s.y0)}" x2="{f(s.X(v))}" y2="{f(s.y0 - s.h)}" stroke="#E6EBF0" stroke-width="1"/>'
            for v in yt[1:]:
                o += f'<line x1="{f(s.x0)}" y1="{f(s.Y(v))}" x2="{f(s.x0 + s.w)}" y2="{f(s.Y(v))}" stroke="#E6EBF0" stroke-width="1"/>'
        o += f'<line x1="{f(s.x0)}" y1="{f(s.y0)}" x2="{f(s.x0 + s.w + 12)}" y2="{f(s.y0)}" stroke="{MUTED}" stroke-width="2"/>'
        o += f'<line x1="{f(s.x0)}" y1="{f(s.y0)}" x2="{f(s.x0)}" y2="{f(s.y0 - s.h - 12)}" stroke="{MUTED}" stroke-width="2"/>'
        o += f'<polygon points="{f(s.x0 + s.w + 20)},{f(s.y0)} {f(s.x0 + s.w + 10)},{f(s.y0 - 5)} {f(s.x0 + s.w + 10)},{f(s.y0 + 5)}" fill="{MUTED}"/>'
        o += f'<polygon points="{f(s.x0)},{f(s.y0 - s.h - 20)} {f(s.x0 - 5)},{f(s.y0 - s.h - 10)} {f(s.x0 + 5)},{f(s.y0 - s.h - 10)}" fill="{MUTED}"/>'
        for v in xt:
            lab = xfmt(v) if xfmt else f(v)
            o += f'<line x1="{f(s.X(v))}" y1="{f(s.y0)}" x2="{f(s.X(v))}" y2="{f(s.y0 + 6)}" stroke="{MUTED}" stroke-width="2"/>'
            o += tex(s.X(v), s.y0 + 24, lab, ts, 'middle', MUTED, mix=False)
        for v in yt:
            lab = yfmt(v) if yfmt else f(v)
            o += f'<line x1="{f(s.x0 - 6)}" y1="{f(s.Y(v))}" x2="{f(s.x0)}" y2="{f(s.Y(v))}" stroke="{MUTED}" stroke-width="2"/>'
            o += tex(s.x0 - 10, s.Y(v) + 6, lab, ts, 'end', MUTED, mix=False)
        if xl:
            o += tex(s.x0 + s.w + 22 + xl_dx, s.y0 - 10, xl, ls, 'end', INK)
        if yl:
            o += tex(s.x0 + 10, s.y0 - s.h - 14, yl, ls, 'start', INK)
        return o
    def path(s, fn, a, b, n=80):
        pts = [(s.X(a + (b - a) * i / n), s.Y(fn(a + (b - a) * i / n))) for i in range(n + 1)]
        return 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    def line(s, x1, y1, x2, y2, col, w=2.5, dash=None, extra=''):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return f'<line x1="{f(s.X(x1))}" y1="{f(s.Y(y1))}" x2="{f(s.X(x2))}" y2="{f(s.Y(y2))}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{d}{extra}/>'
    def dot(s, x, y, col=INK, r=5, fill=None):
        return f'<circle cx="{f(s.X(x))}" cy="{f(s.Y(y))}" r="{r}" fill="{fill or col}" stroke="{col}" stroke-width="2"/>'

def atom(x, y, r, el, lab='-'):
    return f'<g data-atom="{f(x)},{f(y)},{r},{el},{lab}"></g>'

# 작은 분자 (입자 상자, 배율 1/2: O 12, H 9)
RO, RH = 12, 9
def h2o2(x, y, rot=0):
    t = math.radians(rot)
    def p(dx, dy):
        return x + dx * math.cos(t) - dy * math.sin(t), y + dx * math.sin(t) + dy * math.cos(t)
    o1, o2 = p(-11, 0), p(11, 0)
    h1, h2 = p(-20, -13), p(20, 13)
    return atom(*h1, RH, 'H') + atom(*h2, RH, 'H') + atom(*o1, RO, 'O') + atom(*o2, RO, 'O')
def h2o(x, y, rot=0):
    t = math.radians(rot)
    def p(dx, dy):
        return x + dx * math.cos(t) - dy * math.sin(t), y + dx * math.sin(t) + dy * math.cos(t)
    return atom(*p(-13, 10), RH, 'H') + atom(*p(13, 10), RH, 'H') + atom(*p(0, 0), RO, 'O')
def o2(x, y, rot=0):
    t = math.radians(rot)
    return atom(x - 10 * math.cos(t), y - 10 * math.sin(t), RO, 'O') + atom(x + 10 * math.cos(t), y + 10 * math.sin(t), RO, 'O')

def sci(v, d=1):
    """1.4e-3 -> 1.4\\times10^{-3}"""
    e = int(math.floor(math.log10(abs(v))))
    m = v / 10 ** e
    return f'{m:.{d}f}\\times10^{{{e}}}'
