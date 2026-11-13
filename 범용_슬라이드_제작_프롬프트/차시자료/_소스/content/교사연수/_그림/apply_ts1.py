# 1차시 덱에 그림 넣기 — slides.html의 해당 장(data-title)을 바꾸거나 새 장을 끼운다. 여러 번 실행해도 결과가 같다.
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figs import *
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '1_실험실_안전_교육')
P = os.path.join(D, 'slides.html')
s = open(P, encoding='utf-8').read()

def sections(s):
    return re.split(r'(?=\n<section )', s)
def replace_slide(s, title, new):
    parts = sections(s)
    for i, x in enumerate(parts):
        if f'data-title="{title}"' in x:
            parts[i] = '\n' + new.strip() + '\n'; return ''.join(parts)
    raise SystemExit('장 없음: ' + title)
def insert_after(s, title, new, newtitle):
    if f'data-title="{newtitle}"' in s: return replace_slide(s, newtitle, new)
    parts = sections(s)
    for i, x in enumerate(parts):
        if f'data-title="{title}"' in x:
            parts.insert(i + 1, '\n' + new.strip() + '\n'); return ''.join(parts)
    raise SystemExit('장 없음: ' + title)
def tx(x, y, t, size=20, anchor='start', weight=None, fill=None, extra=''):
    w = f' data-weight="{weight}"' if weight else ''; f = f' fill="{fill}"' if fill else ''
    return f'<text class="tex" x="{x}" y="{y}" data-mix="{t}" data-size="{size}" data-anchor="{anchor}"{w}{f}{extra}></text>'

# ── A. GHS 그림문자 9종 (새 장) ──
EX = {'01': '학교 과학실에서는 드묾', '02': '에탄올, 아세톤, 메탄올', '03': '과망가니즈산 칼륨, 질산 은',
      '04': '고압가스 용기(산소 등)', '05': '염산, 황산, 수산화나트륨', '06': '메탄올, 다이크로뮴산 칼륨',
      '07': '자극성 — 황산 구리(Ⅱ), 아세톤', '08': '발암성·장기 손상 — 메탄올 등', '09': '황산 구리(Ⅱ), 질산 은'}
cards = []
for k, c in enumerate(sorted(GHS_NAME)):
    svg = (f'<svg viewBox="0 0 100 100" width="84" height="84" role="img" aria-label="GHS 그림문자 {GHS_NAME[c]}" data-audit="skip">'
           f'<g data-anim="pop" data-o="50,50" data-delay="{k*0.08:.2f}" data-dur="0.5">{ghs_g(c)}</g></svg>')
    cards.append(f'<div class="ts1-ghs">{svg}<div><p class="nm">{GHS_NAME[c]} <span class="cd" data-audit="skip">GHS{c}</span></p><p class="ex">{EX[c]}</p></div></div>')
A = f'''<section class="slide" data-sec="05 · 화학물질 관리" data-title="GHS 그림문자 9종">
  <h2><span class="no">0</span>시약병의 그림문자 9종 — 빨간 마름모</h2>
  <div class="ts1-ghsgrid">
    {''.join(cards)}
  </div>
  <div class="note" style="margin-top:12px">예시는 대표적인 경우입니다. 같은 물질도 농도에 따라 달라지므로 <b>실제 표시는 제품의 경고표지와 MSDS 2항</b>으로 확인합니다.</div>
  <p class="small ts1-src">출처: GHS(화학물질 분류·표시 세계조화시스템) 그림문자 — 소방청 기준 그림과 대조해 다시 그림 · 고용노동부 고시 「화학물질의 분류·표시 및 물질안전보건자료에 관한 기준」 <span class="ts1-flag">확인</span>예시 물질</p>
</section>'''

