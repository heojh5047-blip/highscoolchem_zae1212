# 3-3 다양한 고분자 화합물 — slides.tpl.html 의 @@이름@@ 자리에 그림 SVG를 넣어 slides.html 을 만든다.
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학반응의세계_미래엔/3-3_다양한_고분자_화합물/slides.html'
F = {}
FIELD, BF, PLUS, MINUS, GRAV = '#2E9E6A', '#7B4FC8', '#D7263D', '#1F6FD1', '#8C99A6'
ETH, AA1, AA2, AA3 = '#F08A5D', '#5AA9E6', '#F2C230', '#B07CD8'
PH, SU, BA = '#F6B26B', '#76B7E5', '#E58FB4'


def T(x, y, mix, size=20, anchor='middle', fill=None, weight=None, extra='', halo=False):
    if '<b>' in mix:
        mix = mix.replace('<b>', '').replace('</b>', ''); weight = weight or 700
    fl = f' fill="{fill}"' if fill else ''
    w = f' data-weight="{weight}"' if weight else ''
    h = ' data-halo="1"' if halo else ''
    return f'<text class="tex"{extra} x="{f(x)}" y="{f(y)}" data-mix="{mix}" data-size="{size}" data-anchor="{anchor}"{fl}{w}{h}></text>'


def TX(x, y, tex, size=24, anchor='middle', fill=None, extra=''):
    fl = f' fill="{fill}"' if fill else ''
    return f'<text class="tex"{extra} x="{f(x)}" y="{f(y)}" data-tex="{tex}" data-size="{size}" data-anchor="{anchor}"{fl}></text>'


def arw(x1, y1, x2, y2, col='ink', w=3, extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}"{extra}></g>'


def ln(x1, y1, x2, y2, col=INK, w=3, extra=''):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{extra}/>'


def dots(x, y, col=INK):
    return ''.join(f'<circle cx="{f(x + k * 9)}" cy="{f(y)}" r="2.6" fill="{col}"/>' for k in (-1, 0, 1))


def rbox(x, y, w, h, col, op=.18, dash=False, extra='', rx=10):
    d = ' stroke-dasharray="6 5"' if dash else ''
    return f'<rect{extra} x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-width="2"{d}/>'


def ell(cx, cy, rx, ry, col=MINUS, extra=''):
    return f'<ellipse{extra} cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 5"/>'


def bracket(xl, xr, yt, yb, nlab=True, w=2.5):
    s = (f'<path d="M{f(xl + 10)} {f(yt)} H{f(xl)} V{f(yb)} H{f(xl + 10)}" fill="none" stroke="{INK}" stroke-width="{w}"/>'
         f'<path d="M{f(xr - 10)} {f(yt)} H{f(xr)} V{f(yb)} H{f(xr - 10)}" fill="none" stroke="{INK}" stroke-width="{w}"/>')
    if nlab:
        s += TX(xr + 12, yb + 4, 'n', 24, 'middle')
    return s


def water(x, y, extra=''):
    """떨어져 나가는 물 분자 라벨 (minus 테)"""
    return (f'<g{extra}><rect x="{f(x - 34)}" y="{f(y - 22)}" width="68" height="36" rx="18" fill="#fff" stroke="{MINUS}" stroke-width="2"/>'
            + TX(x, y + 6, '\\ce{H2O}', 22, fill=MINUS) + '</g>')


def bead(x, y, r, col, lab=None, size=18):
    s = f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col}" stroke="#16233D" stroke-opacity=".35" stroke-width="1.5"/>'
    if lab:
        s += T(x, y + size * .36, lab, size, fill=INK)
    return s


# ───────── 구조식 부품 ─────────
def ethene_sf(cx, cy, d=50, S=26, broken=False):
    """에틸렌 구조식. broken: 이중 결합 중 하나가 끊어져 탄소마다 손 하나(바깥쪽)"""
    a = [('C', cx - d / 2, cy), ('C', cx + d / 2, cy),
         ('H', cx - d / 2 - 32, cy - 40), ('H', cx - d / 2 - 32, cy + 40), ('H', cx + d / 2 + 32, cy - 40), ('H', cx + d / 2 + 32, cy + 40)]
    b = [(0, 1, 1 if broken else 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)]
    s = sf(a, b, S=S)
    if broken:
        for sx, x0 in ((-1, cx - d / 2), (1, cx + d / 2)):
            x1, x2 = x0 + sx * 15, x0 + sx * 36
            s += ln(x1, cy, x2, cy, INK, 3)
            s += f'<circle cx="{f(x2 + sx * 2)}" cy="{f(cy)}" r="9" fill="{EQUI}" fill-opacity=".28" stroke="{EQUI}" stroke-width="1.5"/>'
    return s


