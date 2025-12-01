package com.example.fileingestionsystem.service;
import com.example.fileingestionsystem.model.FileMetadata;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

import java.nio.file.Paths;
import java.util.Collections;
import java.util.List;

@Service
public class MetadataService {
    private final ObjectMapper mapper = new ObjectMapper();
    private final String metadataPath = ""; // TODO

    public List<FileMetadata> list() {
        try {
            List<FileMetadata> list = mapper.readValue(Paths.get(metadataPath).toFile(), new TypeReference<List<FileMetadata>>() {});
            return list;
        } catch (Exception e) {
            return Collections.emptyList();
        }
    }
}