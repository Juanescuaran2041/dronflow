package com.dronflow.configuration;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface SystemConfigurationRepository extends MongoRepository<SystemConfiguration, String> {}
