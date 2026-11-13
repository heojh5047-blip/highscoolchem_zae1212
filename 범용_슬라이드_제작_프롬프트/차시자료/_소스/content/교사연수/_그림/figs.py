# 교사연수 덱 공용 그림(SVG 조각) — 직접 그린 그림. GHS 그림문자는 UN GHS 규격 꼴(빨간 마름모 테, 흰 바탕, 검은 상징)을 따라 다시 그림.
INK, PLUS, MINUS, FIELD, EQUI, GRAV, MUTED = '#16233D', '#D7263D', '#1F6FD1', '#2E9E6A', '#E08A2C', '#8C99A6', '#5B6B7F'
BF, OX, RD = '#7B4FC8', '#C2410C', '#0E7490'
GHS_RED = '#E3000F'   # GHS: 빨간 테두리

_SYM = {
 # 폭발성: 터지는 폭탄
 '01': '<circle cx="42" cy="60" r="11"/><path d="M50 50 l4 -4" stroke="#000" stroke-width="3"/>'
       '<g stroke="#000" stroke-width="3" stroke-linecap="round"><path d="M57 42 l6 -8 M60 50 l10 -2 M54 37 l1 -9 M64 58 l8 4"/></g>'
       '<path d="M66 30 l3 3 l-3 3 l-3 -3 z M71 44 l3 2 l-2 3 l-3 -2 z M30 40 l3 1 l-1 3 l-3 -1 z"/>',
 # 인화성: 불꽃
 '02': '<path d="M50 24 C58 34 68 42 66 58 C65 69 58 74 50 74 C41 74 34 67 35 57 C36 49 41 45 43 37 C46 43 47 47 50 50 C53 42 53 32 50 24 Z"/><rect x="32" y="77" width="36" height="4"/>',
 # 산화성: 원 위의 불꽃
 '03': '<path d="M50 22 C56 30 62 35 61 46 C60 53 56 56 50 56 C44 56 39 52 40 45 C40 40 44 37 45 32 C47 36 48 39 50 41 C52 35 52 28 50 22 Z"/>'
       '<circle cx="50" cy="64" r="10" fill="none" stroke="#000" stroke-width="5"/><rect x="32" y="77" width="36" height="4"/>',
 # 고압가스: 가스 실린더
 '04': '<rect x="26" y="45" width="42" height="18" rx="9"/><rect x="68" y="50" width="6" height="8"/><rect x="74" y="47" width="4" height="14" rx="1"/>',
 # 부식성: 시험관 두 개 → 손과 금속판
 '05': '<g transform="rotate(-38 37 28)"><path d="M32 38 v-18 a5 5 0 0 1 10 0 v18 z"/></g><g transform="rotate(38 63 28)"><path d="M58 38 v-18 a5 5 0 0 1 10 0 v18 z"/></g>'
       '<g stroke="#000" stroke-width="2.6" stroke-linecap="round"><path d="M43 44 v6 M45 50 v4 M57 44 v6 M55 50 v4"/></g>'
       '<path d="M20 62 h20 a3 3 0 0 1 0 6 h-4 a2 2 0 0 1 0 4 h-16 z"/><path d="M27 62 l3 4 l3 -4 z" fill="#fff"/>'
       '<path d="M56 62 h24 v12 h-24 z"/><path d="M60 62 l3 5 l3 -5 l3 6 l3 -6 z" fill="#fff"/>',
 # 급성 독성: 해골과 엇갈린 뼈
 '06': '<g stroke="#000" stroke-width="5" stroke-linecap="round"><path d="M32 54 L68 74 M68 54 L32 74"/></g>'
       '<path d="M50 24 C39 24 33 31 33 40 C33 46 36 49 40 51 V56 H60 V51 C64 49 67 46 67 40 C67 31 61 24 50 24 Z"/>'
       '<circle cx="43" cy="40" r="4.5" fill="#fff"/><circle cx="57" cy="40" r="4.5" fill="#fff"/><path d="M50 45 l-2.5 4 h5 z" fill="#fff"/>',
 # 경고: 느낌표
 '07': '<path d="M45 26 h10 l-2 30 h-6 z"/><circle cx="50" cy="66" r="5.5"/>',
 # 건강 유해성: 사람 상반신 + 가슴의 별
 '08': '<circle cx="50" cy="31" r="7"/><path d="M33 76 C33 56 38 42 50 42 C62 42 67 56 67 76 Z"/>'
       '<path d="M50 50 l2.6 5.8 l6.2 .6 l-4.7 4.1 l1.4 6.1 l-5.5 -3.2 l-5.5 3.2 l1.4 -6.1 l-4.7 -4.1 l6.2 -.6 z" fill="#fff"/>',
 # 수생환경 유해성: 죽은 나무와 물고기
 '09': '<g stroke="#000" stroke-width="2.6" stroke-linecap="round" fill="none"><path d="M36 70 V36 M36 50 L28 40 M36 44 L44 34 M36 58 L44 50 M28 40 l-2 -5 M44 34 l3 -4"/><path d="M24 71 H76"/></g>'
       '<path d="M50 62 C55 55 66 55 71 62 C66 69 55 69 50 62 Z"/><path d="M71 62 l6 -5 v10 z"/>'
       '<path d="M54 60 l3 3 M57 60 l-3 3" stroke="#fff" stroke-width="1.4"/>',
}
GHS_NAME = {'01': '폭발성', '02': '인화성', '03': '산화성', '04': '고압가스', '05': '부식성',
            '06': '급성 독성', '07': '경고', '08': '건강 유해성', '09': '수생환경 유해성'}

