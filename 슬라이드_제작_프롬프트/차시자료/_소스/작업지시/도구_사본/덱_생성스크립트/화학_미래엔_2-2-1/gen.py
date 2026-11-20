# tpl*.html 의 @@이름@@ 자리에 계산한 그림 SVG를 넣어 slides.html을 만든다.
import math, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lw import *

F = {}

# ── S1 표지: H:O:H ──
def cover():
    S = 64; cx, cy = 270, 262
    m = Mol({'h1': ('H', cx - 1.4 * S, cy), 'o': ('O', cx, cy), 'h2': ('H', cx + 1.4 * S, cy)},
            [('h1', 'o', 1), ('o', 'h2', 1)], {'o': {'u': 2, 'd': 2}}, S)
    out = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    for i, (el, x, y) in m.a.items():
        out += sym(x, y, el, S)
    k = 0
    for a, b, o in m.b:
        x, y, ori = m.bpos(a, b)
        out += f'<g data-anim="pop" data-o="{f(x)},{f(y)}" data-dur=".6" data-delay="{.3 + .35 * k:.2f}" data-ease="back">' + box(x, y, .55 * S, .85 * S, 'shared') + shared_dots(x, y, ori, 1, S) + '</g>'; k += 1
    for s in ('u', 'd'):
        px, py = side_pos(cx, cy, s, S, 'O')
        out += f'<g data-anim="pop" data-o="{f(px)},{f(py)}" data-dur=".6" data-delay="{.3 + .35 * k:.2f}" data-ease="back">' + box(px, py, .85 * S, .55 * S, 'lone') + dots(px, py, 'h', 2, S) + '</g>'; k += 1
    out += tex(cx - 0.7 * S, cy + 118, '공유 전자쌍', 24, extra=f' fill="{FIELD}" data-weight="700"')
    out += f'<line x1="{f(cx - .7 * S)}" y1="{f(cy + 92)}" x2="{f(cx - .7 * S)}" y2="{f(cy + 30)}" stroke="{FIELD}" stroke-width="2"/>'
    out += tex(cx + 120, cy - 100, '비공유 전자쌍', 24, extra=f' fill="#9A5A12" data-weight="700"')
    out += f'<line x1="{f(cx + 72)}" y1="{f(cy - 92)}" x2="{f(cx + 30)}" y2="{f(cy - .75 * S - 6)}" stroke="{EQUI}" stroke-width="2"/>'
    return out
F['cover'] = cover()

