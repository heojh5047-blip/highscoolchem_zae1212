# 1-2-1 덱 그림 생성: slides.tpl.html 의 {{이름}} 자리에 SVG 조각을 넣어 slides.html 을 만든다.
import math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학_미래엔_1-2-1/out_check.html"
R = {'H': 18, 'C': 24, 'N': 24, 'O': 24, 'Fe': 28, 'S': 29, 'Mg': 29}
INK, MUT, FIELD, EQUI, PLUS, MINUS = '#16233D', '#5B6B7F', '#2E9E6A', '#E08A2C', '#D7263D', '#1F6FD1'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def A(x, y, el, r, lab=None):
    if lab is None:
        lab = '' if r >= 18 else '-'
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{("," + lab) if lab else ""}"></g>'


def T(x, y, s, size=20, anchor='middle', fill=None, weight=None, halo=False, tex=False, extra=''):
    a = f'data-tex="{s}"' if tex else f'data-mix="{s}"'
    return (f'<text class="tex" x="{f(x)}" y="{f(y)}" {a} data-size="{size}" data-anchor="{anchor}"'
            + (f' fill="{fill}"' if fill else '') + (f' data-weight="{weight}"' if weight else '')
            + (' data-halo="1"' if halo else '') + (f' {extra}' if extra else '') + '></text>')


def atoms(kind, x, y, s=1.0, rot=0.0):
    """분자 원자 목록 [(원소, x, y, r, 라벨)] — 뒤 → 앞"""
    def P(d, ang):
        a = math.radians(ang + rot)
        return x + d * math.cos(a), y + d * math.sin(a)
    r = lambda e: R[e] * s
    out = []
    if kind in ('H2', 'O2', 'N2'):
        e = kind[0]; d = 0.78 * r(e)
        out += [(e,) + P(d, 180) + (r(e), None), (e,) + P(d, 0) + (r(e), None)]
    elif kind in ('A2', 'B2'):
        e = 'N' if kind == 'A2' else 'H'; lab = '-'
        d = 0.78 * r(e)
        out += [(e,) + P(d, 180) + (r(e), lab), (e,) + P(d, 0) + (r(e), lab)]
    elif kind == 'AB3':
        d = 0.78 * (r('N') + r('H'))
        out += [('H',) + P(d, a) + (r('H'), '-') for a in (90, 210, 330)] + [('N', x, y, r('N'), '-')]
    elif kind == 'H2O':
        d = 0.78 * (r('O') + r('H'))
        out += [('H',) + P(d, 90 + 52.25) + (r('H'), None), ('H',) + P(d, 90 - 52.25) + (r('H'), None), ('O', x, y, r('O'), None)]
    elif kind == 'H2O2':
        d = 0.78 * 2 * r('O'); dh = 0.78 * (r('O') + r('H'))
        o1 = P(d / 2, 180); o2 = P(d / 2, 0)
        h1 = (o1[0] + dh * math.cos(math.radians(rot + 120)), o1[1] + dh * math.sin(math.radians(rot + 120)))
        h2 = (o2[0] + dh * math.cos(math.radians(rot - 60)), o2[1] + dh * math.sin(math.radians(rot - 60)))
        out += [('H',) + h1 + (r('H'), None), ('H',) + h2 + (r('H'), None), ('O',) + o1 + (r('O'), None), ('O',) + o2 + (r('O'), None)]
    elif kind == 'CO2':
        d = 0.78 * 2 * r('O')
        out += [('O',) + P(d, 180) + (r('O'), None), ('O',) + P(d, 0) + (r('O'), None), ('C', x, y, r('C'), None)]
    elif kind == 'CO':
        d = 0.78 * r('O')
        out += [('C',) + P(d, 180) + (r('C'), None), ('O',) + P(d, 0) + (r('O'), None)]
    elif kind == 'CH4':
        d = 0.78 * (r('C') + r('H'))
        out += [('H',) + P(d, a) + (r('H'), None) for a in (45, 135, 225, 315)] + [('C', x, y, r('C'), None)]
    elif kind == 'NH3':
        d = 0.78 * (r('N') + r('H'))
        out += [('H',) + P(d, a) + (r('H'), None) for a in (90, 210, 330)] + [('N', x, y, r('N'), None)]
    elif kind in ('H', 'O', 'N', 'C'):
        out.append((kind, x, y, r(kind), None))
    return out


def M(kind, x, y, s=1.0, rot=0.0, lab=None):
    return ''.join(A(px, py, e, rr, lab if lab is not None else l) for e, px, py, rr, l in atoms(kind, x, y, s, rot))


