import ffmpeg


class Transcoder:
    def __init__(self, file):
        self.file = file

    def transcode(self, destination):
        ffmpeg \
            .input(self.file) \
            .output(destination, vn=None) \
            .run()

        return destination