# ── S2 블록 ──
def blocks():
    def brick(x, y, w, col, st):
        s = f'<rect x="{x}" y="{y}" width="{w}" height="44" rx="6" fill="{col}" stroke="{st}" stroke-width="2"/>'
        for i in range(w // 40):
            s += f'<rect x="{x + 10 + 40 * i}" y="{y - 12}" width="22" height="14" rx="4" fill="{col}" stroke="{st}" stroke-width="2"/>'
        return s
    return (brick(40, 112, 160, '#9FC3DD', '#5E8FB5') + f'<g data-anim="move" data-from="0,-40" data-dur="1" data-delay=".4" data-ease="bounce">' + brick(80, 68, 120, '#F6C177', '#C98B2E') + '</g>'
            + brick(220, 112, 80, '#B9E3C6', '#4F9A6B'))
F['blocks'] = blocks()

# ── S4 이모티콘 ──
def face(cx, cy, happy, d):
    s = f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".7" data-delay="{d}" data-ease="back"><circle cx="{cx}" cy="{cy}" r="56" fill="#FFD84D" stroke="#C99A1E" stroke-width="3"/>'
    if happy:
        s += f'<path d="M{cx - 30} {cy - 12} q10 -14 20 0 M{cx + 10} {cy - 12} q10 -14 20 0" fill="none" stroke="#16233D" stroke-width="4" stroke-linecap="round"/>'
        s += f'<path d="M{cx - 30} {cy + 10} q30 34 60 0 Z" fill="#16233D"/>'
    else:
        s += f'<circle cx="{cx - 20}" cy="{cy - 12}" r="6" fill="#16233D"/><circle cx="{cx + 20}" cy="{cy - 12}" r="6" fill="#16233D"/>'
        s += f'<path d="M{cx - 24} {cy + 28} q24 -24 48 0" fill="none" stroke="#16233D" stroke-width="4" stroke-linecap="round"/>'
        s += f'<path d="M{cx + 24} {cy - 2} q-6 14 0 18 q6 -4 0 -18 Z" fill="#6FB3E8"/>'
    return s + '</g>'
F['faces'] = (face(80, 80, False, .3) + face(250, 80, True, .7) + tex(80, 172, '슬퍼.', 21) + tex(250, 172, '행복해.', 21))

# ── S5 CO2 보어 모형 ──
def co2_bohr():
    out = ''; R = (28, 56); y = 100; xs = (90, 180, 270)
    for x in xs:
        for r in R:
            out += f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{MUTED}" stroke-width="1.5"/>'
    for x, Z in zip(xs, (8, 6, 8)):
        out += f'<circle cx="{x}" cy="{y}" r="15" fill="{PLUS}"/>' + tex(x, y + 6, f'{Z}+', 17, extra=' fill="#FFFFFF" data-weight="700"')
        for a in (45, 225):
            t = math.radians(a); out += f'<circle cx="{f(x + 28 * math.cos(t))}" cy="{f(y - 28 * math.sin(t))}" r="5.5" fill="{GRAV}"/>'
    # 겹친 곳 공유 전자: 두 원 위, y = ±12
    sh = ''
    for xl, xr in ((90, 180), (180, 270)):
        for yy in (-12, 12):
            dx = math.sqrt(56 ** 2 - yy ** 2)
            sh += f'<circle cx="{f(xl + dx)}" cy="{f(y + yy)}" r="5.5" fill="{MINUS}"/><circle cx="{f(xr - dx)}" cy="{f(y + yy)}" r="5.5" fill="{MINUS}"/>'
    out += f'<g data-anim="fade" data-dur=".9" data-delay=".5">' + sh + '</g>'
    # 산소의 공유하지 않은 바깥 전자 4개
    for x, base in ((90, 180), (270, 0)):
        for a in (base - 52, base - 24, base + 24, base + 52):
            t = math.radians(a); out += f'<circle cx="{f(x + 56 * math.cos(t))}" cy="{f(y - 56 * math.sin(t))}" r="5.5" fill="{MINUS}"/>'
    for x, el in zip(xs, 'OCO'):
        out += tex(x, 186, f'\\mathrm{{{el}}}', 22, mix=False)
    # 안쪽 전자 꼬리표
    out += f'<line x1="{f(270 + 19.8)}" y1="{f(100 - 19.8)}" x2="332" y2="26" stroke="{MUTED}" stroke-width="1.5"/>' + tex(334, 22, '안쪽 전자 껍질의 전자', 18, 'end', extra=f' fill="{MUTED}"')
    return out
F['co2_bohr'] = co2_bohr()

# ── S6 산소: 보어 모형 → 루이스 전자점식 (점 순서 pop) ──
def o_atom():
    out = bohr(80, 95, 8, [2, 6], outer=lewis_angles(6))
    out += arrow_r(160, 214, 95)
    S = 56; x, y = 300, 95
    out += sym(x, y, 'O', S)
    seq = ORDER[:6]; cnt = {}
    final = atom_sides(6)
    for k, s in enumerate(seq):
        cnt[s] = cnt.get(s, 0) + 1
        px, py = side_pos(x, y, s, S, 'O')
        o = 0.18 * S
        if final[s] == 2:
            if cnt[s] == 1:
                px, py = (px - o, py) if s in 'ud' else (px, py - o)
            else:
                px, py = (px + o, py) if s in 'ud' else (px, py + o)
        out += f'<g data-anim="pop" data-o="{f(px)},{f(py)}" data-dur=".4" data-delay="{.4 + .35 * k:.2f}" data-ease="back"><circle cx="{f(px)}" cy="{f(py)}" r="{f(.1 * S)}" fill="{INK}"/></g>'
        # 번호
        nx = px + {'r': 16, 'l': -16, 'u': 0, 'd': 0}[s]; ny = py + {'u': -12, 'd': 26, 'l': 6, 'r': 6}[s]
        if s in 'ud':
            nx = px + (-10 if cnt[s] == 1 else 10) * (1 if final[s] == 2 else 0)
        if s in 'lr' and final[s] == 2:
            ny = py + 6 + (-8 if cnt[s] == 1 else 8); nx = px + (-20 if s == 'l' else 20)
        out += tex(nx, ny, f'\\mathrm{{{k + 1}}}', 18, mix=False, extra=f' fill="{MUTED}"')
    return out
F['o_atom'] = o_atom()

# ── S7 1–3주기 표 ──
def ptable():
    els = [['H', None, None, None, None, None, None, 'He'], ['Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'], ['Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar']]
    Z = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18}
    grp = ['1', '2', '13', '14', '15', '16', '17', '18']
    X0, Y0, W, H = 70, 40, 120, 80; S = 30
    out = ''
    for j, gname in enumerate(grp):
        out += f'<rect x="{X0 + j * W + 3}" y="6" width="{W - 6}" height="28" rx="5" fill="#E3EEFB"/>' + tex(X0 + j * W + W / 2, 27, f'\\mathrm{{{gname}}}', 18, mix=False)
    out += tex(30, 27, '족', 17, extra=f' fill="{MUTED}"')
    for i, row in enumerate(els):
        y = Y0 + i * H
        out += f'<rect x="8" y="{y + 3}" width="{X0 - 16}" height="{H - 6}" rx="5" fill="#E3EEFB"/>' + tex(35, y + H / 2 + 7, f'\\mathrm{{{i + 1}}}', 18, mix=False)
        cells = ''
        for j, el in enumerate(row):
            if not el:
                continue
            x = X0 + j * W
            blank = el in ('N', 'Cl')
            cx, cy = x + W / 2, y + H / 2
            if blank:
                cells += f'<rect x="{x + 3}" y="{y + 3}" width="{W - 6}" height="{H - 6}" rx="6" fill="#FFFFFF" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="6 4"/>'
                cells += sym(cx, cy, el, S)
                n = Z[el] - (2 if Z[el] <= 10 else 10)
                sides = {'u': 2, 'l': 1, 'r': 1, 'd': 1} if el == 'N' else atom_sides(n)
                cells += f'<g class="step" data-g="n1" data-ask>' + side_dots(cx, cy, el, sides, S) + '</g>'
            else:
                cells += f'<rect x="{x + 3}" y="{y + 3}" width="{W - 6}" height="{H - 6}" rx="6" fill="#FFF3C4"/>'
                n = Z[el] if Z[el] <= 2 else (Z[el] - 2 if Z[el] <= 10 else Z[el] - 10)
                cells += sym(cx, cy, el, S) + side_dots(cx, cy, el, atom_sides(n, el), S)
        out += f'<g data-anim="fade" data-dur=".6" data-delay="{.2 + .3 * i:.1f}">' + cells + '</g>'
    return out
