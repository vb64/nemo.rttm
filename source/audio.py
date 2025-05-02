"""Split audio file stuff."""
from pydub.silence import detect_silence


def get_cut_positions(silence_chunks, chunk_length_ms):
    """Return list of cut positions for given minimal chunk length."""
    offset = 0
    cuts = []
    for start, end in silence_chunks:
        pos = start + int((end - start) / 2)
        if (pos - offset) >= chunk_length_ms:
            cuts.append(pos)
            offset = pos

    return cuts


def split_on_silence_min_length(
    audio,
    min_silence_len=1000, silence_thresh=-16, seek_step=1,
    min_chunk_length=0
):
    """Return list of audio segments from splitting audio_segment on silent sections.

    audio_segment - original pydub.AudioSegment() object

    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms

    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS

    seek_step - step size for interating over the segment in ms

    min_chunk_length - minimal chunk length (in ms).
        default: 0 (no minimal chunk length, split by middle of silence segments)
    """
    silence_chunks = detect_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        seek_step=seek_step
    )
    chunks = []
    start = 0
    for i in get_cut_positions(silence_chunks, min_chunk_length):
        chunks.append(audio[start:i])
        start = i
    chunks.append(audio[start:])

    return chunks
