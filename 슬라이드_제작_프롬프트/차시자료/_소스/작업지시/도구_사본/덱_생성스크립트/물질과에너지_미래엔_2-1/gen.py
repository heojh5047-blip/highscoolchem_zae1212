# 2-1 경이로운 물의 성질 — 그림 생성 → slides_tpl.html의 {{이름}}을 채워 slides.html로
import math, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from figs import *

FIG = {}
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/물질과에너지_미래엔/2-1_경이로운_물의_성질/slides.html'
TPL = os.path.join(os.path.dirname(__file__), 'slides_tpl.html')


def g(inner, anim=''):
    return f'<g{(" " + anim) if anim else ""}>{inner}</g>'


# ───────── S1 표지 ─────────
def cover():
    c = W(270, 250, 90)
    nb = [neighbor_via_H(c, 0, -14.5), neighbor_via_H(c, 1, 194.5), neighbor_via_LP(c, 0, -14.5), neighbor_via_LP(c, 1, 194.5)]
    out = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    hb = []
    hb += [hb_line(*c.H[0], nb[0].x, nb[0].y, S1), hb_line(*c.H[1], nb[1].x, nb[1].y, S1)]
    hb += [hb_line(*nb[2].H[1], c.x, c.y, S1), hb_line(*nb[3].H[0], c.x, c.y, S1)]
    out.append(f'<g data-anim="fade" data-dur=".8" data-delay="1.4">{"".join(hb)}</g>')
    for n in nb:
        ux, uy = n.x - c.x, n.y - c.y
        l = math.hypot(ux, uy)
        out.append(f'<g data-anim="move" data-from="{f(ux/l*70)},{f(uy/l*70)}" data-dur="1.2" data-delay=".3" data-ease="out">{n.svg()}</g>')
    out.append(c.svg())
    out.append(legend(150, 505, S6, True, 20))
    return ''.join(out)


# ───────── S2 대단원 도입 칸 그림 ─────────
def intro1():
    a = W(70, 70, 52.25, S6)
    b = neighbor_via_H(a, 0, 52.25)
    c2 = neighbor_via_H(b, 0, 52.25)
    s = hb_line(*a.H[0], b.x, b.y, S6) + hb_line(*b.H[0], c2.x, c2.y, S6)
    return s + a.svg() + b.svg() + c2.svg() + legend(52, 160, S6, True, 18)


def beaker(x, y, w, h, fill='#DDEEF8', level=0.7, sw=3):
    """비커: 왼쪽 위 (x,y), 폭 w, 높이 h. 액면 높이 비율 level"""
    ly = y + h * (1 - level)
    return (f'<rect x="{f(x+2)}" y="{f(ly)}" width="{f(w-4)}" height="{f(y+h-ly-2)}" fill="{fill}"/>'
            f'<line x1="{f(x+2)}" y1="{f(ly)}" x2="{f(x+w-2)}" y2="{f(ly)}" stroke="#9FC3DD" stroke-width="2"/>'
            f'<path d="M{f(x-6)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y+8)} V{f(y+h-8)} Q{f(x)} {f(y+h)} {f(x+8)} {f(y+h)} H{f(x+w-8)} Q{f(x+w)} {f(y+h)} {f(x+w)} {f(y+h-8)} V{f(y)}" fill="none" stroke="#7E8B98" stroke-width="{sw}" stroke-linejoin="round"/>')


def intro2():
    out = [beaker(60, 30, 180, 130, level=0.78)]
    import random
    rnd = random.Random(7)
    pts = []
    while len(pts) < 26:
        x, y = 74 + rnd.random() * 152, 66 + rnd.random() * 84
        if all(math.hypot(x - p[0], y - p[1]) > 17 for p in pts):
            pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        if i % 6 == 0:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="8" fill="#E08A2C" stroke="#A8641C" stroke-width="1.5"/>')
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="6" fill="#8C99A6"/>')
    out.append('<circle cx="70" cy="186" r="6" fill="#8C99A6"/>' + tex(82, 193, '용매', 18))
    out.append('<circle cx="150" cy="186" r="8" fill="#E08A2C" stroke="#A8641C" stroke-width="1.5"/>' + tex(164, 193, '용질', 18))
    return ''.join(out)


def intro3():
    # U자관 + 반투막
    out = []
    x1, x2, top, bot = 80, 220, 20, 150
    wdt = 44
    # 액체 (왼쪽 순수한 물, 오른쪽 용액 — 오른쪽 액면 높음)
    out.append(f'<path d="M{x1} 70 V{bot-20} Q{x1} {bot+wdt-4} {(x1+x2)/2} {bot+wdt-4} Q{x2+wdt} {bot+wdt-4} {x2+wdt} {bot-20} V48 H{x2} V{bot-20} Q{x2} {bot} {(x1+x2+wdt)/2} {bot} Q{x1+wdt} {bot} {x1+wdt} {bot-20} V70 Z" fill="#DDEEF8"/>')
    out.append(f'<rect x="{x2}" y="48" width="{wdt}" height="{bot-48-20}" fill="#F6E7C9" opacity=".8"/>')
    out.append(f'<path d="M{x1} {top} V{bot-20} Q{x1} {bot+wdt} {(x1+x2+wdt)/2} {bot+wdt} Q{x2+wdt} {bot+wdt} {x2+wdt} {bot-20} V{top} M{x1+wdt} {top} V{bot-20} Q{x1+wdt} {bot} {(x1+x2+wdt)/2} {bot} Q{x2} {bot} {x2} {bot-20} V{top}" fill="none" stroke="#7E8B98" stroke-width="3"/>')
    mx = (x1 + x2 + wdt) / 2
    out.append(f'<line x1="{mx}" y1="{bot}" x2="{mx}" y2="{bot+wdt}" stroke="#16233D" stroke-width="3" stroke-dasharray="5 4"/>')
    out.append(tex(mx, 218, '반투막', 21, 'middle'))
    out.append(f'<line x1="{mx}" y1="199" x2="{mx}" y2="{bot+wdt+3}" stroke="#5B6B7F" stroke-width="1.5"/>')
    out.append(tex(x1 + wdt / 2, 10, '물', 21, 'middle'))
    out.append(tex(x2 + wdt / 2, 10, '용액', 21, 'middle'))
    return ''.join(out)


