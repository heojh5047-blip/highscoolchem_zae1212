# ── 교과서 대조 후 추가·교체 그림 ──
def c_rocket():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#1E2A44"/>'
    o += '<path d="M150 20 q18 22 18 60 v34 h-36 v-34 q0 -38 18 -60 z" fill="#EEF3F8" stroke="#9AA5B1" stroke-width="2"/>'
    o += '<circle cx="150" cy="66" r="8" fill="#6EC1E4" stroke="#9AA5B1" stroke-width="2"/>'
    o += '<path d="M132 92 l-14 26 h14 z M168 92 l14 26 h-14 z" fill="#D7263D"/>'
    o += '<g data-anim="scale" data-from="1,.3" data-o="150,114" data-dur=".5" data-rep="alt" data-ease="io"><path d="M136 114 q14 54 14 50 q0 4 14 -50 z" fill="#F2C230"/><path d="M142 114 q8 34 8 32 q0 2 8 -32 z" fill="#E08A2C"/></g>'
    return o
def c_banana():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<path d="M60 70 q90 80 190 -10 q-10 40 -60 52 q-80 14 -136 -36 z" fill="#F2D64B" stroke="#C9A93A" stroke-width="2.5"/>'
    o += '<rect x="244" y="48" width="12" height="18" rx="3" fill="#6B5B3A" transform="rotate(30 250 57)"/>'
    spots = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .7}" fill="#6B4A2B" opacity=".85"/>' for (x, y, r) in ((100, 98, 6), (130, 112, 5), (160, 114, 7), (190, 106, 5), (215, 92, 6), (145, 100, 4)))
    o += f'<g data-anim="fade" data-dur="2" data-delay=".4">{spots}</g>'
    return o
def c_bronze():
    o = '<rect x="4" y="4" width="292" height="162" rx="12" fill="#EEF3F8"/>'
    o += '<path d="M150 22 q-50 0 -56 70 l-14 40 h140 l-14 -40 q-6 -70 -56 -70 z" fill="#B87333" stroke="#7A4A20" stroke-width="2.5"/>'
    o += '<rect x="140" y="12" width="20" height="12" rx="3" fill="#7A4A20"/><circle cx="150" cy="140" r="9" fill="#7A4A20"/>'
    spots = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#4FA38A" opacity=".85"/>' for (x, y, rx, ry) in ((122, 70, 12, 8), (170, 58, 9, 6), (178, 100, 14, 8), (118, 112, 10, 6), (150, 124, 22, 5)))
    o += f'<g data-anim="fade" data-dur="2.2" data-delay=".4">{spots}</g>'
    return o
F['c_rocket'] = c_rocket(); F['c_banana'] = c_banana(); F['c_bronze'] = c_bronze()

def s_readB():
    A = Axes(80, 270, 400, 220, (0, 1), (0, 1))
    o = A.frame(grid=False, xl='시간', yl='$[\\ce{B}]$')
    fn = lambda t: 0.92 * (1 - math.exp(-2.6 * t))
    o += f'<path d="{A.path(fn, 0, 1)}" fill="none" stroke="{FIELD}" stroke-width="4"/>'
    t1, t2 = 0.25, 0.6
    b1, b2 = fn(t1), fn(t2)
    for t, b in ((t1, b1), (t2, b2)):
        o += f'<line x1="{f(A.X(t))}" y1="{f(A.y0)}" x2="{f(A.X(t))}" y2="{f(A.Y(b))}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>'
        o += f'<line x1="{f(A.x0)}" y1="{f(A.Y(b))}" x2="{f(A.X(t))}" y2="{f(A.Y(b))}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    o += tex(A.X(t1), A.y0 + 26, 't_1', 20, 'middle', INK, mix=False) + tex(A.X(t2), A.y0 + 26, 't_2', 20, 'middle', INK, mix=False)
    o += tex(A.x0 - 10, A.Y(b1) + 7, '[\\ce{B}]_1', 20, 'end', INK, mix=False) + tex(A.x0 - 10, A.Y(b2) + 7, '[\\ce{B}]_2', 20, 'end', INK, mix=False)
    o += '<g class="step" data-g="rb1">' + A.line(t1 - .1, b1 - .1 * (b2 - b1) / (t2 - t1), t2 + .12, b2 + .12 * (b2 - b1) / (t2 - t1), MUTED, 3, '7 5') + A.dot(t1, b1, INK, 5, '#fff') + A.dot(t2, b2, INK, 5, '#fff') + '</g>'
    o += tex(A.X(.66), A.Y(.4), '생성물 $\\ce{B}$', 21, 'start', FIELD)
    return o
F['readB'] = s_readB()

def _app(liq, inj):
    o = flask(50, 48, 100, 96, liq=liq)
    o += '<path d="M108 60 h44 V70 H196" fill="none" stroke="#7E8B98" stroke-width="3"/>'
    o += '<rect x="196" y="58" width="52" height="30" rx="6" fill="#16233D"/><rect x="202" y="64" width="40" height="12" rx="2" fill="#9BD86F"/>'
    o += '<rect x="88" y="38" width="24" height="12" rx="3" fill="#5B6B7F"/>'
    o += '<rect x="94" y="28" width="12" height="10" fill="#C9D3DD" stroke="#7E8B98" stroke-width="2"/><line x1="86" y1="33" x2="94" y2="33" stroke="#7E8B98" stroke-width="3"/>'
    o += '<rect x="92" y="4" width="16" height="24" fill="%s" stroke="#7E8B98" stroke-width="2"/>' % ('#fff' if inj else '#DDEEF8')
    if inj:
        o += '<g data-anim="move" data-from="0,-14" data-dur="1.2" data-delay=".3" data-ease="out"><rect x="96" y="2" width="8" height="22" fill="#5B6B7F"/></g>'
    else:
        o += '<rect x="96" y="-2" width="8" height="8" fill="#5B6B7F"/>'
    o += '<rect x="70" y="134" width="40" height="5" rx="2" fill="#9AA5B1"/>'
    return o
def p1m():
    return _app(0, False) + tex(222, 112, '압력 센서', 18, 'middle', MUTED) + tex(150, 28, '염산', 18, 'start', MUTED)
def p2m():
    return _app(.3, True) + bubbles([(80, 128), (90, 122), (74, 130)], dist=20) + tex(222, 112, '시간–압력', 18, 'middle', MUTED) + tex(222, 136, '자동 기록', 18, 'middle', MUTED)
def p3m():
    o = ''
    for i, c in enumerate(('0.10', '0.20', '0.30', '0.40')):
        x = 12 + i * 62
        o += beaker(x + 6, 40, 46, 70, .6)
        o += tex(x + 29, 138, c, 21, 'middle', INK, mix=False)
    o += tex(130, 26, '[\\ce{HCl}]_0\\ (\\text{mol/L})', 21, 'middle', MUTED, mix=False)
    return o
F['p1'] = p1m(); F['p2'] = p2m(); F['p3'] = p3m()
