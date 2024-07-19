from yuki_queue.managers import Worker
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()

    worker = Worker(host='127.0.0.1',
                    port=5000,
                    authkey=b'abc')
    worker.run(apply_f=lambda n:n*n)