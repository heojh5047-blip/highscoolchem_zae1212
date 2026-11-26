# 4-3 유효 충돌과 활성화 에너지 — tpl.html 의 @@이름@@ 자리에 그림을 넣어 slides.html 을 만든다.
import math, os, re, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/물질과에너지_미래엔/4-3_유효_충돌과_활성화_에너지/slides.html'
F = {}
BOND = '#9AA5B1'

def P(x, y, ang, d):
    a = math.radians(ang)
    return x + d * math.cos(a), y + d * math.sin(a)

# ── 분자 (공간 채움 모형: 원자 중심 거리 1.25r) ──
def NO(xN, yN, ang, r, lab='-'):
    """N 원자 (xN,yN), O 는 ang 방향"""
    xo, yo = P(xN, yN, ang, 1.25 * r)
    return atom(xo, yo, r, 'O', lab) + atom(xN, yN, r, 'N', lab)

def O3(xc, yc, apex, r, lab='-'):
    """가운데 O (xc,yc). apex = 가운데 O 가 튀어나온 쪽. 끝 O 둘은 반대쪽에 117°로"""
    t1 = P(xc, yc, apex + 180 - 58.5, 1.25 * r); t2 = P(xc, yc, apex + 180 + 58.5, 1.25 * r)
    return atom(*t1, r, 'O', lab) + atom(*t2, r, 'O', lab) + atom(xc, yc, r, 'O', lab), t1, t2

def NO2(xN, yN, ang, r, lab='-'):
    """N 가운데, O 둘은 ang 쪽으로 134°"""
    a = P(xN, yN, ang - 67, 1.25 * r); b = P(xN, yN, ang + 67, 1.25 * r)
    return atom(*a, r, 'O', lab) + atom(*b, r, 'O', lab) + atom(xN, yN, r, 'N', lab)

def O2(x, y, ang, r, lab='-'):
    a = P(x, y, ang, .625 * r); b = P(x, y, ang + 180, .625 * r)
    return atom(*a, r, 'O', lab) + atom(*b, r, 'O', lab)

def N2(x, y, ang, r, lab='-'):
    a = P(x, y, ang, .625 * r); b = P(x, y, ang + 180, .625 * r)
    return atom(*a, r, 'N', lab) + atom(*b, r, 'N', lab)

def streak(x, y, length, n=3, gap=9, col='#C9D3DD', side=-1):
    """빠르기 표시 줄(움직이는 쪽 반대편)"""
    o = ''
    for i in range(n):
        yy = y + (i - (n - 1) / 2) * gap
        L = length * (1 - .25 * abs(i - (n - 1) / 2))
        o += f'<line x1="{f(x)}" y1="{f(yy)}" x2="{f(x + side * L)}" y2="{f(yy)}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    return o

def flash(x, y, R, n=12, col='#FFD34D', extra=''):
    pts = []
    for i in range(2 * n):
        rr = R if i % 2 == 0 else R * .45
        pts.append(P(x, y, i * 180 / n, rr))
    return f'<polygon points="{" ".join(f(a) + "," + f(b) for a, b in pts)}" fill="{col}" opacity=".85"{extra}/>'

def vdim(x, y1, y2, lab, col=EQUI, size=20, side='right', extra=''):
    """세로 치수선(양 끝 화살촉) + 옆 라벨"""
    top, bot = min(y1, y2), max(y1, y2)
    o = f'<g{extra}><line x1="{f(x)}" y1="{f(top + 3)}" x2="{f(x)}" y2="{f(bot - 3)}" stroke="{col}" stroke-width="2.5"/>'
    o += f'<polygon points="{f(x)},{f(top)} {f(x - 5)},{f(top + 10)} {f(x + 5)},{f(top + 10)}" fill="{col}"/>'
    o += f'<polygon points="{f(x)},{f(bot)} {f(x - 5)},{f(bot - 10)} {f(x + 5)},{f(bot - 10)}" fill="{col}"/>'
    if lab:
        ym = (top + bot) / 2 + size * .35
        if side == 'right': o += tex(x + 10, ym, lab, size, 'start', col if col != EQUI else '#B8661A', halo=True)
        else: o += tex(x - 10, ym, lab, size, 'end', col if col != EQUI else '#B8661A', halo=True)
    return o + '</g>'

