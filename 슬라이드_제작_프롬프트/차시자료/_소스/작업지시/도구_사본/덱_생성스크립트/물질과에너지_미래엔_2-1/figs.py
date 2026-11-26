# 물질과에너지_미래엔 2-1 그림 좌표 계산 도우미 (물 분자·수소 결합 망·그래프)
import math, random

BOND = '#9AA5B1'
INK, MUTED, PLUS, MINUS, EQUI, FIELD, BF = '#16233D', '#5B6B7F', '#D7263D', '#1F6FD1', '#E08A2C', '#2E9E6A', '#7B4FC8'
HALF = 104.5 / 2

# 크기 단계: 1:1 / 망 모형(×0.6)
S1 = dict(rO=24, rH=18, L=58, hb=110, bw=7)
S6 = dict(rO=14, rH=11, L=35, hb=52, bw=5)


def f(v):
    s = f'{v:.1f}'
    return '0' if s in ('-0.0', '0.0') else (s[:-2] if s.endswith('.0') else s)


def d(a):
    r = math.radians(a)
    return math.cos(r), math.sin(r)


def atom(x, y, r, el, lab='-', dashed=False):
    s = f'{f(x)},{f(y)},{r},{el}'
    if lab is not None:
        s += ',' + lab
    if dashed:
        s += ',d'
    return f'<g data-atom="{s}"></g>'


def bar(x1, y1, x2, y2, w=7):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{BOND}" stroke-width="{w}" stroke-linecap="round"/>'


class W:
    """물 분자: O 위치, phi = 두 H 사이 이등분 방향(°, SVG 좌표: 0 오른쪽, 90 아래)"""

    def __init__(self, x, y, phi, sz=S1):
        self.x, self.y, self.phi, self.sz = x, y, phi, sz
        L = sz['L']
        self.hd = [phi - HALF, phi + HALF]
        self.ld = [phi + 180 - HALF, phi + 180 + HALF]
        self.H = [(x + L * d(a)[0], y + L * d(a)[1]) for a in self.hd]

    def svg(self, labels=False, h_extra=''):
        sz = self.sz
        out = [bar(self.x, self.y, hx, hy, sz['bw']) for hx, hy in self.H]
        lh = None if labels else '-'
        out += [atom(hx, hy, sz['rH'], 'H', lh) for hx, hy in self.H]
        out.append(atom(self.x, self.y, sz['rO'], 'O', lh))
        return ''.join(out)

    def lp_point(self, i, k=1.0):
        a = self.ld[i]
        r = self.sz['rO'] + 12 * k
        return self.x + r * d(a)[0], self.y + r * d(a)[1]


def lobes(w, k=1.0, cls=''):
    out = []
    for a in w.ld:
        cx, cy = w.x + (w.sz['rO'] + 12 * k) * d(a)[0], w.y + (w.sz['rO'] + 12 * k) * d(a)[1]
        out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(17*k)}" ry="{f(11*k)}" transform="rotate({f(a)} {f(cx)} {f(cy)})" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>')
        px, py = -d(a)[1], d(a)[0]
        for s in (-1, 1):
            out.append(f'<circle cx="{f(cx+s*5*k*px)}" cy="{f(cy+s*5*k*py)}" r="{f(3.2*k)}" fill="{INK}"/>')
    return ''.join(out)


def neighbor_via_H(c, i, phi_n, sz=None):
    """c의 i번째 H가 이웃 분자 O로 수소 결합 — 이웃의 비공유 전자쌍 방향이 되돌아오도록 phi_n은 hd[i]±HALF"""
    sz = sz or c.sz
    a = c.hd[i]
    D = sz['L'] + sz['hb']
    return W(c.x + D * d(a)[0], c.y + D * d(a)[1], phi_n, sz)


def neighbor_via_LP(c, i, phi_n, sz=None):
    sz = sz or c.sz
    a = c.ld[i]
    D = sz['L'] + sz['hb']
    return W(c.x + D * d(a)[0], c.y + D * d(a)[1], phi_n, sz)


