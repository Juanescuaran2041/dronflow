### HU-07: Seguimiento del avance de una misión

**Como** operador
**Quiero** ver el avance de una misión a través de sus estados (pendiente, despegue, en curso, pausada, retorno, finalizada, abortada)
**Para** monitorear su progreso en tiempo real

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅ No impone mecanismo de telemetría.
- V — Valuable: ✅ Visibilidad operativa esencial.
- E — Estimable: ✅ Estados enumerados.
- S — Small: ✅
- T — Testable: ✅ Cada transición es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Seguimiento del avance de una misión

  Esquema del escenario: Transición de estado de una misión
    Dado que la misión "M-001" está en estado "<estado_actual>"
    Cuando ocurre el evento "<evento>"
    Entonces el estado de la misión cambia a "<estado_nuevo>"

    Ejemplos:
      | estado_actual | evento                           | estado_nuevo |
      | pendiente     | ruta validada y despegue autorizado (HU-06) | despegue     |
      | despegue      | dron alcanza altitud de crucero  | en curso     |
      | en curso      | dron inicia regreso              | retorno      |
      | retorno       | dron aterriza en base            | finalizada   |
      | en curso      | operador aborta la misión         | abortada     |
```

**Supuestos / preguntas abiertas**
- Los eventos de la tabla son ilustrativos; el detalle técnico de sensores queda fuera del alcance de esta historia.
- Decisión del autor: la telemetría (batería y posición del dron) es interna del sistema, no un servicio externo. El propio dron actualiza su batería y posición dentro de Gestión de Flota (`Drone.updateTelemetry`) y cada lectura dispara la evaluación de alertas (HU-09, HU-10). Quién la invoca y cada cuánto se define en la implementación.