# ── B. 경고표지 읽기 (새 장) — 가상 라벨 ──
lab = ['<svg class="fig" viewBox="0 0 600 400" style="width:600px" aria-label="가상 시약 경고표지 예시: 염산 35%">',
       '<rect x="6" y="6" width="588" height="388" rx="14" fill="#fff" stroke="#16233D" stroke-width="3"/>',
       tx(54, 56, '염산 35%', 34, weight='800'), tx(570, 52, '가상 라벨', 18, 'end', fill=MUTED),
       ghs_g('05', 50, 78, 0.92), ghs_g('07', 142, 78, 0.92),
       tx(262, 118, '위험', 34, weight='800', fill=PLUS),
       tx(262, 152, '신호어', 18, fill=MUTED),
       '<line x1="26" y1="186" x2="574" y2="186" stroke="#CFD8E1" stroke-width="2"/>',
       tx(54, 218, '유해·위험 문구', 18, weight='700', fill=MUTED),
       tx(54, 246, '피부에 심한 화상과 눈에 손상을 일으킴', 20), tx(54, 272, '호흡기 자극을 일으킬 수 있음', 20),
       tx(54, 306, '예방조치 문구', 18, weight='700', fill=MUTED),
       tx(54, 334, '보호장갑·보안경을 착용하시오 · 눈에 묻으면 물로 씻으시오', 19),
       '<rect x="6" y="350" width="588" height="44" fill="#F4F5F7"/>',
       tx(54, 379, '공급자: ○○화학 · 주소 · 긴급전화 000-0000-0000', 18, fill=MUTED)]
marks = [(26, 46, '1'), (26, 126, '2'), (244, 110, '3'), (26, 240, '4'), (26, 328, '5'), (26, 373, '6')]
for i, (x, y, n) in enumerate(marks):
    lab.append(f'<g class="step" data-g="w{n}"><circle cx="{x}" cy="{y}" r="14" fill="{MINUS}"/>{tx(x, y+7, n, 18, "middle", "800", "#fff")}</g>')
lab.append('</svg>')
items = ['<b>명칭</b> — 제품명(시약명·농도)', '<b>그림문자</b> — 빨간 마름모, 위험의 종류', '<b>신호어</b> — 「위험」 또는 「경고」',
         '<b>유해·위험 문구</b> — 어떤 해를 입히는가', '<b>예방조치 문구</b> — 보호구·응급조치', '<b>공급자 정보</b> — 회사·주소·긴급전화']
lis = ''.join(f'<li class="step" data-g="w{i+1}">{t}</li>' for i, t in enumerate(items))
B = f'''<section class="slide" data-sec="05 · 화학물질 관리" data-title="경고표지 읽기">
  <h2><span class="no">0</span>시약 라벨, 무엇을 읽어야 할까?</h2>
  <div class="row">
    <div class="col" style="flex:0 0 600px">{''.join(lab)}</div>
    <div class="col">
      <ol class="goals f21" style="margin-top:0">{lis}</ol>
      <div class="note" style="margin-top:12px">100 g(mL) 이하 소형 용기는 명칭·그림문자·신호어·공급자 정보만 표시할 수 있습니다. 없으면 <b>학교가 직접 부착</b>합니다.</div>
    </div>
  </div>
  <p class="small ts1-src">출처: 원고 초안 Ⅴ-4 경고표지와 라벨 · 라벨은 가상 예시(문구는 대표 문구 — 실제는 제품 경고표지·MSDS 2항)</p>
</section>'''

# ── C. 안전장구와 설비 — 아이콘 카드 ──
EQ = [('coat', '실험복', '완전 면 소재 — 합성섬유는 녹아 붙음'), ('glove', '보호장갑', '내열·내화학(나이트릴)·일반 장갑'),
      ('goggle', '보안경', '학생 수만큼'), ('mask', '마스크', '일반 + 방진(독) 마스크'),
      ('eyewash', '눈세척기', '흐르는 물 형태 권장, 용기형은 교체일 기록'), ('ext', '소화장구', '간이 소화기 실험대당 1개 이상, 모래함·소방포'),
      ('shower', '비상샤워기', '분출된 물의 배수구 설치 권장'), ('fan', '환기·전기', '재유입 방지 환풍기, 미사용 콘센트 커버')]
