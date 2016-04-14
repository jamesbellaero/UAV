from socket import socket, SOCK_DGRAM, SOCK_STREAM
from threading import Thread

IP_POLO = 'TODO: get ip of polo'

IN_PORT = 25000
OUT_PORT = 25001

class BaseClient(object):

    def __init__(self, ip, port, tcp = True):

        self.socket = socket(socket.AF_INET,
                socket.SOCK_STREAM if tcp else socket.SOCK_DGRAM)
                
        self.socket.connect((ip, port))

    def receive(self, length):

        self.socket.recv(length)

    def send(self, message):

        self.socket.send(message)

    def close(self):

        self.socket.close()

class IncomingClient(BaseClient):

    def __init__(self, plane):

        super(IncomingClient, self).__init__(IP_POLO, IN_PORT)
        
        self.plane = plane

        in_thread = Thread(target = receive_messages)
        in_thread.start()

    def receive_initial_messages():
    
        # TODO

    def receive_messages():

        in_initial = Thread(target = recieve_initial_messages)
        in_initial.start()
        in_initial.join()

        # TODO

class OutgoingClient(BaseClient):
    
    def __init__(self, plane):
        
        super(OutgoingClient, self).__init__(IP_POLO, OUT_PORT)
        
        self.plane = plane
        
        in_thread = Thread(target = send_messages)
        in_thread.start()
    
    def send_initial_messages():
    
        # TODO
    
    def send_messages():
        
        in_initial = Thread(target = send_initial_messages)
        in_initial.start()
        in_initial.join()

        # TODO
