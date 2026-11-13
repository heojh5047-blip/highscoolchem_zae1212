import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

F = {}
HAc20 = lambda V: ph(0.1, 20, V, Ka=1.8e-5)
PHC = ['#E5323B', '#EA4D35', '#EF7A2E', '#F4A52B', '#F5C928', '#E3D92E', '#A8CF3A', '#6DBE45',
       '#3FA65A', '#2E9A84', '#2E7FB8', '#3560A8', '#4B4499', '#5C338A', '#4A2470']

def svg(vb, w, label, body, cls='fig', extra=''):
    return '<svg class="%s" viewBox="0 0 %d %d" style="width:%dpx" aria-label="%s"%s>%s</svg>' % (cls, vb[0], vb[1], w, label, (' '+extra) if extra else '', body)

def pill(x, y, w, h, kind, lab=None, size=18):
    """중심 (x, y)"""
    st = {'m': ('#D6E6FA', MINUS, ''), 'p': ('#FBD5DA', PLUS, ''), 'g': ('#E3E7EC', GRAV, ''), 'w': ('#FFFFFF', GRAV, ' stroke-dasharray="4 3"')}[kind]
    s = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="2.5"%s/>' % (r(x-w/2), r(y-h/2), r(w), r(h), r(h/2), st[0], st[1], st[2])
    if lab: s += T(x, y+size*.36, tex=lab, size=size, fill=INK)
    return s

def gion(x, y, lab, rr=22, size=18):
    return ion(x, y, rr, 's', lab, size)

def phbar(x0, y0, w, h, ticks=(0, 7, 14), size=19, y_lab=None):
    o = ''
    sw = w/15
    for i in range(15):
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (r(x0+i*sw), r(y0), r(sw+.6), r(h), PHC[i])
    o += '<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1.5"/>' % (r(x0), r(y0), r(w), r(h), MUTED)
    for v in ticks:
        X = x0+(v+.5)*sw
        o += line(X, y0+h, X, y0+h+6, MUTED, 2) + T(X, (y_lab or (y0+h+6+size)), tex=str(v), size=size, fill=MUTED)
    return o

def phx(x0, w, v): return x0+(v+.5)*w/15

def diamond(x, y, s=9, c=INK):
    return '<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="#fff" stroke="%s" stroke-width="2.5"/>' % (r(x-s), r(y), r(x), r(y-s), r(x+s), r(y), r(x), r(y+s), c)

# ── S1 표지: 비커 셋 + pH 시험지
b = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
items = [('\\ce{NH4Cl(aq)}', 5, '산성', PLUS), ('\\ce{NaCl(aq)}', 7, '중성', GRAV), ('\\ce{CH3COONa(aq)}', 9, '염기성', MINUS)]
for i, (lab, p, ac, col) in enumerate(items):
    cx = 150+i*120
    b += beaker(cx-45, 170, 90, 130, 210)
    b += T(cx, 150 if i != 1 else 122, tex=lab, size=20)
    b += '<rect x="%s" y="312" width="34" height="80" rx="3" fill="#F6F1E3" stroke="%s" stroke-width="1.5"/>' % (r(cx-17), MUTED)
    b += '<g data-anim="fade" data-dur=".8" data-delay="%s"><rect x="%s" y="312" width="34" height="40" rx="3" fill="%s"/></g>' % (r(.4+i*.5), r(cx-17), PHC[p])
    b += T(cx, 422, mix='pH %d' % p, size=22, fill=INK)
    b += T(cx, 452, mix=ac, size=24, fill=col if col != GRAV else MUTED, weight='700')
F['S1'] = '<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="염화 암모늄, 염화 나트륨, 아세트산 나트륨 수용액과 pH 시험지 색: 산성, 중성, 염기성">' + b + '</svg>'

