import importlib.util
from pathlib import Path


def load_ai_module():
    path = Path(__file__).resolve().parents[1] / "ai-core" / "aether_ai.py"
    spec = importlib.util.spec_from_file_location("aether_ai", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module
