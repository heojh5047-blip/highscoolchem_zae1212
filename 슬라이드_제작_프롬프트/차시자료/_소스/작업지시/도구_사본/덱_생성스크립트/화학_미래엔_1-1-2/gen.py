# 1-1-2 덱 그림 생성: slides.tpl.html 의 {{이름}} 자리에 SVG 조각을 넣어 slides.html 을 만든다.
import math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/1-1-2_몰과_물질의_양/slides.html'
R = {'H': 18, 'C': 24, 'N': 24, 'O': 24, 'He': 20, 'Mg': 29, 'Cu': 28}
INK, MUT, FIELD, EQUI, PLUS, MINUS = '#16233D', '#5B6B7F', '#2E9E6A', '#E08A2C', '#D7263D', '#1F6FD1'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def A(x, y, el, s=1.0, lab=None, r=None):
    rr = r if r else R[el] * s
    if lab is None:
        lab = '' if rr >= 18 else '-'
    return f'<g data-atom="{f(x)},{f(y)},{f(rr)},{el}{("," + lab) if lab else ""}"></g>'


def T(x, y, s, size=20, anchor='middle', fill=None, weight=None, halo=False, tex=False, extra=''):
    if '<b>' in s:
        s = s.replace('<b>', '').replace('</b>', ''); weight = weight or 700
    a = f'data-tex="{s}"' if tex else f'data-mix="{s}"'
    return (f'<text class="tex" x="{f(x)}" y="{f(y)}" {a} data-size="{size}" data-anchor="{anchor}"'
            + (f' fill="{fill}"' if fill else '') + (f' data-weight="{weight}"' if weight else '')
            + (' data-halo="1"' if halo else '') + (f' {extra}' if extra else '') + '></text>')


def mol(kind, x, y, s=1.0, rot=0.0, lab=None):
    """분자 원자 목록 [(원소,x,y)] — 뒤 → 앞 순서"""
    def P(d, ang):
        a = math.radians(ang + rot)
        return x + d * s * math.cos(a), y + d * s * math.sin(a)
    out = []
    if kind in ('H2', 'O2', 'N2'):
        e = kind[0]
        d = 0.78 * 2 * R[e] / 2
        for ang in (180, 0):
            out.append((e,) + P(d, ang))
    elif kind == 'H2O':
        d = 0.78 * (24 + 18)
        out += [('H',) + P(d, 90 + 52.25), ('H',) + P(d, 90 - 52.25), ('O', x, y)]
    elif kind == 'CO2':
        d = 0.78 * 48
        out += [('O',) + P(d, 180), ('O',) + P(d, 0), ('C', x, y)]
    elif kind == 'CH4':
        d = 0.78 * 42
        out += [('H',) + P(d, a) for a in (45, 135, 225, 315)] + [('C', x, y)]
    elif kind == 'NH3':
        d = 0.78 * 42
        out += [('H',) + P(d, a) for a in (90, 210, 330)] + [('N', x, y)]
    elif kind == 'He':
        out.append(('He', x, y))
    elif kind == 'C':
        out.append(('C', x, y))
    return ''.join(A(px, py, e, s, lab) for e, px, py in out)


def balance(cx, by, w=260, reading='0.00 g', pan=True):
    """전자저울: 가운데 cx, 본체 위 by"""
    x0 = cx - w / 2
    s = (f'<rect x="{f(x0)}" y="{f(by)}" width="{w}" height="58" rx="12" fill="#E9EEF3" stroke="{INK}" stroke-width="2.5"/>'
         f'<rect x="{f(cx-64)}" y="{f(by+12)}" width="128" height="34" rx="6" fill="#1F2A3C"/>'
         + T(cx, by + 37, reading, 22, fill='#9FF0C0', weight=700))
    if pan:
        s += f'<rect x="{f(cx-w*0.38)}" y="{f(by-12)}" width="{f(w*0.76)}" height="12" rx="4" fill="#C9D3DD" stroke="{INK}" stroke-width="2"/>'
    return s


figs = {}

# ── S1 표지 ──
mz = ''.join(f'<g data-anim="move" data-from="{dx},{dy}" data-rep="alt" data-dur="2.4" data-ease="sine">{mol("H2O", x, y, 0.8, r)}</g>'
             for x, y, r, dx, dy in [(222, 98, 0, 8, -6), (316, 84, 30, -7, 6), (240, 180, -20, 6, 7), (322, 172, 10, -8, -5)])
