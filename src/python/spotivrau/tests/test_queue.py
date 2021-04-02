import json
import threading
import time

from redis import Redis

connection = Redis()

def test_queue_push(current_app):
    current_app.queue.enqueue('transcode', id=1337)

    assert current_app.queue._pop_has('transcode', {'id': 1337})


def test_queue_unqueue(current_app):
    def dispatch():
        time.sleep(1)
        current_app.queue.enqueue('transcode', id=1234)

    threading.Thread(target=dispatch).start()
    data = current_app.queue.unqueue('transcode')

    assert data['id'] == 1234
