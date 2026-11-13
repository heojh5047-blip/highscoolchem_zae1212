import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

F = {}
HCl20 = lambda V: ph(0.1, 20, V)
HAc20 = lambda V: ph(0.1, 20, V, Ka=1.8e-5)
HCl100 = lambda V: ph(0.1, 100, V)

def svg(vb, w, label, body, cls='fig', extra=''):
    return '<svg class="%s" viewBox="0 0 %d %d" style="width:%dpx" aria-label="%s"%s>%s</svg>' % (cls, vb[0], vb[1], w, label, (' '+extra) if extra else '', body)

# ── S1 표지
b = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
b += stand(40, 470, 60, 40, 80, 150)
bs, tip = burette(150, 40, 5, 0, labels=False)
b += bs
b += beaker(100, 380, 100, 90, 420)
b += stirrer(85, 472, 130, 20)
b += '<g data-anim="fade" data-dur=".5" data-rep="loop" data-delay=".2"><ellipse cx="150" cy="372" rx="3.5" ry="4.5" fill="%s"/></g>' % WATER_S
ax = Axes(260, 420, 190, 290, 30, 14)
b += line(ax.x0, ax.y0, ax.x0+ax.w+8, ax.y0, MUTED, 2) + line(ax.x0, ax.y0, ax.x0, ax.y0-ax.h-8, MUTED, 2)
b += line(ax.x0, ax.Y(7), ax.x0+ax.w, ax.Y(7), GRAV, 1.5, '6 5')
b += '<g data-anim="draw" data-dur="2">' + curve_pts(ax, HCl20, dense(20, 0, 30), INK, 4) + '</g>'
b += '<g data-anim="pop" data-o="%s,%s" data-delay="1.6" data-dur=".6">%s</g>' % (r(ax.X(20)), r(ax.Y(7)), dot(ax.X(20), ax.Y(7), FIELD, 8))
b += T(ax.x0+10, ax.y0-ax.h+4, tex='\\text{pH}', size=24, anchor='start', fill=MUTED)
b += T(ax.X(20)+14, ax.Y(7)+30, mix='중화점', size=24, anchor='start', fill=FIELD, weight='700')
b += T(ax.x0+4, ax.y0+34, mix='넣은 염기의 부피 →', size=22, anchor='start', fill=MUTED)
F['S1'] = '<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="뷰렛으로 염기 표준 용액을 넣는 장치와 중화 적정 곡선">' + b + '</svg>'

# ── S3 시약병
b = '<path d="M150 40 L230 40 L230 80 Q290 100 290 160 L290 320 Q290 340 270 340 L110 340 Q90 340 90 320 L90 160 Q90 100 150 80 Z" fill="#F4F7FA" stroke="%s" stroke-width="3"/>' % GLASS
b += '<rect x="140" y="20" width="100" height="26" rx="6" fill="#5B6B7F"/>'
b += '<path d="M93 230 L287 230 L287 320 Q287 337 270 337 L110 337 Q93 337 93 320 Z" fill="%s"/>' % WATER
b += line(93, 230, 287, 230, WATER_S, 2)
b += '<rect x="115" y="140" width="150" height="70" rx="6" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % MUTED
b += T(190, 170, mix='묽은 염산', size=24, weight='700')
b += T(190, 200, mix='? M', size=24, fill=PLUS, weight='700')
b += '<g data-anim="fade" data-dur="1.2" data-delay=".6"><ellipse cx="215" cy="190" rx="44" ry="22" fill="#9FC3DD" opacity=".55"/><ellipse cx="180" cy="200" rx="22" ry="12" fill="#9FC3DD" opacity=".45"/></g>'
b += T(190, 372, mix='농도 표시가 물에 젖어 지워졌다', size=20, fill=MUTED)
F['S3'] = svg((380, 390), 360, '농도 표시가 물에 젖어 지워진 묽은 염산 시약병', b)

# ── S4 입자
b = ''
def box(x, y, w, h, title):
    return '<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#F6F9FC" stroke="%s" stroke-width="2"/>' % (x, y, w, h, GLASS) + T(x+w/2, y-10, mix=title, size=20, fill=MUTED)
