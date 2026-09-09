### HU-16: Vista consolidada del estado de la flota

**Como** operador
**Quiero** ver una vista consolidada del estado de toda la flota (disponibles, en misión, en mantenimiento, fuera de servicio)
**Para** tener visibilidad global de la operación en todo momento

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Visibilidad global esencial para la operación.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Conteos por estado son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Vista consolidada de la flota

  Escenario: Visualización del resumen de la flota
    Dado que la flota tiene drones en distintos estados operativos
    Cuando un operador abre el panel de control
    Entonces ve el número de drones en cada estado (disponible, en misión, cargando, en mantenimiento, fuera de servicio)
```

**Supuestos / preguntas abiertas**
- Ninguno relevante.
