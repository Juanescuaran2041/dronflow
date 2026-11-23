package com.dronflow.maintenance;

import com.dronflow.maintenance.dto.MaintenanceRecommendationResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

// HU-14: solo administrador (regla en SecurityConfig). Las recomendaciones las genera el sistema.
@RestController
public class MaintenanceRecommendationController {
    private final MaintenanceRecommendationService service;

    public MaintenanceRecommendationController(MaintenanceRecommendationService service) {
        this.service = service;
    }

    @GetMapping("/api/v1/maintenance-recommendations")
    public List<MaintenanceRecommendationResponse> list() {
        return service.list().stream().map(MaintenanceRecommendationResponse::of).toList();
    }
}
