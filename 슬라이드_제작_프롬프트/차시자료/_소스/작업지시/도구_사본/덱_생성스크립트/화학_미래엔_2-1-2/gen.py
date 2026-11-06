# 2-1-2 그림 생성 — slides.tpl.html 의 {{이름}} 자리에 SVG 조각을 넣어 slides.html 을 만든다.
import math, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/2-1-2_전기음성도와_결합의_극성/slides.html'
R = {'H': 18, 'C': 24, 'N': 24, 'O': 24, 'F': 24, 'Cl': 29, 'S': 29, 'Na': 32, 'Li': 30, 'X': 24}
PLUS, MINUS, MUTED, INK, FIELD, EQUI = '#D7263D', '#1F6FD1', '#5B6B7F', '#16233D', '#2E9E6A', '#E08A2C'
BOND = '#9AA5B1'
EN = {'H': 2.2, 'Li': 1.0, 'Be': 1.6, 'B': 2.0, 'C': 2.6, 'N': 3.0, 'O': 3.4, 'F': 4.0,
      'Na': 0.9, 'Mg': 1.3, 'Al': 1.6, 'Si': 1.9, 'P': 2.2, 'S': 2.6, 'Cl': 3.2,
      'K': 0.8, 'Ca': 1.0, 'Ga': 1.8, 'Ge': 2.0, 'As': 2.0, 'Se': 2.6, 'Br': 3.0,
      'Rb': 0.8, 'Sr': 1.0, 'In': 1.8, 'Sn': 2.0, 'Sb': 2.1, 'Te': 2.1, 'I': 2.7}

