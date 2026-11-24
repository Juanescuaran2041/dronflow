package com.dronflow.fleet;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import com.dronflow.fleet.dto.RegisterDroneRequest;
import com.dronflow.mission.Mission;
import com.dronflow.mission.Priority;
import com.dronflow.mission.Route;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Polimorfismo: cada subtipo ejecuta su propia tarea al recibir el mismo mensaje. */
class DroneTaskTest {

    private static final Location ORIGIN = new Location("Base", 4.60, -74.08, 0);
    private static final Location DESTINATION = new Location("Hospital", 4.65, -74.05, 0);

    private final ListAppender<ILoggingEvent> appender = new ListAppender<>();
    private ch.qos.logback.classic.Logger root;

    @BeforeEach
    void startCapturingLogs() {
        root = ((LoggerContext) LoggerFactory.getILoggerFactory()).getLogger(ch.qos.logback.classic.Logger.ROOT_LOGGER_NAME);
        root.setLevel(Level.INFO);
        appender.start();
        root.addAppender(appender);
    }

    @AfterEach
    void stopCapturingLogs() {
        root.detachAppender(appender);
    }

    private Drone drone(String type) {
        RegisterDroneRequest data = new RegisterDroneRequest("DRN-001", type, 5000, 25, 2, List.of("camera"));
        return switch (type) {
            case "delivery" -> new DeliveryDrone(data);
            case "inspection" -> new InspectionDrone(data);
            default -> new MonitoringDrone(data);
        };
    }

    private Mission flyingMission() {
        Mission mission = new Mission("delivery", Priority.HIGH, ORIGIN, DESTINATION, 1, 10);
        mission.assignDrone("DRN-001");
        mission.takeOff(Route.straight(ORIGIN, DESTINATION));
        return mission;
    }

    private List<String> logged() {
        return appender.list.stream().map(ILoggingEvent::getFormattedMessage).toList();
    }

    @Test
    void deliveryDronePicksUpAndDropsOffTheCargo() {
        drone("delivery").executeTask(flyingMission());

        List<String> messages = logged();
        assertEquals(2, messages.size());
        assertTrue(messages.get(0).contains("recoge") && messages.get(0).contains("Base"), messages.toString());
        assertTrue(messages.get(1).contains("deposita") && messages.get(1).contains("Hospital"), messages.toString());
    }

    @Test
    void inspectionDroneCapturesOnePointPerRouteVertex() {
        drone("inspection").executeTask(flyingMission()); // la ruta recta tiene 2 puntos

        List<String> messages = logged();
        assertEquals(2, messages.size());
        assertTrue(messages.stream().allMatch(m -> m.contains("punto de revisión")), messages.toString());
    }

    @Test
    void monitoringDroneStreamsVideoAndTakesAPhoto() {
        drone("monitoring").executeTask(flyingMission());

        List<String> messages = logged();
        assertEquals(2, messages.size());
        assertTrue(messages.get(0).contains("transmite video"), messages.toString());
        assertTrue(messages.get(1).contains("fotografía"), messages.toString());
    }
}
