package com.dronflow.maintenance.dto;

import com.dronflow.maintenance.MaintenanceRecord;
import com.dronflow.maintenance.MaintenanceResult;

import java.time.Instant;
import java.util.UUID;

public record MaintenanceRecordResponse(UUID id, String droneCode, MaintenanceResult result, Instant date) {
    public static MaintenanceRecordResponse of(MaintenanceRecord r) {
        return new MaintenanceRecordResponse(r.getId(), r.getDroneCode(), r.getResult(), r.getDate());
    }
}
