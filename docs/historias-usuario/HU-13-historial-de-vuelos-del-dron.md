### HU-13: Historial de vuelos del dron

**Como** operador
**Quiero** que el sistema registre el historial de vuelos de cada dron (horas de vuelo, misiones completadas e incidencias)
**Para** tener trazabilidad del uso y desempeño de cada dron

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Trazabilidad necesaria para mantenimiento y análisis.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Registro automático es verificable tras cada misión.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Historial de vuelos del dron

  Escenario: Registro automático al finalizar una misión
    Dado que el dron "DRN-001" completó la misión "M-001"
    Cuando la misión finaliza
    Entonces se agregan al historial del dron las horas de vuelo de la misión y la misión como completada

  Escenario: Registro de una incidencia en el historial
    Dado que durante la misión "M-001" se generó una alerta de severidad "alta"
    Cuando la misión finaliza
    Entonces la alerta queda registrada como incidencia en el historial del dron "DRN-001"
```

**Supuestos / preguntas abiertas**
- Ninguno relevante.
