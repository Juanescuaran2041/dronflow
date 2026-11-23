package com.dronflow.maintenance;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;
import java.util.UUID;

public interface MaintenanceRecommendationRepository extends MongoRepository<MaintenanceRecommendation, UUID> {
    List<MaintenanceRecommendation> findAllByOrderByGeneratedAtDesc();
}
