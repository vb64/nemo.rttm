"""Module to_rttm.py tests.

make test T=test_to_rttm.py
"""
import os
import pytest

from . import TestBase


class TestToRttm(TestBase):
    """Module to_rttm.py."""

    @pytest.mark.longrunning
    def test_main(self):
        """Check main function."""
        from to_rttm import PARSER, main

        options = PARSER.parse_args([
          "--temp_folder", self.build('temp'),
          "--config", os.path.join('nemo.config', 'diar_infer_telephonic.yaml'),
          self.fixture('short.mp3'),
          self.build('short.rttm'),
        ])

        assert main(options) == 0
