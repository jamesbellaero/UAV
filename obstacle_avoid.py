"""Handles the obstacle avoidance system for the UAV.

Uses the flat earth approximation to convert latitudes and longitudes into distances, see
http://williams.best.vwh.net/avform.htm#flat for details.

Note that latitudes and longitudes are expressed in radians and distances are in meters.
"""

from math import sin, cos, atan2, pi
from distance import get_earth_radii, get_linear_distance

def _get_waypoint(lat, lon, alt, bearing, radius):
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
    
    return _get_waypoint(lat, lon, alt, yaw - pi / 2, radius)
    
def get_right_waypoint(lat, lon, yaw, radius):
    """Returns the coordinate the plane would go to if it dodged dead right of an obstacle
    at (lat, lon) at a distance 'radius'. 'alt' is the altitude the plane should be at
    when it reaches this waypoint and 'yaw' is the yaw of the plane.
    
    input: lat, lon, yaw in radians, alt and radius in meters.
    output: dictionary with 'lat', 'lon', and 'alt' inside, lat and lon in radians, alt in
    meters.
    """

    return _get_waypoint(lat, lon, alt, yaw + pi / 2, radius)
    
def get_bearing(lat_1, lon_1, lat_2, lon_2):
    """Returns the bearing from (lat_1, lon_1) to (lat_2, lon_2) using the flat earth
    approximation.
    
    North: 0 rad, East: pi / 2 rad, South: pi rad, West: 3 * pi / 2 rad
    
    input: lat_1, lon_1, lat_2, lon_2 in radians
    output: bearing in radians
    """
    
    dist = get_linear_distance(lat_1, lon_1, 0, lat_2, lon_2, 0)
    
    return atan2(dist['x'], dist['y']) % (2 * pi)