eq = ''.join(f'<div class="ts1-eq">{icon(n, 60)}<div><h3>{h}</h3><p>{t}</p></div></div>' for n, h, t in EQ)
C = f'''<section class="slide" data-sec="03 · 안전한 과학실 환경" data-title="안전장구와 설비">
  <h2><span class="no">0</span>환경 ③ 안전장구와 설비</h2>
  <div class="ts1-eqgrid">{eq}</div>
  <div class="row" style="margin-top:14px">
    <div class="col note puzzle"><b>쓰지 않는 것</b> 석면·수은이 든 설비·교구 — 석면 철망은 세라믹 철망으로 바꿉니다.</div>
    <div class="col note tip"><b>Tip</b> 장비 수량·보관 위치 표를 교직원 안전교육 자료에 넣으면 조례 제7조 '보관위치·사용법 교육'까지 충족합니다.</div>
  </div>
  <p class="small ts1-src">출처: 원고 초안 Ⅲ-3 안전장구와 설비 · 아이콘은 직접 그림</p>
</section>'''

# ── D. 판단 연습 — 서식4 표시 그림 ──
sign = ('<svg class="fig" viewBox="0 0 300 150" style="width:300px;flex:0 0 300px" aria-label="유해화학물질 표시 예시: 흰 바탕, 검은 테두리, 빨간 글씨">'
        '<rect x="4" y="4" width="292" height="142" fill="#fff" stroke="#000" stroke-width="6"/>'
        + tx(150, 62, '유해화학물질', 40, 'middle', '800', '#E3000F')
        + tx(24, 102, '관리책임자: ○○○', 19, fill='#000') + tx(24, 130, '비상전화: ○○○-○○○○', 19, fill='#000') + '</svg>')
s = s.replace('''  <div class="note" style="margin-top:18px">해당하면: 보관 장소에 '유해화학물질' 표시(서식4, 흰 바탕·검은 테두리·빨간 글씨, 관리책임자·비상전화) · 주 1회 이상 자체점검 · 극소량이라도 취급기준 준수 · 구매 시 기준함량 이하 제품 선택</div>''',
 f'''  <div class="row" style="margin-top:16px;align-items:center">{sign}<div class="col note"><b>해당하면</b> 보관 장소에 '유해화학물질' 표시(서식4) · 주 1회 이상 자체점검 · 극소량이라도 취급기준 준수 · 구매 시 기준함량 이하 제품 선택</div></div>''')

# ── E. 분리 보관 — 밀폐형 시약장 2개 ──
def cab(x, name, top, bot, ctop, cbot):
    return (f'<g><rect x="{x}" y="46" width="180" height="250" rx="8" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x+60}" y="22" width="60" height="24" fill="#F4F5F7" stroke="{INK}" stroke-width="2"/>'
            + tx(x+90, 16, '배기', 18, 'middle', fill=MUTED) +
            f'<rect x="{x+12}" y="60" width="156" height="104" rx="6" fill="{ctop}" opacity=".16"/><rect x="{x+12}" y="176" width="156" height="104" rx="6" fill="{cbot}" opacity=".16"/>'
            f'<line x1="{x}" y1="170" x2="{x+180}" y2="170" stroke="{INK}" stroke-width="3"/>'
            + tx(x+90, 120, top, 21, 'middle', '700', ctop) + tx(x+90, 236, bot, 21, 'middle', '700', cbot)
            + f'<rect x="{x+150}" y="160" width="16" height="20" rx="3" fill="{EQUI}"/>'
            + tx(x+90, 326, name, 21, 'middle', '700') + '</g>')
cabs = ('<svg class="fig" viewBox="0 -12 420 352" style="width:420px" aria-label="밀폐형 시약장 2개의 칸 나누기 예시">'
        + cab(20, 'A장', '산성', '무기 화합물', OX, MUTED) + cab(220, 'B장', '유기 화합물', '염기성·위험물', BF, RD) + '</svg>')
