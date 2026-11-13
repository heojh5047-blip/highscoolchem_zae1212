# 4-2-2 중화 적정 덱 그림 생성 — python3 -I gen.py <출력 slides.html>
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *

FIG = {}
PINK_L, PINK_LS = '#F6C3D9', '#E79BBE'
PINK, PINK_S = '#E04A8B', '#B8326C'
STAND = '#5B6B7F'
SPEC = {'H': ('P', '\\ce{H+}', '#FFFFFF', 19), 'OH': ('M', '\\ce{OH-}', '#FFFFFF', 19),
        'Na': ('N', '\\ce{Na+}', INK, 19), 'Cl': ('N', '\\ce{Cl-}', INK, 19),
        'SO4': ('N', '\\ce{SO4^2-}', INK, 23)}


def svg(vb, w, label, body, extra='', cls='fig'):
    c = f' class="{cls}"' if cls else ''
    st = f' style="width:{w}px"' if w else ''
    return f'<svg{c} viewBox="{vb}"{st} aria-label="{label}"{extra}>{body}</svg>'


def ion(x, y, k):
    t, lab, c, r = SPEC[k]
    return f'<g data-chg="{f(x)},{f(y)},{r},{t}"></g>' + tex(x, y + 18 * 0.36, lab, size=18, fill=c, weight=700)


def h2o(x, y):
    o = [atom(x, y - 4, 14, 'O', '-')]
    for a in (90 - 55, 90 + 55):
        hx, hy = pol(x, y - 4, 18, a)
        o.append(atom(hx, hy, 10, 'H', '-'))
    return ''.join(o)


def part(x, y, k):
    return h2o(x, y) if k == 'W' else ion(x, y, k)


# ───── 기구 ─────
def erlen_geom(cx, base, H, W, nw, nh):
    top = base - H
    sh = top + nh            # 어깨(목 끝)
    def hw(y):
        if y <= sh:
            return nw / 2
        return nw / 2 + (W / 2 - nw / 2) * (y - sh) / (base - 8 - sh)
    return top, sh, hw


def erlen(cx, base, H=150, W=180, nw=32, nh=30, level=None, color=WATER, stroke=WATER_S, liq_anim='', spot=None):
    top, sh, hw = erlen_geom(cx, base, H, W, nw, nh)
    o = []
    if level is not None:
        a = hw(level)
        o.append(f'<g {liq_anim}><path d="M{f(cx-a+1.5)},{f(level)} L{f(cx-W/2+3)},{f(base-8)} Q{f(cx-W/2+3)},{f(base-1.5)} {f(cx-W/2+10)},{f(base-1.5)} '
                 f'L{f(cx+W/2-10)},{f(base-1.5)} Q{f(cx+W/2-3)},{f(base-1.5)} {f(cx+W/2-3)},{f(base-8)} L{f(cx+a-1.5)},{f(level)} Z" fill="{color}"/>'
                 f'<line x1="{f(cx-a+1.5)}" y1="{f(level)}" x2="{f(cx+a-1.5)}" y2="{f(level)}" stroke="{stroke}" stroke-width="2"/></g>')
    if spot:
        o.append(spot)
    o.append(f'<path d="M{f(cx-nw/2-3)},{f(top)} L{f(cx-nw/2)},{f(top+4)} L{f(cx-nw/2)},{f(sh)} L{f(cx-W/2)},{f(base-8)} Q{f(cx-W/2)},{f(base)} {f(cx-W/2+8)},{f(base)} '
             f'L{f(cx+W/2-8)},{f(base)} Q{f(cx+W/2)},{f(base)} {f(cx+W/2)},{f(base-8)} L{f(cx+nw/2)},{f(sh)} L{f(cx+nw/2)},{f(top+4)} L{f(cx+nw/2+3)},{f(top)}" '
             f'fill="none" stroke="{GLASS}" stroke-width="2.6" stroke-linejoin="round"/>')
    return ''.join(o)