def f(v):
    s = ('%.1f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def tex(x, y, t, size=20, anchor='middle', fill=None, mix=False, extra=''):
    a = 'data-mix' if mix else 'data-tex'
    fl = f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {a}="{t}" data-size="{size}" data-anchor="{anchor}"{fl}{extra}></text>'

def atom(x, y, el, r=None, lab=None, sc=1.0):
    r = (r or R.get(el, 24)) * sc
    s = f'{f(x)},{f(y)},{f(r)},{el}'
    if lab is not None: s += ',' + lab
    return f'<g data-atom="{s}"></g>'

def bond(x1, y1, x2, y2, n=1, w=7, gap=9):
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    out = []
    for k in range(n):
        o = (k - (n - 1) / 2) * gap
        out.append(f'<line x1="{f(x1+nx*o)}" y1="{f(y1+ny*o)}" x2="{f(x2+nx*o)}" y2="{f(y2+ny*o)}" stroke="{BOND}" stroke-width="{w if n==1 else 5}" stroke-linecap="round"/>')
    return ''.join(out)

def dip(x1, y1, x2, y2, color='ink', w=3, extra=''):
    """쌍극자 모멘트 화살표 ⟼ : (x1,y1)=δ+ 쪽 꼬리, (x2,y2)=δ− 쪽 머리. 꼬리 15% 지점에 수직 막대 14."""
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    tx, ty = x1 + ux * L * 0.15, y1 + uy * L * 0.15
    c = PLUS if color == 'plus' else INK
    return (f'<g{extra}><g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{color},{w}"></g>'
            f'<line x1="{f(tx+nx*7)}" y1="{f(ty+ny*7)}" x2="{f(tx-nx*7)}" y2="{f(ty-ny*7)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/></g>')

def pair(x, y, vertical=True, r=4.5, gap=6.5):
    if vertical:
        return f'<circle cx="{f(x)}" cy="{f(y-gap)}" r="{r}" fill="{INK}"/><circle cx="{f(x)}" cy="{f(y+gap)}" r="{r}" fill="{INK}"/>'
    return f'<circle cx="{f(x-gap)}" cy="{f(y)}" r="{r}" fill="{INK}"/><circle cx="{f(x+gap)}" cy="{f(y)}" r="{r}" fill="{INK}"/>'

def dl(x, y, s, size=24):
    return tex(x, y, '\\delta^' + ('+' if s == '+' else '-'), size, 'middle', PLUS if s == '+' else MINUS)

def cloud(cx, cy, rx, ry, op=.16):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="#8C99A6" fill-opacity="{op}" stroke="#8C99A6" stroke-width="1.5" stroke-dasharray="5 4"/>'

def diatomic(x1, x2, y, a, b, shift=0, cl=True, n=1, deltas=True, anim=False, dsize=24, pair_on=True):
    """두 원자 공-막대 + 공유 전자쌍(가운데에서 shift 만큼 b 쪽으로)."""
    s = ''
    mid = (x1 + x2) / 2
    if cl:
        rx = (x2 - x1) / 2 + R[a] * 0.4 + abs(shift) * 0.35
        c = cloud(mid + shift * 0.8, y, rx + 10, max(R[a], R[b]) + 12)
        if anim and shift:
            c = f'<g data-anim="move" data-from="{f(-shift*0.8)},0" data-dur="1.4" data-delay=".4" data-ease="soft">{c}</g>'
        s += c
    s += bond(x1, y, x2, y, n) + atom(x1, y, a) + atom(x2, y, b)
    if pair_on:
        p = pair(mid + shift, y)
        if anim and shift:
            p = f'<g data-anim="move" data-from="{f(-shift)},0" data-dur="1.4" data-delay=".4" data-ease="soft">{p}</g>'
        s += p
    if deltas and shift:
        sg = 1 if shift > 0 else -1
        s += dl(x1, y - R[a] - 14, '+' if sg > 0 else '-', dsize) + dl(x2, y - R[b] - 14, '-' if sg > 0 else '+', dsize)
    return s

def svg(vb, w, label, body, style=''):
    return f'<svg class="fig" viewBox="0 0 {vb[0]} {vb[1]}" style="width:{w}px{";" + style if style else ""}" aria-label="{label}">{body}</svg>'

F = {}

# ── S1 표지: HCl (1.5배)
def cover():
    sc = 1.5; y = 150; xh, xc = 110, 330
    s = cloud(240, y, 165, 66)
    s += bond(xh, y, xc, y, w=10) + atom(xh, y, 'H', sc=sc) + atom(xc, y, 'Cl', sc=sc)
    s += f'<circle cx="250" cy="{y}" r="22" fill="{FIELD}" fill-opacity=".18" stroke="{FIELD}" stroke-width="1.5"/>'
    s += f'<g data-anim="move" data-from="-30,0" data-dur="1.6" data-delay=".5" data-ease="soft">{pair(250, y, r=5.5, gap=8)}</g>'
    s += dl(xh, 92, '+', 30) + dl(xc, 72, '-', 30)
    s += dip(150, 262, 330, 262, w=4)
    s += tex(240, 306, '\\ce{HCl}', 26)
    return '<svg class="cover-fig" viewBox="0 0 540 540" aria-label="염화 수소 분자에서 공유 전자쌍이 염소 쪽으로 치우치는 그림"><g transform="translate(40,100)">' + s + '</g></svg>' if True else svg((460, 320), 460, '염화 수소 분자에서 공유 전자쌍이 염소 쪽으로 치우치고, 수소는 부분적인 양전하, 염소는 부분적인 음전하를 띠며 쌍극자 모멘트 화살표가 수소에서 염소를 향하는 그림', s)
F['cover'] = cover()

# ── S3 줄다리기
def tug():
    s = ''
    for k, (y, kx, fl, fr, cap) in enumerate([(70, 280, 40, 40, '두 쪽 힘이 같다 → 매듭은 가운데'), (190, 345, 26, 70, '오른쪽 힘이 크다 → 매듭이 오른쪽으로')]):
        s += f'<line x1="280" y1="{y-34}" x2="280" y2="{y+20}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="5 4"/>'
        s += f'<line x1="110" y1="{y}" x2="450" y2="{y}" stroke="#B08B57" stroke-width="7" stroke-linecap="round"/>'
        knot = f'<circle cx="{kx}" cy="{y}" r="11" fill="{PLUS}"/>'
        if kx == 280:
            knot = f'<g data-anim="move" data-from="4,0" data-rep="swing" data-dur=".9">{knot}</g>'
        else:
            knot = f'<g data-anim="move" data-from="{280-kx},0" data-dur="1.6" data-delay=".5" data-ease="soft">{knot}</g>'
        s += knot
        s += f'<g data-arw="100,{y},{100-fl},{y},ink,{4 if fl<60 else 6}"></g><g data-arw="460,{y},{460+fr},{y},ink,{4 if fr<60 else 6}"></g>'
        s += tex(280, y + 50, cap, 20, mix=True, fill=MUTED)
    s += tex(56, 30, '당기는 힘', 19, mix=True, fill=MUTED) + tex(504, 30, '당기는 힘', 19, mix=True, fill=MUTED)
    return svg((560, 260), 520, '줄다리기에서 두 쪽 힘이 같으면 매듭이 가운데, 오른쪽 힘이 크면 매듭이 오른쪽으로 치우치는 그림', s)
F['tug'] = tug()

# ── S4 H2, O2, H2O
def three():
    y = 90; s = ''
    s += diatomic(50, 130, y, 'H', 'H', cl=False, deltas=False)
    s += tex(90, 170, '수소($\\ce{H2}$)', 20, mix=True)
    s += bond(220, y, 310, y, 2) + atom(220, y, 'O') + atom(310, y, 'O') + pair(257, y) + pair(273, y)
    s += tex(265, 170, '산소($\\ce{O2}$)', 20, mix=True)
    ox, oy = 490, 70; L = 80; a = math.radians(52.25)
    hx1, hy1 = ox - L * math.sin(a), oy + L * math.cos(a); hx2 = ox + L * math.sin(a)
    s += bond(ox, oy, hx1, hy1) + bond(ox, oy, hx2, hy1) + atom(hx1, hy1, 'H') + atom(hx2, hy1, 'H') + atom(ox, oy, 'O')
    # O–H 공유 전자쌍: 가운데 → O 쪽
    for hx in (hx1, hx2):
        mx, my = (ox + hx) / 2, (oy + hy1) / 2; tx, ty = mx + (ox - mx) * 0.38, my + (oy - my) * 0.38
        p = f'<circle cx="{f(tx-4)}" cy="{f(ty-4)}" r="4.5" fill="{INK}"/><circle cx="{f(tx+4)}" cy="{f(ty+4)}" r="4.5" fill="{INK}"/>' if hx < ox else f'<circle cx="{f(tx-4)}" cy="{f(ty+4)}" r="4.5" fill="{INK}"/><circle cx="{f(tx+4)}" cy="{f(ty-4)}" r="4.5" fill="{INK}"/>'
        s += f'<g class="step" data-g="w1"><g data-anim="move" data-from="{f(mx-tx)},{f(my-ty)}" data-dur="1.2" data-ease="soft" data-on="step">{p}</g></g>'
    s += tex(490, 170, '물($\\ce{H2O}$)', 20, mix=True)
    s += tex(178, 205, '같은 원자: 공유 전자쌍이 가운데', 19, mix=True, fill=MUTED)
    s += tex(490, 205, '다른 원자: 어느 쪽으로?', 19, mix=True, fill=MUTED)
    return svg((600, 220), 600, '수소와 산소 분자에서는 공유 전자쌍이 두 원자 가운데에 있고, 물 분자에서는 산소 쪽으로 치우치는 그림', s)
F['three'] = three()

# ── S5 F–H 끌어당김
def pull():
    y = 80; xh, xf = 110, 330; px = 255
    s = cloud(235, y, 150, 44)
    s += bond(xh, y, xf, y) + atom(xh, y, 'H') + atom(xf, y, 'F') + pair(px, y)
    s += f'<g data-arw="{px-14},{y+52},{xh+10},{y+52},muted,2.5"></g>'
    s += f'<g data-anim="scale" data-from="0.3,1" data-o="{px+14},{y+52}" data-dur="1.2" data-delay=".4"><g data-arw="{px+14},{y+52},{xf-6},{y+52},field,6"></g></g>'
    s += tex(170, y + 86, '약하게 당김', 19, mix=True, fill=MUTED) + tex(300, y + 86, '세게 당김', 19, mix=True, fill=FIELD)
    s += tex(xh, 34, '2.2', 20, fill=MUTED) + tex(xf, 30, '4.0', 20, fill=MUTED)
    return svg((440, 190), 420, '수소와 플루오린이 공유 전자쌍을 당기는데 플루오린이 더 세게 당겨 공유 전자쌍이 플루오린 쪽에 가까운 그림', s)
F['pull'] = pull()

# ── S6 전기음성도 표 (1·2·13–17족, 1–5주기)
def ptable():
    groups = [1, 2, None, 13, 14, 15, 16, 17]
    rows = [['H', None, None, None, None, None, None, None],
            ['Li', 'Be', None, 'B', 'C', 'N', 'O', 'F'],
            ['Na', 'Mg', None, 'Al', 'Si', 'P', 'S', 'Cl'],
            ['K', 'Ca', None, 'Ga', 'Ge', 'As', 'Se', 'Br'],
            ['Rb', 'Sr', None, 'In', 'Sn', 'Sb', 'Te', 'I']]
    X0, Y0, CW, CH, GW = 58, 42, 92, 64, 72
    def col_x(j):
        x = X0
        for k in range(j):
            x += GW if groups[k] is None else CW
        return x
    def colr(v):
        t = max(0, min(1, (v - 0.7) / 3.3))
        c1, c2 = (0xFF, 0xF6, 0xD2), (0xF0, 0x9A, 0x55)
        return '#%02X%02X%02X' % tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))
    s = tex(20, 26, '족', 19, fill=MUTED) + tex(20, 52, '', 1)
    s = tex(28, 28, '주기＼족', 18, mix=True, fill=MUTED)
    s = ''
    for j, g in enumerate(groups):
        if g is None: continue
        s += tex(col_x(j) + CW / 2 - 4, 30, str(g), 20, fill=MUTED)
    for i, row in enumerate(rows):
        y = Y0 + i * CH
        s += tex(28, y + CH / 2 + 7, str(i + 1), 20, fill=MUTED)
        for j, el in enumerate(row):
            if not el: continue
            x = col_x(j)
            s += f'<rect x="{x+2}" y="{y+2}" width="{CW-6}" height="{CH-6}" rx="8" fill="{colr(EN[el])}" stroke="#E2C48A" stroke-width="1.2"/>'
            s += tex(x + CW / 2 - 1, y + 29, '\\mathrm{' + el + '}', 24)
            s += tex(x + CW / 2 - 1, y + 53, f'{EN[el]:.1f}', 19, fill=INK)
    gx = col_x(2)
    s += f'<rect x="{gx+4}" y="{Y0+CH*3+2}" width="{GW-8}" height="{CH*2-6}" rx="8" fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="5 4"/>'
    s += tex(gx + GW / 2, Y0 + CH * 4 - 6, '전이||원소||생략', 18, mix=True, fill=MUTED)
    s += tex(28, 22, '', 1) if False else ''
    s += tex(col_x(0) - 30, 24, '주기', 18, mix=True, fill=MUTED, extra=' data-anchor="middle"').replace('data-anchor="middle" data-anchor="middle"', 'data-anchor="middle"') if False else ''
    return svg((760, 370), 740, '1주기부터 5주기까지 1족, 2족, 13족부터 17족 원소의 전기음성도 값 표. 플루오린이 4.0으로 가장 크다', s)
