package com.dronflow.configuration;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public record AlertThresholds(
        @PositiveOrZero @Max(100) double batteryMinPercent,
        @Positive double maxDeviationMeters
) {}