b += box(10, 40, 170, 150, '염산')
for i, (x, y) in enumerate([(45, 80), (110, 75), (75, 150)]): b += ion(x, y, 20, 'p', '\\ce{H3O+}', 15) if False else ion(x, y, 18, 'p')
for (x, y) in [(145, 120), (50, 120), (140, 165)]: b += ion(x, y, 20, 's', '\\ce{Cl-}', 18)
b += T(205, 125, tex='+', size=30, fill=INK)
b += box(230, 40, 170, 150, '수산화 나트륨 수용액')
for (x, y) in [(265, 80), (330, 75), (295, 150)]: b += ion(x, y, 18, 'm')
for (x, y) in [(365, 120), (270, 120), (360, 165)]: b += ion(x, y, 20, 's', '\\ce{Na+}', 18)
b += '<g data-arw="412,115,452,115,muted,3"></g>'
b += box(464, 40, 196, 150, '중화 후')
b += '<g data-anim="fade" data-dur=".9" data-delay=".6">'
for (x, y) in [(490, 72), (530, 70), (570, 72), (610, 70), (495, 168), (635, 168)]: b += ion(x, y, 14, 'w')
for (x, y) in [(500, 120), (590, 120), (545, 168)]: b += ion(x, y, 20, 's', '\\ce{Cl-}', 18)
for (x, y) in [(545, 120), (635, 120), (590, 168)]: b += ion(x, y, 20, 's', '\\ce{Na+}', 18)
b += ion(640, 120, 20, 's', '\\ce{Na+}', 18) if False else ''
b += '</g>'
# 범례
b += ion(30, 226, 11, 'p') + T(48, 233, tex='\\ce{H3O+}', size=19, anchor='start')
b += ion(150, 226, 11, 'm') + T(168, 233, tex='\\ce{OH-}', size=19, anchor='start')
b += ion(262, 226, 10, 'w') + T(280, 233, mix='물 분자', size=19, anchor='start')
b += '<circle cx="395" cy="226" r="11" fill="#E3E7EC" stroke="%s" stroke-width="2"/>' % GRAV + T(413, 233, mix='구경꾼 이온', size=19, anchor='start')
F['S4'] = svg((670, 250), 640, '염산과 수산화 나트륨 수용액이 중화하여 물이 생기고 염화 이온과 나트륨 이온은 그대로 남는 입자 모형', b)

# ── S5 기구
b = stand(10, 410, 30, 20, 60, 130)
bs, tip = burette(130, 20, 5, 4, lsize=19)
b += bs
b += '<g data-anim="fade" data-dur=".5" data-rep="loop"><ellipse cx="130" cy="%s" rx="3.5" ry="4.5" fill="%s"/></g>' % (r(tip+14), WATER_S)
b += beaker(85, 330, 90, 78, 362)
b += T(160, 70, mix='뷰렛', size=20, anchor='start', weight='700')
b += T(160, 96, mix='표준 용액', size=20, anchor='start', fill=MINUS)
b += T(160, 120, tex='0.1\\ \\text{M}\\ \\ce{NaOH(aq)}', size=20, anchor='start', fill=MINUS)
b += T(190, 372, mix='농도를 모르는', size=20, anchor='start')
b += T(190, 398, tex='\\ce{HCl(aq)}', size=20, anchor='start', fill=PLUS)
b += T(30, 452, mix='뷰렛 눈금은 위가 0', size=19, anchor='start', fill=MUTED)
F['S5'] = svg((340, 468), 320, '스탠드에 고정한 뷰렛에 수산화 나트륨 표준 용액을 넣고 농도를 모르는 염산이 든 비커에 떨어뜨리는 장치', b)

# ── S7 예상 그래프 3
def mini(fn, title, idx):
    ax = Axes(48, 158, 220, 130, 30, 14)
    o = ax.draw([0, 20], [7], '$V$ [mL]', size=19)
    o += '<g data-anim="draw" data-dur="1.2" data-delay="%s">' % (0.3*idx) + curve_pts(ax, fn, [i*0.05 for i in range(601)], INK, 3.5) + '</g>'
    return svg((300, 225), 300, title, o)
F['S7a'] = mini(lambda V: 1+V*0.4, '부피에 비례하여 pH가 일정하게 증가하는 직선', 0)
F['S7b'] = mini(HCl20, '처음에는 천천히, 20 mL 근처에서 급격히 증가한 뒤 다시 천천히 증가하는 곡선', 1)
F['S7c'] = mini(lambda V: 12-11*math.exp(-V/1.2), '처음부터 급격히 증가한 뒤 거의 일정한 곡선', 2)

