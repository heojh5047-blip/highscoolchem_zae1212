# slides.tpl.html 의 @@이름@@ 자리에 계산한 그림 SVG를 넣어 slides.html을 만든다.
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

F = {}

def best_view(nb, nl=0, ang=None, L=100):
    """원자끼리 가장 덜 겹치는 보기 각도(yaw, pitch)"""
    bd, ld = angle_dirs(nl, nb, ang)
    best = None
    for yaw in range(-60, 61, 3):
        for pitch in (-10, -14, -18, -22):
            pts = [(0, 0)] + [(rot(norm(d), yaw, pitch)[0] * L, rot(norm(d), yaw, pitch)[1] * L) for d in bd + ld]
            m = min(math.hypot(p[0] - q[0], p[1] - q[1]) for i, p in enumerate(pts) for q in pts[i + 1:])
            if best is None or m > best[0]:
                best = (m, yaw, pitch)
    return best[1], best[2]
V4 = best_view(4)
V31 = best_view(3, 1, 107)
print('보기 각도', V4, V31)

# ── S1 표지: 메테인 공-막대 + 옅은 정사면체 테 ──
def cover():
    cx, cy, L, sc, yaw, pitch = 270, 262, 140, 1.5, 24, -14
    bd, _ = angle_dirs(0, 4)
    pts = []
    for d in bd:
        v = rot(norm(d), yaw, pitch)
        l = L * sc * 0.82
        pts.append((cx + v[0] * l, cy - v[1] * l, v[2]))
    edges = ''
    for i in range(4):
        for j in range(i + 1, 4):
            dash = ' stroke-dasharray="7 6"' if (pts[i][2] + pts[j][2]) / 2 < -0.2 else ''
            edges += f'<line x1="{f(pts[i][0])}" y1="{f(pts[i][1])}" x2="{f(pts[j][0])}" y2="{f(pts[j][1])}" stroke="#9FB0C2" stroke-width="2"{dash}/>'
    body = ballstick(cx, cy, 'C', ['H'] * 4, L=L, scale=sc, yaw=yaw, pitch=pitch, anim_out=0.45)
    return (f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
            f'<g data-anim="fade" data-dur=".8" data-delay="1.4">{edges}</g>{body}'
            f'<text class="tex" x="270" y="492" data-mix="메테인 $\\ce{{CH4}}$의 공-막대 모형" data-size="22" data-anchor="middle" fill="#5B6B7F"></text>')
F['cover'] = cover()

# ── S3 생각 열기: 일직선 물 / 굽은 물 ──
F['w_lin'] = ballstick(150, 80, 'O', ['H', 'H'], dirs=[(-1, 0, 0), (1, 0, 0)], L=110, lobes=False)
F['w_bent'] = (f'<g data-anim="rot" data-from="-14" data-o="150,62" data-dur="1.4" data-delay=".6" data-ease="soft">'
               + ballstick(150, 62, 'O', ['H', 'H'], n_lone=2, ang=104.5, L=110, lobes=False) + '</g>')

# ── S4 물의 루이스 전자점식 두 가지 ──
S = 40
def h2o_lin(x, y):
    return (lewis_sym(x, y, 'O', S, dots={'u': 2, 'd': 2, 'l': 2, 'r': 2})
            + lewis_sym(x - 1.4 * S, y, 'H', S) + lewis_sym(x + 1.4 * S, y, 'H', S))
def h2o_bent(x, y):
    return (lewis_sym(x, y, 'O', S, dots={'u': 2, 'r': 2, 'l': 2, 'd': 2})
            + lewis_sym(x - 1.4 * S, y, 'H', S) + lewis_sym(x, y + 1.5 * S, 'H', S))
F['l_h2o2'] = h2o_lin(130, 86) + h2o_bent(400, 70)

