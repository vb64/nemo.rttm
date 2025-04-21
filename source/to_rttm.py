"""Make Nemo rttm files."""
import os
import sys
import time
from nemo_msdd import diarize

VERSION = '1.0'
COPYRIGHTS = 'Copyrights by Vitaly Bogomolov 2025'
PARSER = argparse.ArgumentParser(description='Nemo diarize tool.')

PARSER.add_argument(
  "wav_file",
  help="Wav file for diarize."
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


def main(options):
    print("Nemo diarization tool v.{}. {}".format(VERSION, COPYRIGHTS))
    start_time = time.time()
    diarize(options.wav_file, 'cpu', options.num_speakers, options.temp_folder, options.config)
    dest = os.path.splitext(options.wav_file)[0] + '.rttm'
    print(dest, "{} sec".format(int(time.time() - start_time)))


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(PARSER.parse_args()))
