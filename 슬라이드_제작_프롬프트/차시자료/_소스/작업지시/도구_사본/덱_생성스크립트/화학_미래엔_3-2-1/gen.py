import math, random, sys
OUT = sys.argv[1]
def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def T(x, y, m, size=20, anc='middle', fill='#16233D', extra=''):
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" data-mix="{m}" data-size="{size}" data-anchor="{anc}" fill="{fill}"{extra}></text>'
def A(x1, y1, x2, y2, c='ink', w=3): return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{c},{w}"></g>'
def at(x, y, r, el, lab='-'): return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{","+lab if lab else ""}"></g>'
def rot(px, py, cx, cy, a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return cx+(px-cx)*c-(py-cy)*s, cy+(px-cx)*s+(py-cy)*c
def no2(cx, cy, r, a=0, lab='-'):
    d = 1.35*r; s = ''
    for b in (-67, 67):
        q = math.radians(-90+b); x, y = rot(cx+d*math.cos(q), cy+d*math.sin(q), cx, cy, a); s += at(x, y, r, 'O', lab)
    return s+at(cx, cy, r, 'N', lab)
def n2o4(cx, cy, r, a=0, lab='-'):
    d = 1.35*r; dn = 1.45*r; s = ''; ns = ''
    for sd in (-1, 1):
        nx = cx+sd*dn/2; base = 0 if sd > 0 else 180
        for b in (-62, 62):
            q = math.radians(base+b); x, y = rot(nx+d*math.cos(q), cy+d*math.sin(q), cx, cy, a); s += at(x, y, r, 'O', lab)
        x, y = rot(nx, cy, cx, cy, a); ns += at(x, y, r, 'N', lab)
    return s+ns
NO2C = '#B5562A'; FIELD = '#2E9E6A'; BF = '#7B4FC8'; EQ = '#E08A2C'; MU = '#5B6B7F'; KF = '#C9D3DD'
OR = '#E8792B'; YE = '#F2C230'; GL = '#7E8B98'; PLUS = '#D7263D'; MINUS = '#1F6FD1'; INK = '#16233D'; HE = '#CFE8F5'
def op(c): return 0.9*(1-math.exp(-c/0.06))
def halfarrows(x1, x2, y, w=3, gap=7):
    return (f'<path d="M{f(x1)} {f(y-gap)} H{f(x2)} l-10 -7" fill="none" stroke="{FIELD}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{f(x2)} {f(y+gap)} H{f(x1)} l10 7" fill="none" stroke="{BF}" stroke-width="{w}" stroke-linecap="round"/>')
def grid(items, x0, y0, w, h, r, seed):
    """items: list of 'a'(NO2)/'b'(N2O4)/'h'(He)/'g'(gas dot). grid with jitter."""
    rnd = random.Random(seed); n = len(items)
    best = None
    for cols in range(1, n+1):
        rows = math.ceil(n/cols); cw, ch = w/cols, h/rows
        sc = min(cw/(3.9*r), ch/(3.6*r))
        if best is None or sc > best[0]: best = (sc, cols, rows)
    _, cols, rows = best; cw, ch = w/cols, h/rows
    cells = [(i % cols, i//cols) for i in range(cols*rows)]; rnd.shuffle(cells)
    order = items[:]; rnd.shuffle(order); s = ''
    for k, (ci, ri) in zip(order, cells):
        jx = max(0, (cw-3.9*r)/2); jy = max(0, (ch-3.6*r)/2)
        cx = x0+cw*(ci+.5)+rnd.uniform(-jx, jx); cy = y0+ch*(ri+.5)+rnd.uniform(-jy, jy)
        a = rnd.choice([0, 30, -30, 60, -60, 90, 120, 150, 180, 210])
        if k == 'a': s += no2(cx, cy, r, a)
        elif k == 'b': s += n2o4(cx, cy, r, a if abs(a) <= 30 else (a % 60)-30)
        elif k == 'h': s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{HE}" stroke="#7FA9C2" stroke-width="1.5"/>'
        else: s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#8C99A6"/>'
    return s
def tube(x, ytop, ybot, w, color, level, extra_liq='', fid=''):
    r = w/2; out = f'M{f(x-r)} {f(ytop)} V{f(ybot-r)} A{f(r)} {f(r)} 0 0 0 {f(x+r)} {f(ybot-r)} V{f(ytop)}'
    li = f'M{f(x-r+3)} {f(level)} V{f(ybot-r)} A{f(r-3)} {f(r-3)} 0 0 0 {f(x+r-3)} {f(ybot-r)} V{f(level)} Z'
    s = f'<path d="{li}" fill="{color}"/>' if color else ''
    s += extra_liq.replace('LIQ', li)
    s += f'<path d="{out}" fill="none" stroke="{GL}" stroke-width="3.5"/><path d="M{f(x-r-5)} {f(ytop)} H{f(x+r+5)}" stroke="{GL}" stroke-width="3.5" stroke-linecap="round"/>'
    return s
def dropper(x, ytip, lab, col=INK, drop=True, anim=True, lx=None, ly=None, anc='start', size=24):
    s = f'<path d="M{x-7} {ytip-70} V{ytip-12} L{x} {ytip} L{x+7} {ytip-12} V{ytip-70} Z" fill="#F4F6F8" stroke="{GL}" stroke-width="2.5"/>'
    s += f'<rect x="{x-11}" y="{ytip-100}" width="22" height="32" rx="9" fill="#5B6B7F"/>'
    if drop:
        d = f'<path d="M{x} {ytip+8} q-6 9 0 14 q6 -5 0 -14 Z" fill="{col}" opacity=".85"/>'
        s += f'<g data-anim="move" data-from="0,-14" data-dur=".8" data-rep="loop">{d}</g>' if anim else d
    s += T(x+18 if lx is None else lx, ytip-44 if ly is None else ly, lab, size, anc, col, ' data-halo="1"')
    return s
def beaker(x, y, w, h, color, aniop=None, delay='.3'):
    # x,y = top-left
    liq = f'<path d="M{f(x+4)} {f(y+h*0.35)} H{f(x+w-4)} V{f(y+h-6)} Q{f(x+w-4)} {f(y+h-2)} {f(x+w-8)} {f(y+h-2)} H{f(x+8)} Q{f(x+4)} {f(y+h-2)} {f(x+4)} {f(y+h-6)} Z" fill="{color}"'
    liq += (f' data-anim="fade" data-dur="1.2" data-delay="{delay}"/>' if aniop else '/>')
    s = liq
    s += f'<path d="M{f(x-6)} {f(y-4)} Q{f(x)} {f(y)} {f(x)} {f(y+8)} V{f(y+h-8)} Q{f(x)} {f(y+h)} {f(x+8)} {f(y+h)} H{f(x+w-8)} Q{f(x+w)} {f(y+h)} {f(x+w)} {f(y+h-8)} V{f(y)}" fill="none" stroke="{GL}" stroke-width="3.5" stroke-linejoin="round"/>'
    for k in range(1, 4):
        yy = y+h-k*h*0.2; s += f'<path d="M{f(x+w-24)} {f(yy)} H{f(x+w-8)}" stroke="{GL}" stroke-width="2"/>'
    return s
def syr(cx, ytop, ybot, w, yp, gas_op, inner='', clamp=False, panim='', label=''):
    """vertical syringe. gas region from yp+12 to ybot."""
    x0 = cx-w/2; s = ''
    s += f'<rect x="{f(x0)}" y="{f(yp+12)}" width="{f(w)}" height="{f(ybot-yp-12)}" fill="{NO2C}" fill-opacity="{gas_op:.2f}"/>' if gas_op > 0 else ''
    s += inner
    for k in range(1, 9):
        yy = ytop+(ybot-ytop)*k/9; s += f'<path d="M{f(x0+w-14)} {f(yy)} H{f(x0+w-2)}" stroke="{MU}" stroke-width="1.5"/>'
    s += f'<path d="M{f(x0)} {f(ytop)} V{f(ybot)} H{f(x0+w)} V{f(ytop)}" fill="none" stroke="{GL}" stroke-width="3.5"/>'
    s += f'<path d="M{f(x0-12)} {f(ytop)} H{f(x0+w+12)}" stroke="{GL}" stroke-width="4" stroke-linecap="round"/>'
    s += f'<rect x="{f(cx-18)}" y="{f(ybot)}" width="36" height="16" rx="3" fill="#2B2F36"/>'
    pl = f'<rect x="{f(x0+2)}" y="{f(yp)}" width="{f(w-4)}" height="12" rx="2" fill="#3A3F47"/><rect x="{f(cx-5)}" y="{f(min(ytop,yp)-46)}" width="10" height="{f(yp-min(ytop,yp)+46)}" fill="#8C99A6"/><rect x="{f(cx-34)}" y="{f(min(ytop,yp)-56)}" width="68" height="12" rx="4" fill="#5B6B7F"/>'
    s += f'<g{panim}>{pl}</g>' if panim else pl
    if clamp:
        s += f'<path d="M{f(x0-22)} {f(yp-2)} H{f(x0+w+22)}" stroke="{PLUS}" stroke-width="5" stroke-linecap="round"/>'
    return s
H = {}

# ---------- COVER 540x540 ----------
c = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
c += tube(160, 70, 290, 64, OR, 140)+tube(380, 70, 290, 64, YE, 140)
c += '<g data-anim="draw" data-dur="1" data-delay=".3">'+halfarrows(214, 326, 180, 3.5, 9)+'</g>'
c += T(270, 150, '$\\ce{OH-}$', 24, fill=MINUS)+T(270, 232, '$\\ce{H+}$', 24, fill=PLUS)
c += T(160, 322, '$\\ce{Cr2O7^2-}$', 22)+T(380, 322, '$\\ce{CrO4^2-}$', 22)
inner = grid(['a']*3+['b']*3, 186, 368, 168, 106, 11, 7)
c += f'<path d="M180 362 V486 H360 V362" fill="none" stroke="{GL}" stroke-width="3.5"/>'
c = c.replace('<path d="M180 362', f'<rect x="180" y="362" width="180" height="124" fill="{NO2C}" fill-opacity=".3"/>'+inner+'<path d="M180 362', 1)
c += f'<g data-anim="move" data-from="0,-30" data-dur="1.4" data-delay=".5" data-ease="out"><rect x="183" y="350" width="174" height="12" rx="2" fill="#3A3F47"/><rect x="265" y="306" width="10" height="44" fill="#8C99A6"/><rect x="236" y="296" width="68" height="12" rx="4" fill="#5B6B7F"/>'+A(330, 300, 330, 344, 'ink', 3)+'</g>'
c += '<rect x="252" y="486" width="36" height="14" rx="3" fill="#2B2F36"/>'
c += T(172, 412, '$\\ce{NO2}$', 22, 'end')+T(172, 444, '$\\ce{N2O4}$', 22, 'end')
H['COVER'] = c

# ---------- S2 mountain 380x330 ----------
m = '<rect x="0" y="0" width="380" height="330" rx="18" fill="#E3EEFB"/>'
m += '<g data-anim="rot" data-from="-30" data-o="318,62" data-dur="1.6" data-ease="out">'+''.join(f'<path d="M{f(318+24*math.cos(math.radians(a)))} {f(62+24*math.sin(math.radians(a)))} L{f(318+32*math.cos(math.radians(a)))} {f(62+32*math.sin(math.radians(a)))}" stroke="#E8A317" stroke-width="3.5" stroke-linecap="round"/>' for a in range(0, 360, 45))+'<circle cx="318" cy="62" r="17" fill="#F7C531"/></g>'
m += '<path d="M0 250 L90 120 L150 180 L230 70 L310 170 L380 130 V330 H0 Z" fill="#9C7B5B"/><path d="M230 70 L205 105 L222 100 L236 112 L252 98 Z" fill="#fff"/><path d="M0 280 Q120 240 220 270 T380 260 V330 H0 Z" fill="#7FA36B"/>'
m += '<g transform="translate(120 222)"><circle cx="0" cy="0" r="9" fill="#8A5A3C"/><path d="M-11 10 H11 L16 50 H-16 Z" fill="#D7263D"/><path d="M-16 50 H16 L18 62 H-18 Z" fill="#2B2F36"/><path d="M-13 -6 H13 L9 -14 H-9 Z" fill="#7B4FC8"/></g>'
m += T(190, 32, '해발 고도가 높은 곳', 20, 'middle', INK, ' data-weight="700" data-halo="1"')
m += T(250, 228, '산소 부족', 21, 'middle', PLUS, ' data-weight="700" data-halo="1"')
for k, (x, y) in enumerate([(200, 160), (238, 140), (276, 158), (300, 200)]):
    m += f'<g data-anim="fade" data-dur=".8" data-delay="{.3+.25*k:.2f}" data-rep="alt"><circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{MU}" stroke-width="2" stroke-dasharray="3 3"/></g>'
m += T(306, 186, '$\\ce{O2}$', 18, 'start', MU, ' data-halo="1"')
H['MOUNT'] = m

# ---------- S5 equilibrium box 560x300 ----------
b = f'<rect x="210" y="56" width="320" height="220" rx="18" fill="{NO2C}" fill-opacity=".28"/><rect x="210" y="56" width="320" height="220" rx="18" fill="none" stroke="{GL}" stroke-width="3"/>'
b += f'<rect x="290" y="38" width="160" height="34" rx="10" fill="#fff" stroke="{GL}" stroke-width="2"/>'+T(370, 62, '화학 평형 상태', 20, extra=' data-weight="700"')
b += grid(['a']*6+['b']*3, 222, 82, 296, 184, 12, 3)
b += '<g data-anim="move" data-from="-60,10" data-dur="1.6" data-ease="out">'+no2(130, 190, 12)+'</g>'
b += A(158, 190, 200, 190, 'ink', 3)
b += f'<rect x="20" y="96" width="176" height="44" rx="14" fill="#fff" stroke="{MU}" stroke-width="2"/><path d="M110 140 l-8 16 l18 -16" fill="#fff" stroke="{MU}" stroke-width="2"/><path d="M103 139 H119" stroke="#fff" stroke-width="3"/>'+T(108, 125, '나도 들어갈래.', 20)
b += f'<rect x="330" y="0" width="210" height="30" rx="12" fill="#fff" stroke="{MU}" stroke-width="2"/>'+T(435, 22, '우리는 어떻게 될까?', 19)
b += no2(46, 262, 10)+T(66, 268, '$\\ce{NO2}$', 18, 'start')+n2o4(130, 262, 10)+T(158, 268, '$\\ce{N2O4}$', 18, 'start')
H['EQBOX'] = b

# ---------- S6 connected vessels 3 cards, each 320x220 ----------
def vessels(lv, rv, pour=False, arrow=False, anim=False, old=None):
    W = '#DDEEF8'; WS = '#9FC3DD'; s = ''
    s += f'<path d="M95 172 V196 H225 V172" fill="none" stroke="{GL}" stroke-width="22" stroke-linejoin="round"/><path d="M95 172 V196 H225 V172" fill="none" stroke="{W}" stroke-width="15" stroke-linejoin="round"/>'
    for x, lvv, sgn in ((60, lv, -1), (190, rv, 1)):
        h = 176-lvv
        rect = f'<rect x="{x}" y="{lvv}" width="70" height="{h}" fill="{W}"/><path d="M{x} {lvv} H{x+70}" stroke="{WS}" stroke-width="3"/>'
        if anim:
            frm = (176-(lvv-16))/h if sgn < 0 else (176-(lvv+16))/h
            rect = f'<g data-anim="scale" data-from="1,{frm:.3f}" data-o="{x+35},176" data-dur="1.6" data-delay=".4" data-ease="out">{rect}</g>'
        s += rect
        s += f'<path d="M{x} 30 V176 H{x+70} V30" fill="none" stroke="{GL}" stroke-width="3.5"/>'
    if old: s += f'<path d="M50 {old} H270" stroke="{MU}" stroke-width="2" stroke-dasharray="6 5"/>'
    if pour:
        s += f'<path d="M22 6 L64 6 L60 34 L30 30 Z" fill="#fff" stroke="{GL}" stroke-width="3" transform="rotate(25 44 20)"/>'
        s += f'<g data-anim="dash" data-speed="40" data-flow="1"><path d="M66 30 Q80 40 84 {lv}" fill="none" stroke="{WS}" stroke-width="5" stroke-dasharray="8 6"/></g>'
        s += f'<path d="M66 30 Q80 40 84 {lv}" fill="none" stroke="{WS}" stroke-width="5"/>'
    if arrow:
        s += A(120, 210, 200, 210, 'plus', 3)+T(160, 242, '물의 이동', 23, extra=' data-halo="1"')
    return s
H['V1'] = vessels(110, 110)
H['V2'] = vessels(78, 110, pour=True, old=110)
H['V3'] = vessels(94, 94, arrow=True, anim=True, old=110)

# ---------- S9 safety icons 3 x 150x120 ----------
H['GOG'] = f'<path d="M20 60 Q20 38 50 38 H100 Q130 38 130 60 Q130 84 100 84 Q86 84 80 70 H70 Q64 84 50 84 Q20 84 20 60 Z" fill="#E3EEFB" stroke="{INK}" stroke-width="4"/><path d="M8 56 H20 M130 56 H142" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
H['GLOVE'] = f'<path d="M50 112 V64 Q46 34 54 32 Q60 32 61 50 V22 Q62 12 70 12 Q78 12 78 22 V48 V18 Q80 8 87 8 Q95 9 95 18 V50 V26 Q97 18 104 18 Q111 19 111 28 V74 L122 58 Q130 50 136 56 Q140 62 132 72 L108 112 Z" fill="#9FD3C1" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
H['COAT'] = f'<path d="M52 12 L75 26 L98 12 L128 30 L136 112 H14 L22 30 Z" fill="#fff" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/><path d="M75 26 V112 M52 12 L68 56 L75 26 M98 12 L82 56 L75 26" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="84" cy="74" r="3.5" fill="{INK}"/><circle cx="84" cy="94" r="3.5" fill="{INK}"/>'

# ---------- S10 process tubes (each 300x250) ----------
def ptube(base, top=None, lab=None, labcol=INK, g=None):
    s = tube(110, 108, 254, 50, base, 180)
    if top:
        s += f'<g class="step" data-g="{g}"><path d="M88 180 V229 A22 22 0 0 0 132 229 V180 Z" fill="{top}" data-anim="fade" data-on="step" data-dur="1.4" data-delay=".5"/></g>'
        s = s.replace('<path d="M95', '<path d="M95', 1)
    if lab: s += dropper(110, 100, lab, labcol, ly=44)
    return s
H['P1'] = tube(110, 108, 254, 50, OR, 180)+T(196, 188, '4 mL', 24, 'start', MU)+A(190, 180, 142, 180, 'muted', 2)
H['P2'] = ptube(OR, YE, '$\\ce{NaOH(aq)}$', MINUS, 'p2')
H['P3'] = ptube(YE, OR, '$\\ce{HCl(aq)}$', PLUS, 'p3')

# ---------- S14 NaCl bottle 300x300 ----------
nb = f'<path d="M70 120 V270 Q70 286 86 286 H214 Q230 286 230 270 V120 Q230 104 214 100 L184 92 V60 H116 V92 L86 100 Q70 104 70 120 Z" fill="none" stroke="{GL}" stroke-width="3.5"/>'
nb = f'<path d="M74 170 H226 V270 Q226 282 214 282 H86 Q74 282 74 270 Z" fill="#DDEEF8"/><path d="M74 170 H226" stroke="#9FC3DD" stroke-width="3"/>'+nb
nb += dropper(150, 130, '진한 염산', PLUS, lx=132, ly=40, anc='end')
nb += T(150, 228, '$\\ce{NaCl}$ 포화 수용액', 19, extra=' data-halo="1"')
cr = ''
rnd = random.Random(5)
for k in range(9):
    x = 92+k*14+rnd.uniform(-3, 3); y = 270-rnd.uniform(0, 8)
    cr += f'<rect x="{f(x)}" y="{f(y-9)}" width="11" height="11" fill="#fff" stroke="{MU}" stroke-width="1.5" transform="rotate({rnd.choice([0,15,-15,30])} {f(x+5)} {f(y-4)})"/>'
H['NACL'] = nb
H['NACLX'] = f'<g data-anim="pop" data-on="step" data-o="150,266">{cr}</g>'

# ---------- S15 beakers 1000x230 ----------
bk = ''
for i, (x, col, lab) in enumerate([(70, OR, '$\\ce{K2Cr2O7(aq)}$'), (430, YE, '$\\ce{NaOH(aq)}$을 넣은 후'), (790, OR, '$\\ce{HCl(aq)}$을 넣은 후')]):
    bk += beaker(x, 50, 150, 160, col, aniop=(i > 0), delay=('.4' if i == 1 else '1.4'))
    bk += f'<rect x="{x-35}" y="6" width="220" height="32" rx="16" fill="#FFF3E0" stroke="{EQ}" stroke-width="1.5"/>'+T(x+75, 29, lab, 19)
bk += A(255, 140, 395, 140, 'minus', 4)+T(325, 124, '$\\ce{OH-}$', 22, fill=MINUS)
bk += A(615, 140, 755, 140, 'plus', 4)+T(685, 124, '$\\ce{H+}$', 22, fill=PLUS)
bk += T(145, 228, '주황색', 19, fill=MU)+T(505, 228, '노란색', 19, fill=MU)+T(865, 228, '주황색', 19, fill=MU)
H['BEAK'] = bk

# ---------- S16 particle cards 320x210 ----------
def pbox(items, opv, seed, extra='', newitems=None):
    s = f'<rect x="20" y="16" width="280" height="180" rx="16" fill="{NO2C}" fill-opacity="{opv}"/>'
    s += grid(items, 30, 26, 260, 160, 12, seed) if not newitems else ''
    if newitems:
        allitems = items+newitems
        full = grid(allitems, 30, 26, 260, 160, 12, seed)
        s += full
    s += extra+f'<rect x="20" y="16" width="280" height="180" rx="16" fill="none" stroke="{GL}" stroke-width="3"/>'
    return s
# card 2: draw old ones fixed, new ones moving in
old = grid(['a']*6+['b']*3, 30, 26, 260, 160, 12, 11)
H['C1'] = f'<rect x="20" y="16" width="280" height="180" rx="16" fill="{NO2C}" fill-opacity=".3"/>'+old+f'<rect x="20" y="16" width="280" height="180" rx="16" fill="none" stroke="{GL}" stroke-width="3"/>'
# card 2: 12 NO2 + 3 N2O4. place via grid with 15 items, first keep separate
rnd2 = random.Random(21)
c2 = grid(['a']*12+['b']*3, 30, 26, 260, 160, 12, 21)
# mark: move-in animation for whole group is not atom-preserving; animate the 6 newest via separate grid? simpler: whole box contents fade
H['C2'] = f'<rect x="20" y="16" width="280" height="180" rx="16" fill="{NO2C}" fill-opacity=".5"/>'+c2+f'<rect x="20" y="16" width="280" height="180" rx="16" fill="none" stroke="{GL}" stroke-width="3"/>'
H['C3'] = f'<rect x="20" y="16" width="280" height="180" rx="16" fill="{NO2C}" fill-opacity=".38"/>'+grid(['a']*8+['b']*5, 30, 26, 260, 160, 12, 31)+f'<rect x="20" y="16" width="280" height="180" rx="16" fill="none" stroke="{GL}" stroke-width="3"/>'

# ---------- S20 gas compress 560x300 ----------
g20 = syr(140, 60, 280, 150, 60, 0, grid(['g']*8, 70, 76, 140, 200, 9, 4))
g20 += syr(420, 60, 280, 150, 170, 0, grid(['g']*8, 350, 186, 140, 90, 9, 4), panim=' data-anim="move" data-from="0,-110" data-dur="1.5" data-delay=".5" data-ease="out"')
g20 += A(262, 170, 318, 170, 'ink', 4)+T(290, 150, '누름', 20)
g20 += T(140, 26, '부피 $V$', 21, extra=' data-halo="1"')+T(420, 26, '부피 $\\frac{1}{2}V$', 21, extra=' data-halo="1"')
H['G20'] = g20

# ---------- S22 three syringes 1000x330 ----------
s22 = ''
for i, (x, yp, c) in enumerate([(170, 80, .0206), (500, 175, .0411), (830, 175, .0296)]):
    pan = ' data-anim="move" data-from="0,-95" data-dur="1.2" data-delay=".4" data-ease="out"' if i == 1 else ''
    s22 += syr(x, 80, 300, 120, yp, op(c), panim=pan)
s22 += A(270, 230, 400, 230, 'ink', 4)+A(600, 230, 730, 230, 'ink', 4)
s22 += T(335, 208, '누름', 24)+T(665, 208, '시간', 24)
H['S22'] = s22

# ---------- S25 pressure cards 340x300 (syringe w=240) ----------
def pcard(yp, items, seed, opv, panim=''):
    inner = grid(items, 32, yp+16, 276, 290-yp-16-4, 8, seed)
    return syr(170, 20, 290, 290, yp, opv, inner, panim=panim)
H['Q1'] = pcard(20, ['a']*8+['b']*6, 41, op(.0206))
H['Q2'] = pcard(155, ['a']*8+['b']*6, 42, op(.0411), ' data-anim="move" data-from="0,-135" data-dur="1.4" data-delay=".4" data-ease="out"')
H['Q3'] = pcard(155, ['a']*6+['b']*7, 43, op(.0296))
H['QLEG'] = no2(30, 22, 8)+T(52, 28, '$\\ce{NO2}$', 18, 'start')+n2o4(124, 22, 8)+T(148, 28, '$\\ce{N2O4}$', 18, 'start')

# ---------- S26 H2 I2 HI 560x150 ----------
def dia(cx, cy, r1, e1, r2, e2):
    d = 0.8*(r1+r2); return at(cx-d/2, cy, r1, e1)+at(cx+d/2, cy, r2, e2)
hi = dia(60, 60, 9, 'H', 9, 'H')+T(120, 68, '+', 26)+dia(185, 60, 17.5, 'I', 17.5, 'I')
hi += halfarrows(250, 320, 60, 3)
hi += dia(395, 60, 9, 'H', 17.5, 'I')+dia(485, 60, 9, 'H', 17.5, 'I')
hi += T(60, 100, '$\\ce{H2}$', 19)+T(185, 100, '$\\ce{I2}$', 19)+T(395, 100, '$\\ce{HI}$', 19)+T(485, 100, '$\\ce{HI}$', 19)
hi += T(122, 136, '기체 분자 2개', 20, fill=MU)+T(440, 136, '기체 분자 2개', 20, fill=MU)
H['HI'] = hi

# ---------- S30 He 600x330 ----------
items = ['a']*4+['b']*3
fix = syr(150, 70, 300, 170, 150, op(.03), grid(items+['h']*7, 75, 168, 150, 126, 8, 51), clamp=True)
free = syr(450, 70, 300, 170, 70, op(.015), grid(items+['h']*7, 375, 88, 150, 206, 8, 52), panim=' data-anim="move" data-from="0,80" data-dur="1.6" data-delay=".5" data-ease="out"')
H['HE'] = fix+free+T(150, 334, '피스톤 고정: 부피 그대로', 23)+T(450, 334, '피스톤 자유: 부피 2배', 23)+T(56, 156, '고정', 22, 'end', PLUS, ' data-weight="700"')
H['HELEG'] = f'<circle cx="18" cy="20" r="8" fill="{HE}" stroke="#7FA9C2" stroke-width="1.5"/>'+T(32, 26, '$\\ce{He}$', 18, 'start')+no2(96, 20, 8)+T(112, 26, '$\\ce{NO2}$', 18, 'start')+n2o4(186, 20, 8)+T(206, 26, '$\\ce{N2O4}$', 18, 'start')

# ---------- S32 cobalt tube 240x280 ----------
co = tube(90, 128, 316, 50, '#D9608A', 200, extra_liq='<path d="M68 200 V291 A22 22 0 0 0 112 291 V200 Z" fill="#3B6FD1" data-anim="fade" data-dur="1.6" data-delay=".6"/>')
co = co.replace('<path d="M98 150 V237 A22 22 0 0 0 142 237 V150 Z" fill="#3B6FD1"', '<path d="M98 150 V237 A22 22 0 0 0 142 237 V150 Z" fill="#3B6FD1"', 1)
co += dropper(90, 120, '진한 $\\ce{HCl(aq)}$', PLUS, lx=108, ly=60)
H['CO'] = co


def lab_html(name):
    return f'''<div class="lab cm321-lab" data-lab="{name}">
    <div class="lab-ctl" style="flex:0 0 372px">
      <div class="cm321-seg"><button class="btn" data-mode="conc">농도</button><button class="btn" data-mode="press">압력</button><button class="btn" data-mode="temp">온도</button><button class="btn cm321-rs" data-act="reset">처음부터</button></div>
      <div data-pane="conc">
        <p class="small">처음 용액</p>
        <div class="cm321-seg"><button class="btn" data-sol="0">$\\ce{{K2Cr2O7(aq)}}$</button><button class="btn" data-sol="1">$\\ce{{K2CrO4(aq)}}$</button></div>
        <div class="cm321-seg"><button class="btn cm321-add" data-act="oh">$\\ce{{NaOH(aq)}}$ 넣기</button><button class="btn cm321-add" data-act="h">$\\ce{{HCl(aq)}}$ 넣기</button></div>
        <p class="small">한 번 = 1 mol/L 용액 0.1 mL(약 2 방울)</p>
      </div>
      <div data-pane="press">
        <div class="ctl"><div class="lbl"><span>바꿀 부피</span><output data-o="v"></output></div><input type="range" min="25" max="100" step="5" value="25" data-i="v" aria-label="바꿀 부피"></div>
        <div class="cm321-seg"><button class="btn cm321-add" data-act="vol">부피 바꾸기</button></div>
        <div class="cm321-seg"><button class="btn" data-act="hefix">$\\ce{{He}}$ 넣기 · 피스톤 고정</button><button class="btn" data-act="hefree">$\\ce{{He}}$ 넣기 · 피스톤 자유</button></div>
      </div>
      <div data-pane="temp">
        <div class="cm321-seg"><button class="btn" data-t="0">얼음물 0 °C</button><button class="btn" data-t="25">실온 25 °C</button><button class="btn" data-t="80">뜨거운 물 80 °C</button></div>
        <p class="small">온도가 바뀌면 $K$가 바뀐다 — 까닭은 다음 시간(02)에서</p>
      </div>
      <div class="res"><div class="big"><output data-o="q"></output></div><output class="kind cm321-msg" data-o="msg"></output></div>
    </div>
    <div class="col" style="flex:0 0 704px">
      <div class="lab-fig" style="width:704px;height:304px"><svg viewBox="0 0 700 300" width="700" height="300" aria-label="시험관 또는 주사기, 로그 눈금의 반응 지수와 평형 상수, 물질의 양 막대"></svg></div>
      <table class="tight cm321-log mt8"><thead><tr><th>실험</th><th>변인</th><th>조작</th><th>직후 비교</th><th>우세한 반응</th><th>새 평형에서 관찰</th></tr></thead><tbody data-o="log"></tbody></table>
    </div>
  </div>'''
H['LAB:cm321conc'] = lab_html('cm321conc')
H['LAB:cm321press'] = lab_html('cm321press')

src = open(__file__.replace('gen.py','slides.html.tpl'), encoding='utf-8').read()
for k, v in H.items(): src = src.replace('[['+k+']]', v)
import re
left = re.findall(r'\[\[[A-Za-z0-9:]+\]\]', src)
if left: print('UNFILLED', left)
open(OUT, 'w', encoding='utf-8').write(src)
print('ok', len(src))
