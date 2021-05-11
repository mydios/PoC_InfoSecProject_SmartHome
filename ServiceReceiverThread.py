from threading import Thread
from Messages.KServiceRequestMessage import KServiceRequestMessage
from Messages.TLSMessage import *

class ServiceReceiverThread(Thread):
    """
    Receiver thread of a Smart Service.
    """
    def __init__(self, service):
        super().__init__(daemon=True)
        self.service = service

    def run(self):
        while True:

            tpl = self.service.receive_message()
            sender, message = tpl[0], tpl[1]

            # Kerberos
            ###########

            if isinstance(message, KServiceRequestMessage):
                self.service.handle_service_request(sender, message)
            elif isinstance(message, TLSMessage):
                if message.type == CLIENT_HELLO:
                    self.service.receive_client_hello(message)
                if message.type == SERVER_HELLO:
                    self.service.receive_server_hello(message)
                if message.type == FINISH_S:
                    self.service.receive_finish_server(message)
                if message.type == FINISH_C:
                    self.service.receive_finish_client(message)
            
            ###########
            
            else:
                print("Urecognized message received at " +
                      self.service.name+": "+str(message))