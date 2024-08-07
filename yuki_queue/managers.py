from time import sleep
from multiprocessing.managers import BaseManager
from typing import Callable, TypeVar
import queue
import logging

Any = TypeVar('Any') # Can be anything

class QueueManager(BaseManager):
    pass
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(name)s]: %(message)s')
log = logging.getLogger("yuki_queue")
show_log = False

def _debug_log(msg):
    if show_log:
        log.info(msg)

job_q = queue.Queue()
result_q = queue.Queue()

def get_job_q(): return job_q

def get_result_q(): return result_q

class Master:
    def __init__(self, host, port, authkey):
        QueueManager.register('get_job_q', callable=get_job_q)
        QueueManager.register('get_result_q', callable=get_result_q)

        self.manager = QueueManager(address=(host, port), authkey=authkey)

    def get_finished(self, _result_q):
        while True:
            try:
                yield _result_q.get_nowait()
            except queue.Empty:
                break
            else:
                self.items -= 1

    def run(self, jobs, timeout=10):
        self.manager.start()
        
        _job_q = self.manager.get_job_q()
        _result_q = self.manager.get_result_q()
        
        for job in jobs:
            _debug_log(f"Put job {job} ...")
            _job_q.put(job)

        self.items = len(jobs)
        self.finished = []
        
        _debug_log("Try get result...")
        
        while True:
            if self.items == 0:
                break
            for result in self.get_finished(_result_q):
                _debug_log("Get a result %s" % result)
                self.finished.append(result)
            sleep(timeout)
        
        _debug_log("All finished, cool!!!")
        self.manager.shutdown()

class Worker:
    def __init__(self, host, port, authkey, max_attempts=3, conn_interval=30):
        QueueManager.register('get_job_q')
        QueueManager.register('get_result_q')
        self.manager = QueueManager(address=(host, port), authkey=authkey)
        self.try_connect(max_attempts=max_attempts, conn_interval=conn_interval)

    def try_connect(self, max_attempts, conn_interval):
        if max_attempts != None:
            max_attempts = max(1, max_attempts)
        
        while True:
            try:
                self.manager.connect()
            except ConnectionError as e:
                if max_attempts == 0:
                    raise e
                elif max_attempts == None:
                    pass
                else:
                    log.info("Try connect again...")
                    max_attempts -= 1
                    sleep(conn_interval)
            else:
                break

    def run(self, apply_f: Callable[[Any], Any], timeout=1, interval=1):
        task = self.manager.get_job_q()
        result = self.manager.get_result_q()

        while True:
            try:
                n = task.get(timeout=timeout)
                _debug_log(f'Worker: Get {n}')
                res = apply_f(n)
                sleep(interval)
                _debug_log(f"Worker: {n} finished")
                result.put(res)
            except queue.Empty:
                break