def chain_sf(x0, y, nC, d=60, S=26, stubL=True, stubR=True, vH=48):
    """…−C−C−…− 탄소 nC개 사슬, H는 위아래"""
    a, b = [], []
    for i in range(nC):
        x = x0 + i * d
        a.append(('C', x, y)); ci = len(a) - 1
        a.append(('H', x, y - vH)); b.append((ci, ci + 1, 1))
        a.append(('H', x, y + vH)); b.append((ci, ci + 2, 1))
        if i:
            b.append((ci - 3, ci, 1))
    s = sf(a, b, S=S)
    if stubL:
        s += ln(x0 - 14, y, x0 - d * .62, y) + dots(x0 - d * .62 - 16, y)
    if stubR:
        xe = x0 + (nC - 1) * d
        s += ln(xe + 14, y, xe + d * .62, y) + dots(xe + d * .62 + 16, y)
    return s


def aa_sf(x0, y, R='R1', d=58, S=26, left='H', right='OH'):
    """아미노산 H−N(H)−C(R)(H)−C(=O)−O−H. left/right None이면 그쪽은 열린 결합"""
    a = [('N', x0 + d, y), ('H', x0 + d, y + 52), ('C', x0 + 2 * d, y), (R, x0 + 2 * d, y - 52), ('H', x0 + 2 * d, y + 52),
         ('C', x0 + 3 * d, y), ('O', x0 + 3 * d, y - 52)]
    b = [(0, 1, 1), (0, 2, 1), (2, 3, 1), (2, 4, 1), (2, 5, 1), (5, 6, 2)]
    if left:
        a.append(('H', x0, y)); b.append((0, len(a) - 1, 1))
    if right:
        a.append(('O', x0 + 4 * d, y)); b.append((5, len(a) - 1, 1))
        a.append(('H', x0 + 4 * d + 44, y)); b.append((len(a) - 2, len(a) - 1, 1))
    s = sf(a, b, S=S)
    if not left:
        s += ln(x0 + d - 15, y, x0 + 12, y) + dots(x0 - 4, y)
    if not right:
        s += ln(x0 + 3 * d + 15, y, x0 + 3 * d + 44, y) + dots(x0 + 3 * d + 60, y)
    return s


def dipep_sf(x0, y, d=58, S=26, open_=False):
    """두 아미노산이 이어진 구조식. 반환 svg, 펩타이드 결합 C·N x"""
    a = [('N', x0 + d, y), ('H', x0 + d, y + 52), ('C', x0 + 2 * d, y), ('R1', x0 + 2 * d, y - 52), ('H', x0 + 2 * d, y + 52),
         ('C', x0 + 3 * d, y), ('O', x0 + 3 * d, y - 52),
         ('N', x0 + 4 * d, y), ('H', x0 + 4 * d, y + 52), ('C', x0 + 5 * d, y), ('R2', x0 + 5 * d, y - 52), ('H', x0 + 5 * d, y + 52),
         ('C', x0 + 6 * d, y), ('O', x0 + 6 * d, y - 52)]
    b = [(0, 1, 1), (0, 2, 1), (2, 3, 1), (2, 4, 1), (2, 5, 1), (5, 6, 2), (5, 7, 1), (7, 8, 1), (7, 9, 1), (9, 10, 1), (9, 11, 1), (9, 12, 1), (12, 13, 2)]
    if not open_:
        a += [('H', x0, y), ('O', x0 + 7 * d, y), ('H', x0 + 7 * d + 44, y)]
        b += [(0, 14, 1), (12, 15, 1), (15, 16, 1)]
    s = sf(a, b, S=S)
    if open_:
        s += ln(x0 + d - 15, y, x0 + 12, y) + dots(x0 - 4, y)
        s += ln(x0 + 6 * d + 15, y, x0 + 6 * d + 44, y) + dots(x0 + 6 * d + 60, y)
    return s, x0 + 3 * d, x0 + 4 * d


def ring_sf(cx, cy, r=46, S=24, Hs=True):
    a, b = [], []
    for k in range(6):
        t = math.radians(60 * k)
        a.append(('C', cx + r * math.cos(t), cy - r * math.sin(t)))
    for k in range(6):
        b.append((k, (k + 1) % 6, 2 if k % 2 == 1 else 1))
    if Hs:
        for k in (1, 2, 4, 5):
            t = math.radians(60 * k)
            a.append(('H', cx + (r + 42) * math.cos(t), cy - (r + 42) * math.sin(t))); b.append((k, len(a) - 1, 1))
    return a, b


def tere_sf(cx, cy, S=24, left_open=False, right_link=False, dots_=True):
    """테레프탈산 (left_open: 왼쪽 −OH 대신 열린 결합 / right_link: 오른쪽 −O− 연결만)"""
    a, b = ring_sf(cx, cy, S=S)
    n = len(a)
    a += [('C', cx - 100, cy), ('O', cx - 126, cy - 46), ('C', cx + 100, cy), ('O', cx + 126, cy - 46)]
    b += [(3, n, 1), (n, n + 1, 2), (0, n + 2, 1), (n + 2, n + 3, 2)]
    if not left_open:
        a += [('O', cx - 150, cy), ('H', cx - 194, cy)]; m = len(a)
        b += [(n, m - 2, 1), (m - 2, m - 1, 1)]
    if not right_link:
        a += [('O', cx + 150, cy), ('H', cx + 194, cy)]; m = len(a)
        b += [(n + 2, m - 2, 1), (m - 2, m - 1, 1)]
    s = sf(a, b, S=S)
    if left_open and dots_:
        s += ln(cx - 114, cy, cx - 140, cy) + dots(cx - 156, cy)
    return s


