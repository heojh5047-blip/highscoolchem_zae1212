# 2-2-2 덱 그림 좌표 계산 도우미 (분자 모형·루이스 전자점식·쐐기 결합)
import math

R = {'H': 18, 'Be': 24, 'B': 24, 'C': 24, 'N': 24, 'O': 24, 'F': 24, 'Cl': 29, 'X': 24, 'Si': 29, 'P': 29, 'S': 29}
BOND = '#9AA5B1'
LOBE_F, LOBE_S = '#E08A2C', '#E08A2C'
INK = '#16233D'
MUTED = '#5B6B7F'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def norm(v):
    l = math.sqrt(sum(c * c for c in v))
    return tuple(c / l for c in v)


def rot(v, yaw, pitch):
    x, y, z = v
    a = math.radians(yaw)
    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    b = math.radians(pitch)
    y, z = y * math.cos(b) - z * math.sin(b), y * math.sin(b) + z * math.cos(b)
    return (x, y, z)


def angle_dirs(n_lone, n_bond, ang=None):
    """중심 원자 기준 (결합 방향들, 비공유 전자쌍 방향들) — y 위, x 오른쪽, z 앞"""
    if (n_bond, n_lone) == (2, 0):
        return [(-1, 0, 0), (1, 0, 0)], []
    if (n_bond, n_lone) == (3, 0):
        return [(math.cos(math.radians(a)), math.sin(math.radians(a)), 0) for a in (90, 210, 330)], []
    if (n_bond, n_lone) == (4, 0):
        r = math.sqrt(8) / 3
        return [(0, 1, 0)] + [(r * math.sin(math.radians(p)), -1 / 3, r * math.cos(math.radians(p))) for p in (0, 120, 240)], []
    if (n_bond, n_lone) == (3, 1):
        g = math.radians(ang or 107)
        c = (math.cos(g) + 0.5) / 1.5
        al = math.acos(math.sqrt(c))
        return [(math.sin(al) * math.sin(math.radians(p)), -math.cos(al), math.sin(al) * math.cos(math.radians(p))) for p in (0, 120, 240)], [(0, 1, 0)]
    if (n_bond, n_lone) == (2, 2):
        h = math.radians((ang or 104.5) / 2)
        return [(-math.sin(h), -math.cos(h), 0), (math.sin(h), -math.cos(h), 0)], [norm((0, 0.62, 0.78)), norm((0, 0.62, -0.78))]
    raise ValueError


