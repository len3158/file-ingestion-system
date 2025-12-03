package com.example.fileingestionsystem.controller;

import com.example.fileingestionsystem.service.MetadataService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static java.util.Collections.emptyList;

import com.example.fileingestionsystem.controller.FilesController;

@WebMvcTest(FilesController.class)
class FilesControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MetadataService metadataService;

    @Test
    void testListSuccess() throws Exception {
        when(metadataService.list()).thenReturn(emptyList());
        mockMvc.perform(get("/api/files"))
                .andExpect(status().isOk())
                .andExpect(content().contentType("application/json"))
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$").isEmpty());
    }

    @Test
    void testListError() throws Exception {
        when(metadataService.list()).thenThrow(new RuntimeException("Read error"));
        mockMvc.perform(get("/api/files"))
                .andExpect(status().isInternalServerError());
    }
}