package com.dronflow.mission;

import java.time.Instant;

public record MissionFilter(String droneCode, Instant from, Instant to, MissionState state) {}