F['ptable'] = ptable()

# ── S10 주기성 경향 화살표
def trend():
    X0, Y0, CW, CH = 40, 70, 54, 46
    s = ''
    for i in range(4):
        for j in range(7):
            fill = '#F6C177' if (i == 1 and j == 6) else '#FFF6D2'
            s += f'<rect x="{X0+j*CW+2}" y="{Y0+i*CH+2}" width="{CW-4}" height="{CH-4}" rx="6" fill="{fill}" stroke="#E2C48A" stroke-width="1.2"/>'
    s += tex(X0 + 6 * CW + CW / 2, Y0 + CH + 31, '\\mathrm{F}', 24)
    s += f'<g data-arw="{X0+6},{Y0-22},{X0+7*CW},{Y0-22},field,5"></g>'
    s += tex(X0 + 3.5 * CW, Y0 - 36, '같은 주기: 오른쪽으로 갈수록 증가', 19, mix=True, fill=FIELD)
    s += f'<g data-arw="{X0+7*CW+28},{Y0+4*CH},{X0+7*CW+28},{Y0+4},field,5"></g>'
    s += tex(X0 + 7 * CW + 48, Y0 + 2 * CH - 12, '같은 족:||위로||갈수록||증가', 19, mix=True, fill=FIELD, extra='').replace('data-anchor="middle"', 'data-anchor="start"')
    s += tex(X0 + 3.5 * CW, Y0 + 4 * CH + 30, '화살표 = 전기음성도가 커지는 방향 (18족 제외)', 18, mix=True, fill=MUTED)
    return svg((560, 330), 520, '주기율표에서 같은 주기는 오른쪽으로 갈수록, 같은 족은 위로 갈수록 전기음성도가 증가해 플루오린 쪽이 가장 크다는 경향 화살표 그림', s)
