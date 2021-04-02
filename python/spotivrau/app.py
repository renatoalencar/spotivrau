from flask import Flask
from .queue import Queue

app = Flask(__name__)
queue = Queue(app)

import spotivrau.views

def setup_app():
    import mongoengine
    import redis

    import spotivrau.commands

    app.config['UPLOAD_FOLDER'] = '/tmp'
    app.config['MONGO_CONNECTION_URI'] = 'mongodb://root:spotivrau@localhost/spotivrau?authSource=admin'
    app.config['REDIS_CONNECTION_URI'] = 'redis://localhost/0'

    mongoengine.connect(host=app.config['MONGO_CONNECTION_URI'])
    redis_connection = redis.Redis.from_url(app.config['REDIS_CONNECTION_URI'])

    app.queue.set_connection(redis_connection)

    return app
