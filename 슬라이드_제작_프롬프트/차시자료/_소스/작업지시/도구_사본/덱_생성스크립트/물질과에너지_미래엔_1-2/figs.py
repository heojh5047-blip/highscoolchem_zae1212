# 1-2 덱 그림 도우미 — slides.tpl.html 의 [[이름]] 을 그림 문자열로 바꾼다
import random, math

GLASS = '#7E8B98'
def T(x, y, mix, size=20, anchor='middle', weight=None, fill=None, halo=False, tex=False, extra=''):
    a = f'<text class="tex" x="{x}" y="{y}" '
    a += (f'data-tex="{mix}" ' if tex else f'data-mix="{mix}" ')
    a += f'data-size="{size}" data-anchor="{anchor}"'
    if weight: a += f' data-weight="{weight}"'
    if halo: a += ' data-halo="1"'
    if fill: a += f' fill="{fill}"'
    return a + extra + '></text>'

def place(n, x, y, w, h, seed, rmin=34, avoid=()):
    rnd = random.Random(seed); pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        px = x + 22 + rnd.random() * (w - 44); py = y + 22 + rnd.random() * (h - 44)
        if all((px - a) ** 2 + (py - b) ** 2 > rmin ** 2 for a, b in pts + list(avoid)):
            pts.append((px, py))
    return pts

def diatomic(cx, cy, el, seed, r=12, d=''):
    rnd = random.Random(seed * 7 + int(cx * 13 + cy))
    a = rnd.random() * math.pi
    dx, dy = math.cos(a) * r * 0.68, math.sin(a) * r * 0.68
    s = f',d' if d else ''
    return (f'<g data-atom="{cx-dx:.1f},{cy-dy:.1f},{r},{el},-{s}"></g>'
            f'<g data-atom="{cx+dx:.1f},{cy+dy:.1f},{r},{el},-{s}"></g>')

def simple(cx, cy, kind, r=11, d=''):
    if kind == 'A': f, s = '#F2C230', '#B8901A'
    elif kind == 'B': f, s = '#6C8EBF', '#3E5F8F'
    elif kind == 'He': return f'<g data-atom="{cx:.1f},{cy:.1f},9,He,-{",d" if d else ""}"></g>'
    else: f, s = '#C9D3DD', '#7E8B98'
    dash = ' stroke-dasharray="4 3" fill-opacity=".25"' if d else ''
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{f}" stroke="{s}" stroke-width="1.5"{dash}/>'

def mol(kind, cx, cy, seed=1, d=''):
    if kind in ('O', 'N'): return diatomic(cx, cy, kind, seed, d=d)
    return simple(cx, cy, kind, d=d)

def swing_groups(items, seed, amp=3.0):
    """items: list of svg strings -> two swing groups"""
    if not items: return ''
    a, b = items[0::2], items[1::2]
    rnd = random.Random(seed)
    g1 = f'<g data-anim="move" data-from="{amp:.1f},{-amp*0.6:.1f}" data-rep="swing" data-dur="{0.55+rnd.random()*0.2:.2f}">' + ''.join(a) + '</g>'
    g2 = (f'<g data-anim="move" data-from="{-amp*0.7:.1f},{amp*0.8:.1f}" data-rep="swing" data-dur="{0.65+rnd.random()*0.2:.2f}">' + ''.join(b) + '</g>') if b else ''
    return g1 + g2

def box(x, y, w, h, fill='#F4F8FB'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{GLASS}" stroke-width="3"/>'
            f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2-6}" ry="8" fill="#E6EDF3" stroke="{GLASS}" stroke-width="2"/>')

