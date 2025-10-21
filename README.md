# Wyoming Piper Normalize

[Wyoming protocol](https://github.com/rhasspy/wyoming) server for the [Piper](https://github.com/rhasspy/piper/)
text-to-speech system, featuring Russian text normalization via [RUNorm](https://github.com/Den4ikAI/runorm)

## Home Assistant Add-on

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fwirgen%2Fhomeassistant-addons)

[Source](https://github.com/wirgen/homeassistant-addons)

## Local Install

Clone the repository and set up Python virtual environment:

``` sh
git clone https://github.com/wirgen/wyoming-piper-normalize.git
cd wyoming-piper-normalize
pip install -U setuptools wheel
pip install .
python -m wyoming_piper_normalize --voice ru_RU-irina-medium --uri tcp://0.0.0.0:10200 --data-dir /data
```

## Docker Image

``` sh
docker build . -t wyoming-piper-normalize
docker run -it -p 10200:10200 -v /path/to/local/data:/data wyoming-piper-normalize \
    --voice ru_RU-irina-medium --uri tcp://0.0.0.0:10200 --data-dir /data
```