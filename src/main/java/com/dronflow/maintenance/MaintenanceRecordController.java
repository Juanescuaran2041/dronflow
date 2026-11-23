package com.dronflow.maintenance;

import com.dronflow.maintenance.dto.MaintenanceRecordResponse;
import com.dronflow.maintenance.dto.RecordMaintenanceRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1")
public class MaintenanceRecordController {
    private final MaintenanceRecordService service;

    public MaintenanceRecordController(MaintenanceRecordService service) {
        this.service = service;
    }

    // HU-15
    @PostMapping("/maintenance-records")
    @ResponseStatus(HttpStatus.CREATED)
    public MaintenanceRecordResponse recordResult(@Valid @RequestBody RecordMaintenanceRequest request) {
        return MaintenanceRecordResponse.of(service.recordResult(request.droneCode(), request.result()));
    }

    @GetMapping("/drones/{code}/maintenance-records")
    public List<MaintenanceRecordResponse> findByDrone(@PathVariable String code) {
        return service.findByDrone(code).stream().map(MaintenanceRecordResponse::of).toList();
    }
}