def gauge(cx, cy, val, vmax, label, r=24, side_x=None, side_y=None):
    a0, a1 = math.pi * 0.8, math.pi * 2.2
    ang = a0 + (a1 - a0) * min(max(val / vmax, 0), 1) if val is not None else a0 + (a1 - a0) * 0.5
    s = ''
    if side_x is not None:
        s += f'<path d="M{side_x} {side_y} H{cx-r}" stroke="{GLASS}" stroke-width="5"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>'
    for k in range(5):
        a = a0 + (a1 - a0) * k / 4
        s += f'<line x1="{cx+(r-7)*math.cos(a):.1f}" y1="{cy+(r-7)*math.sin(a):.1f}" x2="{cx+r*math.cos(a):.1f}" y2="{cy+r*math.sin(a):.1f}" stroke="#5B6B7F" stroke-width="1.5"/>'
    if val is None:
        s += T(cx, cy + 8, '?', 24, weight=700, fill='#D7263D')
    else:
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx+(r-6)*math.cos(ang):.1f}" y2="{cy+(r-6)*math.sin(ang):.1f}" stroke="#D7263D" stroke-width="3" stroke-linecap="round"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#16233D"/>'
    s += T(cx, cy - r - 10, label, 20, weight=700)
    return s

def legend(x, y, items, size=19, gap=150):
    s = ''
    for i, (kind, lab) in enumerate(items):
        xx = x + i * gap
        if kind in ('O', 'N'):
            s += diatomic(xx, y - 6, kind, 1, r=10).replace(f'{kind},-', f'{kind},-')
            # 범례는 가로로 고정
            s = s[:s.rfind('<g data-atom')] if False else s
        else:
            s += simple(xx, y - 6, kind, r=9)
        s += T(xx + 22, y, lab, size, anchor='start')
    return s

def leg_mol(x, y, kind, lab, size=19):
    if kind in ('O', 'N'):
        m = f'<g data-atom="{x-7},{y-6},10,{kind},-"></g><g data-atom="{x+7},{y-6},10,{kind},-"></g>'
        return m + T(x + 24, y, lab, size, anchor='start')
    return simple(x, y - 6, kind, r=9) + T(x + 22, y, lab, size, anchor='start')

# ───────── 그림들 ─────────
FIG = {}

# S1 표지
def cover():
    s = '<svg class="cover-fig" viewBox="0 0 540 540" aria-label="둥근 용기 속에 산소 분자 4개와 질소 분자 6개가 섞여 움직이고 압력계가 전체 압력을 나타내는 모습" data-audit="skip">'
    s += '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    s += f'<circle cx="250" cy="290" r="170" fill="#F8FBFD" stroke="{GLASS}" stroke-width="4"/>'
    s += f'<rect x="228" y="96" width="44" height="40" rx="4" fill="#E6EDF3" stroke="{GLASS}" stroke-width="3"/>'
    pts = place(10, 120, 160, 260, 260, 11, rmin=56)
    pts = [p for p in pts if (p[0]-250)**2 + (p[1]-290)**2 < 140**2]
    rnd = random.Random(3)
    while len(pts) < 10:
        a = rnd.random()*6.283; rr = rnd.random()*130
        p = (250+rr*math.cos(a), 290+rr*math.sin(a))
        if all((p[0]-q[0])**2+(p[1]-q[1])**2 > 50**2 for q in pts): pts.append(p)
    items = [mol('O' if i < 4 else 'N', x, y, i) for i, (x, y) in enumerate(pts)]
    s += swing_groups(items, 2, 4)
    s += f'<path d="M420 290 H450" stroke="{GLASS}" stroke-width="6"/>'
    s += gauge(482, 290, 5, 8, '', r=34)
    s += leg_mol(150, 505, 'O', '산소', 22) + leg_mol(300, 505, 'N', '질소', 22)
    return s + '</svg>'
FIG['COVER'] = cover

# S2 다시 보기 — 같은 용기, 분자 3개 / 6개
def s2():
    s = '<svg class="fig" viewBox="0 0 560 300" style="width:540px" aria-label="온도와 부피가 같은 두 용기에 기체 분자가 3개와 6개 들어 있고 압력이 1 기압과 2 기압인 모습">'
    for i, (n, lab) in enumerate([(3, '1 기압'), (6, '2 기압')]):
        x = 20 + i * 280
        s += box(x, 50, 190, 190)
        pts = place(n, x, 56, 190, 180, 20 + i, rmin=44)
        s += swing_groups([simple(px, py, 'B') for px, py in pts], 5 + i)
        s += gauge(x + 232, 180, n / 3, 3, lab, side_x=x + 190, side_y=180)
        s += T(x + 95, 280, ['(가) 기체 1 mol', '(나) 기체 2 mol'][i], 21, weight=700)
    return s + '</svg>'
