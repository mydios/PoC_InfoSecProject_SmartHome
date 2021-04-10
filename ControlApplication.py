from CommunicationInterface import CommunicationInterface

class ControlApplication(CommunicationInterface):
    def __init__(self, addr, name, pw='strong_password'):
        super().__init__(addr, name, pw)