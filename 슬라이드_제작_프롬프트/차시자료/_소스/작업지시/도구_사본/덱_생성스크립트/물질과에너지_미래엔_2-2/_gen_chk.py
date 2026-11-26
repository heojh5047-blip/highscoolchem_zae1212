# 2-2 용액의 성질 — 그림 생성 → slides_tpl.html의 {{이름}}을 채워 slides.html로
import math, re, sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
from figs import f, atom, tex, arw, INK, MUTED, PLUS, MINUS, EQUI, FIELD, BF

FIG = {}
OUT = "/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/물질과에너지_미래엔_2-2/_chk.html"
TPL = os.path.join(os.path.dirname(__file__), 'slides_tpl.html')
SUG, SUGS = '#F2B544', '#B7791F'
GLASS, WATER, WTOP = '#7E8B98', '#DDEEF8', '#9FC3DD'


def g(inner, anim=''):
    return f'<g{(" " + anim) if anim else ""}>{inner}</g>'


def line(x1, y1, x2, y2, col=MUTED, w=2, dash=None, extra=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}"{da}{extra}/>'


def water(x, y, ang, rO=12, rH=8, L=15):
    """작은 물 분자(용매 배경 크기): ang = 두 H 이등분 방향"""
    out = []
    for s in (-1, 1):
        a = math.radians(ang + s * 52.25)
        out.append(atom(x + L * math.cos(a), y + L * math.sin(a), rH, 'H'))
    out.append(atom(x, y, rO, 'O'))
    return ''.join(out)


def sugar(x, y, r=13):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{SUG}" stroke="{SUGS}" stroke-width="2"/>'


def beaker(x, y, w, h, fill=WATER, level=0.7, sw=3, top=WTOP):
    ly = y + h * (1 - level)
    return (f'<rect x="{f(x+2)}" y="{f(ly)}" width="{f(w-4)}" height="{f(y+h-ly-2)}" fill="{fill}"/>'
            f'<line x1="{f(x+2)}" y1="{f(ly)}" x2="{f(x+w-2)}" y2="{f(ly)}" stroke="{top}" stroke-width="2"/>'
            f'<path d="M{f(x-6)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y+8)} V{f(y+h-8)} Q{f(x)} {f(y+h)} {f(x+8)} {f(y+h)} H{f(x+w-8)} Q{f(x+w)} {f(y+h)} {f(x+w)} {f(y+h-8)} V{f(y)}" fill="none" stroke="{GLASS}" stroke-width="{sw}" stroke-linejoin="round"/>')


# ───────── 입자 상자 (표지·S6) ─────────
def box(x0, top, w, liq, bot, sug, nvap, seed, gauge=True, vap_anim=True, cols=5, rows=4):
    """밀폐 용기: 왼쪽 x0, 뚜껑 top, 액면 liq, 바닥 bot. sug=설탕 자리 목록(격자 번호)"""
    rnd = random.Random(seed)
    out = [f'<rect x="{f(x0)}" y="{f(liq)}" width="{f(w)}" height="{f(bot-liq)}" fill="{WATER}"/>',
           line(x0, liq, x0 + w, liq, WTOP, 2),
           f'<rect x="{f(x0)}" y="{f(top)}" width="{f(w)}" height="{f(bot-top)}" fill="none" stroke="{GLASS}" stroke-width="3" rx="6"/>']
    sx, sy = (w - 52) / (cols - 0.5), (bot - liq - 46) / (rows - 1)
    k = 0
    for r in range(rows):
        for c in range(cols):
            x = x0 + 26 + c * sx + (sx / 2 if r % 2 else 0) + rnd.uniform(-2, 2)
            y = liq + 23 + r * sy + rnd.uniform(-2, 2)
            if k in sug:
                out.append(sugar(x, y))
            else:
                out.append(water(x, y, rnd.uniform(0, 360)))
            k += 1
    vp = []
    while len(vp) < nvap:
        x, y = x0 + 22 + rnd.random() * (w - 44), top + 26 + rnd.random() * (liq - top - 52)
        if all(math.hypot(x - p[0], y - p[1]) > 40 for p in vp):
            vp.append((x, y))
    for i, (x, y) in enumerate(vp):
        m = water(x, y, rnd.uniform(0, 360))
        if vap_anim:
            m = g(m, f'data-anim="move" data-from="0,{f(liq-y+10)}" data-dur="1.4" data-delay="{f(0.3+0.25*i)}" data-ease="out"')
        out.append(m)
    if gauge:
        cx, cy = x0 + w / 2, top - 26
        ang = -40 if nvap > 4 else -100
        a = math.radians(ang)
        out.append(line(cx, top - 4, cx, top, GLASS, 4))
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="22" fill="#fff" stroke="{INK}" stroke-width="2.5"/>')
        out.append(line(cx, cy, cx + 16 * math.cos(a), cy + 16 * math.sin(a), PLUS, 3, extra=' stroke-linecap="round"'))
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="3" fill="{INK}"/>')
    return ''.join(out)


def cover():
    out = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    out.append(box(50, 120, 205, 280, 430, [], 6, 11))
    out.append(box(285, 120, 205, 280, 430, [1, 6, 8, 13, 17], 3, 12))
    out.append(tex(152, 470, '물', 24, 'middle', extra=' data-weight="700"'))
    out.append(tex(388, 470, '설탕물', 24, 'middle', extra=' data-weight="700"'))
    return ''.join(out)