FIG['S2'] = s2

# S5 / S6 / S8 — 해 보기 그림
RNDP = None
def haebogi_points():
    # (가) O2 4, (나) N2 6 : 같은 상자 좌표계(0..200, 0..220)에서 겹치지 않게 함께 배치
    pts = place(10, 0, 0, 200, 220, 41, rmin=46)
    return pts[:4], pts[4:]
PO, PN = haebogi_points()

def three_boxes(mode):
    W = 880
    s = f'<svg class="fig" viewBox="0 0 {W} 320" style="width:{W}px" aria-label="일정한 온도에서 부피가 같은 세 용기: (가) 산소 분자 4개 2 기압, (나) 질소 분자 6개 3 기압, (다) 산소와 질소의 혼합 기체">'
    xs = [10, 310, 610]; y0 = 40
    labs = ['(가) $\\ce{O2}$ 기체', '(나) $\\ce{N2}$ 기체', '(다) $\\ce{O2}$와 $\\ce{N2}$의 혼합 기체']
    gv = [(2, '2 기압'), (3, '3 기압'), (None if mode == 'q' else 5, '? 기압' if mode == 'q' else '5 기압')]
    for i, x in enumerate(xs):
        s += box(x, y0, 200, 220)
        g, lab = gv[i]
        s += gauge(x + 238, y0 + 160, g, 6, lab, side_x=x + 200, side_y=y0 + 160)
        s += T(x + 110, 300, labs[i], 21, weight=700)
    d = 'd' if mode == 'move' else ''
    s += swing_groups([mol('O', xs[0] + px, y0 + py, j, d=d) for j, (px, py) in enumerate(PO)], 1) if not d else ''.join(mol('O', xs[0] + px, y0 + py, j, d=d) for j, (px, py) in enumerate(PO))
    s += swing_groups([mol('N', xs[1] + px, y0 + py, j, d=d) for j, (px, py) in enumerate(PN)], 2) if not d else ''.join(mol('N', xs[1] + px, y0 + py, j, d=d) for j, (px, py) in enumerate(PN))
    if mode == 'move':
        s += '<g data-anim="move" data-from="-600,0" data-dur="1.6" data-delay=".3" data-ease="io">' + ''.join(mol('O', xs[2] + px, y0 + py, j) for j, (px, py) in enumerate(PO)) + '</g>'
        s += '<g data-anim="move" data-from="-300,0" data-dur="1.6" data-delay=".3" data-ease="io">' + ''.join(mol('N', xs[2] + px, y0 + py, j) for j, (px, py) in enumerate(PN)) + '</g>'
    elif mode == 'q':
        s += swing_groups([mol('O', xs[2] + px, y0 + py, j) for j, (px, py) in enumerate(PO)] + [mol('N', xs[2] + px, y0 + py, j) for j, (px, py) in enumerate(PN)], 3)
    return s + '</svg>'
FIG['S5'] = lambda: three_boxes('q')
FIG['S6'] = lambda: three_boxes('move')

