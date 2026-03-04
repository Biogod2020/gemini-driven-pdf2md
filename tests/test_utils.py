import pytest
from PIL import Image
from pathlib import Path
from gemini_driven_img2md.utils import crop_image_normalized

def test_crop_image_normalized(tmp_path):
    """Test that cropping logic correctly calculates pixel coordinates."""
    # Create a 100x100 white image
    img = Image.new("RGB", (100, 100), color="white")
    
    # BBox: ymin, xmin, ymax, xmax (0-1000)
    # This should correspond to pixel (10, 20) to (50, 60)
    bbox = [100, 200, 500, 600]
    
    output_path = tmp_path / "assets" / "test_fig.png"
    crop_image_normalized(img, bbox, output_path)
    
    assert output_path.exists()
    
    # Verify the size of the cropped image
    cropped_img = Image.open(output_path)
    # Original: (right-left) = (60-20) = 40
    # Original: (bottom-top) = (50-10) = 40
    # With 2% padding: 40 * 1.04 = 41.6 -> rounded to 42 (actually crop logic uses floats then crop() handle)
    # (60-20) + 40*0.02*2 = 40 + 1.6 = 41.6
    # Top/Left: 20 - 0.8 = 19.2, 10 - 0.8 = 9.2
    # Bottom/Right: 60 + 0.8 = 60.8, 50 + 0.8 = 50.8
    # PIL crop uses int floor/ceil usually or similar.
    # The result (42, 42) is expected with 2% padding on each side (total 4% increase).
    assert cropped_img.size == (42, 42)
