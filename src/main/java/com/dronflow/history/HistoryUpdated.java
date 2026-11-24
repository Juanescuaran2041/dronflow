package com.dronflow.history;

/** Observer: lo escucha MaintenanceRecommendationService para decidir si recomienda mantenimiento. */
public record HistoryUpdated(String droneCode, double flightHours, int completedMissions) {}