F['trend'] = trend()

# ── S12 H–H, H–F, H–Cl 모형
def hx3():
    s = ''
    for k, b in enumerate(['H', 'F', 'Cl']):
        cx = 100 + k * 200
        s += bond(cx - 45, 60, cx + 45, 60) + atom(cx - 45, 60, 'H') + atom(cx + 45, 60, b)
        s += tex(cx, 128, '\\ce{H-' + b + '}', 22)
    return svg((600, 140), 600, '수소, 플루오린화 수소, 염화 수소 분자의 공-막대 모형', s)
F['hx3'] = hx3()

# ── S15 H2 / HCl
def h2fig():
    return svg((300, 140), 300, '수소 분자: 공유 전자쌍이 두 원자 가운데에 있다', diatomic(95, 205, 80, 'H', 'H', deltas=False, cl=True))
def hclfig():
    s = diatomic(90, 210, 80, 'H', 'Cl', shift=20, anim=True)
    return svg((300, 140), 300, '염화 수소 분자: 공유 전자쌍이 염소 쪽으로 치우치고, 수소는 부분적인 양전하, 염소는 부분적인 음전하를 띤다', s)
F['h2fig'] = h2fig(); F['hclfig'] = hclfig()

# ── S16 H–F vs H–Cl
def hfhcl():
    s = ''
    for k, (b, d) in enumerate([('F', 1.8), ('Cl', 1.0)]):
        cx = 150 + k * 300; x1, x2 = cx - 70, cx + 70
        s += diatomic(x1, x2, 90, 'H', b, shift=round(d * 22), anim=True, dsize=24 if d > 1.5 else 22)
        s += tex(x1, 175, '2.2', 21) + tex(cx, 175, '\\ce{H-' + b + '}', 21) + tex(x2, 175, f'{EN[b]:.1f}', 21)
        s += f'<path d="M{x1} 186 V198 H{x2} V186" fill="none" stroke="{MUTED}" stroke-width="1.6"/>'
        s += tex(cx, 222, f'차이 {d}', 21, mix=True, fill=INK)
    s += tex(300, 252, '모식도 — 전자쌍이 옮겨 간 거리는 전기음성도 차이에 비례하게 그림', 18, mix=True, fill=MUTED)
    return svg((600, 262), 600, '플루오린화 수소에서는 공유 전자쌍이 플루오린 쪽으로 많이, 염화 수소에서는 염소 쪽으로 조금 치우친다. 전기음성도 차이는 각각 1.8, 1.0', s)
