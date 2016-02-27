"""Names tuples so that waypoints, obstacles, and distances can have their information
represented by string. If the obstacle is a sphere, height = -1.
Ex: wp = Waypoint(lat = 5, lon = 2, alt = 40)
    obs = Obstacle(wp, height = -1, radius = 20)
    dist = Distance(x = 10, y = 1, z = 20)
"""

from collections import namedtuple

Waypoint = namedtuple('Waypoint', 'lat, lon, alt')

Obstacle = namedtuple('Obstacle', 'wp, height, radius')

Distance = namedtuple('Distance', 'x, y, z')