def hb_line(hx, hy, ox, oy, sz, w=3, extra=''):
    dx, dy = ox - hx, oy - hy
    l = math.hypot(dx, dy)
    ux, uy = dx / l, dy / l
    x1, y1 = hx + ux * (sz['rH'] + 3), hy + uy * (sz['rH'] + 3)
    x2, y2 = ox - ux * (sz['rO'] + 3), oy - uy * (sz['rO'] + 3)
    da = '6 5' if w >= 3 else '4 4'
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{MUTED}" stroke-width="{w}" stroke-dasharray="{da}"{extra}/>'


def tex(x, y, s, size=20, anchor='start', fill=None, mix=True, extra=''):
    a = f' data-anchor="{anchor}"' if anchor != 'start' else ''
    fl = f' fill="{fill}"' if fill else ''
    k = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {k}="{s}" data-size="{size}"{a}{fl}{extra}></text>'


def arw(x1, y1, x2, y2, col='ink', w=3, dash=False, extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if dash else ""}"{extra}></g>'


def legend(x, y, sz=S6, hb=True, size=19):
    """원자 범례: O · H · 수소 결합"""
    out = [atom(x, y - 6, sz['rO'], 'O'), tex(x + sz['rO'] + 6, y, 'O', size),
           atom(x + 62, y - 6, sz['rH'], 'H'), tex(x + 62 + sz['rH'] + 6, y, 'H', size)]
    if hb:
        out.append(f'<line x1="{f(x+116)}" y1="{f(y-6)}" x2="{f(x+150)}" y2="{f(y-6)}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="6 5"/>')
        out.append(tex(x + 156, y, '수소 결합', size))
    return ''.join(out)


# ── 얼음: 벌집 격자(육각 고리) ──
def ice(x0, y0, cols, rows, sz=S6, jitter=0):
    """육각 고리 망. 꼭짓점 = O, 모서리 = O–H…O. 반환 (svg, 분자 수)"""
    D = sz['L'] + sz['hb']
    sq = math.sqrt(3)
    pts = {}
    # 벌집 (pointy-top 육각형 중심 격자의 꼭짓점)
    for r in range(rows):
        for c in range(cols):
            cx = x0 + c * sq * D + (r % 2) * sq * D / 2
            cy = y0 + r * 1.5 * D
            for k in range(6):
                a = math.radians(90 + 60 * k)
                px, py = round(cx + D * math.cos(a), 1), round(cy + D * math.sin(a), 1)
                pts[(round(px), round(py))] = (px, py)
    P = list(pts.values())
    idx = {i: p for i, p in enumerate(P)}
    edges = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if abs(math.hypot(P[i][0] - P[j][0], P[i][1] - P[j][1]) - D) < 2:
                edges.append((i, j))
    own = {i: [] for i in range(len(P))}
    deg = {i: 0 for i in range(len(P))}
    for i, j in edges:
        deg[i] += 1; deg[j] += 1
    for i, j in edges:
        a, b = (i, j) if len(own[i]) <= len(own[j]) else (j, i)
        if len(own[a]) >= 2:
            a, b = b, a
        if len(own[a]) < 2:
            own[a].append(b)
    svg_hb, svg_m = [], []
    for i, p in idx.items():
        hs = []
        for j in own[i]:
            q = idx[j]
            ux, uy = (q[0] - p[0]) / D, (q[1] - p[1]) / D
            hs.append((p[0] + ux * sz['L'], p[1] + uy * sz['L']))
            svg_hb.append(hb_line(hs[-1][0], hs[-1][1], q[0], q[1], sz, 2.5))
        behind = []
        if len(hs) < 2:
            # 남는 방향: 이웃이 없는 방향(가장자리)이면 바깥으로, 아니면 종이 뒤(겹쳐 그림)
            nb = [idx[j] for (a, b) in edges for j in ((b,) if a == i else (a,) if b == i else ())]
            dirs = [math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) for q in nb]
            cand = None
            for k in range(6):
                ang = 90 + 60 * k + 30
                if all(abs(((ang - dd + 180) % 360) - 180) > 50 for dd in dirs):
                    cand = ang; break
            while len(hs) < 2:
                if cand is not None and deg[i] < 3:
                    hs.append((p[0] + sz['L'] * d(cand)[0], p[1] + sz['L'] * d(cand)[1])); cand = None
                else:
                    behind.append((p[0] + 9, p[1] - 9)); hs.append(None)
        m = []
        for b in behind:
            m.append(atom(b[0], b[1], sz['rH'], 'H'))
        for h in hs:
            if h:
                m.append(bar(p[0], p[1], h[0], h[1], sz['bw']))
        for h in hs:
            if h:
                m.append(atom(h[0], h[1], sz['rH'], 'H'))
        m.append(atom(p[0], p[1], sz['rO'], 'O'))
        svg_m.append(''.join(m))
    return ''.join(svg_hb) + ''.join(svg_m), len(P), P


