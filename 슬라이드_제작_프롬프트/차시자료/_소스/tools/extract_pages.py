# -*- coding: utf-8 -*-
"""교과서·지도서 PDF → 쪽별 텍스트 (_추출/ 폴더용, 저작권 때문에 묶음에는 넣지 않으므로 각자 만든다)
사용: python extract_pages.py <PDF> <출력.txt> [--offset=N] [--layout]
  --offset=N : 교과서 쪽 = PDF 쪽 + N  (예: 미래엔 화학 Ⅱ단원 PDF는 1쪽이 교과서 50쪽 → --offset=49)
               덱목록.json의 units[단원].pdfOffset 값을 쓴다. 쪽을 모르면 0
  --layout   : 2단 편집을 줄 맞춤으로 (pdftotext -layout). 지도서처럼 칸이 많은 쪽은 오히려 섞일 수 있음
결과: 쪽마다 "=== p.<PDF쪽> (책 <교과서쪽>쪽) ===" 머리줄 + 본문. 에이전트는 이 머리줄을 Grep으로 찾아 offset/limit로 읽는다.
PyMuPDF(pip install pymupdf)가 있으면 쓰고, 없으면 poppler의 pdftotext를 쓴다.
추출 기호 깨짐(⇌ → ^jjj&, × → _, ℃ → ¾, 위·아래 첨자 분리 등)은 PDF 쪽 이미지로 확인한다(공통.md 1절).
"""
import sys, io, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def pages_fitz(pdf):
    import fitz
    d = fitz.open(pdf)
    return [p.get_text() for p in d]

def pages_poppler(pdf, layout):
    n = int([l for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True, errors='replace').stdout.splitlines() if l.startswith('Pages:')][0].split()[1])
    out = []
    for i in range(1, n + 1):
        args = ['pdftotext', '-f', str(i), '-l', str(i)] + (['-layout'] if layout else []) + [pdf, '-']
        out.append(subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout)
    return out

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if len(a) < 2:
        print(__doc__); sys.exit(2)
    off = next((int(x.split('=')[1]) for x in sys.argv if x.startswith('--offset=')), 0)
    layout = '--layout' in sys.argv
    try:
        if layout: raise ImportError
        pages = pages_fitz(a[0])
    except ImportError:
        pages = pages_poppler(a[0], layout)
    os.makedirs(os.path.dirname(os.path.abspath(a[1])), exist_ok=True)
    with open(a[1], 'w', encoding='utf-8', newline='\n') as f:
        for i, t in enumerate(pages, 1):
            f.write(f'=== p.{i} (책 {i + off}쪽) ===\n{t.strip()}\n\n')
    print(f'{os.path.basename(a[0])}: {len(pages)}쪽 → {a[1]}')
