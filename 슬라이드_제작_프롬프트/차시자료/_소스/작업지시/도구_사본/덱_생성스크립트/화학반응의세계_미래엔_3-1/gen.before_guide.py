# slides.tpl.html 의 @@이름@@ 자리에 그림 SVG를 넣어 slides.html을 만든다.
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학반응의세계_미래엔/3-1_탄소_화합물의_종류/slides.html'
F = {}


def T(x, y, mix, size=20, anchor='middle', fill=None, weight=None, extra=''):
    if '<b>' in mix:
        mix = mix.replace('<b>', '').replace('</b>', ''); weight = weight or 700
    fl = f' fill="{fill}"' if fill else ''
    w = f' data-weight="{weight}"' if weight else ''
    return f'<text class="tex"{extra} x="{f(x)}" y="{f(y)}" data-mix="{mix}" data-size="{size}" data-anchor="{anchor}"{fl}{w}></text>'


def center_chain(n, fg, W, y0, d=62, S=28, **kw):
    w = chain_width(n, fg, d)
    return chain_svg(n, fg, (W - w) / 2, y0, d, S, **kw)


# ── 표지: 에탄올 공-막대 ──
a, b = mol_alkane_like(2, 'OH')
body, P = bs3d(a, b, 270, 250, k=95, yaw='auto', sc=1.45, anim='out')
oi = [i for i, (el, _) in enumerate(a) if el == 'O'][0]
F['COVER'] = (f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>{body}'
              f'<circle cx="{f(P[oi][0] + 22)}" cy="{f(P[oi][1] + 8)}" r="78" fill="none" stroke="{EQUI}" stroke-width="3" stroke-dasharray="8 6" data-anim="fade" data-dur=".8" data-delay="1.5"/>'
              + T(270, 492, '에탄올 $\\ce{C2H5OH}$의 공-막대 모형', 22, fill=MUTED))

# ── S2 대단원: 탄소 + 쓰임 카드 ──
def unit():
    cx, cy = 300, 165
    s = ''
    cards = [(110, 62, '연료', '메테인 $\\ce{CH4}$'), (490, 62, '소독', '에탄올 $\\ce{C2H5OH}$'),
             (110, 268, '식초', '아세트산 $\\ce{CH3COOH}$'), (490, 268, '비닐·병', '폴리에틸렌')]
    for x, y, t1, t2 in cards:
        s += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#9FB0C2" stroke-width="3" stroke-dasharray="6 5"/>'
    s += f'<g data-atom="{cx},{cy},40,C"></g>'
    for k, (x, y, t1, t2) in enumerate(cards):
        s += (f'<g data-anim="pop" data-o="{x},{y}" data-dur=".7" data-delay="{.3 + .2 * k:.1f}" data-ease="back">'
              f'<rect x="{x - 105}" y="{y - 44}" width="210" height="88" rx="14" fill="#fff" stroke="#C9D3DD" stroke-width="2"/>'
              + T(x, y - 8, f'<b>{t1}</b>', 22) + T(x, y + 28, t2, 20, fill=MUTED) + '</g>')
    return s
F['UNIT'] = unit()

# ── S5 탄소 2개 세 물질 ──
F['S5A'] = center_chain(2, None, 300, 100, d=58, S=26)
F['S5B'] = center_chain(2, 'OH', 300, 100, d=58, S=26, g='o1', label='$\\ce{-OH}$', lab_size=19)
F['S5C'] = center_chain(2, 'COOH', 300, 112, d=58, S=26, g='o1', label='$\\ce{-COOH}$', lab_size=19)