# ── S8 단계 카드
# 카드1: 깔때기로 채우고 3방울 흘리기
b = stand(10, 186, 30, 8, 40, 110)
bs, tip = burette(110, 30, 2.2, 0, labels=False, stop_gap=14, tip_len=14)
b += bs
b += '<path d="M92 4 L128 4 L114 22 L114 34 L106 34 L106 22 Z" fill="#F4F7FA" stroke="%s" stroke-width="2"/>' % GLASS
b += beaker(160, 140, 70, 46, 168)
b += '<g data-anim="fade" data-dur=".5" data-rep="loop"><ellipse cx="110" cy="%s" rx="3" ry="4" fill="%s"/></g>' % (r(tip+10), WATER_S)
b += T(196, 128, mix='3방울', size=19, fill=MUTED)
b += T(150, 30, mix='깔때기', size=19, anchor='start', fill=MUTED)
F['S8a'] = svg((260, 200), 240, '깔때기로 뷰렛에 표준 용액을 넣고 꼭지를 열어 3방울 정도 흘리는 모습', b)
# 카드2: 눈금 확대
b = '<rect x="20" y="10" width="220" height="170" rx="10" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % INK
cx = 110; PP = 120  # 1 mL = 120 px, 3 mL at y=40
RD = 0.39  # 3.39 mL (지도서 예시 답안)
y0 = 40
b += '<rect x="%d" y="%s" width="60" height="%s" fill="%s"/>' % (cx-30, r(y0+RD*PP), r(180-(y0+RD*PP)), WATER)
b += '<path d="M%d %s Q%d %s %d %s Q%d %s %d %s" fill="none" stroke="%s" stroke-width="2.4"/>' % (cx-30, r(y0+RD*PP-10), cx-21, r(y0+RD*PP), cx, r(y0+RD*PP), cx+21, r(y0+RD*PP), cx+30, r(y0+RD*PP-10), WATER_S)
b += line(cx-30, 12, cx-30, 178, GLASS, 2.6) + line(cx+30, 12, cx+30, 178, GLASS, 2.6)
for t in range(0, 12):
    y = y0+t*PP/10
    L = 30 if t % 10 == 0 else (20 if t % 5 == 0 else 11)
    b += line(cx-30, y, cx-30+L, y, INK if t % 10 == 0 else MUTED, 2 if t % 10 == 0 else 1.2)
b += T(cx-40, y0+7, tex='3', size=20, anchor='end') + T(cx-40, y0+PP+7, tex='4', size=20, anchor='end')
b += line(cx-36, y0+RD*PP, 238, y0+RD*PP, PLUS, 2, '5 4')
b += T(232, y0+RD*PP-8, mix='눈높이', size=19, anchor='end', fill=PLUS)
F['S8b'] = svg((260, 190), 240, '뷰렛 눈금 확대: 메니스커스 아래쪽이 3.39 mL 눈금에 있다', b)
# 카드3: 피펫으로 염산 20 mL + 자석
b = beaker(70, 100, 120, 80, 140)
b += '<rect x="110" y="160" width="40" height="9" rx="4" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % STAND
b += line(130, 10, 130, 118, GLASS, 5, extra='stroke-linecap="round"')
b += '<ellipse cx="130" cy="44" rx="10" ry="16" fill="%s" stroke="%s" stroke-width="2"/>' % (WATER, GLASS)
b += '<rect x="120" y="0" width="20" height="14" rx="5" fill="#E04A4A"/>'
b += T(200, 40, mix='피펫 필러', size=19, anchor='start', fill=MUTED)
b += line(145, 7, 196, 34, MUTED, 1.5)
b += T(200, 130, tex='\\ce{HCl(aq)}', size=19, anchor='start', fill=PLUS)
b += T(200, 154, tex='20\\ \\text{mL}', size=19, anchor='start', fill=PLUS)
b += T(40, 196, mix='자석', size=19, anchor='start', fill=MUTED) + line(70, 190, 112, 168, MUTED, 1.5)
F['S8c'] = svg((290, 205), 260, '피펫과 피펫 필러로 염산 20 mL를 비커에 옮기고 자석을 넣은 모습', b)

