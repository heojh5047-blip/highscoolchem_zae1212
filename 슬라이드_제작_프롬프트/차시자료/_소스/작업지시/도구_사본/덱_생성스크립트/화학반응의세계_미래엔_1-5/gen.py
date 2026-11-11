import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

F = {}
HAc20 = lambda V: ph(0.1, 20, V, Ka=1.8e-5)
LIGHT_P = '#FBD5DA'; LIGHT_M = '#D6E6FA'; LIGHT_G = '#E3E7EC'; HA_BAR = '#D6E9D8'; VESSEL = '#C8463C'

def svg(vb, w, label, body, cls='fig', extra=''):
    return '<svg class="%s" viewBox="0 0 %d %d" style="width:%dpx" aria-label="%s"%s>%s</svg>' % (cls, vb[0], vb[1], w, label, (' '+extra) if extra else '', body)

def pill(x, y, w, h, kind, lab=None, size=18):
    st = {'m': (LIGHT_M, MINUS, ''), 'p': (LIGHT_P, PLUS, ''), 'g': (LIGHT_G, GRAV, ''), 'w': ('#FFFFFF', GRAV, ' stroke-dasharray="4 3"')}[kind]
    s = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="2.5"%s/>' % (r(x-w/2), r(y-h/2), r(w), r(h), r(h/2), st[0], st[1], st[2])
    if lab: s += T(x, y+size*.36, tex=lab, size=size, fill=INK)
    return s

def gion(x, y, lab, rr=22, size=18):
    return ion(x, y, rr, 's', lab, size)

def HA(x, y, w=104): return pill(x, y, w, 34, 'g', '\\ce{CH3COOH}')
def AC(x, y, w=104): return pill(x, y, w, 34, 'm', '\\ce{CH3COO-}')
def W(x, y): return pill(x, y, 70, 30, 'w', '\\ce{H2O}')
def H3O(x, y, rr=20): return ion(x, y, rr, 'p') + T(x, y-rr-8, tex='\\ce{H3O+}', size=18, fill=PLUS, halo=True)
def OH(x, y, rr=20): return ion(x, y, rr, 'm') + T(x, y-rr-8, tex='\\ce{OH-}', size=18, fill=MINUS, halo=True)

def dropper(cx, ytop, lab):
    s = '<rect x="%s" y="%s" width="30" height="40" rx="12" fill="#3A3F47"/>' % (r(cx-15), r(ytop))
    s += '<path d="M%s %s L%s %s L%s %s L%s %s L%s %s L%s %s Z" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (
        r(cx-9), r(ytop+38), r(cx+9), r(ytop+38), r(cx+9), r(ytop+90), r(cx+3), r(ytop+112), r(cx-3), r(ytop+112), r(cx-9), r(ytop+90), LIGHT_P, GLASS)
    return s

# ── S1 표지: 증류수 vs 완충 용액에 염산 한 방울
b = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
for i, (nm, p0, p1, col) in enumerate([('증류수', '7.0', '1.8', PLUS), ('완충 용액', '4.7', '4.6', INK)]):
    cx = 160+i*220
    b += dropper(cx, 40, '\\ce{HCl(aq)}')
    b += '<g data-anim="move" data-from="0,-50" data-dur=".9" data-ease="in" data-delay="%s"><path d="M%s 182 Q%s 196 %s 200 A7 7 0 1 1 %s 200 Q%s 196 %s 182 Z" fill="%s"/></g>' % (r(.4+i*.6), r(cx), r(cx+6), r(cx+6), r(cx-6), r(cx-6), r(cx), PLUS)
    b += beaker(cx-75, 220, 150, 150, 262)
    if i == 0:
        b += '<rect x="%s" y="264" width="146" height="104" fill="#FFFFFF" opacity=".25"/>' % r(cx-73)
    else:
        for (dx, dy, k) in [(-40, 290, 'g'), (20, 300, 'm'), (-20, 335, 'm'), (40, 340, 'g')]:
            b += pill(cx+dx, dy, 30, 16, k)
    b += T(cx, 400, mix=nm, size=24, weight='700')
    b += T(cx, 440, mix='pH %s → %s' % (p0, p1), size=24, fill=col, weight='700')
