import threading
from datetime import datetime

class ListenerThread(threading.Thread):
    """
    Initialization requires:
        - l =      Listener instance

        - mq =     Queue instance from queue library
                    All incomming messages are inserted into this queue so that they can be routed by
                    the BrokerThread thread of the Broker instance
        
        - n =       str
                    Name used for communication by the process corresponding to this listener.
        
        - h =       list
                    History list of all messages that is maintained by the Broker instance.
        
        - st =      datetime.datetime.timestamp 
                    A timestamp of the zero time point to be able to order messages chronologically

    """
    def __init__(self, l, mq, n, h, st):
        super().__init__(daemon=True)
        self.message_queue = mq
        self.listener = l
        self.name = n
        self.connection = None
        self.history = h
        self.start_time = st
    
    def run(self):
        self.connection = self.listener.accept()

        #first communication of a process is always identification to broker
        #initialized name is always overwritten by the name communicated by the corresponding process
        tpl = self.connection.recv() #(sender_name, sender_name, destination_name) = (string, string, None)
        client_name = tpl[1]
        self.name = client_name

        while (True):
            #BLOCKS UNTIL SOMETHING IS RECEIVED
            m = self.connection.recv()
            #NOTIFY BROKER
            self.message_queue.put(m)
            #UPDATE HISTORY
            timestamp = datetime.timestamp(datetime.now())
            mcopy = list(m)
            mcopy.append(timestamp - self.start_time)
            mcopy = tuple(mcopy)
            self.history.append(mcopy)