# ── S5 전자쌍 반발: 몰린 배치(점선) → 퍼진 배치 ──
def pairs_fig():
    out = ''
    def lobe(cx, cy, a, solid=True, l=78):
        t = math.radians(a)
        ux, uy = math.cos(t), -math.sin(t)
        ccx, ccy = cx + ux * l * .58, cy + uy * l * .58
        st = '' if solid else ' stroke-dasharray="5 4"'
        op = '.16' if solid else '.06'
        s = (f'<ellipse cx="{f(ccx)}" cy="{f(ccy)}" rx="{f(l * .5)}" ry="20" transform="rotate({f(-a)} {f(ccx)} {f(ccy)})" fill="#1F6FD1" fill-opacity="{op}" stroke="#1F6FD1" stroke-width="1.6"{st}/>')
        bx, by = cx + ux * l * .72, cy + uy * l * .72
        s += f'<circle cx="{f(bx - uy * 6)}" cy="{f(by + ux * 6)}" r="4" fill="#16233D"/><circle cx="{f(bx + uy * 6)}" cy="{f(by - ux * 6)}" r="4" fill="#16233D"/>'
        return s
    # 왼쪽: 한쪽에 몰린 네 전자쌍
    cx, cy = 140, 128
    for a in (60, 95, 130, 165):
        out += lobe(cx, cy, a, False)
    out += f'<g data-atom="{cx},{cy},24,X,\\mathrm{{A}}"></g>'
    out += f'<text class="tex" x="{cx}" y="246" data-mix="몰려 있으면||반발이 크다" data-size="20" data-anchor="middle" fill="#5B6B7F"></text>'
    out += '<g data-arw="262,128,318,128,ink,3"></g>'
    # 오른쪽: 고르게 퍼짐(평면 그림에서는 90°씩 — 실제는 입체)
    cx2 = 440
    for k, a in enumerate((90, 180, 270, 0)):
        frm = (60, 95, 130, 165)[k] - a
        if frm > 180: frm -= 360
        if frm < -180: frm += 360
        out += (f'<g data-anim="rot" data-from="{-frm}" data-o="{cx2},{cy}" data-dur="1.4" data-delay=".5" data-ease="out">'
                + lobe(cx2, cy, a) + '</g>')
    out += f'<g data-atom="{cx2},{cy},24,X,\\mathrm{{A}}"></g>'
    out += f'<text class="tex" x="{cx2}" y="246" data-mix="가능한 한||멀리 떨어진다" data-size="20" data-anchor="middle" fill="#1F6FD1"></text>'
    return out
F['pairs'] = pairs_fig()

# ── S6 풍선 ──
def balloon(cx, cy, a, l=70, z=0, col='#CFE3F7', stroke='#6E9CCB'):
    t = math.radians(a)
    ux, uy = math.cos(t), -math.sin(t)
    ccx, ccy = cx + ux * l * .58, cy + uy * l * .58
    rx = l * .52
    return f'<ellipse cx="{f(ccx)}" cy="{f(ccy)}" rx="{f(rx)}" ry="24" transform="rotate({f(-a)} {f(ccx)} {f(ccy)})" fill="{col}" stroke="{stroke}" stroke-width="2"/>'
def balloons(angles3d, yaw=0, pitch=0, cx=150, cy=105, l=80, label=''):
    items = []
    for d in angles3d:
        v = rot(norm(d), yaw, pitch)
        a = math.degrees(math.atan2(v[1], v[0]))
        ll = l * max(0.45, math.hypot(v[0], v[1]))
        col = '#CFE3F7' if v[2] >= -0.1 else '#E3EEF8'
        items.append((v[2], balloon(cx, cy, a, ll, col=col)))
    items.sort()
    body = ''.join(s for _, s in items)
    return (f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".9" data-delay=".4" data-ease="back">{body}'
            f'<circle cx="{cx}" cy="{cy}" r="7" fill="#6E9CCB"/></g>')
F['bal2'] = balloons([(-1, 0, 0), (1, 0, 0)])
F['bal3'] = balloons(angle_dirs(0, 3)[0])
F['bal4'] = balloons(angle_dirs(0, 4)[0], yaw=20, pitch=-12)

# ── S7 전자쌍 배치 3가지 (전자쌍 구름만) ──
def pair_geo(nb, yaw=0, pitch=0, cx=150, cy=110):
    d, _ = angle_dirs(0, nb)
    return ballstick(cx, cy, 'X', [], L=118, dirs=[], lone_dirs=d, yaw=yaw, pitch=pitch, lobe_col='#1F6FD1')
F['g2'] = pair_geo(2)
F['g3'] = pair_geo(3)
F['g4'] = pair_geo(4, 22, -14)

