# 1-2-2 덱 그림 생성: slides.tpl.html 의 {{이름}} 자리에 SVG 조각을 넣어 slides.html 을 만든다.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/highscoolchem_zae1212/슬라이드_제작_프롬프트/차시자료/_소스/content/화학_미래엔/1-2-2_화학_반응의_양적_관계/slides.html'
R = {'H': 18, 'O': 24, 'N': 24, 'C': 24, 'Mg': 29}
INK, MUT, FIELD, EQUI = '#16233D', '#5B6B7F', '#2E9E6A', '#E08A2C'
GL = '#7E8B98'


def f(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def A(x, y, el, r, lab=None):
    if lab is None:
        lab = '' if r >= 18 else '-'
    return f'<g data-atom="{f(x)},{f(y)},{f(r)},{el}{("," + lab) if lab else ""}"></g>'


def T(x, y, s, size=20, anchor='middle', fill=None, weight=None, halo=False, extra=''):
    return (f'<text class="tex" x="{f(x)}" y="{f(y)}" data-mix="{s}" data-size="{size}" data-anchor="{anchor}"'
            + (f' fill="{fill}"' if fill else '') + (f' data-weight="{weight}"' if weight else '')
            + (' data-halo="1"' if halo else '') + (f' {extra}' if extra else '') + '></text>')


def mol(kind, x, y, s=1.0):
    r = lambda e: R[e] * s
    if kind in ('H2', 'O2'):
        e = kind[0]; d = 0.78 * r(e)
        return [(e, x - d, y, r(e)), (e, x + d, y, r(e))]
    if kind == 'H2O':
        d = 0.78 * (r('O') + r('H'))
        dx, dy = d * math.sin(math.radians(52.25)), d * math.cos(math.radians(52.25))
        return [('H', x - dx, y + dy, r('H')), ('H', x + dx, y + dy, r('H')), ('O', x, y, r('O'))]


def lab_of(r):
    return None if r >= 18 else '-'


def moved(dst, src, dur=1.4, delay=.4, on=None):
    """dst 원자를 src 위치에서 옮겨 온다 (원자 보존)"""
    e, x, y, r = dst
    sx, sy = src[1], src[2]
    o = f' data-on="{on}"' if on else ''
    return (f'<g data-anim="move" data-from="{f(sx - x)},{f(sy - y)}" data-dur="{dur}" data-delay="{delay}" data-ease="io"{o}>'
            + A(x, y, e, r, lab_of(r)) + '</g>')


# ───────── 장치(가지 달린 삼각 플라스크 + 고무관 + 주사기) ─────────
def apparatus(V=50, anim=True, bubbles=True, labels=False):
    s = []
    # 고무관
    s.append('<path d="M196 80 C 236 72, 246 120, 302 120" fill="none" stroke="#B9824F" stroke-width="8" stroke-linecap="round"/>')
    # 플라스크
    s.append('<path d="M116 62 V110 L50 236 Q46 250 62 250 H198 Q214 250 210 236 L144 110 V62" fill="#F7FAFC" stroke="%s" stroke-width="3.5" stroke-linejoin="round"/>' % GL)
    hw = lambda yy: 14 + 66 * (yy - 110) / 126
    s.append(f'<path d="M{f(130 - hw(186))} 186 H{f(130 + hw(186))} L208 238 Q211 248 198 248 H62 Q49 248 52 238 Z" fill="#E6F1F8"/>')
    s.append(f'<line x1="{f(130 - hw(186))}" y1="186" x2="{f(130 + hw(186))}" y2="186" stroke="#9FC3DD" stroke-width="2"/>')
    # 가지
    s.append('<path d="M144 82 L196 76 V86 L144 92 Z" fill="#F7FAFC" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % GL)
    # 실리콘 마개
    s.append('<path d="M110 44 H150 L146 72 H114 Z" fill="#6FA8C8" stroke="#16233D" stroke-width="2.5" stroke-linejoin="round"/>')
    # 마그네슘 리본
    s.append('<path d="M98 238 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8" fill="none" stroke="#8E959E" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    if bubbles:
        for i, (bx, by, br) in enumerate([(108, 214, 5), (124, 206, 6), (140, 216, 4.5), (152, 204, 5.5), (116, 196, 4)]):
            s.append(f'<g data-anim="move" data-from="0,{f(232 - by)}" data-dur="{1.3 + .17 * i:.2f}" data-delay="{.2 * i:.2f}" data-rep="loop" data-ease="out"><circle cx="{bx}" cy="{by}" r="{br}" fill="#FFFFFF" fill-opacity=".75" stroke="#7FB6D9" stroke-width="1.8"/></g>')
    # 주사기 몸통·끝
    s.append('<rect x="300" y="114" width="22" height="12" rx="3" fill="#F7FAFC" stroke="%s" stroke-width="2.5"/>' % GL)
    xh = 330 + 2 * V
    gas = f'<rect x="330" y="107" width="{2 * V}" height="26" fill="#DCEFFB"/>'
    if anim:
        gas = f'<g data-anim="scale" data-from="0,1" data-o="330,120" data-dur="2.4" data-delay=".5" data-ease="out">{gas}</g>'
    s.append('<rect x="322" y="104" width="216" height="32" rx="4" fill="#FFFFFF" stroke="%s" stroke-width="3"/>' % GL)
    s.append(gas)
    for v in range(0, 101, 10):
        x = 330 + 2 * v
        s.append(f'<line x1="{x}" y1="104" x2="{x}" y2="{112 if v % 50 else 116}" stroke="{MUT}" stroke-width="1.6"/>')
    s.append('<rect x="538" y="98" width="8" height="44" rx="2" fill="#C9D3DD" stroke="%s" stroke-width="2"/>' % GL)
    pist = (f'<rect x="{xh - 6}" y="106" width="10" height="28" rx="2" fill="#3A3F47"/>'
            f'<rect x="{xh + 4}" y="116" width="{max(150, 560 - xh)}" height="8" fill="#C9D3DD" stroke="{GL}" stroke-width="1.5"/>'
            f'<rect x="{xh + 4 + max(150, 560 - xh)}" y="100" width="8" height="40" rx="2" fill="#9AA5B1" stroke="{GL}" stroke-width="1.5"/>')
    if anim:
        pist = f'<g data-anim="move" data-from="{-2 * V},0" data-dur="2.4" data-delay=".5" data-ease="out">{pist}</g>'
    s.append(pist)
    if labels:
        s.append(T(330, 164, '0', 18, fill=MUT) + T(430, 164, '50', 18, fill=MUT) + T(530, 164, '100', 18, fill=MUT))
    return ''.join(s)


figs = {}

# 표지
figs['COVER'] = ('<svg class="cover-fig" viewBox="0 0 540 540" data-audit="skip" aria-label="가지 달린 삼각 플라스크 속 마그네슘과 염산의 반응으로 생긴 수소가 주사기 피스톤을 밀어낸다">'
                 '<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>'
                 '<g transform="translate(6,130) scale(0.86)">' + apparatus(V=50) + '</g>'
                 + T(270, 120, '수소 기체가 피스톤을 민다', 22, fill=MUT)
                 + T(270, 410, '$\\ce{Mg + 2HCl -&gt; MgCl2 + H2}$', 28, weight=700)
                 + T(270, 448, 'Mg 1 몰 → $\\ce{H2}$ 1 몰', 24, fill=FIELD, weight=700) + '</svg>')

# S5 물 분해 2H2O → 2H2 + O2
b1 = mol('H2O', 120, 70); b2 = mol('H2O', 120, 150)
a_h2a = mol('H2', 350, 62); a_h2b = mol('H2', 350, 140); a_o2 = mol('O2', 458, 101)
s5 = ['<svg class="fig" viewBox="0 0 520 236" style="width:500px" aria-label="물 분자 2개가 수소 분자 2개와 산소 분자 1개로 바뀐다">',
      '<rect x="10" y="10" width="220" height="186" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>',
      '<rect x="290" y="10" width="220" height="186" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>',
      '<g data-arw="238,103,282,103,ink,3"></g>']
s5 += [A(x, y, e, r) for (e, x, y, r) in b1 + b2]
pairs = [(a_h2a[0], b1[0]), (a_h2a[1], b1[1]), (a_h2b[0], b2[0]), (a_h2b[1], b2[1]), (a_o2[0], b1[2]), (a_o2[1], b2[2])]
s5 += [moved(d, src, delay=.5) for d, src in pairs]
s5.append(T(120, 224, '$\\ce{H2O}$ 2개 (H 4, O 2)', 20, weight=700))
s5.append(T(400, 224, '$\\ce{H2}$ 2개 + $\\ce{O2}$ 1개 (H 4, O 2)', 20, weight=700))
s5.append('</svg>')
figs['S5'] = ''.join(s5)

# S6 환산 사다리
xs = [120, 400, 680, 960]
nodes = ['주어진 물질의||질량 · 부피', '주어진 물질의||양(mol)', '구할 물질의||양(mol)', '구할 물질의||질량 · 부피']
arrl = ['÷ 몰질량 · ÷ 22.4 L/mol', '× 계수비(몰비)', '× 몰질량 · × 22.4 L/mol']
s6 = ['<svg class="fig" viewBox="0 0 1080 136" style="width:1080px" aria-label="질량이나 부피를 몰로 바꾸고, 계수비로 구할 물질의 몰을 구한 뒤 다시 질량이나 부피로 바꾸는 환산 사다리">']
for i, x in enumerate(xs):
    fill = '#FFF4B8' if i in (1, 2) else '#FFFFFF'
    stc = '#E0B400' if i in (1, 2) else '#9FB0C2'
    grp = f'<rect x="{x - 100}" y="52" width="200" height="72" rx="14" fill="{fill}" stroke="{stc}" stroke-width="2.5"/>' + T(x, 82, nodes[i], 21, weight=700)
    if i:
        ax = xs[i - 1] + 104
        grp = (f'<g data-arw="{ax},88,{x - 104},88,ink,3"></g>' + T((xs[i - 1] + x) / 2, 34, arrl[i - 1], 19, fill=MUT if i != 2 else FIELD, weight=700) + grp)
        s6.append(f'<g class="step">{grp}</g>')
    else:
        s6.append(grp)
s6.append('</svg>')
figs['S6'] = ''.join(s6)

# S8 입자 상자: H2 5 + O2 2 → H2O 4 + H2 1(남음)
sc = .75
H2b = [mol('H2', x, y, sc) for x, y in [(70, 50), (170, 50), (270, 50), (120, 165), (220, 165)]]
O2b = [mol('O2', x, y, sc) for x, y in [(110, 108), (230, 108)]]
W = [mol('H2O', x, y, sc) for x, y in [(490, 48), (590, 48), (690, 48), (520, 128)]]
left = mol('H2', 650, 140, sc)
s8 = ['<svg class="fig" viewBox="0 0 760 236" style="width:720px" aria-label="수소 분자 5개와 산소 분자 2개가 반응해 물 분자 4개가 생기고 수소 분자 1개가 남는다">',
      '<rect x="10" y="10" width="320" height="190" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>',
      '<rect x="420" y="10" width="330" height="190" rx="14" fill="#F4F8FC" stroke="#9FC3DD" stroke-width="2"/>',
      '<g data-arw="342,105,408,105,ink,3"></g>']
for m in H2b + O2b:
    s8 += [A(x, y, e, r, '-') for (e, x, y, r) in m]
pairs = []
for i in range(4):
    pairs += [(W[i][0], H2b[i][0]), (W[i][1], H2b[i][1])]
pairs += [(W[0][2], O2b[0][0]), (W[1][2], O2b[0][1]), (W[2][2], O2b[1][0]), (W[3][2], O2b[1][1])]
pairs += [(left[0], H2b[4][0]), (left[1], H2b[4][1])]
s8 += [moved(d, src, delay=.5) for d, src in pairs]
s8.append('<circle cx="650" cy="140" r="30" fill="none" stroke="#E08A2C" stroke-width="2.5" stroke-dasharray="6 4"/>')
s8.append(T(650, 191, '남음', 19, fill=EQUI, weight=700))
s8.append(T(170, 226, '반응 전: $\\ce{H2}$ 5개, $\\ce{O2}$ 2개', 20, weight=700))
s8.append(T(585, 226, '반응 후: $\\ce{H2O}$ 4개 + $\\ce{H2}$ 1개', 20, weight=700))
s8.append('</svg>')
figs['S8'] = ''.join(s8)

# S14 장치 그림 (라벨 포함)
s14 = ['<svg class="fig" viewBox="0 0 620 316" style="width:560px" aria-label="가지 달린 삼각 플라스크에 실리콘 마개를 끼우고, 가지를 고무관으로 100 mL 주사기에 이은 장치">',
       '<g transform="translate(0,20)">' + apparatus(V=40, labels=True) + '</g>',
       '<line x1="150" y1="52" x2="182" y2="30" stroke="#5B6B7F" stroke-width="1.6"/>', T(186, 30, '실리콘 마개', 19, anchor='start'),
       '<line x1="238" y1="108" x2="256" y2="66" stroke="#5B6B7F" stroke-width="1.6"/>', T(250, 60, '고무관', 19, anchor='start'),
       T(460, 100, '주사기(100 mL)', 19, weight=700),
       T(130, 304, '가지 달린 삼각 플라스크', 19, weight=700),
       '<line x1="196" y1="232" x2="236" y2="226" stroke="#5B6B7F" stroke-width="1.6"/>', T(242, 232, '묽은 염산 50 mL', 19, anchor='start'),
       '<line x1="158" y1="252" x2="236" y2="262" stroke="#5B6B7F" stroke-width="1.6"/>', T(242, 268, '마그네슘 리본', 19, anchor='start'),
       '</svg>']
figs['S14'] = ''.join(s14)

# S19 그래프: 염산 충분 vs 적게
X0, X1, Y0, YT = 80, 470, 280, 40
px = (X1 - X0) / 4.5; py = (Y0 - YT) / 110
P = lambda n, v: (X0 + n * px, Y0 - v * py)
g = ['<svg class="fig" viewBox="0 0 520 344" style="width:500px" aria-label="마그네슘의 양에 따른 수소 부피 그래프. 염산이 충분하면 직선으로 늘고, 염산이 적으면 2.5 mmol에서 꺾여 60 mL로 일정하다">']
for v in (50, 100):
    y = Y0 - v * py
    g.append(f'<line x1="{X0}" y1="{f(y)}" x2="{X1}" y2="{f(y)}" stroke="#E2E7EC" stroke-width="1.5"/>')
    g.append(T(X0 - 10, y + 7, str(v), 18, anchor='end', fill=MUT))
for n in range(0, 5):
    x = X0 + n * px
    g.append(f'<line x1="{f(x)}" y1="{Y0}" x2="{f(x)}" y2="{Y0 + 6}" stroke="{MUT}" stroke-width="1.6"/>')
    g.append(T(x, Y0 + 28, str(n), 18, fill=MUT))
g.append(f'<g data-arw="{X0},{Y0},{X1 + 26},{Y0},muted,2"></g><g data-arw="{X0},{Y0},{X0},{YT - 22},muted,2"></g>')
g.append(T(X0 + 10, YT - 10, '$V$ [mL]', 20, anchor='start'))
g.append(T(X1 - 4, Y0 + 50, 'Mg의 양 [mmol]', 20, anchor='end'))
a, b = P(0, 0), P(4.4, 105.6)
g.append(f'<path d="M{f(a[0])} {f(a[1])} L{f(b[0])} {f(b[1])}" stroke="{INK}" stroke-width="3" fill="none" data-anim="draw" data-dur="1.2"/>')
g.append(T(b[0] - 6, b[1] + 4, '염산 충분', 19, anchor='end', weight=700, halo=True))
k, e2 = P(2.5, 60), P(4.4, 60)
g.append(f'<path d="M{f(a[0])} {f(a[1])} L{f(k[0])} {f(k[1])} L{f(e2[0])} {f(e2[1])}" stroke="{EQUI}" stroke-width="3.5" stroke-dasharray="9 6" fill="none" data-anim="draw" data-dur="1.4" data-delay=".6"/>')
g.append(T(e2[0], e2[1] + 28, '염산 적게', 19, anchor='end', fill=EQUI, weight=700))
g.append(f'<g class="step" data-g="k1"><circle cx="{f(k[0])}" cy="{f(k[1])}" r="8" fill="#FFE45C" stroke="{INK}" stroke-width="2"/>'
         f'<line x1="{f(k[0])}" y1="{f(k[1] + 10)}" x2="{f(k[0])}" y2="{Y0}" stroke="{MUT}" stroke-width="1.6" stroke-dasharray="5 4"/>'
         + T(k[0] + 12, k[1] + 74, '꺾이는 점||Mg 2.5 mmol, 60 mL', 19, anchor='start', weight=700, halo=True) + '</g>')
g.append('</svg>')
figs['S19'] = ''.join(g)

TPL = open(os.path.join(HERE, 'slides.tpl.html'), encoding='utf-8').read()
for k_, v_ in figs.items():
    TPL = TPL.replace('{{' + k_ + '}}', v_)
assert '{{' not in TPL, TPL[TPL.index('{{'):TPL.index('{{') + 30]
open(OUT, 'w', encoding='utf-8').write(TPL)
print('ok', len(TPL))
