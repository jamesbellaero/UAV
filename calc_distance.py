"""Handles computing the distance between two waypoints, with some functions taking in
consideration turning to go to the next waypoint.

Uses the flat earth approximation to convert latitudes and longitudes into distances, see
http://williams.best.vwh.net/avform.htm#flat for details.

Note that distances are in meters and angles are in radians.
"""

from math import sin, cos, tan, atan2, sqrt, pi
from constants import EARTH_RADIUS, EARTH_ECCEN, ACCEL_GRAV, BANKING_ANGLE
from tuples import Distance, Waypoint

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
    output is a Distance namedtuple.
    
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

def get_turn(wp_plane, wp_2, bearing, airspeed):
    """Returns both the angle that the plane must turn and the distance relative to the
    plane of the point where the plane no longer turns. It is assumed that the plane turns
    in a circular path and then flies directly to wp_2.
    
    input: wp_plane and wp_2, Waypoint namedtuple, lat and lon in radians, alt in meters,
        bearing in radians, airspeed is meters per second
    output: tuple with angle in radians first and Distance namedtuple, x, y, and z in
        meters second
    """
    
    # Get the distance of wp_2 relative to the plane
    dist = get_distance_plane(wp_plane, wp_2, bearing)

    i = dist.x
    j = dist.y
    k = dist.z

    # Get the turning radius of the plane
    R = get_turning_radius(airspeed)
    
    # If the waypoint is to the left make the plane turn left
    if (i < 0):
        R = -R
        
    # If the plane cannot make a tight enough turn, turn the other way
    if ((i - R) ** 2 + j ** 2 < R ** 2):
            R = -R
    
    # Find a, b, and c, the distances relative to the plane of the point where the plane
    # no longer turns
    
    # Try to find a
    try:
        a = (R * i ** 2 - R ** 2 * i + R * j ** 2 - R * j * sqrt(i ** 2 - 2 * R * i + j
                ** 2)) / double(R ** 2 - 2 * R * i + i ** 2 + j ** 2)
    
    # Find a and b due to floating point errors for when the plane doesn't turn at all or
    # when the plane turns pi radians left or right
    except (ZeroDivisionError, ValueError):
        if (abs(i) < abs(R)):
            a = 0
        else:
            a = 2 * R

        b = 0

    # Otherwise, find b
    else:
        b = sqrt(R ** 2 - (a - R) ** 2)
        
        if ((j < 0 and abs(i) < 2 * abs(R)) or i / double(R) < 0):
            B = -B

    # Find how what angle the plane must turn, will be positive for both turning left and
    # right
    angle = (atan2(B, abs(R) / R * (R - A))) % (2 * pi)

    # Find the distances in the xy plane of the circular and linear path
    circ_dist_xy = abs(R) * angle
    lin_dist_xy = sqrt((i - a) ** 2 + (j - b) ** 2)

    # Try to find c as a ratio of the circular distance to the total distance times k
    try:
        c = circ_dist_xy / double(circ_dist_xy + lin_dist_xy) * k

    # c is zero due to floating point errors if both wp_plane and wp_2 are extremely close
    except ZeroDivisionError:
        c = 0

    # Return both and angle the plane must turn and the distance relative to the plane of
    # the point where the plane no longer turns in a tuple
    return (angle, Distance(x = a, y = b, z = c))

#TODO def get_distance()

def get_waypoint(wp_1, dist):
    """Returns the waypoint at dist from wp_1 using the using the flat earth
    approximation. wp_1 is used as the reference point to approximate the waypoint. The
    output is a Waypoint namedtuple.
    
    input: wp_1, Waypoint namedtuple, lat and lon in radians, alt in meters, dist,
        Distance namedtuple, x, y, and z in meters
    output: Waypoint namedtuple, lat and lon in radians, alt in meters
    """
    
    e_radii = get_earth_radii(wp_1.lat)

    wp_lat = dist.y / e_radii[0] + wp_1.lat
    wp_lon = dist.x / e_radii[1] / cos(wp_1.lat) + wp_1.lon
    wp_alt = wp_1.alt + dist.alt
    
    return Waypoint(lat = wp_lat, lon = wp_lon, alt = wp_alt)
