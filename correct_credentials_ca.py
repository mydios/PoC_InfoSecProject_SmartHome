# network.py, example_cp.py and example_lamp.py should be activated when running this test
from ControlApplication import ControlApplication


# try to access lamp with unauthorised control application
ca_guest = ControlApplication(('localhost', 10005), 'control_application2', 'Password', 'guest')
ca_guest.start()
ca_guest.command_device("lamp", "state", "1")
