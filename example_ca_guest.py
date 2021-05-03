from ControlApplication import ControlApplication
ca = ControlApplication(('localhost', 10005), 'control_application_guest','Password', "guest")
ca.start()