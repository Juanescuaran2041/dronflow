package com.dronflow.fleet;

import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface DroneRepository extends MongoRepository<Drone, String> {
    List<Drone> findByStateNot(DroneState state);
}
