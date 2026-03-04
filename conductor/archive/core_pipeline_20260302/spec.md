# Specification: Core Multimodal Document Extraction Pipeline

## Goal
Implement the primary extraction engine that uses Gemini Multimodal APIs to convert PDF/image documents into Markdown while preserving structure, math, and extracting images with captions.

## Scope
- **Stage 0: Global Style Profiler**: Implementation of visual-density clustering and seed page profiling to generate `style_profile.json`.
- **Stage 1: Triplet-Context Engine**: Development of the [N-1, N, N+1] extraction logic.
- **Dynamic Registry**: Logic for incremental style patching during batch processing.
- PDF/Image input handling using Gemini Native API.
- LaTeX math formatting.
- Image identification, extraction (via BBox), and local storage.
- Markdown generation with relative image referencing.
- Companion `images.json` generation.