def bbox(kind, s):
    a = atoms(kind, 0, 0, s)
    return (min(p[1] - p[3] for p in a), max(p[1] + p[3] for p in a), min(p[2] - p[3] for p in a), max(p[2] + p[3] for p in a))


def eqfig(items, cy, x0, s=0.8, gap=14, vgap=10, anim=None):
    """items: [('H2',2), '+', ('O2',1), '->', ...] — 같은 분자 여러 개는 세로로 쌓음. 돌려줌 (svg, x끝, 분자 중심 목록)"""
    out = ''; x = x0; centers = []
    for it in items:
        if it == '+':
            out += T(x + 14, cy + 9, '+', 28, fill=MUT, weight=700); x += 28 + gap
        elif it == '->':
            out += f'<g data-arw="{f(x)},{f(cy)},{f(x + 56)},{f(cy)},ink,3"></g>'; x += 56 + gap
        else:
            k, n = it
            x1, x2, y1, y2 = bbox(k, s); w = x2 - x1; h = y2 - y1
            tot = n * h + (n - 1) * vgap
            for j in range(n):
                cyj = cy - tot / 2 + j * (h + vgap) - y1
                cx = x - x1
                centers.append((k, cx, cyj))
                out += M(k, cx, cyj, s)
            x += w + gap
    return out, x, centers


figs = {}

# ── 표지: 2H2 + O2 → 2H2O, 원자가 반응물 자리에서 생성물로 모임 ──
s = 1.25
start = {'H': [(150, 150), (178, 150), (150, 222), (178, 222)], 'O': [(360, 186), (397, 186)]}
start['H'] = [(118, 150), (162, 150), (118, 230), (162, 230)]
start['O'] = [(360, 190), (407, 190)]
prod = [atoms('H2O', 190, 380, s), atoms('H2O', 350, 380, s)]
cov = '<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="수소 분자 2개와 산소 분자 1개의 원자가 다시 결합해 물 분자 2개가 되는 모형"><circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
# 반응 전 점선 자리
cov += ''.join(A(x, y, 'H', 18 * s, ',d') if False else f'<g data-atom="{x},{y},{f(18*s)},H,-,d"></g>' for x, y in start['H'])
cov += ''.join(f'<g data-atom="{x},{y},{f(24*s)},O,-,d"></g>' for x, y in start['O'])
cov += T(140, 290, '$\\ce{2H2}$', 24, fill=MUT) + T(383, 252, '$\\ce{O2}$', 24, fill=MUT) + T(262, 200, '+', 30, fill=MUT)
cov += '<g data-arw="270,268,270,318,ink,3"></g>'
hi = 0; oi = 0
for mol in prod:
    for e, px, py, rr, l in mol:
        sx, sy = (start['H'][hi] if e == 'H' else start['O'][oi])
        if e == 'H': hi += 1
        else: oi += 1
        cov += f'<g data-anim="move" data-from="{f(sx-px)},{f(sy-py)}" data-dur="1.6" data-delay=".4" data-ease="io">{A(px, py, e, rr)}</g>'
cov += T(270, 478, '$\\ce{2H2 + O2 -&gt; 2H2O}$', 28, weight=700) + T(270, 510, '원자의 종류와 수는 그대로', 21, fill=MUT) + '</svg>'
figs['cover'] = cov

# ── S2 단원 지도 (1-1-1 그림, 오늘 = 2-01) ──
figs['map'] = ('<svg class="fig" viewBox="0 0 1112 150" style="width:1112px" aria-label="대단원 Ⅰ의 단원 지도, 오늘은 중단원 2의 첫 소단원">'
    + T(230, 26, '1. 생활 속 화학과 물질의 양', 19, fill=MUT, weight=700) + '<path d="M70 44 V36 H390 V44" fill="none" stroke="#9FB0C2" stroke-width="2.5"/>'
    + T(710, 26, '2. 화학 반응식', 19, fill=FIELD, weight=700) + '<path d="M550 44 V36 H870 V44" fill="none" stroke="#2E9E6A" stroke-width="2.5"/>'
    + '<line x1="40" y1="60" x2="1072" y2="60" stroke="#C9D3DD" stroke-width="6" stroke-linecap="round"/>'
    + '<path d="M40 60 H600" stroke="#2E9E6A" stroke-width="6" stroke-linecap="round" fill="none" data-anim="draw" data-dur="1.2" data-delay=".3"/>'
    + '<circle cx="120" cy="60" r="11" fill="#2E9E6A"/>' + T(120, 104, '01 화학과 현대||과학·기술·사회', 19, fill=MUT)
    + '<circle cx="340" cy="60" r="11" fill="#2E9E6A"/>' + T(340, 104, '02 몰과||물질의 양', 19, fill=MUT)
    + '<circle cx="600" cy="60" r="14" fill="#2E9E6A"/>' + T(600, 104, '01 화학 반응식의||의미', 20, fill=INK, weight=700)
    + '<circle cx="820" cy="60" r="11" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="4"/>' + T(820, 104, '02 화학 반응의||양적 관계', 19, fill=MUT)
    + '<circle cx="1010" cy="60" r="11" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="4"/>' + T(1010, 104, '대단원 마무리||과학 역량·프로젝트', 19, fill=MUT)
    + '<rect x="622" y="47" width="58" height="26" rx="13" fill="#FFE45C"/>' + T(651, 66, '오늘', 18, weight=700) + '</svg>')


