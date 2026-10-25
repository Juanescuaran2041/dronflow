# Class Diagram — Logical View — Dronflow

Class specification for drawing in Visual Paradigm. Derived from `docs/historias-usuario/` and `docs/requeriments.md`.
Notation: `-` private, `+` public; `{abstract}` = abstract class or operation. Types are written `name: Type`. Class, attribute, operation and enumeration names are in English; the user stories keep the domain wording in Spanish.

---

## 1. Classes

### 1.1 Users

**User**

| Attributes | Operations |
|---|---|
| `-id: UUID` | `+authenticate(password: String): boolean` |
| `-userName: String` | `+editData(userName: String, password: String, role: Role)` |
| `-passwordHash: String` | `+deactivate()` |
| `-role: Role` | `+hasPermission(permission: Permission): boolean` |
| `-active: boolean` | |

**Role** `«enumeration»`: `ADMINISTRATOR`, `OPERATOR`. Operation: `+allows(permission: Permission): boolean`

**Permission** `«enumeration»`: `MANAGE_DRONES`, `CREATE_MISSION`, `INTERVENE_MISSION`, `RECORD_MAINTENANCE`, `VIEW_DASHBOARD`, `RECEIVE_ALERTS`, `CONFIGURE_SYSTEM`, `MANAGE_USERS`

| Role | Permissions |
|---|---|
| ADMINISTRATOR | `MANAGE_DRONES`, `VIEW_DASHBOARD`, `RECEIVE_ALERTS`, `CONFIGURE_SYSTEM`, `MANAGE_USERS` |
| OPERATOR | `MANAGE_DRONES`, `CREATE_MISSION`, `INTERVENE_MISSION`, `RECORD_MAINTENANCE` |

### 1.2 Drones

**Drone** `{abstract}`

| Attributes | Operations |
|---|---|
| `-code: String` (unique) | `+canExecute(mission: Mission): boolean` |
| `-type: String` | `+assignToMission()` |
| `-batteryCapacityMah: int` | `+completeMission(batteryThreshold: double)` |
| `-batteryLevelPercent: double` | `+finishCharging()` |
| `-enduranceMin: int` | `+releaseReservation()` |
| `-maxPayloadKg: double` | `+markOutOfService()` |
| `-equipment: List<String>` | `+sendToMaintenance()` |
| `-location: Location` | `+reactivate()` |
| `-state: DroneState` | `+decommission()` |
| | `+executeTask(mission: Mission)` `{abstract}` |

**DeliveryDrone** (extends Drone): `+executeTask(mission: Mission)`, `-pickUpCargo()`, `-dropOffCargo()`

**InspectionDrone** (extends Drone): `+executeTask(mission: Mission)`, `-captureInspectionPoint()`

**MonitoringDrone** (extends Drone): `+executeTask(mission: Mission)`, `-streamVideo()`, `-takePhoto()`

**DroneState** `«enumeration»`: `AVAILABLE`, `ON_MISSION`, `CHARGING`, `IN_MAINTENANCE`, `OUT_OF_SERVICE`, `DECOMMISSIONED`

Drone state rules:

| From | To | When |
|---|---|---|
| (registration) | AVAILABLE | Drone just registered |
| AVAILABLE | ON_MISSION | A mission is assigned to it (drone is reserved) |
| ON_MISSION | AVAILABLE | The mission ends and the battery is above the threshold, or the 3 route attempts are exhausted |
| ON_MISSION | CHARGING | The mission ends and the battery is below the threshold |
| CHARGING | AVAILABLE | The battery rises above the threshold |
| AVAILABLE | OUT_OF_SERVICE | An operator reports a fault |
| AVAILABLE | IN_MAINTENANCE | The maintenance recommendation is generated |
| IN_MAINTENANCE | AVAILABLE | Result APPROVED |
| IN_MAINTENANCE | OUT_OF_SERVICE | Result REQUIRES_REPAIR |
| OUT_OF_SERVICE / IN_MAINTENANCE | AVAILABLE | Reactivation |
| AVAILABLE / OUT_OF_SERVICE / IN_MAINTENANCE | DECOMMISSIONED | Decommission (terminal state). Not allowed from ON_MISSION |

