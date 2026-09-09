### HU-19: Autenticación de usuario

**Como** usuario del sistema (administrador u operador)
**Quiero** autenticarme con mi usuario y contraseña
**Para** acceder a las funcionalidades correspondientes a mi rol

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Acceso controlado, base de la seguridad del sistema.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Acceso concedido/rechazado es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Autenticación de usuario

  Escenario: Inicio de sesión exitoso
    Dado que el usuario "operador1" tiene una cuenta activa con contraseña válida
    Cuando ingresa sus credenciales correctas
    Entonces el sistema le concede acceso a las funcionalidades de su rol

  Escenario: Inicio de sesión fallido por credenciales incorrectas
    Dado que el usuario "operador1" tiene una cuenta activa
    Cuando ingresa una contraseña incorrecta
    Entonces el sistema rechaza el acceso
    Y muestra un mensaje de credenciales inválidas sin especificar cuál campo es incorrecto
```

**Supuestos / preguntas abiertas**
- No se especifica límite de intentos fallidos ni bloqueo de cuenta; queda fuera del alcance de esta historia.
