# Class Diagram — Logical View — Dronflow

Class specification for drawing in Visual Paradigm. Derived from `docs/historias-usuario/` and `docs/requeriments.md`.
Notation: `-` private, `+` public; `{abstract}` = abstract class or operation. Types are written `name: Type`. Class, attribute and operation names are kept in Spanish to match the user stories.

---

## 1. Classes

### 1.1 Users

**Usuario**

| Attributes | Operations |
|---|---|
| `-id: UUID` | `+autenticar(contrasena: String): boolean` |
| `-nombreUsuario: String` | `+editarDatos(nombreUsuario: String, contrasena: String, rol: Rol)` |
| `-contrasenaHash: String` | `+desactivar()` |
| `-rol: Rol` | `+tienePermiso(permiso: Permiso): boolean` |
| `-activo: boolean` | |

**Rol** `«enumeration»`: `ADMINISTRADOR`, `OPERADOR`. Operation: `+permite(permiso: Permiso): boolean`

**Permiso** `«enumeration»`: `GESTIONAR_DRONES`, `CREAR_MISION`, `INTERVENIR_MISION`, `REGISTRAR_MANTENIMIENTO`, `CONSULTAR_PANEL`, `RECIBIR_ALERTAS`, `CONFIGURAR_SISTEMA`, `GESTIONAR_USUARIOS`

| Role | Permissions |
|---|---|
| ADMINISTRADOR | `GESTIONAR_DRONES`, `CONSULTAR_PANEL`, `RECIBIR_ALERTAS`, `CONFIGURAR_SISTEMA`, `GESTIONAR_USUARIOS` |
| OPERADOR | `GESTIONAR_DRONES`, `CREAR_MISION`, `INTERVENIR_MISION`, `REGISTRAR_MANTENIMIENTO` |

### 1.2 Drones

**Dron** `{abstract}`

| Attributes | Operations |
|---|---|
| `-codigo: String` (unique) | `+puedeEjecutar(mision: Mision): boolean` |
| `-tipo: String` | `+asignarAMision()` |
| `-capacidadBateriaMah: int` | `+completarMision(umbralBateria: double)` |
| `-nivelBateriaPorcentaje: double` | `+finalizarCarga()` |
| `-autonomiaMin: int` | `+liberarReserva()` |
| `-cargaUtilMaxKg: double` | `+marcarFueraDeServicio()` |
| `-equipamiento: List<String>` | `+enviarAMantenimiento()` |
| `-ubicacion: Ubicacion` | `+reactivar()` |
| `-estado: EstadoDron` | `+darDeBaja()` |
| | `+ejecutarTarea(mision: Mision)` `{abstract}` |

**DronEntrega** (extends Dron): `+ejecutarTarea(mision: Mision)`, `-recogerCarga()`, `-depositarCarga()`

**DronInspeccion** (extends Dron): `+ejecutarTarea(mision: Mision)`, `-capturarPuntoRevision()`

**DronMonitoreo** (extends Dron): `+ejecutarTarea(mision: Mision)`, `-transmitirVideo()`, `-tomarFotografia()`

**EstadoDron** `«enumeration»`: `DISPONIBLE`, `EN_MISION`, `CARGANDO`, `EN_MANTENIMIENTO`, `FUERA_DE_SERVICIO`, `DE_BAJA`

Drone state rules:

| From | To | When |
|---|---|---|
| (registration) | DISPONIBLE | Drone just registered |
| DISPONIBLE | EN_MISION | A mission is assigned to it (drone is reserved) |
| EN_MISION | DISPONIBLE | The mission ends and the battery is above the threshold, or the 3 route attempts are exhausted |
| EN_MISION | CARGANDO | The mission ends and the battery is below the threshold |
| CARGANDO | DISPONIBLE | The battery rises above the threshold |
| DISPONIBLE | FUERA_DE_SERVICIO | An operator reports a fault |
| DISPONIBLE | EN_MANTENIMIENTO | The maintenance recommendation is generated |
| EN_MANTENIMIENTO | DISPONIBLE | Result "aprobado" |
| EN_MANTENIMIENTO | FUERA_DE_SERVICIO | Result "requiere reparación" |
| FUERA_DE_SERVICIO / EN_MANTENIMIENTO | DISPONIBLE | Reactivation |
| DISPONIBLE / FUERA_DE_SERVICIO / EN_MANTENIMIENTO | DE_BAJA | Decommission (terminal state). Not allowed from EN_MISION |

### 1.3 Missions and routes

**Mision**

