package com.dronflow.mission;

import com.dronflow.fleet.Location;

import java.util.List;

/** Zona restringida: dato de configuración fija, no se guarda en Mongo. */
public record RestrictedZone(String name, List<Location> perimeter) {

    // Punto dentro del polígono (ray casting)
    public boolean contains(Location p) {
        boolean inside = false;
        for (int i = 0, j = perimeter.size() - 1; i < perimeter.size(); j = i++) {
            Location a = perimeter.get(i), b = perimeter.get(j);
            if ((a.latitude() > p.latitude()) != (b.latitude() > p.latitude())
                    && p.longitude() < (b.longitude() - a.longitude()) * (p.latitude() - a.latitude())
                    / (b.latitude() - a.latitude()) + a.longitude()) {
                inside = !inside;
            }
        }
        return inside;
    }

    // La ruta toca la zona si un punto queda dentro o si algún tramo corta un borde
    public boolean intersects(Route route) {
        List<Location> pts = route.points();
        if (pts.stream().anyMatch(this::contains)) return true;
        for (int i = 0; i + 1 < pts.size(); i++) {
            for (int k = 0, j = perimeter.size() - 1; k < perimeter.size(); j = k++) {
                if (segmentsCross(pts.get(i), pts.get(i + 1), perimeter.get(j), perimeter.get(k))) return true;
            }
        }
        return false;
    }

    private static boolean segmentsCross(Location p1, Location p2, Location q1, Location q2) {
        double d1 = cross(q1, q2, p1), d2 = cross(q1, q2, p2), d3 = cross(p1, p2, q1), d4 = cross(p1, p2, q2);
        return ((d1 > 0) != (d2 > 0)) && ((d3 > 0) != (d4 > 0));
    }

    private static double cross(Location a, Location b, Location c) {
        return (b.longitude() - a.longitude()) * (c.latitude() - a.latitude())
                - (b.latitude() - a.latitude()) * (c.longitude() - a.longitude());
    }
}
