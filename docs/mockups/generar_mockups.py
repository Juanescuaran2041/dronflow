"""Mockups de Dronflow: un .drawio (XML de draw.io con la librería mxgraph.mockup) y un .svg por HU.
Uso: python generar_mockups.py <carpeta_salida>
El .drawio se abre en draw.io (Extras → Edit Diagram, o Archivo → Abrir). El .svg es la misma
pantalla dibujada para verla sin draw.io (en la wiki se publica como PNG)."""
import os
import sys
from html import escape

W, H = 1000, 700            # ventana del navegador
NAV_Y, NAV_H = 110, 50      # navbar (debajo del cromo del navegador)
TOP = NAV_Y + NAV_H         # el contenido empieza aquí
SIDE_W = 190
NAVY, TEAL, SIDE, MUTED = "#1a2340", "#0f8a8a", "#e8f3f3", "#666666"
SEV = {"Baja": ("#e8f5e9", "#2e7d32"), "Media": ("#fff8e1", "#b26a00"),
       "Alta": ("#fff1e6", "#d9480f"), "Crítica": ("#fdecea", "#c62828")}
EST = {"Disponible": ("#e8f5e9", "#2e7d32"), "En misión": ("#e3f2fd", "#1565c0"),
       "Cargando": ("#fff8e1", "#b26a00"), "En mantenimiento": ("#f3e5f5", "#6a1b9a"),
       "Fuera de servicio": ("#fdecea", "#c62828"), "Pendiente": ("#f5f5f5", "#555555"),
       "En curso": ("#e3f2fd", "#1565c0"), "Finalizada": ("#e8f5e9", "#2e7d32"),
       "Abortada": ("#fdecea", "#c62828"), "Pausada": ("#fff8e1", "#b26a00"),
       "Activo": ("#e8f5e9", "#2e7d32")}

MENU_ADMIN = ["Panel de control", "Flota", "Historial de misiones", "Alertas", "Mantenimiento",
              "Configuración", "Usuarios"]
MENU_OPER = ["Flota", "Misiones", "Mantenimiento"]


