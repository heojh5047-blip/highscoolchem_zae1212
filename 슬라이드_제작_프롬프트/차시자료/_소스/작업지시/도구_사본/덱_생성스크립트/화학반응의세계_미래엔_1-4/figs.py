import math, html
Kw = 1e-14
INK='#16233D'; PLUS='#D7263D'; MINUS='#1F6FD1'; FIELD='#2E9E6A'; EQUI='#E08A2C'; GRAV='#8C99A6'; MUTED='#5B6B7F'
GLASS='#7E8B98'; WATER='#DDEEF8'; WATER_S='#9FC3DD'; STAND='#5B6B7F'

def ph(Ca, Va, Vb, Cb=0.1, Ka=None):
    Vt = (Va+Vb)/1000; na = Ca*Va/1000; nb = Cb*Vb/1000
    if Ka is None:
        d = (na-nb)/Vt; H = (d+math.sqrt(d*d+4*Kw))/2; return -math.log10(H)
    Ct = na/Vt; Na = nb/Vt; lo, hi = -14.5, 0.5
    for _ in range(80):
        m = (lo+hi)/2; H = 10**m
        f = H+Na-Ct*Ka/(Ka+H)-Kw/H
        if f > 0: hi = m
        else: lo = m
    return -m

def r(v): return ('%.1f' % v).rstrip('0').rstrip('.')

def esc(s): return html.escape(s, quote=True)

def T(x, y, tex=None, mix=None, size=20, anchor='middle', fill=None, weight=None, halo=False, cls='tex', extra=''):
    a = 'class="%s" x="%s" y="%s"' % (cls, r(x), r(y))
    if tex is not None: a += ' data-tex="%s"' % esc(tex)
    if mix is not None: a += ' data-mix="%s"' % esc(mix)
    a += ' data-size="%d" data-anchor="%s"' % (size, anchor)
    if fill: a += ' fill="%s"' % fill
    if weight: a += ' data-weight="%s"' % weight
    if halo: a += ' data-halo="1"'
    if extra: a += ' ' + extra
    return '<text %s></text>' % a

def line(x1, y1, x2, y2, c=MUTED, w=2, dash=None, extra=''):
    s = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"' % (r(x1), r(y1), r(x2), r(y2), c, w)
    if dash: s += ' stroke-dasharray="%s"' % dash
    return s + (' ' + extra if extra else '') + '/>'

def beaker(x, y, w, h, level, fill=WATER, surf=WATER_S, lip=True):
    """x,y = 왼쪽 위(테 시작), level = 액면 y"""
    x2 = x+w; yb = y+h
    s = '<path d="M%s %s L%s %s Q%s %s %s %s L%s %s Q%s %s %s %s L%s %s Z" fill="%s"/>' % (
        r(x+2), r(level), r(x+2), r(yb-14), r(x+2), r(yb-2), r(x+16), r(yb-2), r(x2-16), r(yb-2), r(x2-2), r(yb-2), r(x2-2), r(yb-14), r(x2-2), r(level), fill)
    s += line(x+2, level, x2-2, level, surf, 2)
    s += '<path d="M%s %s L%s %s L%s %s Q%s %s %s %s L%s %s Q%s %s %s %s L%s %s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (
        r(x-10), r(y), r(x-2), r(y+8), r(x-2), r(yb-14), r(x-2), r(yb+2), r(x+14), r(yb+2), r(x2-14), r(yb+2), r(x2+2), r(yb+2), r(x2+2), r(yb-14), r(x2+2), r(y), GLASS)
    return s

