import math, random, sys
OUT = sys.argv[1]
def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def T(x, y, m, size=20, anc='middle', fill='#16233D', extra=''):
    return f'<text class="tex" x="{f(x)}" y="{f(y)}" data-mix="{m}" data-size="{size}" data-anchor="{anc}" fill="{fill}"{extra}></text>'
def A(x1, y1, x2, y2, c='ink', w=3): return f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},{c},{w}"></g>'
def at(x, y, r, el, lab=''): return f'<g data-atom="{f(x)},{f(y)},{r},{el}{","+lab if lab else ""}"></g>'
def no2(cx, cy, r, rot=0, lab=''):
    d = 1.35*r; s = ''
    for a in (-67, 67):
        q = math.radians(-90+a+rot); s += at(cx+d*math.cos(q), cy+d*math.sin(q), r, 'O', lab)
    return s+at(cx, cy, r, 'N', lab)
def n2o4(cx, cy, r, lab=''):
    d = 1.35*r; dn = 1.45*r; s = ''; ns = ''
    for sd in (-1, 1):
        nx = cx+sd*dn/2; base = 0 if sd > 0 else 180
        for a in (-62, 62):
            q = math.radians(base+a); s += at(nx+d*math.cos(q), cy+d*math.sin(q), r, 'O', lab)
        ns += at(nx, cy, r, 'N', lab)
    return s+ns
NO2C = '#B5562A'; FIELD = '#2E9E6A'; BF = '#7B4FC8'; EQ = '#E08A2C'; MU = '#5B6B7F'; KF = '#C9D3DD'
def halfarrows(x1, x2, y, w=3):
    return (f'<path d="M{x1} {y-7} H{x2} l-10 -7" fill="none" stroke="{FIELD}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x2} {y+7} H{x1} l10 7" fill="none" stroke="{BF}" stroke-width="{w}" stroke-linecap="round"/>')
H = {}
# ---------- cover 540x540 ----------
c = '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
c += f'<path d="M110 110 H430" stroke="{MU}" stroke-width="2" stroke-dasharray="7 6"/>'
c += f'<rect x="300" y="110" width="74" height="170" rx="6" fill="{KF}" stroke="#16233D" stroke-width="3"/>'
c += f'<g data-anim="scale" data-from="1,0.35" data-o="203,280" data-dur="1.6" data-delay=".4" data-ease="out"><rect x="166" y="110" width="74" height="170" rx="6" fill="{EQ}"/></g>'
c += A(132, 250, 132, 120, 'field', 4)
c += T(203, 312, '$Q$', 30)+T(337, 312, '$K$', 30)+T(124, 100, '$Q$가 $K$와 같아질 때까지', 21, 'start', MU)
c += '<g data-anim="move" data-from="5,-4" data-rep="swing" data-dur="1.1">'+no2(160, 376, 24)+'</g>'
c += '<g data-anim="draw" data-dur="1" data-delay=".4">'+halfarrows(228, 304, 380)+'</g>'
c += n2o4(390, 381, 24)
c += T(160, 470, '$\\ce{2NO2}$', 24)+T(390, 470, '$\\ce{N2O4}$', 24)
H['COVER'] = c
# ---------- S3 weather 520x270 ----------
def sun(x, y, anim=False):
    s = ''.join(f'<path d="M{f(x+21*math.cos(math.radians(a)))} {f(y+21*math.sin(math.radians(a)))} L{f(x+29*math.cos(math.radians(a)))} {f(y+29*math.sin(math.radians(a)))}" stroke="#E8A317" stroke-width="3.5" stroke-linecap="round"/>' for a in range(0, 360, 45))
    s += f'<circle cx="{x}" cy="{y}" r="15" fill="#F7C531"/>'
    return f'<g data-anim="rot" data-from="-45" data-o="{x},{y}" data-dur="1.6" data-ease="out">{s}</g>' if anim else s
