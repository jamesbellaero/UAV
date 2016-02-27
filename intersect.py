from math import sqrt
from calc_distance import get_linear_distance, get_bearing
from constants import AVOID_DISTANCE_STAT, AVOID_DISTANCE_MOV

def do_obs_intersect(obs_1, obs_2):
    pass
    #dist = get_linear_distance(obs_1.wp, obs_2.wp)
    #TODO

def get_avoid_radius(obs, pass_alt):
    """Returns how far the plane must avoid obs if it passes obs at pass_alt. Zero is
    returned if obs does not need to be avoided.
    
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

def _can_travel_linear(wp_1, wp_2, obs):

    bearing = get_bearing(wp_1, wp_2)
    
    wp_dist = get_distance_plane(wp_1, wp_2, bearing)
    obs_dist = get_distance_plane(wp_1, obs.wp, bearing)

    pass_alt = wp_1.alt + obs_dist.y / float(wp_dist.y) * wp_dist.z
    avoid_radius = get_avoid_radius(obs, pass_alt)

    #TODO finish

# def _can_travel_circle(wp_1, radius, angle)

# def can_travel(wp_1, wp_2, airspeed)
