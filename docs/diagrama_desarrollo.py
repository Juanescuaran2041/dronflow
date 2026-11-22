"""Genera los SVG del diagrama de despliegue y de la vista de desarrollo REST.
Uso: python diagrama_desarrollo.py   (escribe en docs/vistas/)"""
import os
from uml_lib import Diagrama

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vistas")
os.makedirs(OUT, exist_ok=True)


# =================================================================== despliegue
# Notación estricta de Visual Paradigm: nodos (cubo 3D) con «device» / «executionEnvironment»,
# artefactos anidados dentro del nodo donde se despliegan, rutas de comunicación SOLO entre
# nodos (VP no deja unir dos artefactos) y notas para lo que aún no está definido.
def despliegue():
    d = Diagrama("Dronflow — Deployment diagram · option A: Docker Compose")
    d.nodo("pc", "User machine", "device", 40, 240, 300, 270, centrado=True)
    d.nodo("nav", "Web browser", "executionEnvironment", 62, 320, 256, 170, centrado=True)
    d.artefacto("web", "dronflow-web", 82, 400, 216, centrado=True)

    d.nodo("host", "Host server", "device", 490, 120, 1400, 500, centrado=True)
    d.nodo("dk", "Docker Engine", "executionEnvironment", 515, 195, 1350, 400, centrado=True)
    d.nodo("ng", "nginx · dronflow-frontend", "executionEnvironment", 540, 290, 330, 250, centrado=True)
    d.artefacto("dist", "dist (React build)", 565, 380, 280, centrado=True)
    d.artefacto("ngc", "nginx.conf", 565, 460, 280, centrado=True)
    d.nodo("jvm", "JVM 21 · dronflow-backend", "executionEnvironment", 1030, 290, 330, 250, centrado=True)
    d.artefacto("jar", "dronflow-backend.jar", 1055, 380, 280, centrado=True)
    d.nodo("mg", "MongoDB · dronflow-mongo", "executionEnvironment", 1520, 290, 320, 250, centrado=True)
    d.artefacto("bd", "dronflow (database)", 1545, 380, 280, centrado=True)
    d.artefacto("vol", "mongo-data (volume)", 1545, 460, 280, centrado=True)

    d.nodo("zon", "Restricted Zone\nProvider", "node", 2020, 230, 260, 110, centrado=True)
    d.nodo("tel", "Telemetry Source", "node", 2020, 480, 260, 110, centrado=True)

    d.ruta("nav", "ng", "«HTTP»\nport 80", via=[(340, 405), (530, 405), (530, 480)])
    d.ruta("ng", "jvm", "«HTTP»\nport 8080", via=[(880, 480), (1020, 480)])
    d.ruta("jvm", "mg", "«MongoDB»\nport 27017", via=[(1370, 480), (1510, 480)])
    d.ruta("host", "zon", "to be defined")
    d.ruta("tel", "host", "to be defined")

    d.nota("n1", ["docker-compose.yml · internal network dronflow-net.",
                  "Only the dronflow-frontend container publishes",
                  "a port (80) outside the server."], 490, 680)
    d.ancla("n1", "dk")
    d.nota("n2", ["HTTPS and certificate: pending", "if the server is exposed", "outside the local network."], 40, 570)
    d.ancla("n2", "pc")
    d.nota("n3", ["Protocol and format pending", "(RF-07, HU-06, HU-10).", "Consumed by dronflow-backend."], 2020, 370)
    d.ancla("n3", "zon")
    d.nota("n4", ["Out of scope: HU-07 does not define", "where telemetry comes from.", "Received by dronflow-backend."], 2020, 620)
    d.ancla("n4", "tel")
    d.guardar(os.path.join(OUT, "despliegue.svg"))


