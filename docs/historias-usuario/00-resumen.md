# Resumen de historias de usuario — Dronflow

Backlog derivado de `docs/requeriments.md`. RF-02 se fusionó dentro de HU-01 (ver supuestos de esa historia).

| ID | Título | Valor de negocio | RF origen |
|---|---|---|---|
| [HU-01](HU-01-registro-de-dron.md) | Registro de un dron | Incorporar drones al inventario disponible | RF-01, RF-02 |
| [HU-02](HU-02-estado-operativo-del-dron.md) | Estado operativo del dron | Saber si un dron puede asignarse o requiere atención | RF-03 |
| [HU-03](HU-03-baja-y-reactivacion-de-dron.md) | Baja o reactivación de un dron | Retirar o reincorporar drones al servicio | RF-04 |
| [HU-04](HU-04-creacion-de-mision.md) | Crear una misión | Punto de entrada del flujo operativo | RF-05 |
| [HU-05](HU-05-asignacion-automatica-de-dron.md) | Asignación automática de dron | Automatizar la asignación dron-misión | RF-06 |
| [HU-06](HU-06-validacion-de-ruta-zonas-restringidas.md) | Validación de ruta contra zonas restringidas | Evitar infracciones/incidentes en vuelo | RF-07 |
| [HU-07](HU-07-seguimiento-de-avance-de-mision.md) | Seguimiento del avance de una misión | Visibilidad del progreso en tiempo real | RF-08 |
| [HU-08](HU-08-intervencion-manual-de-mision.md) | Intervención manual de una misión | Reaccionar ante imprevistos en vuelo | RF-09 |
| [HU-09](HU-09-alerta-de-bateria-baja.md) | Alerta de batería baja | Prevenir pérdida de dron por falta de energía | RF-10 |
| [HU-10](HU-10-alerta-de-desvio-o-zona-restringida.md) | Alerta de desvío o zona restringida | Detectar comportamiento anómalo del dron | RF-11 |
| [HU-11](HU-11-notificacion-en-tiempo-real-de-alertas.md) | Notificación en tiempo real de alertas | Reacción inmediata del operador | RF-12 |
| [HU-12](HU-12-clasificacion-de-alertas-por-severidad.md) | Clasificación de alertas por severidad | Priorizar atención sobre alertas urgentes | RF-13 |
| [HU-13](HU-13-historial-de-vuelos-del-dron.md) | Historial de vuelos del dron | Trazabilidad de uso y desempeño | RF-14 |
| [HU-14](HU-14-recomendacion-de-mantenimiento-preventivo.md) | Recomendación de mantenimiento preventivo | Anticipar fallas de drones | RF-15 |
| [HU-15](HU-15-registrar-resultado-de-mantenimiento.md) | Registrar resultado de mantenimiento | Mantener actualizado el estado de la flota | RF-16 |
| [HU-16](HU-16-vista-consolidada-de-la-flota.md) | Vista consolidada de la flota | Visibilidad global de la operación | RF-17 |
| [HU-17](HU-17-consultar-historial-de-misiones.md) | Consultar historial de misiones | Análisis del desempeño operativo pasado | RF-18 |
| [HU-18](HU-18-configurar-reglas-y-umbrales.md) | Configurar reglas de asignación y umbrales | Ajustar el comportamiento del sistema | RF-19 |
| [HU-19](HU-19-autenticacion-de-usuario.md) | Autenticación de usuario | Acceso controlado según rol | RF-20 |
| [HU-20](HU-20-registrar-usuario-operador.md) | Registrar nuevo usuario operador | Dar acceso al personal operativo | RF-21 |
| [HU-21](HU-21-eliminar-cuenta-de-usuario.md) | Eliminar cuenta de usuario | Revocar accesos obsoletos | RF-22 |
| [HU-22](HU-22-editar-cuenta-de-usuario.md) | Editar cuenta de usuario | Mantener datos de acceso actualizados | RF-23 |

## Decisiones confirmadas con el usuario antes de generar el backlog
- Registrar/dar de baja/reactivar drones: **administrador u operador**, sin distinción de permisos (HU-01, HU-03).
- Registrar resultado de mantenimiento: **operador** (HU-15).
- Mapeo tipo de alerta → severidad: definido como ejemplo razonable por el analista, sujeto a validación de negocio (HU-12).
- "Redirigir" una misión: significa asignar un **nuevo destino**, no forzar el regreso a origen (HU-08).