def hdash(x1, x2, y, col=MUTED):
    return f'<line x1="{f(x1)}" y1="{f(y)}" x2="{f(x2)}" y2="{f(y)}" stroke="{col}" stroke-width="1.6" stroke-dasharray="5 5"/>'

def hill(xa, x1, xp, x2, xe, yr, yp, yP, k1=None, k2=None):
    """반응물 수평(xa→x1) → 꼭대기(xp,yp) → 생성물 수평(x2→xe)"""
    k1 = k1 or (xp - x1) * .55; k2 = k2 or (x2 - xp) * .55
    return (f'M{f(xa)} {f(yr)} L{f(x1)} {f(yr)} C{f(x1 + k1)} {f(yr)} {f(xp - k1)} {f(yp)} {f(xp)} {f(yp)} '
            f'C{f(xp + k2)} {f(yp)} {f(x2 - k2)} {f(yP)} {f(x2)} {f(yP)} L{f(xe)} {f(yP)}')

def eaxes(x0, y0, w, h, yl='엔탈피', xl='반응의 진행', size=20):
    o = f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{MUTED}" stroke-width="2"/>'
    o += f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="{MUTED}" stroke-width="2"/>'
    o += f'<polygon points="{x0 + w + 8},{y0} {x0 + w - 2},{y0 - 5} {x0 + w - 2},{y0 + 5}" fill="{MUTED}"/>'
    o += f'<polygon points="{x0},{y0 - h - 8} {x0 - 5},{y0 - h + 2} {x0 + 5},{y0 - h + 2}" fill="{MUTED}"/>'
    o += tex(x0 + 12, y0 - h + 4, yl, size, 'start', INK)
    o += tex(x0 + w, y0 + 26, xl, size, 'end', INK)
    return o

CURVE = lambda d, extra='': f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"{extra}/>'

# ── S1 표지 ──
def cover():
    o = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    yr, yp, yP = 330, 150, 400
    d = hill(70, 140, 270, 400, 470, yr, yp, yP)
    o += CURVE(d, ' data-anim="draw" data-dur="1.2"').replace('3.5', '5')
    o += hdash(140, 216, yp)
    o += vdim(205, yr, yp, '$E_\\mathrm{a}$', EQUI, 26, 'left', ' data-anim="pop" data-o="205,240" data-delay="1.1" data-dur=".5"')
    o += tex(105, yr + 34, '반응물', 22, 'middle', INK) + tex(435, yP + 34, '생성물', 22, 'middle', INK)
    # 언덕을 넘는 입자(꼭대기 위 궤적)
    tr = hill(110, 150, 270, 390, 420, yr - 24, yp - 26, yP - 24)
    o += f'<path d="{tr}" fill="none" stroke="{FIELD}" stroke-width="3" stroke-dasharray="7 7" data-anim="draw" data-dur="1.4" data-delay="1.5"/>'
    o += '<g data-arw="408,376,432,376,field,3" data-delay="2.8"></g>'
    o += atom(110, yr - 24, 15, 'N', '-').replace('></g>', ' data-anim="fade" data-dur=".4"></g>')
    o += tex(270, 488, '에너지 장벽을 넘어야 반응한다', 22, 'middle', MUTED)
    return o
F['cover'] = cover()

