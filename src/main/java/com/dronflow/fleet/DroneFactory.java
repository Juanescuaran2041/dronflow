package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;

/**
 * Factory Method: cada tipo de dron trae su propia fábrica (un @Component).
 * Agregar un tipo nuevo = su subclase + su fábrica; DroneService no cambia.
 */
public interface DroneFactory {

    String type();

    Drone create(RegisterDroneRequest data);
}
