package com.dronflow.configuration;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Singleton: existe un único documento con id fijo, y solo SystemConfigurationService lo crea y lo lee.
 */
@Document("system_configuration")
public class SystemConfiguration {

    public static final String SINGLE_ID = "system";

    @Id
    private String id = SINGLE_ID;
    private AssignmentRule assignmentRule;
    private AlertThresholds alertThresholds;
    private MaintenanceThresholds maintenanceThresholds;

    protected SystemConfiguration() {}

    // Valores por defecto = ejemplos de las HU (decisión del autor)
    static SystemConfiguration withDefaults() {
        SystemConfiguration c = new SystemConfiguration();
        c.assignmentRule = new AssignmentRule(0.33, 0.33, 0.34);
        c.alertThresholds = new AlertThresholds(20, 50);           // HU-09, HU-10
        c.maintenanceThresholds = new MaintenanceThresholds(120, 50); // HU-18
        return c;
    }

    public AssignmentRule getAssignmentRule() { return assignmentRule; }
    public AlertThresholds getAlertThresholds() { return alertThresholds; }
    public MaintenanceThresholds getMaintenanceThresholds() { return maintenanceThresholds; }

    public void updateAssignmentRule(AssignmentRule rule) { this.assignmentRule = rule; }
    public void updateAlertThresholds(AlertThresholds thresholds) { this.alertThresholds = thresholds; }
    public void updateMaintenanceThresholds(MaintenanceThresholds thresholds) { this.maintenanceThresholds = thresholds; }
}