| Attributes | Operations |
|---|---|
| `-codigo: String` | `+asignarDron(dron: Dron)` |
| `-tipo: String` | `+liberarDron()` |
| `-prioridad: Prioridad` | `+registrarIntentoRuta(): int` |
| `-origen: Ubicacion` | `+despegar()` |
| `-destino: Ubicacion` | `+alcanzarCrucero()` |
| `-cargaUtilRequeridaKg: double` | `+pausar()` |
| `-autonomiaMinimaMin: int` | `+reanudar()` |
| `-ruta: Ruta` | `+redirigir(nuevoDestino: Ubicacion)` |
| `-dronAsignado: Dron` (0..1) | `+iniciarRetorno()` |
| `-estado: EstadoMision` | `+finalizar()` |
| `-intentosRuta: int` | `+abortar()` |
| `-creadaEn: Instant` | `+duracionVuelo(): Duration` |
| `-inicioVuelo: Instant` | |
| `-finVuelo: Instant` | |

**EstadoMision** `«enumeration»`: `PENDIENTE`, `DESPEGUE`, `EN_CURSO`, `PAUSADA`, `RETORNO`, `FINALIZADA`, `ABORTADA`

**Prioridad** `«enumeration»`: `BAJA`, `MEDIA`, `ALTA`, `CRITICA`. Operation: `+peso(): int`

**Ubicacion**

| Attributes | Operations |
|---|---|
| `-nombre: String` | `+distanciaA(otra: Ubicacion): double` |
| `-latitud: double` | |
| `-longitud: double` | |
| `-altitud: double` | |

**Ruta**

| Attributes | Operations |
|---|---|
| `-puntos: List<Ubicacion>` (at least 2) | `+desviacionRespectoA(posicion: Ubicacion): double` |
| | `+cruza(zona: ZonaRestringida): boolean` |

**ZonaRestringida** (external data, read-only)

| Attributes | Operations |
|---|---|
| `-nombre: String` | `+intersecta(ruta: Ruta): boolean` |
| `-perimetro: List<Ubicacion>` | `+contiene(posicion: Ubicacion): boolean` |

### 1.4 Alerts

**Alerta** `{abstract}`

| Attributes | Operations |
|---|---|
| `-id: UUID` | `+mensaje(): String` `{abstract}` |
| `-generadaEn: Instant` | `+esIncidencia(): boolean` |
| `-severidad: Severidad` | |
| `-dron: Dron` | |
| `-mision: Mision` (0..1) | |

**AlertaBateriaBaja** (extends Alerta): `-nivelActual: double`; `+mensaje(): String`. Severity: MEDIA

**AlertaDesvioRuta** (extends Alerta): `-metrosDesviado: double`; `+mensaje(): String`. Severity: ALTA

**AlertaZonaRestringida** (extends Alerta): `-nombreZona: String`; `+mensaje(): String`. Severity: CRITICA

**AlertaMantenimiento** (extends Alerta): `-recomendacion: RecomendacionMantenimiento`; `+mensaje(): String`. Severity: BAJA. Has no associated mission

**Severidad** `«enumeration»`: `BAJA`, `MEDIA`, `ALTA`, `CRITICA`. Operation: `+esIncidencia(): boolean` (true for ALTA and CRITICA)

### 1.5 History and maintenance

**HistorialVuelos**

| Attributes | Operations |
|---|---|
| `-dron: Dron` | `+registrarMisionCompletada(duracion: Duration)` |
| `-horasVuelo: Duration` | `+registrarIncidencia(alerta: Alerta)` |
| `-misionesCompletadas: int` | `+reiniciarContadores()` |
| `-incidencias: List<Incidencia>` | |

**Incidencia**

| Attributes | Operations |
|---|---|
| `-idAlerta: UUID` | |
| `-mision: Mision` | |
| `-severidad: Severidad` | |
| `-momento: Instant` | |

**RecomendacionMantenimiento**

| Attributes | Operations |
|---|---|
| `-id: UUID` | |
| `-dron: Dron` | |
| `-motivo: String` | |
| `-generadaEn: Instant` | |

**RegistroMantenimiento**

| Attributes | Operations |
|---|---|
| `-id: UUID` | |
| `-dron: Dron` | |
| `-resultado: ResultadoMantenimiento` | |
| `-fecha: Instant` | |

**ResultadoMantenimiento** `«enumeration»`: `APROBADO`, `REQUIERE_REPARACION`, `DADO_DE_BAJA`. Operation: `+aplicarA(dron: Dron, historial: HistorialVuelos)`

