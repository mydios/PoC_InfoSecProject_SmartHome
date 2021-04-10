from multiprocessing.connection import Listener
from queue import Queue

from ListenerThread import ListenerThread
from BrokerThread import BrokerThread

class Broker(object):
    def __init__(self):
         addresses = [('localhost', 10000+i) for i in range(10)]
         self.listeners = [Listener(addresses[i], authkey=('strong_password'.encode())) for i in range(len(addresses))]
         self.message_queue = Queue()
         self.history = []
         self.threads = [ListenerThread(self.listeners[i], self.message_queue, None, self.history) for i in range(len(self.listeners))]
         self.thread = BrokerThread(self.message_queue, self.threads)

    def start(self):
        for t in self.threads:
            t.start()
        self.thread.start()
        while True:
            u_in = input('')
            if u_in == 'print_messages':
                print("SENDER|MESSAGE|DESTINATION")
                for m in self.history:
                    print(m)