# ── S3 생각 열기: 공기 중 / 엔진 속 ──
def s3():
    r = 13; o = ''
    # 공기 중
    o += '<rect x="6" y="6" width="500" height="230" rx="14" fill="#E3EEFB" stroke="#9FB0C2" stroke-width="2"/>'
    o += tex(256, 40, '공기 중 (상온)', 21, 'middle', INK)
    rnd = random.Random(3)
    spots_air = [(60, 90), (150, 150), (250, 85), (340, 165), (430, 100), (95, 200), (210, 205), (300, 120), (450, 200), (390, 60)]
    for i, (x, y) in enumerate(spots_air):
        ang = rnd.uniform(0, 180); m = N2(x, y, ang, r) if i % 5 != 2 and i % 5 != 4 else O2(x, y, ang, r)
        dx, dy = rnd.choice([-1, 1]) * rnd.uniform(6, 12), rnd.choice([-1, 1]) * rnd.uniform(5, 9)
        o += f'<g data-anim="move" data-from="{f(dx)},{f(dy)}" data-rep="alt" data-dur="{rnd.uniform(1.1, 1.8):.1f}" data-ease="io">{m}</g>'
    o += tex(256, 262, '충돌해도 거의 반응하지 않음', 19, 'middle', MUTED)
    # 엔진 속
    o += '<rect x="530" y="6" width="500" height="230" rx="14" fill="#FDE2E4" stroke="#E7A6AE" stroke-width="2"/>'
    o += tex(780, 40, '자동차 엔진 속 (높은 온도)', 21, 'middle', INK)
    spots_e = [(590, 95), (690, 160), (800, 80), (880, 160), (960, 95), (620, 200), (760, 200), (950, 205), (840, 120)]
    kinds = ['N2', 'NO', 'O2', 'NO', 'N2', 'NO', 'O2', 'N2', 'NO']
    for (x, y), k in zip(spots_e, kinds):
        ang = rnd.uniform(0, 180)
        if k == 'N2': m = N2(x, y, ang, r)
        elif k == 'O2': m = O2(x, y, ang, r)
        else:
            xN, yN = P(x, y, ang + 180, .625 * r); m = NO(xN, yN, ang, r)
        dx, dy = rnd.choice([-1, 1]) * rnd.uniform(16, 26), rnd.choice([-1, 1]) * rnd.uniform(10, 16)
        o += f'<g data-anim="move" data-from="{f(dx)},{f(dy)}" data-rep="alt" data-dur="{rnd.uniform(.5, .8):.2f}" data-ease="io">{m}</g>'
    o += tex(780, 262, '질소 산화물이 생김', 19, 'middle', MUTED)
    # 범례
    o += '<rect x="1046" y="70" width="112" height="100" rx="8" fill="#fff" stroke="#C9D3DD" stroke-width="1.5"/>'
    o += atom(1070, 100, r, 'N') + tex(1092, 107, '$\\mathrm{N}$', 20, 'start', INK)
    o += atom(1070, 142, r, 'O') + tex(1092, 149, '$\\mathrm{O}$', 20, 'start', INK)
    return o
F['s3'] = s3()

# ── S4 연결: H2 + I2 충돌 ──
def s4():
    rH, rI = 18, 35; o = ''
    def card(x, title):
        return f'<rect x="{x}" y="6" width="330" height="210" rx="14" fill="#F4F8FC" stroke="#9FB0C2" stroke-width="2"/>' + tex(x + 165, 40, title, 21, 'middle', INK)
    o += card(6, '① 다가간다') + card(381, '② 충돌한다') + card(756, '③ 결합이 바뀐다')
    o += '<g data-arw="340,120,374,120,ink,3"></g><g data-arw="715,120,749,120,ink,3"></g>'
    # ① H2 왼쪽, I2 오른쪽 (서로 다가감)
    o += f'<g data-anim="move" data-from="-30,0" data-dur="1.2" data-ease="out">' + streak(52, 120, 30) + atom(80, 98, rH, 'H', '') + atom(80, 142, rH, 'H', '') + '</g>'
    o += f'<g data-anim="move" data-from="30,0" data-dur="1.2" data-ease="out">' + streak(300, 120, 30, side=1) + atom(250, 85, rI, 'I', '') + atom(250, 155, rI, 'I', '') + '</g>'
    # ② 맞닿음
    o += atom(546, 85, rI, 'I', '') + atom(546, 155, rI, 'I', '')
    o += flash(522, 120, 30, extra=' data-anim="pop" data-o="522,120" data-delay=".9" data-dur=".5"')
    o += atom(500, 98, rH, 'H', '') + atom(500, 142, rH, 'H', '')
    # ③ 2HI (원자 보존: H 2, I 2)
    o += f'<g data-anim="move" data-from="0,22" data-dur="1" data-delay="1.4" data-ease="out">' + atom(850, 85, rI, 'I', '') + atom(894, 85, rH, 'H', '') + '</g>'
    o += f'<g data-anim="move" data-from="0,-22" data-dur="1" data-delay="1.4" data-ease="out">' + atom(850, 160, rI, 'I', '') + atom(894, 160, rH, 'H', '') + '</g>'
    o += tex(980, 128, '$\\ce{2HI}$', 22, 'middle', INK)
    o += tex(171, 205, '$\\ce{H2}$ + $\\ce{I2}$', 20, 'middle', MUTED) + tex(921, 205, '생성물', 20, 'middle', MUTED)
    return o
