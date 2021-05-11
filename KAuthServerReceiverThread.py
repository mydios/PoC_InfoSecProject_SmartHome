from threading import Thread
from Messages.KAuthRequestMessage import KAuthRequestMessage
from Messages.TLSMessage import *

class KAuthServerReceiverThread(Thread):
    """
    Receiver thread of the Kerberos Authentication Server.
    """
    def __init__(self, auth_server):
        super().__init__(daemon=True)
        self.auth_server = auth_server

    def run(self):
        while True:

            tpl = self.auth_server.receive_message()
            sender, message = tpl[0], tpl[1]

            if isinstance(message, KAuthRequestMessage):
                self.auth_server.handle_auth_request(sender, message)
            elif isinstance(message, TLSMessage):
                if message.type == CLIENT_HELLO:
                    self.auth_server.receive_client_hello(message)
                if message.type == SERVER_HELLO:
                    self.auth_server.receive_server_hello(message)
                if message.type == FINISH_S:
                    self.auth_server.receive_finish_server(message)   
                if message.type == FINISH_C:
                    self.auth_server.receive_finish_client(message)

            else:
                print("Urecognized message received at " +
                      self.auth_server.name+": "+str(message))