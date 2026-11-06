# 4-1-1 덱 그림 좌표 생성 도우미
import math, random

INK = '#16233D'; MUTED = '#5B6B7F'; PLUS = '#D7263D'; MINUS = '#1F6FD1'; FIELD = '#2E9E6A'; BF = '#7B4FC8'
EQUI = '#E08A2C'; GRAV = '#8C99A6'; GLASS = '#7E8B98'; WATER = '#DDEEF8'; WATER_S = '#9FC3DD'; CU = '#3E8ED0'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def atom(x, y, r, el, lab=None, d=False):
    a = f'{f(x)},{f(y)},{f(r)},{el}'
    if lab is not None:
        a += ',' + lab
    if d:
        a += ',d'
    return f'<g data-atom="{a}"></g>'


def tex(x, y, t=None, mix=None, size=20, anchor='middle', fill=None, weight=None, halo=False, extra=''):
    s = f'<text class="tex" x="{f(x)}" y="{f(y)}"'
    if t is not None:
        s += f' data-tex="{t}"'
    if mix is not None:
        s += f' data-mix="{mix}"'
    s += f' data-size="{size}" data-anchor="{anchor}"'
    if weight:
        s += f' data-weight="{weight}"'
    if halo:
        s += ' data-halo="1"'
    if fill:
        s += f' fill="{fill}"'
    if extra:
        s += ' ' + extra
    return s + '></text>'


def arw(x1, y1, x2, y2, col='ink', w=3, dash=False, extra=''):
    s = f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if dash else ""}"'
    return s + (' ' + extra if extra else '') + '></g>'


def pol(cx, cy, d, ang):
    a = math.radians(ang)
    return cx + d * math.cos(a), cy + d * math.sin(a)


# ── 분자·이온 (O 먼저, H 위에) ──
def water(cx, cy, dir=90, s=1.0, lab=True, rO=24, rH=18, d=36):
    out = [atom(cx, cy, rO * s, 'O', None if lab else '-')]
    for a in (dir - 52.25, dir + 52.25):
        x, y = pol(cx, cy, d * s, a)
        out.append(atom(x, y, rH * s, 'H', None if lab else '-'))
    return ''.join(out)


def small_water(cx, cy, dir):
    return water(cx, cy, dir, 1, False, 12, 8, 15)


def hydronium(cx, cy, dirs=(125, 235, 0), s=1.0, sign=True, anim_last=None, lab=True):
    out = [atom(cx, cy, 24 * s, 'O', None if lab else '-')]
    for i, a in enumerate(dirs):
        x, y = pol(cx, cy, 36 * s, a)
        at = atom(x, y, 18 * s, 'H', None if lab else '-')
        if anim_last and i == len(dirs) - 1:
            at = f'<g data-anim="move" data-from="{anim_last}" data-dur="1.2" data-delay=".5" data-ease="out">{at}</g>'
        out.append(at)
    if sign:
        out.append(tex(cx + 30 * s, cy - 30 * s, '+', size=int(30 * s), fill=PLUS, weight=700))
    return ''.join(out)


def hydroxide(cx, cy, dir=230, s=1.0, sign=True, lab=True):
    out = [atom(cx, cy, 24 * s, 'O', None if lab else '-')]
    x, y = pol(cx, cy, 36 * s, dir)
    out.append(atom(x, y, 18 * s, 'H', None if lab else '-'))
    if sign:
        out.append(tex(cx + 30 * s, cy - 30 * s, '-', size=int(30 * s), fill=MINUS, weight=700))
    return ''.join(out)


# ── 기구 ──
def flask_path(cx, base, R=60, neck=22, top=None, s=1.0):
    R *= s; neck *= s
    cy = base - R * 0.86
    hw = neck / 2
    yj = cy - math.sqrt(R * R - hw * hw)
    hb = math.sqrt(R * R - (base - cy) ** 2)
    if top is None:
        top = cy - 150 * s
    d = (f'M{f(cx-hw)},{f(top)} L{f(cx-hw)},{f(yj)} A{f(R)},{f(R)} 0 0 0 {f(cx-hb)},{f(base)} '
         f'L{f(cx+hb)},{f(base)} A{f(R)},{f(R)} 0 0 0 {f(cx+hw)},{f(yj)} L{f(cx+hw)},{f(top)}')
    return d, cy, top, hw


