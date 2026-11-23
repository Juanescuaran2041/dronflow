package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;

/**
 * RNF-02: cada tipo de dron trae su propia fábrica (un @Component).
 * Agregar un tipo nuevo = su subclase + su fábrica; DroneService no cambia.
 */
public interface DroneFactory {

    /** Valor de "type" que atiende esta fábrica, por ejemplo "delivery". */
    String type();

    Drone create(RegisterDroneRequest data);
}