def burette(cx, ytop, ppm, reading, bw=16, vmax=50, labels=True, lsize=18, stop_gap=26, tip_len=22):
    """위가 0 눈금. reading = 지금 눈금(mL). 반환: (svg, tip_y)"""
    y0 = ytop+12; yend = y0+vmax*ppm; stop = yend+stop_gap; tip = stop+tip_len
    s = ''
    yl = y0+reading*ppm
    s += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (r(cx-bw/2+1.5), r(yl), r(bw-3), r(stop-8-yl), WATER)
    s += '<path d="M%s %s Q%s %s %s %s" fill="none" stroke="%s" stroke-width="2"/>' % (r(cx-bw/2+3), r(yl+1.5), r(cx), r(yl+5), r(cx+bw/2-3), r(yl+1.5), WATER_S)
    s += '<rect x="%s" y="%s" width="4" height="%s" fill="%s"/>' % (r(cx-2), r(stop+6), r(tip-stop-10), WATER)
    s += '<path d="M%s %s L%s %s M%s %s L%s %s" fill="none" stroke="%s" stroke-width="2.4"/>' % (r(cx-bw/2), r(ytop), r(cx-bw/2), r(stop-8), r(cx+bw/2), r(ytop), r(cx+bw/2), r(stop-8), GLASS)
    for v in range(0, vmax+1):
        L = 9 if v % 10 == 0 else (6 if v % 5 == 0 else 0)
        if not L: continue
        y = y0+v*ppm
        s += line(cx-bw/2, y, cx-bw/2+L, y, INK if v == 0 else MUTED, 1.6 if v % 10 == 0 else 1.1)
        if labels and v % 10 == 0:
            s += T(cx-bw/2-6, y+6, tex=str(v), size=lsize, anchor='end', fill=INK if v == 0 else MUTED)
    s += '<path d="M%s %s L%s %s L%s %s L%s %s L%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="2.2" stroke-linejoin="round"/>' % (
        r(cx-bw/2), r(stop-8), r(cx-4), r(stop-4), r(cx-4), r(stop+6), r(cx-2.5), r(tip), r(cx+2.5), r(tip), r(cx+4), r(stop+6), r(cx+4), r(stop-4), r(cx+bw/2), r(stop-8), GLASS)
    s += '<rect x="%s" y="%s" width="18" height="10" rx="3" fill="#E9EEF3" stroke="%s" stroke-width="2"/>' % (r(cx-9), r(stop-5), GLASS)
    s += '<rect x="%s" y="%s" width="14" height="7" rx="2" fill="%s"/>' % (r(cx+9), r(stop-3.5), MINUS)
    return s, tip

def stand(xbase, ybase, xrod, ytop, clamp_y, cx):
    s = '<rect x="%s" y="%s" width="%s" height="9" rx="2" fill="%s"/>' % (r(xbase), r(ybase), 150, STAND)
    s += '<rect x="%s" y="%s" width="7" height="%s" fill="#8C99A6" stroke="%s" stroke-width="1.2"/>' % (r(xrod-3.5), r(ytop), r(ybase-ytop), STAND)
    s += line(xrod, clamp_y, cx-12, clamp_y, STAND, 5, extra='stroke-linecap="round"')
    s += '<path d="M%s %s L%s %s L%s %s M%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
        r(cx-13), r(clamp_y-9), r(cx-9), r(clamp_y), r(cx-13), r(clamp_y+9), r(cx+13), r(clamp_y-9), r(cx+9), r(clamp_y), r(cx+13), r(clamp_y+9), STAND)
    return s

def stirrer(x, y, w, h=26):
    s = '<rect x="%s" y="%s" width="%s" height="%s" rx="5" fill="#C9D3DD" stroke="%s" stroke-width="2"/>' % (r(x), r(y), r(w), r(h), STAND)
    s += '<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (r(x+w-18), r(y+h/2), STAND)
    return s

def sensor(x, ytop, ybot):
    s = line(x, ytop, x, ybot-8, '#3A3F47', 7, extra='stroke-linecap="round"')
    s += '<ellipse cx="%s" cy="%s" rx="6" ry="9" fill="#9AA5B1"/>' % (r(x), r(ybot-6))
    return s

def ion(x, y, rr, kind, lab=None, lsize=18):
    if kind == 'p':
        s = '<circle cx="%s" cy="%s" r="%s" fill="#FBD5DA" stroke="%s" stroke-width="2.5"/>' % (r(x), r(y), rr, PLUS)
        s += line(x-rr*.43, y, x+rr*.43, y, PLUS, 2.5) + line(x, y-rr*.43, x, y+rr*.43, PLUS, 2.5)
    elif kind == 'm':
        s = '<circle cx="%s" cy="%s" r="%s" fill="#D6E6FA" stroke="%s" stroke-width="2.5"/>' % (r(x), r(y), rr, MINUS)
        s += line(x-rr*.43, y, x+rr*.43, y, MINUS, 2.5)
    elif kind == 'w':  # 물
        s = '<circle cx="%s" cy="%s" r="%s" fill="#EEF1F4" stroke="%s" stroke-width="2" stroke-dasharray="4 3"/>' % (r(x), r(y), rr, GRAV)
    else:  # 구경꾼
        s = '<circle cx="%s" cy="%s" r="%s" fill="#E3E7EC" stroke="%s" stroke-width="2"/>' % (r(x), r(y), rr, GRAV)
    if lab: s += T(x, y+lsize*.36, tex=lab, size=lsize, fill=INK)
    return s

