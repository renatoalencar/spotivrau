import pytest
from mongoengine import connect, disconnect
from spotivrau import app

app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MONGO_CONNECTION_URI'] = 'mongodb://root:spotivrau@localhost/spotivrau?authSource=admin'

@pytest.fixture
def client():
    with app.test_client() as client:
        connect(host=app.config['MONGO_CONNECTION_URI'])

        yield client

    disconnect()