def bun(x, y, w, top=True):
    if top:
        return f'<path d="M{x} {y} Q{x} {y-34} {x+w/2} {y-36} Q{x+w} {y-34} {x+w} {y} Z" fill="#E7B46A" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>' + ''.join(f'<ellipse cx="{x+w*t}" cy="{y-20+abs(t-.5)*14}" rx="3.5" ry="2" fill="#FFF6DD"/>' for t in (.3, .5, .7))
    return f'<path d="M{x} {y} H{x+w} Q{x+w} {y+20} {x+w-10} {y+20} H{x+10} Q{x} {y+20} {x} {y} Z" fill="#E7B46A" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'


def patty(x, y, w):
    return f'<rect x="{x}" y="{y}" width="{w}" height="16" rx="8" fill="#7A4A2A" stroke="{INK}" stroke-width="2.5"/>'


def cheese(x, y, w):
    return f'<path d="M{x} {y} H{x+w} L{x+w-8} {y+10} L{x+w/2} {y+16} L{x+8} {y+10} Z" fill="#F2C230" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'


# ── S2 햄버거 비유 ──
b = '<svg class="fig" viewBox="0 0 560 190" style="width:540px" aria-label="빵 2개, 패티 1장, 치즈 1장이 모여 햄버거 1개가 된다">'
b += bun(20, 70, 80) + bun(20, 110, 80, False) + T(60, 168, '빵 2', 20, weight=700)
b += T(122, 100, '+', 28, fill=MUT, weight=700)
b += patty(142, 82, 80) + T(182, 168, '패티 1', 20, weight=700)
b += T(244, 100, '+', 28, fill=MUT, weight=700)
b += cheese(264, 84, 80) + T(304, 168, '치즈 1', 20, weight=700)
b += '<g data-arw="356,92,404,92,ink,3"></g>'
b += '<g data-anim="pop" data-o="474,90" data-dur=".8" data-delay=".9" data-ease="back">' + bun(424, 66, 100) + cheese(424, 68, 100) + patty(426, 80, 96) + bun(424, 98, 100, False) + '</g>' + T(474, 168, '햄버거 1', 20, weight=700)
figs['burger'] = b + '</svg>'

# ── S5 생각 열기: 그릇 셋 + 말풍선 ──
def bubble(x, y, w, h, txt, tx, ty, d=0):
    return (f'<g data-anim="pop" data-o="{x+w/2},{y+h}" data-dur=".6" data-delay="{d}" data-ease="back"><path d="M{x+14} {y} H{x+w-14} Q{x+w} {y} {x+w} {y+14} V{y+h-14} Q{x+w} {y+h} {x+w-14} {y+h} H{tx+12} L{tx} {ty} L{tx-6} {y+h} H{x+14} Q{x} {y+h} {x} {y+h-14} V{y+14} Q{x} {y} {x+14} {y} Z" fill="#FFFFFF" stroke="{MUT}" stroke-width="2"/>'
            + T(x + w / 2, y + h / 2 + 8 - (12 if '||' in txt else 0), txt, 20) + '</g>')
def bowl(cx, by, lab):
    return (f'<path d="M{cx-58} {by-40} H{cx+58} Q{cx+54} {by} {cx} {by} Q{cx-54} {by} {cx-58} {by-40} Z" fill="#F4F8FC" stroke="#7E8B98" stroke-width="2.5"/>'
            f'<ellipse cx="{cx}" cy="{by-40}" rx="58" ry="9" fill="#FFFFFF" stroke="#7E8B98" stroke-width="2"/>'
            f'<rect x="{cx-50}" y="{by-30}" width="100" height="26" rx="6" fill="#FFF8D6" stroke="{EQUI}" stroke-width="1.6"/>' + T(cx, by - 11, lab, 19, weight=700))
