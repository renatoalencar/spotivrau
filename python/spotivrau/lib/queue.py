import json


class Serializer:
    def serialize(self, data):
        return json.dumps(data).encode('utf-8')

    def parse(self, data):
        return json.loads(data)


class Queue:
    serializer = Serializer

    def __init__(self, app):
        self.serializer = self.serializer()

        self.app = app
        app.queue = self

    def enqueue(self, name, data):
        self.connection.rpush(name, self.serializer.serialize(data))

    def unqueue(self, name):
        key, data = self.connection.blpop(name)

        return self.serializer.parse(data)

    def set_connection(self, connection):
        self.connection = connection

    def _pop_has(self, name, data):
        message = self.connection.lpop(name)

        return self.serializer.serialize(data) == message
