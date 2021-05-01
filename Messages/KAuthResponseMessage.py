class KAuthResponseMessage(object):
    #SENT FROM KERBEROS AUTHENTICATION SERVER TO CONTROL APPLICATION

    def __init__(self, client_realm, client_id, tgt, session_data):
        # string
        self.client_realm = client_realm
        # int
        self.client_id = client_id
        # encrypted data
        self.tgt = tgt
        # encrypted data
        self.session_data = session_data
    
    def __str__(self):
        return type(self).__name__ + '|' + 'CLIENT_REALM=' + self.client_realm + '|' + 'CLIENT_ID=' + str(self.client_id) + '|' + 'TGT=' + str(self.tgt) + '|' + 'SESSION_DATA=' + str(self.session_data)  
    
    def __repr__(self):
        return self.__str__()