def s8():
    s = '<svg class="fig" viewBox="0 0 900 312" style="width:880px" aria-label="5 기압인 산소와 질소의 혼합 기체는 같은 용기에 산소만 있을 때의 2 기압과 질소만 있을 때의 3 기압으로 나누어 볼 수 있다">'
    xs = [10, 330, 640]; y0 = 30
    vals = [(5, '$P=5$ 기압'), (2, '$P_{\\ce{O2}}=2$ 기압'), (3, '$P_{\\ce{N2}}=3$ 기압')]
    labs = ['혼합 기체', '산소만 있다면', '질소만 있다면']
    for i, x in enumerate(xs):
        s += box(x, y0, 190, 210)
        s += f'<path d="M{x+190} {y0+150} H{x+208}" stroke="{GLASS}" stroke-width="5"/>'
        s += ('' if i == 0 else '<g class="step" data-g="b1">') + gauge(x + 232, y0 + 150, vals[i][0], 6, '') + ('' if i == 0 else '</g>')
        s += T(x + 95, 272, labs[i], 21, weight=700)
        s += T(x + 150, y0 + 104, vals[i][1], 21, weight=700, halo=True) if False else ''
    sc = 190 / 200
    s += swing_groups([mol('O', xs[0] + px * sc, y0 + py * 210 / 220, j) for j, (px, py) in enumerate(PO)] + [mol('N', xs[0] + px * sc, y0 + py * 210 / 220, j) for j, (px, py) in enumerate(PN)], 4)
    s += '<g class="step" data-g="b1">' + swing_groups([mol('O', xs[1] + px * sc, y0 + py * 210 / 220, j) for j, (px, py) in enumerate(PO)], 5) + '</g>'
    s += '<g class="step" data-g="b1">' + swing_groups([mol('N', xs[2] + px * sc, y0 + py * 210 / 220, j) for j, (px, py) in enumerate(PN)], 6) + '</g>'
    # 압력 라벨(게이지 위)
    for i, x in enumerate(xs):
        cls = '' if i == 0 else ' class="step" data-g="b1"'
        s += f'<g{cls}>' + T(x + 95, 302, vals[i][1], 20, fill='#5B6B7F') + '</g>'
    s += T(295, 150, '=', 40, weight=700) + T(610, 150, '+', 40, weight=700)
    return s + '</svg>'
FIG['S8'] = s8

# S10 그림 I-9
def s10():
    s = '<svg class="fig" viewBox="0 0 1100 300" style="width:1100px" aria-label="부피 V인 두 용기에 기체 A와 기체 B가 꼭지로 분리되어 있다가, 꼭지를 열고 피스톤을 눌러 기체 B를 모두 A 쪽 용기로 밀어 넣으면 부피 V 안에 혼합 기체가 된다">'
    rnd = random.Random(9)
    pa = place(4, 0, 0, 170, 180, 61, rmin=38)
    pb = place(6, 0, 0, 170, 180, 62, rmin=38, avoid=pa)
    # 전
    s += box(20, 60, 170, 180) + box(260, 60, 170, 180)
    s += f'<path d="M190 205 H260" stroke="{GLASS}" stroke-width="8"/><rect x="215" y="196" width="20" height="18" rx="3" fill="#16233D"/>'
    s += T(225, 186, '닫힘', 19)
    s += f'<rect x="266" y="74" width="158" height="12" rx="3" fill="#B7C2CE" stroke="{GLASS}" stroke-width="2"/><path d="M345 74 V40" stroke="{GLASS}" stroke-width="6"/>'
    s += swing_groups([simple(20 + x, 60 + y, 'A') for x, y in pa], 7)
    s += swing_groups([simple(260 + x, 60 + y, 'B') for x, y in pb], 8)
    s += T(105, 268, '기체 $\\mathrm{A}$', 20, weight=700) + T(105, 293, '$n_\\mathrm{A}$ mol, $V$ L', 20)
    s += T(345, 268, '기체 $\\mathrm{B}$', 20, weight=700) + T(345, 293, '$n_\\mathrm{B}$ mol, $V$ L', 20)
    s += '<g data-arw="470,150,580,150,ink,4"></g>' + T(525, 130, '피스톤 누름', 20)
    # 후
    X = 620
    s += box(X, 60, 170, 180) + box(X + 240, 60, 170, 180)
    s += f'<path d="M{X+170} 205 H{X+240}" stroke="{GLASS}" stroke-width="8"/><rect x="{X+195}" y="196" width="20" height="18" rx="3" fill="#fff" stroke="#16233D" stroke-width="2"/>'
    s += T(X + 205, 186, '열림', 19)
    s += f'<g data-anim="move" data-from="0,-152" data-dur="1.4" data-delay=".4" data-ease="io"><rect x="{X+246}" y="226" width="158" height="12" rx="3" fill="#B7C2CE" stroke="{GLASS}" stroke-width="2"/><path d="M{X+325} 226 V40" stroke="{GLASS}" stroke-width="6"/></g>'
    s += swing_groups([simple(X + x, 60 + y, 'A') for x, y in pa], 9)
    s += '<g data-anim="move" data-from="240,0" data-dur="1.4" data-delay=".4" data-ease="io">' + ''.join(simple(X + x, 60 + y, 'B') for x, y in pb) + '</g>'
    s += T(X + 85, 268, '혼합 기체', 20, weight=700) + T(X + 85, 293, '$(n_\\mathrm{A}+n_\\mathrm{B})$ mol, $V$ L', 20)
    s += gauge(X + 85, 22, None, 1, '', r=0) if False else ''
    return s + '</svg>'
