from gemini_driven_img2md.extraction import parse_gemini_response

sample_response = """
---
```json
{
  "document_metadata": {"title": "Test Paper"},
  "assets": [{"id": "fig1", "bbox": [100, 100, 200, 200], "caption": "Figure 1"}]
}
```
---
# Test Content
![Figure 1](assets/fig1.png)
"""

try:
    metadata, markdown = parse_gemini_response(sample_response)
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
