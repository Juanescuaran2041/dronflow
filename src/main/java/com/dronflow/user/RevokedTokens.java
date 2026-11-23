package com.dronflow.user;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

@Document("revoked_tokens")
public class RevokedTokens {
    @Id
    private String tokenId;
    private Instant expiresAt;

    protected RevokedTokens() {}

    public RevokedTokens(String tokenId, Instant expiresAt) {
        this.tokenId = tokenId;
        this.expiresAt = expiresAt;
    }

}