# ═════════ 표지: 폴리에틸렌 공-막대 (단위체 3묶음이 모여듦) ═════════
def pe_ballstick(x0, y0, dx=70, amp=18, k=1.0, anim=True, ends=True):
    """C 6, H 12 지그재그. 반환 svg"""
    Cs = [(x0 + i * dx * k, y0 + (-amp if i % 2 == 0 else amp) * k) for i in range(6)]
    rC, rH = 24 * k, 18 * k
    units = []
    bonds_between = ''
    for u in range(3):
        s = ''
        c1, c2 = Cs[2 * u], Cs[2 * u + 1]
        s += f'<line x1="{f(c1[0])}" y1="{f(c1[1])}" x2="{f(c2[0])}" y2="{f(c2[1])}" stroke="{BOND}" stroke-width="{f(7 * k)}" stroke-linecap="round"/>'
        hs = []
        for i, c in ((2 * u, c1), (2 * u + 1, c2)):
            up = i % 2 == 0
            for sx in (-1, 1):
                hx, hy = c[0] + sx * 27 * k, c[1] + (-52 if up else 52) * k
                s += f'<line x1="{f(c[0])}" y1="{f(c[1])}" x2="{f(hx)}" y2="{f(hy)}" stroke="{BOND}" stroke-width="{f(7 * k)}" stroke-linecap="round"/>'
                hs.append((hx, hy))
        for hx, hy in hs:
            s += f'<g data-atom="{f(hx)},{f(hy)},{f(rH)},H"></g>'
        s += f'<g data-atom="{f(c1[0])},{f(c1[1])},{f(rC)},C"></g><g data-atom="{f(c2[0])},{f(c2[1])},{f(rC)},C"></g>'
        if anim:
            fx = (u - 1) * 46 * k
            s = f'<g data-anim="move" data-from="{f(fx)},{f(-26 * k)}" data-dur="1.1" data-delay=".2" data-ease="out">{s}</g>'
        units.append(s)
    for u in (0, 1):
        c1, c2 = Cs[2 * u + 1], Cs[2 * u + 2]
        bonds_between += f'<line x1="{f(c1[0])}" y1="{f(c1[1])}" x2="{f(c2[0])}" y2="{f(c2[1])}" stroke="{BOND}" stroke-width="{f(7 * k)}" stroke-linecap="round"/>'
    if anim:
        bonds_between = f'<g data-anim="fade" data-dur=".5" data-delay="1.2">{bonds_between}</g>'
    endl = ''
    if ends:
        a, z = Cs[0], Cs[-1]
        endl += f'<line x1="{f(a[0] - 46 * k)}" y1="{f(a[1] + 20 * k)}" x2="{f(a[0])}" y2="{f(a[1])}" stroke="{BOND}" stroke-width="{f(7 * k)}" stroke-dasharray="{f(7 * k)} {f(7 * k)}"/>'
        endl += f'<line x1="{f(z[0])}" y1="{f(z[1])}" x2="{f(z[0] + 46 * k)}" y2="{f(z[1] - 20 * k)}" stroke="{BOND}" stroke-width="{f(7 * k)}" stroke-dasharray="{f(7 * k)} {f(7 * k)}"/>'
    return endl + bonds_between + ''.join(units), Cs


body, Cs = pe_ballstick(77.5, 270, k=1.1)
F['COVER'] = (f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>{body}'
              f'<rect x="{f(Cs[2][0] - 50)}" y="160" width="{f(Cs[3][0] - Cs[2][0] + 100)}" height="220" rx="16" fill="none" stroke="{EQUI}" stroke-width="3" stroke-dasharray="8 6" data-anim="fade" data-dur=".8" data-delay="1.7"/>'
              + T(270, 136, '반복 단위', 20, fill='#C26A12', weight=700)
              + T(270, 446, '폴리에틸렌', 24, fill=INK, weight=700)
              + T(270, 478, '에틸렌 단위체가 반복해 이어진 사슬', 20, fill=MUTED))

# ═════════ S3 소화: 큰 분자 → 작은 분자 ═════════
s = ''
s += '<rect x="14" y="20" width="170" height="210" rx="10" fill="#fff" stroke="#7E8B98" stroke-width="2.5"/>'
s += T(99, 52, '<b>영양 정보</b>', 20, fill=INK)
s += ln(28, 66, 170, 66, '#7E8B98', 2)
for i, (nm, w) in enumerate((('탄수화물', 100), ('단백질', 70), ('지방', 50))):
    yy = 100 + i * 44
    s += T(30, yy, nm, 19, 'start', fill=INK)
    s += f'<rect x="30" y="{yy + 8}" width="{w}" height="10" rx="5" fill="{[AA2, AA1, PLUS][i]}" fill-opacity=".7"/>'