c = '<svg class="fig" viewBox="0 0 1112 250" style="width:1040px" aria-label="화학식이 적힌 그릇 세 개와 서로 다른 언어로 말하지만 화학식으로 통하는 요리사들의 말풍선">'
c += '<rect x="40" y="200" width="1032" height="16" rx="6" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/>'
c += bowl(300, 198, '$\\ce{NaCl}$') + bowl(556, 198, '$\\ce{C12H22O11}$') + bowl(812, 198, '$\\ce{H2O}$')
c += bubble(80, 20, 240, 70, '그릇에 화학식이||표시되어 있어.', 250, 124, .2)
c += bubble(436, 20, 240, 60, 'This is salt.', 560, 118, .5)
c += bubble(792, 20, 260, 70, '언어가 달라도||화학식으로 통하네!', 860, 124, .8)
c += T(300, 242, '소금', 19, fill=MUT) + T(556, 242, '설탕', 19, fill=MUT) + T(812, 242, '물', 19, fill=MUT)
figs['cooks'] = c + '</svg>'

# ── S6 연결: 반응 전 → 원자 → 반응 후 ──
def panel(x, w, title, inner):
    return f'<rect x="{x}" y="14" width="{w}" height="180" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>' + T(x + w / 2, 222, title, 21, weight=700) + inner
s6 = '<svg class="fig" viewBox="0 0 1112 236" style="width:1060px" aria-label="수소 분자 2개와 산소 분자 1개가 원자로 나뉜 뒤 다시 결합하여 물 분자 2개가 된다">'
pre = M('H2', 90, 60) + M('H2', 90, 140) + M('O2', 230, 100)
s6 += panel(20, 300, '반응 전: $\\ce{H2}$ 2개, $\\ce{O2}$ 1개', pre)
s6 += '<g data-arw="334,104,384,104,ink,3"></g>'
mid_pts = {'H': [(450, 60), (530, 60), (450, 148), (530, 148)], 'O': [(620, 72), (620, 140)]}
midg = ''.join(A(x, y, 'H', 18) for x, y in mid_pts['H']) + ''.join(A(x, y, 'O', 24) for x, y in mid_pts['O'])
s6 += '<g class="step" data-g="m1">' + panel(398, 300, '결합이 끊어짐: H 4개, O 2개', midg) + '<g data-arw="712,104,762,104,ink,3"></g></g>'
post = atoms('H2O', 860, 70) + atoms('H2O', 990, 120)
pg = ''; hi = oi = 0
for e, px, py, rr, l in post:
    sx, sy = mid_pts[e][hi if e == 'H' else oi]
    if e == 'H': hi += 1
    else: oi += 1
    pg += f'<g data-anim="move" data-from="{f(sx-px)},{f(sy-py)}" data-dur="1.4" data-on="step" data-ease="io">{A(px, py, e, rr)}</g>'
s6 += '<g class="step" data-g="m2">' + panel(776, 316, '새 결합: $\\ce{H2O}$ 2개 (H 4개, O 2개)', pg) + '</g>'
figs['s6'] = s6 + '</svg>'

# ── S7 1단계 그림: 반응물 | → | 생성물 ──
inner, xe, _ = eqfig([('H2', 1), '+', ('O2', 1), '->', ('H2O', 1)], 80, 60, s=1.0, gap=20)
s7 = '<svg class="fig" viewBox="0 0 520 210" style="width:500px" aria-label="반응물 수소와 산소는 화살표 왼쪽, 생성물 물은 오른쪽">' + inner
s7 += '<path d="M54 140 V152 H280 V140" fill="none" stroke="#5B6B7F" stroke-width="2"/>' + T(167, 180, '반응물 (왼쪽)', 21, weight=700)
s7 += '<path d="M372 140 V152 H470 V140" fill="none" stroke="#5B6B7F" stroke-width="2"/>' + T(421, 180, '생성물 (오른쪽)', 21, weight=700)
s7 += T(326, 52, '반응의 진행', 19, fill=MUT) + '</svg>'
figs['s7'] = s7


# ── S8 단계 카드 3장 ──
def card(items, aria):
    inner, xe, _ = eqfig(items, 70, 12, s=0.62, gap=8, vgap=6)
    return f'<svg viewBox="0 0 {int(xe+6)} 140" aria-label="{aria}"><g data-anim="pop" data-o="{xe/2},70" data-dur=".6" data-on="step" data-ease="back">{inner}</g></svg>'
figs['k1'] = card([('H2', 1), '+', ('O2', 1), '->', ('H2O', 1)], '수소 분자 1개, 산소 분자 1개, 물 분자 1개')
figs['k2'] = card([('H2', 1), '+', ('O2', 1), '->', ('H2O', 2)], '수소 분자 1개, 산소 분자 1개, 물 분자 2개')
figs['k3'] = card([('H2', 2), '+', ('O2', 1), '->', ('H2O', 2)], '수소 분자 2개, 산소 분자 1개, 물 분자 2개')

