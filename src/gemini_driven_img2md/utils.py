from typing import List, Tuple
from PIL import Image
from pathlib import Path

def crop_image_normalized(image: Image.Image, bbox: List[int], output_path: Path, padding_ratio: float = 0.02):
    """
    Crops an image based on normalized coordinates [ymin, xmin, ymax, xmax] (0-1000),
    adding a small padding to avoid edge truncation.
    """
    width, height = image.size
    
    ymin, xmin, ymax, xmax = bbox
    
    # Calculate initial pixel coordinates
    left = (xmin / 1000.0) * width
    top = (ymin / 1000.0) * height
    right = (xmax / 1000.0) * width
    bottom = (ymax / 1000.0) * height
    
    # Add padding
    pw = (right - left) * padding_ratio
    ph = (bottom - top) * padding_ratio
    
    left = max(0, left - pw)
    top = max(0, top - ph)
    right = min(width, right + pw)
    bottom = min(height, bottom + ph)
    
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

def image_to_base64(image: Image.Image, max_size=(1024, 1024)) -> str:
    """
    Converts a PIL Image to a base64 encoded string, with optional resizing.
    """
    import base64
    from io import BytesIO
    
    img_copy = image.copy()
    img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img_copy.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
