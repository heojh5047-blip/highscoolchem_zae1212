# 화학반응의세계_미래엔 1-1 산과 염기 — 그림 좌표 생성. tpl.html의 {{이름}}을 바꿔 slides.html을 만든다.
import math, re, sys, os

R = {'H': 18, 'C': 24, 'N': 24, 'O': 24, 'F': 24, 'Cl': 29}
RION = {'Cl-': 32, 'F-': 25}
BOND = '#9AA5B1'
L = 50
EQUI = '#E08A2C'


def f(v):
    s = f'{v:.1f}'
    s = s[:-2] if s.endswith('.0') else s
    return '0' if s == '-0' else s


# 분자 정의: 중심 원소, [(원소, 각도, 길이 배율, 표시)]  표시: '' / 'f'(앞, 나중에 그림) / 'n'(새로 받은 H)
SPEC = {
    'HCl': ('Cl', [('H', 0, 1, '')]),
    'H2O': ('O', [('H', 233, 1, ''), ('H', 307, 1, '')]),
    'H3O+': ('O', [('H', 233, 1, ''), ('H', 307, 1, ''), ('H', 90, 1, 'n')]),
    'OH-': ('O', [('H', 307, 1, '')]),
    'NH3': ('N', [('H', 205, 1, ''), ('H', 335, 1, ''), ('H', 270, .72, 'f')]),
    'NH4+': ('N', [('H', 205, 1, ''), ('H', 335, 1, ''), ('H', 270, .72, 'f'), ('H', 90, 1, 'n')]),
    'HF': ('F', [('H', 0, 1, '')]),
}


def pos(x, y, a, l):
    r = math.radians(a)
    return x + math.cos(r) * l, y - math.sin(r) * l


def mol(x, y, name, rot=0, s=1.0, frm=None, lobe=False, newdelay=.5, hlab=True):
    """공-막대 모형. frm=(dx,dy): 새 H가 그만큼 떨어진 곳에서 와서 붙는다. lobe: 받는 자리(rot+90 방향) 로브"""
    if name in RION:
        el = name[:-1]
        return f'<g data-atom="{f(x)},{f(y)},{f(RION[name] * s)},{el}"></g>'
    c, outs = SPEC[name]
    bonds, back, front, new = [], [], [], []
    for el, a, lf, fl in outs:
        hx, hy = pos(x, y, a + rot, L * lf * s)
        ln = f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(hx)}" y2="{f(hy)}" stroke="{BOND}" stroke-width="{f(7 * s)}" stroke-linecap="round"/>'
        at = f'<g data-atom="{f(hx)},{f(hy)},{f(R[el] * s)},{el}' + ('' if hlab else ',-') + '"></g>'
        if fl == 'n' and frm:
            new.append(f'<g data-anim="fade" data-dur=".4" data-delay="{f(newdelay + .9)}">{ln}</g>')
            new.append(f'<g data-anim="move" data-from="{f(frm[0])},{f(frm[1])}" data-dur="1.1" data-delay="{f(newdelay)}" data-ease="out">{at}</g>')
        elif fl == 'f':
            bonds.append(ln); front.append(at)
        else:
            bonds.append(ln); back.append(at)
    lb = ''
    if lobe:
        lx, ly = pos(x, y, rot + 90, 40 * s)
        lb = (f'<ellipse cx="{f(lx)}" cy="{f(ly)}" rx="{f(15 * s)}" ry="{f(21 * s)}" transform="rotate({f(-rot)} {f(lx)} {f(ly)})" '
              f'fill="{EQUI}" fill-opacity=".18" stroke="{EQUI}" stroke-width="1.5"/>')
        d1 = pos(lx, ly, rot, 5 * s); d2 = pos(lx, ly, rot + 180, 5 * s)
        d1 = pos(*d1, rot + 90, 4 * s); d2 = pos(*d2, rot + 90, 4 * s)
        lb += f'<circle cx="{f(d1[0])}" cy="{f(d1[1])}" r="3.5" fill="#16233D"/><circle cx="{f(d2[0])}" cy="{f(d2[1])}" r="3.5" fill="#16233D"/>'
    return lb + ''.join(bonds) + ''.join(back) + f'<g data-atom="{f(x)},{f(y)},{f(R[c] * s)},{c}"></g>' + ''.join(front) + ''.join(new)