# ── S9 H2O vs H2O2 ──
s9 = '<svg class="fig" viewBox="0 0 520 200" style="width:520px" aria-label="물 분자와 과산화 수소 분자 모형 비교">'
s9 += '<rect x="10" y="10" width="240" height="180" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>' + M('H2O', 130, 80)
s9 += T(130, 150, '물 $\\ce{H2O}$', 22, weight=700) + T(130, 178, '마시는 물', 19, fill=MUT)
s9 += '<rect x="270" y="10" width="240" height="180" rx="14" fill="#FFF4EC" stroke="#E08A2C" stroke-width="2"/>' + M('H2O2', 390, 84)
s9 += T(390, 150, '과산화 수소 $\\ce{H2O2}$', 22, weight=700) + T(390, 178, '소독약 — 다른 물질', 19, fill=MUT) + '</svg>'
figs['s9'] = s9


# ── 반응식 + 상태 기호 라벨 (SVG 안에서 항마다 배치) ──
def termrow(terms, w, h, y=50, size=30):
    """terms: [(x, tex, 아래라벨)] ; tex '->' 이면 화살표"""
    o = f'<svg class="fig" viewBox="0 0 {w} {h}" style="width:{w}px" aria-label="상태 기호를 붙인 화학 반응식과 각 물질의 상태">'
    for j, (x, tx, lab) in enumerate(terms):
        if tx == '->':
            o += f'<g data-arw="{x-34},{y-10},{x+34},{y-10},ink,3"></g>'
        elif tx == '+':
            o += T(x, y, '+', size)
        else:
            o += T(x, y, f'$\\ce{{{tx}}}$', size, weight=700)
            if lab:
                o += f'<g data-anim="fade" data-dur=".6" data-delay="{.3+j*.25:.2f}"><line x1="{x}" y1="{y+14}" x2="{x}" y2="{y+36}" stroke="{MUT}" stroke-width="2"/>' + T(x, y + 62, lab, 20, fill=MUT) + '</g>'
    return o + '</svg>'
figs['s10'] = termrow([(110, '2H2(g)', '수소 기체'), (225, '+', ''), (330, 'O2(g)', '산소 기체'), (450, '->', ''), (580, '2H2O(l)', '액체인 물')], 700, 130)

inner, xe, _ = eqfig([('CO', 2), '+', ('O2', 1), '->', ('CO2', 2)], 70, 10, s=0.62, gap=10, vgap=8)
figs['s11'] = f'<svg class="fig" viewBox="0 0 {int(xe+10)} 140" style="width:{int(xe+10)}px" aria-label="일산화 탄소 분자 2개와 산소 분자 1개가 이산화 탄소 분자 2개가 된다">{inner}</svg>'

# ── S13 철핀 녹 ──
s13 = '<svg class="fig" viewBox="0 0 420 220" style="width:400px" aria-label="욕실의 철핀에 붉은 녹이 생긴 모습">'
s13 += '<rect x="10" y="10" width="400" height="200" rx="16" fill="#EAF4F7" stroke="#9FC3DD" stroke-width="2"/>'
for j in range(6):
    s13 += f'<line x1="{30+j*64}" y1="10" x2="{30+j*64}" y2="210" stroke="#D3E6EC" stroke-width="2"/>'
s13 += '<g transform="rotate(-14 210 110)"><rect x="70" y="96" width="280" height="22" rx="11" fill="#9AA5B1" stroke="#16233D" stroke-width="2.5"/><path d="M350 96 Q384 96 384 107 Q384 118 350 118" fill="#9AA5B1" stroke="#16233D" stroke-width="2.5"/>'
s13 += '<g data-anim="fade" data-dur="1.6" data-delay=".5">' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="7" fill="#B5562A" opacity=".85"/>' for x, y, rx in [(110, 106, 16), (160, 110, 22), (232, 104, 14), (290, 109, 20), (340, 105, 12)]) + '</g></g>'
s13 += T(210, 196, '붉은색 녹 = 산화 철(III) $\\ce{Fe2O3}$', 20, weight=700, halo=True) + '</svg>'
figs['s13'] = s13

# ── S14 호흡: 세포 ──
s14 = '<svg class="fig" viewBox="0 0 420 230" style="width:400px" aria-label="세포가 포도당과 산소를 받아 이산화 탄소와 물을 내보낸다">'
s14 += '<ellipse cx="210" cy="118" rx="120" ry="84" fill="#FDECEC" stroke="#D99" stroke-width="2.5"/><ellipse cx="236" cy="128" rx="30" ry="22" fill="#F6C7C7" stroke="#C88" stroke-width="2"/>'
s14 += T(190, 104, '세포', 22, weight=700)
s14 += '<g data-arw="40,62,112,92,ink,3"></g>' + T(20, 40, '$\\ce{C6H12O6}$, $\\ce{O2}$', 20, anchor='start', weight=700)
s14 += '<g data-arw="310,150,400,184,ink,3"></g>' + T(410, 214, '$\\ce{CO2}$, $\\ce{H2O}$', 20, anchor='end', weight=700) + '</svg>'
figs['s14'] = s14

