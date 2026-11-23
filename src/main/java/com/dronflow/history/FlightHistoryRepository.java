package com.dronflow.history;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface FlightHistoryRepository extends MongoRepository<FlightHistory, String> {}
