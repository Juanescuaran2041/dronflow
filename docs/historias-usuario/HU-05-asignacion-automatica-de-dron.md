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
    Y el estado del dron cambia a "en misión"
    Y el estado de la misión cambia a "despegue"

  Escenario: Ninguna asignación posible por falta de dron compatible
    Dado que existe una misión "M-002" en estado "pendiente"
    Y ningún dron disponible cumple sus requisitos
    Cuando el sistema evalúa la asignación
    Entonces la misión "M-002" permanece en estado "pendiente"

  Escenario: Asignación diferida cuando se libera un dron compatible
    Dado que la misión "M-002" está en estado "pendiente" por falta de dron compatible
    Cuando un dron "DRN-002" que cumple sus requisitos pasa a estado "disponible"
    Entonces el sistema asigna automáticamente la misión "M-002" al dron "DRN-002"
```

**Supuestos / preguntas abiertas**
- La ponderación de criterios tiene valores por defecto configurados por un administrador antes de la primera asignación (ligado a HU-18).
