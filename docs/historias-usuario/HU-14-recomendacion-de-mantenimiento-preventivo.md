### HU-14: Recomendación de mantenimiento preventivo

**Como** administrador
**Quiero** que el sistema me recomiende mantenimiento preventivo cuando un dron supere un umbral de mantenimiento configurable de horas de vuelo o misiones completadas
**Para** anticipar fallas antes de que ocurran

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅ No impone el algoritmo exacto (se definió como regla simple por umbral).
- V — Valuable: ✅ Anticipación de fallas, ahorro de costos.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Umbral cruzado o no es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Recomendación de mantenimiento preventivo

  Escenario: Generación de recomendación al superar el umbral de horas de vuelo
    Dado que el umbral configurado es 100 horas de vuelo
    Y el dron "DRN-001" acumula 95 horas de vuelo
    Cuando el dron completa una misión que suma 6 horas de vuelo
    Entonces el sistema genera una recomendación de mantenimiento preventivo para el dron "DRN-001"
    Y el estado del dron "DRN-001" cambia a "en mantenimiento"
    Y se muestra al administrador una alerta en pantalla con la recomendación

  Escenario: Sin recomendación mientras no se supera el umbral
    Dado que el umbral configurado es 100 horas de vuelo
    Y el dron "DRN-002" acumula 40 horas de vuelo
    Cuando el dron completa una misión que suma 2 horas de vuelo
    Entonces el sistema no genera ninguna recomendación de mantenimiento
```

**Supuestos / preguntas abiertas**
- 100 horas es un valor de ejemplo; el umbral real lo define un administrador (HU-18, umbrales de mantenimiento).
- La recomendación es la que lleva el dron a "en mantenimiento"; no hay otro disparador.
