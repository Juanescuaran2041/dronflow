# Dronflow

Sistema de Gestión Inteligente de Flotas de Drones para Misiones de Entrega, Inspección y Monitoreo.


## Descripción

Dronflow es un sistema de software para la gestión centralizada de una flota de drones autónomos que ejecutan distintos tipos de misiones: entregas, inspección de infraestructura y monitoreo o fotografía aérea. El sistema controla el ciclo de vida completo de cada dron segun su disponibilidad y asigna misiones según criterios como batería disponible, cercanía y prioridad.

Antes de cada vuelo, el sistema valida la ruta planificada contra zonas restringidas, y durante la ejecución de la misión monitorea el estado del dron para generar alertas ante eventos críticos como batería baja, desviación de ruta o ingreso a espacio aéreo prohibido. Cada dron mantiene un historial de vuelos que permite estimar cuándo requerirá mantenimiento preventivo, evitando fallas inesperadas durante una misión.

Un operador cuenta con un panel de control desde el cual puede supervisar el estado de toda la flota en tiempo simulado, consultar el historial de misiones pasadas e intervenir manualmente sobre un dron en curso cuando la situación lo requiera.

El proyecto se desarrolla en Java como trabajo final de la asignatura de Diseño de Software, con énfasis en el diseño orientado a objetos: relaciones de herencia y composición entre los distintos tipos de drones y misiones, manejo del comportamiento dinámico de cada dron a través de sus estados, y aplicación justificada de patrones de diseño para resolver problemas concretos del dominio.

## Características principales

- Gestión completa del ciclo de vida de cada dron (disponible, en misión, cargando, en mantenimiento, fuera de servicio).
- Soporte para múltiples tipos de dron: entrega, inspección y monitoreo/fotografía.
- Asignación automática de misiones según batería, cercanía y prioridad.
- Validación de rutas de vuelo contra zonas restringidas.
- Sistema de alertas por severidad (baja, media, alta, crítica).
- Historial de vuelos y estimación de mantenimiento preventivo.
- Panel de control para supervisión e intervención manual del operador.
- Gestión de roles: operador y administrador.

## Stack tecnológico

- **Backend:** obligatoriamente con **Spring Boot** (Java).
- **Base de datos:** **MongoDB**.

## Arquitectura

El proyecto sigue una **arquitectura en capas** (*layer architecture*). Cada petición atraviesa las capas siempre en el mismo sentido y una capa solo conoce a la que tiene justo debajo:

```
Controller  →  Service  →  Repository  →  MongoDB
  (REST)      (lógica de    (acceso a
              negocio)       datos)
```

- **Controller** — expone los endpoints REST, valida la entrada y traduce a DTO. No contiene lógica de negocio.
- **Service** — concentra las reglas de negocio, las transiciones de estado y la coordinación entre entidades. Es la única capa que puede llamar a varios repositorios.
- **Repository** — acceso a MongoDB. Solo operaciones de persistencia y consulta.

**Regla del proyecto: por cada clase del modelo hay un repositorio, un servicio y un controlador.**

| Clase del modelo | Repository | Service | Controller |
|---|---|---|---|
| `User` | `UserRepository` | `UserService` | `UserController` |
| `Drone` | `DroneRepository` | `DroneService` | `DroneController` |
| `Mission` | `MissionRepository` | `MissionService` | `MissionController` |
| `Alert` | `AlertRepository` | `AlertService` | `AlertController` |
| `FlightHistory` | `FlightHistoryRepository` | `FlightHistoryService` | `FlightHistoryController` |
| `MaintenanceRecord` | `MaintenanceRecordRepository` | `MaintenanceRecordService` | `MaintenanceRecordController` |
| `MaintenanceRecommendation` | `MaintenanceRecommendationRepository` | `MaintenanceRecommendationService` | `MaintenanceRecommendationController` |
| `SystemConfiguration` | `SystemConfigurationRepository` | `SystemConfigurationService` | `SystemConfigurationController` |

Quedan fuera de la regla las clases que no tienen colección propia en MongoDB:

- `DeliveryDrone`, `InspectionDrone` y `MonitoringDrone` son subtipos de `Drone` y comparten su colección, su repositorio, su servicio y su controlador.
- `Location`, `Route`, `Incident`, `AssignmentRule`, `AlertThresholds` y `MaintenanceThresholds` son objetos de valor: van embebidos en el documento de la entidad que los contiene (`Mission`, `FlightHistory` y `SystemConfiguration`).
- `RestrictedZone` no se persiste: según RF-07 las zonas restringidas son datos de configuración fija provistos externamente, y se consultan a través de un proveedor externo.