def hpos(x, y, name, which=0, rot=0, s=1.0):
    c, outs = SPEC[name]
    el, a, lf, fl = outs[which]
    return pos(x, y, a + rot, L * lf * s)


def tex(x, y, t, size=24, anchor='middle', fill=None, mix=False, extra=''):
    a = 'data-mix' if mix else 'data-tex'
    fl = f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" {a}="{t}" data-size="{size}" data-anchor="{anchor}"{fl}{extra}></text>'


def arw(x1, y1, x2, y2, col='plus', w=3, extra=''):
    return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{col},{w}"{extra}></g>'


PLUS, MINUS, FIELD, BF, MUTED, INK = '#D7263D', '#1F6FD1', '#2E9E6A', '#7B4FC8', '#5B6B7F', '#16233D'
ROLE = {'산': PLUS, '염기': MINUS, '짝염기': MINUS, '짝산': PLUS}


def bracket(x1, x2, y0, y1, col, label, g=None, up=False):
    """괄호선: (x1,y0)↓(x1,y1)→(x2,y1)↑(x2,y0). label은 가로선 가운데(halo)."""
    st = f' class="step" data-g="{g}"' if g else ''
    p = f'M{f(x1)} {f(y0)} L{f(x1)} {f(y1)} L{f(x2)} {f(y1)} L{f(x2)} {f(y0)}'
    return (f'<g{st}><path d="{p}" fill="none" stroke="{col}" stroke-width="3" stroke-linejoin="round" data-anim="draw" data-dur=".9" data-on="step"/>'
            + tex((x1 + x2) / 2, y1 + 7, label, 19, fill=col, mix=True, extra=' data-halo="1"') + '</g>')


# ───────────── 그림들 ─────────────
F = {}

# 표지: Cl- + H3O+ (H가 Cl에서 옮겨 옴)
def cover():
    s = 1.45
    cx, cy = 270, 300
    xc, xo = 150, 380
    out = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    # 옮겨 간 H: 처음 위치는 Cl 오른쪽(HCl의 H)
    hx0, hy0 = xc + L * s, cy
    hx1, hy1 = pos(xo, cy, 90, L * s)
    out += mol(xo, cy, 'H3O+', s=s, frm=(hx0 - hx1, hy0 - hy1), newdelay=.6)
    out += mol(xc, cy, 'Cl-', s=1.25)
    out += arw(175, 170, 330, 205, 'plus', 4, ' data-delay="1.4"')
    out += tex(245, 165, '\\ce{H+}', 30, fill=PLUS)
    out += tex(xc, 405, '\\ce{Cl-}', 30)
    out += tex(xo, 405, '\\ce{H3O+}', 30)
    out += tex(270, 455, '염화 수소의 $\\ce{H+}$이 물 분자로 옮겨 간다', 22, fill=MUTED, mix=True)
    F['cover'] = out


# 대단원 도입: 생활 속 pH 띠
def phbar():
    x0, x1, y = 40, 545, 130
    u = (x1 - x0) / 14
    out = ('<defs><linearGradient id="grad-rm11-02" x1="0" x2="1" y1="0" y2="0">'
           '<stop offset="0" stop-color="#F6B8BF"/><stop offset=".5" stop-color="#E4E8EC"/><stop offset="1" stop-color="#B7CFF2"/></linearGradient></defs>')
    out += f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="34" rx="6" fill="url(#grad-rm11-02)" stroke="#9AA5B1" stroke-width="1.5"/>'
    for p in range(0, 15):
        xx = x0 + p * u
        out += f'<line x1="{f(xx)}" y1="{y + 34}" x2="{f(xx)}" y2="{y + 42}" stroke="{MUTED}" stroke-width="1.5"/>'
        if p % 2 == 0:
            out += tex(xx, y + 64, str(p), 18, fill=MUTED)
    out += tex(x0, y + 96, '산성', 20, 'start', PLUS, True)
    out += tex(x0 + 7 * u, y + 96, '중성', 20, 'middle', MUTED, True)
    out += tex(x1, y + 96, '염기성', 20, 'end', MINUS, True)
    out += tex(x1 + 14, y + 64, '\\text{pH}', 18, 'start', MUTED)
    pins = [(1.8, '위액||약 2', 'up'), (2.4, '레몬즙||약 2.4', 'dn'), (7.4, '혈액||7.4', 'up'), (8.1, '바닷물||약 8.1', 'dn'), (10.5, '제산제||약 10.5', 'up')]
    for k, (v, lab, d) in enumerate(pins):
        xx = x0 + v * u
        if d == 'up':
            body = (f'<line x1="{f(xx)}" y1="{y - 34}" x2="{f(xx)}" y2="{y}" stroke="{INK}" stroke-width="2"/>'
                    f'<circle cx="{f(xx)}" cy="{y - 38}" r="6" fill="{INK}"/>' + tex(xx, y - 74, lab, 20, mix=True))
            frm = '0,-30'
        else:
            body = (f'<line x1="{f(xx)}" y1="{y + 34}" x2="{f(xx)}" y2="{y + 102}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 3"/>'
                    f'<circle cx="{f(xx)}" cy="{y + 106}" r="6" fill="{INK}"/>' + tex(xx, y + 134, lab, 20, mix=True))
            frm = '0,30'
        out += f'<g data-anim="move" data-from="{frm}" data-dur=".7" data-delay="{f(.3 + .25 * k)}" data-ease="out">{body}</g>'
    F['phbar'] = out


