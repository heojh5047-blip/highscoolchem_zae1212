# 2-3 삼투 현상 — 그림 생성 → slides_tpl.html의 {{이름}}을 채워 slides.html로
import math, re, sys, os, random
sys.path.insert(0, os.path.dirname(__file__))
from figs import f, atom, tex, arw, INK, MUTED, PLUS, MINUS, EQUI, FIELD, BF

FIG = {}
OUT = '/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/물질과에너지_미래엔_2-3/test_out.html'
TPL = os.path.join(os.path.dirname(__file__), 'slides_tpl.html')
SUG, SUGS = '#F2B544', '#B7791F'
GLASS, WATER, WTOP = '#7E8B98', '#DDEEF8', '#9FC3DD'
SOL, SOLS = '#8FB8DE', '#5B8DB8'      # 튜브 속 설탕물(색소)
WDOT = '#5DA9E9'                      # 단순 입자: 물 분자
RUB = '#8C6D46'


def fig(name):
    def deco(fn):
        FIG[name] = fn
        return fn
    return deco


def line(x1, y1, x2, y2, col=MUTED, w=2, dash=None, extra=''):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" stroke-width="{w}"{da}{extra}/>'


def water(x, y, ang, rO=12, rH=8, L=15):
    out = []
    for s in (-1, 1):
        a = math.radians(ang + s * 52.25)
        out.append(atom(x + L * math.cos(a), y + L * math.sin(a), rH, 'H'))
    out.append(atom(x, y, rO, 'O'))
    return ''.join(out)


def sugar(x, y, r=13):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{SUG}" stroke="{SUGS}" stroke-width="2"/>'


def wdot(x, y, r=7):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{WDOT}" stroke="#2F7FC1" stroke-width="1.2"/>'


def beaker(x, y, w, h, level, fill=WATER):
    """x,y = 왼쪽 위, level = 액면 y"""
    return (f'<rect x="{f(x+2)}" y="{f(level)}" width="{f(w-4)}" height="{f(y+h-level-2)}" fill="{fill}"/>'
            + line(x + 2, level, x + w - 2, level, WTOP, 2)
            + f'<path d="M{f(x-6)} {f(y)} Q{f(x)} {f(y)} {f(x)} {f(y+8)} V{f(y+h-8)} Q{f(x)} {f(y+h)} {f(x+8)} {f(y+h)} H{f(x+w-8)} Q{f(x+w)} {f(y+h)} {f(x+w)} {f(y+h-8)} V{f(y)}" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>')


def device(cx, by, lev, swell=1.0, anim=True, delay=0.3, bw=150, bh=150, ttop=None, straw_top=None, wfill=WATER, tfill=SOL, tstroke=SOLS):
    """삼투 현상 실험 장치: 비커(바닥 by) + 반투막 튜브 + 빨대. lev = 빨대 속 액면 y"""
    tt = ttop if ttop is not None else by - 118   # 튜브 위 끝
    tb = by - 22                                  # 튜브 아래 끝
    st = straw_top if straw_top is not None else by - 320
    tw = 40 * swell
    out = [beaker(cx - bw / 2, by - bh, bw, bh, by - bh + 34, wfill)]
    tube = (f'<path d="M{f(cx-7)} {f(tt)} C{f(cx-tw/2-4)} {f(tt+14)} {f(cx-tw/2)} {f(tt+30)} {f(cx-tw/2)} {f((tt+tb)/2)} '
            f'C{f(cx-tw/2)} {f(tb-16)} {f(cx-tw/2+6)} {f(tb-4)} {f(cx-4)} {f(tb)} L{f(cx+4)} {f(tb)} '
            f'C{f(cx+tw/2-6)} {f(tb-4)} {f(cx+tw/2)} {f(tb-16)} {f(cx+tw/2)} {f((tt+tb)/2)} '
            f'C{f(cx+tw/2)} {f(tt+30)} {f(cx+tw/2+4)} {f(tt+14)} {f(cx+7)} {f(tt)} Z" fill="{tfill}" stroke="{tstroke}" stroke-width="2.5"/>')
    if anim and swell > 1:
        tube = f'<g data-anim="scale" data-from="{f(1/swell)},1" data-o="{f(cx)},{f(tt)}" data-dur="2" data-delay="{delay}" data-ease="soft">{tube}</g>'
    out.append(tube)
    out.append(line(cx - 6, tb + 3, cx + 6, tb + 3, RUB, 4))        # 아래 묶은 곳
    col = f'<rect x="{f(cx-5)}" y="{f(lev)}" width="10" height="{f(tt+4-lev)}" fill="{tfill}"/>'
    if anim:
        fr = max(0.15, min(0.9, 28 / max(1, tt + 4 - lev)))
        col = f'<g data-anim="scale" data-from="1,{f(fr)}" data-o="{f(cx)},{f(tt+4)}" data-dur="2" data-delay="{delay}" data-ease="soft">{col}</g>'
    out.append(col)
    out.append(f'<rect x="{f(cx-7)}" y="{f(st)}" width="14" height="{f(tt+10-st)}" fill="none" stroke="{GLASS}" stroke-width="2.5"/>')
    out.append(f'<rect x="{f(cx-10)}" y="{f(tt+2)}" width="20" height="7" rx="2" fill="{RUB}"/>')   # 고무줄
    return ''.join(out)


