# ── 교과서 대조 후 추가·교체 그림 ──
def unit2():
    cx, cy = 300, 165
    s = ''
    cards = [(110, 62, '밀가루', '녹말'), (490, 62, '달걀', '단백질'),
             (110, 268, '크림', '지방'), (490, 268, '종이 상자', '셀룰로스')]
    for x, y, t1, t2 in cards:
        s += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#9FB0C2" stroke-width="3" stroke-dasharray="6 5"/>'
    s += f'<g data-atom="{cx},{cy},40,C"></g>'
    for k, (x, y, t1, t2) in enumerate(cards):
        s += (f'<g data-anim="pop" data-o="{x},{y}" data-dur=".7" data-delay="{.3 + .2 * k:.1f}" data-ease="back">'
              f'<rect x="{x - 105}" y="{y - 44}" width="210" height="88" rx="14" fill="#fff" stroke="#C9D3DD" stroke-width="2"/>'
              + T(x, y - 8, f'<b>{t1}</b>', 22) + T(x, y + 28, t2, 20, fill=MUTED) + '</g>')
    return s
F['UNIT'] = unit2()

def skel2(pts, bonds, anim=True):
    o = '<g data-anim="draw" data-dur="1" data-on="step">' if anim else '<g>'
    for i, j, od in bonds:
        (x1, y1), (x2, y2) = pts[i], pts[j]
        dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy); px, py = -dy / n, dx / n
        offs = [0] if od == 1 else [-4.5, 4.5]
        w = 7 if od == 1 else 5
        o += ''.join(f'<line x1="{f(x1 + px * q)}" y1="{f(y1 + py * q)}" x2="{f(x2 + px * q)}" y2="{f(y2 + py * q)}" stroke="{BOND}" stroke-width="{w}" stroke-linecap="round"/>' for q in offs)
    o += '</g>' + ''.join(f'<g data-atom="{f(x)},{f(y)},20,C"></g>' for x, y in pts)
    return o

def s8b():
    s = ''
    S, d = 26, 54
    y = 100
    g = '<g class="step" data-g="k1">'
    a, bb, _ = chain(2, None, 180 - 1.5 * d, y, d, S)
    g += sf(a, bb, S)
    cx = 550; c1, c2 = cx - 34, cx + 34
    at = [('C', c1, y), ('C', c2, y)]
    for sx, c in ((-1, c1), (1, c2)):
        for sy in (-1, 1):
            at.append(('H', c + sx * 46, y + sy * 46))
    g += sf(at, [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], S)
    cx = 920
    at = [('H', cx - 120, y), ('C', cx - 40, y), ('C', cx + 40, y), ('H', cx + 120, y)]
    g += sf(at, [(0, 1, 1), (1, 2, 3), (2, 3, 1)], S)
    for x, t in ((180, '에테인 — 단일 결합'), (550, '에텐 — 이중 결합'), (920, '에타인 — 삼중 결합')):
        g += T(x, 190, t, 20, fill=MUTED)
    s += g + '</g>'
    y2 = 300
    g = '<g class="step" data-g="k2">'
    xs = [110 + 52 * k for k in range(5)]
    g += skel2([(x, y2 + (-14 if k % 2 else 14)) for k, x in enumerate(xs)], [(k, k + 1, 1) for k in range(4)])
    pts = [(420, y2 + 14), (472, y2 - 14), (524, y2 + 14), (576, y2 - 14), (472, y2 - 80)]
    g += skel2(pts, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (1, 4, 1)])
    xs = [660 + 52 * k for k in range(5)]
    g += skel2([(x, y2 + (-14 if k % 2 else 14)) for k, x in enumerate(xs)], [(0, 1, 2), (1, 2, 1), (2, 3, 1), (3, 4, 1)])
    pts = [(1000 + 50 * math.cos(math.radians(90 + 72 * k)), y2 - 20 - 50 * math.sin(math.radians(90 + 72 * k))) for k in range(5)]
    g += skel2(pts, [(k, (k + 1) % 5, 1) for k in range(5)])
    for x, t in ((214, '사슬'), (498, '가지 달린 사슬'), (764, '이중 결합이 있는 사슬'), (1000, '고리')):
        g += T(x, 378, t, 20, fill=MUTED)
    s += g + '</g>'
    return s
F['S8'] = s8b()

