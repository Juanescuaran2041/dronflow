### HU-17: Consultar historial de misiones

**Como** administrador
**Quiero** consultar el historial de misiones pasadas de un dron o de toda la flota, filtrando por rango de fechas, dron y estado
**Para** analizar el desempeño operativo pasado

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅
- V — Valuable: ✅ Habilita análisis de desempeño histórico.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Resultados filtrados son verificables.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Consulta del historial de misiones

  Escenario: Consulta filtrada por dron y rango de fechas
    Dado que existen misiones finalizadas registradas para el dron "DRN-001"
    Cuando un administrador consulta el historial filtrando por dron "DRN-001" y un rango de fechas específico
    Entonces el sistema muestra únicamente las misiones de ese dron dentro del rango indicado

  Escenario: Consulta sin resultados
    Dado que no existen misiones registradas para el dron "DRN-099" en el rango de fechas indicado
    Cuando un administrador realiza esa consulta
    Entonces el sistema muestra un listado vacío con un mensaje indicando que no hay resultados
```

**Supuestos / preguntas abiertas**
- Ninguno relevante.
