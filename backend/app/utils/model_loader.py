"""
Model Loader Utility
Loads and manages ML models
"""
import pickle
import os

# Global model storage
_sarima_model = None


def load_sarima_model():
    """Load SARIMA model from disk"""
    global _sarima_model

    if _sarima_model is not None:
        return _sarima_model

    from ..config.settings import SARIMA_MODEL_PATH

    if os.path.exists(SARIMA_MODEL_PATH):
        try:
            with open(SARIMA_MODEL_PATH, "rb") as f:
                _sarima_model = pickle.load(f)
            print("✓ SARIMA model loaded successfully")
            return _sarima_model
        except Exception as e:
            print(f"Warning: Could not load SARIMA model: {e}")
            return None
    else:
        print(f"Warning: SARIMA model not found at {SARIMA_MODEL_PATH}")
        return None


def get_sarima_model():
    """Get loaded SARIMA model instance"""
    global _sarima_model
    if _sarima_model is None:
        _sarima_model = load_sarima_model()
    return _sarima_model