b += T(270, 492, mix='염산을 똑같이 넣었을 때', size=20, fill=MUTED)
b += T(270, 30, tex='\\ce{HCl(aq)}', size=22, fill=PLUS)
F['S1'] = '<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="증류수와 완충 용액에 염산을 넣었을 때 pH 변화: 7.0에서 1.8, 4.7에서 4.6">' + b + '</svg>'

# ── S3 레몬
b = ''
b += '<path d="M150 90 L330 90 L310 310 Q308 322 296 322 L184 322 Q172 322 170 310 Z" fill="#FFF6C9" stroke="%s" stroke-width="3"/>' % GLASS
b += '<path d="M156 130 L324 130" stroke="#E8D77A" stroke-width="2"/>'
b += '<path d="M260 40 L290 40 L268 280" fill="none" stroke="#D7263D" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
b += '<circle cx="318" cy="96" r="38" fill="#F5D33B" stroke="#C9A300" stroke-width="3"/><circle cx="318" cy="96" r="29" fill="#FFF3A6"/>'
for k in range(8):
    import math as _m
    a = k*_m.pi/4
    b += line(318, 96, 318+27*_m.cos(a), 96+27*_m.sin(a), '#E9C83A', 2)
for (x, y) in [(200, 170), (240, 210), (210, 250), (270, 180)]:
    b += '<circle cx="%d" cy="%d" r="6" fill="none" stroke="#E0C040" stroke-width="2"/>' % (x, y)
b += '<ellipse cx="420" cy="290" rx="58" ry="38" fill="#F5D33B" stroke="#C9A300" stroke-width="3"/><path d="M470 280 q16 -4 18 8" fill="none" stroke="#C9A300" stroke-width="3"/>'
b += '<ellipse cx="80" cy="300" rx="50" ry="32" fill="#F5D33B" stroke="#C9A300" stroke-width="3"/>'
b += line(20, 335, 490, 335, MUTED, 2)
b += '<g data-anim="pop" data-o="420,215" data-dur=".7" data-delay=".5"><rect x="350" y="180" width="140" height="62" rx="14" fill="#FFF8E6" stroke="%s" stroke-width="2"/>' % EQUI
b += T(420, 206, mix='레몬', size=20, weight='700') + T(420, 232, mix='산성', size=20, fill=PLUS, weight='700') + '</g>'
F['S3'] = svg((500, 350), 460, '레모네이드 컵과 레몬 — 레몬은 산성', b)

# ── S4 약산–강염기 곡선의 완만한 구간
ax = Axes(66, 290, 330, 240, 30, 14)
b = '<g data-anim="fade" data-dur=".8" data-delay="1.6"><rect x="%s" y="%s" width="%s" height="%s" fill="#FFE45C" opacity=".35"/></g>' % (r(ax.X(4)), r(ax.Y(14)), r(ax.X(16)-ax.X(4)), r(ax.Y(0)-ax.Y(14)))
b += ax.draw([0, 10, 20, 30], [0, 7, 14], '$V_{\\ce{NaOH}}$ [mL]')
b += '<g data-anim="draw" data-dur="1.6">' + curve_pts(ax, HAc20, dense(20, 0, 30), EQUI, 3.5) + '</g>'
b += T(ax.X(10), ax.Y(10.8), mix='pH가 천천히||변하는 구간', size=19, fill=INK, weight='700', halo=True)
b += T(ax.X(10), ax.Y(2.2), tex='\\ce{CH3COOH}+\\ce{CH3COO-}', size=19, fill=INK, halo=True)
b += T(ax.X(21)+4, ax.Y(HAc20(20))+30, mix='중화점', size=19, anchor='start', fill=MUTED, halo=True)
F['S4'] = svg((430, 350), 420, '0.1 M 아세트산을 수산화 나트륨으로 적정한 곡선에서 pH가 천천히 변하는 구간', b)

