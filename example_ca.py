from ControlApplication import ControlApplication
ca = ControlApplication(('localhost', 10002), 'control_application','Password')
ca.start()