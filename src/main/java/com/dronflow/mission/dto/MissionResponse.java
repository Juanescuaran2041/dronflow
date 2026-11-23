package com.dronflow.mission.dto;

import com.dronflow.fleet.Location;
import com.dronflow.mission.Mission;
import com.dronflow.mission.MissionState;
import com.dronflow.mission.Priority;
import com.dronflow.mission.Route;

import java.time.Instant;

public record MissionResponse(
        String code,
        String type,
        Priority priority,
        Location origin,
        Location destination,
        double requiredPayload,
        int minEndurance,
        Route route,
        String assignedDroneCode,
        MissionState state,
        int routeAttempts,
        Instant createdAt,
        Instant start,
        Instant end
) {
    public static MissionResponse of(Mission m) {
        return new MissionResponse(m.getCode(), m.getType(), m.getPriority(), m.getOrigin(), m.getDestination(),
                m.getRequiredPayload(), m.getMinEndurance(), m.getRoute(), m.getAssignedDroneCode(), m.getState(),
                m.getRouteAttempts(), m.getCreatedAt(), m.getStart(), m.getEnd());
    }
}
