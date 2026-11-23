package com.dronflow.monitoring.dto;

import com.dronflow.monitoring.Alert;
import com.dronflow.monitoring.AlertType;
import com.dronflow.monitoring.Severity;

import java.time.Instant;
import java.util.UUID;

public record AlertResponse(
        UUID id,
        Instant generatedAt,
        AlertType type,
        Severity severity,
        String droneCode,
        String missionCode,
        String detail
) {
    public static AlertResponse of(Alert a) {
        return new AlertResponse(a.getId(), a.getGeneratedAt(), a.getType(), a.getSeverity(),
                a.getDroneCode(), a.getMissionCode(), a.getDetail());
    }
}