# ── 액체 물: 무질서 ──
def liquid(x0, y0, w, h, n, seed=3, sz=S6, dmin=52, hbmax=None, anim=None):
    rnd = random.Random(seed)
    mols = []
    tries = 0
    while len(mols) < n and tries < 20000:
        tries += 1
        x = x0 + sz['L'] + rnd.random() * (w - 2 * sz['L'])
        y = y0 + sz['L'] + rnd.random() * (h - 2 * sz['L'])
        if all(math.hypot(x - m.x, y - m.y) > dmin for m in mols):
            mols.append(W(x, y, rnd.random() * 360, sz))
    # H가 다른 분자 O·H와 겹치지 않게 방향 조정
    for m in mols:
        best, bs = m.phi, -1
        for k in range(36):
            ph = k * 10
            t = W(m.x, m.y, ph, sz)
            s = min([math.hypot(hx - o.x, hy - o.y) for hx, hy in t.H for o in mols if o is not m] + [999])
            # 경계 밖 금지
            if any(not (x0 + 10 < hx < x0 + w - 10 and y0 + 10 < hy < y0 + h - 10) for hx, hy in t.H):
                continue
            # 수소 결합 하나 이상을 선호(거리 40–60)
            good = sum(1 for hx, hy in t.H for o in mols if o is not m and 28 < math.hypot(hx - o.x, hy - o.y) < (hbmax or sz['hb'] + 12))
            sc = min(s, 34) + good * 8
            if sc > bs:
                bs, best = sc, ph
        m.__init__(m.x, m.y, best, sz)
    hbs = []
    for m in mols:
        for hx, hy in m.H:
            for o in mols:
                if o is m:
                    continue
                dd = math.hypot(hx - o.x, hy - o.y)
                if sz['rO'] + sz['rH'] + 6 < dd < (hbmax or sz['hb'] + 12):
                    hbs.append(hb_line(hx, hy, o.x, o.y, sz, 2.5))
    return mols, hbs


def liquid2(x0, y0, cols, rows, sx, sy, seed=1, sz=S6, region=None, jit=12):
    """흔든 격자 위 무질서한 물 분자(방향은 겹침이 적게)"""
    rnd = random.Random(seed)
    mols = []
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * sx + (r % 2) * sx / 2 + (rnd.random() - .5) * 2 * jit
            y = y0 + r * sy + (rnd.random() - .5) * 2 * jit
            mols.append(W(x, y, rnd.random() * 360, sz))
    X0, Y0, X1, Y1 = region or (0, 0, 1e9, 1e9)
    for _ in range(3):
        for m in mols:
            best, bs = m.phi, -1e9
            for k in range(36):
                ph = k * 10 + rnd.random() * 4
                t = W(m.x, m.y, ph, sz)
                if any(not (X0 + 12 < hx < X1 - 12 and Y0 + 12 < hy < Y1 - 12) for hx, hy in t.H):
                    continue
                dmin = min([math.hypot(hx - o.x, hy - o.y) for hx, hy in t.H for o in mols if o is not m] +
                           [math.hypot(hx - p[0], hy - p[1]) for hx, hy in t.H for o in mols if o is not m for p in o.H] + [999])
                good = sum(1 for hx, hy in t.H for o in mols if o is not m and 30 < math.hypot(hx - o.x, hy - o.y) < 52)
                sc = min(dmin, 30) + good * 6
                if sc > bs:
                    bs, best = sc, ph
            m.__init__(m.x, m.y, best, sz)
    hbs = []
    for m in mols:
        for hx, hy in m.H:
            for o in mols:
                if o is not m and 30 < math.hypot(hx - o.x, hy - o.y) < 54:
                    hbs.append(hb_line(hx, hy, o.x, o.y, sz, 2.5))
    return mols, hbs