# ───────── S5 호수 두 장 ─────────
def lake(mode):
    out = []
    # 땅
    out.append('<path d="M0 40 H20 Q40 40 60 150 Q80 190 170 192 Q260 190 280 150 Q300 40 320 40 H340 V220 H0 Z" fill="#D9CDB8"/>')
    basin = 'M20 40 Q40 40 60 150 Q80 190 170 192 Q260 190 280 150 Q300 40 320 40 Z'
    out.append(f'<clipPath id="clip-em21-05{mode}"><path d="{basin}"/></clipPath>')
    out.append(f'<g clip-path="url(#clip-em21-05{mode})">')
    out.append('<rect x="0" y="40" width="340" height="160" fill="#DDEEF8"/>')
    if mode == 'a':
        out.append('<rect x="0" y="120" width="340" height="90" fill="#EEF7FC" stroke="#9FC3DD" stroke-width="2"/>')
    else:
        out.append('<rect x="0" y="40" width="340" height="30" fill="#EEF7FC" stroke="#9FC3DD" stroke-width="2"/>')
    out.append('</g>')
    out.append(f'<path d="{basin}" fill="none" stroke="#9A8A6E" stroke-width="2"/>')
    if mode == 'a':
        out.append(tex(170, 158, '얼음', 20, 'middle') + tex(170, 98, '물', 20, 'middle'))
        out.append(tex(170, 28, '(가) 바닥부터 언다', 20, 'middle', mix=True, extra=' data-weight="700"'))
    else:
        out.append(tex(170, 62, '얼음', 20, 'middle') + tex(170, 128, '물', 20, 'middle'))
        # 물고기
        out.append('<g data-anim="move" data-from="-40,0" data-dur="2.4" data-rep="alt" data-ease="io"><path d="M210 150 q18 -12 36 0 q-18 12 -36 0 Z M246 150 l12 -8 v16 Z" fill="#8C99A6" stroke="#16233D" stroke-width="1.5"/><circle cx="217" cy="148" r="1.8" fill="#16233D"/></g>')
        out.append(tex(170, 28, '(나) 표면부터 언다', 20, 'middle', extra=' data-weight="700"'))
    return ''.join(out)


# ───────── S6 물 분자 구조 ─────────
def h2o_struct():
    w = W(200, 150, 90)
    out = [lobes(w, 1.25)]
    # 결합각 호
    r = 96
    a1, a2 = math.radians(w.hd[0]), math.radians(w.hd[1])
    out.append(f'<path d="M{f(w.x+r*math.cos(a1))} {f(w.y+r*math.sin(a1))} A{r} {r} 0 0 1 {f(w.x+r*math.cos(a2))} {f(w.y+r*math.sin(a2))}" fill="none" stroke="{MUTED}" stroke-width="2"/>')
    out.append(tex(200, 150 + r + 26, '104.5^\\circ', 20, 'middle', mix=False))
    out.append(w.svg(labels=True))
    out.append(tex(200, 104, '\\delta^-', 24, 'middle', MINUS, mix=False))
    out.append(tex(w.H[0][0] + 30, w.H[0][1] + 26, '\\delta^+', 24, 'middle', PLUS, mix=False))
    out.append(tex(w.H[1][0] - 30, w.H[1][1] + 26, '\\delta^+', 24, 'middle', PLUS, mix=False))
    out.append(tex(56, 70, '비공유||전자쌍', 18, 'middle', EQUI))
    # 쌍극자 모멘트(합)
    x = 360
    out.append(f'<g data-anim="fade" data-dur=".8" data-delay=".8">{arw(x, 240, x, 110, "plus", 4)}<line x1="{x-7}" y1="221" x2="{x+7}" y2="221" stroke="{PLUS}" stroke-width="4"/>{tex(x, 270, "쌍극자||모멘트", 18, "middle", PLUS)}</g>')
    return ''.join(out)


# ───────── S7 수소 결합 두 분자 ─────────
def hb_pair():
    a = W(110, 140, 52.25)
    b = neighbor_via_H(a, 0, 52.25)
    out = []
    out.append(f'<g data-anim="fade" data-dur=".6" data-delay="1.4">{hb_line(*a.H[0], b.x, b.y, S1)}</g>')
    out.append(a.svg(labels=True))
    inner = lobes(b, 1.1) + b.svg(labels=True) + tex(b.x + 6, b.y - 46, '\\delta^-', 24, 'middle', MINUS, mix=False)
    out.append(f'<g data-anim="move" data-from="70,-30" data-dur="1.2" data-delay=".3" data-ease="out"><g data-anim="rot" data-from="-40" data-o="{f(b.x)},{f(b.y)}" data-dur="1.2" data-delay=".3" data-ease="out">{inner}</g></g>')
    out.append(tex(a.H[0][0], a.H[0][1] - 30, '\\delta^+', 24, 'middle', PLUS, mix=False))
    out.append(tex(a.x - 44, a.y - 4, '\\delta^-', 24, 'middle', MINUS, mix=False))
    # 라벨
    mx = (a.x + a.H[0][0]) / 2
    out.append(f'<line x1="{f(mx)}" y1="{f(a.y+10)}" x2="{f(mx+10)}" y2="226" stroke="{MUTED}" stroke-width="1.5"/>')
    out.append(tex(mx + 10, 248, '공유 결합||(분자 안)', 19, 'middle'))
    hx = (a.H[0][0] + 18 + b.x - 24) / 2
    out.append(f'<line x1="{f(hx)}" y1="{f(a.y+6)}" x2="{f(hx+40)}" y2="226" stroke="{MUTED}" stroke-width="1.5"/>')
    out.append(tex(hx + 60, 248, '수소 결합||(분자 사이)', 19, 'middle'))
    return ''.join(out)


# ───────── S8 분자 하나와 이웃 4개 ─────────
def hb_four():
    c = W(280, 205, 90)
    nb = [neighbor_via_H(c, 0, -14.5), neighbor_via_H(c, 1, 194.5), neighbor_via_LP(c, 0, -14.5), neighbor_via_LP(c, 1, 194.5)]
    out = []
    out.append('<g class="step" data-g="h1">' + hb_line(*c.H[0], nb[0].x, nb[0].y, S1, 3) + hb_line(*c.H[1], nb[1].x, nb[1].y, S1, 3) + '</g>')
    out.append('<g class="step" data-g="h2">' + hb_line(*nb[2].H[1], c.x, c.y, S1, 3) + hb_line(*nb[3].H[0], c.x, c.y, S1, 3) + '</g>')
    for i, n in enumerate(nb):
        out.append(f'<g data-anim="pop" data-o="{f(n.x)},{f(n.y)}" data-dur=".6" data-delay="{.2+.15*i:.2f}">{n.svg()}</g>')
    out.append(f'<circle cx="{c.x}" cy="{c.y}" r="34" fill="#FFE45C" opacity=".45"/>')
    out.append(c.svg(labels=True))
    # 번호 라벨
    def mid(p, q, k=.5):
        return p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k
    m0 = mid(c.H[0], (nb[0].x, nb[0].y))
    m1 = mid(c.H[1], (nb[1].x, nb[1].y))
    m2 = mid(nb[2].H[1], (c.x, c.y), .45)
    m3 = mid(nb[3].H[0], (c.x, c.y), .45)
    out.append(f'<g class="step" data-g="h1">{tex(m0[0]+22, m0[1]+2, "①", 20, "middle")}{tex(m1[0]-22, m1[1]+2, "②", 20, "middle")}</g>')
    out.append(f'<g class="step" data-g="h2">{tex(m2[0]+4, m2[1]-14, "③", 20, "middle")}{tex(m3[0]-4, m3[1]-14, "④", 20, "middle")}</g>')
    out.append(legend(12, 400, S6, True, 19))
    return ''.join(out)


