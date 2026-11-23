package com.dronflow.user.dto;

import com.dronflow.user.Role;

public record Session(
        String token ,
        Role role
) {}