def burette(x, top, y0, y50, stop, tip, level=None, w=14, nums=True, nsize=18, color=WATER, stroke=WATER_S, liq_anim='', minor=True,
            numside='left', drop=None):
    """위가 0 눈금인 뷰렛. y0 = 0 mL 눈금, y50 = 50 mL 눈금, stop = 꼭지 중심, tip = 끝."""
    o = []
    ppm = (y50 - y0) / 50
    if level is not None:
        yl = y0 + level * ppm
        o.append(f'<g {liq_anim}><rect x="{f(x-w/2+1.5)}" y="{f(yl)}" width="{f(w-3)}" height="{f(stop-8-yl)}" fill="{color}"/>'
                 f'<path d="M{f(x-w/2+5)},{f(yl+2)} Q{f(x)},{f(yl+6)} {f(x+w/2-5)},{f(yl+2)}" fill="none" stroke="{stroke}" stroke-width="2"/></g>'
                 f'<rect x="{f(x-2)}" y="{f(stop+6)}" width="4" height="{f(tip-stop-12)}" fill="{color}"/>')
    # 관
    o.append(f'<path d="M{f(x-w/2)},{f(top)} L{f(x-w/2)},{f(stop-8)} M{f(x+w/2)},{f(top)} L{f(x+w/2)},{f(stop-8)}" fill="none" stroke="{GLASS}" stroke-width="2.4"/>')
    # 눈금
    for v in range(0, 51, 1 if minor else 5):
        y = y0 + v * ppm
        L = 9 if v % 10 == 0 else (6 if v % 5 == 0 else 3.5)
        if v % 10 != 0 and not minor and v % 5:
            continue
        o.append(f'<line x1="{f(x-w/2)}" y1="{f(y)}" x2="{f(x-w/2+L)}" y2="{f(y)}" stroke="{INK if v == 0 else MUTED}" stroke-width="{1.6 if v % 10 == 0 else 1.1}"/>')
        if nums and v % 10 == 0:
            if numside == 'left':
                o.append(tex(x - w / 2 - 6, y + nsize * 0.35, str(v), size=nsize, anchor='end', fill=INK if v == 0 else MUTED, weight=700 if v == 0 else None))
            else:
                o.append(tex(x + w / 2 + 6, y + nsize * 0.35, str(v), size=nsize, anchor='start', fill=INK if v == 0 else MUTED, weight=700 if v == 0 else None))
    # 꼭지
    o.append(f'<path d="M{f(x-w/2)},{f(stop-8)} L{f(x-4)},{f(stop-4)} L{f(x-4)},{f(stop+6)} L{f(x-2.5)},{f(tip)} L{f(x+2.5)},{f(tip)} L{f(x+4)},{f(stop+6)} L{f(x+4)},{f(stop-4)} L{f(x+w/2)},{f(stop-8)}" fill="none" stroke="{GLASS}" stroke-width="2.2" stroke-linejoin="round"/>')
    o.append(f'<rect x="{f(x-9)}" y="{f(stop-5)}" width="18" height="10" rx="3" fill="#E9EEF3" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<rect x="{f(x+9)}" y="{f(stop-3.5)}" width="14" height="7" rx="2" fill="{MINUS}"/>')
    if drop:
        o.append(drop)
    return ''.join(o)


def droplet(x, y, color='#9FC3DD', r=4.5, anim=''):
    d = f'<path d="M{f(x)},{f(y-r*1.8)} Q{f(x+r)},{f(y-r*.3)} {f(x+r)},{f(y)} A{f(r)},{f(r)} 0 0 1 {f(x-r)},{f(y)} Q{f(x-r)},{f(y-r*.3)} {f(x)},{f(y-r*1.8)} Z" fill="{color}" stroke="{WATER_S}" stroke-width="1.2"/>'
    return f'<g {anim}>{d}</g>' if anim else d


def stand(xr, yb, top, xb0, xb1, clamp_y, bx):
    o = [f'<rect x="{f(xb0)}" y="{f(yb)}" width="{f(xb1-xb0)}" height="10" rx="2" fill="{STAND}"/>',
         f'<rect x="{f(xr-3.5)}" y="{f(top)}" width="7" height="{f(yb-top)}" fill="#8C99A6" stroke="{STAND}" stroke-width="1.2"/>']
    # 뷰렛 집게
    o.append(f'<rect x="{f(xr-8)}" y="{f(clamp_y-9)}" width="16" height="18" rx="3" fill="#C9D3DD" stroke="{STAND}" stroke-width="1.5"/>')
    x2 = bx - 12 if bx > xr else bx + 12
    o.append(f'<line x1="{f(xr)}" y1="{f(clamp_y)}" x2="{f(x2)}" y2="{f(clamp_y)}" stroke="{STAND}" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<path d="M{f(bx-13)},{f(clamp_y-9)} L{f(bx-9)},{f(clamp_y)} L{f(bx-13)},{f(clamp_y+9)} M{f(bx+13)},{f(clamp_y-9)} L{f(bx+9)},{f(clamp_y)} L{f(bx+13)},{f(clamp_y+9)}" fill="none" stroke="{STAND}" stroke-width="3" stroke-linecap="round"/>')
    return ''.join(o)


def paper(cx, y, w):
    return f'<path d="M{f(cx-w/2)},{f(y+8)} L{f(cx-w/2+16)},{f(y)} L{f(cx+w/2+16)},{f(y)} L{f(cx+w/2)},{f(y+8)} Z" fill="#FFFFFF" stroke="{GRAV}" stroke-width="1.5"/>'


