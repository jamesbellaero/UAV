from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from threading import Thread
from time import time, sleep

IP_POLO = 'TODO: get ip of polo'

IN_PORT = 25000
OUT_PORT = 25001 

class BaseClient(object):

    def __init__(self, ip, port, tcp = True):

        self.socket = socket(AF_INET, SOCK_STREAM if tcp else SOCK_DGRAM)
        self.socket.connect((ip, port))

        self.closed = False

    def receive(self, length):

        return self.socket.recv(length)

    def send(self, message, length):

        if (len(message) == length):
            self.socket.send(message)

    def close(self):

        self.closed = True

        self.socket.close()

class IncomingClient(BaseClient):

    def __init__(self, plane):

        super(IncomingClient, self).__init__(IP_POLO, IN_PORT)
        
        self.plane = plane

        in_thread = Thread(target = process_messages)
        in_thread.start()

    def process_initial_messages(self):
    
        # TODO

    def process_messages(self):

        in_initial = Thread(target = process_initial_messages)
        in_initial.start()
        in_initial.join()

        while (not self.closed):

            # TODO

class OutgoingClient(BaseClient):
    
    def __init__(self, plane):
        
        super(OutgoingClient, self).__init__(IP_POLO, OUT_PORT)

        self.plane = plane
        self.can_send = False

        out_thread = Thread(target = send_messages)
        out_thread.start()
    
    def send_initial_message(self):
    
        home_loc = self.plane.home_loc

        string = '%12.9f%12.9f%8.2f' % (home_loc.lat, home_loc.lon, home_loc.alt)
        send(string, 32)
    
    def send_messages(self):
        
        out_initial_thread = Thread(target = send_initial_message)
        out_initial_thread.start()
        out_initial.join()

        @self.plane.vehicle.on_attribute('commands')
        def send_waypoints(self, name, value):

            # TODO

        while (not self.closed):
    
            if (self.can_send):


                # TODO

            sleep(0.1)

    def start_sending(self):

        if (not 'start_time' in locals()):
            self.start_time = time()

        self.can_send = True

    def stop_sending(self):

        self.can_send = False

    @property
    def time(self):

        return time() - self.start_time
    