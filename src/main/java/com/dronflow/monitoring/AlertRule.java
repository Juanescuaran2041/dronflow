package com.dronflow.monitoring;

import com.dronflow.configuration.AlertThresholds;
import com.dronflow.fleet.Drone;
import com.dronflow.mission.Mission;
import com.dronflow.mission.MissionState;

import java.util.Optional;
import java.util.Set;

/**
 * Strategy: cada regla de alerta es una implementación intercambiable.
 * Una regla nueva es un @Component más; AlertService no cambia.
 */
public interface AlertRule {

    // Cuentan como "en misión" en curso, pausada y retorno
    Set<MissionState> FLYING = Set.of(MissionState.IN_PROGRESS, MissionState.PAUSED, MissionState.RETURNING);

    Optional<Alert> evaluate(Drone drone, Mission mission, AlertThresholds thresholds);
}