# 생각 열기: 두 병과 흰 연기
def smoke():
    out = ''
    for (x, lab) in [(110, '진한||염산'), (390, '진한||암모니아수')]:
        out += (f'<path d="M{x - 45} 250 L{x - 45} 150 Q{x - 45} 128 {x - 22} 122 L{x - 22} 100 L{x + 22} 100 L{x + 22} 122 Q{x + 45} 128 {x + 45} 150 L{x + 45} 250 Z" '
                f'fill="#F4F8FB" stroke="#7E8B98" stroke-width="2.5"/>')
        out += f'<rect x="{x - 45}" y="190" width="90" height="60" fill="#DDEEF8" stroke="none"/>'
        out += f'<path d="M{x - 45} 190 L{x + 45} 190" stroke="#9FC3DD" stroke-width="2"/>'
        out += tex(x, 280, lab.replace('||', ' '), 20, mix=True)
    puffs = [(250, 92, 26), (222, 104, 20), (278, 104, 22), (240, 70, 20), (266, 66, 18), (250, 112, 18)]
    pg = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="#B8C2CC" stroke-width="1.5"/>' for x, y, r in puffs)
    out += f'<g data-anim="move" data-from="0,28" data-dur="1.6" data-delay=".4" data-ease="out"><g data-anim="fade" data-dur="1.2" data-delay=".4">{pg}</g></g>'
    out += arw(160, 100, 205, 100, 'muted', 2) + arw(340, 100, 295, 100, 'muted', 2)
    out += tex(185, 88, '\\ce{HCl}', 20) + tex(318, 88, '\\ce{NH3}', 20)
    out += tex(250, 30, '흰 연기', 20, fill=MUTED, mix=True)
    F['smoke'] = out


# 연결: H+ + H2O -> H3O+
def hydronium():
    x, y = 230, 130
    hx1, hy1 = pos(x, y, 90, L)
    frm = (-110, -15)
    out = mol(x, y, 'H3O+', frm=frm, newdelay=.4)
    # H+ 라벨은 옮겨 오는 H와 함께
    out = out.replace('data-ease="out"><g data-atom', 'data-ease="out"><g data-atom', 1)
    out += f'<g data-anim="move" data-from="{frm[0]},{frm[1]}" data-dur="1.1" data-delay=".4" data-ease="out">' + tex(hx1 - 32, hy1 + 7, '\\ce{H+}', 22, 'end', PLUS) + '</g>'
    out += tex(x, y + 86, '\\ce{H3O+}', 24) + tex(x, y + 116, '하이드로늄 이온', 20, fill=MUTED, mix=True)
    F['hydronium'] = out


