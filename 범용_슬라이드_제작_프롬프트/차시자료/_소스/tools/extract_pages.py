# -*- coding: utf-8 -*-
"""자료 PDF(연수 원고·지침·매뉴얼·교과서 등) → 쪽별 텍스트 (덱 폴더 자료/ 안에 두고 에이전트가 필요한 쪽만 읽는다)
사용: python extract_pages.py <PDF> <출력.txt> [--offset=N] [--layout]
  --offset=N : 인쇄된 쪽 = PDF 쪽 + N  (예: PDF 1쪽이 책 50쪽 → --offset=49). 쪽을 모르면 0
  --layout   : 2단 편집을 줄 맞춤으로 (pdftotext -layout). 칸이 많은 쪽은 오히려 섞일 수 있음
결과: 쪽마다 "=== p.<PDF쪽> (책 <인쇄 쪽>쪽) ===" 머리줄 + 본문. 에이전트는 이 머리줄을 Grep으로 찾아 offset/limit로 읽는다.
PyMuPDF(pip install pymupdf)가 있으면 쓰고, 없으면 poppler의 pdftotext를 쓴다.
표·숫자·기호가 깨질 수 있으므로(× → _, ℃ → ¾, 위·아래 첨자 분리 등) 중요한 값은 PDF 쪽 이미지로 확인한다(공통.md 1절).
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
