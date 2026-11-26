# (선생님 요청) CH4를 정육면체 속에 넣어 보기 — 정확한 3D 좌표를 정사영(평행 투영)해 SVG로.
# 정육면체 꼭짓점 (±1,±1,±1), C = (0,0,0), H = (1,1,1) (-1,-1,1) (1,-1,-1) (-1,1,-1).
# 결합의 쌍극자 모멘트(H → C) ∝ -H.  위쪽 두 H 합 = (0,0,-2), 아래쪽 두 H 합 = (0,0,2), 전체 = 0.
import math
from figs import f, R, BOND, INK, MUTED

ALPHA, BETA = 32, 14          # z축 둘레 회전, 위에서 내려다보는 기울기(°)
PUR, TEAL = '#7B3FB5', '#0E8A7E'  # 위쪽 짝 합(−z), 아래쪽 짝 합(+z)
EDGE = '#5B6B7F'
TET = '#2E9E6A'

# H 번호: 1 (1,1,1) 2 (-1,-1,1) 위쪽 / 3 (1,-1,-1) 4 (-1,1,-1) 아래쪽
H3 = [(1, 1, 1), (-1, -1, 1), (1, -1, -1), (-1, 1, -1)]


def add(a, b): return tuple(p + q for p, q in zip(a, b))
def neg(a): return tuple(-p for p in a)
def mul(a, k): return tuple(p * k for p in a)
def dot(a, b): return sum(p * q for p, q in zip(a, b))
def l3(a): return math.sqrt(dot(a, a))


def make_proj(cx, cy, s):
    a, b = math.radians(ALPHA), math.radians(BETA)

    def P(v):
        x, y, z = v
        x1 = x * math.cos(a) - y * math.sin(a)
        y1 = x * math.sin(a) + y * math.cos(a)          # + : 화면 안쪽
        up = z * math.cos(b) + y1 * math.sin(b)
        depth = -y1 * math.cos(b) + z * math.sin(b)       # + : 보는 사람 쪽
        return (cx + s * x1, cy - s * up, depth)
    W = (-math.sin(a) * math.cos(b), -math.cos(a) * math.cos(b), math.sin(b))  # 보는 사람 쪽 단위 벡터
    return P, W


def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / ((dx * dx + dy * dy) or 1)))
    return math.hypot(ax + dx * t - px, ay + dy * t - py)


def cube_edges(P, W, solid_w=2, col=EDGE, op='1'):
    V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    out = ''
    for i, u in enumerate(V):
        for v in V[i + 1:]:
            diff = [k for k in range(3) if u[k] != v[k]]
            if len(diff) != 1:
                continue
            # 모서리를 공유하는 두 면의 바깥 법선
            fixed = [k for k in range(3) if k != diff[0]]
            ns = []
            for k in fixed:
                n = [0, 0, 0]; n[k] = u[k]; ns.append(tuple(n))
            hidden = all(dot(n, W) < 0 for n in ns)
            p, q = P(u), P(v)
            dash = ' stroke-dasharray="7 6"' if hidden else ''
            out += f'<line x1="{f(p[0])}" y1="{f(p[1])}" x2="{f(q[0])}" y2="{f(q[1])}" stroke="{col}" stroke-width="{solid_w}"{dash} stroke-linecap="round" opacity="{op}"/>'
    return out


def axes(ox, oy, P0, L=40):
    """작은 좌표축 표시 (x, y, z)"""
    s = ''
    o = P0((0, 0, 0))
    for e, nm in (((1, 0, 0), 'x'), ((0, 1, 0), 'y'), ((0, 0, 1), 'z')):
        p = P0(e)
        dx, dy = p[0] - o[0], p[1] - o[1]
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        s += f'<g data-arw="{f(ox)},{f(oy)},{f(ox + ux * L)},{f(oy + uy * L)},muted,2"></g>'
        s += f'<text class="tex" x="{f(ox + ux * (L + 13))}" y="{f(oy + uy * (L + 13) + 7)}" data-tex="{nm}" data-size="19" data-anchor="middle" fill="{MUTED}"></text>'
    return s


def lab(x, y, tex, size=20, col=None, mix=False, anchor='middle'):
    fill = f' fill="{col}"' if col else ''
    key = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {key}="{tex}" data-size="{size}" data-anchor="{anchor}"{fill}></text>'


