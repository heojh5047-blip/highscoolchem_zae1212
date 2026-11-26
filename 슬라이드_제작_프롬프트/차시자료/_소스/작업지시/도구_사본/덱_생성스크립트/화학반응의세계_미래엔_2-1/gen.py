# 2-1 산화와 환원 — tpl*.html 의 @@이름@@ 자리에 그림 SVG 조각을 넣어 slides.html 을 만든다.
import math, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import f, lewis_sym, dot_pair, side_pos, INK, MUTED

OX, RD, MINUS, PLUS, GRAV = '#C2410C', '#0E7490', '#1F6FD1', '#D7263D', '#8C99A6'
CUSOL = '#3E8ED0'
GLASS = '#7E8B98'
F = {}


def atom(x, y, r, el, lab=None, d=False):
    a = f'{f(x)},{f(y)},{r},{el}'
    if lab is not None:
        a += ',' + lab
    if d:
        a += ',d'
    return f'<g data-atom="{a}"></g>'


def ion(x, y, el, q, r=26, sign='+'):
    """원소 색 이온 공 + 전하 테 + 라벨"""
    sup = (q if q != '1' else '') + sign
    col = PLUS if sign == '+' else MINUS
    return (atom(x, y, r, el, '\\mathrm{%s}^{%s}' % (el, sup))
            + f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + 1.5)}" fill="none" stroke="{col}" stroke-width="2.5"/>')


def tex(x, y, t, size=20, anchor='middle', fill=None, mix=False, extra=''):
    fl = f' fill="{fill}"' if fill else ''
    k = 'data-mix' if mix else 'data-tex'
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {k}="{t}" data-size="{size}" data-anchor="{anchor}"{fl}{extra}></text>'


def arw(x1, y1, x2, y2, col='ink', w=3, d=False, extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}{",d" if d else ""}"{extra}></g>'


def edot(x, y, r=6):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{MINUS}"/>'


def bracket(x1, x2, y0, y1, col, lab, ly, step=None, size=20, anim=True):
    """x1 아래(또는 위) y0 에서 y1 까지 꺾어 x2 로 — 끝에 화살촉. 라벨은 가운데"""
    cls = f' class="step" data-g="{step}"' if step else ''
    an = ' data-anim="draw" data-dur=".9"' if anim else ''
    p = f'<path d="M{f(x1)} {f(y0)} V{f(y1)} H{f(x2)} V{f(y0 + (6 if y1 < y0 else -6))}" fill="none" stroke="{col}" stroke-width="3"{an}/>'
    dy = 1 if y1 < y0 else -1  # 화살표 방향(끝에서 y0 쪽)
    head = arw(x2, y0 + dy * 16 * (-1) * (-1) - (14 if y1 < y0 else -14), x2, y0, col, 3)
    return (f'<g{cls}>{p}{arw(x2, (y0 - 20) if y1 < y0 else (y0 + 20), x2, y0, col, 3)}'
            + tex((x1 + x2) / 2, ly, lab, size, fill=col, mix=True, extra=' data-weight="700" data-halo="1"') + '</g>')


def beaker(x0, y0, w, h, sol_top, sol_fill='#DDEEF8', sol_op=1.0, rim=True):
    """비커: 왼쪽 위 (x0,y0), 너비 w, 높이 h, 용액 윗면 sol_top"""
    x1, y1 = x0 + w, y0 + h
    s = (f'<rect x="{f(x0 + 2)}" y="{f(sol_top)}" width="{f(w - 4)}" height="{f(y1 - sol_top - 2)}" rx="8" fill="{sol_fill}" fill-opacity="{sol_op}"/>'
         f'<line x1="{f(x0 + 2)}" y1="{f(sol_top)}" x2="{f(x1 - 2)}" y2="{f(sol_top)}" stroke="#9FC3DD" stroke-width="2"/>'
         f'<path d="M{f(x0 - 6)} {f(y0)} H{f(x0)} V{f(y1 - 10)} Q{f(x0)} {f(y1)} {f(x0 + 10)} {f(y1)} H{f(x1 - 10)} Q{f(x1)} {f(y1)} {f(x1)} {f(y1 - 10)} V{f(y0)} H{f(x1 + 6)}" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linejoin="round"/>')
    return s


