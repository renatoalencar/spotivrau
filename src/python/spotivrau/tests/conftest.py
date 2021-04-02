import pytest
import redis
from mongoengine import connect, disconnect
from spotivrau import app

app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MONGO_CONNECTION_URI'] = 'mongodb://root:spotivrau@localhost/spotivrau?authSource=admin'
app.config['REDIS_CONNECTION_URI'] = 'redis://localhost/1'

@pytest.fixture
def current_app():
    connect(host=app.config['MONGO_CONNECTION_URI'])

    redis_connection = redis.Redis.from_url(app.config['REDIS_CONNECTION_URI'])
    app.queue.set_connection(redis_connection)

    yield app

    disconnect()

    redis_connection.execute_command('DEL', 'transcode')
    redis_connection.close()

@pytest.fixture
def queue(current_app):
    return current_app.queue

@pytest.fixture
def client(current_app):
    return current_app.test_client()
