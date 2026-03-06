# gemini-driven-img2md 🤖📄

> **SOTA Multimodal Document Intelligence Engine** - Transforming complex PDFs into high-fidelity Markdown with pixel-perfect asset extraction and global style consistency.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Gemini 3 Flash](https://img.shields.io/badge/AI-Gemini%203%20Flash-orange.svg)](https://deepmind.google/technologies/gemini/)

## 🚀 Overview

`gemini-driven-img2md` is a next-generation document conversion tool that leverages Gemini's vision-language capabilities to solve the "last mile" of PDF-to-Markdown conversion. Unlike traditional OCR tools, it treats every page as a visual scene, inferring structure, math, and layout with human-like reasoning.

### Key SOTA Features:
- **Triplet-Context Extraction**: Uses a sliding window `[N-1, N, N+1]` to resolve cross-page paragraph breaks and maintain semantic flow.
- **Global Style Profiling**: Stage 0 pre-scan identifies document-wide typography rules (Heading weights, citation styles) for 100% consistency.
- **High-Fidelity Math & Tables**: Native LaTeX support for display/inline math and automatic HTML fallback for complex merged tables.
- **Pixel-Perfect Assets**: Intelligent BBox detection with safety padding ensures figures and charts are cropped precisely from high-res (300 DPI) sources.
- **Dynamic Style Evolution**: Autonomously detects and adapts to layout shifts within ultra-long documents.

---

## 🛠 Architecture

The engine operates on a three-stage intelligence pipeline:

1.  **Stage 0: Profiling** - Visual-density clustering selects representative pages to build a **Global Style Registry**.
2.  **Stage 1: Triplet Extraction** - Parallel sliding-window processing with temporal awareness.
3.  **Stage 2: Realization** - Automated assembly of Markdown, physical image cropping, and cumulative indexing.

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/biogod2020/gemini-driven-img2md.git
cd gemini-driven-img2md

# Install dependencies using Poetry
poetry install
```

---

## 📖 Usage Guide

### 1. Style Profiling (Stage 0)
Analyze the document DNA before full extraction.
```bash
python src/gemini_driven_img2md/cli.py profile resources/paper.pdf --output ./output/paper_profile
```

### 2. High-Fidelity Extraction (Stage 1)
Convert pages with triplet context and style guidance.
```bash
python src/gemini_driven_img2md/cli.py extract resources/paper.pdf --page 1 --prev-page 0 --next-page 2 --style-profile ./output/paper_profile/style_profile.json
```

### 3. Full Batch Processing
Run the automated pipeline for all resources.
```bash
python batch_process.py
```

### 4. Benchmark Evaluation
Measure accuracy (NID/MHS) against the `opendataloader-bench` dataset.
```bash
python src/gemini_driven_img2md/cli.py benchmark --max-docs 30 --concurrency 4
```

---

## 📊 Performance

| Metric | gemini-driven-img2md | Industry SOTA (Docling/Marker) |
| :--- | :---: | :---: |
| **Reading Order (NID)** | **0.91** | 0.89 - 0.90 |
| **Heading Hierarchy (MHS)** | **0.73** | 0.74 - 0.80 |
| **Processing Speed** | **~29s / page** | 0.7s - 54s |

*Data based on 200-document OpenDataLoader-Bench run.*

---

## 🤖 MCP Server (NEW)

This tool now supports the **Model Context Protocol (MCP)**. You can connect your LLM directly to this engine to "see" and "reconstruct" documents in real-time.

```bash
# Start the MCP server
python src/gemini_driven_img2md/mcp_server.py
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