def ghs_g(code, x=0, y=0, s=1.0):
    """GHS 그림문자 하나(<g>) — 원래 크기 100×100"""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M50 3 L97 50 L50 97 L3 50 Z" fill="#fff" stroke="{GHS_RED}" stroke-width="7" stroke-linejoin="miter"/>'
            f'<g fill="#000">{_SYM[code]}</g></g>')

def ghs_svg(code, px=96, extra=''):
    return (f'<svg viewBox="0 0 100 100" width="{px}" height="{px}" role="img" aria-label="GHS 그림문자 {GHS_NAME[code]}" data-audit="skip"{extra}>'
            + ghs_g(code) + '</svg>')

# 보호구·설비 아이콘 (64×64, 선 그림)
_IC = {
 'coat': '<path d="M22 10 L32 18 L42 10 L54 18 L50 30 L46 28 V56 H18 V28 L14 30 L10 18 Z" fill="#fff"/><path d="M32 18 V56"/><path d="M24 38 h5 M35 38 h5"/>',
 'glove': '<path d="M20 56 V30 C20 26 26 26 26 30 V22 C26 18 32 18 32 22 V20 C32 16 38 16 38 20 V24 C38 20 44 20 44 24 V40 L50 34 C53 31 57 35 54 38 L44 52 V56 Z" fill="#E8F1FB"/>',
 'goggle': '<path d="M8 28 C8 22 14 20 20 20 H44 C50 20 56 22 56 28 V36 C56 42 50 44 44 44 C38 44 36 38 32 38 C28 38 26 44 20 44 C14 44 8 42 8 36 Z" fill="#E8F1FB"/><path d="M8 30 H4 M56 30 H60"/>',
 'mask': '<path d="M14 26 C14 20 50 20 50 26 V38 C50 48 40 52 32 52 C24 52 14 48 14 38 Z" fill="#fff"/><path d="M14 30 L6 26 M50 30 L58 26 M14 38 L6 42 M50 38 L58 42"/><circle cx="32" cy="38" r="6" fill="#E8F1FB"/>',
 'eyewash': '<path d="M14 54 H50 M32 54 V36"/><path d="M20 36 H44 L40 28 H24 Z" fill="#E8F1FB"/><path d="M26 22 C26 16 30 14 30 10 M38 22 C38 16 34 14 34 10" stroke="#1F6FD1"/>',
 'ext': '<rect x="22" y="20" width="20" height="36" rx="6" fill="#FDF1F3" stroke="#D7263D"/><path d="M28 20 V14 H38 M38 14 L48 18 M32 14 V10"/><rect x="26" y="30" width="12" height="10" rx="2" fill="#fff" stroke="#D7263D"/>',
 'shower': '<path d="M14 58 V10 H40 V18"/><path d="M30 18 H50 L46 24 H34 Z" fill="#E8F1FB"/><path d="M36 30 l-2 6 M40 30 v6 M44 30 l2 6 M38 42 l-1 5 M42 42 l1 5" stroke="#1F6FD1"/><path d="M28 58 H52"/>',
 'fan': '<circle cx="32" cy="32" r="22" fill="#fff"/><path d="M32 32 C30 20 38 14 42 18 C44 24 36 28 32 32 C44 32 48 40 44 44 C38 46 34 38 32 32 C24 42 16 40 16 34 C18 28 26 30 32 32 Z" fill="#E8F1FB"/><circle cx="32" cy="32" r="3"/>',
 'battery': '<rect x="12" y="18" width="36" height="28" rx="5" fill="#fff"/><rect x="48" y="26" width="5" height="12" rx="1"/><path d="M28 24 L22 34 H30 L26 42" stroke="#E08A2C"/>',
 'sensor': '<rect x="12" y="10" width="22" height="20" rx="4" fill="#E8F1FB"/><path d="M23 30 V54"/><circle cx="23" cy="56" r="3" fill="#16233D"/><path d="M34 20 C44 20 46 30 52 30"/><path d="M44 46 H58 M46 50 H56" stroke="#1F6FD1"/>',
 'printer': '<rect x="10" y="12" width="44" height="40" rx="4" fill="#fff"/><path d="M10 22 H54"/><path d="M26 22 V30 H38 V22"/><path d="M22 48 H42 L38 40 H26 Z" fill="#E8F1FB"/>',
}
def icon(name, px=64, stroke=INK):
    return (f'<svg viewBox="0 0 64 64" width="{px}" height="{px}" aria-hidden="true" data-audit="skip">'
            f'<g fill="none" stroke="{stroke}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{_IC[name]}</g></svg>')