FIG['S10'] = s10

# S13 막대
def s13():
    s = '<svg class="fig" viewBox="0 0 470 330" style="width:450px" aria-label="전체 압력 5 기압 막대가 산소 부분 압력 2 기압과 질소 부분 압력 3 기압으로 나뉜 모습, 몰분율 0.4와 0.6">'
    base = 280; u = 46
    s += f'<line x1="60" y1="{base}" x2="440" y2="{base}" stroke="#5B6B7F" stroke-width="2"/>'
    # 전체
    s += f'<g data-anim="scale" data-from="1,0" data-o="140,{base}" data-dur="1.2"><rect x="100" y="{base-2*u}" width="80" height="{2*u}" fill="#F7C9C1" stroke="#E5533D" stroke-width="2"/><rect x="100" y="{base-5*u}" width="80" height="{3*u}" fill="#C9D3F3" stroke="#4F6BD8" stroke-width="2"/></g>'
    s += T(140, base - u + 7, '$P_{\\ce{O2}}=2$', 20, halo=True) + T(140, base - 3.5 * u + 7, '$P_{\\ce{N2}}=3$', 20, halo=True)
    s += T(140, base + 30, '전체 $P=5$ 기압', 20, weight=700)
    # 분자 수
    s += T(330, 60, '분자 수', 20, weight=700)
    s += leg_mol(270, 110, 'O', '4개 → $X=0.4$', 20) + leg_mol(270, 160, 'N', '6개 → $X=0.6$', 20)
    s += T(330, 220, '합 $=1$', 21, weight=700)
    return s + '</svg>'
FIG['S13'] = s13

# S16 공기 조성 막대
def s16():
    s = '<svg class="fig" viewBox="0 0 1100 150" style="width:1100px" aria-label="공기를 구성하는 기체의 조성(부피비): 질소 78.08 %, 산소 20.95 %, 아르곤 0.93 %, 이산화 탄소 0.04 %">'
    x0, W = 20, 1000; y = 30; h = 56
    parts = [('질소 78.08 %', 78.08, '#C9D3F3', '#4F6BD8'), ('산소 20.95 %', 20.95, '#F7C9C1', '#E5533D'), ('', 0.93, '#D9EEF5', '#5B6B7F'), ('', 0.04, '#3A3F47', '#3A3F47')]
    s += f'<g data-anim="scale" data-from="0,1" data-o="{x0},{y}" data-dur="1.4">'
    x = x0
    for lab, v, f, st in parts:
        w = W * v / 100
        s += f'<rect x="{x:.1f}" y="{y}" width="{max(w,1.5):.1f}" height="{h}" fill="{f}" stroke="{st}" stroke-width="1.5"/>'
        x += w
    s += '</g>'
    s += T(x0 + W * 0.39, y + 36, '질소($\\ce{N2}$) 78.08 %', 22, weight=700)
    s += T(x0 + W * (0.7808 + 0.105), y + 36, '산소($\\ce{O2}$) 20.95 %', 21, weight=700)
    s += f'<path d="M{x0+W*0.995:.0f} {y+h} V{y+h+22} H{x0+W*0.80:.0f}" fill="none" stroke="#5B6B7F" stroke-width="1.5"/>'
    s += T(x0 + W * 0.79, y + h + 30, '아르곤($\\ce{Ar}$) 0.93 %, 이산화 탄소($\\ce{CO2}$) 0.04 %', 19, anchor='end', fill='#5B6B7F')
    s += T(1080, 140, '(자료: 미국항공우주국)', 19, anchor='end', fill='#5B6B7F')
    return s + '</svg>'