def ballstick(cx, cy, center, outer, n_lone=0, ang=None, L=100, yaw=0, pitch=0, scale=1.0, arc=None, lobes=True,
              anim_out=None, labels=True, arc_label=None, arc_r=None, arc_g=None, arc_size=20, dirs=None, extra_bond_orders=None,
              lone_dirs=None, lobe_col=None, dots=True):
    """공-막대 모형 SVG. outer: 결합 원자 원소 목록. arc=(i,j) 결합각 호. anim_out: 바깥 원자가 중심에서 밀려 나오는 움직임"""
    if dirs is None:
        bd, ld = angle_dirs(n_lone, len(outer), ang)
    else:
        bd, ld = dirs, (lone_dirs or [])
    bd = [rot(norm(d), yaw, pitch) for d in bd]
    ld = [rot(norm(d), yaw, pitch) for d in ld]
    rc = R[center] * scale
    items = []  # (z, order, svg)
    P = lambda d, l: (cx + d[0] * l, cy - d[1] * l)
    for k, (el, d) in enumerate(zip(outer, bd)):
        l = L * scale * (0.82 if el == 'H' else 1.0)
        x, y = P(d, l)
        r = R[el] * scale
        order = (extra_bond_orders or {}).get(k, 1)
        bonds = ''
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy) or 1
        px, py = -dy / n, dx / n
        offs = {1: [0], 2: [-4.5, 4.5], 3: [-7, 0, 7]}[order]
        for o in offs:
            bonds += f'<line x1="{f(cx + px * o)}" y1="{f(cy + py * o)}" x2="{f(x + px * o)}" y2="{f(y + py * o)}" stroke="{BOND}" stroke-width="{7 if order == 1 else 5}" stroke-linecap="round"/>'
        lab = '' if labels else ',-'
        atom = f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{lab}"></g>'
        if anim_out:
            mv = f'{f(-dx * anim_out)},{f(-dy * anim_out)}'
            items.append((d[2] * 0.5, 0, f'<g data-anim="draw" data-dur=".9" data-delay=".3">{bonds}</g>' if False else bonds))
            items.append((d[2], 2, f'<g data-anim="move" data-from="{mv}" data-dur="1.2" data-delay=".3" data-ease="out">{atom}</g>'))
        else:
            items.append((d[2] * 0.5, 0, bonds))
            items.append((d[2], 2, atom))
    if lobes:
        for d in ld:
            ll = L * scale * 0.62
            ex, ey = d[0] * ll, -d[1] * ll
            pl = math.hypot(ex, ey)
            ang2 = math.degrees(math.atan2(ey, ex))
            ccx, ccy = cx + ex * 0.62, cy + ey * 0.62
            rx = max(pl * 0.62, 20 * scale)
            ry = 21 * scale
            # 점 두 개: 로브 바깥쪽 끝 근처, 방향에 수직
            ux, uy = (ex / pl, ey / pl) if pl > 1e-6 else (1, 0)
            tip = 0.85 if pl > 8 else 0
            dxp, dyp = -uy * 6 * scale, ux * 6 * scale
            bx, by = cx + ex * tip, cy + ey * tip
            lc = lobe_col or LOBE_F
            svg = (f'<ellipse cx="{f(ccx)}" cy="{f(ccy)}" rx="{f(rx)}" ry="{f(ry)}" transform="rotate({f(ang2)} {f(ccx)} {f(ccy)})" '
                   f'fill="{lc}" fill-opacity=".18" stroke="{lc}" stroke-width="1.5"/>')
            if dots: svg += (f'<circle cx="{f(bx + dxp)}" cy="{f(by + dyp)}" r="{f(3.6 * scale + .4)}" fill="{INK}"/><circle cx="{f(bx - dxp)}" cy="{f(by - dyp)}" r="{f(3.6 * scale + .4)}" fill="{INK}"/>')
            items.append((d[2] * 0.6, 1, svg))
    items.append((0.61, 3, f'<g data-atom="{f(cx)},{f(cy)},{f(rc)},{center}{"" if labels else ",-"}"></g>'))
    items.sort(key=lambda t: (t[0] + (0.001 * t[1])))
    out = ''.join(s for _, _, s in items)
    if arc:
        aps = [P(d, L * scale * (0.82 if el == 'H' else 1.0)) for el, d in zip(outer, bd)] + [(cx, cy)]
        def lab_pos(i, j):
            a, b = bd[i], bd[j]
            m = norm(tuple(p + q for p, q in zip(a, b))) if abs(sum(p * q for p, q in zip(a, b)) + 1) > 1e-3 else (0, 1, 0)
            ra = arc_r or (L * scale * 0.42)
            x, y = P(m, ra)
            vx, vy = x - cx, y - cy
            n = math.hypot(vx, vy) or 1
            return cx + vx / n * (n + 26), cy + vy / n * (n + 26)
        if arc == 'auto':
            pairs = [(i, j) for i in range(len(outer)) for j in range(i + 1, len(outer))]
            def score(pr):
                x, y = lab_pos(*pr)
                return min(math.hypot(x - px, y - py) - (R[outer[k]] * scale if k < len(outer) else rc) for k, (px, py) in enumerate(aps))
            arc = max(pairs, key=score)
        i, j = arc
        a, b = bd[i], bd[j]
        ra = arc_r or (L * scale * 0.42)
        dot = max(-1, min(1, sum(p * q for p, q in zip(a, b))))
        om = math.acos(dot)
        pts = []
        for t in [k / 24 for k in range(25)]:
            if om < 1e-6:
                v = a
            elif abs(om - math.pi) < 1e-3:
                # 180°: 화면 위쪽(보는 쪽)으로 도는 반원
                perp = (0, 1, 0) if abs(a[1]) < .9 else (1, 0, 0)
                th = math.pi * t
                v = tuple(a[k] * math.cos(th) + perp[k] * math.sin(th) for k in range(3))
            else:
                s1 = math.sin((1 - t) * om) / math.sin(om)
                s2 = math.sin(t * om) / math.sin(om)
                v = tuple(s1 * a[k] + s2 * b[k] for k in range(3))
            pts.append(P(v, ra))
        d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
        mid = pts[12]
        vx, vy = mid[0] - cx, mid[1] - cy
        n = math.hypot(vx, vy) or 1
        lx, ly = cx + vx / n * (n + 26), cy + vy / n * (n + 26) + arc_size * 0.36
        g = f' class="step" data-g="{arc_g}"' if arc_g else ''
        out += (f'<g{g}><path d="{d}" fill="none" stroke="{MUTED}" stroke-width="2" data-anim="draw" data-dur=".8" data-delay="1.2"/>'
                f'<text class="tex" x="{f(lx)}" y="{f(ly)}" data-tex="{arc_label}" data-size="{arc_size}" data-anchor="middle" data-halo="1"></text></g>')
    return out


