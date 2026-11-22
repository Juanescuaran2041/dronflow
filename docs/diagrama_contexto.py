"""Genera docs/vistas/diagrama-contexto.svg: Dronflow como caja negra, sus actores y una línea por funcionalidad."""
import math
import os
from html import escape

ADMIN = [
    "Autenticarse (HU-19)", "Registrar operador (HU-20)", "Editar cuenta de usuario (HU-22)",
    "Eliminar cuenta de usuario (HU-21)", "Listar usuarios activos (HU-21, HU-22)", "Registrar dron (HU-01)",
    "Dar de baja un dron (HU-03)", "Reactivar un dron (HU-03)", "Configurar ponderación de asignación (HU-18)",
    "Configurar umbrales de alerta (HU-18)", "Configurar umbrales de mantenimiento (HU-18)",
    "Consultar vista consolidada de la flota (HU-16)", "Consultar historial de misiones (HU-17)",
    "Recibir alerta de batería baja (HU-09)", "Recibir alerta de desvío o zona restringida (HU-10)",
    "Recibir notificación en tiempo real (HU-11)", "Ver severidad de la alerta (HU-12)",
    "Consultar alertas por tipo y severidad (HU-12)", "Recibir recomendación de mantenimiento (HU-14)",
]
OPERADOR = [
    "Autenticarse (HU-19)", "Registrar dron (HU-01)", "Dar de baja un dron (HU-03)", "Reactivar un dron (HU-03)",
    "Gestionar estado operativo del dron (HU-02)", "Crear misión (HU-04)", "Asignar dron automáticamente (HU-05)",
    "Validar ruta antes del despegue (HU-06)", "Ver avance de la misión (HU-07)", "Pausar misión (HU-08)",
    "Reanudar misión (HU-08)", "Redirigir misión (HU-08)", "Abortar misión (HU-08)",
    "Consultar historial de vuelos del dron (HU-13)", "Registrar resultado de mantenimiento (HU-15)",
]
W, H, CX, CY, R, PASO = 2040, 1230, 1020, 600, 400, 38
F = 'font-family="Arial, Helvetica, sans-serif"'
s = []


def texto(x, y, t, size=13, color="#111", extra='text-anchor="middle"'):
    s.append(f'<text x="{x}" y="{y}" {F} font-size="{size}" fill="{color}" {extra}>{escape(t)}</text>')


def etiqueta(x, y, t):  # caja blanca bajo el texto para que la línea no lo tape
    w = len(t) * 7.1 + 16
    s.append(f'<rect x="{x - w / 2:.1f}" y="{y - 11:.1f}" width="{w:.1f}" height="22" fill="#ffffff" fill-opacity="0.95"/>')
    texto(f"{x:.1f}", f"{y + 5:.1f}", t)


def actor(x, lineas, nombre, izquierda):
    h = len(lineas) * PASO + 122
    y0 = CY - h / 2
    s.append(f'<rect x="{x}" y="{y0}" width="170" height="{h}" fill="#fef3c7" stroke="#333" stroke-width="2"/>')
    texto(x + 85, y0 + 28, "«actor»", 13, "#444")
    texto(x + 85, y0 + 50, nombre, 17, "#1a1a1a", 'font-weight="bold" text-anchor="middle"')
    borde = x + 170 if izquierda else x
    etqs = []
    for i, t in enumerate(lineas):
        y = CY + (i - (len(lineas) - 1) / 2) * PASO
        dx = math.sqrt(R * R - (y - CY) ** 2)
        fin = CX - dx if izquierda else CX + dx
        s.append(f'<line x1="{borde:.1f}" y1="{y:.1f}" x2="{fin:.1f}" y2="{y:.1f}" stroke="#333" stroke-width="1.4"/>')
        etqs.append(((borde + fin) / 2, y, t))
    return etqs


def externo(y, nombre):
    s.append(f'<rect x="850" y="{y}" width="340" height="80" fill="#e5e7eb" stroke="#333" stroke-width="2"/>')
    texto(1020.0, y + 28, "«sistema externo»", 13, "#444")
    texto(1020.0, y + 50, nombre, 17, "#1a1a1a", 'font-weight="bold" text-anchor="middle"')


s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
s.append(f'<text x="30" y="40" {F} font-size="26" font-weight="bold" fill="#1a1a1a">Diagrama de contexto — Dronflow</text>')
s.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#dbeafe" stroke="#1d4ed8" stroke-width="3"/>')
etqs = actor(30, ADMIN, "Administrador", True) + actor(1840, OPERADOR, "Operador", False)

externo(70, "Proveedor de zonas restringidas")
s.append('<line x1="1020.0" y1="150.0" x2="1020.0" y2="200.0" stroke="#333" stroke-width="1.4"/>')
externo(1120, "Fuente de telemetría ⚠")
s.append('<line x1="930.0" y1="1120.0" x2="870.0" y2="970.8" stroke="#333" stroke-width="1.4"/>')
s.append('<line x1="1110.0" y1="1120.0" x2="1170.0" y2="970.8" stroke="#333" stroke-width="1.4"/>')

texto(CX, 594, "Dronflow", 34, "#1e3a8a", 'font-weight="bold" text-anchor="middle"')
texto(CX, 626, "Sistema de gestión de flotas de drones", 15, "#1e3a8a")
for x, y, t in etqs:
    etiqueta(x, y, t)
etiqueta(1020.0, 175.0, "Suministrar zonas restringidas (HU-06, HU-10)")
etiqueta(900.0, 1045.0, "Enviar posición del dron · POST (HU-07, HU-10)")
etiqueta(1128.0, 1075.0, "Enviar nivel de batería · POST (HU-09)")

s.append('<circle cx="55" cy="1160" r="14" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>')
texto(80, 1165, "Sistema", 14, "#222", "")
s.append('<rect x="170" y="1147" width="26" height="26" fill="#fef3c7" stroke="#333" stroke-width="2"/>')
texto(206, 1165, "Actor (usuario)", 14, "#222", "")
s.append('<rect x="340" y="1147" width="26" height="26" fill="#e5e7eb" stroke="#333" stroke-width="2"/>')
texto(376, 1165, "Actor de sistema (sistema externo)", 14, "#222", "")
texto(30, 1194, "Cada línea es una funcionalidad. ⚠ = el sistema concreto que envía la telemetría aún no está definido.",
      13, "#444", "")

ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vistas", "diagrama-contexto.svg")
with open(ruta, "w", encoding="utf-8", newline="\n") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
            + "\n".join(s) + "\n</svg>\n")
print("ok", ruta)