s = re.sub(r'(<section class="slide" data-sec="05 · 화학물질 관리" data-title="보관과 분리 보관">.*?</section>)',
 lambda m: f'''<section class="slide" data-sec="05 · 화학물질 관리" data-title="보관과 분리 보관">
  <h2><span class="no">0</span>보관 — 함께 두면 안 되는 것</h2>
  <div class="row">
    <div class="col">
      <table class="tight">
        <tr><th class="l">분류</th><th class="l">예</th><th class="l">분리할 물질</th></tr>
        <tr><td class="l">인화성 액체</td><td class="l">아세톤, 에탄올</td><td class="l">산화제, 산</td></tr>
        <tr><td class="l">유기산</td><td class="l">아세트산, 포름산</td><td class="l">무기산, 산화제, 인화성</td></tr>
        <tr><td class="l">무기산</td><td class="l">염산, 황산, 질산</td><td class="l">염기, 유기산, 인화성</td></tr>
        <tr><td class="l">염기</td><td class="l">수산화나트륨</td><td class="l">산</td></tr>
        <tr><td class="l">물반응성</td><td class="l">나트륨, 칼륨</td><td class="l">모든 수용액, 산화제</td></tr>
        <tr><td class="l">산화제</td><td class="l">과망가니즈산 칼륨</td><td class="l">환원제, 인화성, 유기물</td></tr>
      </table>
      <div class="note" style="margin-top:12px"><b>이중 잠금</b> 준비실 문 + 시약장(준비실이 없으면 시약장에 잠금장치 2개) · 부식성·인화성은 눈높이 아래</div>
    </div>
    <div class="col" style="flex:0 0 420px">{cabs}<p class="small" style="margin-top:2px">현장에서 널리 쓰는 칸 나누기 예(원고 Tip)</p></div>
  </div>
  <p class="small ts1-src">출처: 원고 초안 Ⅴ-3 보관, 분리 보관(혼합 보관 금지 조합) · 시약장 그림은 직접 그림</p>
</section>''', s, flags=re.S)

# ── F. 폐수 3단계 — 폐수통 4종 ──
def can(x, name, col, k):
    return (f'<g><path d="M{x} 40 h96 v108 a8 8 0 0 1 -8 8 h-80 a8 8 0 0 1 -8 -8 z" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x+30}" y="22" width="22" height="18" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M{x+62} 40 v-12 h24 v12" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<g data-anim="scale" data-from="1,0" data-o="{x+48},154" data-dur="1.2" data-delay="{k*0.15:.2f}" data-ease="out"><rect x="{x+4}" y="66" width="88" height="86" rx="4" fill="{col}" opacity=".55"/></g>'
            f'<line x1="{x-6}" y1="66" x2="{x+102}" y2="66" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>'
            + tx(x+48, 186, name, 21, 'middle', '700', col) + '</g>')
cans = ('<svg class="fig" viewBox="0 0 760 196" style="width:760px" aria-label="성상별 폐수통 4종과 80% 선">'
        + can(14, '유기계', BF, 0) + can(194, '산성', OX, 1) + can(374, '알칼리계', RD, 2) + can(554, '무기계', MUTED, 3)
        + tx(756, 72, '80%', 20, 'end', '800') + '</svg>')