F['ptable'] = ptable()

# ── S9 HF 형성 ──
def hf_form():
    S = 44; y = 120; out = ''
    out += sym(70, y, 'H', S) + side_dots(70, y, 'H', {'r': 1}, S)
    out += tex(140, y + 12, '+', 36, extra=f' fill="{GRAV}"')
    out += sym(230, y, 'F', S) + side_dots(230, y, 'F', {'u': 2, 'l': 1, 'r': 2, 'd': 2}, S)
    out += arrow_r(300, 370, y)
    hx = 470; fx = hx + 1.4 * S
    m = Mol({'h': ('H', hx, y), 'f': ('F', fx, y)}, [('h', 'f', 1)], {'f': {'u': 2, 'r': 2, 'd': 2}}, S)
    out += '<g data-anim="move" data-from="-26,0" data-dur="1" data-delay=".3" data-ease="out">' + sym(hx, y, 'H', S) + '</g>'
    out += '<g data-anim="move" data-from="26,0" data-dur="1" data-delay=".3" data-ease="out">' + sym(fx, y, 'F', S) + side_dots(fx, y, 'F', {'u': 2, 'r': 2, 'd': 2}, S) + '</g>'
    px = hx + .7 * S
    out += shared_dots(px, y, 'v', 1, S)
    out += m.boxes('g1', 'g2', 'shared') + m.boxes('g1', 'g2', 'lone')
    out += f'<g class="step" data-g="g1"><line x1="{f(px)}" y1="{f(y - 20)}" x2="{f(px)}" y2="{f(y - 62)}" stroke="{FIELD}" stroke-width="2"/>' + tex(px - 6, y - 70, '공유 전자쌍', 20, 'end', extra=f' fill="{FIELD}" data-weight="700"') + '</g>'
    out += f'<g class="step" data-g="g2"><line x1="{f(fx + 10)}" y1="{f(y - .75 * S - 10)}" x2="{f(fx + 40)}" y2="{f(y - 66)}" stroke="{EQUI}" stroke-width="2"/>' + tex(fx + 44, y - 70, '비공유 전자쌍', 20, 'start', extra=' fill="#9A5A12" data-weight="700"') + '</g>'
    # He·Ne 전자 배치 테
    hb = f'<rect x="{f(hx - .55 * S)}" y="{f(y - .62 * S)}" width="{f(.55 * S + .7 * S + .32 * S)}" height="{f(1.24 * S)}" rx="8" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 4"/>'
    nb = f'<rect x="{f(px - .36 * S)}" y="{f(y - 1.1 * S)}" width="{f(.36 * S + 1.4 * S - .7 * S + .7 * S + .36 * S)}" height="{f(2.2 * S)}" rx="10" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="2 4" stroke-linecap="round"/>'
    out += f'<g class="step" data-g="g3">' + hb + nb + f'<line x1="{f(hx)}" y1="{f(y + .62 * S)}" x2="{f(hx - 30)}" y2="{f(y + 82)}" stroke="{MUTED}" stroke-width="1.5"/>' + tex(hx - 34, y + 100, '$\\mathrm{He}$의 전자 배치와 같다 (2개)', 19, 'end') + f'<line x1="{f(fx + 30)}" y1="{f(y + 1.1 * S)}" x2="{f(fx + 50)}" y2="{f(y + 82)}" stroke="{MUTED}" stroke-width="1.5"/>' + tex(fx + 20, y + 100, '$\\mathrm{Ne}$의 전자 배치와 같다 (8개)', 19, 'start') + '</g>'
    return out
