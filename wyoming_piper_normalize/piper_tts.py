import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional

from piper import PiperVoice
from piper.download_voices import download_voice

_LOGGER = logging.getLogger(__name__)


def get_voices() -> Dict[str, Any]:
    """Loads available voices from downloaded or embedded JSON file."""
    voices_embedded = Path(__file__).parent / "voices.json"
    with open(voices_embedded, "r", encoding="utf-8") as voices_file:
        voices = json.load(voices_file)

    return voices


class PiperTTS:
    _instance = None
    _voice_dir: Optional[Path] = None
    _voice: Optional[PiperVoice] = None


    def __new__(cls, voice_dir: Optional[str] = None):
        if cls._instance is None:
            if voice_dir is None:
                raise ValueError('Voice dir must be set')

            cls._instance = super(PiperTTS, cls).__new__(cls)
            cls._voice_dir = Path(voice_dir).resolve()

        return cls._instance


    def load_voice(self, voice: str, force_redownload: bool = False) -> Optional[PiperVoice]:
        _LOGGER.info(f"Download voice model {voice}...")
        start_time = time.time()

        download_voice(voice, self._voice_dir, force_redownload=force_redownload)
        voice_path = self._voice_dir / f"{voice}.onnx"
        self._voice = PiperVoice.load(str(voice_path))
        end_time = time.time()
        _LOGGER.info(f"Voice model loaded in {end_time - start_time:.2f} seconds")

        return self._voice


    def get_voice(self) -> Optional[PiperVoice]:
        if self._voice:
            return self._voice
        else:
            _LOGGER.error("Voice is not loaded")
            return None
