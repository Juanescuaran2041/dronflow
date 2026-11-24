package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class DroneTest {

    private Drone newDrone() {
        return new DeliveryDrone(new RegisterDroneRequest("DRN-001", "delivery", 5000, 25, 2, List.of("camera")));
    }

    @Test
    void newDroneIsAvailable() {                       // HU-02
        assertEquals(DroneState.AVAILABLE, newDrone().getState());
    }

    @Test
    void faultMovesAvailableToOutOfService() {          // HU-02
        Drone drone = newDrone();
        drone.markOutOfService();
        assertEquals(DroneState.OUT_OF_SERVICE, drone.getState());
    }

    @Test
    void outOfServiceCanBeReactivatedOrDecommissioned() { // HU-03
        Drone drone = newDrone();
        drone.markOutOfService();
        drone.reactivate();
        assertEquals(DroneState.AVAILABLE, drone.getState());
        drone.decommission();
        assertEquals(DroneState.DECOMMISSIONED, drone.getState());
    }

    @Test
    void decommissionedCannotBeReactivated() {           // HU-03 supuesto
        Drone drone = newDrone();
        drone.decommission();
        assertThrows(ResponseStatusException.class, drone::reactivate);
    }

    @Test
    void maintenanceResults() {                             // HU-14, HU-15
        Drone drone = newDrone();
        drone.sendToMaintenance();
        assertEquals(DroneState.IN_MAINTENANCE, drone.getState());
        drone.sendToRepair();
        assertEquals(DroneState.OUT_OF_SERVICE, drone.getState());
        assertThrows(ResponseStatusException.class, drone::sendToRepair);
    }

    @Test
    void availableCannotBeReactivated() {
        assertThrows(ResponseStatusException.class, newDrone()::reactivate);
    }

    @Test
    void completingAMissionWithEnoughBatteryLeavesTheDroneAvailable() {   // HU-07
        Drone drone = newDrone();
        drone.assignToMission();
        drone.completeMission(20);                       // vuelve con 100 %
        assertEquals(DroneState.AVAILABLE, drone.getState());
    }

    @Test
    void completingAMissionWithLowBatterySendsTheDroneToCharge() {        // HU-07
        Drone drone = newDrone();
        drone.assignToMission();
        drone.completeMission(101);                      // umbral por encima de la carga actual
        assertEquals(DroneState.CHARGING, drone.getState());
        drone.finishCharging();
        assertEquals(DroneState.AVAILABLE, drone.getState());
    }

    @Test
    void onlyADroneOnMissionCanCompleteIt() {
        assertThrows(ResponseStatusException.class, () -> newDrone().completeMission(20));
        assertThrows(ResponseStatusException.class, newDrone()::finishCharging);
    }
}
