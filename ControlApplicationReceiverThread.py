from threading import Thread
from Messages.StateUpdateMessage import StateUpdateMessage
from Messages.KAuthResponseMessage import KAuthResponseMessage
from Messages.KTicketResponseMessage import KTicketResponseMessage
from Messages.KServiceResponseMessage import KServiceResponseMessage
from Messages.TLSMessage import *


class ControlApplicationReceiverThread(Thread):
    """
    Initialization requires:
        - ca =      ControlAplication instance
                    The ControlApplication instance for which this thread is performing the receive functionality
    """

    def __init__(self, ca):
        super().__init__(daemon=True)
        self.control_application = ca

    def run(self):
        while True:

            tpl = self.control_application.receive_message()
            message = tpl[1]

            if isinstance(message, StateUpdateMessage):
                self.control_application.update_device_state(
                    message.device_name, message.device_states)
            
            # Kerberos
            ###########
            
            elif isinstance(message, KAuthResponseMessage):
                if message.client_id == self.control_application.client_id: # check client id
                    self.control_application.handle_auth_response(message)
            
            elif isinstance(message, KTicketResponseMessage):
                if message.client_id == self.control_application.client_id: # check client id
                    self.control_application.handle_ticket_response(message)
            
            elif isinstance(message, KServiceResponseMessage):
                self.control_application.handle_service_response(message)
            ###########

            #TLS    
            elif isinstance(message, TLSMessage):
                if message.type == CLIENT_HELLO:
                    self.control_application.receive_client_hello(message)
                if message.type == SERVER_HELLO:
                    self.control_application.receive_server_hello(message)
                if message.type == FINISH_S:
                    self.control_application.receive_finish_server(message)
                if message.type == FINISH_C:
                    self.control_application.receive_finish_client(message)
                