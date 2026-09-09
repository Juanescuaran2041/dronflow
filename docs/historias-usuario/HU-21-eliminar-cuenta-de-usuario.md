### HU-21: Eliminar cuenta de usuario

**Como** administrador
**Quiero** eliminar cuentas de usuario existentes
**Para** revocar el acceso al sistema de personal que ya no debe tenerlo

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Control de accesos vigentes.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Pérdida de acceso es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Eliminación de cuentas de usuario

  Escenario: Eliminación exitosa de una cuenta
    Dado que existe el usuario "operador2" con una cuenta activa
    Cuando un administrador elimina la cuenta "operador2"
    Entonces el usuario "operador2" ya no puede iniciar sesión en el sistema
```

**Supuestos / preguntas abiertas**
- No se especifica si la eliminación es física o lógica; se asume lógica (soft-delete) para preservar trazabilidad de auditoría.
