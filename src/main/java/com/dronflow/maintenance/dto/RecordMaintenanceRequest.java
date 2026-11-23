package com.dronflow.maintenance.dto;

import com.dronflow.maintenance.MaintenanceResult;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record RecordMaintenanceRequest(@NotBlank String droneCode, @NotNull MaintenanceResult result) {}