F['hf_form'] = hf_form()

# ── S10 HF 루이스 구조 ──
def hf_struct():
    S = 44; y = 70; out = ''
    m = Mol({'h': ('H', 60, y), 'f': ('F', 60 + 1.4 * S, y)}, [('h', 'f', 1)], {'f': {'u': 2, 'r': 2, 'd': 2}}, S)
    out += m.svg_dots() + arrow_r(190, 250, y)
    m2 = Mol({'h': ('H', 320, y), 'f': ('F', 320 + 2.1 * S, y)}, [('h', 'f', 1)], {'f': {'u': 2, 'r': 2, 'd': 2}}, S)
    out += '<g data-anim="draw" data-dur=".8" data-delay=".4">' + bondline(m2.a['h'], m2.a['f'], 1, S) + '</g>' + ''.join(sym(x, yy, el, S) for el, x, yy in m2.a.values()) + side_dots(m2.a['f'][1], y, 'F', {'u': 2, 'r': 2, 'd': 2}, S)
    mx = (320 + 320 + 2.1 * S) / 2
    out += f'<line x1="{f(mx)}" y1="{f(y - 6)}" x2="{f(mx)}" y2="{f(y - 40)}" stroke="{MUTED}" stroke-width="1.5"/>' + tex(mx, y - 46, '결합선', 19, extra=f' fill="{MUTED}"')
    out += tex(370, 150, '비공유 전자쌍을 나타냄', 18, extra=f' fill="{MUTED}"')
    m3 = Mol({'h': ('H', 560, y), 'f': ('F', 560 + 2.1 * S, y)}, [('h', 'f', 1)], {}, S)
    out += m3.svg_lines() + tex(608, 150, '비공유 전자쌍을 생략', 18, extra=f' fill="{MUTED}"')
    return out
