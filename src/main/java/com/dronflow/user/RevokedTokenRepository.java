package com.dronflow.user;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface RevokedTokenRepository extends MongoRepository<RevokedTokens, String> {
}