F['s4'] = s4()

# ── S5 해 보기: NO + O3 충돌 모형 ──
def s5():
    r = 16; o = ''
    rows = [('(가)', 62, 'slow', 'end'), ('(나)', 177, 'fast', 'mid'), ('(다)', 292, 'fast', 'end')]
    for lab, y, sp, hit in rows:
        o += tex(16, y + 8, lab, 24, 'start', INK)
        L = 26 if sp == 'slow' else 62
        # 충돌 전: NO (N 이 오른쪽), O3
        xN = 150
        o += streak(xN - 1.25 * r - 12, y, L)
        o += NO(xN, y, 180, r)
        if hit == 'end':
            m, t1, t2 = O3(270, y + 8, -20, r)
        else:
            m, t1, t2 = O3(255, y, 180, r)
        o += streak(305, y, L, side=1) + m
        o += tex(122, y + 58, '$\\ce{NO}$', 23, 'middle', MUTED) + tex(262, y + 58, '$\\ce{O3}$', 23, 'middle', MUTED)
        o += f'<g data-arw="352,{y},384,{y},muted,2.5"></g>'
        # 충돌: N 이 표적 O 에 닿음
        if hit == 'end':
            cx, cy, ap = 500, y + 8, -20
            mm, a1, a2 = O3(cx, cy, ap, r)
            tgt = a2 if a2[0] < a1[0] else a1
            # NO 의 N 을 표적 O 왼쪽에
            nx, ny = tgt[0] - 1.9 * r, tgt[1]
        else:
            cx, cy = 505, y
            mm, a1, a2 = O3(cx, cy, 180, r)
            nx, ny = cx - 1.9 * r, cy
        o += flash((nx + (tgt[0] if hit == 'end' else cx)) / 2, ny, 22 if sp == 'slow' else 36, extra=f' data-anim="pop" data-o="{f(nx + .95 * r)},{f(ny)}" data-dur=".5" data-delay=".6"')
        o += mm + NO(nx, ny, 180, r)
        o += f'<g data-arw="600,{y},632,{y},muted,2.5"></g>'
        # 충돌 후
        if lab == '(다)':
            o += f'<g data-anim="move" data-from="40,0" data-dur="1" data-delay="1" data-ease="out">' + NO2(735, y, 180, r) + streak(770, y, 34, side=1) + '</g>'
            o += f'<g data-anim="move" data-from="-60,0" data-dur="1" data-delay="1" data-ease="out">' + O2(885, y, 0, r) + streak(920, y, 34, side=1) + '</g>'
            o += tex(722, y + 58, '$\\ce{NO2}$', 23, 'middle', MUTED) + tex(885, y + 58, '$\\ce{O2}$', 23, 'middle', MUTED)
        else:
            o += f'<g data-anim="move" data-from="50,0" data-dur="1" data-delay="1" data-ease="out">' + streak(700 - 1.25 * r, y, L * .8, side=1) + NO(712, y, 180, r) + '</g>'
            if hit == 'end': mo = O3(880, y + 8, -20, r)[0]
            else: mo = O3(868, y, 180, r)[0]
            o += f'<g data-anim="move" data-from="-60,0" data-dur="1" data-delay="1" data-ease="out">' + mo + streak(905, y, L * .8, side=-1).replace('x2', 'x2') + '</g>'
            o += tex(694, y + 58, '$\\ce{NO}$', 23, 'middle', MUTED) + tex(872, y + 58, '$\\ce{O3}$', 23, 'middle', MUTED)
    # 아래 묶음 표시
    for x1, x2, lab in [(80, 330, '충돌 전'), (420, 590, '충돌'), (660, 950, '충돌 후')]:
        o += f'<path d="M{x1} 356 v8 H{x2} v-8" fill="none" stroke="{MUTED}" stroke-width="1.6"/>' + tex((x1 + x2) / 2, 390, lab, 23, 'middle', INK)
    o += '<rect x="984" y="120" width="112" height="100" rx="8" fill="#fff" stroke="#C9D3DD" stroke-width="1.5"/>'
    o += atom(1008, 150, r, 'N') + tex(1032, 157, '$\\mathrm{N}$', 23, 'start', INK)
    o += atom(1008, 192, r, 'O') + tex(1032, 199, '$\\mathrm{O}$', 23, 'start', INK)
    return o