| Result | Effect |
|---|---|
| APROBADO | Drone to DISPONIBLE and `historial.reiniciarContadores()` |
| REQUIERE_REPARACION | Drone to FUERA_DE_SERVICIO |
| DADO_DE_BAJA | Drone to DE_BAJA |

### 1.6 Configuration (modified only by the administrator)

**ConfiguracionSistema** (single instance in the system)

| Attributes | Operations |
|---|---|
| `-reglaAsignacion: ReglaAsignacion` | `+actualizarReglaAsignacion(regla: ReglaAsignacion)` |
| `-umbralesAlerta: UmbralesAlerta` | `+actualizarUmbralesAlerta(umbrales: UmbralesAlerta)` |
| `-umbralesMantenimiento: UmbralesMantenimiento` | `+actualizarUmbralesMantenimiento(umbrales: UmbralesMantenimiento)` |

**ReglaAsignacion**: `-pesoBateria: double`, `-pesoCercania: double`, `-pesoPrioridad: double`

**UmbralesAlerta**: `-bateriaMinimaPorcentaje: double`, `-desvioMaximoMetros: double`

**UmbralesMantenimiento**: `-horasMaximas: Duration`, `-misionesMaximas: int`; `+superadoPor(historial: HistorialVuelos): boolean`

---

## 2. Relationships and multiplicities

| Source | Relationship | Target | Multiplicity (source — target) | Evidence |
|---|---|---|---|---|
| Dron | Generalization | DronEntrega, DronInspeccion, DronMonitoreo | — | HU-01, RF-02 |
| Alerta | Generalization | AlertaBateriaBaja, AlertaDesvioRuta, AlertaZonaRestringida, AlertaMantenimiento | — | HU-09, 10, 14 |
| Usuario | Association | Rol | * — 1 | HU-19, 20 |
| Rol | Dependency | Permiso | 1 — 1..* | RNF-04 |
| Dron | Association | EstadoDron | * — 1 | HU-02 |
| Dron | Composition | Ubicacion (current location) | 1 — 1 | HU-10 |
| Mision | Association | EstadoMision | * — 1 | HU-07 |
| Mision | Association | Prioridad | * — 1 | HU-04 |
| Mision | Composition | Ubicacion (origin and destination) | 1 — 2 | HU-04 |
| Mision | Composition | Ruta | 1 — 1 | HU-06 |
| Ruta | Composition | Ubicacion (points) | 1 — 2..* | at least origin and destination |
| Mision | Association | Dron (assigned drone) | 0..* — 0..1 | HU-05: pending without a drone; a drone has at most one active mission |
| ZonaRestringida | Dependency | Ruta (must not cross it) | 0..* — 0..* | HU-06 |
| Alerta | Association | Dron | 0..* — 1 | HU-09, 10 |
| Alerta | Association | Mision | 0..* — 0..1 | mission is null in AlertaMantenimiento |
| Alerta | Association | Severidad | * — 1 | HU-12 |
| AlertaMantenimiento | Association | RecomendacionMantenimiento | 1 — 1 | HU-14 |
| Dron | Association | HistorialVuelos | 1 — 1 | HU-13 |
| HistorialVuelos | Composition | Incidencia | 1 — 0..* | HU-13 |
| Incidencia | Association | Mision | 0..* — 1 | HU-13 |
| Dron | Association | RecomendacionMantenimiento | 1 — 0..* | HU-14 |
| Dron | Association | RegistroMantenimiento | 1 — 0..* | HU-15 |
| RegistroMantenimiento | Association | ResultadoMantenimiento | * — 1 | HU-15 |
| ConfiguracionSistema | Composition | ReglaAsignacion, UmbralesAlerta, UmbralesMantenimiento | 1 — 1 each | HU-18 |

---

## 3. Author decisions applied

| Topic | Decision |
|---|---|
| Thresholds | Global; modified by the administrator. Maintenance thresholds are separate from alert thresholds |
| Battery alert | Generated on every reading below the threshold |
| Assignment | Priority is used to choose among several pending missions when a drone becomes available |
| Route validation | Before takeoff. If the route cannot be calculated, the drone stays reserved; after 3 attempts it is released and the mission returns to pending without a drone |
| End of mission | The drone goes to DISPONIBLE or CARGANDO depending on its battery versus the alert threshold |
| Maintenance | The recommendation sends the drone to EN_MANTENIMIENTO and is shown to the administrator as an on-screen alert. An "aprobado" result resets flight hours and missions |
| Visibility | Control panel and alerts are for the administrator only |
| Users | All user data is editable |
| Telemetry | Unchanged: its origin is out of scope |

**Pending validation:** severity BAJA for `AlertaMantenimiento` (analyst proposal, noted in HU-12).
