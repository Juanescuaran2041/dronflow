"""componentes_lib.py - diagramas de componentes UML (puertos e interfaces) en HTML/SVG, fondo negro."""
from html import escape

RB, RS, RJ = 7, 11, 6  # radio bola (provista), radio enchufe (requerida), radio salto


class Diagrama:
    def __init__(self, titulo, ancho=1600, alto=1200):
        self.titulo, self.W, self.H = titulo, ancho, alto
        self.lineas, self.cajas, self.formas, self.textos = [], [], [], []

    # ---------- elementos ----------
    def componente(self, x, y, nombre, w=180, h=70, estereotipo="«component»"):
        """nombre admite salto de línea con \n (máximo 2 líneas)."""
        cx = x + w / 2
        partes = nombre.split("\n")
        # centrado vertical: con cajas altas el bloque quedaba pegado al borde superior
        tope = y + (h - (20 + 17 * len(partes))) / 2
        self.cajas.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#000" stroke="#fff"/>')
        self.cajas.append(f'<text class="stereo" x="{cx}" y="{tope + 14}" text-anchor="middle">{escape(estereotipo)}</text>')
        ys = [tope + 34 + i * 17 for i in range(len(partes))]
        for t, ty in zip(partes, ys):
            self.cajas.append(f'<text class="name" x="{cx}" y="{ty}" text-anchor="middle">{escape(t)}</text>')

    def interfaz(self, etiqueta, proveedor=None, consumidores=(), saltos=()):
        centro = tuple(proveedor[-1]) if proveedor else tuple(consumidores[0][-1])
        for ruta in consumidores:
            assert tuple(ruta[-1]) == centro, f"La ruta {ruta} no termina en el centro {centro}"
            self._linea(self._recortar(ruta, RS), saltos)
            self._puerto(*ruta[0])
            self._enchufe(centro, self._lado(ruta))
        if proveedor:
            self._linea(self._recortar(proveedor, RB), saltos)
            self._puerto(*proveedor[0])
            self.formas.append(f'<circle cx="{centro[0]}" cy="{centro[1]}" r="{RB}" fill="#000" stroke="#fff" stroke-width="1.4"/>')
        self._texto(*etiqueta)

    # ---------- salida ----------
    def guardar(self, ruta_html):
        self._leyenda()
        cuerpo = "\n  ".join(
            [f'<rect x="1" y="1" width="{self.W - 2}" height="{self.H - 2}" rx="8" fill="none" stroke="#777"/>',
             f'<text class="title" x="{self.W // 2}" y="30" text-anchor="middle">{escape(self.titulo)}</text>']
            + self.lineas + self.cajas + self.formas + self.textos)
        html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(self.titulo)} - Diagrama de componentes</title>
<style>
  html, body {{ margin: 0; background: #000; }}
  body {{ padding: 16px; box-sizing: border-box; }}
  svg {{ width: {self.W}px; height: {self.H}px; font-family: Arial, Helvetica, sans-serif; }}
  .name {{ fill: #fff; font-size: 14px; font-weight: bold; }}
  .stereo {{ fill: #9e9e9e; font-size: 12px; }}
  .ifc {{ fill: #d0d0d0; font-size: 12px; }}
  .title {{ fill: #fff; font-size: 16px; font-weight: bold; }}
</style>
</head>
<body>
<svg viewBox="0 0 {self.W} {self.H}" role="img" aria-label="Diagrama de componentes de {escape(self.titulo)}">
  {cuerpo}
</svg>
</body>
</html>
'''
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html)

    # ---------- internos ----------
    @staticmethod
    def _dir(a, b):
        return ((b[0] > a[0]) - (b[0] < a[0]), (b[1] > a[1]) - (b[1] < a[1]))

    def _recortar(self, ruta, r):
        ruta = [tuple(p) for p in ruta]
        dx, dy = self._dir(ruta[-2], ruta[-1])
        x, y = ruta[-1]
        return ruta[:-1] + [(x - dx * r, y - dy * r)]

    def _lado(self, ruta):
        return {(0, 1): "top", (0, -1): "bottom", (1, 0): "left", (-1, 0): "right"}[self._dir(ruta[-2], ruta[-1])]

    def _linea(self, pts, saltos=()):
        d = f"M{pts[0][0]} {pts[0][1]}"
        for a, b in zip(pts, pts[1:]):
            dx, dy = self._dir(a, b)
            en_tramo = [s for s in saltos if
                        (dx == 0 and s[0] == a[0] and min(a[1], b[1]) + RJ < s[1] < max(a[1], b[1]) - RJ) or
                        (dy == 0 and s[1] == a[1] and min(a[0], b[0]) + RJ < s[0] < max(a[0], b[0]) - RJ)]
            en_tramo.sort(key=lambda s: abs(s[0] - a[0]) + abs(s[1] - a[1]))
            for sx, sy in en_tramo:
                d += (f" L{sx - dx * RJ} {sy - dy * RJ}"
                      f" A{RJ} {RJ} 0 0 1 {sx + dx * RJ} {sy + dy * RJ}")
            d += f" L{b[0]} {b[1]}"
        self.lineas.append(f'<path d="{d}" fill="none" stroke="#e5e5e5" stroke-width="1.2"/>')

    def _puerto(self, x, y):
        self.formas.append(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" fill="#000" stroke="#fff" stroke-width="1.2"/>')

    def _enchufe(self, c, lado):
        cx, cy, r = c[0], c[1], RS
        d = {"top": f"M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}",
             "bottom": f"M{cx - r} {cy} A{r} {r} 0 0 0 {cx + r} {cy}",
             "left": f"M{cx} {cy - r} A{r} {r} 0 0 0 {cx} {cy + r}",
             "right": f"M{cx} {cy - r} A{r} {r} 0 0 1 {cx} {cy + r}"}[lado]
        self.formas.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="1.4"/>')

    def _texto(self, x, y, texto, anchor="start"):
        for i, t in enumerate([texto] if isinstance(texto, str) else texto):
            self.textos.append(f'<text class="ifc" x="{x}" y="{y + i * 15}" text-anchor="{anchor}">{escape(t)}</text>')

    def _leyenda(self):
        y = self.H - 40
        bola = lambda x: self.formas.append(f'<circle cx="{x}" cy="{y}" r="{RB}" fill="#000" stroke="#fff" stroke-width="1.4"/>')
        bola(60); self._texto(74, y + 4, "Interfaz provista")
        self._enchufe((210, y + 5), "top"); self._texto(228, y + 4, "Interfaz requerida")
        self._puerto(370, y); self._texto(384, y + 4, "Puerto")
        self._enchufe((460, y), "left"); bola(460); self._texto(480, y + 4, "Conector de ensamble")
        self._enchufe((680, y), "left"); self._enchufe((680, y), "right"); bola(680)
        self._texto(700, y + 4, "Interfaz compartida")
        self._linea([(860, y), (920, y)], saltos=[(890, y)]); self._texto(932, y + 4, "Cruce sin conexión")
