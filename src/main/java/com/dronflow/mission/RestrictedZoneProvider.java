package com.dronflow.mission;

import java.util.List;

/** Puerto hacia la fuente de zonas restringidas. Hoy es un archivo; mañana podría ser una API. */
public interface RestrictedZoneProvider {
    List<RestrictedZone> getZones();
}
