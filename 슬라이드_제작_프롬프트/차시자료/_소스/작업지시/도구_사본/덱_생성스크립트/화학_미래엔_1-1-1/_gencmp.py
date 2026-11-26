# 1-1-1 덱 그림 생성: slides.tpl.html 의 {{이름}} 자리에 그림 SVG 조각을 넣어 content/.../slides.html 을 만든다.
import math, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs
f = figs.f
R = {'H': 18, 'C': 24, 'N': 24, 'O': 24, 'Si': 29, 'Fe': 28, 'Ca': 32}
INK, MUT, FIELD, EQUI, PLUS, MINUS = '#16233D', '#5B6B7F', '#2E9E6A', '#E08A2C', '#D7263D', '#1F6FD1'
OUT = '/tmp/claude-0/-home-user-highscoolchem-zae1212/ef5e781b-b8a4-55f5-a263-b98d9fe249ad/scratchpad/화학_미래엔_1-1-1/_cmp.html'
HERE = os.path.dirname(os.path.abspath(__file__))


def A(x, y, el, lab=''):
    return f'<g data-atom="{f(x)},{f(y)},{R[el]},{el}{("," + lab) if lab else ""}"></g>'


def T(x, y, s, size=20, anchor='middle', fill=None, weight=None, halo=False, tex=False, extra=''):
    a = f'data-tex="{s}"' if tex else f'data-mix="{s}"'
    return (f'<text class="tex" x="{f(x)}" y="{f(y)}" {a} data-size="{size}" data-anchor="{anchor}"'
            + (f' fill="{fill}"' if fill else '') + (f' data-weight="{weight}"' if weight else '')
            + (' data-halo="1"' if halo else '') + (f' {extra}' if extra else '') + '></text>')


