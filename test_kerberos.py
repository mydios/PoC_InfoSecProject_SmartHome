#A network.py, example_as.py and example_tgs.py process should be activated when running this test
import time
from ControlApplication import ControlApplication

ca = ControlApplication(('localhost', 10002), 'control_application')
time.sleep(0.5)

ca.init_auth_request()
ca.start()