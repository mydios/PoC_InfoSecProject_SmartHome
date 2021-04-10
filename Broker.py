from multiprocessing.connection import Listener
from queue import Queue
from datetime import datetime

from ListenerThread import ListenerThread
from BrokerThread import BrokerThread

class Broker(object):
    def __init__(self):
        #CHOOSE A NUMBER OF PORTS FOR COMMUNICATION
         addresses = [('localhost', 10000+i) for i in range(10)]
         #CREATE A LISTENER FOR EACH PORT
         self.listeners = [Listener(addresses[i], authkey=('strong_password'.encode())) for i in range(len(addresses))]
         #CREATE WORK QUEUE FOR BROKER
         self.message_queue = Queue()
         #CREATE MESSAGE HISTORY
         self.history = []
         #SET ZERO TIMEPOINT
         self.start_time = datetime.timestamp(datetime.now())
         #CREATE A THREAD FOR EACH LISTENER
         self.threads = [ListenerThread(self.listeners[i], self.message_queue, None, self.history, self.start_time) for i in range(len(self.listeners))]
         #CREATE THREAD FOR BROKER ITSELF
         self.thread = BrokerThread(self.message_queue, self.threads)
         

    def start(self):
        #START ALL LISTENER THREADS
        for t in self.threads:
            t.start()
        #START BROKER THREAD
        self.thread.start()
        #POLL FOR USER INPUT
        while True:
            u_in = input('')
            if u_in == 'print_messages':
                print("SENDER|MESSAGE|DESTINATION|TIMESTAMP")
                for m in self.history:
                    print(m)