## Diagrama de clases (vista lógica)

![Diagrama de clases de Dronflow](<docs/Diagrama de clases.jpg>)

## Vista de desarrollo (tres capas)

![Vista de desarrollo de Dronflow](<docs/Development View.jpg>)

Cada entidad tiene su Controller (Presentation Layer), Service (Service Layer) y Repository (Repository Layer). El Domain Layer incluye las entidades y sus clases auxiliares (enumeraciones y objetos de valor).

## Diagrama de componentes

![Diagrama de componentes de Dronflow](<docs/Component Diagram.jpg>)

13 componentes del backend y el proveedor externo de zonas restringidas, con sus interfaces provistas y requeridas y los eventos internos (`«event»`) entre módulos.

## Diagrama de contexto

<img width="1089" height="641" alt="image" src="https://github.com/user-attachments/assets/626b5ed6-dfc9-4b5b-9ef2-abc9e4ea1f20" />

Dronflow como caja negra, con sus actores y los sistemas externos que le suministran datos. Cada línea es una funcionalidad concreta, trazada a su historia de usuario.

## Diagrama de despliegue

![Diagrama de despliegue de Dronflow](docs/vistas/deploymentView.jpg)

Muestra **dónde se ejecuta** cada parte del sistema y cómo se comunican:

- **Equipo del usuario** (`«device»`): el administrador u operador abre la aplicación web (`dronflow-frontend`, React + TS) en su navegador. El frontend vive en otro repositorio.
- **Servidor** (`«device»`): Docker Engine ejecuta tres contenedores en la red interna `dronflow-net`:
  - **Node 20** ejecuta la aplicación React + TS (imagen construida en el repositorio del frontend) en el puerto 5173.
  - **JVM 21** ejecuta `dronflow-backend.jar` (Spring Boot) en el puerto 8080: la API REST y el flujo SSE de alertas en tiempo real. Permite CORS desde el origen del frontend.
  - **MongoDB** guarda la base `dronflow` en el volumen `mongo-data`, para que los datos no se pierdan al reiniciar (RNF-10).
- **Sistemas externos** (`«node»`): el proveedor de zonas restringidas (protocolo por definir). La telemetría (batería y posición) no es un sistema externo: es interna de Gestión de Flota.

Rutas de comunicación: navegador → frontend por HTTP (puerto 5173), navegador → backend por HTTP (puerto 8080) y backend → MongoDB con el protocolo de MongoDB (puerto 27017). No se usa nginx.

## Principios GRASP aplicados

El diseño asigna cada responsabilidad siguiendo los nueve principios GRASP. Cada fila dice dónde se ve en los diagramas de clases, de tres capas y de componentes.

| Principio | Cómo se aplica en Dronflow |
|---|---|
| **Information Expert** | Cada responsabilidad la tiene la clase que posee los datos: `Drone.canExecute(mission)` decide si el dron sirve para una misión, `Route.crosses(zone)` y `Route.deviationFrom(position)` validan la ruta, `Location.distanceTo(other)` calcula la cercanía, `MaintenanceThresholds.exceededBy(history)` decide el mantenimiento y `Alert.isIncident()` decide qué alerta es incidencia. |
| **Creator** | Crea quien contiene: `FlightHistory` crea sus `Incident` (`registerIncident(alert)`), `Mission` contiene su `Route` y `SystemConfiguration` contiene sus tres reglas. Las entidades nuevas las crean los Service del caso de uso (*creates and returns*). |
| **Controller** | Un `@RestController` por entidad recibe la petición HTTP y delega en su Service, sin lógica de negocio. Solo expone lo que un usuario pide: por ejemplo, `FlightHistoryController` solo consulta el historial. |
| **Low Coupling** | Controller → Service → Repository, y ningún componente usa el repositorio de otro: se comunican por interfaces. Los ciclos se rompen con eventos (`MissionCompleted`, `HistoryUpdated`, `DroneAvailable`, `TelemetryReceived`). Meta de CBO ≤ 8 (RNF-01). |
| **High Cohesion** | Un Service por entidad con las reglas de su caso de uso; los Repository solo persisten y las entidades solo guardan su estado y sus reglas. |
| **Polymorphism** | `Drone.executeTask(mission)` cambia según el subtipo (`DeliveryDrone`, `InspectionDrone`, `MonitoringDrone`). Los estados del dron y de la misión usan el patrón State, y los criterios de asignación (batería, cercanía, prioridad) y las reglas de alerta son implementaciones intercambiables de una interfaz. |
| **Pure Fabrication** | Clases que no son del dominio y existen para mantener la cohesión: los Service y Repository, `RouteValidator`, las fábricas de drones (`DroneFactory`), `PasswordHasher` y el canal SSE de alertas. |
| **Indirection** | Entre Monitoreo y Notificación hay un publicador de alertas (patrón Observer); entre módulos, eventos; y el proveedor de zonas restringidas se usa a través de la interfaz `RestrictedZoneProvider`. |
| **Protected Variations** | Lo que puede cambiar queda detrás de una interfaz: el proveedor externo de zonas (protocolo aún sin definir), el algoritmo de contraseñas (`PasswordHasher`) y la creación de drones (`DroneFactory`): un tipo de dron nuevo requiere como máximo 2 clases nuevas, sin tocar el código existente (RNF-02). |

