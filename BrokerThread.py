import threading

class BrokerThread(threading.Thread):
    def __init__(self, mq, lt):
        super().__init__(daemon=True)
        self.message_queue = mq
        self.listener_threads = lt
    
    def run(self):
        while True:
            tpl = self.message_queue.get() #(sender_name, message, destination_name)
            c = self.get_connection(tpl[2])
            if c == "no_connection":
                self.message_queue.put(tpl)
            else:
                c.send(tpl)

    
    def get_connection(self, dst):
        for t in self.listener_threads:
            if t.name == dst:
                return t.connection
        return "no_connection"