figs['cover'] = (
    '<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="전자저울 위 물 18 g과 그 속 물 분자를 확대한 그림">'
    '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
    + balance(270, 372, 300, '18.00 g') +
    f'<rect x="214" y="302" width="112" height="52" fill="#DDEEF8"/><line x1="214" y1="302" x2="326" y2="302" stroke="#9FC3DD" stroke-width="2"/>'
    f'<path d="M212 272 V356 H328 V272" fill="none" stroke="#7E8B98" stroke-width="3"/>'
    f'<line x1="270" y1="242" x2="270" y2="298" stroke="{MUT}" stroke-width="2" stroke-dasharray="6 5"/>'
    f'<g data-anim="pop" data-o="270,132" data-dur=".9" data-ease="back"><circle cx="270" cy="132" r="108" fill="#FFFFFF" stroke="{MUT}" stroke-width="2.5"/>{mz}</g>'
    + T(270, 464, '물 18 g = 물 1 몰', 26, weight=700) + T(270, 496, '= 물 분자 $6.02\\times10^{23}$개', 22) +
    '</svg>')

# ── S3 생각 열기 (사탕 가게) ──
def lolli(x, y, c):
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+70}" stroke="#C9B48A" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y}" r="26" fill="{c}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M{x-14} {y} a14 14 0 0 1 28 0" fill="none" stroke="#FFFFFF" stroke-width="3"/>')
jel = ''.join(f'<rect x="{f(x)}" y="{f(y)}" width="22" height="16" rx="7" fill="{c}" stroke="{INK}" stroke-width="1.6"/>'
              for x, y, c in [(700, 132, '#F4A7B4'), (724, 134, '#9ED7C3'), (748, 132, '#F2C230'), (772, 134, '#F4A7B4'),
                              (712, 118, '#F2C230'), (736, 118, '#F4A7B4'), (760, 118, '#9ED7C3'), (724, 104, '#9ED7C3'), (748, 104, '#F2C230')])
figs['s3'] = (
    '<svg class="fig" viewBox="0 0 1112 250" style="width:1060px" aria-label="막대 사탕은 개수로, 젤리는 무게를 달아 파는 사탕 가게">'
    '<rect x="10" y="10" width="520" height="230" rx="16" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="2"/>'
    + lolli(110, 80, '#F4A7B4') + lolli(190, 80, '#9ED7C3') + lolli(270, 80, '#F2C230') +
    f'<rect x="330" y="62" width="170" height="50" rx="10" fill="#FFF8D6" stroke="{EQUI}" stroke-width="2"/>'
    + T(415, 95, '1개 500원', 22, weight=700) + T(190, 212, '큰 사탕 → <b>개수</b>로 판다', 22) +
    '<rect x="582" y="10" width="520" height="230" rx="16" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="2"/>'
    + jel + balance(740, 150, 240, '100 g') +
    f'<rect x="900" y="62" width="180" height="50" rx="10" fill="#FFF8D6" stroke="{EQUI}" stroke-width="2"/>'
    + T(990, 95, '100 g 2000원', 22, weight=700) + T(842, 232, '작은 젤리 → <b>무게</b>를 달아 판다', 22) +
    '</svg>')

# ── S4 묶음 단위 ──
egg = ''.join(f'<ellipse cx="{60+c*34}" cy="{58+r*30}" rx="13" ry="12" fill="#F7E7C6" stroke="#B9873A" stroke-width="1.6"/>' for r in range(5) for c in range(6))
pen = ''.join(f'<g transform="rotate(-8 {400+i*14} 110)"><rect x="{394+i*14}" y="44" width="10" height="120" rx="2" fill="{["#F2C230","#9ED7C3"][i%2]}" stroke="{INK}" stroke-width="1.4"/><path d="M{394+i*14} 164 l5 14 l5 -14 z" fill="#E8C9A0" stroke="{INK}" stroke-width="1.2"/></g>' for i in range(12))
dots = ''.join(f'<circle cx="{f(820+math.cos(i*2.4)*(8+i*1.3))}" cy="{f(108+math.sin(i*2.4)*(8+i*1.3))}" r="3" fill="{INK}"/>' for i in range(46))
figs['s4'] = (
    '<svg class="fig" viewBox="0 0 1112 236" style="width:1040px" aria-label="달걀 한 판 30개, 연필 한 다스 12자루, 원자의 묶음은?">'
    '<g data-anim="pop" data-o="130,110" data-dur=".7" data-ease="back"><rect x="30" y="30" width="230" height="170" rx="14" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="2"/>' + egg + '</g>'
    + T(145, 228, '달걀 <b>한 판</b> = 30개', 22) +
    '<g data-anim="pop" data-o="470,110" data-dur=".7" data-delay=".25" data-ease="back"><rect x="360" y="30" width="230" height="170" rx="14" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="2"/>' + pen + '</g>'
    + T(475, 228, '연필 <b>한 다스</b> = 12자루', 22) +
    '<g data-anim="pop" data-o="820,110" data-dur=".7" data-delay=".5" data-ease="back"><rect x="690" y="30" width="260" height="170" rx="14" fill="#FFFFFF" stroke="#C9D3DD" stroke-width="2" stroke-dasharray="8 6"/>' + dots + '</g>'
    + T(820, 228, '원자·분자의 묶음은?', 22, weight=700) + T(1010, 118, '?', 56, fill=EQUI, weight=700) +
    '</svg>')

