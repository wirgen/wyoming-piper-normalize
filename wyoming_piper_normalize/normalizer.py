import logging
import time
from typing import Optional

from runorm import RUNorm

_LOGGER = logging.getLogger(__name__)


class Normalizer:
    _instance = None
    _normalizer: Optional[RUNorm] = None


    def __new__(cls, data_dir: Optional[str] = None, model_size='small', device='cpu'):
        if cls._instance is None:
            cls._instance = super(Normalizer, cls).__new__(cls)

            _LOGGER.info(f"Download RUNorm model {model_size}...")
            start_time = time.time()

            try:
                cls._normalizer = RUNorm()
                cls._normalizer.load(model_size=model_size, device=device, workdir=data_dir)
                end_time = time.time()
                _LOGGER.info(f"RUNorm model loaded in {end_time - start_time:.2f} seconds")
            except Exception as e:
                _LOGGER.error(f"Error while loading: {e}")
                cls._normalizer = None

        return cls._instance


    def normalize(self, text: str) -> str:
        if self._normalizer:
            return self._normalizer.norm(text)
        else:
            _LOGGER.error("RUNorm is not initialized")
            return text
