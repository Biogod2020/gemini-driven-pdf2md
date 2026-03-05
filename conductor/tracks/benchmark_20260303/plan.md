# Implementation Plan: Benchmark Integration with opendataloader-bench

## Phase 1: Environment Setup ## Phase 1: Environment Setup & Tool Research Tool Research [checkpoint: dbcc1d8]
- [x] Task: Research `opendataloader-bench` API and data format (66f3ebb)
- [~] Task: Install `opendataloader-bench` and its dependencies
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Core Integration Logic
- [~] Task: Implement Dataset Loader for `opendataloader-bench`
    - [x] Write unit tests for data loading (done)
    - [x] Implement loading logic in `src/gemini_driven_img2md/benchmark/loader.py` (done)
- [ ] Task: Implement Extraction Bridge
    - [ ] Write tests for the bridge (mocking VLM)
    - [ ] Implement bridge logic to connect our pipeline to the bench tool
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Reporting & CLI
- [ ] Task: Implement Metric Aggregator (Accuracy, Latency)
    - [ ] Write tests for aggregation
    - [ ] Implement aggregation logic
- [ ] Task: Implement Hybrid Reporter (Markdown + JSON)
    - [ ] Write tests for report generation
    - [ ] Implement Markdown and JSON exporters
- [ ] Task: Add `benchmark` command to CLI
    - [ ] Update `cli.py` with the new command
    - [ ] Write CLI integration tests
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Execution & Baseline
- [ ] Task: Run benchmark against a standard dataset
- [ ] Task: Document baseline results in the project
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