# ── S5 두 가지 완충 용액(짝 카드)
b = ''
for i, (tt, a, ak, bb, bk, nt) in enumerate([('약산 + 그 짝염기', '\\ce{CH3COOH}', 'g', '\\ce{CH3COO-}', 'm', '아세트산 + 아세트산 나트륨'),
                                           ('약염기 + 그 짝산', '\\ce{NH3}', 'g', '\\ce{NH4+}', 'p', '암모니아 + 염화 암모늄')]):
    y0 = 8+i*166
    b += '<g data-anim="pop" data-o="240,%s" data-dur=".6" data-delay="%s">' % (r(y0+75), r(.3+i*.5))
    b += '<rect x="10" y="%s" width="460" height="152" rx="16" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % (r(y0), MUTED)
    b += T(30, y0+32, mix=tt, size=21, anchor='start', weight='700')
    b += T(30, y0+58, mix=nt, size=18, anchor='start', fill=MUTED)
    b += pill(150, y0+92, 120, 38, ak, a, 20) + T(240, y0+99, tex='+', size=22, fill=INK) + pill(330, y0+92, 120, 38, bk, bb, 20)
    b += '<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="2.5"/>' % (r(150), r(y0+115), r(150), r(y0+124), r(330), r(y0+124), r(330), r(y0+115), FIELD)
    b += T(240, y0+144, mix='짝산·짝염기 쌍', size=19, fill=FIELD, weight='700', halo=True)
    b += '</g>'
F['S5'] = svg((480, 332), 470, '완충 용액의 두 가지 예: 아세트산과 아세트산 나트륨, 암모니아와 염화 암모늄', b)

# ── S7 완충 용액 만들기
def cylinder(cx, top, bot, level, fill=WATER):
    s = '<rect x="%s" y="%s" width="44" height="%s" fill="%s"/>' % (r(cx-22), r(level), r(bot-level), fill)
    s += line(cx-22, level, cx+22, level, WATER_S, 2)
    s += '<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (r(cx-22), r(top), r(cx-22), r(bot), r(cx+22), r(bot), r(cx+22), r(top), GLASS)
    s += '<rect x="%s" y="%s" width="80" height="8" rx="3" fill="%s"/>' % (r(cx-40), r(bot), GLASS)
    for k in range(1, 7):
        yy = bot-k*(bot-top-10)/6
        s += line(cx-22, yy, cx-10, yy, MUTED, 1.5)
    return s
b = ''
b += cylinder(80, 60, 240, 100, '#F3F4F6') + cylinder(240, 60, 240, 100, '#E9F1FB')
b += T(80, 278, tex='\\ce{CH3COOH(aq)}', size=19) + T(80, 304, mix='0.2 M 50 mL', size=19, fill=MUTED)
b += T(240, 278, tex='\\ce{CH3COONa(aq)}', size=19) + T(240, 304, mix='0.2 M 50 mL', size=19, fill=MUTED)
b += T(160, 160, tex='+', size=28)
b += '<g data-arw="300,160,350,160,ink,3"></g>'
b += beaker(370, 90, 150, 160, 130)
b += '<g data-anim="scale" data-from="1,0.2" data-o="445,250" data-dur="1.2" data-delay=".5"><rect x="374" y="131" width="142" height="116" fill="#E9F1FB"/></g>'
b += T(445, 278, mix='완충 용액', size=20, weight='700') + T(445, 304, mix='100 mL', size=19, fill=MUTED)
F['S7'] = svg((540, 320), 500, '0.2 M 아세트산 수용액 50 mL와 0.2 M 아세트산 나트륨 수용액 50 mL를 섞어 완충 용액 100 mL를 만든다', b)

# ── S8 비커 넷 + pH 측정기
b = ''
names = [('증류수', None), ('아세트산', '수용액'), ('아세트산 나트륨', '수용액'), ('완충 용액', None)]
fills = ['#F2F8FD', '#F3F4F6', '#E9F1FB', '#EEF1F8']
for i, (n1, n2) in enumerate(names):
    cx = 75+i*130
    b += beaker(cx-48, 150, 96, 110, 182, fill=fills[i])
    b += T(cx, 290, mix=n1, size=19, weight='700')
    if n2: b += T(cx, 314, mix=n2, size=19)
    b += T(cx, 236, mix='50 mL', size=18, fill=MUTED)
mx = 75+3*130
b += '<g data-anim="move" data-from="-390,0" data-dur="1.6" data-ease="soft" data-delay=".3">'
b += '<rect x="%s" y="14" width="76" height="56" rx="8" fill="#F1F3F5" stroke="%s" stroke-width="2.5"/>' % (r(mx-38), MUTED)
b += '<rect x="%s" y="22" width="60" height="24" rx="3" fill="#DFF3E8"/>' % r(mx-30)
b += T(mx, 42, mix='pH', size=18, fill=INK)
b += line(mx, 70, mx, 206, '#3A3F47', 6, extra='stroke-linecap="round"') + '<ellipse cx="%s" cy="210" rx="6" ry="9" fill="#9AA5B1"/>' % r(mx)
b += '</g>'
b += T(mx-60, 44, mix='pH 측정기', size=19, anchor='end', fill=MUTED)
F['S8'] = svg((540, 330), 520, '증류수, 아세트산 수용액, 아세트산 나트륨 수용액, 완충 용액을 50 mL씩 담은 비커와 pH 측정기', b)