F['hf_struct'] = hf_struct()

# ── S11 O2, N2 ──
def o2n2():
    S = 42; out = ''
    for row, (el, order, lone1, lone2, y) in enumerate((('O', 2, {'l': 2, 'u': 2}, {'r': 2, 'u': 2}, 62), ('N', 3, {'l': 2}, {'r': 2}, 182))):
        x1 = 150; d = 1.6 * S
        m = Mol({'a': (el, x1, y), 'b': (el, x1 + d, y)}, [('a', 'b', order)], {'a': lone1, 'b': lone2}, S)
        out += m.svg_dots() + m.boxes(f'b{row}', f'b{row}', 'shared')
        out += arrow_r(300, 360, y)
        m2 = Mol({'a': (el, 450, y), 'b': (el, 450 + 2.2 * S, y)}, [('a', 'b', order)], {'a': lone1, 'b': lone2}, S)
        out += f'<g data-anim="draw" data-dur=".8" data-delay="{.4 + .5 * row}">' + bondline(m2.a['a'], m2.a['b'], order, S) + '</g>' + ''.join(sym(x, yy, e, S) + side_dots(x, yy, e, m2.lone[i], S) for i, (e, x, yy) in m2.a.items())
        name = '산소 $\\ce{O2}$' if el == 'O' else '질소 $\\ce{N2}$'
        out += tex(20, y + 8, name, 21, 'start', extra=' data-weight="700"')
        out += tex(760, y + 8, '이중 결합' if order == 2 else '삼중 결합', 21, 'start', extra=f' fill="{FIELD}" data-weight="700"')
    return out
F['o2n2'] = o2n2()

# ── S12 PCl3 ──
def pcl3(stage):
    S = 28; cx, cy = 150, 92; out = ''
    if stage == 1:
        d = 2.5 * S
        out += sym(cx, cy, 'P', S) + side_dots(cx, cy, 'P', {'u': 2, 'l': 1, 'r': 1, 'd': 1}, S)
        out += sym(cx - d - 10, cy, 'Cl', S) + side_dots(cx - d - 10, cy, 'Cl', {'u': 2, 'l': 2, 'd': 2, 'r': 1}, S)
        out += sym(cx + d + 10, cy, 'Cl', S) + side_dots(cx + d + 10, cy, 'Cl', {'u': 2, 'r': 2, 'd': 2, 'l': 1}, S)
        out += sym(cx, cy + 2.6 * S, 'Cl', S) + side_dots(cx, cy + 2.6 * S, 'Cl', {'l': 2, 'r': 2, 'd': 2, 'u': 1}, S)
        return out
    if stage == 2:
        dx = (sx('P') + sx('Cl')) * S
        m = Mol({'p': ('P', cx, cy), 'c1': ('Cl', cx - dx, cy), 'c2': ('Cl', cx + dx, cy), 'c3': ('Cl', cx, cy + 1.5 * S)},
                [('c1', 'p', 1), ('p', 'c2', 1), ('p', 'c3', 1)], {'p': {'u': 2}, 'c1': {'u': 2, 'l': 2, 'd': 2}, 'c2': {'u': 2, 'r': 2, 'd': 2}, 'c3': {'l': 2, 'r': 2, 'd': 2}}, S)
        return m.svg_dots()
    dx = 2.4 * S
    m = Mol({'p': ('P', cx, cy), 'c1': ('Cl', cx - dx, cy), 'c2': ('Cl', cx + dx, cy), 'c3': ('Cl', cx, cy + 2.1 * S)},
            [('c1', 'p', 1), ('p', 'c2', 1), ('p', 'c3', 1)], {'p': {'u': 2}, 'c1': {'u': 2, 'l': 2, 'd': 2}, 'c2': {'u': 2, 'r': 2, 'd': 2}, 'c3': {'l': 2, 'r': 2, 'd': 2}}, S)
    return m.svg_lines()