s = re.sub(r'(<section class="slide" data-sec="06 · 폐수·폐기물 관리" data-title="폐수 3단계">.*?</section>)',
 lambda m: f'''<section class="slide" data-sec="06 · 폐수·폐기물 관리" data-title="폐수 3단계">
  <h2><span class="no">0</span>폐수는 한 방울도 싱크대에 버리지 않는다</h2>
  <div class="row" style="align-items:center">
    <div class="col" style="flex:0 0 760px">{cans}</div>
    <div class="col note"><b>4종 이상</b> 분리 · 내화학성 20L 용기 · <mark>80%까지만</mark> · 혼합 전 MSDS로 혼합금지 확인</div>
  </div>
  <div class="stages" style="margin-top:12px">
    <div class="stage" style="border-top:6px solid var(--minus)"><h3>① 수집</h3><p>깔때기로 천천히, 고형물 혼입 금지. 배출할 때마다 대장에 누계 기록</p></div>
    <div class="stage" style="border-top:6px solid var(--equi)"><h3>② 보관</h3><p>준비실 + 보관함 <b>이중 잠금</b>, 관리자·폐기물명 표시, 뚜껑은 항상 닫기, 매월 서식9</p></div>
    <div class="stage" style="border-top:6px solid var(--field)"><h3>③ 처리</h3><p>전량 위탁 — 초·중·소규모 고는 교육지원청 일괄, 대규모 고는 학교별. 확인서 <b>3년</b></p></div>
  </div>
  <p class="small ts1-src">출처: 원고 초안 Ⅵ-2 · 대규모 고 = 이화학실험실 100㎡ 이상이고 1일 폐수 100L 이상 · 책임은 학교장 · 처리비는 12월 예산 요구 때 반드시 편성</p>
</section>''', s, flags=re.S)

# ── G. 수은 — 포장 6단계 그림 ──
def step_card(k, title, body):
    x = 10 + k * 186
    return (f'<g data-anim="pop" data-o="{x+80},70" data-delay="{k*0.18:.2f}" data-dur="0.5"><rect x="{x}" y="6" width="160" height="128" rx="12" fill="#fff" stroke="#CFD8E1" stroke-width="2"/>'
            f'<g transform="translate({x+20} 14)" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">{body}</g>'
            f'<circle cx="{x+16}" cy="22" r="12" fill="{INK}"/>' + tx(x+16, 28, str(k+1), 16, 'middle', '800', '#fff') + '</g>'
            + tx(x+80, 162, title, 20, 'middle', '700'))
TH = '<rect x="30" y="56" width="60" height="10" rx="5" fill="#fff"/><circle cx="30" cy="61" r="7" fill="#D7263D" stroke="#D7263D"/>'
STEPS = [('바닥재 설치', '<path d="M6 92 h108 l-10 14 h-88 z" fill="#E8F1FB"/>' + TH),
         ('1차 포장', '<rect x="14" y="40" width="92" height="44" rx="14" fill="#E8F1FB"/>' + TH),
         ('완충재(에어캡)', '<rect x="8" y="34" width="104" height="56" rx="16" fill="#fff"/>' + ''.join(f'<circle cx="{22+i*19}" cy="{46+j*32}" r="6" fill="#E8F1FB"/>' for i in range(5) for j in range(2))),
         ('2차 포장', '<rect x="4" y="30" width="112" height="64" rx="18" fill="#E8F1FB"/><rect x="16" y="40" width="88" height="44" rx="12"/>'),
         ('상자에 완충재', '<path d="M10 38 h100 v64 h-100 z" fill="#FFF1E0"/><path d="M10 38 l14 -14 h72 l14 14"/><rect x="30" y="52" width="60" height="34" rx="10" fill="#E8F1FB"/>'),
         ('밀봉·배출정보', '<path d="M10 38 h100 v64 h-100 z" fill="#FFF1E0"/><path d="M10 38 h100" stroke="#E08A2C" stroke-width="10"/><rect x="24" y="58" width="72" height="30" fill="#fff"/><path d="M32 68 h56 M32 78 h40" stroke-width="2"/>')]
pk = ('<svg class="fig" viewBox="0 0 1112 176" style="width:1112px" aria-label="수은함유폐기물 포장 6단계 그림">'
      + ''.join(step_card(k, t, b) for k, (t, b) in enumerate(STEPS)) + '</svg>')
