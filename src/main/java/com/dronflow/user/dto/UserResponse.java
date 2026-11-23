package com.dronflow.user.dto;

import com.dronflow.user.Role;
import com.dronflow.user.User;

import java.util.UUID;

public record UserResponse(
    UUID id,
    String username,
    Role role
) {
    public static UserResponse of(User user) {
        return new UserResponse(user.getId(), user.getUsername(), user.getRole());
    }
}
