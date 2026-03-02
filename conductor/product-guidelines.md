# Product Guidelines: gemini-driven-img2md

## Content Integrity
- **Source-Faithful Extraction**: The core mission is extraction, not transformation. Never alter the original document's prose, tone, or content. The generated Markdown must be a direct semantic representation of the source.

## Layout & Formatting
- **Inferred Semantic Structure**: Utilize Gemini's vision capabilities to infer the document's hierarchy (headers, lists, blockquotes) and map them to standard Markdown (H1-H6).
- **Document-Driven Styling**: Formatting rules (e.g., indentation, spacing) should be derived from the input document's visual layout to ensure a unified and consistent output.

## Multimodal Handling
- **Image Extraction & Captioning**: For every illustration, extract the literal caption from the original text.
- **Image Indexing**: Generate a companion `images.json` file that indexes all extracted assets, providing descriptions, original captions, and metadata for each.
- **Relative Referencing**: Link extracted images in the Markdown using standard relative paths (e.g., `![alt-text](assets/fig1.png)`).

## Technical Content
- **LaTeX Math Support**: Mathematical expressions must be converted to LaTeX using standard delimiters (`57613` for blocks, `$` for inline).
- **Fenced Code Blocks**: Automatically detect and wrap code snippets in appropriate fenced blocks with language hints where possible.
- **Markdown Tables**: Convert tabular data into well-formatted Markdown tables, preserving the original data structure.
- **Maximum Context Retention**: Aim to capture as much content as possible from the source document, minimizing omissions of small elements or footnotes.
