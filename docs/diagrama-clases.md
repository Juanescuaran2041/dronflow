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
| `-userName: String` | `+editData(userName: String, password: String, role: Role): void` |
| `-passwordHash: String` | `+deactivate(): void` |
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
| `-type: String` | `+assignToMission(): void` |
| `-batteryCapacityMah: int` | `+completeMission(batteryThreshold: double): void` |
| `-batteryLevelPercent: double` | `+finishCharging(): void` |
| `-enduranceMin: int` | `+releaseReservation(): void` |
| `-maxPayloadKg: double` | `+markOutOfService(): void` |
| `-equipment: List<String>` | `+sendToMaintenance(): void` |
| `-location: Location` | `+reactivate(): void` |
| `-state: DroneState` | `+decommission(): void` |
| | `+executeTask(mission: Mission): void` `{abstract}` |

**DeliveryDrone** (extends Drone): `+executeTask(mission: Mission): void`, `-pickUpCargo(): void`, `-dropOffCargo(): void`

**InspectionDrone** (extends Drone): `+executeTask(mission: Mission): void`, `-captureInspectionPoint(): void`

**MonitoringDrone** (extends Drone): `+executeTask(mission: Mission): void`, `-streamVideo(): void`, `-takePhoto(): void`

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
| `-code: String` | `+assignDrone(drone: Drone): void` |
| `-type: String` | `+releaseDrone(): void` |
| `-priority: Priority` | `+registerRouteAttempt(): int` |
| `-origin: Location` | `+takeOff(): void` |
| `-destination: Location` | `+reachCruise(): void` |
| `-requiredPayloadKg: double` | `+pause(): void` |
| `-minEnduranceMin: int` | `+resume(): void` |
| `-route: Route` | `+redirect(newDestination: Location): void` |
| `-assignedDrone: Drone` (0..1) | `+startReturn(): void` |
| `-state: MissionState` | `+finish(): void` |
| `-routeAttempts: int` | `+abort(): void` |
| `-createdAt: LocalDateTime` | `+flightDuration(): Duration` |
| `-flightStart: LocalDateTime` | |
| `-flightEnd: LocalDateTime` | |

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
| `-generatedAt: LocalDateTime` | `+isIncident(): boolean` |
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
| `-drone: Drone` | `+registerCompletedMission(duration: Duration): void` |
| `-flightHours: Duration` | `+registerIncident(alert: Alert): void` |
| `-completedMissions: int` | `+resetCounters(): void` |
| `-incidents: List<Incident>` | |

**Incident**

| Attributes | Operations |
|---|---|
| `-alertId: UUID` | |
| `-mission: Mission` | |
| `-severity: Severity` | |
| `-moment: LocalDateTime` | |

**MaintenanceRecommendation**

| Attributes | Operations |
|---|---|
| `-id: UUID` | |
| `-drone: Drone` | |
| `-reason: String` | |
| `-generatedAt: LocalDateTime` | |

**MaintenanceRecord**

| Attributes | Operations |
|---|---|
| `-id: UUID` | |
| `-drone: Drone` | |
| `-result: MaintenanceResult` | |
| `-date: LocalDateTime` | |

**MaintenanceResult** `«enumeration»`: `APPROVED`, `REQUIRES_REPAIR`, `DECOMMISSION`. Operation: `+applyTo(drone: Drone, history: FlightHistory): void`

| Result | Effect |
|---|---|
| APPROVED | Drone to AVAILABLE and `history.resetCounters()` |
| REQUIRES_REPAIR | Drone to OUT_OF_SERVICE |
| DECOMMISSION | Drone to DECOMMISSIONED |

### 1.6 Configuration (modified only by the administrator)

**SystemConfiguration** `«singleton»` (single instance in the system)

