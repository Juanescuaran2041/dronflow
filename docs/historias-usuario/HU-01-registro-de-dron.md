### HU-01: Registro de un dron

**Como** administrador u operador
**Quiero** registrar un nuevo dron en la flota especificando identificación, tipo, capacidad de batería, autonomía, carga útil máxima y equipamiento
**Para** incorporarlo al inventario disponible y poder asignarlo a misiones acordes a su tipo y capacidades

**Validación INVEST**
- I — Independent: ✅ No depende de otra historia para entregarse.
- N — Negotiable: ✅ No impone tecnología ni estructura de datos específica.
- V — Valuable: ✅ Es la base de todo el sistema; sin drones registrados no hay flota que gestionar.
- E — Estimable: ✅ Atributos con tipos y unidades ya definidos en los requerimientos.
- S — Small: ✅ Cabe en una iteración corta.
- T — Testable: ✅ Unicidad de identificación y tipo válido son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Registro de drones en la flota

  Esquema del escenario: Registro exitoso de un dron nuevo por distintos roles
    Dado que "<rol>" ha iniciado sesión en el sistema
    Y no existe un dron con identificación "DRN-001"
    Cuando "<rol>" registra el dron con identificación "DRN-001", tipo "entrega", capacidad de batería 5000 mAh, autonomía 25 minutos, carga útil máxima 2 kg y equipamiento "cámara, gancho de carga"
    Entonces el dron se agrega a la flota con estado "disponible"
    Y el sistema confirma el registro exitoso

    Ejemplos:
      | rol           |
      | administrador |
      | operador      |

  Escenario: Rechazo por identificación duplicada
    Dado que ya existe un dron registrado con identificación "DRN-001"
    Cuando se intenta registrar otro dron con la misma identificación "DRN-001"
    Entonces el sistema rechaza el registro
    Y muestra un mensaje indicando que la identificación ya está en uso

  Escenario: Rechazo por tipo de dron inválido
    Dado que se está registrando un nuevo dron
    Cuando se ingresa un tipo que no está entre los soportados (entrega, inspección, monitoreo/fotografía)
    Entonces el sistema rechaza el registro
```

**Supuestos / preguntas abiertas**
- El equipamiento se registra como lista de texto libre, sin catálogo cerrado.
- RF-02 se incorpora aquí como la selección del atributo "tipo"; el comportamiento específico por tipo se manifiesta en las historias de misiones (HU-04 a HU-08), y su extensibilidad es un requisito de diseño (RNF-02), no una acción de usuario aparte.
