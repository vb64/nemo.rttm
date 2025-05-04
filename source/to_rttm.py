"""Make Nemo rttm files."""
import os
import sys
import time
import shutil
import argparse

import torch
import torchaudio
import faster_whisper
from pydub import AudioSegment
import audioread

from audio import split_on_silence_min_length
from nemo_msdd import diarize
from rttm import join_rttms

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
  default=90 * 60,
  help="Split the input file into parts if its duration in seconds exceeds the parameter value. Default is 5400 (90 minutes).",
)


def get_tasks(mp3_file, temp_folder, max_length_sec):
    """Create task list for given mp3."""
    length_sec = audioread.audio_open(mp3_file).duration
    print("# File", mp3_file, length_sec, "sec")

    if length_sec <= max_length_sec:
        print("# Single file.")
        return [mp3_file]

    audio = AudioSegment.from_mp3(mp3_file)
    chunks = split_on_silence_min_length(
      audio, min_silence_len=100, silence_thresh=-40, min_chunk_length=max_length_sec * 1000
    )
    print("# Split to chunks:", len(chunks))

    name = os.path.join(temp_folder, "nemo_chunk_")
    names = []
    for i, chunk in enumerate(chunks):
        names.append(name + str(i) + ".mp3")
        chunk.export(names[-1], format='mp3')

    return names


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
    audio = AudioSegment.from_mp3(mp3_file)

    return (
      os.path.join(temp_folder, "pred_rttms", name + ".rttm"),
      len(audio),
    )


def main(options):
    """Entry point."""
    print("Nemo diarization tool v.{}. {}".format(VERSION, COPYRIGHTS))
    start_time = time.time()

    os.makedirs(options.temp_folder, exist_ok=True)
    rttm = join_rttms([
      make_rttm(i, options.num_speakers, options.config, options.temp_folder)
      for i in get_tasks(options.mp3_file, options.temp_folder, options.max_length)
    ])
    rttm.save(options.rttm_file)
    shutil.rmtree(options.temp_folder)

    print(options.rttm_file, "{} sec".format(int(time.time() - start_time)))

    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(PARSER.parse_args()))
