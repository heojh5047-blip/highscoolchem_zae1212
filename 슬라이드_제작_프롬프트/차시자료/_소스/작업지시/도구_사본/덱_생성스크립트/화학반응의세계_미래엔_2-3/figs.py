# 2-3 화학 전지의 원리 — 그림 도우미 (viewBox 0 0 560 370 두 비커 전지)
MET = {  # 칠, 테
  'Zn': ('#C9D3DD', '#7E8B98'), 'Cu': ('#E6C29C', '#B0835A'), 'Mg': ('#EEF1F4', '#9AA5B1'),
  'Fe': ('#8C8F94', '#5B6B7F'), 'Ag': ('#DDE1E6', '#8C99A6'), 'Pt': ('#B8BEC6', '#7E8B98'),
  'A': ('#E6C29C', '#B0835A'), 'B': ('#AEB8C2', '#7E8B98'), 'X': ('#AEB8C2', '#7E8B98'),
}
SOL = {'w': ('#DDEEF8', 1), 'cu': ('#3E8ED0', .3), 'fe': ('#9CCB8A', .4)}

SC=[1.0]
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

def sol(x0, x1, kind, top=160, bot=298):
    c, o = SOL[kind]
    return f'<rect x="{x0+2}" y="{top}" width="{x1-x0-4}" height="{bot-top}" fill="{c}" fill-opacity="{o}"/>'

def plate(cx, m, top=90, h=180, w=28):
    f, s = MET[m]
    return f'<rect x="{cx-w//2}" y="{top}" width="{w}" height="{h}" rx="3" fill="{f}" stroke="{s}" stroke-width="2"/>'

def cell(Lm, Rm, Ltex, Rtex, Lsol, Rsol, Lsk='w', Rsk='w', e='r', dev='V', poles=True, extra='', flow=True,
         bridge=True, elab=True, devlabel=None):
    """L 비커 40–230 (전극 중심 124), R 비커 330–520 (전극 중심 424). e='r'이면 전자 L→R (L이 (−)극)."""
    o = []
    parts = '[["wire",[[124,90],[124,50],[262,50]]],["wire",[[298,50],[424,50],[424,90]]],'
    parts += '["meter",[280,50],"V",{"r":18}]]' if dev == 'V' else '["bulb",[280,50],{"r":18,"on":true}]]'
    o.append(f"<g data-circuit='{{\"parts\":{parts},\"stroke\":3}}'></g>")
    o.append(beaker(40, 230)); o.append(beaker(330, 520))
    o.append(sol(40, 230, Lsk)); o.append(sol(330, 520, Rsk))
    if bridge:
        o.append('<path d="M190 250 V112 H370 V250" fill="none" stroke="#B9A98A" stroke-width="24"/>')
        o.append('<path d="M190 250 V112 H370 V250" fill="none" stroke="#F6F0E0" stroke-width="18"/>')
        o.append(T(280, 150, mix='염다리', size=18, fill='#5B6B7F'))
    o.append(plate(124, Lm)); o.append(plate(424, Rm))
    if flow:
        d = 'M124 90 V50 H262 M298 50 H424 V90' if e == 'r' else 'M424 90 V50 H298 M262 50 H124 V90'
        o.append(f'<path d="{d}" fill="none" stroke="#1F6FD1" stroke-width="4" stroke-dasharray="3 15" stroke-linecap="round" data-anim="dash" data-flow data-speed="36"/>')
    if elab:
        if e == 'r':
            o.append('<g data-arw="160,30,232,30,minus,3"></g><g data-arw="328,30,400,30,minus,3"></g>')
        else:
            o.append('<g data-arw="232,30,160,30,minus,3"></g><g data-arw="400,30,328,30,minus,3"></g>')
        ey = round(22 + (SC[0]-1)*30); o.append(T(196, ey, tex='e^-', size=20, fill='#1F6FD1')); o.append(T(364, ey, tex='e^-', size=20, fill='#1F6FD1'))
    o.append(T(104, 112, tex=Ltex, size=20, anchor='end')); o.append(T(446, 112, tex=Rtex, size=20, anchor='start'))
    o.append(T(135, 290, tex=Lsol, size=18)); o.append(T(425, 290, tex=Rsol, size=18))
    if poles:
        neg, pos = (135, 425) if e == 'r' else (425, 135)
        o.append(T(neg, 328, mix='(−)극', size=20, weight=700)); o.append(T(neg, 354, mix='산화 전극', size=19, weight=700, fill='#C2410C'))
        o.append(T(pos, 328, mix='(+)극', size=20, weight=700)); o.append(T(pos, 354, mix='환원 전극', size=19, weight=700, fill='#0E7490'))
    o.append(extra)
    return ''.join(o)
