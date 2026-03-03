import pytest
from pathlib import Path
from PIL import Image
import numpy as np
from gemini_driven_img2md.profiler import calculate_page_density, select_representative_pages

def test_calculate_page_density():
    """Test density calculation for simple images."""
    # 1. Pure white image (density 0)
    white_img = Image.new("RGB", (100, 100), color="white")
    assert calculate_page_density(white_img) == 0.0
    
    # 2. Pure black image (density 1.0)
    black_img = Image.new("RGB", (100, 100), color="black")
    assert calculate_page_density(black_img) == 1.0
    
    # 3. Half black, half white (density 0.5)
    half_img = Image.new("RGB", (100, 100), color="white")
    pixels = np.array(half_img)
    pixels[:50, :, :] = 0  # Black top half
    half_img = Image.fromarray(pixels)
    # Density might be slightly different depending on how 'non-white' is defined,
    # but for a simple black/white split it should be around 0.5.
    assert 0.45 <= calculate_page_density(half_img) <= 0.55

def test_select_representative_pages():
    """Test the clustering selection logic."""
    # Create a dummy list of densities for 50 pages
    # Patterns: 0-9 (low), 10-19 (high), 20-29 (medium), 30-49 (low)
    densities = [0.1]*10 + [0.8]*10 + [0.4]*10 + [0.1]*20
    
    # Select 5 pages
    selected = select_representative_pages(densities, max_samples=5)
    
    assert len(selected) == 5
    assert len(set(selected)) == 5  # No duplicates
    
    # Should include at least one from high density and one from low
    # (assuming the algorithm tries to cover the range)
    # Indices 10-19 are high, 0-9 are low.
    has_high = any(10 <= idx < 20 for idx in selected)
    has_low = any(0 <= idx < 10 for idx in selected)
    assert has_high
    assert has_low

def test_select_representative_pages_small():
    """Test selection when fewer pages than max_samples."""
    densities = [0.1, 0.2, 0.3]
    selected = select_representative_pages(densities, max_samples=5)
    assert selected == [0, 1, 2]

def test_select_representative_pages_uniform():
    """Test selection when all pages have same density."""
    densities = [0.5] * 20
    selected = select_representative_pages(densities, max_samples=5)
    assert len(selected) == 5
    assert 0 in selected
    assert 19 in selected

def test_select_representative_pages_filling():
    """Test the logic that fills remaining slots."""
    # Only 3 pages, but we want 15. Logic should handle it.
    densities = [0.1, 0.5, 0.9]
    selected = select_representative_pages(densities, max_samples=15)
    assert len(selected) == 3
    assert selected == [0, 1, 2]

def test_select_representative_pages_linear_fallback():
    """Test fallback when buckets are empty or pages already in selected."""
    # Special case to trigger 'active_buckets' being empty or similar
    densities = [0.0, 1.0] # Only 2 pages, both always selected
    selected = select_representative_pages(densities, max_samples=1)
    assert len(selected) == 2 # 0 and 1 always included
