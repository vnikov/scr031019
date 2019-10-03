import random, sys
import pycos
import pycos.netpycos

from my_ip import MY_IP

def server_proc(task=None):
    task.set_daemon()
    task.register('receiver_task')
    while True:
        msg = yield task.receive()
        print('received %s' % (msg))

# sched = pycos.Pycos.instance(node=MY_IP)
sched = pycos.Pycos.instance()
server = pycos.Task(server_proc)
while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'quit' or cmd == 'exit':
        break
