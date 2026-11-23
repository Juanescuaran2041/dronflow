package com.dronflow.history;

/** Evento: cambió el historial de un dron (HU-14 lo usa para decidir si recomienda mantenimiento). */
public record HistoryUpdated(String droneCode, double flightHours, int completedMissions) {}
