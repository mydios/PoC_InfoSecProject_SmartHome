#A network.py and example_as.py process should be activated when running this test
import time
from ControlApplication import ControlApplication
from Messages.KAuthRequestMessage import KAuthRequestMessage

ca = ControlApplication(('localhost', 10002), 'control_application')
time.sleep(0.5)

ca.nonce = ca.generate_nonce()

request = KAuthRequestMessage(options='', client_id=ca.client_id, client_realm='', tgs_id=ca.tgs_id, times='', nonce=ca.nonce)
ca.post_message(request, 'k_auth_server')

ca.start()