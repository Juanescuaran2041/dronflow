### HU-03: Dar de baja o reactivar un dron

**Como** administrador u operador
**Quiero** dar de baja permanentemente un dron o reactivarlo desde los estados "fuera de servicio" o "en mantenimiento"
**Para** retirar drones inutilizables de la flota o devolver al servicio los que ya están operativos

**Validación INVEST**
- I — Independent: ✅ No depende de otra historia para entregarse.
- N — Negotiable: ✅ No impone mecanismo técnico específico.
- V — Valuable: ✅ Evita que drones no operativos sean candidatos de asignación.
- E — Estimable: ✅ Reglas de bloqueo y transición claras.
- S — Small: ✅ Acotado a dos acciones (baja/reactivar).
- T — Testable: ✅ Reglas de bloqueo (misión activa) y transición son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Baja y reactivación de drones

  Esquema del escenario: Dar de baja un dron sin misión activa
    Dado que el dron "DRN-001" está en estado "<estado>"
    Y no tiene una misión activa
    Cuando "<rol>" da de baja al dron "DRN-001"
    Entonces el dron queda marcado como "dado de baja"
    Y deja de aparecer entre los drones operativos de la flota

    Ejemplos:
      | rol           | estado            |
      | administrador | disponible        |
      | operador      | fuera de servicio |

  Escenario: Rechazo al intentar dar de baja un dron con misión activa
    Dado que el dron "DRN-001" está en estado "en misión"
    Cuando se intenta darlo de baja
    Entonces el sistema rechaza la operación
    Y muestra un mensaje indicando que debe finalizarse o abortarse la misión primero

  Escenario: Reactivación de un dron fuera de servicio
    Dado que el dron "DRN-001" está en estado "fuera de servicio"
    Cuando se reactiva el dron
    Entonces el estado del dron cambia a "disponible"

  Escenario: Reactivación de un dron en mantenimiento
    Dado que el dron "DRN-001" está en estado "en mantenimiento"
    Cuando se reactiva el dron
    Entonces el estado del dron cambia a "disponible"
```

**Supuestos / preguntas abiertas**
- Un dron "dado de baja" no puede reactivarse; reingresarlo requeriría registrarlo como dron nuevo.
