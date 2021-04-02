from spotivrau.transcoder import Transcoder
import os
import io
import magic

dirname = os.path.dirname(os.path.realpath(__file__))

def test_transcode():
    f = open(os.path.join(dirname, 'fixtures/Images - Lost European.wav'), 'rb')

    transcoder = Transcoder(f)
    output = transcoder.transcode('ogg')

    mime = magic.from_buffer(output.read(2048), mime=True)
    assert mime == 'audio/ogg'


def test_metadata():
    f = open(os.path.join(dirname, 'fixtures/Images - Lost European.wav'), 'rb')

    transcoder = Transcoder(f)
    output = transcoder.metadata()

    assert output['format']['duration'] == '249.026667'


def test_metadata():
    f = open(os.path.join(dirname, 'fixtures/Images - Lost European.wav'), 'rb')

    transcoder = Transcoder(f)
    output = transcoder.waveform()

    assert magic.from_buffer(output.read(2048), mime=True) == 'image/png'