# ── S3 식품
b = ''
# 케첩 병
b += '<path d="M70 70 L100 70 L104 110 Q130 130 130 170 L130 300 Q130 316 114 316 L56 316 Q40 316 40 300 L40 170 Q40 130 66 110 Z" fill="#B8322A" stroke="#7A1F1A" stroke-width="2.5"/>'
b += '<rect x="66" y="48" width="38" height="24" rx="5" fill="#F1F3F5" stroke="%s" stroke-width="2"/>' % MUTED
b += '<rect x="52" y="190" width="66" height="54" rx="6" fill="#FFFFFF" opacity=".9"/>'
b += T(85, 224, mix='케첩', size=20, weight='700')
# 소시지
b += '<rect x="160" y="200" width="150" height="46" rx="23" fill="#B5651D" stroke="#7B4310" stroke-width="2.5" transform="rotate(-12 235 223)"/>'
b += '<rect x="168" y="250" width="150" height="46" rx="23" fill="#A85B1A" stroke="#7B4310" stroke-width="2.5" transform="rotate(-6 243 273)"/>'
b += T(240, 330, mix='소시지', size=20, weight='700')
# 빵
b += '<path d="M330 260 Q330 170 400 170 Q470 170 470 260 Z" fill="#E3B06B" stroke="#A8732F" stroke-width="2.5"/>'
b += '<path d="M352 215 Q370 200 388 215 M392 205 Q410 190 428 205 M430 218 Q446 206 458 222" fill="none" stroke="#A8732F" stroke-width="2.5" stroke-linecap="round"/>'
b += T(400, 300, mix='빵', size=20, weight='700')
b += '<g data-anim="pop" data-o="270,50" data-dur=".7" data-delay=".5"><rect x="140" y="20" width="260" height="62" rx="14" fill="#FFF8E6" stroke="%s" stroke-width="2"/>' % EQUI
b += T(270, 46, mix='아세트산 나트륨', size=20, weight='700') + T(270, 74, tex='\\ce{CH3COONa}', size=20) + '</g>'
b += '<path d="M200 82 L120 120 M270 82 L245 180 M340 82 L390 160" stroke="%s" stroke-width="1.6" stroke-dasharray="4 4" fill="none"/>' % EQUI
F['S3'] = svg((500, 350), 470, '아세트산 나트륨이 들어 있는 케첩, 소시지, 빵', b)

# ── S4 약산–강염기 곡선
ax = Axes(66, 290, 330, 240, 30, 14)
b = ax.draw([0, 10, 20, 30], [0, 7, 14], '$V_{\\ce{NaOH}}$ [mL]')
b += '<g data-anim="draw" data-dur="1.8">' + curve_pts(ax, HAc20, dense(20, 0, 30), EQUI, 3.5) + '</g>'
pe = HAc20(20)
b += line(ax.X(20), ax.y0, ax.X(20), ax.Y(pe), FIELD, 1.5, '5 4')
b += '<g data-anim="pop" data-o="%s,%s" data-delay="1.6" data-dur=".6">%s</g>' % (r(ax.X(20)), r(ax.Y(pe)), dot(ax.X(20), ax.Y(pe), FIELD, 7))
b += T(ax.X(20)+14, ax.Y(pe)+28, mix='중화점 pH 8.7', size=20, anchor='start', fill=FIELD, weight='700', halo=True)
b += T(ax.X(2)+4, ax.Y(HAc20(0))-36, mix='$0.1\\ \\text{M}$ $\\ce{CH3COOH}$ 20 mL', size=19, anchor='start', fill=EQUI, halo=True)
F['S4'] = svg((440, 370), 420, '0.1 M 아세트산 20 mL를 0.1 M 수산화 나트륨 수용액으로 적정한 곡선. 중화점 20 mL에서 pH 8.7', b)

