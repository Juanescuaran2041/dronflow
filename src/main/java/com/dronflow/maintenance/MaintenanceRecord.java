package com.dronflow.maintenance;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.UUID;

@Document("maintenance_records")
public class MaintenanceRecord {
    @Id
    private UUID id;
    private String droneCode;
    private MaintenanceResult result;
    private Instant date;

    protected MaintenanceRecord() {}

    public MaintenanceRecord(String droneCode, MaintenanceResult result) {
        this.id = UUID.randomUUID();
        this.droneCode = droneCode;
        this.result = result;
        this.date = Instant.now();
    }

    public UUID getId() { return id; }
    public String getDroneCode() { return droneCode; }
    public MaintenanceResult getResult() { return result; }
    public Instant getDate() { return date; }
}
