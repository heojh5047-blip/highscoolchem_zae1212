import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs411 import *

FIG = {}

# ───── S1 표지 ─────
def cover():
    s = 1.25
    o = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    # 위: 물 분자 두 개
    o.append(water(175, 140, 90, s))
    o.append(tex(270, 152, '+', size=34, fill=MUTED))
    o.append(water(365, 140, 90, s))
    # 가운데 ⇌ (세로 반쪽 화살표)
    o.append(f'<path d="M262,205 V262 L252,250" fill="none" stroke="{FIELD}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="M278,268 V211 L288,223" fill="none" stroke="{BF}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    # 아래: 이온
    o.append('<g data-anim="fade" data-dur=".9" data-delay=".2">')
    o.append(hydronium(170, 350, (125, 235, 0), s, True, anim_last='60,-30'))
    o.append(tex(170, 430, '\\ce{H3O+}', size=26, fill=PLUS, weight=700))
    o.append(hydroxide(375, 350, 230, s))
    o.append(tex(375, 430, '\\ce{OH-}', size=26, fill=MINUS, weight=700))
    o.append('</g>')
    o.append(tex(270, 492, mix='물 분자끼리 $\\ce{H+}$을 주고받는다', size=22, fill=MUTED))
    return ''.join(o)
FIG['cover'] = cover()

# ───── S2 단원 지도 ─────
def unitmap():
    o = []
    W = 1112
    xs = [150, 420, 692, 962]
    o.append(tex(285, 24, mix='1. 물의 자동 이온화와 pH', size=20, weight=700, fill=FIELD))
    o.append(f'<path d="M40 40 V33 H530 V40" fill="none" stroke="{FIELD}" stroke-width="2.5"/>')
    o.append(tex(827, 24, mix='2. 중화 반응', size=20, weight=700, fill=MUTED))
    o.append(f'<path d="M582 40 V33 H1072 V40" fill="none" stroke="#9FB0C2" stroke-width="2.5"/>')
    o.append(f'<line x1="30" y1="54" x2="1082" y2="54" stroke="#C9D3DD" stroke-width="6" stroke-linecap="round"/>')
    for i, x in enumerate(xs):
        if i == 0:
            o.append(f'<g data-anim="pop" data-o="{x},54" data-dur=".7" data-delay=".5" data-ease="back"><circle cx="{x}" cy="54" r="12" fill="{FIELD}"/></g>')
        else:
            col = FIELD if i == 1 else '#9FB0C2'
            o.append(f'<circle cx="{x}" cy="54" r="10" fill="#FFFFFF" stroke="{col}" stroke-width="4"/>')
    o.append(f'<rect x="{xs[0]+22}" y="42" width="58" height="25" rx="12.5" fill="#FFE45C"/>')
    o.append(tex(xs[0] + 51, 61, mix='오늘', size=18, weight=700))
    # 아이콘 0: 물 분자 쌍
    o.append(small_water(xs[0] - 22, 98, 90).replace(',12,O,-', ',14,O,-').replace(',8,H,-', ',9,H,-'))
    o.append(small_water(xs[0] + 22, 98, 90).replace(',12,O,-', ',14,O,-').replace(',8,H,-', ',9,H,-'))
    # 아이콘 1: pH 띠
    cols = ['#D7263D', '#E8792B', '#F2C230', '#9BD86F', '#2E9E6A', '#1F6FD1', '#7B4FC8']
    for k, c in enumerate(cols):
        o.append(f'<rect x="{xs[1]-56+k*16}" y="86" width="16" height="22" fill="{c}"/>')
    o.append(f'<rect x="{xs[1]-56}" y="86" width="112" height="22" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    # 아이콘 2: 비커 두 개
    o.append(beaker(xs[2] - 46, 116, 36, 36, 92, '#F9D7DC', '#F2A7B2'))
    o.append(beaker(xs[2] + 10, 116, 36, 36, 92, '#D6E4F7', '#9EBDE8'))
    # 아이콘 3: 뷰렛 + 삼각 플라스크
    x = xs[3]
    o.append(f'<rect x="{x-5}" y="72" width="10" height="30" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<path d="M{x-18},118 L{x-6},104 V100 H{x+6} V104 L{x+18},118 Z" fill="#F7D3E3" stroke="{GLASS}" stroke-width="2"/>')
    labels = [('물의 자동 이온화와 몰농도', '자동 이온화·$K_\\mathrm{w}$·몰농도'),
              ('pH', 'pH·pOH, 희석과 pH'),
              ('중화 반응의 양적 관계', '알짜 이온 반응식·$nMV=n\'M\'V\'$'),
              ('중화 적정', '식초 속 아세트산 함량')]
    for x, (a, b) in zip(xs, labels):
        o.append(tex(x, 148, mix=a, size=19, weight=700))
        o.append(tex(x, 174, mix=b, size=18, fill=MUTED))
    return ''.join(o)
FIG['unitmap'] = unitmap()

# ───── S4 중단원 도입 그림: 비커 속 물 ─────
def s4fig():
    o = [beaker(70, 250, 200, 190, 90, WATER, WATER_S, 0)]
    pts = rand_points(9, 95, 112, 245, 235, 40, 4)
    for i, (x, y) in enumerate(pts):
        o.append(small_water(x, y, (i * 47) % 360))
    o.append(tex(170, 40, mix='순수한 물속에 $\\ce{H3O+}$과 $\\ce{OH-}$이 있을까?', size=20, weight=700))
    return ''.join(o)
FIG['s4fig'] = s4fig()

# ───── S6 전기 전도성 회로 3개 ─────
def cond(kind):
    # kind: 'bulb_off' / 'meter' / 'bulb_on'
    parts = [["wire", [[125, 112], [125, 62], [60, 62], [60, 30], [87, 30]]],
             ["bat", [95, 30], {"dir": "h", "pos": "left", "signs": False}],
             ["wire", [[103, 30], [191 if kind != 'meter' else 189, 30]]]]
    if kind == 'meter':
        parts.append(["meter", [205, 30], "A", {"r": 16}])
        parts.append(["wire", [[221, 30], [240, 30], [240, 62], [175, 62], [175, 112]]])
    else:
        parts.append(["bulb", [205, 30], {"r": 14, "on": kind == 'bulb_on'}])
        parts.append(["wire", [[219, 30], [240, 30], [240, 62], [175, 62], [175, 112]]])
    import json
    js = json.dumps({"parts": parts, "stroke": 2.5, "labelSize": 20}, ensure_ascii=False)
    o = [f'<svg class="fig" viewBox="0 0 300 250" style="width:280px" data-circuit=\'{js}\' aria-label="{ {"bulb_off":"순수한 물에 전극을 담근 전구 회로 — 전구가 켜지지 않음","meter":"순수한 물에 전극을 담근 예민한 전류계 회로","bulb_on":"소금물에 전극을 담근 전구 회로 — 전구가 켜짐"}[kind] }">']
    col = WATER if kind != 'bulb_on' else '#E6EFF6'
    o.append(beaker(85, 220, 130, 110, 135, col, WATER_S))
    o.append(f'<rect x="120" y="112" width="10" height="88" fill="#B0B8C2" stroke="{INK}" stroke-width="1.5"/>')
    o.append(f'<rect x="170" y="112" width="10" height="88" fill="#B0B8C2" stroke="{INK}" stroke-width="1.5"/>')
    if kind == 'bulb_on':
        for x, y in rand_points(8, 95, 145, 205, 212, 22, 7, avoid=((125, 170, 14), (175, 170, 14))):
            o.append(f'<g data-chg="{f(x)},{f(y)},7,+"></g>' if int(x) % 2 else f'<g data-chg="{f(x)},{f(y)},7,-"></g>')
    if kind == 'meter':
        o.append(f'<g data-anim="rot" data-from="-35" data-o="205,40" data-dur="1.4" data-delay=".6" data-ease="damp"><line x1="205" y1="40" x2="196" y2="22" stroke="{PLUS}" stroke-width="2.4" stroke-linecap="round"/></g>')
    lab = {'bulb_off': '전구가 켜지지 않는다', 'meter': '바늘이 아주 조금 움직인다', 'bulb_on': '전구가 밝게 켜진다'}[kind]
    o.append(tex(150, 244, mix=lab, size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['cond_off'] = cond('bulb_off'); FIG['cond_meter'] = cond('meter'); FIG['cond_on'] = cond('bulb_on')

# ───── S8 자동 이온화 ─────
def autoion():
    o = ['<svg class="fig" viewBox="0 0 1000 240" style="width:1000px" aria-label="왼쪽 물 분자가 오른쪽 물 분자에서 수소 이온을 받아 하이드로늄 이온이 되고, 수소 이온을 내준 물 분자는 수산화 이온이 되는 과정">']
    # 왼쪽 물 A(받는 쪽), 오른쪽 물 B(주는 쪽)
    o.append(water(130, 100, 180))
    # B: H 하나는 A 쪽(아래 왼쪽 127.75°), 하나는 위 오른쪽
    o.append(water(310, 100, 180 - 52.25 + 52.25 + 0))
    o.append(tex(130, 196, '\\ce{H2O}', size=24))
    o.append(tex(310, 196, '\\ce{H2O}', size=24))
    o.append(tex(220, 110, '+', size=30, fill=MUTED))
    o.append(f'<g class="step" data-g="a1">{arw(290, 158, 165, 158, EQUI, 3)}{tex(228, 230, mix="$\\ce{H+}$ 이동", size=20, fill=EQUI, weight=700)}</g>')
    o.append(f'<g class="step" data-g="a2">')
    o.append(tex(470, 116, '\\ce{<=>}', size=44))
    o.append(hydronium(620, 100, (125, 235, 0), 1.0, True, anim_last='70,0'))
    o.append(tex(620, 196, '\\ce{H3O+}', size=24, fill=PLUS, weight=700))
    o.append(tex(620, 226, mix='하이드로늄 이온', size=19, fill=MUTED))
    o.append(tex(730, 110, '+', size=30, fill=MUTED))
    o.append(hydroxide(840, 100, 232.25))
    o.append(tex(840, 196, '\\ce{OH-}', size=24, fill=MINUS, weight=700))
    o.append(tex(840, 226, mix='수산화 이온', size=19, fill=MUTED))
    o.append('</g></svg>')
    return ''.join(o)
FIG['autoion'] = autoion()

# ───── S9 동적 평형 입자 상자 ─────
def eqbox():
    o = ['<svg class="fig" viewBox="0 0 560 300" style="width:560px" aria-label="물 분자들 사이에 하이드로늄 이온과 수산화 이온이 아주 드물게 있는 모습">']
    o.append(f'<rect x="10" y="10" width="540" height="250" rx="10" fill="#F4F9FD" stroke="{WATER_S}" stroke-width="2"/>')
    special = [(330, 120), (400, 170)]
    pts = rand_points(34, 32, 32, 528, 238, 40, 11, avoid=((330, 120, 44), (400, 170, 44)))
    for i, (x, y) in enumerate(pts):
        o.append(small_water(x, y, (i * 73) % 360))
    o.append('<g data-anim="fade" data-dur="1.1" data-delay=".6" data-rep="alt">')
    o.append(hydronium(330, 120, (125, 235, 0), 0.5, False, lab=False))
    o.append(f'<circle cx="330" cy="120" r="30" fill="none" stroke="{PLUS}" stroke-width="2.5"/>')
    o.append(hydroxide(400, 170, 230, 0.5, False, lab=False))
    o.append(f'<circle cx="400" cy="170" r="30" fill="none" stroke="{MINUS}" stroke-width="2.5"/>')
    o.append('</g>')
    o.append(tex(286, 86, '\\ce{H3O+}', size=21, fill=PLUS, weight=700, halo=True, anchor='end'))
    o.append(tex(438, 214, '\\ce{OH-}', size=21, fill=MINUS, weight=700, halo=True, anchor='start'))
    o.append(tex(280, 290, mix='물 분자 사이에 이온이 아주 드물게 있다 (크기·개수 비례 아님)', size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['eqbox'] = eqbox()

# ───── S13 Kw 막대그래프 ─────
def kwbars():
    o = ['<svg class="fig" viewBox="0 0 520 320" style="width:500px" aria-label="온도가 높을수록 물의 이온화 상수가 커지는 막대그래프">']
    x0, y0, sc = 80, 262, 20
    o.append(f'<line x1="{x0}" y1="{y0}" x2="500" y2="{y0}" stroke="{MUTED}" stroke-width="2"/>')
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="40" stroke="{MUTED}" stroke-width="2"/>')
    for v in (0, 2, 4, 6, 8, 10):
        y = y0 - v * sc
        o.append(f'<line x1="{x0-6}" y1="{y}" x2="{x0}" y2="{y}" stroke="{MUTED}" stroke-width="2"/>')
        o.append(tex(x0 - 12, y + 7, str(v), size=18, anchor='end', fill=MUTED))
    o.append(tex(x0 + 4, 26, mix='$K_\\mathrm{w}$ [$\\times10^{-14}$]', size=19, anchor='start', fill=MUTED))
    data = [(0, 0.11), (25, 1.0), (60, 9.5)]
    for i, (t, v) in enumerate(data):
        cx = 160 + i * 130
        h = v * sc
        o.append(f'<g data-anim="scale" data-from="1,0" data-o="{cx},{y0}" data-dur="1" data-delay="{.3+i*.25:.2f}" data-ease="out"><rect x="{cx-26}" y="{f(y0-h)}" width="52" height="{f(h)}" fill="{INK}" opacity=".78"/></g>')
        o.append(tex(cx, y0 - h - 8, '0.11' if v < 1 else ('1.0' if v == 1 else str(v)), size=19, weight=700))
        o.append(tex(cx, y0 + 26, str(t), size=19, fill=MUTED))
    o.append(tex(500, 312, mix='$t$ [°C]', size=19, anchor='end', fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['kwbars'] = kwbars()

# ───── S14 액성 세 칸 ─────
def ionbeaker(nH, nOH, seed):
    o = ['<svg viewBox="0 0 300 170" aria-hidden="true">']
    o.append(beaker(70, 160, 160, 140, 40, '#F4F9FD', WATER_S))
    pts = rand_points(nH + nOH, 90, 58, 210, 145, 27, seed)
    o.append('<g data-anim="pop" data-o="150,100" data-dur=".8" data-delay=".4" data-ease="back">')
    for i, (x, y) in enumerate(pts):
        o.append(f'<g data-chg="{f(x)},{f(y)},11,{"+" if i < nH else "-"}"></g>')
    o.append('</g></svg>')
    return ''.join(o)
FIG['ion_acid'] = ionbeaker(6, 1, 21); FIG['ion_neu'] = ionbeaker(3, 3, 22); FIG['ion_base'] = ionbeaker(1, 6, 23)

# ───── S15 단계 카드 막대 ─────
def twobars(hH, hO, note=None, anim=False, from_h=None, from_o=None):
    o = ['<svg viewBox="0 0 300 200" aria-hidden="true">']
    base = 160
    o.append(f'<line x1="40" y1="{base}" x2="260" y2="{base}" stroke="{MUTED}" stroke-width="2"/>')
    for cx, h, col, lab, fr in ((105, hH, PLUS, '[\\ce{H3O+}]', from_h), (195, hO, MINUS, '[\\ce{OH-}]', from_o)):
        r = f'<rect x="{cx-30}" y="{base-h}" width="60" height="{h}" fill="{col}" opacity=".85"/>'
        if fr:
            r = f'<g data-anim="scale" data-from="1,{fr}" data-o="{cx},{base}" data-dur="1.1" data-delay=".4" data-ease="out" data-on="step">{r}</g>'
        o.append(r)
        o.append(tex(cx, base + 26, lab, size=20, fill=col, weight=700))
    if note:
        o.append(tex(150, 24, mix=note, size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['bar1'] = twobars(60, 60, '같다')
FIG['bar2'] = twobars(130, 60, '$\\ce{H3O+}$ 늘어남', from_h='0.46')
FIG['bar3'] = twobars(124, 14, '$\\ce{OH-}$ 줄어듦', from_o='4.3')

# ───── S19 질량 백분율 같은 두 용액 ─────
def s19():
    o = ['<svg class="fig" viewBox="0 0 560 300" style="width:540px" aria-label="질량 백분율이 같은 설탕물과 소금물 속 용질의 양 막대 비교">']
    o.append(beaker(40, 150, 120, 110, 60, '#FBF6E8', '#E3D3A4'))
    o.append(beaker(220, 150, 120, 110, 60, WATER, WATER_S))
    o.append(tex(100, 182, mix='설탕물 10 %', size=20, weight=700))
    o.append(tex(280, 182, mix='소금물 10 %', size=20, weight=700))
    o.append(tex(100, 208, mix='100 g 속 설탕 10 g', size=19, fill=MUTED))
    o.append(tex(280, 208, mix='100 g 속 $\\ce{NaCl}$ 10 g', size=19, fill=MUTED))
    # 몰 막대 (가로)
    o.append('<g class="step" data-g="m1">')
    o.append(tex(380, 54, mix='용질의 양 [mol]', size=19, anchor='start', fill=MUTED))
    sc = 640
    for y, v, lab, col in ((90, 0.0292, '0.029', '#C9A54A'), (140, 0.171, '0.17', MUTED)):
        o.append(f'<g data-anim="scale" data-from="0,1" data-o="380,{y}" data-dur="1" data-delay=".2" data-ease="out" data-on="step"><rect x="380" y="{y-16}" width="{f(v*sc)}" height="32" fill="{col}" opacity=".85"/></g>')
        o.append(tex(380 + v * sc + 8, y + 7, lab, size=19, anchor='start', weight=700))
    o.append(tex(372, 97, mix='설탕', size=19, anchor='end'))
    o.append(tex(372, 147, mix='$\\ce{NaCl}$', size=19, anchor='end'))
    o.append(tex(470, 196, mix='약 6배', size=20, fill=PLUS, weight=700))
    o.append('</g>')
    o.append(tex(280, 262, mix='설탕 $\\ce{C12H22O11}$ 342 g/mol · $\\ce{NaCl}$ 58.5 g/mol', size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['s19'] = s19()

# ───── S20 몰농도 1 L 부피 플라스크 ─────
def s20():
    o = ['<svg class="fig" viewBox="0 0 400 330" style="width:380px" aria-label="1 L 부피 플라스크의 표시선까지 채운 용액 속 용질 입자">']
    fl, cy, mark, tp = flask(170, 300, 'clip-cm411-20', level=None, R=95, neck=34, s=1, mark=None, top=40)
    # level = mark
    d, cy, tp2, hw = flask_path(170, 300, 95, 34, 40)
    mark = cy - 125
    fl, cy, mark, tp = flask(170, 300, 'clip-cm411-20', level=mark, R=95, neck=34, mark=mark, top=40)
    o.append(fl)
    pts = rand_points(10, 105, cy - 50, 235, 285, 30, 5)
    o.append('<g data-anim="pop" data-o="170,230" data-dur=".9" data-delay=".4" data-ease="back">')
    for x, y in pts:
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="9" fill="{EQUI}" opacity=".85"/>')
    o.append('</g>')
    o.append(tex(206, f'{mark+6:.0f}' and mark + 6, mix='표시선', size=19, anchor='start', fill=INK))
    o.append(f'<g data-arw="300,{f(cy+10)},250,{f(cy+10)},muted,2"></g>')
    o.append(tex(306, cy + 4, mix='용질||1 mol', size=19, anchor='start', fill=MUTED))
    o.append(tex(170, 324, mix='용액 1 L', size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['s20'] = s20()

# ───── S23 물 1 L vs 부피 플라스크 ─────
def s23a():
    o = ['<svg class="fig" viewBox="0 0 300 260" style="width:280px" aria-label="물 1 L가 든 비커에 용질을 녹이면 액면이 1 L 눈금보다 조금 올라감">']
    o.append(beaker(70, 230, 160, 190, None))
    lvl1 = 100
    o.append(f'<g data-anim="scale" data-from="1,.95" data-o="150,230" data-dur="1.2" data-delay=".6" data-ease="out"><rect x="71.5" y="{lvl1-6}" width="157" height="{230-lvl1+6-1.5}" fill="{WATER}"/><line x1="71.5" y1="{lvl1-6}" x2="228.5" y2="{lvl1-6}" stroke="{WATER_S}" stroke-width="2"/></g>')
    o.append(f'<line x1="70" y1="{lvl1}" x2="96" y2="{lvl1}" stroke="{INK}" stroke-width="2"/>')
    o.append(tex(102, lvl1 + 22, mix='1 L 눈금', size=19, anchor='start'))
    for x, y in rand_points(8, 90, 120, 210, 220, 28, 8):
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="8" fill="{EQUI}" opacity=".85"/>')
    o.append(tex(150, 30, mix='물 1 L + 용질 0.1 mol', size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['s23a'] = s23a()

def s23b():
    o = ['<svg class="fig" viewBox="0 0 300 260" style="width:280px" aria-label="녹인 용액을 1 L 부피 플라스크에 옮기고 표시선까지 물을 채움">']
    d, cy, tp, hw = flask_path(150, 240, 80, 30, 34)
    mark = cy - 100
    fl, cy, mark, tp = flask(150, 240, 'clip-cm411-23', level=mark, R=80, neck=30, mark=mark, top=34)
    o.append(fl)
    for x, y in rand_points(8, 95, cy - 30, 205, 230, 26, 9):
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="8" fill="{EQUI}" opacity=".85"/>')
    o.append(tex(176, mark + 7, mix='표시선(1 L)', size=19, anchor='start'))
    o.append('</svg>')
    return ''.join(o)
FIG['s23b'] = s23b()

# ───── S24 희석 ─────
def s24():
    o = ['<svg class="fig" viewBox="0 0 640 280" style="width:620px" aria-label="20 mL 용액에 물을 넣어 100 mL로 묽혀도 용질 입자 수는 같음">']
    o.append(beaker(40, 230, 150, 170, 192, WATER, WATER_S, 4))
    o.append(beaker(430, 230, 150, 170, 72, WATER, WATER_S, 4))
    p1 = rand_points(10, 52, 198, 178, 224, 14, 3)
    p2 = rand_points(10, 445, 85, 565, 222, 34, 6)
    for (x, y) in p1:
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="6.5" fill="{EQUI}"/>')
    for (x1, y1), (x2, y2) in zip(p1, p2):
        o.append(f'<g data-anim="move" data-from="{f(x1+390-x2)},{f(y1-y2)}" data-dur="1.4" data-delay=".5" data-ease="out" data-on="g:d1"><circle cx="{f(x2)}" cy="{f(y2)}" r="6.5" fill="{EQUI}"/></g>')
    o.append(f'<g class="step" data-g="d1">{arw(222, 150, 400, 150, "ink", 3)}{tex(311, 136, mix="물을 넣는다", size=20)}</g>')
    o.append(tex(115, 262, mix='$0.50\\ \\text{M}$, $20\\ \\text{mL}$', size=20))
    o.append(tex(505, 262, mix='$M\'$, $100\\ \\text{mL}$', size=20))
    o.append(tex(311, 200, mix='용질의 양은 그대로', size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['s24'] = s24()

# ───── S26–27 탐구 과정 카드 그림 (300×200) ─────
def st1():
    o = ['<svg viewBox="0 0 300 200" aria-label="전자저울에 칭량 접시를 올리고 염화 나트륨을 덜어 1.46 g을 단다">']
    o.append(balance(75, 100, 150, '5.85\\ \\text{g}', read_anim='data-anim="fade" data-dur=".6" data-delay="1"'))
    # 약숟가락
    o.append(f'<g data-anim="rot" data-from="-18" data-o="230,60" data-dur="1" data-delay=".3" data-ease="out"><line x1="160" y1="88" x2="250" y2="44" stroke="{MUTED}" stroke-width="4" stroke-linecap="round"/><ellipse cx="160" cy="88" rx="12" ry="6" transform="rotate(-26 160 88)" fill="#C9D3DD" stroke="{MUTED}" stroke-width="2"/></g>')
    o.append(tex(70, 40, mix='$\\ce{NaCl}$이면', size=24, anchor='start', fill=MUTED))
    o.append('</svg>')
    return ''.join(o)

def st2():
    o = ['<svg viewBox="0 0 300 200" aria-label="비커의 증류수에 용질을 넣고 유리 막대로 저어 녹인다">']
    o.append(beaker(90, 185, 120, 120, 110, WATER, WATER_S, 2))
    for x, y in rand_points(6, 105, 125, 195, 178, 20, 2):
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="5" fill="{EQUI}" opacity=".7"/>')
    o.append(f'<g data-anim="rot" data-from="12" data-o="150,30" data-dur=".8" data-rep="alt" data-ease="sine"><line x1="150" y1="30" x2="170" y2="176" stroke="{GLASS}" stroke-width="6" stroke-linecap="round"/></g>')
    o.append(tex(245, 52, mix='약 50 mL', size=24, anchor='middle', fill=MUTED))
    o.append('</svg>')
    return ''.join(o)

def st3():
    o = ['<svg viewBox="0 0 300 200" aria-label="부피 플라스크에 깔때기를 꽂고 비커의 용액을 유리 막대를 따라 붓는다">']
    fl, cy, mark, tp = flask(200, 195, 'clip-cm411-26', level=170, R=48, neck=18, mark=None, top=70)
    o.append(fl)
    o.append(f'<path d="M176,46 L224,46 L205,72 L205,92 L195,92 L195,72 Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2.4" stroke-linejoin="round"/>')
    o.append(f'<g transform="rotate(-38 140 70)">{beaker(90, 110, 70, 60, 92, WATER, WATER_S)}</g>')
    o.append(f'<line x1="170" y1="22" x2="198" y2="86" stroke="{GLASS}" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<path d="M165,47 Q182,56 192,70" fill="none" stroke="{WATER_S}" stroke-width="4" stroke-linecap="round"/>')
    o.append(tex(60, 190, mix='깔때기', size=24, anchor='start', fill=MUTED))
    o.append(f'<line x1="122" y1="184" x2="180" y2="60" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    o.append('</svg>')
    return ''.join(o)

def st4():
    o = ['<svg viewBox="0 0 300 200" aria-label="씻기병으로 비커와 유리 막대를 헹군 물을 부피 플라스크에 넣는다">']
    o.append(beaker(40, 185, 90, 80, 172, WATER, WATER_S))
    # 씻기병
    o.append(f'<path d="M60,20 h40 v14 h-40 Z" fill="#E9EEF3" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<rect x="52" y="34" width="56" height="64" rx="10" fill="#EEF6FB" stroke="{GLASS}" stroke-width="2.4"/>')
    o.append(f'<path d="M80,20 V8 H112 L124,24" fill="none" stroke="{GLASS}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<path d="M124,26 Q120,70 96,118" fill="none" stroke="{WATER_S}" stroke-width="3" stroke-dasharray="6 4"/>')
    fl, cy, mark, tp = flask(222, 195, 'clip-cm411-27a', level=150, R=48, neck=18, mark=None, top=70)
    o.append(fl)
    o.append(arw(140, 150, 172, 150, 'muted', 2.5))
    o.append(tex(160, 190, mix='2–3번', size=24, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)

def st5():
    o = ['<svg viewBox="0 0 300 200" aria-label="눈높이를 표시선에 맞추고 스포이트로 물을 한 방울씩 넣어 메니스커스 아랫부분을 표시선에 맞춘다">']
    # 확대한 목
    o.append(f'<rect x="120" y="20" width="60" height="180" fill="none"/>')
    o.append(f'<g clip-path="url(#clip-cm411-27b)"><g data-anim="scale" data-from="1,.86" data-o="150,200" data-dur="1.2" data-delay=".4" data-ease="out"><path d="M122,112 Q150,124 178,112 V200 H122 Z" fill="{WATER}"/><path d="M122,112 Q150,124 178,112" fill="none" stroke="{WATER_S}" stroke-width="2.5"/></g></g>')
    o.append(f'<defs><clipPath id="clip-cm411-27b"><rect x="122" y="20" width="56" height="180"/></clipPath></defs>')
    o.append(f'<line x1="122" y1="20" x2="122" y2="198" stroke="{GLASS}" stroke-width="2.6"/><line x1="178" y1="20" x2="178" y2="198" stroke="{GLASS}" stroke-width="2.6"/>')
    o.append(f'<line x1="114" y1="118" x2="186" y2="118" stroke="{INK}" stroke-width="2"/>')
    o.append(tex(192, 124, mix='표시선', size=19, anchor='start'))
    # 눈
    o.append(f'<path d="M30,118 Q48,104 66,118 Q48,132 30,118 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/><circle cx="54" cy="118" r="5" fill="{INK}"/>')
    o.append(f'<line x1="70" y1="118" x2="112" y2="118" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
    o.append(tex(48, 156, mix='눈높이', size=19, fill=MUTED))
    # 스포이트
    o.append(f'<rect x="143" y="2" width="14" height="40" rx="3" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/><ellipse cx="150" cy="0" rx="10" ry="8" fill="#C9D3DD" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<circle cx="150" cy="56" r="3.5" fill="{WATER_S}"/>')
    o.append(tex(196, 40, mix='스포이트', size=19, anchor='start', fill=MUTED))
    o.append('</svg>')
    return ''.join(o)

def st6(cid='clip-cm411-27c'):
    o = ['<svg viewBox="0 0 300 200" aria-label="마개를 닫은 부피 플라스크를 거꾸로 뒤집어 흔든다">']
    fl, cy, mark, tp = flask(150, 175, cid, level=62, R=50, neck=18, mark=None, top=40, stopper=True)
    o.append(f'<g data-anim="rot" data-from="40" data-o="150,110" data-dur=".9" data-rep="swing" data-ease="sine">{fl}</g>')
    o.append(f'<path d="M66,60 A90,90 0 0 1 112,22" fill="none" stroke="{MUTED}" stroke-width="2.5"/>' + arw(100, 28, 114, 21, 'muted', 2.5))
    o.append(f'<path d="M234,60 A90,90 0 0 0 188,22" fill="none" stroke="{MUTED}" stroke-width="2.5"/>' + arw(200, 28, 186, 21, 'muted', 2.5))
    o.append(tex(150, 196, mix='마개를 닫고 뒤집기', size=19, fill=MUTED))
    o.append('</svg>')
    return ''.join(o)
FIG['st1'] = st1(); FIG['st2'] = st2(); FIG['st3'] = st3(); FIG['st4'] = st4(); FIG['st5'] = st5(); FIG['st6a'] = st6('clip-cm411-28a'); FIG['st6b'] = st6('clip-cm411-28b')

# ───── S34 순서 문항 그림 (작게) ─────
def q4fig():
    o = ['<svg class="fig" viewBox="0 0 1100 230" style="width:1100px" aria-label="(가) 표시선까지 물 채우기, (나) 비커에서 녹이기, (다) 부피 플라스크로 옮기기, (라) 질량 달기">']
    def card(x, inner, lab):
        return f'<g transform="translate({x},0)">{inner}</g>' + tex(x + 135, 222, mix=lab, size=20, weight=700)
    import re as _re
    def strip(svg, nid):
        body = _re.sub(r'^<svg[^>]*>|</svg>$', '', svg)
        body = _re.sub(r'data-anim="[^"]*"( data-[a-z]+="[^"]*")*', '', body)
        return body.replace('clip-cm411-26', nid + 'a').replace('clip-cm411-27b', nid + 'b').replace('clip-cm411-27a', nid + 'c')
    o.append(card(0, strip(st5(), 'clip-cm411-34p'), '(가)'))
    o.append(card(280, strip(st2(), 'clip-cm411-34q'), '(나)'))
    o.append(card(560, strip(st3(), 'clip-cm411-34r'), '(다)'))
    o.append(card(840, strip(st1(), 'clip-cm411-34s'), '(라)'))
    o.append('</svg>')
    return ''.join(o)



# ───── 비커·눈금실린더·부피 플라스크 ─────
def glass3(labs, cid):
    o = [f'<svg class="fig" viewBox="0 0 440 250" style="width:440px" aria-label="{labs[0]} 비커, {labs[1]} 눈금실린더, {labs[2]} 부피 플라스크">']
    o.append(beaker(30, 200, 100, 90, 160, WATER, WATER_S, 3))
    # 눈금실린더
    o.append(f'<rect x="201" y="100" width="38" height="96" fill="{WATER}"/><line x1="201" y1="100" x2="239" y2="100" stroke="{WATER_S}" stroke-width="2"/>')
    o.append(f'<path d="M198,24 V198 H242 V24" fill="none" stroke="{GLASS}" stroke-width="2.6"/><path d="M186,198 H254 V206 H186 Z" fill="#E9EEF3" stroke="{GLASS}" stroke-width="2"/>')
    for k in range(9):
        y = 40 + k * 18
        o.append(f'<line x1="198" y1="{y}" x2="{212 if k % 2 else 218}" y2="{y}" stroke="{MUTED}" stroke-width="1.5"/>')
    fl, cy, mark, tp = flask(360, 206, cid, level=None, R=52, neck=18, mark=None, top=24, stopper=True)
    d, cy, tp, hw = flask_path(360, 206, 52, 18, 24)
    mark = cy - 92
    fl, cy, mark, tp = flask(360, 206, cid, level=mark, R=52, neck=18, mark=mark, top=24, stopper=True)
    o.append(fl)
    for (x, y), l in zip(((40, 92), (176, 44), (306, 44)), labs):
        o.append(tex(x, y, mix=l, size=22, weight=700, anchor='middle'))
    o.append('</svg>')
    return ''.join(o)
FIG['glass3a'] = glass3(('㉠', '㉡', '㉢'), 'clip-cm411-26g')
FIG['glass3b'] = glass3(('ㄱ.', 'ㄴ.', 'ㄷ.'), 'clip-cm411-35')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    def rep(m):
        return FIG[m.group(1)]
    out = re.sub(r'@@(\w+)@@', rep, tpl)
    dst = sys.argv[1]
    open(dst, 'w', encoding='utf-8').write(out)
    print('wrote', dst, len(out))
