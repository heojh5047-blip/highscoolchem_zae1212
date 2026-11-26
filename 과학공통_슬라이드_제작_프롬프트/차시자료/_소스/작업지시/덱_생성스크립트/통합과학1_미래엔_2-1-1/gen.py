# 2-1-1 스펙트럼 그림 생성: slides.src.html의 {SPEC|id|kind|lines|x|y|w|h} 자리를 SVG로 바꿔 slides.html을 만든다.
# kind: cont(연속) · emit(방출: 검은 바탕 + 밝은 선) · abs(흡수: 연속 + 검은 선). lines: 파장 nm를 쉼표로(H, He, Na 같은 이름도 됨)
# 파장 범위 400–700 nm를 너비 w에 선형으로. 색은 파장 → RGB 근사(Bruton).
import os, re
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/2-1-1_우주_초기에_생성된_원소/slides.html')
LINES = {'H': [410.2, 434.0, 486.1, 656.3], 'He': [447.1, 471.3, 492.2, 501.6, 587.6, 667.8], 'Na': [589.0, 589.6], 'O': [557.7, 630.0]}
def rgb(l):
    if l < 440: r, g, b = -(l - 440) / 60, 0, 1
    elif l < 490: r, g, b = 0, (l - 440) / 50, 1
    elif l < 510: r, g, b = 0, 1, -(l - 510) / 20
    elif l < 580: r, g, b = (l - 510) / 70, 1, 0
    elif l < 645: r, g, b = 1, -(l - 645) / 65, 0
    else: r, g, b = 1, 0, 0
    f = 0.3 + 0.7 * (l - 380) / 40 if l < 420 else (0.3 + 0.7 * (780 - l) / 80 if l > 700 else 1)
    return '#%02X%02X%02X' % tuple(int(255 * (c * f) ** 0.8) for c in (r, g, b))
def X(l, x, w): return x + (l - 400) / 300 * w
def spec(i, kind, lines, x, y, w, h):
    x, y, w, h = float(x), float(y), float(w), float(h)
    L = []
    for t in (lines.split(',') if lines else []):
        L += LINES.get(t, [float(t)] if t.replace('.', '').isdigit() else [])
    out = []
    if kind in ('cont', 'abs'):
        stops = ''.join(f'<stop offset="{(l - 400) / 300:.3f}" stop-color="{rgb(l)}"/>' for l in range(400, 701, 10))
        out.append(f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>')
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#{i})"/>')
        for l in L: out.append(f'<rect x="{X(l, x, w) - 1.5:.1f}" y="{y:.1f}" width="3" height="{h:.1f}" fill="#111111"/>')
    else:
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#111111"/>')
        for l in L: out.append(f'<rect x="{X(l, x, w) - 1.5:.1f}" y="{y:.1f}" width="3" height="{h:.1f}" fill="{rgb(l)}"/>')
    return ''.join(out)
def vl(lines, x, w, y1, y2):
    L = []
    for t in lines.split(','): L += LINES.get(t, [])
    return ''.join(f'<line x1="{X(l, float(x), float(w)):.1f}" y1="{y1}" x2="{X(l, float(x), float(w)):.1f}" y2="{y2}"/>' for l in L)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{VL\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: vl(*m.groups()), s)
s = re.sub(r'\{SPEC\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: spec(*m.groups()), s)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
