from multiprocessing.connection import Client
from Messages.TLSMessage import *
import uuid
import nacl.utils
from nacl.public import PrivateKey, Box
import pickle

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

        #DO WE WANT TLS
        self.tls = True

        #Keep track of TLS connections
        self.tls_connections = {self.name: True}

        #Generate public and private keys
        self.secret_key = PrivateKey.generate()

        #While setting up TLS, keep track of the message to sent
        self.to_send = dict()
        self.send_pending = False


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

        if destination not in self.tls_connections and destination is not None:
            self.to_send = {"message":message, "destination": destination}
            self.send_pending = True
            return self.setup_tls_connection(destination)
        if not isinstance(message, TLSMessage) and destination is not None:
            while not self.tls_connections[destination]["ready"]:
                pass

        message = self._encrypt(
            message, destination)
        self.client.send((self.name, message, destination))

    def receive_message(self):
        # RECIEVE A MESSAGE
        message = self.client.recv()
        # Decryption is performed using decryption factory function _decrypt
        source = message[0] if self.tls else None
        message = self._decrypt(
            message, source)
        return message

    def generate_nonce(self):
        # https://stackoverflow.com/questions/5590170/what-is-the-standard-method-for-generating-a-nonce-in-python
        return uuid.uuid4().hex
    
        


    def setup_tls_connection(self, destination):
        #The connection is now added to the dict but won't be True before the handshake is finished.
        self.tls_connections[destination] = {"public_key":None, "ready":False}
        client_hello = TLSMessage(**{"type": CLIENT_HELLO,
                                    "source" : self.name,
                                    "client_random_data": self.generate_nonce(),
                                    "cipher_suites": ["TLS_AES_128_GCM_SHA256"],
                                    "public_key": self.secret_key.public_key,
                                    "supported_versions": [3.1]})
        self.post_message(client_hello, destination)
        print("CLIENT_HELLO SENT")

    def receive_client_hello(self, message):
        self.tls_connections[message.source] = {"public_key": message.public_key, "ready": False, "box":Box(self.secret_key, message.public_key)}
        print(f'Client has shared secret: {self.tls_connections[message.source]["box"].shared_key()}')

        print("CLIENT_HELLO RECEIVED")
        self.send_server_hello(message)

    def send_server_hello(self, client_message):
        client_random_data = client_message.client_random_data
        cipher_suites = client_message.cipher_suites
        client_public_key = client_message.public_key
        supported_versions = client_message.supported_versions

        chosen_version = supported_versions[0]
        selected_cipher = cipher_suites[0]
        server_random_data = self.generate_nonce()
        server_hello = TLSMessage(**{"type": SERVER_HELLO,
                                    "source": self.name,
                                    "server_random_data": server_random_data,
                                    "public_key": self.secret_key.public_key,
                                    "chosen_version": chosen_version,
                                    "selected_cipher": selected_cipher})
        self.post_message(server_hello, client_message.source)
        print("SERVER HELLO")
        self.send_encrypted_extensions(client_message.source)
    def receive_server_hello(self, message):
        self.tls_connections[message.source]["public_key"] = message.public_key
        self.tls_connections[message.source]["box"] = Box(self.secret_key, message.public_key)
        print(f'Server has shared secret: {self.tls_connections[message.source]["box"].shared_key()}')

    def send_encrypted_extensions(self, destination):
        data = b"THIS IS THE DATA THAT IS MEANT FOR THIS MESSAGE"
        encrypted_data = self.tls_connections[destination]["box"].encrypt(data)
        message = TLSMessage(**{"type": ENCRYPTED_EXTENSIONS,
                                "source": self.name,
                                "encrypted_data": encrypted_data})
        self.post_message(message, destination)
        print("ENCRYPTED EXTENSIONS SENT")
        self.send_certificate_request(destination)
    def send_certificate_request(self, destination):
        data = b"THIS IS A HUMBLE REQUEST FOR YOUR CERTIFICATE"
        encrypted_data = self.tls_connections[destination]["box"].encrypt(data)
        message = TLSMessage(**{"type": CERTIFICATE_REQUEST,
                                "source": self.name,
                                "encrypted_data": encrypted_data})
        self.post_message(message, destination)
        print("CERTIFICATE REQUEST SENT")
        self.send_certificate(destination)
    def send_certificate(self, destination, server_sending=True):
        if self.tls_connections[destination]["ready"]:
            return
        data = b"THIS IS MY VERY TRUSTWORTHY CERTIFICATE"
        encrypted_data = self.tls_connections[destination]["box"].encrypt(data)
        message = TLSMessage(**{"type": CERTIFICATE,
                                "source": self.name,
                                "encrypted_data": encrypted_data})
        self.post_message(message, destination)
        print("CERTIFICATE SENT")
        self.send_certificate_verify(destination, server_sending)

    def send_certificate_verify(self, destination, server_sending):
        data = b"THIS IS MY VERY TRUSTWORTHY CERTIFICATE VERIFY MESSAGE"
        encrypted_data = self.tls_connections[destination]["box"].encrypt(data)
        message = TLSMessage(**{"type": CERTIFICATE_VERIFY,
                                "source": self.name,
                                "encrypted_data": encrypted_data})
        self.post_message(message, destination)
        print("CERTIFICATE VERIFY SENT")
        self.send_finish(destination, server_sending)

    def send_finish(self, destination, server_sending):            
        data = b"THE END OF MY PART OF THE HANDSHAKE"
        encrypted_data = self.tls_connections[destination]["box"].encrypt(data)
        message = TLSMessage(**{"type": FINISH_S if server_sending else FINISH_C,
                                "source": self.name,
                                "encrypted_data": encrypted_data})
        self.post_message(message, destination)
        print("FINISH SENT")

    def receive_finish_server(self, message):
        print("SERVER HELLO RECEIVED")
        print("ENCRYPTED EXTENSIONS RECEIVED")
        print("CERTIFICATE REQUEST RECEIVED")
        print("CERTIFICATE RECEIVED")
        print("CERTIFICATE VERIFY RECEIVED")
        print("FINISH RECEIVED")
        self.send_certificate(message.source, server_sending=False)
        self.tls_connections[message.source]["ready"] = True
        self.post_message(self.to_send["message"], self.to_send["destination"])
    def receive_finish_client(self, message):        
        print("CERTIFICATE RECEIVED")
        print("CERTIFICATE VERIFY RECEIVED")
        print("FINISH RECEIVED")        
        self.tls_connections[message.source]["ready"] = True




    def _encrypt(self, message, destination):
        """
        This function encrypts all messages that are sent out from this CommunicationInterface class.
        """
        if destination in self.tls_connections and self.tls_connections[destination]["ready"]:
            message = pickle.dumps(message)
            encrypted_message = self.tls_connections[destination]["box"].encrypt(message)
            tls_message = TLSMessage(**{"type":ENCRYPTED_DATA, "source":self.name,"encrypted_data":encrypted_message})
            return tls_message

        #ENCRYPT A MESSAGE
        if self.encryption_type == "no_encryption":
            return message
        # ...
        # if tself.encryption_typeype == "RSA":
        # ...
        return message

    def _decrypt(self, message, source):
        """
        This function decrypts all messages that are received by this CommunicationInterface class.
        """
        if (source in self.tls_connections) and self.tls_connections[source]["ready"]:
            print(message)
            encrypted_message = message[1].encrypted_data
            decrypted_message = self.tls_connections[source]["box"].decrypt(encrypted_message)
            message = (message[0], pickle.loads(decrypted_message), message[2])
            print(message)
            return message

        #DECRYPT A MESSAGE
        if self.encryption_type == "no_encryption":
            return message
        # ...
        # if tself.encryption_typeype == "RSA":
        # ...
        return message
