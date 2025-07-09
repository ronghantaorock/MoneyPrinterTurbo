"""Data models for edge-tts."""

import argparse
import re


class TTSConfig:
    """
    Represents the internal TTS configuration for edge-tts's Communicate class.
    """

    voice: str
    rate: str
    volume: str
    pitch: str

    @staticmethod
    def validate_string_param(param_name: str, param_value: str, pattern: str) -> str:
        """
        Validates the given string parameter based on type and pattern.

        Args:
            param_name (str): The name of the parameter.
            param_value (str): The value of the parameter.
            pattern (str): The pattern to validate the parameter against.

        Returns:
            str: The validated parameter.
        """
        if not isinstance(param_value, str):
            raise TypeError(f"{param_name} must be str")
        if re.match(pattern, param_value) is None:
            raise ValueError(f"Invalid {param_name} '{param_value}'.")
        return param_value

    def __init__(self, voice: str, rate: str, volume: str, pitch: str):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch

    def __post_init__(self) -> None:
        """
        Validates the TTSConfig object after initialization.
        """

        # Possible values for voice are:
        # - Microsoft Server Speech Text to Speech Voice (cy-GB, NiaNeural)
        # - cy-GB-NiaNeural
        # - fil-PH-AngeloNeural
        # Always send the first variant as that is what Microsoft Edge does.
        match = re.match(r"^([a-z]{2,})-([A-Z]{2,})-(.+Neural)$", self.voice)
        if match is not None:
            lang = match.group(1)
            region = match.group(2)
            name = match.group(3)
            if name.find("-") != -1:
                region = region + "-" + name[: name.find("-")]
                name = name[name.find("-") + 1 :]
            self.voice = ("Microsoft Server Speech Text to Speech Voice" + f" ({lang}-{region}, {name})")

        # Validate the rate, volume, and pitch parameters.
        self.validate_string_pattern("voice", self.voice,r"^Microsoft Server Speech Text to Speech Voice \(.+,.+\)$")
        self.validate_string_pattern("rate", self.rate, r"^[+-]\d+%$")
        self.validate_string_pattern("volume", self.volume, r"^[+-]\d+%$")
        self.validate_string_pattern("pitch", self.pitch, r"^[+-]\d+Hz$")


class UtilArgs(argparse.Namespace):
    """CLI arguments."""

    text: str
    file: str
    voice: str
    list_voices: bool
    rate: str
    volume: str
    pitch: str
    words_in_cue: int
    write_media: str
    write_subtitles: str
    proxy: str
