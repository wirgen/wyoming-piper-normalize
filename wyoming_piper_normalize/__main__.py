#!/usr/bin/env python3
import argparse
import asyncio
import logging
from functools import partial
from typing import Dict, Any

from wyoming.info import TtsVoice, Attribution, TtsVoiceSpeaker, Info, TtsProgram
from wyoming.server import AsyncServer

from . import __version__
from .handler import PiperEventHandler
from .normalizer import Normalizer
from .piper_tts import PiperTTS, get_voices

_LOGGER = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--voice",
        required=True,
        help="Default Piper voice to use (e.g., ru_RU-irina-medium)",
    )
    parser.add_argument("--uri", default="stdio://", help="unix:// or tcp://")
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Data directory to check for downloaded models",
    )
    #
    parser.add_argument(
        "--speaker", type=str, help="Name or id of speaker for default voice"
    )
    parser.add_argument("--volume", type=float, help="Voice volume")
    parser.add_argument("--length-scale", type=float, help="Phoneme length")
    parser.add_argument("--noise-scale", type=float, help="Generator noise")
    parser.add_argument(
        "--noise-w-scale", "--noise-w", type=float, help="Phoneme width noise"
    )
    #
    parser.add_argument("--samples-per-chunk", type=int, default=1024)
    parser.add_argument(
        "--streaming",
        action="store_true",
        help="Enable audio streaming on sentence boundaries",
    )
    #
    parser.add_argument(
        "--update-voices",
        action="store_true",
        help="Download latest voices.json during startup",
    )
    #
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument(
        "--log-format", default=logging.BASIC_FORMAT, help="Format for log messages"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print version and exit",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )
    _LOGGER.debug(args)

    # Init Normalizer
    Normalizer(args.data_dir)

    # Init Piper
    pv = PiperTTS(args.data_dir)
    voices_info = get_voices()

    voices = [
        TtsVoice(
            name=voice_name,
            description=get_description(voice_info),
            attribution=Attribution(
                name="rhasspy", url="https://github.com/rhasspy/piper"
            ),
            installed=True,
            version=None,
            languages=[
                voice_info.get("language", {}).get("code")
            ],
            speakers=(
                [
                    TtsVoiceSpeaker(name=speaker_name)
                    for speaker_name in voice_info["speaker_id_map"]
                ]
                if voice_info.get("speaker_id_map")
                else None
            ),
        )
        for voice_name, voice_info in voices_info.items()
    ]

    wyoming_info = Info(
        tts=[
            TtsProgram(
                name="Piper RUNorm",
                description="A fast, local, neural text to speech engine with russian text normalization",
                attribution=Attribution(
                    name="rhasspy", url="https://github.com/rhasspy/piper"
                ),
                installed=True,
                voices=sorted(voices, key=lambda v: v.name),
                version=__version__,
                supports_synthesize_streaming=args.streaming,
            )
        ],
    )

    pv.load_voice(args.voice, force_redownload=args.update_voices)

    # Start server
    server = AsyncServer.from_uri(args.uri)

    _LOGGER.info("Ready")
    await server.run(
        partial(
            PiperEventHandler,
            wyoming_info,
            args,
            voices_info,
        )
    )


def get_description(voice_info: Dict[str, Any]):
    """Get a human-readable description for a voice."""
    name = voice_info["name"]
    name = " ".join(name.split("_"))
    quality = voice_info["quality"]

    return f"{name} ({quality})"


def run():
    asyncio.run(main())


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
