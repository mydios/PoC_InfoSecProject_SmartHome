#A network.py, example_as.py, example_tgs.py and example_photos.py process should be activated when running this test
import time
from ControlApplication import ControlApplication

ca = ControlApplication(('localhost', 10002), 'control_application', 'Password')
time.sleep(0.5)

ca.start()