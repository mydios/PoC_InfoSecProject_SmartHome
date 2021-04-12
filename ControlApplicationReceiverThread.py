from threading import Thread
from Messages.StateUpdateMessage import StateUpdateMessage


class ControlApplicationReceiverThread(Thread):
    """
    Initialization requires:
        - ca =      ControlAplication instance
                    The ControlApplication instance for which this thread is performing the receive functionality
    """

    def __init__(self, ca):
        super().__init__(daemon=True)
        self.conrol_application = ca

    def run(self):
        while True:

            tpl = self.conrol_application.receive_message()
            message = tpl[1]

            if isinstance(message, StateUpdateMessage):
                self.conrol_application.update_device_state(
                    message.device_name, message.device_states)
