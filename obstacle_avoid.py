"""Handles the obstacle avoidance system for the UAV.

Uses the flat earth approximation to convert latitudes and longitudes into distances, see
http://williams.best.vwh.net/avform.htm#flat for details.

Note that latitudes and longitudes are expressed in radians and distances are in meters.
"""

from math import sin, cos, atan2, pi
from calc_distance import get_earth_radii
from tuples import Waypoint

def _get_waypoint(starting_wp, bearing, distance):
    """Returns the coordinate at a distance 'distance' and at the bearing from an obstacle
    at starting_wp with the plane going through the waypoint at altitude 'alt'.
    
    input: starting_wp, Waypoint namedtuple, lat and lon in radians, alt in meters
    output: Waypoint namedtuple, lat and lon in radians, alt in meters
    """
    
    e_radii = get_earth_radii(starting_wp.lat)
    
    x_dist = distance * sin(bearing)
    y_dist = distance * cos(bearing)

    wp_lat = y_dist / e_radii[0] + starting.wp.lat
    wp_lon = x_dist / e_radii[1] / cos(starting_wp.lat) + starting_wp.lon

    return Waypoint(lat = wp_lat, lon = wp_lon, alt = starting_wp.alt)

# Deprecated?
def get_left_waypoint(lat, lon, yaw, radius):
    """Returns the coordinate the plane would go to if it dodged dead left of an obstacle
    at (lat, lon) at a distance 'radius'. 'alt' is the altitude the plane should be at
    when it reaches this waypoint and 'yaw' is the yaw of the plane.
    
    input: lat, lon, yaw in radians, alt and radius in meters.
    output: dictionary with 'lat', 'lon', and 'alt' inside, lat and lon in radians, alt in
    meters.
    """
    
    return _get_waypoint(lat, lon, alt, yaw - pi / 2, radius)

# Deprecated?
def get_right_waypoint(lat, lon, yaw, radius):
    """Returns the coordinate the plane would go to if it dodged dead right of an obstacle
    at (lat, lon) at a distance 'radius'. 'alt' is the altitude the plane should be at
    when it reaches this waypoint and 'yaw' is the yaw of the plane.
    
    input: lat, lon, yaw in radians, alt and radius in meters.
    output: dictionary with 'lat', 'lon', and 'alt' inside, lat and lon in radians, alt in
    meters.
    """

    return _get_waypoint(lat, lon, alt, yaw + pi / 2, radius)