# ── S16 톡톡 사탕 ──
import random
rnd = random.Random(7)
s16 = '<svg class="fig" viewBox="0 0 420 250" style="width:400px" aria-label="입속 침에 녹은 사탕에서 이산화 탄소 기포가 생겨 터진다">'
s16 += '<path d="M30 200 Q210 250 390 200 V236 H30 Z" fill="#F7C9C9" stroke="#C88" stroke-width="2"/>' + T(210, 232, '침', 19, fill=MUT)
cols = ['#F48FB1', '#81D4FA', '#FFF176', '#A5D6A7', '#CE93D8']
for j in range(14):
    x = 90 + rnd.random() * 240; y = 180 + rnd.random() * 22
    s16 += f'<rect x="{f(x)}" y="{f(y)}" width="14" height="9" rx="4" fill="{cols[j%5]}" stroke="#16233D" stroke-width="1.2" transform="rotate({rnd.randint(-40,40)} {f(x+7)} {f(y+4)})"/>'
for j in range(9):
    x = 100 + j * 26 + rnd.random() * 8; y = 70 + rnd.random() * 80; r = 7 + rnd.random() * 8
    s16 += f'<g data-anim="move" data-from="0,{int(150-y+30)}" data-dur="{1.4+rnd.random():.1f}" data-delay="{j*.15:.2f}" data-rep="loop" data-ease="out"><circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#FFFFFF" fill-opacity=".6" stroke="#7FB6D9" stroke-width="2"/></g>'
s16 += T(210, 40, '$\\ce{CO2}$ 기포 — 톡톡!', 22, weight=700, halo=True) + '</svg>'
figs['s16'] = s16

# ── S17 발포 바이타민 ──
s17 = '<svg class="fig" viewBox="0 0 520 250" style="width:500px" aria-label="물컵 속 발포 바이타민에서 기포가 올라오고, 용기 뚜껑에 제습제가 들어 있다">'
s17 += '<path d="M40 40 L58 220 H182 L200 40" fill="#EEF8E4" stroke="#7E8B98" stroke-width="3"/><rect x="50" y="70" width="140" height="6" fill="#CFE8B8"/>'
s17 += '<path d="M46 76 L58 220 H182 L194 76 Z" fill="#DDF0C8" opacity=".9"/><ellipse cx="120" cy="208" rx="34" ry="8" fill="#F5E6B8" stroke="#B9A24A" stroke-width="2"/>'
for j in range(7):
    x = 92 + j * 9 + (j % 2) * 4; y = 110 + (j * 13) % 70
    s17 += f'<g data-anim="move" data-from="0,{int(200-y)}" data-dur="{1.3+j*.12:.2f}" data-delay="{j*.18:.2f}" data-rep="loop" data-ease="out"><circle cx="{x}" cy="{y}" r="{5+j%3}" fill="#FFFFFF" fill-opacity=".7" stroke="#7FB6D9" stroke-width="1.8"/></g>'
s17 += T(120, 246, '물에 넣은 알약', 19, fill=MUT)
s17 += '<rect x="270" y="120" width="200" height="60" rx="10" fill="#7CC36E" stroke="#16233D" stroke-width="2.5"/><rect x="470" y="114" width="36" height="72" rx="6" fill="#FFFFFF" stroke="#16233D" stroke-width="2.5"/>'
s17 += '<rect x="478" y="126" width="20" height="48" rx="4" fill="#E3EEFB" stroke="#1F6FD1" stroke-width="1.8" stroke-dasharray="4 3"/>' + T(488, 216, '뚜껑 속 제습제', 19, anchor='end', weight=700)
s17 += '<line x1="488" y1="174" x2="480" y2="196" stroke="#5B6B7F" stroke-width="1.8"/>' + T(370, 158, '발포 바이타민', 20, fill='#FFFFFF', weight=700) + '</svg>'
figs['s17'] = s17