# ── S9 장치
b = stand(10, 410, 34, 20, 62, 170)
bs, tip = burette(170, 20, 5, 6, lsize=19)
b += bs
b += '<g data-anim="fade" data-dur=".5" data-rep="loop"><ellipse cx="170" cy="%s" rx="3.5" ry="4.5" fill="%s"/></g>' % (r(tip+12), WATER_S)
b += beaker(115, 300, 120, 80, 330)
b += '<rect x="160" y="362" width="36" height="8" rx="4" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % STAND
b += '<g data-anim="move" data-from="0,-40" data-dur="1" data-delay=".4" data-ease="out">' + sensor(138, 230, 358) + '</g>'
b += '<path d="M138 232 Q120 180 60 170" fill="none" stroke="#3A3F47" stroke-width="2.5"/>'
b += stirrer(95, 384, 160, 24)
b += T(196, 82, mix='뷰렛', size=20, anchor='start', weight='700')
b += T(196, 108, tex='\\ce{NaOH(aq)}', size=20, anchor='start', fill=MINUS)
b += T(60, 160, mix='pH 센서', size=20, anchor='middle')
b += T(250, 330, tex='\\ce{HCl(aq)}', size=20, anchor='start', fill=PLUS)
b += T(250, 360, mix='자석', size=20, anchor='start') + line(246, 355, 198, 366, MUTED, 1.5)
b += T(266, 404, mix='자석 젓개', size=20, anchor='start')
# 태블릿
b += '<rect x="310" y="130" width="160" height="110" rx="10" fill="#16233D"/><rect x="318" y="138" width="144" height="94" rx="4" fill="#FFFFFF"/>'
axm = Axes(332, 222, 120, 74, 30, 14)
b += line(axm.x0, axm.y0, axm.x0+axm.w, axm.y0, MUTED, 1.5) + line(axm.x0, axm.y0, axm.x0, axm.y0-axm.h, MUTED, 1.5)
b += '<g data-anim="draw" data-dur="1.6" data-delay=".8">' + curve_pts(axm, HCl20, dense(20, 0, 23), INK, 2.5) + '</g>'
b += T(390, 266, mix='스마트 기기', size=19, fill=MUTED)
F['S9'] = svg((480, 430), 440, '스탠드의 뷰렛, pH 센서를 담근 염산 비커, 자석 젓개와 데이터를 받는 스마트 기기', b)

# ── S11 결과 그래프
DATA = [(0, 1.01), (5, 1.23), (10, 1.49), (15, 1.86), (18, 2.29), (19, 2.60), (20, 6.95), (21, 11.38), (22, 11.67), (23, 11.85)]
ax = Axes(62, 300, 400, 260, 25, 14)
b = ax.draw([0, 5, 10, 15, 20, 25], [0, 7, 14], '$V_{\\ce{NaOH}}$ [mL]')
b += '<g class="step" data-g="g1">'
b += '<g data-anim="draw" data-dur="1.6" data-on="step">' + curve_pts(ax, HCl20, dense(20, 0, 23), INK, 3) + '</g>'
for v, p in DATA: b += dot(ax.X(v), ax.Y(p), INK, 6)
b += '</g>'
F['S11'] = svg((500, 360), 470, '넣어 준 수산화 나트륨 수용액의 부피에 따른 pH 예시 데이터와 중화 적정 곡선', b)


# ── S12 세 구간
ax = Axes(62, 290, 380, 250, 25, 14)
b = ax.draw([0, 5, 10, 15, 20, 25], [0, 7, 14], '$V_{\\ce{NaOH}}$ [mL]')
for (a1, a2, c, lab, g_) in [(0, 19, '#FDE2E4', '①', 'k1'), (19, 21, '#FFF3B0', '②', 'k2'), (21, 25, '#E3EEFB', '③', 'k3')]:
    b += '<g class="step" data-g="%s"><rect x="%s" y="%s" width="%s" height="%s" fill="%s" opacity=".8"/>' % (g_, r(ax.X(a1)), r(ax.Y(14)), r(ax.X(a2)-ax.X(a1)), r(ax.h), c) + T((ax.X(a1)+ax.X(a2))/2, ax.Y(14)+24, mix=lab, size=22, weight='700') + '</g>'
b += curve_pts(ax, HCl20, dense(20, 0, 25), INK, 3.5)
b += '<g class="step" data-g="k2">' + dot(ax.X(20), ax.Y(7), FIELD, 7) + T(ax.X(20)+12, ax.Y(7)+30, mix='중화점', size=20, anchor='start', fill=FIELD, weight='700', halo=True) + '</g>'
F['S12'] = svg((480, 356), 440, '적정 곡선을 천천히 증가하는 구간, 급격히 증가하는 구간, 다시 천천히 증가하는 구간으로 나눈 그림', b)