# ───────── 표지 ─────────
@fig('cover')
def cover():
    o = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    o.append(device(165, 400, 260, 1.1, delay=0.3, straw_top=70))
    o.append(device(375, 400, 135, 1.25, delay=0.5, straw_top=70))
    o.append(line(165, 260, 375, 260, MUTED, 2, '5 5'))
    o.append(tex(165, 436, '농도가 작은', 21, 'middle', extra=' data-weight="700"'))
    o.append(tex(165, 462, '설탕물', 21, 'middle', extra=' data-weight="700"'))
    o.append(tex(375, 436, '농도가 큰', 21, 'middle', extra=' data-weight="700"'))
    o.append(tex(375, 462, '설탕물', 21, 'middle', extra=' data-weight="700"'))
    return ''.join(o)


# ───────── 생각 열기: 과일청 ─────────
def jar(x, y, juice=False):
    w, h = 150, 190
    o = []
    if juice:
        o.append(f'<g data-anim="scale" data-from="1,0" data-o="{f(x+w/2)},{f(y+h-4)}" data-dur="1.8" data-delay=".6" data-ease="soft"><rect x="{f(x+4)}" y="{f(y+h-80)}" width="{f(w-8)}" height="76" rx="8" fill="#F6C94B" opacity=".75"/></g>')
    random.seed(7 if juice else 3)
    for i, (sx, sy) in enumerate([(40, 150), (100, 140), (70, 110), (40, 80), (108, 82), (72, 50)]):
        cx, cy = x + sx, y + sy + (6 if juice else 0)
        if juice and sy < 90:
            cy += 10
        o.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="24" fill="#FCEB9A" stroke="#E0B52B" stroke-width="3"/>')
        for k in range(6):
            a = math.radians(k * 60 + i * 13)
            o.append(line(cx, cy, cx + 18 * math.cos(a), cy + 18 * math.sin(a), '#E0B52B', 1.6))
    if not juice:
        for k in range(26):
            sx = x + 18 + random.random() * (w - 36)
            sy = y + 30 + random.random() * 140
            o.append(f'<rect x="{f(sx)}" y="{f(sy)}" width="7" height="7" fill="#fff" stroke="#9AA5B1" stroke-width="1.2"/>')
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{w}" height="{h}" rx="16" fill="none" stroke="{GLASS}" stroke-width="3.5"/>')
    o.append(f'<rect x="{f(x+10)}" y="{f(y-22)}" width="{w-20}" height="22" rx="5" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2.5"/>')
    return ''.join(o)


@fig('jar')
def jar_fig():
    o = [jar(20, 46), jar(270, 46, True)]
    o.append(arw(186, 140, 252, 140, 'ink', 3.5))
    o.append(tex(219, 124, '숙성', 19, 'middle'))
    o.append(tex(95, 266, '과일 + 설탕', 20, 'middle', extra=' data-weight="700"'))
    o.append(tex(345, 266, '며칠 뒤', 20, 'middle', extra=' data-weight="700"'))
    o.append(line(424, 200, 446, 200, MUTED, 2) + tex(450, 206, '즙', 20))
    return ''.join(o)


