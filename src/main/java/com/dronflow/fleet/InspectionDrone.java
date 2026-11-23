package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;

public class InspectionDrone extends Drone {

    protected InspectionDrone() {}

    public InspectionDrone(RegisterDroneRequest data) {
        super(data.code(), "inspection", data.batteryCapacity(), data.enduranceMin(), data.maxPayload(), data.equipment());
    }
}
