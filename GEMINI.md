# gemini-driven-img2md

## Project Overview
This project is focused on the conversion of complex research papers (PDF format) into high-quality Markdown. It leverages Gemini's vision and reasoning capabilities to accurately capture text, mathematical notation, tables, and figure descriptions from academic publications.

The current workspace contains a set of "SOTA" (State-of-the-Art) research papers related to single-cell dynamics and spatial transcriptomics, which likely serve as the primary test cases or source material for the conversion engine.

## Directory Structure
- `resources/`: Contains the source PDF files to be processed.
- `GEMINI.md`: This instruction and context file.

## Key Resources
- **CellPace (`resources/cellpace.pdf`)**: A bioRxiv preprint describing a temporal diffusion-forcing framework for single-cell dynamics.
- **ContextFlow (`resources/contextflow.pdf`)**: An arXiv paper on context-aware flow matching for trajectory inference from spatial omics data.
- **NicheFlow (`resources/nicheflow.pdf`)**: A NeurIPS 2025 paper focusing on modeling microenvironment trajectories in spatial transcriptomics.

## Usage
The intended workflow involves:
1.  Using Gemini's vision capabilities to read the pages of the PDFs in the `resources/` directory.
2.  Extracting structured content including headers, paragraphs, LaTeX-style equations, and table data.
3.  Generating a clean Markdown representation that preserves the semantic meaning and structural integrity of the original research.

## Development Status
- [x] Initial resource collection.
- [ ] Automated extraction pipeline.
- [ ] Quality validation and review.