F['hfhcl'] = hfhcl()

# ── S18 쌍극자 모멘트 표시 (그림 II-6 대응)
def dipfig():
    s = tex(120, 96, '\\ce{H - Cl}', 44)
    s += dl(80, 44, '+', 24) + dl(152, 44, '-', 24)
    s += dip(70, 128, 176, 128)
    x1, x2, y = 320, 420, 90
    s += bond(x1, y, x2, y) + atom(x1, y, 'H') + atom(x2, y, 'Cl')
    s += dl(x1, 48, '+', 24) + dl(x2, 42, '-', 24)
    s += f'<g data-anim="scale" data-from="0,1" data-o="{x1-6},128" data-dur="1.2" data-delay=".5">{dip(x1-6, 128, x2+10, 128)}</g>'
    s += tex(250, 172, '꼬리(+) = 전기음성도가 작은 원자 쪽 → 머리 = 큰 원자 쪽', 19, mix=True, fill=MUTED)
    return svg((500, 186), 500, '염화 수소의 구조식과 공-막대 모형 아래에 수소에서 염소를 향하는 쌍극자 모멘트 화살표', s)
F['dipfig'] = dipfig()

# ── S19 쌍극자 모멘트 크기 비교
def dipsize():
    s = ''
    for k, (b, d) in enumerate([('H', 0), ('Cl', 1.0), ('F', 1.8)]):
        y = 52 + k * 92; x1, x2 = 70, 170
        s += bond(x1, y, x2, y) + atom(x1, y, 'H') + atom(x2, y, b)
        if d:
            L = d * 110
            s += f'<g data-anim="scale" data-from="0,1" data-o="240,{y}" data-dur="1.3" data-delay="{.3+k*.5}">{dip(240, y, 240+L, y)}</g>'
        else:
            s += tex(250, y + 8, '쌍극자 모멘트 0', 21, mix=True, anchor='start', fill=MUTED)
        s += tex(500, y + 8, f'차이 {f(d) if d else "0"}', 20, mix=True, anchor='start', fill=MUTED)
    s += tex(300, 296, '화살표 길이는 크기 비교용 모식(정성적)', 18, mix=True, fill=MUTED)
    return svg((600, 306), 600, '수소 분자는 쌍극자 모멘트가 0, 염화 수소는 짧은 화살표, 플루오린화 수소는 긴 화살표로 쌍극자 모멘트 크기를 비교한 그림', s)
