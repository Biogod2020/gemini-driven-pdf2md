# Technical Deep Dive: SOTA Document Intelligence

This document explains the core architectural innovations that power `gemini-driven-img2md`.

## 1. Stage 0: Global Style Profiling

### Problem: Structural Drift
In multi-page documents, LLMs often drift in their interpretation of heading levels (e.g., calling a section "H1" on page 4 but "H2" on page 50) and citation formats.

### Solution: Macro-Micro Intelligence
Before full extraction, the engine performs a **Bootstrapping Phase**:
1.  **Visual-Density Clustering**: The profiler scans the entire document at low resolution to calculate the visual density of every page.
2.  **Diverse Sampling**: It selects up to 15 representative pages (e.g., dense text, sparse diagrams, tables, references).
3.  **DNA Extraction**: Gemini analyzes these samples once to generate a `style_profile.json`.
4.  **Style Registry**: This registry defines the "Heading Weight Dictionary" (mapping font size/weight to H1-H6) and "Visual Matchers" (identifying warning boxes, code blocks, etc.).

## 2. Stage 1: Triplet-Context Sliding Window

### Problem: The "Stitch" Issue
Single-page OCR often breaks paragraphs mid-sentence or fails to recognize that a table continues onto the next page.

### Solution: Spatio-Temporal Reasoning
When processing Page **N**, the engine receives a triplet of images: `[N-1, N, N+1]`.
- **PREVIOUS PAGE (N-1)**: Provides context to ensure the first paragraph of page N correctly joins the last paragraph of page N-1 without repeating headers.
- **TARGET PAGE (N)**: The primary extraction target.
- **NEXT PAGE (N+1)**: Allows the AI to detect if a table or equation is cut off at the bottom, marking it as "continued" or ensuring no content is lost.

### Prompt Engineering
The system prompt uses **Strict Role Definition** and **Output Protocol Enforcement**. It instructs the AI to "see the past and future, but only speak about the present," ensuring that the output is high-fidelity and target-centric.

## 3. Dynamic Style Adaptation

The engine tracks a `style_conformity` score for every page. If the document's layout shifts significantly (e.g., from an academic paper style to an index or glossary), the AI can issue a **Style Patch**—a JSON delta that updates the Global Style Registry in real-time, allowing the pipeline to evolve autonomously.