def pipette(cx, top, bottom, by, brx=10, bry=34, mark=None, level=None, color=WATER, filler=True, liq_anim=''):
    o = []
    if level is not None:
        o.append(f'<g {liq_anim}><rect x="{f(cx-2)}" y="{f(level)}" width="4" height="{f(by-bry-level)}" fill="{color}"/>'
                 f'<ellipse cx="{f(cx)}" cy="{f(by)}" rx="{f(brx-1.5)}" ry="{f(bry-1.5)}" fill="{color}"/></g>'
                 f'<rect x="{f(cx-2)}" y="{f(by+bry-2)}" width="4" height="{f(bottom-by-bry-2)}" fill="{color}"/>')
    o.append(f'<path d="M{f(cx-3.5)},{f(top)} L{f(cx-3.5)},{f(by-bry+2)} M{f(cx+3.5)},{f(top)} L{f(cx+3.5)},{f(by-bry+2)} '
             f'M{f(cx-3.5)},{f(by+bry-2)} L{f(cx-3.5)},{f(bottom-12)} L{f(cx-1.2)},{f(bottom)} M{f(cx+3.5)},{f(by+bry-2)} L{f(cx+3.5)},{f(bottom-12)} L{f(cx+1.2)},{f(bottom)}" fill="none" stroke="{GLASS}" stroke-width="2.2"/>')
    o.append(f'<ellipse cx="{f(cx)}" cy="{f(by)}" rx="{f(brx)}" ry="{f(bry)}" fill="none" stroke="{GLASS}" stroke-width="2.4"/>')
    if mark is not None:
        o.append(f'<line x1="{f(cx-8)}" y1="{f(mark)}" x2="{f(cx+8)}" y2="{f(mark)}" stroke="{INK}" stroke-width="2"/>')
    if filler:
        o.append(f'<ellipse cx="{f(cx)}" cy="{f(top-16)}" rx="15" ry="15" fill="#B9C3CD" stroke="{STAND}" stroke-width="2"/>'
                 f'<rect x="{f(cx-5)}" y="{f(top-3)}" width="10" height="12" rx="2" fill="#B9C3CD" stroke="{STAND}" stroke-width="1.5"/>')
    return ''.join(o)


def cylinder(cx, base, h, w=34, level=None, color=WATER):
    top = base - h
    o = []
    if level is not None:
        o.append(f'<rect x="{f(cx-w/2+1.5)}" y="{f(level)}" width="{f(w-3)}" height="{f(base-10-level)}" fill="{color}"/>')
    o.append(f'<path d="M{f(cx-w/2-4)},{f(top-3)} L{f(cx-w/2)},{f(top+3)} L{f(cx-w/2)},{f(base-10)} M{f(cx+w/2)},{f(top+3)} L{f(cx+w/2)},{f(base-10)}" fill="none" stroke="{GLASS}" stroke-width="2.4"/>')
    o.append(f'<path d="M{f(cx-w/2-14)},{f(base)} L{f(cx-w/2)},{f(base-10)} L{f(cx+w/2)},{f(base-10)} L{f(cx+w/2+14)},{f(base)} Z" fill="#E9EEF3" stroke="{GLASS}" stroke-width="2.2"/>')
    for i in range(1, 11):
        y = base - 10 - (h - 24) * i / 10
        o.append(f'<line x1="{f(cx-w/2)}" y1="{f(y)}" x2="{f(cx-w/2+(10 if i % 5 == 0 else 6))}" y2="{f(y)}" stroke="{MUTED}" stroke-width="1.3"/>')
    return ''.join(o)


def vflask(cx, base, cid, s=1.0, filled=True, mark_label=None, color=WATER, stopper=True):
    cy = base - 60 * s * 0.86
    mark = cy - 100 * s
    body, cy, mark, tp = flask(cx, base, cid, level=mark if filled else None, R=60, neck=20, s=s, color=color, stopper=stopper, mark_label=mark_label)
    return body, mark


def glass_cup(cx, base, w, h, color, edge, level):
    """주스 잔(사다리꼴)."""
    top = base - h
    def hx(y):
        return w / 2 - (w * 0.12) * (base - y) / h
    o = [f'<path d="M{f(cx-hx(level)+2)},{f(level)} L{f(cx-w*0.38+2)},{f(base-2)} L{f(cx+w*0.38-2)},{f(base-2)} L{f(cx+hx(level)-2)},{f(level)} Z" fill="{color}"/>',
         f'<line x1="{f(cx-hx(level)+2)}" y1="{f(level)}" x2="{f(cx+hx(level)-2)}" y2="{f(level)}" stroke="{edge}" stroke-width="2"/>',
         f'<path d="M{f(cx-w/2)},{f(top)} L{f(cx-w*0.38)},{f(base)} L{f(cx+w*0.38)},{f(base)} L{f(cx+w/2)},{f(top)}" fill="none" stroke="{GLASS}" stroke-width="2.6" stroke-linejoin="round"/>']
    return ''.join(o)


def bottle(cx, base, h=230, w=90, label_mix=None, fill='#F4E7B5', anim=''):
    top = base - h
    o = [f'<path d="M{f(cx-w/2)},{f(base-10)} L{f(cx-w/2)},{f(top+90)} Q{f(cx-w/2)},{f(top+60)} {f(cx-14)},{f(top+40)} L{f(cx-14)},{f(top+12)} '
         f'L{f(cx+14)},{f(top+12)} L{f(cx+14)},{f(top+40)} Q{f(cx+w/2)},{f(top+60)} {f(cx+w/2)},{f(top+90)} L{f(cx+w/2)},{f(base-10)} Q{f(cx+w/2)},{f(base)} {f(cx+w/2-10)},{f(base)} '
         f'L{f(cx-w/2+10)},{f(base)} Q{f(cx-w/2)},{f(base)} {f(cx-w/2)},{f(base-10)} Z" fill="{fill}" stroke="{GLASS}" stroke-width="2.4"/>',
         f'<rect x="{f(cx-17)}" y="{f(top)}" width="34" height="16" rx="3" fill="#E8B23A" stroke="#B9862A" stroke-width="2"/>',
         f'<rect x="{f(cx-w/2+6)}" y="{f(top+105)}" width="{f(w-12)}" height="82" rx="5" fill="#FFFFFF" stroke="{FIELD}" stroke-width="2"/>']
    if label_mix:
        o.append(tex(cx, top + 140, mix=label_mix, size=20, weight=700))
    s = ''.join(o)
    return f'<g {anim}>{s}</g>' if anim else s


