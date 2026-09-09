# Requerimientos del sistema — Dronflow

Sistema de Gestión Inteligente de Flotas de Drones

## Requerimientos funcionales

### Gestión de drones

| ID | Descripción |
|---|---|
| RF-01 | El sistema debe permitir registrar un dron con sus atributos (identificacion, tipo, capacidad de batería, carga útil máxima, equipamiento) |
| RF-02 | El sistema debe soportar distintos tipos de dron (entrega, inspección, monitoreo/fotografía), cada uno con comportamiento propio para ejecutar su tarea |
| RF-03 | El sistema debe controlar el estado de cada dron en todo momento: disponible, en misión, cargando, en mantenimiento, fuera de servicio |
| RF-04 | El sistema debe permitir dar de baja o reactivar un dron de la flota. |

### Gestión de misiones

| ID | Descripción |
|---|---|
| RF-05 | El sistema debe permitir crear una misión especificando tipo, prioridad, punto de origen y destino, y requisitos de la entrega (carga útil, autonomía mínima) |
| RF-06 | El sistema debe asignar automáticamente un dron disponible a una misión según un criterio configurable como la batería disponible, cercanía o prioridad |
| RF-07 | El sistema debe validar que la ruta de vuelo no atraviese zonas restringidas antes de autorizar el despegue. |
| RF-08 | El sistema debe registrar el avance de una misión (despegue, en curso, retorno, finalizada, abortada). |
| RF-09 | El sistema debe permitir a un operador intervenir manualmente una misión en curso: pausar, redirigir o abortar. |

### Monitoreo y alertas

| ID | Descripción |
|---|---|
| RF-10 | El sistema debe generar una alerta cuando la batería de un dron caiga por debajo de un umbral definido por el operador durante una misión. |
| RF-11 | El sistema debe generar una alerta cuando un dron se desvíe de su ruta planificada o ingrese a una zona restringida. |
| RF-12 | El sistema debe notificar al operador en tiempo real ante cualquier alerta generada. |
| RF-13 | El sistema debe permitir clasificar las alertas por nivel de severidad (baja, media, alta, crítica). |

### Mantenimiento

| ID | Descripción |
|---|---|
| RF-14 | El sistema debe registrar el historial de vuelos de cada dron (horas de vuelo, misiones completadas, incidencias). |
| RF-15 | El sistema debe estimar, a partir del historial de uso, cuándo un dron requerirá mantenimiento preventivo. |
| RF-16 | El sistema debe permitir registrar el resultado de un mantenimiento (aprobado, requiere reparación, dron dado de baja). |

### Panel de control / operador

| ID | Descripción |
|---|---|
| RF-17 | El sistema debe ofrecer una vista consolidada del estado de toda la flota (disponibles, en misión, en mantenimiento). |
| RF-18 | El sistema debe permitir consultar el historial de misiones pasadas de un dron o de la flota completa. |
| RF-19 | El sistema debe permitir a un operador con rol autorizado crear reglas de asignación o modificar umbrales de alerta. |

### Gestión de usuarios
 
| ID | Descripción |
|---|---|
| RF-21 | El sistema debe permitir que un administrador registre nuevos usuarios con rol de operador|
| RF-22 | El sistema debe permitir que un administrador elimine cuentas de usuario existentes|
| RF-23 | El sistema debe permitir que un administrador edite cuentas de usuario existentes|



## Requerimientos no funcionales

### Mantenibilidad
 
| ID | Descripción | Métrica |
|---|---|---|
| RNF-01 | El sistema debe estar diseñado siguiendo principios SOLID y patrones de diseño orientados a objetos, con alta cohesión y bajo acoplamiento entre módulos. | Complejidad ciclomática ≤ 10 por método; acoplamiento entre clases (CBO) ≤ 8, medido con una herramienta de análisis estático (ej. SonarQube, CheckStyle). |
| RNF-02 | El sistema debe ser extensible para incorporar nuevos tipos de dron o misión sin modificar el código existente de los módulos ya implementados (principio abierto/cerrado). | Agregar un nuevo tipo de dron o misión debe requerir la creación de ≤ 2 clases nuevas|
| RNF-03 | El código debe seguir convenciones estándar de Java (nomenclatura, organización de paquetes) para facilitar su lectura y evaluación. | 0 violaciones críticas y ≤ 5 violaciones menores por cada 1000 líneas de código, verificado con Checkstyle o análisis equivalente. |

 
### Seguridad
 
| ID | Descripción | Métrica |
|---|---|---|
| RNF-04 | El sistema debe autenticar a todo usuario antes de permitir el acceso a cualquier funcionalidad. | 100% de los casos de uso requieren sesión autenticada; 0 accesos posibles sin credenciales válidas en pruebas de acceso directo. |
| RNF-05 | Las credenciales de los usuarios deben almacenarse de forma segura, nunca en texto plano. | 100% de las contraseñas almacenadas con hash|

 
### Usabilidad
 
| ID | Descripción | Métrica |
|---|---|---|
| RNF-06 | El sistema debe ser operable por un usuario sin conocimientos técnicos avanzados, mediante una interfaz clara| Un usuario sin entrenamiento previo debe completar la tarea "consultar estado de la flota" en ≤ 2 minutos, medido en prueba de usabilidad con al menos 3 usuarios. |
| RNF-07 | El sistema debe presentar mensajes de error claros y accionables ante entradas inválidas. | 100% de los flujos con validación de entrada muestran un mensaje específico|
 
### Rendimiento
 
| ID | Descripción | Métrica |
|---|---|---|
| RNF-08 | El sistema debe responder a eventos crítico en un tiempo razonable para no afectar la experiencia del operador. | Tiempo entre la generación y notificacion ≤ 1 segundo|
| RNF-09 | El sistema debe soportar la gestión simultánea de múltiples drones sin degradar su tiempo de respuesta. | El sistema debe simular al menos 50 drones activos concurrentes manteniendo el tiempo de respuesta menor a 1 segundo |
 
### Disponibilidad y confiabilidad
 
| ID | Descripción | Métrica |
|---|---|---|
| RNF-10 | El sistema debe garantizar la persistencia del historial de vuelos y misiones sin pérdida de datos ante un cierre inesperado. | 0% de pérdida de registros ya confirmados como guardados, verificado en pruebas de interrupción forzada. |

