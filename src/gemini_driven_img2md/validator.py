from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
from gemini_driven_img2md.gemini_client import get_gemini_client
from langchain_core.messages import HumanMessage

def image_to_base64(image, max_size=(1024, 1024)):
    img_copy = image.copy()
    img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img_copy.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def validate_conversion(original_image: Image.Image, markdown_path: Path, assets_json_path: Path) -> str:
    """
    Uses Gemini to verify the quality of the conversion.
    """
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(assets_json_path, "r", encoding="utf-8") as f:
        assets_json = f.read()
        
    client = get_gemini_client()
    
    validation_prompt = f"""
You are a Quality Assurance bot for document conversion.
Compare the provided original document image with the extracted Markdown content and the extracted assets index.

### Criteria:
1. **Content Accuracy**: Is all text present and accurate?
2. **Structural Fidelity**: Are headers, lists, and tables correctly identified?
3. **Multimodal Extraction**: Are all figures identified? Do the bounding boxes in the metadata (inferred from placeholders) seem correct?
4. **Formatting**: Is LaTeX used correctly for math?

### Extracted Markdown:
```markdown
{markdown_content}
```

### Extracted Assets Metadata:
```json
{assets_json}
```

Provide a brief report on whether the conversion is "PERFECT", "GOOD", or "FAILED". If not perfect, list the specific issues.
"""

    base64_image = image_to_base64(original_image)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": validation_prompt},
            {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{base64_image}",
            },
        ]
    )
    
    response = client.invoke([message])
    return response.content
