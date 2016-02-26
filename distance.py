"""Handles computing the distance between two waypoints, with some functions taking in
consideration turning to go to the next waypoint.

Note that distances are in meters and angles are in radians.
"""

from math import sin, cos, tan, sqrt, pi
from constants import EARTH_RADIUS, EARTH_ECCEN, ACCEL_GRAV, BANKING_ANGLE

def get_earth_radii(lat):
    """Returns meridional radius of curvature and the radius of curvature in the prime
    vertical, r_1 and r_2, respectively used for the flat earth approximation. r_1 and r_2
    are returned in a tuple, with r_1 first.
        
    input: lat is in radians
    output: (r_1, r_2) is in meters
    """
    
    r_1 = (EARTH_RADIUS * (1 - EARTH_ECCEN ** 2) /
           (1 - EARTH_ECCEN ** 2 * sin(lat) ** 2) ** (3 / 2))
    r_2 = EARTH_RADIUS / sqrt(1 - EARTH_ECCEN ** 2 * sin(lat) ** 2)
    
    return r_1, r_2

def _get_magnitude(*args):
    """Returns the distance given x and y coordinates or x, y, and z"""
    
    sum = 0
    
    for num in args:
        sum += num ** 2
    
    return sqrt(sum)

def _get_turning_radius(airspeed):
    """Returns the turning radius for the plane traveling at true airspeed 'airspeed'
    while banking.
    
    input: airspeed in meters per second
    output: turning radius in radians.
    """

    return airspeed ** 2 / ACCEL_GRAV / tan(BANKING_ANGLE)

def get_linear_distance(lat_1, lon_1, alt_1, lat_2, lon_2, alt_2):
    """Returns the distance between the two sets of coordinates using the flat earth
    approximation. (lat_1, lon_1, alt_1) is used as the reference point to approximate the
    distance. The output is a dictionary with the x, y, z component distances and the
    magnitude.
    
    input: lat_1, lon_1, lat_2, lon_2 in radians, alt_1 and alt_2 in meters
    output: dictionary with 'x', 'y', 'z', and 'mag' keys, distances in meters
    """
    
    e_radii = get_earth_radii(lat_1)
    
    x_dist = e_radii[1] * cos(lat_1) * (lon_2 - lon_1)
    y_dist = e_radii[0] * (lat_2 - lat_1)
    z_dist = alt_2 - alt_1
    
    mag = _get_magnitude(x_dist, y_dist, z_dist)
    
    return {'x': x_dist, 'y': y_dist, 'z': z_dist, 'mag': mag}

#TODO def get_circular_distance()

#TODO def get_distance()