def despliegue_simple():
    """Opción B, como el ejemplo del curso: sin Docker; el JAR sirve la API y el build de React."""
    d = Diagrama("Dronflow — Deployment diagram · option B: JVM + MongoDB (no Docker)")
    d.nodo("pc", "User machine", "device", 40, 230, 300, 270, centrado=True)
    d.nodo("nav", "Web browser", "executionEnvironment", 62, 310, 256, 170, centrado=True)
    d.artefacto("web", "dronflow-web", 82, 390, 216, centrado=True)

    d.nodo("host", "Application server", "device", 480, 150, 930, 330, centrado=True)
    d.nodo("jvm", "JVM 21", "executionEnvironment", 510, 240, 380, 200, centrado=True)
    d.artefacto("jar", "dronflow-backend.jar", 535, 330, 330, centrado=True)
    d.nodo("mg", "MongoDB Server", "executionEnvironment", 1030, 240, 350, 200, centrado=True)
    d.artefacto("bd", "dronflow (database)", 1055, 330, 300, centrado=True)

    d.nodo("zon", "Restricted Zone\nProvider", "node", 1550, 240, 260, 110, centrado=True)
    d.nodo("tel", "Telemetry Source", "node", 1550, 470, 260, 110, centrado=True)

    d.ruta("nav", "jvm", "«HTTP»\nport 8080", via=[(340, 395), (500, 395)])
    d.ruta("jvm", "mg", "«MongoDB»\nport 27017", via=[(900, 390), (1020, 390)])
    d.ruta("host", "zon", "to be defined")
    d.ruta("tel", "host", "to be defined")

    d.nota("n1", ["dronflow-backend.jar serves the REST API, the SSE stream",
                  "and the React build packaged in",
                  "src/main/resources/static (single origin: no CORS)."], 480, 560)
    d.ancla("n1", "jar")
    d.nota("n2", ["HTTPS and certificate: pending", "if the server is exposed", "outside the local network."], 40, 560)
    d.ancla("n2", "pc")
    d.nota("n3", ["Protocol and format pending", "(RF-07, HU-06, HU-10).", "Consumed by dronflow-backend."], 1550, 370)
    d.ancla("n3", "zon")
    d.nota("n4", ["Out of scope: HU-07 does not define", "where telemetry comes from.", "Received by dronflow-backend."], 1550, 620)
    d.ancla("n4", "tel")
    d.guardar(os.path.join(OUT, "despliegue-simple.svg"))


