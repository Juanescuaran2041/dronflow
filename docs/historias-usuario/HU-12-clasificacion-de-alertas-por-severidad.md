### HU-12: Clasificación de alertas por severidad

**Como** operador
**Quiero** que cada alerta se clasifique automáticamente por nivel de severidad (baja, media, alta, crítica)
**Para** priorizar mi atención sobre las alertas más urgentes

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Permite priorizar la atención del operador.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Mapeo tipo→severidad es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Clasificación de alertas por severidad

  Esquema del escenario: Clasificación automática según el tipo de alerta
    Dado que se genera una alerta de tipo "<tipo_alerta>"
    Cuando el sistema la clasifica
    Entonces la alerta queda registrada con severidad "<severidad>"

    Ejemplos:
      | tipo_alerta                | severidad |
      | batería baja               | media     |
      | desvío de ruta             | alta      |
      | ingreso a zona restringida | crítica   |
```

**Supuestos / preguntas abiertas**
- El mapeo tipo de alerta → severidad es un ejemplo razonable propuesto por el analista (confirmado con el usuario); la tabla definitiva debe validarse con el equipo de producto.
