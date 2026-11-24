### HU-24: Promover un operador a administrador

**Como** administrador
**Quiero** promover una cuenta de operador al rol de administrador
**Para** delegar la administración del sistema sin tener que crear una cuenta nueva ni compartir la mía

**Validación INVEST**
- I — Independent: ✅ Se apoya en cuentas que ya existen (HU-20) pero no depende de ningún cambio en ellas.
- N — Negotiable: ✅ Queda abierto si en el futuro se permite revocar el rol; hoy la decisión del autor es que no.
- V — Valuable: ✅ Evita que la administración dependa de la única cuenta creada al arranque del sistema.
- E — Estimable: ✅ Una operación sobre el rol de una cuenta existente.
- S — Small: ✅ Un solo endpoint sin cuerpo de petición.
- T — Testable: ✅ Ascenso, cuenta ya administradora, cuenta dada de baja y cuenta inexistente son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Promoción de un operador a administrador

  Escenario: Promoción exitosa de un operador
    Dado que un administrador tiene sesión activa
    Y que existe una cuenta activa "operador2" con rol "operador"
    Cuando el administrador promueve la cuenta "operador2"
    Entonces la cuenta "operador2" queda con rol "administrador"
    Y al iniciar sesión de nuevo accede a las funcionalidades de administrador

  Escenario: Rechazo al promover una cuenta que ya es administradora
    Dado que existe una cuenta "admin" con rol "administrador"
    Cuando un administrador intenta promover la cuenta "admin"
    Entonces el sistema rechaza la operación por conflicto
    Y la cuenta conserva su rol

  Escenario: Rechazo al promover una cuenta dada de baja
    Dado que existe una cuenta "operador3" dada de baja
    Cuando un administrador intenta promover la cuenta "operador3"
    Entonces el sistema rechaza la operación por conflicto
    Y la cuenta conserva su rol "operador"

  Escenario: Rechazo al promover una cuenta inexistente
    Dado que un administrador tiene sesión activa
    Cuando intenta promover una cuenta que no existe
    Entonces el sistema responde que la cuenta no fue encontrada

  Escenario: Un operador no puede promover a nadie
    Dado que un operador tiene sesión activa
    Cuando intenta promover una cuenta de operador
    Entonces el sistema deniega el acceso a la operación
```

**Supuestos / preguntas abiertas**
- Decisión del autor: la operación es **solo de ascenso**. No existe quitar el rol de administrador, en línea con RF-22, donde una cuenta de administrador tampoco se da de baja.
- Decisión del autor: el operador promovido conserva su sesión actual con rol de operador hasta que esta expire (2 h) o cierre sesión. Su rol nuevo rige desde el siguiente inicio de sesión, porque el rol viaja dentro del token.