# ───────── S10 끓는점 그래프 ─────────
def bp_graph():
    X = {2: 130, 3: 250, 4: 370, 5: 490}
    Y = lambda t: 40 + (120 - t) * 290 / 220
    out = []
    # 축
    out.append(f'<line x1="70" y1="330" x2="540" y2="330" stroke="{MUTED}" stroke-width="2"/><line x1="70" y1="330" x2="70" y2="26" stroke="{MUTED}" stroke-width="2"/>')
    for t in (-100, -50, 0, 50, 100):
        y = Y(t)
        out.append(f'<line x1="64" y1="{f(y)}" x2="540" y2="{f(y)}" stroke="#E2E7EC" stroke-width="1.5"/>' if t != -100 else '')
        out.append(tex(58, y + 6, str(t).replace('-', '−'), 18, 'end', MUTED))
    for p, x in X.items():
        out.append(f'<line x1="{x}" y1="330" x2="{x}" y2="336" stroke="{MUTED}" stroke-width="2"/>' + tex(x, 356, str(p), 18, 'middle', MUTED))
    out.append(tex(305, 380, '주기', 19, 'middle'))
    out.append(tex(80, 18, '끓는점 $t$ [°C]', 19))
    # 실온
    out.append(f'<line x1="70" y1="{f(Y(25))}" x2="540" y2="{f(Y(25))}" stroke="{EQUI}" stroke-width="2" stroke-dasharray="6 5"/>' + tex(536, Y(25) - 8, '실온 25 °C', 18, 'end', EQUI))
    data = {2: 100, 3: -60, 4: -41, 5: -2}
    pts = ' '.join(f'{X[p]},{f(Y(t))}' for p, t in data.items())
    out.append(f'<polyline points="{pts}" fill="none" stroke="{MINUS}" stroke-width="3"/>')
    for p in (3, 4, 5):
        out.append(f'<circle cx="{X[p]}" cy="{f(Y(data[p]))}" r="7" fill="{MINUS}"/>')
    out.append(tex(X[3], Y(-60) + 30, '\\ce{H2S}||−60', 18, 'middle', mix=True).replace('data-mix="\\ce{H2S}||−60"', 'data-mix="$\\ce{H2S}$||−60"'))
    out.append(tex(X[4], Y(-41) + 30, '$\\ce{H2Se}$||−41', 18, 'middle'))
    out.append(tex(X[5], Y(-2) + 30, '$\\ce{H2Te}$||−2', 18, 'middle'))
    # 물 점
    dy = Y(-80) - Y(100)
    out.append(f'<g data-anim="move" data-from="0,{f(dy)}" data-dur="1.2" data-delay=".6" data-ease="back"><circle cx="{X[2]}" cy="{f(Y(100))}" r="9" fill="{MINUS}"/>{tex(X[2]+16, Y(100)+8, "$\\ce{H2O}$ 100", 19)}</g>')
    # 예상
    out.append(f'<g class="step" data-g="p1"><line x1="{X[3]}" y1="{f(Y(-60))}" x2="{X[2]}" y2="{f(Y(-80))}" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="7 5"/><circle cx="{X[2]}" cy="{f(Y(-80))}" r="8" fill="#fff" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="4 3"/>{tex(X[2]-12, Y(-80)+30, "예상 약 −80", 18, "start", MUTED)}</g>')
    return ''.join(out)


# ───────── S11 상태 변화 카드 ─────────
def card_ice():
    s, n, P = ice(112, 118, 2, 1, S6)
    return f'<g data-anim="move" data-from="1.6,0" data-dur=".12" data-rep="swing" data-ease="sine">{s}</g>', n


def card_liquid(n):
    mols, hbs = liquid2(20, 22, 4, 3, 76, 64, seed=11)
    return ''.join(hbs) + ''.join(m.svg() for m in mols)


def card_gas():
    pos = [(60, 60, 30), (250, 50, 200), (150, 120, 120), (60, 190, 300), (270, 180, 60)]
    out = []
    for i, (x, y, ph) in enumerate(pos):
        w = W(x, y, ph, S6)
        a = (ph + 90 + 60 * i) % 360
        ex, ey = x + 40 * d(a)[0], y + 40 * d(a)[1]
        out.append(f'<g data-anim="move" data-from="{f(-14*d(a)[0])},{f(-14*d(a)[1])}" data-dur="1.4" data-rep="alt" data-ease="io">{w.svg()}{arw(x+18*d(a)[0], y+18*d(a)[1], ex+10*d(a)[0], ey+10*d(a)[1], "ink", 2)}</g>')
    return ''.join(out)


# ───────── S12 비열 막대 ─────────
def sh_bars():
    data = [('물', 4.2, MINUS), ('에탄올', 2.5, INK), ('공기', 1.02, INK), ('철', 0.45, INK), ('구리', 0.39, INK)]
    out = []
    for i, (nm, v, col) in enumerate(data):
        y = 20 + i * 48
        out.append(tex(84, y + 24, nm, 20, 'end'))
        w = v * 88
        out.append(f'<g data-anim="scale" data-from="0,1" data-o="96,{y+16}" data-dur="1" data-delay="{.2+.12*i:.2f}" data-ease="out"><rect x="96" y="{y}" width="{f(w)}" height="32" rx="4" fill="{col}" opacity="{1 if i==0 else .55}"/></g>')
        out.append(tex(96 + w + 10, y + 24, f'{v:g}' if v != 4.2 and v != 2.5 else f'{v:.1f}', 20))
    out.append(tex(96, 270, '비열 [J/(g·°C)] (자료: CRC Handbook)', 18, 'start', MUTED))
    return ''.join(out)


# ───────── S15 생활 카드 ─────────
def daily():
    out = [f'<line x1="40" y1="150" x2="300" y2="150" stroke="{MUTED}" stroke-width="2"/><line x1="40" y1="150" x2="40" y2="30" stroke="{MUTED}" stroke-width="2"/>']
    p1, p2 = [], []
    for k in range(0, 25):
        x = 40 + k * 10.5
        ph = math.cos((k - 14) / 24 * 2 * math.pi)
        p1.append(f'{f(x)},{f(85 - 50*ph)}')
        p2.append(f'{f(x)},{f(85 - 16*ph)}')
    out.append(f'<polyline points="{" ".join(p1)}" fill="none" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<polyline points="{" ".join(p2)}" fill="none" stroke="{MINUS}" stroke-width="3" stroke-dasharray="7 5"/>')
    out.append(tex(196, 30, '내륙', 18, 'start', INK) + tex(262, 124, '해안', 18, 'start', MINUS))
    out.append(tex(170, 176, '하루 시각', 18, 'middle', MUTED) + tex(48, 22, '기온', 18, 'start', MUTED))
    return ''.join(out)


