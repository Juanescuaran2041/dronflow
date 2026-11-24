package com.dronflow.fleet;

import com.dronflow.configuration.AlertThresholds;
import com.dronflow.configuration.SystemConfigurationService;
import com.dronflow.fleet.dto.RegisterDroneRequest;
import org.junit.jupiter.api.Test;
import org.springframework.context.ApplicationEventPublisher;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class DroneServiceTest {

    private final DroneRepository repository = mock(DroneRepository.class);
    private final ApplicationEventPublisher events = mock(ApplicationEventPublisher.class);
    private final SystemConfigurationService configuration = mock(SystemConfigurationService.class);
    private final DroneService service = new DroneService(repository, List.of(), events, configuration);

    private Drone droneOnMission() {
        Drone drone = new DeliveryDrone(new RegisterDroneRequest("DRN-001", "delivery", 5000, 25, 2, List.of("camera")));
        drone.assignToMission();
        when(repository.findById("DRN-001")).thenReturn(Optional.of(drone));
        when(repository.save(any(Drone.class))).thenAnswer(call -> call.getArgument(0));
        return drone;
    }

    @Test
    void completingAMissionLeavesTheDroneAvailableAndAnnouncesIt() {     // HU-07, HU-05
        Drone drone = droneOnMission();
        when(configuration.getAlertThresholds()).thenReturn(new AlertThresholds(20, 50));

        service.completeMission("DRN-001");

        assertEquals(DroneState.AVAILABLE, drone.getState());
        verify(events).publishEvent(new DroneAvailable("DRN-001"));
    }

    /** HU-02/HU-14: el historial de la propia misión pudo mandarlo a mantenimiento antes de llegar aquí. */
    @Test
    void completingAMissionRespectsADroneAlreadySentToMaintenance() {
        Drone drone = droneOnMission();
        drone.sendToMaintenance();

        service.completeMission("DRN-001");

        assertEquals(DroneState.IN_MAINTENANCE, drone.getState());
        verify(events, never()).publishEvent(any(DroneAvailable.class));
    }
}
