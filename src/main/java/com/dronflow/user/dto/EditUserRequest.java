package com.dronflow.user.dto;

import jakarta.validation.constraints.Size;

public record EditUserRequest(
        String userName,

        @Size(min = 8)
        String password
) {}
