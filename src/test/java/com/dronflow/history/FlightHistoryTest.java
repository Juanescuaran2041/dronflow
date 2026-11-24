package com.dronflow.history;

import com.dronflow.monitoring.Alert;
import com.dronflow.monitoring.AlertType;
import org.junit.jupiter.api.Test;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FlightHistoryTest {

    @Test
    void completedMissionAddsHoursAndCount() {
        FlightHistory h = new FlightHistory("DRN-001");
        h.registerCompletedMission(Duration.ofMinutes(90));
        assertEquals(1.5, h.getFlightHours(), 1e-9);
        assertEquals(1, h.getCompletedMissions());
    }

    @Test
    void onlyHighOrCriticalAlertsBecomeIncidents() {
        FlightHistory h = new FlightHistory("DRN-001");
        h.registerIncident(new Alert(AlertType.LOW_BATTERY, "DRN-001", "M-1", "medium"));
        h.registerIncident(new Alert(AlertType.ROUTE_DEVIATION, "DRN-001", "M-1", "high"));
        assertEquals(1, h.getIncidents().size());
    }

    @Test
    void resetKeepsTheIncidents() {
        FlightHistory h = new FlightHistory("DRN-001");
        h.registerCompletedMission(Duration.ofHours(105));
        h.registerIncident(new Alert(AlertType.RESTRICTED_ZONE, "DRN-001", "M-1", "critical"));
        h.resetCounters();
        assertEquals(0, h.getFlightHours());
        assertEquals(0, h.getCompletedMissions());
        assertEquals(1, h.getIncidents().size());
    }
}
