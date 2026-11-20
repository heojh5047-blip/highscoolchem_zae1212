# -*- coding: utf-8 -*-
"""차시 덱 빌드: 공용 엔진 + 차시 내용 → HTML 파일 하나 (가이드라인 A형)
사용: python build.py                 # content/ 아래 모든 덱
      python build.py 화학_미래엔/2-2-2  # 덱 id 일부만 맞으면 그 덱만
      python build.py --offline [덱]   # + 교실용(오프라인) 파일: 차시자료/교실용/<과목>/<file>_교실용.html
                                       #   (KaTeX·본문 글꼴을 파일 안에 넣음. 편집기 "교실용(오프라인)"과 같은 app/offline.js 규칙)
content/<과목>/<덱 id>/ 안에
  meta.json   {"title":"…","file":"2-2-2_전자쌍_반발_이론과_분자_구조","header":"Ⅱ-2-2 전자쌍 반발 이론과 분자 구조 (고등 화학, 미래엔 72–77쪽)"}
  slides.html <section class="slide" …> 들
  labs.js     (선택) window.DECK_LABS = { 이름(root, API){ … } };
  extra.css   (선택) 이 덱에서만 쓰는 스타일
결과: 차시자료/<과목>/<file>.html
"""
import json, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # _소스
OUT = os.path.dirname(SRC)                                          # 차시자료
rd = lambda p: open(p, encoding='utf-8-sig').read()   # PowerShell이 붙이는 BOM도 허용
ENG = os.path.join(SRC, 'engine')

HEADER = r"""<!--
  SLIDE HARNESS · {header}
  ─────────────────────────────────────────────────────────────
  하우스 규칙 (docs/슬라이드_제작도구_가이드라인_화학.md)
   T1 어절 단위 줄바꿈 (keep-all + keepWords)   T2 수식·화학식 줄바꿈 금지 (+ WORD JOINER)
   T3 여러 식·반응식은 세로로                     T4 표 칸은 한 줄   T5 flex 요소에 텍스트 직접 금지
   M1 모든 기호 LaTeX(그림 라벨 포함)            M2 단위 곱은 \cdot  M3 단위는 해당 양에만   M9 수와 단위 사이 한 칸
   C1 화학식·이온·반응식은 \ce{{}}(mhchem) — H2O·Na+를 본문 글자로 쓰지 않음   C2 상태 기호 (s)(l)(g)(aq)
   C3 비가역 ->, 가역 <=>                        C5 반응식은 원자 수·전하 보존(검산)   C7 농도 [\ce{{A}}], K·Q·K_\mathrm{{w}}
   D1 회로(전기 분해·화학 전지): 극 라벨·접합점 ●  D2 화살표에 무엇의 이동인지 라벨(전자, 이온, 열)
   D3 대칭 분자 → 대칭 그림   D4 축 라벨 기호 [단위]   D5 id 고유   D6 전자는 전자 껍질 위   D8 라벨 잘림 금지
   D7 (+)·양이온·δ+ plus#D7263D  (−)·음이온·전자·δ− minus#1F6FD1  산화 ox#C2410C 환원 rd#0E7490  강조#FFE45C
      원자 칠은 data-atom(HARNESS_ATOM) — 그림에는 hex 대신 색 이름(HARNESS_COL)
   D21 입자 모형: 원소마다 같은 색·크기, 반응 전후 원자 수 보존   D22 루이스 전자점식   D23 분자 구조·결합각
   D24 쌍극자 모멘트 화살표(+ 꼬리, 전기음성도 큰 쪽으로)          D26 에너지 도표(ΔH, Ea)
   S1 그림+설명은 같은 단계(data-g)              S2 연습 문제는 한 장에 하나 + 판서 공간
   S3 과정은 단계별 그림 카드                    S5 개념 전에 '왜 필요한가' 연결 슬라이드
   S9 실험 슬라이드에 안전 수칙·폐수 처리        S10 현상(거시) → 입자(미시) → 화학식(기호)
   S12 성취기준 <탐구 활동>은 필수 — 실험실 + 탐구 슬라이드로 이행
  조작키
   → / 스페이스 / 클릭 : 다음 단계·슬라이드      ← : 이전      Home / End
   O 목차   F 전체 화면   P 판서 펜   X 판서 지우기   B 화면 가리기   D 자동 점검(?audit)   H 도움말
  작성 빠른 참조
   <section class="slide" data-sec="머리띠 왼쪽" data-title="목차 제목">
   .step (같은 data-g 값은 함께 공개) · <mark>핵심 정의</mark> · .formula · .answer · .board(판서 공간)
   화학식    $\ce{{N2(g) + 3H2(g) <=> 2NH3(g)}}$  $\ce{{SO4^2-}}$  $[\ce{{H3O+}}]$  $\Delta H=-92\ \text{{kJ}}$
   SVG 라벨  <text class="tex" x y data-tex="\ce{{H2O}}"|data-mix="$\ce{{Na+}}$ 이온||둘째 줄" data-size data-anchor fill data-halo>
   SVG 부품  <g data-atom="x,y,r,원소[,라벨|-][,d]">  <g data-arw="x1,y1,x2,y2,색,굵기[,d]">  <g data-chg="x,y,r,+|-|P|M|N[,d]">
             <g data-pm="부호,크기,x:y x:y[,색]">   <svg data-circuit='{{"parts":[["wire",…],["bat",…],["node",…],["sw",…],["meter",…]]}}'>
   실험실    <div class="lab" data-lab="이름"> + window.DECK_LABS.이름(root, API)
  인터넷이 없는 교실: KaTeX(cdn.jsdelivr.net)를 못 불러오면 수식이 원문으로 보입니다. 미리 한 번 열어 확인하세요.
  이 파일은 차시자료/_소스 에서 빌드되었습니다. 고칠 때는 _소스/content 의 내용을 고치고 tools/build.py 를 다시 실행하세요.
-->"""

