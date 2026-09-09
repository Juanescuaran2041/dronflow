### HU-11: Notificación en tiempo real de alertas

**Como** operador
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
    Dado que un operador tiene sesión activa en el sistema
    Cuando se genera una alerta para un dron de su flota
    Entonces el operador recibe una notificación en menos de 1 segundo desde la generación de la alerta
```

**Supuestos / preguntas abiertas**
- El canal de notificación no se especifica; se asume dentro del panel de control (HU-16), sin canal externo (email/SMS).