for k in (1, 2, 3):
    F[f'pcl3_{k}'] = pcl3(k)
F['pcl3_2'] = '<g data-anim="pop" data-o="150,110" data-dur=".7" data-on="step" data-ease="back">' + F['pcl3_2'] + '</g>'

# ── S13–S14 해 보기 ──
def tbl(name, lines):
    S = 28; cx, cy = 110, 72
    if name == 'CH4':
        d = (1.4 if not lines else 2.0) * S; v = (1.5 if not lines else 1.85) * S
        m = Mol({'c': ('C', cx, cy), 'a': ('H', cx - d, cy), 'b': ('H', cx + d, cy), 'u': ('H', cx, cy - v), 'd': ('H', cx, cy + v)},
                [('a', 'c', 1), ('c', 'b', 1), ('u', 'c', 1), ('c', 'd', 1)], {}, S)
    elif name == 'NH3':
        d = (1.4 if not lines else 2.0) * S; v = (1.5 if not lines else 1.85) * S
        m = Mol({'c': ('N', cx, cy - 8), 'a': ('H', cx - d, cy - 8), 'b': ('H', cx + d, cy - 8), 'd': ('H', cx, cy - 8 + v)},
                [('a', 'c', 1), ('c', 'b', 1), ('c', 'd', 1)], {'c': {'u': 2}}, S)
    elif name == 'H2O':
        d = (1.4 if not lines else 2.0) * S; v = (1.5 if not lines else 1.85) * S
        m = Mol({'c': ('O', cx + 10, cy - 8), 'a': ('H', cx + 10 - d, cy - 8), 'd': ('H', cx + 10, cy - 8 + v)},
                [('a', 'c', 1), ('c', 'd', 1)], {'c': {'u': 2, 'r': 2}}, S)
    else:
        d = (1.6 if not lines else 2.3) * S
        m = Mol({'c': ('C', cx, cy), 'a': ('O', cx - d, cy), 'b': ('O', cx + d, cy)},
                [('a', 'c', 2), ('c', 'b', 2)], {'a': {'u': 2, 'd': 2}, 'b': {'u': 2, 'd': 2}}, S)
    return m.svg_lines() if lines else m.svg_dots()
for n in ('CH4', 'NH3', 'H2O', 'CO2'):
    F[f'd_{n}'] = tbl(n, False); F[f'l_{n}'] = tbl(n, True)

# ── S15 HCl, CCl4 ──
def hcl():
    S = 36; m = Mol({'h': ('H', 60, 60), 'c': ('Cl', 60 + (0.7 + 0.95) * S, 60)}, [('h', 'c', 1)], {'c': {'u': 2, 'r': 2, 'd': 2}}, S)
    return m.svg_dots() + m.boxes(None, None)
def ccl4():
    S = 34; cx, cy = 130, 100; dx = (0.7 + 0.95) * S; v = 1.55 * S
    m = Mol({'c': ('C', cx, cy), 'a': ('Cl', cx - dx, cy), 'b': ('Cl', cx + dx, cy), 'u': ('Cl', cx, cy - v), 'd': ('Cl', cx, cy + v)},
            [('a', 'c', 1), ('c', 'b', 1), ('u', 'c', 1), ('c', 'd', 1)],
            {'a': {'u': 2, 'l': 2, 'd': 2}, 'b': {'u': 2, 'r': 2, 'd': 2}, 'u': {'l': 2, 'u': 2, 'r': 2}, 'd': {'l': 2, 'd': 2, 'r': 2}}, S)
    return m.svg_dots() + m.boxes(None, None)
F['hcl'] = hcl(); F['ccl4'] = ccl4()

