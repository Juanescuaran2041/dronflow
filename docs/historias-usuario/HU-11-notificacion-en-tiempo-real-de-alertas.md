### HU-11: Notificación en tiempo real de alertas

**Como** administrador
**Quiero** ser notificado en tiempo real cuando se genere cualquier alerta
**Para** reaccionar de inmediato ante situaciones que requieren mi atención

**Validación INVEST**
- I — Independent: ✅
- N — Negotiable: ✅ No impone el canal de notificación.
- V — Valuable: ✅ Reacción inmediata del operador.
- E — Estimable: ✅
- S — Small: ✅
- T — Testable: ✅ Tiempo ≤ 1 segundo (RNF-08) es medible.

**Criterios de aceptación (Gherkin)**
```gherkin
# language: es
Característica: Notificación en tiempo real de alertas

  Escenario: Notificación inmediata al generarse una alerta
    Dado que un administrador tiene sesión activa en el sistema
    Cuando se genera una alerta (incluida la de recomendación de mantenimiento, HU-14)
    Entonces el administrador recibe una notificación en menos de 1 segundo desde la generación de la alerta
```

**Supuestos / preguntas abiertas**
- La notificación es una alerta en pantalla dentro del panel de control (HU-16), sin canal externo (email/SMS). Solo la reciben los administradores.
