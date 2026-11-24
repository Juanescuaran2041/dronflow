package com.dronflow.monitoring;

import com.dronflow.configuration.SystemConfigurationService;
import com.dronflow.fleet.Drone;
import com.dronflow.fleet.TelemetryReceived;
import com.dronflow.mission.Mission;
import com.dronflow.mission.MissionService;
import com.dronflow.monitoring.dto.AlertResponse;
import org.springframework.context.event.EventListener;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.time.Duration;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class AlertService {
    private static final Sort NEWEST_FIRST = Sort.by(Sort.Direction.DESC, "generatedAt");

    private final AlertRepository alertRepository;
    private final List<AlertRule> rules;
    private final SystemConfigurationService configuration;
    private final MissionService missionService;
    private final List<SseEmitter> subscribers = new CopyOnWriteArrayList<>();

    public AlertService(AlertRepository alertRepository, List<AlertRule> rules,
                        SystemConfigurationService configuration, MissionService missionService) {
        this.alertRepository = alertRepository;
        this.rules = rules;
        this.configuration = configuration;
        this.missionService = missionService;
    }

    @EventListener
    public void onTelemetryReceived(TelemetryReceived event) {
        missionService.activeMissionOf(event.drone().getCode())
                .ifPresent(mission -> evaluate(event.drone(), mission));
    }

    public List<Alert> evaluate(Drone drone, Mission mission) {
        var thresholds = configuration.getAlertThresholds();
        return rules.stream()
                .map(rule -> rule.evaluate(drone, mission, thresholds))
                .flatMap(Optional::stream)
                .map(this::raise)
                .toList();
    }

    public Alert raise(Alert alert) {
        Alert saved = alertRepository.save(alert);
        for (SseEmitter emitter : subscribers) {
            try {
                emitter.send(SseEmitter.event().name("alert").data(AlertResponse.of(saved)));
            } catch (IOException | IllegalStateException e) {
                subscribers.remove(emitter); // el cliente se desconectó
            }
        }
        return saved;
    }

    public SseEmitter subscribe() {
        SseEmitter emitter = new SseEmitter(Duration.ofMinutes(30).toMillis());
        subscribers.add(emitter);
        emitter.onCompletion(() -> subscribers.remove(emitter));
        emitter.onTimeout(() -> subscribers.remove(emitter));
        emitter.onError(e -> subscribers.remove(emitter));
        try {
            emitter.send(SseEmitter.event().comment("connected")); // envía los headers ya, para que el cliente sepa que conectó
        } catch (IOException e) {
            subscribers.remove(emitter);
        }
        return emitter;
    }

    public List<Alert> find(AlertType type, Severity severity) {
        if (type != null && severity != null) return alertRepository.findByTypeAndSeverity(type, severity, NEWEST_FIRST);
        if (type != null) return alertRepository.findByType(type, NEWEST_FIRST);
        if (severity != null) return alertRepository.findBySeverity(severity, NEWEST_FIRST);
        return alertRepository.findAll(NEWEST_FIRST);
    }

    public List<Alert> alertsOfMission(String missionCode) {
        return alertRepository.findByMissionCode(missionCode);
    }
}