# ── S16 BCl3 + NH3 ──
def bcl3_nh3():
    S = 34; bx, by = 230, 222; dx = (0.7 + 0.95) * S
    b = Mol({'b': ('B', bx, by), 'c1': ('Cl', bx - dx, by), 'c2': ('Cl', bx + dx, by), 'c3': ('Cl', bx, by + 1.55 * S)},
            [('c1', 'b', 1), ('b', 'c2', 1), ('b', 'c3', 1)], {'c1': {'u': 2, 'l': 2, 'd': 2}, 'c2': {'u': 2, 'r': 2, 'd': 2}, 'c3': {'l': 2, 'r': 2, 'd': 2}}, S)
    out = '<g class="step" data-g="k1">' + b.svg_dots() + b.boxes(None, None, 'shared')
    px, py = side_pos(bx, by, 'u', S, 'B')
    out += f'<rect x="{f(px - .45 * S)}" y="{f(py - .3 * S)}" width="{f(.9 * S)}" height="{f(.6 * S)}" rx="6" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 4"/>'
    out += tex(px + 16, py - 24, '빈자리', 19, 'start', extra=f' fill="{MUTED}"') + '</g>'
    nx, ny = bx, 92; d = 1.4 * S
    n = Mol({'n': ('N', nx, ny), 'a': ('H', nx - d, ny), 'b': ('H', nx + d, ny), 'u': ('H', nx, ny - 1.5 * S)},
            [('a', 'n', 1), ('n', 'b', 1), ('u', 'n', 1)], {'n': {'d': 2}}, S)
    out += '<g class="step" data-g="k2"><g data-anim="move" data-from="0,-26" data-dur="1.1" data-on="step" data-ease="out">' + n.svg_dots() + n.boxes('k2', 'k2', 'lone') + '</g>'
    out += tex(nx + 70, ny + 6, '$\\ce{NH3}$', 21, 'start') + tex(bx + 108, by + 64, '$\\ce{BCl3}$', 21, 'start')
    out += f'<g data-arw="{f(nx)},{f(ny + .75 * S + 10)},{f(nx)},{f(py - .3 * S - 8)},equi,3"></g></g>'
    return out
F['bcl3_nh3'] = bcl3_nh3()

# ── S17 디지털 소양: CHCl3, NF3, OCl2 ──
def dig(name):
    S = 26; cx, cy = 130, 92; dx = 2.3 * S; v = 2.0 * S
    if name == 'CHCl3':
        m = Mol({'c': ('C', cx, cy), 'h': ('H', cx, cy - v), 'a': ('Cl', cx - dx, cy), 'b': ('Cl', cx + dx, cy), 'd': ('Cl', cx, cy + v)},
                [('h', 'c', 1), ('a', 'c', 1), ('c', 'b', 1), ('c', 'd', 1)], {'a': {'u': 2, 'l': 2, 'd': 2}, 'b': {'u': 2, 'r': 2, 'd': 2}, 'd': {'l': 2, 'r': 2, 'd': 2}}, S)
    elif name == 'NF3':
        m = Mol({'c': ('N', cx, cy), 'a': ('F', cx - dx, cy), 'b': ('F', cx + dx, cy), 'd': ('F', cx, cy + v)},
                [('a', 'c', 1), ('c', 'b', 1), ('c', 'd', 1)], {'c': {'u': 2}, 'a': {'u': 2, 'l': 2, 'd': 2}, 'b': {'u': 2, 'r': 2, 'd': 2}, 'd': {'l': 2, 'r': 2, 'd': 2}}, S)
    else:
        m = Mol({'c': ('O', cx, cy), 'a': ('Cl', cx - dx, cy), 'b': ('Cl', cx + dx, cy)},
                [('a', 'c', 1), ('c', 'b', 1)], {'c': {'u': 2, 'd': 2}, 'a': {'u': 2, 'l': 2, 'd': 2}, 'b': {'u': 2, 'r': 2, 'd': 2}}, S)
    return m.svg_lines()
for n in ('CHCl3', 'NF3', 'OCl2'):
    F[f'g_{n}'] = dig(n)

