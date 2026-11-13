# 2차시 교구 관리 틀(_교구_공통틀/slides.tpl.html)에 그림 넣기 → gen_gugu.py로 고등·중등 생성. 여러 번 실행해도 결과가 같다.
import os, re, sys, subprocess
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from figs import *
T = os.path.join(os.path.dirname(H), '_교구_공통틀')
P = os.path.join(T, 'slides.tpl.html')
s = open(P, encoding='utf-8').read()
def tx(x, y, t, size=20, anchor='start', weight=None, fill=None):
    w = f' data-weight="{weight}"' if weight else ''; f = f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{x}" y="{y}" data-mix="{t}" data-size="{size}" data-anchor="{anchor}"{w}{f}></text>'
def replace_slide(s, title, new):
    parts = re.split(r'(?=\n<section )', s)
    for i, x in enumerate(parts):
        if f'data-title="{title}"' in x: parts[i] = '\n' + new.strip() + '\n'; return ''.join(parts)
    raise SystemExit('장 없음: ' + title)

# ── 과학실 배치 예시(평면도) ──
def mark(x, y, n, col):
    return f'<circle cx="{x}" cy="{y}" r="14" fill="{col}"/>' + tx(x, y+7, n, 18, 'middle', '800', '#fff')
fp = ['<svg class="fig" viewBox="0 0 620 356" style="width:560px" aria-label="과학실 설비 배치 예시 평면도">',
      '<rect x="10" y="10" width="440" height="340" fill="#fff" stroke="#16233D" stroke-width="4"/>',
      '<rect x="450" y="10" width="160" height="340" fill="#F4F5F7" stroke="#16233D" stroke-width="4"/>',
      tx(530, 40, '준비실', 20, 'middle', '700'),
      '<rect x="120" y="16" width="220" height="12" fill="#5B6B7F"/>', tx(230, 50, '칠판', 18, 'middle', fill=MUTED),
      '<rect x="170" y="62" width="120" height="34" rx="4" fill="#E8F1FB" stroke="#16233D" stroke-width="2"/>', tx(230, 85, '교사용 실험대', 18, 'middle')]
for i in range(3):
    for j in range(2):
        x, y = 60 + i * 130, 140 + j * 100
        fp.append(f'<rect x="{x}" y="{y}" width="96" height="56" rx="4" fill="#fff" stroke="#16233D" stroke-width="2"/>')
        fp.append(f'<rect x="{x+100}" y="{y+18}" width="12" height="22" rx="3" fill="{PLUS}"/>')
fp += ['<rect x="16" y="150" width="22" height="140" fill="#E8F1FB" stroke="#16233D" stroke-width="2"/>', tx(46, 300, '싱크대', 18),
       '<rect x="356" y="306" width="88" height="40" fill="#FFF1E0" stroke="#16233D" stroke-width="2"/>', tx(400, 332, '흄후드', 18, 'middle'),
       '<path d="M10 330 h0" />', '<rect x="4" y="60" width="12" height="44" fill="#fff" stroke="#16233D" stroke-width="2"/>', tx(22, 52, '출입문', 18),
       '<rect x="470" y="70" width="120" height="70" rx="4" fill="#fff" stroke="#16233D" stroke-width="2"/>', tx(530, 112, '밀폐 시약장', 18, 'middle'),
       '<rect x="470" y="170" width="120" height="70" rx="4" fill="#fff" stroke="#16233D" stroke-width="2"/>', tx(530, 212, '폐수 보관함', 18, 'middle'),
       '<rect x="462" y="60" width="16" height="16" fill="#E08A2C"/>',
       mark(350, 22, '1', EQUI), mark(132, 168, '2', PLUS), mark(54, 132, '3', MINUS), mark(30, 84, '4', PLUS), mark(400, 290, '5', MUTED), mark(560, 290, '6', EQUI),
       '</svg>']
legend = [('1', 'equi', '콘센트 전원 비상 차단 스위치 — 칠판 근처'), ('2', 'plus', '간이 소화기 — 실험대 주위, 실험실당 4'),
          ('3', 'minus', '눈세척기 — 안내표지 포함, 학교당 1'), ('4', 'plus', 'ABC 소화기·소화용 모래'),
          ('5', 'muted', '흄후드 — 학교당 1'), ('6', 'equi', '준비실 이중 잠금(문 + 보관함)')]
lg = ''.join(f'<li><span class="PFXdot" style="background:var(--{c})">{n}</span>{t}</li>' for n, c, t in legend)
SAFE = f'''<section class="slide" data-sec="03 · 필수 교구" data-title="필수 ① 설비와 안전">
  <h2><span class="no">7</span>필수 ① 설비와 안전 — 95% 목표의 대상</h2>
  <div class="row">
    <div class="col" style="flex:0 0 560px">{''.join(fp)}</div>
    <div class="col">
      <ul class="PFXlegend">{lg}</ul>
      <div class="card" style="margin-top:10px"><p class="f21"><b>개인 보호구</b> 학생당 1: 장갑·마스크·방독 마스크·보안경·레이저 보안경·면 실험복 · PPEEXTRA</p></div>
    </div>
  </div>
  <div class="row" style="margin-top:10px">
    <div class="col note">그 밖의 필수: 자동화재탐지설비, 환풍기, 구급함, 금속 쓰레기통, 흡착포, 폐수통 4종 · 권장: 비상샤워기 등</div>
    NOTEEXTRA
  </div>
  <p class="small PFXsrc">출처: 원고 초안 제2부 Ⅲ-1 · 평면도는 예시 배치(크기 비례 아님)</p>
</section>'''
s = replace_slide(s, '필수 ① 설비와 안전', SAFE)