def cloud(x, y, col='#C9D3DD'):
    return f'<g fill="{col}"><circle cx="{x-12}" cy="{y+4}" r="13"/><circle cx="{x+4}" cy="{y-6}" r="16"/><circle cx="{x+18}" cy="{y+5}" r="12"/><rect x="{x-25}" y="{y+4}" width="55" height="13" rx="6"/></g>'
def rain(x, y):
    return cloud(x, y, '#AEB9C6')+''.join(f'<path d="M{x+dx} {y+24} l-5 12" stroke="#1F6FD1" stroke-width="3" stroke-linecap="round"/>' for dx in (-12, 2, 16))
w = '<rect x="10" y="10" width="500" height="250" rx="16" fill="#fff" stroke="#7E8B98" stroke-width="3"/><rect x="10" y="10" width="500" height="46" rx="16" fill="#E3EEFB"/><path d="M10 56 H510" stroke="#7E8B98" stroke-width="2"/>'
w += T(30, 42, '주간 날씨 예보', 21, 'start', '#16233D', ' data-weight="700"')
days = ['월', '화', '수', '목', '금']; ic = ['sun', 'sun', 'cloud', 'rain', 'sun']; hi = [25, 27, 24, 21, 26]; lo = [19, 20, 16, 15, 16]
for i in range(5):
    x = 70+95*i
    w += T(x, 92, days[i], 21)
    w += sun(x, 140, i == 0) if ic[i] == 'sun' else (cloud(x-3, 136) if ic[i] == 'cloud' else rain(x-3, 128))
    w += T(x, 206, f'{hi[i]}°', 21, fill='#D7263D')+T(x, 238, f'{lo[i]}°', 21, fill='#1F6FD1')
H['WEATHER'] = w
# ---------- S4 three flasks 560x290 ----------
fl = ''
for x, op, lab, cap in [(100, .5, '(가)', '$\\ce{NO2}$만'), (280, 0, '(나)', '$\\ce{N2O4}$만'), (460, .3, '(다)', '둘 다')]:
    if op: fl += f'<path d="M{x-25} 34 V84 A80 80 0 1 0 {x+25} 84 V34 Z" fill="{NO2C}" fill-opacity="{op}" data-anim="fade" data-dur="1.2" data-delay=".3"/>'
    fl += f'<path d="M{x-25} 34 V84 A80 80 0 1 0 {x+25} 84 V34" fill="none" stroke="#7E8B98" stroke-width="4"/><rect x="{x-32}" y="20" width="64" height="20" rx="5" fill="#C9B79C" stroke="#8C7A5E" stroke-width="2.5"/>'
    fl += T(x, 180, cap, 21, extra=' data-halo="1"')+T(x, 282, lab, 22, extra=' data-weight="700"')
H['FLASKS'] = fl
# ---------- S6 number line 1000x150 ----------
L0, L1 = 60, 960; lmin, lmax = 1, math.log10(300)
X = lambda v: L0+(math.log10(v)-lmin)/(lmax-lmin)*(L1-L0)
nl = A(L0-20, 100, L1+24, 100, 'ink', 2)
for v in (10, 20, 50, 100, 200):
    nl += f'<path d="M{f(X(v))} 92 V108" stroke="#16233D" stroke-width="2"/>'+T(X(v), 134, str(v), 19)
nl += T(L1+22, 134, '(로그 눈금)', 18, 'end', MU)
nl += f'<path d="M{f(X(50))} 26 V100" stroke="#16233D" stroke-width="3" stroke-dasharray="7 5"/>'+T(X(50)+10, 30, '$K=50$', 22, 'start', extra=' data-weight="700"')
for v, lab, g, arr in [(24.7, '실험 1', 'v1', (X(24.7)+14, X(50)-10, 'field')), (186.7, '실험 2', 'v2', (X(186.7)-14, X(50)+10, 'bfield')), (50.2, '실험 3', 'v3', None)]:
    yy = 100 if v != 50.2 else 100
    s = f'<g class="step" data-g="{g}"><g data-anim="pop" data-on="step" data-o="{f(X(v))},{yy}"><circle cx="{f(X(v))}" cy="{yy}" r="10" fill="{EQ}" stroke="#fff" stroke-width="2"/></g>'
    s += T(X(v), 76 if v != 50.2 else 60, lab, 19, extra=' data-halo="1"')
    if arr: s += A(arr[0], 70, arr[1], 70, arr[2], 3) if False else ''
    s += '</g>'
    nl += s
