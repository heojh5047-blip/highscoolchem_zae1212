# 물질과에너지_미래엔 1-1 기체의 성질 — 그림 좌표 도우미
import math, random

INK = '#16233D'; MUTED = '#5B6B7F'; FIELD = '#2E9E6A'; EQUI = '#E08A2C'; PLUS = '#D7263D'; MINUS = '#1F6FD1'
GLASS = '#7E8B98'; WATER = '#DDEEF8'; WATER_E = '#9FC3DD'
GAS = '#6C8EBF'; GAS_E = '#3E5F8F'      # 상자 속 기체 분자(단순 원) — 덱 공통 약속
HOT = '#FDE2E4'; COLD = '#E3EEFB'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def tex(x, y, t, size=20, anchor='middle', fill=None, halo=False, weight=None, mix=False, extra=''):
    a = f'<text class="tex" x="{f(x)}" y="{f(y)}" {"data-mix" if mix else "data-tex"}="{t}" data-size="{size}" data-anchor="{anchor}"'
    if weight: a += f' data-weight="{weight}"'
    if halo: a += ' data-halo="1"'
    if fill: a += f' fill="{fill}"'
    if extra: a += ' ' + extra
    return a + '></text>'


def line(x1, y1, x2, y2, c=INK, w=2, dash=None, extra=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}"{d} {extra}/>'.replace(' />', '/>')


def arw(x1, y1, x2, y2, c='ink', w=3, dash=False):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{c},{w}{",d" if dash else ""}"></g>'


def particles(x, y, w, h, n, r=9, seed=1, pad=3, dense=False):
    """상자 (x,y,w,h) 안에 겹치지 않게 n개 — [(px,py)]"""
    rnd = random.Random(seed)
    pts = []
    tries = 0
    gap = 2 * r + (1 if dense else 6)
    while len(pts) < n and tries < 20000:
        tries += 1
        px = rnd.uniform(x + r + pad, x + w - r - pad)
        py = rnd.uniform(y + r + pad, y + h - r - pad)
        if all((px - a) ** 2 + (py - b) ** 2 >= gap ** 2 for a, b in pts):
            pts.append((px, py))
    return pts


def dot(px, py, r=9):
    return f'<circle cx="{f(px)}" cy="{f(py)}" r="{r}" fill="{GAS}" stroke="{GAS_E}" stroke-width="1.5"/>'


def gas(pts, r=9, amp=5, dur=.7, seed=3, vel=0, vseed=5):
    """기체 분자 묶음 둘(서로 다른 방향으로 흔들림 — 무질서한 운동). vel>0이면 속도 화살표(ink) 함께"""
    rnd = random.Random(vseed)
    A, B = [], []
    for i, (px, py) in enumerate(pts):
        s = dot(px, py, r)
        if vel:
            a = rnd.uniform(0, 2 * math.pi)
            s += line(px + (r + 2) * math.cos(a), py + (r + 2) * math.sin(a), px + (r + vel) * math.cos(a), py + (r + vel) * math.sin(a), INK, 1.8)
            hx, hy = px + (r + vel) * math.cos(a), py + (r + vel) * math.sin(a)
            b1 = a + math.pi * 0.82; b2 = a - math.pi * 0.82
            s += f'<polygon points="{f(hx)},{f(hy)} {f(hx + 6 * math.cos(b1))},{f(hy + 6 * math.sin(b1))} {f(hx + 6 * math.cos(b2))},{f(hy + 6 * math.sin(b2))}" fill="{INK}"/>'
        (A if i % 2 == 0 else B).append(s)
    if amp == 0:
        return ''.join(A + B)
    return (f'<g data-anim="move" data-from="{amp},{-amp * .6:.1f}" data-rep="swing" data-dur="{dur}">' + ''.join(A) + '</g>'
            f'<g data-anim="move" data-from="{-amp * .7:.1f},{amp * .8:.1f}" data-rep="swing" data-dur="{dur * 1.17:.2f}">' + ''.join(B) + '</g>')