# ── S8 평면 CH4(90°) vs 쐐기 CH4(109.5°) ──
def flat_ch4(cx=150, cy=120):
    out = ''
    for a in (0, 90, 180, 270):
        t = math.radians(a); ux, uy = math.cos(t), -math.sin(t)
        out += f'<line x1="{f(cx + ux * 18)}" y1="{f(cy + uy * 18)}" x2="{f(cx + ux * 72)}" y2="{f(cy + uy * 72)}" stroke="#16233D" stroke-width="3.5" stroke-linecap="round"/>'
        out += f'<text class="tex" x="{f(cx + ux * 90)}" y="{f(cy + uy * 90 + 10.8)}" data-tex="\\mathrm{{H}}" data-size="30" data-anchor="middle"></text>'
    out += f'<text class="tex" x="{cx}" y="{f(cy + 10.8)}" data-tex="\\mathrm{{C}}" data-size="30" data-anchor="middle"></text>'
    out += f'<path d="M{cx + 40} {cy} A40 40 0 0 0 {cx} {cy - 40}" fill="none" stroke="#5B6B7F" stroke-width="2"/>'
    out += f'<text class="tex" x="{cx + 52}" y="{cy - 40}" data-tex="90^\\circ" data-size="22" data-halo="1"></text>'
    return out
F['flat_ch4'] = flat_ch4()
def wedge_ch4(cx=150, cy=118, arc=True):
    out = wedge(cx, cy, 'C', [(90, 'l', 'H'), (205, 'l', 'H'), (-20, 'w', 'H'), (-60, 'd', 'H')], L=92)
    if arc:
        r = 40
        a1, a2 = math.radians(90), math.radians(205)
        out += (f'<path d="M{f(cx + r * math.cos(a1))} {f(cy - r * math.sin(a1))} A{r} {r} 0 0 0 {f(cx + r * math.cos(a2))} {f(cy - r * math.sin(a2))}" fill="none" stroke="#5B6B7F" stroke-width="2" data-anim="draw" data-dur=".8" data-delay=".4"/>'
                f'<text class="tex" x="{f(cx - 64)}" y="{f(cy - 40)}" data-tex="109.5^\\circ" data-size="22" data-anchor="middle" data-halo="1"></text>')
    return out
F['wedge_ch4'] = wedge_ch4()

# ── S9–S11 공유 전자쌍만 ──
def lw_bef2(x=230, y=90):
    return (lewis_sym(x, y, 'Be', S) + dot_pair(x - 40, y, 'v') + dot_pair(x + 40, y, 'v')
            + lewis_sym(x - 68, y, 'F', S, dots={'u': 2, 'd': 2, 'l': 2})
            + lewis_sym(x + 68, y, 'F', S, dots={'u': 2, 'd': 2, 'r': 2}))
F['lw_bef2'] = lw_bef2() + hl_box(190, 90, 22, 34, 'shared', 'h9') + hl_box(270, 90, 22, 34, 'shared', 'h9')
# (Be 기호가 두 글자라 F를 1.6S 떨어뜨림: 공유 전자쌍은 Be의 왼쪽·오른쪽 자리 ±0.70S → 가운데 보정은 아래 수동 배치로)
F['m_bef2'] = ballstick(240, 105, 'Be', ['F', 'F'], L=135, arc=(0, 1), arc_label='180^\\circ', anim_out=.35, arc_r=46)
def lw_bf3(x=230, y=78):
    return (lewis_sym(x, y, 'B', S, dots={'l': 2, 'r': 2, 'd': 2})
            + lewis_sym(x - 1.4 * S, y, 'F', S, dots={'u': 2, 'd': 2, 'l': 2})
            + lewis_sym(x + 1.4 * S, y, 'F', S, dots={'u': 2, 'd': 2, 'r': 2})
            + lewis_sym(x, y + 1.5 * S, 'F', S, dots={'l': 2, 'r': 2, 'd': 2}))