def evap():
    out = [box(30, 70, 250, 190, 350, [], 6, 21, cols=6), box(330, 70, 250, 190, 350, [2, 7, 9, 14, 19, 22], 3, 22, cols=6)]
    out.append(tex(155, 384, '물', 21, 'middle', extra=' data-weight="700"'))
    out.append(tex(455, 384, '설탕물', 21, 'middle', extra=' data-weight="700"'))
    # 범례
    out.append(water(40, 418, 270) + tex(60, 425, '물 분자', 19))
    out.append(sugar(170, 418) + tex(190, 425, '설탕 분자', 19))
    out.append(tex(330, 425, '증기압 계기', 19, fill=MUTED))
    return ''.join(out)


# ───────── S3 생각 열기: 냉동실 ─────────
def freezer():
    o = [f'<rect x="10" y="10" width="400" height="230" rx="14" fill="#E3EEFB" stroke="{MUTED}" stroke-width="3"/>',
         line(10, 200, 410, 200, MUTED, 3)]
    # 물 컵(얼음)
    o.append(f'<path d="M70 90 L82 196 H158 L170 90 Z" fill="#EEF7FC" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>')
    o.append(f'<path d="M76 112 L84 194 H156 L164 112 Z" fill="#F7FBFE" stroke="#7FB3D5" stroke-width="2"/>')
    o.append(''.join(line(92 + i * 18, 122, 100 + i * 18, 186, '#BFD9EC', 2) for i in range(4)))
    # 주스 컵(액체)
    o.append(f'<path d="M250 90 L262 196 H338 L350 90 Z" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>')
    o.append(g(f'<path d="M256 112 L264 194 H336 L344 112 Z" fill="#F6B04B" opacity=".85"/>', 'data-anim="move" data-from="0,6" data-dur="1.2" data-rep="alt" data-ease="sine"'))
    o.append(tex(120, 70, '물 → 얼음', 20, 'middle', extra=' data-weight="700"'))
    o.append(tex(300, 70, '주스 → 액체', 20, 'middle', extra=' data-weight="700"'))
    o.append(tex(210, 228, '냉동실 (같은 양, 같은 시간)', 18, 'middle', fill=MUTED))
    # 눈송이 표시
    o.append(tex(30, 40, '❄', 22, fill='#7FB3D5'))
    return ''.join(o)


# ───────── S4 다시 보기: 증기압 ─────────
def eq_box():
    rnd = random.Random(5)
    o = [f'<rect x="40" y="40" width="220" height="230" rx="8" fill="none" stroke="{GLASS}" stroke-width="3"/>',
         f'<rect x="41.5" y="180" width="217" height="88.5" fill="{WATER}"/>', line(42, 180, 258, 180, WTOP, 2)]
    for r in range(3):
        for c in range(8):
            o.append(water(58 + c * 26 + (13 if r % 2 else 0) * (c < 7), 198 + r * 26, rnd.uniform(0, 360)))
    for (x, y) in [(72, 66), (150, 62), (232, 72), (68, 148), (236, 150)]:
        o.append(water(x, y, rnd.uniform(0, 360)))
    o.append(g(arw(126, 172, 126, 96, 'field', 4) + tex(118, 132, '증발', 19, 'end', fill=FIELD, extra=' data-halo="1"'), 'data-anim="fade" data-dur=".8" data-delay=".3"'))
    o.append(g(arw(176, 96, 176, 172, 'bfield', 4) + tex(184, 132, '응축', 19, fill=BF, extra=' data-halo="1"'), 'data-anim="fade" data-dur=".8" data-delay=".9"'))
    o.append(tex(150, 300, '밀폐 용기 속 물', 19, 'middle', fill=MUTED))
    return ''.join(o)


def vp_curve():
    # 물의 증기압: 0–110 °C, 0–900 mmHg
    X = lambda t: 70 + t * 3.4
    Y = lambda p: 260 - p * 0.26
    data = [(0, 4.6), (10, 9.2), (20, 17.5), (30, 31.8), (40, 55.3), (50, 92.5), (60, 149.4), (70, 233.7), (80, 355.1), (90, 525.8), (100, 760), (105, 906)]
    o = [line(70, 260, 460, 260), line(70, 260, 70, 22)]
    for t in (0, 20, 40, 60, 80, 100):
        o.append(line(X(t), 260, X(t), 266) + tex(X(t), 286, str(t), 18, 'middle', fill=MUTED))
    for p in (0, 380, 760):
        o.append(line(64, Y(p), 70, Y(p)) + tex(60, Y(p) + 6, str(p), 18, 'end', fill=MUTED))
    o.append(line(70, Y(760), 440, Y(760), MUTED, 2, '6 5'))
    o.append(tex(80, Y(760) - 10, '1 기압(760 mmHg)', 18, fill=MUTED))
    pts = ' '.join(f'{f(X(t))},{f(Y(p))}' for t, p in data)
    o.append(f'<polyline points="{pts}" fill="none" stroke="{MINUS}" stroke-width="3.5" data-anim="draw" data-dur="1.6"/>')
    o.append(f'<g class="step" data-g="bp">{line(X(100), Y(760), X(100), 260, MUTED, 2, "4 4")}<circle cx="{f(X(100))}" cy="{f(Y(760))}" r="6" fill="{PLUS}"/>{tex(X(100) - 8, 240, "100 °C에서 끓음", 18, "end", fill=PLUS, extra=" data-halo=\"1\"")}</g>')
    o.append(tex(330, 312, '온도 [°C]', 19, 'middle'))
    o.append(tex(20, 22, '증기압 [mmHg]', 19))
    o.append(tex(X(60) + 8, Y(149) - 30, '물', 20, fill=MINUS, extra=' data-weight="700"'))
    return ''.join(o)


