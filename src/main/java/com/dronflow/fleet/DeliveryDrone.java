package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import com.dronflow.mission.Mission;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DeliveryDrone extends Drone {

    private static final Logger log = LoggerFactory.getLogger(DeliveryDrone.class);

    protected DeliveryDrone() {}

    public DeliveryDrone(RegisterDroneRequest data) {
        super(data.code(), "delivery", data.batteryCapacity(), data.enduranceMin(), data.maxPayload(), data.equipment());
    }

    // RF-02: entrega = recoger la carga en el origen y depositarla en el destino
    @Override
    public void executeTask(Mission mission) {
        pickUpCargo(mission);
        dropOffCargo(mission);
    }

    private void pickUpCargo(Mission mission) {
        log.info("[{}] recoge {} kg en {}", getCode(), mission.getRequiredPayload(), mission.getOrigin().name());
    }

    private void dropOffCargo(Mission mission) {
        log.info("[{}] deposita la carga en {}", getCode(), mission.getDestination().name());
    }
}
