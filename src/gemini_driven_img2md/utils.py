from typing import List, Tuple
from PIL import Image
from pathlib import Path

def crop_image_normalized(image: Image.Image, bbox: List[int], output_path: Path):
    """
    Crops an image based on normalized coordinates [ymin, xmin, ymax, xmax] (0-1000).
    
    Args:
        image: The PIL Image object.
        bbox: List of 4 integers [ymin, xmin, ymax, xmax] between 0 and 1000.
        output_path: Path where the cropped image will be saved.
    """
    width, height = image.size
    
    ymin, xmin, ymax, xmax = bbox
    
    # Convert normalized to pixel coordinates
    left = (xmin / 1000.0) * width
    top = (ymin / 1000.0) * height
    right = (xmax / 1000.0) * width
    bottom = (ymax / 1000.0) * height
    
    # Crop and save
    cropped = image.crop((left, top, right, bottom))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(output_path)
    return output_path

def get_page_image(pdf_path: Path, page_number: int, dpi: int = 300) -> Image.Image:
    """
    Converts a specific PDF page to a PIL Image using PyMuPDF.
    """
    import fitz  # PyMuPDF
    
    doc = fitz.open(str(pdf_path))
    page = doc.load_page(page_number)
    
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/300)) # Adjust scaling for DPI
    # Note: fix matrix calculation for exact DPI if needed
    pix = page.get_pixmap(dpi=dpi)
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img
