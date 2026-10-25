### HU-18: Configurar reglas de asignación y umbrales

**Como** administrador
**Quiero** crear o modificar las reglas de ponderación de asignación automática, los umbrales de alerta (batería y desvío) y los umbrales de mantenimiento (horas de vuelo y misiones)
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

  Escenario: Modificación exitosa del umbral de batería
    Dado que un administrador tiene sesión activa
    Cuando modifica el umbral de batería a 25%
    Entonces el sistema genera alertas de batería baja con lecturas inferiores a 25%
    Y usa 25% para decidir si un dron que termina una misión pasa a "disponible" o "cargando"

  Escenario: Modificación exitosa de los umbrales de mantenimiento
    Dado que un administrador tiene sesión activa
    Cuando modifica el umbral de mantenimiento a 120 horas de vuelo y 50 misiones
    Entonces el sistema usa esos valores para recomendar mantenimiento preventivo (HU-14)
    Y los umbrales de alerta no cambian
```

**Supuestos / preguntas abiertas**
- Los umbrales de mantenimiento son independientes de los umbrales de alerta.