## Patrones de diseño

### Factory Method: creación de drones (RF-02, RNF-02)

**Problema:** al registrar un dron (HU-01) llega un `type` (`delivery`, `inspection` o `monitoring`) y hay que crear la subclase correcta de `Drone`. Con un `if`/`switch` sobre el tipo, cada tipo nuevo obligaría a modificar `DroneService`, y RNF-02 pide agregar tipos sin tocar el código existente y con máximo 2 clases nuevas.

**Solución:** cada tipo de dron tiene su propia fábrica, y todas cumplen la misma interfaz.

| Rol del patrón | Clase en Dronflow |
|---|---|
| Producto | `Drone` (abstracta) |
| Productos concretos | `DeliveryDrone`, `InspectionDrone`, `MonitoringDrone` |
| Creador | `DroneFactory` (interfaz): `type()` y `create(data)` |
| Creadores concretos | `DeliveryDroneFactory`, `InspectionDroneFactory`, `MonitoringDroneFactory` (cada uno es un `@Component`) |
| Cliente | `DroneService` |

**Cómo funciona:**
1. Spring encuentra todas las clases `@Component` que implementan `DroneFactory` y se las entrega a `DroneService` como una lista.
2. `DroneService` las guarda en un mapa indexado por `type()`. Este mapa es el registro de fábricas.
3. En `register(data)`, el servicio busca la fábrica de `data.type()` y llama a `create(data)`. Si el tipo no existe, responde 400 con la lista de tipos soportados.
4. El servicio solo conoce a `Drone` y a `DroneFactory`: no sabe qué subclases existen.

**Agregar un tipo nuevo**, por ejemplo un dron de fumigación, requiere solo 2 clases nuevas: `SprayingDrone extends Drone` y `SprayingDroneFactory implements DroneFactory` con `@Component`. No se modifica ninguna clase existente (principio abierto/cerrado), y así se cumple RNF-02.

Los tres subtipos se guardan en la misma colección `drones`. Spring Data agrega el campo `_class` para saber qué subclase crear al leerlos.

### Singleton: configuración del sistema (HU-18)

`SystemConfiguration` existe una sola vez en todo el sistema: es un único documento de Mongo con id fijo (`"system"`), y solo `SystemConfigurationService` (un bean de Spring, que también es único) lo crea y lo lee. Si el documento todavía no existe, el servicio lo crea con los valores por defecto de las HU: ponderación 0.33 / 0.33 / 0.34, batería 20 %, desvío 50 m y mantenimiento 120 h o 50 misiones. Así todos los módulos leen la misma ponderación y los mismos umbrales, y un cambio del administrador aplica de inmediato a todo el sistema.

### Strategy: reglas de alerta (HU-09, HU-10)

Cada condición que genera una alerta es una estrategia que implementa la interfaz `AlertRule`: `LowBatteryRule` (batería bajo el umbral), `RouteDeviationRule` (desvío mayor a la distancia configurada) y `RestrictedZoneRule` (ingreso a una zona restringida). `AlertService` recibe todas las reglas de Spring y aplica cada una a la lectura del dron. Para agregar una regla nueva basta con una clase `@Component` más, sin tocar el servicio. La severidad de cada alerta la define su tipo (`AlertType`), según la tabla de HU-12.

## Autor

-🧑‍💻 Juan Esteban Cuaran Santander — Estudiante de Ingeniería de Software 