### 1.3 Missions and routes

**Mission**

| Attributes | Operations |
|---|---|
| `-code: String` | `+assignDrone(drone: Drone)` |
| `-type: String` | `+releaseDrone()` |
| `-priority: Priority` | `+registerRouteAttempt(): int` |
| `-origin: Location` | `+takeOff()` |
| `-destination: Location` | `+reachCruise()` |
| `-requiredPayloadKg: double` | `+pause()` |
| `-minEnduranceMin: int` | `+resume()` |
| `-route: Route` | `+redirect(newDestination: Location)` |
| `-assignedDrone: Drone` (0..1) | `+startReturn()` |
| `-state: MissionState` | `+finish()` |
| `-routeAttempts: int` | `+abort()` |
| `-createdAt: Instant` | `+flightDuration(): Duration` |
| `-flightStart: Instant` | |
| `-flightEnd: Instant` | |

**MissionState** `«enumeration»`: `PENDING`, `TAKEOFF`, `IN_PROGRESS`, `PAUSED`, `RETURNING`, `COMPLETED`, `ABORTED`

**Priority** `«enumeration»`: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. Operation: `+weight(): int`

**Location**

| Attributes | Operations |
|---|---|
| `-name: String` | `+distanceTo(other: Location): double` |
| `-latitude: double` | |
| `-longitude: double` | |
| `-altitude: double` | |

**Route**

| Attributes | Operations |
|---|---|
| `-points: List<Location>` (at least 2) | `+deviationFrom(position: Location): double` |
| | `+crosses(zone: RestrictedZone): boolean` |

**RestrictedZone** (external data, read-only)

| Attributes | Operations |
|---|---|
| `-name: String` | `+intersects(route: Route): boolean` |
| `-perimeter: List<Location>` | `+contains(position: Location): boolean` |

### 1.4 Alerts

**Alert** `{abstract}`

| Attributes | Operations |
|---|---|
| `-id: UUID` | `+message(): String` `{abstract}` |
| `-generatedAt: Instant` | `+isIncident(): boolean` |
| `-severity: Severity` | |
| `-drone: Drone` | |
| `-mission: Mission` (0..1) | |

**LowBatteryAlert** (extends Alert): `-currentLevel: double`; `+message(): String`. Severity: MEDIUM

**RouteDeviationAlert** (extends Alert): `-metersDeviated: double`; `+message(): String`. Severity: HIGH

**RestrictedZoneAlert** (extends Alert): `-zoneName: String`; `+message(): String`. Severity: CRITICAL

**MaintenanceAlert** (extends Alert): `-recommendation: MaintenanceRecommendation`; `+message(): String`. Severity: LOW. Has no associated mission

**Severity** `«enumeration»`: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. Operation: `+isIncident(): boolean` (true for HIGH and CRITICAL)

### 1.5 History and maintenance

**FlightHistory**

| Attributes | Operations |
|---|---|
| `-drone: Drone` | `+registerCompletedMission(duration: Duration)` |
| `-flightHours: Duration` | `+registerIncident(alert: Alert)` |
| `-completedMissions: int` | `+resetCounters()` |
| `-incidents: List<Incident>` | |

**Incident**

| Attributes | Operations |
|---|---|
| `-alertId: UUID` | |
| `-mission: Mission` | |
| `-severity: Severity` | |
| `-moment: Instant` | |

**MaintenanceRecommendation**

| Attributes | Operations |
|---|---|
| `-id: UUID` | |
| `-drone: Drone` | |
| `-reason: String` | |
| `-generatedAt: Instant` | |

**MaintenanceRecord**

| Attributes | Operations |
|---|---|
| `-id: UUID` | |
| `-drone: Drone` | |
| `-result: MaintenanceResult` | |
| `-date: Instant` | |

**MaintenanceResult** `«enumeration»`: `APPROVED`, `REQUIRES_REPAIR`, `DECOMMISSION`. Operation: `+applyTo(drone: Drone, history: FlightHistory)`

| Result | Effect |
|---|---|
| APPROVED | Drone to AVAILABLE and `history.resetCounters()` |
| REQUIRES_REPAIR | Drone to OUT_OF_SERVICE |
| DECOMMISSION | Drone to DECOMMISSIONED |

