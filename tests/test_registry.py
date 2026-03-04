import json
import pytest
from pathlib import Path
from gemini_driven_img2md.registry import StyleRegistryManager

def test_registry_manager_init(tmp_path):
    # Test with no file
    manager = StyleRegistryManager()
    assert manager.registry == {}
    
    # Test with base file
    profile = {"h1": "bold"}
    profile_path = tmp_path / "profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile, f)
        
    manager = StyleRegistryManager(profile_path)
    assert manager.registry["h1"] == "bold"

def test_apply_patch():
    manager = StyleRegistryManager()
    manager.registry = {"heading_weights": {"h1": "large"}}
    
    patch = {"heading_weights": {"h2": "medium"}, "new_rule": "strict"}
    manager.apply_patch(patch)
    
    assert manager.registry["heading_weights"]["h1"] == "large"
    assert manager.registry["heading_weights"]["h2"] == "medium"
    assert manager.registry["new_rule"] == "strict"
    assert len(manager.patches) == 1