# 큰 사슬
cols = [AA1, AA2, AA3]
pts = [(230 + 34 * i, 70 + (12 if i % 2 else 0)) for i in range(7)]
s += f'<polyline points="{" ".join(f"{f(x)},{f(y)}" for x, y in pts)}" fill="none" stroke="#7E8B98" stroke-width="4"/>'
s += ''.join(bead(x, y, 14, cols[i % 3]) for i, (x, y) in enumerate(pts))
s += T(332, 124, '큰 분자 (단백질)', 19, fill=INK)
s += arw(332, 140, 332, 196, 'muted', 3)
s += T(346, 176, '소화', 19, 'start', fill=MUTED)
for i in range(7):
    x, y = 222 + 36 * i, 236 + (16 if i % 2 else 0)
    ox, oy = pts[i]
    s += f'<g data-anim="move" data-from="{f(ox - x)},{f(oy - y)}" data-dur="1.2" data-delay="{.3 + .06 * i:.2f}" data-ease="out">{bead(x, y, 14, cols[i % 3])}</g>'
s += T(332, 300, '작은 분자 (아미노산)', 19, fill=INK)
F['DIGEST'] = s

# ═════════ S4 에틸렌 ═════════
F['ETHENE4'] = ethene_sf(150, 85, d=56, S=28) + rbox(108, 64, 84, 42, EQUI) + T(150, 162, '이중 결합', 20, fill='#C26A12', weight=700)

# ═════════ S5 단위체와 고분자 (구슬) ═════════
def wave_pts(n, x0, y0, dx, amp, per):
    return [(x0 + dx * i, y0 + amp * math.sin(i * 2 * math.pi / per)) for i in range(n)]


def panel_beads(px, title, chain, mono_cols, mono_lab, colfn):
    s = f'<rect x="{px}" y="10" width="520" height="290" rx="16" fill="#F7F9FB" stroke="#D5DCE3" stroke-width="2"/>'
    s += T(px + 260, 44, f'<b>{title}</b>', 21, fill=INK)
    s += f'<polyline points="{" ".join(f"{f(x)},{f(y)}" for x, y in chain)}" fill="none" stroke="#7E8B98" stroke-width="3.5" stroke-linejoin="round"/>'
    beads = ''.join(bead(x, y, 12, colfn(i)) for i, (x, y) in enumerate(chain))
    s += f'<g data-anim="pop" data-o="{px + 170},170" data-dur="1" data-ease="back">{beads}</g>'
    s += T(px + 170, 286, '고분자', 20, fill=MUTED, weight=700)
    s += f'<line x1="{px + 342}" y1="60" x2="{px + 342}" y2="280" stroke="#D5DCE3" stroke-width="2" stroke-dasharray="6 5"/>'
    for i, c in enumerate(mono_cols):
        y = 100 + i * 62
        s += f'<g data-anim="move" data-from="40,0" data-dur=".9" data-delay="{.6 + .15 * i:.2f}" data-ease="out">{bead(px + 430, y, 17, c)}</g>'
    s += T(px + 430, 286, '단위체', 20, fill=MUTED, weight=700)
    s += T(px + 430, 78, mono_lab, 19, fill=INK)
    return s


ch1 = [(55 + i * 11.5, 165 + 70 * math.sin(i / 25 * 2 * math.pi * 1.5)) for i in range(26)]
ch2 = [(560 + 25 + i * 11.5, 165 + 55 * math.sin(i / 25 * 2 * math.pi)) for i in range(26)]
F['BEADS'] = (panel_beads(20, '단백질', ch1, [AA1, AA2, AA3], '아미노산', lambda i: [AA1, AA2, AA3, AA2, AA1, AA3][i % 6])
              + panel_beads(560, '폴리에틸렌', ch2, [ETH, ETH, ETH], '에틸렌(에텐)', lambda i: ETH))

# ═════════ S6 공-막대 사슬 (단계 ②) ═════════
body, _ = pe_ballstick(65, 112, dx=70, k=1.0)
F['PECHAIN'] = body + T(240, 222, '$\\ce{C}$ 6개, $\\ce{H}$ 12개 — 하나의 분자', 19, fill=INK)

# 비닐봉지
F['BAG'] = ('<path d="M60 70 Q40 70 40 100 L30 230 Q30 250 50 250 H190 Q210 250 210 230 L200 100 Q200 70 180 70 L165 70 Q165 30 145 30 Q125 30 125 70 H115 Q115 30 95 30 Q75 30 75 70 Z" fill="#EAF2F7" fill-opacity=".9" stroke="#9FB0C2" stroke-width="3"/>'
            '<path d="M70 120 Q120 150 170 110" fill="none" stroke="#C9D6E2" stroke-width="3"/><path d="M60 180 Q120 205 185 170" fill="none" stroke="#C9D6E2" stroke-width="3"/>')