def build(subject, deck_id):
    d = os.path.join(SRC, 'content', subject, deck_id)
    meta = json.loads(rd(os.path.join(d, 'meta.json')))
    slides = rd(os.path.join(d, 'slides.html'))
    labs = rd(os.path.join(d, 'labs.js')) if os.path.exists(os.path.join(d, 'labs.js')) else ''
    extra = rd(os.path.join(d, 'extra.css')) if os.path.exists(os.path.join(d, 'extra.css')) else ''
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="deck-id" content="{subject}/{deck_id}">
{HEADER.format(header=meta.get('header', meta['title']))}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/mhchem.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
{rd(os.path.join(ENG, 'harness.css'))}
/*EXTRA:BEGIN*/
{extra}
/*EXTRA:END*/
</style>
</head>
<body>
<div id="viewport"><div id="deck">
<canvas id="ink"></canvas>
<!--SLIDES:BEGIN-->
{slides.strip()}
<!--SLIDES:END-->
</div></div>

{rd(os.path.join(ENG, 'harness-ui.html')).strip()}

<script>
/* ════════════════ 이 차시의 실험실 ════════════════ */
/*LABS:BEGIN*/
{labs.strip() or 'window.DECK_LABS = window.DECK_LABS || {};'}
/*LABS:END*/
</script>
<script>
{rd(os.path.join(ENG, 'harness.js')).strip()}
</script>
</body>
</html>
"""
    outdir = os.path.join(OUT, subject)
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, meta['file'] + '.html')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(f"built {subject}/{meta['file']}.html  ({len(html)//1024} KB)")
    return out

def offline(subject, html_path):
    """빌드된 덱 → 교실용 파일. 변환은 node tools/offline.mjs (편집기와 같은 app/offline.js)"""
    import subprocess
    out = os.path.join(OUT, '교실용', subject, os.path.basename(html_path)[:-5] + '_교실용.html')
    r = subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'offline.mjs'), html_path, out],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('  ' + (r.stdout.strip() or r.stderr.strip()))
    if r.returncode: sys.exit(r.returncode)

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    OFFLINE = '--offline' in sys.argv
    pat = args[0] if args else ''
    root = os.path.join(SRC, 'content')
    n = 0
    for subject in sorted(os.listdir(root)):
        sd = os.path.join(root, subject)
        if not os.path.isdir(sd): continue
        for deck in sorted(os.listdir(sd)):
            if not os.path.exists(os.path.join(sd, deck, 'meta.json')): continue
            if not os.path.exists(os.path.join(sd, deck, 'slides.html')): continue   # 구성안(plan.md)만 있는 폴더는 건너뜀
            if pat and pat not in f'{subject}/{deck}': continue
            out = build(subject, deck); n += 1
            if OFFLINE: offline(subject, out)   # 과목 제한 없음(화학 과목 포함). app/offline.js가 mhchem.min.js도 넣어야 한다(README)
    if not n: print('빌드할 덱이 없습니다:', pat); sys.exit(1)