# ── S19 N2 + 3H2 → 2NH3 (원자 재배열) ──
s = 0.9
inner_l, xl, cl = eqfig([('N2', 1), '+', ('H2', 3)], 110, 30, s=s, gap=22, vgap=10)
# 생성물: 반응물 원자에서 출발
prod = atoms('NH3', 0, 0, s)
rc = [a for k, cx, cy in cl for a in atoms(k, cx, cy, s)]
Ns = [(p[1], p[2]) for p in rc if p[0] == 'N']; Hs = [(p[1], p[2]) for p in rc if p[0] == 'H']
xs = xl + 70
o = '<svg class="fig" viewBox="0 0 640 230" style="width:620px" aria-label="질소 분자 1개와 수소 분자 3개의 원자가 다시 결합해 암모니아 분자 2개가 된다">'
o += ''.join(f'<g data-atom="{f(x)},{f(y)},{f(R["N"]*s)},N,-,d"></g>' for x, y in Ns) + ''.join(f'<g data-atom="{f(x)},{f(y)},{f(R["H"]*s)},H,-,d"></g>' for x, y in Hs)
o += T(cl[0][1] + 18 * 0, 220, '', 1) if False else ''
o += T((cl[0][1]), 212, '질소 $\\ce{N2}$', 20) + T(cl[1][1], 212, '수소 $\\ce{3H2}$', 20)
o += f'<g data-arw="{f(xl)},110,{f(xl+56)},110,ink,3"></g>'
hi = ni = 0
for j, cy in enumerate((70, 150)):
    for e, px, py, rr, l in atoms('NH3', xs + 70, cy, s):
        sx, sy = (Ns[ni] if e == 'N' else Hs[hi])
        if e == 'N': ni += 1
        else: hi += 1
        o += f'<g data-anim="move" data-from="{f(sx-px)},{f(sy-py)}" data-dur="1.6" data-delay=".4" data-ease="io">{A(px, py, e, rr)}</g>'
o += T(xs + 70, 212, '암모니아 $\\ce{2NH3}$', 20) + T((cl[0][1] + cl[1][1]) / 2, 120, '+', 28, fill=MUT) + '</svg>'
figs['s19'] = o


# ── S20 물질의 양 더미 ──
def pile(cx, by, col, st, n=1):
    out = ''
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * 92
        out += f'<path d="M{x-40} {by} Q{x} {by-70} {x+40} {by} Z" fill="{col}" stroke="{st}" stroke-width="2"/><ellipse cx="{x}" cy="{by+4}" rx="46" ry="7" fill="#E8D7A6" stroke="#B9A24A" stroke-width="2"/>'
    return out
s20 = '<svg class="fig" viewBox="0 0 900 132" style="width:860px" aria-label="질소 1 몰, 수소 3 몰, 암모니아 2 몰의 더미">'
s20 += '<g data-anim="pop" data-o="110,96" data-dur=".6" data-ease="back">' + pile(110, 80, '#4F6BD8', '#2E46A8') + '</g>'
s20 += '<g data-anim="pop" data-o="420,96" data-dur=".6" data-delay=".3" data-ease="back">' + pile(420, 80, '#F4F6F8', '#9AA5B1', 3) + '</g>'
s20 += '<g data-anim="pop" data-o="760,96" data-dur=".6" data-delay=".6" data-ease="back">' + pile(760, 80, '#8FA4E8', '#2E46A8', 2) + '</g>'
s20 += T(110, 118, '1 몰', 20, weight=700) + T(420, 118, '3 몰', 20, weight=700) + T(760, 118, '2 몰', 20, weight=700) + '</svg>'
figs['s20'] = s20


# ── S21 22.4 L 상자 ──
def cube(x, y, d=0):
    return (f'<g data-anim="pop" data-o="{x+40},{y+80}" data-dur=".5" data-delay="{d:.2f}" data-ease="back"><rect x="{x}" y="{y+14}" width="70" height="70" fill="#E3F2F8" stroke="#7FB6D9" stroke-width="2"/>'
            f'<path d="M{x} {y+14} l14 -14 h70 l-14 14 z M{x+70} {y+14} l14 -14 v70 l-14 14 z" fill="#CBE6F2" stroke="#7FB6D9" stroke-width="2"/>' + T(x + 35, y + 56, '22.4 L', 18, weight=700) + '</g>')
s21 = '<svg class="fig" viewBox="0 0 900 110" style="width:860px" aria-label="22.4 L 상자 1개, 3개, 2개">'
s21 += cube(70, 6) + ''.join(cube(300 + k * 92, 6, .25 + k * .15) for k in range(3)) + ''.join(cube(680 + k * 92, 6, .8 + k * .15) for k in range(2))
figs['s21'] = s21 + '</svg>'