# ───────── ① 반투막 ─────────
@fig('memb')
def memb():
    o = ['<rect x="10" y="20" width="500" height="250" rx="10" fill="#F4F9FD" stroke="#9FC3DD" stroke-width="2"/>']
    # 막: 벽 조각 + 구멍(52)
    walls = [(22, 96), (148, 190), (242, 268)]
    for a, b in walls:
        o.append(f'<rect x="252" y="{a}" width="16" height="{b-a}" fill="#9AA5B1"/>')
    # 왼쪽(설탕물)
    o.append(sugar(100, 84, 34))
    o.append(water(56, 176, 200) + water(150, 150, 40) + water(196, 58, 90) + water(96, 240, -90))
    # 막힌 설탕 분자
    o.append(sugar(212, 216, 34))
    o.append(line(236, 204, 250, 218, INK, 4) + line(250, 204, 236, 218, INK, 4))
    # 오른쪽
    o.append(water(350, 70, 30) + water(440, 140, 160) + water(360, 230, -60) + water(450, 235, 200))
    # 통과하는 물 분자
    o.append(f'<g data-anim="move" data-from="-112,0" data-dur="2" data-delay=".4" data-ease="soft">{water(320, 122, 0)}</g>')
    o.append(arw(282, 88, 330, 88, 'ink', 3))
    o.append(tex(306, 78, '통과', 19, 'middle', extra=' data-halo="1"'))
    o.append(tex(212, 236 - 20, '', 1)) if False else None
    o.append(tex(262, 296, '반투막', 20, 'middle', extra=' data-weight="700"'))
    o.append(tex(196, 176, '통과 못 함', 19, 'middle', extra=' data-halo="1"'))
    return ''.join(x for x in o if x)


# ───────── ② 삼투 현상 (그림 II-17 꼴) ─────────
@fig('osmo')
def osmo():
    random.seed(11)
    o = ['<rect x="10" y="40" width="540" height="230" rx="10" fill="#F4F9FD" stroke="#9FC3DD" stroke-width="2"/>']
    o.append(line(280, 42, 280, 268, MUTED, 5, '16 9'))
    sugL = [(90, 110), (190, 200), (120, 230)]
    sugR = [(330, 90), (420, 80), (500, 120), (360, 170), (460, 180), (330, 240), (420, 235), (510, 230)]
    occ = sugL + sugR
    def free(x, y, rad=24):
        return all((x - a) ** 2 + (y - b) ** 2 > rad ** 2 for a, b in occ)
    dots = []
    for side, n, x0, x1 in (('L', 26, 26, 262), ('R', 11, 298, 536)):
        k = 0
        while k < n:
            x, y = x0 + random.random() * (x1 - x0), 56 + random.random() * 198
            if free(x, y, 22 if side == 'L' else 26):
                occ.append((x, y)); dots.append(wdot(x, y)); k += 1
    o += [sugar(x, y) for x, y in sugL + sugR] + dots
    # 이동하는 물 분자: 왼쪽→오른쪽 4, 오른쪽→왼쪽 1 (막 구멍을 지남)
    mv = [((300, 70), 1), ((304, 132), 1), ((298, 206), 1), ((306, 258), 1), ((258, 160), -1)]
    for i, ((x, y), d) in enumerate(mv):
        o.append(f'<g data-anim="move" data-from="{-50*d},0" data-dur="1.6" data-delay="{f(.3+.35*i)}" data-ease="soft">{wdot(x, y)}</g>')
    o.append(arw(220, 296, 340, 296, 'ink', 4))
    o.append(tex(280, 326, '용매(물 분자)의 이동', 19, 'middle'))
    o.append(tex(140, 30, '농도가 낮은 용액', 20, 'middle', extra=' data-weight="700"'))
    o.append(tex(420, 30, '농도가 높은 용액', 20, 'middle', extra=' data-weight="700"'))
    return ''.join(o)


def legend_dots(x, y):
    return (wdot(x, y - 6) + tex(x + 14, y, '물 분자', 19)
            + sugar(x + 110, y - 6) + tex(x + 130, y, '설탕 분자', 19)
            + line(x + 238, y - 18, x + 238, y + 4, MUTED, 5, '8 5') + tex(x + 250, y, '반투막', 19))


@fig('osmo_leg')
def osmo_leg():
    return legend_dots(20, 26)


