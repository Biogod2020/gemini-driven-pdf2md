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
    # (right-left) = (60-20) = 40
    # (bottom-top) = (50-10) = 40
    assert cropped_img.size == (40, 40)
