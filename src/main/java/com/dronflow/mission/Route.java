package com.dronflow.mission;

import com.dronflow.fleet.Location;

import java.util.List;

// shortcut: la ruta es la línea recta entre los puntos y la geometría se calcula en el plano lat/lon,
// suficiente para zonas pequeñas; para rutas largas habría que usar geometría esférica.
public record Route(List<Location> points) {

    public static Route straight(Location from, Location to) {
        return new Route(List.of(from, to));
    }

    public boolean crosses(RestrictedZone zone) {
        return zone.intersects(this);
    }

    // HU-10: distancia en metros desde una posición al tramo más cercano de la ruta
    public double deviationFrom(Location position) {
        double min = Double.MAX_VALUE;
        for (int i = 0; i + 1 < points.size(); i++) {
            Location a = points.get(i), b = points.get(i + 1);
            double dx = b.longitude() - a.longitude(), dy = b.latitude() - a.latitude();
            double len2 = dx * dx + dy * dy;
            double t = len2 == 0 ? 0 : Math.max(0, Math.min(1,
                    ((position.longitude() - a.longitude()) * dx + (position.latitude() - a.latitude()) * dy) / len2));
            Location closest = new Location(null, a.latitude() + t * dy, a.longitude() + t * dx, 0);
            min = Math.min(min, position.distanceTo(closest));
        }
        return min;
    }
}