| Attributes | Operations |
|---|---|
| `-instance: SystemConfiguration` `{static}` | `+getInstance(): SystemConfiguration` `{static}` |
| `-assignmentRule: AssignmentRule` | `+getAssignmentRule(): AssignmentRule` |
| `-alertThresholds: AlertThresholds` | `+getAlertThresholds(): AlertThresholds` |
| `-maintenanceThresholds: MaintenanceThresholds` | `+getMaintenanceThresholds(): MaintenanceThresholds` |
| | `+updateAssignmentRule(rule: AssignmentRule): void` |
| | `+updateAlertThresholds(thresholds: AlertThresholds): void` |
| | `+updateMaintenanceThresholds(thresholds: MaintenanceThresholds): void` |

The constructor is private; the only way to get the instance is `getInstance()`. The update operations change the instance and save it, so every reader (assignment, monitoring, maintenance, end of mission) sees the new values on its next call. Implementation in Spring Boot: a singleton-scoped bean that loads the single MongoDB document (fixed id) at startup, instead of a hand-written static field.

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
| Route | Dependency (arrow to RestrictedZone) | RestrictedZone (must not cross it) | 0..* — 0..* | HU-06 |
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
| System configuration | Singleton pattern: one instance holds the assignment rule and both threshold groups |

**Pending validation:** severity LOW for `MaintenanceAlert` (analyst proposal, noted in HU-12).

---

## 4. Attribute types and how state is modeled

- `equipment` is `List<String>` (free text, no closed catalog, HU-01).
- `location` is a `Location` object (name, latitude, longitude, altitude), not a date type.
- All date-time attributes use `LocalDateTime`: `createdAt`, `flightStart`, `flightEnd`, `generatedAt`, `moment`, `date`. Durations use `Duration`.
- **State** is an attribute whose type is an enumeration: `Drone.state: DroneState` and `Mission.state: MissionState`. In the logical view it is just that enum; the allowed transitions are the table in section 1.2 (for missions, the state diagram of HU-07/08). An invalid transition throws `IllegalOperationException`.
- In the development view the enum is paired with an interface, one class per state, so each state decides which transitions are valid (State pattern): `DroneStateHandler` with `AvailableState`, `OnMissionState`, `ChargingState`, `InMaintenanceState`, `OutOfServiceState`, `DecommissionedState`; and `MissionStateHandler` with `PendingState`, `TakeoffState`, `InProgressState`, `PausedState`, `ReturningState`, `CompletedState`, `AbortedState`. `Drone.state` stays the enum; the handler is looked up from it.

---

## 5. Index of classes, enumerations and interfaces

### 5.1 Logical view

| Kind | Name |
|---|---|
| Abstract class | `Drone`, `Alert` |
| Class | `User`, `DeliveryDrone`, `InspectionDrone`, `MonitoringDrone`, `Mission`, `Location`, `Route`, `RestrictedZone`, `LowBatteryAlert`, `RouteDeviationAlert`, `RestrictedZoneAlert`, `MaintenanceAlert`, `FlightHistory`, `Incident`, `MaintenanceRecommendation`, `MaintenanceRecord`, `SystemConfiguration`, `AssignmentRule`, `AlertThresholds`, `MaintenanceThresholds` |
| Enumeration | `Role`, `Permission`, `DroneState`, `MissionState`, `Priority`, `Severity`, `MaintenanceResult` |
| Interface | none (the logical view only has domain concepts) |

### 5.2 Development view

