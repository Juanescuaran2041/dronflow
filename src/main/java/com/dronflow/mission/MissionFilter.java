package com.dronflow.mission;

import java.time.Instant;

/** HU-17: todos los filtros son opcionales. */
public record MissionFilter(String droneCode, Instant from, Instant to, MissionState state) {}