F['lw_bf3'] = lw_bf3() + ''.join(hl_box(*p, 'shared', 'h10') for p in [(230 - 28, 78, 22, 34), (230 + 28, 78, 22, 34), (230, 78 + 30, 34, 22)])
F['m_bf3'] = ballstick(240, 150, 'B', ['F', 'F', 'F'], L=118, arc=(1, 2), arc_label='120^\\circ', anim_out=.35, arc_r=48)
def lw_ch4(x=230, y=110):
    return (lewis_sym(x, y, 'C', S, dots={'l': 2, 'r': 2, 'u': 2, 'd': 2}) + lewis_sym(x - 1.4 * S, y, 'H', S)
            + lewis_sym(x + 1.4 * S, y, 'H', S) + lewis_sym(x, y - 1.5 * S, 'H', S) + lewis_sym(x, y + 1.5 * S, 'H', S))
F['lw_ch4'] = lw_ch4() + ''.join(hl_box(*p, 'shared', 'h11') for p in [(202, 110, 22, 34), (258, 110, 22, 34), (230, 80, 34, 22), (230, 140, 34, 22)])
F['m_ch4'] = ballstick(170, 115, 'C', ['H'] * 4, L=118, yaw=V4[0], pitch=V4[1], arc='auto', arc_label='109.5^\\circ', anim_out=.35, arc_r=44)
F['w_ch4b'] = wedge_ch4(cx=120, cy=118, arc=False)

# ── S13 NH3 루이스 ──
def lw_nh3(x, y, g=None):
    s = (lewis_sym(x, y, 'N', S, dots={'u': 2, 'l': 2, 'r': 2, 'd': 2}) + lewis_sym(x - 1.4 * S, y, 'H', S)
         + lewis_sym(x + 1.4 * S, y, 'H', S) + lewis_sym(x, y + 1.5 * S, 'H', S))
    if g:
        s += ''.join(hl_box(*p, 'shared', g) for p in [(x - 28, y, 22, 34), (x + 28, y, 22, 34), (x, y + 30, 34, 22)])
        s += hl_box(x, y - 30, 34, 22, 'lone', g)
    return s
F['lw_nh3_13'] = lw_nh3(150, 92, 'h13')
F['lw_nh3'] = lw_nh3(150, 92, 'h15')
def lw_h2o(x, y, g=None):
    s = (lewis_sym(x, y, 'O', S, dots={'u': 2, 'r': 2, 'l': 2, 'd': 2}) + lewis_sym(x - 1.4 * S, y, 'H', S) + lewis_sym(x, y + 1.5 * S, 'H', S))
    if g:
        s += ''.join(hl_box(*p, 'shared', g) for p in [(x - 28, y, 22, 34), (x, y + 30, 34, 22)])
        s += hl_box(x, y - 30, 34, 22, 'lone', g) + hl_box(x + 28, y, 22, 34, 'lone', g)
    return s
F['lw_h2o'] = lw_h2o(170, 92, 'h16')

# ── S14 공유 전자쌍 vs 비공유 전자쌍 로브 ──
def lobe_cmp():
    out = ''
    # 공유 전자쌍: 두 원자핵 사이에 가늘고 길게
    out += '<ellipse cx="130" cy="80" rx="62" ry="17" fill="#2E9E6A" fill-opacity=".18" stroke="#2E9E6A" stroke-width="1.5"/>'
    out += '<g data-atom="60,80,24,X,\\mathrm{A}"></g><g data-atom="200,80,24,X,\\mathrm{B}"></g>'
    out += '<circle cx="124" cy="80" r="4" fill="#16233D"/><circle cx="136" cy="80" r="4" fill="#16233D"/>'
    out += '<text class="tex" x="130" y="142" data-mix="공유 전자쌍||두 원자핵이 끌어 가늘다" data-size="19" data-anchor="middle" fill="#2E9E6A"></text>'
    # 비공유 전자쌍: 한 원자핵 가까이 짧고 넓게
    out += '<g data-anim="scale" data-from=".55" data-o="330,80" data-dur="1.2" data-delay=".4" data-ease="out"><ellipse cx="370" cy="80" rx="42" ry="34" fill="#E08A2C" fill-opacity=".18" stroke="#E08A2C" stroke-width="1.5"/>'
    out += '<circle cx="388" cy="73" r="4" fill="#16233D"/><circle cx="388" cy="87" r="4" fill="#16233D"/></g>'
    out += '<g data-atom="330,80,24,X,\\mathrm{A}"></g>'
    out += '<text class="tex" x="370" y="142" data-mix="비공유 전자쌍||한 원자핵만 끌어 넓게 퍼진다" data-size="19" data-anchor="middle" fill="#B5661B"></text>'
    return out
