# Mockups por historia de usuario

Un archivo `.drawio` por historia de usuario, con la pantalla del frontend que la cubre.
Cada mockup está dibujado a partir del código del frontend ya implementado
(`dronflow-frontend/src/modules/...`): los mismos campos, las mismas columnas, los mismos
textos de botón y la misma paleta (`src/index.css`).

**Para abrirlos:** `app.diagrams.net` → *File → Open from → Device*, o arrastrar el archivo.
También se pueden pegar: *Extras → Edit Diagram*, borrar lo que haya y pegar el XML.

## Historias con pantalla

| HU | Pantalla | Ruta | Qué mira esta historia |
|---|---|---|---|
| [HU-01](HU-01-registro-de-dron.drawio) | Registrar dron | `/drones/new` | Formulario de alta: identificación, tipo, batería, autonomía, carga y equipamiento |
| [HU-02](HU-02-estado-operativo-del-dron.drawio) | Flota | `/drones` | Columna Estado (chip de color) y acción «Reportar avería» |
| [HU-03](HU-03-baja-y-reactivacion-de-dron.drawio) | Flota | `/drones` | Acciones «Reactivar» y «Dar de baja» según el estado de cada fila |
| [HU-04](HU-04-creacion-de-mision.drawio) | Crear misión | `/missions/new` | Tipo, prioridad, origen y destino, carga útil y autonomía mínima |
| [HU-05](HU-05-asignacion-automatica-de-dron.drawio) | Detalle de misión | `/missions/:code` | Aviso de creación y campo «Dron asignado»: la elección la hace el sistema |
| [HU-06](HU-06-validacion-de-ruta-zonas-restringidas.drawio) | Detalle de misión | `/missions/:code` | Rechazo del despegue por zona restringida, con el motivo y el contador de intentos |
| [HU-07](HU-07-seguimiento-de-avance-de-mision.drawio) | Detalle de misión | `/missions/:code` | Ficha completa: estado, ruta y marcas de tiempo |
| [HU-08](HU-08-intervencion-manual-de-mision.drawio) | Detalle de misión | `/missions/:code` | Pausar / Abortar y el panel de redirección a un destino nuevo |
| [HU-09](HU-09-alerta-de-bateria-baja.drawio) | Alertas | `/alerts` | Listado filtrado por tipo «Batería baja» |
| [HU-10](HU-10-alerta-de-desvio-o-zona-restringida.drawio) | Alertas | `/alerts` | Alertas de desvío de ruta y de zona restringida |
| [HU-11](HU-11-notificacion-en-tiempo-real-de-alertas.drawio) | Alertas | `/alerts` | Aviso emergente que llega por SSE sin recargar |
| [HU-12](HU-12-clasificacion-de-alertas-por-severidad.drawio) | Alertas | `/alerts` | Chip de severidad y filtro por severidad |
| [HU-13](HU-13-historial-de-vuelos-del-dron.drawio) | Detalle del dron | `/drones/:code` | Horas de vuelo, misiones completadas e incidencias |
| [HU-14](HU-14-recomendacion-de-mantenimiento-preventivo.drawio) | Mantenimiento | `/maintenance-recommendations` | Recomendaciones generadas al superar los umbrales |
| [HU-15](HU-15-registrar-resultado-de-mantenimiento.drawio) | Detalle del dron | `/drones/:code` | Alta del resultado de mantenimiento y su historial |
| [HU-16](HU-16-vista-consolidada-de-la-flota.drawio) | Flota | `/drones` | Tabla con todos los drones activos y sus características |
| [HU-17](HU-17-consultar-historial-de-misiones.drawio) | Misiones | `/missions` | Buscador por código y filtros por dron, fechas y estado |
| [HU-18](HU-18-configurar-reglas-y-umbrales.drawio) | Configuración | `/configuration` | Ponderación de asignación y umbrales de alerta y mantenimiento |
| [HU-19](HU-19-autenticacion-de-usuario.drawio) | Acceso | `/login` | Usuario y contraseña; el rol decide el menú posterior |
| [HU-20](HU-20-registrar-usuario-operador.drawio) | Registrar operador | `/users/new` | Alta de operador, solo para el administrador |
| [HU-23](HU-23-cerrar-sesion.drawio) | Barra lateral | cualquiera | El botón vive al pie del menú, bajo el usuario y su rol |

## Historias sin pantalla

Estas tres existen en la API pero **no tienen interfaz en el frontend**, así que no se
dibujó un mockup: inventarlo sería diseñar una pantalla que nadie aprobó.

| HU | Endpoint que la cubre |
|---|---|
| HU-21 — Eliminar cuenta de usuario | `DELETE /api/v1/users/{id}` |
| HU-22 — Editar cuenta de usuario | `PUT /api/v1/users/{id}` |
| HU-24 — Promover operador a administrador | `PUT /api/v1/users/{id}/role` |

Se prueban con la colección de Postman (`postman/`), carpeta «1. Acceso y usuarios».