# ── S7 탄소 결합 4개 ──
def s7():
    s = lewis_c(70, 120, 40)
    s += T(70, 222, '탄소 원자', 19, fill=MUTED)
    s += '<g data-arw="128,120,168,120,ink,3"></g>'
    cx, cy, S = 270, 120, 36
    s += f'<text class="tex" x="{cx}" y="{f(cy + .36 * S)}" data-tex="\\mathrm{{C}}" data-size="{S}" data-anchor="middle"></text>'
    # 공유 전자쌍
    for dx, dy, o in ((0, -.75, 'h'), (0, .75, 'h'), (-.70, 0, 'v'), (.70, 0, 'v')):
        x, y = cx + dx * S, cy + dy * S
        q = .18 * S
        pts = [(x - q, y), (x + q, y)] if o == 'h' else [(x, y - q), (x, y + q)]
        bw, bh = (34, 20) if o == 'h' else (20, 34)
        s += f'<rect class="step" data-g="b1" x="{f(x - bw / 2)}" y="{f(y - bh / 2)}" width="{bw}" height="{bh}" rx="7" fill="#2E9E6A" fill-opacity=".18" stroke="#2E9E6A" stroke-width="1.5"/>'
        s += ''.join(f'<circle cx="{f(px)}" cy="{f(py)}" r="4" fill="{INK}"/>' for px, py in pts)
    for dx, dy in ((0, -1.62), (0, 1.62), (-1.55, 0), (1.55, 0)):
        x, y = cx + dx * S, cy + dy * S
        s += (f'<g data-anim="move" data-from="{f(dx * 28)},{f(dy * 28)}" data-dur="1.1" data-delay=".4" data-ease="out">'
              f'<text class="tex" x="{f(x)}" y="{f(y + .36 * S)}" data-tex="\\mathrm{{H}}" data-size="{S}" data-anchor="middle"></text></g>')
    s += T(cx, 222, '메테인의 루이스 전자점식', 19, fill=MUTED)
    s += '<g data-arw="352,120,392,120,ink,3"></g>'
    a, b = mol_methane()
    body, P = bs3d(a, b, 480, 116, k=58, yaw=24, pitch=-14, sc=.85)
    s += body + T(480, 222, '정사면체형 $109.5^\\circ$', 19, fill=MUTED)
    return s
F['S7'] = s7()