# =================================================================== vista de desarrollo (tres capas)
# Formato del curso ("Diagrama UML de clases: implementación organizada en tres capas"):
# un marco por capa, clases con sus operaciones, asociaciones continuas Controller → Service →
# Repository (referencias inyectadas), dependencias punteadas hacia el modelo de dominio y
# generalización con triángulo hueco. El modelo de dominio va aparte: no es una cuarta capa.
COLUMNAS = [
    ("User", "UserController", [
        "+login(credentials) : Session",
        "+registerOperator(data) : User",
        "+edit(id, data) : User",
        "+delete(id) : void",
        "+listUsers() : List<User>"],
     "UserService", [
        "+login(userName, password) : Session",
        "+registerOperator(data) : User",
        "+edit(id, data) : User",
        "+delete(id) : void",
        "+listUsers() : List<User>"],
     "UserRepository", [
        "+save(user) : User",
        "+findById(id) : Optional<User>",
        "+findByUserName(userName) : Optional<User>",
        "+findByActiveTrue() : List<User>"],
     None, [
        "-UUID id", "-String userName", "-String passwordHash", "-Role role", "-boolean active"], [
        "+authenticate(password) : boolean",
        "+editData(userName, password) : void",
        "+deactivate() : void",
        "+hasPermission(permission) : boolean"],
     "creates and returns"),
    ("Drone", "DroneController", [
        "+register(data) : Drone",
        "+listAll() : List<Drone>",
        "+findByCode(code) : Drone",
        "+fleetSummary() : FleetSummary",
        "+reportFault(code) : Drone",
        "+decommission(code) : Drone",
        "+reactivate(code) : Drone",
        "+receiveTelemetry(code, batteryLevel, position) : void"],
     "DroneService", [
        "+register(data) : Drone",
        "+listAll() : List<Drone>",
        "+findByCode(code) : Drone",
        "+fleetSummary() : FleetSummary",
        "+reportFault(code) : Drone",
        "+decommission(code) : Drone",
        "+reactivate(code) : Drone",
        "+reserve(code) : void",
        "+release(code) : void",
        "+completeMission(code) : void",
        "+sendToMaintenance(code) : void",
        "+receiveTelemetry(code, batteryLevel, position) : void"],
     "DroneRepository", [
        "+save(drone) : Drone",
        "+findByCode(code) : Optional<Drone>",
        "+findByState(state) : List<Drone>",
        "+findAll() : List<Drone>"],
     "abstract", [
        "-String code", "-String type", "-int batteryCapacity", "-double batteryLevelPercent",
        "-int enduranceMin", "-double maxPayload", "-List<String> equipment", "-Location location",
        "-DroneState state"], [
        "+canExecute(mission) : boolean",
        "+assignToMission() : void",
        "+completeMission(batteryThreshold) : void",
        "+finishCharging() : void",
        "+releaseReservation() : void",
        "+markOutOfService() : void",
        "+sendToMaintenance() : void",
        "+reactivate() : void",
        "+decommission() : void",
        "+executeTask(mission) : void"],
     "creates and returns"),
    ("Mission", "MissionController", [
        "+create(data) : Mission",
        "+find(filter) : List<Mission>",
        "+findByCode(code) : Mission",
        "+authorizeTakeoff(code) : Mission",
        "+pause(code) : Mission",
        "+resume(code) : Mission",
        "+redirect(code, destination) : Mission",
        "+abort(code) : Mission",
        "+finish(code) : Mission"],
     "MissionService", [
        "+create(data) : Mission",
        "+find(filter) : List<Mission>",
        "+findByCode(code) : Mission",
        "+authorizeTakeoff(code) : Mission",
        "+pause(code) : Mission",
        "+resume(code) : Mission",
        "+redirect(code, destination) : Mission",
        "+abort(code) : Mission",
        "+finish(code) : Mission"],
     "MissionRepository", [
        "+save(mission) : Mission",
        "+findByCode(code) : Optional<Mission>",
        "+findByState(state) : List<Mission>",
        "+findAll() : List<Mission>"],
     None, [
        "-String code", "-String type", "-Priority priority", "-Location origin",
        "-Location destination", "-double requiredPayload", "-int minEndurance", "-Route route",
        "-MissionState state", "-int routeAttempts", "-LocalDateTime createdAt",
        "-LocalDateTime start", "-LocalDateTime end"], [
        "+assignDrone(drone) : void",
        "+releaseDrone() : void",
        "+registerRouteAttempt() : int",
        "+takeOff() : void",
        "+reachCruise() : void",
        "+pause() : void",
        "+resume() : void",
        "+redirect(newDestination) : void",
        "+startReturn() : void",
        "+finish() : void",
        "+abort() : void",
        "+flightDuration() : Duration"],
     "creates and returns"),
    ("Alert", "AlertController", [
        "+stream() : SseEmitter",
        "+find(type, severity) : List<Alert>"],
     "AlertService", [
        "+onTelemetryReceived(event) : void",
        "+evaluate(droneCode, missionCode) : void",
        "+alertsOfMission(missionCode) : List<Alert>",
        "+subscribe() : SseEmitter",
        "+find(type, severity) : List<Alert>"],
     "AlertRepository", [
        "+save(alert) : Alert",
        "+findByMissionCode(missionCode) : List<Alert>",
        "+findByTypeAndSeverity(type, severity) : List<Alert>"],
     None, [
        "-UUID id", "-LocalDateTime generatedAt", "-Severity severity", "-Drone drone",
        "-AlertType type", "-String detail"], [
        "+message() : String",
        "+isIncident() : boolean"],
     "creates and returns"),
    ("FlightHistory", "FlightHistoryController", [
        "+getHistory(droneCode) : FlightHistory"],
     "FlightHistoryService", [
        "+getHistory(droneCode) : FlightHistory",
        "+onMissionCompleted(event) : void",
        "+resetCounters(droneCode) : void"],
     "FlightHistoryRepository", [
        "+save(history) : FlightHistory",
        "+findByDroneCode(droneCode) : Optional<FlightHistory>"],
     None, [
        "-Drone drone", "-Duration flightHours", "-int completedMissions",
        "-List<Incident> incidents"], [
        "+registerCompletedMission(duration) : void",
        "+registerIncident(alert) : void",
        "+resetCounters() : void"],
     "updates and returns"),
    ("MaintenanceRecord", "MaintenanceRecordController", [
        "+recordResult(droneCode, result) : MaintenanceRecord"],
     "MaintenanceRecordService", [
        "+recordResult(droneCode, result) : MaintenanceRecord"],
     "MaintenanceRecordRepository", [
        "+save(record) : MaintenanceRecord",
        "+findByDroneCode(droneCode) : List<MaintenanceRecord>"],
     None, [
        "-UUID id", "-Drone drone", "-MaintenanceResult result", "-LocalDateTime date"], [],
     "creates and returns"),
    ("MaintenanceRecommendation", "MaintenanceRecommendationController", [
        "+list() : List<MaintenanceRecommendation>"],
     "MaintenanceRecommendationService", [
        "+onHistoryUpdated(event) : void",
        "+list() : List<MaintenanceRecommendation>"],
     "MaintenanceRecommendationRepository", [
        "+save(recommendation) : MaintenanceRecommendation",
        "+findAll() : List<MaintenanceRecommendation>"],
     None, [
        "-UUID id", "-Drone drone", "-String reason", "-LocalDateTime generatedAt"], [],
     "creates and returns"),
    ("SystemConfiguration", "SystemConfigurationController", [
        "+getAssignmentRule() : AssignmentRule",
        "+updateAssignmentRule(rule) : void",
        "+getAlertThresholds() : AlertThresholds",
        "+updateAlertThresholds(thresholds) : void",
        "+getMaintenanceThresholds() : MaintenanceThresholds",
        "+updateMaintenanceThresholds(thresholds) : void"],
     "SystemConfigurationService", [
        "+getAssignmentRule() : AssignmentRule",
        "+updateAssignmentRule(rule) : void",
        "+getAlertThresholds() : AlertThresholds",
        "+updateAlertThresholds(thresholds) : void",
        "+getMaintenanceThresholds() : MaintenanceThresholds",
        "+updateMaintenanceThresholds(thresholds) : void"],
     "SystemConfigurationRepository", [
        "+save(configuration) : SystemConfiguration",
        "+findById(id) : Optional<SystemConfiguration>"],
     "singleton", [
        "-AssignmentRule assignmentRule", "-AlertThresholds alertThresholds",
        "-MaintenanceThresholds maintenanceThresholds"], [
        "+getAssignmentRule() : AssignmentRule",
        "+getAlertThresholds() : AlertThresholds",
        "+getMaintenanceThresholds() : MaintenanceThresholds",
        "+updateAssignmentRule(rule) : void",
        "+updateAlertThresholds(thresholds) : void",
        "+updateMaintenanceThresholds(thresholds) : void"],
     "reads and updates"),
]