# ───────── 삼투 현상 실험 장치 (그림 II-18 꼴) ─────────
@fig('setup')
def setup():
    o = [device(110, 330, 196, 1.0, anim=False, straw_top=24)]
    o.append(device(400, 330, 104, 1.25, anim=True, straw_top=24, delay=.4))
    o.append(line(400, 196, 400, 196))
    o.append(arw(200, 150, 310, 150, 'ink', 3.5))
    o.append(tex(255, 132, '충분한 시간이', 18, 'middle') + tex(255, 180, '흐른 후', 18, 'middle'))
    o.append(line(118, 200, 150, 200, MUTED, 1.5, '3 3') + line(408, 196, 440, 196, MUTED, 1.5, '3 3'))
    o.append(line(150, 200, 448, 200, MUTED, 1.5, '3 3'))
    o.append(tex(110, 362, '처음', 20, 'middle', extra=' data-weight="700"'))
    o.append(tex(400, 362, '나중', 20, 'middle', extra=' data-weight="700"'))
    # 라벨(처음 장치)
    o.append(line(124, 268, 176, 286, MUTED, 1.5) + tex(180, 292, '설탕물', 18))
    o.append(line(36, 300, 48, 300, MUTED, 1.5) + tex(32, 306, '물', 18, 'end'))
    o.append(line(117, 60, 150, 60, MUTED, 1.5) + tex(154, 66, '빨대', 18))
    return ''.join(o)


# ───────── 탐구: 장치 만들기 ─────────
@fig('tie')
def tie():
    o = [f'<rect x="113" y="14" width="14" height="110" fill="#fff" stroke="{GLASS}" stroke-width="2.5"/>']
    o.append(f'<path d="M108 118 C88 140 92 180 92 230 C92 280 100 300 116 314 L124 314 C140 300 148 280 148 230 C148 180 152 140 132 118 Z" fill="#EEF3F8" stroke="{SOLS}" stroke-width="2.5"/>')
    o.append(f'<g data-anim="pop" data-dur=".8" data-delay=".3"><rect x="106" y="114" width="28" height="9" rx="2" fill="{RUB}"/></g>')
    o.append(f'<g data-anim="pop" data-dur=".8" data-delay=".8"><rect x="106" y="312" width="28" height="9" rx="2" fill="{RUB}"/></g>')
    o.append(line(127, 50, 168, 50, MUTED, 1.5) + tex(172, 56, '빨대', 19))
    o.append(line(134, 118, 168, 104, MUTED, 1.5) + tex(172, 110, '고무줄', 19))
    o.append(line(148, 220, 168, 220, MUTED, 1.5) + tex(172, 214, '물에 불린', 19) + tex(172, 238, '반투막 튜브', 19))
    o.append(line(134, 318, 168, 318, MUTED, 1.5) + tex(172, 324, '고무줄(새지 않게)', 19))
    return ''.join(o)


# ───────── ③ 농도와 삼투 현상 (그림 II-19 꼴) ─────────
@fig('conc2')
def conc2():
    o = [device(120, 360, 214, 1.1, delay=.3, straw_top=30), device(360, 360, 96, 1.25, delay=.3, straw_top=30)]
    o.append(line(126, 214, 354, 214, MUTED, 1.5, '4 4') + line(366, 96, 400, 96, MUTED, 1.5, '4 4'))
    o.append(arw(392, 150, 392, 98, 'muted', 2) + arw(392, 160, 392, 212, 'muted', 2))
    o.append(tex(400, 162, '높이 차', 18))
    o.append(tex(120, 394, '농도가 작은 설탕물', 19, 'middle', extra=' data-weight="700"'))
    o.append(tex(360, 394, '농도가 큰 설탕물', 19, 'middle', extra=' data-weight="700"'))
    o.append(line(62, 300, 44, 300, MUTED, 1.5) + tex(40, 306, '물', 18, 'end'))
    return ''.join(o)


