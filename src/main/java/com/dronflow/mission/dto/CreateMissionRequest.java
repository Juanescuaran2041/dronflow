package com.dronflow.mission.dto;

import com.dronflow.fleet.Location;
import com.dronflow.mission.Priority;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;

public record CreateMissionRequest(
        @NotBlank String type,
        @NotNull Priority priority,
        @NotNull Location origin,
        @NotNull Location destination,
        @PositiveOrZero double requiredPayload,
        @Positive int minEndurance
) {}
