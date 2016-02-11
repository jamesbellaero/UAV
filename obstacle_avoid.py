"""
Handles the obstacle avoidance system for the UAV.

Uses the flat earth approximation to convert latitudes and longitudes into distances, see
http://williams.best.vwh.net/avform.htm#flat for details.

Note that latitudes and longitudes are expressed in radians and distances are in meters.
"""

from math import sin, cos, atan2, sqrt, pi

def get_earth_radii(lat):
    """Returns meridional radius of curvature and the radius of curvature in the prime
    vertical, r_1 and r_2, respectively used for the flat earth approximation. r_1 and r_2
    are returned in a tuple, with r_1 first.
    
    input: lat is in radians
    output: (r_1, r_2) is in meters
    """
    
    a = 6378137
    f = 1 / 298.257223563
    e = f * (2 - f)
    
    r_1 = a * (1 - e) / (1 - e * sin(lat) ** 2) ** (3 / 2)
    r_2 = a / sqrt(1 - e * sin(lat) ** 2)
    
    return r_1, r_2

def get_magnitude(*args):
    """Returns the distance given x and y coordinates or x, y, and z"""
    
    sum = 0
    
    for num in args:
        sum += num ** 2
    
    return sqrt(sum)

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
    
    mag = get_magnitude(x_dist, y_dist, z_dist)
    
    return {'x': x_dist, 'y': y_dist, 'z': z_dist, 'mag': mag}

def get_waypoint(lat, lon, alt, bearing, radius):
    """Returns the coordinate at a distance 'radius' and at the bearing from an obstacle
    at (lat, lon) with the plane going through the waypoint at altitude 'alt'.
    
    input: lat, lon, bearing in radians, and alt and radius in meters.
    output: dictionary with 'lat', 'lon', and 'alt' inside, lat and lon in radians, alt in
    meters.
    """
    
    e_radii = get_earth_radii(lat)

    x_dist = radius * sin(bearing)
    y_dist = radius * cos(bearing)
    
    wp_lat = y_dist / e_radii[0] + lat
    wp_lon = x_dist / e_radii[1] / cos(lat) + lon
    
    return {'lat': wp_lat, 'lon': wp_lon, 'alt': alt}
    
def get_left_waypoint(lat, lon, yaw, radius):
    """Returns the coordinate the plane would go to if it dodged dead left of an obstacle
    at (lat, lon) at a distance 'radius'. 'alt' is the altitude the plane should be at
    when it reaches this waypoint and 'yaw' is the yaw of the plane.
    
    input: lat, lon, yaw in radians, alt and radius in meters.
    output: dictionary with 'lat', 'lon', and 'alt' inside, lat and lon in radians, alt in
    meters.
    """
    
    return get_waypoint(lat, lon, alt, yaw - pi / 2, radius)
    
def get_right_waypoint(lat, lon, yaw, radius):
    """Returns the coordinate the plane would go to if it dodged dead right of an obstacle
    at (lat, lon) at a distance 'radius'. 'alt' is the altitude the plane should be at
    when it reaches this waypoint and 'yaw' is the yaw of the plane.
    
    input: lat, lon, yaw in radians, alt and radius in meters.
    output: dictionary with 'lat', 'lon', and 'alt' inside, lat and lon in radians, alt in
    meters.
    """

    return get_waypoint(lat, lon, alt, yaw + pi / 2, radius)
    
def get_bearing(lat_1, lon_1, lat_2, lon_2):
    """Returns the bearing from (lat_1, lon_1) to (lat_2, lon_2) using the flat earth
    approximation.
    
    North: 0 rad, East: pi / 2 rad, South: pi rad, West: 3 * pi / 2 rad
    
    input: lat_1, lon_1, lat_2, lon_2 in radians
    output: bearing in radians
    """
    
    dist = get_linear_distance(lat_1, lon_1, 0, lat_2, lon_2, 0)
    
    return atan2(dist['x'], dist['y']) % (2 * pi)
