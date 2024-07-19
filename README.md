# yuki_queue
A tiny but powerful distributed task queue for python.  

# Install
```
pip install yuki_queue
```

# Examples
Worker: get job from Master and handle it, then send result to master:   
```python
from yuki_queue.managers import Worker
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()

    worker = Worker(host='127.0.0.1',
                    port=5000,
                    authkey=b'abc')
    worker.run(apply_f=lambda n:n*n)
```
Master: push the job into the queue and wait for the worker's execution result:   
```python
from yuki_queue.managers import Master
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    
    master = Master(host='127.0.0.1', 
                    port=5000, 
                    authkey=b'abc')
    master.run(jobs=[i for i in range(10)], timeout=5)
    print(master.finished) # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
