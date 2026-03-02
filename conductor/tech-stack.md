# Technology Stack: gemini-driven-img2md

## Core Languages
- **Python**: Primary language for the extraction engine, AI integration, and core logic.
- **TypeScript (Node.js)**: Secondary language for optional web-based visualization or frontend components.

## AI & Orchestration
- **Gemini Multimodal Models**: The primary vision and reasoning engine.
- **LangChain / LangGraph**: Framework for orchestrating complex extraction workflows, managing state, and handling multimodal data flows.

## Document Handling (LLM-Centric)
- **Direct Multimodal Input**: Leveraging Gemini's native ability to process PDF files and images directly, minimizing reliance on traditional PDF parsing libraries.
- **Image Processing**: Basic utilities (e.g., `PIL` or `opencv`) for any necessary image cropping/saving requested by the LLM.

## Command Line Interface
- **Typer**: A modern, type-safe library for building the Python CLI.

## Development & Infrastructure
- **Poetry / npm**: Dependency management for Python and Node.js.
- **Docker**: For consistent environment packaging and deployment.
