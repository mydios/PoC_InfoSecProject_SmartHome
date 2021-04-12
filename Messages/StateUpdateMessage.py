class StateUpdateMessage(object):
    #SENT FROM DEVICE TO CONTROL PLATFORM
    #SENT FROM CONTROL PLATFORM TO CONTROL APPLICATION

    def __init__(self, device_name, device_states):
        self.device_name = device_name
        self.device_states = device_states
    
    def __str__(self):
        return type(self).__name__ + '|' + 'DEVICE_NAME=' + self.device_name + '|' + 'NEW_STATE=' + str(self.device_states)
    
    def __repr__(self):
        return self.__str__()