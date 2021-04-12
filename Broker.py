from multiprocessing.connection import Listener
from queue import Queue
from datetime import datetime

from ListenerThread import ListenerThread
from BrokerThread import BrokerThread

class Broker(object):
    """
        A Broker instance is a class that manages a collection of Listener class instances of the multiprocessing library
        and routes any communication between the processes connected to these listeners. This class thus manages all server-side
        functionality of the inter-process communication. Its initialization requires:

            - startportnr =         int
                                    The starting portnumber to be used to create the Listener instances.
                        
            - n_listeners =         int
                                    The number of Listener instances to be initialized and thus ports to be assigned.

        Because this class supports user input via the command console, this class uses a threads to mangage the 
        server-side functionality of the inter-process communication. These threads are instances of the BrokerThread and 
        ListenerThread classes.
    """
    def __init__(self, startportnr=10000, n_listeners = 10):
        #CHOOSE A NUMBER OF PORTS FOR COMMUNICATION
         addresses = [('localhost', startportnr+i) for i in range(n_listeners)]
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
            print("")
            u_in = input('')

            # CLEAR THE CONSOLE
            if u_in == 'clear':
                try:
                    os.system('clear')
                    continue
                except:
                    pass
            
            # SHUT DOWN THE DEVICE
            if u_in == 'exit':
                exit()
            
            # PRINT A HISTORY OF ALL MESSAGES ROUTED
            if u_in == 'print_messages':
                print("SENDER|MESSAGE|DESTINATION|TIMESTAMP")
                for m in self.history:
                    print(m)
                continue
            
            print("Unrecognized command")
            