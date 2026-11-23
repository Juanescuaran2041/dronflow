package com.dronflow.maintenance;

import com.dronflow.fleet.Drone;
import com.dronflow.fleet.DroneService;
import com.dronflow.fleet.DroneState;
import com.dronflow.history.FlightHistoryService;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@Service
public class MaintenanceRecordService {
    private final MaintenanceRecordRepository recordRepository;
    private final DroneService droneService;
    private final FlightHistoryService historyService;

    public MaintenanceRecordService(MaintenanceRecordRepository recordRepository, DroneService droneService,
                                    FlightHistoryService historyService) {
        this.recordRepository = recordRepository;
        this.droneService = droneService;
        this.historyService = historyService;
    }

    // HU-15: solo se registra para un dron en mantenimiento, y el resultado decide su nuevo estado
    public MaintenanceRecord recordResult(String droneCode, MaintenanceResult result) {
        Drone drone = droneService.findByCode(droneCode);
        if (drone.getState() != DroneState.IN_MAINTENANCE) {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "The drone is not in maintenance: it is " + drone.getState());
        }
        switch (result) {
            case APPROVED -> {
                historyService.resetCounters(droneCode); // reinicia horas y misiones, conserva incidencias
                droneService.reactivate(droneCode);      // vuelve a disponible
            }
            case REQUIRES_REPAIR -> droneService.sendToRepair(droneCode);
            case DECOMMISSION -> droneService.decommission(droneCode);
        }
        return recordRepository.save(new MaintenanceRecord(droneCode, result));
    }

    public List<MaintenanceRecord> findByDrone(String droneCode) {
        droneService.findByCode(droneCode); // 404 si el dron no existe
        return recordRepository.findByDroneCodeOrderByDateDesc(droneCode);
    }
}