F['s5'] = s5()

# ── S7 유효 충돌의 두 조건 (작은 그림 둘씩) ──
def mini(kind):
    r = 14; o = '<rect x="4" y="4" width="252" height="112" rx="10" fill="#F4F8FC" stroke="#C9D3DD" stroke-width="1.5"/>'
    y = 62
    if kind in ('ok', 'fast'):
        m, a1, a2 = O3(165, y + 7, -20, r); tgt = a2 if a2[0] < a1[0] else a1
        nx = tgt[0] - 1.9 * r
        o += streak(nx - 1.25 * r - 10, tgt[1], 44) + NO(nx, tgt[1], 180, r) + m
        o += flash((nx + tgt[0]) / 2, tgt[1], 24, extra=f' data-anim="pop" data-o="{f((nx + tgt[0]) / 2)},{f(tgt[1])}" data-dur=".5" data-delay=".5"')
        o += NO(nx, tgt[1], 180, r)
    elif kind == 'bad':
        m, a1, a2 = O3(165, y, 180, r); nx = 165 - 1.9 * r
        o += streak(nx - 1.25 * r - 10, y, 44) + NO(nx, y, 180, r) + m
    elif kind == 'slow':
        m, a1, a2 = O3(165, y + 7, -20, r); tgt = a2 if a2[0] < a1[0] else a1
        nx = tgt[0] - 1.9 * r
        o += streak(nx - 1.25 * r - 10, tgt[1], 14) + NO(nx, tgt[1], 180, r) + m
    return o
for k in ('ok', 'bad', 'fast', 'slow'):
    F['m_' + k] = mini(k)

# ── S9 에너지 장벽과 높이뛰기 ──
def s9a():
    o = ''
    yr, yp, yP = 230, 70, 280
    o += CURVE(hill(20, 90, 230, 370, 440, yr, yp, yP))
    o += tex(55, yr + 30, '반응물', 20, 'middle', INK) + tex(410, yP + 30, '생성물', 20, 'middle', INK)
    # 느린 입자: 중간까지 올라갔다가 되돌아옴
    o += f'<path d="M70 {yr - 20} L100 {yr - 20} C140 {yr - 20} 150 {yr - 70} 168 {yr - 92}" fill="none" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="6 6" data-anim="draw" data-dur="1"/>'
    o += f'<g data-arw="150,{yr - 98},116,{yr - 44},muted,2.5" data-delay="1.1"></g>'
    # 빠른 입자: 넘어감
    tr = hill(60, 100, 230, 360, 400, yr - 40, yp - 24, yP - 24)
    o += f'<path d="{tr}" fill="none" stroke="{FIELD}" stroke-width="3" stroke-dasharray="7 7" data-anim="draw" data-dur="1.4" data-delay=".6"/>'
    o += '<g data-arw="392,256,420,256,field,3" data-delay="2"></g>'
    o += f'<line x1="20" y1="336" x2="60" y2="336" stroke="{FIELD}" stroke-width="3" stroke-dasharray="7 7"/>' + tex(68, 342, '충분한 에너지 → 넘어감', 18, 'start', INK)
    o += f'<line x1="250" y1="336" x2="290" y2="336" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="6 6"/>' + tex(298, 342, '부족 → 되돌아옴', 18, 'start', INK)
    o += hdash(90, 190, yp) + vdim(180, yr, yp, '$E_\\mathrm{a}$', EQUI, 22, 'left')
    return o