| Package | Kind | Name | Main operations |
|---|---|---|---|
| fleet | Interface | `DroneStateHandler` | `assignToMission`, `completeMission`, `finishCharging`, `markOutOfService`, `sendToMaintenance`, `reactivate`, `decommission` |
| fleet | Abstract class | `BaseDroneState` | rejects every transition by default |
| fleet | Classes | `AvailableState`, `OnMissionState`, `ChargingState`, `InMaintenanceState`, `OutOfServiceState`, `DecommissionedState` | override only the valid transitions |
| fleet | Interface | `DroneFactory` | `type()`, `create(DroneData)` |
| fleet | Classes | `DeliveryDroneFactory`, `InspectionDroneFactory`, `MonitoringDroneFactory`, `DroneFactoryRegistry` | `supports(type)`, `create(DroneData)` |
| fleet | Class | `DroneService` | `register`, `reportFault`, `decommission`, `reactivate` |
| fleet | Interface | `DroneRepository` | `save`, `findById` |
| missions | Interface | `MissionStateHandler` | `assignDrone`, `takeOff`, `reachCruise`, `startReturn`, `finish`, `pause`, `resume`, `redirect`, `abort` |
| missions | Abstract class | `BaseMissionState` | rejects every transition by default |
| missions | Classes | `PendingState`, `TakeoffState`, `InProgressState`, `PausedState`, `ReturningState`, `CompletedState`, `AbortedState` | override only the valid transitions |
| missions | Class | `MissionService` | `create`, `authorizeTakeoff`, `pause`, `resume`, `redirect`, `abort` |
| missions | Interface | `MissionRepository` | `save`, `findById`, `find(MissionFilter)` |
| assignment | Class | `AssignmentService` | `assignDrone(mission, drones, rule)`, `chooseMission(drone, missions, rule)` |
| assignment | Interface | `AssignmentCriterion` | `score(drone, mission)` |
| assignment | Classes | `BatteryCriterion`, `ProximityCriterion`, `PriorityCriterion` | implement `AssignmentCriterion` |
| routes | Class | `RouteValidator` | `validate(route)` |
| routes | Value object | `ValidationResult` | `authorized`, `reason` |
| routes | Interface | `RestrictedZoneProvider` | `getZones()` |
| monitoring | Class | `MonitoringService` | `evaluate(drone, mission, thresholds)` |
| monitoring | Interface | `AlertRule` | `evaluate(drone, mission, thresholds): Optional<Alert>` |
| monitoring | Classes | `LowBatteryRule`, `RouteDeviationRule`, `RestrictedZoneRule` | implement `AlertRule` |
| monitoring | Class | `SeverityClassifier` | `classify(alert)` |
| monitoring | Interface | `AlertRepository` | `save`, `findByMission` |
| notification | Interface | `AlertPublisher` (Subject) | `subscribe`, `unsubscribe`, `publish(alert)` |
| notification | Class | `AsyncAlertPublisher` | implements `AlertPublisher` |
| notification | Interface | `AlertObserver` (Observer) | `onAlert(alert)` |
| notification | Class | `UserNotificationChannel` | implements `AlertObserver` |
| history | Class | `FlightHistoryService` | `onMissionCompleted(MissionCompleted)` |
| history | Events | `MissionCompleted`, `HistoryUpdated` | published between modules |
| history | Interface | `FlightHistoryRepository` | `save`, `findByDrone` |
| maintenance | Class | `MaintenanceService` | `onHistoryUpdated(HistoryUpdated)`, `recordResult(drone, result)` |
| maintenance | Interfaces | `MaintenanceRecordRepository`, `MaintenanceRecommendationRepository` | `save`, `findByDrone` |
| configuration | Interface | `ConfigurationRepository` | `get`, `save` |
| users | Classes | `AuthenticationService`, `UserService`, `Session` | `login`; `registerOperator`, `edit`, `delete` |
| users | Interface | `PasswordHasher` | `hash`, `matches` |
| users | Class | `BCryptHasher` | implements `PasswordHasher` |
| users | Interface | `UserRepository` | `save`, `findById`, `findByUserName` |
| panel | Class | `DashboardService` | `fleetSummary`, `queryMissions(filter)` |
| panel | Value objects | `FleetSummary`, `MissionFilter` | |
| shared | Interface | `Repository<T, ID>` | `save`, `findById` |
| shared | Exception | `IllegalOperationException` | thrown by an invalid state transition |
