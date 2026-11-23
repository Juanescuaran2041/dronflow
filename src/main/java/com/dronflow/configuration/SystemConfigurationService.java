package com.dronflow.configuration;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class SystemConfigurationService {
    private final SystemConfigurationRepository repository;

    public SystemConfigurationService(SystemConfigurationRepository repository) {
        this.repository = repository;
    }

    private SystemConfiguration current() {
        return repository.findById(SystemConfiguration.SINGLE_ID)
                .orElseGet(() -> repository.save(SystemConfiguration.withDefaults()));
    }

    public AssignmentRule getAssignmentRule() { return current().getAssignmentRule(); }
    public AlertThresholds getAlertThresholds() { return current().getAlertThresholds(); }
    public MaintenanceThresholds getMaintenanceThresholds() { return current().getMaintenanceThresholds(); }

    public AssignmentRule updateAssignmentRule(AssignmentRule rule) {
        if (rule.batteryWeight() + rule.proximityWeight() + rule.priorityWeight() == 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "At least one weight must be greater than 0");
        }
        SystemConfiguration c = current();
        c.updateAssignmentRule(rule);
        return repository.save(c).getAssignmentRule();
    }

    public AlertThresholds updateAlertThresholds(AlertThresholds thresholds) {
        SystemConfiguration c = current();
        c.updateAlertThresholds(thresholds);
        return repository.save(c).getAlertThresholds();
    }

    public MaintenanceThresholds updateMaintenanceThresholds(MaintenanceThresholds thresholds) {
        SystemConfiguration c = current();
        c.updateMaintenanceThresholds(thresholds);
        return repository.save(c).getMaintenanceThresholds();
    }
}
