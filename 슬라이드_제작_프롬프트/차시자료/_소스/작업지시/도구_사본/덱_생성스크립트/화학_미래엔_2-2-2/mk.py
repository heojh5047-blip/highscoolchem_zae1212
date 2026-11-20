# 교과서 재검토용 새 그림: BeCl2·BCl3 루이스 전자점식, 털실 철사 배치
import math, os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cm222_copy'))
from figs import *

S = 40
def sym(x, y, el):
    return f'<text class="tex" x="{f(x)}" y="{f(y + 0.36 * S)}" data-tex="\\mathrm{{{el}}}" data-size="{S}" data-anchor="middle"></text>'
def cl(x, y, sides):
    # Cl 기호(너비 약 40px) 둘레 전자점: 위·아래는 0.75S, 좌우는 30px
    pos = {'u': (x, y - 0.75 * S, 'h'), 'd': (x, y + 0.75 * S, 'h'), 'l': (x - 30, y, 'v'), 'r': (x + 30, y, 'v')}
    return sym(x, y, 'Cl') + ''.join(dot_pair(pos[s][0], pos[s][1], pos[s][2], 2, S) for s in sides)

out = {}
x, y = 230, 90
out['lw_becl2'] = (sym(x, y, 'Be') + dot_pair(x - 40, y, 'v') + dot_pair(x + 40, y, 'v')
                   + cl(x - 75, y, 'udl') + cl(x + 75, y, 'udr')
                   + hl_box(190, 90, 22, 34, 'shared', 'h9') + hl_box(270, 90, 22, 34, 'shared', 'h9'))
x, y = 230, 78
out['lw_bcl3'] = (sym(x, y, 'B') + dot_pair(x - 28, y, 'v') + dot_pair(x + 28, y, 'v') + dot_pair(x, y + 30, 'h')
                  + cl(x - 64, y, 'udl') + cl(x + 64, y, 'udr') + cl(x, y + 60, 'lrd')
                  + ''.join(hl_box(*p, 'shared', 'h10') for p in [(202, 78, 22, 34), (258, 78, 22, 34), (230, 108, 34, 22)]))

def wires(dirs, yaw=0, pitch=0, cx=150, cy=100, l=80):
    items, ends = [], []
    for d in dirs:
        v = rot(norm(d), yaw, pitch)
        ex, ey = cx + v[0] * l, cy - v[1] * l
        ends.append((ex, ey))
        col = '#C96A2B' if v[2] >= -0.1 else '#E3B28E'
        items.append((v[2], f'<line x1="{cx}" y1="{cy}" x2="{f(ex)}" y2="{f(ey)}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>'))
    items.sort()
    body = ''.join(s for _, s in items)
    seg = ''
    for i in range(len(ends)):
        for j in range(i + 1, len(ends)):
            if len(ends) == 3 or len(ends) == 4 or len(ends) == 2:
                a, b = ends[i], ends[j]
                seg += f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="#5B6B7F" stroke-width="2" stroke-dasharray="6 5"/>'
    return (f'<g data-anim="pop" data-o="{cx},{cy}" data-dur=".9" data-delay=".4" data-ease="back">{body}'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="#8A4A1C"/></g>'
            f'<g class="step" data-g="w4">{seg}</g>')
out['w2'] = wires([(-1, 0, 0), (1, 0, 0)], l=95)
out['w3'] = wires(angle_dirs(0, 3)[0], cy=110)
out['w4'] = wires(angle_dirs(0, 4)[0], yaw=20, pitch=-12, cy=110)

R['Y']=24; R['Z']=24
def best_view(nb, nl=0, ang=None, L=100):
    bd, ld = angle_dirs(nl, nb, ang)
    best = None
    for yaw in range(-60, 61, 3):
        for pitch in (-10, -14, -18, -22):
            pts = [(0, 0)] + [(rot(norm(d), yaw, pitch)[0] * L, rot(norm(d), yaw, pitch)[1] * L) for d in bd]
            m = min(math.hypot(p[0] - q[0], p[1] - q[1]) for i, p in enumerate(pts) for q in pts[i + 1:])
            if best is None or m > best[0]:
                best = (m, yaw, pitch)
    return best[1], best[2]
V31 = best_view(3, 1, 107)
# 05: Y:X:Y, 아래 Y, X 위에 비공유 전자쌍
x, y = 230, 70
out['lw_xy3'] = (lewis_sym(x, y, 'X', S, dots={'u': 2, 'l': 2, 'r': 2, 'd': 2})
                 + lewis_sym(x - 56, y, 'Y', S, dots={'u': 2, 'd': 2, 'l': 2})
                 + lewis_sym(x + 56, y, 'Y', S, dots={'u': 2, 'd': 2, 'r': 2})
                 + lewis_sym(x, y + 60, 'Y', S, dots={'l': 2, 'r': 2, 'd': 2}))
# 06: (가) 삼각뿔 X, (나) 평면 삼각형 Y, (다) 굽은 형 Z (비공유 전자쌍은 그리지 않음 — 교과서 그림처럼)
out['q06'] = (ballstick(100, 82, 'X', ['H'] * 3, n_lone=1, ang=107, L=96, yaw=V31[0], pitch=V31[1], lobes=False)
              + ballstick(300, 92, 'Y', ['H'] * 3, L=84)
              + ballstick(500, 80, 'Z', ['H'] * 2, n_lone=2, ang=104.5, L=90, lobes=False))
print('V31', V31)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figs_new.json'), 'w'), ensure_ascii=False)
print({k: len(v) for k, v in out.items()})
