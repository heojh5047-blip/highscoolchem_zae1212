# 2-1-3 그림 생성: slides.src.html의 자리 표시를 계산한 SVG로 바꿔 slides.html을 만든다.
#  {PT|x|y|cell|mode}   주기율표 격자(18열 × 7행). mode: plain(주기·족 번호) · metal(금속·비금속·준금속 칠) · group(1족·17족 강조)
#  {BOHR|cx|cy|Z|r1}    보어 원자 모형: 원자핵(Z+) + 전자 껍질 + 전자(껍질 위, 2·8·8 규칙)
#  {VE|x|y|w|h}         원자 번호 1–20의 원자가 전자 수 그래프(18족 제외 점)
import os, re, math
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/2-1-3_원소의_주기성과_결합/slides.html')
SYM = 'H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca'.split()
NONMETAL = {1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18, 34, 35, 36, 53, 54, 86}
METALLOID = {5, 14, 32, 33, 51, 52}
def pos(z):  # (주기, 족)
    if z <= 2: return (1, 1 if z == 1 else 18)
    if z <= 10: p, k = 2, z - 2
    elif z <= 18: p, k = 3, z - 10
    elif z <= 36: p, k = 4, z - 18
    elif z <= 54: p, k = 5, z - 36
    elif z <= 86: p, k = 6, z - 54
    else: p, k = 7, z - 86
    if p <= 3: g = k if k <= 2 else k + 10
    elif p <= 5: g = k
    else:
        if k <= 2: g = k
        elif k <= 17: return None   # 란타넘족·악티늄족은 표 아래(생략), 3족 칸에 대표
        else: g = k - 14
    return (p, g)
def pt(x, y, c, mode):
    x, y, c = float(x), float(y), float(c); out = []
    cells = {}
    for z in range(1, 119):
        q = pos(z)
        if q: cells[q] = z
    for p in range(1, 8):
        for g in range(1, 19):
            if (p, g) not in cells and not (g == 3 and p >= 6): continue
            z = cells.get((p, g))
            fill = '#FFFFFF'
            if mode == 'metal' and z:
                fill = '#DDEEF8' if z in NONMETAL else ('#F1ECFB' if z in METALLOID else '#FDE8C8')
            if mode == 'metal' and g == 3 and p >= 6: fill = '#FDE8C8'
            if mode == 'group' and g == 1 and p >= 2: fill = '#FCE8EA'
            if mode == 'group' and g == 17: fill = '#E8F5EE'
            cx, cy = x + (g - 1) * c, y + (p - 1) * c
            out.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{c:.1f}" height="{c:.1f}" fill="{fill}" stroke="#9FB0C2" stroke-width="1"/>')
            if z and z <= 20 and c >= 26:
                out.append(f'<text class="tex" x="{cx + c / 2:.1f}" y="{cy + c * 0.66:.1f}" data-tex="\\mathrm{{{SYM[z - 1]}}}" data-size="{max(18, int(c * 0.42))}" data-anchor="middle"></text>')
    if mode == 'plain':
        for g in range(1, 19):
            out.append(f'<text class="tex" x="{x + (g - 0.5) * c:.1f}" y="{y - 8:.1f}" data-tex="{g}" data-size="16" data-anchor="middle" fill="#5B6B7F"></text>')
        for p in range(1, 8):
            out.append(f'<text class="tex" x="{x - 8:.1f}" y="{y + (p - 0.5) * c + 6:.1f}" data-tex="{p}" data-size="16" data-anchor="end" fill="#5B6B7F"></text>')
    return ''.join(out)
def bohr(cx, cy, Z, r1):
    cx, cy, Z, r1 = float(cx), float(cy), int(Z), float(r1)
    shells = [min(Z, 2)] + ([min(Z - 2, 8)] if Z > 2 else []) + ([Z - 10] if Z > 10 else [])
    out = []
    for i, n in enumerate(shells):
        r = r1 * (i + 1)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#9FB0C2" stroke-width="1.5"/>')
        for k in range(n):
            # 짝을 지어 4방향(위·오른쪽·아래·왼쪽)에 배치: 1–4번째는 각 방향 하나씩, 5–8번째는 짝
            if i == 0: t = -math.pi / 2 + math.pi * k
            else:
                d = k % 4; base = -math.pi / 2 + d * math.pi / 2
                t = base + ((-0.24 if k < 4 else 0.24) if n > 4 + d else 0)
            out.append(f'<circle cx="{cx + r * math.cos(t):.1f}" cy="{cy + r * math.sin(t):.1f}" r="{max(3.5, r1 * 0.16):.1f}" fill="#1F6FD1"/>')
    rn = r1 * 0.66
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rn:.1f}" fill="#D7263D"/>')
    out.append(f'<text class="tex" x="{cx:.1f}" y="{cy + rn * 0.36:.1f}" data-tex="{Z}+" data-size="{max(16, int(rn * (0.95 if Z < 10 else 0.8)))}" data-anchor="middle" fill="#FFFFFF"></text>')
    return ''.join(out)
def ve(x, y, w, h):
    x, y, w, h = float(x), float(y), float(w), float(h)
    X = lambda z: x + (z - 1) / 17 * w; Y = lambda v: y + h - v / 8 * h
    out = [f'<g data-arw="{x:.0f},{y + h:.0f},{x + w + 24:.0f},{y + h:.0f},muted,2.5"></g>', f'<g data-arw="{x:.0f},{y + h:.0f},{x:.0f},{y - 20:.0f},muted,2.5"></g>']
    for v in (2, 4, 6, 8):
        out.append(f'<line x1="{x:.0f}" y1="{Y(v):.1f}" x2="{x + w:.0f}" y2="{Y(v):.1f}" stroke="#E2E7EC" stroke-width="1.5"/>')
        out.append(f'<text class="tex" x="{x - 10:.0f}" y="{Y(v) + 6:.1f}" data-tex="{v}" data-size="18" data-anchor="end"></text>')
    val = lambda z: z if z <= 2 else (z - 2 if z <= 10 else z - 10)
    segs = [range(3, 10), range(11, 18)]
    for sg in segs:
        out.append('<polyline points="' + ' '.join(f'{X(z):.1f},{Y(val(z)):.1f}' for z in sg) + '" fill="none" stroke="#16233D" stroke-width="2.5"/>')
    for z in range(1, 19):
        if z in (2, 10, 18):
            out.append(f'<circle cx="{X(z):.1f}" cy="{y + h:.1f}" r="6" fill="#FFFFFF" stroke="#8C99A6" stroke-width="2.5"/>')
        else:
            out.append(f'<circle cx="{X(z):.1f}" cy="{Y(val(z)):.1f}" r="6" fill="#D7263D"/>')
        out.append(f'<text class="tex" x="{X(z):.1f}" y="{y + h + 26:.0f}" data-tex="\\mathrm{{{SYM[z - 1]}}}" data-size="17" data-anchor="middle"></text>')
    return ''.join(out)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{PT\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: pt(*m.groups()), s)
s = re.sub(r'\{BOHR\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: bohr(*m.groups()), s)
s = re.sub(r'\{VE\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: ve(*m.groups()), s)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
