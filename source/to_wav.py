"""Make mono wav from mp3 files."""
import os
import sys
import argparse

import torch
import torchaudio
import faster_whisper

VERSION = '1.0'
COPYRIGHTS = 'Copyrights by Vitaly Bogomolov 2025'
PARSER = argparse.ArgumentParser(description='Mp3 to mono wav tool.')

PARSER.add_argument(
  "mp3_file",
  help="Mp3 file for diarize."
)


def main(options):
    """Entry point."""
    print("Mp3 to mono wav tool v.{}. {}".format(VERSION, COPYRIGHTS))
    waveform = faster_whisper.decode_audio(options.mp3_file)
    wav_file = os.path.splitext(options.mp3_file)[0] + '.wav'
    torchaudio.save(
      wav_file,
      torch.from_numpy(waveform).unsqueeze(0).float(),
      16000,
      channels_first=True
    )
    print(wav_file)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(PARSER.parse_args()))