# ═════════ S7 해 보기 모형 (가)(나) ═════════
PINK = '#F28DB2'
s = '<rect x="6" y="6" width="488" height="300" rx="16" fill="none" stroke="#9FB0C2" stroke-width="2" stroke-dasharray="7 6"/>'
for (xa, xb) in ((70, 140), (290, 360)):
    s += f'<rect x="{xa - 40}" y="40" width="{xb - xa + 80}" height="80" rx="14" fill="{[AA2, "#BFE3C8"][xa > 200]}" fill-opacity=".45"/>'
    s += ln(xa + 24, 72, xb - 24, 72, INK, 3) + ln(xa + 24, 88, xb - 24, 88, INK, 3)
    s += bead(xa, 80, 26, PINK) + bead(xb, 80, 26, PINK)
s += T(215, 146, '단위체 2개', 19, fill=MUTED)
s += arw(250, 128, 250, 186, 'field', 4)
xs = [100, 200, 300, 400]
s += ln(52, 240, 448, 240, INK, 3) + dots(36, 240) + dots(464, 240)
s += ''.join(bead(x, 240, 26, PINK) for x in xs)
s += T(250, 294, '고분자 — 단위체 4개 → 구슬 4개', 19, fill=MUTED)
F['MODEL_A'] = s

s = '<rect x="6" y="6" width="488" height="300" rx="16" fill="none" stroke="#9FB0C2" stroke-width="2" stroke-dasharray="7 6"/>'
for x in (95, 250, 405):
    s += ln(x - 40, 80, x + 40, 80, INK, 3)
    s += bead(x, 80, 24, PINK)
    s += f'<circle cx="{x - 44}" cy="80" r="10" fill="{EQUI}"/><circle cx="{x + 44}" cy="80" r="10" fill="{BF}"/>'
s += T(250, 140, '단위체 3개 (양 끝에 작은 부분)', 19, fill=MUTED)
s += arw(250, 150, 250, 194, 'bfield', 4)
s += ln(105, 224, 395, 224, INK, 3)
s += f'<circle cx="101" cy="224" r="10" fill="{EQUI}"/><circle cx="399" cy="224" r="10" fill="{BF}"/>'
s += ''.join(bead(x, 224, 24, PINK) for x in (150, 250, 350))
for x in (200, 300):
    s += (f'<g data-anim="move" data-from="0,-50" data-dur="1" data-delay=".4" data-ease="out">'
          f'<circle cx="{x - 10}" cy="274" r="10" fill="{BF}"/><circle cx="{x + 10}" cy="274" r="10" fill="{EQUI}"/></g>')
s += T(420, 280, '떨어져 나감', 19, fill=MUTED)
F['MODEL_B'] = s

# ═════════ S8 첨가 중합 단계 ═════════
F['ADD1'] = ethene_sf(92, 110, d=50, S=24) + ethene_sf(268, 110, d=50, S=24) + T(180, 196, '에틸렌 2분자', 19, fill=MUTED)
F['ADD2'] = (rbox(64, 92, 56, 36, EQUI, extra=' class="step" data-g="a2"') + rbox(240, 92, 56, 36, EQUI, extra=' class="step" data-g="a2"')
             + ethene_sf(92, 110, d=50, S=24, broken=True) + ethene_sf(268, 110, d=50, S=24, broken=True)
             + T(180, 196, '결합 하나가 끊어짐', 19, fill='#C26A12'))
s = rbox(122, 92, 76, 36, FIELD)
s += (f'<g data-anim="move" data-from="-22,0" data-dur=".9" data-delay=".2" data-ease="out">{chain_sf(70, 110, 2, d=60, S=24, stubR=False, vH=46)}</g>'
      f'<g data-anim="move" data-from="22,0" data-dur=".9" data-delay=".2" data-ease="out">{chain_sf(190, 110, 2, d=60, S=24, stubL=False, vH=46)}</g>')
s += ln(144, 110, 176, 110)
s += T(180, 196, '이웃 탄소끼리 새 결합', 19, fill=FIELD)
F['ADD3'] = s

# ═════════ S9 축합 중합 단계 ═════════
def blockA(x, y):
    return f'<rect x="{x}" y="{y - 22}" width="56" height="44" rx="8" fill="{AA1}" fill-opacity=".55" stroke="{INK}" stroke-width="2"/>' + T(x + 28, y + 8, '<b>A</b>', 22, fill=INK)


def blockB(x, y):
    return f'<rect x="{x}" y="{y - 22}" width="56" height="44" rx="8" fill="{AA2}" fill-opacity=".6" stroke="{INK}" stroke-width="2"/>' + T(x + 28, y + 8, '<b>B</b>', 22, fill=INK)