# ───────── 해 보기 그림 ─────────
@fig('cabbage')
def cabbage():
    o = ['<path d="M30 150 C30 70 90 30 150 30 C210 30 270 70 270 150 Z" fill="#E9F3C9" stroke="#8DAA3B" stroke-width="3"/>']
    for k, r in enumerate((100, 75, 50, 26)):
        o.append(f'<path d="M{150-r*1.15} 150 C{150-r*1.15} {150-r*0.9} {150-r*0.6} {150-r*1.1} 150 {150-r*1.1} C{150+r*0.6} {150-r*1.1} {150+r*1.15} {150-r*0.9} {150+r*1.15} 150" fill="none" stroke="{"#B9CF6E" if k % 2 else "#F2F6E0"}" stroke-width="5"/>')
    o.append('<path d="M110 150 L130 70 L150 150 Z" fill="#F8FBEA" stroke="#C9D98C" stroke-width="2"/>')
    random.seed(5)
    for k in range(18):
        x, y = 50 + random.random() * 200, 50 + random.random() * 90
        if (x - 150) ** 2 / 120 ** 2 + (y - 150) ** 2 / 115 ** 2 < 1:
            o.append(f'<rect x="{f(x)}" y="{f(y)}" width="7" height="7" fill="#fff" stroke="#9AA5B1" stroke-width="1.2"/>')
    o.append(line(20, 152, 280, 152, MUTED, 2))
    drops = [(46, 164), (96, 170), (204, 170), (254, 164)]
    for i, (x, y) in enumerate(drops):
        o.append(f'<g data-anim="move" data-from="0,-14" data-dur="1.2" data-delay="{f(.3+.25*i)}" data-ease="out"><path d="M{x} {y-9} C{x+7} {y} {x+7} {y+7} {x} {y+7} C{x-7} {y+7} {x-7} {y} {x} {y-9} Z" fill="#9FC3DD"/></g>')
    o.append(tex(150, 196, '소금 + 빠져나온 물', 22, 'middle', fill=MUTED))
    return ''.join(o)


@fig('plant')
def plant():
    o = ['<path d="M150 118 C150 80 148 60 150 40" fill="none" stroke="#5E8C3A" stroke-width="5"/>']
    o.append('<path d="M150 70 C120 60 96 80 86 104 C110 100 136 90 150 72 Z" fill="#A9C46C" stroke="#5E8C3A" stroke-width="2"/>')
    o.append('<path d="M150 52 C178 46 204 64 214 90 C190 88 164 76 150 54 Z" fill="#A9C46C" stroke="#5E8C3A" stroke-width="2"/>')
    o.append('<path d="M150 40 C140 26 146 12 156 8 C160 20 158 32 150 40 Z" fill="#B9CF6E" stroke="#5E8C3A" stroke-width="2"/>')
    o.append('<path d="M92 118 H208 L196 196 H104 Z" fill="#D9B38C" stroke="#8C6D46" stroke-width="3"/>')
    o.append('<path d="M150 120 C146 140 136 150 128 166 M150 120 C154 142 166 152 172 170 M150 120 V176" fill="none" stroke="#F3E6D3" stroke-width="3"/>')
    random.seed(9)
    for k in range(14):
        x, y = 104 + random.random() * 92, 124 + random.random() * 10
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="#fff" stroke="#7B4FC8" stroke-width="1.5"/>')
    for i, (x, y, dx) in enumerate([(124, 178, 12), (180, 176, -12)]):
        o.append(f'<g data-anim="move" data-from="{dx},-8" data-dur="1.2" data-delay="{f(.4+.3*i)}" data-ease="out"><path d="M{x} {y-8} C{x+6} {y} {x+6} {y+6} {x} {y+6} C{x-6} {y+6} {x-6} {y} {x} {y-8} Z" fill="#9FC3DD"/></g>')
    o.append(line(208, 128, 228, 128, MUTED, 1.5) + tex(232, 136, '비료', 22))
    return ''.join(o)


