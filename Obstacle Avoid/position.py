from math import sin, cos, atan2, pi

from dronekit import LocationGlobalRelative

from unit_conversions import deg_to_rad, rad_to_deg

class Distance(object):

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

    def get_magnitude(self):
    
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def get_magnitude_xy(self):
        
        return sqrt(self.x ** 2 + self.y ** 2)

    def get_transform(self, angle):
        
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        z = self.z

        return Distance(x, y, z)

class Location(object):
    
    EARTH_RADIUS = 6378137
    EARTH_ECCEN = 0.0818191908
    
    def __init__(self, lon, lat, alt):
        
        self.lon = lon
        self.lat = lat
        self.alt = alt

    def _get_earth_radii(self):
    
        r_1 = (EARTH_RADIUS * (1 - EARTH_RADIUS ** 2) /
               (1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2) ** (3 / 2))
        r_2 = EARTH_RADIUS / sqrt(1 - EARTH_ECCEN ** 2 * sin(self.lat) ** 2)
           
        return (r_1, r_2)

    def get_distance(self, loc, angle=0):
    
        e_radii = _get_earth_radii()
        
        x = e_radii[1] * cos(self.lat) * (loc.lon - self.lon)
        y = e_radii[0] * (loc.lat - self.lat)
        z = loc.alt - self.alt
        
        dist = Distance(x, y, z)
        
        return dist.get_transform(angle)

    def get_location(self, dist):
        
        e_radii = _get_earth_radii()
    
        lat = dist.y / e_radii[0] + self.lat
        lon = dist.x / e_radii[1] / cos(self.lat) + self.lon
        alt = self.alt + dist.alt
    
        return Location(lat, lon, alt)
    
    def get_bearing(self, loc):
    
        dist = get_distance(loc)
    
        return atan2(dist.x, dist.y) % (2 * pi)
    
    @staticmethod
    def from_dronekit_location(dk_loc):
        
        lon = deg_to_rad(dk_loc.lon)
        lat = deg_to_rad(dk_loc.lat)
        alt = dk_loc.alt

        return Location(lon, lat, alt)

    def to_dronekit_location(self):

        lon = rad_to_deg(self.lon)
        lat = rad_to_deg(self.lat)
        alt = self.alt

        return LocationGlobalRelative(lon, lat, alt)