class Axes:
    def __init__(s, x0, y0, w, h, xmax, ymax, xmin=0, ymin=0):
        s.x0, s.y0, s.w, s.h, s.xmax, s.ymax, s.xmin, s.ymin = x0, y0, w, h, xmax, ymax, xmin, ymin
    def X(s, v): return s.x0+(v-s.xmin)/(s.xmax-s.xmin)*s.w
    def Y(s, v): return s.y0-(v-s.ymin)/(s.ymax-s.ymin)*s.h
    def draw(s, xt, yt, xlab, ylab='\\text{pH}', size=19, ph7=True, grid=False):
        o = line(s.x0, s.y0, s.x0+s.w+12, s.y0, MUTED, 2) + line(s.x0, s.y0, s.x0, s.y0-s.h-14, MUTED, 2)
        o += '<path d="M%s %s L%s %s L%s %s Z" fill="%s"/>' % (r(s.x0+s.w+20), r(s.y0), r(s.x0+s.w+10), r(s.y0-5), r(s.x0+s.w+10), r(s.y0+5), MUTED)
        o += '<path d="M%s %s L%s %s L%s %s Z" fill="%s"/>' % (r(s.x0), r(s.y0-s.h-22), r(s.x0-5), r(s.y0-s.h-12), r(s.x0+5), r(s.y0-s.h-12), MUTED)
        for v in xt:
            X = s.X(v); o += line(X, s.y0, X, s.y0+6, MUTED, 2)
            o += T(X, s.y0+6+size, tex=str(v), size=size, fill=MUTED)
        for v in yt:
            Y = s.Y(v); o += line(s.x0-6, Y, s.x0, Y, MUTED, 2)
            o += T(s.x0-10, Y+size*.36, tex=str(v), size=size, anchor='end', fill=MUTED)
        if ph7:
            o += line(s.x0, s.Y(7), s.x0+s.w, s.Y(7), GRAV, 1.5, '6 5')
        o += T(s.x0+12, s.y0-s.h-10, tex=ylab, size=size, anchor='start', fill=MUTED)
        o += T(s.x0+s.w+14, s.y0+size*2+12, mix=xlab, size=size, anchor='end', fill=MUTED)
        return o
    def curve(s, f, a, b, c=INK, w=3.5, extra='', dash=None, n=400):
        pts = []
        vs = sorted(set([a+(b-a)*i/n for i in range(n+1)]))
        for v in vs:
            y = max(s.ymin, min(s.ymax, f(v)))
            pts.append((s.X(v), s.Y(y)))
        d = 'M' + ' L'.join('%s %s' % (r(x), r(y)) for x, y in pts)
        st = '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"' % (d, c, w)
        if dash: st += ' stroke-dasharray="%s"' % dash
        return st + (' ' + extra if extra else '') + '/>'

def dense(Veq, a, b, n=300):
    """중화점 근처를 촘촘히"""
    vs = [a+(b-a)*i/n for i in range(n+1)]
    vs += [Veq+Veq*0.02*math.tanh(t/20.0)*1.0 for t in range(-60, 61)]
    return sorted(set(v for v in vs if a <= v <= b))

def curve_pts(ax, f, vs, c=INK, w=3.5, extra=''):
    pts = [(ax.X(v), ax.Y(max(ax.ymin, min(ax.ymax, f(v))))) for v in vs]
    d = 'M' + ' L'.join('%s %s' % (r(x), r(y)) for x, y in pts)
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"%s/>' % (d, c, w, (' '+extra) if extra else '')

def dot(x, y, c=INK, rr=6, fill=None):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (r(x), r(y), rr, fill or c, c)
