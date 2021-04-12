from SmartDevice import SmartDevice
d = SmartDevice(('localhost', 10003), 'lamp', {'state': [(1, "ON"), (False, "OFF")], 'color': [
                (0, "WHITE"), (1, "RED"), (2, "GREEN")]}, {'state': (0, "OFF"), 'color': (1, "RED")}, "control_platform")
d.start()