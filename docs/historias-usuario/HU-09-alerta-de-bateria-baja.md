### HU-09: Alerta de batería baja

**Como** administrador
**Quiero** recibir una alerta cuando la batería de un dron en misión caiga por debajo del umbral de batería configurado
**Para** poder intervenir antes de que el dron se quede sin energía

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Previene pérdida de dron por falta de energía.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Lectura bajo el umbral o no es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Alerta de batería baja

  Escenario: Alerta en cada lectura bajo el umbral de batería
    Dado que el umbral de batería configurado es 20%
    Y el dron "DRN-001" está en misión con 25% de batería
    Cuando la batería del dron desciende a 19%
    Entonces el sistema genera una alerta de batería baja para el dron "DRN-001"
    Y cuando la siguiente lectura sigue bajo el umbral (18%) genera otra alerta de batería baja

  Escenario: Sin alerta mientras la batería está sobre el umbral
    Dado que el umbral de batería configurado es 20%
    Y el dron "DRN-001" está en misión con 30% de batería
    Cuando la batería del dron desciende a 21%
    Entonces el sistema no genera ninguna alerta
```

**Supuestos / preguntas abiertas**
- El umbral de batería es global y lo modifica el administrador (HU-18). La alerta se genera en cada lectura bajo el umbral, no solo al cruzarlo.
