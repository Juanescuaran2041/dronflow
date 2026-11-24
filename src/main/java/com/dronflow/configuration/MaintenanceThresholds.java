package com.dronflow.configuration;

import jakarta.validation.constraints.Positive;

public record MaintenanceThresholds(
        @Positive double maxHours,
        @Positive int maxMissions
) {
    public boolean exceededBy(double flightHours, int completedMissions) {
        return flightHours >= maxHours || completedMissions >= maxMissions;
    }
}
