package com.dronflow.history;

import com.dronflow.history.dto.FlightHistoryResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// HU-13: solo consulta; el historial lo actualiza el sistema al terminar cada misión
@RestController
public class FlightHistoryController {
    private final FlightHistoryService service;

    public FlightHistoryController(FlightHistoryService service) {
        this.service = service;
    }

    @GetMapping("/api/v1/drones/{code}/flight-history")
    public FlightHistoryResponse getHistory(@PathVariable String code) {
        return FlightHistoryResponse.of(service.getHistory(code));
    }
}
