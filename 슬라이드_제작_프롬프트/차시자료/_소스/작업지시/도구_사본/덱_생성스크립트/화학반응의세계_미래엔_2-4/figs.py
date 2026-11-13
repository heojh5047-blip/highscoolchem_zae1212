# 2-4 전기 분해 — 그림 도우미 (2-3 figs.py의 T·beaker·plate를 이어 씀)
MET = {  # 칠, 테
  'Zn': ('#C9D3DD', '#7E8B98'), 'Cu': ('#E6C29C', '#B0835A'), 'Ag': ('#DDE1E6', '#8C99A6'),
  'Fe': ('#8C8F94', '#5B6B7F'), 'C': ('#4A4F57', '#16233D'), 'Pt': ('#B8BEC6', '#7E8B98'),
}
SOL = {'w': ('#DDEEF8', 1), 'cu': ('#3E8ED0', .3), 'melt': ('#F6E7C8', 1), 'cry': ('#F9DDB0', 1)}
OX, RD, MINUS, PLUS, MUTED, INK = '#C2410C', '#0E7490', '#1F6FD1', '#D7263D', '#5B6B7F', '#16233D'
SC = [1.0]

def T(x, y, tex=None, mix=None, size=20, anchor='middle', fill=None, weight=None, halo=False, extra=''):
    a = f'<text class="tex" x="{x}" y="{y}"'
    a += f' data-tex="{tex}"' if tex is not None else f' data-mix="{mix}"'
    a += f' data-size="{round(size*SC[0])}" data-anchor="{anchor}"'
    if weight: a += f' data-weight="{weight}"'
    if halo: a += ' data-halo="1"'
    if fill: a += f' fill="{fill}"'
    return a + f'{extra}></text>'

def beaker(x0, x1, top=120, bot=300):
    return (f'<path d="M{x0-6} {top} H{x0} V{bot-10} Q{x0} {bot} {x0+10} {bot} H{x1-10} Q{x1} {bot} {x1} {bot-10} V{top} H{x1+6}" '
            f'fill="none" stroke="#7E8B98" stroke-width="3" stroke-linejoin="round"/>')

def sol(x0, x1, kind, top=150, bot=298):
    c, o = SOL[kind]
    return f'<rect x="{x0+2}" y="{top}" width="{x1-x0-4}" height="{bot-top}" fill="{c}" fill-opacity="{o}"/>'

def plate(cx, m, top=88, h=180, w=28, specks=False):
    f, s = MET[m]
    o = f'<rect x="{cx-w//2}" y="{top}" width="{w}" height="{h}" rx="3" fill="{f}" stroke="{s}" stroke-width="2"/>'
    if specks:
        for dx, dy in [(-6, 40), (5, 70), (-4, 104), (6, 132), (-7, 160), (3, 22)]:
            o += f'<circle cx="{cx+dx}" cy="{top+dy}" r="2.6" fill="#5B4636"/>'
    return o

def bubbles(x, ys, kind='h', side=1, anim=True, on=''):
    f, s = ('#E8F2B8', '#8FAE3A') if kind == 'cl' else ('#FFFFFF', '#7FA8C9')
    o = f'<g data-anim="move" data-from="0,36" data-dur="1.8" data-rep="loop"{on}>' if anim else '<g>'
    for i, y in enumerate(ys):
        r = [6, 5, 7, 5, 6][i % 5]
        o += f'<circle cx="{x + side*(r+2) + (i%2)*side*4}" cy="{y}" r="{r}" fill="{f}" stroke="{s}" stroke-width="2"/>'
    return o + '</g>'

def ion(x, y, sign, tex, ly=None, lx=None, size=18, fill=None, halo=True):
    ly = y - 16 if ly is None else ly
    lx = x if lx is None else lx
    return f'<g data-chg="{x},{y},10,{sign}"></g>' + T(lx, ly, tex=tex, size=size, fill=fill, halo=halo)

