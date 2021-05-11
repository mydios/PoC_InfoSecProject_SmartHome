from threading import Thread
from Messages.KTicketRequestMessage import KTicketRequestMessage
from Messages.TLSMessage import *

class KTicketGServerReceiverThread(Thread):
    """
    Receiver thread of the Kerberos Ticket-Granting Server.
    """
    def __init__(self, ticket_server):
        super().__init__(daemon=True)
        self.ticket_server = ticket_server

    def run(self):
        while True:

            tpl = self.ticket_server.receive_message()
            sender, message = tpl[0], tpl[1]

            if isinstance(message, KTicketRequestMessage):
                self.ticket_server.handle_ticket_request(sender, message)
            elif isinstance(message, TLSMessage):
                if message.type == CLIENT_HELLO:
                    self.ticket_server.receive_client_hello(message)
                if message.type == SERVER_HELLO:
                    self.ticket_server.receive_server_hello(message)
                if message.type == FINISH_S:
                    self.ticket_server.receive_finish_server(message)
                if message.type == FINISH_C:
                    self.ticket_server.receive_finish_client(message)

            else:
                print("Unrecognized message received at " +
                      self.ticket_server.name+": "+str(message))