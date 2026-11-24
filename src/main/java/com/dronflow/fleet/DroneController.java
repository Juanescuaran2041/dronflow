package com.dronflow.fleet;

import com.dronflow.fleet.dto.DroneResponse;
import com.dronflow.fleet.dto.RegisterDroneRequest;
import com.dronflow.fleet.dto.TelemetryRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/drones")
public class DroneController {
    private final DroneService service;

    public DroneController(DroneService service) {
        this.service = service;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public DroneResponse register(@Valid @RequestBody RegisterDroneRequest data) {
        return DroneResponse.of(service.register(data));
    }

    @GetMapping
    public List<DroneResponse> listAll() {
        return service.listAll().stream().map(DroneResponse::of).toList();
    }

    @GetMapping("/{code}")
    public DroneResponse findByCode(@PathVariable String code) {
        return DroneResponse.of(service.findByCode(code));
    }

    @PostMapping("/{code}/telemetry")
    public DroneResponse updateTelemetry(@PathVariable String code, @Valid @RequestBody TelemetryRequest data) {
        return DroneResponse.of(service.updateTelemetry(code, data.batteryLevelPercent(), data.location()));
    }

    @PostMapping("/{code}/report-fault")
    public DroneResponse reportFault(@PathVariable String code) {
        return DroneResponse.of(service.reportFault(code));
    }

    @PostMapping("/{code}/decommission")
    public DroneResponse decommission(@PathVariable String code) {
        return DroneResponse.of(service.decommission(code));
    }

    @PostMapping("/{code}/finish-charging")
    public DroneResponse finishCharging(@PathVariable String code) {
        return DroneResponse.of(service.finishCharging(code));
    }

    @PostMapping("/{code}/reactivate")
    public DroneResponse reactivate(@PathVariable String code) {
        return DroneResponse.of(service.reactivate(code));
    }
}
