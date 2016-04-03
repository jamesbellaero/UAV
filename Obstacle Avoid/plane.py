from dronekit import connect

from types.Location import convert_location

from math import tan

class Plane(object):
    
    BANKING_ANGLE = 0.53260
    ACCEL_GRAV = 9.80665
    
    def __init__(self, connection_string='/dev/ttyAMA0', baud_rate=57600):
        
        # TODO: Thread to ask Marco when to connect.
        
        self.vehicle = connect(connection_string, baud = baud_rate, wait_ready=True)

        # TODO: Notify Marco that dronekit as been connected.

        # TODO: Start obstacle avoidance thread.

    @property
    def airspeed(self):
        
        return self.vehicle.airspeed

    @property
    def heading(self):
        
        return self.vehicle.heading

    @property
    def loc(self):
        
        return convert_location(self.vehicle.global_relative_frame)
    
    @property
    def turning_radius(self):
        
        return self.airspeed ** 2 / ACCEL_GRAV / tan(BANKING_ANGLE)