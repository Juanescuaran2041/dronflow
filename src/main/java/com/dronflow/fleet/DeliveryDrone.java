package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;

public class DeliveryDrone extends Drone {

    protected DeliveryDrone() {}

    public DeliveryDrone(RegisterDroneRequest data) {
        super(data.code(), "delivery", data.batteryCapacity(), data.enduranceMin(), data.maxPayload(), data.equipment());
    }
}
