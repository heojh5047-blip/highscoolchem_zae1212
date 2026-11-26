# 2-1-4 그림 생성: slides.src.html의 자리 표시를 계산한 SVG로 바꿔 slides.html을 만든다.
#  {ION|cx|cy|Z|r1|q}           이온(또는 q=0이면 원자) 보어 모형: 전자 수 = Z − q, q≠0이면 대괄호와 전하 표시
#  {MOL|cx|cy|Zc|r1|a1,a2,..|l1,l2,..}  중심 원자 Zc + 수소 원자들(각도 a, 도). 공유 전자쌍은 겹친 곳, l은 비공유 전자쌍 방향(도)
#  {DIA|cx|cy|Z|r1|n|l1,l2,..}  같은 원자 2개(가로)가 전자쌍 n개를 공유. l은 왼쪽 원자의 비공유 전자쌍 방향(오른쪽 원자는 좌우 대칭)
#  {LAT|x|y|nx|ny|s}            염화 나트륨 단면 격자: 양이온(작은 빨강)·음이온(큰 파랑) 번갈아
import os, re, math
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/2-1-4_이온_결합과_공유_결합/slides.html')
EL = '#1F6FD1'; NUC = '#D7263D'; SH = '#9FB0C2'
def shells_of(n):
    return [min(n, 2)] + ([min(n - 2, 8)] if n > 2 else []) + ([n - 10] if n > 10 else [])
def ang_list(n, first=False):
    if first: return [-math.pi / 2 + math.pi * k for k in range(n)]
    out = []
    for k in range(n):
        d = k % 4; base = -math.pi / 2 + d * math.pi / 2
        out.append(base + ((-0.24 if k < 4 else 0.24) if n > 4 + d else 0))
    return out
def e(x, y, r): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{EL}"/>'
def nucleus(cx, cy, Z, r1):
    rn = r1 * 0.66; fs = max(16, int(rn * (0.95 if Z < 10 else 0.8)))
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rn:.1f}" fill="{NUC}"/>'
            f'<text class="tex" x="{cx:.1f}" y="{cy + rn * 0.36:.1f}" data-tex="{Z}+" data-size="{fs}" data-anchor="middle" fill="#FFFFFF"></text>')
def ion(cx, cy, Z, r1, q):
    cx, cy, Z, r1, q = float(cx), float(cy), int(Z), float(r1), int(q)
    sh = shells_of(Z - q); out = []; er = max(3.5, r1 * 0.16)
    for i, n in enumerate(sh):
        r = r1 * (i + 1)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{SH}" stroke-width="1.5"/>')
        for t in ang_list(n, i == 0): out.append(e(cx + r * math.cos(t), cy + r * math.sin(t), er))
    out.append(nucleus(cx, cy, Z, r1))
    if q:
        R = r1 * len(sh) + 12; w = 10
        out.append(f'<path d="M{cx - R + w:.1f} {cy - R:.1f} H{cx - R:.1f} V{cy + R:.1f} H{cx - R + w:.1f} M{cx + R - w:.1f} {cy - R:.1f} H{cx + R:.1f} V{cy + R:.1f} H{cx + R - w:.1f}" fill="none" stroke="#16233D" stroke-width="2.5"/>')
        # q>0: 전자를 잃음 → 양이온(+), q<0: 전자를 얻음 → 음이온(−)
        lab = ('' if abs(q) == 1 else str(abs(q))) + ('+' if q > 0 else '-')
        out.append(f'<text class="tex" x="{cx + R + 4:.1f}" y="{cy - R + 14:.1f}" data-tex="{lab}" data-size="22"></text>')
    return ''.join(out)
def inner(cx, cy, Z, r1):
    """원자핵과 안쪽 껍질(가장 바깥 껍질 제외)."""
    sh = shells_of(Z); out = []; er = max(3.5, r1 * 0.16)
    for i, n in enumerate(sh[:-1]):
        r = r1 * (i + 1)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{SH}" stroke-width="1.5"/>')
        for t in ang_list(n, i == 0): out.append(e(cx + r * math.cos(t), cy + r * math.sin(t), er))
    R = r1 * len(sh)
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="none" stroke="{SH}" stroke-width="1.5"/>')
    return ''.join(out), R