def cube_figs(arw):
    F = {}
    W_, H_ = 500, 440
    cx, cy, s = 262, 222, 118
    P, W = make_proj(cx, cy, s)
    P0, _ = make_proj(0, 0, 1)
    C = P((0, 0, 0))
    Hp = [P(h) for h in H3]

    # ── 기하 점검 (3D) ──
    bl = [l3(h) for h in H3]
    assert max(bl) - min(bl) < 1e-12, '결합 길이 같아야 함'
    for i in range(4):
        for j in range(i + 1, 4):
            ang = math.degrees(math.acos(dot(H3[i], H3[j]) / (bl[i] * bl[j])))
            assert abs(ang - 109.47) < 0.01, ang
            assert dot(H3[i], H3[j]) != -3, '마주 보는(대각) 꼭짓점이면 안 됨'
            hh = l3(add(H3[i], neg(H3[j])))
            assert abs(hh - 2 * math.sqrt(2)) < 1e-12, '두 H 사이 = 면 대각선'
    mu = [neg(h) for h in H3]                         # H → C
    top, bot = add(mu[0], mu[1]), add(mu[2], mu[3])
    assert top == (0, 0, -2) and bot == (0, 0, 2), (top, bot)
    assert add(top, bot) == (0, 0, 0)
    # 투영이 선형인지(합의 투영 = 투영의 합), z축이 화면 세로인지
    for vec in (top, bot):
        p = P(vec)
        assert abs(p[0] - cx) < 1e-9, '짝 합은 화면에서 세로(축 방향)여야 함'
    for i in range(4):
        a = P(add(mu[0], mu[i])); b = P(mu[0]); c2 = P(mu[i])
        assert abs(a[0] - (b[0] + c2[0] - cx)) < 1e-9 and abs(a[1] - (b[1] + c2[1] - cy)) < 1e-9
    # 화면에서 원자가 겹치지 않음
    pts = [C] + Hp
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            assert d > 60, (i, j, d)
    for p in Hp:
        assert 30 < p[0] < W_ - 30 and 30 < p[1] < H_ - 30, p

    def bond(p, op='1'):
        return f'<line x1="{f(C[0])}" y1="{f(C[1])}" x2="{f(p[0])}" y2="{f(p[1])}" stroke="{BOND}" stroke-width="7" stroke-linecap="round" opacity="{op}"/>'

    def hnum(i, p, size=19):
        dx, dy = p[0] - C[0], p[1] - C[1]
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        # 원자 바깥쪽 옆
        x, y = p[0] + ux * 30 + (-uy) * 0, p[1] + uy * 30
        return lab(x, y + 7, str(i + 1), size, MUTED)

    order = sorted(range(4), key=lambda i: Hp[i][2])     # 뒤 → 앞
    back = [i for i in order if Hp[i][2] < 0]
    front = [i for i in order if Hp[i][2] >= 0]

    # 정사면체 모서리(H–H, 정육면체 면의 대각선): 숨은 면 위면 점선
    def tet_edges():
        o = ''
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = H3[i], H3[j]
                k = [k for k in range(3) if a[k] == b[k]][0]   # 두 점이 놓인 면
                n = [0, 0, 0]; n[k] = a[k]
                hidden = dot(n, W) < 0
                dash = ' stroke-dasharray="6 6"' if hidden else ''
                o += f'<line x1="{f(Hp[i][0])}" y1="{f(Hp[i][1])}" x2="{f(Hp[j][0])}" y2="{f(Hp[j][1])}" stroke="{TET}" stroke-width="2.5"{dash} opacity=".85"/>'
        return o

    # 결합각 호 (H2–C–H3: 앞쪽 두 결합) — 3D 원호를 투영
    def angle_arc(i, j, r=0.26):
        a, b = [mul(H3[k], 1 / math.sqrt(3)) for k in (i, j)]
        th = math.acos(dot(a, b))
        pts = []
        for t in range(0, 31):
            u = t / 30
            w1, w2 = math.sin((1 - u) * th) / math.sin(th), math.sin(u * th) / math.sin(th)
            v = add(mul(a, w1 * r * math.sqrt(3)), mul(b, w2 * r * math.sqrt(3)))
            pts.append(P(v))
        d = 'M' + ' L'.join(f'{f(p[0])} {f(p[1])}' for p in pts)
        m = add(a, b); m = mul(m, 1 / l3(m))
        lp = P(mul(m, r * math.sqrt(3) + 0.36))
        return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2"/>' + lab(lp[0], lp[1] + 7, '109.5^\\circ', 20), [p[:2] for p in pts[::5]] + [lp[:2]]

    # ── 그림 A: 정육면체 + C → H 배치 → 결합의 쌍극자 ──
    a = cube_edges(P, W)
    a += f'<circle cx="{f(C[0])}" cy="{f(C[1])}" r="3" fill="{MUTED}"/>'
    a += axes(66, 420, P0)
    # ② 결합·정사면체 (C보다 먼저 그려 C가 위에 오게)
    g2a = tet_edges() + ''.join(bond(Hp[i]) for i in range(4))
    a += f'<g class="step" data-g="n13b">{g2a}</g>'
    a += f'<g data-atom="{f(C[0])},{f(C[1])},24,C"></g>'
    g2b = ''.join(f'<g data-atom="{f(Hp[i][0])},{f(Hp[i][1])},18,H"></g>' for i in back + front)
    g2b += ''.join(hnum(i, Hp[i]) for i in range(4))
    def sang(i, j):
        u = (Hp[i][0] - C[0], Hp[i][1] - C[1]); v = (Hp[j][0] - C[0], Hp[j][1] - C[1])
        return math.degrees(math.acos((u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))
    AP = min(((i, j) for i in range(4) for j in range(i + 1, 4)), key=lambda ij: abs(sang(*ij) - 109.5))
    arc_svg, arc_pts = angle_arc(*AP)
    g2b += arc_svg
    a += f'<g class="step" data-g="n13b">{g2b}</g>'
    # ③ 결합의 쌍극자 모멘트: 결합 옆에 나란히, H 쪽(꼬리 +) → C 쪽
    segs = [(C[:2], Hp[i][:2]) for i in range(4)]
    arrs = ''
    lens3d = []
    for i in range(4):
        hx, hy = Hp[i][0], Hp[i][1]
        dx, dy = hx - C[0], hy - C[1]
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        best = None
        for sd in (1, -1):
            off = 19
            t0, t1 = 0.86, 0.42
            x1, y1 = C[0] + dx * t0 + px * off * sd, C[1] + dy * t0 + py * off * sd
            x2, y2 = C[0] + dx * t1 + px * off * sd, C[1] + dy * t1 + py * off * sd
            mid = ((x1 + x2) / 2, (y1 + y2) / 2)
            clr = min(seg_dist(mid, *segs[k]) for k in range(4) if k != i)
            clr = min(clr, min(seg_dist(mid, Hp[k][:2], Hp[m][:2]) for k in range(4) for m in range(k + 1, 4)))
            clr = min(clr, min(math.hypot(mid[0] - q[0], mid[1] - q[1]) for q in arc_pts) - 6)
            if best is None or clr > best[0]:
                best = (clr, x1, y1, x2, y2)
        _, x1, y1, x2, y2 = best
        assert math.hypot(x2 - C[0], y2 - C[1]) < math.hypot(x1 - C[0], y1 - C[1]), '화살표는 H → C'
        lens3d.append(0.5 * l3(H3[i]))
        arrs += arw(x1, y1, x2, y2)
    assert max(lens3d) == min(lens3d)
    a += f'<g class="step" data-g="n13c">{arrs}</g>'
    F['S13CUBE'] = a

    # ── 그림 B: 쌍극자 4개를 C에 모아 짝지어 더하기 ──
    k = 0.65         # 화살표 = 0.65 × (−H)
    b = cube_edges(P, W, 2, EDGE, '.55')
    b += ''.join(bond(Hp[i], '.35') for i in range(4))
    b += '<g opacity=".45">' + ''.join(f'<g data-atom="{f(Hp[i][0])},{f(Hp[i][1])},18,H"></g>' for i in back + front) + '</g>'
    b += ''.join(hnum(i, Hp[i]) for i in range(4))
    b += axes(66, 420, P0)
    tips = [P(mul(m, k)) for m in mu]
    # 모은 쌍극자(검정): 꼬리 = C
    vec = ''
    for i in range(4):
        vec += arw(C[0], C[1], tips[i][0], tips[i][1])
    # μ 라벨: 끝 바깥쪽
    mlab = ''
    for i in range(4):
        dx, dy = tips[i][0] - C[0], tips[i][1] - C[1]
        n = math.hypot(dx, dy)
        sx = 1 if dx >= 0 else -1
        mlab += lab(tips[i][0] + dx / n * 16 + sx * 14, tips[i][1] + dy / n * 16 + 7, f'\\mu_{i + 1}', 20)
    b += vec + mlab
    dirs = [math.atan2(t[1] - C[1], t[0] - C[0]) for t in tips] + [math.pi / 2, -math.pi / 2]
    def gap(th):
        return min(abs((th - d + math.pi) % (2 * math.pi) - math.pi) for d in dirs)
    th = max((math.radians(a_) for a_ in range(0, 360, 5)), key=gap)
    b += f'<g data-atom="{f(C[0])},{f(C[1])},8,C,-"></g>' + lab(C[0] + math.cos(th) * 24, C[1] + math.sin(th) * 24 + 7, '\\mathrm{C}', 20)

    def pair(i, j, col, g):
        st = P(mul(add(mu[i], mu[j]), k))
        o = ''
        for p_, q_ in ((tips[i], st), (tips[j], st)):
            o += f'<line x1="{f(p_[0])}" y1="{f(p_[1])}" x2="{f(q_[0])}" y2="{f(q_[1])}" stroke="{col}" stroke-width="2" stroke-dasharray="6 5"/>'
        o += arw(C[0], C[1], st[0], st[1], col, 5)
        # 평행사변형 점검: 끝 + 다른 벡터 = 합 끝
        for p_, m in ((tips[i], mu[j]), (tips[j], mu[i])):
            q = P(mul(m, k))
            assert abs(p_[0] + q[0] - C[0] - st[0]) < 1e-9 and abs(p_[1] + q[1] - C[1] - st[1]) < 1e-9
        return f'<g class="step" data-g="{g}">{o}</g>', st

    gtop, st_top = pair(0, 1, PUR, 'n14a')
    gbot, st_bot = pair(2, 3, TEAL, 'n14b')
    b += gtop + gbot
    assert abs((st_top[1] - C[1]) + (st_bot[1] - C[1])) < 1e-9 and abs(st_top[0] - cx) < 1e-9
    F['S14CUBE'] = b
    F['_pos'] = (C, Hp, tips, st_top, st_bot)
    return F
