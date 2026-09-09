### HU-09: Alerta de batería baja

**Como** operador
**Quiero** recibir una alerta cuando la batería de un dron en misión caiga por debajo de un umbral que yo defino
**Para** poder intervenir antes de que el dron se quede sin energía

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Previene pérdida de dron por falta de energía.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Umbral cruzado o no es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Alerta de batería baja

  Escenario: Generación de alerta al cruzar el umbral de batería
    Dado que el operador definió un umbral de batería de 20% para el dron "DRN-001"
    Y el dron "DRN-001" está en misión con 25% de batería
    Cuando la batería del dron desciende a 19%
    Entonces el sistema genera una alerta de batería baja para el dron "DRN-001"

  Escenario: Sin alerta mientras la batería está sobre el umbral
    Dado que el operador definió un umbral de batería de 20% para el dron "DRN-001"
    Y el dron "DRN-001" está en misión con 30% de batería
    Cuando la batería del dron desciende a 21%
    Entonces el sistema no genera ninguna alerta
```

**Supuestos / preguntas abiertas**
- Se asume que el umbral se define por dron (no se especifica si es global o por misión).
