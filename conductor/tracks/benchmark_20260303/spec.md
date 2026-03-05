# Specification: Benchmark Integration with opendataloader-bench

## Overview
Implement an evaluation pipeline using `opendataloader-bench` to measure the accuracy, performance, and competitive standing of our Gemini-driven document extraction engine.

## Functional Requirements
- **Integration**: Connect our extraction pipeline to the `opendataloader-bench` framework.
- **Data Loading**: Support processing datasets provided by the benchmarking tool.
- **Metrics Extraction**: Capture accuracy scores, latency per page, and compare results against ground truth.
- **Reporting**: Generate a hybrid output consisting of a detailed Markdown report and a machine-readable JSON data file.
- **CLI Command**: Add a new `benchmark` command to the CLI to trigger evaluation manually.

## Non-Functional Requirements
- **Observability**: Provide clear logs during the benchmarking process.
- **Extensibility**: Ensure the benchmarking logic can easily incorporate new metrics or datasets.

## Acceptance Criteria
- A new `benchmark` command is available in the CLI.
- The command successfully processes a standard dataset from `opendataloader-bench`.
- A results folder is created containing both `report.md` and `results.json`.
- The report includes accuracy and performance metrics.

## Out of Scope
- Automated optimization of the engine based on benchmark results (this is for future tracks).