# ── S11 pH 변화 비교 (처음 → NaOH / HCl)
data = [('증류수', None, 7.0, 12.2, 1.8, '+5.2', '−5.2'), ('아세트산', '수용액', 2.7, 3.8, 1.7, '+1.1', '−1.0'),
        ('아세트산||나트륨', '수용액', 9.0, 12.2, 5.7, '+3.2', '−3.3'), ('완충 용액', None, 4.7, 4.9, 4.6, '+0.2', '−0.1')]
x0, y0, hh = 70, 340, 294
Y = lambda p: y0-p/14*hh
b = line(x0, y0, x0, y0-hh-14, MUTED, 2) + '<path d="M%s %s L%s %s L%s %s Z" fill="%s"/>' % (r(x0), r(y0-hh-22), r(x0-5), r(y0-hh-12), r(x0+5), r(y0-hh-12), MUTED)
b += line(x0, y0, 580, y0, MUTED, 2)
for v in [0, 7, 14]:
    b += line(x0-6, Y(v), x0, Y(v), MUTED, 2) + T(x0-10, Y(v)+7, tex=str(v), size=19, anchor='end', fill=MUTED)
b += line(x0, Y(7), 580, Y(7), GRAV, 1.5, '6 5')
b += T(x0+10, y0-hh-12, tex='\\text{pH}', size=19, anchor='start', fill=MUTED)
for i, (n1, n2, p0, pb, pa, db, da) in enumerate(data):
    cx = 140+i*122
    if i == 0:
        b += '<rect x="%s" y="%s" width="92" height="%s" rx="10" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 5"/>' % (r(cx-46), r(Y(14)-4), r(hh+8), GRAV)
    if i == 3:
        b += '<rect x="%s" y="%s" width="92" height="%s" rx="10" fill="#FFFDF0" stroke="%s" stroke-width="3"/>' % (r(cx-46), r(Y(14)-4), r(hh+8), INK)
    if abs(pb-p0) >= .5:
        b += '<g data-arw="%s,%s,%s,%s,minus,4"></g>' % (r(cx+8), r(Y(p0)), r(cx+8), r(Y(pb)))
    else:
        b += line(cx+2, Y(pb), cx+14, Y(pb), MINUS, 4)
    if abs(pa-p0) >= .5:
        b += '<g data-arw="%s,%s,%s,%s,plus,4"></g>' % (r(cx-8), r(Y(p0)), r(cx-8), r(Y(pa)))
    else:
        b += line(cx-14, Y(pa), cx-2, Y(pa), PLUS, 4)
    b += dot(cx, Y(p0), INK, 7)
    b += T(cx+16, Y(pb)-4 if pb-p0 >= .5 else Y(pb)-12, mix=db, size=19, anchor='start', fill=MINUS, weight='700', halo=True)
    b += T(cx-16, Y(pa)+18 if p0-pa >= .5 else Y(pa)+26, mix=da, size=19, anchor='end', fill=PLUS, weight='700', halo=True)
    nb = len(n1.split('||'))
    for k, nn in enumerate(n1.split('||') + ([n2] if n2 else [])):
        b += T(cx, y0+26+k*24, mix=nn, size=19, weight='700' if k < nb else None)
b += dot(150, 24, INK, 6) + T(162, 31, mix='처음 pH', size=19, anchor='start')
b += '<g data-arw="270,36,270,14,minus,4"></g>' + T(282, 31, mix='NaOH 5 mL', size=19, anchor='start', fill=MINUS)
b += '<g data-arw="410,14,410,36,plus,4"></g>' + T(422, 31, mix='HCl 5 mL', size=19, anchor='start', fill=PLUS)
F['S11'] = svg((590, 420), 540, '네 액체의 처음 pH와 수산화 나트륨, 염산을 넣었을 때의 pH 변화 폭', b)

