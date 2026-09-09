### HU-08: Intervención manual de una misión en curso

**Como** operador
**Quiero** pausar, reanudar, redirigir a un nuevo destino o abortar una misión en curso
**Para** responder a situaciones imprevistas durante la ejecución

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Control operativo ante imprevistos.
- E — Estimable: ✅
- S — Small: ⚠️ Agrupa 4 acciones relacionadas; se mantienen juntas porque comparten actor y contexto (intervención en curso), pero podría dividirse si el equipo lo prefiere.
- T — Testable: ✅ Cada acción tiene un resultado verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Intervención manual de una misión en curso

  Escenario: Pausar una misión en curso
    Dado que la misión "M-001" está en estado "en curso"
    Cuando un operador la pausa
    Entonces el estado de la misión cambia a "pausada"
    Y el dron permanece en su posición actual

  Escenario: Reanudar una misión pausada
    Dado que la misión "M-001" está en estado "pausada"
    Cuando un operador la reanuda
    Entonces el estado de la misión vuelve a "en curso"

  Escenario: Redirigir una misión en curso a un nuevo destino
    Dado que la misión "M-001" está en estado "en curso" con destino "Cliente Norte"
    Cuando un operador la redirige al nuevo destino "Cliente Sur"
    Entonces el destino de la misión se actualiza a "Cliente Sur"
    Y el dron recalcula su ruta hacia el nuevo destino

  Escenario: Abortar una misión en curso
    Dado que la misión "M-001" está en estado "en curso"
    Cuando un operador la aborta
    Entonces el estado de la misión cambia a "abortada"
    Y el dron inicia retorno a la base
```

**Supuestos / preguntas abiertas**
- Al redirigir, el nuevo destino debe cumplir las mismas validaciones que un destino de creación (ej. no atravesar zonas restringidas — ver HU-06).
