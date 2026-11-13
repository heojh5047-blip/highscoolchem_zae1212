# 3-1 탄소 화합물의 종류 — 그림 좌표 도우미 (구조식 sf, 3차원 공-막대 bs3d)
import math

R = {'H': 18, 'C': 24, 'O': 24, 'N': 24}
BOND = '#9AA5B1'
INK = '#16233D'
MUTED = '#5B6B7F'
EQUI = '#E08A2C'


def f(v):
    s = f'{v:.1f}'
    s = s[:-2] if s.endswith('.0') else s
    return '0' if s == '-0' else s


# ───────── 구조식 (2D) ─────────
def lab_tex(sym):
    if sym in ('C', 'H', 'O', 'N', 'R'):
        return '\\mathrm{%s}' % sym
    return '\\ce{%s}' % sym


def half_w(sym, S):
    n = len(sym.replace('2', '').replace('3', '')) + 0.55 * (sum(ch.isdigit() for ch in sym))
    return (0.36 + 0.33 * (n - 1)) * S


def sf(atoms, bonds, S=28, col=INK, lw=3, gap=7, extra=''):
    """atoms: [(sym,x,y)] 중심 좌표, bonds: [(i,j,order)]"""
    out = []
    for i, j, o in bonds:
        s1, x1, y1 = atoms[i]
        s2, x2, y2 = atoms[j]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L

        def cut(sym):
            hw, hh = half_w(sym, S) + 0.16 * S, 0.5 * S
            # 타원 경계까지 거리
            return 1 / math.sqrt((ux / hw) ** 2 + (uy / hh) ** 2)
        a, b = cut(s1), cut(s2)
        px, py = -uy, ux
        offs = {1: [0], 2: [-gap / 2, gap / 2], 3: [-gap, 0, gap]}[o]
        for k in offs:
            out.append(f'<line x1="{f(x1 + ux * a + px * k)}" y1="{f(y1 + uy * a + py * k)}" x2="{f(x2 - ux * b + px * k)}" y2="{f(y2 - uy * b + py * k)}" stroke="{col}" stroke-width="{lw}" stroke-linecap="round"/>')
    for sym, x, y in atoms:
        out.append(f'<text class="tex" x="{f(x)}" y="{f(y + 0.36 * S)}" data-tex="{lab_tex(sym)}" data-size="{S}" data-anchor="middle"></text>')
    return ''.join(out) + extra


def box(x, y, w, h, g=None, cls='', anim=''):
    c = f' class="step{(" " + cls) if cls else ""}" data-g="{g}"' if g else (f' class="{cls}"' if cls else '')
    return f'<rect{c}{anim} x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="10" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>'


def chain(n, fg, x0, y0, d=62, S=28, Hup=True):
    """탄소 n개 가로 사슬 + 끝 작용기. fg: None|'OH'|'CHO'|'COOH'. 반환 atoms, bonds, 작용기 상자(x,y,w,h)"""
    atoms, bonds = [], []
    x = x0
    atoms.append(('H', x, y0)); x += d
    cidx = []
    for k in range(n):
        atoms.append(('C', x, y0)); ci = len(atoms) - 1; cidx.append(ci)
        bonds.append((ci - 1 if k == 0 else cidx[k - 1], ci, 1))
        last = (k == n - 1)
        if last and fg in ('CHO', 'COOH'):
            atoms.append(('O', x, y0 - d)); bonds.append((ci, len(atoms) - 1, 2))
        else:
            atoms.append(('H', x, y0 - d)); bonds.append((ci, len(atoms) - 1, 1))
            atoms.append(('H', x, y0 + d)); bonds.append((ci, len(atoms) - 1, 1))
        x += d
    ce = cidx[-1]
    gb = None
    if fg is None:
        atoms.append(('H', x, y0)); bonds.append((ce, len(atoms) - 1, 1))
    elif fg == 'OH':
        atoms.append(('O', x, y0)); oi = len(atoms) - 1; bonds.append((ce, oi, 1))
        atoms.append(('H', x + d, y0)); bonds.append((oi, len(atoms) - 1, 1))
        gb = (x - 0.62 * S, y0 - 0.62 * S, d + 1.24 * S, 1.24 * S)
    elif fg == 'CHO':
        atoms.append(('H', x, y0)); bonds.append((ce, len(atoms) - 1, 1))
        xc = x - d
        gb = (xc - 0.62 * S, y0 - d - 0.62 * S, d + 1.24 * S, d + 1.24 * S)
    elif fg == 'COOH':
        atoms.append(('O', x, y0)); oi = len(atoms) - 1; bonds.append((ce, oi, 1))
        atoms.append(('H', x + d, y0)); bonds.append((oi, len(atoms) - 1, 1))
        xc = x - d
        gb = (xc - 0.62 * S, y0 - d - 0.62 * S, 2 * d + 1.24 * S, d + 1.24 * S)
    return atoms, bonds, gb


