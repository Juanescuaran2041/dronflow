### HU-23: Cerrar sesión

**Como** usuario del sistema (administrador u operador)
**Quiero** cerrar mi sesión
**Para** que nadie pueda seguir usando mi acceso después de que termino de trabajar

**Validación INVEST**
- I — Independent: ✅ Solo depende de que exista el inicio de sesión (HU-19).
- N — Negotiable: ✅ No impone cómo se invalida el acceso.
- V — Valuable: ✅ Protege la cuenta en equipos compartidos.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ El acceso posterior al cierre es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Cierre de sesión

  Escenario: Cierre de sesión exitoso
    Dado que el usuario "operador1" tiene una sesión activa
    Cuando cierra su sesión
    Entonces el sistema confirma el cierre de sesión

  Escenario: Acceso rechazado después de cerrar sesión
    Dado que el usuario "operador1" cerró su sesión
    Cuando intenta usar una funcionalidad con la sesión cerrada
    Entonces el sistema rechaza el acceso
    Y le pide autenticarse de nuevo
```

**Supuestos / preguntas abiertas**
- Decisión del autor: se agrega a partir de RF-20 y RNF-04 (todo acceso requiere sesión autenticada); ningún RF lo pedía de forma explícita.
- Decisión del autor: como la sesión es un token JWT (HU-19), al cerrar sesión el token se invalida en el servidor y deja de servir aunque no haya expirado.