def mol(kind, x, y):
    """분자 안 원자 (원소, x, y) — 그리는 순서(뒤 → 앞)"""
    d2, dh, dhx = 37, 28, 33
    if kind in ('N2', 'O2'):
        e = kind[0]
        return [(e, x - d2 / 2, y), (e, x + d2 / 2, y)]
    if kind == 'H2':
        return [('H', x - dh / 2, y), ('H', x + dh / 2, y)]
    if kind == 'NH3':
        hs = [('H', x + dhx * math.cos(math.radians(a)), y + dhx * math.sin(math.radians(a))) for a in (90, 210, 330)]
        return hs + [('N', x, y)]
    if kind == 'CH4':
        hs = [('H', x + dhx * math.cos(math.radians(a)), y + dhx * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]
        return hs + [('C', x, y)]
    if kind == 'CO2':
        return [('O', x - d2, y), ('O', x + d2, y), ('C', x, y)]
    if kind == 'H2O':
        a = math.radians(52.25)
        return [('H', x - dhx * math.sin(a), y + dhx * math.cos(a)), ('H', x + dhx * math.sin(a), y + dhx * math.cos(a)), ('O', x, y)]
    raise ValueError(kind)


def mols(lst):
    out = []
    for k, x, y in lst:
        out += mol(k, x, y)
    return out


def static(atoms):
    return ''.join(A(x, y, e) for e, x, y in atoms)


def rearrange(react, prod, dur=1.4, delay=.5, on=None):
    """반응 전 원자(react) 자리에서 반응 후 원자(prod) 자리로 같은 원소를 순서대로 옮김 (원자 수 보존 검사)"""
    pool = {}
    for e, x, y in react:
        pool.setdefault(e, []).append((x, y))
    cnt = {e: len(v) for e, v in pool.items()}
    pc = {}
    for e, _, _ in prod:
        pc[e] = pc.get(e, 0) + 1
    assert cnt == pc, (cnt, pc)
    s = ''
    for e, x, y in prod:
        sx, sy = pool[e].pop(0)
        s += (f'<g data-anim="move" data-from="{f(sx - x)},{f(sy - y)}" data-dur="{dur}" data-delay="{delay}" data-ease="soft"'
              + (f' data-on="{on}"' if on else '') + f'>{A(x, y, e)}</g>')
    return s


def plus(x, y):
    return T(x, y + 10, '+', 28, fill=INK, tex=True)


# ───────── 표지: 암모니아 공-막대
def cover():
    s = figs.ballstick(270, 200, 'N', ['H', 'H', 'H'], n_lone=1, ang=107, L=150, yaw=28, pitch=12, scale=1.5, lobes=False, anim_out=-0.55)
    lines = re.findall(r'<line [^>]*/>', s)
    s = ''.join(lines) + re.sub(r'<line [^>]*/>', '', s)
    return (f'<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="질소 원자 하나에 수소 원자 세 개가 결합한 암모니아 공-막대 모형">'
            f'<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>{s}'
            + T(270, 430, '암모니아 $\\ce{NH3}$', 26, weight=700)
            + T(270, 462, '공기 속 질소로 만든 비료의 원료', 21, fill=MUT) + '</svg>')


# ───────── 대단원 지도 (1112×200)
def unitmap(cur=0):
    xs = [120, 340, 600, 820, 1010]
    names = ['01 화학과 현대||과학·기술·사회', '02 몰과||물질의 양', '01 화학 반응식의||의미', '02 화학 반응의||양적 관계', '대단원 마무리||과학 역량·프로젝트']
    pages = ['13–17쪽', '18–26쪽', '31–35쪽', '36–40쪽', '44–49쪽']
    s = (T(230, 26, '1. 생활 속 화학과 물질의 양', 19, weight=700, fill=FIELD)
         + '<path d="M70 44 V36 H390 V44" fill="none" stroke="#2E9E6A" stroke-width="2.5"/>'
         + T(710, 26, '2. 화학 반응식', 19, weight=700, fill=MUT)
         + '<path d="M550 44 V36 H870 V44" fill="none" stroke="#9FB0C2" stroke-width="2.5"/>')
    s += '<line x1="40" y1="60" x2="1072" y2="60" stroke="#C9D3DD" stroke-width="6" stroke-linecap="round"/>'
    s += f'<path d="M40 60 H{xs[cur]}" stroke="#2E9E6A" stroke-width="6" stroke-linecap="round" fill="none" data-anim="draw" data-dur="1" data-delay=".3"/>'
    for i, x in enumerate(xs):
        col = FIELD if i <= 1 else '#9FB0C2'
        if i == cur:
            s += f'<circle cx="{x}" cy="60" r="14" fill="#2E9E6A"/>'
        else:
            s += f'<circle cx="{x}" cy="60" r="11" fill="#FFFFFF" stroke="{col}" stroke-width="4"/>'
        s += T(x, 110, names[i], 20, weight=700 if i == cur else None, fill=INK if i == cur else MUT)
        s += T(x, 182, pages[i], 19, fill=MUT)
    x = xs[cur]
    s += f'<rect x="{x + 22}" y="47" width="58" height="26" rx="13" fill="#FFE45C"/>' + T(x + 51, 66, '오늘', 18, weight=700)
    return f'<svg class="fig" viewBox="0 0 1112 200" style="width:1112px" aria-label="대단원 Ⅰ의 중단원과 소단원 지도, 오늘은 첫 소단원">{s}</svg>'


# ───────── 생활 아이콘 (중심 cx, cy, 크기 약 80)
def icon(kind, cx, cy):
    st = 'stroke="#16233D" stroke-width="2.5" stroke-linejoin="round"'
    if kind == 'bread':
        return (f'<path d="M{cx-38} {cy+22} V{cy-6} Q{cx-38} {cy-30} {cx} {cy-30} Q{cx+38} {cy-30} {cx+38} {cy-6} V{cy+22} Z" fill="#F3D9A4" {st}/>'
                f'<path d="M{cx-18} {cy-12} l8 -8 M{cx-2} {cy-12} l8 -8 M{cx+14} {cy-12} l8 -8" stroke="#B9873A" stroke-width="2.5" stroke-linecap="round"/>')
    if kind == 'shirt':
        return (f'<path d="M{cx-14} {cy-32} L{cx-40} {cy-18} L{cx-30} {cy} L{cx-22} {cy-4} V{cy+30} H{cx+22} V{cy-4} L{cx+30} {cy} L{cx+40} {cy-18} L{cx+14} {cy-32} Q{cx} {cy-20} {cx-14} {cy-32} Z" fill="#CFE3F7" {st}/>'
                f'<path d="M{cx-22} {cy+8} H{cx+22}" stroke="#6E9CCB" stroke-width="3"/>')
    if kind == 'brush':
        return (f'<rect x="{cx-40}" y="{cy+4}" width="64" height="12" rx="6" fill="#9ED7C3" {st}/>'
                f'<rect x="{cx+16}" y="{cy-14}" width="26" height="18" rx="3" fill="#FFFFFF" {st}/>'
                f'<path d="M{cx+21} {cy-14} V{cy-26} M{cx+29} {cy-14} V{cy-26} M{cx+37} {cy-14} V{cy-26}" stroke="#6E9CCB" stroke-width="3" stroke-linecap="round"/>')
    if kind == 'pill':
        return (f'<g transform="rotate(-35 {cx} {cy})"><rect x="{cx-36}" y="{cy-14}" width="72" height="28" rx="14" fill="#FFFFFF" {st}/>'
                f'<path d="M{cx} {cy-14} H{cx+22} A14 14 0 0 1 {cx+22} {cy+14} H{cx} Z" fill="#F4A7B4" stroke="#16233D" stroke-width="2.5"/></g>')
    if kind == 'phone':
        return (f'<rect x="{cx-20}" y="{cy-34}" width="40" height="68" rx="7" fill="#3A3F47" {st}/>'
                f'<rect x="{cx-15}" y="{cy-27}" width="30" height="50" rx="2" fill="#BFE0F5"/><circle cx="{cx}" cy="{cy+29}" r="2.5" fill="#FFFFFF"/>')
    if kind == 'bus':
        return (f'<rect x="{cx-40}" y="{cy-26}" width="80" height="46" rx="8" fill="#FBE3B0" {st}/>'
                f'<rect x="{cx-33}" y="{cy-19}" width="66" height="16" rx="2" fill="#BFE0F5" stroke="#16233D" stroke-width="1.8"/>'
                f'<circle cx="{cx-22}" cy="{cy+22}" r="8" fill="#16233D"/><circle cx="{cx+22}" cy="{cy+22}" r="8" fill="#16233D"/>')
    if kind == 'house':
        return (f'<path d="M{cx-40} {cy-4} L{cx} {cy-36} L{cx+40} {cy-4}" fill="none" stroke="#16233D" stroke-width="3" stroke-linejoin="round"/>'
                f'<rect x="{cx-30}" y="{cy-8}" width="60" height="40" fill="#E9EEF3" {st}/>'
                f'<rect x="{cx-20}" y="{cy+2}" width="14" height="14" fill="#BFE0F5" stroke="#16233D" stroke-width="1.8"/><rect x="{cx+4}" y="{cy+6}" width="14" height="26" fill="#C9A27A" stroke="#16233D" stroke-width="1.8"/>')
    raise ValueError(kind)


def life6():
    items = [('bread', '빵'), ('shirt', '운동복'), ('brush', '칫솔'), ('pill', '감기약'), ('phone', '스마트폰'), ('bus', '버스')]
    s = ''
    for i, (k, n) in enumerate(items):
        cx = 90 + i * 186
        s += f'<g data-anim="pop" data-o="{cx},70" data-dur=".7" data-delay="{.2 + i * .15:.2f}" data-ease="back"><circle cx="{cx}" cy="70" r="62" fill="#F4F7FA" stroke="#C9D3DD" stroke-width="2"/>{icon(k, cx, 72)}</g>'
        s += T(cx, 166, n, 21, weight=700)
    return f'<svg class="fig" viewBox="0 0 1112 180" style="width:1112px" aria-label="빵, 운동복, 칫솔, 감기약, 스마트폰, 버스 그림">{s}</svg>'


def unit4():
    items = [('bread', '빵', '질소 비료'), ('shirt', '옷', '합성 섬유'), ('house', '집', '철·시멘트'), ('phone', '스마트폰', '반도체·전지')]
    s = ''
    for i, (k, n, tag) in enumerate(items):
        cx = 70 + i * 140
        s += f'<circle cx="{cx}" cy="64" r="56" fill="#F4F7FA" stroke="#C9D3DD" stroke-width="2"/>{icon(k, cx, 66)}'
        s += T(cx, 148, n, 20, weight=700)
        s += (f'<g data-anim="fade" data-dur=".6" data-delay="{.5 + i * .35:.2f}"><rect x="{cx - 58}" y="160" width="116" height="34" rx="17" fill="#E6F4EC" stroke="#2E9E6A" stroke-width="2"/>'
              + T(cx, 184, tag, 19, fill='#1B5E3F', weight=700) + '</g>')
    return f'<svg class="fig" viewBox="0 0 560 204" style="width:540px" aria-label="빵, 옷, 집, 스마트폰과 각각에 쓰인 화학: 질소 비료, 합성 섬유, 철과 시멘트, 반도체와 전지">{s}</svg>'


# ───────── 화학과 인류의 문제 (허브)
def hub():
    cx, cy, r = 300, 196, 74
    names = ['식량', '의류', '주거', '건강', '에너지', '환경', '첨단 기술']
    s = ''
    for i, n in enumerate(names):
        a = math.radians(-90 + i * 360 / 7)
        bx, by = cx + 205 * math.cos(a), cy + 150 * math.sin(a)
        x1, y1 = cx + (r + 8) * math.cos(a), cy + (r + 8) * math.sin(a)
        # 상자 가장자리까지
        w, h = 120, 44
        tx = (w / 2 + 6) / abs(math.cos(a)) if abs(math.cos(a)) > 1e-6 else 1e9
        ty = (h / 2 + 6) / abs(math.sin(a)) if abs(math.sin(a)) > 1e-6 else 1e9
        t = min(tx, ty)
        x2, y2 = bx - t * math.cos(a), by - t * math.sin(a)
        s += f'<g data-arw="{f(x1)},{f(y1)},{f(x2)},{f(y2)},field,3"></g>'
        s += f'<rect x="{f(bx - w / 2)}" y="{f(by - h / 2)}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>'
        s += T(bx, by + 8, n, 21, weight=700)
    s += (f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".8" data-ease="back"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#E6F4EC" stroke="#2E9E6A" stroke-width="3"/>'
          + T(cx, cy - 4, '화학', 30, weight=700, fill='#1B5E3F') + T(cx, cy + 26, '새 물질·새 반응', 18, fill='#1B5E3F') + '</g>')
    return f'<svg class="fig" viewBox="0 0 600 392" style="width:560px" aria-label="가운데 화학에서 식량, 의류, 주거, 건강, 에너지, 환경, 첨단 기술로 뻗어 나가는 화살표">{s}</svg>'


# ───────── 공기 속 질소
def air():
    s = '<rect x="16" y="40" width="300" height="230" rx="16" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2.5" stroke-dasharray="8 6"/>'
    s += T(166, 28, '공기', 21, weight=700)
    pos = [('N2', 80, 92), ('N2', 230, 84), ('O2', 158, 150), ('N2', 76, 218), ('N2', 248, 214)]
    for i, (k, x, y) in enumerate(pos):
        dx, dy = [(10, -6), (-8, 8), (6, 8), (-10, -5), (8, -8)][i]
        s += f'<g data-anim="move" data-from="{dx},{dy}" data-rep="alt" data-dur="{1.4 + i * .2:.1f}" data-ease="io">' + static(mol(k, x, y)) + '</g>'
    s += T(166, 300, '질소 $\\ce{N2}$ 약 78 %, 산소 $\\ce{O2}$ 약 21 % (부피)', 19, fill=MUT)
    # 식물
    px = 470
    s += f'<path d="M{px} 262 V150" stroke="#2E9E6A" stroke-width="5" stroke-linecap="round"/>'
    s += f'<path d="M{px} 200 Q{px-46} 186 {px-58} 150 Q{px-14} 160 {px} 200 Z" fill="#9BD86F" stroke="#2E9E6A" stroke-width="2.5"/>'
    s += f'<path d="M{px} 176 Q{px+46} 160 {px+56} 122 Q{px+12} 134 {px} 176 Z" fill="#9BD86F" stroke="#2E9E6A" stroke-width="2.5"/>'
    s += f'<path d="M{px-60} 262 H{px+60}" stroke="#8C6A4A" stroke-width="6" stroke-linecap="round"/>'
    s += T(px, 300, '식물', 21, weight=700)
    s += '<g data-arw="326,150,396,150,muted,3,d"></g>'
    s += f'<g stroke="{PLUS}" stroke-width="5" stroke-linecap="round"><line x1="346" y1="128" x2="376" y2="158"/><line x1="376" y1="128" x2="346" y2="158"/></g>'
    s += T(361, 196, '직접||못 씀', 19, fill=PLUS, weight=700)
    return f'<svg class="fig" viewBox="0 0 560 312" style="width:540px" aria-label="공기 속 질소 분자와 산소 분자, 식물은 공기 중의 질소를 직접 쓰지 못한다">{s}</svg>'


# ───────── 하버·보슈 공정: 반응 탑 (현상)
def reactor():
    s = ''
    s += '<rect x="110" y="70" width="110" height="200" rx="40" fill="#E9EEF3" stroke="#16233D" stroke-width="3"/>'
    s += '<rect x="126" y="140" width="78" height="70" rx="6" fill="#C7743D" fill-opacity=".35" stroke="#874A20" stroke-width="2" stroke-dasharray="5 4"/>'
    s += T(165, 182, '철 촉매', 23, weight=700, fill='#874A20')
    s += '<g data-arw="20,110,104,110,ink,3"></g>' + T(48, 96, '$\\ce{N2}$, $\\ce{H2}$', 23, anchor='middle')
    s += '<g data-arw="226,230,310,230,ink,3"></g>' + T(270, 216, '$\\ce{NH3}$', 23)
    s += T(165, 46, '높은 온도·높은 압력', 23, fill=PLUS, weight=700)
    s += '<path d="M150 70 q6 -10 0 -18 M180 70 q6 -10 0 -18" fill="none" stroke="#D7263D" stroke-width="2.5" stroke-linecap="round" data-anim="fade" data-rep="alt" data-dur="1"/>'
    s += T(165, 302, '반응 탑 (모식도)', 23, fill=MUT)
    return f'<svg class="fig" viewBox="0 0 330 312" style="width:262px" aria-label="질소와 수소를 넣으면 철 촉매가 든 고온 고압 반응 탑에서 암모니아가 나오는 모식도">{s}</svg>'


def haber_particles():
    react = mols([('N2', 62, 60), ('H2', 168, 60), ('H2', 238, 60), ('H2', 308, 60)])
    prod = mols([('NH3', 130, 216), ('NH3', 250, 216)])
    s = static(react)
    s += plus(116, 60)
    s += '<g data-arw="185,96,185,164,ink,3"></g>'
    s += rearrange(react, prod, on='g:h2')
    s += plus(190, 214)
    s += T(185, 294, '원자 수: $\\mathrm{N}$ 2개, $\\mathrm{H}$ 6개 (반응 전 = 후)', 19, fill=MUT)
    return f'<svg class="fig" viewBox="0 0 370 306" style="width:366px" aria-label="질소 분자 1개와 수소 분자 3개가 반응해 암모니아 분자 2개가 되는 입자 모형">{s}</svg>'


# ───────── 단위체 → 사슬
def chain():
    s = ''
    n = 8
    xs = [60 + i * 62 for i in range(n)]
    y = 150
    s += '<path d="' + 'M' + ' L'.join(f'{x} {y + (12 if i % 2 else -12)}' for i, x in enumerate(xs)) + '" fill="none" stroke="#9AA5B1" stroke-width="6" stroke-linecap="round" data-anim="fade" data-dur=".5" data-delay="1.5"/>'
    rnd = [(-30, -90), (20, 70), (-40, 80), (30, -86), (-20, 92), (36, -70), (-26, 76), (24, -94)]
    for i, x in enumerate(xs):
        yy = y + (12 if i % 2 else -12)
        col, st = ('#CFE3F7', '#6E9CCB') if i % 2 == 0 else ('#FBDDBF', '#D08A47')
        dx, dy = rnd[i]
        s += f'<g data-anim="move" data-from="{dx},{dy}" data-dur="1.3" data-delay=".3" data-ease="soft"><circle cx="{x}" cy="{yy}" r="22" fill="{col}" stroke="{st}" stroke-width="2.5"/></g>'
    s += T(268, 52, '작은 분자(단위체) 여러 개가', 20, fill=MUT)
    s += T(268, 236, '→ 길게 이어진 사슬 모양 분자', 20, fill=INK, weight=700)
    s += '<circle cx="150" cy="276" r="11" fill="#CFE3F7" stroke="#6E9CCB" stroke-width="2"/>' + T(168, 283, '단위체 A', 19, anchor='start', fill=MUT)
    s += '<circle cx="310" cy="276" r="11" fill="#FBDDBF" stroke="#D08A47" stroke-width="2"/>' + T(328, 283, '단위체 B', 19, anchor='start', fill=MUT)
    return f'<svg class="fig" viewBox="0 0 536 296" style="width:500px" aria-label="두 종류의 작은 분자가 번갈아 이어져 긴 사슬 모양 분자가 되는 모식도">{s}</svg>'


# ───────── 용광로
def furnace():
    s = ''
    s += '<path d="M150 70 L120 330 Q120 372 160 372 H300 Q340 372 340 330 L310 70 Z" fill="#EEF2F6" stroke="#16233D" stroke-width="3" stroke-linejoin="round"/>'
    s += '<path d="M124 300 H336 L340 330 Q340 372 300 372 H160 Q120 372 120 330 Z" fill="#F29A4A" stroke="none"/>'
    s += '<path d="M126 276 H334 L337 300 H123 Z" fill="#B9A8A0"/>'
    s += '<path d="M150 70 L120 330 Q120 372 160 372 H300 Q340 372 340 330 L310 70 Z" fill="none" stroke="#16233D" stroke-width="3" stroke-linejoin="round"/>'
    # 장입물 알갱이
    for i, (x, y) in enumerate([(180, 110), (230, 100), (280, 115), (200, 150), (255, 145), (170, 195), (225, 190), (285, 200), (195, 240), (260, 238)]):
        c = '#A5452B' if i % 3 == 0 else ('#3A3F47' if i % 3 == 1 else '#D9D2C5')
        s += f'<circle cx="{x}" cy="{y}" r="10" fill="{c}" stroke="#16233D" stroke-width="1.2"/>'
    s += '<g data-arw="230,20,230,62,ink,3"></g>'
    s += T(250, 30, '철광석·코크스·석회석', 19, anchor='start')
    s += '<g data-arw="40,262,116,262,plus,3"></g><g data-arw="420,262,344,262,plus,3"></g>'
    s += T(60, 226, '뜨거운||공기', 19, fill=PLUS, anchor='middle')
    s += T(400, 226, '뜨거운||공기', 19, fill=PLUS, anchor='middle')
    s += T(230, 294, '슬래그', 19, fill=INK)
    s += T(230, 344, '쇳물(철)', 21, weight=700, fill='#16233D')
    s += '<path d="M340 352 H392 V384" fill="none" stroke="#F29A4A" stroke-width="10" stroke-linecap="round"/>'
    s += '<g data-anim="move" data-from="0,-26" data-rep="loop" data-dur="1.2" data-ease="in"><circle cx="392" cy="398" r="7" fill="#F29A4A"/></g>'
    s += '<g data-arw="320,96,392,70,muted,3"></g>' + T(396, 62, '기체', 19, anchor='start', fill=MUT)
    s += T(230, 404, '용광로 (모식도)', 19, fill=MUT)
    return f'<svg class="fig" viewBox="0 0 470 414" style="width:430px" aria-label="위에서 철광석과 코크스, 석회석을 넣고 아래에서 뜨거운 공기를 불어 넣어 바닥에 쇳물이 고이는 용광로 모식도">{s}</svg>'


def card_icons():
    # 시멘트·콘크리트(건물), 유리창, 플라스틱 관
    a = ('<svg viewBox="0 0 300 180" aria-label="철근 콘크리트 건물"><g data-anim="pop" data-o="150,150" data-dur=".8" data-delay=".3" data-ease="back">'
         '<rect x="70" y="30" width="160" height="120" fill="#D9DDE2" stroke="#16233D" stroke-width="2.5"/>'
         + ''.join(f'<rect x="{88 + c * 46}" y="{46 + r * 34}" width="28" height="20" fill="#BFE0F5" stroke="#16233D" stroke-width="1.5"/>' for r in range(3) for c in range(3))
         + '<path d="M70 150 H230" stroke="#16233D" stroke-width="3"/>'
         '<g stroke="#874A20" stroke-width="2.5" stroke-dasharray="6 5"><line x1="78" y1="34" x2="78" y2="146"/><line x1="222" y1="34" x2="222" y2="146"/></g></g>'
         + T(150, 168, '철근(점선)이 든 콘크리트', 19, fill=MUT) + '</svg>')
    b = ('<svg viewBox="0 0 300 180" aria-label="빛이 들어오는 유리창"><g data-anim="pop" data-o="150,90" data-dur=".8" data-delay=".5" data-ease="back">'
         '<rect x="80" y="20" width="140" height="130" fill="#E3F1FA" stroke="#16233D" stroke-width="3"/><line x1="150" y1="20" x2="150" y2="150" stroke="#16233D" stroke-width="3"/><line x1="80" y1="85" x2="220" y2="85" stroke="#16233D" stroke-width="3"/>'
         '<path d="M96 40 l26 -14 M170 46 l26 -14" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></g>'
         '<g data-arw="30,30,74,60,equi,3"></g>' + T(36, 22, '빛', 19, fill=EQUI, weight=700) + T(150, 168, '모래가 원료인 유리', 19, fill=MUT) + '</svg>')
    c = ('<svg viewBox="0 0 300 180" aria-label="플라스틱 수도관과 단열재"><g data-anim="pop" data-o="150,90" data-dur=".8" data-delay=".7" data-ease="back">'
         '<rect x="30" y="40" width="160" height="34" rx="6" fill="#CFE3F7" stroke="#16233D" stroke-width="2.5"/><ellipse cx="190" cy="57" rx="10" ry="17" fill="#FFFFFF" stroke="#16233D" stroke-width="2.5"/>'
         '<rect x="60" y="96" width="200" height="50" rx="4" fill="#FFFFFF" stroke="#16233D" stroke-width="2.5"/>'
         + ''.join(f'<circle cx="{78 + i * 22}" cy="{112 + (i % 2) * 18}" r="7" fill="none" stroke="#9FB0C2" stroke-width="1.8"/>' for i in range(9))
         + '</g>' + T(150, 168, '수도관·단열재', 19, fill=MUT) + '</svg>')
    return a, b, c


# ───────── 의약품 연표
def timeline():
    ev = [(80, '옛날', '버드나무 껍질||열·통증 완화'), (300, '1897', '아스피린 합성||(호프만)'), (520, '1928', '페니실린 발견||(플레밍)'),
          (750, '1940년대', '페니실린||대량 생산'), (990, '오늘날', '백신·||항바이러스제')]
    s = '<path d="M40 70 H1070" stroke="#5B6B7F" stroke-width="4" stroke-linecap="round" fill="none" data-anim="draw" data-dur="1.4" data-delay=".2"/>'
    for i, (x, y, t) in enumerate(ev):
        s += f'<g data-anim="pop" data-o="{x},70" data-dur=".6" data-delay="{.4 + i * .25:.2f}" data-ease="back"><circle cx="{x}" cy="70" r="13" fill="#FFFFFF" stroke="#2E9E6A" stroke-width="4"/></g>'
        s += T(x, 40, y, 21, weight=700, fill='#1B5E3F')
        s += T(x, 118, t, 20)
    return f'<svg class="fig" viewBox="0 0 1110 168" style="width:1110px" aria-label="의약품 연표: 버드나무 껍질, 1897 아스피린 합성, 1928 페니실린 발견, 1940년대 대량 생산, 오늘날 백신">{s}</svg>'


# ───────── 메테인 연소 입자
def combustion():
    react = mols([('CH4', 60, 60), ('O2', 182, 60), ('O2', 312, 60)])
    prod = mols([('CO2', 90, 186), ('H2O', 225, 178), ('H2O', 352, 178)])
    s = static(react) + plus(118, 60) + plus(247, 60)
    s += '<g data-arw="200,94,200,140,ink,3"></g>' + T(216, 124, '연소', 19, anchor='start', fill=MUT)
    s += rearrange(react, prod, delay=.6)
    s += plus(166, 168) + plus(288, 168)
    s += T(200, 246, '$\\mathrm{C}$ 1, $\\mathrm{H}$ 4, $\\mathrm{O}$ 4 (반응 전 = 후)', 19, fill=MUT)
    return f'<svg class="fig" viewBox="0 0 400 258" style="width:400px" aria-label="메테인 분자 1개와 산소 분자 2개가 반응해 이산화 탄소 분자 1개와 물 분자 2개가 되는 입자 모형">{s}</svg>'


# ───────── 환경 카드 그림 (문제 → 해결)
def env_icons():
    def pair(prob, sol, lab1, lab2, aria, d):
        return (f'<svg viewBox="0 0 300 156" aria-label="{aria}">{prob}<g data-arw="128,62,172,62,field,3"></g>'
                f'<g data-anim="pop" data-o="230,62" data-dur=".7" data-delay="{d}" data-ease="back">{sol}</g>'
                + T(70, 140, lab1, 19, fill=PLUS) + T(230, 140, lab2, 19, fill='#1B5E3F') + '</svg>')
    bottle = '<path d="M60 20 h20 v14 q14 8 14 24 v52 q0 8 -8 8 h-32 q-8 0 -8 -8 v-52 q0 -16 14 -24 Z" fill="#DDEEF8" stroke="#16233D" stroke-width="2.5" stroke-linejoin="round"/>'
    leaf = '<path d="M230 112 Q190 92 196 40 Q246 36 262 76 Q268 100 230 112 Z" fill="#9BD86F" stroke="#2E9E6A" stroke-width="2.5"/><path d="M230 112 Q222 76 208 52" fill="none" stroke="#2E9E6A" stroke-width="2"/>'
    a = pair(bottle, leaf, '썩지 않음', '미생물이 분해', '썩지 않는 플라스틱에서 미생물이 분해하는 생분해성 플라스틱으로', '.4')
    spray = '<rect x="48" y="40" width="40" height="72" rx="8" fill="#E9EEF3" stroke="#16233D" stroke-width="2.5"/><rect x="58" y="24" width="20" height="16" fill="#9FB0C2" stroke="#16233D" stroke-width="2"/><path d="M92 30 l14 -6 M92 36 l16 0 M92 42 l14 6" stroke="#9FB0C2" stroke-width="2.5" stroke-linecap="round"/>'
    earth = '<circle cx="230" cy="62" r="40" fill="#BFE0F5" stroke="#16233D" stroke-width="2.5"/><path d="M204 46 q14 -10 26 0 q10 10 0 20 q-16 6 -26 -6 Z M238 74 q12 -4 18 6 q-6 12 -20 6 Z" fill="#9BD86F" stroke="#2E9E6A" stroke-width="1.6"/><circle cx="230" cy="62" r="50" fill="none" stroke="#7FB3E0" stroke-width="4" stroke-dasharray="4 4"/>'
    b = pair(spray, earth, '프레온 가스', '오존층 보호', '프레온 가스 스프레이에서 대체 물질 사용으로 오존층을 보호', '.6')
    chim = '<rect x="50" y="56" width="40" height="64" fill="#D9DDE2" stroke="#16233D" stroke-width="2.5"/><path d="M60 52 q-10 -14 4 -22 q14 -8 10 -22 M80 52 q10 -12 0 -24" fill="none" stroke="#8C99A6" stroke-width="3" stroke-linecap="round"/>'
    tank = '<rect x="204" y="28" width="52" height="84" rx="14" fill="#E6F4EC" stroke="#16233D" stroke-width="2.5"/>' + T(230, 78, '$\\ce{CO2}$', 20, weight=700)
    c = pair(chim, tank, '$\\ce{CO2}$ 배출', '포집·활용', '공장 굴뚝의 이산화 탄소를 모아 저장하고 활용', '.8')
    return a, b, c


# ───────── 그래핀
def graphene():
    L = 64
    w3 = L * math.sqrt(3)
    pts = []
    for j in range(2):
        for i in range(3):
            cx = 92 + i * w3 + (j % 2) * w3 / 2
            cy = 94 + j * 1.5 * L
            for k in range(6):
                a = math.radians(30 + 60 * k)
                p = (round(cx + L * math.cos(a), 1), round(cy + L * math.sin(a), 1))
                if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 2 for q in pts):
                    pts.append(p)
    bonds = []
    for i, (x1, y1) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if j > i and abs(math.hypot(x1 - x2, y1 - y2) - L) < 1:
                bonds.append((x1, y1, x2, y2))
    s = '<g data-anim="fade" data-dur="1" data-delay=".2">' + ''.join(f'<line x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}" stroke="#9AA5B1" stroke-width="6" stroke-linecap="round"/>' for a, b, c, d in bonds) + '</g>'
    s += ''.join(A(x, y, 'C', '-') for x, y in pts)
    s += A(170, 306, 'C', '-') + T(202, 313, '탄소 원자', 20, anchor='start')
    return f'<svg class="fig" viewBox="0 0 456 334" style="width:440px" aria-label="탄소 원자가 육각형 그물 모양으로 연결된 그래핀 모형">{s}</svg>', len(pts)


