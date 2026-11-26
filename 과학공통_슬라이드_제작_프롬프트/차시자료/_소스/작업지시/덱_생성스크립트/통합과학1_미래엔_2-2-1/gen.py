# 2-2-1 그림 생성: slides.src.html의 자리 표시를 계산한 SVG로 바꿔 slides.html을 만든다.
#  {MIN|x|y|kind|s}   규산염 광물 결합 모식도(위에서 본 사면체 = 삼각형, 꼭짓점 산소·가운데 규소)
#                     kind: ol(독립) · py(한 줄 사슬) · am(두 줄 사슬) · bi(판) · qz(입체)
#  {TET|cx|cy|s}      규산염 사면체 입체 그림(규소 1 + 산소 4)
#  {CRUST|x|y|w|h}    지각의 원소 질량비 가로 막대(지도서 자료)
import os, re, math
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/2-2-1_지각과_생명체를_구성하는_물질/slides.html')
OF, OS, SIF = '#E5533D', '#A8321F', '#4F6BD8'
def tri(cx, cy, s, up=True, op=1.0):
    h = s * math.sqrt(3) / 2; k = 1 if up else -1
    p = [(cx, cy - k * 2 * h / 3), (cx - s / 2, cy + k * h / 3), (cx + s / 2, cy + k * h / 3)]
    out = [f'<path d="M{p[0][0]:.1f} {p[0][1]:.1f} L{p[1][0]:.1f} {p[1][1]:.1f} L{p[2][0]:.1f} {p[2][1]:.1f} Z" fill="#FDE8C8" fill-opacity="{0.9*op:.2f}" stroke="#C2410C" stroke-opacity="{op:.2f}" stroke-width="2"/>']
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s*0.09:.1f}" fill="{SIF}" opacity="{op:.2f}"/>')
    return out, p
def oxy(pts, s, op=1.0):
    seen = []; out = []
    for x, y in pts:
        if any(abs(x - a) < 1 and abs(y - b) < 1 for a, b in seen): continue
        seen.append((x, y)); out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s*0.13:.1f}" fill="{OF}" stroke="{OS}" stroke-width="1" opacity="{op:.2f}"/>')
    return out
def rows(x, y, s, nrow, ncol, op=1.0):
    h = s * math.sqrt(3) / 2; body = []; pts = []
    for r in range(nrow):
        off = (r % 2) * s / 2
        for c in range(ncol - (r % 2)):
            cx = x + off + c * s + s / 2; cy = y + r * h + 2 * h / 3
            b, p = tri(cx, cy, s, True, op); body += b; pts += p
    return body + oxy(pts, s, op)
def mineral(x, y, kind, s):
    x, y, s = float(x), float(y), float(s); out = []
    if kind == 'ol':
        for i in range(3):
            b, p = tri(x + s * 0.7 + i * s * 1.6, y + s * (0.6 if i % 2 else 1.1), s); out += b + oxy(p, s)
    elif kind == 'py': out += rows(x, y + s * 0.4, s, 1, 4)
    elif kind == 'am': out += rows(x, y + s * 0.1, s, 2, 4)
    elif kind == 'bi': out += rows(x, y - s * 0.2, s, 3, 4)
    elif kind == 'qz':
        out += rows(x + s * 0.35, y - s * 0.45, s, 3, 4, 0.35)
        out += rows(x, y - s * 0.05, s, 3, 4)
    return ''.join(out)
def tet(cx, cy, s):
    cx, cy, s = float(cx), float(cy), float(s)
    top = (cx, cy - s * 0.95); a = (cx - s * 0.85, cy + s * 0.45); b = (cx + s * 0.85, cy + s * 0.45); c = (cx + s * 0.38, cy - s * 0.28)
    out = [f'<path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} L{top[0]:.1f} {top[1]:.1f} Z" fill="#FDE8C8" fill-opacity=".55" stroke="#C2410C" stroke-width="2.5"/>']
    for p, q in ((top, c), (a, c), (b, c)):
        out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#C2410C" stroke-width="2" stroke-dasharray="6 5"/>')
    ctr = ((top[0] + a[0] + b[0] + c[0]) / 4, (top[1] + a[1] + b[1] + c[1]) / 4)
    for p in (top, a, b, c):
        out.append(f'<line x1="{ctr[0]:.1f}" y1="{ctr[1]:.1f}" x2="{p[0]:.1f}" y2="{p[1]:.1f}" stroke="#8C99A6" stroke-width="3"/>')
    out.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{s*0.2:.1f}" fill="{OF}" stroke="{OS}" stroke-width="1.5" opacity=".8"/>')
    out.append(f'<circle cx="{ctr[0]:.1f}" cy="{ctr[1]:.1f}" r="{s*0.15:.1f}" fill="{SIF}"/>')
    for p in (top, a, b):
        out.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{s*0.2:.1f}" fill="{OF}" stroke="{OS}" stroke-width="1.5"/>')
    return ''.join(out)
CR = [('산소', 46.6), ('규소', 27.7), ('알루미늄', 8.1), ('철', 5.0), ('칼슘', 3.6), ('나트륨', 2.8), ('칼륨', 2.6), ('마그네슘', 2.1), ('기타', 1.5)]
def crust(x, y, w, h):
    x, y, w, h = float(x), float(y), float(w), float(h); out = []
    rh = h / len(CR); X0 = x + 100; K = (w - 170) / 50
    for i, (n, v) in enumerate(CR):
        yy = y + i * rh; col = '#E5533D' if i == 0 else ('#4F6BD8' if i == 1 else '#9FB0C2')
        out.append(f'<text class="tex" x="{X0 - 10:.0f}" y="{yy + rh * 0.62:.1f}" data-mix="{n}" data-size="18" data-anchor="end"></text>')
        out.append(f'<rect x="{X0:.0f}" y="{yy + rh * 0.15:.1f}" width="{v * K:.1f}" height="{rh * 0.7:.1f}" rx="4" fill="{col}"/>')
        out.append(f'<text class="tex" x="{X0 + v * K + 8:.1f}" y="{yy + rh * 0.62:.1f}" data-tex="{v}" data-size="18"></text>')
    return ''.join(out)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{MIN\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: mineral(*m.groups()), s)
s = re.sub(r'\{TET\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: tet(*m.groups()), s)
s = re.sub(r'\{CRUST\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: crust(*m.groups()), s)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
