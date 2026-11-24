package com.dronflow.monitoring;

import com.dronflow.monitoring.dto.AlertResponse;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.List;

@RestController
@RequestMapping("/api/v1/alerts")
public class AlertController {
    private final AlertService service;

    public AlertController(AlertService service) {
        this.service = service;
    }

    @GetMapping(path = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter stream() {
        return service.subscribe();
    }

    @GetMapping
    public List<AlertResponse> find(@RequestParam(required = false) AlertType type,
                                    @RequestParam(required = false) Severity severity) {
        return service.find(type, severity).stream().map(AlertResponse::of).toList();
    }
}
