package com.dronflow.mission;

import com.dronflow.fleet.Location;
import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class MissionTest {
    private static final Location A = new Location("Bodega Central", 4.60, -74.08, 0);
    private static final Location B = new Location("Cliente Norte", 4.65, -74.05, 0);

    private Mission newMission() {
        return new Mission("delivery", Priority.HIGH, A, B, 1.5, 20);
    }

    @Test
    void newMissionIsPending() {
        assertEquals(MissionState.PENDING, newMission().getState());
    }

    @Test
    void sameOriginAndDestinationIsRejected() {
        assertThrows(ResponseStatusException.class, () -> new Mission("delivery", Priority.LOW, A, A, 1, 10));
    }

    @Test
    void followsTheStatesOfHu07AndHu08() {
        Mission m = newMission();
        assertThrows(ResponseStatusException.class, () -> m.takeOff(Route.straight(A, B))); // sin dron
        m.assignDrone("DRN-001");
        m.takeOff(Route.straight(A, B));
        assertEquals(MissionState.TAKEOFF, m.getState());
        m.reachCruise();
        m.pause();
        assertEquals(MissionState.PAUSED, m.getState());
        m.resume();
        assertEquals(MissionState.IN_PROGRESS, m.getState());
        m.abort();
        assertEquals(MissionState.ABORTED, m.getState());
        assertThrows(ResponseStatusException.class, m::resume);
    }

    @Test
    void releasingTheDroneResetsTheAttempts() {
        Mission m = newMission();
        m.assignDrone("DRN-001");
        m.registerRouteAttempt();
        m.releaseDrone();
        assertNull(m.getAssignedDroneCode());
        assertEquals(0, m.getRouteAttempts());
        assertEquals(MissionState.PENDING, m.getState());
    }

    @Test
    void routeCrossingAZoneIsDetected() {
        RestrictedZone zone = new RestrictedZone("Z", List.of(
                new Location(null, 4.62, -74.07, 0), new Location(null, 4.63, -74.07, 0),
                new Location(null, 4.63, -74.06, 0), new Location(null, 4.62, -74.06, 0)));
        assertTrue(Route.straight(A, B).crosses(zone));
        assertFalse(Route.straight(A, new Location(null, 4.60, -74.00, 0)).crosses(zone));
    }
}