F['s9a'] = s9a()

def s9b():
    o = '<rect x="4" y="250" width="352" height="40" rx="6" fill="#C7744A" opacity=".35"/>'
    o += '<line x1="150" y1="250" x2="150" y2="80" stroke="#5B6B7F" stroke-width="5"/><line x1="290" y1="250" x2="290" y2="80" stroke="#5B6B7F" stroke-width="5"/>'
    o += f'<line x1="150" y1="110" x2="290" y2="110" stroke="{PLUS}" stroke-width="6" stroke-linecap="round"/>'
    o += '<rect x="80" y="250" width="200" height="30" rx="6" fill="#4F6BD8" opacity=".35"/>'
    # 넘은 궤적, 못 넘은 궤적
    o += f'<path d="M40 240 Q215 -20 330 236" fill="none" stroke="{FIELD}" stroke-width="3" stroke-dasharray="7 7" data-anim="draw" data-dur="1.3" data-delay=".3"/>'
    o += f'<path d="M40 240 Q130 110 196 150" fill="none" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="6 6" data-anim="draw" data-dur="1" data-delay=".3"/>'
    o += f'<circle cx="40" cy="240" r="9" fill="{INK}"/>'
    o += vdim(322, 250, 110, '가로대||높이', EQUI, 22, 'right')
    return o
F['s9b'] = s9b()

# ── S10 그림 IV-4 다시 그림: NO + O3 ──
def s10():
    x0, y0, w, h = 70, 380, 610, 350
    o = eaxes(x0, y0, w, h)
    s = 1.3  # px per kJ/mol
    yP = 352; yr = yP - 199.5 * s; yp = yr - 10.5 * s
    o += CURVE(hill(x0 + 10, 190, 330, 480, 650, yr, yp, yP), ' data-anim="draw" data-dur="1.4"')
    o += tex(130, yr + 28, '$\\ce{NO(g) + O3(g)}$', 20, 'middle', INK) + tex(130, yr + 52, '반응물', 18, 'middle', MUTED)
    o += tex(580, yP - 14, '$\\ce{NO2(g) + O2(g)}$', 20, 'middle', INK) + tex(600, yP + 24, '생성물', 18, 'middle', MUTED)
    # 활성화물
    r = 11
    m, a1, a2 = O3(355, yp - 40, -20, r); tgt = a2 if a2[0] < a1[0] else a1
    o += m + NO(tgt[0] - 1.9 * r, tgt[1], 180, r)
    o += tex(392, yp - 30, '활성화물', 19, 'start', INK)
    # Ea
    o += f'<g class="step" data-g="ea">' + hdash(190, 260, yp) + vdim(250, yr, yp, '', EQUI) + tex(240, yp - 12, '$E_\\mathrm{a}=10.5\\ \\text{kJ/mol}$', 19, 'end', '#B8661A', halo=True) + '</g>'
    # ΔH
    o += f'<g class="step" data-g="dh">' + hdash(190, 300, yr) + hdash(300, 480, yP) + f'<g data-arw="300,{f(yr + 2)},300,{f(yP - 2)},ink,3"></g>' + tex(290, (yr + yP) / 2 + 20, '$\\Delta H=-199.5\\ \\text{kJ/mol}$', 19, 'end', INK, halo=True) + '</g>'
    # Ea'
    o += f'<g class="step" data-g="ear">' + hdash(330, 650, yp) + vdim(630, yP, yp, '', EQUI) + tex(622, yp + 60, "$E_\\mathrm{a}'=210.0\\ \\text{kJ/mol}$", 19, 'end', '#B8661A', halo=True) + '</g>'
    return o
F['s10'] = s10()

