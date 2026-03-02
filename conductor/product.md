# Initial Concept\n一个简单快捷的利用gemini模型的多模态能力将pdf/其他带图文档转换为格式规范统一的markdown文档（其中markdown的格式规范应该从文档中infer出来，所有的插图都应该利用vlm截取+caption+单独储存+在生成的markdown中引用）

# Product Guide: gemini-driven-img2md

## Vision
A high-fidelity multimodal document conversion tool that leverages Gemini's vision and reasoning capabilities to transform PDFs and image-heavy documents into standard, unified Markdown. It prioritizes structural accuracy, seamless image extraction with AI-generated captions, and LaTeX math support.

## Target Users
- **Researchers/Academics**: Converting scientific papers for better readability, searchability, and archival.
- **Developers**: Integrating automated document conversion into existing workflows or knowledge bases.
- **Technical Writers**: Migrating legacy documentation or image-rich manuals into modern Markdown formats.

## Core Goals
- **High Structural Fidelity**: Accurately infer document hierarchy (headers, lists, tables) from the source layout.
- **Processing Speed**: Efficiently convert complex documents without sacrificing accuracy.
- **Rich Multimodal Support**: Automatically detect, extract, and caption all visual elements.

## Key Features
- **Layout Inference**: Automatically determines formatting rules based on the input document's structure.
- **VLM-based Image Extraction**: Uses Vision-Language Models to intercept, crop, and caption illustrations.
- **LaTeX Math Support**: Converts complex mathematical notation into standard LaTeX.
- **Local Asset Management**: Extracted images are stored in a dedicated local `assets/` folder and referenced within the Markdown.

## Technical Scope
- **Input**: PDF files, documents with images.
- **Output**: Markdown (.md) files with relative image links.
- **Engine**: Gemini Multimodal APIs.