def chain_svg(n, fg, x0, y0, d=62, S=28, g=None, label=None, lab_size=20, box_cls='', box_anim=''):
    a, b, gb = chain(n, fg, x0, y0, d, S)
    s = ''
    if gb:
        s += box(*gb, g=g, cls=box_cls, anim=box_anim)
    s += sf(a, b, S)
    if gb and label:
        x, y, w, h = gb
        s += f'<text class="tex{" step" if g else ""}"{f" data-g=\"{g}\"" if g else ""} x="{f(x + w / 2)}" y="{f(y + h + lab_size + 4)}" data-mix="{label}" data-size="{lab_size}" data-anchor="middle" fill="{EQUI}" data-weight="700"></text>'
    return s


def chain_width(n, fg, d=62):
    extra = {None: 1, 'OH': 2, 'CHO': 1, 'COOH': 2}[fg]
    return d * (n + extra)


# ───────── 3차원 공-막대 ─────────
def add(a, b): return tuple(p + q for p, q in zip(a, b))
def sub(a, b): return tuple(p - q for p, q in zip(a, b))
def mul(a, k): return tuple(p * k for p in a)
def dot(a, b): return sum(p * q for p, q in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm(a):
    l = math.sqrt(dot(a, a)); return tuple(p / l for p in a)


def tet_rest(u_list, w=None):
    """기존 결합 방향 목록에서 나머지 정사면체 방향"""
    z = (0, 0, 1)
    if len(u_list) == 1:
        u = norm(u_list[0])
        if w is None:
            w = norm(cross(z, u))
        w = norm(sub(w, mul(u, dot(w, u))))
        v = cross(u, w)
        t = math.radians(70.53)
        return [norm(add(mul(u, -math.cos(t)), add(mul(w, math.sin(t) * math.cos(math.radians(p))), mul(v, math.sin(t) * math.sin(math.radians(p)))))) for p in (0, 120, 240)]
    if len(u_list) == 2:
        u1, u2 = norm(u_list[0]), norm(u_list[1])
        bsec = norm(mul(add(u1, u2), -1))
        n = norm(cross(u1, u2))
        t = math.radians(54.75)
        return [norm(add(mul(bsec, math.cos(t)), mul(n, math.sin(t)))), norm(add(mul(bsec, math.cos(t)), mul(n, -math.sin(t))))]
    if len(u_list) == 3:
        return [norm(mul(add(add(norm(u_list[0]), norm(u_list[1])), norm(u_list[2])), -1))]
    raise ValueError


def rot3(v, yaw, pitch):
    x, y, z = v
    a = math.radians(yaw)
    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    b = math.radians(pitch)
    y, z = y * math.cos(b) - z * math.sin(b), y * math.sin(b) + z * math.cos(b)
    return (x, y, z)


def best_view(atoms, k, sc):
    best = None
    c = mul(tuple(sum(a[1][i] for a in atoms) for i in range(3)), 1 / len(atoms))
    for yaw in range(-90, 91, 6):
        for pitch in range(-40, 41, 8):
            P = [rot3(sub(p, c), yaw, pitch) for _, p in atoms]
            m = min(math.hypot((P[i][0] - P[j][0]) * k, (P[i][1] - P[j][1]) * k) - (R[atoms[i][0]] + R[atoms[j][0]]) * sc * .6
                    for i in range(len(P)) for j in range(i + 1, len(P)))
            if best is None or m > best[0] + 1e-6:
                best = (m, yaw, pitch)
    return best[1], best[2]


def bs3d(atoms, bonds, cx, cy, k=62, yaw=0, pitch=0, sc=1.0, labels=True, anim=None, center=None, rlab=None):
    """yaw='auto' 이면 원자끼리 가장 덜 겹치는 보기 각도.atoms: [(el,(x,y,z))] Å, bonds: [(i,j,order)]. k: px/Å. anim: 'out' → 원자가 중심 쪽에서 바깥으로 move"""
    if yaw == 'auto':
        yaw, pitch = best_view(atoms, k, sc)
    P = []
    if center is None:
        center = mul(tuple(sum(a[1][i] for a in atoms) for i in range(3)), 1 / len(atoms))
    for el, p in atoms:
        v = rot3(sub(p, center), yaw, pitch)
        P.append((cx + v[0] * k, cy - v[1] * k, v[2]))
    items = []
    for i, j, o in bonds:
        x1, y1, z1 = P[i]; x2, y2, z2 = P[j]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        px, py = -dy / n, dx / n
        offs = {1: [0], 2: [-4.5 * sc, 4.5 * sc], 3: [-7.5 * sc, 0, 7.5 * sc]}[o]
        w = (7 if o == 1 else 5) * sc
        s = ''.join(f'<line x1="{f(x1 + px * q)}" y1="{f(y1 + py * q)}" x2="{f(x2 + px * q)}" y2="{f(y2 + py * q)}" stroke="{BOND}" stroke-width="{f(w)}" stroke-linecap="round"/>' for q in offs)
        items.append(((z1 + z2) / 2 - 0.01, s))
    for idx, ((el, _), (x, y, z)) in enumerate(zip(atoms, P)):
        r = R[el] * sc
        lab = '' if (labels and r >= 18.5) else ',-'
        if rlab and idx in rlab:
            lab = ',' + rlab[idx]
        s = f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{lab}"></g>'
        if anim == 'out':
            s = f'<g data-anim="move" data-from="{f((cx - x) * .35)},{f((cy - y) * .35)}" data-dur="1.1" data-delay=".3" data-ease="out">{s}</g>'
        items.append((z, s))
    items.sort(key=lambda t: t[0])
    return ''.join(s for _, s in items), P


# 분자 3차원 좌표 만들기 (xy 평면 지그재그 골격)
BL = {('C', 'C', 1): 1.54, ('C', 'C', 2): 1.34, ('C', 'C', 3): 1.20, ('C', 'H', 1): 1.09, ('C', 'O', 1): 1.43, ('C', 'O', 2): 1.21, ('O', 'H', 1): 0.96}


def bl(a, b, o):
    return BL.get((a, b, o)) or BL.get((b, a, o))


def mol_alkane_like(n, fg=None):
    """CnH(2n+1)-X 지그재그 (fg None/OH/CHO/COOH). 반환 atoms, bonds"""
    atoms, bonds = [], []
    ang = math.radians(109.5)
    # 골격 방향: 번갈아 +30°, -30°(수평 기준) → 사이각 120에 가깝게, sp3면 109.5
    pos = [(0.0, 0.0, 0.0)]
    atoms.append(('C', pos[0]))
    heavy = [0]
    dirs = []
    half = (math.pi - ang) / 2
    for k in range(1, n):
        s = 1 if k % 2 == 1 else -1
        d = (math.cos(half), s * math.sin(half), 0)
        p = add(atoms[heavy[-1]][1], mul(d, bl('C', 'C', 1)))
        atoms.append(('C', p)); bonds.append((heavy[-1], len(atoms) - 1, 1)); heavy.append(len(atoms) - 1)
    last = heavy[-1]
    s = 1 if n % 2 == 1 else -1
    dnext = (math.cos(half), s * math.sin(half), 0)
    sp2 = fg in ('CHO', 'COOH')
    if fg == 'OH':
        po = add(atoms[last][1], mul(dnext, bl('C', 'O', 1)))
        atoms.append(('O', po)); oi = len(atoms) - 1; bonds.append((last, oi, 1))
        s2 = -s
        dh = (math.cos(half), s2 * math.sin(half), 0)
        atoms.append(('H', add(po, mul(norm(dh), bl('O', 'H', 1))))); bonds.append((oi, len(atoms) - 1, 1))
    # 수소
    for idx, ci in enumerate(heavy):
        nb = [sub(atoms[j][1], atoms[ci][1]) for (i, j, o) in bonds if i == ci] + [sub(atoms[i][1], atoms[ci][1]) for (i, j, o) in bonds if j == ci]
        if ci == last and sp2:
            # 평면 삼각형: 이웃 방향 u, 나머지 두 방향 ±120°
            if nb:
                u = norm(nb[0])
            else:
                u = (-1, 0, 0)
            th = math.atan2(u[1], u[0])
            d1 = (math.cos(th + math.radians(120)), math.sin(th + math.radians(120)), 0)
            d2 = (math.cos(th - math.radians(120)), math.sin(th - math.radians(120)), 0)
            if d1[1] < d2[1]:
                d1, d2 = d2, d1
            po = add(atoms[ci][1], mul(d1, bl('C', 'O', 2)))
            atoms.append(('O', po)); bonds.append((ci, len(atoms) - 1, 2))
            if fg == 'CHO':
                atoms.append(('H', add(atoms[ci][1], mul(d2, bl('C', 'H', 1))))); bonds.append((ci, len(atoms) - 1, 1))
            else:
                po2 = add(atoms[ci][1], mul(d2, bl('C', 'O', 1)))
                atoms.append(('O', po2)); oi = len(atoms) - 1; bonds.append((ci, oi, 1))
                dd = norm(sub(po2, atoms[ci][1]))
                th2 = math.atan2(dd[1], dd[0]) + math.radians(-105 if d2[1] < 0 else 105) * (1)
                # O–H 는 C=O 반대쪽으로 꺾어 평면에
                cand = [(math.cos(math.atan2(dd[1], dd[0]) + math.radians(a)), math.sin(math.atan2(dd[1], dd[0]) + math.radians(a)), 0) for a in (75, -75)]
                dh = max(cand, key=lambda c: -dot(c, d1))
                atoms.append(('H', add(po2, mul(dh, bl('O', 'H', 1))))); bonds.append((oi, len(atoms) - 1, 1))
            if n == 1 and fg == 'CHO':
                pass
            if n == 1:
                # 폼알데하이드·폼산: 남은 자리 H 하나 (u 방향)
                atoms.append(('H', add(atoms[ci][1], mul(u, bl('C', 'H', 1))))); bonds.append((ci, len(atoms) - 1, 1))
            continue
        need = 4 - len(nb)
        if len(nb) == 0:
            ds = [(0, 1, 0)] + [(math.sqrt(8) / 3 * math.sin(math.radians(p)), -1 / 3, math.sqrt(8) / 3 * math.cos(math.radians(p))) for p in (0, 120, 240)]
        elif len(nb) == 1:
            u = norm(nb[0])
            w = (0, -1 if (u[1] >= 0) else 1, 0) if abs(u[0]) > .5 else (1, 0, 0)
            if ci == 0 and n > 1:
                w = (-1, 0, 0)
            ds = tet_rest([u], w)
        else:
            ds = tet_rest(nb)
        for d in ds[:need]:
            atoms.append(('H', add(atoms[ci][1], mul(d, bl('C', 'H', 1))))); bonds.append((ci, len(atoms) - 1, 1))
    return atoms, bonds


def mol_ethene():
    c = 0.67
    a = [('C', (-c, 0, 0)), ('C', (c, 0, 0))]
    b = [(0, 1, 2)]
    for sx, i in ((-1, 0), (1, 1)):
        for sy in (1, -1):
            a.append(('H', (sx * (c + 1.09 * math.cos(math.radians(60))), sy * 1.09 * math.sin(math.radians(60)), 0))); b.append((i, len(a) - 1, 1))
    return a, b


def mol_ethyne():
    c = 0.60
    a = [('C', (-c, 0, 0)), ('C', (c, 0, 0)), ('H', (-c - 1.06, 0, 0)), ('H', (c + 1.06, 0, 0))]
    return a, [(0, 1, 3), (0, 2, 1), (1, 3, 1)]


def mol_methane():
    r = math.sqrt(8) / 3
    ds = [(0, 1, 0)] + [(r * math.sin(math.radians(p)), -1 / 3, r * math.cos(math.radians(p))) for p in (0, 120, 240)]
    a = [('C', (0, 0, 0))] + [('H', mul(d, 1.09)) for d in ds]
    return a, [(0, i, 1) for i in range(1, 5)]


def mol_benzene():
    a, b = [], []
    for k in range(6):
        t = math.radians(90 + 60 * k)
        a.append(('C', (1.39 * math.cos(t), 1.39 * math.sin(t), 0)))
    for k in range(6):
        t = math.radians(90 + 60 * k)
        a.append(('H', (2.48 * math.cos(t), 2.48 * math.sin(t), 0)))
        b.append((k, (k + 1) % 6, 2 if k % 2 == 0 else 1)); b.append((k, 6 + k, 1))
    return a, b


def lewis_c(x, y, S=40):
    """탄소 원자 루이스 전자점식 (점 4개 한 자리에 하나씩)"""
    s = f'<text class="tex" x="{f(x)}" y="{f(y + .36 * S)}" data-tex="\\mathrm{{C}}" data-size="{S}" data-anchor="middle"></text>'
    for dx, dy in ((0, -.75), (0, .75), (-.70, 0), (.70, 0)):
        s += f'<circle cx="{f(x + dx * S)}" cy="{f(y + dy * S)}" r="4" fill="{INK}"/>'
    return s


def axis_label(x, y, tex, size=19, anchor='middle', fill=MUTED, mix=True):
    k = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {k}="{tex}" data-size="{size}" data-anchor="{anchor}" fill="{fill}"></text>'