# ── S14 완충 용액 속 입자 (같은 양)
b = beaker(20, 70, 420, 230, 92)
slots = [(80, 140), (185, 140), (290, 140), (395, 140), (80, 200), (185, 200), (290, 200), (395, 200), (80, 260), (185, 260), (290, 260), (395, 260)]
kinds = ['ha', 'na', 'ac', 'ha', 'ac', 'ha', 'na', 'ac', 'na', 'ac', 'ha', 'na']
b += '<g data-anim="move" data-from="0,-14" data-dur="1" data-rep="damp">'
for (x, y), k in zip(slots, kinds):
    b += HA(x, y) if k == 'ha' else (AC(x, y) if k == 'ac' else gion(x, y, '\\ce{Na+}', 20))
b += '</g>'
b += T(230, 44, mix='아세트산 + 아세트산 나트륨 (같은 양(mol))', size=19, fill=MUTED)
F['S14'] = svg((460, 320), 450, '완충 용액 속 아세트산 분자 4개, 아세트산 이온 4개, 나트륨 이온 4개', b)

# ── S15/S16 산·염기 첨가 두 칸
def two_panel(add):
    b = ''
    for p in range(2):
        x0 = 10+p*330
        b += beaker(x0+5, 110, 250, 240, 128)
        b += T(x0+130, 30, mix='(가) 첨가한 직후' if p == 0 else '(나) 반응한 뒤', size=20, weight='700')
    # (가): HA 4, AC 4 + 들어오는 이온 2
    sl = lambda x0: [(x0+72, 158), (x0+188, 158), (x0+72, 206), (x0+188, 206), (x0+72, 254), (x0+188, 254), (x0+72, 302), (x0+188, 302)]
    for i, (x, y) in enumerate(sl(10)):
        b += HA(x, y) if i % 2 == 0 else AC(x, y)
    b += '<g data-anim="move" data-from="0,-36" data-dur=".9" data-ease="in" data-delay=".3">'
    for x in (90, 180):
        b += H3O(x, 88, 18) if add == 'acid' else OH(x, 88, 18)
    b += '</g>'
    b += '<g data-arw="268,220,322,220,ink,3"></g>'
    # (나)
    s2 = [(412, 158), (528, 158), (412, 206), (528, 206), (412, 254), (528, 254), (412, 302), (528, 302)]
    if add == 'acid':
        ks = ['ha', 'ac', 'ha', 'ac', 'ha', 'new', 'ha', 'new']
    else:
        ks = ['ac', 'ha', 'ac', 'new', 'ac', 'ha', 'new', 'ac']
    for (x, y), k in zip(s2, ks):
        if k == 'new':
            b += '<g data-anim="pop" data-o="%s,%s" data-dur=".6" data-delay="1">' % (r(x), r(y))
            b += (HA(x, y) if add == 'acid' else AC(x, y))
            b += '<rect x="%s" y="%s" width="112" height="42" rx="21" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 4"/></g>' % (r(x-56), r(y-21), EQUI)
        else:
            b += HA(x, y) if k == 'ha' else AC(x, y)
    b += '<g data-anim="fade" data-dur=".6" data-delay="1.2">' + W(430, 88) + W(510, 88) + '</g>'
    return b
F['S15'] = svg((600, 360), 590, '완충 용액에 하이드로늄 이온 2개를 넣으면 아세트산 이온 2개가 아세트산 분자로 바뀌고 물이 생긴다', two_panel('acid'))
F['S16'] = svg((600, 360), 590, '완충 용액에 수산화 이온 2개를 넣으면 아세트산 분자 2개가 아세트산 이온으로 바뀌고 물이 생긴다', two_panel('base'))

# ── S17 완충 용액의 원리(막대)
b = ''
U = 24; base = 210
def bars(cx, nha, nac, title, anim=None):
    s = '<rect x="%s" y="8" width="170" height="34" rx="17" fill="#EEF3F8"/>' % r(cx-85)
    s += T(cx, 32, mix=title, size=19, weight='700')
    s += line(cx-110, base-5*U, cx+110, base-5*U, MUTED, 1.5, '3 4')
    for k, (n, fill, st, lab) in enumerate([(nha, LIGHT_G, GRAV, '\\ce{CH3COOH}'), (nac, LIGHT_M, MINUS, '\\ce{CH3COO-}')]):
        x = cx-96+k*100
        rect = '<rect x="%s" y="%s" width="92" height="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (r(x), r(base-n*U), r(n*U), fill, st)
        if anim and n != 5:
            rect = '<g data-anim="scale" data-from="1,%s" data-o="%s,%s" data-dur="1" data-delay="%s">%s</g>' % (r(5/n), r(x+46), base, anim, rect)
        s += rect
        s += T(x+46, base+26, tex=lab, size=18)
    s += line(cx-110, base, cx+110, base, INK, 2)
    return s
