### HU-02: Estado operativo del dron

**Como** operador
**Quiero** que el sistema mantenga y muestre el estado operativo de cada dron (disponible, en misión, cargando, en mantenimiento, fuera de servicio) actualizado en todo momento
**Para** saber si puedo asignarlo a una misión o si requiere atención

**Validación INVEST**
- I — Independent: ⚠️ Depende parcialmente de otras historias (misiones, mantenimiento) para exhibir todos los estados, pero es entregable incrementalmente.
- N — Negotiable: ✅ No impone mecanismo técnico de actualización.
- V — Valuable: ✅ Sin este estado no se puede decidir a qué dron asignar una misión.
- E — Estimable: ✅ Estados enumerados explícitamente.
- S — Small: ✅ Acotado a un campo de estado y sus transiciones.
- T — Testable: ✅ Verificable tras cada evento disparador.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Estado operativo del dron

  Escenario: Dron recién registrado queda disponible
    Dado que un dron fue registrado exitosamente
    Entonces su estado operativo es "disponible"

  Escenario: Dron asignado a una misión cambia de estado
    Dado que el dron "DRN-001" está en estado "disponible"
    Cuando el sistema le asigna una misión
    Entonces el estado del dron cambia a "en misión"

  Escenario: Dron marcado como fuera de servicio
    Dado que el dron "DRN-001" está en estado "disponible"
    Cuando un operador reporta una avería en el dron
    Entonces el estado del dron cambia a "fuera de servicio"
    Y el dron deja de estar disponible para nuevas asignaciones

  Escenario: Dron que termina una misión con batería suficiente
    Dado que el dron "DRN-001" está en estado "en misión"
    Y el umbral de batería configurado es 20%
    Cuando la misión finaliza o se aborta y el dron tiene 60% de batería
    Entonces el estado del dron cambia a "disponible"

  Escenario: Dron que termina una misión con batería bajo el umbral
    Dado que el dron "DRN-001" está en estado "en misión"
    Y el umbral de batería configurado es 20%
    Cuando la misión finaliza o se aborta y el dron tiene 15% de batería
    Entonces el estado del dron cambia a "cargando"
    Y vuelve a "disponible" cuando su batería supera el umbral
```

**Supuestos / preguntas abiertas**
- Se asume que el operador puede marcar manualmente un dron como "fuera de servicio" ante una avería reportada.
- Al terminar una misión (finalizada o abortada) el dron no pasa automáticamente a "cargando": vuelve a "disponible" si su batería supera el umbral de batería (el mismo de HU-09/HU-18) y pasa a "cargando" si no. El mecanismo físico de carga está fuera del alcance.
