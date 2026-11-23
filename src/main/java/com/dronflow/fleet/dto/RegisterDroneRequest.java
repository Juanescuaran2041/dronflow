package com.dronflow.fleet.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.util.List;

public record RegisterDroneRequest(
        @NotBlank String code,
        @NotBlank String type,
        @Positive int batteryCapacity,
        @Positive int enduranceMin,
        @Positive double maxPayload,
        @NotNull List<String> equipment
) {}