def pair_at(cx, cy, R, t, er, gap=0.2):
    return e(cx + R * math.cos(t - gap), cy + R * math.sin(t - gap), er) + e(cx + R * math.cos(t + gap), cy + R * math.sin(t + gap), er)
def shared(x1, y1, x2, y2, f, er, n=1, sep=None):
    """두 중심 사이 비율 f 지점에 공유 전자쌍 n개(선에 수직으로 나란히)."""
    mx, my = x1 + (x2 - x1) * f, y1 + (y2 - y1) * f
    L = math.hypot(x2 - x1, y2 - y1); px, py = -(y2 - y1) / L, (x2 - x1) / L
    sep = sep or er * 2.6; out = []
    m = 2 * n
    for k in range(m):
        o = (k - (m - 1) / 2) * sep
        out.append(e(mx + px * o, my + py * o, er))
    return ''.join(out)
def mol(cx, cy, Zc, r1, angs, lones):
    cx, cy, Zc, r1 = float(cx), float(cy), int(Zc), float(r1)
    er = max(3.5, r1 * 0.16); out = []
    s, R = inner(cx, cy, Zc, r1); out.append(s)
    rh = r1 * 1.15; d = R + rh - rh * 0.55
    for a in [float(v) for v in angs.split(',') if v]:
        t = math.radians(a); hx, hy = cx + d * math.cos(t), cy + d * math.sin(t)
        out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{rh:.1f}" fill="none" stroke="{SH}" stroke-width="1.5"/>')
        out.append(nucleus(hx, hy, 1, r1 * 0.6))
        f = ((d - rh) + R) / 2 / d   # 겹친 곳 한가운데
        out.append(shared(cx, cy, hx, hy, f, er))
    for a in [float(v) for v in lones.split(',') if v]:
        out.append(pair_at(cx, cy, R, math.radians(a), er))
    out.append(nucleus(cx, cy, Zc, r1))
    return ''.join(out)
def dia(cx, cy, Z, r1, n, lones):
    cx, cy, Z, r1, n = float(cx), float(cy), int(Z), float(r1), int(n)
    er = max(3.5, r1 * 0.16); out = []
    R = r1 * len(shells_of(Z)); d = 2 * R - R * 0.55
    x1, x2 = cx - d / 2, cx + d / 2
    for x in (x1, x2):
        s, _ = inner(x, cy, Z, r1); out.append(s)
    out.append(shared(x1, cy, x2, cy, 0.5, er, n, sep=er * 2.5))
    for a in [float(v) for v in lones.split(',') if v]:
        t = math.radians(a)
        out.append(pair_at(x1, cy, R, t, er)); out.append(pair_at(x2, cy, R, math.pi - t, er))
    out.append(nucleus(x1, cy, Z, r1)); out.append(nucleus(x2, cy, Z, r1))
    return ''.join(out)
def lat(x, y, nx, ny, s):
    x, y, nx, ny, s = float(x), float(y), int(nx), int(ny), float(s); out = []
    for j in range(ny):
        for i in range(nx):
            cx, cy = x + i * s, y + j * s
            if (i + j) % 2: out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s * 0.46:.1f}" fill="#7FB3E6" stroke="#1F6FD1" stroke-width="1.5"/>')
            else: out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s * 0.28:.1f}" fill="#F08A97" stroke="#D7263D" stroke-width="1.5"/>')
    return ''.join(out)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{ION\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: ion(*m.groups()), s)
s = re.sub(r'\{MOL\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: mol(*m.groups()), s)
s = re.sub(r'\{DIA\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: dia(*m.groups()), s)
s = re.sub(r'\{LAT\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: lat(*m.groups()), s)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
