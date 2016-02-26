"""Contains a bunch of constants in one place for the obstacle avoidance code."""

# Constants for finding the turning radius. BANKING_ANGLE is in radians and ACCEL_GRAV is
# in ms^-2.
BANKING_ANGLE = 0.5235987756
ACCEL_GRAV = 9.80665

# Distance from stationary and moving obstacles that the plane should try to avoid in
# meters.
AVOID_DISTANCE_STAT = 15
AVOID_DISTANCE_MOV = 30

# Constants for the flat Earth approximation. EARTH_RADIUS is in meters and EARTH_ECCEN
# is dimensionless.
EARTH_RADIUS = 6378137
EARTH_ECCEN = 0.0818191908