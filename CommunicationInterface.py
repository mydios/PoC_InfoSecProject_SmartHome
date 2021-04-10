from multiprocessing.connection import Client
import time


class CommunicationInterface(object):
    def __init__(self, addr, name, pw='strong_password'):
        self.client = Client(address=addr, authkey=pw.encode())
        self.name = name
        #register with broker
        self.post_message(self.name, None)
    
    def post_message(self, message, destination):
        #Messages are pickled tuples of the form (string, object, string)=(sender_name, message, destination_name)
        self.client.send((self.name, message, destination))
    
    def receive_message(self):
        message = self.client.recv()
        return message

"""
ci0 = CommunicationInterface(('localhost', 10000), name='ci0')
ci1 = CommunicationInterface(('localhost', 10001), name='ci1')
time.sleep(0.5)

ci0.post_message("hey ci1", "ci1")
print("posted message")
m = ci1.receive_message()
print(m)

time.sleep(1200)
"""