package com.dronflow.mission;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

import java.util.Collection;
import java.util.List;

public interface MissionRepository extends MongoRepository<Mission, String>, MissionQueryRepository {
    /** HU-05: misiones en ese estado que todavia no tienen dron. */
    @Query("{ 'state': ?0, 'assignedDroneCode': null }")
    List<Mission> findUnassigned(MissionState state);

    /** Misiones del dron que estan en alguno de esos estados. */
    @Query("{ 'assignedDroneCode': ?0, 'state': { $in: ?1 } }")
    List<Mission> findByDrone(String droneCode, Collection<MissionState> states);
}