# ── S13 가운데 부피 읽기
ax = Axes(56, 200, 300, 160, 25, 14)
b = ax.draw([0, 10, 20], [0, 7, 14], '$V$ [mL]')
b += curve_pts(ax, HCl20, dense(20, 0, 25), INK, 3)
b += '<rect x="%s" y="%s" width="%s" height="%s" fill="#FFE45C" opacity=".35"/>' % (r(ax.X(19)), r(ax.Y(14)), r(ax.X(21)-ax.X(19)), r(ax.h))
b += '<g data-anim="move" data-from="-60,0" data-dur="1" data-ease="out">' + line(ax.X(20), ax.y0, ax.X(20), ax.Y(13), FIELD, 2.5, '5 4') + '</g>'
b += T(ax.X(20)+10, ax.Y(3), mix='급변 구간의||가운데', size=19, anchor='start', fill=FIELD, weight='700', halo=True)
F['S13'] = svg((400, 262), 380, '적정 곡선에서 pH가 급격히 변하는 구간의 가운데 부피 20 mL를 읽는 그림', b)

# ── S15 교과서 그림 I-4 꼴
ax = Axes(70, 330, 460, 280, 120, 12)
b = ax.draw([0, 25, 50, 75, 100], [0, 2, 4, 6, 8, 10, 12], '넣은 $0.1\\ \\text{M}\\ \\ce{NaOH(aq)}$의 부피 $V$ [mL]')
b += '<g data-anim="draw" data-dur="2">' + curve_pts(ax, HCl100, dense(100, 0, 120, 400), INK, 3.5) + '</g>'
b += line(ax.X(100), ax.y0, ax.X(100), ax.Y(7), FIELD, 2, '5 4') + line(ax.x0, ax.Y(7), ax.X(100), ax.Y(7), FIELD, 2, '5 4')
b += dot(ax.X(50), ax.Y(HCl100(50)), INK, 6, '#FFFFFF') + dot(ax.X(101), ax.Y(HCl100(101)), INK, 6, '#FFFFFF')
b += dot(ax.X(100), ax.Y(7), FIELD, 8)
b += T(ax.X(50), ax.Y(HCl100(50))-16, tex='50\\ \\text{mL}', size=19, halo=True)
b += T(ax.X(101)-12, ax.Y(HCl100(101))+4, tex='101\\ \\text{mL}', size=19, anchor='end', halo=True)
b += T(ax.X(100)+14, ax.Y(7)+7, mix='중화점', size=21, anchor='start', fill=FIELD, weight='700', halo=True)
F['S15'] = svg((560, 400), 540, '0.1 M 염산 100 mL를 0.1 M 수산화 나트륨 수용액으로 적정할 때의 중화 적정 곡선. 100 mL에서 pH가 급격히 변하며 중화점의 pH는 7이다', b)

# ── 막대 (S16, S18)
def bars(vals, labs, cols, unit, label, maxv):
    b = line(40, 220, 400, 220, MUTED, 2)
    for i, (v, l, c) in enumerate(zip(vals, labs, cols)):
        x = 70+i*120; h = v/maxv*170
        b += '<g data-anim="scale" data-from="1,0" data-o="%d,220" data-dur=".8" data-delay="%s"><rect x="%d" y="%s" width="64" height="%s" fill="%s" opacity=".85"/></g>' % (x+32, 0.4*i, x, r(220-h), r(h), c)
        b += T(x+32, 212-h, tex=unit[i], size=19)
        b += T(x+32, 248, mix=l[0], size=19) + T(x+32, 272, mix=l[1], size=19)
    return svg((420, 285), 400, label, b)
F['S16'] = bars([0.01, 0.005, 0.005], [('처음', '$\\ce{H3O+}$'), ('넣은', '$\\ce{OH-}$'), ('남은', '$\\ce{H3O+}$')], [PLUS, MINUS, PLUS], ['0.01', '0.005', '0.005'], '처음 H3O+ 0.01 mol, 넣은 OH- 0.005 mol, 남은 H3O+ 0.005 mol 막대그래프', 0.0105)
F['S18'] = bars([0.01, 0.0101, 0.0001], [('처음', '$\\ce{H3O+}$'), ('넣은', '$\\ce{OH-}$'), ('남은', '$\\ce{OH-}$')], [PLUS, MINUS, MINUS], ['0.0100', '0.0101', '0.0001'], '처음 H3O+ 0.0100 mol, 넣은 OH- 0.0101 mol, 남은 OH- 0.0001 mol 막대그래프', 0.0105)

