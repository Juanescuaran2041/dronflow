package com.dronflow.fleet;

public record Location(String name, double latitude, double longitude, double altitude) {

    private static final double EARTH_RADIUS_METERS = 6_371_000;

    // Distancia en metros sobre la superficie (haversine); la altitud no se considera
    public double distanceTo(Location other) {
        double dLat = Math.toRadians(other.latitude - latitude);
        double dLon = Math.toRadians(other.longitude - longitude);
        double a = Math.pow(Math.sin(dLat / 2), 2)
                + Math.cos(Math.toRadians(latitude)) * Math.cos(Math.toRadians(other.latitude)) * Math.pow(Math.sin(dLon / 2), 2);
        return 2 * EARTH_RADIUS_METERS * Math.asin(Math.sqrt(a));
    }

    public boolean samePointAs(Location other) {
        return latitude == other.latitude && longitude == other.longitude;
    }
}
