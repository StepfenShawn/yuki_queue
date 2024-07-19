from yuki_queue.managers import Master
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    
    master = Master(host='127.0.0.1', 
                    port=5000, 
                    authkey=b'abc')
    master.run(jobs=[i for i in range(10)])
