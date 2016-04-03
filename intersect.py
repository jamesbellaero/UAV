from math import sqrt
from calc_distance import (get_linear_distance, get_bearing, get_magnitude_xy,
        get_turn)
from constants import AVOID_DISTANCE_STAT, AVOID_DISTANCE_MOV

def do_obs_overlap(obs_1, obs_2, pass_alt):
    """Returns whether or not the area in which two obstacles overlap at pass_alt. If the
    two areas are tangent at the point it does not count as overlapping.
    
    input: obs and pass_alt, obs_1 and obs_2 are Obstacle namedtuples, lat, lon in
        radians, alt, height, radius, and pass_alt in meters
    output: True or False
    """
    
    radius_1 = get_avoid_radius(obs_1, pass_alt)
    radius_2 = get_avoid_radius(obs_2, pass_alt)

    if radius_1 == 0 or radius_2 == 0:
        return False

    dist = get_linear_distance(obs_1.wp, obs_2.wp)
    dist_xy = get_magnitude_xy(dist)

    return radius_1 + radius_2 > dist_xy

def get_avoid_radius(obs, pass_alt):
    """Returns how far the plane must avoid obs if it passes obs at pass_alt. Zero is
    returned if obs does not need to be avoided at pass_alt.
    
    input: obs and pass_alt, obs is Obstacle namedtuple, lat, lon in radians, alt, height,
        radius, and pass_alt in meters
    output: radius in meters
    """

    # If obs is a cylinder
    if (obs.height != -1):
        
        # If pass_alt is not above or below obs
        if (abs(pass_alt - obs.wp.alt) <= obs.height / 2.0):
            return obs.radius + AVOID_DISTANCE_STAT
        
        # If pass_alt is a little above or below obs
        elif (abs(pass_alt - obs.wp.alt) < obs.height / 2.0 + AVOID_DISTANCE_STAT):
            return obs.radius + sqrt(AVOID_DISTANCE_STAT ** 2 - (abs(pass_alt -
                    obs.wp.alt) - obs.height / 2.0) ** 2)

    # If obs is a sphere
    elif (abs(pass_alt - obs.wp.alt) < AVOID_DISTANCE_MOV + obs.radius):
        return sqrt((AVOID_DISTANCE_MOV + obs.radius) ** 2 - (pass_alt - obs.wp.alt) ** 2)
    
    # Return zero if pass_alt is far above or below obs
    return 0

def _is_obs_in_way_linear(wp_1, wp_2, obs):
    """TODO
    """
    
    ###############################
    #                             #
    # FIX RADIUS AT WP_1 and WP_2 #
    #                             #
    ###############################
    
    # Find the distances of wp_2 and obs_1 relative to wp_1 with the plane at that bearing
    bearing = get_bearing(wp_1, wp_2)
    
    wp_dist = get_distance_plane(wp_1, wp_2, bearing)
    obs_dist = get_distance_plane(wp_1, obs.wp, bearing)

    # Find the radius obs must be avoided at
    pass_alt = wp_1.alt + obs_dist.y / float(wp_dist.y) * wp_dist.z
    avoid_radius = get_avoid_radius(obs, pass_alt)
    
    # If wp_1 is within obs return True
    if (sqrt(obs_dist.x ** 2 + obs_dist.y ** 2) < avoid_radius):
        return False

    # If obs is behind wp_1 return False
    if (obs_dist.y < 0):
        return False

    # If obs is not farther ahead than wp_2
    if (obs_dist.y > wp_dist.y):
        
        # If obs is not far enough to the left or right return True
        return obs_dist.x < avoid_radius

    # Otherwise return True if wp_2 is within obs
    obs_dist_2 = get_distance_plane(wp_2, obs.wp, bearing)

    return sqrt(obs_dist_2.x ** 2 + obs_dist_2.y ** 2) < avoid_radius

def _is_obs_in_way_helix(wp_1, radius, angle):

def can_travel(wp_plane, wp_2, bearing, airspeed, obs_list):
    turn = get_turn(wp_plane, wp_2, bearing, airspeed)
    
    angle = turn[0]
    dist = turn[1]
    
    for obs in obs_list:
        pass # TODO
    
    return true
