### HU-22: Editar cuenta de usuario

**Como** administrador
**Quiero** editar la información de cuentas de usuario existentes
**Para** mantener los datos de acceso actualizados

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Mantiene la información de acceso al día.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Cambios reflejados son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Edición de cuentas de usuario

  Escenario: Edición exitosa de una cuenta
    Dado que existe el usuario "operador2" con una cuenta activa
    Cuando un administrador actualiza su información
    Entonces los cambios quedan reflejados en la cuenta del usuario "operador2"
```

**Supuestos / preguntas abiertas**
- No se especifica qué campos son editables; se asume datos de perfil y posibilidad de reset de contraseña, sin incluir necesariamente cambio de rol.