FIG['S16'] = s16

# S17 고기 포장 / 마취 가스
def s17a():
    s = '<svg class="fig" viewBox="0 0 320 210" style="width:300px" aria-label="고기 포장 용기 안에 산소와 이산화 탄소가 섞여 있는 모습">'
    s += '<path d="M20 120 L40 190 H280 L300 120 Z" fill="#fff" stroke="#7E8B98" stroke-width="3"/>'
    s += '<path d="M24 120 Q160 40 296 120" fill="#F4F8FB" stroke="#7E8B98" stroke-width="2.5"/>'
    s += '<path d="M70 165 Q90 130 150 140 Q220 128 250 160 Q230 182 150 180 Q90 184 70 165 Z" fill="#C8463C" stroke="#8E2A22" stroke-width="2"/>'
    s += '<path d="M110 160 Q150 150 200 162" fill="none" stroke="#F2D6CF" stroke-width="5"/>'
    items = []
    for i, (x, y) in enumerate([(90, 108), (150, 92), (210, 104)]):
        items.append(diatomic(x, y, 'O', i, r=10))
    s += swing_groups(items, 3, 2)
    for x, y in [(120, 112), (182, 112), (240, 116)]:
        s += f'<g data-atom="{x-15},{y},9,O,-"></g><g data-atom="{x},{y},11,C,-"></g><g data-atom="{x+15},{y},9,O,-"></g>'
    return s + '</svg>'
FIG['S17A'] = s17a

def s17b():
    s = '<svg class="fig" viewBox="0 0 300 210" style="width:280px" aria-label="일산화 이질소 통과 산소 통에서 나온 기체가 섞여 마취용 마스크로 가는 모습">'
    for i, (x, lab, f) in enumerate([(40, '\\ce{N2O}', '#C9D3DD'), (110, '\\ce{O2}', '#F7C9C1')]):
        s += f'<rect x="{x}" y="70" width="50" height="120" rx="20" fill="{f}" stroke="#7E8B98" stroke-width="2.5"/><rect x="{x+17}" y="52" width="16" height="20" fill="#7E8B98"/>'
        s += T(x + 25, 140, lab, 20, tex=True)
    s += '<path d="M65 52 V30 H200 M135 52 V30" fill="none" stroke="#7E8B98" stroke-width="4"/>'
    s += '<path d="M200 30 Q240 30 240 80 V110" fill="none" stroke="#7E8B98" stroke-width="4" stroke-dasharray="8 6" data-anim="dash" data-speed="30" data-flow="1"/>'
    s += '<path d="M240 30 Q240 30 240 30" fill="none"/>'
    s += '<path d="M210 110 Q240 160 270 110 Z" fill="#E3EEFB" stroke="#7E8B98" stroke-width="2.5"/>'
    s += T(240, 196, '마스크', 19)
    return s + '</svg>'
FIG['S17B'] = s17b

