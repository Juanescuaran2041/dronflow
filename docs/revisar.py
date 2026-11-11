"""Revisa el SVG generado: lineas sobre cajas, etiquetas chocando y cruces sin salto."""
import re, sys

html = open(sys.argv[1], encoding="utf-8").read()
W = int(re.search(r'viewBox="0 0 (\d+) (\d+)"', html).group(1))
H = int(re.search(r'viewBox="0 0 (\d+) (\d+)"', html).group(2))

cajas = [(int(a), int(b), int(a) + int(c), int(b) + int(d)) for a, b, c, d in
         re.findall(r'<rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)" rx="4"', html)]

segs = []
for m in re.finditer(r'<path d="([^"]+)" fill="none" stroke="#e5e5e5"', html):
    cur = None
    for cmd, nums in re.findall(r'([MLA])([-\d. ]+)', m.group(1)):
        v = [float(n) for n in nums.split()]
        if cmd == "M":
            cur = (v[0], v[1])
        elif cmd == "L":
            p = (v[0], v[1]); segs.append((cur, p)); cur = p
        elif cmd == "A":
            cur = (v[-2], v[-1])

etiquetas = []
for m in re.finditer(r'<text class="ifc" x="(-?[\d.]+)" y="(-?[\d.]+)" text-anchor="(\w+)">([^<]*)</text>', html):
    x, y, anc, t = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
    if y > H - 60:
        continue  # leyenda
    w = len(t) * 6.4
    x1 = {"start": x, "end": x - w, "middle": x - w / 2}[anc]
    etiquetas.append((x1, y - 10, x1 + w, y + 2, t))

probs = []
for (x1, y1), (x2, y2) in segs:
    for bx1, by1, bx2, by2 in cajas:
        a, b, c, dd = bx1 + 2, by1 + 2, bx2 - 2, by2 - 2
        if (x1 == x2 and a < x1 < c and min(y1, y2) < dd and max(y1, y2) > b) or \
           (y1 == y2 and b < y1 < dd and min(x1, x2) < c and max(x1, x2) > a):
            probs.append(f"LINEA ({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f}) atraviesa caja {(bx1,by1,bx2,by2)}")

for lx1, ly1, lx2, ly2, t in etiquetas:
    if lx2 > W or lx1 < 0 or ly2 > H:
        probs.append(f"ETIQUETA {t!r} fuera del lienzo ({lx1:.0f}..{lx2:.0f})")
    for bx1, by1, bx2, by2 in cajas:
        if lx1 < bx2 and lx2 > bx1 and ly1 < by2 and ly2 > by1:
            probs.append(f"ETIQUETA {t!r} sobre caja {(bx1,by1,bx2,by2)}")
    for (sx1, sy1), (sx2, sy2) in segs:
        a, b = sorted((sx1, sx2)); c, dd = sorted((sy1, sy2))
        if lx1 < b and lx2 > a and ly1 < dd and ly2 > c:
            probs.append(f"ETIQUETA {t!r} sobre linea ({sx1:.0f},{sy1:.0f})-({sx2:.0f},{sy2:.0f})")
for i, (ax1, ay1, ax2, ay2, at) in enumerate(etiquetas):
    for bx1, by1, bx2, by2, bt in etiquetas[i + 1:]:
        if ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1:
            probs.append(f"ETIQUETAS {at!r} y {bt!r} se pisan")

Hs = [s for s in segs if s[0][1] == s[1][1]]
Vs = [s for s in segs if s[0][0] == s[1][0]]
cruces = set()
for a, b in Hs:
    y = a[1]; lo, hi = sorted((a[0], b[0]))
    for c, dd in Vs:
        x = c[0]; y1, y2 = sorted((c[1], dd[1]))
        if lo < x < hi and y1 < y < y2:
            cruces.add((int(x), int(y)))
declarados = set()
for m in re.finditer(r'saltos=\[([^\]]*)\]', open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else ""):
    for a, b in re.findall(r'\((\d+),\s*(\d+)\)', m.group(1)):
        declarados.add((int(a), int(b)))

print(f"cajas={len(cajas)} interfaces={len(etiquetas)} segmentos={len(segs)}")
print("cruces sin salto:", sorted(cruces - declarados) or "ninguno")
print(f"problemas ({len(probs)}):")
for p in probs:
    print("  -", p)