# ── S5 몰 정의 그림 ──
pts = [(70 + (i % 9) * 20 + (10 if (i // 9) % 2 else 0), 50 + (i // 9) * 19) for i in range(54)]
d5 = ''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="#3A3F47" stroke="#1C1F24" stroke-width="1.2"/>' for x, y in pts)
figs['s5'] = (
    '<svg class="fig" viewBox="0 0 560 250" style="width:540px" aria-label="원자 6.02 곱하기 10의 23제곱 개를 묶으면 원자 1 몰">'
    f'<rect x="40" y="24" width="230" height="150" rx="14" fill="#F4F8FC" stroke="#C9D3DD" stroke-width="2"/>{d5}'
    + T(155, 214, '원자 $6.02\\times10^{23}$개', 22, weight=700) +
    '<g data-arw="290,100,350,100,ink,3"></g>' +
    f'<g data-anim="fade" data-dur="1" data-delay=".6"><rect x="372" y="24" width="160" height="150" rx="14" fill="#FFF8D6" stroke="{EQUI}" stroke-width="3"/>'
    + T(452, 112, '1 몰', 40, weight=700) + '</g>'
    + T(452, 214, '원자 <b>1 몰</b>', 22, weight=700) +
    '</svg>')

# ── S6 초콜릿 탑 ──
coins = ''.join(f'<g data-anim="move" data-from="0,-{40+i*10}" data-dur=".5" data-delay="{f(0.1+(9-i)*0.08)}" data-ease="out"><ellipse cx="120" cy="{f(232-i*16)}" rx="62" ry="13" fill="#8A5A3B" stroke="#4E2F1C" stroke-width="2"/><ellipse cx="120" cy="{f(228-i*16)}" rx="62" ry="13" fill="#B07A52" stroke="#4E2F1C" stroke-width="2"/></g>' for i in range(10))
figs['s6'] = (
    '<svg class="fig" viewBox="0 0 300 280" style="width:280px" aria-label="동전 모양 초콜릿 10개를 쌓은 탑과 높이 치수선">'
    + coins +
    f'<line x1="200" y1="243" x2="200" y2="77" stroke="{MUT}" stroke-width="2"/><line x1="192" y1="243" x2="208" y2="243" stroke="{MUT}" stroke-width="2"/><line x1="192" y1="77" x2="208" y2="77" stroke="{MUT}" stroke-width="2"/>'
    + T(214, 166, '10개', 21, anchor='start', weight=700) + T(214, 192, '높이 ?', 20, anchor='start', fill=MUT) +
    '<line x1="40" y1="250" x2="200" y2="250" stroke="#C9D3DD" stroke-width="2"/>'
    + T(120, 274, '동전 모양 초콜릿', 20) +
    '</svg>')

# ── S7 몰과 입자 수 ──
cbox = ''.join(A(x, y, 'C') for x, y in [(80, 70), (140, 70), (200, 70), (110, 124), (170, 124), (230, 124)])
hbox = ''.join(f'<g data-anim="move" data-from="{dx},{dy}" data-rep="alt" data-dur="2.2" data-ease="sine">{mol("H2", x, y, 1, r)}</g>'
               for x, y, r, dx, dy in [(420, 72, 0, 6, 5), (520, 68, 30, -6, 6), (440, 130, -25, 5, -6), (540, 128, 10, -5, -5)])
figs['s7'] = (
    '<svg class="fig" viewBox="0 0 620 200" style="width:600px" aria-label="탄소 1 몰은 탄소 원자, 수소 1 몰은 수소 분자 6.02 곱하기 10의 23제곱 개">'
    '<rect x="40" y="30" width="230" height="130" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>' + cbox +
    '<rect x="360" y="30" width="230" height="130" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>' + hbox +
    T(155, 190, '탄소 $\\ce{C}$ <b>1 몰</b>', 22) + T(475, 190, '수소 $\\ce{H2}$ <b>1 몰</b>', 22) +
    '</svg>')

# ── S9 나사못 ──
def screw(x, y, a=0):
    return (f'<g transform="rotate({a} {x} {y})"><rect x="{x-3}" y="{y-14}" width="6" height="28" rx="1" fill="#AEB7C2" stroke="{INK}" stroke-width="1.2"/>'
            f'<rect x="{x-8}" y="{y-18}" width="16" height="5" rx="2" fill="#AEB7C2" stroke="{INK}" stroke-width="1.2"/></g>')
sc1 = ''.join(screw(150 + (i % 6) * 18 - 45, 104 - (i // 6) * 16, (i * 37) % 60 - 30) for i in range(18))
figs['s9'] = (
    '<svg class="fig" viewBox="0 0 560 230" style="width:540px" aria-label="나사못 100개는 50 g, 나사못 500 g은 몇 개일까">'
    f'<g data-anim="pop" data-o="150,100" data-dur=".7" data-ease="back">{sc1}</g>' + balance(150, 140, 230, '50.00 g') +
    T(150, 222, '나사못 <b>100개</b>', 21) +
    f'<rect x="340" y="40" width="180" height="96" rx="8" fill="#E8C9A0" stroke="{INK}" stroke-width="2.5"/><line x1="340" y1="68" x2="520" y2="68" stroke="{INK}" stroke-width="2"/>'
    + T(430, 112, '?개', 30, weight=700) + balance(430, 140, 230, '500.00 g') +
    T(430, 222, '나사못 한 상자', 21) +
    '</svg>')

# ── S10 C 1몰 vs Mg 1몰 접시 ──
def dish(cx, by, w=200):
    return f'<ellipse cx="{cx}" cy="{by}" rx="{w/2}" ry="16" fill="#F4F8FC" stroke="#7E8B98" stroke-width="2.5"/>'
figs['s10'] = (
    '<svg class="fig" viewBox="0 0 500 270" style="width:480px" aria-label="탄소 1 몰 12 g과 마그네슘 1 몰 24.3 g — 원자 수는 같고 질량은 다르다">'
    + dish(120, 150) + '<path d="M70 150 Q120 98 170 150 Z" fill="#3A3F47" stroke="#1C1F24" stroke-width="2"/>' +
    dish(380, 150) + ''.join(f'<path d="M{316+i*14} 152 q10 -{38+(i%3)*8} 22 -{12+(i%2)*6}" fill="none" stroke="#9AA5B1" stroke-width="5" stroke-linecap="round"/>' for i in range(8)) +
    T(120, 200, '탄소 $\\ce{C}$ 1 몰', 22, weight=700) + T(120, 230, '12 g', 22) +
    T(380, 200, '마그네슘 $\\ce{Mg}$ 1 몰', 22, weight=700) + T(380, 230, '24.3 g', 22) +
    T(250, 40, '원자 수는 둘 다 $6.02\\times10^{23}$개', 21, fill=MUT) +
    '</svg>')

# ── S11 분자 몰질량 그림 ──
figs['s11a'] = ('<svg class="fig" viewBox="0 0 190 110" style="width:190px" aria-label="물 분자 모형">'
                f'<g data-anim="move" data-from="0,-14" data-dur="1" data-ease="out">{mol("H2O", 95, 42)}</g>' + '</svg>')
figs['s11b'] = ('<svg class="fig" viewBox="0 0 190 110" style="width:190px" aria-label="이산화 탄소 분자 모형">'
                f'<g data-anim="move" data-from="0,-14" data-dur="1" data-delay=".3" data-ease="out">{mol("CO2", 95, 55)}</g>' + '</svg>')

# ── S12 여러 가지 물질 1몰 ──
def beaker(x, y, w, h, fill_h, fill, powder=False):
    s = f'<path d="M{x} {y} V{y+h} H{x+w} V{y}" fill="none" stroke="#7E8B98" stroke-width="2.5"/>'
    if powder:
        s = f'<path d="M{x+3} {y+h-2} Q{x+w/2} {y+h-fill_h*1.6} {x+w-3} {y+h-2} Z" fill="{fill}" stroke="#9AA5B1" stroke-width="1.5"/>' + s
    else:
        s = f'<rect x="{x+2}" y="{y+h-fill_h}" width="{w-4}" height="{fill_h-2}" fill="{fill}"/>' + s
    return s
it = [
    ('cube', 20, '이산화 탄소', '\\ce{CO2}', 44),
    ('cyl', 300, '에탄올', '\\ce{C2H5OH}', 46),
    ('pow1', 450, '포도당', '\\ce{C6H12O6}', 180),
    ('pow2', 640, '설탕', '\\ce{C12H22O11}', 342),
    ('heap', 830, '탄산수소 나트륨', '\\ce{NaHCO3}', 84),
    ('wat', 990, '물', '\\ce{H2O}', 18),
]
p12 = ''
for i, (k, x, nm, fm, mm) in enumerate(it):
    d = f'{0.15*i:.2f}'
    if k == 'cube':
        g = (f'<rect x="{x}" y="34" width="230" height="200" fill="#FFF8D6" fill-opacity=".7" stroke="#B9A24A" stroke-width="2"/>'
             f'<path d="M{x} 34 l40 -26 h230 l-40 26 z M{x+230} 34 l40 -26 v200 l-40 26 z" fill="#FFF3B8" fill-opacity=".7" stroke="#B9A24A" stroke-width="2"/>'
             + T(x + 115, 140, '기체', 21, fill=MUT) +
             f'<line x1="{x}" y1="246" x2="{x+230}" y2="246" stroke="{MUT}" stroke-width="1.8"/>' + T(x + 115, 266, '28.2 cm', 19, fill=MUT, halo=True))
        cx = x + 125
    elif k == 'cyl':
        g = beaker(x + 30, 110, 44, 124, 60, '#EEF6FB') + ''.join(f'<line x1="{x+30}" y1="{130+j*20}" x2="{x+40}" y2="{130+j*20}" stroke="{MUT}" stroke-width="1.5"/>' for j in range(5))
        cx = x + 52
    elif k == 'pow1':
        g = beaker(x + 20, 170, 110, 64, 26, '#FFFFFF', True); cx = x + 75
    elif k == 'pow2':
        g = beaker(x + 10, 140, 140, 94, 46, '#FFFFFF', True); cx = x + 80
    elif k == 'heap':
        g = f'<ellipse cx="{x+60}" cy="230" rx="60" ry="9" fill="#F4F8FC" stroke="#7E8B98" stroke-width="2"/><path d="M{x+22} 230 Q{x+60} 190 {x+98} 230 Z" fill="#FFFFFF" stroke="#9AA5B1" stroke-width="1.5"/>'; cx = x + 60
    else:
        g = beaker(x + 30, 196, 40, 38, 24, '#DDEEF8'); cx = x + 50
    p12 += f'<g data-anim="pop" data-o="{cx},230" data-dur=".6" data-delay="{d}" data-ease="back">{g}</g>'
    p12 += T(cx, 296 if k != 'cube' else 296, nm, 20, weight=700) + T(cx, 322, f'${fm}$', 20) + T(cx, 348, f'{mm} g/mol', 20, fill=MUT)
figs['s12'] = ('<svg class="fig" viewBox="0 0 1112 360" style="width:1080px" aria-label="이산화 탄소, 에탄올, 포도당, 설탕, 탄산수소 나트륨, 물 각 1 몰의 양과 몰질량">' + p12 + '</svg>')

# ── S13 NaCl 격자 ──
lat = ''
for r_ in range(2):
    for c in range(4):
        x, y = 70 + c * 56, 70 + r_ * 56
        na = (r_ + c) % 2 == 0
        lat += f'<g data-atom="{x},{y},{19 if na else 32},{"Na" if na else "Cl"},-"></g>'
figs['s13'] = ('<svg class="fig" viewBox="0 0 360 230" style="width:340px" aria-label="나트륨 이온과 염화 이온이 1 대 1로 번갈아 배열된 염화 나트륨 모형">'
               f'<g data-anim="fade" data-dur="1">{lat}</g>'
               '<g data-atom="60,186,19,Na,-"></g>' + T(88, 194, '$\\ce{Na+}$', 21, anchor='start') +
               '<g data-atom="200,186,24,Cl,-"></g>' + T(232, 194, '$\\ce{Cl-}$', 21, anchor='start') +
               '</svg>')

# ── 사다리 (S14, S19) ──
def ladder(left, mid, right, l_top, l_bot, r_top, r_bot, aria):
    s = f'<svg class="fig" viewBox="0 0 1040 190" style="width:1000px" aria-label="{aria}">'
    for x, lab, hl in [(20, left, False), (400, mid, True), (780, right, False)]:
        s += f'<rect x="{x}" y="62" width="240" height="70" rx="14" fill="{"#FFF3A8" if hl else "#FFFFFF"}" stroke="{EQUI if hl else "#9FB0C2"}" stroke-width="{3 if hl else 2}"/>' + T(x + 120, 106, lab, 25, weight=700)
    s += ('<g data-arw="268,82,392,82,ink,3"></g><g data-arw="392,112,268,112,ink,3"></g>'
          '<g data-arw="648,82,772,82,ink,3"></g><g data-arw="772,112,648,112,ink,3"></g>')
    s += T(330, 48, l_top, 21) + T(330, 160, l_bot, 21) + T(710, 48, r_top, 21) + T(710, 160, r_bot, 21)
    return s + '</svg>'
figs['s14'] = ladder('질량(g)', '몰(mol)', '입자 수(개)', '$\\div$ 몰질량(g/mol)', '$\\times$ 몰질량(g/mol)', '$\\times6.02\\times10^{23}$ 개/mol', '$\\div6.02\\times10^{23}$ 개/mol', '질량을 몰질량으로 나누면 몰, 몰에 아보가드로수를 곱하면 입자 수')
figs['s19'] = ladder('기체의 부피(L)', '몰(mol)', '입자 수(개)', '$\\div22.4$ L/mol', '$\\times22.4$ L/mol', '$\\times6.02\\times10^{23}$ 개/mol', '$\\div6.02\\times10^{23}$ 개/mol', '0 °C 1 기압에서 기체 부피를 22.4 L/mol로 나누면 몰')

# ── S18 기체 상자 3개 ──
def gasbox(x, kind, name, delay):
    s = f'<rect x="{x}" y="20" width="300" height="200" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2.5"/>'
    pos = [(x + 62, 62, 10), (x + 232, 58, -12), (x + 150, 118, 8), (x + 70, 178, -8), (x + 236, 178, 14)]
    for j, (px, py, r) in enumerate(pos):
        dx, dy = [(8, 6), (-7, 8), (9, -5), (-8, -6), (6, -8)][j]
        s += f'<g data-anim="move" data-from="{dx},{dy}" data-rep="alt" data-dur="{1.8+j*0.2:.1f}" data-ease="sine">{mol(kind, px, py, 0.75, r)}</g>'
    s += T(x + 150, 252, name, 22, weight=700) + T(x + 150, 280, '1 몰 · 22.4 L · $6.02\\times10^{23}$개', 20, fill=MUT)
    return s
figs['s18'] = ('<svg class="fig" viewBox="0 0 1040 290" style="width:980px" aria-label="0 °C 1 기압에서 산소, 헬륨, 이산화 탄소 1 몰은 모두 22.4 L">'
               + gasbox(20, 'O2', '산소 $\\ce{O2}$', 0) + gasbox(370, 'He', '헬륨 $\\ce{He}$', 0) + gasbox(720, 'CO2', '이산화 탄소 $\\ce{CO2}$', 0)
               + T(905, 44, '$\\ce{O}$', 19, fill=MUT) + '</svg>')
figs['s18'] = figs['s18'].replace(T(905, 44, '$\\ce{O}$', 19, fill=MUT), '')

# ── S20 물 컵 vs 상자 ──
figs['s20'] = ('<svg class="fig" viewBox="0 0 470 280" style="width:440px" aria-label="물 1 몰 18 mL와 기체 1 몰 22.4 L 비교">'
               f'<g data-anim="pop" data-o="80,230" data-dur=".6" data-ease="back">' + beaker(60, 196, 40, 38, 24, '#DDEEF8') + '</g>'
               + T(80, 262, '물 1 몰 약 18 mL', 20, weight=700) +
               f'<g data-anim="pop" data-o="320,230" data-dur=".7" data-delay=".3" data-ease="back"><rect x="210" y="40" width="200" height="190" fill="#FFF8D6" fill-opacity=".7" stroke="#B9A24A" stroke-width="2"/>'
               f'<path d="M210 40 l34 -22 h200 l-34 22 z M410 40 l34 -22 v190 l-34 22 z" fill="#FFF3B8" fill-opacity=".7" stroke="#B9A24A" stroke-width="2"/></g>'
               + T(310, 262, '기체 1 몰 22.4 L', 20, weight=700) + '</svg>')

# ── S22 몰 지도 ──
hub = '<svg class="fig" viewBox="0 0 1040 330" style="width:980px" aria-label="몰을 가운데에 두고 입자 수, 질량, 기체의 부피로 바꾸는 지도">'
hub += (f'<rect x="20" y="40" width="220" height="74" rx="14" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(130, 86, '입자 수(개)', 24, weight=700) +
        f'<rect x="800" y="40" width="220" height="74" rx="14" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(910, 86, '질량(g)', 24, weight=700) +
        f'<rect x="410" y="236" width="220" height="74" rx="14" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(520, 274, '기체의 부피(L)', 24, weight=700) + T(520, 300, '0 °C, 1 기압', 18, fill=MUT) +
        f'<g data-anim="pop" data-o="520,77" data-dur=".8" data-ease="back"><rect x="410" y="40" width="220" height="74" rx="14" fill="#FFF3A8" stroke="{EQUI}" stroke-width="3"/>' + T(520, 88, '몰(mol)', 28, weight=700) + '</g>')
hub += ('<g class="step" data-g="h1"><g data-arw="402,64,248,64,ink,3"></g><g data-arw="248,92,402,92,ink,3"></g>' + T(325, 50, '$\\times6.02\\times10^{23}$', 20) + T(325, 128, '$\\div6.02\\times10^{23}$', 20) + '</g>'
        '<g class="step" data-g="h2"><g data-arw="638,64,792,64,ink,3"></g><g data-arw="792,92,638,92,ink,3"></g>' + T(715, 50, '$\\times$ 몰질량', 20) + T(715, 128, '$\\div$ 몰질량', 20) + '</g>'
        '<g class="step" data-g="h3"><g data-arw="500,122,500,228,ink,3"></g><g data-arw="540,228,540,122,ink,3"></g>' + T(490, 182, '$\\times22.4$ L/mol', 20, anchor='end') + T(550, 182, '$\\div22.4$ L/mol', 20, anchor='start') + '</g>')
figs['s22'] = hub + '</svg>'

# ── S25 탐구 과정 카드 그림 ──
figs['s25a'] = ('<svg class="fig" viewBox="0 0 220 110" style="width:200px" aria-hidden="true">'
                + ''.join(f'<rect x="{20+c*46}" y="{14+r_*46}" width="40" height="40" rx="5" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(40 + c * 46, 42 + r_ * 46, ['$\\ce{H}$', '$\\ce{C}$', '$\\ce{O}$', '$\\ce{Na}$', '$\\ce{Cl}$', '$\\ce{Cu}$', '?', '?'][r_ * 4 + c], 19) for r_ in range(2) for c in range(4)) + '</svg>')
figs['s25b'] = ('<svg class="fig" viewBox="0 0 220 110" style="width:200px" aria-hidden="true">'
                + T(110, 50, '$0.1\\ \\text{mol}\\times180\\ \\text{g/mol}$', 20) + T(110, 88, '$=18\\ \\text{g}$', 24, weight=700) + '</svg>')
figs['s25c'] = ('<svg class="fig" viewBox="0 0 220 110" style="width:200px" aria-hidden="true">'
                + '<ellipse cx="110" cy="44" rx="56" ry="8" fill="#F4F8FC" stroke="#7E8B98" stroke-width="2"/><path d="M76 44 Q110 14 144 44 Z" fill="#FFFFFF" stroke="#9AA5B1" stroke-width="1.5"/>' + balance(110, 52, 200, '18.00 g') + '</svg>')

# ── S31 연표 ──
tl = '<svg class="fig" viewBox="0 0 1040 200" style="width:1000px" aria-label="아보가드로수 정의의 변화 연표">'
tl += f'<g data-anim="draw" data-dur="1.4"><line x1="40" y1="70" x2="1000" y2="70" stroke="{MUT}" stroke-width="3"/></g>'
for i, (x, yr, t1, t2) in enumerate([(120, '1960년대', '탄소-12 12 g 속', '원자 수로 정의'), (400, '문제점', '킬로그램 원기 질량이', '미세하게 줄어듦'), (680, '국제 공동 연구', '규소 구로', '원자 수 측정'), (930, '2019년', '$6.02214076\\times10^{23}$', '정해진 상수')]):
    tl += f'<g data-anim="pop" data-o="{x},70" data-dur=".5" data-delay="{0.3+i*0.3:.1f}" data-ease="back"><circle cx="{x}" cy="70" r="11" fill="{EQUI if i == 3 else "#FFFFFF"}" stroke="{INK}" stroke-width="2.5"/></g>'
    tl += T(x, 44, yr, 21, weight=700) + T(x, 116, t1, 20) + T(x, 144, t2, 20)
figs['s31'] = tl + '</svg>'

# ── S38 문항 10 ──
def qbox(x, kind, name):
    s = f'<rect x="{x}" y="14" width="200" height="160" rx="12" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2.5"/>'
    for j, (px, py, r) in enumerate([(x + 55, 55, 0), (x + 145, 60, 40), (x + 65, 130, -30), (x + 150, 135, 15)]):
        dx, dy = [(6, 5), (-6, 6), (6, -5), (-5, -6)][j]
        s += f'<g data-anim="move" data-from="{dx},{dy}" data-rep="alt" data-dur="{1.8+j*0.2:.1f}" data-ease="sine">{mol(kind, px, py, 0.75, r)}</g>'
    return s + T(x + 100, 204, name, 21, weight=700)
figs['s38'] = ('<svg class="fig" viewBox="0 0 470 220" style="width:450px" aria-label="같은 온도와 압력에서 같은 부피의 수소 기체와 산소 기체, 각 분자 4개">'
               + qbox(20, 'H2', '수소 기체') + qbox(250, 'O2', '산소 기체') + '</svg>')

# ── S36 없음, S33 등 그림 없음 ──
# ── S16, S15 사다리 작게 ──
figs['s15'] = ('<svg class="fig" viewBox="0 0 470 110" style="width:440px" aria-hidden="true">'
               '<rect x="10" y="30" width="120" height="54" rx="10" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(70, 64, '23 g', 22, weight=700) +
               '<g data-arw="136,57,186,57,ink,3"></g>' + T(161, 22, '$\\div46$', 19) +
               '<rect x="192" y="30" width="110" height="54" rx="10" fill="#FFF3A8" stroke="#E08A2C" stroke-width="2.5"/>' + T(247, 64, '0.5 mol', 22, weight=700) +
               '<g data-arw="308,57,348,57,ink,3"></g>' + T(328, 22, '$\\times N$', 19) +
               '<rect x="354" y="30" width="106" height="54" rx="10" fill="#FFFFFF" stroke="#9FB0C2" stroke-width="2"/>' + T(407, 64, '분자 수', 21, weight=700) + '</svg>')


# ── 확인하기 그림 (S8, S17, S23) ──
def okfig(kind, cap1, cap2, aria):
    return (f'<svg class="fig" viewBox="0 0 520 170" style="width:520px" aria-label="{aria}">'
            f'<rect x="10" y="10" width="500" height="150" rx="16" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>'
            f'<g data-anim="pop" data-o="130,85" data-dur=".7" data-ease="back">{mol(kind, 130, 85, 1.2)}</g>'
            + T(360, 76, cap1, 22, weight=700) + T(360, 112, cap2, 21, fill=MUT) + '</svg>')
figs['s8'] = okfig('CO2', '$\\ce{CO2}$ 분자 1개', '산소 원자 2개', '이산화 탄소 분자 1개에 산소 원자 2개')
figs['s17'] = okfig('CH4', '$\\ce{CH4}$ 분자 1개', '수소 원자 4개 (모양은 Ⅱ 단원에서)', '메테인 분자 1개에 수소 원자 4개')
figs['s23'] = ('<svg class="fig" viewBox="0 0 520 190" style="width:520px" aria-label="22.4 L 상자의 절반인 11.2 L는 기체 0.5 몰">'
               '<rect x="40" y="40" width="140" height="130" fill="#FFF8D6" fill-opacity=".7" stroke="#B9A24A" stroke-width="2"/>'
               '<path d="M40 40 l26 -18 h140 l-26 18 z M180 40 l26 -18 v130 l-26 18 z" fill="#FFF3B8" fill-opacity=".7" stroke="#B9A24A" stroke-width="2"/>'
               '<line x1="40" y1="105" x2="180" y2="105" stroke="#B9A24A" stroke-width="2" stroke-dasharray="6 5"/>'
               f'<g data-anim="scale" data-from="1,0" data-o="110,170" data-dur="1" data-ease="out"><rect x="42" y="106" width="136" height="62" fill="#F2C230" fill-opacity=".45"/></g>'
               + T(330, 80, '22.4 L = 1 몰', 22, weight=700) + T(330, 120, '11.2 L = 0.5 몰', 22, weight=700, fill='#8A6D00') + T(330, 156, '(0 °C, 1 기압)', 20, fill=MUT) + '</svg>')

tpl = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
out = re.sub(r'\{\{(\w+)\}\}', lambda m: figs[m.group(1)], tpl)
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', len(out))