# 브뢴스테드·라우리: 수소 원자 → H+
def proton():
    out = ''
    cx, cy = 80, 110
    out += f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{MUTED}" stroke-width="1.8" stroke-dasharray="5 4"/>'
    out += f'<g data-chg="{cx},{cy},11,+"></g>'
    ex, ey = pos(cx, cy, 50, 46)
    efx, efy = 205, 52
    out += f'<g data-anim="move" data-from="{f(ex - efx)},{f(ey - efy)}" data-dur="1.2" data-delay=".5" data-ease="out"><g data-chg="{efx},{efy},9,-"></g>' + tex(efx + 16, efy + 7, 'e^-', 20, 'start', MINUS) + '</g>'
    out += tex(cx, 190, '수소 원자', 20, mix=True)
    out += arw(150, 110, 230, 110, 'ink', 3)
    out += tex(190, 140, '전자를||잃음', 19, fill=MUTED, mix=True)
    out += f'<g data-chg="290,110,11,+"></g>'
    out += tex(290, 160, '\\ce{H+}', 24) + tex(290, 190, '= 양성자', 20, mix=True)
    F['proton'] = out


def roles_box():
    out = (f'<rect x="10" y="40" width="150" height="90" rx="14" fill="#FDECEE" stroke="{PLUS}" stroke-width="2.5"/>'
           + tex(85, 80, '산', 26, fill=PLUS, mix=True, extra=' data-weight="700"') + tex(85, 112, '제공하는 물질', 19, fill=PLUS, mix=True)
           + f'<rect x="290" y="40" width="150" height="90" rx="14" fill="#E8F0FB" stroke="{MINUS}" stroke-width="2.5"/>'
           + tex(365, 80, '염기', 26, fill=MINUS, mix=True, extra=' data-weight="700"') + tex(365, 112, '제공받는 물질', 19, fill=MINUS, mix=True)
           + arw(170, 85, 280, 85, 'plus', 4) + tex(225, 68, '\\ce{H+}', 22, fill=PLUS))
    F['roles'] = out


# 반응 모형 그림 (반응물 2 → 생성물 2)
def rxfig(key, items, arrowtex, give, gid='g1'):
    """items: [(name, x, formula, role, kwargs)] 4개(반응물 2, 생성물 2). give=(산 index, 염기 index, 산의 H index)"""
    y = 150
    out = ''
    ai, bi, hi = give
    an, ax = items[ai][0], items[ai][1]
    bn, bx = items[bi][0], items[bi][1]
    hx, hy = hpos(ax, y, an, hi, items[ai][4].get('rot', 0))
    tx, ty = bx, y - 62
    for k, (name, x, form, role, kw) in enumerate(items):
        out += mol(x, y, name, **kw)
        out += tex(x, y + 92, form, 26)
        if role:
            col = ROLE[role.split('|')[0]]
            out += f'<g class="step" data-g="{gid}">' + tex(x, y + 128, role.split('|')[0] + (f'||<span style="font-size:17px"></span>' if False else ''), 21, fill=col, mix=True, extra=' data-weight="700"') + '</g>'
    out += tex(items[0][1] / 2 + items[1][1] / 2, y + 10, '+', 30) + tex(items[2][1] / 2 + items[3][1] / 2, y + 10, '+', 30)
    out += tex((items[1][1] + items[2][1]) / 2, y + 8, arrowtex, 34)
    # H+ 이동 화살표(반응물 위)
    sx = hx
    dirn = 1 if bx > sx else -1
    out += arw(sx, y - 70, tx - dirn * 22, y - 70, 'plus', 3.5) + tex((sx + tx) / 2, y - 82, '\\ce{H+}', 22, fill=PLUS)
    out += f'<path d="M{f(sx)} {f(hy - 22)} L{f(sx)} {f(y - 70)}" stroke="{PLUS}" stroke-width="2" stroke-dasharray="4 3" fill="none"/>'
    F[key] = out


def figs_rx():
    # S9 HCl + H2O -> Cl- + H3O+
    hfrom = (-150, 50)  # 새 H가 처음에 있던 곳(Cl- 쪽) 상대 위치
    rxfig('rx9', [('HCl', 110, '\\ce{HCl}', '산', {}), ('H2O', 330, '\\ce{H2O}', '염기', {'lobe': True}),
                  ('Cl-', 560, '\\ce{Cl-}', '', {}), ('H3O+', 780, '\\ce{H3O+}', '', {'frm': (-130, 50)})], '\\ce{->}', (0, 1, 0))
    # S10 NH3 + H2O <=> NH4+ + OH-   (물의 오른쪽 H가 왼쪽 NH3로) → 물을 거울상으로: H at 233,307 중 233(왼쪽)이 떠남
    rxfig('rx10', [('NH3', 110, '\\ce{NH3}', '염기', {'lobe': True}), ('H2O', 330, '\\ce{H2O}', '산', {}),
                   ('NH4+', 560, '\\ce{NH4+}', '', {'frm': (110, 40)}), ('OH-', 780, '\\ce{OH-}', '', {})], '\\ce{<=>}', (1, 0, 0))


