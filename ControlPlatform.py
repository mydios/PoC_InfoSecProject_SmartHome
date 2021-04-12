from CommunicationInterface import CommunicationInterface

class ControlPlatform(CommunicationInterface):
    def __init__(self, addr, name, pw='strong_password'):
        super().__init__(addr, name, pw, encryption_type="conrol_platform", encryption_args=[])
        