# ───────── S5 수은 U자관 장치 ─────────
def manometer():
    o = []
    def flask(cx, fill, dots):
        s = f'<path d="M{cx-14} 60 V150 A72 72 0 1 0 {cx+14} 150 V60" fill="#fff" stroke="{GLASS}" stroke-width="3"/>'
        s += f'<path d="M{cx-62} 230 Q{cx} 236 {cx+62} 230 A70 70 0 0 1 {cx-62} 230 Z" fill="{fill}"/>'
        s += line(cx - 62, 230, cx + 62, 230, WTOP, 2)
        for i, (dx, dy) in enumerate(dots):
            s += f'<circle cx="{cx+dx}" cy="{230+dy}" r="6" fill="{SUG}" stroke="{SUGS}" stroke-width="1.5"/>'
        return s
    o.append(flask(100, WATER, []))
    o.append(flask(500, WATER, [(-30, 20), (0, 34), (28, 16), (-8, 54), (34, 44)]))
    # 유리관
    tube = 'M100 60 V30 H250 V250 Q250 270 270 270 H330 Q350 270 350 250 V30 H500 V60'
    o.append(f'<path d="{tube}" fill="none" stroke="{GLASS}" stroke-width="14" stroke-linejoin="round"/>')
    o.append(f'<path d="{tube}" fill="none" stroke="#fff" stroke-width="8" stroke-linejoin="round"/>')
    # 수은: 바닥 U + 두 기둥 (그린 모습 = 충분한 시간 뒤: 물 쪽 190, 설탕물 쪽 150)
    o.append(f'<path d="M250 230 V250 Q250 270 270 270 H330 Q350 270 350 250 V230" fill="none" stroke="#9AA5B1" stroke-width="8"/>')
    o.append(f'<g data-anim="scale" data-from="1,1.6667" data-o="250,230" data-dur="1.6" data-delay=".6" data-ease="soft"><rect x="246" y="200" width="8" height="30" fill="#9AA5B1"/></g>')
    o.append(f'<g data-anim="scale" data-from="1,0.7143" data-o="350,230" data-dur="1.6" data-delay=".6" data-ease="soft"><rect x="346" y="160" width="8" height="70" fill="#9AA5B1"/></g>')
    o.append(line(226, 200, 246, 200, INK, 2) + line(354, 160, 374, 160, INK, 2))
    o.append(f'<g class="step" data-g="h">{line(370, 160, 370, 200, MUTED, 2)}{line(362, 160, 378, 160, MUTED, 2)}{line(362, 200, 378, 200, MUTED, 2)}{line(354, 200, 378, 200, MUTED, 2, "4 4")}{tex(384, 188, "높이 차", 18, fill=MUTED)}</g>')
    o.append(tex(100, 330, '물', 21, 'middle', extra=' data-weight="700"'))
    o.append(tex(500, 330, '설탕물', 21, 'middle', extra=' data-weight="700"'))
    o.append(tex(300, 300, '수은', 19, 'middle', fill=MUTED))
    o.append(tex(175, 22, '유리관', 18, 'middle', fill=MUTED))
    o.append(g(arw(232, 60, 232, 140, 'minus', 3) + tex(222, 112, '증기압', 18, 'end', fill=MINUS) + tex(222, 134, '큼', 18, 'end', fill=MINUS), 'class="step" data-g="p"'))
    o.append(g(arw(368, 60, 368, 120, 'equi', 3) + tex(380, 92, '증기압', 18, fill=EQUI) + tex(380, 114, '작음', 18, fill=EQUI), 'class="step" data-g="p"'))
    return ''.join(o)


# ───────── 그래프 도우미 ─────────
def axes(x0, y0, x1, y1, xl, yl, xs=19, extra=''):
    return (line(x0, y0, x1, y0) + line(x0, y0, x0, y1) + tex(x1, y0 + 40, xl, xs, 'end') + tex(x0 - 50, y1 - 10, yl, xs))


