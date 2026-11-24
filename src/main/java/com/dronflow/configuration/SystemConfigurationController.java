package com.dronflow.configuration;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/configuration")
public class SystemConfigurationController {
    private final SystemConfigurationService service;

    public SystemConfigurationController(SystemConfigurationService service) {
        this.service = service;
    }

    @GetMapping("/assignment-rule")
    public AssignmentRule getAssignmentRuleConfig() { return service.getAssignmentRule(); }

    @PutMapping("/assignment-rule")
    public AssignmentRule updateAssignmentRuleConfig(@Valid @RequestBody AssignmentRule rule) {
        return service.updateAssignmentRule(rule);
    }

    @GetMapping("/alert-thresholds")
    public AlertThresholds getAlertThresholdsConfig() { return service.getAlertThresholds(); }

    @PutMapping("/alert-thresholds")
    public AlertThresholds updateAlertThresholdsConfig(@Valid @RequestBody AlertThresholds thresholds) {
        return service.updateAlertThresholds(thresholds);
    }

    @GetMapping("/maintenance-thresholds")
    public MaintenanceThresholds getMaintenanceThresholdsConfig() { return service.getMaintenanceThresholds(); }

    @PutMapping("/maintenance-thresholds")
    public MaintenanceThresholds updateMaintenanceThresholdsConfig(@Valid @RequestBody MaintenanceThresholds thresholds) {
        return service.updateMaintenanceThresholds(thresholds);
    }
}