# ── S8 결합 종류 + 골격 ──
def s8():
    s = ''
    S, d = 26, 54
    # 위 줄: 에테인, 에텐, 에타인 (x 중심 180, 550, 920)
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
    for x, t in ((180, '에테인 — 단일 결합'), (550, '에텐 — 2중 결합'), (920, '에타인 — 3중 결합')):
        g += T(x, 190, t, 20, fill=MUTED)
    s += g + '</g>'
    # 아래 줄: 골격 (수소 생략)
    y2 = 290
    g = '<g class="step" data-g="k2">'
    def skel(pts, bonds):
        o = '<g data-anim="draw" data-dur="1" data-on="step">' + ''.join(
            f'<line x1="{f(pts[i][0])}" y1="{f(pts[i][1])}" x2="{f(pts[j][0])}" y2="{f(pts[j][1])}" stroke="{BOND}" stroke-width="7" stroke-linecap="round"/>' for i, j in bonds) + '</g>'
        o += ''.join(f'<g data-atom="{f(x)},{f(y)},20,C"></g>' for x, y in pts)
        return o
    pts = [(180 - 105 + 70 * k, y2 + (-18 if k % 2 else 18)) for k in range(4)]
    g += skel(pts, [(0, 1), (1, 2), (2, 3)])
    pts = [(550 - 75, y2 + 18), (550, y2 - 18), (550 + 75, y2 + 18), (550, y2 - 88)]
    g += skel(pts, [(0, 1), (1, 2), (1, 3)])
    pts = [(920 + 56 * math.cos(math.radians(90 + 60 * k)), y2 - 22 + 56 * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    g += skel(pts, [(k, (k + 1) % 6) for k in range(6)])
    for x, t in ((180, '사슬 모양'), (550, '가지 달린 사슬 모양'), (920, '고리 모양')):
        g += T(x, 372, t, 20, fill=MUTED)
    s += g + '</g>'
    return s
F['S8'] = s8()

# ── S9 에탄올 구조식·모형 ──
F['S9SF'] = center_chain(2, 'OH', 260, 100, d=50, S=24)
a, b = mol_alkane_like(2, 'OH')
F['S9BS'] = bs3d(a, b, 130, 100, k=48, yaw='auto', sc=.8)[0]

# ── S10 프로페인 ──
F['S10'] = center_chain(3, None, 330, 95, d=56, S=26)

# ── S11 분류 칸 그림 ──
def mini_ring(cx, cy, r, dbl=False, lab='C', S=22, circle=False):
    pts = [(cx + r * math.cos(math.radians(90 + 60 * k)), cy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    s = ''
    for k in range(6):
        x1, y1 = pts[k]; x2, y2 = pts[(k + 1) % 6]
        s += f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
        if dbl and k % 2 == 0:
            # 안쪽 평행선
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            vx, vy = cx - mx, cy - my; n = math.hypot(vx, vy)
            ox, oy = vx / n * 8, vy / n * 8
            sx, sy = (x2 - x1) * .18, (y2 - y1) * .18
            s += f'<line x1="{f(x1 + ox + sx)}" y1="{f(y1 + oy + sy)}" x2="{f(x2 + ox - sx)}" y2="{f(y2 + oy - sy)}" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    if circle:
        s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * .58)}" fill="none" stroke="{INK}" stroke-width="3"/>'
    return s
F['S11A'] = center_chain(2, None, 230, 60, d=40, S=20)
F['S11B'] = mini_ring(115, 62, 46)
F['S11C'] = (sf([('C', 70, 60), ('C', 130, 60), ('H', 36, 28), ('H', 36, 92), ('H', 164, 28), ('H', 164, 92)], [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], 20)
             + sf([('H', 190, 60), ('C', 236, 60), ('C', 290, 60), ('H', 336, 60)], [(0, 1, 1), (1, 2, 3), (2, 3, 1)], 20))
F['S11D'] = mini_ring(115, 62, 46, dbl=True)

# ── S12 알케인 끓는점 막대 ──
def s12():
    bp = [-162, -89, -42, -0.5, 36, 69]
    X0, Y0, W, H = 78, 40, 360, 250  # 그래프 영역
    lo, hi = -200, 100
    Y = lambda v: Y0 + (hi - v) / (hi - lo) * H
    s = ''
    for v in (-200, -150, -100, -50, 0, 50, 100):
        s += f'<line x1="{X0}" y1="{f(Y(v))}" x2="{X0 + W}" y2="{f(Y(v))}" stroke="#E2E7EC" stroke-width="1.5"/>'
        s += T(X0 - 10, Y(v) + 7, f'${v}$', 18, 'end', MUTED)
    s += f'<line x1="{X0}" y1="{f(Y(0))}" x2="{X0 + W}" y2="{f(Y(0))}" stroke="{MUTED}" stroke-width="2"/>'
    s += f'<line x1="{X0}" y1="{Y0 - 6}" x2="{X0}" y2="{Y0 + H}" stroke="{MUTED}" stroke-width="2"/>'
    s += f'<line x1="{X0}" y1="{f(Y(25))}" x2="{X0 + W}" y2="{f(Y(25))}" stroke="{EQUI}" stroke-width="2" stroke-dasharray="6 5"/>'
    s += T(X0 + W - 4, Y(25) - 8, '$25\\ {}^\\circ\\text{C}$', 18, 'end', EQUI)
    bw = 36
    for k, v in enumerate(bp):
        cx = X0 + 30 + k * 60
        y0 = Y(0)
        top = min(y0, Y(v)); h = abs(Y(v) - y0)
        s += (f'<rect x="{f(cx - bw / 2)}" y="{f(top)}" width="{bw}" height="{f(h)}" rx="4" fill="#8C99A6" fill-opacity=".75" '
              f'data-anim="scale" data-from="1,0" data-o="{f(cx)},{f(y0)}" data-dur=".9" data-delay="{.2 + .12 * k:.2f}" data-ease="out"/>')
        s += T(cx, Y0 + H + 26, f'${k + 1}$', 18, fill=MUTED)
    s += T(X0 + W / 2, Y0 + H + 52, '탄소 수', 19, fill=MUTED)
    s += T(X0 - 6, 22, '끓는점 [°C]', 19, 'start', MUTED)
    return s
F['S12'] = s12()

# ── S13 에텐·에타인 ──
a, b = mol_ethene()
F['S13A'] = (sf([('C', 70, 100), ('C', 140, 100), ('H', 30, 60), ('H', 30, 140), ('H', 180, 60), ('H', 180, 140)], [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], 26)
             + bs3d(a, b, 340, 100, k=62, yaw=0, pitch=-20, sc=.9, anim='out')[0]
             + f'<path d="M 362.3 72.4 A 32 32 0 0 1 362.3 127.6" fill="none" stroke="{MUTED}" stroke-width="2"/>'
             + T(436, 108, '약 $120^\\circ$', 19, 'start', MUTED, extra=' data-halo="1"'))
a, b = mol_ethyne()
F['S13B'] = (sf([('H', 20, 100), ('C', 80, 100), ('C', 150, 100), ('H', 210, 100)], [(0, 1, 1), (1, 2, 3), (2, 3, 1)], 26)
             + bs3d(a, b, 350, 100, k=50, yaw=0, pitch=0, sc=.9, anim='out')[0]
             + T(350, 170, '일직선 $180^\\circ$', 19, fill=MUTED))

# ── S14 사이클로헥세인·벤젠 ──
def chx():
    cx, cy, r = 150, 130, 82
    pts = [(cx + r * math.cos(math.radians(90 + 60 * k)), cy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    atoms = [('CH2', x, y) for x, y in pts]
    return sf(atoms, [(k, (k + 1) % 6, 1) for k in range(6)], 24)
F['S14A'] = chx()
def bz():
    cx, cy, r = 140, 130, 62
    pts = [(cx + r * math.cos(math.radians(90 + 60 * k)), cy - r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    hp = [(cx + 1.75 * r * math.cos(math.radians(90 + 60 * k)), cy - 1.75 * r * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
    atoms = [('C', x, y) for x, y in pts] + [('H', x, y) for x, y in hp]
    bonds = [(k, (k + 1) % 6, 2 if k % 2 == 0 else 1) for k in range(6)] + [(k, 6 + k, 1) for k in range(6)]
    s = sf(atoms, bonds, 24, gap=7)
    s += f'<g class="step" data-g="z1">' + T(296, 136, '$=$', 30, fill=MUTED)
    s += mini_ring(400, 130, 62, circle=False).replace('<line', '<line data-x="1"', 0)
    # 원 표기 육각형
    s += f'<circle cx="400" cy="130" r="36" fill="none" stroke="{INK}" stroke-width="3" data-anim="draw" data-dur="1" data-on="step"/>'
    s += T(400, 236, '간단히 나타낸 벤젠', 19, fill=MUTED) + '</g>'
    return s
F['S14B'] = bz()

# ── S15 분별 증류탑 ──
def tower():
    s = ''
    x0, x1, top, bot = 150, 290, 30, 390
    s += f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bot - top}" rx="18" fill="#F4F6F8" stroke="#7E8B98" stroke-width="3"/>'
    fr = [('석유 가스', '$30\\ {}^\\circ\\text{C}$ 이하', 'C1–C4'), ('휘발유', '$30$–$180\\ {}^\\circ\\text{C}$', 'C5–C12'),
          ('등유', '$170$–$250\\ {}^\\circ\\text{C}$', 'C10–C16'), ('경유', '$250$–$350\\ {}^\\circ\\text{C}$', 'C14–C20'),
          ('중유', '$350\\ {}^\\circ\\text{C}$ 이상', 'C20 이상')]
    ys = [70, 135, 200, 265, 330]
    for (n, t, c), y in zip(fr, ys):
        cc = c.replace('C1–C4', '$\\mathrm{C}_1$–$\\mathrm{C}_4$').replace('C5–C12', '$\\mathrm{C}_5$–$\\mathrm{C}_{12}$').replace('C10–C16', '$\\mathrm{C}_{10}$–$\\mathrm{C}_{16}$').replace('C14–C20', '$\\mathrm{C}_{14}$–$\\mathrm{C}_{20}$').replace('C20 이상', '$\\mathrm{C}_{20}$ 이상')
        s += f'<line x1="{x0 + 10}" y1="{y + 22}" x2="{x1 - 10}" y2="{y + 22}" stroke="#9AA5B1" stroke-width="3"/>'
        s += f'<line x1="{x1}" y1="{y}" x2="{x1 + 40}" y2="{y}" stroke="#7E8B98" stroke-width="6"/>'
        s += f'<g data-arw="{x1 + 40},{y},{x1 + 62},{y},muted,2.5"></g>'
        s += T(x1 + 70, y + 7, f'<b>{n}</b> {cc}', 20, 'start')
        s += T(x1 + 70, y + 33, t, 18, 'start', MUTED)
    s += T(220, 425, '아스팔트(찌꺼기)', 18, fill=MUTED)
    # 가열 원유
    s += f'<line x1="40" y1="372" x2="{x0}" y2="372" stroke="#7E8B98" stroke-width="7"/>'
    s += T(70, 360, '가열한 원유', 18, 'start', MUTED)
    s += f'<g data-arw="40,372,140,372,ink,2.5"></g>'
    # 증기 화살표
    s += '<g data-anim="move" data-from="0,60" data-dur="1.6" data-delay=".3" data-rep="loop" data-ease="lin"><g data-arw="220,350,220,250,equi,3"></g></g>'
    s += T(100, 230, '위로 갈수록||온도가 낮다', 18, fill=EQUI)
    s += f'<g data-arw="110,200,110,60,muted,2"></g>'
    return s
F['S15'] = tower()

# ── S17 에테인 → 에탄올 ──
F['S17A'] = center_chain(2, None, 300, 100, d=56, S=26)
def s17b():
    a, b, gb = chain(2, 'OH', 0, 0, 56, 26)
    w = chain_width(2, 'OH', 56); x0 = (330 - w) / 2; y0 = 100
    a = [(s, x + x0, y + y0) for s, x, y in a]
    gb = (gb[0] + x0, gb[1] + y0, gb[2], gb[3])
    oi = [i for i, (s, _, _) in enumerate(a) if s == 'O'][0]
    rest = [k for k in range(len(a)) if k not in (oi, oi + 1)]
    # 기본 골격 (O-H 제외)
    idx = {k: n for n, k in enumerate(rest)}
    core = sf([a[k] for k in rest], [(idx[i], idx[j], o) for i, j, o in b if i in idx and j in idx], 26)
    grp = box(*gb) + sf([a[oi - 1], a[oi], a[oi + 1]], [(0, 1, 1), (1, 2, 1)], 26).split('<text')[0]
    grp = box(*gb) + sf([a[oi], a[oi + 1]], [(0, 1, 1)], 26)
    # C-O 결합선만 따로 (C는 core에 있음)
    cline = sf([a[oi - 1], a[oi]], [(0, 1, 1)], 26)
    cline = cline[:cline.index('<text')]
    return core + f'<g data-anim="move" data-from="40,-40" data-dur="1.1" data-delay=".5" data-ease="out">{cline}{grp}</g>' + T(gb[0] + gb[2] / 2, gb[1] + gb[3] + 24, '$\\ce{-OH}$', 19, fill=EQUI, weight=700)
F['S17B'] = s17b()

# ── S18 작용기 구조 (R) ──
def grp(kind):
    S, d = 24, 52
    if kind == 'OH':
        at = [('R', 30, 60), ('O', 30 + d, 60), ('H', 30 + 2 * d, 60)]; bd = [(0, 1, 1), (1, 2, 1)]
        bx = (30 + d - 16, 40, d + 32, 40)
    elif kind == 'CHO':
        at = [('R', 30, 74), ('C', 30 + d, 74), ('O', 30 + d, 74 - d * .85), ('H', 30 + 2 * d, 74)]; bd = [(0, 1, 1), (1, 2, 2), (1, 3, 1)]
        bx = (30 + d - 16, 74 - d * .85 - 16, d + 32, d * .85 + 32)
    else:
        at = [('R', 30, 74), ('C', 30 + d, 74), ('O', 30 + d, 74 - d * .85), ('O', 30 + 2 * d, 74), ('H', 30 + 3 * d, 74)]; bd = [(0, 1, 1), (1, 2, 2), (1, 3, 1), (3, 4, 1)]
        bx = (30 + d - 16, 74 - d * .85 - 16, 2 * d + 32, d * .85 + 32)
    return box(*bx) + sf(at, bd, S)
for k in ('OH', 'CHO', 'COOH'):
    F['S18' + k] = grp(k)

# ── S19 메탄올·에탄올 ──
def card_pair(n, fg, W=470, d=50, S=24, yaw='auto', k=46, sc=.78, y=78, anim=None, label=None):
    w = chain_width(n, fg, d)
    s = chain_svg(n, fg, 20, y, d, S, box_anim=anim or '')
    a, b = mol_alkane_like(n, fg)
    s += bs3d(a, b, 40 + w + (W - 40 - w) / 2, y, k=k, yaw=yaw, sc=sc)[0]
    return s
F['S19A'] = card_pair(1, 'OH', anim=' data-anim="draw" data-dur=".9" data-delay=".4"')
F['S19B'] = card_pair(2, 'OH', anim=' data-anim="draw" data-dur=".9" data-delay=".6"')

# ── S20 에탄올과 물 수소 결합 ──
def s20():
    a, b = mol_alkane_like(2, 'OH')
    body, P = bs3d(a, b, 170, 150, k=58, yaw=15, pitch=-30, sc=1.0)
    oi = [i for i, (el, _) in enumerate(a) if el == 'O'][0]
    hi = [j for i, j, o in b if i == oi][0]
    ox, oy = P[oi][0], P[oi][1]
    hx, hy = P[hi][0], P[hi][1]
    s = body
    def water(xo, yo, ang, flip=1):
        # O 중심, 두 H 104.5°
        out = ''
        hs = []
        for t in (ang - 52, ang + 52):
            x = xo + 46 * math.cos(math.radians(t)); y = yo - 46 * math.sin(math.radians(t))
            hs.append((x, y))
        out += ''.join(f'<line x1="{f(xo)}" y1="{f(yo)}" x2="{f(x)}" y2="{f(y)}" stroke="{BOND}" stroke-width="6" stroke-linecap="round"/>' for x, y in hs)
        out += f'<g data-atom="{f(xo)},{f(yo)},20,O"></g>' + ''.join(f'<g data-atom="{f(x)},{f(y)},15,H,-"></g>' for x, y in hs)
        return out, hs
    hb = []
    # 물 1: 에탄올 H(O) → 물 O
    ux, uy = hx - ox, hy - oy; n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    w1x, w1y = hx + ux * 92, hy + uy * 92
    w, hs1 = water(w1x, w1y, math.degrees(math.atan2(-uy, ux)))
    s += w; hb.append((hx + ux * 18, hy + uy * 18, w1x - ux * 22, w1y - uy * 22))
    # 물 2: 물 H → 에탄올 O (아래쪽 비공유 방향)
    w2x, w2y = ox - 20, oy + 128
    w, hs2 = water(w2x, w2y, 90 + 10)
    s += w
    hxx, hyy = min(hs2, key=lambda p: math.hypot(p[0] - ox, p[1] - oy))
    vx, vy = ox - hxx, oy - hyy; n = math.hypot(vx, vy)
    hb.append((hxx + vx / n * 15, hyy + vy / n * 15, ox - vx / n * 24, oy - vy / n * 24))
    for x1, y1, x2, y2 in hb:
        s += f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="#2E9E6A" stroke-width="3.5" stroke-dasharray="5 5" data-anim="dash" data-speed="14" data-rep="loop"/>'
    s += T(330, 305, '점선: 수소 결합', 19, 'start', '#2E9E6A', 700)
    s += T(80, 300, '에탄올', 19, fill=MUTED)
    return s, (ox, oy)
F['S20'], _o = s20()

# ── S21 폼알데하이드·아세트알데하이드 ──
F['S21A'] = card_pair(1, 'CHO', y=92)
F['S21B'] = card_pair(2, 'CHO', y=92)
# ── S22 폼산·아세트산 ──
F['S22A'] = card_pair(1, 'COOH', y=92)
F['S22B'] = card_pair(2, 'COOH', y=92)
def s22ion():
    a, b, gb = chain(2, 'COOH', 20, 100, 50, 24)
    hi = len(a) - 1
    core = sf(a[:hi], [x for x in b if x[1] != hi], 24)
    hx, hy = a[hi][1], a[hi][2]
    ox, oy = a[hi - 1][1], a[hi - 1][2]
    s = core + f'<circle cx="{f(hx)}" cy="{f(hy)}" r="15" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 4"/>'
    s += T(ox + 18, oy - 16, '$-$', 22, fill='#1F6FD1', weight=700)
    # 물 분자 (텍스트)
    wx = 470
    s += f'<text class="tex" x="{wx}" y="{f(hy + 9)}" data-tex="\\ce{{H2O}}" data-size="26" data-anchor="middle"></text>'
    s += f'<g data-arw="{f(hx + 22)},{f(hy - 50)},{wx - 60},{f(hy - 50)},plus,3"></g>'
    s += (f'<g data-anim="move" data-from="{f(hx - (wx - 62))},0" data-dur="1.2" data-delay=".5" data-ease="io" data-on="step">'
          f'<g data-atom="{wx - 62},{f(hy)},15,H,-"></g>' + T(wx - 62, hy - 22, '$\\ce{H+}$', 20, fill='#D7263D', weight=700) + '</g>')
    s += T(wx - 20, hy + 52, '$\\ce{H3O+}$', 22, fill='#D7263D', weight=700)
    s += T(110, 190, '아세트산 이온 $\\ce{CH3COO-}$', 19, fill=MUTED)
    return s
F['S22ION'] = s22ion()

# ── S25 확인하기 4 구조 ──
for key, n, fg in (('S25A', 3, 'OH'), ('S25B', 3, 'CHO'), ('S25C', 1, 'COOH'), ('S25D', 3, None)):
    F[key] = center_chain(n, fg, 300, 82 if fg in ('CHO', 'COOH') else 70, d=46, S=22)

# ── S27 과정 그림 (시험관) ──
def tube(x, top, h=150, w=44, fill=None, lvl=None, extra=''):
    s = ''
    if fill:
        s += f'<path d="M{x - w / 2 + 3} {lvl} L{x - w / 2 + 3} {top + h - w / 2} A{w / 2 - 3} {w / 2 - 3} 0 0 0 {x + w / 2 - 3} {top + h - w / 2} L{x + w / 2 - 3} {lvl} Z" fill="{fill}" stroke="#9FC3DD" stroke-width="1.5"/>'
    s += f'<path d="M{x - w / 2} {top} L{x - w / 2} {top + h - w / 2} A{w / 2} {w / 2} 0 0 0 {x + w / 2} {top + h - w / 2} L{x + w / 2} {top}" fill="none" stroke="#7E8B98" stroke-width="3"/>'
    return s + extra
def s27():
    s = ''
    for k, (x, n) in enumerate(((90, '헥세인'), (240, '에탄올'), (390, '아세트산'))):
        s += tube(x, 70, fill='#DDEEF8', lvl=150)
        s += f'<g data-anim="move" data-from="0,-30" data-dur=".9" data-delay="{.3 + .25 * k:.2f}" data-ease="out"><path d="M{x - 8} 14 L{x + 8} 14 L{x + 4} 52 L{x - 4} 52 Z" fill="#fff" stroke="#7E8B98" stroke-width="2"/><g data-arw="{x},54,{x},92,ink,2.5"></g></g>'
        s += T(x, 260, n, 19)
    s += T(470, 140, '물 $5\\ \\text{mL}$||+ 시료 $1\\ \\text{mL}$', 18, 'start', MUTED)
    return s
F['S27'] = s27()

# ── S31 세 구조 ──
def s31():
    s = ''
    for x0, n, fg, lab in ((10, 2, 'OH', '(가)'), (230, 2, 'CHO', '(나)'), (430, 2, 'COOH', '(다)')):
        s += chain_svg(n, fg, x0, 100, 44, 22)
        w = chain_width(n, fg, 44)
        s += T(x0 + w / 2, 186, lab, 20)
    return s
F['S31'] = s31()

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
    o += '</g>' + ''.join(f'<g data-atom="{f(x)},{f(y)},20,C,-"></g>' for x, y in pts)
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
    pts = [(420, y2 - 14), (472, y2 + 14), (524, y2 - 14), (576, y2 + 14), (472, y2 + 72)]
    g += skel2(pts, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (1, 4, 1)])
    xs = [660 + 52 * k for k in range(5)]
    g += skel2([(x, y2 + (-14 if k % 2 else 14)) for k, x in enumerate(xs)], [(0, 1, 2), (1, 2, 1), (2, 3, 1), (3, 4, 1)])
    pts = [(1000 + 50 * math.cos(math.radians(90 + 72 * k)), y2 - 20 - 50 * math.sin(math.radians(90 + 72 * k))) for k in range(5)]
    g += skel2(pts, [(k, (k + 1) % 5, 1) for k in range(5)])
    for x, t in ((214, '사슬'), (498, '가지 달린 사슬'), (764, '이중 결합이 있는 사슬'), (1000, '고리')):
        g += T(x, 400, t, 20, fill=MUTED)
    s += g + '</g>'
    return s
F['S8'] = s8b()

# 프로페인 분자식·구조식·모형
F['S9SF'] = center_chain(3, None, 260, 100, d=46, S=22)
a, b = mol_alkane_like(3)
F['S9BS'] = bs3d(a, b, 130, 104, k=40, yaw='auto', sc=.7)[0]
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
    s += T(cx + 76, 150, '$\\ce{-COOH}$', 19, fill=EQUI, weight=700)
    s += f'<text class="tex step" data-g="fa" x="{f(cx)}" y="205" data-mix="$\\ce{{-CHO}}$" data-size="19" data-anchor="middle" fill="#7B4FC8" data-weight="700"></text>'
    return s
F['FORMIC'] = formic()
# 대단원 마무리 03: (가) 메테인 (나) 에테인 (다) 아세트산 공-막대
def q03():
    s = ''
    for x, mol, lab in ((100, mol_methane(), '(가)'), (310, mol_alkane_like(2), '(나)'), (530, mol_alkane_like(2, 'COOH'), '(다)')):
        a, b = mol
        s += bs3d(a, b, x, 95, k=42, yaw='auto', sc=.72)[0]
        s += T(x, 196, lab, 20)
    return s
F['Q03'] = q03()
# 대단원 마무리 04: (가) 메탄올 (나) 아세트산 (다) 폼산 (라) 1-프로판올
for key, n, fg in (('Q4A', 1, 'OH'), ('Q4B', 2, 'COOH'), ('Q4C', 1, 'COOH'), ('Q4D', 3, 'OH')):
    F[key] = center_chain(n, fg, 300, 80 if fg == 'COOH' else 70, d=44, S=21)

F['S9SF2'] = center_chain(2, 'OH', 260, 100, d=50, S=24)
a, b = mol_alkane_like(2, 'OH')
F['S9BS2'] = bs3d(a, b, 130, 100, k=48, yaw='auto', sc=.8)[0]
F['S22S'] = center_chain(2, 'COOH', 300, 92, d=50, S=24)
tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
miss = set(re.findall(r'@@(\w+)@@', tpl)) - set(F)
if miss:
    raise SystemExit('없는 그림: ' + ', '.join(sorted(miss)))
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
open(OUT, 'w', encoding='utf-8').write(out)
print('slides.html', len(out), '바이트,', out.count('<section'), '장')
