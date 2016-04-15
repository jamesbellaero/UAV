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

        message_count = 0

    def receive(self, length):

        message = self.socket.recv(length)

        if (message):
            message_count += 1

        if (message_count % 10 == 0):
            send('ping', 4)

        return message

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

        in_thread = Thread(target = _process_messages)
        in_thread.start()

    def _process_initial_messages(self):
    
        # TODO

    def _process_messages(self):

        in_initial = Thread(target = _process_initial_messages)
        in_initial.start()
        in_initial.join()

        while (not self.closed):

            # TODO

class OutgoingClient(BaseClient):
    
    def __init__(self, plane):
        
        super(OutgoingClient, self).__init__(IP_POLO, OUT_PORT)

        self.plane = plane
        self.can_send = False

        out_thread = Thread(target = _send_messages)
        out_thread.start()
    
    def _send_initial_message(self):
    
        home_loc = self.plane.home_loc

        string = '%12.9f%12.9f%8.2f' % (home_loc.lat, home_loc.lon, home_loc.alt)
        send(string, 32)
    
    def _send_messages(self):
        
        out_initial_thread = Thread(target = _send_initial_message)
        out_initial_thread.start()
        out_initial.join()

        sending_waypoints = False
        sending_position = False

        @self.plane.vehicle.on_attribute('commands')
        def send_waypoints(self, name, value):

            # TODO get the waypoints here

            count_string = 'w' + 'TODO'
            waypoint_string = 'TODO'

            while (sending_position):

                sleep(0.001)

            sending_waypoints = True

            send(count_string, 8)
            send(waypoint_string, 'TODO: find length')

            sending_waypoints = False

        while (not self.closed):
    
            if (self.can_send):

                # Gather position data

                time_string = 't' + 'TODO'
                position_string = 'TODO'

                sending_list.extend((time_string, position_string))

                while (not sending_waypoints and not sending_list):

                    sending_position = True

                    sending_message = sending_list.pop(0)
                    send(sending_message, 8 if sending_message[0] == 't' else 'TODO: len')

                sending_position = False

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
    