# ───── 1 표지 ─────
def cover():
    o = ['<circle cx="270" cy="270" r="250" fill="#EEF3F8"/>']
    o.append(stand(150, 470, 40, 90, 420, 110, 270))
    o.append(paper(270, 470, 230))
    o.append(burette(270, 40, 64, 314, 340, 372, level=11, w=20, nsize=22, minor=False, numside='right'))
    o.append(stand(150, 470, 40, 90, 420, 110, 270)[0:0])
    o.append(erlen(270, 466, H=118, W=190, nw=34, nh=26, level=420, color=PINK_L, stroke=PINK_LS,
                   liq_anim='data-anim="fade" data-dur="1.4" data-delay="1.2"'))
    o.append(droplet(270, 392, anim='data-anim="move" data-from="0,-14" data-dur=".9" data-rep="loop" data-ease="in"'))
    o.append(tex(326, 92, mix='뷰렛', size=24, anchor='start', weight=700))
    o.append(tex(374, 410, mix='삼각||플라스크', size=22, anchor='start', weight=700))
    return svg('0 0 540 540', None, '스탠드에 고정한 뷰렛에서 삼각 플라스크로 표준 용액을 떨어뜨리고, 플라스크 속 용액이 연붉은색으로 변한 중화 적정 장치', ''.join(o),
               ' data-audit="skip"', cls='cover-fig')
FIG['cover'] = cover()


# ───── 3 생각 열기: 주스 ─────
def juices():
    o = []
    data = [(110, '#F5A623', '#D9861A', '오렌지주스'), (300, '#F4E27A', '#D2BE4E', '레몬주스'), (490, '#F3A3A0', '#D97C78', '자몽주스')]
    for i, (cx, c, e, nm) in enumerate(data):
        g = glass_cup(cx, 210, 120, 150, c, e, 92)
        o.append(f'<g data-anim="pop" data-o="{cx},210" data-dur=".6" data-delay="{.2+.25*i:.2f}" data-ease="back">{g}</g>')
        o.append(tex(cx, 246, mix=nm, size=21, weight=700))
    o.append(tex(300, 30, mix='모두 신맛 — 수소 이온의 농도는?', size=22, weight=700, fill=PLUS))
    return svg('0 0 600 260', 560, '오렌지주스, 레몬주스, 자몽주스가 담긴 잔 세 개', ''.join(o))
FIG['juice'] = juices()


# ───── 5 중화 적정 도식 ─────
def setup_small():
    o = [stand(60, 400, 20, 30, 270, 70, 160), paper(160, 400, 170)]
    o.append(burette(160, 20, 40, 230, 252, 280, level=8, w=16, nsize=19, minor=False, numside='right'))
    o.append(erlen(160, 396, H=96, W=150, nw=28, nh=22, level=356, color=WATER))
    o.append(droplet(160, 300, anim='data-anim="move" data-from="0,-12" data-dur=".9" data-rep="loop" data-ease="in"'))
    o.append(tex(206, 116, mix='염기||표준 용액', size=21, anchor='start', weight=700, fill=MINUS))
    o.append(tex(206, 176, '(M^\\prime\\ \\text{아는 값})', size=20, anchor='start', fill=MINUS))
    o.append(tex(160, 438, mix='농도 모르는 산', size=21, anchor='middle', weight=700, fill=PLUS))
    o.append(tex(160, 464, '(V\\ \\text{아는 값})', size=20, anchor='middle', fill=PLUS))
    return svg('0 0 340 476', 320, '뷰렛에 염기 표준 용액, 삼각 플라스크에 농도를 모르는 산을 넣은 중화 적정 장치', ''.join(o))
FIG['setup_small'] = setup_small()


# ───── 6 페놀프탈레인 ─────
def php3():
    o = []
    items = [(95, WATER, WATER_S, '산성', '무색', PLUS), (285, WATER, WATER_S, '중성', '무색', GRAV), (475, PINK, PINK_S, '염기성', '붉은색', MINUS)]
    for i, (cx, c, e, k, col, kc) in enumerate(items):
        anim = 'data-anim="fade" data-dur="1.2" data-delay=".6"' if i == 2 else ''
        o.append(erlen(cx, 170, H=130, W=150, nw=30, nh=26, level=110, color=c, stroke=e, liq_anim=anim))
        o.append(tex(cx, 202, mix=k, size=21, weight=700, fill=kc))
        o.append(tex(cx, 228, mix=col, size=20, fill=MUTED if i < 2 else PINK_S, weight=700))
    return svg('0 0 570 236', 520, '페놀프탈레인 용액을 넣은 산성·중성 용액은 무색, 염기성 용액은 붉은색', ''.join(o))
