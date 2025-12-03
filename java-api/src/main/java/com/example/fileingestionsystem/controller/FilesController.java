package com.example.fileingestionsystem.controller;

import com.example.fileingestionsystem.model.FileMetadata;
import com.example.fileingestionsystem.service.MetadataService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.io.File;
import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api")
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
    public ResponseEntity<String> reprocess(@PathVariable String filename) {
        // Basic validation
        if (filename.contains("..") || !filename.endsWith(".csv")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid filename");
        }

        String rejectedPath = "../python-app/data/rejected/" + filename;
        String incomingPath = "../python-app/data/incoming/" + filename;
        File rejectedFile = new File(rejectedPath);

        if (!rejectedFile.exists()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "File not found in rejected");
        }

        rejectedFile.renameTo(new File(incomingPath));

        try {
            ProcessBuilder pb = new ProcessBuilder("../python-app/ingest.sh");
            pb.inheritIO();  // Log to console
            Process process = pb.start();
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Ingestion failed");
            }
        } catch (IOException | InterruptedException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Error triggering retry: " + e.getMessage());
        }

        return ResponseEntity.ok("Retry triggered for " + filename);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleException(Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
    }
}