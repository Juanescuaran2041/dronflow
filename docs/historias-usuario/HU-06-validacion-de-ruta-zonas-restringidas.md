### HU-06: Validación de ruta contra zonas restringidas

**Como** operador
**Quiero** que el sistema valide que la ruta de vuelo de una misión no atraviese zonas restringidas antes de autorizar el despegue
**Para** evitar infracciones o incidentes en zonas prohibidas

**Validación INVEST**
- I — Independent: ✅ No depende de otra historia para entregarse.
- N — Negotiable: ✅ No impone el mecanismo de validación geoespacial.
- V — Valuable: ✅ Evita riesgos legales/operativos.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Verificable con ruta que cruza o no zona restringida.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Validación de ruta contra zonas restringidas

  Escenario: Autorización de despegue con ruta libre de zonas restringidas
    Dado que la misión "M-001" tiene una ruta que no atraviesa ninguna zona restringida
    Cuando el sistema valida la ruta antes del despegue
    Entonces el despegue es autorizado

  Escenario: Rechazo de despegue por ruta que atraviesa una zona restringida
    Dado que la misión "M-003" tiene una ruta que atraviesa una zona restringida
    Cuando el sistema valida la ruta antes del despegue
    Entonces el despegue es rechazado
    Y se notifica al operador el motivo del rechazo

  Escenario: Ruta que no se logra calcular mantiene el dron reservado
    Dado que la misión "M-004" tiene un dron asignado
    Cuando el sistema no logra calcular o validar su ruta
    Entonces el dron permanece reservado para la misión
    Y el sistema reintenta el cálculo

  Escenario: Dron liberado tras agotar los intentos
    Dado que el sistema ya intentó calcular la ruta de la misión "M-004" 3 veces sin éxito
    Cuando falla el tercer intento
    Entonces el dron pasa a estado "disponible"
    Y la misión "M-004" queda en estado "pendiente" sin dron asignado
```

**Supuestos / preguntas abiertas**
- El máximo de intentos de cálculo de ruta es 3 (valor inicial, sujeto a cambio).
- Las zonas restringidas son datos de configuración fija/externa (RF-07); esta historia solo cubre su consulta, no su gestión.
