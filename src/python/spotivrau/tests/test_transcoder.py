import magic

from spotivrau.transcoder import Transcoder
from .utils import file_fixture


def test_transcode():
    f = file_fixture('Images - Lost European.wav')

    transcoder = Transcoder(f)
    output = transcoder.transcode('ogg')

    mime = magic.from_buffer(output.read(2048), mime=True)
    assert mime == 'audio/ogg'


def test_metadata():
    f = file_fixture('fixtures/Images - Lost European.wav')

    transcoder = Transcoder(f)
    output = transcoder.metadata()

    assert output['format']['duration'] == '249.026667'


def test_metadata():
    f = file_fixture('Images - Lost European.wav')

    transcoder = Transcoder(f)
    output = transcoder.waveform()

    assert magic.from_buffer(output.read(2048), mime=True) == 'image/png'
