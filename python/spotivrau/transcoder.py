import tempfile
import ffmpeg
import shutil


class Transcoder:
    def __init__(self, file):
        self.file = file
        self._tempfile = None

    @property
    def tempfile(self):
        if self._tempfile is None:
            self._tempfile = tempfile.NamedTemporaryFile()
            shutil.copyfileobj(self.file, self._tempfile)
        else:
            self._tempfile.seek(0)

        return self._tempfile

    def transcode(self, format):
        output = tempfile.NamedTemporaryFile(suffix='.' + format)

        ffmpeg \
            .input(self.tempfile.name) \
            .output(output.name, vn=None) \
            .overwrite_output() \
            .run()

        return output

    def metadata(self):
        return ffmpeg.probe(self.tempfile.name)

    def waveform(self):
        output = tempfile.NamedTemporaryFile(suffix='.png')

        ffmpeg \
            .input(self.tempfile.name) \
            .output(output.name, vframes=1, filter_complex='showwavespic=s=640x120') \
            .overwrite_output() \
            .run()

        return output
