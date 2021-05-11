from threading import Thread
from Messages.RegisterDeviceMessage import RegisterDeviceMessage
from Messages.RegisterControlApplicationMessage import RegisterControlApplicationMessage
from Messages.StateUpdateMessage import StateUpdateMessage
from Messages.DeviceCommandMessage import DeviceCommandMessage
from Messages.TLSMessage import *

class ControlPlatformReceiverThread(Thread):
    """
    Initialization requires:
        - cp =      ConrolPlatform instance
                    The ControlPlatform instance for which this thread is performing the receive functionality
    """

    def __init__(self, cp):
        super().__init__(daemon=True)
        self.control_platform = cp

    def run(self):
        while True:

            tpl = self.control_platform.receive_message()
            message = tpl[1]

            if isinstance(message, RegisterDeviceMessage):
                self.control_platform.register_device(
                    message.device_name, message.command_manual, message.encryption_type, message.encryption_args)

            elif isinstance(message, RegisterControlApplicationMessage):
                self.control_platform.register_control_application(
                    message.application_name, message.credentials, message.authorisation_level, message.encryption_type, message.encryption_args)

            elif isinstance(message, StateUpdateMessage):
                self.control_platform.handle_state_update(message)

            elif isinstance(message, DeviceCommandMessage):
                self.control_platform.handle_device_command(message)
            elif isinstance(message, TLSMessage):
                if message.type == CLIENT_HELLO:
                    self.control_platform.receive_client_hello(message)
                if message.type == SERVER_HELLO:
                    self.control_platform.receive_server_hello(message)
                if message.type == FINISH_S:
                    self.control_platform.receive_finish_server(message)
                if message.type == FINISH_C:
                    self.control_platform.receive_finish_client(message)

            else:
                print("Urecognized message received at " +
                      self.control_platform.name+": "+str(message))
