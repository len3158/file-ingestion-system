package com.example.fileingestionsystem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main entry point for the File Ingestion System API.
 *
 * This class bootstraps the Spring Boot application, enabling auto-configuration
 * and component scanning for controllers, services, and models.
 */
@SpringBootApplication
public class FileIngestionSystemApplication {

    public static void main(String[] args) {
        SpringApplication.run(FileIngestionSystemApplication.class, args);
    }
}