b += bars(150, 7, 3, '산 첨가 후', '.6') + bars(500, 5, 5, '완충 용액') + bars(850, 3, 7, '염기 첨가 후', '.6')
b += '<g data-arw="384,110,276,110,plus,4"></g>' + T(330, 96, tex='\\ce{H3O+}', size=20, fill=PLUS, halo=True)
b += '<g data-arw="616,110,724,110,minus,4"></g>' + T(670, 96, tex='\\ce{OH-}', size=20, fill=MINUS, halo=True)
F['S17'] = svg((1000, 246), 1000, '완충 용액에 산을 넣으면 아세트산 막대가 길어지고 아세트산 이온 막대가 짧아지며, 염기를 넣으면 반대가 된다', b)

# ── S18 암모니아–염화 암모늄
b = beaker(20, 80, 380, 200, 104)
sl = [(80, 150), (200, 150), (320, 150), (80, 200), (200, 200), (320, 200), (80, 250), (200, 250), (320, 250)]
ks = ['nh3', 'nh4', 'cl', 'nh4', 'cl', 'nh3', 'cl', 'nh3', 'nh4']
for (x, y), k in zip(sl, ks):
    if k == 'nh3': b += pill(x, y, 80, 34, 'g', '\\ce{NH3}')
    elif k == 'nh4': b += pill(x, y, 80, 34, 'p', '\\ce{NH4+}')
    else: b += gion(x, y, '\\ce{Cl-}', 20)
b += '<g data-anim="move" data-from="0,-30" data-dur=".9" data-ease="in" data-delay=".3">' + OH(210, 64, 18) + '</g>'
b += T(250, 70, mix='소량 첨가', size=19, anchor='start', fill=MINUS)
F['S18'] = svg((420, 300), 400, '암모니아 3개, 암모늄 이온 3개, 염화 이온 3개가 들어 있는 완충 용액에 수산화 이온을 넣는다', b)

# ── S19 혈액 pH 수직선
def phline(w=600, x0=40, yb=110, arrows=False):
    lo, hi = 6.8, 8.0
    X = lambda v: x0+(v-lo)/(hi-lo)*(w-2*x0)
    s = '<rect x="%s" y="%s" width="%s" height="34" fill="#F7C9C9"/>' % (r(X(6.8)), r(yb-34), r(X(7.0)-X(6.8)))
    s += '<rect x="%s" y="%s" width="%s" height="34" fill="#F7C9C9"/>' % (r(X(7.8)), r(yb-34), r(X(8.0)-X(7.8)))
    s += '<g data-anim="fade" data-dur=".8" data-delay=".5"><rect x="%s" y="%s" width="%s" height="34" fill="%s"/></g>' % (r(X(7.35)), r(yb-34), r(X(7.45)-X(7.35)), FIELD)
    s += '<rect x="%s" y="%s" width="%s" height="34" fill="none" stroke="%s" stroke-width="1.5"/>' % (r(X(lo)), r(yb-34), r(X(hi)-X(lo)), MUTED)
    for v in [6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0]:
        s += line(X(v), yb, X(v), yb+7, MUTED, 2) + T(X(v), yb+30, tex='%.1f' % v, size=19, fill=MUTED)
    s += T(X(7.4), yb-46, mix='적정 범위 7.35~7.45', size=19, fill=FIELD, weight='700')
    s += T(X(6.9), yb-46, mix='매우 위험', size=19, fill=PLUS, weight='700')
    s += T(X(7.9), yb-46, mix='매우 위험', size=19, fill=PLUS, weight='700')
    if arrows:
        s += '<g data-arw="%s,%s,%s,%s,plus,4"></g>' % (r(X(7.30)), r(yb+58), r(X(6.95)), r(yb+58)) + T(X(7.12), yb+88, mix='산증', size=20, fill=PLUS, weight='700')
        s += '<g data-arw="%s,%s,%s,%s,minus,4"></g>' % (r(X(7.50)), r(yb+58), r(X(7.85)), r(yb+58)) + T(X(7.68), yb+88, mix='알칼리증', size=20, fill=MINUS, weight='700')
    s += T(w-x0+26, yb+30, tex='\\text{pH}', size=19, anchor='start', fill=MUTED)
    return s
