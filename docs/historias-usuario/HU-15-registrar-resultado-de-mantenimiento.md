### HU-15: Registrar resultado de un mantenimiento

**Como** operador
**Quiero** registrar el resultado de un mantenimiento realizado a un dron (aprobado, requiere reparación, dron dado de baja)
**Para** mantener actualizado el estado operativo de la flota

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Mantiene consistente el estado de la flota.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Cada resultado mapea a un estado verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Registro de resultado de mantenimiento

  Esquema del escenario: Registro del resultado de mantenimiento
    Dado que el dron "DRN-001" está en estado "en mantenimiento"
    Cuando un operador registra el resultado "<resultado>"
    Entonces el estado del dron cambia a "<estado_resultante>"

    Ejemplos:
      | resultado          | estado_resultante  |
      | aprobado            | disponible         |
      | requiere reparación | fuera de servicio  |
      | dron dado de baja   | dado de baja       |
```

**Supuestos / preguntas abiertas**
- Ninguno relevante.
