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

def get_distance(lat_1, lon_1, lat_2, lon_2):
	"""Returns the distance between the two pairs of coordinates using the flat earth
	approximation. (lat_1, lon_1) is used as the reference point to approximate the
	distance. The output is a dictionary with the x and y component distances.
	
	input: lat_1, lon_1, lat_2, lon_2 in radians
	output: dictionary with 'x' and 'y' keys, distances in meters
	"""

    e_radii = get_earth_radii(lat)
    
    x_dist = radius * sin(yaw - pi / 2)
    y_dist = radius * cos(yaw - pi / 2)
        
    wp_lat = y_dist / e_radii[0] + lat
    wp_lon = x_dist / e_radii[1] / cos(lat) + lon

def get_waypoint(lat, lon, bearing, radius):
    """Returns the coorinate at a distance 'radius' and at the bearing from an obstacle at
    (lat, lon).
    
    input: lat, lon, bearing in radians and radius in meters.
    output: dictionary with "lat" and "lon" inside, lat and lon in radians.
    """

    e_radii = get_earth_radii(lat)

    x_dist = radius * sin(bearing)
    y_dist = radius * cos(bearing)

    wp_lat = y_dist / e_radii[0] + lat
    wp_lon = x_dist / e_radii[1] / cos(lat) + lon

    return {'lat': wp_lat, 'lon': wp_lon}

def get_left_waypoint(lat, lon, yaw, radius):
	"""Returns the coordinate the plane would go to if it dodged dead left of an obstacle
	at (lat, lon) at a distance 'radius'.
	
	input: lat, lon, yaw in radians and radius in meters.
	output: dictionary with "lat" and "lon" inside, lat and lon in radians.
	"""
	
	return get_waypoint(lat, lon, yaw - pi / 2, radius)
            
def get_right_waypoint(lat, lon, yaw, radius):
    """Returns the coordinate the plane would go to if it dodged dead right of an obstacle
    at (lat, lon) at a distance 'radius'.
        
    input: lat, lon, yaw in radians and radius in meters.
    output: dictionary with "lat" and "lon" inside, lat and lon in radians.
    """
                        
    return get_waypoint(lat, lon, yaw + pi / 2, radius)

def get_bearing(lat_1, lon_1, lat_2, lon_2):
	"""Returns the bearing from (lat_1, lon_1) to (lat_2, lon_2) using the flat earth
	approximation.
	
	North: 0 rad, East: pi / 2 rad, South: pi rad, West: 3 * pi / 2 rad
	
	input: lat_1, lon_1, lat_2, lon_2 in radians
	output: bearing in radians
	"""
	
	dist = get_distance(lat_1, lon_1, lat_2, lon_2)
	
	return atan2(dist['x'], dist['y']) % (2 * pi)