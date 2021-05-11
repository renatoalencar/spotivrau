import os


dirname = os.path.dirname(os.path.realpath(__file__))


def file_fixture_path(name):
    return os.path.join(dirname, 'fixtures', name)


def file_fixture(name):
    return open(file_fixture_path(name), 'rb')


def uploaded_media_path(client, name):
    return os.path.join(
        client.application.config['UPLOAD_FOLDER'],
        name
    )
