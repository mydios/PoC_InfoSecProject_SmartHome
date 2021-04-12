from CommunicationInterface import CommunicationInterface
from Messages.RegisterControlApplicationMessage import RegisterControlApplicationMessage


class ControlApplication(CommunicationInterface):
    def __init__(self, addr, name, control_platform_name="control_platform", pw='strong_password', encryption_type="no_encryption", encryption_args=[]):
        super().__init__(addr, name, pw, encryption_type, encryption_args)
        self.control_name = control_platform_name
        # add shit
        self.devices_information = {}
        self.

    def _register(self):
        """
        This function sends the enregistrement message to the ControlPlatform instance that this ControlApplication instance
        is registered with. The message contains all necessary information for the ControlPlatform and the ControlApplication
        to communicate in the future.
        """
        # THE ENCRYPTION SUPPORTED BY THIS DEVICE IS INCORPORATED IN THE REGISTER MESSAGE
        content = RegisterControlApplicationMessage(
            self.name, self.encryption_type, self.encryption_args)
        self.post_message(message=content, destination=self.control_name)
    
    def 