SUBTIPOS = [
    ("DeliveryDrone", ["+executeTask(mission) : void", "-pickUpCargo() : void", "-dropOffCargo() : void"]),
    ("InspectionDrone", ["+executeTask(mission) : void", "-captureInspectionPoint() : void"]),
    ("MonitoringDrone", ["+executeTask(mission) : void", "-streamVideo() : void", "-takePhoto() : void"]),
]


def capas():
    d = Diagrama("Dronflow — Development view: UML class diagram organized in three layers")
    d.fill_clase, d.borde_clase = "#ececff", "#9370db"
    GAP, PAD, TOP = 150, 24, 34   # separación entre columnas, margen del marco, alto del título del marco

    for ent, ctl, ops_c, srv, ops_s, rep, ops_r, est, atr, ops_e, _ in COLUMNAS:
        d.clase("c_" + ent, ctl, None, [], ops_c)
        d.clase("s_" + ent, srv, None, [], ops_s)
        d.clase("r_" + ent, rep, "interface", [], ops_r)
        d.clase("m_" + ent, ent, est, atr, ops_e)
    for nom, ops in SUBTIPOS:
        d.clase("m_" + nom, nom, None, [], ops)

    # columnas: cada una con su Controller, Service, Repository y entidad, centrados
    ents = [c[0] for c in COLUMNAS]
    filas = ["c_", "s_", "r_", "m_"]
    anchos = [max(d.cajas[f + e][2] for f in filas) for e in ents]
    xs, x = [], 40 + PAD
    for w in anchos:
        xs.append(x)
        x += w + GAP
    ancho_total = x - GAP + PAD - 40
    y = 60
    marcos = [("f_ctl", "Presentation_Controller"), ("f_srv", "Business_Service"),
              ("f_rep", "Data_Repository"), ("f_dom", "Domain_Model")]
    for (fid, titulo), f in zip(marcos, filas):
        alto = max(d.cajas[f + e][3] for e in ents)
        for e, cx, w in zip(ents, xs, anchos):
            caja = d.cajas[f + e]
            caja[0], caja[1] = cx + (w - caja[2]) / 2, y + TOP
        alto_marco = TOP + alto + PAD
        if f == "m_":  # los subtipos de Drone van en una segunda fila del modelo de dominio
            ys = y + TOP + alto + 130
            for (nom, _), i in zip(SUBTIPOS, range(3)):
                caja = d.cajas["m_" + nom]
                caja[0], caja[1] = xs[i] + (anchos[i] - caja[2]) / 2, ys
            alto_marco += 130 + max(d.cajas["m_" + n][3] for n, _ in SUBTIPOS)
        d.marco(fid, titulo, 40, y, ancho_total, alto_marco)
        y += alto_marco + 90

    for (ent, *_, verbo), cx, w in zip(COLUMNAS, xs, anchos):
        d.asociacion("c_" + ent, "s_" + ent, etiqueta="delegates")
        d.asociacion("s_" + ent, "r_" + ent, etiqueta="saves and queries")
        d.dependencia("r_" + ent, "m_" + ent, "persists")
        s, m = d.cajas["s_" + ent], d.cajas["m_" + ent]
        lane = cx + w + 28
        rep, dom = d.cajas["f_rep"], d.cajas["f_dom"]
        d.dependencia("s_" + ent, "m_" + ent, (verbo, (lane, (rep[1] + rep[3] + dom[1]) / 2 - 18)),
                      via=[(lane, s[1] + s[3] / 2), (lane, m[1] - 28), (m[0] + m[2] - 30, m[1] - 28)])

    for nom, _ in SUBTIPOS:
        d.generalizacion("m_" + nom, "m_Drone")
    d.asociacion("m_Mission", "m_Drone", "assignedDrone", "0..1")
    d.asociacion("m_Alert", "m_Mission", "mission", "0..1")
    d.guardar(os.path.join(OUT, "capas.svg"))


for f in (despliegue, despliegue_simple, capas):
    f()
print("generado en", OUT)