F['dipsize'] = dipsize()

# ── S21 연습: H2, H2O, CO2
def practice(step=True):
    s = ''
    # H2
    s += bond(40, 120, 120, 120) + atom(40, 120, 'H') + atom(120, 120, 'H')
    s += f'<rect x="12" y="88" width="136" height="64" rx="10" fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="5 4"/>'
    s += tex(80, 205, '\\ce{H2}', 22)
    # H2O
    ox, oy = 300, 80; L = 84; a = math.radians(52.25)
    hx1, hy = ox - L * math.sin(a), oy + L * math.cos(a); hx2 = ox + L * math.sin(a)
    s += bond(ox, oy, hx1, hy) + bond(ox, oy, hx2, hy) + atom(hx1, hy, 'H') + atom(hx2, hy, 'H') + atom(ox, oy, 'O')
    s += tex(300, 205, '\\ce{H2O}', 22)
    # CO2
    cx, cy = 520, 120
    s += bond(cx - 84, cy, cx, cy, 2) + bond(cx, cy, cx + 84, cy, 2) + atom(cx - 84, cy, 'O') + atom(cx, cy, 'C') + atom(cx + 84, cy, 'O')
    s += tex(520, 205, '\\ce{CO2}', 22)
    st = ' class="step" data-g="p2"'
    g = ''
    # H2O 화살표: H → O, 결합 바깥쪽으로 26 떨어진 평행선
    for sx in (-1, 1):
        hx = ox + sx * L * math.sin(a)
        ux, uy = (ox - hx) / L, (oy - hy) / L; nx, ny = (uy, -ux) if sx < 0 else (-uy, ux)
        off = 28
        x1, y1 = hx + ux * L * .18 + nx * off, hy + uy * L * .18 + ny * off
        x2, y2 = hx + ux * L * .82 + nx * off, hy + uy * L * .82 + ny * off
        g += dip(x1, y1, x2, y2)
    g += dl(hx1 - 34, hy + 10, '+', 22) + dl(hx2 + 34, hy + 10, '+', 22) + dl(ox + 38, oy - 24, '-', 22)
    g += dip(cx - 14, cy + 44, cx - 76, cy + 44) + dip(cx + 14, cy + 44, cx + 76, cy + 44)
    g += dl(cx, cy - 36, '+', 22) + dl(cx - 84, cy - 36, '-', 22) + dl(cx + 84, cy - 36, '-', 22)
    g += tex(80, 180, '화살표 없음', 19, mix=True, fill=MUTED)
    s += f'<g{st}>{g}</g>'
    return svg((640, 215), 640, '수소, 물, 이산화 탄소 분자 모형. 물은 두 수소에서 산소를 향하는 화살표, 이산화 탄소는 탄소에서 두 산소를 향하는 화살표를 그린다', s)
F['practice'] = practice()

