package com.dronflow.mission.dto;

import com.dronflow.fleet.Location;
import jakarta.validation.constraints.NotNull;

public record RedirectRequest(@NotNull Location destination) {}
