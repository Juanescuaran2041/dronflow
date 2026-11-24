package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import com.dronflow.mission.Mission;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MonitoringDrone extends Drone {

    private static final Logger log = LoggerFactory.getLogger(MonitoringDrone.class);

    protected MonitoringDrone() {}

    public MonitoringDrone(RegisterDroneRequest data) {
        super(data.code(), "monitoring", data.batteryCapacity(), data.enduranceMin(), data.maxPayload(), data.equipment());
    }

    @Override
    public void executeTask(Mission mission) {
        streamVideo(mission);
        takePhoto(mission);
    }

    private void streamVideo(Mission mission) {
        log.info("[{}] transmite video de la misión {}", getCode(), mission.getCode());
    }

    private void takePhoto(Mission mission) {
        log.info("[{}] fotografía {}", getCode(), mission.getDestination().name());
    }
}