# S4 생각 열기
def s4():
    s = '<svg class="fig" viewBox="0 0 470 300" style="width:450px" aria-label="살충제 통과 이산화 탄소 통에서 나온 기체가 섞여 과일 상자가 든 훈증실로 들어가는 모습">'
    for i, (x, lab, f) in enumerate([(20, '살충제', '#E8E1C9'), (100, '$\\ce{CO2}$', '#C9D3DD')]):
        s += f'<rect x="{x}" y="120" width="56" height="140" rx="22" fill="{f}" stroke="#7E8B98" stroke-width="2.5"/><rect x="{x+20}" y="100" width="16" height="22" fill="#7E8B98"/>'
        s += T(x + 28, 290, lab, 20, weight=700)
    s += '<path d="M48 100 V70 H200 M128 100 V70" fill="none" stroke="#7E8B98" stroke-width="5"/>'
    s += '<path d="M200 70 H232" stroke="#7E8B98" stroke-width="5" stroke-dasharray="9 6" data-anim="dash" data-speed="40" data-flow="1"/>'
    s += '<rect x="232" y="40" width="220" height="220" rx="10" fill="#F4F8FB" stroke="#7E8B98" stroke-width="3"/>'
    s += T(342, 290, '훈증실', 20, weight=700)
    for bx, by in [(256, 180), (346, 180), (300, 120)]:
        s += f'<rect x="{bx}" y="{by}" width="84" height="60" fill="#E7C9A0" stroke="#A8865A" stroke-width="2"/>'
        for k in range(3):
            s += f'<circle cx="{bx+18+k*24}" cy="{by+14}" r="11" fill="#F29A2E" stroke="#C26E12" stroke-width="1.5"/>'
    items = [simple(x, y, 'G', r=6) for x, y in [(260, 70), (300, 92), (360, 66), (410, 96), (430, 150), (250, 140)]]
    s += swing_groups(items, 4, 3)
    return s + '</svg>'
FIG['S4'] = s4

# S9 막대 P = PA + PB
def s9():
    s = '<svg class="fig" viewBox="0 0 400 300" style="width:380px" aria-label="부피와 온도가 일정한 용기에 기체 A만 있을 때의 압력 막대에 기체 B를 더 넣으면 늘어난 양만큼 압력 막대가 높아진다">'
    base = 250; u = 40
    s += f'<line x1="30" y1="{base}" x2="380" y2="{base}" stroke="#5B6B7F" stroke-width="2"/>'
    s += f'<rect x="70" y="{base-2*u}" width="80" height="{2*u}" fill="#FBEBB5" stroke="#B8901A" stroke-width="2"/>'
    s += T(110, base - u + 7, '$P_\\mathrm{A}$', 22)
    s += T(110, base + 30, '$\\mathrm{A}$만', 20)
    s += f'<rect x="240" y="{base-2*u}" width="80" height="{2*u}" fill="#FBEBB5" stroke="#B8901A" stroke-width="2"/>'
    s += f'<g data-anim="scale" data-from="1,0" data-o="280,{base-2*u}" data-dur="1.2" data-delay=".5"><rect x="240" y="{base-5*u}" width="80" height="{3*u}" fill="#D6E2F2" stroke="#3E5F8F" stroke-width="2"/></g>'
    s += T(280, base - u + 7, '$P_\\mathrm{A}$', 22) + T(280, base - 3.5 * u + 7, '$P_\\mathrm{B}$', 22)
    s += T(280, base + 30, '$\\mathrm{B}$를 더 넣음', 20)
    s += f'<path d="M340 {base} V{base-5*u}" stroke="#5B6B7F" stroke-width="1.5"/><path d="M334 {base-5*u} H346 M334 {base} H346" stroke="#5B6B7F" stroke-width="1.5"/>'
    s += T(356, base - 2.5 * u + 7, '$P$', 24, anchor='start', weight=700)
    s += '<g data-arw="165,170,225,170,muted,2.5"></g>'
    return s + '</svg>'
FIG['S9'] = s9

