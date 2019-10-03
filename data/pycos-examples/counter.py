import sys
import pycos
import pycos.netpycos

from my_ip import MY_IP

# sched = pycos.Pycos.instance(node=MY_IP)
sched = pycos.Pycos.instance()
channel = pycos.Channel('counter')

def server_proc(task=None):
    task.set_daemon()
    channel.register()
    i = 0
    while True:
        channel.send(i)
        yield task.sleep(1)
        i += 1

server = pycos.Task(server_proc)
while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'quit' or cmd == 'exit':
        break