def cylinder(x, y, w, h, vfrac, n, seed=1, r=9, bg='#FFFFFF', amp=4, dur=.7, vel=0, weight=None, piston_anim=None):
    """실린더: 바닥 y+h, 위 열림. 피스톤 높이 = vfrac*h. 안 기체 n개."""
    gh = h * vfrac
    top = y + h - gh
    s = f'<rect x="{f(x)}" y="{f(top)}" width="{f(w)}" height="{f(gh)}" fill="{bg}"/>'
    pts = particles(x + 3, top + 12, w - 6, gh - 14, n, r, seed)
    s += gas(pts, r, amp, dur, vel=vel, vseed=seed + 7)
    # 피스톤
    pis = f'<rect x="{f(x + 2)}" y="{f(top - 12)}" width="{f(w - 4)}" height="12" rx="2" fill="#B7C2CE" stroke="{GLASS}" stroke-width="2"/>'
    pis += f'<rect x="{f(x + w / 2 - 6)}" y="{f(top - 52)}" width="12" height="40" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>'
    if weight:
        pis += weight(x + w / 2, top - 52)
    if piston_anim:
        pis = f'<g data-anim="move" data-from="0,{piston_anim}" data-dur="1.4" data-delay=".4" data-ease="out">' + pis + '</g>'
    s += pis
    # 벽
    s += f'<path d="M{f(x)} {f(y - 30)} V{f(y + h)} H{f(x + w)} V{f(y - 30)}" fill="none" stroke="{GLASS}" stroke-width="3"/>'
    return s


# ─── 그래프 ───
class G:
    def __init__(s, ox, oy, pw, ph, xr, yr):
        s.ox, s.oy, s.pw, s.ph, s.xr, s.yr = ox, oy, pw, ph, xr, yr

    def X(s, v):
        return s.ox + (v - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.pw

    def Y(s, v):
        return s.oy - (v - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.ph

    def axes(s, xt, yt, xlab, ylab, xfmt=None, yfmt=None, size=18, origin=True, grid=True, xaxis_at=None):
        o = []
        yb = s.oy if xaxis_at is None else s.Y(xaxis_at)
        if grid:
            for v in xt:
                if s.X(v) > s.ox + 1:
                    o.append(line(s.X(v), s.oy, s.X(v), s.oy - s.ph, '#E3E8EE', 1.2))
            for v in yt:
                if s.Y(v) < s.oy - 1:
                    o.append(line(s.ox, s.Y(v), s.ox + s.pw, s.Y(v), '#E3E8EE', 1.2))
        o.append(arw(s.ox, s.oy + 0.01, s.ox, s.oy - s.ph - 22, 'muted', 2))
        o.append(arw(s.ox - 0.01, yb, s.ox + s.pw + 22, yb, 'muted', 2))
        for v in xt:
            lab = xfmt(v) if xfmt else f(v)
            if lab is None: continue
            o.append(line(s.X(v), yb, s.X(v), yb + 6, MUTED, 2))
            o.append(tex(s.X(v), yb + 26, lab, size))
        for v in yt:
            lab = yfmt(v) if yfmt else f(v)
            if lab is None: continue
            o.append(line(s.ox - 6, s.Y(v), s.ox, s.Y(v), MUTED, 2))
            o.append(tex(s.ox - 10, s.Y(v) + 6, lab, size, 'end'))
        o.append(tex(s.ox + s.pw + 24, yb + 26, xlab, 20, 'end', mix=True))
        o.append(tex(s.ox + 12, s.oy - s.ph - 14, ylab, 20, 'start', mix=True))
        return ''.join(o)

    def pts(s, data, r=6, c=INK, extra=''):
        return ''.join(f'<circle cx="{f(s.X(a))}" cy="{f(s.Y(b))}" r="{r}" fill="{c}" {extra}/>' for a, b in data)

    def curve(s, fn, x0, x1, n=60, c=INK, w=3, dash=None, extra=''):
        p = []
        for i in range(n + 1):
            v = x0 + (x1 - x0) * i / n
            p.append(f'{f(s.X(v))},{f(s.Y(fn(v)))}')
        d = f' stroke-dasharray="{dash}"' if dash else ''
        return f'<polyline points="{" ".join(p)}" fill="none" stroke="{c}" stroke-width="{w}"{d} stroke-linecap="round" {extra}/>'


def svg(w, h, body, disp=None, label='', cls='fig', extra=''):
    disp = disp or w
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" style="width:{disp}px" aria-label="{label}" {extra}>{body}</svg>'.replace(' >', '>')