def con_pair(Y=112):
    s = blockA(8, Y) + sf([('C', 100, Y), ('O', 100, Y - 50), ('O', 146, Y), ('H', 184, Y)], [(0, 1, 2), (0, 2, 1), (2, 3, 1)], S=24) + ln(64, Y, 88, Y)
    s += sf([('H', 226, Y), ('O', 266, Y)], [(0, 1, 1)], S=24) + ln(278, Y, 298, Y) + blockB(298, Y)
    return s


F['CON1'] = con_pair() + T(130, 172, '$\\ce{-COOH}$', 20, fill='#C26A12') + T(246, 172, '$\\ce{-OH}$', 20, fill='#C26A12') + T(180, 204, '두 단위체의 작용기가 마주 봄', 19, fill=MUTED)
F['CON2'] = (con_pair() + ell(165, 112, 40, 22, extra=' class="step" data-g="c2"') + ell(226, 112, 18, 22, extra=' class="step" data-g="c2"')
             + water(196, 176, extra=' data-anim="move" data-from="0,-56" data-dur="1" data-delay=".2" data-ease="out"')
             + T(180, 214, '물 분자가 떨어져 나감', 19, fill=MINUS))
s = rbox(80, 52, 90, 82, FIELD)
s += blockA(8, 112) + sf([('C', 100, 112), ('O', 100, 62), ('O', 146, 112)], [(0, 1, 2), (0, 2, 1)], S=24) + ln(64, 112, 88, 112)
s += f'<g data-anim="move" data-from="60,0" data-dur=".9" data-delay=".2" data-ease="out">{ln(158, 112, 182, 112) + blockB(182, 112)}</g>'
s += T(270, 120, '+', 24, fill=INK) + water(318, 112)
s += T(150, 204, 'A와 B가 이어짐', 19, fill=FIELD)
F['CON3'] = s

# ═════════ S13 아미노산 → 두 아미노산이 이어진 분자 ═════════
def aa_reaction(open_prod=False, lab_names=True, tag=True):
    s = '<rect x="20" y="18" width="350" height="160" rx="14" fill="#E3EEFB"/><rect x="398" y="18" width="350" height="160" rx="14" fill="#FFF3D6"/>'
    s += aa_sf(40, 100, 'R1') + aa_sf(420, 100, 'R2')
    if lab_names:
        s += T(195, 205, '아미노산' if not tag else '(가)', 20, fill=MUTED) + T(573, 205, '아미노산' if not tag else '(나)', 20, fill=MUTED)
    s += ell(294, 100, 44, 24) + ell(420, 100, 18, 24)
    s += arw(384, 178, 384, 246, 'bfield', 4)
    s += T(372, 222, '축합 중합', 20, 'end', fill=BF, weight=700)
    s += water(470, 214, extra=' data-anim="move" data-from="-60,-90" data-dur="1.1" data-delay=".3" data-ease="out"')
    py = 330
    p, cx, nx = dipep_sf(70, py, open_=open_prod)
    s += f'<rect x="60" y="262" width="{f(cx - 60 + 29)}" height="128" rx="14" fill="#E3EEFB"/><rect x="{f(cx + 29)}" y="262" width="{f(560 - cx)}" height="128" rx="14" fill="#FFF3D6"/>'
    s += f'<g data-anim="fade" data-dur=".8" data-delay="1">{p}</g>'
    s += rbox(cx - 24, py - 76, nx - cx + 48, 150, FIELD, op=.10, dash=True, rx=8)
    return s, cx, nx


s, cx, nx = aa_reaction(tag=False)
s += T((cx + nx) / 2, 424, '<b>펩타이드 결합</b>', 20, fill=FIELD)
F['AA'] = s
s, cx, nx = aa_reaction(open_prod=True, tag=True)
s += T(380, 424, '(다)', 20, fill=MUTED)
F['Q07'] = s

# ═════════ S14 배열 순서 ═════════
s = ''
seqs = [[AA1, AA2, AA3, AA1, AA2, AA3, AA1], [AA3, AA1, AA1, AA2, AA3, AA2, AA2]]
for r, sq in enumerate(seqs):
    y = 60 + r * 110
    s += T(16, y + 7, f'<b>단백질 {r + 1}</b>', 20, 'start', fill=INK)
    s += ln(150, y, 150 + 58 * 6, y, '#7E8B98', 4) + dots(132, y, '#7E8B98') + dots(168 + 58 * 6, y, '#7E8B98')
    g = ''.join(bead(150 + 58 * i, y, 19, c) for i, c in enumerate(sq))
    if r == 1:
        g = f'<g data-anim="move" data-from="0,-110" data-dur="1" data-delay=".3" data-ease="out">{g}</g>'
    s += g
for i, (c, nm) in enumerate(((AA1, '아미노산 ㉮'), (AA2, '아미노산 ㉯'), (AA3, '아미노산 ㉰'))):
    x = 60 + i * 175
    s += bead(x, 250, 15, c) + T(x + 24, 257, nm, 19, 'start', fill=INK)