# ── S1 표지: 황산 구리(II) 수용액 속 아연판 + 확대 원 ──
def cover():
    s = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    s += beaker(70, 150, 170, 270, 215, CUSOL, .26)
    s += '<rect x="135" y="100" width="40" height="300" rx="3" fill="#8FA3B8" stroke="#5C6F82" stroke-width="2"/>'
    for i, y in enumerate(range(240, 396, 18)):
        x = 132 if i % 2 == 0 else 178
        s += f'<circle cx="{x}" cy="{y}" r="6" fill="#C8803A" stroke="#8A5221" stroke-width="1.2"/>'
    s += f'<line x1="178" y1="300" x2="262" y2="232" stroke="{MUTED}" stroke-width="1.5"/><line x1="178" y1="320" x2="262" y2="420" stroke="{MUTED}" stroke-width="1.5"/>'
    cx, cy, r = 380, 326, 122
    s += f'<defs><clipPath id="clip-rm21-01"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>'
    s += f'<g clip-path="url(#clip-rm21-01)"><rect x="250" y="190" width="260" height="270" fill="#FFFFFF"/><rect x="250" y="190" width="260" height="270" fill="{CUSOL}" fill-opacity=".14"/>'
    s += '<rect x="250" y="190" width="58" height="270" fill="#C9D3DD"/>'
    s += atom(300, 262, 27, 'Zn', d=True) + atom(300, 326, 27, 'Zn') + atom(300, 390, 27, 'Zn') + atom(246, 294, 27, 'Zn') + atom(246, 358, 27, 'Zn')
    s += atom(354, 326, 27, 'Cu')
    s += '</g>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{MUTED}" stroke-width="3"/>'
    s += f'<g data-anim="move" data-from="-76,0" data-dur="1.4" data-delay=".4" data-ease="out">{ion(440, 262, "Zn", "2")}</g>'
    s += f'<g data-anim="move" data-from="60,0" data-dur="1.4" data-delay="1.2" data-ease="out">{ion(436, 390, "Cu", "2")}</g>'
    s += arw(330, 384, 404, 384, 'minus', 3) + tex(367, 372, 'e^-', 22, fill=MINUS)
    s += tex(300, 484, '황산 구리(II) 수용액 속 아연판', 18, fill=MUTED, mix=True)
    return s
F['cover'] = cover()