def lewis_sym(x, y, el, S=40, color=None, dots=None):
    """원소 기호(중심 x,y)와 전자점. dots = {'u':n,'d':n,'l':n,'r':n}"""
    fill = f' fill="{color}"' if color else ''
    s = f'<text class="tex" x="{f(x)}" y="{f(y + 0.36 * S)}" data-tex="\\mathrm{{{el}}}" data-size="{S}" data-anchor="middle"{fill}></text>'
    for side, n in (dots or {}).items():
        s += dot_pair(*side_pos(x, y, side, S), 'h' if side in 'ud' else 'v', n, S)
    return s


def side_pos(x, y, side, S):
    return {'u': (x, y - 0.75 * S), 'd': (x, y + 0.75 * S), 'l': (x - 0.70 * S, y), 'r': (x + 0.70 * S, y)}[side]


def dot_pair(x, y, orient, n=2, S=40, r=4):
    if n == 1:
        return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{INK}"/>'
    o = 0.18 * S
    if orient == 'h':
        return f'<circle cx="{f(x - o)}" cy="{f(y)}" r="{r}" fill="{INK}"/><circle cx="{f(x + o)}" cy="{f(y)}" r="{r}" fill="{INK}"/>'
    return f'<circle cx="{f(x)}" cy="{f(y - o)}" r="{r}" fill="{INK}"/><circle cx="{f(x)}" cy="{f(y + o)}" r="{r}" fill="{INK}"/>'


def hl_box(x, y, w, h, kind, g=None):
    col = '#2E9E6A' if kind == 'shared' else '#E08A2C'
    cls = f' class="step" data-g="{g}"' if g else ''
    return f'<rect{cls} x="{f(x - w / 2)}" y="{f(y - h / 2)}" width="{f(w)}" height="{f(h)}" rx="8" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="1.5"/>'


def wedge(cx, cy, center, bonds, lone=(), L=96, S=30, lone_len=44):
    """쐐기 결합 구조식. bonds = [(각도°(화면, 0=오른쪽, 반시계 +), 'l'|'w'|'d', 원소)], lone=[각도]"""
    out = ''
    for a, kind, el in bonds:
        t = math.radians(a)
        ux, uy = math.cos(t), -math.sin(t)
        x1, y1 = cx + ux * 18, cy + uy * 18
        ex, ey = cx + ux * L, cy + uy * L
        x2, y2 = cx + ux * (L - 18), cy + uy * (L - 18)
        px, py = -uy, ux
        if kind == 'l':
            out += f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
        elif kind == 'w':
            out += f'<polygon points="{f(x1)},{f(y1)} {f(x2 + px * 7)},{f(y2 + py * 7)} {f(x2 - px * 7)},{f(y2 - py * 7)}" fill="{INK}"/>'
        else:
            n = 7
            for k in range(1, n + 1):
                tt = k / n
                mx, my = x1 + (x2 - x1) * tt, y1 + (y2 - y1) * tt
                w = 7 * tt
                out += f'<line x1="{f(mx + px * w)}" y1="{f(my + py * w)}" x2="{f(mx - px * w)}" y2="{f(my - py * w)}" stroke="{INK}" stroke-width="2.2"/>'
        out += f'<text class="tex" x="{f(ex)}" y="{f(ey + 0.36 * S)}" data-tex="\\mathrm{{{el}}}" data-size="{S}" data-anchor="middle"></text>'
    for a in lone:
        t = math.radians(a)
        ux, uy = math.cos(t), -math.sin(t)
        ccx, ccy = cx + ux * (lone_len * 0.75), cy + uy * (lone_len * 0.75)
        out += (f'<ellipse cx="{f(ccx)}" cy="{f(ccy)}" rx="{f(lone_len * 0.55)}" ry="15" transform="rotate({f(-a)} {f(ccx)} {f(ccy)})" fill="{LOBE_F}" fill-opacity=".18" stroke="{LOBE_S}" stroke-width="1.5"/>')
        bx, by = cx + ux * lone_len, cy + uy * lone_len
        out += dot_pair(bx, by, 'h' if abs(uy) > abs(ux) else 'v', 2, 30, 3.6) if abs(ux) < .2 or abs(uy) < .2 else \
            f'<circle cx="{f(bx - uy * 5.4)}" cy="{f(by + ux * 5.4)}" r="3.6" fill="{INK}"/><circle cx="{f(bx + uy * 5.4)}" cy="{f(by - ux * 5.4)}" r="3.6" fill="{INK}"/>'
    out += f'<text class="tex" x="{f(cx)}" y="{f(cy + 0.36 * S)}" data-tex="\\mathrm{{{center}}}" data-size="{S}" data-anchor="middle"></text>'
    return out
