# 3-2-1 그림 생성: slides.src.html의 자리 표시를 계산한 SVG로 바꿔 slides.html을 만든다.
#  {STROBE|x|y|s|vx|mode}  0.1 s 간격 다중 섬광 그림. s = 화면 px/cm, vx = 수평 속력 m/s.
#                          mode: A(자유 낙하만) · AB(둘 다) — 위치 y = ½ g t² (g = 9.8 m/s²), x = vx t
#  {VT|x|y|w|h}            자유 낙하 속력–시간 그래프 0–4 s, 9.8 m/s 간격
import os, re
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/3-2-1_중력의_작용/slides.html')
g = 9.8
def strobe(x, y, s, vx, mode):
    x, y, s, vx = float(x), float(y), float(s), float(vx)
    out = []
    W, Hh = 70, 130  # cm
    for c in range(0, W + 1, 10):
        out.append(f'<line x1="{x + c * s:.1f}" y1="{y:.1f}" x2="{x + c * s:.1f}" y2="{y + Hh * s:.1f}" stroke="#E2E7EC" stroke-width="1"/>')
    for r in range(0, Hh + 1, 10):
        out.append(f'<line x1="{x:.1f}" y1="{y + r * s:.1f}" x2="{x + W * s:.1f}" y2="{y + r * s:.1f}" stroke="#E2E7EC" stroke-width="1"/>')
    for i in range(6):
        t = i / 10; d = 0.5 * g * t * t * 100
        op = 0.35 + 0.65 * (i == 5)
        out.append(f'<circle cx="{x + 4 * s:.1f}" cy="{y + d * s:.1f}" r="{max(5, 2.6 * s):.1f}" fill="#D7263D" opacity="{0.55 + 0.09 * i:.2f}"/>')
        if mode == 'AB':
            out.append(f'<circle cx="{x + (4 + vx * t * 100) * s:.1f}" cy="{y + d * s:.1f}" r="{max(5, 2.6 * s):.1f}" fill="#1F6FD1" opacity="{0.55 + 0.09 * i:.2f}"/>')
            out.append(f'<line x1="{x + 4 * s:.1f}" y1="{y + d * s:.1f}" x2="{x + (4 + vx * t * 100) * s:.1f}" y2="{y + d * s:.1f}" stroke="#8C99A6" stroke-width="1.2" stroke-dasharray="4 4"/>')
    return ''.join(out)
def vt(x, y, w, h):
    x, y, w, h = map(float, (x, y, w, h))
    X = lambda t: x + t / 4.4 * w; Y = lambda v: y + h - v / 44 * h
    out = [f'<g data-arw="{x:.0f},{y + h:.0f},{x + w + 14:.0f},{y + h:.0f},muted,2.5"></g><g data-arw="{x:.0f},{y + h:.0f},{x:.0f},{y - 14:.0f},muted,2.5"></g>']
    for t in range(1, 5):
        v = g * t
        out.append(f'<line x1="{X(t):.1f}" y1="{Y(v):.1f}" x2="{X(t):.1f}" y2="{y + h:.1f}" stroke="#C9D3DD" stroke-dasharray="4 4"/><line x1="{x:.1f}" y1="{Y(v):.1f}" x2="{X(t):.1f}" y2="{Y(v):.1f}" stroke="#C9D3DD" stroke-dasharray="4 4"/>')
        out.append(f'<text class="tex" x="{X(t):.1f}" y="{y + h + 22:.0f}" data-tex="{t}" data-size="16" data-anchor="middle"></text>')
        out.append(f'<text class="tex" x="{x - 8:.0f}" y="{Y(v) + 6:.1f}" data-tex="{v:.1f}" data-size="16" data-anchor="end"></text>')
    out.append(f'<g data-anim="draw" data-dur="1.6"><line x1="{X(0):.1f}" y1="{Y(0):.1f}" x2="{X(4.2):.1f}" y2="{Y(g * 4.2):.1f}" stroke="#D7263D" stroke-width="3.5"/></g>')
    return ''.join(out)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{STROBE\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: strobe(*m.groups()), s)
s = re.sub(r'\{VT\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: vt(*m.groups()), s)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
