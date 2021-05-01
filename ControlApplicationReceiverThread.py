from threading import Thread
from Messages.StateUpdateMessage import StateUpdateMessage
from Messages.KAuthResponseMessage import KAuthResponseMessage


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

            elif isinstance(message, KAuthResponseMessage):
                if message.client_id == self.control_application.client_id: # check client id
                    self.control_application.handle_auth_response(message)