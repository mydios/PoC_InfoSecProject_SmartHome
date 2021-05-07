from threading import Thread
from Messages.KServiceRequestMessage import KServiceRequestMessage

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
            
            ###########

            elif isinstance(message, ServiceCommandMessage):
                tpl = self.service.receive_message()
                message = tpl[1]
                if isinstance(message, ServiceCommandMessage):
                    self.service.return_service(message.commander)
            
            else:
                print("Urecognized message received at " +
                      self.service.name+": "+str(message))