# ───────── ④ 자료실: U자관 ─────────
def utube(ox, yl, yr, press=False, anim=None):
    a, b, yb = ox + 30, ox + 130, 230
    r = (b - a) / 2
    mid = (a + b) / 2
    o = []
    wl = f'<rect x="{f(a-15)}" y="{f(yl)}" width="30" height="{f(yb-yl+1)}" fill="{WATER}"/>'
    wr = f'<rect x="{f(b-15)}" y="{f(yr)}" width="30" height="{f(yb-yr+1)}" fill="#B9D6EE"/>'
    if anim:
        wl = f'<g data-anim="scale" data-from="1,{f((yb-anim[0])/(yb-yl))}" data-o="{f(a)},{yb}" data-dur="2" data-delay=".4" data-ease="soft">{wl}</g>'
        wr = f'<g data-anim="scale" data-from="1,{f((yb-anim[1])/(yb-yr))}" data-o="{f(b)},{yb}" data-dur="2" data-delay=".4" data-ease="soft">{wr}</g>'
    o.append(wl + wr)
    o.append(f'<path d="M{f(a)} {yb} A{f(r)} {f(r)} 0 0 0 {f(mid)} {f(yb+r)}" fill="none" stroke="{WATER}" stroke-width="30"/>')
    o.append(f'<path d="M{f(mid)} {f(yb+r)} A{f(r)} {f(r)} 0 0 0 {f(b)} {yb}" fill="none" stroke="#B9D6EE" stroke-width="30"/>')
    o.append(line(a - 15, yl, a + 15, yl, WTOP, 2) + line(b - 15, yr, b + 15, yr, WTOP, 2))
    for s in (1, -1):
        rr = r + 16 * s
        o.append(f'<path d="M{f(a-16*s)} 40 V{yb} A{f(rr)} {f(rr)} 0 0 0 {f(b+16*s)} {yb} V40" fill="none" stroke="{GLASS}" stroke-width="3"/>')
    o.append(line(mid, yb + r - 16, mid, yb + r + 16, '#D7263D', 4, '5 3'))
    if press:
        o.append(f'<rect x="{f(b-14)}" y="{f(yr-26)}" width="28" height="24" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>')
        o.append(arw(b, yr - 74, b, yr - 30, 'plus', 4))
        o.append(tex(b, yr - 82, '삼투압', 19, 'middle', fill=PLUS, extra=' data-weight="700"'))
    return ''.join(o)


@fig('utube')
def utube_fig():
    o = [utube(10, 120, 120), utube(230, 140, 100, anim=(120, 120)), utube(450, 120, 120, press=True)]
    o.append(arw(186, 160, 226, 160, 'ink', 3) + arw(406, 160, 446, 160, 'ink', 3))
    # 치수선 h (둘째 그림)
    x = 395
    o.append(line(375, 100, 402, 100, MUTED, 1.5, '3 3') + line(276, 140, 402, 140, MUTED, 1.5, '3 3'))
    o.append(arw(x, 120, x, 102, 'muted', 2) + arw(x, 120, x, 138, 'muted', 2))
    o.append(tex(x + 8, 127, '$h$', 20))
    o.append(tex(90, 324, '처음', 19, 'middle', extra=' data-weight="700"'))
    o.append(tex(310, 324, '오랫동안 둔 뒤', 19, 'middle', extra=' data-weight="700"'))
    o.append(tex(530, 324, '설탕물 쪽에 압력', 19, 'middle', extra=' data-weight="700"'))
    o.append(tex(40, 30, '물', 19, 'middle') + tex(140, 30, '설탕물', 19, 'middle'))
    o.append(line(80, 276, 64, 300, PLUS, 1.5) + tex(60, 306, '반투막', 18, 'end', fill=PLUS))
    return ''.join(o)


# ───────── 대단원 마무리 10 ─────────
@fig('q10')
def q10():
    o = [device(130, 330, 70, 1.25, delay=.3, straw_top=24, tfill='#B9D6EE', tstroke=SOLS)]
    o.append(line(140, 196, 214, 196, MUTED, 1.5, '4 4') + line(140, 70, 214, 70, MUTED, 1.5, '4 4'))
    o.append(arw(206, 133, 206, 72, 'muted', 2) + arw(206, 133, 206, 194, 'muted', 2))
    o.append(tex(214, 140, '$h$', 20))
    o.append(line(150, 250, 214, 250, MUTED, 1.5) + tex(218, 256, '수용액 B', 19))
    o.append(line(150, 280, 214, 290, MUTED, 1.5) + tex(218, 296, '반투막 튜브', 19))
    o.append(line(196, 318, 214, 326, MUTED, 1.5) + tex(218, 332, '수용액 A', 19))
    o.append(tex(112, 204, '처음 높이', 18, 'end', fill=MUTED))
    return ''.join(o)


def main():
    tpl = open(TPL, encoding='utf-8').read()
    def rep(m):
        k = m.group(1)
        if k not in FIG:
            raise KeyError(k)
        return FIG[k]()
    out = re.sub(r'\{\{(\w+)\}\}', rep, tpl)
    open(OUT, 'w', encoding='utf-8').write(out)
    print('ok', len(out))


if __name__ == '__main__':
    main()
