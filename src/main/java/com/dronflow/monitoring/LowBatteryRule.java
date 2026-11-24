package com.dronflow.monitoring;

import com.dronflow.configuration.AlertThresholds;
import com.dronflow.fleet.Drone;
import com.dronflow.mission.Mission;
import org.springframework.stereotype.Component;

import java.util.Optional;

// Alerta en cada lectura bajo el umbral, no solo al cruzarlo
@Component
public class LowBatteryRule implements AlertRule {

    @Override
    public Optional<Alert> evaluate(Drone drone, Mission mission, AlertThresholds thresholds) {
        if (!FLYING.contains(mission.getState()) || drone.getBatteryLevelPercent() >= thresholds.batteryMinPercent()) {
            return Optional.empty();
        }
        return Optional.of(new Alert(AlertType.LOW_BATTERY, drone.getCode(), mission.getCode(),
                "Battery at " + drone.getBatteryLevelPercent() + "% (threshold " + thresholds.batteryMinPercent() + "%)"));
    }
}
