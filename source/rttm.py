"""RTTM file operations.

https://habr.com/ru/articles/900988/
"""


class NemoRow:
    """Nemo RTTM file row."""

    # SPEAKER xxx.mp3 1   8.940   6.060 <NA> <NA> speaker_0 <NA> <NA>
    row_template = "SPEAKER {} 1 {} {} <NA> <NA> speaker_{} <NA> <NA>\n"

    def __init__(self):
        """Make empty row."""
        self.start = None
        self.length = None
        self.fname = None
        self.speaker = None

    @classmethod
    def from_line(cls, line):
        """Load data from file."""
        obj = cls()
        fields = line.split()
        obj.fname = fields[1]
        obj.start = int(float(fields[3]) * 1000)
        obj.length = int(float(fields[4]) * 1000)
        obj.speaker = int(fields[7].split('_')[1])

    @property
    def line(self):
        """Return data as string."""
        return self.row_template.format(
          self.fname,
          round(self.start / 1000.0, 3),
          round(self.length / 1000.0, 3),
          self.speaker
        )


class NemoRttm:
    """Nemo RTTM file."""

    encoding = 'UTF-8'

    def __init__(self):
        """Make empty file."""
        self.speakers = {}
        self.rows = []

    @classmethod
    def from_file(cls, file_name):
        """Load data from file."""
        obj = cls()
        with open(file_name, 'r', encoding=cls.encoding) as inp:
            for line in inp:
                row = NemoRow.from_line(line)
                if row.speaker not in obj.speakers:
                    obj.speakers[row.speaker] = []
                obj.speakers[row.speaker].append(row)
                obj.rows.append(row)

    def save(self, file_name):
        """Save data to file."""
        with open(file_name, 'wt', encoding=self.encoding) as out:
            for row in self.rows:
                out.write(row.line)

    def append(self, rttm):
        """Append data from another rttm."""
