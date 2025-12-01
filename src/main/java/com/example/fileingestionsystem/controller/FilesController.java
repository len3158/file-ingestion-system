package com.example.fileingestionsystem.controller;
import com.example.fileingestionsystem.model.FileMetadata;
import com.example.fileingestionsystem.service.MetadataService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class FilesController {
    private final MetadataService service;
    public FilesController(MetadataService service) {
        this.service = service;
    }

    @GetMapping("/files")
    public List<FileMetadata> list() {
        return service.list();
    }

    @PostMapping("/retry/{filename}")
    public String reprocess(@PathVariable String filename) {
        return "Retrying file upload" + filename;
    }
}