package com.dronflow.mission;

import com.dronflow.fleet.Location;
import org.springframework.stereotype.Component;

import java.util.Optional;

// HU-06: el sistema calcula la ruta (decisión del autor) y la valida contra las zonas restringidas
@Component
public class RouteValidator {
    private final RestrictedZoneProvider zones;

    public RouteValidator(RestrictedZoneProvider zones) {
        this.zones = zones;
    }

    public Route calculate(Location from, Location to) {
        return Route.straight(from, to);
    }

    /** La primera zona que la ruta cruza, si hay alguna. */
    public Optional<RestrictedZone> firstCrossedZone(Route route) {
        return zones.getZones().stream().filter(route::crosses).findFirst();
    }
}
