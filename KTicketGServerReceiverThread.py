from threading import Thread
from Messages.KTicketRequestMessage import KTicketRequestMessage

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

            else:
                print("Urecognized message received at " +
                      self.ticket_server.name+": "+str(message))