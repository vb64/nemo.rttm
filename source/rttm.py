"""RTTM file operations."""


class NemoRow:
    """Nemo RTTM file row."""

    # SPEAKER xxx.mp3 1   8.940   6.060 <NA> <NA> speaker_0 <NA> <NA>
    row_template = "SPEAKER {} 1 {:.3f} {:.3f} <NA> <NA> speaker_{} <NA> <NA>\n"

    def __init__(self, rttm_file):
        """Make empty row."""
        self.start = None
        self.length = None
        self.speaker = None
        self.file_index = rttm_file.file_index

    @classmethod
    def from_line(cls, line, rttm_file):
        """Load data from file."""
        obj = cls(rttm_file)
        fields = line.split()
        obj.start = int(float(fields[3]) * 1000)
        obj.length = int(float(fields[4]) * 1000)
        obj.speaker = int(fields[7].split('_')[1])

        return obj

    @property
    def line(self):
        """Return data as string."""
        return self.row_template.format(
          self.file_index,
          self.start / 1000.0,
          self.length / 1000.0,
          self.speaker
        )


class NemoRttm:
    """Nemo RTTM file."""

    encoding = 'UTF-8'

    def __init__(self):
        """Make empty file."""
        self.rows = []
        self.length_ms = 0
        self.file_index = 0

    @classmethod
    def from_file(cls, file_name, file_index, length_ms):
        """Load data from file."""
        obj = cls()
        obj.length_ms = length_ms
        obj.file_index = file_index
        with open(file_name, 'r', encoding=cls.encoding) as inp:
            for line in inp:
                obj.rows.append(NemoRow.from_line(line, obj))

        return obj

    def save(self, file_name):
        """Save data to file."""
        with open(file_name, 'wt', encoding=self.encoding) as out:
            for row in self.rows:
                out.write(row.line)

    def append(self, rttm):
        """Append data from another rttm."""
        last = self.rows[-1]
        first = rttm.rows[0]
        speaker_map = {}
        if last.speaker != first.speaker:
            speaker_map[first.speaker] = last.speaker
            speaker_map[last.speaker] = first.speaker

        for row in rttm.rows:
            row.speaker = speaker_map.get(row.speaker, row.speaker)
            row.start += self.length_ms
            self.rows.append(row)

        self.length_ms += rttm.length_ms


def join_rttms(rttms):
    """Join rttm files from list to single rttm file."""
    name, length = rttms[0]
    rttm = NemoRttm.from_file(name, length, 0)
    for i, (name, length) in enumerate(rttms[1:], start=1):
        rttm.append(NemoRttm.from_file(name, length, i))

    return rttm
