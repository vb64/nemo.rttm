"""Module nemo_msdd.py tests.

make test T=test_nemo_msdd.py
"""
import os
from . import TestBase


class MockWget:
    """Mocked wget."""

    def download(self, _url, _path):
        """Mock download function."""
        return os.path.join('nemo.config', 'diar_infer_telephonic.yaml')


class TestNemoMsdd(TestBase):
    """Module nemo_msdd.py."""

    def test_create_config(self):
        """Check create_config function."""
        import nemo_msdd

        wget = nemo_msdd.wget
        nemo_msdd.wget = MockWget()
        assert nemo_msdd.create_config('xxx.wav', self.build(), 'not_exist.yaml', num_speakers=2)
        nemo_msdd.wget = wget
