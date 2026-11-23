package com.dronflow.monitoring;

// HU-12: cada tipo de alerta trae su severidad (mapeo confirmado por el autor)
public enum AlertType {
    LOW_BATTERY(Severity.MEDIUM),
    ROUTE_DEVIATION(Severity.HIGH),
    RESTRICTED_ZONE(Severity.CRITICAL),
    MAINTENANCE(Severity.LOW);

    private final Severity severity;

    AlertType(Severity severity) {
        this.severity = severity;
    }

    public Severity severity() {
        return severity;
    }
}
