package com.example.fileingestionsystem.service;

import com.example.fileingestionsystem.model.FileMetadata;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

@Service
public class MetadataService {
    private static final Logger logger = LoggerFactory.getLogger(MetadataService.class);

    private final ObjectMapper mapper = new ObjectMapper();
    private final Path metadataPath;

    public MetadataService(@Value("${metadata.file.path:../python-app/metadata.json}") String path) {
        this.metadataPath = Paths.get(path).toAbsolutePath().normalize();
        logger.info("Metadata file path set to: {}", this.metadataPath);
    }

    public List<FileMetadata> list() {
        if (!Files.exists(metadataPath)) {
            logger.warn("Metadata file not found: {}", metadataPath);
            return new ArrayList<>();
        }

        try {
            return mapper.readValue(metadataPath.toFile(), new TypeReference<List<FileMetadata>>() {});
        } catch (IOException e) {
            logger.error("Error reading metadata file: {}", metadataPath, e);
            return new ArrayList<>();
        }
    }
}