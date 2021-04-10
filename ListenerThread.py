import threading
from datetime import datetime

class ListenerThread(threading.Thread):
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

        #first communication is identification to broker
        tpl = self.connection.recv() #(sender_name, message, destination_name)
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
