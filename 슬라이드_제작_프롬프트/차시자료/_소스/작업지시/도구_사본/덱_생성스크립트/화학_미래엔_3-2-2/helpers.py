import math, random, sys

def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def T(x, y, m, size=20, anc='middle', fill='#16233D', extra=''):
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" data-mix="{m}" data-size="{size}" data-anchor="{anc}" fill="{fill}"{extra}></text>'
def A(x1, y1, x2, y2, c='ink', w=3): return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{c},{w}"></g>'
def at(x, y, r, el, lab='-'): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{","+lab if lab else ""}"></g>'
def rot(px, py, cx, cy, a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return cx+(px-cx)*c-(py-cy)*s, cy+(px-cx)*s+(py-cy)*c
def no2(cx, cy, r, a=0, lab='-'):
    d = 1.35*r; s = ''
    for b in (-67, 67):
        q = math.radians(-90+b); x, y = rot(cx+d*math.cos(q), cy+d*math.sin(q), cx, cy, a); s += at(x, y, r, 'O', lab)
    return s+at(cx, cy, r, 'N', lab)
def n2o4(cx, cy, r, a=0, lab='-'):
    d = 1.35*r; dn = 1.45*r; s = ''; ns = ''
    for sd in (-1, 1):
        nx = cx+sd*dn/2; base = 0 if sd > 0 else 180
        for b in (-62, 62):
            q = math.radians(base+b); x, y = rot(nx+d*math.cos(q), cy+d*math.sin(q), cx, cy, a); s += at(x, y, r, 'O', lab)
        x, y = rot(nx, cy, cx, cy, a); ns += at(x, y, r, 'N', lab)
    return s+ns
NO2C = '#B5562A'; FIELD = '#2E9E6A'; BF = '#7B4FC8'; EQ = '#E08A2C'; MU = '#5B6B7F'; KF = '#C9D3DD'
OR = '#E8792B'; YE = '#F2C230'; GL = '#7E8B98'; PLUS = '#D7263D'; MINUS = '#1F6FD1'; INK = '#16233D'; HE = '#CFE8F5'
def op(c): return 0.9*(1-math.exp(-c/0.06))
def halfarrows(x1, x2, y, w=3, gap=7):
    return (f'<path d="M{f(x1)} {f(y-gap)} H{f(x2)} l-10 -7" fill="none" stroke="{FIELD}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{f(x2)} {f(y+gap)} H{f(x1)} l10 7" fill="none" stroke="{BF}" stroke-width="{w}" stroke-linecap="round"/>')
def grid(items, x0, y0, w, h, r, seed):
    """items: list of 'a'(NO2)/'b'(N2O4)/'h'(He)/'g'(gas dot). grid with jitter."""
    rnd = random.Random(seed); n = len(items)
    best = None
    for cols in range(1, n+1):
        rows = math.ceil(n/cols); cw, ch = w/cols, h/rows
        sc = min(cw/(3.9*r), ch/(3.6*r))
        if best is None or sc > best[0]: best = (sc, cols, rows)
    _, cols, rows = best; cw, ch = w/cols, h/rows
    cells = [(i % cols, i//cols) for i in range(cols*rows)]; rnd.shuffle(cells)
    order = items[:]; rnd.shuffle(order); s = ''
    for k, (ci, ri) in zip(order, cells):
        jx = max(0, (cw-3.9*r)/2); jy = max(0, (ch-3.6*r)/2)
        cx = x0+cw*(ci+.5)+rnd.uniform(-jx, jx); cy = y0+ch*(ri+.5)+rnd.uniform(-jy, jy)
        a = rnd.choice([0, 30, -30, 60, -60, 90, 120, 150, 180, 210])
        if k == 'a': s += no2(cx, cy, r, a)
        elif k == 'b': s += n2o4(cx, cy, r, a if abs(a) <= 30 else (a % 60)-30)
        elif k == 'h': s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{HE}" stroke="#7FA9C2" stroke-width="1.5"/>'
        else: s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#8C99A6"/>'
    return s
def tube(x, ytop, ybot, w, color, level, extra_liq='', fid=''):
    r = w/2; out = f'M{f(x-r)} {f(ytop)} V{f(ybot-r)} A{f(r)} {f(r)} 0 0 0 {f(x+r)} {f(ybot-r)} V{f(ytop)}'
    li = f'M{f(x-r+3)} {f(level)} V{f(ybot-r)} A{f(r-3)} {f(r-3)} 0 0 0 {f(x+r-3)} {f(ybot-r)} V{f(level)} Z'
    s = f'<path d="{li}" fill="{color}"/>' if color else ''
    s += extra_liq.replace('LIQ', li)
    s += f'<path d="{out}" fill="none" stroke="{GL}" stroke-width="3.5"/><path d="M{f(x-r-5)} {f(ytop)} H{f(x+r+5)}" stroke="{GL}" stroke-width="3.5" stroke-linecap="round"/>'
    return s
def dropper(x, ytip, lab, col=INK, drop=True, anim=True, lx=None, ly=None, anc='start', size=24):
    s = f'<path d="M{x-7} {ytip-70} V{ytip-12} L{x} {ytip} L{x+7} {ytip-12} V{ytip-70} Z" fill="#F4F6F8" stroke="{GL}" stroke-width="2.5"/>'
    s += f'<rect x="{x-11}" y="{ytip-100}" width="22" height="32" rx="9" fill="#5B6B7F"/>'
    if drop:
        d = f'<path d="M{x} {ytip+8} q-6 9 0 14 q6 -5 0 -14 Z" fill="{col}" opacity=".85"/>'
        s += f'<g data-anim="move" data-from="0,-14" data-dur=".8" data-rep="loop">{d}</g>' if anim else d
    s += T(x+18 if lx is None else lx, ytip-44 if ly is None else ly, lab, size, anc, col, ' data-halo="1"')
    return s
def beaker(x, y, w, h, color, aniop=None, delay='.3'):
    # x,y = top-left
    liq = f'<path d="M{f(x+4)} {f(y+h*0.35)} H{f(x+w-4)} V{f(y+h-6)} Q{f(x+w-4)} {f(y+h-2)} {f(x+w-8)} {f(y+h-2)} H{f(x+8)} Q{f(x+4)} {f(y+h-2)} {f(x+4)} {f(y+h-6)} Z" fill="{color}"'
    liq += (f' data-anim="fade" data-dur="1.2" data-delay="{delay}"/>' if aniop else '/>')
    s = liq
    s += f'<path d="M{f(x-6)} {f(y-4)} Q{f(x)} {f(y)} {f(x)} {f(y+8)} V{f(y+h-8)} Q{f(x)} {f(y+h)} {f(x+8)} {f(y+h)} H{f(x+w-8)} Q{f(x+w)} {f(y+h)} {f(x+w)} {f(y+h-8)} V{f(y)}" fill="none" stroke="{GL}" stroke-width="3.5" stroke-linejoin="round"/>'
    for k in range(1, 4):
        yy = y+h-k*h*0.2; s += f'<path d="M{f(x+w-24)} {f(yy)} H{f(x+w-8)}" stroke="{GL}" stroke-width="2"/>'
    return s
def syr(cx, ytop, ybot, w, yp, gas_op, inner='', clamp=False, panim='', label=''):
    """vertical syringe. gas region from yp+12 to ybot."""
    x0 = cx-w/2; s = ''
    s += f'<rect x="{f(x0)}" y="{f(yp+12)}" width="{f(w)}" height="{f(ybot-yp-12)}" fill="{NO2C}" fill-opacity="{gas_op:.2f}"/>' if gas_op > 0 else ''
    s += inner
    for k in range(1, 9):
        yy = ytop+(ybot-ytop)*k/9; s += f'<path d="M{f(x0+w-14)} {f(yy)} H{f(x0+w-2)}" stroke="{MU}" stroke-width="1.5"/>'
    s += f'<path d="M{f(x0)} {f(ytop)} V{f(ybot)} H{f(x0+w)} V{f(ytop)}" fill="none" stroke="{GL}" stroke-width="3.5"/>'
    s += f'<path d="M{f(x0-12)} {f(ytop)} H{f(x0+w+12)}" stroke="{GL}" stroke-width="4" stroke-linecap="round"/>'
    s += f'<rect x="{f(cx-18)}" y="{f(ybot)}" width="36" height="16" rx="3" fill="#2B2F36"/>'
    pl = f'<rect x="{f(x0+2)}" y="{f(yp)}" width="{f(w-4)}" height="12" rx="2" fill="#3A3F47"/><rect x="{f(cx-5)}" y="{f(min(ytop,yp)-46)}" width="10" height="{f(yp-min(ytop,yp)+46)}" fill="#8C99A6"/><rect x="{f(cx-34)}" y="{f(min(ytop,yp)-56)}" width="68" height="12" rx="4" fill="#5B6B7F"/>'
    s += f'<g{panim}>{pl}</g>' if panim else pl
    if clamp:
        s += f'<path d="M{f(x0-22)} {f(yp-2)} H{f(x0+w+22)}" stroke="{PLUS}" stroke-width="5" stroke-linecap="round"/>'
    return s