H['NUMLINE'] = nl
# ---------- S11 Q bar grows to K 440x320 ----------
b = f'<path d="M30 270 H410" stroke="#16233D" stroke-width="2.5"/><path d="M40 70 H410" stroke="{MU}" stroke-width="2" stroke-dasharray="7 6"/>'
b += f'<rect x="250" y="70" width="80" height="200" rx="5" fill="{KF}" stroke="#16233D" stroke-width="3"/>'
b += f'<rect x="110" y="70" width="80" height="100" rx="5" fill="none" stroke="{EQ}" stroke-width="2.5" stroke-dasharray="7 5"/>'
b += f'<g data-anim="scale" data-from="1,0" data-o="150,270" data-dur="1.2" data-ease="out"><rect x="110" y="170" width="80" height="100" rx="5" fill="{EQ}"/></g>'
b += f'<g class="step" data-g="q1">'+A(70, 168, 70, 76, 'field', 4)+T(60, 130, '$Q$||증가', 20, 'end', FIELD, ' data-weight="700"')+'</g>'
b += T(150, 300, '$Q=100$', 22)+T(290, 300, '$K=200$', 22)+T(150, 230, '지금', 19, fill='#fff', extra=' data-weight="700"')+T(290, 60, '평형에서의 값', 19, fill=MU)
H['QBAR'] = b
# ---------- S12 three panels 300x270 ----------
def panel(qh, kind):
    s = f'<path d="M30 230 H280" stroke="#16233D" stroke-width="2.5"/><path d="M40 100 H280" stroke="{MU}" stroke-width="2" stroke-dasharray="7 6"/>'
    s += f'<rect x="170" y="100" width="64" height="130" rx="5" fill="{KF}" stroke="#16233D" stroke-width="3"/>'
    s += f'<g data-anim="scale" data-from="1,{0.5 if kind!="eq" else 0.8}" data-o="122,230" data-dur="1.1" data-ease="out"><rect x="90" y="{230-qh}" width="64" height="{qh}" rx="5" fill="{EQ}"/></g>'
    if kind == 'lt': s += A(58, 228-qh, 58, 106, 'field', 4)
    if kind == 'gt': s += A(58, 232-qh, 58, 94, 'bfield', 4)
    s += T(122, 256, '$Q$', 22)+T(202, 256, '$K$', 22)
    return s
H['P_LT'] = panel(65, 'lt'); H['P_EQ'] = panel(130, 'eq'); H['P_GT'] = panel(200, 'gt')
# ---------- S13/14 particle cards 320x280 ----------
def place(kinds, seed):
    rnd = random.Random(seed)
    for _ in range(4000):
        pts = []; ok = True
        for k in kinds:
            for t in range(400):
                x = rnd.uniform(62, 258); y = rnd.uniform(56, 160)
                good = True
                for (px, py, pk) in pts:
                    need = 48 if (k == 0 and pk == 0) else (58 if k != pk else 66)
                    if math.hypot(x-px, (y-py)*1.25) < need: good = False; break
                if good: pts.append((x, y, k)); break
            else: ok = False; break
        if ok: return pts
    raise SystemExit('place fail')
