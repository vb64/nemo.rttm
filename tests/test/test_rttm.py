"""Module rttm.py tests.

make test T=test_rttm.py
"""
from pydub import AudioSegment
from . import TestBase


class TestRttm(TestBase):
    """Module rttm.py."""

    def test_speakers(self):
        """Check speakers count for rttm."""
        from rttm import NemoRttm

        rttm = NemoRttm.from_file(self.fixture('xxx.rttm'), 777, 0)
        assert len(rttm.speakers) == 2

    def test_join_rttms(self):
        """Check join_rttms function."""
        from rttm import join_rttms

        length_ms = len(AudioSegment.from_mp3(self.fixture('short.mp3')))
        assert length_ms == 19593
        speak_2 = (self.fixture('xxx.rttm'), length_ms)

        rttm = join_rttms([
          speak_2,
          speak_2,
        ])

        assert rttm.length_ms == (length_ms * 2)
        assert rttm.rows[-1].speaker == 0
        assert len(rttm.speakers) == 2

        rttm = join_rttms([
          speak_2,
          speak_2,
          speak_2,
        ])
        assert rttm.length_ms == (length_ms * 3)
        assert rttm.rows[-1].speaker == 1
        assert len(rttm.speakers) == 2

        speak_3 = (self.fixture('poly.rttm'), length_ms)

        rttm = join_rttms([
          speak_3,
          speak_3,
          speak_3,
        ])

        assert rttm.length_ms == (length_ms * 3)
        assert len(rttm.speakers) == 9
