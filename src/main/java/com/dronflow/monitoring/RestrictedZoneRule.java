package com.dronflow.monitoring;

import com.dronflow.configuration.AlertThresholds;
import com.dronflow.fleet.Drone;
import com.dronflow.mission.Mission;
import com.dronflow.mission.RestrictedZoneProvider;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component
public class RestrictedZoneRule implements AlertRule {
    private final RestrictedZoneProvider zones;

    public RestrictedZoneRule(RestrictedZoneProvider zones) {
        this.zones = zones;
    }

    @Override
    public Optional<Alert> evaluate(Drone drone, Mission mission, AlertThresholds thresholds) {
        if (!FLYING.contains(mission.getState()) || drone.getLocation() == null) {
            return Optional.empty();
        }
        return zones.getZones().stream()
                .filter(zone -> zone.contains(drone.getLocation()))
                .findFirst()
                .map(zone -> new Alert(AlertType.RESTRICTED_ZONE, drone.getCode(), mission.getCode(),
                        "Entered the restricted zone '" + zone.name() + "'"));
    }
}
