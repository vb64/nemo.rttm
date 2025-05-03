"""Module rttm.py tests.

make test T=test_rttm.py
"""
from pydub import AudioSegment
from . import TestBase


class TestRttm(TestBase):
    """Module rttm.py."""

    def test_join_rttms(self):
        """Check join_rttms function."""
        from rttm import join_rttms

        length_ms = len(AudioSegment.from_mp3(self.fixture('short.mp3')))
        rttm = join_rttms([
          (self.fixture('xxx.rttm'), length_ms),
          (self.fixture('xxx.rttm'), length_ms),
        ])

        assert rttm.length_ms == (length_ms * 2)
        assert rttm.rows[-1].speaker == 0

        rttm = join_rttms([
          (self.fixture('xxx.rttm'), length_ms),
          (self.fixture('xxx.rttm'), length_ms),
          (self.fixture('xxx.rttm'), length_ms),
        ])
        assert rttm.length_ms == (length_ms * 3)
        assert rttm.rows[-1].speaker == 1