class Mockup:
    def __init__(self, hu, titulo):
        self.hu, self.titulo = hu, titulo
        self.cells, self.svg, self.n = [], [], 0

    # ------------------------------------------------------------ bajo nivel
    def _id(self, base):
        self.n += 1
        return f"{base}-{self.n}"

    def cell(self, base, style, value, x, y, w, h, svg):
        v = escape(value, quote=True) if value else ""
        self.cells.append(f'<mxCell id="{self._id(base)}" parent="browser-1" style="{style}" value="{v}" vertex="1">'
                          f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>')
        self.svg.append(svg)

    @staticmethod
    def _t(x, y, txt, size=12, color="#333333", anchor="start", bold=False):
        b = ' font-weight="bold"' if bold else ""
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"{b}>{escape(txt)}</text>'

    # ------------------------------------------------------------ componentes (estilos de la skill)
    def rect(self, x, y, w, h, fill, stroke="none", value="", font="#333333", size=12, align="center", bold=False):
        st = (f"rounded=0;whiteSpace=wrap;html=1;strokeColor={stroke};fillColor={fill};fontColor={font};"
              f"align={align};fontSize={size};" + ("fontStyle=1;" if bold else "") + ("spacingLeft=10;" if align == "left" else ""))
        tx = x + 10 if align == "left" else x + w / 2
        svg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'
        if value:
            svg += self._t(tx, y + h / 2 + size / 3, value, size, font, "start" if align == "left" else "middle", bold)
        self.cell("rect", st, value, x, y, w, h, svg)

    def texto(self, x, y, w, txt, size=12, color=MUTED, bold=False, align="left"):
        st = (f"strokeWidth=1;shadow=0;dashed=0;html=1;shape=mxgraph.mockup.forms.anchor;fontSize={size};"
              f"fontColor={color};align={align};" + ("fontStyle=1;" if bold else ""))
        ax = {"left": x, "center": x + w / 2, "right": x + w}[align]
        an = {"left": "start", "center": "middle", "right": "end"}[align]
        self.cell("txt", st, txt, x, y, w, size + 8, self._t(ax, y + size + 1, txt, size, color, an, bold))

    def titulo_seccion(self, x, y, txt, w=400):
        self.texto(x, y, w, txt, 18, "#000000", bold=True)

    def campo(self, x, y, w, etiqueta, valor, select=False, placeholder=False):
        self.texto(x, y, w, etiqueta, 12, MUTED)
        st = ("strokeWidth=1;shadow=0;dashed=0;html=1;shape=mxgraph.mockup.forms.rrect;rSize=0;strokeColor=#999999;"
              f"fontColor={'#aaaaaa' if placeholder else '#333333'};align=left;spacingLeft=5;")
        svg = (f'<rect x="{x}" y="{y + 20}" width="{w}" height="28" fill="#fff" stroke="#999999"/>'
               + self._t(x + 7, y + 38, valor, 12, "#aaaaaa" if placeholder else "#333333"))
        if select:
            svg += f'<path d="M{x + w - 18} {y + 31} l5 6 l5 -6" fill="none" stroke="#666" stroke-width="1.5"/>'
        self.cell("input", st, valor + ("   ▾" if select else ""), x, y + 20, w, 28, svg)

    def boton(self, x, y, w, txt, tipo="primario", h=32, deshabilitado=False):
        if tipo == "primario":
            fill, stroke, font = ("#b0b6c3" if deshabilitado else NAVY), "none", "#ffffff"
        elif tipo == "peligro":
            fill, stroke, font = "#c62828", "none", "#ffffff"
        else:
            fill, stroke, font = "#ffffff", "#999999", ("#aaaaaa" if deshabilitado else "#333333")
        st = (f"strokeWidth=1;shadow=0;dashed=0;align=center;html=1;shape=mxgraph.mockup.forms.rrect;rSize=5;"
              f"strokeColor={stroke};fontColor={font};fillColor={fill};fontSize=13;" + ("fontStyle=1;" if tipo != "secundario" else ""))
        svg = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}"/>'
               + self._t(x + w / 2, y + h / 2 + 4, txt, 13, font, "middle", tipo != "secundario"))
        self.cell("btn", st, txt, x, y, w, h, svg)

    def mensaje(self, x, y, w, txt, tipo="error", h=40):
        colores = {"error": ("#fdecea", "#f5b5b0", "#c62828"), "ok": ("#e8f5e9", "#a5d6a7", "#2e7d32"),
                   "info": ("#e3f2fd", "#90caf9", "#1565c0"), "aviso": ("#fff5f0", "#f5c6a0", "#cc6600")}
        fill, stroke, font = colores[tipo]
        st = (f"strokeWidth=1;shadow=0;dashed=0;align=left;spacingLeft=12;html=1;shape=mxgraph.mockup.forms.rrect;"
              f"rSize=0;strokeColor={stroke};fillColor={fill};fontColor={font};fontSize=13;whiteSpace=wrap;")
        svg = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'
               + self._t(x + 12, y + h / 2 + 5, txt, 13, font))
        self.cell("msg", st, txt, x, y, w, h, svg)

    def insignia(self, x, y, txt, colores, w=None):
        fill, font = colores
        w = w or len(txt) * 7 + 18
        st = (f"strokeWidth=1;shadow=0;dashed=0;align=center;html=1;shape=mxgraph.mockup.forms.rrect;rSize=10;"
              f"strokeColor=none;fillColor={fill};fontColor={font};fontSize=11;fontStyle=1;")
        svg = (f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="10" fill="{fill}"/>'
               + self._t(x + w / 2, y + 14, txt, 11, font, "middle", True))
        self.cell("badge", st, txt, x, y, w, 20, svg)

    def tabla(self, x, y, anchos, encabezado, filas, alto_fila=34):
        """Tabla: encabezado oscuro y filas; una celda puede ser ('badge', texto, colores) o ('btn', texto)."""
        cx = x
        for a, e in zip(anchos, encabezado):
            self.rect(cx, y, a, alto_fila, "#f0f2f5", "#d0d4db", e, "#333333", 12, "left", True)
            cx += a
        for i, fila in enumerate(filas):
            fy = y + alto_fila * (i + 1)
            cx = x
            for a, c in zip(anchos, fila):
                if isinstance(c, tuple):
                    self.rect(cx, fy, a, alto_fila, "#ffffff", "#e3e6ea")
                    if c[0] == "badge":
                        self.insignia(cx + 8, fy + 7, c[1], c[2])
                    elif c[0] == "btn":
                        self.boton(cx + 8, fy + 5, a - 16, c[1], c[2] if len(c) > 2 else "secundario", h=24)
                    elif c[0] == "btns":  # varios botones en la misma celda
                        bw = (a - 8) / len(c[1]) - 8
                        for k, (txt, tipo) in enumerate(c[1]):
                            self.boton(cx + 8 + k * (bw + 8), fy + 5, bw, txt, tipo, h=24)
                else:
                    self.rect(cx, fy, a, alto_fila, "#ffffff", "#e3e6ea", c, "#333333", 12, "left")
                cx += a

    def tarjeta(self, x, y, w, h, etiqueta, valor, colores):
        fill, font = colores
        self.rect(x, y, w, h, fill, "#d0d4db")
        self.texto(x + 14, y + 12, w - 28, etiqueta, 12, font, bold=True)
        self.texto(x + 14, y + 38, w - 28, valor, 30, "#111111", bold=True)

    def mapa(self, x, y, w, h, ruta, zona=None, dron=None, desvio=None):
        """Marcador de mapa: ruta planificada (línea), zona restringida (rojo) y posición del dron."""
        self.rect(x, y, w, h, "#eef3ec", "#c9d3c5")
        self.texto(x + 10, y + 6, 200, "Mapa (ruta planificada)", 11, "#7a8a74")
        if zona:
            zx, zy, zw, zh, nom = zona
            self.rect(x + zx, y + zy, zw, zh, "#fdecea", "#e57373", nom, "#c62828", 11)
        pts = [(x + px, y + py) for px, py in ruta]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            self.linea(ax, ay, bx, by, TEAL, 3)
        for px, py in (pts[0], pts[-1]):
            self.punto(px, py, TEAL)
        if desvio:
            self.linea(x + desvio[0][0], y + desvio[0][1], x + desvio[1][0], y + desvio[1][1], "#d9480f", 2, True)
        if dron:
            self.punto(x + dron[0], y + dron[1], "#d9480f", 8)

    def linea(self, x1, y1, x2, y2, color, ancho=1, punteada=False):
        dash = "dashed=1;" if punteada else ""
        st = f"endArrow=none;html=1;strokeColor={color};strokeWidth={ancho};{dash}"
        self.cells.append(f'<mxCell id="{self._id("line")}" parent="browser-1" style="{st}" edge="1">'
                          f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="{y1}" as="sourcePoint" />'
                          f'<mxPoint x="{x2}" y="{y2}" as="targetPoint" /></mxGeometry></mxCell>')
        d = ' stroke-dasharray="6 4"' if punteada else ""
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{ancho}"{d}/>')

    def punto(self, x, y, color, r=6):
        st = f"ellipse;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#ffffff;"
        self.cell("dot", st, "", x - r, y - r, 2 * r, 2 * r,
                  f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#fff" stroke-width="2"/>')

    def modal(self, x, y, w, h, contenido_x=SIDE_W):
        st_o = "rounded=0;whiteSpace=wrap;html=1;strokeColor=none;fillColor=#000000;opacity=30;"
        self.cell("overlay", st_o, "", contenido_x, TOP, W - contenido_x, H - TOP,
                  f'<rect x="{contenido_x}" y="{TOP}" width="{W - contenido_x}" height="{H - TOP}" fill="#000" opacity="0.3"/>')
        st = "strokeWidth=1;shadow=1;dashed=0;align=center;html=1;shape=mxgraph.mockup.forms.rrect;rSize=5;strokeColor=#cccccc;fillColor=#ffffff;"
        self.cell("modal", st, "", x, y, w, h, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fff" stroke="#ccc"/>')

    def divisor(self, x, y, w):
        self.cell("div", "shape=line;strokeColor=#dddddd;strokeWidth=1;html=1;", "", x, y, w, 10,
                  f'<line x1="{x}" y1="{y + 5}" x2="{x + w}" y2="{y + 5}" stroke="#ddd"/>')

    def toast(self, x, y, w, titulo, detalle, sev):
        fill, font = SEV[sev]
        self.rect(x, y, w, 64, "#ffffff", "#d0d4db")
        self.rect(x, y, 6, 64, font)
        self.texto(x + 18, y + 8, w - 120, titulo, 13, "#111111", bold=True)
        self.texto(x + 18, y + 34, w - 30, detalle, 12, MUTED)
        self.insignia(x + w - 86, y + 10, sev, SEV[sev], 72)

    # ------------------------------------------------------------ marco de la aplicación
    def app(self, rol, activo, ruta):
        menu = MENU_ADMIN if rol == "Administrador" else MENU_OPER
        self.marco_navegador(ruta)
        self.rect(0, NAV_Y, W, NAV_H, NAVY, NAVY, "     Dronflow", "#ffffff", 16, "left", True)
        self.texto(W - 330, NAV_Y + 16, 180, f"{rol}", 12, "#cfd6e4", align="right")
        st = ("strokeWidth=1;shadow=0;dashed=0;align=center;html=1;shape=mxgraph.mockup.forms.rrect;rSize=3;"
              "strokeColor=#ffffff;fontColor=#ffffff;fillColor=none;fontSize=11;")
        self.cell("logout", st, "Cerrar sesión", W - 130, NAV_Y + 11, 110, 28,
                  f'<rect x="{W - 130}" y="{NAV_Y + 11}" width="110" height="28" rx="3" fill="none" stroke="#fff"/>'
                  + self._t(W - 75, NAV_Y + 29, "Cerrar sesión", 11, "#ffffff", "middle"))
        self.rect(0, TOP, SIDE_W, H - TOP, SIDE)
        for i, item in enumerate(menu):
            on = item == activo
            self.rect(0, TOP + 20 + i * 38, SIDE_W, 36, TEAL if on else SIDE, "none", "  " + item,
                      "#ffffff" if on else "#333333", 13, "left", on)
        return SIDE_W + 30   # x donde empieza el contenido

    def marco_navegador(self, ruta):
        self._ruta = ruta

    # ------------------------------------------------------------ salida
    def guardar(self, carpeta):
        nombre = f"HU-{self.hu:02d}"
        browser = ('<mxCell id="browser-1" parent="1" style="strokeWidth=1;shadow=0;dashed=0;align=center;html=1;'
                   'shape=mxgraph.mockup.containers.browserWindow;rSize=0;strokeColor=#666666;strokeColor2=#008cff;'
                   f'strokeColor3=#c4c4c4;mainText=Dronflow,https://dronflow.local{escape(self._ruta)};recursiveResize=0;" value="" vertex="1">'
                   f'<mxGeometry x="20" y="20" width="{W}" height="{H}" as="geometry" /></mxCell>')
        xml = (f'<mxfile host="app.diagrams.net"><diagram id="{nombre}" name="{nombre} {escape(self.titulo)}">'
               '<mxGraphModel dx="1381" dy="803" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
               f'fold="1" page="1" pageScale="1" pageWidth="{W + 40}" pageHeight="{H + 40}" math="0" shadow="0"><root>'
               '<mxCell id="0" /><mxCell id="1" parent="0" />' + browser + "".join(self.cells)
               + "</root></mxGraphModel></diagram></mxfile>\n")
        with open(os.path.join(carpeta, nombre + ".drawio"), "w", encoding="utf-8") as f:
            f.write(xml)
        cromo = (f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff" stroke="#666"/>'
                 f'<rect x="0" y="0" width="{W}" height="40" fill="#e8eaed"/>'
                 f'<path d="M14 40 v-26 q0 -6 6 -6 h270 q6 0 6 6 v26 z" fill="#fff" stroke="#c4c4c4"/>'
                 + self._t(28, 30, f"Dronflow · {self.titulo}"[:40], 12, "#333")
                 + '<circle cx="24" cy="74" r="7" fill="none" stroke="#999"/><circle cx="48" cy="74" r="7" fill="none" stroke="#999"/>'
                 f'<rect x="70" y="58" width="{W - 90}" height="32" rx="16" fill="#f1f3f4" stroke="#c4c4c4"/>'
                 + self._t(90, 79, f"https://dronflow.local{self._ruta}", 13, "#555")
                 + f'<line x1="0" y1="{NAV_Y - 8}" x2="{W}" y2="{NAV_Y - 8}" stroke="#c4c4c4"/>')
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 40}" height="{H + 40}" '
               f'viewBox="0 0 {W + 40} {H + 40}" font-family="Helvetica, Arial, sans-serif">'
               f'<rect width="{W + 40}" height="{H + 40}" fill="#ffffff"/><g transform="translate(20,20)">'
               + cromo + "".join(self.svg) + "</g></svg>\n")
        with open(os.path.join(carpeta, nombre + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg)


# =================================================================== pantallas
def hu01():
    m = Mockup(1, "Registrar dron"); x = m.app("Operador", "Flota", "/flota/nuevo")
    m.titulo_seccion(x, TOP + 20, "Registrar dron")
    m.mensaje(x, TOP + 58, 700, "La identificación DRN-001 ya está en uso. Ingresa otra identificación.", "error")
    c1, c2 = x, x + 370
    m.campo(c1, TOP + 115, 330, "Identificación", "DRN-001")
    m.campo(c2, TOP + 115, 330, "Tipo de dron", "Entrega", select=True)
    m.campo(c1, TOP + 180, 330, "Capacidad de batería (mAh)", "5000")
    m.campo(c2, TOP + 180, 330, "Autonomía (minutos)", "25")
    m.campo(c1, TOP + 245, 330, "Carga útil máxima (kg)", "2")
    m.campo(c2, TOP + 245, 330, "Equipamiento", "cámara, gancho de carga")
    m.texto(c1, TOP + 312, 700, "Tipos soportados: entrega, inspección, monitoreo/fotografía. El dron queda en estado «disponible».", 11)
    m.boton(c1, TOP + 350, 200, "Registrar dron")
    m.boton(c1 + 215, TOP + 350, 120, "Cancelar", "secundario")
    return m


def hu02():
    m = Mockup(2, "Estado operativo"); x = m.app("Operador", "Flota", "/flota")
    m.titulo_seccion(x, TOP + 20, "Flota de drones")
    m.campo(x, TOP + 50, 220, "Filtrar por estado", "Todos", select=True)
    m.boton(x + 600, TOP + 70, 150, "+ Registrar dron")
    m.tabla(x, TOP + 125, [110, 160, 90, 190, 200], ["Código", "Tipo", "Batería", "Estado", "Acciones"], [
        ["DRN-001", "Entrega", "60 %", ("badge", "Disponible", EST["Disponible"]), ("btn", "Reportar avería")],
        ["DRN-002", "Inspección", "48 %", ("badge", "En misión", EST["En misión"]), ""],
        ["DRN-003", "Monitoreo", "15 %", ("badge", "Cargando", EST["Cargando"]), ""],
        ["DRN-004", "Entrega", "90 %", ("badge", "En mantenimiento", EST["En mantenimiento"]), ""],
        ["DRN-005", "Inspección", "70 %", ("badge", "Fuera de servicio", EST["Fuera de servicio"]), ""]])
    m.texto(x, TOP + 345, 740, "El estado se actualiza solo: al asignar misión, al terminarla (disponible o cargando según la batería) o al reportar avería.", 11)
    return m


def hu03():
    m = Mockup(3, "Baja o reactivación"); x = m.app("Operador", "Flota", "/flota/DRN-005")
    m.titulo_seccion(x, TOP + 20, "Dron DRN-005")
    m.insignia(x + 170, TOP + 24, "Fuera de servicio", EST["Fuera de servicio"])
    for i, (k, v) in enumerate([("Tipo", "Inspección"), ("Batería", "70 %"), ("Autonomía", "30 min"), ("Carga útil", "1 kg")]):
        m.texto(x, TOP + 70 + i * 26, 140, k, 12, MUTED)
        m.texto(x + 150, TOP + 70 + i * 26, 200, v, 12, "#111111")
    m.boton(x, TOP + 190, 150, "Reactivar")
    m.boton(x + 165, TOP + 190, 150, "Dar de baja", "peligro")
    m.modal(x + 150, TOP + 120, 400, 190)
    m.texto(x + 175, TOP + 140, 350, "¿Dar de baja el dron DRN-005?", 15, "#111111", bold=True)
    m.texto(x + 175, TOP + 175, 360, "Es permanente: un dron dado de baja no se puede reactivar.", 12)
    m.texto(x + 175, TOP + 197, 360, "No se permite si el dron está en misión.", 12)
    m.boton(x + 300, TOP + 255, 110, "Cancelar", "secundario")
    m.boton(x + 420, TOP + 255, 110, "Dar de baja", "peligro")
    return m


def hu04():
    m = Mockup(4, "Crear misión"); x = m.app("Operador", "Misiones", "/misiones/nueva")
    m.titulo_seccion(x, TOP + 20, "Crear misión")
    m.mensaje(x, TOP + 58, 700, "El origen y el destino no pueden ser el mismo punto.", "error")
    c1, c2 = x, x + 370
    m.campo(c1, TOP + 115, 330, "Tipo de misión", "Entrega", select=True)
    m.campo(c2, TOP + 115, 330, "Prioridad", "Alta", select=True)
    m.campo(c1, TOP + 180, 330, "Origen", "Bodega Central")
    m.campo(c2, TOP + 180, 330, "Destino", "Cliente Norte")
    m.campo(c1, TOP + 245, 330, "Carga útil requerida (kg)", "1.5")
    m.campo(c2, TOP + 245, 330, "Autonomía mínima (minutos)", "20")
    m.texto(c1, TOP + 312, 700, "Prioridad: baja, media, alta, crítica. La misión se crea en estado «pendiente».", 11)
    m.boton(c1, TOP + 350, 200, "Crear misión")
    m.boton(c1 + 215, TOP + 350, 120, "Cancelar", "secundario")
    return m


def hu05():
    m = Mockup(5, "Asignación automática"); x = m.app("Operador", "Misiones", "/misiones")
    m.titulo_seccion(x, TOP + 20, "Misiones")
    m.boton(x + 600, TOP + 20, 150, "+ Crear misión")
    m.mensaje(x, TOP + 65, 750, "Misión M-001 creada y asignada automáticamente al dron DRN-001.", "ok")
    m.tabla(x, TOP + 125, [90, 110, 100, 170, 130, 150], ["Código", "Tipo", "Prioridad", "Destino", "Dron asignado", "Estado"], [
        ["M-001", "Entrega", "Alta", "Cliente Norte", "DRN-001", ("badge", "Pendiente", EST["Pendiente"])],
        ["M-002", "Inspección", "Media", "Torre 4", "— sin dron —", ("badge", "Pendiente", EST["Pendiente"])],
        ["M-004", "Entrega", "Alta", "Cliente Sur", "DRN-003", ("badge", "En curso", EST["En curso"])]])
    m.mensaje(x, TOP + 280, 750, "M-002 espera un dron compatible: se asignará sola cuando uno quede disponible.", "info")
    m.texto(x, TOP + 335, 750, "Criterios: batería, cercanía y prioridad, con la ponderación que define el administrador (HU-18).", 11)
    return m


def hu06():
    m = Mockup(6, "Validación de ruta"); x = m.app("Operador", "Misiones", "/misiones/M-003")
    m.titulo_seccion(x, TOP + 20, "Misión M-003 · autorizar despegue")
    m.mapa(x, TOP + 60, 470, 300, [(40, 250), (200, 150), (420, 60)], zona=(240, 70, 120, 90, "Zona restringida"))
    px = x + 495
    m.texto(px, TOP + 60, 260, "Dron asignado: DRN-002 (reservado)", 12, "#111111")
    m.texto(px, TOP + 85, 260, "Intento de cálculo de ruta: 1 de 3", 12, MUTED)
    m.mensaje(px, TOP + 120, 265, "Despegue rechazado: la ruta cruza", "error", 36)
    m.texto(px + 12, TOP + 158, 250, "la zona «Aeropuerto». Ajusta la ruta.", 12, "#c62828")
    m.boton(px, TOP + 200, 265, "Validar ruta y despegar")
    m.texto(px, TOP + 245, 265, "Si la ruta no se calcula en 3 intentos,", 11)
    m.texto(px, TOP + 263, 265, "el dron vuelve a disponible y la misión", 11)
    m.texto(px, TOP + 281, 265, "queda pendiente.", 11)
    return m


def hu07():
    m = Mockup(7, "Seguimiento de misión"); x = m.app("Operador", "Misiones", "/misiones/M-001")
    m.titulo_seccion(x, TOP + 20, "Misión M-001 · seguimiento")
    pasos = ["Pendiente", "Despegue", "En curso", "Retorno", "Finalizada"]
    for i, p in enumerate(pasos):
        cx = x + 40 + i * 170
        if i:
            m.linea(cx - 140, TOP + 82, cx - 12, TOP + 82, TEAL if i <= 2 else "#cccccc", 3)
        m.punto(cx, TOP + 82, TEAL if i <= 2 else "#cccccc", 11)
        m.texto(cx - 60, TOP + 100, 120, p, 12, "#111111" if i == 2 else MUTED, bold=i == 2, align="center")
    m.texto(x, TOP + 130, 750, "También puede quedar «pausada» o «abortada» (HU-08).", 11)
    m.mapa(x, TOP + 160, 470, 220, [(40, 180), (220, 110), (430, 40)], dron=(220, 110))
    px = x + 495
    for i, (k, v) in enumerate([("Dron", "DRN-001"), ("Destino", "Cliente Norte"), ("Batería", "54 %"),
                                ("Despegue", "10:42"), ("Estado", "En curso")]):
        m.texto(px, TOP + 165 + i * 28, 110, k, 12, MUTED)
        m.texto(px + 110, TOP + 165 + i * 28, 150, v, 12, "#111111", bold=k == "Estado")
    return m


def hu08():
    m = Mockup(8, "Intervención manual"); x = m.app("Operador", "Misiones", "/misiones/M-001")
    m.titulo_seccion(x, TOP + 20, "Misión M-001")
    m.insignia(x + 150, TOP + 24, "En curso", EST["En curso"])
    m.texto(x, TOP + 60, 500, "Destino actual: Cliente Norte · Dron DRN-001 · Batería 54 %", 12, "#111111")
    m.boton(x, TOP + 95, 130, "Pausar")
    m.boton(x + 145, TOP + 95, 130, "Reanudar", "secundario", deshabilitado=True)
    m.boton(x + 290, TOP + 95, 130, "Redirigir", "secundario")
    m.boton(x + 435, TOP + 95, 130, "Abortar", "peligro")
    m.modal(x + 150, TOP + 160, 420, 220)
    m.texto(x + 175, TOP + 180, 360, "Redirigir misión M-001", 15, "#111111", bold=True)
    m.campo(x + 175, TOP + 215, 370, "Nuevo destino", "Cliente Sur")
    m.texto(x + 175, TOP + 275, 370, "La misión sigue en curso hacia el nuevo destino.", 12)
    m.boton(x + 315, TOP + 325, 110, "Cancelar", "secundario")
    m.boton(x + 435, TOP + 325, 110, "Redirigir")
    return m


def detalle_alerta(m, x, titulo, sev, filas):
    m.titulo_seccion(x, TOP + 20, titulo)
    m.insignia(x + 10 + len(titulo) * 10, TOP + 24, sev, SEV[sev], 72)
    for i, (k, v) in enumerate(filas):
        m.texto(x, TOP + 70 + i * 28, 170, k, 12, MUTED)
        m.texto(x + 170, TOP + 70 + i * 28, 300, v, 12, "#111111")


def hu09():
    m = Mockup(9, "Alerta de batería baja"); x = m.app("Administrador", "Alertas", "/alertas/A-1031")
    detalle_alerta(m, x, "Alerta: batería baja", "Media", [
        ("Dron", "DRN-001"), ("Misión", "M-001 (en curso)"), ("Batería actual", "19 %"),
        ("Umbral configurado", "20 %"), ("Generada", "18/11/2026 10:58:03")])
    m.rect(x, TOP + 230, 500, 26, "#eeeeee", "#cccccc")
    m.rect(x, TOP + 230, 95, 26, "#e65100", "none", "19 %", "#ffffff", 12)
    m.linea(x + 100, TOP + 224, x + 100, TOP + 262, "#333333", 2, True)
    m.texto(x + 105, TOP + 264, 200, "umbral 20 %", 11)
    m.mensaje(x, TOP + 300, 740, "Cada lectura por debajo del umbral genera una nueva alerta (18 % → otra alerta).", "aviso")
    m.boton(x, TOP + 360, 160, "Ver misión")
    return m


def hu10():
    m = Mockup(10, "Alerta de desvío o zona"); x = m.app("Administrador", "Alertas", "/alertas/A-1032")
    m.titulo_seccion(x, TOP + 20, "Alerta: ingreso a zona restringida")
    m.insignia(x + 360, TOP + 24, "Crítica", SEV["Crítica"], 72)
    m.mapa(x, TOP + 60, 470, 300, [(40, 250), (200, 170), (430, 60)], zona=(250, 180, 130, 90, "Zona restringida"),
           dron=(300, 215), desvio=((200, 170), (300, 215)))
    px = x + 495
    for i, (k, v) in enumerate([("Dron", "DRN-002"), ("Misión", "M-004"), ("Zona", "Aeropuerto"),
                                ("Generada", "10:59:41")]):
        m.texto(px, TOP + 65 + i * 28, 90, k, 12, MUTED)
        m.texto(px + 90, TOP + 65 + i * 28, 170, v, 12, "#111111")
    m.divisor(px, TOP + 185, 265)
    m.texto(px, TOP + 205, 265, "Otra alerta del mismo tipo:", 12, MUTED)
    m.texto(px, TOP + 228, 265, "Desvío de ruta: 60 m (umbral 50 m)", 12, "#111111")
    m.insignia(px, TOP + 255, "Alta", SEV["Alta"], 72)
    return m


def hu11():
    m = Mockup(11, "Notificación en tiempo real"); x = m.app("Administrador", "Panel de control", "/panel")
    m.titulo_seccion(x, TOP + 20, "Panel de control")
    for i, (k, v) in enumerate([("Disponibles", "12"), ("En misión", "5"), ("Mantenim.", "2")]):
        m.tarjeta(x + i * 125, TOP + 65, 115, 90, k, v, ("#f7f8fa", "#555555"))
    m.toast(W - 400, TOP + 15, 380, "Nueva alerta · Zona restringida", "DRN-002 entró a «Aeropuerto» · hace 1 s", "Crítica")
    m.toast(W - 400, TOP + 90, 380, "Nueva alerta · Batería baja", "DRN-001 con 19 % de batería", "Media")
    m.toast(W - 400, TOP + 165, 380, "Mantenimiento recomendado", "DRN-004 superó 100 h de vuelo", "Baja")
    m.texto(x, TOP + 280, 380, "Las alertas llegan en menos de 1 segundo, solo en pantalla,", 11)
    m.texto(x, TOP + 298, 380, "a los administradores con sesión activa (sin correo ni SMS).", 11)
    return m


def hu12():
    m = Mockup(12, "Severidad de alertas"); x = m.app("Administrador", "Alertas", "/alertas")
    m.titulo_seccion(x, TOP + 20, "Alertas")
    m.campo(x, TOP + 50, 200, "Severidad", "Todas", select=True)
    m.campo(x + 220, TOP + 50, 200, "Tipo", "Todos", select=True)
    m.tabla(x, TOP + 125, [110, 220, 100, 100, 210], ["Severidad", "Tipo", "Dron", "Misión", "Generada"], [
        [("badge", "Crítica", SEV["Crítica"]), "Ingreso a zona restringida", "DRN-002", "M-004", "18/11 10:59"],
        [("badge", "Alta", SEV["Alta"]), "Desvío de ruta (60 m)", "DRN-002", "M-004", "18/11 10:57"],
        [("badge", "Media", SEV["Media"]), "Batería baja (19 %)", "DRN-001", "M-001", "18/11 10:58"],
        [("badge", "Baja", SEV["Baja"]), "Mantenimiento recomendado", "DRN-004", "—", "18/11 09:12"]])
    m.texto(x, TOP + 310, 740, "La severidad la asigna el sistema según el tipo de alerta; alta y crítica cuentan como incidencias.", 11)
    return m


def hu13():
    m = Mockup(13, "Historial de vuelos"); x = m.app("Operador", "Flota", "/flota/DRN-001/historial")
    m.titulo_seccion(x, TOP + 20, "Historial de vuelos · DRN-001")
    m.tarjeta(x, TOP + 60, 230, 90, "Horas de vuelo", "105 h", ("#f7f8fa", "#555555"))
    m.tarjeta(x + 250, TOP + 60, 230, 90, "Misiones completadas", "40", ("#f7f8fa", "#555555"))
    m.tarjeta(x + 500, TOP + 60, 230, 90, "Incidencias", "2", ("#fdecea", "#c62828"))
    m.texto(x, TOP + 170, 400, "Incidencias (alertas altas o críticas)", 13, "#111111", bold=True)
    m.tabla(x, TOP + 198, [150, 110, 300, 170], ["Fecha", "Misión", "Alerta", "Severidad"], [
        ["02/11/2026 15:20", "M-021", "Desvío de ruta (75 m)", ("badge", "Alta", SEV["Alta"])],
        ["28/10/2026 09:05", "M-017", "Ingreso a zona restringida", ("badge", "Crítica", SEV["Crítica"])]])
    return m


def hu14():
    m = Mockup(14, "Recomendación de mantenimiento"); x = m.app("Administrador", "Mantenimiento", "/mantenimiento")
    m.titulo_seccion(x, TOP + 20, "Mantenimiento preventivo")
    m.toast(W - 400, TOP + 15, 380, "Mantenimiento recomendado", "DRN-004: 106 h de vuelo (umbral 100 h)", "Baja")
    m.texto(x, TOP + 100, 400, "Recomendaciones generadas", 13, "#111111", bold=True)
    m.tabla(x, TOP + 128, [110, 330, 150, 160], ["Dron", "Motivo", "Generada", "Estado del dron"], [
        ["DRN-004", "Superó 100 h de vuelo (106 h)", "18/11 09:12", ("badge", "En mantenimiento", EST["En mantenimiento"])],
        ["DRN-007", "Superó 50 misiones completadas", "15/11 17:40", ("badge", "En mantenimiento", EST["En mantenimiento"])]])
    m.mensaje(x, TOP + 250, 750, "Al generarse la recomendación el dron pasa a «en mantenimiento» y se avisa en pantalla al administrador.", "info")
    return m


def hu15():
    m = Mockup(15, "Resultado de mantenimiento"); x = m.app("Operador", "Mantenimiento", "/mantenimiento/registrar")
    m.titulo_seccion(x, TOP + 20, "Registrar resultado de mantenimiento")
    m.campo(x, TOP + 60, 330, "Dron en mantenimiento", "DRN-004 · 106 h · 40 misiones", select=True)
    m.texto(x, TOP + 130, 300, "Resultado", 12, MUTED)
    for i, (r, e) in enumerate([("Aprobado", "→ disponible y reinicia horas y misiones a 0"),
                                ("Requiere reparación", "→ fuera de servicio"),
                                ("Dar de baja", "→ dado de baja (permanente)")]):
        y = TOP + 158 + i * 34
        m.cell("radio", "shape=ellipse;html=1;strokeColor=#666666;fillColor=#ffffff;", "", x, y, 16, 16,
               f'<circle cx="{x + 8}" cy="{y + 8}" r="8" fill="#fff" stroke="#666"/>'
               + (f'<circle cx="{x + 8}" cy="{y + 8}" r="4" fill="{NAVY}"/>' if i == 0 else ""))
        m.texto(x + 26, y - 2, 170, r, 13, "#111111", bold=i == 0)
        m.texto(x + 200, y - 1, 400, e, 12, MUTED)
    m.boton(x, TOP + 280, 210, "Registrar resultado")
    m.boton(x + 225, TOP + 280, 120, "Cancelar", "secundario")
    return m


def hu16():
    m = Mockup(16, "Vista consolidada de la flota"); x = m.app("Administrador", "Panel de control", "/panel")
    m.titulo_seccion(x, TOP + 20, "Panel de control · estado de la flota")
    tarjetas = [("Disponibles", "12", EST["Disponible"]), ("En misión", "5", EST["En misión"]),
                ("Cargando", "3", EST["Cargando"]), ("En mantenimiento", "2", EST["En mantenimiento"]),
                ("Fuera de servicio", "1", EST["Fuera de servicio"])]
    for i, (k, v, c) in enumerate(tarjetas):
        m.tarjeta(x + i * 150, TOP + 65, 138, 95, k, v, c)
    m.texto(x, TOP + 185, 400, "Drones en misión", 13, "#111111", bold=True)
    m.tabla(x, TOP + 212, [110, 120, 110, 200, 200], ["Dron", "Misión", "Batería", "Destino", "Estado de la misión"], [
        ["DRN-001", "M-001", "54 %", "Cliente Norte", ("badge", "En curso", EST["En curso"])],
        ["DRN-002", "M-004", "48 %", "Cliente Sur", ("badge", "Pausada", EST["Pausada"])]])
    return m


def hu17():
    m = Mockup(17, "Historial de misiones"); x = m.app("Administrador", "Historial de misiones", "/misiones/historial")
    m.titulo_seccion(x, TOP + 20, "Historial de misiones")
    m.campo(x, TOP + 50, 160, "Desde", "01/11/2026")
    m.campo(x + 175, TOP + 50, 160, "Hasta", "18/11/2026")
    m.campo(x + 350, TOP + 50, 160, "Dron", "DRN-001", select=True)
    m.campo(x + 525, TOP + 50, 120, "Estado", "Todos", select=True)
    m.boton(x + 660, TOP + 70, 90, "Buscar")
    m.tabla(x, TOP + 125, [90, 110, 160, 110, 130, 150], ["Misión", "Tipo", "Destino", "Dron", "Fecha", "Estado"], [
        ["M-001", "Entrega", "Cliente Norte", "DRN-001", "18/11/2026", ("badge", "Finalizada", EST["Finalizada"])],
        ["M-021", "Entrega", "Bodega Sur", "DRN-001", "02/11/2026", ("badge", "Finalizada", EST["Finalizada"])],
        ["M-019", "Inspección", "Torre 2", "DRN-001", "01/11/2026", ("badge", "Abortada", EST["Abortada"])]])
    m.mensaje(x, TOP + 280, 750, "Sin resultados: no hay misiones para DRN-099 en el rango indicado.", "aviso")
    return m


def hu18():
    m = Mockup(18, "Reglas y umbrales"); x = m.app("Administrador", "Configuración", "/configuracion")
    m.titulo_seccion(x, TOP + 20, "Configuración del sistema")
    secciones = [("Ponderación de asignación automática", [("Batería (%)", "40"), ("Cercanía (%)", "35"), ("Prioridad (%)", "25")]),
                 ("Umbrales de alerta", [("Batería mínima (%)", "25"), ("Desvío máximo (m)", "80")]),
                 ("Umbrales de mantenimiento", [("Horas de vuelo", "120"), ("Misiones completadas", "50")])]
    y = TOP + 60
    for titulo, campos in secciones:
        m.texto(x, y, 400, titulo, 13, "#111111", bold=True)
        for i, (k, v) in enumerate(campos):
            m.campo(x + i * 250, y + 24, 220, k, v)
        y += 100
    m.boton(x, y + 5, 180, "Guardar cambios")
    m.texto(x + 200, y + 13, 500, "Los nuevos valores se usan desde la siguiente asignación o lectura.", 11)
    return m


def hu19():
    m = Mockup(19, "Iniciar sesión")
    m.marco_navegador("/login")
    m.rect(0, NAV_Y, W, NAV_H, NAVY, NAVY, "     Dronflow", "#ffffff", 16, "left", True)
    m.rect(0, TOP, W, H - TOP, "#f5f7fa")
    bx = W / 2 - 190
    m.rect(bx, TOP + 50, 380, 400, "#ffffff", "#d0d4db")
    m.texto(bx, TOP + 80, 380, "Iniciar sesión", 20, "#000000", bold=True, align="center")
    m.texto(bx, TOP + 112, 380, "Gestión de flotas de drones", 12, MUTED, align="center")
    m.mensaje(bx + 40, TOP + 150, 300, "Usuario o contraseña inválidos.", "error", 36)
    m.campo(bx + 40, TOP + 200, 300, "Usuario", "operador1")
    m.campo(bx + 40, TOP + 265, 300, "Contraseña", "••••••••")
    m.boton(bx + 40, TOP + 345, 300, "Ingresar", h=36)
    m.texto(bx, TOP + 400, 380, "El mensaje no indica qué campo es incorrecto.", 11, align="center")
    return m


def hu20():
    m = Mockup(20, "Registrar operador"); x = m.app("Administrador", "Usuarios", "/usuarios/nuevo")
    m.titulo_seccion(x, TOP + 20, "Registrar usuario operador")
    m.mensaje(x, TOP + 58, 500, "El nombre de usuario «operador2» ya existe.", "error")
    m.campo(x, TOP + 115, 360, "Nombre de usuario", "operador2")
    m.campo(x, TOP + 180, 360, "Contraseña", "••••••••")
    m.campo(x, TOP + 245, 360, "Confirmar contraseña", "••••••••")
    m.campo(x, TOP + 310, 360, "Rol", "Operador")
    m.boton(x, TOP + 380, 200, "Registrar usuario")
    m.boton(x + 215, TOP + 380, 120, "Cancelar", "secundario")
    return m


def tabla_usuarios(m, x):
    m.tabla(x, TOP + 75, [180, 150, 140, 270], ["Usuario", "Rol", "Estado", "Acciones"], [
        ["admin", "Administrador", ("badge", "Activo", EST["Activo"]), ""],
        ["operador1", "Operador", ("badge", "Activo", EST["Activo"]), ("btns", [("Editar", "secundario"), ("Eliminar", "peligro")])],
        ["operador2", "Operador", ("badge", "Activo", EST["Activo"]), ("btns", [("Editar", "secundario"), ("Eliminar", "peligro")])]])


def hu21():
    m = Mockup(21, "Eliminar cuenta"); x = m.app("Administrador", "Usuarios", "/usuarios")
    m.titulo_seccion(x, TOP + 20, "Usuarios")
    m.boton(x + 590, TOP + 20, 150, "+ Registrar operador")
    tabla_usuarios(m, x)
    m.modal(x + 150, TOP + 160, 420, 180)
    m.texto(x + 175, TOP + 180, 360, "¿Eliminar la cuenta «operador2»?", 15, "#111111", bold=True)
    m.texto(x + 175, TOP + 215, 370, "El usuario ya no podrá iniciar sesión en el sistema.", 12)
    m.boton(x + 315, TOP + 285, 110, "Cancelar", "secundario")
    m.boton(x + 435, TOP + 285, 110, "Eliminar", "peligro")
    return m


def hu22():
    m = Mockup(22, "Editar cuenta"); x = m.app("Administrador", "Usuarios", "/usuarios/operador2")
    m.titulo_seccion(x, TOP + 20, "Editar usuario · operador2")
    m.mensaje(x, TOP + 58, 500, "Cambios guardados en la cuenta «operador2».", "ok")
    m.campo(x, TOP + 115, 360, "Nombre de usuario", "operador2")
    m.campo(x, TOP + 180, 360, "Nueva contraseña (opcional)", "Dejar vacío para no cambiarla", placeholder=True)
    m.campo(x, TOP + 245, 360, "Confirmar contraseña", "", placeholder=True)
    m.boton(x, TOP + 320, 200, "Guardar cambios")
    m.boton(x + 215, TOP + 320, 120, "Cancelar", "secundario")
    return m


PANTALLAS = [hu01, hu02, hu03, hu04, hu05, hu06, hu07, hu08, hu09, hu10, hu11, hu12, hu13, hu14, hu15,
             hu16, hu17, hu18, hu19, hu20, hu21, hu22]

if __name__ == "__main__":
    destino = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(destino, exist_ok=True)
    for p in PANTALLAS:
        p().guardar(destino)
    print(len(PANTALLAS), "mockups en", destino)
