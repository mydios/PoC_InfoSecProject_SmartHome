from threading import Thread
from Messages.KAuthRequestMessage import KAuthRequestMessage

class KAuthServerReceiverThread(Thread):
    """
    
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

            else:
                print("Urecognized message received at " +
                      self.auth_server.name+": "+str(message))