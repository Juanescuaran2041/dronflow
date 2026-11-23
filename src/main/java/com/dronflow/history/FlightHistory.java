package com.dronflow.history;

import com.dronflow.monitoring.Alert;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

@Document("flight_histories")
public class FlightHistory {
    @Id
    private String droneCode; // un historial por dron
    private double flightHours;
    private int completedMissions;
    private List<Incident> incidents = new ArrayList<>();

    protected FlightHistory() {}

    public FlightHistory(String droneCode) {
        this.droneCode = droneCode;
    }

    // HU-13: suma las horas de la misión y la cuenta como completada
    public void registerCompletedMission(Duration duration) {
        flightHours += duration.toMillis() / 3_600_000.0;
        completedMissions++;
    }

    // HU-13 (Creator): el historial crea sus incidencias a partir de las alertas altas o críticas
    public void registerIncident(Alert alert) {
        if (alert.isIncident()) {
            incidents.add(new Incident(alert.getId(), alert.getMissionCode(), alert.getSeverity(), alert.getGeneratedAt()));
        }
    }

    // HU-15: un mantenimiento aprobado reinicia los contadores; las incidencias no se borran
    public void resetCounters() {
        flightHours = 0;
        completedMissions = 0;
    }

    public String getDroneCode() { return droneCode; }
    public double getFlightHours() { return flightHours; }
    public int getCompletedMissions() { return completedMissions; }
    public List<Incident> getIncidents() { return incidents; }
}
