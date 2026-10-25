### HU-05: Asignación automática de dron a misión

**Como** operador
**Quiero** que el sistema asigne automáticamente un dron disponible a una misión según batería, cercanía y prioridad ponderados
**Para** no tener que elegir manualmente el dron en cada misión

**Validación INVEST**
- I — Independent: ⚠️ Depende de que existan misiones (HU-04) y drones disponibles (HU-01/HU-02), pero constituye una unidad de valor propia.
- N — Negotiable: ✅ No impone el algoritmo exacto de ponderación.
- V — Valuable: ✅ Automatiza una decisión operativa repetitiva.
- E — Estimable: ✅ Criterios de asignación enumerados.
- S — Small: ✅ Acotado a la lógica de asignación.
- T — Testable: ✅ Verificable con dron disponible/no disponible.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Asignación automática de dron a misión

  Escenario: Asignación exitosa cuando hay un dron compatible disponible
    Dado que existe una misión "M-001" en estado "pendiente" que requiere carga útil de 1.5 kg y autonomía mínima de 20 minutos
    Y existe un dron "DRN-001" disponible que cumple esos requisitos
    Cuando el sistema evalúa la asignación
    Entonces la misión "M-001" se asigna al dron "DRN-001"
    Y el estado del dron cambia a "en misión" (dron reservado)
    Y la misión permanece en estado "pendiente" hasta que su ruta sea validada (HU-06)

  Escenario: Ninguna asignación posible por falta de dron compatible
    Dado que existe una misión "M-002" en estado "pendiente"
    Y ningún dron disponible cumple sus requisitos
    Cuando el sistema evalúa la asignación
    Entonces la misión "M-002" permanece en estado "pendiente"

  Escenario: Asignación diferida cuando se libera un dron compatible
    Dado que la misión "M-002" está en estado "pendiente" por falta de dron compatible
    Cuando un dron "DRN-002" que cumple sus requisitos pasa a estado "disponible"
    Entonces el sistema asigna automáticamente la misión "M-002" al dron "DRN-002"

  Escenario: Elección entre varias misiones pendientes por prioridad
    Dado que las misiones "M-004" de prioridad "alta" y "M-005" de prioridad "baja" están pendientes
    Y ambas son compatibles con el dron "DRN-003"
    Cuando el dron "DRN-003" pasa a estado "disponible"
    Entonces el sistema le asigna la misión "M-004"
```

**Supuestos / preguntas abiertas**
- La prioridad de la misión no distingue entre drones candidatos: sirve para elegir entre varias misiones pendientes cuando un dron queda disponible.
- La ponderación de criterios tiene valores por defecto configurados por un administrador antes de la primera asignación (ligado a HU-18).
