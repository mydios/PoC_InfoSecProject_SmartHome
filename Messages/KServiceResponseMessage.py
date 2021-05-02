class KServiceResponseMessage(object):
    #SENT FROM SERVICE TO CONTROL APPLICATION
    #slide 27 (V --> C)

    def __init__(self, auth_data):
        # encrypted data
        self.auth_data = auth_data
    
    def __str__(self):
        return type(self).__name__ + '|' + 'AUTH_DATA=' + str(self.auth_data)
    
    def __repr__(self):
        return self.__str__()