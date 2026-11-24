package com.dronflow.fleet;

/** Observer: lo escucha MissionService para darle una misión pendiente. */
public record DroneAvailable(String droneCode) {}