F['S19'] = svg((640, 160), 600, '혈액의 적정 pH 7.35~7.45와 매우 위험한 7.0 이하, 7.8 이상', phline(600, 40, 100))
F['S21'] = svg((640, 210), 560, '혈액 pH가 7.35보다 낮아지면 산증, 7.45보다 높아지면 알칼리증', phline(600, 40, 100, True))

# ── S20 혈관
b = ''
def vessel(y):
    return '<rect x="20" y="%s" width="460" height="100" rx="50" fill="#FBE4E1" stroke="%s" stroke-width="4"/>' % (r(y), VESSEL)
b += vessel(40) + vessel(220)
b += T(250, 26, mix='젖산이 생성된 직후', size=19, fill=MUTED)
b += T(250, 212, mix='평형이 이동한 뒤', size=19, fill=MUTED)
for (x, y, k) in [(90, 72, 'h'), (210, 72, 'c'), (330, 72, 'h'), (150, 112, 'c'), (270, 112, 'h')]:
    b += pill(x, y, 96, 34, 'm' if k == 'h' else 'g', '\\ce{HCO3-}' if k == 'h' else '\\ce{H2CO3}')
b += '<g data-anim="move" data-from="0,-30" data-dur=".9" data-ease="in" data-delay=".3">' + ion(410, 100, 18, 'p') + T(410, 132, tex='\\ce{H3O+}', size=18, fill=PLUS, halo=True) + '</g>'
b += '<g data-arw="250,146,250,186,muted,3"></g>'
for (x, y, k) in [(90, 252, 'h'), (210, 252, 'c'), (150, 292, 'c'), (270, 292, 'h')]:
    b += pill(x, y, 96, 34, 'm' if k == 'h' else 'g', '\\ce{HCO3-}' if k == 'h' else '\\ce{H2CO3}')
b += '<g data-anim="move" data-from="-60,0" data-dur="1.2" data-delay=".9">' + '<circle cx="380" cy="270" r="24" fill="#FFFFFF" stroke="%s" stroke-width="2.5"/>' % MUTED + T(380, 277, tex='\\ce{CO2}', size=18) + '</g>'
b += '<g data-arw="408,270,470,270,muted,3"></g>'
b += T(447, 254, mix='폐로 배출', size=19, fill=MUTED, halo=True)
F['S20'] = svg((500, 340), 480, '혈관 속 탄산수소 이온과 탄산: 하이드로늄 이온이 들어오면 탄산이 늘고 이산화 탄소가 폐로 배출된다', b)

# ── S23 (가)+(나)→(다)
b = ''
for i, (lab, fill, nm) in enumerate([('(가)', '#F3F4F6', '\\ce{CH3COOH(aq)}'), ('(나)', '#E9F1FB', '\\ce{CH3COONa(aq)}')]):
    cx = 80+i*170
    b += beaker(cx-55, 50, 110, 120, 100, fill=fill)
    b += T(cx, 32, mix=lab, size=20, weight='700')
    b += T(cx, 196, mix='0.1 M', size=18) + T(cx, 220, tex=nm, size=18) + T(cx, 244, mix='50 mL', size=18)
b += T(165, 120, tex='+', size=26)
b += '<g data-arw="320,110,370,110,field,4"></g>'
b += beaker(395, 50, 130, 140, 80, fill='#EEF1F8')
b += '<g data-anim="scale" data-from="1,0.5" data-o="460,188" data-dur="1" data-delay=".4"><rect x="399" y="81" width="122" height="105" fill="#EEF1F8"/></g>'
b += T(460, 32, mix='(다)', size=20, weight='700') + T(460, 140, mix='(가)+(나)', size=19, weight='700')
F['S23'] = svg((550, 260), 520, '0.1 M 아세트산 수용액 50 mL (가)와 0.1 M 아세트산 나트륨 수용액 50 mL (나)를 섞어 (다)를 만든다', b)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slides.tpl.html'), encoding='utf-8').read()
out = re.sub(r'\{\{(\w+)\}\}', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('ok', len(out))
