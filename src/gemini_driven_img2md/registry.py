import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class StyleRegistryManager:
    """
    Manages the Global Style Registry and its incremental evolution via patches.
    """
    def __init__(self, base_profile_path: Optional[Path] = None):
        self.registry: Dict[str, Any] = {}
        self.patches: List[Dict[str, Any]] = []
        
        if base_profile_path and base_profile_path.exists():
            with open(base_profile_path, "r", encoding="utf-8") as f:
                self.registry = json.load(f)

    def apply_patch(self, patch: Dict[str, Any]):
        """
        Applies a delta patch to the current registry.
        """
        if not patch:
            return
            
        self.patches.append(patch)
        # Deep merge or simple update depending on patch structure
        # For now, we'll do a shallow update of keys
        for key, value in patch.items():
            if isinstance(value, dict) and key in self.registry and isinstance(self.registry[key], dict):
                self.registry[key].update(value)
            else:
                self.registry[key] = value

    def get_current_profile_json(self) -> str:
        """
        Returns the current state of the registry as a JSON string.
        """
        return json.dumps(self.registry, indent=2, ensure_ascii=False)

    def save(self, output_path: Path):
        """
        Saves the evolved registry to a file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "registry": self.registry,
            "patches_applied": self.patches
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
