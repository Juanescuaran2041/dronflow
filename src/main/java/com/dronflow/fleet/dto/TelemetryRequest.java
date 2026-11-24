package com.dronflow.fleet.dto;

import com.dronflow.fleet.Location;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;

public record TelemetryRequest(
        @PositiveOrZero @Max(100) double batteryLevelPercent,
        @NotNull Location location
) {}
