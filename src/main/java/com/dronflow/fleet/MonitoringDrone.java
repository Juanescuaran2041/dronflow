package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;

public class MonitoringDrone extends Drone {

    protected MonitoringDrone() {}

    public MonitoringDrone(RegisterDroneRequest data) {
        super(data.code(), "monitoring", data.batteryCapacity(), data.enduranceMin(), data.maxPayload(), data.equipment());
    }
}
