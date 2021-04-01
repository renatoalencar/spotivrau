from spotivrau.worker import Worker


def test_process_queue(queue):
    worker = Worker(queue)

    args = []

    @worker.job('transcode')
    def transcode(data):
        args.append(data)

    queue.enqueue('transcode', {'id': 1990})
    worker.process_item('transcode')

    assert args[0] == {'id': 1990}
