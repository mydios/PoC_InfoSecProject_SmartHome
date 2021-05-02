class KTicketResponseMessage(object):
    #SENT FROM KERBEROS TICKET-GRANTING SERVER TO CONTROL APPLICATION
    #slide 25 (TGS --> C)

    def __init__(self, client_realm, client_id, sgt, session_data):
        # string
        self.client_realm = client_realm
        # int
        self.client_id = client_id
        # encrypted data
        self.sgt = sgt
        # encrypted data
        self.session_data = session_data
    
    def __str__(self):
        return type(self).__name__ + '|' + 'CLIENT_REALM=' + self.client_realm + '|' + 'CLIENT_ID=' + str(self.client_id) + '|' + 'SGT=' + str(self.sgt) + '|' + 'SESSION_DATA=' + str(self.session_data)  
    
    def __repr__(self):
        return self.__str__()