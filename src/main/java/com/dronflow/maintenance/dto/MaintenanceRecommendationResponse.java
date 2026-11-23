package com.dronflow.maintenance.dto;

import com.dronflow.maintenance.MaintenanceRecommendation;

import java.time.Instant;
import java.util.UUID;

public record MaintenanceRecommendationResponse(UUID id, String droneCode, String reason, Instant generatedAt) {
    public static MaintenanceRecommendationResponse of(MaintenanceRecommendation r) {
        return new MaintenanceRecommendationResponse(r.getId(), r.getDroneCode(), r.getReason(), r.getGeneratedAt());
    }
}