F['SEQ'] = s

# ═════════ S15 뉴클레오타이드 ═════════
def pent(cx, cy, r=24, col=SU):
    pts = ' '.join(f'{f(cx + r * math.cos(math.radians(-90 + 72 * k)))},{f(cy + r * math.sin(math.radians(-90 + 72 * k)))}' for k in range(5))
    return f'<polygon points="{pts}" fill="{col}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>'


def nucleo(x, y, lab=True):
    s = ln(x, y, x + 64, y, '#7E8B98', 3) + ln(x + 64, y, x + 130, y, '#7E8B98', 3)
    s += f'<circle cx="{x}" cy="{y}" r="22" fill="{PH}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>'
    s += pent(x + 64, y)
    s += f'<rect x="{x + 112}" y="{y - 17}" width="56" height="34" rx="6" fill="{BA}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>'
    if lab:
        s += T(x, y + 7, '인산', 20, fill=INK) + T(x + 64, y + 8, '당', 20, fill=INK) + T(x + 140, y + 7, '염기', 20, fill=INK)
    return s


s = nucleo(50, 70) + nucleo(50, 220)
s += T(64 + 50, 126, '$\\ce{H}$', 20, fill=INK) + T(50, 180, '$\\ce{HO}$', 20, fill=INK)
s += ell(82, 152, 50, 44)
s += water(200, 150, extra=' data-anim="move" data-from="-100,0" data-dur="1.1" data-delay=".3" data-ease="out"')
s += T(110, 290, '뉴클레오타이드 2개', 20, fill=MUTED)
s += arw(258, 196, 318, 196, 'bfield', 4) + T(288, 232, '축합 중합', 20, fill=BF, weight=700)
# 사슬
bb = [(372, 50, 'P'), (430, 98, 'S'), (372, 158, 'P'), (430, 206, 'S'), (372, 266, 'P'), (430, 314, 'S')]
s += f'<polyline points="{" ".join(f"{x},{y}" for x, y, _ in bb)}" fill="none" stroke="#7E8B98" stroke-width="3"/>'
for x, y, k in bb:
    if k == 'P':
        s += f'<circle cx="{x}" cy="{y}" r="22" fill="{PH}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>' + T(x, y + 7, '인산', 20, fill=INK)
    else:
        s += ln(x, y, x + 60, y, '#7E8B98', 3) + pent(x, y)
        s += f'<rect x="{x + 50}" y="{y - 17}" width="56" height="34" rx="6" fill="{BA}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.5"/>' + T(x, y + 8, '당', 20, fill=INK) + T(x + 78, y + 7, '염기', 20, fill=INK)
s += T(410, 360, '당–인산 골격', 20, fill=MUTED, weight=700)
F['NUC'] = s

# DNA 이중 나선 (단순화)
s = ''
y0, y1 = 20, 340
A1 = [(130 + 70 * math.sin((y - y0) / 320 * 2 * math.pi * 1.25), y) for y in range(y0, y1 + 1, 8)]
A2 = [(130 - 70 * math.sin((y - y0) / 320 * 2 * math.pi * 1.25), y) for y in range(y0, y1 + 1, 8)]
rung = ''
rc = [('#E58FB4', '#76B7E5'), ('#F2C230', '#9CC46B')]
for k, y in enumerate(range(y0 + 16, y1, 26)):
    xa = 130 + 70 * math.sin((y - y0) / 320 * 2 * math.pi * 1.25)
    xb = 130 - 70 * math.sin((y - y0) / 320 * 2 * math.pi * 1.25)
    if abs(xa - xb) < 14:
        continue
    m = (xa + xb) / 2
    c1, c2 = rc[k % 2]
    rung += ln(xa, y, m, y, c1, 7) + ln(m, y, xb, y, c2, 7)
s += f'<g data-anim="scale" data-from="0,1" data-o="130,180" data-dur="1" data-delay=".4" data-ease="out">{rung}</g>'
s += f'<polyline points="{" ".join(f"{f(x)},{f(y)}" for x, y in A1)}" fill="none" stroke="{PH}" stroke-width="7"/>'
s += f'<polyline points="{" ".join(f"{f(x)},{f(y)}" for x, y in A2)}" fill="none" stroke="#7E8B98" stroke-width="7"/>'
s += T(130, 372, 'DNA 이중 나선', 20, fill=MUTED, weight=700)
F['DNA'] = s

# ═════════ S17 폴리에틸렌 ═════════
s = ethene_sf(110, 120, d=56, S=26) + T(110, 214, '에틸렌(에텐)', 20, fill=MUTED)
s += arw(214, 120, 290, 120, 'field', 4) + T(252, 100, '첨가 중합', 19, fill=FIELD, weight=700)
s += f'<g data-anim="move" data-from="-30,0" data-dur="1" data-delay=".3" data-ease="out">{chain_sf(372, 120, 4, d=62, S=26)}</g>'
s += T(465, 214, '폴리에틸렌', 20, fill=MUTED)
s += f'<g class="step" data-g="p2">'
s += arw(636, 120, 690, 120, 'muted', 3) + T(663, 100, '간단히', 19, fill=MUTED)
s += bracket(740, 874, 54, 186) + chain_sf(776, 120, 2, d=62, S=26, stubL=False, stubR=False)
s += ln(763, 120, 720, 120) + ln(851, 120, 894, 120)
s += T(807, 214, '반복 단위를 괄호로', 19, fill=MUTED) + '</g>'
F['PE'] = s

