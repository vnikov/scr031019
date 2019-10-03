import random
import pycos
import pycos.netpycos

from my_ip import MY_IP

n_producer = 3
msgs_per_producer = 3
sched = pycos.Pycos.instance()
#sched = pycos.Pycos.instance(node=MY_IP)

def main_proc(task=None):
    print('Entering main_proc')
    consumer = yield task.locate('receiver_task')
    print(f'Located {consumer!r}, type {type(consumer)}')
    for i in range(n_producer):
        pycos.Task(producer_proc, consumer, i)


def producer_proc(consumer, i, task=None):
    print('Entering producer_proc')
    for j in range(msgs_per_producer):
        yield task.sleep(random.uniform(0.5, 3))
        msg = f'Message {i}-{j}'
        consumer.send(msg)
    print(f'Producer {i} exiting')
    
pycos.Task(main_proc)

pycos.Pycos().join()