### 1.6 Configuration (modified only by the administrator)

**SystemConfiguration** (single instance in the system)

| Attributes | Operations |
|---|---|
| `-assignmentRule: AssignmentRule` | `+updateAssignmentRule(rule: AssignmentRule)` |
| `-alertThresholds: AlertThresholds` | `+updateAlertThresholds(thresholds: AlertThresholds)` |
| `-maintenanceThresholds: MaintenanceThresholds` | `+updateMaintenanceThresholds(thresholds: MaintenanceThresholds)` |

**AssignmentRule**: `-batteryWeight: double`, `-proximityWeight: double`, `-priorityWeight: double`

**AlertThresholds**: `-batteryMinPercent: double`, `-maxDeviationMeters: double`

**MaintenanceThresholds**: `-maxHours: Duration`, `-maxMissions: int`; `+exceededBy(history: FlightHistory): boolean`

---

## 2. Relationships and multiplicities

| Source | Relationship | Target | Multiplicity (source — target) | Evidence |
|---|---|---|---|---|
| Drone | Generalization | DeliveryDrone, InspectionDrone, MonitoringDrone | — | HU-01, RF-02 |
| Alert | Generalization | LowBatteryAlert, RouteDeviationAlert, RestrictedZoneAlert, MaintenanceAlert | — | HU-09, 10, 14 |
| User | Association | Role | * — 1 | HU-19, 20 |
| Role | Dependency | Permission | 1 — 1..* | RNF-04 |
| Drone | Association | DroneState | * — 1 | HU-02 |
| Drone | Composition | Location (current location) | 1 — 1 | HU-10 |
| Mission | Association | MissionState | * — 1 | HU-07 |
| Mission | Association | Priority | * — 1 | HU-04 |
| Mission | Composition | Location (origin and destination) | 1 — 2 | HU-04 |
| Mission | Composition | Route | 1 — 1 | HU-06 |
| Route | Composition | Location (points) | 1 — 2..* | at least origin and destination |
| Mission | Association | Drone (assigned drone) | 0..* — 0..1 | HU-05: pending without a drone; a drone has at most one active mission |
| RestrictedZone | Dependency | Route (must not cross it) | 0..* — 0..* | HU-06 |
| Alert | Association | Drone | 0..* — 1 | HU-09, 10 |
| Alert | Association | Mission | 0..* — 0..1 | mission is null in MaintenanceAlert |
| Alert | Association | Severity | * — 1 | HU-12 |
| MaintenanceAlert | Association | MaintenanceRecommendation | 1 — 1 | HU-14 |
| Drone | Association | FlightHistory | 1 — 1 | HU-13 |
| FlightHistory | Composition | Incident | 1 — 0..* | HU-13 |
| Incident | Association | Mission | 0..* — 1 | HU-13 |
| Drone | Association | MaintenanceRecommendation | 1 — 0..* | HU-14 |
| Drone | Association | MaintenanceRecord | 1 — 0..* | HU-15 |
| MaintenanceRecord | Association | MaintenanceResult | * — 1 | HU-15 |
| SystemConfiguration | Composition | AssignmentRule, AlertThresholds, MaintenanceThresholds | 1 — 1 each | HU-18 |

---

## 3. Author decisions applied

| Topic | Decision |
|---|---|
| Thresholds | Global; modified by the administrator. Maintenance thresholds are separate from alert thresholds |
| Battery alert | Generated on every reading below the threshold |
| Assignment | Priority is used to choose among several pending missions when a drone becomes available |
| Route validation | Before takeoff. If the route cannot be calculated, the drone stays reserved; after 3 attempts it is released and the mission returns to pending without a drone |
| End of mission | The drone goes to AVAILABLE or CHARGING depending on its battery versus the alert threshold |
| Maintenance | The recommendation sends the drone to IN_MAINTENANCE and is shown to the administrator as an on-screen alert. An APPROVED result resets flight hours and missions |
| Visibility | Control panel and alerts are for the administrator only |
| Users | All user data is editable |
| Telemetry | Unchanged: its origin is out of scope |

**Pending validation:** severity LOW for `MaintenanceAlert` (analyst proposal, noted in HU-12).