# ───────── S7 해 보기 그래프 ─────────
def hb_graph():
    X = lambda c: 90 + c * 5.4
    Y = lambda p: 270 - (p - 10) * 15
    o = [line(90, 270, 540, 270), line(90, 270, 90, 30)]
    for c in range(0, 81, 10):
        o.append(line(X(c), 270, X(c), 276) + tex(X(c), 296, str(c), 18, 'middle', fill=MUTED))
    for p in (10, 15, 20, 25):
        o.append(line(84, Y(p), 90, Y(p)) + tex(80, Y(p) + 6, str(p), 18, 'end', fill=MUTED))
        if p > 10:
            o.append(line(90, Y(p), 530, Y(p), '#E2E7EC', 1.5))
    data = [(0, 23.8), (10, 23.6), (20, 23.3), (30, 22.9), (40, 22.3), (50, 21.6), (60, 20.7), (70, 19.6)]
    pts = ' '.join(f'{f(X(c))},{f(Y(p))}' for c, p in data)
    o.append(f'<polyline points="{pts}" fill="none" stroke="{MINUS}" stroke-width="3" data-anim="draw" data-dur="1.6"/>')
    o.append(''.join(f'<circle cx="{f(X(c))}" cy="{f(Y(p))}" r="5" fill="{MINUS}"/>' for c, p in data))
    o.append(f'<g class="step" data-g="p80">{line(X(70), Y(19.6), X(80), Y(18.2), PLUS, 3, "6 5")}<circle cx="{f(X(80))}" cy="{f(Y(18.2))}" r="7" fill="#fff" stroke="{PLUS}" stroke-width="3"/>{tex(X(80) - 12, Y(18.2) + 34, "예상 약 18", 18, "end", fill=PLUS)}</g>')
    o.append(tex(540, 334, '설탕물의 농도 [%]', 19, 'end'))
    o.append(tex(30, 20, '증기압 [mmHg]', 19))
    o.append(tex(530, 56, '25 °C', 19, 'end', fill=MUTED))
    return ''.join(o)


# ───────── 증기 압력 곡선(모식) ─────────
U = lambda u: 80 + 360 * u
def Hs(u): return 30 * math.exp(2.1 * u)
def curve(k, umax, y0=300, top=40):
    pts = []
    u = 0
    while u <= umax + 1e-9:
        h = k * Hs(u)
        if y0 - h < top:
            break
        pts.append(f'{f(U(u))},{f(y0-h)}')
        u += 0.02
    return ' '.join(pts)


def vp_two(mode):
    """mode 'dp' 그림 II-13 꼴 / 'bp' 그림 II-14 꼴"""
    y0 = 300
    o = [line(80, y0, 500, y0), line(80, y0, 80, 30)]
    o.append(f'<polyline points="{curve(1, 1.2)}" fill="none" stroke="{MINUS}" stroke-width="3.5" data-anim="draw" data-dur="1.4"/>')
    o.append(f'<polyline points="{curve(0.72, 1.2)}" fill="none" stroke="{EQUI}" stroke-width="3.5" data-anim="draw" data-dur="1.4" data-delay=".5"/>')
    o.append(tex(500, y0 - 10, '온도', 19, 'end'))
    o.append(tex(30, 22, '증기압 [mmHg]', 19))
    if mode == 'dp':
        u = 0.62
        hs, hl = Hs(u), 0.72 * Hs(u)
        o.append(line(80, y0 - hs, U(u), y0 - hs, MUTED, 2, '4 4') + line(80, y0 - hl, U(u), y0 - hl, MUTED, 2, '4 4') + line(U(u), y0, U(u), y0 - hs, MUTED, 2, '4 4'))
        o.append(tex(72, y0 - hs + 7, '$P_\\text{용매}$', 19, 'end') + tex(72, y0 - hl + 7, '$P_\\text{용액}$', 19, 'end'))
        o.append(g(arw(U(u) + 16, y0 - hs, U(u) + 16, y0 - hl, 'ink', 3) + tex(U(u) + 26, y0 - (hs + hl) / 2 + 7, '$\\Delta P$', 21), 'class="step" data-g="dp"'))
        o.append(tex(U(1.0) - 20, y0 - Hs(1.0) + 10, '용매', 20, 'end', fill=MINUS, extra=' data-weight="700"'))
        o.append(tex(U(1.15), y0 - 0.72 * Hs(1.15) + 34, '용액', 20, 'middle', fill=EQUI, extra=' data-weight="700"'))
    else:
        h760 = 200
        ub = math.log(h760 / 30) / 2.1
        ub2 = math.log(h760 / 30 / 0.72) / 2.1
        o.append(line(80, y0 - h760, 500, y0 - h760, MUTED, 2, '6 5') + tex(72, y0 - h760 + 7, '760', 18, 'end', fill=MUTED))
        o.append(line(U(ub), y0, U(ub), y0 - h760, MUTED, 2, '4 4') + line(U(ub2), y0, U(ub2), y0 - h760, MUTED, 2, '4 4'))
        o.append(tex(U(ub), y0 + 28, '$T_\\mathrm{b}$', 20, 'middle') + tex(U(ub2) + 6, y0 + 28, "$T_\\mathrm{b}'$", 20, 'middle'))
        o.append(f'<circle cx="{f(U(ub))}" cy="{f(y0-h760)}" r="6" fill="{MINUS}"/><circle cx="{f(U(ub2))}" cy="{f(y0-h760)}" r="6" fill="{EQUI}"/>')
        hl = 0.72 * h760
        o.append(g(arw(U(ub) - 14, y0 - h760, U(ub) - 14, y0 - hl, 'ink', 3) + tex(U(ub) - 22, y0 - (h760 + hl) / 2 + 7, '$\\Delta P$', 20, 'end'), 'class="step" data-g="b1"'))
        yb = y0 - 30
        o.append(g(line(U(ub), yb, U(ub2), yb, INK, 2) + line(U(ub), yb - 7, U(ub), yb + 7, INK, 2) + line(U(ub2), yb - 7, U(ub2), yb + 7, INK, 2) + tex((U(ub) + U(ub2)) / 2, yb - 12, '$\\Delta T_\\mathrm{b}$', 20, 'middle', extra=' data-halo="1"'), 'class="step" data-g="b2"'))
        o.append(tex(U(ub) - 24, 40, '용매', 20, 'end', fill=MINUS, extra=' data-weight="700"'))
        o.append(tex(427, 178, '용액', 20, fill=EQUI, extra=' data-weight="700"'))
        o.append(tex(90, y0 - h760 - 10, '1 기압', 18, fill=MUTED))
    return ''.join(o)


