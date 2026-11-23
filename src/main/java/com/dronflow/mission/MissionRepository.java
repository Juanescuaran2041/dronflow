package com.dronflow.mission;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface MissionRepository extends MongoRepository<Mission, String>, MissionQueryRepository {
    List<Mission> findByStateAndAssignedDroneCodeIsNull(MissionState state);
}