def person():
    return ('<circle cx="80" cy="42" r="22" fill="#DDEEF8" stroke="#16233D" stroke-width="2.5"/>'
            '<path d="M44 160 V100 Q44 72 80 72 Q116 72 116 100 V160 Z" fill="#DDEEF8" stroke="#16233D" stroke-width="2.5"/>'
            '<rect x="46" y="118" width="68" height="40" fill="#9FC3DD" opacity=".6"/>'
            + tex(80, 112, '물', 18, 'middle') + tex(220, 70, '체온', 19, 'middle') + tex(220, 100, '약 37 °C', 22, 'middle', PLUS) + tex(220, 134, '몸의||60 % 이상이 물', 18, 'middle', MUTED))


def radiator():
    out = ['<rect x="30" y="50" width="100" height="80" rx="8" fill="#E6EAEE" stroke="#16233D" stroke-width="2.5"/>',
           tex(80, 98, '엔진', 20, 'middle'),
           '<rect x="210" y="40" width="70" height="100" rx="6" fill="#F4F6F8" stroke="#16233D" stroke-width="2.5"/>',
           '<g stroke="#9FB0C2" stroke-width="2">' + ''.join(f'<line x1="218" y1="{y}" x2="272" y2="{y}"/>' for y in range(52, 136, 12)) + '</g>',
           tex(245, 164, '방열기', 18, 'middle'),
           '<path d="M130 70 H210 M210 110 H130" fill="none" stroke="#9FC3DD" stroke-width="8"/>',
           '<path d="M130 70 H210 M210 110 H130" fill="none" stroke="#1F6FD1" stroke-width="3" stroke-dasharray="8 8" data-anim="dash" data-speed="30" data-flow=""/>',
           tex(170, 60, '냉각수', 18, 'middle', MINUS)]
    return ''.join(out)


# ───────── S16 기화열 막대 + 땀 ─────────
def hv_bars():
    data = [('\\ce{CH4}', 8.2, INK, '16'), ('\\ce{NH3}', 23.3, INK, '17'), ('\\ce{H2O}', 40.7, MINUS, '18')]
    out = [f'<line x1="40" y1="270" x2="330" y2="270" stroke="{MUTED}" stroke-width="2"/>']
    for i, (fm, v, col, mw) in enumerate(data):
        x = 70 + i * 90
        h = v * 5.0
        out.append(f'<g data-anim="scale" data-from="1,0" data-o="{x+25},270" data-dur="1" data-delay="{.2+.15*i:.2f}" data-ease="out"><rect x="{x}" y="{f(270-h)}" width="50" height="{f(h)}" rx="3" fill="{col}" opacity="{1 if i==2 else .55}"/></g>')
        out.append(tex(x + 25, 262 - h, f'{v:g}', 20, 'middle'))
        out.append(tex(x + 25, 298, f'${fm}$', 20, 'middle'))
        out.append(tex(x + 25, 322, f'분자량 {mw}', 18, 'middle', MUTED))
    out.append(tex(40, 20, '기화열 [kJ/mol] (기준 끓는점)', 18, 'start', MUTED))
    return ''.join(out)


def sweat():
    out = ['<rect x="0" y="200" width="380" height="70" fill="#F3D9C6"/>',
           '<line x1="0" y1="200" x2="380" y2="200" stroke="#B98A6A" stroke-width="2"/>',
           tex(16, 254, '피부', 19, 'start', '#7A5236'),
           '<path d="M120 200 Q120 150 190 148 Q260 150 260 200 Z" fill="#DDEEF8" stroke="#9FC3DD" stroke-width="2"/>',
           tex(190, 188, '땀', 19, 'middle')]
    # 떠나는 물 분자
    for i, (x, y, ph) in enumerate([(150, 78, 60), (232, 60, 130), (300, 106, 20)]):
        w = W(x, y, ph, S6)
        out.append(f'<g data-anim="move" data-from="{f((190-x)*.8)},{f((165-y)*.8)}" data-dur="1.6" data-delay="{.3+.4*i:.1f}" data-ease="out">{w.svg()}</g>')
    out.append(arw(70, 236, 140, 182, 'equi', 4))
    out.append(tex(26, 140, '열 흡수||(몸 → 땀)', 18, 'start', EQUI))
    out.append(tex(330, 40, '증발', 19, 'middle', MUTED))
    out.append(legend(160, 290, S6, False, 18))
    return ''.join(out)


# ───────── S17 비커 두 개 ─────────
def float_sink():
    out = [beaker(30, 40, 190, 200, '#DDEEF8', .72), beaker(300, 40, 190, 200, '#F3E9C6', .72)]
    ly = 40 + 200 * .28
    out.append(f'<g data-anim="move" data-from="0,90" data-dur="1.4" data-delay=".4" data-ease="out"><rect x="95" y="{f(ly-10)}" width="60" height="56" rx="6" fill="#EEF7FC" stroke="#7FB3D5" stroke-width="2.5"/></g>')
    out.append(f'<g data-anim="move" data-from="0,-130" data-dur="1.4" data-delay=".4" data-ease="in"><rect x="365" y="186" width="60" height="50" rx="6" fill="#FBF6E4" stroke="#B8A26A" stroke-width="2.5"/></g>')
    out.append(tex(125, 30, '(가) 물과 얼음', 20, 'middle', extra=' data-weight="700"'))
    out.append(tex(395, 30, '(나) 파라핀', 20, 'middle', extra=' data-weight="700"'))
    out.append(tex(125, 152, '얼음', 19, 'middle') + tex(125, 218, '물', 19, 'middle'))
    out.append(tex(395, 180, '고체', 19, 'middle') + tex(395, 140, '액체', 19, 'middle'))
    return ''.join(out)


# ───────── S18 얼음과 물 ─────────
def ice_panel():
    s, n, P = ice(150, 112, 2, 2, S6)
    holes = []
    D = S6['L'] + S6['hb']
    for r in range(2):
        for cidx in range(2):
            cx = 150 + cidx * math.sqrt(3) * D + (r % 2) * math.sqrt(3) * D / 2
            cy = 112 + r * 1.5 * D
            holes.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="40" fill="#FFE45C" opacity=".4" stroke="{EQUI}" stroke-width="2" stroke-dasharray="5 4"/>')
    return f'<g class="step" data-g="i1">{"".join(holes)}</g>' + s, n, P


def water_panel(n):
    mols, hbs = liquid2(110, 96, 4, 4, 90, 64, seed=5, region=(30, 40, 500, 320))
    out = ''.join(hbs)
    for i, m in enumerate(mols):
        if i % 5 == 2:
            out += f'<g data-anim="move" data-from="{(-1)**i*24},{-20}" data-dur="1.4" data-delay=".5" data-ease="out">{m.svg()}</g>'
        else:
            out += m.svg()
    return out


# ───────── S19 밀도 그래프 ─────────
RHO = [0.99984, 0.99990, 0.99994, 0.99996, 0.99997, 0.99996, 0.99994, 0.99990, 0.99985, 0.99978, 0.99970,
       0.99961, 0.99950, 0.99938, 0.99924, 0.99910, 0.99894, 0.99877, 0.99860, 0.99841, 0.99821]