# ── S17 두 구간 강조
ax = Axes(66, 300, 400, 250, 120, 14)
b = ax.draw([0, 50, 90, 100], [0, 7, 14], '$V$ [mL]', ph7=True)
b += '<rect x="%s" y="%s" width="%s" height="%s" fill="#FFE45C" opacity=".35"/>' % (r(ax.X(0)), r(ax.Y(14)), r(ax.X(90)-ax.X(0)), r(ax.h))
b += '<rect x="%s" y="%s" width="%s" height="%s" fill="#FDE2E4" opacity=".8"/>' % (r(ax.X(99)), r(ax.Y(14)), r(ax.X(101)-ax.X(99)+2), r(ax.h))
b += curve_pts(ax, HCl100, dense(100, 0, 120, 400), INK, 3.5)
b += T(ax.X(45), ax.Y(5), mix='90 mL 동안||pH 1.0 → 2.3', size=20, halo=True)
b += '<g class="step" data-g="z2">' + T(ax.X(99)-8, ax.Y(12.2), mix='2 mL 동안||pH 3.3 → 10.7', size=20, anchor='end', fill=PLUS, halo=True) + '</g>'
F['S17'] = svg((500, 360), 460, '0에서 90 mL까지는 pH가 1.3 증가하고 99에서 101 mL까지 2 mL 동안 pH가 7.4 증가하는 곡선', b)

# ── S19 미지 농도 염산 25 mL
U = lambda V: ph(0.08, 25, V)
ax = Axes(60, 276, 380, 230, 30, 14)
b = ax.draw([0, 10, 20, 30], [0, 7, 14], '$V_{\\ce{NaOH}}$ [mL]')
b += '<g data-anim="draw" data-dur="1.6">' + curve_pts(ax, U, dense(20, 0, 30), INK, 3.5) + '</g>'
b += '<g class="step" data-g="u1">' + line(ax.X(20), ax.y0, ax.X(20), ax.Y(7), FIELD, 2, '5 4') + dot(ax.X(20), ax.Y(7), FIELD, 8) + T(ax.X(20)+12, ax.Y(7)+30, mix='중화점 20 mL', size=20, anchor='start', fill=FIELD, weight='700', halo=True) + '</g>'
F['S19'] = svg((470, 340), 450, '농도를 모르는 염산 25 mL를 0.1 M 수산화 나트륨 수용액으로 적정한 곡선, 중화점 20 mL', b)

# ── S21 두 곡선
ax = Axes(66, 330, 470, 290, 30, 14)
b = ax.draw([0, 10, 20, 30], [0, 2, 4, 6, 8, 10, 12, 14], '넣은 $0.1\\ \\text{M}\\ \\ce{NaOH(aq)}$의 부피 $V$ [mL]')
b += '<g data-anim="draw" data-dur="1.6">' + curve_pts(ax, HCl20, dense(20, 0, 30), INK, 3.5) + '</g>'
b += '<g data-anim="draw" data-dur="1.6" data-delay="1.6">' + curve_pts(ax, HAc20, dense(20, 0, 30), EQUI, 3.5) + '</g>'
b += dot(ax.X(20), ax.Y(7), INK, 6) + dot(ax.X(20), ax.Y(HAc20(20)), EQUI, 6)
b += line(ax.X(20), ax.y0, ax.X(20), ax.Y(12), FIELD, 2, '5 4')
b += T(ax.X(20)+10, ax.Y(7)+8, tex='7.0', size=19, anchor='start', halo=True)
b += T(ax.X(20)-10, ax.Y(HAc20(20))+4, tex='8.7', size=19, anchor='end', fill=EQUI, halo=True)
b += T(ax.X(20), ax.Y(12)-10, mix='중화점 20 mL', size=19, fill=FIELD, weight='700')
# 범례
b += line(430, 236, 462, 236, INK, 3.5) + T(470, 243, tex='\\ce{HCl}', size=19, anchor='start')
b += line(430, 266, 462, 266, EQUI, 3.5) + T(470, 273, tex='\\ce{CH3COOH}', size=19, anchor='start')
b += T(430, 300, mix='(각 0.1 M, 20 mL)', size=19, anchor='start', fill=MUTED)
F['S21'] = svg((580, 400), 560, '0.1 M 염산과 0.1 M 아세트산 수용액 각 20 mL를 0.1 M 수산화 나트륨 수용액으로 적정한 두 곡선. 중화점 부피는 20 mL로 같고 처음 pH와 중화점 pH가 다르다', b)

