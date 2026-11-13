# -*- coding: utf-8 -*-
"""차시 덱 빌드: 공용 엔진 + 차시 내용 → HTML 파일 하나 (가이드라인 A형)
사용: python build.py                 # content/ 아래 모든 덱
      python build.py 교사연수/1_실험실  # 덱 id 일부만 맞으면 그 덱만
      python build.py --offline [덱]   # + 완성본(오프라인 단일 파일): 차시자료/완성본/<묶음 키>/<file>.html
                                       #   (KaTeX·본문 글꼴을 파일 안에 넣음 — tools/offline.mjs)
content/<묶음 키>/<덱 폴더>/ 안에
  meta.json   {"title":"…","file":"1_실험실_안전_교육","header":"1차시 실험실 안전 교육 (교사 연수, 50분)","credit":"(선택) 꼬리말"}
  slides.html <section class="slide" …> 들
  labs.js     (선택) window.DECK_LABS = { 이름(root, API){ … } };
  extra.css   (선택) 이 덱에서만 쓰는 스타일
  img/        (선택) 직접 만든 그림·화면 갈무리. slides.html에서 src="img/파일.png" — 빌드할 때 파일 안에 들어감
결과: 차시자료/<묶음 키>/<file>.html
꼬리말: _소스/묶음설정.json의 "credit"(meta.json의 "credit"이 있으면 그것, 빈 글이면 넣지 않음)을 표지(없으면 첫 장) 왼쪽 아래에 넣는다.
"""
import json, os, sys, io, re
from html import escape as html_escape
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # _소스
OUT = os.path.dirname(SRC)                                          # 차시자료
rd = lambda p: open(p, encoding='utf-8-sig').read()   # PowerShell이 붙이는 BOM도 허용
ENG = os.path.join(SRC, 'engine')
_cfgp = os.path.join(SRC, '묶음설정.json')
CFG = json.loads(rd(_cfgp)) if os.path.exists(_cfgp) else {}   # {"credit": "제작: ○○학교 ○○○"}

HEADER = r"""<!--
  SLIDE HARNESS · {header}
  ─────────────────────────────────────────────────────────────
  하우스 규칙 (docs/슬라이드_제작_가이드라인_범용.md)
   T1 어절 단위 줄바꿈 (keep-all + keepWords)   T2 수식 줄바꿈 금지 (+ WORD JOINER)
   T3 여러 식은 세로로   T4 표 칸은 한 줄   T5 flex 요소에 텍스트 직접 금지   T6 여러 줄 식은 등호 맞춤
   M1 모든 기호 LaTeX(그림 라벨 포함)   M2 단위 곱은 \cdot   M3 단위는 해당 양에만   M9 수와 단위 사이 한 칸
   C1 (교과 수업에서 화학식을 쓸 때) 화학식은 \ce{{}} — H2O·Na+를 본문 글자로 쓰지 않음
   D2 화살표에는 무엇의 흐름인지 라벨   D3 대칭인 것은 대칭으로   D4 축 라벨 기호 [단위]   D5 id 고유
   D7 색 하나 = 뜻 하나(HARNESS_COL 이름)   D8 라벨 잘림·겹침 금지   D9 길이·막대는 크기에 비례
   S1 그림+설명은 같은 단계(data-g)   S2 문제는 한 장에 하나 + 판서 공간   S3 과정은 단계별 그림 카드
   S5 새 내용 전에 '왜 필요한가'   S6 예측 → 관찰 → 설명   S7 활동·실습은 목적 → 방법 → 결과 → 정리
  조작키
   → / 스페이스 / 클릭 : 다음 단계·슬라이드      ← : 이전      Home / End
   O 목차   F 전체 화면   P 판서 펜   X 판서 지우기   B 화면 가리기   D 자동 점검(?audit)   H 도움말
  작성 빠른 참조
   <section class="slide" data-sec="머리띠 왼쪽" data-title="목차 제목">
   .step (같은 data-g 값은 함께 공개) · <mark>핵심 정의</mark> · .formula · .answer · .board(판서 공간)
   SVG 라벨  <text class="tex" x y data-tex="..."|data-mix="한글 $x$||둘째 줄" data-size data-anchor fill data-halo>
   SVG 부품  <g data-arw="x1,y1,x2,y2,색,굵기[,d]">  <g data-chg="x,y,r,+|-|P|M|N[,d]">  <g data-atom="x,y,r,원소[,라벨|-][,d]">
   실험실    <div class="lab" data-lab="이름"> + window.DECK_LABS.이름(root, API)
  인터넷이 없는 교실: KaTeX(cdn.jsdelivr.net)를 못 불러오면 수식이 원문으로 보입니다. 완성본(build.py --offline)을 쓰세요.
  이 파일은 차시자료/_소스 에서 빌드되었습니다. 고칠 때는 _소스/content 의 내용을 고치고 tools/build.py 를 다시 실행하세요.
-->"""

MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml'}
def inline_images(d, slides):
    """덱 폴더 img/ 안의 그림(src="img/…")을 data URI로 넣는다 — 결과가 HTML 파일 하나로 끝나게."""
    import base64
    def rep(m):
        rel = m.group(2); p = os.path.join(d, *rel.split('/'))
        ext = os.path.splitext(p)[1].lower()
        if ext not in MIME or not os.path.exists(p):
            print(f'  경고: 그림을 찾지 못함 {rel}'); return m.group(0)
        return f'{m.group(1)}="data:{MIME[ext]};base64,{base64.b64encode(open(p, "rb").read()).decode()}"'
    return re.sub(r'\b(src|href)="(img/[^"]+)"', rep, slides)

def build(subject, deck_id):
    d = os.path.join(SRC, 'content', subject, deck_id)
    meta = json.loads(rd(os.path.join(d, 'meta.json')))
    slides = rd(os.path.join(d, 'slides.html'))
    labs = rd(os.path.join(d, 'labs.js')) if os.path.exists(os.path.join(d, 'labs.js')) else ''
    extra = rd(os.path.join(d, 'extra.css')) if os.path.exists(os.path.join(d, 'extra.css')) else ''
    slides = inline_images(d, slides)
    credit = meta.get('credit', CFG.get('credit', ''))
    if credit:   # 꼬리말(제작자 표시): 표지(class="slide cover"), 없으면 첫 장 안에 넣는다 — 엔진은 고치지 않음
        tag = f'\n  <p class="deck-credit">{html_escape(credit)}</p>\n'
        m = re.search(r'<section\b[^>]*class="[^"]*\bcover\b[^"]*"[^>]*>', slides) or re.search(r'<section\b[^>]*>', slides)
        if m:
            j = slides.find('</section>', m.end())
            if j > 0: slides = slides[:j] + tag + slides[j:]
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']}</title>
<meta name="deck-id" content="{subject}/{deck_id}">{f'''
<meta name="author" content="{html_escape(credit)}">''' if credit else ''}
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
.slide .deck-credit{{position:absolute;left:84px;bottom:66px;margin:0;font-size:19px;line-height:1.3;color:var(--muted)}}
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
    """빌드된 덱 → 완성본(오프라인 단일 파일). 변환은 node tools/offline.mjs"""
    import subprocess
    out = os.path.join(OUT, '완성본', subject, os.path.basename(html_path))
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
            if OFFLINE: offline(subject, out)
    if not n: print('빌드할 덱이 없습니다:', pat); sys.exit(1)
