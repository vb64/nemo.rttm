"""Make Nemo rttm files."""
import os
import sys
import time
import shutil
import argparse

import torch
import torchaudio
import faster_whisper

from nemo_msdd import diarize

VERSION = '1.0'
COPYRIGHTS = 'Copyrights by Vitaly Bogomolov 2025'
PARSER = argparse.ArgumentParser(description='Nemo diarize tool.')

PARSER.add_argument(
  "mp3_file",
  help="Mp3 file for diarize."
)
PARSER.add_argument(
  "rttm_file",
  help="Rttm file for output."
)
PARSER.add_argument(
  "--num_speakers",
  type=int,
  default=0,
  help="Forcing the number of speakers, default 0 (auto detection)",
)
PARSER.add_argument(
  "--temp_folder",
  default='temp',
  help="Folder for temp files.",
)
PARSER.add_argument(
  "--config",
  default='nemo.cfg',
  help="Path to Nemo config file.",
)
PARSER.add_argument(
  "--max_length",
  type=int,
  default=90,
  help="Split the input file into parts if its duration in minutes exceeds the parameter value. Default is 90 minutes.",
)


def get_tasks(mp3_file, _temp_folder, _max_length):
    """Create task list for given mp3."""
    return [mp3_file]


def join_rttms(rttms, rttm_file):
    """Create rttm files from list to single rttm file."""
    shutil.copyfile(rttms[0], rttm_file)


def make_rttm(mp3_file, num_speakers, config_file, temp_folder):
    """Create rttm file by given mp3."""
    waveform = faster_whisper.decode_audio(mp3_file)
    name = os.path.basename(mp3_file)
    wav_file = os.path.join(temp_folder, name + ".wav")
    torchaudio.save(  # pylint: disable=no-member
      wav_file,
      torch.from_numpy(waveform).unsqueeze(0).float(),
      16000,
      channels_first=True
    )
    diarize(wav_file, 'cpu', num_speakers, temp_folder, config_file)

    return os.path.join(temp_folder, "pred_rttms", name + ".rttm")


def main(options):
    """Entry point."""
    print("Nemo diarization tool v.{}. {}".format(VERSION, COPYRIGHTS))
    start_time = time.time()

    os.makedirs(options.temp_folder, exist_ok=True)
    rttms = [
      make_rttm(i, options.num_speakers, options.config, options.temp_folder)
      for i in get_tasks(options.mp3_file, options.temp_folder, options.max_length)
    ]
    join_rttms(rttms, options.rttm_file)
    shutil.rmtree(options.temp_folder)

    print(options.rttm_file, "{} sec".format(int(time.time() - start_time)))


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(PARSER.parse_args()))