# ── S18 중단원 마무리 01 ──
def q01():
    S = 30; out = ''; d = 1.9 * S; v = 1.75 * S
    cfg = [('X', 110, {'u': 2, 'd': 2}, ['a', 'b'], '(가)'), ('Y', 330, {'u': 2}, ['a', 'b', 'd'], '(나)'), ('Z', 550, {}, ['a', 'b', 'd', 'u'], '(다)')]
    for el, cx, lone, hs, lab in cfg:
        cy = 90
        pos = {'a': (cx - d, cy), 'b': (cx + d, cy), 'd': (cx, cy + v), 'u': (cx, cy - v)}
        atoms = {'c': (el, cx, cy)}; bonds = []
        for h in hs:
            atoms[h] = ('H', *pos[h]); bonds.append((h, 'c', 1) if h in 'au' else ('c', h, 1))
        out += Mol(atoms, bonds, {'c': lone}, S).svg_lines()
        out += tex(cx, 190, lab, 20)
    return out
F['q01'] = q01()

# ── S20 중단원 마무리 03 ──
def q03():
    S = 42
    return (sym(110, 62, 'A', S) + side_dots(110, 62, 'A', {'u': 2, 'l': 1, 'r': 1, 'd': 1}, S)
            + sym(270, 62, 'B', S) + side_dots(270, 62, 'B', {'u': 2, 'l': 2, 'r': 1, 'd': 2}, S))
F['q03'] = q03()

# ── S21 함께 풀어 보기: NH3 ──
def nh3_form():
    S = 30; y = 110; out = ''
    out += sym(40, y, 'H', S) + side_dots(40, y, 'H', {'r': 1}, S) + tex(84, y + 8, '+', 26, extra=f' fill="{GRAV}"')
    nx = 150
    out += sym(nx, y, 'N', S) + side_dots(nx, y, 'N', {'l': 1, 'r': 1, 'u': 1, 'd': 2}, S)
    out += sym(nx, y - 1.9 * S, 'H', S) + side_dots(nx, y - 1.9 * S, 'H', {'d': 1}, S) + tex(nx + 26, y - 1.9 * S + 30, '+', 20, extra=f' fill="{GRAV}"')
    out += tex(216, y + 8, '+', 26, extra=f' fill="{GRAV}"') + sym(270, y, 'H', S) + side_dots(270, y, 'H', {'l': 1}, S)
    out += '<g data-anim="draw" data-dur=".6" data-delay=".3">' + arrow_r(310, 360, y) + '</g>'
    cx = 470
    m = Mol({'n': ('N', cx, y), 'a': ('H', cx - 1.4 * S, y), 'b': ('H', cx + 1.4 * S, y), 'u': ('H', cx, y - 1.5 * S)},
            [('a', 'n', 1), ('n', 'b', 1), ('u', 'n', 1)], {'n': {'d': 2}}, S)
    out += m.svg_dots()
    px = cx + .7 * S
    out += f'<line x1="{f(px + 6)}" y1="{f(y - 8)}" x2="{f(px + 40)}" y2="{f(y - 44)}" stroke="{FIELD}" stroke-width="1.5"/>'
    out += f'<rect x="{f(px + 40)}" y="{f(y - 66)}" width="150" height="32" rx="6" fill="#FFFFFF" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="5 4"/>' + tex(px + 52, y - 43, '❷', 19, 'start')
    out += f'<text class="tex step" x="{f(px + 124)}" y="{f(y - 43)}" data-mix="공유 전자쌍" data-size="19" data-anchor="middle" fill="{FIELD}"></text>'
    out += f'<line x1="{f(cx)}" y1="{f(y + .75 * S + 6)}" x2="{f(cx + 30)}" y2="{f(y + 48)}" stroke="{EQUI}" stroke-width="1.5"/>' + tex(cx + 34, y + 58, '비공유 전자쌍', 19, 'start', extra=' fill="#9A5A12"')
    return out
F['nh3_form'] = nh3_form()

D = os.path.dirname(os.path.abspath(__file__))
tpl = ''.join(open(p, encoding='utf-8').read() for p in sorted(glob.glob(os.path.join(D, 'tpl*.html'))))
miss = set(re.findall(r'@@(\w+)@@', tpl)) - set(F)
if miss: raise SystemExit('없는 그림: ' + ', '.join(sorted(miss)))
out = re.sub(r'@@(\w+)@@', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('slides.html', len(out), 'bytes,', out.count('<section'), 'slides')
