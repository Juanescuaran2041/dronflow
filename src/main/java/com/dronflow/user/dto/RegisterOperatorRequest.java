package com.dronflow.user.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record RegisterOperatorRequest(
        @NotBlank
        String userName,

        @NotBlank
        @Size(min = 8)
        String password
) {}
