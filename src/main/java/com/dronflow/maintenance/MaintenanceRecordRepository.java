package com.dronflow.maintenance;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;
import java.util.UUID;

public interface MaintenanceRecordRepository extends MongoRepository<MaintenanceRecord, UUID> {
    List<MaintenanceRecord> findByDroneCodeOrderByDateDesc(String droneCode);
}