def ecell(plus='L', xL=170, xR=390, x0=60, x1=500, solk='w', Lel='', Rel='', dev='bat', poles=True, rdox=True,
          flow=True, elab=True, extra='', top=120, bot=300, soltop=150, wire=50, eltop=88, solid_beaker=None):
    """전기 분해 장치(viewBox 560×370): 전원 장치(가운데 위, 긴 판 = (+)) + 비커 + 두 전극.
       plus='L'이면 왼쪽 전극이 (+)극(산화 전극). 전자: (+)극 → 전원 (+)단자, 전원 (−)단자 → (−)극."""
    o = []
    if dev == 'bat':
        pos = 'left' if plus == 'L' else 'right'
        parts = f'[["wire",[[{xL},{eltop}],[{xL},{wire}],[272,{wire}]]],["wire",[[288,{wire}],[{xR},{wire}],[{xR},{eltop}]]],["bat",[280,{wire}],{{"dir":"h","pos":"{pos}","signs":true}}]]'
    else:
        parts = f'[["wire",[[{xL},{eltop}],[{xL},{wire}],[262,{wire}]]],["wire",[[298,{wire}],[{xR},{wire}],[{xR},{eltop}]]],["bulb",[280,{wire}],{{"r":18,"on":true}}]]'
    o.append(f"<g data-circuit='{{\"parts\":{parts},\"stroke\":3}}'></g>")
    o.append(solid_beaker if solid_beaker else beaker(x0, x1, top, bot))
    if not solid_beaker: o.append(sol(x0, x1, solk, soltop, bot - 2))
    o.append(Lel); o.append(Rel)
    if flow:
        gap = (262, 298) if dev != 'bat' else (272, 288)
        right = (plus == 'L') if dev == 'bat' else (plus != 'L')  # 화학 전지(dev=bulb): plus는 (+)극 쪽 → 전자는 반대쪽에서 옴
        d = f'M{xL} {eltop} V{wire} H{gap[0]} M{gap[1]} {wire} H{xR} V{eltop}' if right else f'M{xR} {eltop} V{wire} H{gap[1]} M{gap[0]} {wire} H{xL} V{eltop}'
        o.append(f'<path d="{d}" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>')
    if elab:
        right = (plus == 'L') if dev == 'bat' else (plus != 'L')
        a1, a2 = ((xL + 30, 236), (310, xR - 30))
        if right:
            o.append(f'<g data-arw="{a1[0]},30,{a1[1]},30,minus,3"></g><g data-arw="{a2[0]},30,{a2[1]},30,minus,3"></g>')
        else:
            o.append(f'<g data-arw="{a1[1]},30,{a1[0]},30,minus,3"></g><g data-arw="{a2[1]},30,{a2[0]},30,minus,3"></g>')
        ey = round(22 + (SC[0]-1)*26)
        o.append(T((a1[0]+a1[1])//2, ey, tex='e^-', size=20, fill=MINUS)); o.append(T((a2[0]+a2[1])//2, ey, tex='e^-', size=20, fill=MINUS))
    if poles:
        py = bot + round(28*SC[0]) - (6 if SC[0] > 1.2 else 0)
        pL, pR = (('(+)극', '산화 전극', OX), ('(−)극', '환원 전극', RD)) if plus == 'L' else (('(−)극', '환원 전극', RD), ('(+)극', '산화 전극', OX))
        if dev != 'bat':  # 화학 전지: (−)극 = 산화 전극
            pL, pR = (('(+)극', '환원 전극', RD), ('(−)극', '산화 전극', OX)) if plus == 'L' else (('(−)극', '산화 전극', OX), ('(+)극', '환원 전극', RD))
        for x, (p, n, c) in ((xL, pL), (xR, pR)):
            o.append(T(x, py, mix=p, size=20, weight=700))
            if rdox: o.append(T(x, py + round(26*SC[0]), mix=n, size=19, weight=700, fill=c))
    o.append(extra)
    return ''.join(o)

def pendant(cx, cy, r=24, coat=False, step=''):
    o = f'<line x1="{cx}" y1="88" x2="{cx}" y2="{cy-r}" stroke="#5B6B7F" stroke-width="3"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#D9925E" stroke="#A0623A" stroke-width="2.5"/>'
    o += f'<circle cx="{cx}" cy="{cy-r+5}" r="3" fill="#FFFFFF" stroke="#A0623A" stroke-width="1.5"/>'
    if coat:
        o += f'<g{step}><g data-anim="fade" data-dur="1.6"{" data-on=\"step\"" if step else ""}><circle cx="{cx}" cy="{cy}" r="{r+1}" fill="#E4E8EC" stroke="#8C99A6" stroke-width="3"/></g></g>'
    return o
