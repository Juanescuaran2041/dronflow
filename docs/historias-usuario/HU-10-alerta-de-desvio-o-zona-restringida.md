### HU-10: Alerta de desvío de ruta o ingreso a zona restringida

**Como** operador
**Quiero** recibir una alerta cuando un dron se desvíe más de una distancia configurable de su ruta planificada o ingrese a una zona restringida
**Para** detectar comportamientos anómalos durante la misión

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Detección temprana de anomalías.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Umbral en metros es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Alerta de desvío de ruta o zona restringida

  Escenario: Alerta por desvío de ruta superior al umbral configurado
    Dado que el umbral de desvío configurado es 50 metros
    Y el dron "DRN-001" está siguiendo su ruta planificada
    Cuando el dron se desvía 60 metros de la ruta planificada
    Entonces el sistema genera una alerta de desvío de ruta

  Escenario: Alerta por ingreso a zona restringida
    Dado que el dron "DRN-001" está en misión fuera de zonas restringidas
    Cuando el dron ingresa a una zona restringida
    Entonces el sistema genera una alerta de ingreso a zona restringida
```

**Supuestos / preguntas abiertas**
- 50 metros es un valor de ejemplo; el valor real lo define un administrador (ligado a HU-18).
