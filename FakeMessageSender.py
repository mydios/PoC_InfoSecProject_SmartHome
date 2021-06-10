from Messages.TLSMessage import TLSMessage
from CommunicationInterface import CommunicationInterface
class FakeMessageSender(CommunicationInterface):
    def __init__(self, source, message, destination):
        super().__init__(('localhost', 10009), source)
        self.source = source
        m = TLSMessage(source=source, type=8, encrypted_data=message)
        self.tls = False
        self.send_fake_message(m, destination)

    def send_fake_message(self, message, destination):
        m = TLSMessage(source=self.source, type=8, encrypted_data=message)
        self.post_message(m, destination)