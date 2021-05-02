class KServiceRequestMessage(object):
    #SENT FROM CONTROL APPLICATION TO SERVICE

    def __init__(self, options, sgt, auth_data):
        # string
        self.options = options
        # encrypted data
        self.sgt = sgt
        # encrypted data
        self.auth_data = auth_data
    
    def __str__(self):
        return type(self).__name__ + '|' + 'OPTIONS=' + self.options + '|' + 'SGT=' + self.sgt + '|' + 'AUTH_DATA=' + self.auth_data
    
    def __repr__(self):
        return self.__str__()