# S18 잠수부
def s18():
    s = '<svg class="fig" viewBox="0 0 380 400" style="width:340px" aria-label="수면에서 깊이 내려갈수록 압력이 커지는 바닷속에서 공기통을 멘 잠수부와 위로 올라가는 기포">'
    s += '<rect x="10" y="40" width="360" height="350" fill="#DDEEF8" stroke="#9FC3DD" stroke-width="2"/>'
    s += '<path d="M10 40 Q55 30 100 40 T190 40 T280 40 T370 40" fill="none" stroke="#9FC3DD" stroke-width="3"/>'
    s += T(60, 30, '수면', 19, anchor='start')
    for i, d in enumerate([0, 10, 20, 30]):
        y = 40 + i * 110 if i < 3 else 370
        y = [40, 150, 260, 370][i]
        s += f'<line x1="10" y1="{y}" x2="26" y2="{y}" stroke="#5B6B7F" stroke-width="2"/>'
        if i: s += T(32, y + 7, f'{d} m', 19, anchor='start', fill='#5B6B7F')
    # 잠수부
    s += '<g transform="translate(205 230) rotate(-18)">'
    s += '<ellipse cx="0" cy="0" rx="62" ry="20" fill="#3A3F47"/><rect x="-40" y="-36" width="70" height="20" rx="10" fill="#E8C547" stroke="#A8865A" stroke-width="2"/>'
    s += '<circle cx="70" cy="-4" r="17" fill="#3A3F47"/><rect x="74" y="-14" width="16" height="12" rx="3" fill="#BFE3F5" stroke="#16233D" stroke-width="1.5"/>'
    s += '<path d="M-60 -4 L-100 -18 L-104 8 Z M-60 6 L-98 18 L-90 34 Z" fill="#1F6FD1"/>'
    s += '</g>'
    s += '<g data-anim="move" data-from="0,60" data-dur="2.4" data-rep="loop" data-ease="lin">'
    for x, y, r in [(286, 170, 6), (292, 140, 5), (284, 110, 7), (290, 80, 4)]:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#9FC3DD" stroke-width="1.5"/>'
    s += '</g>'
    s += T(200, 330, '수심이 깊을수록 압력이 커진다', 19, fill='#5B6B7F')
    return s + '</svg>'
FIG['S18'] = s18

# S23 대단원 마무리 03
def s23():
    s = '<svg class="fig" viewBox="0 0 520 260" style="width:500px" aria-label="꼭지로 연결된 두 둥근 용기: 왼쪽 산소 1 기압 2 L, 오른쪽 질소 2 기압 3 L">'
    s += f'<circle cx="120" cy="140" r="80" fill="#F8FBFD" stroke="{GLASS}" stroke-width="3"/>'
    s += f'<circle cx="390" cy="140" r="98" fill="#F8FBFD" stroke="{GLASS}" stroke-width="3"/>'
    s += f'<rect x="199" y="132" width="94" height="16" fill="#E6EDF3" stroke="{GLASS}" stroke-width="2"/>'
    s += f'<rect x="236" y="120" width="20" height="40" rx="4" fill="#16233D"/><path d="M246 120 V100" stroke="#16233D" stroke-width="4"/>'
    s += T(246, 90, '꼭지', 19)
    s += T(120, 132, '$\\ce{O2}(g)$', 22, halo=True) + T(120, 162, '1 기압, 2 L', 20, halo=True)
    s += T(390, 132, '$\\ce{N2}(g)$', 22, halo=True) + T(390, 162, '2 기압, 3 L', 20, halo=True)
    return s + '</svg>'
FIG['S23'] = s23

# S21 금성
def s21():
    s = '<svg class="fig" viewBox="0 0 240 200" style="width:220px" aria-label="두꺼운 대기에 싸인 금성">'
    s += '<circle cx="120" cy="100" r="88" fill="#F6E7C1" opacity=".7"/><circle cx="120" cy="100" r="70" fill="#E9C97E" stroke="#B8901A" stroke-width="2"/>'
    s += '<g data-anim="rot" data-from="-30" data-o="120,100" data-dur="3" data-ease="out"><path d="M60 80 Q120 60 180 84 M56 110 Q120 96 184 116 M70 138 Q120 128 170 142" fill="none" stroke="#C9A24E" stroke-width="5" opacity=".7"/></g>'
    s += T(120, 196, '금성', 20, weight=700)
    return s + '</svg>'
FIG['S21'] = s21

import sys, re
src, dst = sys.argv[1], sys.argv[2]
html = open(src, encoding='utf-8').read()
html = re.sub(r'\[\[(\w+)\]\]', lambda m: FIG[m.group(1)](), html)
open(dst, 'w', encoding='utf-8').write(html)
print('ok', len(html))