# ── 디지털 도구 모둠 세트 그림 (측정·디지털 장의 왼쪽 메모 자리) ──
kit = ('<svg class="fig" viewBox="0 0 260 120" style="width:260px;flex:0 0 260px" aria-label="센서·충전기·케이블을 한 상자에 묶은 모둠 세트 예시">'
       '<rect x="6" y="20" width="248" height="94" rx="10" fill="#fff" stroke="#16233D" stroke-width="3"/>'
       '<rect x="186" y="6" width="62" height="28" rx="6" fill="#1F6FD1"/>' + tx(217, 27, '세트 3', 17, 'middle', '800', '#fff') +
       '<g transform="translate(14 40) scale(.9)" fill="none" stroke="#16233D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' + '<rect x="12" y="10" width="22" height="20" rx="4" fill="#E8F1FB"/><path d="M23 30 V54"/>' + '</g>'
       '<g transform="translate(74 40) scale(.9)" fill="none" stroke="#16233D" stroke-width="3" stroke-linecap="round"><path d="M8 20 C28 0 40 40 60 20 S 90 40 96 20"/></g>'
       '<g transform="translate(176 46)" fill="none" stroke="#16233D" stroke-width="3" stroke-linejoin="round"><rect x="4" y="10" width="40" height="30" rx="5" fill="#fff"/><path d="M14 10 V2 M34 10 V2"/></g>'
       + tx(36, 106, '센서', 16, 'middle') + tx(118, 106, '케이블', 16, 'middle') + tx(200, 106, '충전기', 16, 'middle') + '</svg>')
s = s.replace('<div class="col note">센서 규격은 <b>유선 또는 무선</b> — 학교가 고를 수 있습니다. 무선은 배터리 충전·보관 관리가 따릅니다(1차시 Ⅸ).</div>',
              f'<div class="col" style="display:flex;gap:12px;align-items:center">{kit}<p class="f21">센서는 <b>유선 또는 무선</b>. 센서·충전기·케이블을 <b>모둠 세트</b>로 묶고 번호 라벨 <span class="PFXflag">제안</span></p></div>')

# ── 교구 라벨 예시 (구입~불용 장의 Tip 자리) ──
tag = ('<svg class="fig" viewBox="0 0 330 124" style="width:330px;flex:0 0 330px" aria-label="교구장 라벨 예시">'
       '<rect x="4" y="4" width="322" height="116" rx="8" fill="#fff" stroke="#16233D" stroke-width="3"/><rect x="4" y="4" width="322" height="30" rx="8" fill="#1F6FD1"/><rect x="4" y="24" width="322" height="10" fill="#1F6FD1"/>'
       + tx(18, 26, '과학 교구 · 예시', 17, weight='800', fill='#fff') + tx(312, 26, '교구장 B-2', 16, 'end', fill='#fff')
       + tx(18, 60, '품명  디지털 온도계', 18, weight='700') + tx(18, 86, '규격  -50~150 ℃ · 수량 7', 17) + tx(18, 110, '취득 2026 · 대출 기록: 교구 목록', 17, fill=MUTED) + '</svg>')
s = s.replace('<div class="note puzzle" style="margin-top:14px"><b>Tip</b> 불용 신청은 연말에 몰지 말고 <b>4월 보유 현황 조사 전에</b> — 현황과 실제가 일치합니다. 세부 절차·서식은 행정실에 확인하세요.</div>',
              f'<div class="row" style="margin-top:12px;align-items:center">{tag}<div class="col note puzzle"><b>Tip</b> 불용 신청은 연말에 몰지 말고 <b>4월 보유 현황 조사 전에</b> — 현황과 실제가 일치합니다. 라벨 항목(품명·규격·수량·취득 연도)이 그대로 불용 목록이 됩니다. 세부 절차·서식은 행정실에 확인하세요.</div></div>')
open(P, 'w', encoding='utf-8').write(s)

css = open(os.path.join(T, 'extra.tpl.css'), encoding='utf-8').read().split('/* ── 그림 ── */')[0].rstrip()
css += '''
/* ── 그림 ── */
.PFXlegend{list-style:none;padding:0;margin:0}
.PFXlegend li{font-size:19px;line-height:1.4;margin-top:4px;padding-left:38px;text-indent:-38px}
.slide table.PFXcompact td,.slide table.PFXcompact th{padding:7px 12px}
.PFXdot{display:inline-block;width:26px;height:26px;line-height:26px;border-radius:50%;color:#fff;font-size:15px;font-weight:800;text-align:center;margin-right:12px;text-indent:0}
'''
open(os.path.join(T, 'extra.tpl.css'), 'w', encoding='utf-8').write(css + '\n')
subprocess.run([sys.executable, '-I', os.path.join(T, 'gen_gugu.py')], check=True)