def card(na, nb, fw, rv, seed, anim=False):  # noqa
    o = f'<rect x="30" y="26" width="260" height="164" rx="18" fill="{NO2C}" fill-opacity="{f(0.05*na)}"/><rect x="30" y="26" width="260" height="164" rx="18" fill="none" stroke="#7E8B98" stroke-width="3"/><rect x="134" y="12" width="52" height="20" rx="4" fill="#C9B79C" stroke="#8C7A5E" stroke-width="2"/>'
    rnd = random.Random(seed+7)
    mv = ''
    for (x, y, k) in place([1]*nb+[0]*na, seed):
        mv += no2(x, y, 12, rnd.randrange(0, 360, 15), '-') if k == 0 else n2o4(x, y, 12, '-')
    o += f'<g data-anim="move" data-from="3,-3" data-rep="swing" data-dur=".9">{mv}</g>' if anim else mv
    o += T(14, 222, '정반응', 22, 'start', FIELD, ' data-weight="700"')+A(96, 215, 96+fw, 215, 'field', 3.5)
    o += T(14, 254, '역반응', 22, 'start', BF, ' data-weight="700"')+A(96+rv, 247, 96, 247, 'bfield', 3.5)
    return o
def stages(spec, aria):
    out = ''
    for (h3, na, nb, fw, rv, seed, q, key, cls) in spec:
        out += f'<div class="stage{cls}"><h3>{h3}</h3><svg viewBox="0 0 320 266" style="height:206px" aria-label="{aria}">{card(na, nb, fw, rv, seed, anim=(cls!=""))}</svg><p class="key">{key}</p><p class="cm313-q">{q}</p></div>'
    return out
AR = '밀폐 용기 속 이산화 질소와 사산화 이질소 분자, 정반응과 역반응의 빠르기'
H['CARDS_LT'] = stages([
    ('① 처음 ($Q&lt;K$)', 10, 1, 170, 25, 31, '$Q=\\dfrac{1}{10^2}=\\dfrac{1}{100}$', '$\\ce{NO2}$ 10개, $\\ce{N2O4}$ 1개', ''),
    ('② 반응이 진행하면', 8, 2, 120, 50, 32, '$Q=\\dfrac{2}{8^2}=\\dfrac{1}{32}$', '$\\ce{NO2}$ 8개, $\\ce{N2O4}$ 2개', ''),
    ('③ 평형 ($Q=K$)', 6, 3, 75, 75, 33, '$Q=\\dfrac{3}{6^2}=\\dfrac{1}{12}=K$', '$\\ce{NO2}$ 6개, $\\ce{N2O4}$ 3개', ' cm313-eqc')], AR)
H['CARDS_GT'] = stages([
    ('① 처음 ($Q&gt;K$)', 2, 5, 25, 170, 41, '$Q=\\dfrac{5}{2^2}=\\dfrac{5}{4}$', '$\\ce{NO2}$ 2개, $\\ce{N2O4}$ 5개', ''),
    ('② 반응이 진행하면', 4, 4, 50, 120, 42, '$Q=\\dfrac{4}{4^2}=\\dfrac{1}{4}$', '$\\ce{NO2}$ 4개, $\\ce{N2O4}$ 4개', ''),
    ('③ 평형 ($Q=K$)', 6, 3, 75, 75, 43, '$Q=\\dfrac{3}{6^2}=\\dfrac{1}{12}=K$', '$\\ce{NO2}$ 6개, $\\ce{N2O4}$ 3개', ' cm313-eqc')], AR)
# ---------- S18 cylinders 460x270 ----------
def cyl(x, gh, anim):
    s = f'<path d="M{x} 30 V240 H{x+120} V30" fill="none" stroke="#7E8B98" stroke-width="4"/>'
    s += f'<rect x="{x+2}" y="{240-gh}" width="116" height="{gh}" fill="#DDE7F0"/>'
    pist = f'<rect x="{x+3}" y="{240-gh-14}" width="114" height="14" rx="3" fill="#8C99A6" stroke="#5B6B7F" stroke-width="2"/><path d="M{x+60} {240-gh-14} V{240-gh-56}" stroke="#5B6B7F" stroke-width="6"/>'
    s += f'<g data-anim="move" data-from="0,{gh//2}" data-dur="1.4" data-delay=".4" data-ease="out">{pist}</g>' if anim else pist
    return s
