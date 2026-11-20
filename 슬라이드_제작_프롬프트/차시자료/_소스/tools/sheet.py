# -*- coding: utf-8 -*-
"""캡처 모음: 슬라이드 캡처 4장을 한 장(2×2)에 모은다 — 전체 훑어보기용(읽는 양 1/4)
사용: python sheet.py <캡처 폴더> [--slides=3-10] [--steps]
  캡처 폴더  : render.mjs 출력 폴더 (s01.png, s02.png …)
  --slides   : 일부만 (예: 3,5-8)
  --steps    : 단계별 캡처(sNN-K.png)를 모음 (render.mjs --steps 출력 폴더에 쓴다)
결과: <캡처 폴더>/sheet_NN_MM.png (칸마다 왼쪽 위에 슬라이드 번호)
필요: Pillow (pip install pillow)
"""
import sys, os, re, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image, ImageDraw

def parse(spec):
    s = set()
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-'); s.update(range(int(a), int(b) + 1))
        elif part: s.add(int(part))
    return s

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if not a: print(__doc__); sys.exit(2)
    d = a[0]
    steps = '--steps' in sys.argv
    want = next((parse(x.split('=')[1]) for x in sys.argv if x.startswith('--slides=')), None)
    pat = re.compile(r'^s(\d+)-(\d+)\.png$' if steps else r'^s(\d+)\.png$')
    files = sorted((f for f in os.listdir(d) if pat.match(f)), key=lambda f: tuple(int(x) for x in pat.match(f).groups()))
    if want: files = [f for f in files if int(pat.match(f).group(1)) in want]
    for f in os.listdir(d):
        if f.startswith('sheet_') and f.endswith('.png'): os.remove(os.path.join(d, f))
    W, H, G = 1280, 720, 8
    for k in range(0, len(files), 4):
        grp = files[k:k + 4]
        sheet = Image.new('RGB', (2 * W + 3 * G, 2 * H + 3 * G), (60, 60, 60))
        dr = ImageDraw.Draw(sheet)
        for j, f in enumerate(grp):
            im = Image.open(os.path.join(d, f)).convert('RGB').resize((W, H))
            x, y = G + (j % 2) * (W + G), G + (j // 2) * (H + G)
            sheet.paste(im, (x, y))
            dr.rectangle([x, y, x + 150, y + 44], fill=(22, 35, 61))
            dr.text((x + 12, y + 10), f[:-4], fill=(255, 255, 255))
        sheet = sheet.resize((sheet.width // 2, sheet.height // 2))
        n1, n2 = pat.match(grp[0]).group(1), pat.match(grp[-1]).group(1)
        out = os.path.join(d, f'sheet_{n1}_{n2}' + (f'_{k // 4:02d}' if steps else '') + '.png')
        sheet.save(out)
        print(out)
