package com.dronflow.monitoring;

import com.dronflow.configuration.AlertThresholds;
import com.dronflow.fleet.Drone;
import com.dronflow.mission.Mission;
import org.springframework.stereotype.Component;

import java.util.Optional;

// HU-10: alerta si el dron se aleja de su ruta más de la distancia configurada
@Component
public class RouteDeviationRule implements AlertRule {

    @Override
    public Optional<Alert> evaluate(Drone drone, Mission mission, AlertThresholds thresholds) {
        if (!FLYING.contains(mission.getState()) || drone.getLocation() == null || mission.getRoute() == null) {
            return Optional.empty();
        }
        double meters = mission.getRoute().deviationFrom(drone.getLocation());
        if (meters <= thresholds.maxDeviationMeters()) {
            return Optional.empty();
        }
        return Optional.of(new Alert(AlertType.ROUTE_DEVIATION, drone.getCode(), mission.getCode(),
                "Deviated " + Math.round(meters) + " m from the route (threshold " + thresholds.maxDeviationMeters() + " m)"));
    }
}
