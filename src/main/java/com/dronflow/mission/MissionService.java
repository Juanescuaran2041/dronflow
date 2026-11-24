package com.dronflow.mission;

import com.dronflow.fleet.DroneAvailable;
import com.dronflow.fleet.DroneService;
import com.dronflow.fleet.Location;
import com.dronflow.mission.dto.CreateMissionRequest;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.Set;

@Service
public class MissionService {
    private static final Set<String> MISSION_TYPES = Set.of("delivery", "inspection", "monitoring"); // HU-04

    // Estados en los que el dron está en el aire y su telemetría puede generar alertas
    private static final Set<MissionState> IN_FLIGHT = Set.of(MissionState.TAKEOFF, MissionState.IN_PROGRESS,
            MissionState.PAUSED, MissionState.RETURNING);

    private final MissionRepository missionRepository;
    private final AssignmentService assignmentService;
    private final DroneService droneService;
    private final RouteValidator routeValidator;
    private final ApplicationEventPublisher events;

    public MissionService(MissionRepository missionRepository, AssignmentService assignmentService,
                          DroneService droneService, RouteValidator routeValidator,
                          ApplicationEventPublisher events) {
        this.missionRepository = missionRepository;
        this.assignmentService = assignmentService;
        this.droneService = droneService;
        this.routeValidator = routeValidator;
        this.events = events;
    }

    // HU-04 + HU-05: se crea pendiente y el sistema intenta asignarle un dron de inmediato
    public Mission create(CreateMissionRequest data) {
        if (!MISSION_TYPES.contains(data.type())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Unsupported mission type. Supported types: " + MISSION_TYPES);
        }
        Mission mission = new Mission(data.type(), data.priority(), data.origin(), data.destination(),
                data.requiredPayload(), data.minEndurance());
        tryAssign(mission);
        return missionRepository.save(mission);
    }

    private void tryAssign(Mission mission) {
        assignmentService.chooseDrone(mission).ifPresent(drone -> {
            droneService.reserve(drone.getCode());
            mission.assignDrone(drone.getCode());
        });
    }

    // HU-05, asignación diferida: el dron liberado toma la misión pendiente compatible de mayor prioridad
    @EventListener
    public void onDroneAvailable(DroneAvailable event) {
        var drone = droneService.findByCode(event.droneCode());
        missionRepository.findByStateAndAssignedDroneCodeIsNull(MissionState.PENDING).stream()
                .filter(m -> drone.canExecute(m.getRequiredPayload(), m.getMinEndurance()))
                .max(Comparator.comparing(Mission::getPriority).thenComparing(Mission::getCreatedAt, Comparator.reverseOrder()))
                .ifPresent(m -> {
                    droneService.reserve(drone.getCode());
                    m.assignDrone(drone.getCode());
                    missionRepository.save(m);
                });
    }

    // HU-09/HU-10: la misión que el dron está volando, si tiene alguna
    public Optional<Mission> activeMissionOf(String droneCode) {
        return missionRepository.findByAssignedDroneCodeAndStateIn(droneCode, IN_FLIGHT).stream().findFirst();
    }

    public List<Mission> find(MissionFilter filter) {
        return missionRepository.find(filter);
    }

    public Mission findByCode(String code) {
        return missionRepository.findById(code)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Mission not found"));
    }

    // HU-06: valida la ruta; si cruza una zona cuenta el intento y al tercero libera el dron
    public Mission authorizeTakeoff(String code) {
        Mission mission = findByCode(code);
        if (mission.getAssignedDroneCode() == null) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "The mission has no assigned drone yet");
        }
        Route route = routeValidator.calculate(mission.getOrigin(), mission.getDestination());
        var crossed = routeValidator.firstCrossedZone(route);
        if (crossed.isEmpty()) {
            mission.takeOff(route);
            // RF-02: el despegue dispara la tarea propia del tipo de dron, sin que el servicio sepa cuál es
            droneService.findByCode(mission.getAssignedDroneCode()).executeTask(mission);
            return missionRepository.save(mission);
        }
        int attempt = mission.registerRouteAttempt();
        String reason = "Takeoff rejected: the route crosses the restricted zone '" + crossed.get().name() + "'";
        if (attempt >= Mission.MAX_ROUTE_ATTEMPTS) {
            droneService.release(mission.getAssignedDroneCode());
            mission.releaseDrone();
            reason += ". The drone was released after " + Mission.MAX_ROUTE_ATTEMPTS + " attempts";
        } else {
            reason += " (attempt " + attempt + " of " + Mission.MAX_ROUTE_ATTEMPTS + ")";
        }
        missionRepository.save(mission);
        throw new ResponseStatusException(HttpStatus.CONFLICT, reason);
    }

    // HU-07: avance de la misión. El aterrizaje libera el dron y alimenta el historial (HU-13)
    public Mission reachCruise(String code) {
        Mission mission = findByCode(code);
        mission.reachCruise();
        return missionRepository.save(mission);
    }

    public Mission startReturn(String code) {
        Mission mission = findByCode(code);
        mission.startReturn();
        return missionRepository.save(mission);
    }

    public Mission finish(String code) {
        Mission mission = findByCode(code);
        String droneCode = mission.getAssignedDroneCode();
        mission.finish();
        Mission saved = missionRepository.save(mission);
        // el historial primero: el dron puede tomar otra misión apenas quede disponible
        events.publishEvent(new MissionCompleted(code, droneCode, mission.flightDuration()));
        droneService.completeMission(droneCode);
        return saved;
    }

    public Mission pause(String code) {
        Mission mission = findByCode(code);
        mission.pause();
        return missionRepository.save(mission);
    }

    public Mission resume(String code) {
        Mission mission = findByCode(code);
        mission.resume();
        return missionRepository.save(mission);
    }

    // HU-08: la nueva ruta se valida igual que en HU-06; si cruza una zona, la misión sigue a su destino actual
    public Mission redirect(String code, Location destination) {
        Mission mission = findByCode(code);
        var drone = droneService.findByCode(mission.getAssignedDroneCode());
        Location from = drone.getLocation() != null ? drone.getLocation() : mission.getOrigin();
        Route route = routeValidator.calculate(from, destination);
        routeValidator.firstCrossedZone(route).ifPresent(zone -> {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "Redirect rejected: the new route crosses the restricted zone '" + zone.name() + "'");
        });
        mission.redirect(destination, route);
        return missionRepository.save(mission);
    }

    // HU-08: el dron inicia el retorno a su base; su llegada la reporta el sistema (fuera de alcance por ahora)
    public Mission abort(String code) {
        Mission mission = findByCode(code);
        mission.abort();
        return missionRepository.save(mission);
    }
}