# 프로페인 분자식·구조식·모형
F['S9SF'] = center_chain(3, None, 260, 100, d=46, S=22)
a, b = mol_alkane_like(3)
F['S9BS'] = bs3d(a, b, 130, 104, k=40, yaw=0, pitch=-12, sc=.7)[0]
# 뷰테인 정답
F['S10'] = center_chain(4, None, 360, 95, d=54, S=24)
# 탄화수소 4카드
F['HC1'] = center_chain(1, None, 260, 85, d=46, S=22)
F['HC2'] = center_chain(3, None, 260, 85, d=46, S=22)
F['HC3'] = sf([('C', 100, 85), ('C', 160, 85), ('H', 66, 52), ('H', 66, 118), ('H', 194, 52), ('H', 194, 118)], [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], 22)
F['HC4'] = sf([('H', 50, 85), ('C', 105, 85), ('C', 160, 85), ('H', 215, 85)], [(0, 1, 1), (1, 2, 3), (2, 3, 1)], 22)
# 메테인 → 메탄올
F['S17A'] = center_chain(1, None, 260, 100, d=56, S=26)
def s17c():
    a, b, gb = chain(1, 'OH', 0, 0, 56, 26)
    w = chain_width(1, 'OH', 56); x0 = (300 - w) / 2; y0 = 100
    a = [(s, x + x0, y + y0) for s, x, y in a]
    gb = (gb[0] + x0, gb[1] + y0, gb[2], gb[3])
    oi = [i for i, (s, _, _) in enumerate(a) if s == 'O'][0]
    rest = [k for k in range(len(a)) if k not in (oi, oi + 1)]
    idx = {k: n for n, k in enumerate(rest)}
    core = sf([a[k] for k in rest], [(idx[i], idx[j], o) for i, j, o in b if i in idx and j in idx], 26)
    ci = [i for i, j, o in b if j == oi][0]
    cline = sf([a[ci], a[oi]], [(0, 1, 1)], 26); cline = cline[:cline.index('<text')]
    grp = box(*gb) + sf([a[oi], a[oi + 1]], [(0, 1, 1)], 26)
    return core + f'<g data-anim="move" data-from="40,-40" data-dur="1.1" data-delay=".5" data-ease="out">{cline}{grp}</g>' + T(gb[0] + gb[2] / 2, gb[1] + gb[3] + 24, '$\\ce{-OH}$', 19, fill=EQUI, weight=700)
F['S17B'] = s17c()
# 에탄올·1-프로판올 (작용기 같으면 비슷)
F['FG2'] = center_chain(2, 'OH', 300, 100, d=50, S=24, label='$\\ce{-OH}$', lab_size=18)
F['FG3'] = center_chain(3, 'OH', 330, 100, d=50, S=24, label='$\\ce{-OH}$', lab_size=18)
# 탐구 과정 1: 여섯 구조 (작용기 상자 단계)
for k, (key, n, fg) in enumerate((('Q1', 1, 'OH'), ('Q2', 2, 'CHO'), ('Q3', 2, 'OH'), ('Q4', 1, 'CHO'), ('Q5', 2, 'COOH'), ('Q6', 1, 'COOH'))):
    F['TQ' + key[1]] = center_chain(n, fg, 300, 88 if fg != 'OH' else 75, d=48, S=23, g=f'p{k + 1}')
# 에틸렌 글리콜·글리세롤
def polyol(n):
    S, d = 22, 54
    x0 = 30; y = 70
    at = [('H', x0, y)]; bd = []
    cs = []
    for k in range(n):
        at.append(('C', x0 + d * (k + 1), y)); ci = len(at) - 1; cs.append(ci)
        bd.append((ci - 1 if k == 0 else cs[k - 1], ci, 1))
        at.append(('H', x0 + d * (k + 1), y - d)); bd.append((ci, len(at) - 1, 1))
        at.append(('O', x0 + d * (k + 1), y + d)); oi = len(at) - 1; bd.append((ci, oi, 1))
        at.append(('H', x0 + d * (k + 1), y + 2 * d)); bd.append((oi, len(at) - 1, 1))
    at.append(('H', x0 + d * (n + 1), y)); bd.append((cs[-1], len(at) - 1, 1))
    s = ''
    for c in cs:
        x = at[c][1]
        s += box(x - 16, y + d - 16, 32, d + 32)
    return s + sf(at, bd, S)
F['PG2'] = polyol(2)
F['PG3'] = polyol(3)
# 폼산: -CHO(점선)와 -COOH(실선) 상자
def formic():
    a, b, gb = chain(1, 'COOH', 40, 100, 56, 26)
    cx = a[1][1]
    s = box(*gb)
    s += f'<rect x="{f(cx - 20)}" y="{f(100 - 56 - 20)}" width="40" height="{56 + 40 + 56 + 2}" rx="10" fill="none" stroke="#7B4FC8" stroke-width="2.5" stroke-dasharray="6 5" class="step" data-g="fa"/>'
    s += sf(a, b, 26)
    s += T(gb[0] + gb[2] / 2 + 30, 205, '$\\ce{-COOH}$', 19, fill=EQUI, weight=700)
    s += T(cx - 34, 205, '$\\ce{-CHO}$', 19, 'end', '#7B4FC8', 700, extra=' class="tex step" data-g="fa"').replace('class="tex" class="tex step"', 'class="tex step"')
    return s
F['FORMIC'] = formic()
# 대단원 마무리 03: (가) 메테인 (나) 에테인 (다) 아세트산 공-막대
def q03():
    s = ''
    for x, mol, lab in ((100, mol_methane(), '(가)'), (310, mol_alkane_like(2), '(나)'), (530, mol_alkane_like(2, 'COOH'), '(다)')):
        a, b = mol
        s += bs3d(a, b, x, 95, k=42, yaw=18, pitch=-14, sc=.72)[0]
        s += T(x, 196, lab, 20)
    return s
F['Q03'] = q03()
# 대단원 마무리 04: (가) 메탄올 (나) 아세트산 (다) 폼산 (라) 1-프로판올
for key, n, fg in (('Q4A', 1, 'OH'), ('Q4B', 2, 'COOH'), ('Q4C', 1, 'COOH'), ('Q4D', 3, 'OH')):
    F[key] = center_chain(n, fg, 300, 80 if fg == 'COOH' else 70, d=44, S=21)