def rho_graph(tmax=20, lo=0.9980, hi=1.0002, ticks=(0.9980, 0.9985, 0.9990, 0.9995, 1.0000), W0=600, show4=True, anim=True, xstep=None):
    x0, x1, y0, y1 = 96, W0 - 30, 330, 40
    X = lambda t: x0 + (x1 - x0) * t / tmax
    Y = lambda r: y0 - (r - lo) / (hi - lo) * (y0 - y1)
    out = [f'<line x1="{x0}" y1="{y0}" x2="{x1+10}" y2="{y0}" stroke="{MUTED}" stroke-width="2"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1-14}" stroke="{MUTED}" stroke-width="2"/>']
    for r in ticks:
        out.append(f'<line x1="{x0-6}" y1="{f(Y(r))}" x2="{x1}" y2="{f(Y(r))}" stroke="#E2E7EC" stroke-width="1.5"/>' + tex(x0 - 10, Y(r) + 6, f'{r:.4f}', 18, 'end', MUTED))
    step = xstep or (4 if tmax == 20 else 2)
    for t in range(0, tmax + 1, step):
        out.append(f'<line x1="{f(X(t))}" y1="{y0}" x2="{f(X(t))}" y2="{y0+6}" stroke="{MUTED}" stroke-width="2"/>' + tex(X(t), y0 + 26, str(t), 18, 'middle', MUTED))
    out.append(tex((x0 + x1) / 2, y0 + 52, '온도 $t$ [°C]', 19, 'middle'))
    out.append(tex(x0 + 8, y1 - 18, '밀도 $d$ [g/cm³]', 19).replace('g/cm³', 'g/cm$^3$'))
    pts = ' '.join(f'{f(X(t))},{f(Y(RHO[t]))}' for t in range(0, tmax + 1))
    an = ' data-anim="draw" data-dur="1.8" data-delay=".3"' if anim else ''
    out.append(f'<polyline points="{pts}" fill="none" stroke="{MINUS}" stroke-width="3.5" stroke-linejoin="round"{an}/>')
    if show4:
        out.append(f'<line x1="{f(X(4))}" y1="{f(Y(RHO[4]))}" x2="{f(X(4))}" y2="{y0}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>')
        out.append(f'<circle cx="{f(X(4))}" cy="{f(Y(RHO[4]))}" r="7" fill="{MINUS}"/>')
    return ''.join(out), X, Y


# ───────── S20 호수 3장 ─────────
def lake3(k):
    out = ['<path d="M0 30 H14 Q30 30 44 120 Q60 160 150 162 Q240 160 256 120 Q270 30 286 30 H300 V190 H0 Z" fill="#D9CDB8"/>']
    basin = 'M14 30 Q30 30 44 120 Q60 160 150 162 Q240 160 256 120 Q270 30 286 30 Z'
    out.append(f'<clipPath id="clip-em21-20{k}"><path d="{basin}"/></clipPath><g clip-path="url(#clip-em21-20{k})">')
    if k == 1:
        out.append('<rect x="0" y="30" width="300" height="140" fill="#DDEEF8"/><rect x="0" y="30" width="300" height="34" fill="#E3EEFB"/>')
    elif k == 2:
        out.append('<rect x="0" y="30" width="300" height="140" fill="#D4E6F5"/><rect x="0" y="30" width="300" height="26" fill="#EAF2FB"/>')
    else:
        out.append('<rect x="0" y="30" width="300" height="140" fill="#D4E6F5"/>')
        out.append('<g data-anim="scale" data-from="1,0" data-o="150,30" data-dur="1.4" data-delay=".3" data-ease="out"><rect x="0" y="30" width="300" height="28" fill="#EEF7FC" stroke="#9FC3DD" stroke-width="2"/></g>')
    out.append('</g>' + f'<path d="{basin}" fill="none" stroke="#9A8A6E" stroke-width="2"/>')
    if k == 1:
        out.append(arw(110, 54, 110, 128, 'ink', 3) + arw(190, 54, 190, 128, 'ink', 3))
        out.append(tex(150, 52, '4 °C', 19, 'middle') + tex(150, 142, '무거운 물이 가라앉음', 18, 'middle'))
    elif k == 2:
        out.append(tex(150, 50, '0–3 °C (가벼워 위에 남음)', 18, 'middle') + tex(150, 120, '4 °C', 20, 'middle'))
    else:
        out.append(tex(150, 52, '얼음 0 °C', 19, 'middle') + tex(150, 120, '물 약 4 °C', 20, 'middle'))
        out.append('<path d="M196 138 q14 -10 28 0 q-14 10 -28 0 Z M224 138 l10 -7 v14 Z" fill="#8C99A6" stroke="#16233D" stroke-width="1.5"/>')
    return ''.join(out)


# ───────── S21 동전 카드 ─────────
def coin(x, y, rx=46):
    return (f'<ellipse cx="{x}" cy="{y+6}" rx="{rx}" ry="{rx*.3:.1f}" fill="#8A919C"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*.3:.1f}" fill="#C9CED6" stroke="#7E8B98" stroke-width="2"/>')


def coins(k):
    out = ['<rect x="0" y="120" width="300" height="10" fill="#E6EAEE"/>']
    if k == 1:
        out += [coin(80, 112), coin(220, 112), tex(80, 160, '물', 19, 'middle'), tex(220, 160, '에탄올', 19, 'middle')]
    elif k == 2:
        out += [coin(150, 112), '<rect x="140" y="10" width="20" height="60" rx="4" fill="#F4F6F8" stroke="#7E8B98" stroke-width="2"/><path d="M144 70 L150 88 L156 70 Z" fill="#F4F6F8" stroke="#7E8B98" stroke-width="2"/><ellipse cx="150" cy="100" rx="5" ry="7" fill="#DDEEF8" stroke="#6E9CCB" stroke-width="1.5"/>',
                tex(184, 40, '스포이트', 18)]
    else:
        out += [coin(80, 112), coin(220, 112)]
        out.append('<g data-anim="scale" data-from="1,0.2" data-o="80,110" data-dur="1.4" data-delay=".4" data-ease="out"><path d="M36 110 Q38 60 80 58 Q122 60 124 110 Z" fill="#DDEEF8" stroke="#6E9CCB" stroke-width="2"/></g>')
        out.append('<path d="M176 110 Q180 96 220 95 Q260 96 264 110 Z" fill="#F4F6F8" stroke="#8C99A6" stroke-width="2"/>')
        out += [tex(80, 160, '물: 둥글고 높게', 19, 'middle'), tex(220, 160, '에탄올: 납작', 19, 'middle')]
    return ''.join(out)


