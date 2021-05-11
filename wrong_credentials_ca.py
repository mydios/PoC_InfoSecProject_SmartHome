# network.py, example_cp.py and example_lamp.py should be activated when running this test
from ControlApplication import ControlApplication

# try to register with wrong credentials
ca_wrong_pass = ControlApplication(('localhost', 10004), 'control_application1', '123_pass')
ca_wrong_pass.start()

# example_cp terminal should print two lines, one for each mistake
# lamp should have state 'OFF' (unchanged)