# ── S11 활성화 상태: 반응물 → 활성화물 → 생성물 ──
def s11():
    r = 20; o = ''
    def card(x, title, sub, hl=False):
        fill = '#FFF6E5' if hl else '#F4F8FC'; st = EQUI if hl else '#9FB0C2'
        return f'<rect x="{x}" y="6" width="340" height="200" rx="14" fill="{fill}" stroke="{st}" stroke-width="2"/>' + tex(x + 170, 40, title, 21, 'middle', INK) + tex(x + 170, 194, sub, 18, 'middle', MUTED)
    o += card(6, '반응물', '$\\ce{NO}$ + $\\ce{O3}$') + card(386, '활성화물 (활성화 상태)', '결합이 끊어지기 직전', True) + card(766, '생성물', '$\\ce{NO2}$ + $\\ce{O2}$')
    o += '<g data-arw="350,110,380,110,ink,3"></g><g data-arw="730,110,760,110,ink,3"></g>'
    y = 112
    # 반응물
    m, a1, a2 = O3(250, y + 10, -20, r)
    o += NO(96, y, 180, r) + m
    # 활성화물: N…O 새 결합 생기는 중, O–O 끊어지는 중 (점선 결합)
    m, a1, a2 = O3(580, y + 10, -20, r); tgt = a2 if a2[0] < a1[0] else a1
    nx = tgt[0] - 2.9 * r
    # 가운데 O 를 조금 떼어 놓은 활성화물
    c = (580, y + 10); t1o = a1 if tgt is a2 else a2
    tm = P(tgt[0], tgt[1], math.degrees(math.atan2(tgt[1] - c[1], tgt[0] - c[0])), 12)
    o += atom(*t1o, r, 'O', '-') + atom(*c, r, 'O', '-')
    o += f'<g data-anim="swing" data-from="3,0" data-dur=".25">' + atom(*tm, r, 'O', '-') + '</g>'
    o += NO(nx, tgt[1], 180, r)
    o += f'<line x1="{f(nx)}" y1="{f(tgt[1])}" x2="{f(tgt[0])}" y2="{f(tgt[1])}" stroke="{EQUI}" stroke-width="5" stroke-dasharray="5 5"/>'
    o += f'<line x1="{f(tgt[0])}" y1="{f(tgt[1])}" x2="580" y2="{y + 10}" stroke="{EQUI}" stroke-width="5" stroke-dasharray="5 5"/>'
    # 생성물
    o += f'<g data-anim="move" data-from="30,0" data-dur="1" data-delay=".6" data-ease="out">' + NO2(870, y, 180, r) + '</g>'
    o += f'<g data-anim="move" data-from="-30,0" data-dur="1" data-delay=".6" data-ease="out">' + O2(1030, y, 0, r) + '</g>'
    return o
F['s11'] = s11()

# ── S12 다시 보기: N2 + O2 -> 2NO (정성) ──
def s12():
    x0, y0, w, h = 60, 330, 560, 300
    o = eaxes(x0, y0, w, h)
    yr, yp, yP = 290, 60, 230
    o += CURVE(hill(x0 + 10, 170, 330, 470, 600, yr, yp, yP), ' data-anim="draw" data-dur="1.4"')
    o += tex(140, yr + 24, '$\\ce{N2(g) + O2(g)}$', 20, 'middle', INK)
    o += tex(540, yP - 14, '$\\ce{2NO(g)}$', 20, 'middle', INK)
    o += hdash(170, 260, yp) + vdim(250, yr, yp, '$E_\\mathrm{a}$ (매우 큼)', EQUI, 20, 'left')
    o += hdash(430, 600, yr) + f'<g data-arw="590,{yr - 2},590,{yP + 2},ink,3"></g>' + tex(580, (yr + yP) / 2 + 8, '$\\Delta H&gt;0$', 19, 'end', INK, halo=True)
    return o
F['s12'] = s12()

# ── S13 연습 문제: 흡열 반응 ──
def s13():
    x0, y0, w, h = 60, 330, 540, 300
    o = eaxes(x0, y0, w, h)
    yr, yp, yP = 280, 60, 196
    o += CURVE(hill(x0 + 10, 160, 310, 450, 580, yr, yp, yP), ' data-anim="draw" data-dur="1.2"')
    o += tex(140, yr + 26, '$\\ce{A2(g) + B2(g)}$', 20, 'middle', INK)
    o += tex(520, yP - 14, '$\\ce{2AB(g)}$', 20, 'middle', INK)
    o += hdash(160, 240, yp) + vdim(230, yr, yp, '$150\\ \\text{kJ}$', EQUI, 20, 'left')
    o += hdash(450, 590, yr) + vdim(560, yr, yP, '$60\\ \\text{kJ}$', MUTED, 19, 'left')
    return o
