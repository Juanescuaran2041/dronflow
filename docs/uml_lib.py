"""uml_lib.py - diagramas UML (clases, paquetes, despliegue) en SVG con la notación de Visual Paradigm."""
from html import escape
import math

CW, CWB, LH = 6.3, 7.3, 16  # ancho medio de carácter (normal, negrita) y alto de línea
NAVY, TEAL = "#1a2340", "#0f8a8a"
FILL_CLASS, FILL_NODE, FILL_ART, FILL_PKG, FILL_NOTE = "#fffde8", "#eef2f8", "#ffffff", "#f3f7ee", "#fffbd0"


class Diagrama:
    def __init__(self, titulo):
        self.titulo = titulo
        self.cajas = {}           # id -> (x, y, w, h)
        self.fondo, self.frente, self.lineas = [], [], []
        self.fill_clase, self.borde_clase = FILL_CLASS, "#333"

    # ------------------------------------------------------------ clases
    def clase(self, cid, nombre, estereotipo=None, atributos=(), operaciones=(), x=0, y=0,
              abstracta=False, plantilla=None, simple=False, ancho=None):
        """Tres compartimentos (nombre, atributos, operaciones), como en VP.
        simple=True: un solo compartimento (atributos y operaciones suprimidos, opción de VP)."""
        cab = ([f"«{estereotipo}»"] if estereotipo else []) + [nombre]
        w = ancho or (max([len(nombre) * CWB] + [len(t) * CW for t in cab[:-1] + list(atributos) + list(operaciones)]) + 24)
        h_cab = 10 + LH * len(cab)
        h_at = 0 if simple else max(10, 8 + LH * len(atributos))
        h_op = 0 if simple else max(10, 8 + LH * len(operaciones))
        self.cajas[cid] = [x, y, w, h_cab + h_at + h_op]
        self._pend = getattr(self, "_pend", [])
        self._pend.append(("clase", cid, cab, atributos, operaciones, h_cab, h_at, abstracta, plantilla))
        return cid

    def _dibujar_clase(self, cid, cab, atributos, operaciones, h_cab, h_at, abstracta, plantilla):
        x, y, w, h = self.cajas[cid]
        s = self.frente
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{self.fill_clase}" stroke="{self.borde_clase}"/>')
        for i, t in enumerate(cab):
            ultimo = i == len(cab) - 1
            estilo = 'class="nm"' + (' font-style="italic"' if ultimo and abstracta else '') if ultimo else 'class="st"'
            s.append(f'<text {estilo} x="{x + w / 2}" y="{y + 18 + i * LH}" text-anchor="middle">{escape(t)}</text>')
        y1 = y + h_cab
        if h_at:
            s.append(f'<line x1="{x}" y1="{y1}" x2="{x + w}" y2="{y1}" stroke="{self.borde_clase}"/>')
        for i, t in enumerate(atributos):
            s.append(f'<text class="mb" x="{x + 8}" y="{y1 + 17 + i * LH}">{escape(t)}</text>')
        y2 = y1 + h_at
        if h_at:  # en modo simple (un solo compartimento) no hay separadores
            s.append(f'<line x1="{x}" y1="{y2}" x2="{x + w}" y2="{y2}" stroke="{self.borde_clase}"/>')
        for i, t in enumerate(operaciones):
            s.append(f'<text class="mb" x="{x + 8}" y="{y2 + 17 + i * LH}">{escape(t)}</text>')
        if plantilla:  # parámetros de plantilla: rectángulo punteado en la esquina superior derecha
            pw = len(plantilla) * CW + 14
            s.append(f'<rect x="{x + w - pw + 10}" y="{y - 12}" width="{pw}" height="20" fill="#fff" stroke="#333" stroke-dasharray="4 3"/>')
            s.append(f'<text class="mb" x="{x + w - pw / 2 + 10}" y="{y + 3}" text-anchor="middle">{escape(plantilla)}</text>')

    # ------------------------------------------------------------ paquetes, notas
    def marco(self, mid, titulo, x, y, w, h):
        """Marco de capa (como en el material del curso): rectángulo con el título centrado arriba."""
        self.cajas[mid] = [x, y, w, h]
        self.fondo.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffde" stroke="#aaaa33"/>')
        self.fondo.append(f'<text class="mb" x="{x + w / 2}" y="{y + 17}" text-anchor="middle">{escape(titulo)}</text>')
        return mid

    def paquete(self, pid, nombre, x, y, w=160, h=70, contenedor=False, estereotipo=None):
        """Paquete UML (carpeta con pestaña). contenedor=True: el nombre va arriba a la izquierda
        y el cuerpo queda libre para dibujar dentro las clases que contiene (como en VP)."""
        self.cajas[pid] = [x, y, w, h]
        tw = max(60, len(nombre) * CWB * 0.6)
        capa = self.fondo if contenedor else self.frente
        capa.append(f'<path d="M{x} {y} v-14 h{tw} v14 z" fill="{FILL_PKG}" stroke="#333"/>')  # pestaña de carpeta
        capa.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{FILL_PKG}" stroke="#333"/>')
        if contenedor:
            if estereotipo:
                capa.append(f'<text class="st" x="{x + 12}" y="{y + 18}">{escape("«" + estereotipo + "»")}</text>')
            capa.append(f'<text class="nm" x="{x + 12}" y="{y + (36 if estereotipo else 22)}">{escape(nombre)}</text>')
        else:
            capa.append(f'<text class="nm" x="{x + w / 2}" y="{y + h / 2 + 5}" text-anchor="middle">{escape(nombre)}</text>')
        return pid

    def nota(self, nid, lineas, x, y):
        w = max(len(t) for t in lineas) * CW + 26
        h = 12 + LH * len(lineas)
        self.cajas[nid] = [x, y, w, h]
        self.frente.append(f'<path d="M{x} {y} h{w - 12} l12 12 v{h - 12} h-{w} z M{x + w - 12} {y} v12 h12" fill="{FILL_NOTE}" stroke="#333"/>')
        for i, t in enumerate(lineas):
            self.frente.append(f'<text class="mb" x="{x + 10}" y="{y + 19 + i * LH}">{escape(t)}</text>')
        return nid

    # ------------------------------------------------------------ despliegue
    def nodo(self, nid, nombre, estereotipo, x, y, w, h, prof=12, centrado=False):
        """Nodo UML (cubo 3D): «estereotipo» y debajo el nombre.
        centrado=True: etiqueta centrada arriba, como la dibuja Visual Paradigm."""
        self.cajas[nid] = [x, y, w, h]
        f = self.fondo
        f.append(f'<path d="M{x} {y} l{prof} -{prof} h{w} v{h} l-{prof} {prof}" fill="#dfe3ea" stroke="{NAVY}" stroke-width="1.4"/>')
        f.append(f'<path d="M{x + w} {y} l{prof} -{prof}" stroke="{NAVY}" stroke-width="1.4"/>')
        f.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{NAVY}" stroke-width="1.4"/>')
        tx, anc = (x + w / 2, "middle") if centrado else (x + 16, "start")
        f.append(f'<text class="dst" x="{tx}" y="{y + 22}" text-anchor="{anc}">{escape("«" + estereotipo + "»")}</text>')
        for i, t in enumerate(nombre.split("\n")):
            f.append(f'<text class="dnm" x="{tx}" y="{y + 42 + i * 19}" text-anchor="{anc}">{escape(t)}</text>')
        return nid

    def artefacto(self, aid, nombre, x, y, w=220, centrado=False):
        """«artifact»: rectángulo con el icono de documento arriba a la derecha (notación de VP)."""
        lineas = nombre.split("\n")
        h = 34 + 19 * len(lineas)
        self.cajas[aid] = [x, y, w, h]
        f = self.fondo
        f.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{NAVY}" stroke-width="1.4"/>')
        ix, iy = x + w - 26, y + 8  # icono de artefacto: hoja con la esquina doblada
        f.append(f'<path d="M{ix} {iy} h10 l5 5 v12 h-15 z M{ix + 10} {iy} v5 h5" fill="#fff" stroke="{NAVY}" stroke-width="1.1"/>')
        tx, anc = (x + w / 2, "middle") if centrado else (x + 14, "start")
        f.append(f'<text class="dst" x="{tx}" y="{y + 20}" text-anchor="{anc}">«artifact»</text>')
        for i, t in enumerate(lineas):
            f.append(f'<text class="dnm" x="{tx}" y="{y + 40 + i * 19}" text-anchor="{anc}">{escape(t)}</text>')
        return aid

    # ------------------------------------------------------------ relaciones
    def asociacion(self, a, b, rol=None, mult=None, via=(), etiqueta=None):
        """Asociación navegable a -> b: línea continua, flecha abierta; rol y multiplicidad en el extremo b."""
        self._rel(a, b, via, punta="abierta", etiqueta=etiqueta, fin=(rol, mult))

    def dependencia(self, a, b, etiqueta=None, via=()):
        self._rel(a, b, via, punta="abierta", guion=True, etiqueta=etiqueta)

    def generalizacion(self, a, b, via=()):
        self._rel(a, b, via, punta="triangulo")

    def realizacion(self, a, b, etiqueta=None, via=()):
        self._rel(a, b, via, punta="triangulo", guion=True, etiqueta=etiqueta)

    def ruta(self, a, b, etiqueta=None, via=(), guion=False, flecha=True):
        """Ruta de comunicación entre nodos: línea continua con el protocolo y el puerto.
        La flecha abierta marca el extremo navegable (quien atiende la conexión): en VP es
        clic derecho sobre el extremo → Navigable."""
        self._rel(a, b, via, punta="abierta" if flecha else None, guion=guion, etiqueta=etiqueta)

    def ancla(self, nota, b):
        self._rel(nota, b, (), punta=None, guion=True)

    def _rel(self, a, b, via, punta, guion=False, etiqueta=None, fin=(None, None)):
        self._pend = getattr(self, "_pend", [])
        self._pend.append(("rel", a, b, list(via), punta, guion, etiqueta, fin))

    @staticmethod
    def _centro(c):
        return (c[0] + c[2] / 2, c[1] + c[3] / 2)

    @staticmethod
    def _borde(c, hacia):
        """Punto donde la recta centro->hacia sale del rectángulo c."""
        cx, cy = c[0] + c[2] / 2, c[1] + c[3] / 2
        dx, dy = hacia[0] - cx, hacia[1] - cy
        if dx == 0 and dy == 0:
            return cx, cy
        t = min((c[2] / 2) / abs(dx) if dx else math.inf, (c[3] / 2) / abs(dy) if dy else math.inf)
        return cx + dx * t, cy + dy * t

    def _dibujar_rel(self, a, b, via, punta, guion, etiqueta, fin):
        ca, cb = self.cajas[a], self.cajas[b]
        pts = [self._borde(ca, via[0] if via else self._centro(cb))] + via + \
              [self._borde(cb, via[-1] if via else self._centro(ca))]
        self._extra = getattr(self, "_extra", []) + pts
        d = "M" + " L".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts)
        marca = {"abierta": ' marker-end="url(#abierta)"', "llena": ' marker-end="url(#llena)"', "triangulo": ' marker-end="url(#triangulo)"', None: ""}[punta]
        dash = ' stroke-dasharray="7 4"' if guion else ""
        self.lineas.append(f'<path d="{d}" fill="none" stroke="#333" stroke-width="1.2"{dash}{marca}/>')
        if isinstance(etiqueta, tuple):  # (texto, (x, y)): posición explícita
            etiqueta, (mx, my) = etiqueta
            self._etiqueta(mx, my, etiqueta)
        elif etiqueta:  # en el centro del tramo más largo
            i = max(range(len(pts) - 1), key=lambda k: math.dist(pts[k], pts[k + 1]))
            mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
            self._etiqueta(mx, my, etiqueta)
        rol, mult = fin
        if rol or mult:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            L = math.dist(pts[-2], pts[-1]) or 1
            ux, uy = (x2 - x1) / L, (y2 - y1) / L
            if abs(ux) >= abs(uy):  # tramo horizontal: rol encima, multiplicidad debajo, antes del borde
                ex = x2 - ux * 10
                ancla = "end" if ux > 0 else "start"
                if rol:
                    self._etiqueta(ex, y2 - uy * 10 - 10, rol, fondo=False, ancla=ancla)
                if mult:
                    self._etiqueta(ex, y2 - uy * 10 + 12, mult, fondo=False, ancla=ancla)
            else:  # tramo vertical: rol a la derecha, multiplicidad a la izquierda
                ey = y2 - uy * 14
                if rol:
                    self._etiqueta(x2 - ux * 14 + 7, ey, rol, fondo=False, ancla="start")
                if mult:
                    self._etiqueta(x2 - ux * 14 - 7, ey, mult, fondo=False, ancla="end")

    def _etiqueta(self, x, y, texto, fondo=True, ancla="middle"):
        lineas = texto.split("\n")
        if fondo:
            w = max(len(t) for t in lineas) * CW + 8
            h = LH * len(lineas) + 2
            self.frente.append(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="#fff" opacity="0.92"/>')
        for i, t in enumerate(lineas):
            yy = y + 4 + (i - (len(lineas) - 1) / 2) * LH
            self.frente.append(f'<text class="mb" x="{x}" y="{yy}" text-anchor="{ancla}">{escape(t)}</text>')

    # ------------------------------------------------------------ disposición
    def columnas(self, cols, x0=40, y0=70, gap_x=200, gap_y=40):
        """Coloca cajas ya creadas en columnas, cada columna centrada verticalmente.
        gap_x puede ser una lista: separación después de cada columna."""
        gaps = gap_x if isinstance(gap_x, list) else [gap_x] * len(cols)
        alto = [sum(self.cajas[c][3] for c in col) + gap_y * (len(col) - 1) for col in cols]
        H = max(alto)
        x = x0
        for col, a, gap in zip(cols, alto, gaps):
            y = y0 + (H - a) / 2
            w = max(self.cajas[c][2] for c in col)
            for c in col:
                self.cajas[c][0] = x + (w - self.cajas[c][2]) / 2
                self.cajas[c][1] = y
                y += self.cajas[c][3] + gap_y
            x += w + gap

    # ------------------------------------------------------------ salida
    def guardar(self, ruta):
        for p in getattr(self, "_pend", []):
            (self._dibujar_clase if p[0] == "clase" else self._dibujar_rel)(*p[1:])
        xs = [c[0] + c[2] for c in self.cajas.values()] + [p[0] + 20 for p in getattr(self, "_extra", [])]
        ys = [c[1] + c[3] for c in self.cajas.values()] + [p[1] + 20 for p in getattr(self, "_extra", [])]
        W, H = int(max(xs) + 60), int(max(ys) + 50)
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial, Helvetica, sans-serif">
<defs>
  <marker id="abierta" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M1 1 L11 6 L1 11" fill="none" stroke="#333" stroke-width="1.2"/></marker>
  <marker id="triangulo" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M1 1 L15 8 L1 15 z" fill="#fff" stroke="#333" stroke-width="1.2"/></marker>
  <marker id="llena" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse" markerUnits="userSpaceOnUse"><path d="M1 1 L11 6 L1 11 z" fill="#1a2340"/></marker>
  <style>.dst{{font-size:13px;fill:#1a2340}} .dnm{{font-size:16px;fill:#1a2340}} .nm{{font-size:13px;font-weight:bold;fill:#111}} .st{{font-size:12px;fill:#333}} .mb{{font-size:12px;fill:#111}} .tt{{font-size:15px;font-weight:bold;fill:#111}}</style>
</defs>
<rect width="{W}" height="{H}" fill="#fff"/>
<text class="tt" x="20" y="28">{escape(self.titulo)}</text>
{chr(10).join(self.fondo + self.lineas + self.frente)}
</svg>
'''
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(svg)
