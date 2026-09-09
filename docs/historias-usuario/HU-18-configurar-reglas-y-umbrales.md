### HU-18: Configurar reglas de asignación y umbrales de alerta

**Como** administrador
**Quiero** crear o modificar las reglas de ponderación de asignación automática y los umbrales de alerta
**Para** ajustar el comportamiento del sistema a las necesidades operativas de la flota

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Permite adaptar el sistema sin cambios de código.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Cambio de configuración aplicado es verificable.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Configuración de reglas de asignación y umbrales de alerta

  Escenario: Modificación exitosa de la ponderación de criterios de asignación
    Dado que un administrador tiene sesión activa
    Cuando modifica la ponderación de los criterios de asignación (batería, cercanía, prioridad)
    Entonces el sistema aplica la nueva ponderación a las siguientes asignaciones automáticas

  Escenario: Modificación exitosa de un umbral de alerta
    Dado que un administrador tiene sesión activa
    Cuando modifica el umbral de desvío de ruta a 80 metros
    Entonces el sistema utiliza 80 metros como nuevo umbral para generar alertas de desvío
```

**Supuestos / preguntas abiertas**
- Ninguno relevante.
