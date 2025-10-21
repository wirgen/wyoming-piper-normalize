"""Wyoming server for Piper TTS with Russian text normalization"""


def get_version():
    """Get package version with fallback."""
    try:
        from importlib.metadata import version
        return version("wyoming_piper_normalize")
    except Exception:
        return '0.0.0'


__version__ = get_version()

__all__ = ['__version__', 'get_version']
