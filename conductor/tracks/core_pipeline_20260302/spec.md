# Specification: Core Multimodal Document Extraction Pipeline

## Goal
Implement the primary extraction engine that uses Gemini Multimodal APIs to convert PDF/image documents into Markdown while preserving structure, math, and extracting images with captions.

## Scope
- PDF/Image input handling.
- Gemini API integration for structural and content extraction.
- LaTeX math formatting.
- Image identification, extraction, and local storage.
- Markdown generation with relative image referencing.
- Companion `images.json` generation.
