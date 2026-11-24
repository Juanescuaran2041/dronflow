package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import com.dronflow.mission.Mission;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InspectionDrone extends Drone {

    private static final Logger log = LoggerFactory.getLogger(InspectionDrone.class);

    protected InspectionDrone() {}

    public InspectionDrone(RegisterDroneRequest data) {
        super(data.code(), "inspection", data.batteryCapacity(), data.enduranceMin(), data.maxPayload(), data.equipment());
    }

    @Override
    public void executeTask(Mission mission) {
        mission.getRoute().points().forEach(this::captureInspectionPoint);
    }

    private void captureInspectionPoint(Location point) {
        log.info("[{}] captura el punto de revisión {} ({}, {})", getCode(), point.name(), point.latitude(), point.longitude());
    }
}
