package com.example.fileingestionsystem.model;

public class FileMetadata{
    private String filename;
    private long size;
    private String sha256;
    private String status;
    private String path;

    public String getFilename() { return filename; }
    public void setFilename(String filename) { this.filename = filename; }
    public long getSize() { return size; }
    public void setSize(long size) { this.size = size; }
    public String getSha256() { return sha256; }
    public void setSha256(String sha256) { this.sha256 = sha256; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getPath() { return path; }
    public void setPath(String path) { this.path = path; }
}