### HU-20: Registrar nuevo usuario operador

**Como** administrador
**Quiero** registrar nuevos usuarios con rol de operador
**Para** dar acceso al sistema al personal que gestionará la flota día a día

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Habilita la incorporación de personal operativo.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Creación y duplicidad de usuario son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Registro de usuarios operadores

  Escenario: Registro exitoso de un nuevo operador
    Dado que un administrador tiene sesión activa
    Cuando registra un nuevo usuario con nombre de usuario "operador2" y rol "operador"
    Entonces el usuario "operador2" queda creado y puede iniciar sesión con rol "operador"

  Escenario: Rechazo por nombre de usuario duplicado
    Dado que ya existe un usuario "operador2"
    Cuando un administrador intenta registrar otro usuario con el mismo nombre "operador2"
    Entonces el sistema rechaza el registro
```

**Supuestos / preguntas abiertas**
- Ninguno relevante.
