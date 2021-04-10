#A network.py process should be activated when running this test
import time
from CommunicationInterface import CommunicationInterface

ci0 = CommunicationInterface(('localhost', 10000), name='ci0')
ci1 = CommunicationInterface(('localhost', 10001), name='ci1')
time.sleep(0.5)

ci0.post_message("hey ci1", "ci1")
print("posted message")
m = ci1.receive_message()
print(m)

time.sleep(1200)