# 해 보기: 유리관 흰 고리
def tube():
    out = ''
    out += '<rect x="20" y="78" width="300" height="34" rx="17" fill="#F4F8FB" stroke="#7E8B98" stroke-width="2.5"/>'
    out += '<circle cx="42" cy="95" r="13" fill="#FFFFFF" stroke="#9AA5B1" stroke-width="2"/><circle cx="298" cy="95" r="13" fill="#FFFFFF" stroke="#9AA5B1" stroke-width="2"/>'
    ring = 58 + 0.594 * (282 - 58)
    out += f'<g data-anim="fade" data-dur="1.2" data-delay=".9"><ellipse cx="{f(ring)}" cy="95" rx="9" ry="16" fill="#FFFFFF" stroke="#8C99A6" stroke-width="2"/><ellipse cx="{f(ring)}" cy="95" rx="4" ry="12" fill="#E9EDF1"/></g>'
    out += arw(62, 60, 130, 60, 'muted', 2) + arw(278, 60, 236, 60, 'muted', 2)
    out += tex(96, 46, '\\ce{NH3}', 23) + tex(257, 46, '\\ce{HCl}', 23)
    out += tex(70, 146, '진한||암모니아수 솜', 22, mix=True) + tex(280, 146, '진한||염산 솜', 22, mix=True)
    out += tex(ring, 192, '흰 고리', 22, fill=INK, mix=True, extra=' data-weight="700"')
    F['tube'] = out


def nh4cl():
    out = ''
    # 위: NH3(받는 자리 오른쪽) + HCl(H 왼쪽)
    y1, y2 = 62, 222
    out += mol(85, y1, 'NH3', rot=-90, lobe=True, hlab=False) + tex(190, y1 + 9, '+', 26)
    out += mol(270, y1, 'HCl', rot=180) if False else ''
    # HCl: H 왼쪽 — SPEC 회전 사용
    out += mol(268, y1, 'HCl', rot=180, hlab=False)
    out += tex(85, y1 + 82, '\\ce{NH3}', 25) + tex(262, y1 + 82, '\\ce{HCl}', 25)
    out += arw(182, 118, 182, 168, 'ink', 3)
    hx0, hy0 = pos(268, y1, 180, L)
    hx1, hy1 = pos(95, y2, 0 - 90 + 90, L)  # NH4+ 회전 -90 → 새 H는 0°(오른쪽)
    out += mol(95, y2, 'NH4+', rot=-90, frm=(hx0 - hx1, hy0 - hy1), newdelay=.6, hlab=False)
    out += mol(232, y2, 'Cl-')
    out += tex(95, y2 + 82, '\\ce{NH4+}', 25) + tex(232, y2 + 82, '\\ce{Cl-}', 25) + '<g data-atom="20,326,10,H,-"></g>' + tex(36, 333, '= 수소 원자', 22, 'start', MUTED, True)
    F['nh4cl'] = out


# 짝산·짝염기 반응식 그림
def eqfig(key, parts, roles, fwd, rev, p1, p2, g=('g1', 'g2', 'g3', 'g3'), W=900):
    """parts: [(x, tex)] 7개(종1, +, 종2, 화살표, 종3, +, 종4). roles: 4개 (글, 색). fwd/rev: (from x, to x)"""
    y = 160
    out = ''
    for x, t in parts:
        out += tex(x, y, t, 34)
    xs = [parts[0][0], parts[2][0], parts[4][0], parts[6][0]]
    for k, (t, col) in enumerate(roles):
        gg = g[0] if k < 2 else g[1]
        out += f'<g class="step" data-g="{gg}">' + tex(xs[k], y + 48, t, 24, fill=col) + '</g>'
    # 정반응 H+ (위, 아래쪽 줄) / 역반응 H+ (위, 위쪽 줄)
    a, b = fwd
    out += f'<g class="step" data-g="{g[0]}">' + arw(a, 100, b, 100, 'plus', 3) + tex((a + b) / 2, 88, '\\ce{H+}', 21, fill=PLUS) + '</g>'
    a, b = rev
    out += f'<g class="step" data-g="{g[1]}">' + arw(a, 100, b, 100, 'plus', 3) + tex((a + b) / 2, 88, '\\ce{H+}', 21, fill=PLUS) + '</g>'
    # 쌍 1 아래(field), 쌍 2 더 아래(bfield)
    out += bracket(p1[0], p1[1], y + 64, y + 96, FIELD, '짝산·짝염기 쌍 1', g[2])
    out += bracket(p2[0], p2[1], y + 64, y + 136, BF, '짝산·짝염기 쌍 2', g[3])
    F[key] = out