FIG['php3'] = php3()


# ───── 7 기구 세 장 ─────
def tool_pipette():
    o = [pipette(150, 46, 228, 140, 12, 40, mark=72, level=72, filler=True)]
    o.append(tex(170, 77, mix='표시선', size=19, anchor='start', fill=INK, weight=700))
    o.append(tex(124, 36, mix='피펫 필러', size=19, anchor='end', fill=MUTED))
    o.append(arw(170, 70, 158, 72, 'muted', 2)[0:0])
    return svg('0 0 300 250', None, '피펫 필러를 끼운 피펫, 가운데가 부풀고 위쪽에 표시선 하나', ''.join(o), cls='')


def tool_vflask():
    body, mark = vflask(150, 236, 'clip-cm422-07')
    o = [body]
    o.append(tex(172, mark + 7, mix='표시선', size=19, anchor='start', fill=INK, weight=700))
    o.append(tex(150, 196, '100\\ \\text{mL}', size=19, fill=MUTED))
    return svg('0 0 300 250', None, '목에 표시선 하나가 있는 부피 플라스크', ''.join(o), cls='')


def tool_burette():
    o = [burette(150, 12, 30, 190, 210, 240, level=0, w=18, nsize=19, minor=True,
                 drop=droplet(150, 246, anim='data-anim="move" data-from="0,-8" data-dur=".9" data-rep="loop" data-ease="in"'))]
    o.append(tex(182, 36, mix='0 눈금이 위', size=19, anchor='start', fill=INK, weight=700))
    o.append(tex(184, 216, mix='꼭지', size=19, anchor='start', fill=MINUS, weight=700))
    return svg('0 0 300 252', None, '위가 0 눈금이고 아래로 갈수록 눈금이 커지는 뷰렛과 꼭지', ''.join(o), cls='')
FIG['tool_pip'] = tool_pipette(); FIG['tool_vf'] = tool_vflask(); FIG['tool_bu'] = tool_burette()


# ───── 8 그림 IV-9 단계 카드 ─────
def titr_card(i):
    o = [paper(150, 318, 210)]
    lv = [10, 18, 21][i]
    o.append(burette(150, -60, -40, 110, 122, 146, level=lv, w=16, nums=False, minor=False))
    flask_c = [WATER, WATER, PINK_L][i]; flask_e = [WATER_S, WATER_S, PINK_LS][i]
    spot = ''
    if i == 1:
        spot = (f'<g data-anim="fade" data-dur=".4" data-delay=".9" data-on="step"><ellipse cx="150" cy="232" rx="34" ry="10" fill="{PINK}" opacity=".55"/></g>')
    anim = 'data-anim="fade" data-dur="1.2" data-delay=".6" data-on="step"' if i == 2 else ''
    o.append(erlen(150, 314, H=160, W=230, nw=34, nh=28, level=224, color=flask_c, stroke=flask_e, liq_anim=anim, spot=spot))
    kinds = [['H', 'Cl', 'H', 'Cl'], ['Cl', 'W', 'Na', 'Cl', 'H'], ['Cl', 'W', 'Na', 'Cl', 'Na', 'W']][i]
    pts = [(96, 292), (150, 292), (204, 292), (124, 252), (176, 252), (150, 252)]
    pts = [(92, 292), (134, 292), (176, 292), (218, 292), (126, 252), (174, 252)] if i else [(100, 290), (150, 290), (200, 290), (150, 252)]
    if i == 0:
        pts = [(105, 292), (155, 292), (205, 292), (155, 252)]
    for k, (x, y) in zip(kinds, pts):
        o.append(part(x, y, k))
    if i:
        o.append(droplet(150, 160, anim='data-anim="move" data-from="0,-14" data-dur=".9" data-rep="loop" data-ease="in"'))
    return svg('0 0 300 330', None, ['염산에 페놀프탈레인을 넣은 무색 용액, 수소 이온 2개와 염화 이온 2개',
                                     '수산화 나트륨 표준 용액을 떨어뜨리면 떨어진 자리가 붉어졌다가 흔들면 없어진다. 수소 이온 1개가 물이 됨',
                                     '혼합 용액 전체가 연붉은색으로 변하는 순간, 수소 이온이 모두 물이 됨'][i], ''.join(o), cls='')
for i in range(3):
    FIG[f'titr{i}'] = titr_card(i)


