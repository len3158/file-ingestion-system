package com.example.fileingestionsystem.model;

/**
 * Immutable model for file metadata, mapped from ingestion process.
 *
 * @param filename The original filename.
 * @param size The file size in bytes.
 * @param sha256 The SHA-256 hash for integrity.
 * @param status The processing status (e.g., "processed" or "rejected").
 * @param reason Optional rejection reason (empty if processed).
 * @param path The final storage path.
 */
public record FileMetadata(
        String filename,
        long size,
        String sha256,
        String status,
        String reason,
        String path
) {}