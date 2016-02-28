"""Handles computing the distance between two waypoints, with some functions taking in
consideration turning to go to the next waypoint.

Note that distances are in meters and angles are in radians.
"""

from math import sin, cos, tan, sqrt, pi
from constants import EARTH_RADIUS, EARTH_ECCEN, ACCEL_GRAV, BANKING_ANGLE
from tuples import Distance

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

def get_magnitude(dist):
    """Returns the magnitude given a distance.
        
    input: dist, Distance namedtuple
    output: magnitude
    """

    return sqrt(dist.x ** 2 + dist.y ** 2 + dist.z ** 2)

def get_magnitude_xy(dist):
    """Returns the magnitude given a distance on only the xy plane.
        
    input: dist, Distance namedtuple
    output: magnitude
    """
    
    return sqrt(dist.x ** 2 + dist.y ** 2)

def get_turning_radius(airspeed):
    """Returns the turning radius for the plane traveling at true airspeed 'airspeed'
    while banking.
    
    input: airspeed in meters per second
    output: turning radius in radians.
    """

    return airspeed ** 2 / ACCEL_GRAV / tan(BANKING_ANGLE)

def get_bearing(wp_1, wp_2):
    """Returns the bearing from wp_1 to wp_2 using the flat earth approximation.
    
    North: 0 rad, East: pi / 2 rad, South: pi rad, West: 3 * pi / 2 rad
    
    input: wp_1 and wp_2, Waypoint namedtuple, lat and lon in radians, alt in meters
    output: bearing in radians
    """
    
    dist = get_linear_distance(wp_1, wp_2)
    
    return atan2(dist['x'], dist['y']) % (2 * pi)

def get_linear_distance(wp_1, wp_2):
    """Returns the distance between the two sets of coordinates using the flat earth
    approximation. wp_1 is used as the reference point to approximate the distance. The
    output is the Distance namedtuple.
    
    input: wp_1 and wp_2, Waypoint namedtuple, lat and lon in radians, alt in meters
    output: Distance namedtuple, x, y, and z in meters
    """
    
    e_radii = get_earth_radii(wp_1.lat)
    
    x_dist = e_radii[1] * cos(wp_1.lat) * (wp_2.lon - wp_1.lon)
    y_dist = e_radii[0] * (wp_2.lat - wp_1.lat)
    z_dist = wp_2.alt - wp_1.alt
    
    return Distance(x = x_dist, y = y_dist, z = z_dist)

def get_distance_plane(wp_plane, wp_2, bearing):
    """Returns the distance from the nose of the plane to a waypoint with a given bearing.
    The x coordinate is the distance to the left and right of the plane in the direction
    of the nose, the y coordinate is how far in front of or behind the plane, and the z
    coordinate is how far above or below the plane.
    
    input: wp_plane and wp_2, Waypoint namedtuple, lat and lon in radians, alt in meters,
        bearing in radians
    output: Distance namedtuple, x, y, and z in meters
    """
    
    dist = get_linear_distance(wp_plane, wp_2)

    i = dist.x * cos(bearing) - dist.y * sin(bearing)
    j = dist.x * sin(bearing) + dist.y * cos(bearing)
    k = dist.z

    return Distance(x = i, y = j, z = k)

#TODO def get_helix_distance(wp_1, radius, angle)

#TODO def get_distance()