# ── S22 화학 결합의 구분 (그림 II-7 대응)
def spectrum():
    s = ''
    # Cl2
    s += bond(100, 92, 168, 92) + atom(100, 92, 'Cl') + atom(168, 92, 'Cl') + tex(134, 22, '\\ce{Cl2}', 21)
    # HCl
    s += bond(440, 92, 508, 92) + atom(440, 92, 'H') + atom(508, 92, 'Cl') + tex(474, 22, '\\ce{HCl}', 21)
    s += dl(440, 62, '+', 21) + dl(548, 64, '-', 21)
    # NaCl ions
    s += atom(800, 92, 'Na', r=19, lab='-') + tex(774, 100, '\\ce{Na+}', 21, anchor='end') + atom(860, 92, 'Cl', r=32, lab='\\mathrm{Cl}^{-}') + tex(825, 22, '\\ce{NaCl}', 21)
    e = f'<g data-anim="move" data-from="-62,0" data-dur="1.4" data-delay=".6" data-ease="soft"><circle cx="878" cy="70" r="6" fill="{MINUS}"/></g>'
    s += f'<g data-arw="770,140,880,140,minus,3"></g>' + tex(825, 162, '전자 이동 $\\ce{e-}$', 19, mix=True, fill=MINUS) + e
    bars = [('전기음성도 차이', '#CFE8C0', '0', '크다'), ('쌍극자 모멘트', '#F6CDB0', '0', '크다')]
    for k, (name, col, a, b) in enumerate(bars):
        y = 190 + k * 48
        s += f'<rect x="14" y="{y-17}" width="150" height="34" rx="17" fill="#EEF1F4"/>' + tex(89, y + 7, name, 19, mix=True)
        s += f'<g data-anim="scale" data-from="0.05,1" data-o="184,{y}" data-dur="1.2" data-delay="{.4+k*.3}"><path d="M184 {y-15} H880 L910 {y} L880 {y+15} H184 Z" fill="{col}"/></g>'
        s += tex(250, y + 7, a, 19, mix=True) + tex(840, y + 7, b, 19, mix=True)
    y = 286
    s += f'<rect x="14" y="{y-17}" width="150" height="34" rx="17" fill="#EEF1F4"/>' + tex(89, y + 7, '화학 결합의 성질', 19, mix=True)
    for x0, x1, nm, col in [(184, 410, '무극성 공유 결합', '#E9E6F5'), (410, 660, '극성 공유 결합', '#DCD8F0'), (660, 910, '이온 결합', '#C9D4F2')]:
        s += f'<rect x="{x0}" y="{y-16}" width="{x1-x0}" height="32" fill="{col}"/>' + tex((x0 + x1) / 2, y + 7, nm, 19, mix=True)
    return svg((920, 310), 920, '염소 분자, 염화 수소, 염화 나트륨을 전기음성도 차이와 쌍극자 모멘트가 커지는 순서로 놓고 무극성 공유 결합, 극성 공유 결합, 이온 결합으로 구분한 그림', s)
F['spectrum'] = spectrum()

# ── S23 NH3
def nh3():
    nx, ny = 200, 70
    Hs = [(122, 128), (282, 118), (196, 178)]
    s = ''
    for hx, hy in Hs: s += bond(nx, ny, hx, hy)
    for hx, hy in Hs: s += atom(hx, hy, 'H')
    s += atom(nx, ny, 'N')
    s += f'<path d="M100 55 L215 22 L305 70 L300 150 L200 210 L100 160 Z" fill="none" stroke="{MUTED}" stroke-width="1.3" stroke-dasharray="5 4"/>'
    g = ''
    for (hx, hy), sd in zip(Hs, (-1, 1, 1)):
        L = math.hypot(nx - hx, ny - hy); ux, uy = (nx - hx) / L, (ny - hy) / L
        px, py = (-uy, ux)
        if sd < 0: px, py = -px, -py
        off = 24
        g += dip(hx + ux * L * .2 + px * off, hy + uy * L * .2 + py * off, hx + ux * L * .85 + px * off, hy + uy * L * .85 + py * off)
    g += dl(nx + 34, ny - 26, '-', 22) + dl(98, 126, '+', 22) + dl(318, 126, '+', 22) + dl(232, 196, '+', 22)
    s += f'<g class="step" data-g="n1">{g}</g>'
    return svg((380, 230), 380, '암모니아 분자 모형. 세 수소에서 질소를 향하는 쌍극자 모멘트 화살표와 부분 전하를 표시한다', s)
F['nh3'] = nh3()

# ── S27 문항 04 주기율표 일부
def q04():
    gs = ['1', '2', '13', '14', '15', '16', '17', '18']
    s = ''; X0, Y0, CW, CH = 70, 40, 62, 56
    for j, g in enumerate(gs): s += tex(X0 + j * CW + CW / 2, 28, g, 19, fill=MUTED)
    marks = {(0, 0): 'W', (0, 3): 'X', (0, 4): 'Y', (1, 0): 'Z'}
    for i in range(2):
        s += tex(36, Y0 + i * CH + CH / 2 + 7, str(i + 2), 20, fill=MUTED)
        for j in range(8):
            s += f'<rect x="{X0+j*CW+2}" y="{Y0+i*CH+2}" width="{CW-4}" height="{CH-4}" rx="7" fill="#FBD2AE" stroke="#EE9B5C" stroke-width="1.4"/>'
            if (i, j) in marks:
                s += tex(X0 + j * CW + CW / 2, Y0 + i * CH + CH / 2 + 8, '\\mathrm{' + marks[(i, j)] + '}', 24)
    s += tex(36, 28, '주기', 17, mix=True, fill=MUTED) if False else ''
    return svg((580, 160), 560, '2주기 1족 W, 2주기 14족 X, 2주기 15족 Y, 3주기 1족 Z가 표시된 주기율표 일부', s)
