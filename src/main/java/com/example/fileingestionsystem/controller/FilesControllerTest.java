package com.example.filescontroller.controller;
import com.example.filescontroller.service.MetadataService;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.beans.factory.annotation.Autowired;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import java.util.Collections;

@WebMvcTest(FilesController.class)
public class FilesControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private MetadataService metadataService;

    @Test
    public void testList() throws Exception {
        when(metadataService.list()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/files")).andExpect(status().isOk());
    }
}