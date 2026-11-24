package com.dronflow.monitoring;

import com.dronflow.configuration.AlertThresholds;
import com.dronflow.fleet.DeliveryDrone;
import com.dronflow.fleet.Drone;
import com.dronflow.fleet.Location;
import com.dronflow.fleet.dto.RegisterDroneRequest;
import com.dronflow.mission.Mission;
import com.dronflow.mission.Priority;
import com.dronflow.mission.RestrictedZone;
import com.dronflow.mission.Route;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AlertRulesTest {
    private static final Location A = new Location("A", 4.60, -74.08, 0);
    private static final Location B = new Location("B", 4.65, -74.08, 0);
    private static final AlertThresholds THRESHOLDS = new AlertThresholds(20, 50);

    private Mission flyingMission() {
        Mission m = new Mission("delivery", Priority.HIGH, A, B, 1, 20);
        m.assignDrone("DRN-001");
        m.takeOff(Route.straight(A, B));
        m.reachCruise();
        return m;
    }

    // La telemetría todavía no tiene disparador, así que el test fija batería y posición directamente
    private Drone drone(double battery, Location at) {
        Drone d = new DeliveryDrone(new RegisterDroneRequest("DRN-001", "delivery", 5000, 25, 2, List.of()));
        ReflectionTestUtils.setField(d, "batteryLevelPercent", battery);
        ReflectionTestUtils.setField(d, "location", at);
        return d;
    }

    @Test
    void lowBatteryOnlyBelowTheThresholdAndWhileFlying() {
        LowBatteryRule rule = new LowBatteryRule();
        assertTrue(rule.evaluate(drone(19, A), flyingMission(), THRESHOLDS).isPresent());
        assertTrue(rule.evaluate(drone(21, A), flyingMission(), THRESHOLDS).isEmpty());
        Mission pending = new Mission("delivery", Priority.LOW, A, B, 1, 20);
        assertTrue(rule.evaluate(drone(5, A), pending, THRESHOLDS).isEmpty());
    }

    @Test
    void deviationAboveTheThreshold() {
        RouteDeviationRule rule = new RouteDeviationRule();
        assertTrue(rule.evaluate(drone(80, new Location(null, 4.62, -74.08, 0)), flyingMission(), THRESHOLDS).isEmpty());
        // ~0.001° de longitud ≈ 110 m fuera de la ruta
        assertTrue(rule.evaluate(drone(80, new Location(null, 4.62, -74.079, 0)), flyingMission(), THRESHOLDS).isPresent());
    }

    @Test
    void enteringARestrictedZone() {
        RestrictedZone zone = new RestrictedZone("Z", List.of(
                new Location(null, 4.61, -74.09, 0), new Location(null, 4.63, -74.09, 0),
                new Location(null, 4.63, -74.07, 0), new Location(null, 4.61, -74.07, 0)));
        RestrictedZoneRule rule = new RestrictedZoneRule(() -> List.of(zone));
        assertEquals(Severity.CRITICAL, rule.evaluate(drone(80, new Location(null, 4.62, -74.08, 0)), flyingMission(), THRESHOLDS)
                .orElseThrow().getSeverity());
        assertTrue(rule.evaluate(drone(80, new Location(null, 4.70, -74.08, 0)), flyingMission(), THRESHOLDS).isEmpty());
    }

    @Test
    void severityComesFromTheType() {
        assertEquals(Severity.MEDIUM, new Alert(AlertType.LOW_BATTERY, "D", "M", "").getSeverity());
        assertEquals(Severity.HIGH, new Alert(AlertType.ROUTE_DEVIATION, "D", "M", "").getSeverity());
        assertEquals(Severity.CRITICAL, new Alert(AlertType.RESTRICTED_ZONE, "D", "M", "").getSeverity());
        assertEquals(Severity.LOW, new Alert(AlertType.MAINTENANCE, "D", null, "").getSeverity());
        assertTrue(new Alert(AlertType.ROUTE_DEVIATION, "D", "M", "").isIncident());
        assertFalse(new Alert(AlertType.LOW_BATTERY, "D", "M", "").isIncident());
    }
}