# ───────── S22 표면 장력 ─────────
def surface():
    out = ['<rect x="20" y="90" width="480" height="230" fill="#DDEEF8"/><line x1="20" y1="90" x2="500" y2="90" stroke="#9FC3DD" stroke-width="3"/>']
    r = 17
    pos = []
    for row in range(4):
        for col in range(9):
            x = 52 + col * 52 + (row % 2) * 26
            y = 110 + row * 50
            if x < 490:
                pos.append((x, y))
    S = (234, 110)   # 표면 분자
    I = (260, 210)   # 내부 분자
    for p in pos:
        hl = p == S or p == I
        out.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" fill="{"#7FB3D5" if hl else "#BFD9EE"}" stroke="#6E9CCB" stroke-width="{2.5 if hl else 1.5}"/>')
    # 내부: 6방향
    for a in (0, 60, 120, 180, 240, 300):
        out.append(arw(I[0] + 18 * d(a)[0], I[1] + 18 * d(a)[1], I[0] + 46 * d(a)[0], I[1] + 46 * d(a)[1], 'ink', 2.5))
    for a in (0, 180, 60, 120):
        out.append(arw(S[0] + 18 * d(a)[0], S[1] + 18 * d(a)[1], S[0] + 46 * d(a)[0], S[1] + 46 * d(a)[1], 'ink', 2.5))
    out.append(f'<g data-anim="fade" data-dur=".8" data-delay="1.2">{arw(S[0]-74, S[1]-8, S[0]-74, S[1]+60, "plus", 5)}{tex(S[0]-84, S[1]+30, "알짜 인력||(안쪽으로)", 19, "end", PLUS, extra=' data-halo="1"')}</g>')
    out.append(tex(S[0] + 4, 60, '표면의 분자: 위쪽에는 당기는 분자가 없다', 19, 'middle'))
    out.append(f'<line x1="{S[0]}" y1="68" x2="{S[0]}" y2="{S[1]-r-2}" stroke="{MUTED}" stroke-width="1.5"/>')
    out.append(tex(380, 300, '내부의 분자: 합 0', 19, 'middle', mix=True, extra=' data-halo="1"'))
    out.append(f'<line x1="330" y1="286" x2="{I[0]+20}" y2="{I[1]+14}" stroke="{MUTED}" stroke-width="1.5"/>')
    out.append(f'<circle cx="40" cy="352" r="12" fill="#BFD9EE" stroke="#6E9CCB" stroke-width="1.5"/>' + tex(60, 359, '물 분자(공 하나로 단순화) · 화살표 = 이웃 분자가 당기는 힘', 18))
    return ''.join(out)


# ───────── S23 모세관 ─────────
def capillary():
    out = [beaker(30, 140, 400, 190, '#DDEEF8', .62)]
    surf = 140 + 190 * .38
    tubes = [(110, 34, 40), (230, 20, 75), (340, 10, 140)]
    for i, (cx, w, h) in enumerate(tubes):
        top = surf - h
        x1, x2 = cx - w / 2, cx + w / 2
        # 물기둥
        out.append(f'<g data-anim="scale" data-from="1,0" data-o="{cx},{f(surf)}" data-dur="1.4" data-delay="{.3+.25*i:.2f}" data-ease="out"><path d="M{f(x1)} {f(surf)} V{f(top)} Q{cx} {f(top+w*.45)} {f(x2)} {f(top)} V{f(surf)} Z" fill="#9FC3DD"/></g>')
        out.append(f'<rect x="{f(x1-3)}" y="20" width="{w+6}" height="{f(300-20)}" fill="none" stroke="#7E8B98" stroke-width="3"/>')
        out.append(tex(cx, 352, ['굵은 관', '중간 관', '가는 관'][i], 18, 'middle'))
    out.append(f'<line x1="440" y1="{f(surf)}" x2="470" y2="{f(surf)}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 3"/>' + tex(474, surf + 6, '바깥 수면', 18))
    return ''.join(out)


def wall_zoom():
    out = ['<rect x="0" y="0" width="240" height="220" fill="#FFFFFF"/>',
           '<rect x="0" y="0" width="34" height="220" fill="#E6EDF2"/><line x1="34" y1="0" x2="34" y2="220" stroke="#7E8B98" stroke-width="3"/>',
           tex(22, 196, '유리', 18, 'middle', mix=True).replace('data-size="18"', 'data-size="18" data-halo="1"'),
           '<path d="M34 40 Q60 110 240 120 V220 H34 Z" fill="#DDEEF8"/>']
    mol = [(58, 92), (60, 140), (104, 132), (96, 180), (150, 168), (200, 172)]
    for x, y in mol:
        out.append(f'<circle cx="{x}" cy="{y}" r="14" fill="#BFD9EE" stroke="#6E9CCB" stroke-width="1.5"/>')
    out.append(arw(44, 92, 38, 92, 'ink', 3).replace('44,92,38,92', '62,72,37,72'))
    out.append(arw(56, 140, 37, 140, 'ink', 3).replace('56,140,37,140', '46,140,37,140'))
    out.append(tex(64, 40, '관 표면과 물 사이의 인력', 18, 'start'))
    out.append(arw(118, 132, 146, 158, 'ink', 2.5) + arw(110, 180, 136, 172, 'ink', 2.5))
    out.append(tex(140, 214, '물의 표면 장력', 18, 'middle'))
    return ''.join(out)


# ───────── S24 수화 ─────────
def hydration():
    out = []
    na, cl = (150, 150), (440, 150)
    for k in range(4):
        a = -45 + 90 * k
        o = (na[0] + 47 * d(a)[0], na[1] + 47 * d(a)[1])
        w = W(o[0], o[1], a, S1)
        out.append(f'<g data-anim="rot" data-from="{150 if k%2 else -150}" data-o="{f(o[0])},{f(o[1])}" data-dur="1.3" data-delay="{.3+.08*k:.2f}" data-ease="out">{w.svg()}</g>')
    out.append(atom(na[0], na[1], 19, 'Na', '-') + tex(na[0], na[1] + 7, '\\ce{Na+}', 18, 'middle', '#FFFFFF', mix=False))
    for k in range(5):
        a = -90 + 72 * k + 36
        hpos = 54
        ox, oy = cl[0] + (hpos + S1['L']) * d(a)[0], cl[1] + (hpos + S1['L']) * d(a)[1]
        phi = a + 180 + HALF
        w = W(ox, oy, phi, S1)
        out.append(f'<g data-anim="rot" data-from="{150 if k%2 else -150}" data-o="{f(ox)},{f(oy)}" data-dur="1.3" data-delay="{.3+.08*k:.2f}" data-ease="out">{w.svg()}</g>')
    out.append(atom(cl[0], cl[1], 32, 'Cl', '-') + tex(cl[0], cl[1] + 8, '\\ce{Cl-}', 22, 'middle', '#FFFFFF', mix=False))
    return ''.join(out)


# ───────── S28 확인 문제 01 ─────────
def q1_chain():
    a = W(90, 120, 52.25)
    b = neighbor_via_H(a, 0, 52.25)
    c = neighbor_via_H(b, 0, 52.25)
    out = [hb_line(*a.H[0], b.x, b.y, S1), hb_line(*b.H[0], c.x, c.y, S1), a.svg(True), b.svg(True), c.svg(True)]
    mx = (b.x + b.H[0][0]) / 2
    out.append(tex(mx, b.y - 22, 'a', 22, 'middle', extra=' data-weight="700"'))
    hx = (a.H[0][0] + b.x) / 2
    out.append(tex(hx, a.y - 22, 'b', 22, 'middle', extra=' data-weight="700"'))
    return ''.join(out)


