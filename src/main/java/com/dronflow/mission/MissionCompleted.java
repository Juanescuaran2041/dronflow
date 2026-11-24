package com.dronflow.mission;

import java.time.Duration;

/** Evento: una misión aterrizó y terminó (HU-13). Lo publica MissionService.finish. */
public record MissionCompleted(String missionCode, String droneCode, Duration flightDuration) {}
