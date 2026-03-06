import json
from gemini_driven_img2md.extraction import parse_gemini_json_response

def simulate_stream_accumulation(chunks):
    """Simulates the logic in process_pdf_page for chunks."""
    response_text = ""
    for chunk_content in chunks:
        if isinstance(chunk_content, list):
            text_parts = []
            for part in chunk_content:
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
                elif isinstance(part, str):
                    text_parts.append(part)
            response_text += "".join(text_parts)
        elif isinstance(chunk_content, str):
            response_text += chunk_content
    return response_text

def test_stream_pressure_scenarios():
    print("\n🔥 Starting Streaming Pressure Tests...")
    
    # Scenario 1: JSON split across chunks
    chunks_1 = [
        "```json\n{\n  \"mark",
        "down\": \"# Markdown Content\",\n  \"doc",
        "ument_metadata\": {\"title\": \"Test\"},\n  \"assets\": []\n}",
        "\n```"
    ]
    full_text_1 = simulate_stream_accumulation(chunks_1)
    metadata, markdown = parse_gemini_json_response(full_text_1)
    assert metadata["document_metadata"]["title"] == "Test"
    assert "# Markdown Content" in markdown
    print("✅ Scenario 1: JSON split across chunks PASSED")

    # Scenario 2: Truncated JSON in stream
    chunks_2 = [
        "```json\n{\"markdown\": \"# Only Markdown here\", \"id\": \"truncated\"",
        "\n```"
    ]
    full_text_2 = simulate_stream_accumulation(chunks_2)
    metadata, markdown = parse_gemini_json_response(full_text_2)
    assert metadata["id"] == "truncated"
    assert "# Only Markdown here" in markdown
    print("✅ Scenario 2: Truncated JSON in stream PASSED")

    # Scenario 3: Large content with nested braces
    chunks_3 = [
        "```json\n{\"markdown\": \"# Math: $$x^2$$\", \"complex\": {\"nested\": [1, 2, 3]}, \"assets\": []}```"
    ]
    full_text_3 = simulate_stream_accumulation(chunks_3)
    metadata, markdown = parse_gemini_json_response(full_text_3)
    assert metadata["complex"]["nested"] == [1, 2, 3]
    assert "$$x^2$$" in markdown
    print("✅ Scenario 3: Complex nested structure PASSED")

    # Scenario 4: No Markdown markers, just raw text (fallback)
    chunks_4 = [
        "{\"markdown\": \"raw text\", \"just\": \"json\"}",
        " and then some extra text"
    ]
    full_text_4 = simulate_stream_accumulation(chunks_4)
    metadata, markdown = parse_gemini_json_response(full_text_4)
    assert metadata["just"] == "json"
    assert "raw text" in markdown
    print("✅ Scenario 4: Raw text fallback PASSED")

if __name__ == "__main__":
    try:
        test_stream_pressure_scenarios()
        print("\n🏆 ALL STREAM PRESSURE TESTS PASSED")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ TEST FAILED: {e}")
