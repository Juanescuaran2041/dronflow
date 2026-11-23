package com.dronflow.user;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.UUID;

@Document("users")
public class User {

    @Id
    private UUID id;

    @Indexed(unique = true)
    private String username;

    private String passwordHash;

    private Role role;

    private boolean active = true;

    protected User() {}

    public User(String username, String passwordHash, Role role) {
        this.id = UUID.randomUUID();
        this.username = username;
        this.passwordHash = passwordHash;
        this.role = role;
    }

    public boolean authenticate(String password, PasswordEncoder passwordEncoder) {
        return active && passwordEncoder.matches(password, passwordHash);
    }

    public UUID getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }
    public Role getRole() {
        return role;
    }

    public boolean isActive() {
        return active;
    }
}
