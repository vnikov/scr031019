import sys
import time
import pycos
import pycos.netpycos

from my_ip import MY_IP

# sched = pycos.Pycos.instance(node=MY_IP)
sched = pycos.Pycos.instance()
channel = pycos.Channel('timeserver')

def server_proc(task=None):
    task.set_daemon()
    channel.register()
    while True:
        channel.send(time.ctime())
        yield task.sleep(1)

server = pycos.Task(server_proc)
while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'quit' or cmd == 'exit':
        break