# ───── 9 뷰렛 눈금 읽기 확대 창 ─────
def zoom(x0, y0, w, h, center, reading, title, cid, anim=''):
    """center: 창 가운데 눈금(mL). reading: 액면 눈금."""
    ppm = 46        # 1 mL = 46 px
    cx = x0 + w / 2
    o = [f'<defs><clipPath id="{cid}"><rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10"/></clipPath></defs>',
         f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10" fill="#FFFFFF"/>']
    g = []
    tw = 70
    yl = y0 + h / 2 + (reading - center) * ppm
    g.append(f'<g {anim}><rect x="{f(cx-tw/2)}" y="{f(yl)}" width="{tw}" height="{f(h)}" fill="{WATER}"/>'
             f'<path d="M{f(cx-tw/2)},{f(yl-9)} Q{f(cx-tw/2+8)},{f(yl)} {f(cx)},{f(yl)} Q{f(cx+tw/2-8)},{f(yl)} {f(cx+tw/2)},{f(yl-9)}" fill="{WATER}" stroke="{WATER_S}" stroke-width="2.4"/></g>')
    g.append(f'<path d="M{f(cx-tw/2)},{f(y0)} L{f(cx-tw/2)},{f(y0+h)} M{f(cx+tw/2)},{f(y0)} L{f(cx+tw/2)},{f(y0+h)}" stroke="{GLASS}" stroke-width="2.6"/>')
    v = math.floor((center - 3) * 10)
    while v <= (center + 3) * 10:
        y = y0 + h / 2 + (v / 10 - center) * ppm
        if y0 + 4 < y < y0 + h - 4 and v >= 0:
            L = 34 if v % 10 == 0 else (24 if v % 5 == 0 else 14)
            g.append(f'<line x1="{f(cx-tw/2)}" y1="{f(y)}" x2="{f(cx-tw/2+L)}" y2="{f(y)}" stroke="{INK if v % 10 == 0 else MUTED}" stroke-width="{2 if v % 10 == 0 else 1.3}"/>')
            if v % 10 == 0 and y0 + 14 < y < y0 + h - 14:
                g.append(tex(cx - tw / 2 - 8, y + 7, str(v // 10), size=20, anchor='end', weight=700))
        v += 1
    o.append(f'<g clip-path="url(#{cid})">{"".join(g)}</g>')
    o.append(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(w)}" height="{f(h)}" rx="10" fill="none" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<line x1="{f(cx-tw/2-4)}" y1="{f(yl)}" x2="{f(x0+w+18)}" y2="{f(yl)}" stroke="{PLUS}" stroke-width="2" stroke-dasharray="5 4"/>')
    o.append(tex(x0 + w / 2, y0 - 12, mix=title, size=21, weight=700))
    return ''.join(o), yl


def read2():
    a, ya = zoom(40, 40, 180, 230, 0.6, 0.50, '처음 눈금', 'clip-cm422-09a')
    b, yb = zoom(330, 40, 180, 230, 20.5, 20.55, '나중 눈금', 'clip-cm422-09b', anim='data-anim="move" data-from="0,-40" data-dur="1.4" data-delay=".4" data-ease="out"')
    o = [a, b]
    o.append(tex(240, ya + 7, '0.50', size=21, anchor='start', weight=700, fill=PLUS, halo=True))
    o.append(tex(530, yb + 7, '20.55', size=21, anchor='start', weight=700, fill=PLUS, halo=True))
    o.append(arw(232, 250, 312, 250, 'muted', 3))
    o.append(tex(272, 238, mix='적정', size=19, fill=MUTED))
    return svg('0 0 600 290', 600, '뷰렛 확대 창: 처음 눈금 0.50 mL, 나중 눈금 20.55 mL, 메니스커스 아랫부분을 읽는다', ''.join(o))
FIG['read2'] = read2()


# ───── 13 장치 그림 (라벨) ─────
def setup_big(labels=True, vb_w=420, title_set=None):
    o = [stand(80, 500, 20, 40, 330, 90, 210), paper(210, 500, 200)]
    o.append(burette(210, 20, 44, 314, 340, 372, level=6, w=18, nsize=23, minor=False, numside='right'))
    o.append(erlen(210, 496, H=110, W=170, nw=30, nh=24, level=456, color=WATER))
    o.append(droplet(210, 390, anim='data-anim="move" data-from="0,-12" data-dur=".9" data-rep="loop" data-ease="in"'))
    if labels:
        for (x, y, t, c, a) in [(262, 100, '뷰렛', INK, 'start'), (140, 74, '뷰렛 집게', INK, 'middle'), (262, 348, '꼭지', MINUS, 'start'),
                             (300, 430, '삼각||플라스크', INK, 'start'), (330, 524, '흰 종이', MUTED, 'start'), (72, 300, '스탠드', MUTED, 'end')]:
            o.append(tex(x, y, mix=t, size=23, anchor=a, weight=700, fill=c, halo=True))
    return o


def setup_label():
    return svg('0 0 420 530', 380, '스탠드, 뷰렛 집게, 뷰렛, 꼭지, 삼각 플라스크, 흰 종이로 꾸민 중화 적정 장치', ''.join(setup_big()))
FIG['setup'] = setup_label()


def setup_map():
    o = setup_big(labels=False)
    o.append(tex(262, 120, mix='농도를 알고||있는 염기(산)||표준 용액', size=24, anchor='start', weight=700))
    o.append(tex(282, 410, mix='농도를 모르는||산(염기)||+ 지시약', size=24, anchor='start', weight=700))
    return svg('0 0 440 530', 340, '뷰렛에 농도를 알고 있는 표준 용액, 삼각 플라스크에 농도를 모르는 용액과 지시약', ''.join(o))
FIG['setup_map'] = setup_map()


# ───── 15·16 실험 과정 카드 ─────
def step1():
    body, mark = vflask(190, 236, 'clip-cm422-15a')
    o = [body]
    o.append(f'<g data-anim="move" data-from="0,-20" data-dur="1" data-ease="out">{pipette(80, 40, 200, 120, 10, 34, mark=62, level=62, color="#F4EBC4", filler=True)}</g>')
    o.append(tex(80, 236, mix='식초 10.0 mL', size=19, weight=700))
    o.append(tex(212, mark + 7, mix='표시선', size=19, anchor='start', weight=700))
    o.append(tex(190, 196, '100\\ \\text{mL}', size=19, fill=MUTED))
    return svg('0 0 300 250', None, '피펫으로 식초 10.0 mL를 100 mL 부피 플라스크에 넣고 표시선까지 증류수를 채운다', ''.join(o), cls='')


def step2():
    o = [erlen(190, 236, H=130, W=170, nw=30, nh=24, level=196, color=WATER)]
    o.append(f'<g data-anim="move" data-from="0,-20" data-dur="1" data-ease="out">{pipette(56, 40, 190, 116, 10, 34, mark=62, level=62, color=WATER, filler=True)}</g>')
    # 스포이트(페놀프탈레인)
    o.append(f'<path d="M232,40 L232,84 L236,98 L240,84 L240,40 Z" fill="#FFFFFF" stroke="{GLASS}" stroke-width="2"/><rect x="229" y="22" width="14" height="20" rx="6" fill="#B9C3CD" stroke="{STAND}" stroke-width="1.5"/>')
    o.append(droplet(236, 116, anim='data-anim="move" data-from="0,-12" data-dur=".9" data-rep="loop" data-ease="in"'))
    o.append(tex(56, 218, mix='묽힌 식초||10.0 mL', size=19, weight=700))
    o.append(tex(250, 64, mix='페놀프탈레인', size=19, anchor='start', weight=700)[0:0])
    return svg('0 0 300 250', None, '피펫으로 묽힌 식초 10.0 mL를 삼각 플라스크에 옮기고 페놀프탈레인 용액을 2–3 방울 넣는다', ''.join(o), cls='')


def step3():
    o = [burette(150, 40, 60, 160, 176, 200, level=-3, w=16, nums=False, minor=False)]
    # 깔때기
    o.append(f'<path d="M126,14 L174,14 L156,36 L156,50 L144,50 L144,36 Z" fill="none" stroke="{GLASS}" stroke-width="2.2"/>')
    o.append(beaker(112, 246, 76, 40, 228))
    o.append(droplet(150, 214, anim='data-anim="move" data-from="0,-10" data-dur=".9" data-rep="loop" data-ease="in"'))
    o.append(tex(186, 30, mix='깔때기로 채움', size=19, anchor='start', weight=700))
    o.append(tex(186, 182, mix='꼭지 열어||공기 빼기', size=19, anchor='start', weight=700, fill=MINUS))
    o.append(tex(114, 100, mix='처음||눈금', size=19, anchor='end', weight=700, fill=PLUS))
    return svg('0 0 300 250', None, '뷰렛을 표준 용액으로 헹군 뒤 깔때기로 채우고 꼭지를 열어 끝의 공기를 뺀 다음 처음 눈금을 읽는다', ''.join(o), cls='')


def step4():
    spot = f'<g data-anim="fade" data-dur=".5" data-delay=".8" data-on="step"><ellipse cx="150" cy="200" rx="30" ry="8" fill="{PINK}" opacity=".5"/></g>'
    o = [paper(150, 240, 180), burette(150, -40, -20, 70, 84, 108, level=14, w=16, nums=False, minor=False)]
    o.append(erlen(150, 236, H=120, W=170, nw=30, nh=24, level=192, color=WATER, spot=spot))
    o.append(droplet(150, 122, anim='data-anim="move" data-from="0,-12" data-dur=".9" data-rep="loop" data-ease="in"'))
    o.append(f'<path d="M60,214 A92,22 0 0 0 240,214" fill="none" stroke="{MUTED}" stroke-width="2.4" stroke-dasharray="6 5"/>')
    o.append(arw(232, 222, 244, 210, 'muted', 2.4))
    o.append(tex(56, 160, mix='흔들며', size=19, anchor='middle', weight=700))
    return svg('0 0 300 250', None, '삼각 플라스크를 흔들면서 표준 용액을 떨어뜨린다. 떨어진 자리가 잠깐 붉어진다', ''.join(o), cls='')


def step5():
    o = [paper(110, 240, 150), erlen(110, 236, H=120, W=150, nw=28, nh=22, level=190, color=PINK_L, stroke=PINK_LS,
                                    liq_anim='data-anim="fade" data-dur="1.2" data-delay=".5" data-on="step"')]
    z, yl = zoom(196, 40, 90, 160, 20.5, 20.55, '', 'clip-cm422-16a')
    o.append(z.replace(tex(241, 28, mix='', size=21, weight=700), ''))
    o.append(tex(240, 228, mix='나중 눈금', size=19, weight=700, fill=PLUS))
    o.append(tex(110, 104, mix='연붉은색', size=19, weight=700, fill=PINK_S))
    return svg('0 0 300 250', None, '용액 전체가 연붉은색으로 변하면 멈추고 나중 눈금을 읽는다', ''.join(o), cls='')


def step6():
    o = []
    for i, cx in enumerate((58, 150, 242)):
        o.append(erlen(cx, 170, H=100, W=84, nw=20, nh=18, level=136, color=PINK_L, stroke=PINK_LS))
        o.append(tex(cx, 200, mix=f'{i+1}회', size=20, weight=700))
    o.append(tex(150, 240, 'V_\\text{평균}=\\dfrac{V_1+V_2+V_3}{3}', size=21))
    return svg('0 0 300 260', None, '같은 과정을 3회 반복하고 넣은 부피의 평균을 구한다', ''.join(o), cls='')
FIG['st1'] = step1(); FIG['st2'] = step2(); FIG['st3'] = step3(); FIG['st4'] = step4(); FIG['st5'] = step5(); FIG['st6'] = step6()


# ───── 20 식초병 ─────
FIG['vinegar'] = svg('0 0 200 280', 180, '총산도 6 %–7 %라고 표시된 식초병',
                     bottle(100, 270, h=250, w=110, label_mix='식초', anim='data-anim="pop" data-o="100,270" data-dur=".7" data-ease="back"')
                     + tex(100, 206, mix='총산도', size=19, fill=MUTED) + tex(100, 230, mix='6 %~7 %', size=19, weight=700, fill=PLUS))


# ───── 23 식초 A·B 비교 (뷰렛 두 개) ─────
def compare_ab():
    o = []
    for cx, used, nm in ((90, 11.1, '식초 A'), (250, 7.5, '식초 B')):
        o.append(burette(cx, 20, 34, 214, 230, 252, level=used, w=16, nsize=21, minor=False,
                         liq_anim=f'data-anim="move" data-from="0,{-used*3.6:.0f}" data-dur="1.6" data-delay=".3" data-ease="out" data-on="step"'))
        o.append(tex(cx, 284, mix=nm, size=20, weight=700))
        o.append(tex(cx + 18, 34 + used * 3.6 + 7, f'{used:.1f}', size=19, anchor='start', weight=700, fill=PLUS, halo=True))
    return svg('0 0 340 296', 300, '같은 부피의 식초 A와 B를 적정하면 식초 A에 표준 용액이 11.1 mL, B에 7.5 mL 들어간다', ''.join(o))
FIG['ab'] = compare_ab()


# ───── 24 과학 수사 ─────
def forensic():
    o = []
    for i, x in enumerate((40, 76, 112, 148)):
        c = ['#F6C3D9', '#DDEEF8', '#F4E27A', '#BFE3B4'][i]
        o.append(f'<rect x="{x}" y="{110 - (i % 2) * 8}" width="24" height="70" rx="12" fill="{c}" stroke="{GLASS}" stroke-width="2"/>')
    o.append(f'<rect x="28" y="168" width="156" height="18" rx="4" fill="#C9D3DD" stroke="{STAND}" stroke-width="1.5"/>')
    o.append(f'<circle cx="214" cy="84" r="40" fill="#EEF3F8" stroke="{INK}" stroke-width="5"/><line x1="242" y1="112" x2="276" y2="148" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    return svg('0 0 300 200', 260, '시료가 든 시험관과 돋보기', ''.join(o))
FIG['forensic'] = forensic()


# ───── 25 중단원 마무리 06 ─────
def q06():
    o = [beaker(40, 250, 220, 200, 90)]
    pts = [('Na', 90, 130), ('H', 170, 126), ('H', 120, 182), ('SO4', 206, 182), ('SO4', 92, 226), ('Na', 196, 232)]
    for i, (k, x, y) in enumerate(pts):
        o.append(f'<g data-anim="pop" data-o="{x},{y}" data-dur=".5" data-delay="{.2+.12*i:.2f}" data-ease="back">{ion(x, y, k)}</g>')
    return svg('0 0 300 262', 290, '혼합 용액 속 나트륨 이온 2개, 수소 이온 2개, 황산 이온 2개', ''.join(o))
FIG['q06'] = q06()


# ───── 26 중단원 마무리 07 ─────
def q07():
    o = []
    o.append(erlen(80, 220, H=140, W=120, nw=26, nh=26))
    body, mark = vflask(240, 220, 'clip-cm422-26', s=0.9, filled=False)
    o.append(body)
    o.append(cylinder(390, 220, 190, w=36))
    o.append(burette(530, 26, 40, 176, 190, 214, level=None, w=12, nums=False, minor=False))
    for x, t in ((80, '(가)'), (240, '(나)'), (390, '(다)'), (530, '(라)')):
        o.append(tex(x, 254, mix=t, size=21, weight=700))
    return svg('0 0 620 266', 600, '(가) 삼각 플라스크, (나) 부피 플라스크, (다) 눈금실린더, (라) 뷰렛', ''.join(o))
FIG['q07'] = q07()


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    out = re.sub(r'@@(\w+)@@', lambda m: FIG[m.group(1)], tpl)
    open(sys.argv[1], 'w', encoding='utf-8').write(out)
    print('wrote', sys.argv[1], len(out))