cy_ = cyl(30, 80, False)+cyl(300, 160, True)
cy_ += T(90, 216, '$V$', 24)+T(360, 176, '$2V$', 24)+A(178, 160, 284, 160, 'ink', 3)+T(231, 146, '부피 2배', 20)
cy_ += T(90, 266, '평형', 21)+T(360, 266, '농도 모두 $\\frac{1}{2}$배', 21)
H['CYL'] = cy_
# ---------- S20 rocket 260x380 ----------
r = '<g data-anim="move" data-from="0,40" data-dur="1.6" data-ease="out">'
r += '<path d="M130 20 C165 60 172 120 170 230 H90 C88 120 95 60 130 20 Z" fill="#F4F6F8" stroke="#16233D" stroke-width="3"/>'
r += '<path d="M90 190 L58 262 H92 Z M170 190 L202 262 H168 Z" fill="#D7263D" stroke="#16233D" stroke-width="3" stroke-linejoin="round"/>'
r += '<circle cx="130" cy="110" r="20" fill="#9FC3DD" stroke="#16233D" stroke-width="3"/><rect x="96" y="230" width="68" height="22" rx="4" fill="#8C99A6" stroke="#16233D" stroke-width="3"/>'
r += '<path d="M104 254 Q130 350 156 254 Z" fill="#F7C531"/><path d="M116 254 Q130 318 144 254 Z" fill="#E08A2C"/></g>'
H['ROCKET'] = r
# ---------- S21 06 boxes 460x190 ----------
def box(x, lines, cap):
    s = f'<rect x="{x}" y="14" width="170" height="130" rx="14" fill="#fff" stroke="#7E8B98" stroke-width="3"/>'
    s += T(x+85, 50, lines, 20)+T(x+85, 134, '1 L', 19, fill=MU)+T(x+85, 176, cap, 20, extra=' data-weight="700"')
    return s
H['BOX06'] = box(10, '$\\ce{C(s)}$ 1 몰||$\\ce{CO2(g)}$ 1 몰', '처음')+A(190, 79, 268, 79, 'muted', 3)+T(229, 66, '평형', 19, fill=MU)+box(280, '$\\ce{CO(g)}$ 1 몰||생성', '평형')
# ---------- S23 08 partition 520x200 ----------
p = '<rect x="10" y="30" width="220" height="120" rx="12" fill="#fff" stroke="#7E8B98" stroke-width="3"/><path d="M120 30 V150" stroke="#16233D" stroke-width="5"/>'
p += T(65, 70, '$\\mathrm{A}(g)$', 20)+T(65, 104, '1 몰', 20)+T(65, 138, '0.5 L', 19, fill=MU)
p += T(175, 70, '$\\mathrm{B}(g)$', 20)+T(175, 104, '$x$ 몰', 20)+T(175, 138, '0.5 L', 19, fill=MU)+T(120, 22, '칸막이', 18, fill=MU)
p += A(244, 90, 300, 90, 'ink', 3)+T(272, 76, '제거', 18, fill=MU)
p += '<g data-anim="fade" data-dur="1" data-delay=".5"><rect x="310" y="30" width="200" height="120" rx="12" fill="#fff" stroke="#7E8B98" stroke-width="3"/>'
p += T(410, 72, '$\\mathrm{A}(g)$, $\\mathrm{B}(g)$, $\\mathrm{C}(g)$', 20)+T(410, 106, '3 몰', 20)+T(410, 138, '1 L', 19, fill=MU)+'</g>'
p += T(120, 186, '(가)', 20, extra=' data-weight="700"')+T(410, 186, '(나)', 20, extra=' data-weight="700"')
H['PART'] = p

src = open(OUT+'.tpl', encoding='utf-8').read()
for k, v in H.items(): src = src.replace('[['+k+']]', v)
import re
left = re.findall(r'\[\[[A-Z_0-9]+\]\]', src)
if left: raise SystemExit('unfilled '+str(left))
open(OUT, 'w', encoding='utf-8').write(src)
print('ok', len(src))
