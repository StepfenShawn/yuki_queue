from time import sleep
from multiprocessing.managers import BaseManager
import logging
import queue

class QueueManager(BaseManager):
    pass

class Const:
    def __init__(self, v):
        self.v = v
    
    def set(self, v):
        self.v = v

debug = False

job_q = queue.Queue()
result_q = queue.Queue()
close_q = Const(False)

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

    def close_job_q():
        pass

    def run(self, jobs, timeout=10):
        self.manager.start()
        
        _job_q = self.manager.get_job_q()
        _result_q = self.manager.get_result_q()
        
        for job in jobs:
            print(f"Put job {job} ...")
            _job_q.put(job)

        self.items = len(jobs)
        
        print("Try get result...")

        while True:
            if self.items == 0:
                break
            for result in self.get_finished(_result_q):
                print(result)
        
        self.manager.shutdown()

class Worker:
    def __init__(self, host, port, authkey):
        QueueManager.register('get_job_q')
        QueueManager.register('get_result_q')
        self.manager = QueueManager(address=(host, port), authkey=authkey)
        self.manager.connect()

    def run(self, handler, timeout=1):
        task = self.manager.get_job_q()
        result = self.manager.get_result_q()

        while True:
            try:
                n = task.get(timeout=timeout)
                handler(n)
                sleep(timeout)
                result.put(n)
            except queue.Empty:
                break
        self.manager.shutdown()