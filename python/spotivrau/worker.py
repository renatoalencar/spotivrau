import threading

class Worker:
    def __init__(self, queue):
        self.queue = queue
        self.jobs = {}

    def job(self, name):
        def decorator(fn):
            self.create_job(name, fn)

        return decorator

    def create_job(self, name, fn):
        if name not in self.jobs:
            self.jobs[name] = [fn]
        else:
            self.jobs[name].append(fn)

    def process_item(self, name):
        data = self.queue.unqueue(name)

        print(f'Received mesage on queue {name}')

        for fn in self.jobs[name]:
            fn(data)

    def work_loop(self):
        for queue in self.jobs.keys():
            threading.Thread(
                target=self.work_on_queue,
                args=(queue,)
            ).start()

    def work_on_queue(self, name):
        while True:
            self.process_item(name)
