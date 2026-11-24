package com.dronflow.monitoring;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.UUID;

@Document("alerts")
public class Alert {
    @Id
    private UUID id;
    private Instant generatedAt;
    private AlertType type;
    private Severity severity;
    private String droneCode;
    private String missionCode; // null en las de mantenimiento
    private String detail;

    protected Alert() {}

    public Alert(AlertType type, String droneCode, String missionCode, String detail) {
        this.id = UUID.randomUUID();
        this.generatedAt = Instant.now();
        this.type = type;
        this.severity = type.severity();
        this.droneCode = droneCode;
        this.missionCode = missionCode;
        this.detail = detail;
    }

    public String message() {
        return type + " (" + severity + ") on drone " + droneCode + ": " + detail;
    }

    public boolean isIncident() {
        return severity == Severity.HIGH || severity == Severity.CRITICAL;
    }

    public UUID getId() { return id; }
    public Instant getGeneratedAt() { return generatedAt; }
    public AlertType getType() { return type; }
    public Severity getSeverity() { return severity; }
    public String getDroneCode() { return droneCode; }
    public String getMissionCode() { return missionCode; }
    public String getDetail() { return detail; }
}
