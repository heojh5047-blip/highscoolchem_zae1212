# 3-1-1 그림 생성: slides.src.html의 자리 표시를 계산한 SVG로 바꿔 slides.html을 만든다.
#  {ATM|x|y|w|h}    기권의 높이–기온 그래프(표준 대기 근삿값: 0 km 15 ℃, 11 km −56, 20 km −56, 50 km −2, 85 km −86, 110 km 약 20)
#  {SEA|x|y|w|h}    해수의 깊이–수온 그래프(중위도 여름 모식: 0–50 m 20 ℃, 50–1000 m 급감, 1000 m 아래 약 4 ℃)
#  {EARTH|cx|cy|R}  지구 내부 단면(반지름 비례: 지각 과장, 맨틀 6371–3480, 외핵 3480–1220, 내핵 1220 km)
import os, re
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '../../../content/통합과학1_미래엔/3-1-1_지구시스템의_구성과_상호작용/slides.html')
ATM = [(15, 0), (-56, 11), (-56, 20), (-2, 50), (-86, 85), (-60, 95), (20, 110)]
LAY = [(0, 11, '대류권', '#DDEEF8'), (11, 50, '성층권', '#E8F5EE'), (50, 85, '중간권', '#FFF7DB'), (85, 110, '열권', '#FCE8EA')]
def atm(x, y, w, h):
    x, y, w, h = map(float, (x, y, w, h))
    X = lambda t: x + (t + 100) / 140 * w; Y = lambda z: y + h - z / 110 * h
    out = []
    for z0, z1, n, c in LAY:
        out.append(f'<rect x="{x:.0f}" y="{Y(z1):.1f}" width="{w:.0f}" height="{Y(z0) - Y(z1):.1f}" fill="{c}"/>')
        out.append(f'<text class="tex" x="{x + w - 8:.0f}" y="{(Y(z0) + Y(z1)) / 2 + 7:.1f}" data-mix="{n}" data-size="18" data-anchor="end" data-weight="700"></text>')
    for z in (0, 20, 40, 60, 80, 100):
        out.append(f'<text class="tex" x="{x - 8:.0f}" y="{Y(z) + 6:.1f}" data-tex="{z}" data-size="16" data-anchor="end"></text>')
    for t in (-80, -40, 0, 40):
        out.append(f'<text class="tex" x="{X(t):.1f}" y="{y + h + 22:.0f}" data-tex="{t}" data-size="16" data-anchor="middle"></text>')
    out.append(f'<g data-arw="{x:.0f},{y + h:.0f},{x + w + 16:.0f},{y + h:.0f},muted,2.5"></g><g data-arw="{x:.0f},{y + h:.0f},{x:.0f},{y - 16:.0f},muted,2.5"></g>')
    out.append('<g data-anim="draw" data-dur="1.8"><polyline points="' + ' '.join(f'{X(t):.1f},{Y(z):.1f}' for t, z in ATM) + '" fill="none" stroke="#D7263D" stroke-width="3.5"/></g>')
    oz = Y(25)
    out.append(f'<rect x="{X(-100):.0f}" y="{oz - 6:.1f}" width="{w * 0.35:.0f}" height="12" rx="6" fill="#2E9E6A" opacity=".55"/>')
    out.append(f'<text class="tex" x="{X(-100) + 6:.0f}" y="{oz - 12:.1f}" data-mix="오존층" data-size="16" fill="#1D6B47"></text>')
    return ''.join(out)
SEA = [(20, 0), (20, 50), (17, 100), (10, 250), (6, 500), (4.5, 1000), (3, 2000)]
def sea(x, y, w, h):
    x, y, w, h = map(float, (x, y, w, h))
    X = lambda t: x + t / 25 * w
    def Y(d):  # 0–200 m를 넓게(위 40 %), 200–2000 m 압축
        return y + (d / 200 * 0.4 * h if d <= 200 else 0.4 * h + (d - 200) / 1800 * 0.6 * h)
    out = []
    for d0, d1, n, c in ((0, 50, '혼합층', '#F7D9A8'), (50, 1000, '수온 약층', '#BFE0F2'), (1000, 2000, '심해층', '#7FB3E6')):
        out.append(f'<rect x="{x:.0f}" y="{Y(d0):.1f}" width="{w:.0f}" height="{Y(d1) - Y(d0):.1f}" fill="{c}" opacity=".7"/>')
        out.append(f'<text class="tex" x="{x + w - 8:.0f}" y="{(Y(d0) + Y(d1)) / 2 + 7:.1f}" data-mix="{n}" data-size="18" data-anchor="end" data-weight="700"></text>')
    for d in (0, 200, 1000, 2000):
        out.append(f'<text class="tex" x="{x - 8:.0f}" y="{Y(d) + 6:.1f}" data-tex="{d}" data-size="16" data-anchor="end"></text>')
    for t in (0, 5, 10, 15, 20, 25):
        out.append(f'<text class="tex" x="{X(t):.1f}" y="{y - 10:.0f}" data-tex="{t}" data-size="16" data-anchor="middle"></text>')
    out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + w:.0f}" y2="{y:.0f}" stroke="#5B6B7F" stroke-width="2.5"/><line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{y + h:.0f}" stroke="#5B6B7F" stroke-width="2.5"/>')
    out.append('<g data-anim="draw" data-dur="1.8"><polyline points="' + ' '.join(f'{X(t):.1f},{Y(d):.1f}' for t, d in SEA) + '" fill="none" stroke="#D7263D" stroke-width="3.5"/></g>')
    return ''.join(out)
def earth(cx, cy, R):
    cx, cy, R = map(float, (cx, cy, R))
    r = lambda km: R * km / 6371
    out = [f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R:.1f}" fill="#8C6A4F"/>',
           f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R - 6:.1f}" fill="#E08A2C"/>',
           f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r(3480):.1f}" fill="#F7C548"/>',
           f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r(1220):.1f}" fill="#FDF1C4" stroke="#C2410C" stroke-width="1.5"/>']
    return ''.join(out)
s = open(os.path.join(H, 'slides.src.html'), encoding='utf-8').read()
s = re.sub(r'\{ATM\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: atm(*m.groups()), s)
s = re.sub(r'\{SEA\|([^|]*)\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: sea(*m.groups()), s)
s = re.sub(r'\{EARTH\|([^|]*)\|([^|]*)\|([^}]*)\}', lambda m: earth(*m.groups()), s)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(s); print('written', len(s))
