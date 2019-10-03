import sys
import pycos
import pycos.netpycos

from my_ip import MY_IP

# sched = pycos.Pycos.instance(node=MY_IP) #, udp_port=9706, tcp_port=9706)
sched = pycos.Pycos.instance()

def main_proc(task=None):
    task.set_daemon()
    chan = yield pycos.Channel.locate('timeserver')
    print(f'Located {chan}')
    yield chan.subscribe(task)
    while True:
        msg = yield task.receive()
        print(f'received {msg}')
    
pycos.Task(main_proc)
while True:
    cmd = sys.stdin.readline().strip().lower()
    if cmd == 'quit' or cmd == 'exit':
        break