def flask(cx, base, cid, level=None, R=60, neck=22, s=1.0, mark=None, color=WATER, stroke=WATER_S, stopper=False, top=None,
          extra_liquid='', mark_label=None, liq_anim=''):
    d, cy, tp, hw = flask_path(cx, base, R, neck, top, s)
    if mark is None:
        mark = cy - 100 * s
    out = [f'<defs><clipPath id="{cid}"><path d="{d} Z"/></clipPath></defs>']
    if level is not None:
        out.append(f'<g clip-path="url(#{cid})"><g {liq_anim}><rect x="{f(cx-R*s-2)}" y="{f(level)}" width="{f(2*R*s+4)}" height="{f(base-level+2)}" fill="{color}"/>'
                   f'<line x1="{f(cx-R*s)}" y1="{f(level)}" x2="{f(cx+R*s)}" y2="{f(level)}" stroke="{stroke}" stroke-width="2"/></g>{extra_liquid}</g>')
    out.append(f'<path d="{d}" fill="none" stroke="{GLASS}" stroke-width="2.6" stroke-linejoin="round"/>')
    out.append(f'<line x1="{f(cx-hw-5)}" y1="{f(mark)}" x2="{f(cx+hw+5)}" y2="{f(mark)}" stroke="{INK}" stroke-width="2"/>')
    if stopper:
        out.append(f'<rect x="{f(cx-hw-3)}" y="{f(tp-14*s)}" width="{f(2*hw+6)}" height="{f(16*s)}" rx="3" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>')
    if mark_label:
        out.append(tex(cx + hw + 10, mark + 6, mix=mark_label, size=19, anchor='start', fill=MUTED))
    return ''.join(out), cy, mark, tp


def beaker(x, base, w, h, level=None, color=WATER, stroke=WATER_S, ticks=0, liq_anim=''):
    top = base - h
    out = []
    if level is not None:
        out.append(f'<g {liq_anim}><rect x="{f(x+1.5)}" y="{f(level)}" width="{f(w-3)}" height="{f(base-level-1.5)}" fill="{color}"/>'
                   f'<line x1="{f(x+1.5)}" y1="{f(level)}" x2="{f(x+w-1.5)}" y2="{f(level)}" stroke="{stroke}" stroke-width="2"/></g>')
    out.append(f'<path d="M{f(x-5)},{f(top-4)} L{f(x)},{f(top+4)} L{f(x)},{f(base)} L{f(x+w)},{f(base)} L{f(x+w)},{f(top+4)} L{f(x+w+5)},{f(top-4)}" '
               f'fill="none" stroke="{GLASS}" stroke-width="2.6" stroke-linejoin="round"/>')
    for i in range(1, ticks + 1):
        yy = base - h * i / (ticks + 1)
        out.append(f'<line x1="{f(x)}" y1="{f(yy)}" x2="{f(x+12)}" y2="{f(yy)}" stroke="{MUTED}" stroke-width="1.5"/>')
    return ''.join(out)


def balance(x, y, w=150, reading='1.46\\ \\text{g}', dish=True, heap=True, read_anim=''):
    # x,y = 왼쪽 위(접시 높이)
    out = []
    out.append(f'<rect x="{f(x)}" y="{f(y+22)}" width="{f(w)}" height="58" rx="8" fill="#EEF2F6" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<rect x="{f(x+w/2-42)}" y="{f(y+12)}" width="84" height="10" rx="2" fill="#C9D3DD" stroke="{INK}" stroke-width="2"/>')
    if dish:
        out.append(f'<path d="M{f(x+w/2-38)},{f(y+12)} L{f(x+w/2-30)},{f(y+2)} L{f(x+w/2+30)},{f(y+2)} L{f(x+w/2+38)},{f(y+12)} Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/>')
    if heap:
        out.append(f'<path d="M{f(x+w/2-18)},{f(y+3)} Q{f(x+w/2)},{f(y-14)} {f(x+w/2+18)},{f(y+3)} Z" fill="#F4F6F8" stroke="{MUTED}" stroke-width="1.5"/>')
    out.append(f'<rect x="{f(x+18)}" y="{f(y+38)}" width="{f(w-36)}" height="30" rx="4" fill="#E3F2E9" stroke="{INK}" stroke-width="1.5"/>')
    rd = tex(x + w / 2, y + 62, reading, size=24, weight=700)
    if read_anim:
        rd = f'<g {read_anim}>{rd}</g>'
    out.append(rd)
    return ''.join(out)


def rand_points(n, x0, y0, x1, y1, mind, seed, avoid=()):
    rnd = random.Random(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        if all(math.hypot(x - a, y - b) >= mind for a, b in pts) and all(math.hypot(x - a, y - b) >= r for a, b, r in avoid):
            pts.append((x, y))
    return pts