def figs_eq():
    eqfig('eq13', [(110, '\\ce{HCO3-}'), (230, '+'), (330, '\\ce{H2O}'), (440, '\\ce{<=>}'), (560, '\\ce{H2CO3}'), (680, '+'), (790, '\\ce{OH-}')],
          [('\\text{염기}_1', MINUS), ('\\text{산}_2', PLUS), ('\\text{산}_1', PLUS), ('\\text{염기}_2', MINUS)],
          (300, 150), (590, 765), (110, 560), (330, 790))
    eqfig('eq15', [(90, '\\ce{HF}'), (170, '+'), (250, '\\ce{NH3}'), (350, '\\ce{<=>}'), (450, '\\ce{F-}'), (530, '+'), (620, '\\ce{NH4+}')],
          [('\\text{산}_1', PLUS), ('\\text{염기}_2', MINUS), ('\\text{염기}_1', MINUS), ('\\text{산}_2', PLUS)],
          (110, 230), (600, 470), (90, 450), (250, 620), g=('e1', 'e2', 'e3', 'e3'))


# 양쪽성: 물 가운데
def amph():
    y = 150
    out = mol(90, y, 'HCl') + mol(300, y, 'H2O', lobe=True) + mol(515, y, 'NH3', lobe=True)
    out += tex(90, y + 88, '\\ce{HCl}', 24) + tex(300, y + 88, '\\ce{H2O}', 24) + tex(515, y + 88, '\\ce{NH3}', 24)
    out += arw(150, 120, 270, 92, 'plus', 3.5) + tex(205, 84, '\\ce{H+}', 21, fill=PLUS)
    hx, hy = pos(300, y, 307, L)
    out += arw(hx + 18, hy - 12, 488, 98, 'plus', 3.5) + tex(430, 122, '\\ce{H+}', 21, fill=PLUS, extra=' data-halo="1"')
    out += tex(170, 38, '받음 → 물은 염기', 21, fill=MINUS, mix=True, extra=' data-weight="700"')
    out += tex(440, 38, '내놓음 → 물은 산', 21, fill=PLUS, mix=True, extra=' data-weight="700"')
    F['amph'] = out


def venn():
    out = (f'<g data-anim="scale" data-from=".6" data-o="230,170" data-dur="1.1" data-delay=".3" data-ease="back">'
           f'<ellipse cx="230" cy="170" rx="215" ry="150" fill="#F2FAF5" stroke="{FIELD}" stroke-width="2.5"/></g>'
           f'<ellipse cx="160" cy="190" rx="105" ry="78" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    out += tex(230, 50, '브뢴스테드·라우리 산·염기', 21, fill='#1B5E3F', mix=True, extra=' data-weight="700"')
    out += tex(160, 160, '아레니우스||산·염기', 20, mix=True, extra=' data-weight="700"')
    out += tex(160, 238, '\\ce{HCl(aq)}, \\ce{NaOH(aq)}', 19)
    out += tex(352, 120, '\\ce{NH3}', 21) + tex(352, 178, '\\ce{HCO3-}', 21) + tex(352, 236, '\\ce{H2O}', 21)
    out += tex(230, 296, '\\ce{HCl(g) + NH3(g)}', 19)
    F['venn'] = out


cover(); phbar(); smoke(); hydronium(); proton(); roles_box(); figs_rx(); tube(); nh4cl(); figs_eq(); amph(); venn()

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    def rep(m):
        k = m.group(1)
        if k not in F:
            sys.exit('없는 그림: ' + k)
        return F[k]
    out = re.sub(r'\{\{(\w+)\}\}', rep, tpl)
    dst = sys.argv[1]
    open(dst, 'w', encoding='utf-8').write(out)
    print('ok', len(out))