# ── S22 지시약 띠 + 약산 곡선
ax = Axes(66, 300, 400, 250, 30, 14)
b = ax.draw([0, 10, 20, 30], [0, 7, 14], '$V$ [mL]')
b += '<g data-anim="fade" data-dur=".8" data-delay=".3"><rect x="%s" y="%s" width="%s" height="%s" fill="#F6C3D9" opacity=".55"/></g>' % (r(ax.x0), r(ax.Y(10)), r(ax.w), r(ax.Y(8.3)-ax.Y(10)))
b += '<g data-anim="fade" data-dur=".8" data-delay=".3"><rect x="%s" y="%s" width="%s" height="%s" fill="#FBD9A8" opacity=".55"/></g>' % (r(ax.x0), r(ax.Y(4.4)), r(ax.w), r(ax.Y(3.1)-ax.Y(4.4)))
b += curve_pts(ax, HCl20, dense(20, 0, 30), INK, 2.5, 'stroke-dasharray="7 5" opacity=".55"')
b += curve_pts(ax, HAc20, dense(20, 0, 30), EQUI, 3.5)
b += T(ax.x0+8, ax.Y(10)-6, mix='페놀프탈레인 8.3–10.0', size=19, anchor='start', fill='#B8326C', halo=True)
b += T(ax.x0+ax.w-4, ax.Y(3.1)+24, mix='메틸 오렌지||3.1–4.4', size=19, anchor='end', fill='#C2410C', halo=True)
F['S22'] = svg((500, 360), 460, '약산을 강염기로 적정한 곡선(주황)과 강산 곡선(점선) 위에 페놀프탈레인 변색 범위 8.3에서 10.0, 메틸 오렌지 변색 범위 3.1에서 4.4 띠', b)

# ── S23 강산 곡선 + 페놀프탈레인 띠 + 한 방울 확대
ax = Axes(66, 290, 330, 240, 30, 14)
b = ax.draw([0, 10, 20, 30], [0, 7, 14], '$V$ [mL]')
b += '<g data-anim="fade" data-dur=".8" data-delay=".3"><rect x="%s" y="%s" width="%s" height="%s" fill="#F6C3D9" opacity=".55"/></g>' % (r(ax.x0), r(ax.Y(10)), r(ax.w), r(ax.Y(8.3)-ax.Y(10)))
b += curve_pts(ax, HCl20, dense(20, 0, 30), INK, 3.5)
b += T(ax.x0+8, ax.Y(10)-6, mix='페놀프탈레인 변색 범위', size=19, anchor='start', fill='#B8326C', halo=True)
# 확대 창
zx, zy, zw, zh = 430, 40, 150, 260
b += '<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' % (zx, zy, zw, zh, INK)
az = Axes(zx+30, zy+zh-30, zw-50, zh-60, 20.1, 14, xmin=19.9)
b += '<rect x="%s" y="%s" width="%s" height="%s" fill="#F6C3D9" opacity=".55"/>' % (r(az.x0), r(az.Y(10)), r(az.w), r(az.Y(8.3)-az.Y(10)))
b += curve_pts(az, HCl20, [19.9+0.2*i/300 for i in range(301)], INK, 3)
b += dot(az.X(19.95), az.Y(HCl20(19.95)), INK, 5, '#FFFFFF') + dot(az.X(20.05), az.Y(HCl20(20.05)), INK, 5, '#FFFFFF')
b += T(az.X(19.95)-8, az.Y(HCl20(19.95))+6, tex='3.9', size=19, anchor='end', halo=True)
b += T(az.X(20.05)+8, az.Y(HCl20(20.05))+20, tex='10.1', size=19, anchor='start', halo=True)
b += T(zx+zw/2, zy-12, mix='중화점 앞뒤 1방울씩', size=19, fill=MUTED)
b += T(zx+zw/2, zy+zh-8, mix='2방울(0.1 mL)', size=19, fill=MUTED)
b += '<rect x="%s" y="%s" width="16" height="%s" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="3 3"/>' % (r(ax.X(20)-8), r(ax.Y(12)), r(ax.Y(2)-ax.Y(12)), MUTED)
b += line(ax.X(20)+8, ax.Y(12), zx, zy+20, MUTED, 1.2, '3 4')
F['S23'] = svg((600, 350), 560, '강산과 강염기의 적정 곡선과 페놀프탈레인 변색 범위 띠. 중화점 앞뒤 한 방울에 pH가 3.9에서 10.1로 변하는 확대 창', b)

