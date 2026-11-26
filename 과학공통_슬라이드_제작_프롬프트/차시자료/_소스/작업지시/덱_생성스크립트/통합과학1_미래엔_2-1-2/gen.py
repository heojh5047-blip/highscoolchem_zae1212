# 2-1-2 원그래프(도넛) 생성: slides.src.html의 {PIE|이름|cx|cy|r} 자리를 교과서 59쪽 질량비로 계산한 부채꼴로 바꾼다.
import os, math, re
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/2-1-2_별의_진화와_원소의_생성/slides.html')
DATA = {
 'earth': [('철', 35.0, '#8C99A6'), ('산소', 30.0, '#9FC3DD'), ('규소', 15.0, '#C9A27A'), ('마그네슘', 13.0, '#A7D7B8'), ('니켈', 2.4, '#5B6B7F'), ('황', 1.9, '#F7C548'), ('칼슘', 1.1, '#F2C9A0'), ('알루미늄', 1.1, '#D6DCE3'), ('기타', 0.5, '#EEF3F8')],
 'human': [('산소', 65.0, '#9FC3DD'), ('탄소', 18.5, '#5B6B7F'), ('수소', 9.5, '#F9A8D4'), ('질소', 3.3, '#C4B5FD'), ('칼슘', 1.5, '#F2C9A0'), ('인', 1.0, '#FDBA74'), ('기타', 1.2, '#EEF3F8')]}
def pie(name, cx, cy, r):
    cx, cy, r = float(cx), float(cy), float(r); r0 = r * 0.55
    a = -math.pi / 2; out = []
    for lab, v, col in DATA[name]:
        b = a + 2 * math.pi * v / 100; big = 1 if b - a > math.pi else 0
        p = lambda R, t: (cx + R * math.cos(t), cy + R * math.sin(t))
        x1, y1 = p(r, a); x2, y2 = p(r, b); x3, y3 = p(r0, b); x4, y4 = p(r0, a)
        out.append(f'<path d="M{x1:.1f} {y1:.1f} A{r:.0f} {r:.0f} 0 {big} 1 {x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} A{r0:.0f} {r0:.0f} 0 {big} 0 {x4:.1f} {y4:.1f} Z" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')
        if v >= 9:
            m = (a + b) / 2; lx, ly = p((r + r0) / 2, m)
            out.append(f'<text class="tex" x="{lx:.0f}" y="{ly + 7:.0f}" data-mix="{lab}||{v:g} %" data-size="18" data-anchor="middle"></text>')
        a = b
    return ''.join(out)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{PIE\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: pie(*m.groups()), s)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
