from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from threading import Thread
from Queue import Queue
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

                send('ping')

        return message

    def send(self, message):

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
        self.queue = Queue

        self.has_started = False
        self.can_send = False

        sending_thread = Thread(target = sending_thread)
        sending_thread.start()

        message_thread = Thread(target = _send_messages)
        message_thread.start()
    
    def _send_initial_message(self):
    
        home_loc = self.plane.home_loc

        string = '%12.8f%12.8f%8.3f' % (home_loc.lat, home_loc.lon, home_loc.alt)
        send(string, 32)
    
    def _send_messages(self):
        
        out_initial_thread = Thread(target = _send_initial_message)
        out_initial_thread.start()
        out_initial.join()

        @self.plane.vehicle.on_attribute('commands')
        def send_waypoints(self_, name, value):

            if (not self.closed):

                # TODO get the waypoints here

                count_string = 'w' + 'TODO'
                waypoint_string = 'TODO'

                queue.add((count_string, 8, waypoint_string, 'TODO: find length'))

        while (not has_started):

            sleep(0.1)

        while (not self.closed):

            next_wp = self.plane.next_wp
            loc = self.plane.loc
            heading = self.plane.heading
            pitch = self.plane.pitch
            roll = self.plane.roll
            #put airspeed

            time_string = 't%7.2f' % self.time
            telemetry_string = '%3.0f%12.8f%12.8f%8.3f%6.3f%7.3f' % (next_wp, loc.lat,
                    loc.lon, loc.alt, heading, pitch, roll)

            queue.add((time_string, 8, telemetry_string, 48))

            sleep(0.1)

    def _sending_thread(self):

        while (not self.closed):

            if (self.can_send):

                messages = queue.get()

                if (len(messages[0]) == messages[1] and len(messages[2]) == messages[3]):

                    send(messages[0])
                    send(messages[2])

                queue.task_done()

    def start_sending(self):

        if (not has_started):

            self.start_time = time()
            has_started = True

        self.can_send = True

    def stop_sending(self):

        self.can_send = False

    @property
    def time(self):

        return time() - self.start_time
    