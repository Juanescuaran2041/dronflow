package com.dronflow.mission;

import java.time.Duration;

/** Observer: lo escucha FlightHistoryService. Lo publica MissionService.finish. */
public record MissionCompleted(String missionCode, String droneCode, Duration flightDuration) {}