# ── S2 대단원 도입: 세 장면 ──
def scene_nail():
    s = '<rect x="0" y="0" width="300" height="170" rx="10" fill="#F4F1EC"/>'
    s += '<rect x="40" y="76" width="200" height="18" rx="4" fill="#9AA5B1" stroke="#5B6B7F" stroke-width="2"/><rect x="34" y="62" width="12" height="46" rx="3" fill="#9AA5B1" stroke="#5B6B7F" stroke-width="2"/><path d="M240 76 L272 85 L240 94 Z" fill="#9AA5B1" stroke="#5B6B7F" stroke-width="2"/>'
    s += '<g data-anim="fade" data-dur="1.6" data-delay=".5">'
    for x, y, rx in ((90, 85, 18), (140, 82, 12), (185, 88, 20), (225, 84, 10)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="8" fill="#B5562A" fill-opacity=".85"/>'
    s += '</g>' + tex(150, 145, '녹: 철 + 산소 + 물', 20, fill=MUTED, mix=True)
    return s


def scene_cell():
    s = '<rect x="0" y="0" width="300" height="170" rx="10" fill="#EEF3F8"/>'
    s += '<rect x="40" y="40" width="70" height="100" rx="10" fill="#FFFFFF" stroke="#16233D" stroke-width="2.5"/><rect x="62" y="32" width="26" height="10" rx="3" fill="#16233D"/>'
    s += tex(75, 78, '+', 26) + tex(75, 128, '-', 26)
    s += '<path d="M75 32 V18 H230 V60" fill="none" stroke="#16233D" stroke-width="3"/><path d="M75 142 V156 H230 V100" fill="none" stroke="#16233D" stroke-width="3"/>'
    s += '<circle cx="230" cy="80" r="20" fill="#FFF3B0" stroke="#16233D" stroke-width="2.5"/>'
    s += f'<path d="M75 156 H230 V100" fill="none" stroke="{MINUS}" stroke-width="3" stroke-dasharray="6 10" data-anim="dash" data-speed="30" data-flow="1"/>'
    s += tex(180, 140, 'e^-', 20, fill=MINUS) + tex(150, 110, '전지', 20, fill=MUTED, mix=True, anchor='start')
    return s


def scene_leaf():
    s = '<rect x="0" y="0" width="300" height="170" rx="10" fill="#EEF7EF"/>'
    s += '<circle cx="50" cy="40" r="18" fill="#F7C948"/>'
    s += '<path d="M100 130 C120 50 210 30 260 40 C250 100 190 145 100 130 Z" fill="#6FBF73" stroke="#2E7D32" stroke-width="2.5"/><path d="M100 130 C150 100 200 70 258 42" fill="none" stroke="#2E7D32" stroke-width="2"/>'
    s += tex(150, 160, '광합성 · 호흡', 20, fill=MUTED, mix=True)
    return s
F['sc_nail'] = scene_nail()
F['sc_cell'] = scene_cell()
F['sc_leaf'] = scene_leaf()


# ── S5 생각 열기: 구리선과 질산 은 수용액 ──
def silver_tree(after):
    s = beaker(40, 30, 140, 190, 70, CUSOL if after else '#EEF4F8', .22 if after else 1)
    s += '<path d="M110 10 V200" stroke="#C8803A" stroke-width="7" stroke-linecap="round" fill="none"/>'
    if after:
        s += '<g data-anim="pop" data-o="110,140" data-dur="1" data-delay=".5" data-ease="back">'
        for y in range(90, 200, 16):
            for sgn in (-1, 1):
                L = 16 + (y % 3) * 4
                s += f'<path d="M110 {y} l{sgn * L} {-L * .6:.0f} M{110 + sgn * L * .5:.0f} {y - L * .3:.0f} l{sgn * 6} 6" stroke="#9AA5B1" stroke-width="3" stroke-linecap="round" fill="none"/>'
        s += '</g>'
    return s
F['ag_before'] = silver_tree(False)
F['ag_after'] = silver_tree(True)


# ── S6 2CuO + C → 2Cu + CO2 입자 모형 ──
def cuo_c():
    s = atom(116, 80, 24, 'O') + atom(70, 80, 27, 'Cu') + atom(116, 160, 24, 'O') + atom(70, 160, 27, 'Cu')
    s += atom(205, 120, 24, 'C')
    s += arw(250, 120, 300, 120, 'ink', 3)
    s += atom(360, 80, 27, 'Cu') + atom(360, 160, 27, 'Cu')
    s += f'<g data-anim="move" data-from="-332,-40" data-dur="1.4" data-delay=".5" data-ease="soft">{atom(448, 120, 24, "O")}</g>'
    s += f'<g data-anim="move" data-from="-416,40" data-dur="1.4" data-delay=".5" data-ease="soft">{atom(532, 120, 24, "O")}</g>'
    s += atom(490, 120, 24, 'C')
    for x, t in ((93, '\\ce{2CuO}'), (160, '+'), (205, '\\ce{C}'), (360, '\\ce{2Cu}'), (420, '+'), (490, '\\ce{CO2}')):
        s += tex(x, 228, t, 24)
    s += bracket(205, 490, 92, 44, OX, '산화: 산소를 얻음', 36, step='o1')
    s += bracket(93, 360, 244, 272, RD, '환원: 산소를 잃음', 298, step='o2')
    return s
F['cuo_c'] = cuo_c()


# ── S7 철의 제련 반응식 + 괄호 ──
def fe_eq():
    s = ''
    for x, t in ((90, '\\ce{Fe2O3}'), (178, '+'), (250, '\\ce{3CO}'), (340, '\\ce{->}'), (428, '\\ce{2Fe}'), (500, '+'), (578, '\\ce{3CO2}')):
        s += tex(x, 120, t, 34)
    s += bracket(250, 578, 84, 46, OX, '산화: 산소를 얻음', 36, step='f1')
    s += bracket(90, 428, 140, 172, RD, '환원: 산소를 잃음', 200, step='f2')
    return s
F['fe_eq'] = fe_eq()


# 용광로
def furnace():
    s = '<path d="M90 40 L170 40 L200 230 L60 230 Z" fill="#E9E2DA" stroke="#5B6B7F" stroke-width="3" stroke-linejoin="round"/>'
    s += '<rect x="70" y="230" width="120" height="30" rx="4" fill="#E9E2DA" stroke="#5B6B7F" stroke-width="3"/>'
    s += '<rect x="74" y="238" width="112" height="18" rx="3" fill="#F28C28"/>'
    for i in range(14):
        x, y = 100 + (i * 37) % 64, 70 + (i * 23) % 140
        s += f'<circle cx="{x}" cy="{y}" r="{5 + i % 3}" fill="{"#7A4A2A" if i % 2 else "#3A3F47"}"/>'
    s += arw(130, 24, 130, 52, 'muted', 2.5)
    s += arw(30, 214, 66, 214, 'equi', 3) + arw(230, 214, 194, 214, 'equi', 3)
    s += tex(130, 18, '철광석 · 코크스', 18, fill=MUTED, mix=True)
    s += tex(28, 198, '뜨거운 공기', 18, fill='#B5651D', mix=True, anchor='start')
    s += tex(130, 282, '녹은 철', 18, fill='#B5651D', mix=True)
    return s
F['furnace'] = furnace()


# ── S8 나트륨과 염소 ──
def na_cl2():
    s = '<path d="M95 40 V90 Q40 110 40 170 Q40 230 120 230 Q200 230 200 170 Q200 110 145 90 V40" fill="#E5EFB8" fill-opacity=".7" stroke="#7E8B98" stroke-width="3"/>'
    s += '<path d="M120 20 V150" stroke="#5B6B7F" stroke-width="3"/><path d="M104 150 Q120 168 136 150 Z" fill="#9AA5B1" stroke="#5B6B7F" stroke-width="2"/>'
    s += '<path d="M120 152 C104 136 112 118 120 104 C128 118 136 136 120 152 Z" fill="#F7A41C" fill-opacity=".85"/>'
    for x, y in ((80, 190), (100, 205), (150, 200), (165, 180), (70, 165), (130, 215)):
        s += f'<circle cx="{x}" cy="{y}" r="7" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="1.5"/>'
    s += tex(232, 120, '염소 기체 속에서||타는 나트륨', 19, fill=MUTED, mix=True, anchor='start')
    s += tex(232, 205, '흰 고체 $\\ce{NaCl}$', 19, fill=MUTED, mix=True, anchor='start')
    return s
F['na_cl2'] = na_cl2()


# ── S9 루이스 전자점식: Na + Cl → Na+ + Cl- ──
def na_cl_lewis():
    S = 40
    s = lewis_sym(80, 96, 'Na', S, dots={'r': 1})
    s += lewis_sym(230, 96, 'Cl', S, dots={'u': 2, 'd': 2, 'r': 2, 'l': 1})
    s += f'<path d="M114 84 Q150 34 196 84" fill="none" stroke="{MINUS}" stroke-width="2.5"/>' + arw(186, 76, 197, 87, 'minus', 2.5)
    s += tex(155, 46, 'e^-', 22, fill=MINUS)
    s += arw(296, 96, 346, 96, 'ink', 3)
    s += tex(410, 110.4, '\\mathrm{Na}^{+}', 40)
    # [ :Cl: ]-
    x = 545
    s += lewis_sym(x, 96, 'Cl', S, dots={'u': 2, 'd': 2, 'r': 2})
    s += dot_pair(*side_pos(x, 96, 'l', S), 'v', 1, S).replace(f'cy="96"', 'cy="88.8"')
    s += f'<g data-anim="move" data-from="-460,0" data-dur="1.4" data-delay=".6" data-ease="soft"><circle cx="{f(x - 0.7 * S)}" cy="103.2" r="5" fill="{MINUS}"/></g>'
    s += f'<path d="M{x - 44} 56 h-8 v80 h8 M{x + 44} 56 h8 v80 h-8" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s += tex(x + 62, 62, '-', 26)
    s += tex(410, 166, '전자를 잃음||→ 산화', 20, fill=OX, mix=True, extra=' data-weight="700"')
    s += tex(545, 166, '전자를 얻음||→ 환원', 20, fill=RD, mix=True, extra=' data-weight="700"')
    return s
F['na_cl_lewis'] = na_cl_lewis()


# ── S10 아연판 비커 (현상) / 입자 모형 ──
def zn_beaker(op=.22):
    s = beaker(70, 40, 160, 150, 80, CUSOL, op)
    s += '<rect x="132" y="16" width="36" height="160" rx="3" fill="#8FA3B8" stroke="#5C6F82" stroke-width="2"/>'
    for i, y in enumerate(range(96, 172, 14)):
        x = 130 if i % 2 == 0 else 170
        s += f'<circle cx="{x}" cy="{y}" r="5.5" fill="#C8803A" stroke="#8A5221" stroke-width="1.2"/>'
    s += tex(176, 34, '아연판', 19, fill=MUTED, mix=True, anchor='start')
    return s
F['zn_beaker'] = zn_beaker()


def zn_particles():
    s = '<rect x="0" y="0" width="300" height="210" rx="8" fill="#3E8ED0" fill-opacity=".10"/>'
    s += '<rect x="0" y="0" width="64" height="210" fill="#C9D3DD"/>'
    s += atom(40, 50, 27, 'Zn', d=True) + atom(40, 104, 27, 'Zn') + atom(40, 158, 27, 'Zn')
    s += atom(94, 104, 27, 'Cu')
    s += f'<g data-anim="move" data-from="-100,0" data-dur="1.3" data-delay=".3" data-ease="out">{ion(160, 50, "Zn", "2")}</g>'
    s += f'<g data-anim="move" data-from="50,0" data-dur="1.3" data-delay=".9" data-ease="out">{ion(206, 158, "Cu", "2")}</g>'
    s += arw(70, 150, 176, 150, 'minus', 2.5) + tex(120, 140, '2e^-', 19, fill=MINUS)
    s += f'<circle cx="250" cy="70" r="16" fill="#C9D3DD" stroke="{GRAV}" stroke-width="2"/>' + tex(250, 110, '\\ce{SO4^2-}', 18, fill=MUTED)
    return s
F['zn_particles'] = zn_particles()


# ── S14 Cu + 2Ag+ → Cu2+ + 2Ag ──
def cu_ag():
    s = atom(80, 110, 27, 'Cu')
    s += ion(230, 60, 'Ag', '1') + ion(230, 160, 'Ag', '1')
    s += arw(108, 100, 198, 70, 'minus', 2.5) + arw(108, 120, 198, 150, 'minus', 2.5)
    s += f'<g data-anim="move" data-from="-80,28" data-dur="1.2" data-delay=".5" data-ease="out">{edot(182, 76)}</g>'
    s += f'<g data-anim="move" data-from="-80,-28" data-dur="1.2" data-delay=".5" data-ease="out">{edot(182, 144)}</g>'
    s += tex(140, 70, 'e^-', 20, fill=MINUS) + tex(140, 166, 'e^-', 20, fill=MINUS)
    s += arw(296, 110, 350, 110, 'ink', 3)
    s += ion(420, 110, 'Cu', '2') + atom(530, 60, 29, 'Ag') + atom(530, 160, 29, 'Ag')
    s += tex(80, 214, '전자 2개를 잃음', 19, fill=OX, mix=True) + tex(230, 214, '전자 1개씩 얻음', 19, fill=RD, mix=True)
    return s
F['cu_ag'] = cu_ag()


# ── S16 물 분자의 전자 치우침 ──
def water_delta():
    O = (150, 70)
    h = math.radians(104.5 / 2)
    L = 74
    Hs = [(O[0] - L * math.sin(h), O[1] + L * math.cos(h)), (O[0] + L * math.sin(h), O[1] + L * math.cos(h))]
    s = ''
    for hx, hy in Hs:
        s += f'<line x1="{O[0]}" y1="{O[1]}" x2="{f(hx)}" y2="{f(hy)}" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/>'
    s += ''.join(atom(hx, hy, 18, 'H') for hx, hy in Hs) + atom(*O, 24, 'O')
    s += f'<g data-anim="fade" data-dur="1.2" data-delay=".5"><ellipse cx="{O[0]}" cy="{O[1] + 6}" rx="44" ry="36" fill="{MINUS}" fill-opacity=".14" stroke="{MINUS}" stroke-width="1.5" stroke-dasharray="5 4"/></g>'
    s += tex(O[0] + 48, O[1] - 18, '\\delta^-', 22, fill=MINUS)
    s += tex(Hs[0][0] - 30, Hs[0][1] + 10, '\\delta^+', 22, fill=PLUS) + tex(Hs[1][0] + 30, Hs[1][1] + 10, '\\delta^+', 22, fill=PLUS)
    return s
F['water_delta'] = water_delta()


# ── S17 물의 산화수 정하기 ──
def water_ox():
    S = 40
    def h2o(x, y, give):
        s = lewis_sym(x, y, 'O', S, dots={'u': 2, 'r': 2, 'l': 2, 'd': 2})
        s += lewis_sym(x - 1.4 * S, y, 'H', S) + lewis_sym(x, y + 1.5 * S, 'H', S)
        if give:
            s += f'<rect x="{x - 38}" y="{y - 42}" width="76" height="84" rx="14" fill="#E08A2C" fill-opacity=".16" stroke="#E08A2C" stroke-width="1.8"/>'
        else:
            s += f'<rect x="{x - 36}" y="{y - 10}" width="16" height="22" rx="5" fill="#2E9E6A" fill-opacity=".18" stroke="#2E9E6A" stroke-width="1.5"/>'
            s += f'<rect x="{x - 9}" y="{y + 18}" width="22" height="16" rx="5" fill="#2E9E6A" fill-opacity=".18" stroke="#2E9E6A" stroke-width="1.5"/>'
        return s
    s = h2o(140, 80, False) + tex(118, 200, '공유 전자쌍 2개', 19, fill='#2E9E6A', mix=True)
    s += arw(250, 100, 310, 100, 'ink', 3)
    s += '<g class="step" data-g="w1">' + h2o(430, 80, True)
    s += tex(430, 26, '-2', 24, fill=INK, extra=' data-weight="700" data-halo="1"').replace('y="26"', 'y="28"')
    s += tex(362, 46, '+1', 24, extra=' data-weight="700"') + tex(476, 152, '+1', 24, extra=' data-weight="700"')
    s += tex(430, 200, '공유 전자쌍을 모두 O에게', 19, fill='#B5651D', mix=True) + '</g>'
    return s
F['water_ox'] = water_ox()


# ── S21 2H2 + O2 → 2H2O 산화수 ──
def h2o2_ox():
    t = '2\\overset{0}{\\ce{H}}{}_2 + \\overset{0}{\\ce{O}}{}_2 \\ce{->} 2\\overset{+1}{\\ce{H}}{}_2\\overset{-2}{\\ce{O}}'
    s = tex(300, 132, t, 40)
    s += bracket(150, 445, 70, 36, OX, 'H: 0 → +1 산화수 증가 → 산화', 26, step='h1', size=20)
    s += bracket(268, 510, 152, 184, RD, 'O: 0 → −2 산화수 감소 → 환원', 212, step='h2', size=20)
    return s
F['h2o2_ox'] = h2o2_ox()


# ── S24 산화제·환원제 ──
def roles():
    s = atom(100, 90, 27, 'Zn') + ion(400, 90, 'Cu', '2')
    s += arw(134, 90, 366, 90, 'minus', 3)
    s += f'<g data-anim="move" data-from="-200,0" data-dur="1.3" data-delay=".4" data-ease="soft">{edot(340, 82)}{edot(326, 98)}</g>'
    s += tex(250, 72, '전자 2개 이동', 20, fill=MINUS, mix=True)
    s += tex(100, 160, '\\textbf{환원제}', 24, fill=OX) + tex(100, 192, '전자를 줌 · 산화됨', 19, fill=OX, mix=True)
    s += tex(400, 160, '\\textbf{산화제}', 24, fill=RD) + tex(400, 192, '전자를 받음 · 환원됨', 19, fill=RD, mix=True)
    return s
F['roles'] = roles()


# ── S31 은수저 ──
def spoon():
    s = '<path d="M40 120 H400 L380 200 Q376 214 360 214 H80 Q64 214 60 200 Z" fill="#DDEEF8" stroke="#7E8B98" stroke-width="3"/>'
    s += '<path d="M60 194 H380" stroke="#B9A8A0" stroke-width="6"/>'
    s += '<rect x="64" y="186" width="312" height="8" fill="#D6D9DE" stroke="#A9AFB8" stroke-width="1.5"/>'
    sp = '<ellipse cx="120" cy="170" rx="40" ry="16"/><rect x="155" y="164" width="200" height="11" rx="5"/>'
    s += f'<g fill="#3A3F47">{sp}</g>'
    s += f'<g fill="#C9CED6" stroke="#8A919C" stroke-width="1.5" data-anim="fade" data-dur="2" data-delay=".8">{sp}</g>'
    for x in (100, 180, 260, 340):
        s += f'<path d="M{x} 110 q-8 -14 0 -28 q8 -14 0 -28" fill="none" stroke="#9FB0C2" stroke-width="2.5"/>'
    s += tex(420, 150, '알루미늄 포일', 19, fill=MUTED, mix=True, anchor='start').replace('y="150"', 'y="196"')
    s += tex(420, 160, '은수저', 19, fill=MUTED, mix=True, anchor='start')
    s += tex(420, 124, '뜨거운 물 +||베이킹 소다', 19, fill=MUTED, mix=True, anchor='start').replace('y="124"', 'y="96"')
    return s
F['spoon'] = spoon()


# ── S33 확인 문제 01 입자 그림 ──
def q1fig():
    s = '<rect x="0" y="0" width="380" height="220" rx="10" fill="#3E8ED0" fill-opacity=".10"/><rect x="0" y="0" width="70" height="220" fill="#C9D3DD"/>'
    s += atom(44, 50, 27, 'Zn') + atom(44, 110, 27, 'Zn') + atom(44, 170, 27, 'Zn')
    s += ion(170, 60, 'Cu', '2') + ion(260, 150, 'Cu', '2') + ion(320, 60, 'Cu', '2')
    s += f'<circle cx="160" cy="170" r="14" fill="#C9D3DD" stroke="{GRAV}" stroke-width="2"/><circle cx="245" cy="60" r="14" fill="#C9D3DD" stroke="{GRAV}" stroke-width="2"/><circle cx="340" cy="170" r="14" fill="#C9D3DD" stroke="{GRAV}" stroke-width="2"/>'
    s += tex(110, 212, '아연판', 18, fill=MUTED, mix=True).replace('x="110"', 'x="36"') + tex(300, 212, '○ $\\ce{SO4^2-}$', 18, fill=MUTED, mix=True)
    return s
F['q1fig'] = q1fig()



# ══════ 교과서 대조 뒤 추가한 그림 ══════
def firefly():
    s = '<rect x="0" y="0" width="420" height="230" rx="12" fill="#1E2A44"/>'
    for x, y in ((40, 40), (120, 25), (300, 30), (380, 60), (350, 190), (60, 200)):
        s += f'<circle cx="{x}" cy="{y}" r="1.8" fill="#FFFFFF" fill-opacity=".7"/>'
    s += '<path d="M0 230 Q120 170 230 200 T420 180 V230 Z" fill="#2E4A3A"/>'
    for i, (x, y, sc) in enumerate(((150, 110, 1), (270, 80, .75), (330, 140, .6))):
        glow = (f'<g data-anim="fade" data-dur="1.1" data-delay="{.3 + i * .4:.1f}" data-rep="alt">'
                f'<circle cx="{x + 14 * sc:.0f}" cy="{y + 6 * sc:.0f}" r="{26 * sc:.0f}" fill="#F7F06D" fill-opacity=".35"/>'
                f'<circle cx="{x + 14 * sc:.0f}" cy="{y + 6 * sc:.0f}" r="{11 * sc:.0f}" fill="#FBF7A8"/></g>')
        body = (f'<ellipse cx="{x}" cy="{y}" rx="{18 * sc:.0f}" ry="{8 * sc:.0f}" fill="#3A3F47"/>'
                f'<circle cx="{x - 18 * sc:.0f}" cy="{y - 2 * sc:.0f}" r="{6 * sc:.0f}" fill="#C2410C"/>'
                f'<ellipse cx="{x - 2 * sc:.0f}" cy="{y - 10 * sc:.0f}" rx="{14 * sc:.0f}" ry="{6 * sc:.0f}" fill="#9FB0C2" fill-opacity=".6" transform="rotate(-20 {x} {y})"/>')
        s += glow + body
    s += tex(210, 220, '루시페린의 산화 → 빛', 19, fill='#FBF7A8', mix=True)
    return s
F['firefly'] = firefly()


def celadon():
    s = '<ellipse cx="150" cy="250" rx="80" ry="10" fill="#C9D3DD"/>'
    s += ('<path d="M128 40 h44 q-4 18 -6 26 q60 40 54 110 q-6 50 -40 70 h-60 q-34 -20 -40 -70 q-6 -70 54 -110 q-2 -8 -6 -26 z" '
          'fill="#8FB9A8" stroke="#4E7C69" stroke-width="3"/>')
    s += '<path d="M110 150 q40 -30 80 0 M118 190 q32 -22 64 0" fill="none" stroke="#5E8F7B" stroke-width="2.5"/>'
    s += '<g data-anim="fade" data-dur="1.4" data-delay=".4"><circle cx="128" cy="110" r="7" fill="#FFFFFF" fill-opacity=".45"/></g>'
    s += tex(150, 288, '비취색 청자', 19, fill=MUTED, mix=True)
    return s
F['celadon'] = celadon()


def fe_eq2():
    s = ''
    for x, t in ((95, '\\ce{Fe2O3(s)}'), (192, '+'), (272, '\\ce{3CO(g)}'), (370, '\\ce{->}'), (460, '\\ce{2Fe(s)}'), (540, '+'), (630, '\\ce{3CO2(g)}')):
        s += tex(x, 120, t, 30)
    s += bracket(272, 630, 88, 48, OX, '산화: 산소를 얻음', 38, step='f1')
    s += bracket(95, 460, 140, 172, RD, '환원: 산소를 잃음', 200, step='f2')
    return s
F['fe_eq2'] = fe_eq2()


def mg_o2():
    s = atom(70, 70, 29, 'Mg') + atom(70, 160, 29, 'Mg')
    s += atom(180, 115, 24, 'O') + atom(220, 115, 24, 'O')
    s += arw(290, 115, 340, 115, 'ink', 3)
    s += ion(400, 70, 'Mg', '2') + ion(400, 160, 'Mg', '2')
    s += f'<g data-anim="move" data-from="-260,45" data-dur="1.4" data-delay=".5" data-ease="soft">{ion(456, 70, "O", "2", sign="-")}</g>'
    s += f'<g data-anim="move" data-from="-236,-45" data-dur="1.4" data-delay=".5" data-ease="soft">{ion(456, 160, "O", "2", sign="-")}</g>'
    s += f'<path d="M100 62 Q150 30 172 92" fill="none" stroke="{MINUS}" stroke-width="2.5"/>' + arw(166, 80, 173, 93, 'minus', 2.5)
    s += f'<path d="M100 168 Q160 196 214 138" fill="none" stroke="{MINUS}" stroke-width="2.5"/>' + arw(206, 150, 215, 137, 'minus', 2.5)
    s += tex(140, 34, '2e^-', 20, fill=MINUS) + tex(150, 210, '2e^-', 20, fill=MINUS)
    s += tex(70, 22, '\\ce{2Mg}', 22) + tex(200, 70, '\\ce{O2}', 22) + tex(428, 22, '\\ce{2MgO}', 22)
    return s
F['mg_o2'] = mg_o2()


def h2o2_models():
    s = atom(50, 80, 18, 'H') + atom(82, 80, 18, 'H')
    s += '<line x1="168" y1="74" x2="214" y2="74" stroke="#9AA5B1" stroke-width="6"/><line x1="168" y1="86" x2="214" y2="86" stroke="#9AA5B1" stroke-width="6"/>'
    s += atom(168, 80, 24, 'O') + atom(214, 80, 24, 'O')
    O = (360, 62); h = math.radians(104.5 / 2); L = 70
    Hs = [(O[0] - L * math.sin(h), O[1] + L * math.cos(h)), (O[0] + L * math.sin(h), O[1] + L * math.cos(h))]
    for hx, hy in Hs:
        s += f'<line x1="{O[0]}" y1="{O[1]}" x2="{f(hx)}" y2="{f(hy)}" stroke="#9AA5B1" stroke-width="7" stroke-linecap="round"/>'
    s += ''.join(atom(hx, hy, 18, 'H') for hx, hy in Hs) + atom(*O, 24, 'O')
    s += tex(66, 150, '수소', 19, fill=MUTED, mix=True) + tex(191, 150, '산소', 19, fill=MUTED, mix=True) + tex(360, 160, '물', 19, fill=MUTED, mix=True)
    s += '<g class="step" data-g="hm">'
    s += f'<ellipse cx="{O[0]}" cy="{O[1] + 4}" rx="42" ry="34" fill="{MINUS}" fill-opacity=".12" stroke="{MINUS}" stroke-width="1.5" stroke-dasharray="5 4"/>'
    s += tex(O[0] + 46, O[1] - 16, '\\delta^-', 22, fill=MINUS) + tex(Hs[0][0] - 28, Hs[0][1] + 6, '\\delta^+', 22, fill=PLUS) + tex(Hs[1][0] + 28, Hs[1][1] + 6, '\\delta^+', 22, fill=PLUS)
    s += tex(66, 118, '치우침 없음', 18, fill=MUTED, mix=True) + tex(191, 118, '치우침 없음', 18, fill=MUTED, mix=True) + '</g>'
    return s
F['h2o2_models'] = h2o2_models()


def ch4_ox():
    s = ''
    items = ((86, '\\overset{-4}{\\ce{C}}\\ce{H4(g)}'), (172, '+'), (252, '2\\overset{0}{\\ce{O}}{}_2\\ce{(g)}'), (350, '\\ce{->}'), (452, '\\overset{+4}{\\ce{C}}\\ce{O2(g)}'), (540, '+'), (628, '2\\ce{H2}\\overset{-2}{\\ce{O}}\\ce{(l)}'))
    for x, t in items:
        s += tex(x, 132, t, 34)
    s += bracket(52, 420, 82, 44, OX, 'C: −4 → +4 산화수 증가 (산화)', 34, step='c1')
    s += bracket(230, 652, 150, 182, RD, 'O: 0 → −2 산화수 감소 (환원)', 210, step='c2')
    return s
F['ch4_ox'] = ch4_ox()


def mg_s():
    s = atom(100, 90, 29, 'Mg') + atom(400, 90, 29, 'S')
    s += arw(134, 90, 366, 90, 'minus', 3)
    s += f'<g data-anim="move" data-from="-200,0" data-dur="1.3" data-delay=".4" data-ease="soft">{edot(340, 82)}{edot(326, 98)}</g>'
    s += tex(250, 72, '전자 2개 이동', 20, fill=MINUS, mix=True)
    s += tex(100, 160, '\\textbf{환원제}', 24, fill=OX) + tex(100, 192, '전자를 줌 · 산화됨', 19, fill=OX, mix=True)
    s += tex(400, 160, '\\textbf{산화제}', 24, fill=RD) + tex(400, 192, '전자를 받음 · 환원됨', 19, fill=RD, mix=True)
    return s
F['mg_s'] = mg_s()

D = os.path.dirname(os.path.abspath(__file__))
tpl = ''.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob(os.path.join(D, 'tpl*.html'))))
miss = set(re.findall(r'@@(\w+)@@', tpl)) - set(F)
if miss:
    raise SystemExit('없는 그림: ' + ', '.join(sorted(miss)))
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('slides.html', len(out), 'bytes,', out.count('<section'), 'slides')