# ───────── S11 몰농도와 몰랄 농도 ─────────
def vflask():
    o = [f'<path d="M86 20 V80 Q30 100 30 150 Q30 200 100 200 Q170 200 170 150 Q170 100 114 80 V20" fill="none" stroke="{GLASS}" stroke-width="3"/>',
         f'<path d="M33 140 Q40 196 100 197 Q160 196 167 140 Q140 100 114 92 V52 H86 V92 Q60 100 33 140 Z" fill="#E7F0D9"/>',
         line(80, 52, 120, 52, INK, 2.5), tex(128, 58, '표선', 18),
         tex(100, 236, '용액의 부피 기준', 18, 'middle', fill=MUTED)]
    o.append(g(tex(186, 120, '온도↑', 19, fill=PLUS) + tex(186, 146, '부피 변함', 19, fill=PLUS), 'class="step" data-g="mv"'))
    return ''.join(o)


def balance():
    o = [beaker(50, 50, 120, 110, level=0.6),
         f'<rect x="30" y="170" width="160" height="40" rx="6" fill="#E9EDF1" stroke="{INK}" stroke-width="2.5"/>',
         f'<rect x="70" y="180" width="80" height="22" rx="3" fill="#0E2A3A"/>', tex(110, 198, '1.000 kg', 18, 'middle', fill='#9BE7A0'),
         tex(110, 236, '용매의 질량 기준', 18, 'middle', fill=MUTED)]
    o.append(g(tex(180, 100, '온도↑', 19, fill=FIELD) + tex(180, 126, '질량', 19, fill=FIELD) + tex(180, 150, '그대로', 19, fill=FIELD), 'class="step" data-g="mm"'))
    return ''.join(o)


# ───────── S12 설탕물 만들기 ─────────
def make_sol(nsug, grams, lab):
    o = [beaker(40, 40, 150, 140, level=0.62)]
    rnd = random.Random(nsug)
    for i in range(nsug):
        o.append(f'<circle cx="{f(60+rnd.random()*110)}" cy="{f(110+rnd.random()*60)}" r="6" fill="{SUG}" stroke="{SUGS}" stroke-width="1.5"/>')
    o.append(g(f'<path d="M208 34 L250 34 L262 64 H196 Z" fill="#fff" stroke="{INK}" stroke-width="2"/>' + ''.join(f'<circle cx="{f(214+i*9)}" cy="{f(54-(i%2)*6)}" r="5" fill="{SUG}" stroke="{SUGS}" stroke-width="1.2"/>' for i in range(5)), 'data-anim="move" data-from="0,-20" data-dur="1" data-ease="out"'))
    o.append(tex(229, 92, grams, 19, 'middle'))
    o.append(tex(115, 214, '물 100 g', 19, 'middle'))
    o.append(tex(115, 240, lab, 19, 'middle', fill=MUTED))
    return ''.join(o)


# ───────── S14·S15 장치 ─────────
def tablet(x, y, kind):
    o = [f'<rect x="{x}" y="{y}" width="150" height="104" rx="10" fill="#1E2B3C"/>', f'<rect x="{x+8}" y="{y+8}" width="134" height="88" rx="4" fill="#fff"/>',
         line(x + 18, y + 84, x + 134, y + 84, MUTED, 1.5), line(x + 18, y + 84, x + 18, y + 16, MUTED, 1.5)]
    if kind == 'b':
        d = f'M{x+18} {y+78} Q{x+60} {y+40} {x+82} {y+28} H{x+134}'
        col = PLUS
    else:
        d = f'M{x+18} {y+22} Q{x+40} {y+66} {x+62} {y+72} L{x+68} {y+60} H{x+134}'
        col = MINUS
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3" data-anim="draw" data-dur="2" data-delay=".4"/>')
    return ''.join(o)


def app_boil():
    o = [f'<rect x="20" y="300" width="300" height="16" rx="3" fill="#5B6B7F"/>',  # 받침
         f'<rect x="44" y="40" width="10" height="262" fill="#9AA5B1"/>',  # 스탠드
         f'<rect x="80" y="236" width="200" height="64" rx="8" fill="#E9EDF1" stroke="{INK}" stroke-width="2.5"/>',
         f'<circle cx="112" cy="268" r="10" fill="#fff" stroke="{INK}" stroke-width="2"/>', f'<rect x="200" y="258" width="58" height="20" rx="3" fill="#D7263D" opacity=".75"/>',
         beaker(120, 130, 120, 104, level=0.62),
         line(54, 76, 180, 76, INK, 4),  # 집게 팔
         f'<rect x="174" y="62" width="14" height="22" rx="3" fill="{INK}"/>',
         f'<rect x="177" y="84" width="8" height="128" rx="4" fill="#C9D3DD" stroke="{INK}" stroke-width="2"/>',
         f'<path d="M181 62 C181 20 300 20 330 70" fill="none" stroke="{INK}" stroke-width="2.5"/>',
         tablet(320, 70, 'b')]
    for i in range(5):
        o.append(g(f'<circle cx="{140+i*18}" cy="{220-(i%2)*12}" r="3.5" fill="#fff" stroke="{WTOP}" stroke-width="1.5"/>', f'data-anim="move" data-from="0,22" data-dur="1.2" data-delay="{f(i*0.2)}" data-rep="loop" data-ease="lin"'))
    o.append(tex(180, 330, '가열 장치', 18, 'middle', fill=MUTED) + tex(96, 64, '온도 센서', 18, 'middle', fill=MUTED) + tex(395, 202, '스마트 기기', 18, 'middle', fill=MUTED))
    o.append(tex(246, 228, '증류수 50 mL', 18))
    return ''.join(o)