F['s13'] = s13()

# ── S18 대단원 마무리 05: HI 분해 ──
def s18():
    x0, y0, w, h = 60, 330, 520, 300
    o = eaxes(x0, y0, w, h, size=24)
    s = 1.3
    yr = 268; yp = yr - 184 * s; yP = yr - 9.4 * s * 2.2  # 9.4 kJ 차이는 보이게 키움(눈금 없음)
    o += CURVE(hill(x0 + 10, 160, 300, 440, 560, yr, yp, yP))
    o += tex(120, yr - 12, '$\\mathrm{HI}+\\mathrm{HI}$', 24, 'middle', INK)
    o += tex(510, yP - 14, '$\\mathrm{H_2}+\\mathrm{I_2}$', 24, 'middle', INK)
    o += hdash(x0, 560, yr) + vdim(300, yr, yp, '', EQUI) + tex(310, yr - 40, '$184\\ \\text{kJ}$', 24, 'start', '#B8661A', halo=True)
    o += vdim(548, yr, yP, '', MUTED) + tex(540, yr + 26, '$9.4\\ \\text{kJ}$', 23, 'end', INK, halo=True)
    return o
F['s18'] = s18()

# ── S16 디지털 소양: BrNO 두 분자 ──
def brno(xBr, yBr, ang_to_N, bend, rB=28, r=22):
    """Br–N=O 굽은 분자: Br (xBr,yBr) → N 은 ang 방향, O 는 N 에서 ang+bend 방향"""
    xN, yN = P(xBr, yBr, ang_to_N, .62 * (rB + r) * 1.25)
    xO, yO = P(xN, yN, ang_to_N + bend, 1.25 * r)
    return atom(xBr, yBr, rB, 'Br', '') + atom(xO, yO, r, 'O', '') + atom(xN, yN, r, 'N', '')

def s16(kind):
    o = '<rect x="4" y="4" width="392" height="170" rx="12" fill="#F4F8FC" stroke="#C9D3DD" stroke-width="1.5"/>'
    if kind == 'A':  # Br 끼리 마주 봄
        o += brno(169, 90, 180, 60) + brno(231, 90, 0, -60)
        o += '<g data-arw="22,150,70,150,ink,2.5"></g><g data-arw="378,150,330,150,ink,2.5"></g>'
    else:  # O 끼리 마주 봄
        o += brno(118, 84, 0, 60) + brno(282, 84, 180, -60)
        o += '<g data-arw="22,150,70,150,ink,2.5"></g><g data-arw="378,150,330,150,ink,2.5"></g>'
    return o
F['s16a'] = s16('A'); F['s16b'] = s16('B')

def s16c():
    """생성물: Br2 + 2NO"""
    o = '<rect x="4" y="4" width="392" height="170" rx="12" fill="#F4F8FC" stroke="#C9D3DD" stroke-width="1.5"/>'
    o += f'<g data-anim="move" data-from="0,10" data-dur=".8" data-on="step">' + atom(176, 66, 28, 'Br', '') + atom(224, 66, 28, 'Br', '') + '</g>'
    o += f'<g data-anim="move" data-from="40,-20" data-dur=".8" data-on="step">' + NO(90, 122, 180 + 60, 22, '') + '</g>'
    o += f'<g data-anim="move" data-from="-40,-20" data-dur=".8" data-on="step">' + NO(310, 122, -60, 22, '') + '</g>'
    o += tex(200, 160, '$\\ce{Br2}$ + $\\ce{2NO}$', 19, 'middle', MUTED)
    return o
F['s16c'] = s16c()

tpl = open(os.path.join(HERE, 'tpl.html'), encoding='utf-8').read()
def rep(m):
    k = m.group(1)
    if k not in F: raise KeyError(k)
    return F[k]
html = re.sub(r'@@(\w+)@@', rep, tpl)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('slides.html', len(html))