F['lobe_cmp'] = lobe_cmp()

# ── S15, S16 모형 ──
F['m_nh3'] = ballstick(200, 120, 'N', ['H'] * 3, n_lone=1, ang=107, L=118, yaw=V31[0], pitch=V31[1], arc='auto', arc_label='107^\\circ', arc_r=44)
F['m_h2o'] = ballstick(200, 120, 'O', ['H'] * 2, n_lone=2, ang=104.5, L=118, yaw=28, pitch=-6, arc='auto', arc_label='104.5^\\circ', arc_r=44)
F['m_nh3a'] = '<g data-anim="rot" data-from="-10" data-o="200,120" data-dur="1.6" data-delay=".3" data-ease="soft">' + F['m_nh3'].split('<g><path')[0] + '</g>' + '<g><path' + F['m_nh3'].split('<g><path')[1]
F['m_h2oa'] = '<g data-anim="rot" data-from="10" data-o="200,120" data-dur="1.6" data-delay=".3" data-ease="soft">' + F['m_h2o'].split('<g><path')[0] + '</g>' + '<g><path' + F['m_h2o'].split('<g><path')[1]

# ── S14 압축 그림: 비공유 전자쌍이 결합을 민다 ──
def squeeze():
    cx, cy = 150, 70
    out = '<ellipse cx="150" cy="38" rx="30" ry="36" fill="#E08A2C" fill-opacity=".18" stroke="#E08A2C" stroke-width="1.5"/><circle cx="143" cy="20" r="4" fill="#16233D"/><circle cx="157" cy="20" r="4" fill="#16233D"/>'
    for sgn in (-1, 1):
        a = math.radians(-90 + sgn * 53.5)
        ex, ey = cx + math.cos(a) * 110, cy - math.sin(a) * 110
        a0 = math.radians(-90 + sgn * 54.75)
        dx0, dy0 = cx + math.cos(a0) * 110, cy - math.sin(a0) * 110
        out += f'<line x1="{cx}" y1="{cy}" x2="{f(dx0)}" y2="{f(dy0)}" stroke="#9AA5B1" stroke-width="3" stroke-dasharray="6 5"/>'
        out += (f'<g data-anim="rot" data-from="{-sgn * 8}" data-o="{cx},{cy}" data-dur="1.3" data-delay=".8" data-ease="out">'
                f'<line x1="{cx}" y1="{cy}" x2="{f(ex)}" y2="{f(ey)}" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/><g data-atom="{f(ex)},{f(ey)},18,H"></g></g>')
    out += f'<g data-atom="{cx},{cy},24,N"></g>'
    return out
F['squeeze'] = squeeze()

# ── S17 비교 카드 ──
F['c_ch4'] = ballstick(160, 86, 'C', ['H'] * 4, L=92, yaw=V4[0], pitch=V4[1], arc='auto', arc_label='109.5^\\circ', arc_r=36, arc_size=19)
F['c_nh3'] = ballstick(160, 86, 'N', ['H'] * 3, n_lone=1, ang=107, L=92, yaw=V31[0], pitch=V31[1], arc='auto', arc_label='107^\\circ', arc_r=36, arc_size=19)
F['c_h2o'] = ballstick(160, 86, 'O', ['H'] * 2, n_lone=2, ang=104.5, L=92, yaw=28, pitch=-6, arc='auto', arc_label='104.5^\\circ', arc_r=36, arc_size=19)

# ── S18 CO2, HCN 루이스 구조(결합선) ──
def bondline(x1, y1, x2, y2, order=1, sh=14):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy); ux, uy = dx / n, dy / n; px, py = -uy, ux
    a1x, a1y, a2x, a2y = x1 + ux * sh, y1 + uy * sh, x2 - ux * sh, y2 - uy * sh
    offs = {1: [0], 2: [-5, 5], 3: [-8, 0, 8]}[order]
    return ''.join(f'<line x1="{f(a1x + px * o)}" y1="{f(a1y + py * o)}" x2="{f(a2x + px * o)}" y2="{f(a2y + py * o)}" stroke="#16233D" stroke-width="3" stroke-linecap="round"/>' for o in offs)
