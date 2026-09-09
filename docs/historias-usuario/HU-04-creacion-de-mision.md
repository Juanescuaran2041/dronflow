### HU-04: Crear una misión

**Como** operador
**Quiero** crear una misión especificando tipo, prioridad, origen, destino y requisitos (carga útil, autonomía mínima)
**Para** que el sistema pueda asignarle un dron adecuado y ejecutarla

**Validación INVEST**
- I — Independent: ✅ No depende de otra historia para entregarse.
- N — Negotiable: ✅ No impone solución técnica.
- V — Valuable: ✅ Punto de entrada de todo el flujo operativo.
- E — Estimable: ✅ Campos y validaciones claros.
- S — Small: ✅ Cabe en una iteración corta.
- T — Testable: ✅ Origen≠destino y tipo válido son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Creación de misiones

  Escenario: Creación exitosa de una misión
    Dado que un operador ha iniciado sesión
    Cuando crea una misión de tipo "entrega" con prioridad "alta", origen "Bodega Central", destino "Cliente Norte", carga útil requerida 1.5 kg y autonomía mínima 20 minutos
    Entonces la misión se crea con estado "pendiente"
    Y queda disponible para asignación automática de dron

  Escenario: Rechazo por origen y destino iguales
    Dado que un operador está creando una misión
    Cuando ingresa el mismo punto como origen y destino
    Entonces el sistema rechaza la creación de la misión

  Escenario: Rechazo por tipo de misión inválido
    Dado que un operador está creando una misión
    Cuando ingresa un tipo que no está entre los soportados (entrega, inspección, monitoreo/fotografía)
    Entonces el sistema rechaza la creación de la misión
```

**Supuestos / preguntas abiertas**
- El campo prioridad usa la misma escala que la severidad de alertas (baja, media, alta, crítica).