F['q04'] = q04()

# ── S28 문항 05
def q05():
    s = ''
    s += cloud(140, 80, 110, 50) + bond(100, 80, 180, 80) + atom(100, 80, 'X', lab='\\mathrm{X}') + atom(180, 80, 'X', lab='\\mathrm{X}') + pair(140, 80)
    s += tex(140, 160, '(가)', 21, mix=True)
    s += cloud(450, 80, 112, 52) + bond(380, 80, 460, 80) + atom(380, 80, 'X', lab='\\mathrm{Y}') + atom(460, 80, 'X', r=29, lab='\\mathrm{Z}') + '<g data-anim="move" data-from="-20,0" data-dur="1.4" data-delay=".5" data-ease="soft">' + pair(440, 80) + '</g>'
    s += dl(380, 36, '+', 22) + dl(460, 30, '-', 22)
    s += tex(430, 160, '(나)', 21, mix=True)
    return svg((600, 175), 600, '(가)는 같은 원자 X 두 개가 결합해 전자 구름이 대칭이고, (나)는 Y와 Z가 결합해 전자 구름과 공유 전자쌍이 Z 쪽으로 치우치며 Y는 부분적인 양전하, Z는 부분적인 음전하를 띤다', s)
F['q05'] = q05()

# ── S31 문항 08
def q08():
    s = ''; y = 60
    def A(x, l): return atom(x, y, 'X', lab='\\mathrm{' + l + '}')
    # B–A–B
    s += bond(50, y, 190, y) + A(50, 'B') + A(120, 'A') + A(190, 'B')
    s += dip(108, 112, 52, 112) + dip(132, 112, 188, 112)
    # C–A–D
    s += bond(260, y, 400, y) + A(260, 'C') + A(330, 'A') + A(400, 'D')
    s += dip(262, 112, 318, 112) + dip(342, 112, 398, 112)
    # B–D
    s += bond(480, y, 550, y) + A(480, 'B') + A(550, 'D')
    s += dip(548, 112, 482, 112)
    return svg((600, 135), 580, '분자 B–A–B는 A에서 양쪽 B를 향하는 화살표, C–A–D는 C에서 A로, A에서 D로 향하는 화살표, B–D는 D에서 B를 향하는 화살표', s)
F['q08'] = q08()

# ── S32 문항 09
def q09():
    s = ''; y = 110
    xs = [40, 115, 205, 280]
    s += bond(xs[0], y, xs[1], y) + bond(xs[1], y, xs[2], y, 3) + bond(xs[2], y, xs[3], y)
    s += atom(xs[0], y, 'H') + atom(xs[1], y, 'C') + atom(xs[2], y, 'C') + atom(xs[3], y, 'H')
    s += tex(160, 190, '(가)', 21, mix=True)
    cx, cy = 450, 110
    s += bond(cx, cy, cx, cy - 78, 2) + bond(cx, cy, cx - 66, cy + 40) + bond(cx, cy, cx + 66, cy + 40)
    s += atom(cx - 66, cy + 40, 'H') + atom(cx + 66, cy + 40, 'H') + atom(cx, cy - 78, 'O') + atom(cx, cy, 'C')
    s += tex(450, 190, '(나)', 21, mix=True)
    return svg((560, 205), 560, '(가) 수소–탄소–탄소–수소가 일직선이고 탄소 사이가 3중 결합인 분자, (나) 탄소에 산소가 2중 결합, 수소 두 개가 단일 결합한 분자', s)
F['q09'] = q09()

def build():
    tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
    def rep(m):
        k = m.group(1)
        if k not in F: sys.exit('missing ' + k)
        return F[k]
    out = re.sub(r'\{\{(\w+)\}\}', rep, tpl)
    open(OUT, 'w', encoding='utf-8').write(out)
    print('ok', len(out))

if __name__ == '__main__':
    build()