def ls_co2(x=200, y=60, D=96):
    return (bondline(x - D, y, x, y, 2, 22) + bondline(x, y, x + D, y, 2, 22)
            + lewis_sym(x, y, 'C', S) + lewis_sym(x - D, y, 'O', S, dots={'u': 2, 'd': 2}) + lewis_sym(x + D, y, 'O', S, dots={'u': 2, 'd': 2}))
F['ls_co2'] = ls_co2()
F['m_co2'] = '<g data-anim="draw" data-dur="1" data-delay=".3">' + ballstick(200, 70, 'C', ['O', 'O'], L=120, extra_bond_orders={0: 2, 1: 2}) + '</g>'
def ls_hcn(x=200, y=60, D=96):
    return (bondline(x - D, y, x, y, 1, 22) + bondline(x, y, x + D, y, 3, 22)
            + lewis_sym(x, y, 'C', S) + lewis_sym(x - D, y, 'H', S) + lewis_sym(x + D, y, 'N', S, dots={'r': 2}))
F['ls_hcn'] = ls_hcn()
F['m_hcn'] = '<g data-anim="draw" data-dur="1" data-delay=".3">' + ballstick(200, 70, 'C', ['H', 'N'], L=120, extra_bond_orders={1: 3}) + '</g>'

# ── S19 HCHO ──
def ls_hcho(x=150, y=150, D=96):
    return (bondline(x, y, x, y - D, 2, 22) + bondline(x - D, y, x, y, 1, 22) + bondline(x, y, x + D, y, 1, 22)
            + lewis_sym(x, y, 'C', S) + lewis_sym(x, y - D, 'O', S, dots={'l': 2, 'r': 2}) + lewis_sym(x - D, y, 'H', S) + lewis_sym(x + D, y, 'H', S))
F['ls_hcho'] = ls_hcho()
F['m_hcho'] = '<g data-anim="pop" data-o="200,150" data-dur=".9" data-delay=".3" data-ease="back">' + ballstick(200, 150, 'C', ['O', 'H', 'H'], L=118, extra_bond_orders={0: 2}, arc=(0, 1), arc_label='\\text{약 }120^\\circ', arc_r=48) + '</g>'

# ── S21 OF2 루이스 ──
def lw_of2(x=210, y=80):
    return (lewis_sym(x, y, 'O', S, dots={'u': 2, 'd': 2, 'l': 2, 'r': 2})
            + lewis_sym(x - 1.4 * S, y, 'F', S, dots={'u': 2, 'd': 2, 'l': 2}) + lewis_sym(x + 1.4 * S, y, 'F', S, dots={'u': 2, 'd': 2, 'r': 2})
            + hl_box(x - 28, y, 22, 34, 'shared', 'e1') + hl_box(x + 28, y, 22, 34, 'shared', 'e1')
            + hl_box(x, y - 30, 34, 22, 'lone', 'e1') + hl_box(x, y + 30, 34, 22, 'lone', 'e1'))
F['lw_of2'] = lw_of2()
F['m_of2'] = ballstick(210, 70, 'O', ['F', 'F'], n_lone=2, ang=103, L=110, yaw=28, pitch=-6, lobes=True)

# ── S28 확인 문제 01 세 모형 ──
F['q_bf3'] = ballstick(100, 112, 'B', ['F'] * 3, L=82)
F['q_nh3'] = ballstick(295, 98, 'N', ['H'] * 3, n_lone=1, ang=107, L=82, yaw=V31[0], pitch=V31[1])
F['q_ch4'] = ballstick(485, 104, 'C', ['H'] * 4, L=82, yaw=V4[0], pitch=V4[1])

import glob
D = os.path.dirname(os.path.abspath(__file__))
tpl = ''.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob(os.path.join(D, 'tpl*.html'))))
miss = set(re.findall(r'@@(\w+)@@', tpl)) - set(F)
if miss: raise SystemExit('없는 그림: ' + ', '.join(sorted(miss)))
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('slides.html', len(out), 'bytes,', out.count('<section'), 'slides')
