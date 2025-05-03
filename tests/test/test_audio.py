"""Module audio tests.

make test T=test_audio.py
"""
from pydub import AudioSegment
from . import TestBase


class TestAudio(TestBase):
    """Module audio."""

    def test_split_on_silence_min_length(self):
        """Check split_on_silence_min_length function."""
        from audio import split_on_silence_min_length

        audio = AudioSegment.from_file(self.fixture('short.mp3'))
        assert len(split_on_silence_min_length(audio, min_chunk_length=2 * 1000)) == 2
        assert len(split_on_silence_min_length(audio, min_chunk_length=600 * 1000)) == 1