# ── S22 질량 막대 (비례) ──
s22 = '<svg class="fig" viewBox="0 0 470 280" style="width:440px" aria-label="질소 28 g과 수소 6 g이 반응해 암모니아 34 g이 된다, 막대 길이는 질량에 비례">'
k = 5.6
s22 += f'<line x1="40" y1="240" x2="450" y2="240" stroke="{MUT}" stroke-width="2"/>'
s22 += f'<g data-anim="scale" data-from="1,0" data-o="110,240" data-dur="1" data-on="step"><rect x="80" y="{240-28*k}" width="60" height="{28*k}" fill="#4F6BD8"/><rect x="80" y="{240-34*k}" width="60" height="{6*k}" fill="#F4F6F8" stroke="#9AA5B1" stroke-width="2"/></g>'
s22 += T(110, 240 - 28 * k / 2 + 8, '28 g', 20, fill='#FFFFFF', weight=700) + T(110, 240 - 31 * k + 7, '6 g', 19, weight=700)
s22 += T(110, 266, '$\\ce{N2}$ + $\\ce{3H2}$', 20)
s22 += f'<g data-anim="scale" data-from="1,0" data-o="330,240" data-dur="1" data-delay=".4" data-on="step"><rect x="300" y="{240-34*k}" width="60" height="{34*k}" fill="#8FA4E8"/></g>' + T(330, 240 - 17 * k + 8, '34 g', 20, weight=700)
s22 += T(330, 266, '$\\ce{2NH3}$', 20) + f'<line x1="150" y1="{240-34*k}" x2="290" y2="{240-34*k}" stroke="{MUT}" stroke-width="2" stroke-dasharray="6 5"/>' + T(220, 240 - 34 * k - 10, '같은 높이 = 질량 보존', 19, fill=MUT) + '</svg>'
figs['s22'] = s22

# ── S26 진주와 식초 ──
s26 = '<svg class="fig" viewBox="0 0 360 240" style="width:340px" aria-label="식초가 담긴 컵 속 진주 표면에서 기포가 생긴다">'
s26 += '<path d="M60 30 L80 220 H280 L300 30" fill="#FFFDF3" stroke="#7E8B98" stroke-width="3"/><path d="M68 80 L80 220 H280 L292 80 Z" fill="#F6EFD2"/>'
s26 += '<circle cx="180" cy="196" r="22" fill="#FBFBFF" stroke="#B8B8D0" stroke-width="2"/><circle cx="173" cy="189" r="6" fill="#FFFFFF"/>'
for j in range(5):
    x = 166 + j * 7; y = 150 - j * 12
    s26 += f'<g data-anim="move" data-from="0,{int(170-y)}" data-dur="{1.5+j*.15:.2f}" data-delay="{j*.25:.2f}" data-rep="loop" data-ease="out"><circle cx="{x}" cy="{y}" r="5" fill="#FFFFFF" stroke="#C9B48A" stroke-width="1.6"/></g>'
s26 += T(180, 64, '식초 (아세트산)', 20, weight=700) + T(250, 200, '진주', 19, anchor='start', fill=MUT) + '</svg>'
figs['s26'] = s26

# ── S32 문항 05 모형 ──
def box(x, mols):
    o = f'<rect x="{x}" y="10" width="220" height="170" rx="10" fill="#E8F5F3" stroke="#4FB3A6" stroke-width="2.5"/>'
    for j, (k, px, py, rot) in enumerate(mols):
        dx, dy = [(5, 4), (-5, 5), (5, -4), (-4, -5), (4, 5), (-5, -4)][j]
        o += f'<g data-anim="move" data-from="{dx},{dy}" data-rep="alt" data-dur="{1.8+j*.2:.1f}" data-ease="sine">{M(k, x+px, py, 0.75, rot)}</g>'
    return o
s32 = '<svg class="fig" viewBox="0 0 560 220" style="width:560px" aria-label="반응 전 A2 분자 3개와 B2 분자 3개, 반응 후 AB3 분자 2개와 A2 분자 2개">'
s32 += box(10, [('A2', 50, 50, 0), ('B2', 160, 44, 30), ('B2', 60, 140, -20), ('A2', 160, 140, 20), ('B2', 110, 96, 0), ('A2', 50, 96, 0)][:0] + [('A2', 60, 48, 0), ('B2', 168, 46, 30), ('B2', 54, 102, 0), ('A2', 158, 104, -25), ('A2', 70, 150, 10), ('B2', 170, 150, -20)])
s32 += '<g data-arw="242,95,312,95,grav,6"></g>'
s32 += box(328, [('AB3', 60, 58, 0), ('A2', 160, 50, 10), ('A2', 64, 140, -15), ('AB3', 162, 128, 0)])
s32 += T(120, 206, '반응 전', 20) + T(438, 206, '반응 후', 20) + '</svg>'
figs['s32'] = s32

tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
out = re.sub(r'\{\{(\w+)\}\}', lambda m: figs[m.group(1)], tpl)
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', len(out))
