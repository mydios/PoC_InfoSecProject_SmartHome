class StateUpdateMessage(object):
    #SENT FROM DEVICE TO CONTROL PLATFORM

    def __init__(self, device_states):
        self.device_states = device_states
    
    def __str__(self):
        return type(self).__name__ + '|' + 'NEW_STATE=' + str(self.device_states)