# ── S5 NaCl 수용액
b = '<rect x="10" y="20" width="400" height="230" rx="14" fill="#F2F8FD" stroke="%s" stroke-width="2"/>' % WATER_S
pos = [(70, 80, 'Na+'), (200, 70, 'Cl-'), (330, 85, 'Na+'), (120, 190, 'Cl-'), (260, 175, 'Na+'), (360, 200, 'Cl-')]
for i, (x, y, k) in enumerate(pos):
    dx, dy = (190+(i % 2)*44-22-x, 140-(i//2)*0+((i % 3)-1)*20-y)
    b += '<g data-anim="move" data-from="%s,%s" data-dur="1.2" data-delay="%s">%s</g>' % (r(dx*.8), r(dy*.8), r(.2+i*.08), gion(x, y, '\\ce{%s}' % k))
for (x, y) in [(140, 115), (290, 125), (55, 150), (205, 220), (380, 140)]:
    b += ion(x, y, 11, 'w')
b += T(210, 284, mix='물 분자(점선 원) 사이에 흩어진 이온 — pH 7, 중성', size=19, fill=MUTED)
F['S5'] = svg((420, 300), 410, '염화 나트륨 수용액: 나트륨 이온과 염화 이온이 물 분자 사이에 흩어져 있고 pH 7', b)

# ── 가수 분해 두 칸 (S6, S10)
def hyd(kind):
    o = ''
    for px, title in [(5, '(가) 녹은 직후'), (305, '(나) 물과 반응한 뒤')]:
        o += '<rect x="%d" y="30" width="260" height="250" rx="14" fill="#F2F8FD" stroke="%s" stroke-width="2"/>' % (px, WATER_S)
        o += T(px+130, 20, mix=title, size=20, fill=MUTED)
    o += '<g data-arw="270,155,300,155,muted,3"></g>'
    if kind == 'ac':
        A = lambda x, y: pill(x, y, 100, 38, 'm', '\\ce{CH3COO-}', 18)
        Bs = lambda x, y: gion(x, y, '\\ce{Na+}')
    else:
        A = lambda x, y: pill(x, y, 76, 38, 'p', '\\ce{NH4+}', 18)
        Bs = lambda x, y: gion(x, y, '\\ce{Cl-}')
    W = lambda x, y: pill(x, y, 70, 34, 'w', '\\ce{H2O}', 18)
    o += ''.join(A(5+x, y) for (x, y) in [(70, 75), (195, 130), (75, 245)])
    o += ''.join(Bs(5+x, y) for (x, y) in [(200, 70), (50, 160), (210, 240)])
    o += W(5+130, 190)
    if kind == 'ac':
        o += '<g data-arw="160,176,180,151,plus,3"></g>' + T(186, 178, tex='\\ce{H+}', size=18, anchor='start', fill=PLUS, halo=True)
    else:
        o += '<g data-arw="188,151,166,174,plus,3"></g>' + T(186, 180, tex='\\ce{H+}', size=18, anchor='start', fill=PLUS, halo=True)
    ox = 305
    o += ''.join(A(ox+x, y) for (x, y) in [(70, 75), (75, 245)])
    o += ''.join(Bs(ox+x, y) for (x, y) in [(200, 70), (50, 160), (210, 240)])
    if kind == 'ac':
        o += '<g data-anim="move" data-from="30,30" data-dur="1" data-delay=".6">' + pill(ox+190, 138, 108, 38, 'g', '\\ce{CH3COOH}', 18) + '</g>'
    else:
        o += '<g data-anim="move" data-from="-10,0" data-dur="1" data-delay=".6">' + pill(ox+200, 138, 68, 38, 'g', '\\ce{NH3}', 18) + '</g>'
    c, lab = ('m', '\\ce{OH-}') if kind == 'ac' else ('p', '\\ce{H3O+}')
    o += '<g data-anim="pop" data-o="%d,190" data-dur=".7" data-delay="1.2">' % (ox+130) + ion(ox+130, 176, 20, c) + T(ox+130, 214, tex=lab, size=18, fill=MINUS if c == 'm' else PLUS, halo=True) + '</g>'
    return o
F['S6'] = svg((570, 290), 560, '아세트산 나트륨 수용액: 녹은 직후 아세트산 이온, 나트륨 이온, 물. 물 분자가 아세트산 이온에 수소 이온을 주어 아세트산 분자와 수산화 이온이 생긴다', hyd('ac'))
F['S10'] = svg((570, 290), 560, '염화 암모늄 수용액: 녹은 직후 암모늄 이온, 염화 이온, 물. 암모늄 이온이 물에 수소 이온을 주어 암모니아와 하이드로늄 이온이 생긴다', hyd('am'))

# ── S11 pH 막대 + 세 염
x0, w = 20, 480
b = phbar(x0, 120, w, 34, ticks=(0, 7, 14))
for i, (lab, v, c) in enumerate([('\\ce{NH4Cl}', 5.1, PLUS), ('\\ce{NaCl}', 7.0, MUTED), ('\\ce{CH3COONa}', 8.9, MINUS)]):
    X = phx(x0, w, v)
    b += '<g data-anim="pop" data-o="%s,110" data-dur=".6" data-delay="%s">' % (r(X), r(.3+i*.35))
    b += '<path d="M%s 112 L%s 96 L%s 96 Z" fill="%s"/>' % (r(X), r(X-9), r(X+9), INK)
    b += T(X, 22 if i == 1 else 54, tex=lab, size=20, fill=INK) + T(X, 84, mix='%.1f' % v, size=19, fill=c if c != MUTED else INK, weight='700') + '</g>'
b += T(phx(x0, w, 1.5), 210, mix='← 산성', size=19, fill=PLUS, weight='700') + T(phx(x0, w, 12.5), 210, mix='염기성 →', size=19, fill=MINUS, weight='700')
F['S11'] = svg((520, 222), 500, 'pH 막대 위의 0.1 M 염 수용액: 염화 암모늄 5.1, 염화 나트륨 7.0, 아세트산 나트륨 8.9', b)

# ── S17 pH 시험지 과정
b = ''
b += beaker(30, 120, 110, 120, 160) + T(85, 108, tex='\\ce{CH3COONa(aq)}', size=19)
b += beaker(190, 120, 110, 120, 160) + T(245, 108, tex='\\ce{NH4Cl(aq)}', size=19)
# 흰 타일 위 시험지
b += '<rect x="340" y="190" width="170" height="40" rx="6" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % MUTED
b += '<rect x="356" y="198" width="54" height="24" rx="2" fill="#F6F1E3" stroke="%s" stroke-width="1.2"/>' % MUTED
b += '<rect x="440" y="198" width="54" height="24" rx="2" fill="#F6F1E3" stroke="%s" stroke-width="1.2"/>' % MUTED
b += '<g data-anim="fade" data-dur=".8" data-delay="1.1"><circle cx="383" cy="210" r="11" fill="%s"/><circle cx="467" cy="210" r="11" fill="%s"/></g>' % (PHC[9], PHC[5])
b += '<g data-anim="move" data-from="-120,-60" data-dur="1.1" data-ease="soft"><line x1="330" y1="80" x2="380" y2="196" stroke="#7E8B98" stroke-width="6" stroke-linecap="round"/><line x1="330" y1="80" x2="380" y2="196" stroke="#EEF3F8" stroke-width="2.5" stroke-linecap="round"/></g>'
b += T(330, 70, mix='유리 막대', size=19, anchor='end', fill=MUTED)
b += T(383, 258, mix='①', size=19) + T(467, 258, mix='②', size=19)
# 색표
cx0, cw = 30, 480
for i in range(15):
    b += '<rect x="%s" y="282" width="%s" height="22" fill="%s"/>' % (r(cx0+i*cw/15), r(cw/15+.6), PHC[i])
b += '<rect x="%d" y="282" width="%d" height="22" fill="none" stroke="%s" stroke-width="1.2"/>' % (cx0, cw, MUTED)
for v in (0, 7, 14):
    b += T(cx0+(v+.5)*cw/15, 326, tex=str(v), size=19, fill=MUTED)
b += T(cx0+cw+10, 300, mix='색표', size=19, anchor='start', fill=MUTED)
F['S17'] = svg((560, 336), 520, '유리 막대로 두 염 수용액을 pH 시험지에 묻히고 색표와 비교하는 과정', b)

# ── S19 결과 비교 막대
x0, w = 170, 450
b = ''
for i, (lab, pv, mv) in enumerate([('\\ce{CH3COONa(aq)}', 8.9, 9.0), ('\\ce{NH4Cl(aq)}', 5.1, 5.0)]):
    y = 50+i*70
    b += T(155, y+7, tex=lab, size=19, anchor='end')
    b += line(x0, y, x0+w, y, '#D5DCE3', 2)
    b += '<g data-anim="pop" data-o="%s,%s" data-dur=".6" data-delay="%s">%s</g>' % (r(phx(x0, w, pv)), y, r(.3+i*.3), diamond(phx(x0, w, pv), y))
    b += '<g data-anim="pop" data-o="%s,%s" data-dur=".6" data-delay="%s"><circle cx="%s" cy="%s" r="7" fill="%s"/></g>' % (r(phx(x0, w, mv)), y, r(.5+i*.3), r(phx(x0, w, mv)), y+16, EQUI)
b += phbar(x0, 160, w, 22, ticks=(0, 5, 7, 9, 14), size=19)
b += diamond(200, 238, 8) + T(216, 245, mix='예측한 값(계산)', size=19, anchor='start')
b += '<circle cx="400" cy="238" r="7" fill="%s"/>' % EQUI + T(414, 245, mix='실험 결과(예시)', size=19, anchor='start')
F['S19'] = svg((640, 256), 600, '예측한 pH와 실험 결과: 아세트산 나트륨 8.9와 약 9.0, 염화 암모늄 5.1과 약 5.0', b)

# ── S22 중화점 곡선 + 비커 입자
ax = Axes(60, 280, 300, 230, 30, 14)
b = ax.draw([0, 10, 20, 30], [0, 7, 14], '$V$ [mL]')
b += '<g data-anim="draw" data-dur="1.6">' + curve_pts(ax, HAc20, dense(20, 0, 30), EQUI, 3.5) + '</g>'
b += dot(ax.X(20), ax.Y(pe), FIELD, 7)
b += T(ax.X(20)-12, ax.Y(pe)-14, mix='중화점', size=19, anchor='end', fill=FIELD, weight='700', halo=True)
b += line(ax.X(20)+8, ax.Y(pe), 420, 120, MUTED, 1.2, '3 4')
b += '<rect x="420" y="40" width="200" height="230" rx="14" fill="#F2F8FD" stroke="%s" stroke-width="2"/>' % WATER_S
b += T(520, 30, mix='중화점의 수용액', size=19, fill=MUTED)
for (x, y) in [(480, 80), (560, 170), (490, 235)]: b += pill(x, y, 104, 36, 'm', '\\ce{CH3COO-}', 18)
for (x, y) in [(580, 85), (460, 160), (590, 240)]: b += gion(x, y, '\\ce{Na+}')
b += '<g data-anim="pop" data-o="530,128" data-dur=".6" data-delay="1.4">' + ion(530, 128, 17, 'm') + T(552, 134, tex='\\ce{OH-}', size=18, anchor='start', fill=MINUS, halo=True) + '</g>'
F['S22'] = svg((640, 356), 600, '약산을 강염기로 적정한 곡선의 중화점과 그 수용액 속 아세트산 이온, 나트륨 이온, 가수 분해로 생긴 수산화 이온', b)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slides.tpl.html'), encoding='utf-8').read()
out = re.sub(r'\{\{(\w+)\}\}', lambda m: F[m.group(1)], tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('ok', len(out))
