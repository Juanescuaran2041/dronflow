package com.dronflow.mission;

import com.dronflow.configuration.AssignmentRule;
import com.dronflow.configuration.SystemConfigurationService;
import com.dronflow.fleet.Drone;
import com.dronflow.fleet.DroneService;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.Optional;

/**
 * HU-05: elige el dron disponible y compatible con mejor puntaje según la ponderación de HU-18.
 * La prioridad no distingue entre drones (supuesto de HU-05): sirve para elegir entre misiones pendientes.
 */
@Service
public class AssignmentService {
    private final DroneService drones;
    private final SystemConfigurationService configuration;

    public AssignmentService(DroneService drones, SystemConfigurationService configuration) {
        this.drones = drones;
        this.configuration = configuration;
    }

    public Optional<Drone> chooseDrone(Mission mission) {
        AssignmentRule rule = configuration.getAssignmentRule();
        return drones.findAvailable().stream()
                .filter(d -> d.canExecute(mission.getRequiredPayload(), mission.getMinEndurance()))
                .max(Comparator.comparingDouble(d -> score(d, mission, rule)));
    }

    static double score(Drone drone, Mission mission, AssignmentRule rule) {
        double battery = drone.getBatteryLevelPercent() / 100;
        // sin posición conocida, el dron no suma por cercanía
        double proximity = drone.getLocation() == null ? 0
                : 1 / (1 + drone.getLocation().distanceTo(mission.getOrigin()) / 1000);
        return rule.batteryWeight() * battery + rule.proximityWeight() * proximity;
    }
}
