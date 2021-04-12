from multiprocessing.connection import Client


class CommunicationInterface(object):
    """
    The CommunicationInterface class implements all functionality for client-side communication between processes. 
    It uses the Client class from the multiprocessing library which upon creation connects to a corresponding 
    Listener instance from the multiprocessing library. The Listeners are gathered in the Broker class and thus 
    all classes inheriting the CommunicationInterface class require that a Broker instance with active Listeners
    is already active upon creation. 

    Initialization of a CommunicationInterface class requires:

        - addr =            (str, int)
                            (INET_ADDRESS, PORTNR) e.g. ('localhost', 10000)

        - name =            str
                            Name used for routing. This name is used by both the Broker and other CommunicationInterface
                            to communicate with this process.
        
        - pw =              str
                            A phrase used to ensure that communication between processes is authorized. The multiprocessing
                            library communicates by pickling/unpickling python datatypes which is potentially unsafe without
                            authorization. Therefore both communication sides must know this same assymetric keyphrase to ensure
                            authentication. This is purely for the functioning of the used multiprocessing classes.
        
        - encryption_type   str
                            Specification about which type of encryption this process will use for its messages.
        
        - encryption_args   list
                            A list of arguments/parameters that entail the further details of the encryption functionality


    """
    def __init__(self, addr, name, pw='strong_password', encryption_type = "no_encryption", encryption_args =[]):
        # CREATE CLIENT CONNECTION TO ONE OF THE LISTENERS IN THE BROKER
        # This Client class automatically establishes a connection to a Listener class in the Broker
        self.client = Client(address=addr, authkey=pw.encode())

        # SET NAME FOR COMMUNICATION
        self.name = name
        # SET ENCRYPTION TYPE
        self.encryption_type = encryption_type
        # SET ENCRYPTION ARGS
        self.encryption_args = encryption_args

        # FIRST REGISTER MESSAGE TO BROKER (i.e. broadcast name of this CommunicationInterface instance)
        self.post_message(self.name, None)
        

    def post_message(self, message, destination):
        """
        This function is used to send messages to other processes.
        It takes the follwing arguments:
            - message =         object
                                any picklable python object
            - destination =     str
                                The name of the other CommunicationInterface instance to which the message needs
                                to be sent.
        """
        # SEND A MESSAGE
        # The actual python object sent is a pickled tuple of the form (string, object, string)=(sender_name, message, destination_name)
        # Encryption is performed using encryption factory function _encrypt
        message = self._encrypt(
            message)
        self.client.send((self.name, message, destination))

    def receive_message(self):
        # RECIEVE A MESSAGE
        message = self.client.recv()
        # Decryption is performed using decryption factory function _decrypt
        message = self._decrypt(
            message)
        return message

    def _encrypt(self, message):
        """
        This function encrypts all messages that are sent out from this CommunicationInterface class.
        """
        #ENCRYPT A MESSAGE
        if self.encryption_type == "no_encryption":
            return message
        # ...
        # if tself.encryption_typeype == "RSA":
        # ...
        return message

    def _decrypt(self, message):
        """
        This function decrypts all messages that are received by this CommunicationInterface class.
        """
        #DECRYPT A MESSAGE
        if self.encryption_type == "no_encryption":
            return message
        # ...
        # if tself.encryption_typeype == "RSA":
        # ...
        return message
