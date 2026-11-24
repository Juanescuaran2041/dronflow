package com.dronflow.user.dto;

import jakarta.validation.constraints.Size;

/** RF-23: ambos campos son opcionales; solo se cambia lo que llega. */
public record EditUserRequest(
        String userName,

        @Size(min = 8)
        String password
) {}
