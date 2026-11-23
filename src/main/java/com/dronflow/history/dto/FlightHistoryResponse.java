package com.dronflow.history.dto;

import com.dronflow.history.FlightHistory;
import com.dronflow.history.Incident;

import java.util.List;

public record FlightHistoryResponse(String droneCode, double flightHours, int completedMissions, List<Incident> incidents) {
    public static FlightHistoryResponse of(FlightHistory h) {
        return new FlightHistoryResponse(h.getDroneCode(), h.getFlightHours(), h.getCompletedMissions(), h.getIncidents());
    }
}