def match():
    L = ['(가) 식량 부족', '(나) 튼튼한 건물', '(다) 질병 치료', '(라) 전기 저장']
    Rr = ['㉠ 아스피린 합성', '㉡ 리튬 이온 전지', '㉢ 암모니아 합성', '㉣ 철의 제련']
    ans = [2, 3, 0, 1]
    s = ''
    for i, t in enumerate(L):
        y = 40 + i * 70
        s += f'<rect x="10" y="{y - 24}" width="200" height="46" rx="10" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(110, y + 7, t, 20)
        s += f'<circle cx="214" cy="{y - 1}" r="5" fill="#16233D"/>'
    for i, t in enumerate(Rr):
        y = 40 + i * 70
        s += f'<rect x="350" y="{y - 24}" width="210" height="46" rx="10" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(455, y + 7, t, 20)
        s += f'<circle cx="346" cy="{y - 1}" r="5" fill="#16233D"/>'
    g = ''.join(f'<line x1="219" y1="{39 + i * 70}" x2="341" y2="{39 + j * 70}" stroke="#2E9E6A" stroke-width="3.5" stroke-linecap="round"/>' for i, j in enumerate(ans))
    s += f'<g class="step" data-g="m1" data-anim="draw" data-on="step" data-dur="1">{g}</g>'
    return f'<svg class="fig" viewBox="0 0 570 290" style="width:540px" aria-label="왼쪽 인류의 문제 네 가지와 오른쪽 화학의 기여 네 가지를 잇는 문제">{s}</svg>'


def main():
    tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
    gr, n = graphene()
    ci = card_icons(); ei = env_icons()
    F = {'cover': cover(), 'unitmap': unitmap(0), 'unit4': unit4(), 'life6': life6(), 'hub': hub(), 'air': air(),
         'reactor': reactor(), 'haber': haber_particles(), 'chain': chain(), 'furnace': furnace(),
         'card1': ci[0], 'card2': ci[1], 'card3': ci[2], 'timeline': timeline(), 'combust': combustion(),
         'env1': ei[0], 'env2': ei[1], 'env3': ei[2], 'graphene': gr, 'match': match()}
    def rep(m):
        k = m.group(1)
        return F.get(k, m.group(0))
    out = re.sub(r'\{\{(\w+)\}\}', rep, tpl)
    open(OUT, 'w', encoding='utf-8').write(out)
    print('written', OUT, len(out), 'graphene atoms', n)


if __name__ == '__main__':
    main()
