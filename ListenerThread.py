import threading

class ListenerThread(threading.Thread):
    def __init__(self, l, mq, n, h):
        super().__init__(daemon=True)
        self.message_queue = mq
        self.listener = l
        self.name = n
        self.connection = None
        self.history = h
    
    def run(self):
        self.connection = self.listener.accept()

        #first communication is identification to broker
        tpl = self.connection.recv() #(sender_name, message, destination_name)
        client_name = tpl[1]
        self.name = client_name

        while (True):
            m = self.connection.recv()
            self.message_queue.put(m)
            self.history.append(m)