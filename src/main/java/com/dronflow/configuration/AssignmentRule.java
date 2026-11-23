package com.dronflow.configuration;

import jakarta.validation.constraints.PositiveOrZero;

public record AssignmentRule(
        @PositiveOrZero double batteryWeight,
        @PositiveOrZero double proximityWeight,
        @PositiveOrZero double priorityWeight
) {}
