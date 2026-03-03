# Implementation Plan: Core Multimodal Document Extraction Pipeline

## Phase 0: Global Style Profiler (Bootstrapping)
- [x] Task: Implement `profiler.py` with Visual Density Clustering (7612645)
- [x] Task: Develop Stage 0 prompt for Style Registry generation (12104bb)
- [ ] Task: Conductor - User Manual Verification 'Phase 0' (Protocol in workflow.md)

## Phase 1: Triplet Extraction Engine
- [ ] Task: Implement Triplet Sliding Window logic in `batch_process.py`
- [ ] Task: Update Gemini client to handle multi-image payloads
- [ ] Task: Integrate Style Registry into extraction prompts
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Dynamic Adaptation & Realization
- [ ] Task: Implement Style Conformity Scorer and Delta Patching
- [ ] Task: Refine physical BBox cropping using high-res sources
- [ ] Task: Automate `images.json` and Markdown assembly
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Validation & Full Batch
- [ ] Task: Update QA Critic Agent for Triplet awareness
- [ ] Task: Execute full batch processing for all resources
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