FIG['cover'] = cover()
FIG['intro1'] = intro1()
FIG['intro2'] = intro2()
FIG['intro3'] = intro3()
FIG['lake_a'] = lake('a')
FIG['lake_b'] = lake('b')
FIG['h2o'] = h2o_struct()
FIG['hbpair'] = hb_pair()
FIG['hbfour'] = hb_four()
FIG['bp'] = bp_graph()
ic, nice = card_ice()
FIG['c_ice'] = ic
FIG['c_liq'] = card_liquid(10)
FIG['c_gas'] = card_gas()
FIG['shbars'] = sh_bars()
FIG['daily'] = daily()
FIG['person'] = person()
FIG['radiator'] = radiator()
FIG['hvbars'] = hv_bars()
FIG['sweat'] = sweat()
FIG['floatsink'] = float_sink()
ip, nip, _ = ice_panel()
FIG['icepanel'] = ip + legend(20, 345, S6, True, 18)
FIG['waterpanel'] = water_panel(nip) + legend(20, 345, S6, True, 18)
FIG['N_ICE'] = str(nip)
rg, X, Y = rho_graph()
rg += tex(X(4) + 14, Y(RHO[4]) - 12, '4 °C에서 밀도 최대', 19, 'start', INK)
FIG['rho'] = rg
FIG['lake1'] = lake3(1)
FIG['lake2'] = lake3(2)
FIG['lake3'] = lake3(3)
FIG['coin1'] = coins(1)
FIG['coin2'] = coins(2)
FIG['coin3'] = coins(3)
FIG['surface'] = surface()
FIG['capillary'] = capillary()
FIG['wallzoom'] = wall_zoom()
FIG['hydration'] = hydration()
FIG['q1'] = q1_chain()
rg2, X2, Y2 = rho_graph(10, 0.9996, 1.00002, (0.9996, 0.9997, 0.9998, 0.9999, 1.0000), 560, show4=False, anim=False, xstep=2)
FIG['rho2'] = rg2


# ───────── 교과서 대조 뒤 추가 그림 ─────────
def planet():
    out = ['<rect x="0" y="0" width="420" height="220" fill="#F3D2B6"/>',
           '<path d="M0 150 Q100 120 200 140 T420 130 V220 H0 Z" fill="#E4B48E"/>',
           '<path d="M20 60 Q80 70 120 100 Q150 120 170 160 Q190 190 260 200 M120 100 Q150 80 200 84 M170 160 Q220 150 280 160 Q330 168 400 150" fill="none" stroke="#B9835C" stroke-width="7" stroke-linecap="round"/>',
           '<path d="M20 60 Q80 70 120 100 Q150 120 170 160 Q190 190 260 200 M120 100 Q150 80 200 84 M170 160 Q220 150 280 160 Q330 168 400 150" fill="none" stroke="#9FC3DD" stroke-width="2.5" stroke-dasharray="6 6" data-anim="dash" data-speed="24" data-flow=""/>',
           '<circle cx="360" cy="46" r="22" fill="#F0E2D0" stroke="#C9A37E" stroke-width="2"/>',
           '<rect x="210" y="14" width="196" height="40" rx="12" fill="#FFFFFF" stroke="#16233D" stroke-width="2"/>',
           '<path d="M240 54 L232 70 L256 54 Z" fill="#FFFFFF" stroke="#16233D" stroke-width="2" stroke-linejoin="round"/><line x1="241" y1="54" x2="253" y2="54" stroke="#FFFFFF" stroke-width="3"/>',
           tex(308, 41, '이건 물이 흘렀던 흔적?', 19, 'middle'),
           tex(14, 210, '다른 행성 표면의 골짜기(모식도)', 18, 'start', MUTED)]
    return ''.join(out)


def breeze(day):
    out = []
    out.append('<rect x="0" y="0" width="320" height="200" fill="#EEF3F8"/>')
    out.append('<path d="M0 150 H170 Q180 150 186 158 L196 200 H0 Z" fill="#C9B79C"/>')
    out.append('<path d="M186 158 Q190 150 200 150 H320 V200 H196 Z" fill="#9FC3DD"/>')
    out.append(tex(80, 182, '육지', 19, 'middle') + tex(262, 182, '바다', 19, 'middle'))
    if day:
        out.append('<circle cx="170" cy="30" r="16" fill="#F2C230"/>')
        out.append(f'<g data-anim="move" data-from="40,0" data-dur="1.6" data-rep="loop" data-ease="lin">{arw(280, 120, 120, 120, "ink", 4)}</g>')
        out.append(tex(200, 106, '해풍', 20, 'middle', extra=' data-weight="700"'))
        out.append(tex(80, 60, '빨리 데워짐', 18, 'middle', PLUS) + tex(262, 60, '천천히 데워짐', 18, 'middle', MINUS))
    else:
        out.append('<path d="M286 22 a16 16 0 1 0 14 26 a12 12 0 1 1 -14 -26 Z" fill="#9AA5B1"/>')
        out.append(f'<g data-anim="move" data-from="-40,0" data-dur="1.6" data-rep="loop" data-ease="lin">{arw(60, 120, 220, 120, "ink", 4)}</g>')
        out.append(tex(140, 106, '육풍', 20, 'middle', extra=' data-weight="700"'))
        out.append(tex(80, 60, '빨리 식음', 18, 'middle', MINUS) + tex(240, 60, '천천히 식음', 18, 'middle', PLUS))
    return ''.join(out)