def app_freeze():
    rnd = random.Random(4)
    o = [f'<rect x="20" y="300" width="300" height="16" rx="3" fill="#5B6B7F"/>', f'<rect x="44" y="40" width="10" height="262" fill="#9AA5B1"/>',
         f'<rect x="102" y="144" width="156" height="152" fill="#F3F7FB"/>']
    for i in range(16):
        x, y = 112 + rnd.random() * 130, 156 + rnd.random() * 128
        o.append(f'<rect x="{f(x)}" y="{f(y)}" width="16" height="13" rx="3" fill="#fff" stroke="#9FC3DD" stroke-width="1.5" transform="rotate({rnd.randint(-30,30)} {f(x+8)} {f(y+6)})"/>')
    o.append(f'<path d="M94 120 Q100 120 100 126 V290 Q100 298 108 298 H252 Q260 298 260 290 V120" fill="none" stroke="{GLASS}" stroke-width="3"/>')
    o.append(f'<path d="M168 66 V256 A12 12 0 0 0 192 256 V66" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>')
    o.append(g(f'<rect x="170" y="214" width="20" height="46" fill="{WATER}"/>', 'data-anim="fade" data-dur="1"'))
    o.append(line(54, 76, 180, 76, INK, 4) + f'<rect x="174" y="62" width="12" height="22" rx="3" fill="{INK}"/><rect x="176" y="84" width="8" height="166" rx="4" fill="#C9D3DD" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<path d="M180 62 C180 20 300 20 330 70" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    o.append(tablet(320, 70, 'f'))
    o.append(tex(180, 330, '한제(얼음 + 소금)', 18, 'middle', fill=MUTED) + tex(96, 64, '온도 센서', 18, 'middle', fill=MUTED) + tex(395, 202, '스마트 기기', 18, 'middle', fill=MUTED))
    o.append(tex(270, 250, '증류수 5 mL를', 18, extra=' data-halo="1"') + tex(270, 274, '넣은 시험관', 18, extra=' data-halo="1"'))
    return ''.join(o)


# ───────── S21 어는점 내림: −1 °C의 물과 설탕물 ─────────
def freeze_cmp():
    o = []
    for i, (lab, frozen) in enumerate([('물', True), ('1 m 설탕물', False)]):
        x = 30 + i * 230
        o.append(f'<path d="M{x+40} 50 V200 A30 30 0 0 0 {x+100} 200 V50" fill="#fff" stroke="{GLASS}" stroke-width="3"/>')
        if frozen:
            o.append(g(f'<path d="M{x+43} 110 V200 A27 27 0 0 0 {x+97} 200 V110 Z" fill="#EEF7FC" stroke="#7FB3D5" stroke-width="2"/>' + ''.join(line(x + 52 + k * 12, 120, x + 58 + k * 12, 210, '#BFD9EC', 2) for k in range(4)), 'data-anim="fade" data-dur="1.4" data-delay=".4"'))
        else:
            o.append(f'<path d="M{x+43} 110 V200 A27 27 0 0 0 {x+97} 200 V110 Z" fill="{WATER}"/>' + line(x + 43, 110, x + 97, 110, WTOP, 2))
            o.append(''.join(f'<circle cx="{x+55+k*10}" cy="{150+(k%3)*18}" r="4.5" fill="{SUG}" stroke="{SUGS}" stroke-width="1.2"/>' for k in range(4)))
        o.append(tex(x + 70, 262, lab, 20, 'middle', extra=' data-weight="700"'))
        o.append(tex(x + 70, 290, '얼었다' if frozen else '얼지 않았다', 19, 'middle', fill=MINUS if frozen else EQUI))
    # 온도계
    o.append(f'<rect x="200" y="40" width="16" height="190" rx="8" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="208" cy="236" r="13" fill="{MINUS}" stroke="{INK}" stroke-width="2"/>')
    o.append(g(f'<rect x="204" y="150" width="8" height="80" fill="{MINUS}"/>', 'data-anim="scale" data-from="1,1.8" data-o="208,230" data-dur="1.4" data-ease="soft"'))
    o.append(tex(208, 28, '−1 °C', 20, 'middle', fill=MINUS, extra=' data-weight="700"'))
    return ''.join(o)


# ───────── S22 그림 II-15 꼴 ─────────
def bpfp():
    xs = [120, 300, 480]
    yb = lambda k: 90 - 22 * k
    yf = lambda k: 170 + 40 * k
    o = [line(60, 40, 60, 300, MUTED, 2)]
    o.append(f'<path d="M50 136 l20 -6 M50 144 l20 -6" stroke="{MUTED}" stroke-width="2"/>')  # 축 생략 표시
    o.append(tex(52, yb(0) + 6, '끓는점 100 °C', 18, 'end', fill=PLUS) if False else '')
    o.append(line(60, yb(0), 540, yb(0) - 0.0, PLUS, 1.5, '4 4') + line(60, yf(0), 540, yf(0), MINUS, 1.5, '4 4'))
    o.append(f'<polyline points="{xs[0]},{yb(0)} {xs[2]},{yb(2)}" fill="none" stroke="{PLUS}" stroke-width="4" data-anim="draw" data-dur="1.4"/>')
    o.append(f'<polyline points="{xs[0]},{yf(0)} {xs[2]},{yf(2)}" fill="none" stroke="{MINUS}" stroke-width="4" data-anim="draw" data-dur="1.4" data-delay=".4"/>')
    o.append(tex(52, yb(0) - 6, '끓는점||100 °C', 18, 'end', fill=PLUS) + tex(52, yf(0) - 6, '어는점||0 °C', 18, 'end', fill=MINUS))
    for k in (1, 2):
        x = xs[k]
        o.append(line(x, 30, x, 300, MUTED, 1.5, '4 4'))
        o.append(g(line(x + 10, yb(0), x + 10, yb(k), INK, 2.5) + tex(x + 18, (yb(0) + yb(k)) / 2 + 7, ('' if k == 1 else '2') + '$\\Delta T_\\mathrm{b}$', 19), f'class="step" data-g="k{k}"'))
        o.append(g(line(x + 10, yf(0), x + 10, yf(k), INK, 2.5) + tex(x + 18, (yf(0) + yf(k)) / 2 + 7, ('' if k == 1 else '2') + '$\\Delta T_\\mathrm{f}$', 19), f'class="step" data-g="k{k}"'))
    for k, lab in enumerate(['물', '1 m 수용액', '2 m 수용액']):
        x = xs[k]
        o.append(beaker(x - 26, 260, 52, 48, level=0.6))
        o.append(''.join(f'<circle cx="{f(x-15+j*30/max(1,k*3-1))}" cy="{294-(j%2)*8}" r="3.5" fill="{SUG}" stroke="{SUGS}" stroke-width="1"/>' for j in range(k * 3)))
        o.append(tex(x, 334, lab, 19, 'middle'))
    return '<g transform="translate(18,0)">' + ''.join(o) + '</g>'


# ───────── S24 자료 읽기 아이콘 ─────────
def ic_car():
    return (f'<path d="M20 90 L40 60 H120 L145 90 H170 V112 H20 Z" fill="#9FB7CF" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="55" cy="114" r="14" fill="{INK}"/><circle cx="140" cy="114" r="14" fill="{INK}"/>'
            f'<rect x="180" y="40" width="44" height="70" rx="6" fill="#B9E3A2" stroke="{INK}" stroke-width="2.5"/><rect x="194" y="28" width="16" height="12" fill="{INK}"/>')


def ic_frog():
    return (f'<ellipse cx="120" cy="96" rx="64" ry="34" fill="#7DAE5A" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="92" cy="62" r="13" fill="#7DAE5A" stroke="{INK}" stroke-width="2.5"/><circle cx="148" cy="62" r="13" fill="#7DAE5A" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="92" cy="62" r="5" fill="{INK}"/><circle cx="148" cy="62" r="5" fill="{INK}"/>'
            + f'<path d="M50 128 Q120 112 190 128" fill="none" stroke="#8A6A3A" stroke-width="4"/>')


def ic_ice():
    return (f'<path d="M90 70 L120 130 L150 70 Z" fill="#E8C38A" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="104" cy="58" r="20" fill="#F7C6D4" stroke="{INK}" stroke-width="2"/><circle cx="136" cy="58" r="20" fill="#FFF3C4" stroke="{INK}" stroke-width="2"/>'
            + tex(196, 82, '−18 °C', 26, 'middle', fill=MINUS, extra=' data-weight="700"'))


def ic_road():
    return (f'<rect x="10" y="100" width="230" height="26" fill="#9AA5B1"/>' + line(20, 113, 230, 113, '#fff', 3, '14 10')
            + f'<rect x="40" y="46" width="90" height="46" rx="6" fill="#E08A2C" stroke="{INK}" stroke-width="2.5"/><circle cx="62" cy="96" r="9" fill="{INK}"/><circle cx="112" cy="96" r="9" fill="{INK}"/>'
            + ''.join(g(f'<circle cx="{150+k*16}" cy="{70+(k%2)*14}" r="4" fill="#fff" stroke="{MUTED}" stroke-width="1.5"/>', f'data-anim="move" data-from="-20,-10" data-dur="1" data-delay="{f(k*.15)}" data-rep="loop" data-ease="lin"') for k in range(4)))


# ───────── 대단원 마무리 05 ─────────
def q05():
    y0 = 300
    o = [line(80, y0, 480, y0), line(80, y0, 80, 30)]
    o.append(f'<polyline points="{curve(1, 1.0)}" fill="none" stroke="{MINUS}" stroke-width="3.5"/>')
    o.append(f'<polyline points="{curve(0.8, 1.05)}" fill="none" stroke="{EQUI}" stroke-width="3.5"/>')
    u = 0.85
    hs, hl = Hs(u), 0.8 * Hs(u)
    o.append(line(80, y0 - hs, U(u), y0 - hs, MUTED, 2, '4 4') + line(80, y0 - hl, U(u), y0 - hl, MUTED, 2, '4 4') + line(U(u), y0, U(u), y0 - hs, MUTED, 2, '4 4'))
    o.append(tex(72, y0 - hs + 7, '$P$', 20, 'end') + tex(72, y0 - hl + 10, '$0.8P$', 20, 'end') + tex(U(u), y0 + 28, '$t$', 20, 'middle') + tex(72, y0 + 26, '0', 18, 'end'))
    o.append(tex(480, y0 + 40, '온도 [°C]', 19, 'end') + tex(30, 22, '증기압 [mmHg]', 19))
    o.append(tex(U(0.68), 48, '증류수', 19, 'end', fill=MINUS, extra=' data-weight="700"') + tex(250, 264, '수용액 (가)', 19, fill=EQUI, extra=' data-weight="700"'))
    return ''.join(o)


def q07():
    o = [line(80, 280, 470, 280), line(80, 280, 80, 30)]
    o.append(f'<path d="M80 168 q10 -6 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t10 0" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
    o.append(f'<path d="M80 174 q10 -6 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t10 0" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
    o.append(f'<polyline points="80,236 180,104 440,56" fill="none" stroke="{EQUI}" stroke-width="3.5" data-anim="draw" data-dur="1.6"/>')
    o.append(f'<circle cx="180" cy="104" r="5" fill="{INK}"/>' + line(80, 104, 180, 104, MUTED, 1.5, '4 4') + line(180, 104, 180, 280, MUTED, 1.5, '4 4'))
    o.append(tex(72, 110, '100.05', 18, 'end') + tex(180, 306, '$t$', 20, 'middle') + tex(72, 300, '0', 18, 'end'))
    o.append(tex(470, 320, '시간', 19, 'end') + tex(30, 22, '온도 [°C]', 19) + tex(420, 100, '수용액 (가)', 19, 'middle', fill=EQUI, extra=' data-weight="700"'))
    return ''.join(o)


def q08():
    X = lambda x: 90 + x * 380
    Y = lambda p: 270 - p * 44
    o = [line(90, 270, 490, 270), line(90, 270, 90, 30)]
    o.append(f'<polyline points="{f(X(0))},{f(Y(5))} {f(X(0.8))},{f(Y(1))}" fill="none" stroke="{MINUS}" stroke-width="3.5" data-anim="draw" data-dur="1.2"/>' + line(X(0.8), Y(1), X(1), Y(0), MINUS, 3.5, '5 5'))
    o.append(f'<polyline points="{f(X(0))},{f(Y(3))} {f(X(0.8))},{f(Y(0.6))}" fill="none" stroke="{EQUI}" stroke-width="3.5" data-anim="draw" data-dur="1.2" data-delay=".4"/>' + line(X(0.8), Y(0.6), X(1), Y(0), EQUI, 3.5, '5 5'))
    x = 1 / 3
    o.append(f'<circle cx="{f(X(x))}" cy="{f(Y(2))}" r="6" fill="{INK}"/>' + line(90, Y(2), X(x), Y(2), MUTED, 1.5, '4 4') + line(X(x), Y(2), X(x), 270, MUTED, 1.5, '4 4'))
    for v, lab in ((5, '5a'), (3, '3a'), (2, '2a')):
        o.append(tex(82, Y(v) + 7, f'${lab[0]}a$', 19, 'end'))
    o.append(tex(82, 294, '0', 18, 'end') + tex(X(x), 298, '$x$', 20, 'middle') + tex(X(0.5), 298, '0.5', 18, 'middle') + line(X(0.5), 270, X(0.5), 276) + tex(X(1), 298, '1', 18, 'middle'))
    o.append(tex(490, 330, '용질의 몰분율', 19, 'end') + tex(30, 22, '증기압(상댓값)', 19))
    o.append(tex(X(0.45), Y(3.1) - 10, '용액 (가)', 19, fill=MINUS, extra=' data-weight="700"') + tex(260, 254, '용액 (나)', 19, fill=EQUI, extra=' data-weight="700"'))
    return ''.join(o)


FIG.update(cover=cover(), evap=evap(), freezer=freezer(), eqbox=eq_box(), vpcurve=vp_curve(), mano=manometer(), hbg=hb_graph(),
           vpdp=vp_two('dp'), vpbp=vp_two('bp'), vflask=vflask(), balance=balance(), mk05=make_sol(6, '설탕 17.1 g', '0.5 m'),
           mk10=make_sol(12, '설탕 34.2 g', '1 m'), appb=app_boil(), appf=app_freeze(), frz=freeze_cmp(), bpfp=bpfp(),
           icar=ic_car(), ifrog=ic_frog(), iice=ic_ice(), iroad=ic_road(), q05=q05(), q07=q07(), q08=q08())

if __name__ == '__main__':
    tpl = open(TPL, encoding='utf-8').read()
    miss = set()
    def rep(m):
        k = m.group(1)
        if k not in FIG:
            miss.add(k); return m.group(0)
        return FIG[k]
    out = re.sub(r'\{\{(\w+)\}\}', rep, tpl)
    if miss:
        print('없는 그림:', miss)
    open(OUT, 'w', encoding='utf-8').write(out)
    print('ok', len(out))
