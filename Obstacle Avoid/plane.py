from dronekit import connect

from position.Location import from_dronekit_location
from unit_conversions import deg_to_rad
from client import IncomingClient, OutgoingClient

from math import tan

BANKING_ANGLE = 0.53260
ACCEL_GRAV = 9.80665

class Plane(object):
    
    def __init__(self, connection_string='/dev/ttyAMA0', baud_rate=57600):
        
        self.vehicle = connect(connection_string, baud = baud_rate, wait_ready=True)

        self.in_client = IncomingClient(self)
        self.out_client = OutgoingClient(self)
    
        # TODO: Start obstacle avoidance thread.

    @property
    def airspeed(self):
        
        return self.vehicle.airspeed

    @property
    def heading(self):
        
        return deg_to_rad(self.vehicle.heading)

    @property
    def pitch(self):

        return self.vehicle.pitch
    
    @property
    def roll(self):
        
        return self.vehicle.roll

    @property
    def loc(self):
        
        return from_dronekit_location(self.vehicle.global_relative_frame)
    
    @property
    def turning_radius(self):
        
        return self.airspeed ** 2 / ACCEL_GRAV / tan(BANKING_ANGLE)
    
    @property
    def commands(self):
        
        commands = self.vehicle.commands
        
        commands.download()
        commands.wait_ready()

        return commands

    @property
    def home_loc(self):

        commands = self.commands

        return from_dronekit_location(self.vehicle.home_location)

    @property
    def next_wp(self):

        return self.vehicle.next