# ── S24 전도도·온도 미니 그래프
def mini2(kind):
    ax = Axes(44, 150, 200, 110, 30, 10)
    o = line(ax.x0, ax.y0, ax.x0+ax.w+8, ax.y0, MUTED, 2) + line(ax.x0, ax.y0, ax.x0, ax.y0-ax.h-8, MUTED, 2)
    o += line(ax.X(20), ax.y0, ax.X(20), ax.y0-ax.h, FIELD, 1.5, '5 4')
    if kind == 'c':
        f = lambda V: (8-6*V/20) if V < 20 else (2+0.5*(V-20)*0.9)
        o += T(ax.x0+6, ax.y0-ax.h-6, mix='전기 전도도', size=19, anchor='start', fill=MUTED)
    else:
        f = lambda V: (2+5*V/20) if V < 20 else (7-0.12*(V-20))
        o += T(ax.x0+6, ax.y0-ax.h-6, mix='온도', size=19, anchor='start', fill=MUTED)
    o += '<g data-anim="draw" data-dur="1.2">' + curve_pts(ax, f, [i*0.1 for i in range(301)], INK, 3) + '</g>'
    o += T(ax.X(20), ax.y0+24, mix='중화점', size=19, fill=FIELD)
    o += T(ax.x0+ax.w+6, ax.y0+24, tex='V', size=19, anchor='end', fill=MUTED)
    lab = '넣은 염기의 부피에 따른 전기 전도도: 중화점에서 가장 작다' if kind == 'c' else '넣은 염기의 부피에 따른 온도: 중화점에서 가장 높다'
    return svg((260, 185), 240, lab, o)
F['S24c'] = mini2('c'); F['S24t'] = mini2('t')

# ── S25 대단원 마무리 04 그래프
ax = Axes(60, 300, 380, 250, 120, 14)
b = line(ax.x0, ax.y0, ax.x0+ax.w+12, ax.y0, MUTED, 2) + line(ax.x0, ax.y0, ax.x0, ax.y0-ax.h-14, MUTED, 2)
b += T(ax.x0+12, ax.y0-ax.h-6, tex='\\text{pH}', size=19, anchor='start', fill=MUTED)
for v in (50, 100):
    b += line(ax.X(v), ax.y0, ax.X(v), ax.y0+6, MUTED, 2) + T(ax.X(v), ax.y0+26, tex=str(v), size=19, fill=MUTED)
b += T(ax.x0-8, ax.y0+20, tex='0', size=19, anchor='end', fill=MUTED)
b += '<g data-anim="draw" data-dur="1.6">' + curve_pts(ax, HCl100, dense(100, 0, 120, 400), INK, 3.5) + '</g>'
xA = HCl100(50)
b += line(ax.x0, ax.Y(7), ax.X(100), ax.Y(7), MUTED, 1.5, '3 4') + line(ax.x0, ax.Y(xA), ax.X(50), ax.Y(xA), MUTED, 1.5, '3 4')
b += T(ax.x0-8, ax.Y(7)+7, tex='7', size=19, anchor='end') + T(ax.x0-8, ax.Y(xA)+7, tex='x', size=19, anchor='end')
b += dot(ax.X(50), ax.Y(xA), INK, 5) + dot(ax.X(100), ax.Y(7), INK, 5)
b += T(ax.X(50), ax.Y(xA)-14, tex='\\mathrm{A}', size=20, halo=True) + T(ax.X(100)+12, ax.Y(7)+7, tex='\\mathrm{B}', size=20, anchor='start', halo=True)
b += T(ax.x0+ax.w+14, ax.y0+52, mix='$0.1\\ \\text{M}$ 수산화 나트륨 수용액의 부피(mL)', size=19, anchor='end', fill=MUTED)
F['S25'] = svg((480, 360), 440, '농도를 모르는 염산 100 mL를 0.1 M 수산화 나트륨 수용액으로 적정한 곡선. A는 50 mL에서 pH x, B는 100 mL에서 pH 7', b)

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slides.tpl.html'), encoding='utf-8').read()
def sub(m):
    k = m.group(1)
    return F[k]
out = re.sub(r'\{\{(\w+)\}\}', sub, tpl)
open(sys.argv[1], 'w', encoding='utf-8').write(out)
print('ok', len(out))