# ═════════ S18 PET ═════════
s = tere_sf(250, 112)
s += T(250, 228, '테레프탈산', 20, fill=MUTED)
gl = [('H', 520, 112), ('O', 564, 112), ('C', 618, 112), ('C', 676, 112), ('O', 730, 112), ('H', 774, 112), ('H', 618, 64), ('H', 618, 160), ('H', 676, 64), ('H', 676, 160)]
s += sf(gl, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (2, 6, 1), (2, 7, 1), (3, 8, 1), (3, 9, 1)], S=24)
s += T(647, 228, '에틸렌 글리콜', 20, fill=MUTED)
s += ell(422, 112, 40, 22) + ell(520, 112, 18, 22)
s += arw(560, 244, 560, 300, 'bfield', 4) + T(548, 280, '축합 중합', 19, 'end', fill=BF, weight=700)
s += water(640, 274, extra=' data-anim="move" data-from="-160,-160" data-dur="1.1" data-delay=".3" data-ease="out"')
py = 380
p = tere_sf(230, py, left_open=True, right_link=True)
link = [('O', 380, py), ('C', 434, py), ('C', 492, py), ('O', 546, py), ('H', 434, py - 48), ('H', 434, py + 48), ('H', 492, py - 48), ('H', 492, py + 48)]
p += ln(343, py, 367, py) + sf(link, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (1, 4, 1), (1, 5, 1), (2, 6, 1), (2, 7, 1)], S=24)
p += ln(560, py, 588, py) + dots(604, py)
s += rbox(312, py - 70, 86, 92, FIELD, op=.10, dash=True, rx=8)
s += f'<g data-anim="fade" data-dur=".8" data-delay="1">{p}</g>'
F['PET'] = s

# ═════════ S20 고무 (반복 단위 괄호 구조식) ═════════
def rubber(x0, y0, sub='CH3', hl_anim=True, S=24):
    a = [('CH2', x0, y0), ('C', x0 + 44, y0 + 54), ('C', x0 + 124, y0 + 54), ('H2C', x0 + 170, y0), (sub, x0 + 44, y0 + 112), ('H', x0 + 124, y0 + 112)]
    b = [(0, 1, 1), (1, 2, 2), (2, 3, 1), (1, 4, 1), (2, 5, 1)]
    s = sf(a, b, S=S)
    s += ln(x0 - 28, y0, x0 - 58, y0) + ln(x0 + 198, y0, x0 + 228, y0)
    s += bracket(x0 - 44, x0 + 214, y0 - 34, y0 + 140)
    an = ' data-anim="draw" data-dur=".8" data-delay=".6"' if hl_anim else ''
    s += f'<rect x="{f(x0 + 44 - 30)}" y="{f(y0 + 112 - 22)}" width="60" height="40" rx="10" fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="2"{an}/>'
    return s


F['RUBBER'] = (rubber(80, 50) + T(165, 236, '<b>천연고무</b>', 20, fill=INK) + T(165, 262, '단위체: 아이소프렌', 19, fill=MUTED)
               + rubber(460, 50, 'Cl') + T(545, 236, '<b>네오프렌</b> (합성 고무)', 20, fill=INK) + T(545, 262, '단위체: 클로로프렌', 19, fill=MUTED))

# ═════════ S25 대단원 마무리 09 ═════════
F['Q09'] = (bracket(40, 190, 22, 158) + chain_sf(84, 90, 2, d=62, S=26, stubL=False, stubR=False)
            + ln(71, 90, 22, 90) + ln(159, 90, 208, 90))

# ═════════ S26 대단원 마무리 10 ═════════
s = rubber(70, 60, 'Cl', hl_anim=False).replace(f'fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}"', 'fill="none" stroke="none"')
s += T(155, 250, '(가) 네오프렌', 20, fill=MUTED)
s += bracket(370, 940, 4, 214) + tere_sf(530, 110, left_open=True, right_link=True, dots_=False)
s += ln(417, 110, 352, 110) + ln(643, 110, 672, 110) + TX(735, 110 + 0.36 * 24, '\\ce{OCH2CH2O}', 24) + ln(798, 110, 958, 110)
s += T(655, 250, '(나) 폴리(에틸렌 테레프탈레이트)', 20, fill=MUTED)
F['Q10'] = s

tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
miss = set(re.findall(r'@@(\w+)@@', tpl)) - set(F)
assert not miss, miss
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', len(out))