def sch_graph(kind, w=470, h=330, anim=True):
    """교과서 그림 II-5·II-6 꼴 모식 그래프(−4–10 °C). kind 'v' 부피 / 'd' 밀도"""
    x0, x1, y0, y1 = 96, w - 20, h - 62, 50
    X = lambda t: x0 + (x1 - x0) * (t + 4) / 14
    out = [f'<line x1="{x0}" y1="{y0}" x2="{x1+6}" y2="{y0}" stroke="{MUTED}" stroke-width="2"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1-12}" stroke="{MUTED}" stroke-width="2"/>']
    for t in (-4, -2, 0, 2, 4, 6, 8, 10):
        out.append(f'<line x1="{f(X(t))}" y1="{y0}" x2="{f(X(t))}" y2="{y0+6}" stroke="{MUTED}" stroke-width="2"/>' + tex(X(t), y0 + 25, str(t).replace('-', '−'), 18, 'middle', MUTED))
    out.append(tex((x0 + x1) / 2 + 40, y0 + 48, '온도 [°C]', 19, 'middle'))
    # 축 끊김 표시
    yb = (y0 + y1) / 2 + 10
    out.append(f'<path d="M{x0-8} {yb+4} l8 -6 l8 6 M{x0-8} {yb+12} l8 -6 l8 6" fill="none" stroke="{MUTED}" stroke-width="2"/>'.replace(f'M{x0-8} {yb+4}', f'M{x0-8} {f(yb+4)}').replace(f'M{x0-8} {yb+12}', f'M{x0-8} {f(yb+12)}'))
    an = ' data-anim="draw" data-dur="1.6" data-delay=".3"' if anim else ''
    if kind == 'v':
        yt, yw = y1 + 10, y0 - 40            # 1.0909, 1.0000
        out.append(tex(x0 - 10, yt + 6, '1.0909', 18, 'end', MUTED) + tex(x0 - 10, yw + 6, '1.0000', 18, 'end', MUTED))
        out.append(tex(x0 + 8, y1 - 16, '물 1 g의 부피 [cm³]', 19).replace('cm³', 'cm$^3$'))
        out.append(f'<line x1="{x0}" y1="{yt}" x2="{f(X(0))}" y2="{yt}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        out.append(f'<line x1="{x0}" y1="{yw}" x2="{f(X(4))}" y2="{yw}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        out.append(f'<line x1="{f(X(-4))}" y1="{yt+30}" x2="{f(X(0))}" y2="{yt}" stroke="{EQUI}" stroke-width="3.5"{an}/>')
        out.append(f'<line x1="{f(X(0))}" y1="{yt}" x2="{f(X(0))}" y2="{yw-14}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>')
        pts = ' '.join(f'{f(X(t/2))},{f(yw - 14 + 14 - 1.4*((t/2-4)**2) * -1 - 14 if False else yw - 1.3*((t/2-4)**2)*-1 - 0)}' for t in range(0, 21))
        pts = ' '.join(f'{f(X(t/2))},{f(yw - 1.3*((t/2-4)**2))}' for t in range(0, 21))
        pts = ' '.join(f'{f(X(t/2))},{f(yw - 0.9*((t/2-4)**2) )}' for t in range(0, 21))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{MINUS}" stroke-width="3.5"{an}/>')
        out.append(tex(X(-2) - 4, yt + 52, '얼음', 19, 'middle', EQUI) + tex(X(6), yw - 22, '물', 19, 'middle', MINUS))
    else:
        yw, yi = y1 + 10, y0 - 40           # 1.0000, 0.9167
        out.append(tex(x0 - 10, yw + 6, '1.0000', 18, 'end', MUTED) + tex(x0 - 10, yi + 6, '0.9167', 18, 'end', MUTED))
        out.append(tex(x0 + 8, y1 - 16, '밀도 [g/cm³]', 19).replace('g/cm³', 'g/cm$^3$'))
        out.append(f'<line x1="{x0}" y1="{yw}" x2="{f(X(4))}" y2="{yw}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        out.append(f'<line x1="{x0}" y1="{yi}" x2="{f(X(0))}" y2="{yi}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        out.append(f'<line x1="{f(X(-4))}" y1="{yi-26}" x2="{f(X(0))}" y2="{yi}" stroke="{EQUI}" stroke-width="3.5"{an}/>')
        out.append(f'<line x1="{f(X(0))}" y1="{yi}" x2="{f(X(0))}" y2="{yw+16}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>')
        pts = ' '.join(f'{f(X(t/2))},{f(yw + 1.0*((t/2-4)**2))}' for t in range(0, 21))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{MINUS}" stroke-width="3.5"{an}/>')
        out.append(f'<line x1="{f(X(4))}" y1="{yw}" x2="{f(X(4))}" y2="{y0}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/><circle cx="{f(X(4))}" cy="{yw}" r="6" fill="{MINUS}"/>')
        out.append(tex(X(-2), yi - 36, '얼음', 19, 'middle', EQUI) + tex(X(8), yw + 50, '물', 19, 'middle', MINUS))
    return ''.join(out)


def rock():
    out = ['<path d="M20 190 L40 80 Q60 40 110 46 L130 120 L150 44 Q210 36 240 70 L270 190 Z" fill="#8C8F94" stroke="#4A4D52" stroke-width="2.5" stroke-linejoin="round"/>',
           '<path d="M130 120 L118 50 L142 50 Z" fill="#EEF7FC" stroke="#7FB3D5" stroke-width="2"/>']
    out.append(f'<g data-anim="move" data-from="10,0" data-dur=".9" data-rep="alt" data-ease="io">{arw(146, 92, 186, 92, "ink", 3)}</g>')
    out.append(f'<g data-anim="move" data-from="-10,0" data-dur=".9" data-rep="alt" data-ease="io">{arw(114, 92, 74, 92, "ink", 3)}</g>')
    out.append(tex(130, 30, '틈 속 물이 얼면 부피 증가', 18, 'middle'))
    out.append(tex(146, 216, '얼었다 녹기를 되풀이 → 바위가 부서짐', 18, 'middle', MUTED))
    return ''.join(out)


def drops():
    out = ['<rect x="20" y="120" width="440" height="22" rx="3" fill="#E3EEFB" stroke="#9FC3DD" stroke-width="2"/>',
           '<path d="M60 120 Q66 106 120 104 Q174 106 180 120 Z" fill="#DDEEF8" stroke="#6E9CCB" stroke-width="2"/>',
           '<path d="M300 120 Q298 70 340 68 Q382 70 380 120 Z" fill="#DDEEF8" stroke="#6E9CCB" stroke-width="2"/>',
           tex(120, 172, 'A', 22, 'middle', extra=' data-weight="700"'), tex(340, 172, 'B', 22, 'middle', extra=' data-weight="700"'),
           tex(240, 160, '아크릴판', 18, 'middle', MUTED)]
    return ''.join(out)


def ice_benzene():
    s = float_sink()
    s = s.replace("'(나) 파라핀'", "").replace('(나) 파라핀', '(나) 벤젠')
    s = s.replace('data-mix="고체"', 'data-mix="고체 벤젠"').replace('data-mix="액체"', 'data-mix="액체 벤젠"')
    return s.replace('(가) 물과 얼음', '(가) 물과 얼음')

FIG['planet'] = planet()
FIG['breeze_d'] = breeze(True)
FIG['breeze_n'] = breeze(False)
FIG['volg'] = sch_graph('v')
FIG['densg'] = sch_graph('d')
FIG['volq'] = sch_graph('v', anim=False)
FIG['rock'] = rock()
FIG['lake3b'] = lake3(3).replace('clip-em21-203', 'clip-em21-203b')
FIG['drops'] = drops()
FIG['icebz'] = ice_benzene()

if __name__ == '__main__':
    tpl = open(TPL, encoding='utf-8').read()
    missing = set()

    def rep(m):
        k = m.group(1)
        if k not in FIG:
            missing.add(k)
            return m.group(0)
        return FIG[k]
    out = re.sub(r'\{\{(\w+)\}\}', rep, tpl)
    if missing:
        print('없는 그림:', missing)
    open(OUT, 'w', encoding='utf-8').write(out)
    print('ok', len(out), 'ice molecules', nip, nice)
