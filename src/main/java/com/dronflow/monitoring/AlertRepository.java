package com.dronflow.monitoring;

import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;
import java.util.UUID;

public interface AlertRepository extends MongoRepository<Alert, UUID> {
    List<Alert> findByMissionCode(String missionCode);
    List<Alert> findByTypeAndSeverity(AlertType type, Severity severity, Sort sort);
    List<Alert> findByType(AlertType type, Sort sort);
    List<Alert> findBySeverity(Severity severity, Sort sort);
}
