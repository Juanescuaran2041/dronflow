package com.dronflow.configuration;

import jakarta.validation.constraints.Positive;

public record MaintenanceThresholds(
        @Positive double maxHours,
        @Positive int maxMissions
) {
    // HU-14: se supera si las horas o las misiones acumuladas alcanzan el umbral
    public boolean exceededBy(double flightHours, int completedMissions) {
        return flightHours >= maxHours || completedMissions >= maxMissions;
    }
}
