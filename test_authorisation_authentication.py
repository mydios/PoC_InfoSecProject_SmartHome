# network.py, example_cp.py and example_lamp.py should be activated when running this test
from ControlApplication import ControlApplication

# try to register with wrong credentials
ca_wrong_pass = ControlApplication(('localhost', 10004), 'control_application', '123_pass')
ca_wrong_pass._register()

# try to access lamp with unauthorised control application
ca_guest = ControlApplication(('localhost', 10005), 'control_application', 'Password', 'guest')
ca_guest._register()
ca_guest.command_device("lamp", "state", "1")

# example_cp terminal should print two lines, one for each mistake
# lamp should have state 'OFF' (unchanged)