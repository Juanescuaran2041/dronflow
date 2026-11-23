package com.dronflow.maintenance;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.UUID;

@Document("maintenance_recommendations")
public class MaintenanceRecommendation {
    @Id
    private UUID id;
    private String droneCode;
    private String reason;
    private Instant generatedAt;

    protected MaintenanceRecommendation() {}

    public MaintenanceRecommendation(String droneCode, String reason) {
        this.id = UUID.randomUUID();
        this.droneCode = droneCode;
        this.reason = reason;
        this.generatedAt = Instant.now();
    }

    public UUID getId() { return id; }
    public String getDroneCode() { return droneCode; }
    public String getReason() { return reason; }
    public Instant getGeneratedAt() { return generatedAt; }
}
