package com.dronflow.mission;

import java.time.Duration;

/**
 * Evento: una misión terminó (HU-13). Lo publicará Mission.finish cuando se defina quién reporta el aterrizaje;
 * por ahora no tiene publicador (decisión del autor).
 */
public record MissionCompleted(String missionCode, String droneCode, Duration flightDuration) {}