s = s.replace('''  <div class="flow">
    <span class="fnode">바닥재 설치</span><span class="farr">→</span><span class="fnode">1차 포장</span><span class="farr">→</span><span class="fnode">완충재(에어캡)</span><span class="farr">→</span><span class="fnode">2차 포장</span><span class="farr">→</span><span class="fnode">상자에 완충재 충전</span><span class="farr">→</span><span class="fnode hl">밀봉</span>
  </div>''', '  ' + pk)
s = re.sub(r'<div class="ts1-pk">.*?</div>\n', '', s)

# ── H. 디지털 도구 — 아이콘 (장 전체를 다시 씀) ──
H = f'''<section class="slide" data-sec="09 · 디지털 탐구 도구 안전" data-title="디지털 탐구 도구 안전">
  <h2><span class="no">0</span>새로운 위험 — 디지털 탐구 도구</h2>
  <div class="stages">
    <div class="stage"><h3>{icon('battery', 36)}리튬이온 배터리</h3><p>화재는 대부분 <mark>과충전</mark>에서 시작. 정품 충전기, 완충 후 분리, 주변 가연물 치우기. 부푼 기기는 즉시 사용 중지 <span class="ts1-flag">제안</span></p></div>
    <div class="stage"><h3>{icon('sensor', 36)}센서와 물·약품·열</h3><p>본체는 대부분 방수가 안 됨 — 탐침만 담그기. pH 전극은 보관액에. 센서 헹군 물도 폐수통으로.</p></div>
    <div class="stage"><h3>{icon('printer', 36)}3D 프린터</h3><p>사용 전·후 1시간 이상 환기, 필터 있는 밀폐형, 출력 중 마스크·장갑·보안경. 사용관리대장 비치.</p></div>
  </div>
  <div class="note" style="margin-top:16px"><span class="ts1-flag">제안</span>은 공식 지침이 아니라 재단 매뉴얼·소방본부 수칙·제조사 설명서를 과학실에 적용한 것입니다.</div>
  <p class="small ts1-src">출처: 원고 초안 Ⅸ 디지털 탐구 도구 안전(서울소방재난본부 2025, 제조사 사용설명서) · 아이콘은 직접 그림</p>
</section>'''

# 새 장 끼우기, 번호 다시 매기기
s = replace_slide(s, '안전장구와 설비', C)
s = replace_slide(s, '디지털 탐구 도구 안전', H)
s = insert_after(s, 'MSDS 교육', A, 'GHS 그림문자 9종')
s = insert_after(s, 'GHS 그림문자 9종', B, '경고표지 읽기')
n = [0]
def ren(m): n[0] += 1; return f'<span class="no">{n[0]}</span>'
s = re.sub(r'<span class="no">\d+</span>', ren, s)
open(P, 'w', encoding='utf-8').write(s)

css = open(os.path.join(D, 'extra.css'), encoding='utf-8').read().split('/* ── 그림 ── */')[0].rstrip()
css += '''
/* ── 그림 ── */
.ts1-ghsgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 16px}
.ts1-ghs{display:flex;gap:12px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:8px 10px}
.ts1-ghs svg{flex:0 0 auto}
.ts1-ghs .nm{font-size:21px;font-weight:700;line-height:1.3}
.ts1-ghs .cd{font-size:17px;font-weight:500;color:var(--muted);margin-left:4px}
.ts1-ghs .ex{font-size:19px;line-height:1.4;margin-top:2px}
.ts1-eqgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.ts1-eq{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:12px 14px}
.ts1-eq svg{flex:0 0 auto}
.ts1-eq h3{font-size:22px;margin-bottom:2px}
.ts1-eq p{font-size:19px;line-height:1.45}
.slide .stage h3 svg{display:inline-block;width:36px;height:36px;vertical-align:-9px;margin:0 6px 0 0}
'''
open(os.path.join(D, 'extra.css'), 'w', encoding='utf-8').write(css + '\n')
print('ok', s.count('<section '), '장')
